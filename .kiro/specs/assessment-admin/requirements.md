# 评估工具后台管理系统 — 需求文档

## 1. 简介

本文档描述 RICE AI 后台管理系统中「评估工具管理」模块的完整需求。该模块供管理员使用，用于创建、编辑、导入和管理评估工具（如 PEP-3、C-PEP、VB-MAPP 及自定义通用评估工具），包括工具基本信息、评分体系、领域/子测验结构、题目内容和类型配置。

管理员通过此模块维护的评估工具数据，将直接供康复师 App 端的答题和报告功能使用。本模块仅在 Web/PAD 端运行（后台管理系统），不提供手机端界面。

后台管理系统整体风格：左侧导航栏采用图标+文字竖排布局（宽度约80px），紫色（#7C3AED）高亮当前选中项。导航项顺序：产品、订单、用户、学生、**评估**、课程包、学习、AI助手、营销、设置。顶部栏包含系统 logo（"RICE AI 后台管理系统"）、面包屑导航、搜索(⌘K)、全屏、刷新、设置、语言切换(En)、用户头像。

---

## 2. 术语表

| 术语 | 说明 |
|------|------|
| **评估工具** | 一套标准化评估量表的数字化配置，包含领域结构、题目和评分规则（如 PEP-3、VB-MAPP、C-PEP） |
| **评分体系（scoreOptions）** | 评估工具的评分选项配置，定义每个评分等级的分值、标签和说明。如 PEP-3 为 0-不通过/1-萌芽/2-通过，VB-MAPP 为 0/0.5/1。评分体系在题目级别配置，每道题可有独立的评分说明 |
| **子测验/领域（domain）** | 评估工具内的二级分组结构，PEP-3 称"子测验"（如认知/语前语言、语言表达），VB-MAPP 称"领域"（如 Mand、Tact） |
| **分组（group）** | 子测验/领域的上级分类（一级分类），如 PEP-3 的"发展性子测验""行为特征子测验""养育者报告"，VB-MAPP 的"Level 1 (0-18月)""Level 2 (18-30月)" |
| **类型配置（eval-type-config）** | 控制不同评估工具类型在答题页、报告页的行为差异的全局配置项，包括答题模式、卡片字段、评分说明显示等 |
| **后台管理系统** | RICE AI 后台管理系统，Web 端管理后台，管理员使用 |
| **康复师 App** | 评估师使用的移动端应用，支持手机和 PAD 两种屏幕，用于答题和查看评估结果 |
| **CSV 导入** | 通过 CSV/Excel 文件批量导入评估题目的功能，支持行级评分配置 |
| **行级评分** | 每道题自带独立的评分分值/标签/说明，通过 CSV 表头的 `评分_{字母}_{字段}` 格式列定义 |

---

## 3. 功能描述

### 3.1 评估工具列表管理

**用户角色**：管理员

**功能概述**：
管理员通过左侧导航栏【评估】菜单（位于【学生】和【课程包】之间）进入评估工具管理页面。页面以卡片网格布局（每行3个卡片）展示所有已配置的评估工具，支持搜索和筛选。

**卡片网格**：
- 布局：3列网格，gap 20px，响应式 ≤1024px 变2列，≤768px 变1列
- 每张卡片包含：
  - 左上角：圆形图标（40px，支持自定义头像上传，默认显示 📋 emoji）
  - 右上角：toggle switch 开关组件
    - 启用状态：绿色开关（#059669）+ "已启用"文案
    - 停用状态：灰白色开关（#D1D5DB）+ "已停用"文案
  - 工具名称：16px Semi-Bold
  - 描述文字：13px 灰色，最多2行截断（-webkit-line-clamp: 2）
  - 底部信息行：`题数: N题 · 修改: YYYY-MM-DD`（左对齐，题数/修改为灰色标题），"编辑"链接（右对齐，紫色 #7C3AED）
- 停用状态的卡片整体降低不透明度（opacity: 0.55），hover 时恢复到 0.85
- 卡片 hover 效果：box-shadow: 0 4px 12px rgba(0,0,0,0.08)
- 卡片网格末尾固定一张虚线边框卡片（"+ 新建评估工具"），点击弹出新建弹窗

**筛选条件区**：
- 白色圆角面板，内边距 16-20px
- 左侧：名称搜索输入框（240px）+ 状态下拉选择（全部状态/启用/停用，onchange 实时触发筛选）+ 搜索按钮（紫色主按钮）+ 重置按钮（白色次按钮）
- 右侧：「类型管理」按钮（紫色边框+紫色文字，带网格图标）

**业务规则**：
- 评估工具状态仅有两种：启用、停用
- 新建的评估工具默认为"停用"状态
- 停用状态的工具在康复师 App 新建评估弹窗中不可见
- 题目数量为 0 的工具不允许启用，系统提示"该评估工具尚无题目，无法启用"并阻止操作，开关恢复为停用状态
- 点击开关直接切换启用/停用状态，无需额外确认弹窗
- 搜索支持名称和描述的模糊匹配
- 类型显示名映射：pep3→"PEP-3 · 心理教育评估"，cpep→"C-PEP · 孤独症儿童发展评估"，vbmapp→"VB-MAPP · 语言行为里程碑评估"，common→"通用评估 · 综合型评估"

---

### 3.2 评估工具类型配置管理

**用户角色**：管理员

**功能概述**：
管理员通过列表页筛选区右侧的「类型管理」按钮打开类型配置弹窗，管理评估工具的类型配置。类型配置控制不同评估工具类型在答题页、报告页的行为差异。

**弹窗 UI**：
- 弹窗标题："评估类型配置管理"
- 说明文字："管理评估工具的类型配置，包括答题模式、卡片字段、评分说明显示、导航折叠和快捷操作等。修改后点击保存生效。"
- 类型列表：每个类型一个卡片区块（带边框），展示以下可编辑配置项：
  - 类型标识和名称（只读展示，如 "PEP-3 (pep3)"）
  - 工具简介（只读展示）
  - 答题模式（listMode）：下拉选择 — 按领域分组(byDomain) / 按题号排序(byOrder)
  - 显示评分说明（showScoreDesc）：下拉选择 — 是/否。`true` 表示每题评分说明不同需直接展示在评分按钮下方，`false` 表示统一标签在弹窗查看即可
  - 导航默认折叠（navCollapsedByDefault）：下拉选择 — 是/否。领域数量多时建议折叠
  - 允许未全作答提交（allowPartialSubmit）：下拉选择 — 否（必须全部作答）/ 是（可部分提交）
  - 卡片展示字段（cardFields）：多选复选框 — 评估项目名(itemName)、操作描述(desc)、所需材料(materials)、适用年龄(ageRange)
  - 底部快捷操作（quickActions）：多选复选框 — 一键不通过(failAll)、一键通过(passAll)、下一领域(nextDomain)
- 底部：取消 + 保存按钮

**类型配置数据结构**（参考 `eval-type-config.json`）：

| 类型ID | 名称 | 描述 | cardFields | showScoreDesc | navCollapsed | allowPartialSubmit |
|--------|------|------|------------|---------------|--------------|-------------------|
| pep3 | PEP-3 | 心理教育评估（Schopler修订版） | itemName, desc, materials | false | false | false |
| cpep | C-PEP | 孤独症儿童发展评估（中国残联版） | itemName, desc, materials, ageRange | true | true | false |
| vbmapp | VB-MAPP | 语言行为里程碑评估 | itemName, desc | false | false | false |
| common | 通用评估 | 综合型评估（适用于自定义评估工具） | itemName, desc, materials, ageRange | true | false | true |

**报告配置**（reportConfig，只读展示）：

| 类型ID | reportPage | reportTitle |
|--------|-----------|-------------|
| pep3 | assessment-result-pep3.html | PEP-3 心理教育评估报告 |
| cpep | assessment-result-cpep.html | C-PEP 孤独症儿童发展评估报告 |
| vbmapp | assessment-result-vbmapp.html | VB-MAPP 语言行为里程碑评估报告 |
| common | assessment-result.html | 评估报告 |

---

### 3.3 评估工具编辑

**用户角色**：管理员

