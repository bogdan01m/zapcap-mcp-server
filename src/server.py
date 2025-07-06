# server.py
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import httpx
import os

# Create an MCP server
mcp = FastMCP("zapcap-mcp-server")

def get_api_key() -> str:
    api_key = os.getenv("ZAPCAP_API_KEY")
    if not api_key:
        raise ValueError("ZAPCAP_API_KEY environment variable is required")
    return api_key

class UploadVideo(BaseModel):
    file_path: str = Field(description="Path to video file")

class UploadVideoByUrl(BaseModel):
    url: str = Field(description="URL to video file")

class CreateTask(BaseModel):
    video_id: str = Field(description="Video ID from upload")
    template_id: str = Field(description="Template ID")
    auto_approve: bool = Field(default=True, description="Auto approve the task")
    language: str = Field(default="en", description="Language code")
    enable_broll: bool = Field(default=False, description="Enable B-roll (requires video > 8-10 seconds)")
    broll_percent: int = Field(default=30, description="B-roll percentage (0-100)")
    # Subtitle options
    emoji: bool = Field(default=True, description="Enable emoji in subtitles")
    emoji_animation: bool = Field(default=True, description="Enable emoji animation")
    emphasize_keywords: bool = Field(default=True, description="Emphasize keywords")
    animation: bool = Field(default=True, description="Enable subtitle animation")
    punctuation: bool = Field(default=True, description="Include punctuation")
    display_words: int = Field(default=1, description="Number of words to display")
    # Style options
    position_top: int = Field(default=60, description="Subtitle position from top")
    font_uppercase: bool = Field(default=True, description="Use uppercase font")
    font_size: int = Field(default=30, description="Font size")
    font_weight: int = Field(default=900, description="Font weight")
    font_color: str = Field(default="#ffffff", description="Font color")
    font_shadow: str = Field(default="l", description="Font shadow (s/m/l)")
    stroke: str = Field(default="s", description="Stroke style")
    stroke_color: str = Field(default="#000000", description="Stroke color")
    # Highlight colors
    highlight_color_1: str = Field(default="#2bf82a", description="First highlight color")
    highlight_color_2: str = Field(default="#fdfa14", description="Second highlight color")
    highlight_color_3: str = Field(default="#f01916", description="Third highlight color")

class MonitorTask(BaseModel):
    video_id: str = Field(description="Video ID")
    task_id: str = Field(description="Task ID")

@mcp.tool(description="Upload video file to ZapCap")
def zapcap_mcp_upload_video(request: UploadVideo) -> Dict[str, Any]:
    headers = {"x-api-key": get_api_key()}
    
    with open(request.file_path, 'rb') as f:
        files = {'file': f}
        with httpx.Client() as client:
            response = client.post(
                "https://api.zapcap.ai/videos",
                headers=headers,
                files=files
            )
    
    response.raise_for_status()
    return response.json()

@mcp.tool(description="Upload video by URL to ZapCap")
def zapcap_mcp_upload_video_by_url(request: UploadVideoByUrl) -> Dict[str, Any]:
    headers = {
        "x-api-key": get_api_key(),
        "Content-Type": "application/json"
    }
    
    data = {"url": request.url}
    with httpx.Client() as client:
        response = client.post(
            "https://api.zapcap.ai/videos/url",
            headers=headers,
            json=data
        )
    
    response.raise_for_status()
    return response.json()

@mcp.tool(description="Get available templates from ZapCap")
def zapcap_mcp_get_templates() -> Dict[str, Any]:
    return {
        "result": {
            "templates_url": "https://platform.zapcap.ai/dashboard/templates",
            "message": "Templates are available in the ZapCap dashboard with preview images",
            "instructions": "1. Visit the dashboard URL above\n2. Browse templates with visual previews\n3. Copy the template ID for use in create_task",
            "note": "Templates include various caption styles, animations, and layouts"
        }
    }

@mcp.tool(description="Create video processing task with full customization options")
def zapcap_mcp_create_task(request: CreateTask) -> Dict[str, Any]:
    headers = {
        "x-api-key": get_api_key(),
        "Content-Type": "application/json"
    }
    
    data = {
        "templateId": request.template_id,
        "autoApprove": request.auto_approve,
        "language": request.language,
        "renderOptions": {
            "subsOptions": {
                "emoji": request.emoji,
                "emojiAnimation": request.emoji_animation,
                "emphasizeKeywords": request.emphasize_keywords,
                "animation": request.animation,
                "punctuation": request.punctuation,
                "displayWords": request.display_words
            },
            "styleOptions": {
                "top": request.position_top,
                "fontUppercase": request.font_uppercase,
                "fontSize": request.font_size,
                "fontWeight": request.font_weight,
                "fontColor": request.font_color,
                "fontShadow": request.font_shadow,
                "stroke": request.stroke,
                "strokeColor": request.stroke_color
            },
            "highlightOptions": {
                "randomColourOne": request.highlight_color_1,
                "randomColourTwo": request.highlight_color_2,
                "randomColourThree": request.highlight_color_3
            }
        }
    }
    
    # Add B-roll settings only if enabled
    if request.enable_broll:
        data["transcribeSettings"] = {
            "broll": {
                "brollPercent": request.broll_percent
            }
        }
    
    with httpx.Client() as client:
        response = client.post(
            f"https://api.zapcap.ai/videos/{request.video_id}/task",
            headers=headers,
            json=data
        )
    
    response.raise_for_status()
    return response.json()

@mcp.tool(description="Monitor task progress")
def zapcap_mcp_monitor_task(request: MonitorTask) -> Dict[str, Any]:
    headers = {"x-api-key": get_api_key()}
    
    with httpx.Client() as client:
        response = client.get(
            f"https://api.zapcap.ai/videos/{request.video_id}/task/{request.task_id}",
            headers=headers
        )
    
    response.raise_for_status()
    return response.json()

def main():
    """Entry point for the MCP server."""
    mcp.run()

