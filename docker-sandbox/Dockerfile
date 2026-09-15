# Python sandbox for safe code execution
FROM python:3.11-slim

# Create non-root user for security
RUN useradd -m -u 1000 sandbox && \
    mkdir -p /app && \
    chown sandbox:sandbox /app

# Install only essential packages (no network, no file system access)
RUN pip install --no-cache-dir numpy

# Set working directory
WORKDIR /app

# Switch to non-root user
USER sandbox

# Default command runs Python from stdin
CMD ["python", "-"]
