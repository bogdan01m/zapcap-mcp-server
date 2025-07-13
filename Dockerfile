# Use Python 3.13 slim image as base
FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install uv package manager
RUN pip install uv

# Copy dependency files first for better caching
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen

# Copy source code
COPY src/ ./src/

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash zapcap && \
    chown -R zapcap:zapcap /app

USER zapcap

# Set environment variable for Python path
ENV PYTHONPATH=/app/src

# Run the MCP server via STDIO (default MCP transport)
CMD ["uv", "run", "zapcap-mcp-server"]