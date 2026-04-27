#!/usr/bin/env python3
"""
Office文件整合到Notes知识库工具
将Office文件内容提炼并整合到Notes知识库
"""

import os
import re
import json
from datetime import datetime
from pathlib import Path
import subprocess
import shutil

# 配置
OFFICE_DIR = "/Users/mac/Documents/Office"
NOTES_DIR = "/Users/mac/Documents/Notes"
BACKUP_DIR = "/Users/mac/Developer/hermes-workspace/backups/office"
LOG_FILE = "/Users/mac/Developer/hermes-workspace/logs/office_integration.log"

# 创建目录
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log(message):
    """记录日志"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    print(log_entry)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(log_entry + "\n")

def extract_text_from_file(file_path):
    """从Office文件提取文本内容"""
    try:
        ext = os.path.splitext(file_path)[1].lower()
        
        if ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()
        
        elif ext in ['.docx', '.doc']:
            # 使用textutil提取文本
            cmd = ['textutil', '-convert', 'txt', '-stdout', file_path]
            result = subprocess.run(cmd, capture_output=True, text=True)
            return result.stdout if result.returncode == 0 else ""
        
        elif ext in ['.xlsx', '.xls']:
            # 对于Excel文件，只提取基本信息
            return f"Excel文件: {os.path.basename(file_path)}"
        
        elif ext in ['.pptx', '.ppt']:
            # 对于PPT文件，只提取基本信息
            return f"PPT文件: {os.path.basename(file_path)}"
        
        else:
            return f"不支持的文件格式: {ext}"
            
    except Exception as e:
        log(f"提取文件内容失败 {file_path}: {str(e)}")
        return ""

def analyze_filename(filename):
    """分析文件名，提取关键信息"""
    # 移除扩展名
    name = os.path.splitext(filename)[0]
    
    # 常见模式识别
    patterns = {
        'student_id': r'(\d{10,12})',  # 学号
        'student_name': r'([\u4e00-\u9fa5]{2,4})',  # 中文姓名
        'course_code': r'(\d{8,10})',  # 课程代码
        'year': r'(20\d{2})',  # 年份
        'version': r'([vV]\d+|\(\d+\)|版本\d+)',  # 版本号
    }
    
    info = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, name)
        if match:
            info[key] = match.group(1)
    
    # 判断文件类型
    if '论文' in name or '毕业论文' in name or '毕业设计' in name:
        info['type'] = 'student_thesis'
    elif '教学大纲' in name or '课程大纲' in name:
        info['type'] = 'course_syllabus'
    elif '教案' in name or '讲义' in name or '课件' in name:
        info['type'] = 'teaching_material'
    elif '研究' in name or '项目' in name or '课题' in name:
        info['type'] = 'research_project'
    elif '表格' in name or '审批' in name or '申请' in name:
        info['type'] = 'administrative'
    elif '个人' in name or '简历' in name:
        info['type'] = 'personal'
    else:
        info['type'] = 'unknown'
    
    return info

def generate_english_name(file_info, original_name):
    """生成英文逻辑文件名"""
    file_type = file_info.get('type', 'unknown')
    
    # 基础模板
    templates = {
        'student_thesis': "student_thesis_{name}_{topic}_{year}_v1",
        'course_syllabus': "course_syllabus_{code}_{name}_{year}_v1",
        'teaching_material': "teaching_{material_type}_{course}_{date}_v1",
        'research_project': "research_{project_name}_{type}_{year}_v1",
        'administrative': "admin_{form_type}_{purpose}_{date}_v1",
        'personal': "personal_{doc_type}_{name}_{date}_v1",
        'unknown': "document_{category}_{date}_v1"
    }
    
    template = templates.get(file_type, templates['unknown'])
    
    # 提取信息
    name_parts = []
    
    if 'student_name' in file_info:
        # 中文姓名转拼音（简化版）
        name = file_info['student_name']
        name_parts.append(name.lower().replace(' ', '_'))
    
    if 'course_code' in file_info:
        name_parts.append(file_info['course_code'])
    
    if 'year' in file_info:
        name_parts.append(file_info['year'])
    
    # 生成文件名
    if name_parts:
        base_name = "_".join(name_parts)
    else:
        # 使用原始文件名（清理后）
        clean_name = re.sub(r'[^\w\s-]', '', original_name)
        clean_name = re.sub(r'[\s]+', '_', clean_name)
        base_name = clean_name[:50]
    
    return f"{base_name}.md"

def create_markdown_content(file_info, text_content, original_path):
    """创建Markdown内容"""
    # 提取基本信息
    title = os.path.splitext(os.path.basename(original_path))[0]
    
    # 创建Markdown
    content = f"""# {title}

## 文件信息
- **原始文件**: `{os.path.basename(original_path)}`
- **文件类型**: {file_info.get('type', 'unknown')}
- **提取时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **来源路径**: `{original_path}`

