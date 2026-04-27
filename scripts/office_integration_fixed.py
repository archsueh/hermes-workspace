#!/usr/bin/env python3
"""
Office文件整合到Notes知识库工具 - 修复版
"""

import os
import re
import json
from datetime import datetime
import subprocess
import shutil

# 配置
OFFICE_DIR = "/Users/mac/Documents/Office"
NOTES_DIR = "/Users/mac/Documents/Notes"
BACKUP_DIR = "/Users/mac/Developer/hermes-workspace/backups/office"
LOG_FILE = "/Users/mac/Developer/hermes-workspace/logs/office_integration_fixed.log"

# 确保所有目录存在
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# 确保Notes子目录存在
notes_subdirs = [
    os.path.join(NOTES_DIR, "06-学术研究", "students"),
    os.path.join(NOTES_DIR, "06-学术研究", "projects"),
    os.path.join(NOTES_DIR, "05-教学管理", "courses"),
    os.path.join(NOTES_DIR, "05-教学管理", "materials"),
    os.path.join(NOTES_DIR, "07-系统规则", "administration"),
    os.path.join(NOTES_DIR, "08-个人记录", "documents"),
    os.path.join(NOTES_DIR, "00-索引与导航", "unclassified")
]

for dir_path in notes_subdirs:
    os.makedirs(dir_path, exist_ok=True)

def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")

def safe_filename(name):
    """生成安全的文件名"""
    # 移除非法字符
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    # 替换空格为下划线
    name = re.sub(r'\s+', '_', name)
    # 限制长度
    if len(name) > 100:
        name = name[:100]
    return name

def extract_text_from_file(file_path):
    """从Office文件提取文本内容"""
    try:
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.txt':
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        
        elif ext in ['.docx', '.doc']:
            # 使用textutil提取文本
            cmd = ['textutil', '-convert', 'txt', '-stdout', file_path]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            return result.stdout if result.returncode == 0 else ""
        
        elif ext in ['.xlsx', '.xls', '.pptx', '.ppt', '.pdf']:
            # 对于这些格式，返回基本信息
            return f"文件类型: {ext.upper()}\n文件名: {os.path.basename(file_path)}"
        
        else:
            return f"不支持的文件格式: {ext}"
            
    except Exception as e:
        log(f"提取文件内容失败 {file_path}: {str(e)}")
        return ""

def analyze_filename(filename):
    """分析文件名，提取关键信息"""
    name = os.path.splitext(filename)[0]
    
    info = {
        'original_name': filename,
        'cleaned_name': safe_filename(name)
    }
    
    # 识别学号
    student_id_match = re.search(r'(\d{10,12})', name)
    if student_id_match:
        info['student_id'] = student_id_match.group(1)
    
    # 识别中文姓名
    name_match = re.search(r'([\u4e00-\u9fa5]{2,4})', name)
    if name_match:
        info['chinese_name'] = name_match.group(1)
    
    # 识别年份
    year_match = re.search(r'(20\d{2})', name)
    if year_match:
        info['year'] = year_match.group(1)
    
    # 识别课程代码
    course_match = re.search(r'(\d{8,10})', name)
    if course_match:
        info['course_code'] = course_match.group(1)
    
    # 判断文件类型
    type_keywords = {
        'student_thesis': ['论文', '毕业论文', '毕业设计', '开题报告', '指导记录'],
        'course_syllabus': ['教学大纲', '课程大纲', '教学计划', '课程计划'],
        'teaching_material': ['教案', '讲义', '课件', 'PPT', '教学日历'],
        'research_project': ['研究', '项目', '课题', '申报', '申请书'],
        'administrative': ['表格', '审批', '申请', '登记', '汇总', '统计', '附件'],
        'personal': ['个人', '简历', '自述', '信息表']
    }
    
    info['type'] = 'unknown'
    for file_type, keywords in type_keywords.items():
        if any(keyword in name for keyword in keywords):
            info['type'] = file_type
            break
    
    return info

def generate_english_name(file_info):
    """生成英文逻辑文件名"""
    file_type = file_info.get('type', 'unknown')
    
    # 构建名称部分
    parts = []
    
    # 添加类型前缀
    type_prefix = {
        'student_thesis': 'thesis',
        'course_syllabus': 'syllabus',
        'teaching_material': 'teaching',
        'research_project': 'research',
        'administrative': 'admin',
        'personal': 'personal',
        'unknown': 'document'
    }.get(file_type, 'document')
    
    parts.append(type_prefix)
    
    # 添加姓名或标识
    if 'chinese_name' in file_info:
        parts.append(file_info['chinese_name'].lower())
    elif 'student_id' in file_info:
        parts.append(file_info['student_id'])
    elif 'course_code' in file_info:
        parts.append(file_info['course_code'])
    
    # 添加年份
    if 'year' in file_info:
        parts.append(file_info['year'])
    
    # 添加日期戳
    parts.append(datetime.now().strftime("%Y%m%d"))
    
    # 生成文件名
    filename = "_".join(parts)
    return safe_filename(filename) + ".md"

def determine_target_directory(file_info):
    """确定目标目录"""
    file_type = file_info.get('type', 'unknown')
    
    mapping = {
        'student_thesis': os.path.join(NOTES_DIR, "06-学术研究", "students"),
        'course_syllabus': os.path.join(NOTES_DIR, "05-教学管理", "courses"),
        'teaching_material': os.path.join(NOTES_DIR, "05-教学管理", "materials"),
        'research_project': os.path.join(NOTES_DIR, "06-学术研究", "projects"),
        'administrative': os.path.join(NOTES_DIR, "07-系统规则", "administration"),
        'personal': os.path.join(NOTES_DIR, "08-个人记录", "documents"),
        'unknown': os.path.join(NOTES_DIR, "00-索引与导航", "unclassified")
    }
    
    return mapping.get(file_type, mapping['unknown'])

