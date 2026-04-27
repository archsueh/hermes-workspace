# Hermes Agent 工作区

## 概述
这是 Hermes Agent 的专用工作区，位于您的 Code 目录下，避免影响根目录整洁。

## 目录结构

```
hermes-workspace/
├── config/                 # 配置文件
│   └── hermes-config.yaml # 主配置文件
├── skills/                # 技能库
│   └── README.md          # 技能说明
├── scripts/               # 自定义脚本
├── cache/                 # 临时缓存
├── logs/                  # 运行日志
├── memory/                # 记忆存储
├── sessions/              # 会话历史
└── README.md              # 本文档
```

## 使用方法

### 1. 技能管理
- 将自定义技能放入 `skills/` 目录
- 技能格式：`技能名/SKILL.md`
- 支持子目录分类

### 2. 脚本使用
- 自定义Python脚本放在 `scripts/`
- 可在任务中调用

### 3. 配置修改
- 编辑 `config/hermes-config.yaml`
- 修改后需要重启Agent生效

### 4. 日志查看
- 运行日志：`logs/hermes.log`
- 错误日志：`logs/error.log`

## 迁移说明

### 从默认位置迁移
如果您之前有Hermes配置，可以：
1. 复制 `~/.hermes/` 内容到本工作区
2. 或让Hermes自动使用新工作区

### 备份工作区
```bash
# 备份整个工作区
cp -r /Users/mac/Developer/hermes-workspace /path/to/backup/

# 仅备份重要配置
tar -czf hermes-backup.tar.gz config/ skills/ memory/
```

## 注意事项

1. **不要删除**：工作区包含您的配置和记忆
2. **定期备份**：重要技能和配置建议备份
3. **清理缓存**：可定期清理 `cache/` 目录
4. **查看日志**：遇到问题时查看 `logs/`

## 联系支持

如有问题，请参考：
- Hermes官方文档
- 或联系开发团队

---
*创建时间：2026-04-09*
*位置：/Users/mac/Developer/hermes-workspace*
