# NetEase Music MCP Server (Pro)

[![English](https://img.shields.io/badge/Language-English-blue.svg)](#english) [![中文](https://img.shields.io/badge/Language-中文-red.svg)](#chinese)

An advanced Model Context Protocol (MCP) server for controlling NetEase Cloud Music on macOS/Windows using the Open API.

---

<a name="english"></a>
## 🎵 English

### ✨ Features

*   **🤖 AI DJ for You**: Let Gemini (or any MCP-compatible Agent) control your music. Just say "Play some music" and it handles the rest.
*   **🔓 Seamless QR Code Login**: Securely login via QR Code scan (simulating the official client behavior). Your session cookies are stored locally and never uploaded to the cloud.
*   **🧠 Personalized Experience**: Access your **Daily Recommendations** and **User Playlists** (including your "Red Heart" / Liked Songs). The Agent plays music based on your personal taste.
*   **🔍 Search & Play**: Search for any song, artist, or album by keyword and play it instantly.
*   **🚀 High Performance**: Built with `pyncm` (Open API) and `fastmcp`, it's significantly faster and more stable than traditional UI automation methods.
*   **🛡️ Smart Fallback**: Automatically detects if the desktop client is installed. If not, it gracefully falls back to the Web Player.

### 🛠️ Tools

This server exposes the following tools to the AI Agent:

1.  **`netease_login`**: Initiates the QR code login flow.
2.  **`netease_status`**: Checks current login status and user profile.
3.  **`netease_get_daily_recommend`**: Retrieves the list of today's recommended songs.
4.  **`netease_my_playlists`**: Lists all user playlists (created & subscribed).
5.  **`netease_search`**: Searches for songs by keyword.
6.  **`netease_play`**: Plays a specific song or playlist by ID (Auto-wakes the desktop app).

### 🚀 Setup & Usage

#### Prerequisites
*   macOS or Windows
*   NetEase Cloud Music Desktop App (Recommended for best experience)
*   `uv` package manager (Recommended) or `pip`

#### Installation
This project uses `uv` for dependency management.

```bash
cd agent_space/mcp/netease-openapi-mcp
uv venv
uv pip install -r requirements.txt
```

#### Configuration (settings.json)
Ensure your MCP settings are configured to use the virtual environment:

```json
"netease-music-pro": {
  "command": "/path/to/project/.venv/bin/python",
  "args": [
    "src/main.py"
  ],
  "cwd": "/path/to/project",
  "env": {
    "PYTHONPATH": "src"
  }
}
```

---

<a name="chinese"></a>
## 🎵 中文 (Chinese)

### ✨ 功能特性

*   **🤖 让 Gemini 为你播放音乐**：通过自然语言指令控制音乐播放。只需说“给我放首歌”，Agent 就会为你搞定一切。
*   **🔓 扫码登录**：支持使用手机 App 扫码安全登录。登录状态（Cookies）仅保存在本地，保护您的隐私。
*   **🧠 个性化推荐**：完美接入您的**每日推荐**和**歌单**（包括“我喜欢的音乐”）。Agent 会根据您的听歌品味来播放音乐。
*   **🔍 搜歌功能**：支持按关键词搜索歌曲、歌手或专辑，并直接播放。
*   **🚀 高性能**：基于 `pyncm` (Open API) 和 `fastmcp` 构建，比传统的 Selenium UI 自动化脚本更快、更稳定。
*   **🛡️ 智能降级**：自动检测是否安装了桌面客户端。如果没有安装，会自动调用浏览器打开网页版播放，保证服务可用性。

### 🛠️ 工具列表

本服务器向 AI Agent 暴露以下工具：

1.  **`netease_login`**: 启动扫码登录流程。
2.  **`netease_status`**: 检查当前登录状态和用户信息。
3.  **`netease_get_daily_recommend`**: 获取今日推荐歌曲列表。
4.  **`netease_my_playlists`**: 获取用户的所有歌单（创建的和收藏的）。
5.  **`netease_search`**: 按关键词搜索歌曲。
6.  **`netease_play`**: 播放指定的歌曲或歌单（自动唤起桌面应用）。

### 🚀 安装与使用

#### 前置条件
*   macOS 或 Windows 系统
*   网易云音乐桌面客户端（推荐）
*   `uv` 包管理器（推荐）或 `pip`

#### 安装步骤

```bash
cd agent_space/mcp/netease-openapi-mcp
# 创建虚拟环境并安装依赖
uv venv
uv pip install -r requirements.txt
```

#### 配置指南 (settings.json)
请确保您的 MCP 配置文件指向了正确的虚拟环境路径：

```json
"netease-music-pro": {
  "command": "/path/to/project/.venv/bin/python", // 指向虚拟环境的 python
  "args": [
    "src/main.py"
  ],
  "cwd": "/path/to/project",
  "env": {
    "PYTHONPATH": "src" // 确保能找到模块
  }
}
```

## 🏗️ 架构 (Architecture)

*   **API Layer**: `pyncm` (基于逆向工程的 Open API，支持 Weapi 加密)。
*   **MCP Framework**: `fastmcp`.
*   **Auth**: 扫码登录 (模拟官方客户端)，Cookies 存储在 `src/storage/cookies.json`。
*   **Control**: 通过 `subprocess` 调用系统命令 (`open` / `start`)，配合 `orpheus://` 协议和 Base64 编码指令实现自动播放。