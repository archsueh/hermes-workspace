#!/usr/bin/env python3
"""
Office源文件删除脚本
验证已整合的Markdown文件后，删除对应的Office源文件
"""

import os
import shutil
from datetime import datetime

# 配置
BACKUP_DIR = "/Users/mac/Developer/hermes-workspace/backups/office"
OFFICE_DIR = "/Users/mac/Documents/Office"
NOTES_DIR = "/Users/mac/Documents/Notes"
LOG_FILE = "/Users/mac/Developer/hermes-workspace/logs/office_deletion.log"
DELETION_REPORT = "/Users/mac/Developer/hermes-workspace/reports/office_deletion_report.md"

# 已处理的文件映射（从备份目录推断）
processed_files = [
    "1．2024年度云南省艺术名家工作室申请书.doc",
    "201903174068_顾益铭_毕业论文5.0.docx", 
    "202103174041_张王博_202103174041_张王博_云南艺术学院本科生论文开题报告书.docx",
    "202103174070_彭锐捷_(已瘦身)云南艺术学院设计学院毕业论文彭锐捷.docx",
    "202103174076_何雨莲_2025年4月26日-论文初稿指导.docx",
    "2024届：毕业设计归档情况统计表【数字媒体艺术】.xls",
    "2025年度绩效支撑材料 - 杨雪果.docx",
    "副本2024届本科论文答辩成绩（一.xlsx"
]

# 对应的Markdown文件
md_mapping = {
    "1．2024年度云南省艺术名家工作室申请书.doc": "research_年度云南_2024_20260409.md",
    "201903174068_顾益铭_毕业论文5.0.docx": "thesis_顾益铭_2019_20260409.md",
    "202103174041_张王博_202103174041_张王博_云南艺术学院本科生论文开题报告书.docx": "thesis_张王博_2021_20260409.md",
    "202103174070_彭锐捷_(已瘦身)云南艺术学院设计学院毕业论文彭锐捷.docx": "thesis_彭锐捷_2021_20260409.md", 
    "202103174076_何雨莲_2025年4月26日-论文初稿指导.docx": "thesis_何雨莲_2021_20260409.md",
    "2024届：毕业设计归档情况统计表【数字媒体艺术】.xls": "thesis_副本_2024_20260409.md",
    "2025年度绩效支撑材料 - 杨雪果.docx": "document_年度绩效_2025_20260409.md",
    "副本2024届本科论文答辩成绩（一.xlsx": "thesis_副本_2024_20260409.md"
}

def log(message, level="INFO"):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] [{level}] {message}"
    print(log_entry)
    
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")
    
    return log_entry

def verify_markdown_file(md_filename):
    """验证Markdown文件是否存在且非空"""
    # 在Notes目录中查找文件
    md_path = None
    for root, dirs, files in os.walk(NOTES_DIR):
        if md_filename in files:
            md_path = os.path.join(root, md_filename)
            break
    
    if not md_path:
        return False, f"Markdown文件未找到: {md_filename}"
    
    # 检查文件大小
    try:
        size = os.path.getsize(md_path)
        if size < 100:  # 小于100字节认为可能有问题
            return False, f"Markdown文件过小: {md_path} ({size}字节)"
        
        # 读取文件内容检查
        with open(md_path, 'r', encoding='utf-8') as f:
            content = f.read(500)  # 读取前500字符
        
        if not content.strip():
            return False, f"Markdown文件为空: {md_path}"
        
        # 检查是否包含必要的信息
        required_keywords = ['原始文件', '文件信息', '内容']
        content_lower = content.lower()
        found_keywords = [kw for kw in required_keywords if kw in content_lower]
        
        if len(found_keywords) < 2:
            return False, f"Markdown文件缺少必要信息: {md_path}"
        
        return True, f"验证通过: {md_path} ({size}字节)"
        
    except Exception as e:
        return False, f"验证失败 {md_path}: {str(e)}"

def find_office_file(filename):
    """在Office目录中查找文件"""
    for root, dirs, files in os.walk(OFFICE_DIR):
        if filename in files:
            return os.path.join(root, filename)
    
    # 尝试模糊匹配（文件名包含关系）
    for root, dirs, files in os.walk(OFFICE_DIR):
        for file in files:
            if filename in file or file in filename:
                return os.path.join(root, file)
    
    return None

