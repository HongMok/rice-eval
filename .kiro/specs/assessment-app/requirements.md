# 评估答题与结果系统 — 需求文档（康复师App端）

## 1. 简介

本文档定义康复师App端（PAD + 手机）的评估答题与评估结果两大核心模块的完整功能需求。系统支持 PEP-3（心理教育评估第三版）、C-PEP（孤独症儿童发展评估）和 VB-MAPP（语言行为里程碑评估）三套标准化评估工具的数字化施测与报告生成。

核心功能包括：
1. **评估报告列表页** — 查看、筛选、新建、删除评估记录，含测试数据生成
2. **评估答题页** — 支持直接评分与回合统计（Cold Probe）两种模式，含标记待定、备注、一键操作、断点续答
3. **评估结果路由页** — 根据工具类型自动跳转到对应的专属报告页
4. **PEP-3 / C-PEP / VB-MAPP 独立报告页** — 各含 3 个 Tab（评估报告 / IEP / 评估量表），按量表专业规范渲染
5. **家长端简化报告** — 隐藏专业评分细节，面向家长的可视化报告

---

## 2. 术语表

| 术语 | 说明 |
|------|------|
| **PEP-3** | Psychoeducational Profile Third Edition，心理教育评估第三版。包含功能发展子测验（模仿、知觉、小肌肉、大肌肉、手眼协调、认知理解、认知表达）和行为特征子测验（情感关系、游戏及兴趣、感觉反应、语言异常），评分为 0（不通过）/ 1（萌芽）/ 2（通过） |
| **C-PEP** | 孤独症儿童发展评估（中国残联版），包含 7 个领域（感知觉、精细动作、粗大动作、模仿、认知、语言理解、语言表达），评分为 0（不通过）/ 0.5（中间反应）/ 1（通过） |
| **VB-MAPP** | Verbal Behavior Milestones Assessment and Placement Program，语言行为里程碑评估。包含里程碑评估（3 个阶段 × 多领域）、障碍评估（24 项）、转衔评估（18 项 × 3 类），里程碑评分为 0 / 0.5 / 1 |
| **直接评分模式** | 评估师直接点击评分等级按钮（如 0-不通过 / 1-萌芽 / 2-通过），一次点击完成评分 |
| **回合统计模式（Cold Probe）** | 评估师对每道题进行多回合探测（默认 3 回合），每回合记录独立完成(+)、错误(-)、辅助完成(P) 三种结果之一，系统自动换算最终评分 |
| **独立完成率（indepRate）** | 独立完成回合数 / 总回合数，用于回合统计→评分换算 |
| **scoringMode** | 当前评分统计模式，取值 `direct`（直接评分）或 `rounds`（回合统计），全局设置，缓存在 localStorage |
| **roundsData** | 回合统计数据，每道题的多回合探测结果数组，格式 `[{round:1, result:'independent'}, ...]` |
| **IEP** | Individualized Education Program，个别化教育计划，根据评估结果生成的训练目标和阶段计划 |
| **课程包** | 系统预设的干预项目数据库，用于根据评估结果匹配推荐 IEP 目标 |
| **answerConfig** | 答题交互配置对象，由 `eval-type-config.json` 定义，控制卡片字段、评分描述显示、导航折叠、快捷操作、部分提交等行为 |
| **allowPartialSubmit** | 是否允许部分作答提交，PEP-3/C-PEP/VB-MAPP 均为 `false`，通用类型为 `true` |
| **quickActions** | 底部快捷操作按钮配置，可选值：`failAll`（一键评最低分）、`passAll`（一键评最高分）、`nextDomain`（下一领域） |
| **showScoreDesc** | 评分按钮下方是否展示当前选中等级的说明文字。C-PEP 为 `true`，PEP-3/VB-MAPP 为 `false` |
| **P/E/F 评分** | PEP-3 功能发展评分体系：P（Pass，已有能力/通过）、E（Emerging，部分能力/萌芽）、F（Fail，未达到/不通过） |
| **A/M/S 评分** | PEP-3 行为表现评分等级：A（Adequate，适当）、M（Mild，轻度）、S（Severe，严重） |

---

## 3. 功能描述

### 3.1 评估报告列表页

#### 3.1.1 左侧导航栏（PAD端）

- 宽度 160px，白色背景，右侧 1px `#E8ECF0` 分割线
- 顶部：学生头像（圆形 48px，浅蓝背景 `#EBF5FF`）+ 姓名（14px 600）+ 性别·年龄（12px `#8C95A6`）
- 导航项列表（从上到下）：📊 康复概述、📝 评估报告（当前选中）、📖 1对1训练课、👥 小组课、📋 康复报告、🏛️ 残联报告
- 选中态：浅蓝背景 `#EBF5FF`，文字和图标变蓝 `#3B9BF5`，左侧 3px 蓝色竖条
- 未选中态：文字 `#5A6478`
- 底部分割线下方：🔒 冻结（蓝色链接）

#### 3.1.2 Tab 筛选栏

- 顶部 48px 白色栏，底部 1px 分割线
- 左侧 Tab 组：全部 | 已完成 | 评估中
  - 选中态：蓝色文字 `#3B9BF5` + 底部 2px 蓝色下划线
  - 未选中态：灰色文字 `#5A6478`
- 右侧：📋 新建评估（蓝色文字按钮）

#### 3.1.3 评估记录卡片

每条记录为一个白色圆角卡片（16px 圆角，`0 2px 8px rgba(0,0,0,0.06)` 阴影），包含：

- **标题行**：日期-状态（如 `2026.04.10-评估中`），状态文字颜色：评估中=蓝色 `#3B9BF5`，已完成=绿色 `#52C41A`
- **信息行**：评估时间（完整时间戳）、评估工具名称、评估师姓名，13px `#8C95A6`
- **操作按钮**（右侧）：
  - 评估中状态：【删除】红色边框按钮 + 【继续评估】蓝色实心按钮
  - 已完成状态：【查看】蓝色实心按钮

#### 3.1.4 新建评估弹窗

- 点击【📋 新建评估】触发，弹出模态弹窗
- 标题：选择评估工具 + 右上角关闭按钮 ✕
- 工具列表：每个工具一张可点击卡片，包含：
  - 左侧圆形图标（40px，PEP-3=📋 紫色底，VB-MAPP=📊 蓝色底，C-PEP=🧩）
  - 工具名称（15px 600）
  - 描述文字（13px `#8C95A6`）
  - 底部信息：题目数量 + 预估用时
- 仅展示 `status === 'active'` 的工具
- 点击工具卡片 → 创建新评估记录（状态=ongoing）→ 跳转到答题页

#### 3.1.5 测试数据生成按钮

- 位置：页面右侧中部，固定定位，可拖拽
- 3 个按钮纵向排列：🟢 高分、🟡 中分、🔴 低分
- 按钮样式：40×40px，左侧圆角 8px，右侧无圆角（吸附右边缘），带阴影
- 点击后为所有已启用工具各生成一条已完成记录 + 答题数据（含约 50% 题目的回合统计数据）
- 分数档位：
  - 高分：80-100% 概率最高分，0-20% 中间分
  - 中分：40-60% 最高分，20-40% 中间分，20% 最低分
  - 低分：60-80% 最低分，10-20% 中间分，10% 最高分
- 回合统计数据：3-4 回合，结果分布与分数档位对应

#### 3.1.6 删除确认弹窗

- 标题：确认删除
- 内容：确定要删除这条评估记录吗？删除后数据无法恢复。
- 按钮：【取消】灰色边框 + 【删除】红色实心
- 确认后：从 localStorage 删除记录和对应答题数据，刷新列表