"""
    
    # 添加提取的文本内容
    if text_content and len(text_content.strip()) > 0:
        content += f"""
## 内容摘要

```
{text_content[:2000]}...
```

> 注：此为自动提取的文本内容摘要，完整内容请参考原始文件。
"""
    else:
        content += """
## 内容摘要

> 注：此文件内容需要手动处理或使用专业工具提取。
"""
    
    # 添加知识整合建议
    content += f"""
## 知识整合建议

### 1. 核心知识点
- [ ] 待提炼：主要观点/结论
- [ ] 待提炼：方法/流程
- [ ] 待提炼：数据/案例
- [ ] 待提炼：参考文献

### 2. 关联主题
- [ ] 关联到现有笔记：
- [ ] 创建新笔记主题：

### 3. 后续操作
- [ ] 人工审核内容完整性
- [ ] 提炼核心知识到对应笔记
- [ ] 更新知识图谱索引
- [ ] 确认后删除原始文件

---
*本文件由Hermes Agent自动生成，用于Office文件内容整合到Notes知识库。*
"""
    
    return content

def process_office_files(batch_size=10):
    """处理Office文件"""
    log("开始处理Office文件整合")
    
    # 获取Office文件列表
    office_files = []
    for root, dirs, files in os.walk(OFFICE_DIR):
        for file in files:
            if file.lower().endswith(('.docx', '.doc', '.xlsx', '.xls', '.pptx', '.ppt', '.txt', '.pdf')):
                office_files.append(os.path.join(root, file))
    
    log(f"找到 {len(office_files)} 个Office文件")
    
    # 分批处理
    processed_count = 0
    for i, file_path in enumerate(office_files[:batch_size]):
        try:
            log(f"处理文件 {i+1}/{min(batch_size, len(office_files))}: {os.path.basename(file_path)}")
            
            # 1. 备份原始文件
            backup_path = os.path.join(BACKUP_DIR, os.path.basename(file_path))
            shutil.copy2(file_path, backup_path)
            
            # 2. 分析文件名
            file_info = analyze_filename(os.path.basename(file_path))
            
            # 3. 提取文本内容
            text_content = extract_text_from_file(file_path)
            
            # 4. 生成英文文件名
            english_name = generate_english_name(file_info, os.path.basename(file_path))
            
            # 5. 确定目标目录
            target_dir = determine_target_directory(file_info)
            
            # 6. 创建Markdown内容
            md_content = create_markdown_content(file_info, text_content, file_path)
            
            # 7. 保存Markdown文件
            target_path = os.path.join(target_dir, english_name)
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(md_content)
            
            log(f"✅ 创建: {target_path}")
            processed_count += 1
            
        except Exception as e:
            log(f"❌ 处理失败 {file_path}: {str(e)}")
    
    log(f"处理完成: {processed_count}/{min(batch_size, len(office_files))} 个文件")
    return processed_count

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

def create_integration_report():
    """创建整合报告"""
    report = f"""# Office文件整合报告

## 项目概述
- **执行时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
- **源目录**: {OFFICE_DIR}
- **目标目录**: {NOTES_DIR}
- **备份目录**: {BACKUP_DIR}

## 处理统计
- 总文件数: 待统计
- 已处理: 待统计
- 成功: 待统计
- 失败: 待统计

## 目录结构
```
{NOTES_DIR}/
├── 05-教学管理/
│   ├── courses/      # 课程大纲
│   └── materials/    # 教学材料
├── 06-学术研究/
│   ├── students/     # 学生论文
│   └── projects/     # 研究项目
├── 07-系统规则/
│   └── administration/ # 行政文件
└── 08-个人记录/
    └── documents/    # 个人资料
```

## 命名规则
采用英文逻辑命名：`category_topic_description_version.ext`

## 后续步骤
1. 人工审核生成的Markdown文件
2. 提炼核心知识到对应主题笔记
3. 更新知识图谱索引
4. 确认内容完整性后删除原始Office文件

## 注意事项
- 重要文件已备份到: {BACKUP_DIR}
- 所有操作记录在: {LOG_FILE}
- 建议分批处理，验证每批结果
"""
    
    report_path = os.path.join(os.path.dirname(LOG_FILE), "office_integration_report.md")
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    log(f"创建整合报告: {report_path}")
    return report_path

if __name__ == "__main__":
    print("=== Office文件整合工具 ===")
    print(f"源目录: {OFFICE_DIR}")
    print(f"目标目录: {NOTES_DIR}")
    print()
    
    # 处理第一批文件（10个）
    processed = process_office_files(batch_size=10)
    
    # 创建报告
    report_path = create_integration_report()
    
    print(f"\n✅ 处理完成: {processed} 个文件")
    print(f"📋 报告: {report_path}")
    print(f"📝 日志: {LOG_FILE}")
    print(f"💾 备份: {BACKUP_DIR}")