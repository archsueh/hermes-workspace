# 技能库

这是您的Hermes Agent技能存储目录。

## 技能结构

每个技能是一个目录，包含：
```
技能名/
├── SKILL.md          # 技能主文件（必须）
├── references/       # 参考文件（可选）
├── templates/        # 模板文件（可选）
└── scripts/         # 脚本文件（可选）
```

## 现有技能

### 用户创建
- `knowledge-management-rules` - 知识管理规则

### 系统技能
系统技能位于其他位置，可通过技能列表查看。

## 添加新技能

### 方法1：通过Agent创建
```bash
# Agent会自动创建技能结构
skill_manage action="create" name="新技能名"
```

### 方法2：手动创建
1. 创建技能目录：`mkdir 技能名`
2. 创建SKILL.md文件
3. 添加必要的内容

## 技能格式

SKILL.md文件格式：
```yaml
---
name: 技能名称
description: 技能描述
category: 分类
tags: [标签1, 标签2]
version: 1.0
---

# 技能名称

## 触发条件
何时使用此技能

## 步骤
1. 第一步
2. 第二步

## 注意事项
- 注意点1
- 注意点2

## 示例
具体使用示例
```

## 管理技能

### 查看技能
```bash
skills_list
skill_view name="技能名"
```

### 更新技能
```bash
skill_manage action="patch" name="技能名"
```

### 删除技能
```bash
skill_manage action="delete" name="技能名"
```

## 最佳实践

1. **明确触发条件**：清晰定义何时使用
2. **步骤详细**：提供可执行的具体步骤
3. **包含示例**：展示实际使用方式
4. **定期更新**：保持技能内容最新
5. **分类整理**：按用途分类存储
