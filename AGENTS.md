# RICE AI 评估系统 - Codex 项目背景

## 项目概述

RICE AI 是面向特需儿童康复机构的智能评估系统。核心流程是：评估答题 → 自动计分 → AI 生成评估报告 → AI 生成 IEP 个别化教育计划 → 导出文档。

目标用户包括 ABA 康复机构的康复师、督导、管理员和家长。项目重点围绕三类评估工具：

- PEP-3：心理教育量表第三版，评分体系为 P/E/F 或对应分值。
- C-PEP-3：中文修订版，包含发展领域、病理行为领域和补充项目。
- VB-MAPP：语言行为里程碑评估，包含 170 个里程碑、24 项障碍评估、18 项转衔评估。

## 关键目录

- `config/`：AI prompt、工具介绍、免责声明、评估类型配置。
- `config/report-prompt-*.md`：评估报告生成规则。
- `config/iep-prompt-*.md`：IEP 生成规则。
- `config/eval-type-config.json`：评估工具交互配置，包括答题模式、卡片字段、报告页路由。
- `config/course-packets.json`：IEP 目标匹配时使用的课程包项目。
- `data/`：评估量表配置数据和原始资料。
- `data/pep3-config-v5.csv`：PEP-3 当前题目配置。
- `data/cpep-config-v3.csv`：C-PEP 当前题目配置。
- `data/vbmapp-config-v4.csv`：VB-MAPP 当前题目配置。
- `features/assessment-admin/pad/`：后台管理端 HTML 原型。
- `features/assessment-app/pad/`：康复师 App PAD/Web 端 HTML 原型。
- `features/assessment-app/mobile/`：康复师 App 手机端 HTML 原型。
- `docs/`：产品需求文档。
- `design/DESIGN.md`：设计规范。
- `scripts/`：解析量表、生成配置、截图等辅助脚本。

## 当前重要文件

- `CLAUDE.md`：已有项目说明，内容较完整，可作为补充背景。
- `config/report-prompt-vbmapp-v3.0.md`：VB-MAPP 报告 prompt 的最新 v3.0 版本，基于真实报告案例增强。
- `config/report-prompt-vbmapp-v2.0.md`：VB-MAPP v2.0 版本，保留用于对比。
- `config/report-prompt-pep3-v2.0.md`：PEP-3 v2.0 prompt。
- `workbench.html` 和 `workbench-config.json`：评估配置查看/调试工作台。

## Prompt 编写规则

评估报告 prompt 的核心目标是生成专业、稳定、可落地的报告，不是简单罗列分数。

- 必须基于评估数据和观察记录，不编造儿童具体表现。
- 报告正文偏连续专业段落，少用清单式堆砌，除非模板明确要求。
- 要写出儿童会什么、部分会什么、不会什么，以及对应干预方向。
- 每个领域都应关联未掌握能力和下一步教学建议。
- IEP 目标必须具体、可测量、3 个月内可达成。
- 课程包或干预项目名称必须与 `config/course-packets.json` 中的项目一致，不能自行创造。
- VB-MAPP 术语保持准确：提要求=Mand，命名=Tact，听者反应=LR，LRFFC 等。

VB-MAPP 报告尤其注意：

- 里程碑、障碍、转衔三大模块都要覆盖。
- 里程碑分析使用领域三段式：领域功能说明和观察描述 → 得分与阶段子项 → 课程定位/教学建议。
- 障碍分析使用：现象描述 → 功能分析 → 干预方案。
- v3.0 要求 16 个里程碑领域均以某种形式呈现，高阶 0 分领域也要合理说明。
- 社交行为、社交游戏、集体技能得分均为 0 时，要输出评估环境限制说明。

## CSV 数据规则

评估工具题目配置统一使用 CSV。

- 表头结构包括：排序、一级分类、二级分类、评估项目、操作描述、所需材料、适用年龄、是否必答、评分_a_分值、评分_a_标签、评分_a_说明等。
- CSV 使用 UTF-8。
- 导出时所有字段建议用双引号包裹。
- 评分说明放在对应评分说明列，不要混入操作描述列。
- 数据变更需要检查链路：CSV → 后台配置 → App 答题页 → 缓存/localStorage → 结果页/报告 → 文档。

## 前端原型规则

这是偏静态 HTML 原型的项目，主要用 HTML/CSS/JS 和 localStorage 模拟业务流程。

- 后台管理端路径：`features/assessment-admin/pad/`。
- 康复师 App PAD 端路径：`features/assessment-app/pad/`。
- 康复师 App 手机端路径：`features/assessment-app/mobile/`。
- localStorage key 使用 `rice_assessment_` 前缀。
- 原型页面通常需要重置/测试数据入口，方便演示与验证。
- 需求打磨阶段优先改 `pad/`，手机端是否同步需看用户要求。
- 静态 HTML 可直接打开；若需要截图或浏览器验证，可用项目里的 Puppeteer 脚本或启动本地服务。

## 设计约定

优先遵守 `design/DESIGN.md`。

- 后台管理端主色：紫色 `#7C3AED`。
- 康复师 App 端主色：蓝色 `#3B9BF5`。
- 后台页面偏管理系统风格：高信息密度、清晰卡片/表格、克制视觉。
- App 端偏康复师工作流：答题效率、进度明确、结果页易读。
- 保持现有静态原型风格，不做无关视觉重构。

## 常用命令

```bash
rg --files
npm install
node scripts/screenshot-html.js
```

`package.json` 当前没有有效测试脚本，`npm test` 只会返回占位错误。需要验证时，根据改动选择查看 HTML、运行相关脚本或做人工 diff。

## Git 和协作

- 不主动提交 git，除非用户明确要求“提交git”或类似表述。
- commit message 用中文。
- 工作区里可能有用户未跟踪或未提交文件，不要回滚或覆盖无关变更。
- 修改 prompt 或数据配置时，优先新增版本文件或小范围编辑，保留旧版本用于对比。

## 外部集成

- 需求文档可能维护在飞书云端，历史说明提到使用 `lark-cli`。
- HTML 原型可部署到 GitHub Pages，路径形如 `https://hongmok.github.io/rice-eval/features/...`。
