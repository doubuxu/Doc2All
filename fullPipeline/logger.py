# logger.py
import logging
import logging.handlers
from pathlib import Path

LOG_DIR = Path("logs")          # 日志文件夹
LOG_DIR.mkdir(exist_ok=True)    # 自动创建

def get_logger(name: str = None) -> logging.Logger:
    """统一拿 logger 的入口，name 不传默认用模块名"""
    logger = logging.getLogger(name or __name__)

    # 只初始化一次，防止重复 addHandler
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.DEBUG)          # 全局最低级别

    # 1. 屏幕打印（INFO 以上）
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    console.setFormatter(
        logging.Formatter("[%(asctime)s] %(levelname)s  %(name)s | %(message)s",
                          datefmt="%m-%d %H:%M:%S")
    )

    # 2. 按天分割文件，保留 14 天
    file_handler = logging.handlers.TimedRotatingFileHandler(
        LOG_DIR / "app.log", when="midnight", backupCount=14, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s")
    )

    logger.addHandler(console)
    logger.addHandler(file_handler)
    return logger