---

### 3.2 评估答题页 — PAD端

#### 3.2.0 整体布局

- 顶部栏（56px）：返回箭头 ← + 标题（工具名称）+ 进度区域 + 设置按钮
- 主体区域：左侧导航树（240px）+ 右侧题目卡片区域
- 底部操作栏：待定信息 + 快捷操作 + 提交按钮

#### 3.2.0.1 进度条

- 进度标签"已完成" + 进度条轨道（6px 高，`#E8ECF0` 背景，蓝色渐变填充）+ 进度数字（如 `45/172`）
- 全部完成时：数字变绿色 `#52C41A`，提示文字变为"（全部完成）"
- 未完成时：提示文字"（进度自动保存，中途退出不会丢失）"

#### 3.2.0.2 设置按钮与浮窗

- 设置按钮：进度条右侧，36×36px 齿轮 SVG 图标，灰色边框
- 点击弹出设置浮窗（280px 宽，固定在右上角 top:60px right:20px）
- 浮窗内容：
  - 标题"统计方式"
  - 两个选项卡（radio 样式）：
    - **直接评分**：直接点击评分等级，一次完成评分
    - **回合统计**：多回合探测，自动换算评分
  - 选中项：蓝色边框 + 浅蓝背景 `#EBF5FF` + 蓝色圆点

#### 3.2.0.3 评分模式缓存

- 评分模式存储在 localStorage key `rice_scoring_mode`
- 默认模式：`rounds`（回合统计）
- 切换模式时需确认弹窗（见 3.2.3）

#### 3.2.0.4 左侧导航树

- 宽度 240px，白色背景，右侧 1px 分割线
- 树形结构：分组标题（可折叠）→ 领域项
- 分组标题：14px 600，左侧 ▼ 箭头（折叠时旋转 -90°），点击折叠/展开
- 领域项：
  - 左侧圆点状态指示：灰色（未答）、橙色（部分）、绿色（全部完成）
  - 领域名称
  - 右侧进度数字 `(已答/总数)`，12px `#B0B8C8`
  - 选中态：浅蓝背景 `#EBF5FF`，蓝色文字，左侧 3px 蓝色竖条
- `navCollapsedByDefault` 配置控制分组是否默认折叠（C-PEP=true，其他=false）


#### 3.2.1 题目卡片（直接评分模式）

每道题渲染为一张白色圆角卡片（16px 圆角，阴影），结构如下：

- **卡片头部**：
  - 左侧：题号（12px `#8C95A6`）+ 评估项目名称（14px 600 `#1A2233`）
  - 右侧：待定标记按钮（32×32px，旗帜 SVG 图标，默认灰色 `#C4C9D4`，标记后橙色 `#F5A623`）
- **信息盒子**（浅蓝背景 `#EBF5FF`，圆角 8px，内边距 10px 12px）：
  - 操作描述（`desc` 字段）：14px `#1A2233`
  - 所需材料（`materials` 字段）：12px `#5A6478`，前缀"材料："标签色 `#8C95A6`
  - 适用年龄（`ageRange` 字段）：12px 蓝色标签，背景 `rgba(59,155,245,0.1)`，圆角 4px
  - 字段显示由 `answerConfig.cardFields` 配置控制
- **评分按钮组**：
  - 横排排列，无间距，首尾圆角 8px，中间按钮无圆角
  - 每个按钮：最小宽度 100px，高度 48px，蓝色边框 `rgba(59,155,245,0.35)`
  - 未选中：白色背景，蓝色文字 `#3B9BF5`
  - 选中：对应颜色填充 + 白色文字
  - 颜色规则（按分值从低到高排列）：红色 `#F56C6C` → 橙色 `#F5A623` → 绿色 `#52C41A`
  - 按钮显示顺序：从高分到低分（左→右），即绿色在左、红色在右
- **评分描述**（仅 `showScoreDesc=true` 时显示）：
  - 位于评分按钮下方，12px `#8C95A6`
  - 显示当前选中评分等级的说明文字（`scores[].desc`）
  - 未选中时为空
- **备注区域**：见 3.2.5

#### 3.2.2 题目卡片（回合统计模式）

回合统计模式下，评分按钮组被替换为回合统计区域：

- **回合统计区域**（灰色背景 `#FAFBFC`，1px 边框 `#E8ECF0`，圆角 10px，内边距 12px）：
  - **头部行**：
    - 左侧标题："回合统计"（13px 600 `#1A2233`）
    - 右侧提示："默认建议 3 回合，可自由增加"（11px `#8C95A6`）
  - **回合行**（每行一个回合）：
    - 回合标签："第1回合"/"第2回合"/...（12px 600 蓝色 `#3B9BF5`，最小宽度 52px）
    - 3 个结果按钮横排（flex:1，高度 36px，圆角 6px，蓝色边框）：
      - **独立(+)**：选中后绿色背景 `#52C41A` + 白色文字
      - **错误(-)**：选中后红色背景 `#F56C6C` + 白色文字
      - **辅助(P)**：选中后橙色背景 `#F5A623` + 白色文字
      - 未选中：白色背景，蓝色文字
    - 每行间距 6px
  - **新增回合按钮**："+ 新增测试回合"（虚线边框，12px `#8C95A6`，hover 变蓝）
  - **重置按钮**：灰色文字，清空当前题目所有回合数据
  - **换算结果显示**（回合统计完成后自动出现）：
    - 位于回合区域底部，上方 1px 分割线
    - 格式："换算评分：{分值}-{标签}（独立率{百分比}%）"
    - 分值文字加粗蓝色 `#3B9BF5`

- **评分换算规则**（来自 `scoring-mode-rules.md`）：

  ```
  独立率 = 独立完成数 / 总回合数
  辅助率 = 辅助完成数 / 总回合数

  if (独立率 >= 0.8) → 最高分
  else if (独立率 >= 0.3) → 中间分
  else if (辅助率 > 0) → 中间分（有辅助能力，视为萌芽）
  else → 最低分
  ```

  各工具评分映射：

  | 工具 | 最高分 | 中间分 | 最低分 |
  |------|--------|--------|--------|
  | PEP-3 | 2（通过） | 1（萌芽） | 0（不通过） |
  | C-PEP | 1（通过） | 0.5（中间反应） | 0（不通过） |
  | VB-MAPP | 1（达标） | 0.5（部分达标） | 0（未达标） |

- **直接评分结果回显**：当回合统计区域为空（无任何回合数据）时，如果该题已有直接评分结果，则在回合区域下方显示当前直接评分值，方便评估师参考

#### 3.2.3 评分模式切换

- **默认模式**：`rounds`（回合统计），缓存在 localStorage key `rice_scoring_mode`
- **切换入口**：顶部栏设置按钮 → 设置浮窗 → 选择模式
- **切换确认弹窗**：
  - 标题："切换统计方式"
  - 从直接评分 → 回合统计：
    - 提示："切换到回合统计模式后，已有的评分结果将保留，但需要通过回合统计重新验证。是否继续？"
    - 确认后：评分数据保留（scores 同步），回合数据为空
  - 从回合统计 → 直接评分：
    - 提示："切换到直接评分模式后，回合统计数据将被清除，仅保留换算后的评分结果。是否继续？"
    - 确认后：评分数据保留（scores 同步），回合数据（roundsData）清除
  - 取消：保持当前模式不变
- **切换范围**：全局设置，影响整份评估的所有题目

#### 3.2.4 底部操作栏