**功能概述**：
管理员从列表页点击"编辑"进入编辑页，管理评估工具的基本信息、领域结构和题目内容。

#### 3.3.1 基本信息区

- 默认只读展示：头像（32px 圆形）+ 名称 + 类型 + 描述，右上角"编辑"链接（紫色）
- 点击"编辑"弹出右侧抽屉（宽度 520px），包含：
  - 工具图标：64px 圆形，点击上传图片，虚线边框
  - 名称输入框（200px，必填，带红色 * 标记）
  - 类型：已创建的工具类型只读显示（灰色背景输入框），不允许修改；新建时显示自定义下拉组件
  - 描述 textarea（80px 高度，可拉伸）
  - 底部分割线下方："删除此评估工具"红色链接
    - 删除前置条件：工具必须先停用才能删除，否则提示"请先停用该评估工具后再删除"
    - 删除确认弹窗："确定要删除评估工具"XXX"吗？该工具下的所有题目配置将被永久删除，历史评估记录不受影响。此操作无法恢复。"
  - 抽屉底部：取消 + 保存按钮

#### 3.3.2 评分体系配置

- 评分体系在题目级别配置（每道题的 scores 数组），不在工具级别统一配置
- 预设评分体系（用于新建题目时的默认值）：
  - PEP-3：2-通过 / 1-萌芽 / 0-不通过
  - C-PEP：1-通过 / 0.5-中间反应 / 0-不通过
  - VB-MAPP：1-1分 / 0.5-0.5分 / 0-0分
- 新增题目时，自动从同领域已有题目复制评分结构（分值和标签），说明留空
- 如果领域内无已有题目，则 fallback 到工具类型对应的预设评分体系

#### 3.3.3 领域结构树

- 左侧树面板（280px），标题"领域目录"，右上角"编辑"按钮切换编辑模式
- 树形结构为两级：分组（group）→ 子测验/领域（domain）
- 普通模式：
  - 点击分组标题可折叠/展开子项（▼ 箭头旋转动画）
  - 点击子项选中，右侧加载该领域的题目列表
  - 选中项高亮：紫色浅底（#EDE9FE）+ 紫色文字 + 紫色圆点
- 编辑模式（点击"编辑"按钮后）：
  - 按钮区变为"取消"（灰色文字链接）+ "保存"（紫色实心小按钮）
  - 编辑区外覆盖半透明遮罩层，树面板提升 z-index
  - 分组节点 hover 显示操作图标：✏️ 改名、🗑 删除
  - 子项节点 hover 显示操作图标：✏️ 改名、🗑 删除
  - 每个分组底部显示"+ 添加子组"链接
  - 树底部显示"+ 添加分组"链接
- 添加分组：弹出弹窗输入分组名称
- 添加子项：弹出弹窗输入子测验/领域名称
- 重命名：弹出弹窗，预填当前名称
- 删除分组：确认弹窗显示"该分组下共有 N 道题目将被一并删除"
- 删除子项：确认弹窗显示"该子组下共有 N 道题目将被一并删除"

**预设领域结构**：

PEP-3 结构：
```
发展性子测验
  ├ 认知/语前语言
  ├ 语言表达
  ├ 语言理解
  ├ 精细动作
  ├ 粗大动作
  └ 视觉动作模仿
行为特征子测验
  ├ 情感表达
  ├ 社会互动
  ├ 非语言行为特征
  └ 语言行为特征
养育者报告
  ├ 问题行为
  ├ 个人自理
  └ 适应行为
```

VB-MAPP 结构：
```
Level 1 (0-18月)
  ├ Mand(要求)、Tact(命名)、Listener(听者反应)、VP/MTS(视觉配对)
  ├ Play(游戏)、Social(社交)、Imitation(模仿)、Echoic(仿说)、LRFFC(听者功能)
Level 2 (18-30月)
  ├ Mand、Tact、Listener、VP/MTS、Play、Social
  ├ Reading(阅读)、Writing(书写)、LRFFC、Intraverbal(对话)
Level 3 (30-48月)
  ├ Mand、Tact、Listener、VP/MTS、Play、Social
  ├ Reading、Writing、LRFFC、Intraverbal、Group(团体)、Linguistics(语言结构)
障碍评估
  ├ 行为障碍、注意力障碍、社交障碍
转衔评估
  └ 转衔技能
```

C-PEP 结构：
```
感知觉
  ├ 视觉注视、视觉追踪、听觉、触觉、嗅觉、味觉、本体觉、前庭觉
精细动作
  ├ 手指精细动作、手眼协调、双手协调、工具使用
大运动
  ├ 坐、站、走、跑跳、平衡、球类
言语/语言
  ├ 语前技能、语言理解、语言表达、对话
认知
  ├ 注意力、记忆、概念、推理
社会交往
  ├ 社会认知、社会互动、游戏、情绪
自理
  ├ 进食、穿衣、如厕、个人卫生
```

#### 3.3.4 题目管理

- 右侧题目面板，标题显示当前选中领域名称 + "— 题目列表"
- 顶部操作按钮：「+ 添加题目」（紫色主按钮）
- 题目以表格形式展示，列包含：
  - 排序号（紫色加粗，可点击切换升序/降序）
  - 评估项目（itemName）
  - 操作描述（desc，截断显示，hover 显示完整 title）
  - 所需材料
  - 适用年龄
  - 是否必答（绿色"是" / 灰色"否"）
  - 启用状态（绿色"已启用" / 灰色"已停用"）
  - 评分等级列（动态列数，根据题目 scores 数组渲染，每个等级拆为3列：分值、标签、说明）
  - 操作列（固定在右侧，sticky 定位）：编辑（紫色链接）、删除（红色链接）
- 表格表头 sticky 定位，内容区可滚动
- 操作列有左侧阴影效果（box-shadow: -4px 0 8px rgba(0,0,0,0.04)）

#### 3.3.5 题目编辑抽屉

- 从右侧滑出，宽度 520px，带遮罩层
- 标题：新增时"添加题目"，编辑时"编辑题目"
- 核心字段（始终展示）：
  - 排序号（number 输入框，100px，必填）
  - 评估项目名称（text 输入框，必填）
  - 操作描述（textarea，80px 高度，可拉伸）
  - 评分说明区域（根据工具 scoreOptions 动态渲染）：
    - 每个评分等级一个卡片区块（灰色背景 #F9FAFB，圆角 8px）
    - 卡片标题："评分等级 A/B/C..."（紫色加粗）
    - 分值输入框（80px，number 类型，step=0.5）
    - 标签输入框（必填，如"通过/萌芽/不通过"）
    - 说明 textarea（48px 高度，可拉伸）
- 扩展字段（默认折叠，点击"扩展字段"展开；如果已有数据则自动展开）：
  - 所需材料（text 输入框）
  - 适用年龄（text 输入框，如"12-24月"）
  - 是否必答（下拉：是/否）
  - 启用状态（toggle 开关）
- 底部：取消 + 保存按钮
- 保存时校验：排序号必填、评估项目必填、评分标签必填

---

### 3.4 评估工具新建

**用户角色**：管理员

**功能概述**：
管理员点击列表页末尾的虚线卡片（"+ 新建评估工具"），弹出新建弹窗。

**弹窗 UI**：
- 弹窗标题："新建评估工具"，右上角关闭按钮
- 副标题："请先填写基本信息，然后选择配置方式"

**基本信息区**：
- 工具图标：64px 圆形，点击上传图片，虚线边框，默认显示 📋
- 名称输入框（180px，必填，带红色 * 标记）
- 类型自定义下拉组件（非原生 select），展示类型名称和描述：
  - PEP-3 · 心理教育评估 — Schopler修订版，适用于2-7.5岁儿童
  - C-PEP · 孤独症儿童发展评估（残联版） — 中国残联版，适用于0-7岁孤独症儿童
  - VB-MAPP · 语言行为里程碑评估 — 基于ABA原理评估语言和社交技能
  - 通用评估 · 综合型评估 — 适用于自定义评估工具
- 描述 textarea（80px 高度）
- 选择类型后，如果描述为空，自动填入该类型的工具简介（intro 字段）

