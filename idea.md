DJのアプリを作りたいです。MCPで作りたいです。

import subprocess
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("spotify")

def osascript(cmd: str) -> str:
    result = subprocess.run(
        ["osascript", "-e", f'tell application "Spotify" to {cmd}'],
        capture_output=True, text=True,
    )
    return result.stdout.strip() or "Done"

@mcp.tool()
def play() -> str:
    """Resume Spotify playback."""
    return osascript("play")

@mcp.tool()
def pause() -> str:
    """Pause Spotify playback."""
    return osascript("pause")

@mcp.tool()
def skip_track() -> str:
    """Skip to the next track."""
    return osascript("next track")

@mcp.tool()
def current_track() -> str:
    """Get the currently playing track name and artist."""
    name = osascript("name of current track")
    artist = osascript("artist of current track")
    return f"{name} by {artist}"

if __name__ == "__main__":
    mcp.run(transport="stdio")

以上のコードをうまく組み込んでいい感じにしてください。