- 高度：固定底部，白色背景，上方 1px 分割线，内边距 12px 20px
- **左侧区域**（min-width 200px）：
  - 待定计数：旗帜 SVG 图标 + "待定: {N}题"（13px 橙色 `#F5A623`）
  - 查看链接："查看"（蓝色 `#3B9BF5`），点击弹出待定列表弹窗
- **中间区域**（flex:1，居中）：
  - 快捷操作按钮组（由 `answerConfig.quickActions` 配置）：
    - `failAll`：一键评最低分（红色边框按钮，110px 宽）
    - `passAll`：一键评最高分（绿色边框按钮，110px 宽）
    - `nextDomain`：下一领域（蓝色边框按钮，110px 宽）
  - 每个快捷操作点击前弹出确认弹窗，说明影响范围
- **右侧区域**（min-width 120px，右对齐）：
  - 提交按钮：
    - 未全部完成时：`secondary` 样式（白色背景，灰色边框，灰色文字）
    - 全部完成时：`primary` 样式（蓝色背景，白色文字）
    - 文字："提交评估"

#### 3.2.5 备注功能

- **折叠式备注区域**：每道题卡片底部
  - 触发器："📝 备注"文字链接（13px `#5A6478`，有内容时变蓝 `#3B9BF5` 并显示"(已填)"）
  - 点击展开/收起备注输入区
  - 互斥收起：展开一个备注时，自动收起其他空备注
- **备注输入框**：
  - 宽度 100%，高度 60px，可拖拽调整高度
  - 边框 1px `#E8ECF0`，圆角 8px，聚焦时边框变蓝 `#3B9BF5`
  - placeholder："记录观察到的行为表现、环境因素等..."（斜体 `#B0B8C8`）
  - 字数限制：200 字，底部显示字数统计 `{N}/200`（11px `#B0B8C8`）
- **保存机制**：
  - 失焦（blur）时自动保存到 localStorage
  - 保存按钮：聚焦时显示，点击手动保存
  - 保存后显示"已保存"提示

#### 3.2.6 待定标记功能

- **标记按钮**：位于卡片头部右上角（32×32px）
  - 默认：灰色旗帜图标 `#C4C9D4`，1px 灰色边框 `#D1D5DB`
  - 标记后：橙色旗帜图标 `#F5A623`，橙色边框，浅橙背景 `rgba(245,166,35,0.1)`
  - hover：图标和边框变橙色
- **卡片视觉反馈**：被标记的卡片左侧显示 3px 橙色竖条（`border-left-color: #F5A623`）
- **待定列表弹窗**：
  - 标题："待定题目列表"
  - 内容：按领域分组显示所有被标记的题目
    - 分组标题：领域名称（13px 600）
    - 题目项：题号 + 题目名称（13px 蓝色 `#3B9BF5`，可点击）
    - 点击题目 → 跳转到对应领域并滚动到该题
  - 底部：【关闭】按钮
- **标记操作**：点击标记按钮切换标记状态，显示 toast 提示"已标记为待定"/"已取消待定"

#### 3.2.7 提交评估

- **提交前校验**（基于 `answerConfig.allowPartialSubmit`）：
  - **0 题已答**：弹出阻断弹窗"无法提交 — 当前没有任何答题数据，请至少完成部分题目后再提交。"，仅【知道了】按钮
  - **部分已答 + allowPartialSubmit=true**：弹出确认弹窗"当前已完成 {N}/{Total} 题，还有 {M} 题未作答。确认提交吗？"，【取消】+【确认提交】
  - **部分已答 + allowPartialSubmit=false**：弹出阻断弹窗"无法提交 — 该评估工具要求完成所有题目后才能提交。当前还有 {M} 题未作答。"，仅【知道了】按钮
  - **全部完成**：弹出确认弹窗"已完成全部 {Total} 题，确认提交评估吗？"，【取消】+【确认提交】
- **提交操作**：
  - 更新评估记录状态：`status` 从 `ongoing` 改为 `completed`
  - 更新 `answeredCount` 为实际已答题数
  - 保存到 localStorage
  - 跳转到评估结果路由页：`assessment-result.html?record={recordId}&tool={toolId}`

#### 3.2.8 断点续答

- **自动保存**：
  - 每次评分操作后立即保存到 localStorage（key: `rice_assessment_answers_{recordId}`）
  - 备注在失焦时自动保存
  - 进度条实时更新
- **退出确认弹窗**：
  - 点击返回箭头 ← 触发
  - 标题："确认退出"
  - 内容："当前评估进度已自动保存，下次可继续作答。确定退出吗？"
  - 按钮：【继续评估】蓝色实心 + 【退出】灰色边框
  - 退出后跳转到评估列表页
- **恢复机制**：
  - 从列表页点击【继续评估】→ 进入答题页
  - 自动从 localStorage 加载已保存的答题数据（scores、notes、marks、roundsData）
  - 恢复到上次的领域位置（通过 currentDomain 状态）
  - 进度条显示已完成数量


---

### 3.3 评估答题页 — 手机端

手机端答题页采用单卡片视图 + 滑动导航模式，适配小屏幕操作：

#### 3.3.1 整体布局

- 顶部栏（48px）：返回箭头 ← + 标题（工具名称）+ 设置按钮
- 进度条：顶部栏下方，全宽 6px 高，蓝色渐变填充
- 中间区域：单张题目卡片（全屏宽度，max-width 420px）
- 评分按钮：固定底部，3 个等宽按钮横排
- 底部导航栏：上一题 / 题号指示 / 下一题

#### 3.3.2 单卡片视图

- 每次只显示一道题目
- 卡片内容：题号 + 题目描述 + 标记待定链接
- 卡片样式：白色背景，16px 圆角，阴影，内边距 20px

#### 3.3.3 触摸滑动支持

- 左滑：下一题
- 右滑：上一题
- 滑动动画：卡片水平滑出/滑入

#### 3.3.4 底部评分按钮

- 固定在屏幕底部（底部导航栏上方）
- 3 个等宽按钮横排，间距 8px
- 未选中：白底 + 灰边框
- 选中：对应语义色填充 + 白色文字
  - PEP-3：0-不通过（红 `#F56C6C`）/ 1-萌芽（橙 `#F5A623`）/ 2-通过（绿 `#52C41A`）
  - C-PEP：0-不通过（红）/ 0.5-中间反应（橙）/ 1-通过（绿）
  - VB-MAPP：0-未达标（红）/ 0.5-部分达标（橙）/ 1-达标（绿）

#### 3.3.5 底部导航

- 【← 上一题】+【{当前题号}/{总题数}】+【下一题 →】
- 到达最后一题时，"下一题"变为"提交评估"

---

### 3.4 评估结果路由页

路由页（`assessment-result.html`）负责根据评估工具类型自动跳转到对应的专属报告页。

#### 3.4.1 路由逻辑

1. 读取 URL 参数 `tool`（工具 ID）和 `record`（记录 ID）
2. 查找 `REPORT_PAGES` 映射表：
   ```javascript
   const REPORT_PAGES = {
     pep3: 'assessment-result-pep3.html',
     cpep: 'assessment-result-cpep.html',
     vbmapp: 'assessment-result-vbmapp.html'
   };
   ```
3. 优先用 `toolId` 直接匹配
4. 若未匹配，从 localStorage `rice_assessment_tools` 查找工具的 `type` 字段再匹配
5. 若仍未匹配，从 localStorage `rice_assessment_eval_type_config` 查找 `reportConfig.reportPage`
6. 匹配成功 → `location.replace(targetPage + '?' + params)` 跳转
7. 未匹配（通用类型）→ 留在当前页作为通用报告页 fallback

#### 3.4.2 加载状态

