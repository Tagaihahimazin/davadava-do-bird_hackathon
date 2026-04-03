"""davadava - Voice-controlled DJ MCP Server.

VoiceOS からの音声コマンドで Spotify を操作し、
タスク・モチベーション・ドライブの目的地に応じた曲を推薦・再生する。
"""

from mcp.server.fastmcp import FastMCP

from spotify import (
    play,
    pause,
    toggle,
    next_track,
    prev_track,
    play_uri,
    play_playlist,
    current_track_summary,
    set_volume,
    get_volume,
    fade_volume,
    seek,
    set_shuffle,
    set_repeat,
    set_system_volume,
)
from recommender import (
    recommend_drive_music,
    recommend_task_music,
    recommend_for_motivation,
)

mcp = FastMCP("davadava-dj")


# =========================================================================
# Basic Playback Controls
# =========================================================================

@mcp.tool()
def resume_playback() -> str:
    """Resume playing music. Use when asked to play or continue music."""
    return play()


@mcp.tool()
def pause_playback() -> str:
    """Pause the currently playing music."""
    return pause()


@mcp.tool()
def toggle_play_pause() -> str:
    """Toggle between play and pause."""
    return toggle()


@mcp.tool()
def next_song() -> str:
    """Skip to the next song."""
    return next_track()


@mcp.tool()
def previous_song() -> str:
    """Go back to the previous song."""
    return prev_track()


@mcp.tool()
def now_playing() -> str:
    """Get information about the currently playing song, including title, artist, and album."""
    return current_track_summary()


# =========================================================================
# Volume & Playback Settings
# =========================================================================

@mcp.tool()
def change_volume(level: int) -> str:
    """Set the music volume. Level is 0 to 100."""
    return set_volume(level)


@mcp.tool()
def check_volume() -> str:
    """Check the current volume level."""
    return f"Current volume: {get_volume()}"


@mcp.tool()
def smooth_fade(target_volume: int) -> str:
    """Smoothly fade the volume to a target level (0-100). Good for transitions."""
    return fade_volume(target_volume)


@mcp.tool()
def jump_to_position(seconds: float) -> str:
    """Jump to a specific position in the current song (in seconds)."""
    return seek(seconds)


@mcp.tool()
def shuffle_on() -> str:
    """Turn on shuffle mode to randomize playback order."""
    set_shuffle(True)
    return "Shuffle is now ON"


@mcp.tool()
def shuffle_off() -> str:
    """Turn off shuffle mode."""
    set_shuffle(False)
    return "Shuffle is now OFF"


@mcp.tool()
def repeat_on() -> str:
    """Turn on repeat mode."""
    set_repeat(True)
    return "Repeat is now ON"


@mcp.tool()
def repeat_off() -> str:
    """Turn off repeat mode."""
    set_repeat(False)
    return "Repeat is now OFF"


@mcp.tool()
def change_system_volume(level: int) -> str:
    """Set the Mac system volume (0-100). Different from Spotify volume."""
    return set_system_volume(level)


# =========================================================================
# Smart Recommendations - Driving
# =========================================================================

@mcp.tool()
def drive_music(destination: str, mood: str = "") -> str:
    """Recommend and play music for driving based on destination.

    Destination examples: beach, mountain, city, highway, countryside, night_drive, date.
    Mood examples: high, low, neutral, stressed, excited.

    Use this when the user is driving or about to drive somewhere.
    """
    rec = recommend_drive_music(destination, mood)
    result = play_playlist(rec.playlist_uri)
    return f"{rec.description} ({rec.genre})\n{result}"


@mcp.tool()
def beach_drive_music() -> str:
    """Play upbeat beach/summer music for a drive to the beach or coast."""
    return drive_music("beach", "high")


@mcp.tool()
def night_drive_music() -> str:
    """Play chill, atmospheric music for driving at night."""
    return drive_music("night_drive")


@mcp.tool()
def highway_drive_music() -> str:
    """Play energetic music for highway/freeway driving."""
    return drive_music("highway", "excited")


# =========================================================================
# Smart Recommendations - Task & Motivation
# =========================================================================

@mcp.tool()
def task_music(task: str, motivation: str = "") -> str:
    """Recommend and play music suited to a specific task.

    Task examples: focus, exercise, relax, creative, meeting.
    Motivation examples: high, low, neutral, stressed, excited.

    Use this when the user wants music for working or an activity.
    """
    rec = recommend_task_music(task, motivation)
    result = play_playlist(rec.playlist_uri)
    return f"{rec.description} ({rec.genre})\n{result}"


@mcp.tool()
def focus_music() -> str:
    """Play calm, instrumental music for focused work or studying."""
    return task_music("focus")


@mcp.tool()
def workout_music() -> str:
    """Play high-energy music for exercising or working out."""
    return task_music("exercise", "high")


@mcp.tool()
def relax_music() -> str:
    """Play soothing music for relaxation or winding down."""
    return task_music("relax", "low")


@mcp.tool()
def creative_music() -> str:
    """Play inspiring music for creative work like design, writing, or brainstorming."""
    return task_music("creative")


# =========================================================================
# Mood-based
# =========================================================================

@mcp.tool()
def mood_music(mood: str) -> str:
    """Play music matching your current mood.

    Mood examples: high, low, neutral, stressed, excited.
    """
    rec = recommend_for_motivation(mood)
    result = play_playlist(rec.playlist_uri)
    return f"{rec.description} ({rec.genre})\n{result}"


@mcp.tool()
def cheer_me_up() -> str:
    """Play uplifting music to boost your mood when you're feeling down."""
    return mood_music("low")


@mcp.tool()
def hype_music() -> str:
    """Play hype/exciting music to match or boost high energy."""
    return mood_music("excited")


# =========================================================================
# Direct Play
# =========================================================================

@mcp.tool()
def play_spotify_uri(uri: str) -> str:
    """Play a specific Spotify URI directly.

    Examples:
      spotify:track:6rqhFgbbKwnb9MLmUQDhG6
      spotify:playlist:37i9dQZF1DXcBWIGoYBM5M
    """
    return play_uri(uri)


# =========================================================================
# Entry point
# =========================================================================

if __name__ == "__main__":
    mcp.run(transport="stdio")
