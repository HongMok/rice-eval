# 设计规范

> 本文件包含不同端的设计规范，按端分区管理。

---

# Part A：后台管理端设计规范

> 从现有管理后台界面（课程包管理页）提炼，仅适用于后台管理端页面（`pad/admin-*.html`）。

---

## 1. 配色体系

### 主色（Primary）
| 用途 | 色值 | 说明 |
|------|------|------|
| 品牌紫 / 主操作按钮 | `#7C3AED` | 左侧导航高亮背景、主按钮（新增课程包等） |
| 主按钮悬停 | `#6D28D9` | hover 加深 |
| 导航选中背景 | `#7C3AED` | 左侧导航当前项，圆角矩形高亮 |
| 导航选中文字/图标 | `#FFFFFF` | 白色 |

### 中性色（Neutral）
| 用途 | 色值 |
|------|------|
| 页面背景 | `#F5F5F5` / `#F9FAFB` |
| 卡片/面板背景 | `#FFFFFF` |
| 卡片边框 | `#E5E7EB` |
| 分割线 | `#E5E7EB` |
| 正文文字 | `#1F2937` |
| 次要文字 / 描述 | `#6B7280` |
| 占位符文字 | `#9CA3AF` |
| 导航未选中文字 | `#6B7280` |
| 导航栏背景 | `#FFFFFF` |

### 语义色（Semantic）
| 用途 | 色值 | 说明 |
|------|------|------|
| 启用状态标签背景 | `#ECFDF5` | 浅绿底 |
| 启用状态标签文字 | `#059669` | 绿色文字 |
| 停用状态标签背景 | `#FFF7ED` | 浅橙底 |
| 停用状态标签文字 | `#EA580C` | 橙色文字 |
| 编辑链接 | `#7C3AED` | 紫色 |
| 停用/启用操作链接 | `#EA580C` / `#059669` | 橙/绿 |
| 危险操作（删除） | `#DC2626` | 红色 |

---

## 2. 字体与排版

| 元素 | 字号 | 字重 | 颜色 |
|------|------|------|------|
| 页面标题（如"课程包管理"） | 20px | 600 (Semi-Bold) | `#1F2937` |
| 卡片名称 | 16px | 600 | `#1F2937` |
| 卡片描述 | 13px | 400 | `#6B7280` |
| 卡片底部信息 | 12px | 400 | `#6B7280` |
| 操作链接 | 13px | 500 | `#7C3AED` / 语义色 |
| 状态标签 | 12px | 500 | 语义色 |
| 筛选区标签 | 13px | 400 | `#6B7280` |
| 输入框文字 | 14px | 400 | `#1F2937` |
| 按钮文字 | 14px | 500 | `#FFFFFF`（主按钮）/ `#1F2937`（次按钮） |
| 导航菜单文字 | 12px | 400 / 500(选中) | `#6B7280` / `#FFFFFF`(选中) |

- 字体族：`-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans SC", sans-serif`
- 行高：1.5（正文）、1.2（标题）

---

## 3. 间距与圆角

| 元素 | 数值 |
|------|------|
| 页面内边距（content area） | 24px |
| 卡片圆角 | 12px |
| 卡片内边距 | 16px ~ 20px |
| 卡片间距（grid gap） | 16px ~ 20px |
| 按钮圆角 | 8px |
| 输入框圆角 | 8px |
| 状态标签圆角 | 12px（pill 形） |
| 导航选中项圆角 | 8px |
| 弹窗圆角 | 12px |

---

## 4. 组件样式

### 4.1 左侧导航栏
- 宽度：约 80px（收起态，图标+文字竖排）/ 可展开至 200px
- 背景：`#FFFFFF`，右侧 1px `#E5E7EB` 分割线
- 导航项：图标（20px）+ 文字（12px）垂直居中排列，间距 4px
- 选中态：紫色圆角矩形背景 `#7C3AED`，图标和文字变白
- 未选中态：图标和文字 `#6B7280`
- 底部有收起/展开按钮 `<≡`
- 顶部显示主操作按钮（如"课程包"紫色按钮）

### 4.2 顶部栏
- 高度：约 56px
- 背景：`#FFFFFF`，底部 1px `#E5E7EB` 分割线
- 左侧：系统 Logo + 名称 "RICE AI 后台管理系统"
- 中间：面包屑导航（`< 返回` 链接）
- 右侧工具栏：搜索(⌘K)、全屏、刷新、设置、语言切换(En)、用户头像+名称+下拉