- 页面居中显示加载动画：旋转圆环 + "正在加载评估报告..." 文字
- 跳转通常在毫秒级完成，用户几乎无感知

---

### 3.5 PEP-3 报告页

PEP-3 报告页（`assessment-result-pep3.html`）包含 3 个 Tab：评估报告 / IEP / 评估量表。

#### 3.5.1 顶部结构

- 顶部栏（48px）：返回箭头 ← + 标题"张小明评估报告"
- Tab 栏：评估报告 | IEP | 评估量表
  - 选中态：蓝色文字 + 底部 2px 蓝色下划线
  - 未选中态：灰色文字 `#5A6478`

#### 3.5.2 Tab 1：评估报告

- **报告标题**："PEP-3 心理教育评估报告"（20px 600）
- **报告说明**：13px `#8C95A6`，说明评估依据
- **基本信息卡片**：
  - 蓝色标签"基本信息"
  - 3 列网格：儿童姓名、出生日期、实足年龄、发展年龄、评估时间、评估师
- **功能发展评分表**（P/E/F 体系）：
  - 表头：范围 | 项目总分 | 已有能力(P分) | 部分能力(E分) | 简要评价
  - 7 个功能发展领域行：模仿(I)、知觉(P)、小肌肉(FM)、大肌肉(GM)、手眼协调(EH)、认知理解(CP)、认知表达(CV)
  - 简要评价列：得分率≥75% 显示"强处"（绿色），≤40% 显示"弱处"（红色）
  - 合计行：加粗背景 `#F5F7FA`
- **行为表现评分**（A/M/S 体系）：
  - 4 个行为领域：情感关系(R)、游戏及兴趣(M)、感觉反应(S)、语言异常(L)
  - 每行：领域名称 + 得分 + A/M/S 三个 pill 按钮（选中项蓝色填充）
  - 评级规则：平均分≥1.5→A，≥0.8→M，<0.8→S
- **教育训练纲要**（可编辑区域）：
  - 蓝色标签 + 右侧"编辑"链接
  - 默认显示文本模式（14px，行高 1.8）
  - 点击编辑 → 切换为 textarea，显示【取消】+【保存】按钮
  - 保存到 localStorage key `rice_assessment_report_edit_{recordId}_eduOutline`
- **评估总结表**：
  - 表头：范围 | 已有能力(P分) | 部分能力(E分) | 未达到的能力(F分)
  - 功能发展 7 领域 + 行为表现 4 领域（行为领域合并显示评级）
- **发展概况雷达图**：
  - SVG 雷达图（420×420px），7 个功能发展领域
  - 4 层同心多边形网格（`#E8ECF0`）
  - 数据多边形：蓝色填充 `rgba(59,155,245,0.15)` + 蓝色描边
  - 各顶点彩色圆点（5px 半径）+ 领域名称标签
  - 颜色序列：`#7EC8F0, #FFB88C, #FFD966, #7ED6A8, #B8A0E0, #FFB0C8, #A0D8EF`
- **综合分析**（可编辑区域）：
  - 自动生成内容：各领域得分概述、优势领域、需关注领域、行为表现、建议
  - 支持编辑和保存

#### 3.5.3 Tab 2：IEP（个别化教育计划）

- **标题**："张小明IEP"（18px 600 居中）
- **基本信息卡片**：
  - 3 列网格：学生姓名、性别、出生日期、使用日期（可选择）、制定人员、家长签名
- **课程包选择器**：
  - 下拉选择框，选项来自 `COURSE_PACKETS` 数组
  - 可选课程包：RICE1v1、春暖综合ABA、春暖言语
  - 选择后自动根据评估结果生成 IEP
- **IEP 表格**：
  - 表头（蓝色背景白色文字）：年龄段及领域 | 干预目标 | 阶段目标 | 操作（编辑模式）
  - 领域列：rowspan 合并，显示 `stairAndDomain`（如"1-2岁-沟通-语言理解"）
  - 目标列：rowspan 合并，显示干预项目名称
  - 阶段目标列：每行一个阶段目标
  - 数据来源：根据薄弱领域（得分率≤70%）匹配 `INTERVENTION_PROJECTS` 干预项目库
  - PEP-3 领域 → 干预项目领域映射（`PEP3_DOMAIN_MAP`）
- **IEP 操作按钮**（底部 sticky）：
  - 查看模式：【导出】灰色边框 + 【导入干预目标】蓝色边框 + 【编辑】蓝色实心
  - 编辑模式：【取消】灰色边框 + 【添加目标】蓝色边框（带弹出菜单）+ 【保存】蓝色实心
- **添加目标弹出菜单**：
  - 从底部向上弹出的 popover（160px 宽，带三角箭头）
  - 选项："从目标库添加"（开发中）+ 分割线 + "+ 自定义"
- **自定义目标弹窗**：
  - 表单字段：年龄段及领域（input）、干预目标（input）、阶段目标（textarea，每行一个）
  - 按钮：【取消】+【确认添加】
- **删除功能**：
  - 编辑模式下每行显示删除链接（红色 `#F56C6C`）
  - 删除前弹出确认弹窗
  - 支持删除整个领域或单条阶段目标
- **导出功能**：
  - 生成 Word 文档（.doc 格式）
  - 包含标题、基本信息、IEP 表格
  - 通过 Blob + URL.createObjectURL 下载

#### 3.5.4 Tab 3：评估量表

- **基本信息栏**（固定顶部）：
  - 3 列网格：学生姓名、评估工具、评估时间、评估师、评估次数、实足年龄
- **左右分栏布局**：
  - 左侧导航（220px）：树形结构，按子测验分组
    - 分组：发展性子测验（6 项）、行为特征子测验（4 项）、养育者报告（3 项）
    - 每项显示：名称 + 得分率百分比
    - 选中态：浅蓝背景 + 蓝色文字 + 左侧蓝色竖条
  - 右侧详情区：
    - **领域信息栏**：领域名称 + "答题明细"
    - **统计摘要**：通过/萌芽/不通过 题数 + 得分率 + 堆叠进度条（绿/橙/红）
    - **题目卡片列表**：
      - 每题一张卡片：题号（蓝色）+ 描述 + 评分选项（pill 按钮，选中项高亮）
      - 评分选项颜色：0-不通过（红底）、1-萌芽（橙底）、2-通过（绿底）
      - 回合统计展示：若有回合数据，在评分下方显示回合统计详情
        - 灰色背景区域，标题"回合统计"
        - 每回合一个标签：`第{N}回合 {结果}`，颜色对应结果类型
      - 备注展示：若有备注，显示 📝 前缀的灰色背景文字

#### 3.5.5 底部操作栏

- 仅在 Tab 1（评估报告）时显示
- 按钮：【导出PDF】灰色边框 + 【发送报告】蓝色实心
- 导出 PDF：调用 `window.print()`
- 发送报告：生成家长版报告链接（toast 提示）

---

### 3.6 C-PEP 报告页

C-PEP 报告页（`assessment-result-cpep.html`）结构与 PEP-3 类似，但评分体系和领域不同。

#### 3.6.1 Tab 1：评估报告

- **报告标题**："C-PEP 孤独症儿童发展评估报告"
- **基本信息**：儿童姓名、出生日期、实足年龄、评估时间、评估师
- **各领域得分表**：
  - 表头：领域 | 通过数 | 中间反应 | 不通过 | 得分 | 发展年龄 | 得分率
  - 7 个领域：感知觉(55题)、精细动作(36题)、粗大动作(72题)、模仿(14题)、认知(48题)、语言理解(30题)、语言表达(30题)
  - 得分率列：彩色进度条 + 百分比数字
  - **发展年龄映射**（简化）：
    - 得分率≥90% → 5岁0月
    - ≥75% → 4岁0月
    - ≥60% → 3岁6月
    - ≥50% → 3岁0月
    - ≥40% → 2岁6月
    - ≥25% → 2岁0月
    - <25% → 1岁6月
