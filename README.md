# Netease OpenAPI MCP Server

> 基于 [网易云音乐开发平台](https://developer.music.163.com/st/developer/) 标准 API 实现

**🎵 为您的 AI Agent 插上音乐的翅膀**

这是一个基于 **Netease Cloud Music OpenAPI** 构建的高级 Model Context Protocol (MCP) 服务器。它打破了传统自动化的局限，让 Claude、Gemini 等 AI 助手能够以**原生 API** 的方式，优雅、高效地控制您的网易云音乐播放体验。

不再是笨重的模拟点击，而是真正的深度集成——从扫码登录到红心歌单，从每日推荐到精准搜索，一切尽在 AI 掌握之中。

---

## ✨ 功能特性

- **🤖 让 AI Agent 为你播放音乐**：通过自然语言指令控制音乐播放。只需说“给我放首歌”，Agent 就会为你搞定一切。
- **🔓 扫码登录**：支持使用手机 App 扫码安全登录。登录状态（Cookies）仅保存在本地，保护您的隐私。
- **🧠 个性化推荐**：完美接入您的**每日推荐**和**歌单**（包括“我喜欢的音乐”）。Agent 会根据您的听歌品味来播放音乐。
- **🔍 搜歌功能**：支持按关键词搜索歌曲、歌手或专辑，并直接播放。
- **🚀 高性能**：基于 `pyncm` (Open API) 和 `fastmcp` 构建，比传统的 Selenium UI 自动化脚本更快、更稳定。

## 🛠️ 工具列表

本服务器向 AI Agent 暴露以下工具：

| 工具名称 (Tool Name) | 参数 (Parameters) | 功能描述 (Description) |
| :--- | :--- | :--- |
| `netease_login` | 无 | 启动扫码登录流程 (模拟官方 App)。 |
| `netease_status` | 无 | 检查当前登录状态和用户信息。 |
| `netease_get_daily_recommend` | 无 | 获取今日推荐歌曲列表。 |
| `netease_my_playlists` | 无 | 获取用户的所有歌单（包括创建的和收藏的）。 |
| `netease_search` | `keyword`: 关键词 (歌名/歌手) | 按关键词搜索歌曲、歌手或专辑。 |
| `netease_play` | `id`: 资源ID<br>`type`: 类型 ('song'/'playlist') | 播放指定的歌曲或歌单（自动唤起桌面应用）。 |

## 🚀 安装与使用

### 前置条件

- macOS 或 Windows 系统
- 网易云音乐桌面客户端（推荐）
- `uv` 包管理器（推荐）或 `pip`

### 安装步骤

```bash
# 1. 克隆项目
git clone https://github.com/Code-MonkeyZhang/netease-mcp-server.git
cd netease-mcp-server

# 2. 创建虚拟环境并安装依赖
uv venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows
uv pip install -r requirements.txt
```

### 配置指南 (settings.json)

请确保您的 MCP 配置文件指向了正确的虚拟环境路径。您也可以在此处通过环境变量开启日志功能。

```json
"netease-music-pro": {
  "command": "/path/to/project/.venv/bin/python", // 指向虚拟环境的 python
  "args": [
    "src/main.py"
  ],
  "cwd": "/path/to/project",
  "env": {
    "PYTHONPATH": "src", // 确保能找到模块
    "MCP_LOG_ENABLE": "true" // [可选] 开启日志记录，日志将保存在 logs/ 目录下
  }
}
```

**日志说明：**
*   **默认状态**：日志功能默认关闭。
*   **开启后**：日志会以 `session_YYYYMMDD_HHMMSS.log` 的格式保存在项目根目录的 `logs/` 文件夹中。
*   **注意**：所有日志仅写入文件，**绝不会**输出到终端，避免干扰 MCP 协议。