def create_markdown_content(file_info, text_content, original_path):
    """创建Markdown内容"""
    title = file_info.get('cleaned_name', os.path.splitext(os.path.basename(original_path))[0])
    
    content = f"""# {title}

## 文件信息
- **原始文件**: `{os.path.basename(original_path)}`
- **文件类型**: {file_info.get('type', 'unknown')}
- **提取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **来源路径**: `{original_path}`

## 元数据
```
{json.dumps(file_info, ensure_ascii=False, indent=2)}
```

"""
    
    # 添加提取的文本内容
    if text_content and len(text_content.strip()) > 0:
        # 限制内容长度
        preview = text_content[:1000]
        if len(text_content) > 1000:
            preview += "..."
        
        content += f"""
## 内容预览

```
{preview}
```

> 注：此为自动提取的文本内容预览。
"""
    
    # 添加整合指南
    content += f"""
## 知识整合指南

### 1. 内容提炼
- [ ] 阅读完整内容，提炼核心观点
- [ ] 提取关键数据、案例、方法
- [ ] 总结主要结论和建议

### 2. 知识关联
- [ ] 关联到现有笔记主题
- [ ] 创建双链引用
- [ ] 更新知识图谱索引

### 3. 文件管理
- [ ] 验证内容完整性
- [ ] 备份重要信息
- [ ] 确认后可删除原始文件

---
*本文件由Hermes Agent自动生成，遵循英文逻辑命名规范。*
"""
    
    return content

def process_files_sample(sample_size=5):
    """处理文件样本"""
    log("开始处理Office文件样本")
    
    # 获取文件列表
    all_files = []
    for root, dirs, files in os.walk(OFFICE_DIR):
        for file in files:
            if file.lower().endswith(('.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt', '.txt', '.pdf')):
                all_files.append(os.path.join(root, file))
    
    log(f"找到 {len(all_files)} 个Office文件")
    
    # 选择样本
    import random
    sample_files = random.sample(all_files, min(sample_size, len(all_files)))
    
    processed = []
    for i, file_path in enumerate(sample_files):
        try:
            filename = os.path.basename(file_path)
            log(f"处理 {i+1}/{len(sample_files)}: {filename}")
            
            # 1. 分析文件
            file_info = analyze_filename(filename)
            
            # 2. 提取内容
            text_content = extract_text_from_file(file_path)
            
            # 3. 生成目标信息
            english_name = generate_english_name(file_info)
            target_dir = determine_target_directory(file_info)
            target_path = os.path.join(target_dir, english_name)
            
            # 4. 创建内容
            md_content = create_markdown_content(file_info, text_content, file_path)
            
            # 5. 保存文件
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            # 6. 备份原始文件
            backup_path = os.path.join(BACKUP_DIR, filename)
            shutil.copy2(file_path, backup_path)
            
            processed.append({
                'original': file_path,
                'new': target_path,
                'info': file_info
            })
            
            log(f"✅ 创建: {target_path}")
            
        except Exception as e:
            log(f"❌ 失败: {filename} - {str(e)}")
    
    return processed

def create_sample_report(processed_files):
    """创建样本处理报告"""
    report = f"""# Office文件整合样本报告

## 执行信息
- **时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **样本大小**: {len(processed_files)} 个文件
- **日志文件**: {LOG_FILE}

## 处理结果
| 序号 | 原始文件 | 新文件 | 类型 | 状态 |
|------|----------|--------|------|------|
"""
    
    for i, item in enumerate(processed_files, 1):
        report += f"| {i} | `{os.path.basename(item['original'])}` | `{os.path.basename(item['new'])}` | {item['info'].get('type', 'unknown')} | ✅ 成功 |\n"
    
    report += f"""
## 目录结构
```
{NOTES_DIR}/
├── 00-索引与导航/unclassified/      # 未分类文件
├── 05-教学管理/courses/            # 课程大纲
├── 05-教学管理/materials/          # 教学材料
├── 06-学术研究/students/           # 学生论文
├── 06-学术研究/projects/           # 研究项目
├── 07-系统规则/administration/     # 行政文件
└── 08-个人记录/documents/          # 个人资料
```

## 命名规则示例
- 学生论文: `thesis_姓名_年份_日期.md`
- 课程大纲: `syllabus_课程代码_年份_日期.md`
- 行政文件: `admin_描述_年份_日期.md`

## 后续步骤
1. 审核生成的Markdown文件内容
2. 根据内容提炼核心知识
3. 整合到对应主题笔记
4. 更新知识图谱索引

## 注意事项
- 所有原始文件已备份到: {BACKUP_DIR}
- 采用英文逻辑命名，避免乱码
- 分批处理，确保质量
"""
    
    report_path = os.path.join(os.path.dirname(LOG_FILE), "office_sample_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return report_path

if __name__ == "__main__":
    print("=== Office文件整合工具 (修复版) ===")
    print(f"源目录: {OFFICE_DIR}")
    print(f"目标目录: {NOTES_DIR}")
    print(f"样本大小: 5 个文件")
    print()
    
    # 处理5个样本文件
    processed = process_files_sample(5)
    
    # 创建报告
    report_path = create_sample_report(processed)
    
    print(f"\n✅ 处理完成: {len(processed)} 个文件")
    print(f"📋 报告: {report_path}")
    print(f"📝 日志: {LOG_FILE}")
    print(f"💾 备份: {BACKUP_DIR}")
    
    # 显示处理结果
    print("\n=== 处理结果 ===")
    for item in processed:
        print(f"• {os.path.basename(item['original'])} → {os.path.basename(item['new'])}")