### 4.3 筛选条件区
- 背景：`#FFFFFF` 圆角面板，内边距 16px ~ 20px
- 布局：水平排列，左侧为筛选项（标签+输入框/下拉），右侧为搜索/重置按钮
- 输入框：高度 36px，边框 `#D1D5DB`，圆角 8px，placeholder `#9CA3AF`
- 下拉选择：同输入框样式，右侧箭头图标
- 搜索按钮：紫色主按钮 `#7C3AED`，白色文字，带搜索图标
- 重置按钮：白色底 + `#D1D5DB` 边框，灰色文字

### 4.4 卡片（列表项）
- 布局：网格，每行 3 列（PAD/Web），响应式可调
- 背景：`#FFFFFF`
- 边框：1px `#E5E7EB`，圆角 12px
- 阴影：`0 1px 3px rgba(0,0,0,0.05)` 或无阴影
- 内部结构（从上到下）：
  1. 头部行：左侧圆形图标（40px，带品牌色背景）+ 右上角状态标签（pill 形）
  2. 名称：16px Semi-Bold
  3. 描述：13px 灰色，1~2行
  4. 底部信息行：12px 灰色，多个信息用分隔符隔开（如 "超级管理员 · 回合/频次 · 一对一"）
  5. 操作行：编辑（紫色链接）、停用/启用（橙/绿色链接），右对齐或左对齐
- 悬停效果：可加轻微阴影提升 `box-shadow: 0 4px 12px rgba(0,0,0,0.08)`

### 4.5 主按钮（Primary Button）
- 背景：`#7C3AED`
- 文字：`#FFFFFF`，14px，500
- 圆角：8px
- 内边距：8px 16px
- 悬停：`#6D28D9`
- 示例：`新增课程包`、`新增评估工具`

### 4.6 次按钮（Secondary Button）
- 背景：`#FFFFFF`
- 边框：1px `#D1D5DB`
- 文字：`#374151`，14px，500
- 圆角：8px
- 悬停：背景 `#F9FAFB`
- 示例：`重置`、`取消`

### 4.7 状态标签（Tag / Badge）
- 形状：pill（圆角 12px）
- 内边距：2px 10px
- 启用：背景 `#ECFDF5`，文字 `#059669`，12px
- 停用：背景 `#FFF7ED`，文字 `#EA580C`，12px

### 4.8 输入框 / 下拉
- 高度：36px
- 边框：1px `#D1D5DB`
- 圆角：8px
- 内边距：0 12px
- 聚焦：边框变 `#7C3AED`，外发光 `0 0 0 2px rgba(124,58,237,0.2)`

### 4.9 弹窗（Modal / Dialog）
- 遮罩：`rgba(0,0,0,0.4)`
- 弹窗背景：`#FFFFFF`
- 圆角：12px
- 内边距：24px
- 标题：16px Semi-Bold
- 底部操作栏：右对齐，主按钮 + 次按钮

---

## 5. 布局规则

### 后台管理端（PAD/Web）
- 整体布局：左侧固定导航 + 右侧内容区
- 内容区最大宽度：不限（撑满剩余空间）
- 内容区内边距：24px
- 卡片网格：3列，gap 16~20px，响应式 ≤1024px 变 2列，≤768px 变 1列

### 手机端（康复师App）
- 单列全宽，max-width 420px，居中
- 底部 Tab 导航（固定底部）
- 内容区内边距：16px
- 卡片全宽，圆角 12px

### PAD端（康复师App）
- 可双列/左右分栏
- 内容区更宽，信息密度更高
- 导航可用侧边栏或顶部 Tab

---

## 6. 图标规范

- 导航图标：线性风格，20px，1.5px 描边
- 操作图标：16px
- 图标库建议：Lucide Icons / Heroicons（线性风格）
- 卡片圆形图标：40px 圆形，品牌色或渐变背景 + 白色图标

---

## 7. CSS 变量参考