- **发展概况雷达图**：7 个领域，与 PEP-3 雷达图结构相同
- **综合分析**（可编辑）：自动生成优势/需关注领域分析
- **训练建议**（可编辑）：按领域列出训练建议

#### 3.6.2 Tab 2：IEP

- 结构与 PEP-3 IEP 相同
- 使用 `CPEP_DOMAIN_MAP` 映射 C-PEP 领域到干预项目
- 薄弱领域阈值：得分率≤65%

#### 3.6.3 Tab 3：评估量表

- 左侧导航：7 个领域直接列出（无分组层级）
- 评分选项：不通过(0) / 中间反应(0.5) / 通过(1)
- 选中颜色：不通过=红底、中间反应=橙底、通过=绿底
- 其余结构与 PEP-3 评估量表 Tab 相同

---

### 3.7 VB-MAPP 报告页

VB-MAPP 报告页（`assessment-result-vbmapp.html`）包含里程碑评估、障碍评估、转衔评估三大模块。

#### 3.7.1 Tab 1：评估报告

- **报告标题**："VB-MAPP 语言行为里程碑评估报告"
- **基本信息**：4 列网格 — 姓名、性别、出生日期、测评日期

##### 3.7.1.1 里程碑评估

- **总分显示**："里程碑评估得分：{总分} / 170"
- **里程碑网格表**（3 个阶段，从高到低排列）：
  - 第三阶段（30-48月）：12 个领域 × 5 个里程碑
  - 第二阶段（18-30月）：12 个领域 × 5 个里程碑
  - 第一阶段（0-18月）：9 个领域 × 5 个里程碑
  - 网格单元格：填充色表示达标程度
    - 蓝色填充 `#3B9BF5`：达标
    - 浅蓝填充 `#93C5FD`：部分达标
    - 灰色填充 `#F0F2F5`：未达标
  - 行标签：里程碑编号（如 1M-5M、6M-10M、11M-15M）
  - 列标签：领域名称缩写
- **里程碑各领域报告及建议**：
  - 每个领域一张报告卡片（带边框圆角）
  - 头部：领域名称 + 得分（如"8.5分 / 15分"）
  - 描述：表现评级（表现良好/发展中/需重点关注）+ 得分率
  - 建议：根据得分率自动生成
  - 领域列表：提要求、命名、听者反应、视觉配对、游戏、社交、模仿、仿说、发音、LRFFC、对话、集体技能、语言结构、数学、阅读、书写

##### 3.7.1.2 障碍评估

- **总分显示**："障碍评估得分：{总分}"
- **障碍网格表**：
  - 24 项障碍，每项 0-4 分
  - 网格展示前 6 项（完整 24 项在详细报告中）
  - 行标签：分值 1-4
  - 列标签：障碍名称缩写
- **障碍各项报告及建议**：
  - 每项一张卡片：障碍名称 + 得分 + 影响评估 + 建议
  - 24 项障碍：行为问题、教学控制、提要求的缺陷、命名的缺陷、模仿的缺陷、仿说的缺陷、视觉感知和配对的缺失、听者技能的缺陷、对话的缺陷、社会技能的缺陷、依赖辅助、猜想式回答、扫视的缺陷、条件性辨别的缺陷、不能泛化、薄弱动机、对行为有要求就会减弱动机、依赖强化物、自我刺激、发音清晰度的缺陷、强迫性行为、多动行为、没有目光接触、感觉防御

##### 3.7.1.3 转衔评估

- **总分显示**："转衔评估得分：{总分}"
- **三类转衔评估**：
  - 第一类：VB-MAPP得分和独立学习的能力（7 项）
  - 第二类：学习模式（6 项）
  - 第三类：自理、自发和自主（6 项）
  - 每项 0-5 分
- **各项报告及建议**：按类别分组，每项一张卡片

##### 3.7.1.4 综合分析（可编辑）

- 自动生成内容：里程碑评估概述（优势/弱势领域）、障碍评估概述、转衔评估概述、综合建议

#### 3.7.2 Tab 2：IEP

- 结构与 PEP-3/C-PEP IEP 相同
- 使用 `VBMAPP_DOMAIN_MAP` 映射 VB-MAPP 领域到干预项目
- 薄弱领域阈值：得分率≤60%
- 额外：障碍评估高分项（≥3分）也加入 IEP，生成行为干预目标

#### 3.7.3 Tab 3：评估量表

- 左侧导航：按 3 个阶段分组
  - Level 1 (0-18月)：9 个领域
  - Level 2 (18-30月)：12 个领域
  - Level 3 (30-48月)：12 个领域
- 评分选项：0 未达标 / 0.5 部分达标 / 1 达标
- 选中颜色：0=红底、0.5=橙底、1=绿底
- 其余结构与 PEP-3 评估量表 Tab 相同

---

### 3.8 家长端简化报告

家长端报告页（`assessment-result-parent.html`）面向家长，隐藏专业评分细节，以可视化方式呈现评估结果。

#### 3.8.1 整体布局

- **顶部横幅**：蓝色渐变背景（`#3B9BF5` → `#60B8FF`），白色文字
  - 学生姓名 + "评估报告"（26px 600）
  - 副标题：工具名称 + 评估日期（15px，透明度 0.9）
- **内容区域**：max-width 960px 居中，左右 24px 内边距

#### 3.8.2 左右分栏

- **左栏**：发展概况雷达图
  - SVG 雷达图（320×320px）
  - 结构与专业报告雷达图相同，但尺寸更小
- **右栏**：各领域表现
  - 每个领域一行：
    - 领域名称（14px 500）
    - 表现等级：良好（绿色 `#52C41A`）/ 中等（橙色 `#F5A623`）/ 需关注（红色 `#F56C6C`）
    - 进度条（10px 高，圆角 pill）：彩色填充，宽度=得分率百分比
  - 等级判定：得分率≥70%=良好，≥50%=中等，<50%=需关注

#### 3.8.3 评估总结

- 卡片标题："📝 评估总结"
- 内容：面向家长的通俗语言描述（14px，行高 1.8）
- 不显示原始分数、P/E/F 等专业术语
- 重点说明：优势领域、需关注领域、家庭训练建议

#### 3.8.4 底部说明

- 居中文字："本报告由 RICE AI 康复系统生成"
- "如有疑问请联系您的康复师"

#### 3.8.5 数据适配

- 通过 URL 参数 `tool` 判断工具类型
- PEP-3：展示认知、语言表达、语言理解、精细动作、粗大动作、视觉模仿 6 个维度
- VB-MAPP：展示提要求、命名、听者反应、视觉配对、游戏、社交 6 个维度
- 不展示：原始分数、评分等级、行为评分、障碍评估等专业数据


---

## 4. 需求描述（EARS 格式）

### R1：评估报告列表管理

**用户故事**：作为康复师，我需要查看某个学生的所有评估记录，按状态筛选，以便快速找到需要继续或查看的评估。

**验收标准**：
- AC1.1：页面加载时从 localStorage 读取评估记录列表，按日期倒序排列
- AC1.2：Tab 筛选"全部"显示所有记录，"已完成"仅显示 `status=completed`，"评估中"仅显示 `status=ongoing`
- AC1.3：评估中记录显示【删除】和【继续评估】按钮，已完成记录显示【查看】按钮
- AC1.4：点击【继续评估】跳转到答题页，携带 `record` 和 `tool` 参数
- AC1.5：点击【查看】跳转到结果路由页，携带 `record` 和 `tool` 参数
- AC1.6：左侧导航栏"评估报告"项处于选中态

