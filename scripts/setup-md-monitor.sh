#!/bin/bash
# 设置每小时检查一次
(crontab -l 2>/dev/null; echo "0 * * * * /Users/mac/Developer/hermes-workspace/scripts/md-root-monitor.sh") | crontab -
echo "✅ 已设置每小时自动监控根目录.md文件"
