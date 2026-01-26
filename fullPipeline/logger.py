# logger.py
import logging
import logging.handlers
from pathlib import Path


def get_logger(output_dir:str | Path,filename,name: str = None) -> logging.Logger:
    output_dir=Path(output_dir)
    log_file=output_dir/f"{filename}"/"log"/"app.log"
    log_file.parent.mkdir(parents=True, exist_ok=True)
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
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s")
    )

    logger.addHandler(console)
    logger.addHandler(file_handler)
    return logger