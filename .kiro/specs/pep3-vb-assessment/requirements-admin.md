# 评估工具后台管理系统 — 需求文档

## 简介

本文档描述 RICE AI 后台管理系统中「评估工具管理」模块的完整需求。该模块供管理员使用，用于创建、编辑、导入和管理评估工具（如 PEP-3、C-PEP、VB-MAPP 等），包括工具基本信息、评分体系、领域/子测验结构、题目内容和类型配置。管理员通过此模块维护的评估工具数据，将直接供康复师 App 端的答题和报告功能使用。

本模块仅在 Web/PAD 端运行，不提供手机端界面。

---

## 术语表

- **评估工具**：一套标准化评估量表的数字化配置，包含领域结构、题目和评分规则（如 PEP-3、VB-MAPP、C-PEP）
- **评分体系（scoreOptions）**：评估工具的评分选项配置，定义每个评分等级的分值和标签。如 PEP-3 为 0-不通过/1-萌芽/2-通过，VB-MAPP 为 0/0.5/1
- **子测验/领域**：评估工具内的分组结构，PEP-3 称"子测验"，VB-MAPP 称"领域"
- **分组**：子测验/领域的上级分类（如 PEP-3 的"发展性子测验""行为特征子测验""养育者报告"）
- **类型配置（eval-type-config）**：控制不同评估工具类型在答题页、报告页的行为差异的配置项
- **后台管理系统**：RICE AI 后台管理系统，Web 端管理后台，管理员使用。左侧导航栏采用图标+文字竖排布局，紫色高亮当前选中项。导航项顺序：产品、订单、用户、学生、评估、课程包、学习、AI助手、营销、设置。顶部栏包含系统logo、面包屑导航、搜索(⌘K)、全屏、刷新、设置、语言切换、用户头像

---

## 功能描述

### 功能模块一：评估工具列表页

**用户角色**：管理员

**功能描述**：
管理员通过左侧导航栏【评估】菜单（位于【学生】和【课程包】之间）进入评估工具管理页面。页面以卡片网格布局（每行3个卡片）展示所有已配置的评估工具，支持搜索和筛选。

**业务规则**：
- 评估工具状态仅有两种：启用、停用
- 新建的评估工具默认为"停用"状态
- 停用状态的工具在康复师 App 新建评估弹窗中不可见
- 题目数量为 0 的工具不允许启用，系统提示"该评估工具尚无题目，无法启用"
- 点击开关直接切换启用/停用状态，无需额外确认

**UI 描述**（参考 `admin-assessment-list.html`）：
- 页面顶部：页面标题"评估工具管理"
- 筛选条件区：左侧名称搜索输入框 + 状态下拉选择（onchange 实时筛选）+ 搜索/重置按钮 + 右侧"类型管理"按钮
- 卡片网格（3列）：
  - 每张卡片包含：左侧圆形图标（支持自定义头像）、右上角 toggle switch 开关（启用=绿色"已启用"，停用=灰白"已停用"）、工具名称（16px 600）、描述文字（13px，2行截断）、底部信息行（类型·题目数·修改时间 左对齐，"编辑"链接右对齐）
  - 停用卡片整体 opacity: 0.55，hover 时恢复到 0.85
- 卡片网格末尾固定一张虚线边框卡片"+ 新建评估工具"，点击弹出新建弹窗

### 功能模块二：新建评估工具

**用户角色**：管理员

**功能描述**：
管理员点击列表页末尾的虚线卡片，弹出新建弹窗。先填写基本信息（工具图标、名称、类型、描述），然后选择配置方式。

**业务规则**：
- 名称为必填项
- 类型为必选项，从类型配置中读取可选类型列表（pep3/cpep/vbmapp/common）
- 类型选择使用自定义下拉组件（非原生 select），展示类型名称和描述
- 配置方式二选一：表格导入 或 手动录入
- 手动录入：创建工具后跳转到空白编辑页，左侧显示"暂无领域结构，请添加分组"提示
- 表格导入：在弹窗内切换到导入步骤

**UI 描述**（参考 `admin-assessment-list.html` 新建弹窗）：
- 弹窗标题"新建评估工具"
- 基本信息区：工具图标（点击上传）、名称输入框（180px）、类型自定义下拉（带描述）、描述 textarea
- 配置方式选择区：两张等宽卡片横排
  - 📥 表格录入：下载模板，填写后上传导入
  - ✏️ 手动录入：在线逐条添加领域和题目
