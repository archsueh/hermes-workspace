# Code文件夹清理分析报告

## 执行信息
- **分析时间**: 2026-04-09 15:44:24
- **分析目录**: `/Users/mac/Documents/Code`
- **总项目数**: 25
- **备份目录**: `/Users/mac/Documents/Code/hermes-workspace/backups/code_cleanup`

## 清理原则
1. **有用代码提取**: 将有用的代码、配置、日志提取到Markdown文档
2. **无用文件删除**: 删除临时文件、重复文件、过时文件
3. **项目目录保留**: 保留完整的项目目录结构
4. **完整备份**: 所有操作前先备份原始文件

## 文件分析结果

| 序号 | 文件/目录 | 类型 | 大小 | 有用性 | 建议操作 | 原因 |
|------|-----------|------|------|--------|----------|------|
| 1 | `19d0c4caa48.yaml` | config | 476.7KB | medium | extract_to_md | 配置文件，提取关键信息到文档 |
| 2 | `Claudebot-vibe` | directory | 0.0KB | high | keep | 重要项目目录 |
| 3 | `hermes-workspace` | directory | 0.0KB | high | keep | 重要项目目录 |
| 4 | `New project` | directory | 0.0KB | medium | review | 新项目，需要检查内容 |
| 5 | `nas_copy.py` | code | 3.1KB | high | extract_to_md | 有用的工具脚本，提取到文档 |
| 6 | `清理日志_NAS_Archives_20260408.txt` | documentation | 7.4KB | low | delete | 临时文档 |
| 7 | `mihomo.yaml` | config | 2.3KB | medium | extract_to_md | 配置文件，提取关键信息到文档 |
| 8 | `fieldtheory-cli` | directory | 0.0KB | high | keep | 重要项目目录 |
| 9 | `find_dupes.py` | code | 3.7KB | medium | review | 需要检查代码内容 |
| 10 | `清理日志_20260408.txt` | documentation | 34.9KB | low | delete | 临时文档 |
| 11 | `override.yaml` | config | 0.1KB | medium | extract_to_md | 配置文件，提取关键信息到文档 |
| 12 | `config.yaml` | config | 1.2KB | medium | extract_to_md | 配置文件，提取关键信息到文档 |
| 13 | `dupes_report.txt` | documentation | 49.3KB | medium | extract_to_md | 清理日志或报告，提取总结到文档 |
| 14 | `asset_organizer.py` | code | 19.3KB | high | extract_to_md | 有用的工具脚本，提取到文档 |
| 15 | `core-plugins.json` | config | 0.7KB | low | delete | 临时或过时配置文件 |
| 16 | `CokeCloud.yaml` | config | 481.2KB | medium | extract_to_md | 配置文件，提取关键信息到文档 |
| 17 | `delete_dupes.py` | code | 1.4KB | medium | review | 需要检查代码内容 |
| 18 | `清理日志_Archives_20260408.txt` | documentation | 1.0KB | low | delete | 临时文档 |
| 19 | `hermes` | directory | 0.0KB | low | delete | 空目录或符号链接 |
| 20 | `profile.yaml` | config | 0.5KB | medium | extract_to_md | 配置文件，提取关键信息到文档 |
| 21 | `appearance.json` | config | 0.0KB | low | delete | 临时或过时配置文件 |
| 22 | `default.yaml` | config | 0.0KB | medium | extract_to_md | 配置文件，提取关键信息到文档 |
| 23 | `migrate_hsueh.sh` | code | 1.1KB | high | extract_to_md | 有用的工具脚本，提取到文档 |
| 24 | `nas_dedup_nonmaterial.py` | code | 2.9KB | high | extract_to_md | 有用的工具脚本，提取到文档 |
| 25 | `nas_graphics_cleanup.py` | code | 3.6KB | high | extract_to_md | 有用的工具脚本，提取到文档 |

## 操作统计
- **保留项目**: 3 个
- **提取到文档**: 13 个
- **需要审查**: 3 个
- **建议删除**: 6 个

## 执行计划
1. **第一阶段**: 备份所有文件
2. **第二阶段**: 提取有用内容到Markdown文档
3. **第三阶段**: 删除无用文件
4. **第四阶段**: 验证清理结果

## 注意事项
1. 所有删除操作前都会备份文件
2. 项目目录（hermes-workspace, Claudebot-vibe等）会完整保留
3. 提取的文档会保存到Notes知识库
4. 删除前会再次确认文件内容

---
*生成时间: 2026-04-09 15:44:24*
*工具: Hermes Agent文件夹分析模块*