**配置方式选择区**：
- 两张等宽卡片横排，hover 时紫色边框 + 阴影
- 📥 表格录入：下载模板，填写评估题目后上传导入
- ✏️ 手动录入：在线逐条添加评估领域和题目

**表单校验**：
- 名称为空时提示"请输入评估工具名称"
- 类型未选时提示"请选择评估工具类型"
- 名称重复时提示"评估工具名称"XXX"已存在，请使用其他名称"

**手动录入流程**：
1. 校验通过后创建工具（status=inactive, questionCount=0）
2. 跳转到编辑页（admin-assessment-edit.html?id=xxx）
3. 编辑页完全空白，左侧显示"暂无领域结构，请添加分组"提示

**表格导入流程**：
1. 校验通过后弹窗内切换到导入步骤（隐藏基本信息和配置方式选择区）
2. 副标题变为"下载模板并填写评估题目，然后上传导入"
3. 展示导入三步流程（详见 3.5 批量导入）

---

### 3.5 批量导入

**用户角色**：管理员

**功能概述**：
管理员通过新建弹窗的"表格导入"或编辑页的导入入口，上传 Excel/CSV 文件批量录入评估题目。

**导入入口**：
- 新建弹窗 → 选择"表格导入" → 弹窗内展示导入步骤
- 编辑页 → 独立导入页面（admin-assessment-import.html）

**三步流程**：

**第1步：下载模板**
- 提供两套预设模板下载链接：
  - 📄 下载 PEP-3 模板（pep3-import-template.csv）
  - 📄 下载 VB-MAPP 模板（vbmapp-import-template.csv）
- 支持 Excel (.xlsx) 和 CSV (.csv) 两种格式

**第2步：上传文件**
- 拖拽上传区域（虚线边框，支持拖拽和点击选择）
- 支持格式：.xlsx, .csv
- 上传后显示文件信息（文件名 + 移除按钮）
- 上传区域隐藏，显示文件信息条（绿色背景）

**第3步：预览数据**
- 解析文件后展示预览表格：题号、子测验/领域、题目描述、评分选项、状态
- 异常行红色背景高亮，状态列显示 ❌ 异常
- 底部统计：共 N 条，有效 N 条，异常 N 条（异常数 > 0 时红色显示）
- 确认导入按钮（预览数据后才可点击）

**导入结果**：
- 隐藏三步流程，显示导入结果：✅ 导入完成
- 结果详情：成功导入 N 条，失败 N 条
- 底部按钮变为"返回编辑页"

**评分体系解析规则说明**（紫色提示卡片）：
- 标题："📌 CSV 表头格式说明"
- 内容：评分列采用行级配置，列名格式为 `评分_{字母}_{字段}`，字段包括 分值/标签/说明
- 示例：`评分_a_分值`、`评分_a_标签`、`评分_a_说明`
- 说明：每道题自带评分分值/标签/说明，动态列数，用字母编号（a, b, c, ...）

---

### 3.6 CSV 导入解析规则

#### 3.6.1 CSV 表头格式

必填列：
| 列名 | 说明 | 是否必填 |
|------|------|---------|
| 排序 | 题目排序号 | 否（缺失时自动递增） |
| 一级分类 | 分组名称（group） | **是** |
| 二级分类 | 子测验/领域名称（domain） | **是** |
| 评估项目 | 题目简短名称（itemName） | 否 |
| 操作描述 | 题目详细描述（desc） | **是** |
| 所需材料 | 评估所需教具 | 否 |
| 适用年龄 | 如 12-24月 | 否 |
| 是否必答 | "是"或"否" | 否（默认"是"） |

评分列（动态列数）：
| 列名格式 | 说明 |
|----------|------|
| `评分_a_分值` | 第1个评分等级的分值（如 0） |
| `评分_a_标签` | 第1个评分等级的标签（如 "不通过"） |
| `评分_a_说明` | 第1个评分等级的说明（如 "无反应或无法完成"） |
| `评分_b_分值` | 第2个评分等级的分值（如 1） |
| `评分_b_标签` | 第2个评分等级的标签（如 "萌芽"） |
| `评分_b_说明` | 第2个评分等级的说明 |
| `评分_c_分值` | 第3个评分等级的分值（如 2） |
| `评分_c_标签` | 第3个评分等级的标签（如 "通过"） |
| `评分_c_说明` | 第3个评分等级的说明 |
| ... | 可继续扩展 d, e, f... |

#### 3.6.2 解析逻辑

1. 读取表头行，识别所有列的索引位置
2. 通过正则 `^评分_([a-z])_(分值|标签|说明)$` 匹配评分列
3. 按字母排序评分列组（a, b, c, ...），构建 scoreColMap
4. 逐行解析数据：
   - 缺少一级分类或二级分类的行标记为无效（invalidCount++），跳过
   - 构建 domainKey = `{一级分类}__{二级分类}`
   - 每行生成一个 Question 对象，scores 数组从评分列动态构建
5. 解析完成后返回：config（按 domainKey 分组的题目数据）、totalCount、invalidCount

#### 3.6.3 CSV 文件格式规范

- 所有字段一律用双引号包裹（QUOTE_ALL）
- 字段内容包含双引号时用两个双引号转义
- 统一使用 UTF-8 编码，不带 BOM
- Excel (.xlsx) 文件使用 SheetJS 库解析

---

### 3.7 课包干预目标关联

**用户角色**：管理员

**功能概述**：
管理员在评估工具编辑页中，为评估工具关联课包的干预目标。关联数据用于康复师 App 端生成 IEP 时，自动匹配评估结果对应的干预项目。

#### 3.7.1 课包关联栏

- **位置**：评估工具编辑页，基本信息区和评估项目列表之间
- **展示**：横向排列所有课包图标（48px 紫色圆形 + 文字缩写）+ 课包名称
- **状态**：
  - 已启用：图标正常显示，右上角绿色勾（16px 圆形 + 白色 ✓）
  - 未启用：图标灰度（filter: grayscale(1) opacity(0.5)），名称灰色
- **交互**：点击任意课包图标进入全屏干预目标关联界面
- **数据源**：课包列表从 `config/course-packets.json` 读取（id, name, brief, icon）
- **默认状态**：RICE1v1 默认启用，其他课包默认关闭

#### 3.7.2 全屏关联界面

**顶部栏**：
- 返回按钮（SVG 箭头图标）
- 课包名称（16px 加粗）
- 关联备注（灰底标签，格式：`评估工具「PEP-3」↔ 课包「RICE1v1」`）
- 匹配进度（`X/Y 已匹配`，仅预设匹配模式显示）
- 启用/关闭 toggle（右对齐，切换时弹窗确认）

**模式选择**（两张卡片，单选）：
- **预设匹配**：每个评估项目和课包内干预项目做匹配，可手动编辑或AI自动匹配
- **规则匹配**：不做预设匹配，提供匹配规则文本，AI在生成IEP时自动匹配

切换模式时弹窗确认（如果当前模式有数据）。

#### 3.7.3 预设匹配模式

**子模式切换**（radio pills）：
- **评估项目匹配**：按评估项目为单位，每个评估项目可关联多个干预目标（一对多）
- **评估分数匹配**：同一评估项目下，不同评分等级分别匹配不同干预目标（也是一对多）

切换子模式时弹窗确认（如果有匹配数据，切换会清空）。

**左侧目录树**（260px）：
- 和评估工具编辑页左侧树一致的视觉风格
- 分组 → 子领域两层结构
- 每个子领域显示匹配进度（如 `3/10`），颜色：全匹配=绿色，部分=紫色，无=灰色
- 点击子领域切换右侧详情

**右侧详情面板**：
- 表头4列：题号 | 评估项目 | 匹配的干预目标 | 操作
- 表头使用 `pf-q-row` 同结构对齐，灰底（#F9FAFB），高度 44px
- 每行显示：
  - 题号（紫色加粗）
  - 评估项目标题（14px 加粗）+ 描述（12px 灰色，单行省略号截断）
  - 匹配的干预目标名称（加粗）+ 下方领域标签（紫色一级领域 + 橙色二级细分领域）
  - 操作按钮（设置/编辑/删除）
