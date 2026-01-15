import os
import logging
import sys
import time
from logging.handlers import RotatingFileHandler

def setup_logging(name: str = "netease_mcp"):
    """
    配置日志记录
    1. 通过环境变量 MCP_LOG_ENABLE=true 开启
    2. 开启时，日志写入 logs/session_{timestamp}.log
    3. 默认关闭 (Level CRITICAL+1)
    """
    # 1. 检查开关 (默认关闭)
    enable_log = os.getenv("MCP_LOG_ENABLE", "false").lower() == "true"

    root_logger = logging.getLogger()
    
    # 清除现有的 handlers，防止重复
    if root_logger.handlers:
        root_logger.handlers.clear()

    if not enable_log:
        # 关闭日志
        root_logger.setLevel(logging.CRITICAL + 1)
        root_logger.addHandler(logging.NullHandler())
        return logging.getLogger(name)


    # 2. 确定日志目录和文件名 (带时间戳)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    log_dir = os.path.join(project_root, "logs")
    
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
        
    # 文件名格式: session_YYYYMMDD_HHMMSS.log
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(log_dir, f"session_{timestamp}.log")
    
    # 3. 配置 Root Logger
    root_logger.setLevel(logging.INFO)

    # 4. Formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # 5. File Handler
    # 不再使用 RotatingFileHandler 覆盖同一个文件，而是每次新文件
    # 但为了防止单次运行日志过大，还是可以用 FileHandler 或 RotatingFileHandler (单文件不轮转)
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # 6. 抑制过于啰嗦的库日志
    logging.getLogger("urllib3").setLevel(logging.WARNING)
    logging.getLogger("PIL").setLevel(logging.WARNING)

    return logging.getLogger(name)
