# ZapCap MCP Server

## Overview
This is an unofficial MCP (Model Context Protocol) server implementation for ZapCap.ai - a video processing and caption generation service. The server provides tools for uploading videos, creating processing tasks, and monitoring their progress through the ZapCap API.

## Project Structure
```
zapcap-mcp-server/
├── src/
│   └── server.py          # Main MCP server implementation
├── main.py                # Entry point (placeholder)
├── pyproject.toml         # Project configuration and dependencies
├── README.md              # Basic project documentation
└── uv.lock               # Lock file for uv package manager
```

## Package Management
This project uses **uv** as the package manager instead of pip. All dependencies are managed through `pyproject.toml` and locked in `uv.lock`.

## Architecture
The server is built using the FastMCP framework and provides the following tools:

### Available Tools
1. **zapcap_mcp_upload_video** - Upload video files to ZapCap
2. **zapcap_mcp_upload_video_by_url** - Upload videos by URL
3. **zapcap_mcp_get_templates** - Get available processing templates
4. **zapcap_mcp_create_task** - Create video processing tasks with full customization
5. **zapcap_mcp_monitor_task** - Monitor task progress

### Dependencies
- `mcp[cli]>=1.10.1` - MCP server framework
- `httpx>=0.28.1` - HTTP client for API requests
- `pydantic>=2.11.7` - Data validation and serialization

## Configuration
The server requires the `ZAPCAP_API_KEY` environment variable to be set for authentication with the ZapCap API.

## API Integration
The server integrates with the ZapCap API endpoints:
- `https://api.zapcap.ai/videos` - Video upload
- `https://api.zapcap.ai/videos/url` - Upload by URL
- `https://api.zapcap.ai/videos/{video_id}/task` - Task creation
- `https://api.zapcap.ai/videos/{video_id}/task/{task_id}` - Task monitoring

## Data Models
The server defines several Pydantic models for request validation:
- `UploadVideo` - File path for video upload
- `UploadVideoByUrl` - URL for video upload
- `CreateTask` - Task creation parameters with full customization options
- `MonitorTask` - Task monitoring parameters

## Error Handling
The server includes basic error handling with `response.raise_for_status()` for HTTP errors and environment variable validation for API keys.

## Testing
Testing infrastructure needs to be implemented. Consider using:
- pytest for test framework
- httpx-mock or responses for mocking HTTP requests
- pytest-asyncio for async testing if needed

## Development Commands
Since this project uses uv:
- `uv sync` - Install dependencies
- `uv run python main.py` - Run the application
- `uv add <package>` - Add new dependencies
- `uv run pytest` - Run tests (when implemented)