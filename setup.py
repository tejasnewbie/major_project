"""Setup script for Council of Frontiers."""
from setuptools import setup, find_packages

setup(
    name="council-of-frontiers",
    version="1.0.0",
    packages=find_packages(where="backend"),
    package_dir={"": "backend"},
    install_requires=[
        "fastapi==0.109.0",
        "uvicorn[standard]==0.27.0",
        "websockets==12.0",
        "pydantic==2.5.0",
        "pydantic-settings==2.1.0",
        "httpx==0.26.0",
        "aiohttp==3.9.0",
        "python-dotenv==1.0.0",
        "docker==7.0.0",
        "numpy==1.26.0",
        "scikit-learn==1.4.0",
    ],
    python_requires=">=3.9",
)