- 评估分数匹配子模式下：
  - 主行显示评估项目 + 配置状态（已配置/部分配置/未配置）
  - 子行按评分等级展开，评分标签在"评估项目"列，干预目标在"匹配的干预目标"列
  - 配置状态判断：所有评分等级都配置了=已配置（绿色），部分=部分配置（橙色），无=未配置（灰色）

**匹配完成度**（2层）：
- 顶部栏：整体 `已匹配 X/Y`
- 左侧树每个子领域：`X/Y`

**AI自动匹配**：
- 按钮使用机器人 SVG 图标
- 点击弹确认（如果已有匹配数据，提示会清空）
- 匹配完成后所有评估项目都有对应的干预目标
- 按领域关键词智能匹配

**导出关联表**：
- 按钮在AI自动匹配左边，白底灰边样式 + 下载 SVG 图标
- 导出 CSV 文件，表头9列：评估项目题号、评估项目、评估项目描述、评估项目评分、评估项目评分标签、关联干预项目ID、关联干预项目、关联干预项目大领域、关联干预项目子领域
- 评估分数匹配模式下同一评估项目按评分等级展开多行
- 所有字段 QUOTE_ALL，UTF-8 BOM 编码

#### 3.7.4 匹配设置抽屉

- 从右侧滑出，宽度 480px，带遮罩层
- 顶部：评估项目名称（加粗）+ 描述（灰色小字）
- 搜索框：支持多关键词空格分隔（AND 逻辑），最大50字符，实时搜索
- 默认展示 AI 推荐列表（基于评估项目领域智能推荐），顶部紫色"☆ AI推荐"标签 + 右侧"刷新"按钮
- 输入搜索后切换为搜索结果，输入框右侧出现 × 清除按钮，清除后回到 AI 推荐
- 干预目标列表项：紫色一级领域标签 + 橙色二级细分领域标签 + 项目名称
- 支持多选（toggle 选中/取消），已选项以紫色标签展示（带 × 删除按钮）
- 底部：取消 + 保存按钮

#### 3.7.5 规则匹配模式

**查看模式（默认）**：
- 规则文本以只读灰底区块展示（pre-wrap，可滚动，max-height 400px）
- 右上角"编辑"链接
- 底部提示："AI在生成IEP时会参考此规则文本自动匹配干预目标"

**编辑模式（弹窗）**：
- 点击"编辑"弹出 860px 宽、80vh 高的居中弹窗
- 顶部栏：标题"编辑匹配规则" + AI润色按钮（机器人 SVG 图标）
- 大面积 textarea 可编辑
- AI润色只替换文本框内容，不自动保存
- 底部：取消 + 保存按钮
- 取消/关闭不保存

#### 3.7.6 干预目标数据结构

干预目标为3层架构：
- **territory**（一级领域）：如"动作发展""沟通""认知""社交情绪""游戏""发音""生活自理""学习行为"
- **subdomain**（二级细分领域）：如"粗大动作""精细动作""语言理解""语言表达""配对""模仿"
- **name**（项目名称）：如"多种基本姿势""走台阶""仿说""轮流"

#### 3.7.7 数据存储

- localStorage key：`rice_assessment_packet_bindings_{toolId}`
- 存储格式：
```json
{
  "packetId": {
    "enabled": true,
    "mode": 1,
    "presetSubMode": "item",
    "matchRule": "...",
    "matches": {
      "questionId": {
        "targets": [{ "projectName": "...", "stages": [] }]
      }
    }
  }
}
```
- 评估分数匹配模式下 matches 格式：
```json
{
  "questionId": {
    "scoreTargets": {
      "2": [{ "projectName": "...", "stages": [] }],
      "1": [{ "projectName": "...", "stages": [] }],
      "0": [{ "projectName": "...", "stages": [] }]
    }
  }
}
```

---

## 4. 需求描述（EARS 格式）

### Requirement 1：评估工具列表管理

**User Story:** 作为管理员，我希望能查看和管理所有评估工具，以便对评估配置进行统一管理。

#### Acceptance Criteria

1. WHEN 管理员点击左侧导航【评估】菜单（位于【学生】和【课程包】之间）, THE 后台管理系统 SHALL 展示评估工具管理页面，采用卡片网格布局（每行3个卡片）展示所有已配置的评估工具
2. THE 评估工具卡片 SHALL 展示评估工具的圆形图标（支持自定义头像）、名称（16px 600）、描述（13px 灰色，2行截断）、右上角 toggle switch 开关组件（绿色"已启用"或灰白"已停用"）、底部信息行（类型显示名·题目数·修改时间 左对齐，"编辑"链接右对齐）
3. WHEN 管理员在筛选条件区输入名称关键词, THE 评估工具列表 SHALL 按名称和描述进行模糊匹配筛选
4. WHEN 管理员在状态下拉中选择状态（onchange 实时触发）, THE 评估工具列表 SHALL 立即按状态筛选并刷新卡片展示，无需点击搜索按钮
5. WHEN 管理员点击搜索按钮, THE 评估工具列表 SHALL 同时按名称关键词和状态条件筛选
6. WHEN 管理员点击重置按钮, THE 筛选条件 SHALL 清空并恢复展示全部评估工具
7. THE 卡片网格末尾 SHALL 固定展示一张虚线边框卡片（"+ 新建评估工具"），hover 时紫色边框 + 阴影效果，WHEN 管理员点击该卡片, THE 后台管理系统 SHALL 弹出"新建评估工具"弹窗
8. WHEN 管理员点击某张评估工具卡片底部的【编辑】链接, THE 后台管理系统 SHALL 跳转到该评估工具的编辑页（admin-assessment-edit.html?id=xxx）并加载已有数据
9. THE 评估工具卡片 SHALL 对停用状态的卡片整体降低不透明度（opacity: 0.55），hover 时恢复到 0.85，与启用卡片形成明显视觉区分
10. THE 卡片 hover 效果 SHALL 添加阴影（box-shadow: 0 4px 12px rgba(0,0,0,0.08)）

### Requirement 2：评估工具启用/停用管理

**User Story:** 作为管理员，我希望能控制评估工具的启用状态，以便管理哪些评估工具可供评估师使用。

#### Acceptance Criteria

1. WHEN 管理员在列表页卡片右上角将 toggle switch 开关从"已停用"切换为"已启用", THE 后台管理系统 SHALL 将该评估工具状态变更为"启用"，开关变为绿色（#059669）并显示"已启用"文案，卡片恢复正常不透明度
2. WHEN 管理员在列表页卡片右上角将 toggle switch 开关从"已启用"切换为"已停用", THE 后台管理系统 SHALL 将该评估工具状态变更为"停用"，开关变为灰白色（#D1D5DB）并显示"已停用"文案，卡片降低不透明度
3. THE 后台管理系统 SHALL 将新建的评估工具默认设置为"停用"状态
4. WHILE 评估工具状态为"停用", THE 康复师App SHALL 在新建评估弹窗中隐藏该评估工具，不可选择
5. IF 管理员尝试启用一个题目数量为0的评估工具, THEN THE 后台管理系统 SHALL 提示"该评估工具尚无题目，无法启用"并阻止操作，开关自动恢复为停用状态
6. THE 启用/停用切换 SHALL 无需额外确认弹窗，点击开关直接生效

### Requirement 3：新建评估工具

**User Story:** 作为管理员，我希望能创建新的评估工具，以便扩展系统支持的评估量表。

#### Acceptance Criteria

