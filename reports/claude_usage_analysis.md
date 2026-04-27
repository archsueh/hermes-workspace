# Claude Usage Dashboard 项目分析报告

分析时间: 2026-04-09 19:02:27
项目路径: /tmp/claude-usage

## 📁 项目结构分析

### 核心文件

### cli.py - 命令行界面
**大小**: 10324 字节

**开头内容**:
```python
"""
cli.py - Command-line interface for the Claude Code usage dashboard.

Commands:
  scan      - Scan JSONL files and update the database
  today     - Print today's usage summary
  stats     - Print all-time usage statistics
  dashboard - Scan + open browser + start dashboard server
"""

import os
import sys
import sqlite3
from pathlib import Path
from datetime import datetime, date
```

### dashboard.py - Web仪表板
**大小**: 42019 字节

**开头内容**:
```python
"""
dashboard.py - Local web dashboard served on localhost:8080.
"""

import json
import os
import sqlite3
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from datetime import datetime

DB_PATH = Path.home() / ".claude" / "usage.db"


def get_dashboard_data(db_path=DB_PATH):
```

### scanner.py - 日志扫描器
**大小**: 19867 字节

**开头内容**:
```python
"""
scanner.py - Scans Claude Code JSONL transcript files and stores data in SQLite.
"""

import json
import os
import glob
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

PROJECTS_DIR = Path.home() / ".claude" / "projects"
XCODE_PROJECTS_DIR = Path.home() / "Library" / "Developer" / "Xcode" / "CodingAssistant" / "ClaudeAgentConfig" / "projects"
DB_PATH = Path.home() / ".claude" / "usage.db"
DEFAULT_PROJECTS_DIRS = [PROJECTS_DIR, XCODE_PROJECTS_DIR]
```

### README.md - 项目文档
**大小**: 4714 字节

**开头内容**:
```python
# Claude Code Usage Dashboard

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg?style=flat-square)](LICENSE)
[![claude-code](https://img.shields.io/badge/claude--code-black?style=flat-square)](https://claude.ai/code)

**Pro and Max subscribers get a progress bar. This gives you the full picture.**

Claude Code writes detailed usage logs locally — token counts, models, sessions, projects — regardless of your plan. This dashboard reads those logs and turns them into charts and cost estimates. Works on API, Pro, and Max plans.

![Claude Usage Dashboard](docs/screenshot.png)

**Created by:** [The Product Compass Newsletter](https://www.productcompass.pm)

---

```

## 🔧 技术架构

### 依赖分析
- **零第三方依赖**: 仅使用Python标准库
- **核心模块**: sqlite3, http.server, json, pathlib, datetime, argparse
- **数据存储**: SQLite数据库 + JSONL日志文件
- **Web界面**: 内置HTTP服务器

### 数据流程
1. **日志扫描**: scanner.py 读取 ~/.claude/transcripts/ 目录
2. **数据解析**: 提取会话、token、模型信息
3. **数据库存储**: 存入SQLite数据库
4. **Web展示**: dashboard.py 提供可视化界面
5. **CLI查询**: cli.py 提供命令行接口

## 🎯 核心功能

### 1. 使用统计
- Token使用量（输入/输出）
- 模型分布（claude-3-5-sonnet, claude-3-opus等）
- 会话时长和频率
- 项目/目录使用情况

### 2. 成本估算
- 基于Anthropic定价模型
- 按模型和token数计算
- 支持API、Pro、Max不同计划

### 3. 可视化
- 使用趋势图表
- 模型分布饼图
- 成本预测图表
- 交互式Web界面

### 4. 数据导出
- CSV格式导出
- JSON数据接口
- 定期报告生成

## 📊 数据源分析

### Claude Code 日志位置
- **macOS**: ~/.claude/transcripts/
- **Windows**: %USERPROFILE%/.claude/transcripts/
- **Linux**: ~/.claude/transcripts/

### 日志格式
- JSONL格式（每行一个JSON对象）
- 包含会话元数据
- 包含token计数
- 包含模型信息

## 🔌 集成可能性

### 与现有工作流集成
1. **自动化监控**: 定期运行扫描和报告
2. **成本警报**: 设置token使用阈值
3. **效率分析**: 识别高消耗任务模式
4. **团队协作**: 共享使用统计数据

### 扩展功能
1. **多用户支持**: 团队使用统计
2. **项目分析**: 按项目统计使用情况
3. **趋势预测**: 基于历史数据预测未来使用
4. **预算管理**: 设置月度/季度预算

## 🚀 部署方案

### 本地部署
```bash
git clone https://github.com/phuryn/claude-usage
cd claude-usage
python cli.py dashboard
```

### 自动化部署
1. 创建systemd服务（Linux）
2. 创建launchd任务（macOS）
3. 创建计划任务（Windows）

### 监控集成
1. 与Prometheus集成
2. Grafana仪表板
3. 邮件/Slack通知

---

**分析完成**: 项目结构清晰，零依赖，易于集成
**建议**: 立即部署并建立自动化监控流程