### R2：新建评估

**用户故事**：作为康复师，我需要为学生创建新的评估，选择评估工具后直接进入答题。

**验收标准**：
- AC2.1：点击"新建评估"弹出工具选择弹窗
- AC2.2：弹窗仅展示 `status=active` 的评估工具
- AC2.3：每个工具卡片显示名称、描述、题目数量、预估用时
- AC2.4：点击工具卡片后创建新记录（id=`rec_` + 时间戳，status=ongoing），保存到 localStorage
- AC2.5：创建后自动跳转到答题页

### R3：评估答题 — PAD端直接评分

**用户故事**：作为康复师，我需要在 PAD 上逐题评分，通过直接点击评分按钮快速完成评估。

**验收标准**：
- AC3.1：左侧导航树按分组→领域层级展示，点击领域切换右侧题目列表
- AC3.2：每道题卡片显示题号、项目名称、信息盒子（描述/材料/年龄）、评分按钮
- AC3.3：评分按钮从高分到低分排列（左→右），颜色从绿→橙→红
- AC3.4：点击评分按钮后立即保存到 localStorage，进度条实时更新
- AC3.5：导航树领域项显示圆点状态（灰=未答，橙=部分，绿=全部完成）和进度数字
- AC3.6：`showScoreDesc=true` 时，评分按钮下方显示当前选中等级的说明文字
- AC3.7：卡片字段显示由 `answerConfig.cardFields` 配置控制

### R4：评估答题 — 回合统计模式

**用户故事**：作为康复师，我需要对每道题进行多回合探测（Cold Probe），系统自动换算评分，以获得更客观的评估结果。

**验收标准**：
- AC4.1：回合统计模式下，评分按钮区域替换为回合统计区域
- AC4.2：默认显示 3 个回合行，每行 3 个按钮（独立/错误/辅助）
- AC4.3：点击"+ 新增测试回合"可增加回合，无上限
- AC4.4：回合统计完成后自动显示换算结果（分值 + 标签 + 独立率百分比）
- AC4.5：换算规则：独立率≥80%→最高分，≥30%→中间分，辅助率>0→中间分，否则→最低分
- AC4.6：回合数据保存在 `answers[qId].rounds` 数组中
- AC4.7：最少 1 个回合即可出分

### R5：评分模式切换

**用户故事**：作为康复师，我需要在直接评分和回合统计模式之间切换，根据实际评估需要选择合适的方式。

**验收标准**：
- AC5.1：设置浮窗中可选择"直接评分"或"回合统计"
- AC5.2：切换时弹出确认弹窗，说明数据影响
- AC5.3：直接→回合：评分数据保留，回合数据为空
- AC5.4：回合→直接：评分数据保留，回合数据清除
- AC5.5：模式缓存在 localStorage key `rice_scoring_mode`
- AC5.6：切换为全局设置，影响所有题目

### R6：评估提交

**用户故事**：作为康复师，完成评估后我需要提交评估，系统校验完成度并更新记录状态。

**验收标准**：
- AC6.1：0 题已答时阻断提交，显示提示
- AC6.2：部分已答 + `allowPartialSubmit=false` 时阻断提交，显示未完成题数
- AC6.3：部分已答 + `allowPartialSubmit=true` 时弹出确认弹窗，显示已完成/未完成题数
- AC6.4：全部完成时弹出确认弹窗
- AC6.5：确认提交后更新记录 `status=completed`，跳转到结果路由页
- AC6.6：提交按钮样式随完成度变化（secondary/primary）

### R7：断点续答

**用户故事**：作为康复师，我需要中途退出评估后能恢复到上次的进度继续作答。

**验收标准**：
- AC7.1：每次评分操作后立即保存到 localStorage
- AC7.2：点击返回箭头弹出退出确认弹窗
- AC7.3：从列表页点击"继续评估"后恢复所有已保存数据（scores、notes、marks、roundsData）
- AC7.4：进度条显示已完成数量
- AC7.5：提示文字"进度自动保存，中途退出不会丢失"

### R8：评估答题 — 手机端

**用户故事**：作为康复师，我需要在手机上进行评估答题，通过单卡片视图和滑动操作完成评分。

**验收标准**：
- AC8.1：单卡片视图，每次显示一道题
- AC8.2：支持左右滑动切换题目
- AC8.3：底部固定评分按钮，3 个等宽横排
- AC8.4：底部导航显示当前题号/总题数
- AC8.5：最后一题时"下一题"变为"提交评估"

### R9：评估结果路由

**用户故事**：作为系统，我需要根据评估工具类型自动跳转到对应的专属报告页。

**验收标准**：
- AC9.1：读取 URL 参数 `tool` 匹配 `REPORT_PAGES` 映射
- AC9.2：匹配成功时使用 `location.replace()` 跳转（不留历史记录）
- AC9.3：未匹配时留在当前页作为通用报告 fallback
- AC9.4：跳转时携带原有 URL 参数

### R10：PEP-3 报告页

**用户故事**：作为康复师，我需要查看 PEP-3 评估的专业报告，包含功能发展评分、行为表现评分、雷达图和综合分析。

**验收标准**：
- AC10.1：3 个 Tab 正确切换（评估报告/IEP/评估量表）
- AC10.2：功能发展评分表正确计算 P/E/F 分数
- AC10.3：行为表现评分正确计算 A/M/S 等级
- AC10.4：雷达图正确渲染 7 个领域数据
- AC10.5：教育训练纲要和综合分析支持编辑和保存
- AC10.6：评估总结表汇总所有领域数据
- AC10.7：底部操作栏支持导出 PDF 和发送报告

### R11：C-PEP 报告页

**用户故事**：作为康复师，我需要查看 C-PEP 评估的专业报告，包含各领域得分、发展年龄和训练建议。

**验收标准**：
- AC11.1：各领域得分表正确计算通过/中间反应/不通过数量
- AC11.2：发展年龄根据得分率正确映射
- AC11.3：雷达图正确渲染 7 个领域数据
- AC11.4：综合分析和训练建议支持编辑和保存
- AC11.5：得分率列显示彩色进度条

### R12：VB-MAPP 报告页

**用户故事**：作为康复师，我需要查看 VB-MAPP 评估的专业报告，包含里程碑网格、障碍评估和转衔评估。

**验收标准**：
- AC12.1：里程碑网格正确渲染 3 个阶段的填充状态
- AC12.2：各领域报告卡片显示得分、评级和建议
- AC12.3：障碍评估网格和各项报告正确渲染
- AC12.4：转衔评估按 3 类分组显示
- AC12.5：综合分析涵盖里程碑、障碍、转衔三个维度

### R13：IEP 生成与编辑

**用户故事**：作为康复师，我需要根据评估结果自动生成 IEP，并能编辑、添加、删除目标，最终导出为 Word 文档。

**验收标准**：
- AC13.1：选择课程包后自动根据薄弱领域匹配干预项目生成 IEP
- AC13.2：IEP 表格支持编辑模式（添加/删除目标）
- AC13.3：支持自定义添加目标（领域+目标+阶段目标）
- AC13.4：删除操作有确认弹窗
- AC13.5：保存后数据持久化到 localStorage
- AC13.6：导出功能生成 Word 文档并下载

### R14：家长端报告