- 表格导入步骤：模板下载（PEP-3/VB-MAPP 两套）+ 评分体系解析规则说明（紫色提示卡片）+ 文件上传区 + 预览数据 + 确认导入

### 功能模块三：评估工具编辑页

**用户角色**：管理员

**功能描述**：
管理员从列表页点击"编辑"进入编辑页，管理评估工具的基本信息、领域结构和题目内容。

**业务规则**：
- 基本信息区默认只读展示，点击"编辑"弹出右侧抽屉（520px）
- 抽屉内可编辑：工具图标、名称、类型（已创建后只读）、描述，底部提供"删除此评估工具"链接
- 领域结构为树形结构，支持分组（group）和子项（domain）两级
- 树形结构支持：添加分组、添加子项、重命名、删除、拖拽排序
- 编辑模式下节点的改名/删除操作用图标按钮（✏️ 🗑），hover 时才显示
- 删除包含题目的节点需确认提示
- 底部操作栏仅保留【保存】按钮

**UI 描述**（参考 `admin-assessment-edit.html`）：
- 顶部面包屑导航（< 返回 + 工具名称）
- 基本信息栏（只读）：头像 + 名称 + 类型 + 描述，右上角"编辑"链接
- 编辑区左右分栏：
  - 左侧树面板（280px）：领域目录，顶部"编辑"按钮切换编辑模式
  - 右侧题目面板：表格式题目列表，列包含排序号、评估项目、操作描述、评分说明列（动态）、材料、年龄、必答、启用状态、操作（编辑/删除）
- 题目编辑抽屉（520px，从右侧滑出）：
  - 核心字段（始终展示）：排序号、评估项目名称、操作描述 textarea、评分说明（根据 scoreOptions 动态渲染每个等级一个输入框）
  - 扩展字段（默认折叠，有数据时自动展开）：所需材料、适用年龄、是否必答、启用状态

### 功能模块四：批量导入

**用户角色**：管理员

**功能描述**：
管理员通过编辑页或新建弹窗进入批量导入流程，上传 Excel/CSV 文件批量录入评估题目。

**业务规则**：
- 支持 .xlsx 和 .csv 格式
- 提供 PEP-3 和 VB-MAPP 两套预设模板下载
- 评分体系自动解析规则：CSV 表头列名格式为 `评分_{字母}_{字段}`（字段包括 分值/标签/说明），如 `评分_a_分值`、`评分_a_标签`、`评分_a_说明`，每道题自带评分配置，动态列数，用字母编号（a, b, c, ...）
- 上传后预览数据，显示统计：总条数、有效条数、异常条数
- 异常行高亮显示（红色背景），标注具体错误原因（如缺少领域、缺少描述）
- 确认导入后写入对应评估工具，显示导入结果

**UI 描述**（参考 `admin-assessment-import.html` 和 `admin-assessment-list.html` 导入步骤）：
- 三步流程：下载模板 → 上传文件 → 预览数据
- 模板下载区：Excel 模板 + CSV 模板按钮
- 评分体系解析规则说明（紫色提示卡片）
- 上传区：拖拽或点击选择文件
- 预览表格：题号、子测验/领域、题目描述、评分选项、状态
- 底部操作：取消 + 确认导入

### 功能模块五：类型配置管理

**用户角色**：管理员

**功能描述**：
管理员通过列表页筛选区右侧的"类型管理"按钮打开类型配置弹窗，管理评估工具的类型配置。

**业务规则**：
- 类型配置结构（eval-type-config.json）：
  - `id`：类型标识（pep3/cpep/vbmapp/common）
  - `name`：类型名称
  - `description`：类型描述
  - `intro`：类型简介
  - `answerConfig`：答题交互配置
    - `listMode`：题目列表模式（byDomain/byOrder）
    - `cardFields`：题目卡片展示字段（itemName/desc/materials/ageRange）
    - `showScoreDesc`：是否展示评分说明
    - `navCollapsedByDefault`：导航是否默认折叠
    - `quickActions`：快捷操作按钮（failAll/passAll/nextDomain）
    - `allowPartialSubmit`：是否允许部分提交
  - `reportConfig`：报告页配置
    - `reportPage`：独立报告页文件名
    - `reportTitle`：报告标题

**UI 描述**（参考 `admin-assessment-list.html` 类型管理弹窗）：
- 弹窗标题"评估类型配置管理"
- 说明文字
- 类型列表：每个类型展示配置项，可编辑
- 底部：取消 + 保存按钮