1. WHEN 管理员点击列表页末尾的虚线卡片"+ 新建评估工具", THE 后台管理系统 SHALL 弹出新建弹窗，包含基本信息填写区和配置方式选择区
2. THE 新建弹窗基本信息区 SHALL 包含：工具图标上传（64px 圆形，点击上传）、名称输入框（180px，必填）、类型自定义下拉组件（展示类型名称和描述，必填）、描述 textarea
3. THE 类型下拉组件 SHALL 使用自定义 HTML 组件（非原生 select），每个选项展示类型名称（14px 500）和描述（12px 灰色）
4. WHEN 管理员选择类型后, IF 描述 textarea 为空, THEN THE 系统 SHALL 自动填入该类型的工具简介（intro 字段）
5. IF 管理员未填写名称就选择配置方式, THEN THE 系统 SHALL 提示"请输入评估工具名称"
6. IF 管理员未选择类型就选择配置方式, THEN THE 系统 SHALL 提示"请选择评估工具类型"
7. IF 管理员输入的名称与已有工具重复, THEN THE 系统 SHALL 提示"评估工具名称"XXX"已存在，请使用其他名称"
8. WHEN 管理员选择"手动录入", THE 系统 SHALL 创建工具（status=inactive, questionCount=0）并跳转到空白编辑页，左侧显示"暂无领域结构，请添加分组"提示
9. WHEN 管理员选择"表格导入", THE 弹窗 SHALL 切换到导入步骤界面（隐藏基本信息和配置方式选择区），展示模板下载、文件上传和预览流程
10. WHEN 管理员在导入步骤点击"返回", THE 弹窗 SHALL 恢复到基本信息和配置方式选择界面，清除已上传的文件和预览数据

### Requirement 4：评估工具编辑 — 基本信息

**User Story:** 作为管理员，我希望能编辑评估工具的基本信息，以便维护工具的名称、描述和图标。

#### Acceptance Criteria

1. THE 评估工具编辑页顶部 SHALL 展示面包屑导航（"< 返回" 链接 + 工具名称），点击返回跳转到列表页
2. THE 基本信息栏 SHALL 默认只读展示：头像（32px 圆形）+ "名称: XXX" + "类型: XXX" + "描述: XXX"，右上角"编辑"链接
3. WHEN 管理员点击"编辑"链接, THE 编辑页 SHALL 弹出右侧抽屉（520px），带遮罩层，包含工具图标上传、名称输入、类型（只读）、描述 textarea
4. THE 抽屉内类型字段 SHALL 对已创建的工具显示为只读文本（灰色背景），不允许修改
5. THE 抽屉底部 SHALL 提供"删除此评估工具"红色链接
6. IF 管理员点击"删除此评估工具"且工具状态为"启用", THEN THE 系统 SHALL 提示"请先停用该评估工具后再删除"
7. IF 管理员点击"删除此评估工具"且工具状态为"停用", THEN THE 系统 SHALL 弹出确认弹窗，确认后删除工具及其所有领域和题目配置，跳转回列表页
8. WHEN 管理员在抽屉中修改信息并点击"保存", THE 系统 SHALL 保存修改并更新只读展示区的内容

### Requirement 5：评估工具编辑 — 领域结构管理

**User Story:** 作为管理员，我希望能管理评估工具的领域/子测验结构，以便构建完整的评估框架。

#### Acceptance Criteria

1. THE 编辑页左侧 SHALL 展示领域目录树面板（280px），标题"领域目录"，右上角"编辑"按钮
2. THE 领域树 SHALL 支持两级结构：分组（group，可折叠/展开）→ 子测验/领域（domain，可点击选中）
3. WHEN 管理员点击"编辑"按钮, THE 树面板 SHALL 进入编辑模式：按钮区变为"取消"+紫色"保存"，编辑区外覆盖遮罩层，节点 hover 显示 ✏️ 改名和 🗑 删除图标按钮
4. WHEN 管理员在编辑模式点击"+ 添加分组", THE 系统 SHALL 弹出弹窗输入分组名称，确认后在树底部新增分组节点
5. WHEN 管理员在编辑模式点击某分组下的"+ 添加子组", THE 系统 SHALL 弹出弹窗输入子测验/领域名称，确认后在该分组下新增子项节点
6. WHEN 管理员点击节点的 ✏️ 改名按钮, THE 系统 SHALL 弹出弹窗预填当前名称，确认后更新节点名称，同时更新关联的题目数据的 domainKey
7. IF 管理员点击分组的 🗑 删除按钮, THEN THE 系统 SHALL 弹出确认弹窗"确定要删除分组"XXX"吗？该分组下共有 N 道题目将被一并删除，此操作无法恢复。"
8. IF 管理员点击子项的 🗑 删除按钮, THEN THE 系统 SHALL 弹出确认弹窗"确定要删除子组"XXX"吗？该子组下共有 N 道题目将被一并删除，此操作无法恢复。"
9. WHEN 管理员点击某个子测验/领域节点（非编辑模式）, THE 编辑页 SHALL 在右侧题目表格区域展示该节点下的所有题目，选中项高亮（紫色浅底+紫色文字）
10. THE 预设工具（pep3/cpep/vbmapp）SHALL 在首次加载时自动生成默认领域结构和模拟题目数据

### Requirement 6：题目管理

**User Story:** 作为管理员，我希望能在子测验/领域下添加、编辑、删除题目，以便完善评估内容。

#### Acceptance Criteria

1. WHEN 管理员选中左侧某个领域节点后点击【+ 添加题目】, THE 编辑页 SHALL 自动打开右侧题目编辑抽屉（520px），进入新增模式，排序号自动填入当前领域题目数+1
2. IF 管理员未选中左侧任何领域节点就点击【+ 添加题目】, THEN THE 编辑页 SHALL 提示"请先在左侧选择一个领域"
3. THE 题目编辑抽屉 SHALL 包含核心字段（排序号-必填、评估项目名称-必填、操作描述 textarea、评分说明-动态渲染每个等级的分值/标签/说明输入框）和扩展字段（所需材料、适用年龄、是否必答、启用状态，默认折叠）
4. THE 评分说明区域 SHALL 根据当前领域已有题目的 scores 结构动态渲染；如果领域内无题目则 fallback 到工具类型对应的预设评分体系
5. WHEN 管理员点击题目表格中某题的【编辑】链接, THE 编辑页 SHALL 打开右侧抽屉并加载该题所有数据（包括核心字段和扩展字段）
6. THE 扩展字段区域 SHALL 在已有数据（所需材料或适用年龄非空）时自动展开，否则默认折叠
7. WHEN 管理员点击某题目的【删除】链接, THE 编辑页 SHALL 弹出确认弹窗"确定要删除这道题目吗？删除后无法恢复。"，确认后删除该题目并重新编号
8. WHEN 管理员在抽屉中填写完毕并点击"保存", THE 系统 SHALL 校验必填字段（排序号、评估项目、评分标签），校验通过后保存题目数据并刷新题目表格
9. THE 题目表格排序号列 SHALL 支持点击切换升序/降序排列
10. WHEN 管理员点击编辑页底部的【保存】按钮, THE 系统 SHALL 保存当前工具的所有修改（基本信息+领域结构+题目数据）并更新工具的题目总数和修改时间

### Requirement 7：批量导入评估题目

**User Story:** 作为管理员，我希望能通过 Excel/CSV 文件批量导入评估题目，以便快速完成大量题目的录入。

#### Acceptance Criteria

1. WHEN 管理员在新建弹窗选择"表格导入"或从编辑页进入导入页面, THE 系统 SHALL 展示三步导入流程：下载模板 → 上传文件 → 预览数据
2. THE 导入流程 SHALL 提供 PEP-3 和 VB-MAPP 两套预设模板的下载链接
3. THE 导入流程 SHALL 在模板下载区域下方展示评分体系解析规则说明（紫色提示卡片），说明 CSV 表头列名格式为 `评分_{字母}_{字段}`，字段包括 分值/标签/说明
4. THE 上传区域 SHALL 支持拖拽上传和点击选择文件，接受 .xlsx 和 .csv 格式
5. WHEN 管理员上传文件后, THE 系统 SHALL 解析文件内容：
   - 识别必填列（一级分类、二级分类、操作描述）
   - 通过正则 `^评分_([a-z])_(分值|标签|说明)$` 匹配评分列
   - 逐行解析数据，缺少一级分类或二级分类的行标记为无效
6. THE 预览区域 SHALL 展示解析结果统计：共 N 行，有效 N 条，异常 N 条（缺少必填字段已跳过）
7. IF 文件格式不正确（缺少必填列）, THEN THE 系统 SHALL 提示"文件格式不正确，需包含'一级分类、二级分类、操作描述'列"
8. IF 文件为空或解析失败, THEN THE 系统 SHALL 提示具体错误信息
9. WHEN 管理员确认导入, THE 系统 SHALL 将有效数据写入评估工具配置，更新题目总数，并显示导入结果
10. THE 导入完成后 SHALL 提供"返回编辑页"按钮，点击跳转到编辑页查看导入的数据

