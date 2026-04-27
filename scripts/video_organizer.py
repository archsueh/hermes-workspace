#!/usr/bin/env python3
"""
视频文件整理脚本
按照"按图索骥"原则整理视频文件名
"""

import os
import re
import shutil
from datetime import datetime
from pathlib import Path

# 配置
MOVIES_DIR = "/Users/mac/Movies"
LOG_FILE = "/Users/mac/Movies/视频整理日志_详细.md"
BACKUP_DIR = "/Users/mac/Movies/原始文件备份"

# 创建备份目录
os.makedirs(BACKUP_DIR, exist_ok=True)

def log(message, level="INFO"):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    print(log_entry)
    
    # 追加到日志文件
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")
    
    return log_entry

def analyze_video_filename(filename):
    """分析视频文件名"""
    name, ext = os.path.splitext(filename)
    ext = ext.lower()
    
    info = {
        'original': filename,
        'extension': ext,
        'has_date': False,
        'has_meaningful_name': False,
        'needs_rename': True,
        'suggested_name': None
    }
    
    # 检查常见视频格式
    video_extensions = ['.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.m4v']
    if ext not in video_extensions:
        info['needs_rename'] = False
        return info
    
    # 检查是否已有有意义的名字
    meaningful_patterns = [
        r'[\u4e00-\u9fa5]',  # 包含中文
        r'[a-zA-Z]{3,}',       # 包含3个以上英文字母
        r'旅行|旅游|旅游|vlog|VLOG|记录|教学|教程|课程|讲座',  # 关键词
    ]
    
    for pattern in meaningful_patterns:
        if re.search(pattern, name):
            info['has_meaningful_name'] = True
            break
    
    # 检查日期格式
    date_patterns = [
        r'(20\d{2})[-_]?(0[1-9]|1[0-2])[-_]?(0[1-9]|[12]\d|3[01])',  # YYYYMMDD
        r'(\d{4})[-_]?(\d{2})[-_]?(\d{2})',  # YYYY_MM_DD
    ]
    
    for pattern in date_patterns:
        match = re.search(pattern, name)
        if match:
            info['has_date'] = True
            date_str = match.group(0)
            # 标准化日期格式
            date_str = re.sub(r'[-_]', '', date_str)
            if len(date_str) == 8:
                info['date'] = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}"
            break
    
    # 检查无意义命名
    meaningless_patterns = [
        r'^\d+$',                    # 纯数字
        r'^[a-f0-9]{32}$',           # MD5哈希
        r'^视频\d+$',                # 视频1, 视频2
        r'^VID_\d+$',               # VID_001
        r'^IMG_\d+$',               # IMG_001
        r'^\w{8,16}$',              # 随机字符串
    ]
    
    for pattern in meaningless_patterns:
        if re.match(pattern, name, re.IGNORECASE):
            info['has_meaningful_name'] = False
            break
    
    return info

def generate_new_name(file_info, index):
    """生成新文件名"""
    original = file_info['original']
    ext = file_info['extension']
    
    # 如果有日期，优先使用日期
    if file_info.get('date'):
        date_part = file_info['date'].replace('-', '')
        base_name = f"video_{date_part}"
    else:
        # 使用时间戳
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        base_name = f"video_{timestamp}"
    
    # 添加序号避免重复
    new_name = f"{base_name}_{index:03d}{ext}"
    
    # 确保文件名安全
    new_name = re.sub(r'[<>:"/\\|?*]', '', new_name)
    
    file_info['suggested_name'] = new_name
    return new_name

def extract_video_metadata(file_path):
    """提取视频元数据（简化版）"""
    try:
        # 使用file命令获取基本信息
        import subprocess
        cmd = ['file', '-b', file_path]
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            return result.stdout.strip()[:100]
    except:
        pass
    
    # 获取文件大小和修改时间
    stat = os.stat(file_path)
    size_mb = stat.st_size / (1024 * 1024)
    mtime = datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S")
    
    return f"大小: {size_mb:.1f}MB, 修改时间: {mtime}"

