
# Office文件夹内容整合到Notes知识库方案

## 目标
将Office文件夹中的有用内容从内容层级整合到Notes知识库，删除原Office文件

## 整合原则
1. **内容提炼**：只整理内容，不复制文件形态
2. **知识关联**：与现有Notes知识图谱关联
3. **英文逻辑命名**：使用英文逻辑命名规范
4. **分类归档**：按主题分类到Notes对应目录

## 整合流程

### 第一阶段：内容分析 (Content Analysis)
1. 扫描Office文件夹，识别文件类型和内容
2. 分类：学生论文、课程材料、研究项目、行政文件等
3. 提取关键信息：作者、主题、日期、版本

### 第二阶段：知识提炼 (Knowledge Extraction)
1. 读取Office文件内容（使用OCR/文本提取）
2. 提炼核心知识：主要观点、方法、结论
3. 结构化整理：摘要、要点、引用

### 第三阶段：知识整合 (Knowledge Integration)
1. 匹配现有Notes主题
2. 创建/更新对应.md文件
3. 添加双链引用
4. 更新索引和MOC页面

### 第四阶段：文件清理 (File Cleanup)
1. 验证整合内容完整性
2. 备份重要原始文件
3. 删除已整合的Office文件

## Notes目录映射
- **学生论文** → `06-学术研究/students/`
- **课程大纲** → `05-教学管理/courses/`
- **教学材料** → `05-教学管理/materials/`
- **研究项目** → `06-学术研究/projects/`
- **行政文件** → `07-系统规则/administration/`
- **个人资料** → `08-个人记录/`

## 英文命名示例
```
原文件：201903174005_章颖洁_201903174005_章颖洁_指导记录2.docx
新文件：06-学术研究/students/zhang_yingjie_thesis_guidance_201903_v2.md

原文件：2003042700 创意编程基础.docx
新文件：05-教学管理/courses/creative_programming_basics_syllabus_2003042700.md

原文件：设计学院2026届本科毕业论文中期检查.docx
新文件：07-系统规则/administration/design_college_thesis_midterm_check_2026.md
```

## 工具需求
1. Office文件解析工具（docx, xlsx, pptx）
2. 文本提取和OCR
3. 批量重命名工具
4. 内容摘要生成

## 风险控制
1. 重要文件先备份再处理
2. 分批处理，验证每批结果
3. 保留元数据和版本历史
4. 用户确认后删除原文件
