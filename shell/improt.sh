#!/bin/bash
# @Author: JogFeelingVI
# @Date:   2024-04-21 21:05:21
# @Last Modified by:   JogFeelingVI
# @Last Modified time: 2024-06-25 09:59:18

# 定义源文件夹和目标文件夹
source_dir=~/Downloads/Github/autoasset
target_dir=~/Downloads/Github/JackpotMaximizer
# source_dir=~/Github/autoasset
# target_dir=~/Github/JackpotMaximizer

# 复制文件
dataf="DataFrame.json"
json="filterN_v3.json"
insx="insx.rego"
# filterN_v3="codex/filters_v3.py"

# 验证文件是否复制成功
if [[ -f "${source_dir}/${json}" ]]; then
    echo "The '${json}' file exists."
    cp "${source_dir}/${json}" "${target_dir}"
    echo "The '${json}' file has been copied."
else
    echo "${json} copy failed."
fi

if [[ -f "${source_dir}/${dataf}" ]]; then
    echo "The '${dataf}' file exists."
    cp "${source_dir}/${dataf}" "${target_dir}"
    echo "The '${dataf}' file has been copied."
else
    echo "${dataf} copy failed."
fi

if [[ -f "${source_dir}/${insx}" ]]; then
    echo "The '${insx}' file exists."
    cp "${source_dir}/${insx}" "${target_dir}"
    echo "The '${insx}' file has been copied."
else
    echo "${insx} copy failed."
fi

# if [[ -f "${source_dir}/${filterN_v3}" ]]; then
#     echo "The '${filterN_v3}' file exists."
#     cp "${source_dir}/${filterN_v3}" "${target_dir}/${filterN_v3}"
#     echo "The '${filterN_v3}' file has been copied."
# else
#     echo "${filterN_v3} copy failed."
# fi