### Requirement 8：类型配置管理

**User Story:** 作为管理员，我希望能管理评估工具的类型配置，以便控制不同类型工具在答题页和报告页的行为差异。

#### Acceptance Criteria

1. WHEN 管理员点击列表页筛选区右侧的【类型管理】按钮, THE 后台管理系统 SHALL 弹出类型配置管理弹窗（720px 宽度，最大高度 80vh）
2. THE 类型配置弹窗 SHALL 展示说明文字和所有已配置的评估类型列表，每个类型一个带边框的卡片区块
3. THE 每个类型卡片 SHALL 展示以下可编辑配置项：答题模式（下拉）、显示评分说明（下拉）、导航默认折叠（下拉）、允许未全作答提交（下拉）、卡片展示字段（多选复选框）、底部快捷操作（多选复选框）
4. THE 每个类型卡片 SHALL 展示只读信息：类型标识、名称、描述、工具简介
5. WHEN 管理员修改配置并点击【保存】, THE 系统 SHALL 保存配置并提示"类型配置已保存"
6. WHEN 管理员点击【取消】, THE 弹窗 SHALL 关闭，不保存任何修改

---

## 5. 后端需求

### API: 评估工具列表查询（含筛选）

- 方法: GET
- 路径: `/api/assessment-tools`
- 描述: 获取评估工具列表，支持名称模糊搜索和状态筛选
- 请求参数:
  - `name` (string, 可选) — 名称关键词，模糊匹配名称和描述
  - `status` (string, 可选) — 状态筛选，可选值：`active`、`inactive`
  - `page` (number, 可选) — 页码，默认 1
  - `pageSize` (number, 可选) — 每页数量，默认 20
- 响应数据:
  ```json
  {
    "code": 200,
    "data": {
      "total": 3,
      "list": [
        {
          "id": "string",
          "name": "PEP-3",
          "type": "pep3",
          "typeDisplayName": "PEP-3 · 心理教育评估",
          "description": "心理教育评估第三版",
          "avatar": "string | null",
          "status": "active",
          "questionCount": 138,
          "createdAt": "2024-01-15T00:00:00Z",
          "updatedAt": "2024-01-15T00:00:00Z"
        }
      ]
    }
  }
  ```

---

### API: 评估工具详情查询

- 方法: GET
- 路径: `/api/assessment-tools/:id`
- 描述: 获取单个评估工具的完整信息，包含领域结构和题目数据
- 请求参数:
  - `id` (string, 路径参数) — 评估工具 ID
- 响应数据:
  ```json
  {
    "code": 200,
    "data": {
      "id": "string",
      "name": "PEP-3",
      "type": "pep3",
      "description": "心理教育评估第三版",
      "avatar": "string | null",
      "status": "active",
      "questionCount": 138,
      "createdAt": "2024-01-15T00:00:00Z",
      "updatedAt": "2024-01-15T00:00:00Z",
      "domainGroups": [
        {
          "id": "string",
          "name": "发展性子测验",
          "sortOrder": 1,
          "domains": [
            {
              "id": "string",
              "name": "认知/语前语言",
              "sortOrder": 1,
              "questionCount": 20,
              "questions": [
                {
                  "id": "string",
                  "sortOrder": 1,
                  "itemName": "对铃声转头寻找声源",
                  "description": "摇铃铛，观察儿童是否转头寻找声源",
                  "materials": "小铃铛",
                  "ageRange": "6-12月",
                  "required": true,
                  "enabled": true,
                  "scores": [
                    { "value": 2, "label": "通过", "description": "独立完成" },
                    { "value": 1, "label": "萌芽", "description": "部分完成或需要提示" },
                    { "value": 0, "label": "不通过", "description": "无反应或无法完成" }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  }
  ```

---

### API: 评估工具创建

- 方法: POST
- 路径: `/api/assessment-tools`
- 描述: 创建新的评估工具，默认状态为 inactive
- 请求参数:
  ```json
  {
    "name": "string (必填，不可重复)",
    "type": "string (必填，pep3/cpep/vbmapp/common)",
    "description": "string (可选)",
    "avatar": "string (可选，base64 或 URL)"
  }
  ```
- 响应数据:
  ```json
  {
    "code": 200,
    "data": {
      "id": "string (新创建的工具ID)",
      "name": "string",
      "type": "string",
      "description": "string",
      "status": "inactive",
      "questionCount": 0,
      "createdAt": "string",
      "updatedAt": "string"
    }
  }
  ```
- 业务逻辑:
  - 校验名称不为空
  - 校验名称不与已有工具重复
  - 校验类型为有效值（pep3/cpep/vbmapp/common）
  - 默认 status = "inactive"，questionCount = 0

---

### API: 评估工具更新（基本信息）

- 方法: PUT
- 路径: `/api/assessment-tools/:id`
- 描述: 更新评估工具的基本信息（名称、描述、图标）
- 请求参数:
  ```json
  {
    "name": "string (必填，不可与其他工具重复)",
    "description": "string (可选)",
    "avatar": "string (可选，base64 或 URL)"
  }
  ```
- 响应数据:
  ```json
  {
    "code": 200,
    "data": {
      "id": "string",
      "name": "string",
      "description": "string",
      "avatar": "string | null",
      "updatedAt": "string"
    }
  }
  ```
- 业务逻辑:
  - 类型（type）创建后不可修改，请求中不接受 type 字段
  - 校验名称不与其他工具重复（排除自身）
  - 自动更新 updatedAt

---

### API: 评估工具启用/停用

- 方法: PATCH
- 路径: `/api/assessment-tools/:id/status`
- 描述: 切换评估工具的启用/停用状态
- 请求参数:
  ```json
  {
    "status": "active | inactive"
  }
  ```
- 响应数据:
  ```json
  {
    "code": 200,
    "data": {
      "id": "string",
      "status": "active | inactive"
    }
  }
  ```
- 业务逻辑:
  - 启用时校验 questionCount > 0，否则返回错误："该评估工具尚无题目，无法启用"
  - 停用时无额外校验

---

### API: 评估工具删除

- 方法: DELETE
- 路径: `/api/assessment-tools/:id`
- 描述: 删除评估工具及其所有领域和题目配置
- 请求参数:
  - `id` (string, 路径参数) — 评估工具 ID
- 响应数据:
  ```json
  {
    "code": 200,
    "message": "删除成功"
  }
  ```
- 业务逻辑:
  - 删除前校验工具状态必须为 inactive，否则返回错误："请先停用该评估工具后再删除"
  - 级联删除：assessment_domain_groups → assessment_domains → assessment_questions
  - 历史评估记录（assessment_records）不受影响，保留快照数据

---

### API: 领域分组 CRUD

#### 创建分组
- 方法: POST
- 路径: `/api/assessment-tools/:toolId/domain-groups`
- 描述: 在评估工具下创建新的领域分组
- 请求参数:
  ```json
  {
    "name": "string (必填)",
    "sortOrder": "number (可选，默认追加到末尾)"
  }
  ```
- 响应数据:
  ```json
  {
    "code": 200,
    "data": {
      "id": "string",
      "name": "string",
      "sortOrder": 1,
      "domains": []
    }
  }
  ```

#### 更新分组（重命名）
- 方法: PUT
- 路径: `/api/assessment-tools/:toolId/domain-groups/:groupId`
- 描述: 重命名领域分组
- 请求参数:
  ```json
  {
    "name": "string (必填)"
  }
  ```

#### 删除分组
- 方法: DELETE
- 路径: `/api/assessment-tools/:toolId/domain-groups/:groupId`
- 描述: 删除领域分组及其下所有子测验/领域和题目
- 业务逻辑: 级联删除该分组下的所有 domains 和 questions

#### 排序分组
- 方法: PUT
- 路径: `/api/assessment-tools/:toolId/domain-groups/sort`
- 描述: 批量更新分组排序
- 请求参数:
  ```json
  {
    "sortOrders": [
      { "id": "string", "sortOrder": 1 },
      { "id": "string", "sortOrder": 2 }
    ]
  }
  ```

