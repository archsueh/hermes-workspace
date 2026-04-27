#!/bin/bash
# Agent团队优化 - 梯度1清理脚本
# 清理演示协作的临时文件

echo "开始清理演示临时文件..."

# 定义工作目录
WORKSPACE_DIR="Code/hermes-workspace/temp"

# 要删除的文件列表
FILES_TO_REMOVE=(
    "演示协作-任务分配.md"
    "演示协作-状态报告.md"
    "演示协作-任务汇总.md"
)

# 删除文件
cd "$WORKSPACE_DIR" || exit 1

for file in "${FILES_TO_REMOVE[@]}"; do
    if [ -f "$file" ]; then
        echo "删除: $file"
        rm -f "$file"
        if [ $? -eq 0 ]; then
            echo "  ✅ 删除成功"
        else
            echo "  ❌ 删除失败"
        fi
    else
        echo "跳过: $file (不存在)"
    fi
done

# 显示剩余文件
echo ""
echo "清理完成！剩余文件："
ls -lh "$WORKSPACE_DIR"