```css
:root {
  /* 主色 */
  --color-primary: #7C3AED;
  --color-primary-hover: #6D28D9;
  --color-primary-light: #EDE9FE;

  /* 中性色 */
  --color-bg-page: #F5F5F5;
  --color-bg-card: #FFFFFF;
  --color-border: #E5E7EB;
  --color-border-input: #D1D5DB;
  --color-text-primary: #1F2937;
  --color-text-secondary: #6B7280;
  --color-text-placeholder: #9CA3AF;

  /* 语义色 */
  --color-success: #059669;
  --color-success-bg: #ECFDF5;
  --color-warning: #EA580C;
  --color-warning-bg: #FFF7ED;
  --color-danger: #DC2626;

  /* 圆角 */
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-pill: 9999px;

  /* 间距 */
  --spacing-xs: 4px;
  --spacing-sm: 8px;
  --spacing-md: 16px;
  --spacing-lg: 24px;
  --spacing-xl: 32px;

  /* 字体 */
  --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans SC", sans-serif;
  --font-size-xs: 12px;
  --font-size-sm: 13px;
  --font-size-base: 14px;
  --font-size-lg: 16px;
  --font-size-xl: 20px;

  /* 阴影 */
  --shadow-sm: 0 1px 3px rgba(0,0,0,0.05);
  --shadow-md: 0 4px 12px rgba(0,0,0,0.08);
  --shadow-lg: 0 8px 24px rgba(0,0,0,0.12);
}
```

---

## 8. 适用范围

本 Part A 设计规范仅适用于：
- 后台管理端页面（`pad/admin-*.html`），包括评估工具列表页、编辑页、批量导入弹窗等

不适用于：
- 康复师 App 手机端页面（`mobile/assessment-*.html`）
- 康复师 App PAD 端页面（`pad/assessment-*.html`）

> 康复师 App 端（答题交互、评估结果等页面）的设计规范将在收到 App 界面截图后，作为 Part B 补充到本文件中。

---

# Part B：康复师 App 端设计规范

> 从康复师 App 界面（学生康复概况页 PAD 端）提炼，适用于评估答题和评估结果相关页面（`mobile/assessment-*.html` 和 `pad/assessment-*.html`）。

---

## 1. 配色体系

### 主色（Primary）
| 用途 | 色值 | 说明 |
|------|------|------|
| 品牌蓝 / 主操作 | `#3B9BF5` | 导航选中背景、主按钮、链接色 |
| 主色浅底 | `#EBF5FF` | 导航选中项背景、轻量高亮 |
| 主色悬停 | `#2B8AE0` | hover 加深 |

### 中性色（Neutral）
| 用途 | 色值 |
|------|------|
| 页面背景 | `#F0F2F5` / `#F5F7FA` |
| 卡片/面板背景 | `#FFFFFF` |
| 卡片边框 | 无边框（靠阴影区分）或 `#E8ECF0` |
| 正文文字 | `#1A2233` |
| 次要文字 / 描述 | `#8C95A6` |
| 占位符文字 | `#B0B8C8` |
| 分割线 | `#E8ECF0` |
| 导航未选中文字 | `#5A6478` |
| 导航栏背景 | `#FFFFFF` |

### 语义色 / 多彩色板（用于图表和分类卡片）
| 用途 | 色值 | 说明 |
|------|------|------|
| 粉色系 | `#FFB0C8` / `#FFD6E4` | 动作发展等领域柱状图 |
| 橙色系 | `#FFB88C` / `#FFDCC8` | 游戏等领域 |
| 黄色系 | `#FFD966` / `#FFECB3` | 发音等领域 |
| 绿色系 | `#7ED6A8` / `#C8F0DC` | 沟通等领域 |
| 蓝色系 | `#7EC8F0` / `#C8E8FF` | 社交情绪/认知等领域 |
| 紫色系 | `#B8A0E0` / `#DDD0F0` | 生活自理等领域 |
| 青色系 | `#6DD4D4` / `#C0F0F0` | 行为管理等领域 |
| 核心特征卡片 | `#EBF5FF` 底 + `#3B9BF5` 图标 | 蓝色系信息卡片 |
| 干预重点卡片 | `#FFF4EB` 底 + `#F5A623` 图标 | 橙色系信息卡片 |
| 注意事项卡片 | `#FFF0F0` 底 + `#F56C6C` 图标 | 红色系信息卡片 |
| 成功/通过 | `#52C41A` | 绿色 |
| 进行中 | `#3B9BF5` | 蓝色 |
| 冻结/停用 | `#3B9BF5` | 蓝色链接 |

---

## 2. 字体与排版

