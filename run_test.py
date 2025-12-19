#!/usr/bin/env python
"""快速運行測試腳本"""

import subprocess
import sys
import os

os.chdir("c:/Users/USER/Documents/PlaywrightProject-1")

# 執行 pytest
cmd = [
    sys.executable, 
    "-m", "pytest", 
    "tests/test_cart.py", 
    "-v", 
    "--tb=short",
    "-s"
]

print(f"執行命令: {' '.join(cmd)}")
print("=" * 80)

result = subprocess.run(cmd)
sys.exit(result.returncode)
