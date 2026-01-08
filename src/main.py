from fastmcp import FastMCP
import subprocess
import logging
import sys
import os
import json
import base64

# 确保能导入同级模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from auth import check_login_status, login_via_qrcode
from api import get_daily_recommendations, get_user_playlists, search_song
from control import control_media

# 初始化 MCP Server
mcp = FastMCP("Netease-OpenAPI-Music")
logger = logging.getLogger(__name__)

# ... (omitted previous tools) ...

@mcp.tool()
def netease_status():
    """检查网易云音乐当前是否已登录"""
    status = check_login_status()
    if status['logged_in']:
        return f"已登录，当前用户: {status['nickname']}"
    else:
        return "未登录，请使用 netease_login 进行扫码登录"

@mcp.tool()
def netease_login():
    """
    登录网易云音乐 (模拟 OAuth 流程)
    调用此工具后，电脑会弹出一张二维码图片。
    请用网易云音乐 App 扫描该二维码。
    扫描成功后，工具会自动保存登录状态。
    """
    return login_via_qrcode()

@mcp.tool()
def netease_get_daily_recommend():
    """
    获取今日推荐歌曲
    返回歌曲列表 (包含 ID, 歌名, 歌手)
    """
    result = get_daily_recommendations()
    if result['success']:
        # 格式化输出以便阅读
        text = f"📅 今日推荐 ({len(result['songs'])}首):\n"
        for i, song in enumerate(result['songs'][:10], 1): # 只展示前10首
            text += f"{i}. {song['name']} - {song['artist']} (ID: {song['id']})\n"
        return text
    else:
        return f"获取失败: {result.get('error')}"

@mcp.tool()
def netease_my_playlists():
    """
    获取我的歌单 (包括创建的歌单和红心歌单)
    """
    result = get_user_playlists()
    if result['success']:
        text = "我的歌单:\n"
        for pl in result['playlists']:
            mark = "❤️ " if "喜欢" in pl['name'] else ("👤 " if pl['is_mine'] else "收藏 ")
            text += f"{mark} {pl['name']} (ID: {pl['id']}, {pl['count']}首)\n"
        return text
    else:
        return f"获取失败: {result.get('error')}"

@mcp.tool()
def netease_search(keyword: str):
    """
    搜索歌曲
    args:
        keyword: 歌名或歌手
    """
    result = search_song(keyword)
    if result['success']:
        return result['songs']
    else:
        return f"搜索失败: {result.get('error')}"

@mcp.tool()
def netease_play(id: str, type: str = "song"):
    """
    唤起客户端播放指定歌曲或歌单
    args:
        id: 歌曲ID 或 歌单ID
        type: 'song' (单曲) 或 'playlist' (歌单)
    """
    try:
        # 构造 JSON 指令
        command = {
            "type": type,
            "id": str(id),
            "cmd": "play"
        }
        
        # 序列化并 Base64 编码
        json_str = json.dumps(command, separators=(',', ':'))
        encoded = base64.b64encode(json_str.encode('utf-8')).decode('utf-8')
        
        # 生成客户端 URL Scheme
        app_url = f"orpheus://{encoded}"
        logger.info(f"Generated App URL: {app_url}")
        
        # 尝试唤起客户端
        try:
            if sys.platform == 'win32':
                os.startfile(app_url)
            else:
                # macOS open 命令，检查返回码
                ret = subprocess.run(["open", app_url], capture_output=True)
                if ret.returncode != 0:
                    raise FileNotFoundError("macOS open failed")
            
            return f"已发送播放指令: {type} {id}"
            
        except (OSError, FileNotFoundError, subprocess.CalledProcessError) as e:
            logger.warning(f"无法唤起客户端: {e}，尝试使用网页版")
            
            # 构造网页版 URL
            # 单曲: https://music.163.com/#/song?id=123
            # 歌单: https://music.163.com/#/playlist?id=123
            web_type = "song" if type == "song" else "playlist"
            web_url = f"https://music.163.com/#/{web_type}?id={id}"
            
            if sys.platform == 'win32':
                os.startfile(web_url)
            else:
                subprocess.run(["open", web_url])
                
            return f"⚠️ 未检测到客户端，已在浏览器中播放: {web_url}"
        
    except Exception as e:
        return f"播放失败: {e}"

# === Media Control Tools ===

@mcp.tool()
def netease_pause():
    """
    暂停/继续播放 (Toggle Play/Pause)
    """
    if control_media("play_pause"):
        return "已执行暂停/播放操作"
    return "操作失败"

@mcp.tool()
def netease_next():
    """
    播放下一首 (Next Track)
    """
    if control_media("next"):
        return "已切换下一首"
    return "操作失败"

@mcp.tool()
def netease_previous():
    """
    播放上一首 (Previous Track)
    """
    if control_media("previous"):
        return "已切换上一首"
    return "操作失败"

@mcp.tool()
def netease_volume_up():
    """
    调大音量 (Volume Up)
    """
    if control_media("volume_up"):
        return "音量已调大"
    return "操作失败"

@mcp.tool()
def netease_volume_down():
    """
    调小音量 (Volume Down)
    """
    if control_media("volume_down"):
        return "音量已调小"
    return "操作失败"

if __name__ == "__main__":
    mcp.run()