---

## 后端需求

### API 1：评估工具 CRUD

**接口模式**：RESTful

| 操作 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 获取工具列表 | GET | `/api/assessment-tools` | 支持 name/status 筛选 |
| 获取单个工具 | GET | `/api/assessment-tools/:id` | 含完整领域结构和题目 |
| 创建工具 | POST | `/api/assessment-tools` | 基本信息 + 可选导入数据 |
| 更新工具 | PUT | `/api/assessment-tools/:id` | 基本信息 + 领域结构 + 题目 |
| 删除工具 | DELETE | `/api/assessment-tools/:id` | 级联删除领域和题目 |
| 切换状态 | PATCH | `/api/assessment-tools/:id/status` | 启用/停用切换 |

**请求/响应数据字段**：

```typescript
// 评估工具
interface AssessmentTool {
  id: string;
  name: string;
  type: string;           // pep3/cpep/vbmapp/common
  description: string;
  avatar?: string;        // 图标 URL 或 base64
  status: 'active' | 'inactive';
  questionCount: number;
  scoreOptions: ScoreOption[];
  createdAt: string;
  updatedAt: string;
}

interface ScoreOption {
  value: number;    // 分值，如 0, 1, 2
  label: string;    // 标签，如 "不通过", "萌芽", "通过"
}

// 领域结构
interface DomainGroup {
  id: string;
  name: string;       // 分组名称
  sortOrder: number;
  domains: Domain[];
}

interface Domain {
  id: string;
  name: string;       // 子测验/领域名称
  sortOrder: number;
  questionCount: number;
}

// 题目
interface Question {
  id: string;
  toolId: string;
  domainId: string;
  sortOrder: number;
  itemName: string;       // 评估项目名称
  description: string;    // 操作描述
  materials?: string;     // 所需材料
  ageRange?: string;      // 适用年龄
  required: boolean;      // 是否必答
  enabled: boolean;       // 启用状态
  scores: QuestionScore[];  // 每题的评分说明
}

interface QuestionScore {
  value: number;
  label: string;
  description: string;  // 该题该等级的评分说明
}
```

**业务逻辑**：
- 创建工具时默认 status = 'inactive'
- 启用工具前校验 questionCount > 0
- 删除工具级联删除所有领域和题目
- 更新工具时重新计算 questionCount

### API 2：批量导入

| 操作 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 上传并解析 | POST | `/api/assessment-tools/:id/import/preview` | 返回预览数据 |
| 确认导入 | POST | `/api/assessment-tools/:id/import/confirm` | 写入题目数据 |

**请求/响应**：
```typescript
// 预览响应
interface ImportPreview {
  total: number;
  valid: number;
  errors: number;
  rows: ImportRow[];
  parsedScoreOptions: ScoreOption[];  // 从表头解析的评分体系
}

interface ImportRow {
  rowNumber: number;
  domain: string;
  itemName: string;
  description: string;
  scores: QuestionScore[];
  valid: boolean;
  errorMessage?: string;
}
```

### API 3：类型配置

| 操作 | 方法 | 路径 | 说明 |
|------|------|------|------|
| 获取类型配置 | GET | `/api/assessment-type-config` | 返回所有类型配置 |
| 更新类型配置 | PUT | `/api/assessment-type-config` | 保存修改后的配置 |

### 数据模型

```
assessment_tools
├── id (PK)
├── name
├── type
├── description
├── avatar
├── status (active/inactive)
├── question_count
├── score_options (JSON)
├── created_at
└── updated_at

assessment_domain_groups
├── id (PK)
├── tool_id (FK → assessment_tools)
├── name
└── sort_order

assessment_domains
├── id (PK)
├── group_id (FK → assessment_domain_groups)
├── tool_id (FK → assessment_tools)
├── name
├── question_count
└── sort_order

assessment_questions
├── id (PK)
├── tool_id (FK → assessment_tools)
├── domain_id (FK → assessment_domains)
├── sort_order
├── item_name
├── description
├── materials
├── age_range
├── required (boolean)
├── enabled (boolean)
└── scores (JSON: [{value, label, description}])

assessment_type_config
├── id (PK)
├── type_id (unique)
├── name
├── description
├── answer_config (JSON)
├── report_config (JSON)
└── updated_at
```

---

## EARS 格式需求

### Requirement 1：评估工具列表管理

**User Story:** 作为管理员，我希望能查看和管理所有评估工具，以便对评估配置进行统一管理。

