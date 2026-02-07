import os
import shutil
import sys
from pathlib import Path

scan_path='./'

for item in Path(scan_path).iterdir():
    if item.is_dir():
        shutil.rmtree(item)