---

### API: 子测验/领域 CRUD

#### 创建领域
- 方法: POST
- 路径: `/api/assessment-tools/:toolId/domain-groups/:groupId/domains`
- 描述: 在分组下创建新的子测验/领域
- 请求参数:
  ```json
  {
    "name": "string (必填)",
    "sortOrder": "number (可选)"
  }
  ```
- 响应数据:
  ```json
  {
    "code": 200,
    "data": {
      "id": "string",
      "name": "string",
      "sortOrder": 1,
      "questionCount": 0
    }
  }
  ```

#### 更新领域（重命名）
- 方法: PUT
- 路径: `/api/assessment-tools/:toolId/domains/:domainId`
- 描述: 重命名子测验/领域
- 请求参数:
  ```json
  {
    "name": "string (必填)"
  }
  ```

#### 删除领域
- 方法: DELETE
- 路径: `/api/assessment-tools/:toolId/domains/:domainId`
- 描述: 删除子测验/领域及其下所有题目
- 业务逻辑:
  - 级联删除该领域下的所有 questions
  - 如果删除后该分组下没有其他领域，保留空分组

#### 排序领域
- 方法: PUT
- 路径: `/api/assessment-tools/:toolId/domain-groups/:groupId/domains/sort`
- 描述: 批量更新领域排序
- 请求参数:
  ```json
  {
    "sortOrders": [
      { "id": "string", "sortOrder": 1 },
      { "id": "string", "sortOrder": 2 }
    ]
  }
  ```

---

### API: 题目 CRUD（含排序）

#### 创建题目
- 方法: POST
- 路径: `/api/assessment-tools/:toolId/domains/:domainId/questions`
- 描述: 在领域下创建新题目
- 请求参数:
  ```json
  {
    "sortOrder": "number (必填)",
    "itemName": "string (必填)",
    "description": "string (可选)",
    "materials": "string (可选)",
    "ageRange": "string (可选)",
    "required": "boolean (默认 true)",
    "enabled": "boolean (默认 true)",
    "scores": [
      {
        "value": "number (必填)",
        "label": "string (必填)",
        "description": "string (可选)"
      }
    ]
  }
  ```
- 响应数据:
  ```json
  {
    "code": 200,
    "data": {
      "id": "string",
      "sortOrder": 1,
      "itemName": "string",
      "description": "string",
      "scores": []
    }
  }
  ```
- 业务逻辑:
  - 创建后自动更新所属工具的 questionCount
  - 校验 sortOrder、itemName、scores[].label 不为空

#### 更新题目
- 方法: PUT
- 路径: `/api/assessment-tools/:toolId/questions/:questionId`
- 描述: 更新题目的所有字段
- 请求参数: 同创建题目
- 业务逻辑: 更新后自动更新工具的 updatedAt

#### 删除题目
- 方法: DELETE
- 路径: `/api/assessment-tools/:toolId/questions/:questionId`
- 描述: 删除单个题目
- 业务逻辑:
  - 删除后自动重新编号同领域内的其他题目
  - 更新所属工具的 questionCount 和 updatedAt

#### 批量排序题目
- 方法: PUT
- 路径: `/api/assessment-tools/:toolId/domains/:domainId/questions/sort`
- 描述: 批量更新题目排序
- 请求参数:
  ```json
  {
    "sortOrders": [
      { "id": "string", "sortOrder": 1 },
      { "id": "string", "sortOrder": 2 }
    ]
  }
  ```

---

### API: 批量导入题目

#### 上传并预览
- 方法: POST
- 路径: `/api/assessment-tools/:toolId/import/preview`
- 描述: 上传 CSV/Excel 文件，解析并返回预览数据
- 请求参数:
  - Content-Type: `multipart/form-data`
  - `file` (File, 必填) — .xlsx 或 .csv 文件
- 响应数据:
  ```json
  {
    "code": 200,
    "data": {
      "total": 172,
      "valid": 170,
      "invalid": 2,
      "rows": [
        {
          "rowNumber": 1,
          "group": "发展性子测验",
          "domain": "认知/语前语言",
          "itemName": "对铃声转头寻找声源",
          "description": "摇铃铛，观察儿童是否转头寻找声源",
          "materials": "小铃铛",
          "ageRange": "6-12月",
          "required": true,
          "scores": [
            { "value": 2, "label": "通过", "description": "独立完成" },
            { "value": 1, "label": "萌芽", "description": "部分完成" },
            { "value": 0, "label": "不通过", "description": "无反应" }
          ],
          "valid": true,
          "errorMessage": null
        },
        {
          "rowNumber": 9,
          "group": "",
          "domain": "",
          "description": "缺少子测验信息",
          "valid": false,
          "errorMessage": "缺少一级分类"
        }
      ]
    }
  }
  ```
- 业务逻辑:
  - 解析 CSV 表头，识别必填列和评分列
  - 评分列通过正则 `^评分_([a-z])_(分值|标签|说明)$` 匹配
  - 缺少一级分类或二级分类的行标记为无效
  - 返回预览数据供前端展示，不写入数据库

#### 确认导入
- 方法: POST
- 路径: `/api/assessment-tools/:toolId/import/confirm`
- 描述: 确认导入预览数据中的有效行
- 请求参数:
  ```json
  {
    "previewToken": "string (预览接口返回的临时令牌)"
  }
  ```
- 响应数据:
  ```json
  {
    "code": 200,
    "data": {
      "imported": 170,
      "failed": 2,
      "toolId": "string"
    }
  }
  ```
- 业务逻辑:
  - 将有效行写入 assessment_questions 表
  - 自动创建不存在的 domain_groups 和 domains
  - 更新工具的 questionCount 和 updatedAt
  - 清理预览临时数据

---

### API: 评估类型配置查询

- 方法: GET
- 路径: `/api/assessment-type-config`
- 描述: 获取所有评估类型的配置
- 响应数据:
  ```json
  {
    "code": 200,
    "data": {
      "types": [
        {
          "id": "pep3",
          "name": "PEP-3",
          "description": "心理教育评估（Schopler修订版）",
          "intro": "心理教育评估第三版，适用于2-7.5岁儿童",
          "answerConfig": {
            "listMode": "byDomain",
            "cardFields": ["itemName", "desc", "materials"],
            "showScoreDesc": false,
            "navCollapsedByDefault": false,
            "quickActions": ["failAll", "passAll", "nextDomain"],
            "allowPartialSubmit": false
          },
          "reportConfig": {
            "reportPage": "assessment-result-pep3.html",
            "reportTitle": "PEP-3 心理教育评估报告"
          }
        }
      ]
    }
  }
  ```

---

### API: 评估类型配置更新

- 方法: PUT
- 路径: `/api/assessment-type-config`
- 描述: 批量更新评估类型配置
- 请求参数:
  ```json
  {
    "types": [
      {
        "id": "pep3",
        "answerConfig": {
          "listMode": "byDomain",
          "cardFields": ["itemName", "desc", "materials"],
          "showScoreDesc": false,
          "navCollapsedByDefault": false,
          "quickActions": ["failAll", "passAll", "nextDomain"],
          "allowPartialSubmit": false
        }
      }
    ]
  }
  ```
- 响应数据:
  ```json
  {
    "code": 200,
    "message": "类型配置已保存"
  }
  ```
- 业务逻辑:
  - 仅更新 answerConfig 中的可配置字段
  - id、name、description、intro、reportConfig 不可通过此接口修改

---

### 数据模型