#### Acceptance Criteria

1. WHEN 管理员点击左侧导航【评估】菜单（位于【学生】和【课程包】之间）, THE 后台管理系统 SHALL 展示评估工具管理页面，采用卡片网格布局（每行3个卡片）展示所有已配置的评估工具
2. THE 评估工具卡片 SHALL 展示评估工具的名称、描述、类型、题目数量、右上角 toggle switch 开关组件（绿色"已启用"或灰白"已停用"）、最后修改时间，底部信息行与"编辑"链接同行（信息左对齐、编辑右对齐）
3. WHEN 管理员在筛选条件区输入名称关键词或选择状态（状态下拉 onchange 实时触发筛选）, THE 评估工具列表 SHALL 按条件进行筛选并刷新卡片展示
4. THE 卡片网格末尾 SHALL 固定展示一张虚线边框卡片（"+ 新建评估工具"），WHEN 管理员点击该卡片, THE 后台管理系统 SHALL 弹出"新建评估工具"弹窗
5. WHEN 管理员点击某张评估工具卡片的【编辑】操作, THE 后台管理系统 SHALL 跳转到该评估工具的编辑页并加载已有数据
6. THE 评估工具卡片 SHALL 对停用状态的卡片整体降低不透明度（opacity: 0.55），hover 时恢复到 0.85，与启用卡片形成明显视觉区分

### Requirement 2：评估工具启用/停用管理

**User Story:** 作为管理员，我希望能控制评估工具的启用状态，以便管理哪些评估工具可供评估师使用。

#### Acceptance Criteria

1. WHEN 管理员在列表页卡片右上角将 toggle switch 开关从"已停用"切换为"已启用", THE 后台管理系统 SHALL 将该评估工具状态变更为"启用"，开关变为绿色并显示"已启用"
2. WHEN 管理员在列表页卡片右上角将 toggle switch 开关从"已启用"切换为"已停用", THE 后台管理系统 SHALL 将该评估工具状态变更为"停用"，开关变为灰白色并显示"已停用"
3. THE 后台管理系统 SHALL 将新建的评估工具默认设置为"停用"状态
4. WHILE 评估工具状态为"停用", THE 康复师App SHALL 在新建评估弹窗中隐藏该评估工具
5. IF 管理员尝试启用一个题目数量为0的评估工具, THEN THE 后台管理系统 SHALL 提示"该评估工具尚无题目，无法启用"并阻止操作，开关恢复为停用状态

### Requirement 3：评估工具编辑 — 基本信息与结构配置

**User Story:** 作为管理员，我希望能编辑评估工具的基本信息和子测验/领域结构，以便构建完整的评估框架。

#### Acceptance Criteria

1. THE 评估工具编辑页 SHALL 包含只读基本信息栏（头像+名称+类型+描述，右上角"编辑"链接）和左右分栏编辑区（左侧领域树280px + 右侧题目表格）
2. WHEN 管理员点击基本信息栏的"编辑"链接, THE 编辑页 SHALL 弹出右侧抽屉（520px），包含工具图标上传、名称输入、类型（已创建后只读）、描述 textarea 和底部"删除此评估工具"链接
3. WHEN 管理员在结构树中添加分组或子项节点, THE 编辑页 SHALL 弹出对应弹窗输入名称，确认后在树形结构中新增该节点
4. WHEN 管理员拖拽结构树中的节点, THE 编辑页 SHALL 更新节点排序并实时反映变化
5. WHEN 管理员点击结构树中的某个子测验/领域节点, THE 编辑页 SHALL 在右侧题目表格区域展示该节点下的所有题目
6. IF 管理员尝试删除一个包含题目的子测验/领域节点, THEN THE 编辑页 SHALL 弹出确认提示"该节点下有N道题目，删除后题目将一并删除，是否继续？"
7. THE 编辑页底部操作栏 SHALL 仅包含【保存】按钮，启用/停用操作统一在列表页的开关组件上完成
8. THE 新建评估工具弹窗 SHALL 包含基本信息填写（工具图标、名称、类型自定义下拉、描述）和配置方式选择（"表格导入"和"手动录入"两种方式）
9. WHEN 管理员在新建弹窗选择"手动录入", THE 后台管理系统 SHALL 创建工具后跳转到空白编辑页，左侧显示"暂无领域结构，请添加分组"提示，不加载任何默认结构
10. WHEN 管理员在新建弹窗选择"表格导入", THE 后台管理系统 SHALL 在弹窗内切换到导入步骤，提供模板下载及文件上传