**用户故事**：作为家长，我需要查看孩子的评估报告，以通俗易懂的方式了解孩子的发展状况。

**验收标准**：
- AC14.1：不显示原始分数、P/E/F、A/M/S 等专业术语
- AC14.2：雷达图展示各领域发展概况
- AC14.3：进度条展示各领域表现等级（良好/中等/需关注）
- AC14.4：评估总结使用通俗语言描述
- AC14.5：根据 URL 参数 `tool` 适配不同工具的数据

### R15：评估量表明细（含回合统计展示）

**用户故事**：作为康复师，我需要在报告页查看每道题的评分明细和回合统计数据，以便复核评估结果。

**验收标准**：
- AC15.1：评估量表 Tab 左侧导航按分组/领域展示
- AC15.2：每道题卡片显示题号、描述、评分选项（选中项高亮）
- AC15.3：若有回合统计数据，在评分下方显示各回合结果（独立/错误/辅助，对应颜色标签）
- AC15.4：若有备注，显示备注内容
- AC15.5：领域信息栏显示统计摘要（各等级题数 + 得分率 + 堆叠进度条）


---

## 5. 后端需求

### 5.1 API 接口规范

#### 5.1.1 评估记录列表查询（含筛选）

```
GET /api/assessment/records?studentId={studentId}&status={status}
```

- 请求参数：
  - `studentId`（必填）：学生 ID
  - `status`（可选）：`all` | `completed` | `ongoing`
- 响应：
  ```json
  {
    "code": 200,
    "data": [{
      "id": "rec001",
      "toolId": "pep3",
      "toolName": "PEP-3",
      "date": "2024-01-15",
      "time": "2024-01-15 09:30:00",
      "status": "completed",
      "assessor": "李老师",
      "answeredCount": 174,
      "totalCount": 174
    }]
  }
  ```

#### 5.1.2 评估记录创建

```
POST /api/assessment/records
```

- 请求体：
  ```json
  {
    "studentId": "stu001",
    "toolId": "pep3",
    "assessor": "李老师"
  }
  ```
- 响应：返回新创建的记录对象（含自动生成的 `id`、`date`、`time`、`status=ongoing`）

#### 5.1.3 评估记录删除

```
DELETE /api/assessment/records/{recordId}
```

- 仅允许删除 `status=ongoing` 的记录
- 同时删除关联的答题数据

#### 5.1.4 评估记录状态更新（提交）

```
PUT /api/assessment/records/{recordId}/submit
```

- 请求体：
  ```json
  {
    "answeredCount": 174,
    "totalCount": 174
  }
  ```
- 操作：将 `status` 从 `ongoing` 更新为 `completed`

#### 5.1.5 答题数据保存（含回合统计）

```
PUT /api/assessment/answers/{recordId}
```

- 请求体：
  ```json
  {
    "answers": {
      "pep3_q1": {
        "value": 2,
        "label": "通过",
        "scoringMode": "rounds",
        "rounds": [
          {"round": 1, "result": "independent"},
          {"round": 2, "result": "error"},
          {"round": 3, "result": "prompted"}
        ],
        "independentRate": 0.33,
        "notes": "第一回合自发完成"
      }
    },
    "marks": {"pep3_q5": true},
    "scoringMode": "rounds"
  }
  ```

#### 5.1.6 答题数据查询

```
GET /api/assessment/answers/{recordId}
```

- 响应：返回完整答题数据对象（同保存格式）

#### 5.1.7 评估报告数据查询（含得分计算）

```
GET /api/assessment/reports/{recordId}
```

- 响应：返回计算后的报告数据，包含：
  - 各领域得分统计
  - 评级结果（P/E/F、A/M/S 等）
  - 雷达图数据
  - 自动生成的分析文本

#### 5.1.8 IEP 数据保存/查询

```
PUT /api/assessment/iep/{recordId}
GET /api/assessment/iep/{recordId}
```

- 数据结构：
  ```json
  {
    "coursePacketId": 1,
    "domains": [{
      "domain": "认知表达",
      "domainLabel": "1-2岁-沟通-语言表达",
      "goals": [{
        "name": "仿说",
        "stages": ["仿说单韵母", "仿说复韵母", "仿说词组"]
      }]
    }]
  }
  ```

#### 5.1.9 报告编辑内容保存

```
PUT /api/assessment/reports/{recordId}/edits
```

- 请求体：
  ```json
  {
    "eduOutline": "编辑后的教育训练纲要内容",
    "analysis": "编辑后的综合分析内容",
    "recommend": "编辑后的训练建议内容"
  }
  ```

#### 5.1.10 家长端报告查询

```
GET /api/assessment/reports/{recordId}/parent
```

- 响应：返回简化后的报告数据（不含原始分数和专业术语）

#### 5.1.11 评估工具配置查询（答题页用）

```
GET /api/assessment/tools/{toolId}/config
```

- 响应：返回题目配置数据（分组→领域→题目列表，含评分选项）

#### 5.1.12 评估类型配置查询

```
GET /api/assessment/types
```

- 响应：返回 `eval-type-config.json` 中的类型配置列表

### 5.2 数据模型（SQL）

#### 5.2.1 assessment_records（评估记录表）

```sql
CREATE TABLE assessment_records (
  id            VARCHAR(64)   PRIMARY KEY,
  student_id    VARCHAR(64)   NOT NULL,
  tool_id       VARCHAR(32)   NOT NULL,
  tool_name     VARCHAR(64)   NOT NULL,
  status        VARCHAR(16)   NOT NULL DEFAULT 'ongoing',  -- ongoing / completed
  assessor      VARCHAR(64),
  answered_count INT          DEFAULT 0,
  total_count   INT           DEFAULT 0,
  scoring_mode  VARCHAR(16)   DEFAULT 'rounds',  -- direct / rounds
  created_at    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_student_status (student_id, status),
  INDEX idx_created (created_at DESC)
);
```

#### 5.2.2 assessment_answers（答题数据表，含回合统计）

```sql
CREATE TABLE assessment_answers (
  id            BIGINT        AUTO_INCREMENT PRIMARY KEY,
  record_id     VARCHAR(64)   NOT NULL,
  question_id   VARCHAR(64)   NOT NULL,
  score_value   DECIMAL(3,1),                    -- 评分值（0, 0.5, 1, 2 等）
  score_label   VARCHAR(32),                     -- 评分标签（通过/萌芽/不通过等）
  scoring_mode  VARCHAR(16)   DEFAULT 'direct',  -- direct / rounds
  rounds_data   JSON,                            -- 回合统计数据 [{round:1, result:'independent'}, ...]
  independent_rate DECIMAL(5,4),                 -- 独立完成率
  notes         VARCHAR(200),                    -- 备注
  is_marked     TINYINT(1)    DEFAULT 0,         -- 是否标记待定
  created_at    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uk_record_question (record_id, question_id),
  INDEX idx_record (record_id)
);
```

#### 5.2.3 assessment_reports（评估报告表）

```sql
CREATE TABLE assessment_reports (
  id            BIGINT        AUTO_INCREMENT PRIMARY KEY,
  record_id     VARCHAR(64)   NOT NULL UNIQUE,
  report_data   JSON          NOT NULL,          -- 计算后的报告数据（领域得分、评级等）
  edit_data     JSON,                            -- 用户编辑的内容（教育纲要、综合分析等）
  created_at    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  INDEX idx_record (record_id)
);
```

#### 5.2.4 assessment_iep_plans（IEP 计划表）