```sql
-- 评估工具表
CREATE TABLE assessment_tools (
  id          VARCHAR(64) PRIMARY KEY,
  name        VARCHAR(100) NOT NULL UNIQUE,
  type        VARCHAR(20) NOT NULL,          -- pep3/cpep/vbmapp/common
  description TEXT,
  avatar      TEXT,                           -- 图标 URL 或 base64
  status      VARCHAR(10) NOT NULL DEFAULT 'inactive',  -- active/inactive
  question_count INT NOT NULL DEFAULT 0,
  created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 领域分组表
CREATE TABLE assessment_domain_groups (
  id          VARCHAR(64) PRIMARY KEY,
  tool_id     VARCHAR(64) NOT NULL REFERENCES assessment_tools(id) ON DELETE CASCADE,
  name        VARCHAR(100) NOT NULL,
  sort_order  INT NOT NULL DEFAULT 0,
  UNIQUE(tool_id, name)
);

-- 子测验/领域表
CREATE TABLE assessment_domains (
  id          VARCHAR(64) PRIMARY KEY,
  group_id    VARCHAR(64) NOT NULL REFERENCES assessment_domain_groups(id) ON DELETE CASCADE,
  tool_id     VARCHAR(64) NOT NULL REFERENCES assessment_tools(id) ON DELETE CASCADE,
  name        VARCHAR(100) NOT NULL,
  sort_order  INT NOT NULL DEFAULT 0,
  question_count INT NOT NULL DEFAULT 0,
  UNIQUE(group_id, name)
);

-- 题目表
CREATE TABLE assessment_questions (
  id          VARCHAR(64) PRIMARY KEY,
  tool_id     VARCHAR(64) NOT NULL REFERENCES assessment_tools(id) ON DELETE CASCADE,
  domain_id   VARCHAR(64) NOT NULL REFERENCES assessment_domains(id) ON DELETE CASCADE,
  sort_order  INT NOT NULL DEFAULT 0,
  item_name   VARCHAR(200) NOT NULL,          -- 评估项目名称
  description TEXT,                            -- 操作描述
  materials   VARCHAR(500),                    -- 所需材料
  age_range   VARCHAR(50),                     -- 适用年龄
  required    BOOLEAN NOT NULL DEFAULT TRUE,   -- 是否必答
  enabled     BOOLEAN NOT NULL DEFAULT TRUE,   -- 启用状态
  scores      JSON NOT NULL,                   -- [{value, label, description}]
  created_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  updated_at  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 评估类型配置表
CREATE TABLE assessment_type_config (
  id            VARCHAR(64) PRIMARY KEY,
  type_id       VARCHAR(20) NOT NULL UNIQUE,   -- pep3/cpep/vbmapp/common
  name          VARCHAR(50) NOT NULL,
  description   VARCHAR(200),
  intro         TEXT,
  answer_config JSON NOT NULL,                  -- answerConfig 对象
  report_config JSON NOT NULL,                  -- reportConfig 对象
  updated_at    TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- 索引
CREATE INDEX idx_questions_tool_id ON assessment_questions(tool_id);
CREATE INDEX idx_questions_domain_id ON assessment_questions(domain_id);
CREATE INDEX idx_domains_tool_id ON assessment_domains(tool_id);
CREATE INDEX idx_domains_group_id ON assessment_domains(group_id);
CREATE INDEX idx_domain_groups_tool_id ON assessment_domain_groups(tool_id);
```

---

## 6. HTML 文件清单

| 文件路径 | 页面说明 | 主要功能 |
|----------|---------|---------|
| `features/pep3-vb-assessment/pad/admin-assessment-list.html` | 评估工具列表页 | 卡片网格展示、筛选搜索、启用/停用切换、新建弹窗（含基本信息+配置方式选择+表格导入流程）、类型管理弹窗 |
| `features/pep3-vb-assessment/pad/admin-assessment-edit.html` | 评估工具编辑页 | 基本信息只读/抽屉编辑、领域结构树（编辑模式：添加/重命名/删除分组和子项）、题目表格列表、题目编辑抽屉（核心字段+扩展字段+评分说明）、新建面板（从列表页跳转时） |
| `features/pep3-vb-assessment/pad/admin-assessment-import.html` | 批量导入页面 | 三步导入流程：下载模板→上传文件→预览数据→确认导入→导入结果 |

### 页面跳转关系

```
admin-assessment-list.html
  │
  ├── [点击"编辑"链接] ──→ admin-assessment-edit.html?id={toolId}
  │                           │
  │                           ├── [点击"< 返回"] ──→ admin-assessment-list.html
  │                           │
  │                           └── [进入导入页] ──→ admin-assessment-import.html?id={toolId}
  │                                                  │
  │                                                  └── [点击"< 返回编辑页"] ──→ admin-assessment-edit.html?id={toolId}
  │
  ├── [新建弹窗 → 手动录入] ──→ admin-assessment-edit.html?id={newToolId}
  │
  └── [新建弹窗 → 表格导入 → 确认导入] ──→ admin-assessment-edit.html?id={newToolId}
```

### 页面间数据共享

所有页面通过 localStorage 共享数据，key 前缀统一为 `rice_assessment_`：

| localStorage Key | 数据说明 | 读写页面 |
|-----------------|---------|---------|
| `rice_assessment_tools` | 评估工具列表（JSON 数组） | list / edit / import |
| `rice_assessment_config_{toolId}` | 工具的领域结构和题目数据（JSON 对象，key 为 `{group}__{domain}`） | edit / import |
| `rice_assessment_config_{toolId}_groups` | 空分组列表（JSON 数组，用于保留无子项的分组） | edit |
| `rice_assessment_type_config` | 类型配置（JSON 对象，结构同 eval-type-config.json） | list |

### 关联配置文件

| 文件路径 | 说明 | 关联页面 |
|----------|------|---------|
| `config/eval-type-config.json` | 评估类型配置（默认值） | list（类型管理弹窗） |
| `config/scoring-mode-rules.md` | 评分模式规则（直接评分/回合统计） | 答题页参考，管理端不直接使用 |
| `data/pep3-config.csv` | PEP-3 题目配置数据 | edit（loadPresetFromCSV） |
| `data/vbmapp-config.csv` | VB-MAPP 题目配置数据 | edit（loadPresetFromCSV） |
| `data/cpep-config.csv` | C-PEP 题目配置数据 | edit（loadPresetFromCSV） |

---

## 7. 设计规范引用

本模块所有页面（`pad/admin-*.html`）遵循 `design/DESIGN.md` **Part A：后台管理端设计规范**。

### 关键设计规范摘要

| 规范项 | 值 |
|--------|-----|
| 主色（品牌紫） | `#7C3AED` |
| 主色悬停 | `#6D28D9` |
| 主色浅底 | `#EDE9FE` |
| 页面背景 | `#F5F5F5` |
| 卡片背景 | `#FFFFFF` |
| 卡片边框 | `#E5E7EB`，圆角 12px |
| 输入框边框 | `#D1D5DB`，圆角 8px，高度 36px |
| 输入框聚焦 | 边框 `#7C3AED`，外发光 `0 0 0 2px rgba(124,58,237,0.2)` |
| 启用状态 | 背景 `#ECFDF5`，文字 `#059669` |
| 停用状态 | 背景 `#FFF7ED`，文字 `#EA580C` |
| 危险操作（删除） | `#DC2626` |
| 页面标题 | 20px Semi-Bold |
| 卡片名称 | 16px Semi-Bold |
| 正文 | 14px Regular |
| 描述文字 | 13px Regular `#6B7280` |
| 弹窗圆角 | 12px |
| 弹窗遮罩 | `rgba(0,0,0,0.4)` |
| 左侧导航宽度 | 80px（收起态） |
| 顶部栏高度 | 56px |
| 内容区内边距 | 24px |
| 卡片网格 | 3列，gap 20px |
| 字体族 | `-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "Noto Sans SC", sans-serif` |

### 组件规范

- **主按钮**：背景 `#7C3AED`，白色文字，圆角 8px，padding 8px 16px
- **次按钮**：白色背景，`#D1D5DB` 边框，灰色文字，圆角 8px
- **Toggle Switch**：宽 40px，高 22px，圆形滑块 18px，启用绿色 `#059669`，停用灰色 `#D1D5DB`
- **自定义下拉**：非原生 select，带描述的选项列表，选中项紫色背景
- **右侧抽屉**：宽度 520px，从右侧滑出，带遮罩层，阴影 `-4px 0 24px rgba(0,0,0,0.12)`
- **确认弹窗**：白色背景，圆角 12px，padding 24px，底部右对齐按钮组
- **Toast 提示**：固定顶部居中，深色背景 `#1F2937`，白色文字，2秒自动消失

> 完整设计规范详见 `design/DESIGN.md` Part A 部分。