| 元素 | 字号 | 字重 | 颜色 |
|------|------|------|------|
| 页面/区块标题（如"康复概况"） | 18px | 600 | `#1A2233` |
| 卡片标题（如"信息摘要"） | 16px | 600 | `#1A2233` |
| 子标题（如"核心特征"） | 15px | 600 | `#3B9BF5` / 语义色 |
| 正文 | 14px | 400 | `#1A2233` |
| 描述/说明文字 | 13px | 400 | `#8C95A6` |
| 数据数值（如"100%""57%"） | 14px | 600 | `#1A2233` |
| 图表标签 | 12px | 400 | `#5A6478` |
| 导航菜单文字 | 14px | 400 / 500(选中) | `#5A6478` / `#3B9BF5`(选中) |
| 操作链接 | 14px | 500 | `#3B9BF5` |

- 字体族：`-apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", "Noto Sans SC", sans-serif`
- 行高：1.6（正文）、1.3（标题）

---

## 3. 间距与圆角

| 元素 | 数值 |
|------|------|
| 页面内边距 | 20px（手机端 16px） |
| 卡片圆角 | 16px |
| 卡片内边距 | 20px（手机端 16px） |
| 卡片间距 | 16px |
| 信息子卡片圆角 | 12px |
| 按钮圆角 | 8px |
| 输入框圆角 | 8px |
| 头像圆角 | 50%（圆形） |
| 柱状图柱体圆角 | 8px（顶部） |
| 进度条圆角 | 9999px（pill） |

---

## 4. 组件样式

### 4.1 左侧导航栏（PAD端）
- 宽度：约 160px
- 背景：`#FFFFFF`
- 顶部：用户头像（圆形 48px）+ 姓名 + 性别图标 + 年龄
- 课程包选择器：下拉，带品牌色方块图标
- 导航项：图标（18px）+ 文字（14px）水平排列，左侧内边距 16px
- 选中态：浅蓝背景 `#EBF5FF`，文字和图标变蓝 `#3B9BF5`，左侧 3px 蓝色竖条
- 未选中态：文字 `#5A6478`，图标同色
- 导航项列表：康复概述、评估报告、1对1训练课、小组课、康复报告、残联报告
- 底部：操作链接（如"冻结"，蓝色文字）

### 4.2 顶部栏（PAD端）
- 高度：约 48px
- 背景：`#FFFFFF`
- 左侧：返回箭头 `<` + 排序/筛选图标
- 无系统级顶部栏（App 内嵌页面）

### 4.3 内容卡片
- 背景：`#FFFFFF`
- 圆角：16px
- 阴影：`0 2px 8px rgba(0,0,0,0.06)`
- 内边距：20px
- 标题行：标题文字 + 右侧操作链接/按钮（如"编辑摘要"、"AI生成"）

### 4.4 柱状图（康复概况）
- 柱体：渐变色，从深到浅（底部深、顶部浅），圆角顶部 8px
- 柱体宽度：约 48px，间距 12px
- 百分比数值：显示在柱体中间，白色文字 14px 600
- 底部标签：12px `#5A6478`
- 基准线：虚线，`#C8D0DC`
- 顶部统计：干预中 / 已通过 / 完成率，数值加粗

### 4.5 信息摘要卡片（三列彩色子卡片）
- 布局：3列等宽，gap 16px
- 每个子卡片：
  - 圆角 12px
  - 内边距 16px
  - 背景：对应语义浅色底（蓝/橙/红）
  - 顶部：圆形图标（24px）+ 标题（15px 600，对应深色）
  - 内容：14px 正文，`#1A2233`，行高 1.6
  - 列表项前缀：`·` 圆点

### 4.6 右侧面板（PAD端）
- 宽度：约 280px
- 包含：快捷操作按钮（资料库、AI历史对话）、AI建议区、家长反馈区
- 按钮样式：白底 + 浅灰边框，圆角 8px，图标+文字
- 空状态：插画图 + 灰色提示文字

### 4.7 主按钮（Primary Button）
- 背景：`#3B9BF5`
- 文字：`#FFFFFF`，14px，500
- 圆角：8px
- 内边距：8px 20px
- 悬停：`#2B8AE0`

### 4.8 次按钮 / 文字按钮
- 背景：`#FFFFFF` 或透明
- 边框：1px `#D8DDE5`（有边框时）
- 文字：`#3B9BF5`，14px，500
- 圆角：8px
- 示例：编辑摘要、AI生成

### 4.9 进度条
- 高度：6px ~ 8px
- 背景轨道：`#E8ECF0`
- 填充色：`#3B9BF5`（蓝色渐变）
- 圆角：9999px（pill）

