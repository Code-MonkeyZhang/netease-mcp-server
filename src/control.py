import sys
import subprocess
import logging
import pyautogui

logger = logging.getLogger(__name__)

def control_media(action: str):
    """
    控制媒体播放 (跨平台)
    Args:
        action: 'play_pause', 'next', 'previous', 'volume_up', 'volume_down'
    """
    system = sys.platform
    logger.info(f"Executing media control: {action} on {system}")

    try:
        if system == 'darwin': # macOS
            # 优先尝试通过 AppleScript 直接控制网易云音乐
            # 如果网易云未运行，这可能会启动它，但通常没问题
            
            script = ""
            if action == 'play_pause':
                # 尝试发送给 "NeteaseMusic"
                script = 'tell application "NeteaseMusic" to playpause'
            elif action == 'next':
                script = 'tell application "NeteaseMusic" to next track'
            elif action == 'previous':
                script = 'tell application "NeteaseMusic" to previous track'
            elif action == 'volume_up':
                # 调节系统音量 (网易云没有暴露音量 AS 接口)
                script = 'set volume output volume (output volume of (get volume settings) + 10)'
            elif action == 'volume_down':
                script = 'set volume output volume (output volume of (get volume settings) - 10)'
            
            # 执行 AppleScript
            result = subprocess.run(["osascript", "-e", script], capture_output=True, text=True)
            
            # 如果直接控制 App 失败 (比如应用名不对)，尝试模拟系统媒体键
            if result.returncode != 0:
                logger.warning(f"Direct app control failed ({result.stderr}), falling back to System Events")
                # 备用：模拟系统媒体键 (通过 Key Code)
                # 100: F8/Play? 不太准。
                # 最好还是建议用户确认 App 名字。通常是 "NeteaseMusic" 或 "网易云音乐"
                # 我们可以尝试中文名
                if "NeteaseMusic" in script:
                    script = script.replace('"NeteaseMusic"', '"网易云音乐"')
                    subprocess.run(["osascript", "-e", script])
            
            return True

        elif system == 'win32': # Windows
            # 使用 pyautogui 模拟多媒体键
            # 这些键通常是全局有效的
            key_map = {
                'play_pause': 'playpause',
                'next': 'nexttrack',
                'previous': 'prevtrack',
                'volume_up': 'volumeup',
                'volume_down': 'volumedown'
            }
            
            if action in key_map:
                pyautogui.press(key_map[action])
                return True
            else:
                logger.error(f"Unknown action for Windows: {action}")
                return False
                
        else: # Linux etc
            logger.warning("Unsupported platform for media control")
            return False

    except Exception as e:
        logger.error(f"Control failed: {e}")
        return False
