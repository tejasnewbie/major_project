"""Docker-based code execution service."""
import docker
import asyncio
import tempfile
import os
from typing import Dict, Any, Optional
from dataclasses import dataclass
import logging
from app.core.config import get_settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class ExecutionResult:
    """Result of code execution."""
    stdout: str
    stderr: str
    exit_code: int
    execution_time: float
    error: Optional[str] = None


class CodeExecutor:
    """Safe code execution using Docker containers."""
    
    def __init__(self):
        self.settings = get_settings()
        self.image_name = "council-sandbox"
        self.client = None
        self.docker_available = False
        
        try:
            # Try to connect to Docker
            self.client = docker.from_env()
            # Test connection
            self.client.ping()
            self.docker_available = True
            logger.info("Docker connection successful")
            self._ensure_image_exists()
        except Exception as e:
            logger.warning(f"Docker not available: {e}")
            logger.warning("Code execution will use local Python (less secure)")
            self.docker_available = False
    
    def _ensure_image_exists(self):
        """Build the sandbox image if it doesn't exist."""
        if not self.docker_available:
            return
            
        try:
            self.client.images.get(self.image_name)
            logger.info(f"Using existing Docker image: {self.image_name}")
        except docker.errors.ImageNotFound:
            logger.info(f"Building Docker image: {self.image_name}")
            try:
                # Build from the docker-sandbox directory
                dockerfile_path = os.path.join(
                    os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
                    "docker-sandbox"
                )
                self.client.images.build(
                    path=dockerfile_path,
                    tag=self.image_name,
                    rm=True
                )
                logger.info("Docker image built successfully")
            except Exception as e:
                logger.error(f"Failed to build Docker image: {e}")
                self.docker_available = False
    
    async def execute(
        self, 
        code: str, 
        timeout: Optional[int] = None,
        test_cases: Optional[list] = None
    ) -> ExecutionResult:
        """
        Execute Python code in a Docker container (or local fallback).
        
        Args:
            code: Python code to execute
            timeout: Max execution time in seconds
            test_cases: Optional list of test inputs to run
        
        Returns:
            ExecutionResult with output and metadata
        """
        timeout = timeout or self.settings.docker_timeout
        
        # If test cases provided, wrap code to run them
        if test_cases:
            code = self._wrap_with_tests(code, test_cases)
        
        # Use Docker if available, otherwise local execution
        if self.docker_available:
            return await self._execute_docker(code, timeout)
        else:
            return await self._execute_local(code, timeout)
    
    async def _execute_docker(self, code: str, timeout: int) -> ExecutionResult:
        """Execute code in Docker container."""
        try:
            # Create temporary file with code
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            # Run in Docker container
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._run_container,
                temp_file,
                timeout
            )
            
            # Cleanup
            os.unlink(temp_file)
            
            return result
            
        except Exception as e:
            logger.error(f"Docker execution error: {e}")
            # Fallback to local execution
            return await self._execute_local(code, timeout)
    
    async def _execute_local(self, code: str, timeout: int) -> ExecutionResult:
        """Execute code locally (fallback when Docker unavailable)."""
        import time
        import subprocess
        
        start_time = time.time()
        
        try:
            # Create temp file
            with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
                f.write(code)
                temp_file = f.name
            
            import sys
            # Run with timeout using subprocess
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                lambda: subprocess.run(
                    [sys.executable, temp_file],
                    capture_output=True,
                    text=True,
                    timeout=timeout
                )
            )
            
            os.unlink(temp_file)
            
            return ExecutionResult(
                stdout=result.stdout[:self.settings.max_output_length],
                stderr=result.stderr[:self.settings.max_output_length],
                exit_code=result.returncode,
                execution_time=time.time() - start_time
            )
            
        except subprocess.TimeoutExpired:
            return ExecutionResult(
                stdout="",
                stderr="Execution timed out",
                exit_code=-1,
                execution_time=time.time() - start_time,
                error=f"Timeout after {timeout}s"
            )
        except Exception as e:
            return ExecutionResult(
                stdout="",
                stderr="",
                exit_code=-1,
                execution_time=time.time() - start_time,
                error=str(e)
            )
    
    def _run_container(
        self, 
        code_file: str, 
        timeout: int
    ) -> ExecutionResult:
        """Run Docker container with code file."""
        import time
        
        start_time = time.time()
        
        try:
            container = self.client.containers.run(
                image=self.image_name,
                command=["python", "/app/code.py"],
                volumes={code_file: {'bind': '/app/code.py', 'mode': 'ro'}},
                mem_limit='512m',
                cpu_quota=50000,  # 0.5 CPU
                network_mode='none',
                read_only=True,
                detach=True,
                stderr=True,
                stdout=True
            )
            
            # Wait for container to finish
            try:
                result = container.wait(timeout=timeout)
                logs = container.logs().decode('utf-8', errors='replace')
                
                # Split stdout and stderr (Docker combines them)
                stdout = logs
                stderr = ""
                
                container.remove(force=True)
                
                return ExecutionResult(
                    stdout=stdout[:self.settings.max_output_length],
                    stderr=stderr[:self.settings.max_output_length],
                    exit_code=result['StatusCode'],
                    execution_time=time.time() - start_time
                )
                
            except Exception as e:
                # Timeout or other error
                container.kill()
                container.remove(force=True)
                return ExecutionResult(
                    stdout="",
                    stderr="",
                    exit_code=-1,
                    execution_time=time.time() - start_time,
                    error=f"Execution timeout or error: {e}"
                )
                
        except Exception as e:
            return ExecutionResult(
                stdout="",
                stderr="",
                exit_code=-1,
                execution_time=time.time() - start_time,
                error=str(e)
            )
    
    def _wrap_with_tests(self, code: str, test_cases: list) -> str:
        """Wrap user code with test case execution."""
        test_code = "\n\n# Test cases execution\n"
        test_code += "if __name__ == '__main__':\n"
        test_code += "    print('\\n' + '='*50)\n"
        test_code += "    print('RUNNING TEST CASES')\n"
        test_code += "    print('='*50)\n"
        
        for i, test in enumerate(test_cases, 1):
            if isinstance(test, dict):
                input_val = repr(test.get('input', ''))
                expected = repr(test.get('expected', ''))
                test_code += f"    print(f'Test {i}: Input = {{{input_val}}}')\n"
                test_code += f"    try:\n"
                test_code += f"        result = solution({input_val})\n"
                test_code += f"        passed = result == {expected}\n"
                test_code += f"        print(f'  Expected: {{{expected}}}')\n"
                test_code += f"        print(f'  Got: {{result}}')\n"
                test_code += f"        print(f'  Status: {{\"PASS\" if passed else \"FAIL\"}}')\n"
                test_code += f"    except Exception as e:\n"
                test_code += f"        print(f'  ERROR: {{e}}')\n"
            else:
                test_code += f"    print(f'Test {i}: {test}')\n"
        
        return code + test_code
    
    async def validate_syntax(self, code: str) -> tuple[bool, Optional[str]]:
        """Check if Python code has valid syntax without executing."""
        try:
            import ast
            ast.parse(code)
            return True, None
        except SyntaxError as e:
            return False, f"Syntax Error at line {e.lineno}: {e.msg}"
        except Exception as e:
            return False, str(e)
    
    def is_docker_available(self) -> bool:
        """Check if Docker is available for code execution."""
        return self.docker_available


# Singleton instance
_executor: Optional[CodeExecutor] = None


def get_executor() -> CodeExecutor:
    """Get or create CodeExecutor singleton."""
    global _executor
    if _executor is None:
        _executor = CodeExecutor()
    return _executor