def process_videos(batch_size=50):
    """处理视频文件"""
    log("开始视频文件整理", "INFO")
    
    # 获取所有视频文件
    video_files = []
    for root, dirs, files in os.walk(MOVIES_DIR):
        # 跳过备份目录
        if BACKUP_DIR in root:
            continue
            
        for file in files:
            if file.lower().endswith(('.mp4', '.mov', '.avi', '.mkv', '.wmv', '.flv', '.m4v')):
                video_files.append(os.path.join(root, file))
    
    log(f"找到 {len(video_files)} 个视频文件", "INFO")
    
    # 分析文件名
    file_analysis = []
    for file_path in video_files[:batch_size]:
        filename = os.path.basename(file_path)
        info = analyze_video_filename(filename)
        info['full_path'] = file_path
        file_analysis.append(info)
    
    # 分类统计
    needs_rename = [f for f in file_analysis if f['needs_rename']]
    has_meaningful = [f for f in file_analysis if f['has_meaningful_name']]
    has_date = [f for f in file_analysis if f.get('has_date', False)]
    
    log(f"需要重命名: {len(needs_rename)} 个", "INFO")
    log(f"已有有意义名称: {len(has_meaningful)} 个", "INFO")
    log(f"包含日期信息: {len(has_date)} 个", "INFO")
    
    # 生成新文件名并重命名
    renamed_count = 0
    rename_log = []
    
    for i, file_info in enumerate(needs_rename):
        try:
            old_path = file_info['full_path']
            old_name = file_info['original']
            
            # 备份原始文件
            backup_path = os.path.join(BACKUP_DIR, old_name)
            shutil.copy2(old_path, backup_path)
            
            # 生成新文件名
            new_name = generate_new_name(file_info, i+1)
            new_path = os.path.join(os.path.dirname(old_path), new_name)
            
            # 重命名文件
            os.rename(old_path, new_path)
            
            # 提取元数据
            metadata = extract_video_metadata(new_path)
            
            rename_log.append({
                'old': old_name,
                'new': new_name,
                'metadata': metadata,
                'path': os.path.dirname(old_path)
            })
            
            log(f"重命名: {old_name} → {new_name}", "SUCCESS")
            renamed_count += 1
            
        except Exception as e:
            log(f"重命名失败 {file_info['original']}: {str(e)}", "ERROR")
    
    # 创建详细报告
    create_rename_report(rename_log, len(video_files), len(needs_rename))
    
    return renamed_count

def create_rename_report(rename_log, total_files, needs_rename_count):
    """创建重命名报告"""
    report = f"""# 视频文件整理报告

## 执行信息
- **整理时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **总视频文件数**: {total_files}
- **需要重命名文件数**: {needs_rename_count}
- **本次处理文件数**: {len(rename_log)}
- **成功重命名数**: {len(rename_log)}

## 整理原则
1. **按图索骥**：直接整理文件名，不创建子目录
2. **英文逻辑命名**：优先使用英文，避免乱码
3. **日期优先**：有日期的文件使用日期作为名称基础
4. **保留元数据**：备份原始文件，记录文件信息

## 重命名详情

| 序号 | 原始文件名 | 新文件名 | 文件路径 | 元数据 |
|------|------------|----------|----------|--------|
"""
    
    for i, item in enumerate(rename_log, 1):
        report += f"| {i} | `{item['old']}` | `{item['new']}` | `{item['path']}` | {item['metadata']} |\n"
    
    report += f"""
## 命名规则
1. **有日期文件**: `video_YYYYMMDD_序号.扩展名`
2. **无日期文件**: `video_时间戳_序号.扩展名`
3. **序号**: 三位数字，避免重复

## 备份信息
- **备份目录**: `{BACKUP_DIR}`
- **备份文件数**: {len(rename_log)}
- **备份时间**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 后续建议
1. 验证重命名后的文件可正常播放
2. 根据需要进一步分类整理
3. 删除确认无用的视频文件
4. 定期清理备份目录

## 统计摘要
- ✅ 成功重命名: {len(rename_log)} 个文件
- 📁 总视频文件: {total_files} 个
- 🔄 待处理文件: {total_files - len(rename_log)} 个
- 💾 备份文件: {len(rename_log)} 个

---
*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*工具: Hermes Agent视频整理模块*
"""
    
    report_path = "/Users/mac/Movies/视频整理详细报告.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    log(f"创建详细报告: {report_path}", "INFO")
    return report_path

def main():
    """主函数"""
    print("=== 视频文件整理工具 ===")
    print(f"视频目录: {MOVIES_DIR}")
    print(f"备份目录: {BACKUP_DIR}")
    print(f"日志文件: {LOG_FILE}")
    print()
    
    # 初始化日志文件
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"# 视频整理日志\n")
        f.write(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n")
    
    # 处理一批视频文件（50个）
    renamed = process_videos(batch_size=50)
    
    print(f"\n✅ 整理完成: {renamed} 个视频文件已重命名")
    print(f"📋 详细报告: /Users/mac/Movies/视频整理详细报告.md")
    print(f"📝 操作日志: {LOG_FILE}")
    print(f"💾 文件备份: {BACKUP_DIR}")

if __name__ == "__main__":
    main()