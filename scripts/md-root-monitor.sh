#!/bin/bash
# .md文件根目录监控脚本
# 自动检测并处理根目录的.md文件

NOTES_DIR="/Users/mac/Documents/Notes"
LOG_FILE="/Users/mac/Documents/Notes/07-系统规则/logs/md-monitor.log"

# 创建日志目录
mkdir -p "$(dirname "$LOG_FILE")"

# 检查根目录.md文件
check_root_md_files() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 开始检查根目录.md文件" >> "$LOG_FILE"
    
    # 查找根目录.md文件
    find /Users/mac -maxdepth 1 -name "*.md" -type f | while read file_path; do
        filename=$(basename "$file_path")
        
        echo "发现: $filename" >> "$LOG_FILE"
        
        # 确定分类
        if [[ "$filename" == *"cnki"* ]]; then
            category="06-学术研究/research-tools/"
        elif [[ "$filename" == *"claude"* ]] || [[ "$filename" == *"hermes"* ]] || [[ "$filename" == *"ecc"* ]]; then
            category="01-技术工具/ai-agents/"
        elif [[ "$filename" == *"monitor"* ]] || [[ "$filename" == *"report"* ]]; then
            category="07-系统规则/monitoring/"
        elif [[ "$filename" == *"analysis"* ]] || [[ "$filename" == *"研究"* ]]; then
            category="06-学术研究/analyses/"
        elif [[ "$filename" == *"plan"* ]] || [[ "$filename" == *"计划"* ]]; then
            category="07-系统规则/plans/"
        else
            category="00-索引与导航/temp-integration/"
        fi
        
        target_dir="$NOTES_DIR/$category"
        mkdir -p "$target_dir"
        
        # 整合文件名
        base_name="${filename%.md}"
        target_name="${base_name}_integrated.md"
        target_path="$target_dir/$target_name"
        
        # 整合文件
        echo "---" > "$target_path"
        echo "title: "${base_name//_/ }"" >> "$target_path"
        echo "source_file: "$filename"" >> "$target_path"
        echo "original_path: "$file_path"" >> "$target_path"
        echo "integration_date: "$(date '+%Y-%m-%d')"" >> "$target_path"
        echo "integration_method: "自动监控整合"" >> "$target_path"
        echo "category: "$category"" >> "$target_path"
        echo "tags: ["自动整合", "知识管理", "文件整理"]" >> "$target_path"
        echo "---" >> "$target_path"
        echo "" >> "$target_path"
        echo "# ${base_name//_/ }" >> "$target_path"
        echo "" >> "$target_path"
        echo "## 文件信息" >> "$target_path"
        echo "- **原始位置**: \`$file_path\`" >> "$target_path"
        echo "- **整合时间**: $(date '+%Y-%m-%d %H:%M:%S')" >> "$target_path"
        echo "- **整合规则**: 所有.md文件自动落入Notes知识库" >> "$target_path"
        echo "" >> "$target_path"
        echo "---" >> "$target_path"
        echo "" >> "$target_path"
        
        # 添加原始内容
        cat "$file_path" >> "$target_path"
        
        echo "" >> "$target_path"
        echo "---" >> "$target_path"
        echo "" >> "$target_path"
        echo "*本文档由自动监控系统从根目录迁移*" >> "$target_path"
        echo "*迁移时间: $(date '+%Y-%m-%d %H:%M:%S')*" >> "$target_path"
        echo "*整合规则: 所有.md文件必须落入Notes文件夹*" >> "$target_path"
        
        # 删除原始文件
        rm "$file_path"
        
        echo "整合完成: $filename → $target_path" >> "$LOG_FILE"
        echo "删除原始文件: $file_path" >> "$LOG_FILE"
    done
    
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] 检查完成" >> "$LOG_FILE"
}

# 执行检查
check_root_md_files

# 发送通知（如果有通知系统）
# send_notification "根目录.md文件检查完成"