### Requirement 4：题目管理

**User Story:** 作为管理员，我希望能在子测验/领域下添加、编辑、删除和排序题目，以便完善评估内容。

#### Acceptance Criteria

1. WHEN 管理员在某个子测验/领域下点击【添加题目】, THE 编辑页 SHALL 自动打开右侧题目编辑抽屉（520px），进入新增模式
2. IF 管理员未选中左侧任何领域节点就点击【添加题目】, THEN THE 编辑页 SHALL 提示"请先在左侧选择一个子测验或领域"
3. THE 题目编辑抽屉 SHALL 包含核心字段（排序号、评估项目名称、操作描述、评分说明——根据工具 scoreOptions 动态渲染）和扩展字段（所需材料、适用年龄、是否必答、启用状态，默认折叠，有数据时自动展开）
4. WHEN 管理员点击题目表格中某题的【编辑】链接, THE 编辑页 SHALL 打开右侧抽屉并加载该题数据
5. WHEN 管理员点击某题目的【删除】链接, THE 编辑页 SHALL 弹出确认提示后删除该题目并重新编号
6. WHEN 管理员点击【保存】, THE 后台管理系统 SHALL 保存当前所有修改并更新题目总数

### Requirement 5：批量导入评估题目

**User Story:** 作为管理员，我希望能通过 Excel/CSV 文件批量导入评估题目，以便快速完成大量题目的录入。

#### Acceptance Criteria

1. WHEN 管理员点击编辑页的【导入】按钮或新建弹窗选择"表格导入", THE 后台管理系统 SHALL 展示批量导入流程
2. THE 批量导入流程 SHALL 提供 PEP-3 和 VB-MAPP 两套预设模板的下载链接（Excel + CSV 格式）
3. THE 批量导入流程 SHALL 在模板下载区域下方展示评分体系解析规则说明（紫色提示卡片）：CSV 表头列名格式为 `评分_{字母}_{字段}`，字段包括 分值/标签/说明，每道题自带评分配置
4. WHEN 管理员上传文件后, THE 后台管理系统 SHALL 解析文件内容并在预览区域展示数据，包含题号、子测验/领域、题目描述、评分选项和状态
5. THE 预览区域 SHALL 显示数据统计：总条数、有效条数、异常条数
6. IF 上传文件格式不正确或内容解析失败, THEN THE 后台管理系统 SHALL 显示具体的错误信息和对应行号
7. WHEN 管理员确认导入, THE 后台管理系统 SHALL 将有效数据写入对应的评估工具，并显示导入结果（成功数和失败数）

### Requirement 6：类型配置管理

**User Story:** 作为管理员，我希望能管理评估工具的类型配置，以便控制不同类型工具在答题页和报告页的行为差异。

#### Acceptance Criteria

1. WHEN 管理员点击列表页筛选区右侧的【类型管理】按钮, THE 后台管理系统 SHALL 弹出类型配置管理弹窗
2. THE 类型配置弹窗 SHALL 展示所有已配置的评估类型，每个类型显示 answerConfig 和 reportConfig 的可编辑配置项
3. WHEN 管理员修改配置并点击【保存】, THE 后台管理系统 SHALL 保存配置到 localStorage（rice_assessment_type_config）并同步到 eval-type-config.json 结构
4. THE 类型配置 SHALL 包含以下可配置项：listMode、cardFields、showScoreDesc、navCollapsedByDefault、quickActions、allowPartialSubmit、reportPage、reportTitle

---

## HTML 文件清单

| 文件名 | 页面说明 | 关联页面 |
|--------|---------|---------|
| `pad/admin-assessment-list.html` | 评估工具列表页（含新建弹窗、类型管理弹窗、导入流程） | → admin-assessment-edit.html |
| `pad/admin-assessment-edit.html` | 评估工具编辑页（含领域树、题目表格、基本信息抽屉、题目编辑抽屉） | ← admin-assessment-list.html, → admin-assessment-import.html |
| `pad/admin-assessment-import.html` | 批量导入独立页面（三步流程：下载模板→上传→预览） | ← admin-assessment-edit.html |

### 页面跳转关系

```
admin-assessment-list ──→ admin-assessment-edit ──→ admin-assessment-import
  (新建弹窗)          ←── (< 返回)              ←── (< 返回编辑页)
  (类型管理弹窗)
```