```sql
CREATE TABLE assessment_iep_plans (
  id              BIGINT        AUTO_INCREMENT PRIMARY KEY,
  record_id       VARCHAR(64)   NOT NULL,
  course_packet_id INT,
  iep_data        JSON          NOT NULL,        -- IEP 完整数据（领域→目标→阶段目标）
  created_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at      DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  UNIQUE KEY uk_record_packet (record_id, course_packet_id),
  INDEX idx_record (record_id)
);
```

---

## 6. HTML 文件清单

### 6.1 PAD 端文件

| 文件名 | 功能 | 依赖关系 |
|--------|------|----------|
| `pad/assessment-list.html` | 评估记录列表页 | 入口页，跳转到 answer 或 result |
| `pad/assessment-answer.html` | 评估答题页（直接评分+回合统计） | 从 list 页进入，提交后跳转到 result |
| `pad/assessment-result.html` | 评估结果路由页 | 从 answer 页或 list 页进入，自动跳转到对应报告页 |
| `pad/assessment-result-pep3.html` | PEP-3 专属报告页 | 由 result 路由页跳转 |
| `pad/assessment-result-cpep.html` | C-PEP 专属报告页 | 由 result 路由页跳转 |
| `pad/assessment-result-vbmapp.html` | VB-MAPP 专属报告页 | 由 result 路由页跳转 |
| `pad/assessment-result-parent.html` | 家长端简化报告页 | 由报告页"发送报告"生成链接 |

### 6.2 手机端文件

| 文件名 | 功能 | 依赖关系 |
|--------|------|----------|
| `mobile/assessment-list.html` | 评估记录列表页（手机版） | 入口页 |
| `mobile/assessment-answer.html` | 评估答题页（单卡片+滑动） | 从 list 页进入 |
| `mobile/assessment-result.html` | 评估结果路由页 | 同 PAD 端逻辑 |
| `mobile/assessment-result-pep3.html` | PEP-3 报告页（手机版） | 由 result 路由页跳转 |
| `mobile/assessment-result-cpep.html` | C-PEP 报告页（手机版） | 由 result 路由页跳转 |
| `mobile/assessment-result-vbmapp.html` | VB-MAPP 报告页（手机版） | 由 result 路由页跳转 |
| `mobile/assessment-result-parent.html` | 家长端报告页（手机版） | 由报告页生成链接 |

### 6.3 页面跳转关系

```
assessment-list.html
  ├── [新建评估] → assessment-answer.html?record={id}&tool={toolId}
  ├── [继续评估] → assessment-answer.html?record={id}&tool={toolId}
  └── [查看] → assessment-result.html?record={id}&tool={toolId}
                  ├── → assessment-result-pep3.html?record={id}&tool=pep3
                  ├── → assessment-result-cpep.html?record={id}&tool=cpep
                  └── → assessment-result-vbmapp.html?record={id}&tool=vbmapp
                          └── [发送报告] → assessment-result-parent.html?tool={toolId}
```

---

## 7. 设计规范引用

本模块所有页面遵循 `design/DESIGN.md` Part B（康复师 App 端设计规范）：

- **主色**：蓝色 `#3B9BF5`，浅蓝底 `#EBF5FF`
- **页面背景**：`#F0F2F5`
- **卡片**：白色背景，16px 圆角，`0 2px 8px rgba(0,0,0,0.06)` 阴影
- **字体族**：`-apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", "Noto Sans SC", sans-serif`
- **评分按钮色**：红 `#F56C6C` / 橙 `#F5A623` / 绿 `#52C41A`
- **图表色板**：`#7EC8F0, #FFB88C, #FFD966, #7ED6A8, #B8A0E0, #FFB0C8, #A0D8EF`
- **导航选中态**：浅蓝背景 + 蓝色文字 + 左侧 3px 蓝色竖条

详细规范请参考 `design/DESIGN.md` Part B 各章节。

---

## 8. 数据流转说明

### 8.1 localStorage Key 映射

| Key | 说明 | 数据格式 |
|-----|------|----------|
| `rice_assessment_records` | 评估记录列表 | `[{id, toolId, toolName, date, time, status, assessor, answeredCount, totalCount}]` |
| `rice_assessment_tools` | 评估工具列表 | `[{id, name, desc, type, questionCount, estimatedTime, status}]` |
| `rice_assessment_answers_{recordId}` | 答题数据（含回合统计） | `{qId: {value, label, scoringMode, rounds, independentRate, notes}, _marks: {qId: bool}}` |
| `rice_assessment_config_{toolId}` | 评估工具题目配置 | `{groupName__domainName: [{id, number, itemName, desc, materials, ageRange, scores}]}` |
| `rice_assessment_current_record` | 当前评估记录 ID | `string` |
| `rice_assessment_current_tool` | 当前评估工具 ID | `string` |
| `rice_scoring_mode` | 评分模式 | `"direct"` 或 `"rounds"` |
| `rice_assessment_iep_{recordId}` | IEP 数据 | `[{domain, domainLabel, pct, goals: [{name, stages}]}]` |
| `rice_assessment_report_edit_{recordId}_{section}` | 报告编辑内容 | `string`（section: eduOutline/analysis/recommend） |
| `rice_assessment_eval_type_config` | 评估类型配置 | 同 `eval-type-config.json` 结构 |
| `rice_assessment_type_config` | 类型管理保存的配置 | 同上 |

### 8.2 页面间数据流转

```
[列表页]
  │ 写入: rice_assessment_records（创建/删除记录）
  │ 写入: rice_assessment_current_record / rice_assessment_current_tool
  │ 写入: rice_assessment_answers_{recordId}（测试数据生成）
  ▼
[答题页]
  │ 读取: rice_assessment_config_{toolId}（题目配置）
  │ 读取: rice_assessment_answers_{recordId}（恢复进度）
  │ 读取: rice_scoring_mode（评分模式）
  │ 写入: rice_assessment_answers_{recordId}（实时保存评分/备注/标记/回合数据）
  │ 写入: rice_scoring_mode（切换模式）
  │ 写入: rice_assessment_records（更新 answeredCount / status）
  ▼
[结果路由页]
  │ 读取: URL 参数 tool / record
  │ 读取: rice_assessment_tools（查找工具类型）
  │ 读取: rice_assessment_eval_type_config（查找报告页配置）
  ▼
[报告页 PEP-3/C-PEP/VB-MAPP]
  │ 读取: rice_assessment_answers_{recordId}（计算得分）
  │ 写入: rice_assessment_report_edit_{recordId}_{section}（编辑内容）
  │ 写入: rice_assessment_iep_{recordId}（IEP 数据）
  ▼
[家长端报告页]
  │ 读取: URL 参数 tool
  │ 使用硬编码或从报告页传递的简化数据
```

### 8.3 答题数据格式详解

```json
{
  "pep3_q1": {
    "value": 2,
    "label": "通过",
    "scoringMode": "rounds",
    "rounds": [
      {"round": 1, "result": "independent"},
      {"round": 2, "result": "error"},
      {"round": 3, "result": "prompted"}
    ],
    "independentRate": 0.33,
    "notes": "第一回合自发完成，后两回合注意力下降"
  },
  "pep3_q2": {
    "value": 1,
    "label": "萌芽",
    "scoringMode": "direct"
  },
  "_marks": {
    "pep3_q5": true,
    "pep3_q12": true
  }
}
```

- `value`：评分数值
- `label`：评分标签文字
- `scoringMode`：该题的评分方式（`direct` 或 `rounds`）
- `rounds`：回合统计数据数组，`result` 取值 `independent` / `error` / `prompted`
- `independentRate`：独立完成率（0-1）
- `notes`：备注文字（最多 200 字）
- `_marks`：待定标记映射，`true` 表示已标记
