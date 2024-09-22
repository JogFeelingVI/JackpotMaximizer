#!/bin/bash
# @Author: Your name
# @Date:   2024-09-17 07:10:25
# @Last Modified by:   Your name
# @Last Modified time: 2024-09-22 07:58:32
start_time=$(date +%s)
# 设置 Python 解释器路径
PYTHON_PATH="./.venv/bin/python"  # 或你的 Python 解释器路径
echo "PYTHON_PATH: $PYTHON_PATH"
# 设置 Python 程序路径
PYTHON_SCRIPT="./Perform_exploration.py"  # 替换为你的 Python 程序路径

# 执行 Python 程序
sudo systemd-inhibit --what=sleep --who="Perform_exploration" --why="Running python No handle-freeze" --mode=block $PYTHON_PATH $PYTHON_SCRIPT
end_time=$(date +%s)
execution_time=$((end_time - start_time))

ps -ef | grep './venv'| grep -v 'pts' | awk '{print $2}' | xargs kill -9
# 可选: 打印程序返回值
echo "Execution time: $execution_time seconds"