def delete_office_file(office_filename, md_filename):
    """删除Office源文件"""
    # 1. 查找Office文件
    office_path = find_office_file(office_filename)
    
    if not office_path:
        return False, f"Office文件未找到: {office_filename}"
    
    # 2. 验证备份文件存在
    backup_path = os.path.join(BACKUP_DIR, office_filename)
    if not os.path.exists(backup_path):
        return False, f"备份文件不存在: {backup_path}"
    
    # 3. 验证Markdown文件
    md_valid, md_message = verify_markdown_file(md_filename)
    if not md_valid:
        return False, f"Markdown验证失败: {md_message}"
    
    # 4. 删除Office文件
    try:
        # 获取文件信息（用于报告）
        file_size = os.path.getsize(office_path)
        file_mtime = datetime.fromtimestamp(os.path.getmtime(office_path)).strftime("%Y-%m-%d %H:%M:%S")
        
        # 执行删除
        os.remove(office_path)
        
        return True, {
            'office_file': office_filename,
            'office_path': office_path,
            'md_file': md_filename,
            'backup_path': backup_path,
            'size': file_size,
            'mtime': file_mtime,
            'deleted_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        return False, f"删除失败 {office_path}: {str(e)}"

def create_deletion_report(deletion_results):
    """创建删除报告"""
    successful = [r for r in deletion_results if r['success']]
    failed = [r for r in deletion_results if not r['success']]
    
    report = f"""# Office源文件删除报告

## 执行信息
- **执行时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **处理文件数**: {len(deletion_results)}
- **成功删除**: {len(successful)} 个文件
- **删除失败**: {len(failed)} 个文件
- **日志文件**: {LOG_FILE}

## 删除原则
1. **备份验证**: 确保备份文件存在
2. **Markdown验证**: 确保对应的Markdown文件完整
3. **安全删除**: 只删除已验证的文件
4. **完整记录**: 记录所有操作详情

## 成功删除的文件

| 序号 | Office文件 | Markdown文件 | 文件大小 | 修改时间 | 删除时间 |
|------|------------|--------------|----------|----------|----------|
"""
    
    for i, result in enumerate(successful, 1):
        info = result['info']
        size_mb = info['size'] / (1024 * 1024)
        report += f"| {i} | `{info['office_file']}` | `{info['md_file']}` | {size_mb:.1f}MB | {info['mtime']} | {info['deleted_at']} |\n"
    
    if failed:
        report += f"""
## 删除失败的文件

| 序号 | Office文件 | 错误原因 |
|------|------------|----------|
"""
        for i, result in enumerate(failed, 1):
            report += f"| {i} | `{result['office_file']}` | {result['error']} |\n"
    
    report += f"""
## 备份信息
- **备份目录**: `{BACKUP_DIR}`
- **备份文件数**: {len(successful)} 个
- **备份大小**: 待统计

## 安全验证
✅ **三重验证机制**:
1. 备份文件存在性验证
2. Markdown文件完整性验证  
3. 文件路径有效性验证

## 后续建议
1. 定期检查备份文件完整性
2. 验证Markdown文件内容准确性
3. 根据需要恢复文件（从备份目录）
4. 更新知识库索引

## 统计摘要
- ✅ 成功删除: {len(successful)} 个Office文件
- 📄 对应Markdown: {len(successful)} 个文件
- 💾 备份保留: {len(successful)} 个文件
- ⚠️ 处理失败: {len(failed)} 个文件

---
*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
*工具: Hermes Agent文件清理模块*
"""
    
    with open(DELETION_REPORT, "w", encoding="utf-8") as f:
        f.write(report)
    
    return DELETION_REPORT

def main():
    """主函数"""
    print("=== Office源文件删除工具 ===")
    print(f"Office目录: {OFFICE_DIR}")
    print(f"备份目录: {BACKUP_DIR}")
    print(f"Notes目录: {NOTES_DIR}")
    print(f"日志文件: {LOG_FILE}")
    print()
    
    # 初始化日志
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(f"# Office文件删除日志\n")
        f.write(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n")
    
    log("开始Office源文件删除验证", "INFO")
    
    # 处理每个文件
    deletion_results = []
    
    for office_file, md_file in md_mapping.items():
        log(f"处理文件: {office_file} → {md_file}", "INFO")
        
        success, result = delete_office_file(office_file, md_file)
        
        if success:
            log(f"✅ 成功删除: {office_file}", "SUCCESS")
            deletion_results.append({
                'success': True,
                'office_file': office_file,
                'md_file': md_file,
                'info': result
            })
        else:
            log(f"❌ 删除失败: {office_file} - {result}", "ERROR")
            deletion_results.append({
                'success': False,
                'office_file': office_file,
                'md_file': md_file,
                'error': result
            })
    
    # 创建报告
    report_path = create_deletion_report(deletion_results)
    
    # 统计
    successful = len([r for r in deletion_results if r['success']])
    total = len(deletion_results)
    
    print(f"\n✅ 处理完成: {successful}/{total} 个文件成功删除")
    print(f"📋 详细报告: {report_path}")
    print(f"📝 操作日志: {LOG_FILE}")
    print(f"💾 备份保留: {BACKUP_DIR}")
    
    # 显示结果摘要
    print("\n=== 处理结果 ===")
    for result in deletion_results:
        if result['success']:
            info = result['info']
            size_mb = info['size'] / (1024 * 1024)
            print(f"✅ {result['office_file']} → {result['md_file']} ({size_mb:.1f}MB)")
        else:
            print(f"❌ {result['office_file']}: {result['error']}")

if __name__ == "__main__":
    main()