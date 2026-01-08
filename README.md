# NetEase Music MCP Server (Pro)

An advanced Model Context Protocol (MCP) server for controlling NetEase Cloud Music on macOS using the Open API.

## ✨ Features

*   **🎧 Intelligent Playback**: Auto-play songs and playlists in the desktop app via URL Scheme.
*   **🔓 Seamless Login**: QR Code login support with persistent session management.
*   **📅 Daily Recommendations**: Access your personalized "Daily Recommend" songs instantly.
*   **❤️ User Playlists**: Full access to your created and favorited playlists (including "Red Heart" list).
*   **🚀 High Performance**: Built with `fastmcp` and `pyncm`, significantly faster and more stable than Selenium-based automation.

## 🛠️ Tools

This server exposes the following tools to the AI Agent:

1.  **`netease_login`**: Initiates the QR code login flow.
2.  **`netease_status`**: Checks current login status and user profile.
3.  **`netease_get_daily_recommend`**: Retrieves the list of today's recommended songs.
4.  **`netease_my_playlists`**: Lists all user playlists (created & subscribed).
5.  **`netease_search`**: Searches for songs by keyword.
6.  **`netease_play`**: Plays a specific song or playlist by ID (Auto-wakes the desktop app).

## 🚀 Setup & Usage

### Prerequisites
*   macOS (for `open orpheus://` support)
*   NetEase Cloud Music Desktop App installed
*   `uv` package manager installed

### Installation
This project is configured to use `uv` for dependency management.

```bash
cd agent_space/mcp/netease-openapi-mcp
uv venv
uv pip install -r requirements.txt
```

### Configuration
Ensure your `settings.json` is configured to use `uv run`:

```json
"netease-music-pro": {
  "command": "/path/to/uv",
  "args": [
    "run",
    "src/main.py"
  ],
  "cwd": "/path/to/project",
  "env": {
    "PYTHONPATH": "src"
  }
}
```

## 🏗️ Architecture

*   **API Layer**: `pyncm` (Reverse-engineered Open API with Weapi encryption).
*   **MCP Framework**: `fastmcp`.
*   **Auth**: QR Code based (simulates official client), Cookies stored in `src/storage/cookies.json`.
*   **Control**: `subprocess` calling macOS `open` with `orpheus://` scheme + Base64 encoded JSON commands.
