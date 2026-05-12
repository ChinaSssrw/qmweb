# 企盟小程序 (QianMeng Web)

以"人"为核心的实名制私域社交圈子小程序。

## 项目结构

```
qmweb/
├── doc/                          # 完整文档体系（Vibe Coding框架）
│   ├── vision.md                 # 产品愿景与边界 ← 开工前先读
│   ├── roadmap.md                # 阶段规划与里程碑
│   ├── design-doc.md             # 系统设计（核心）
│   ├── architecture.md           # 技术架构
│   ├── modules/                  # 模块详细说明（9个模块）
│   │   ├── module-01-digital-card.md
│   │   ├── module-02-status-post.md
│   │   ├── module-03-contacts.md
│   │   ├── module-04-activity.md
│   │   ├── module-05-space.md
│   │   ├── module-06-membership.md
│   │   ├── module-07-interaction-stats.md
│   │   ├── module-08-profile.md
│   │   └── module-09-payment.md
│   ├── data-model.md             # 数据模型（11个核心表）
│   ├── api-contract.md           # API接口契约
│   ├── workflows.md              # 核心业务流程
│   ├── ai-collaboration.md       # AI协作规则
│   ├── decisions.md              # 架构决策记录（ADR）
│   ├── tasks.md                  # 当前任务拆解（验收标准）
│   ├── changelog.md              # 变更记录
│   └── testing/                  # 测试验证框架
│       ├── strategy.md
│       ├── test-cases/
│       ├── acceptance-criteria/
│       ├── mocks-and-fixtures.md
│       └── bug-template.md
├── backend/                      # 后端代码（FastAPI）
├── frontend/                     # 前端代码（微信小程序）
└── README.md
```

## 快速开始

1. 先读 `doc/vision.md` 了解产品定位和边界
2. 看 `doc/tasks.md` 了解当前任务
3. 按 `doc/architecture.md` 搭建开发环境

## 核心原则

> **文档不是交付物，是AI协作的上下文控制系统。**