### 4.10 评分按钮组（答题页专用）
- 手机端：底部固定，3个等宽按钮横排
  - 未选中：白底 + 灰边框
  - 选中：对应语义色填充 + 白色文字
  - PEP-3：0-不通过（`#F56C6C`红）/ 1-萌芽（`#F5A623`橙）/ 2-通过（`#52C41A`绿）
  - VB-MAPP：0（`#F56C6C`）/ 0.5（`#F5A623`）/ 1（`#52C41A`）
- PAD端：表格行内 radio 按钮组，同色系

### 4.11 题目卡片（手机端答题页）
- 背景：`#FFFFFF`
- 圆角：16px
- 阴影：`0 2px 8px rgba(0,0,0,0.06)`
- 内边距：20px
- 题号：14px 600 `#3B9BF5`
- 题目描述：16px 400 `#1A2233`
- 标记待定：文字链接 `#F5A623`，带旗帜图标

---

## 5. 布局规则

### PAD端（康复师App）
- 整体布局：左侧导航（160px）+ 中间内容区（flex: 1）+ 右侧面板（280px，可选）
- 内容区背景：`#F0F2F5`
- 内容区内边距：20px
- 答题页特殊布局：左侧子测验导航（200px）+ 右侧题目表格区

### 手机端（康复师App）
- 单列全宽，max-width 420px，居中
- 底部 Tab 导航（固定底部，高度 56px）
- Tab 项：图标（20px）+ 文字（10px），选中态蓝色 `#3B9BF5`，未选中 `#8C95A6`
- 内容区内边距：16px
- 答题页特殊布局：顶部进度条 + 中间题目卡片 + 底部评分按钮（固定底部）

---

## 6. 图标规范

- 导航图标：线性风格，18px，1.5px 描边
- 操作图标：16px
- 图标库建议：与后台管理端一致，Lucide Icons / Heroicons
- 特殊图标：AI 相关用 ✨ 星形，编辑用 ✏️ 铅笔，标记用 ⚑ 旗帜

---

## 7. CSS 变量参考

```css
/* === 康复师 App 端变量 === */
:root {
  /* 主色 */
  --app-color-primary: #3B9BF5;
  --app-color-primary-hover: #2B8AE0;
  --app-color-primary-light: #EBF5FF;

  /* 中性色 */
  --app-color-bg-page: #F0F2F5;
  --app-color-bg-card: #FFFFFF;
  --app-color-border: #E8ECF0;
  --app-color-text-primary: #1A2233;
  --app-color-text-secondary: #8C95A6;
  --app-color-text-placeholder: #B0B8C8;
  --app-color-text-nav: #5A6478;

  /* 语义色 */
  --app-color-success: #52C41A;
  --app-color-warning: #F5A623;
  --app-color-danger: #F56C6C;

  /* 信息卡片背景 */
  --app-color-info-blue-bg: #EBF5FF;
  --app-color-info-orange-bg: #FFF4EB;
  --app-color-info-red-bg: #FFF0F0;

  /* 图表多彩色板 */
  --app-chart-pink: #FFB0C8;
  --app-chart-orange: #FFB88C;
  --app-chart-yellow: #FFD966;
  --app-chart-green: #7ED6A8;
  --app-chart-blue: #7EC8F0;
  --app-chart-purple: #B8A0E0;
  --app-chart-cyan: #6DD4D4;

  /* 评分按钮色 */
  --app-score-fail: #F56C6C;
  --app-score-emerging: #F5A623;
  --app-score-pass: #52C41A;

  /* 圆角 */
  --app-radius-sm: 4px;
  --app-radius-md: 8px;
  --app-radius-lg: 12px;
  --app-radius-xl: 16px;
  --app-radius-pill: 9999px;

  /* 间距 */
  --app-spacing-xs: 4px;
  --app-spacing-sm: 8px;
  --app-spacing-md: 16px;
  --app-spacing-lg: 20px;
  --app-spacing-xl: 24px;

  /* 字体 */
  --app-font-family: -apple-system, BlinkMacSystemFont, "PingFang SC", "Helvetica Neue", "Noto Sans SC", sans-serif;

  /* 阴影 */
  --app-shadow-sm: 0 2px 8px rgba(0,0,0,0.06);
  --app-shadow-md: 0 4px 16px rgba(0,0,0,0.1);
}
```

---

## 8. 适用范围

本 Part B 设计规范适用于：
- 康复师 App 手机端页面（`mobile/assessment-*.html`）
- 康复师 App PAD 端页面（`pad/assessment-*.html`）

不适用于：
- 后台管理端页面（`pad/admin-*.html`）— 请参考 Part A
