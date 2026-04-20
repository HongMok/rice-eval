# 系统数据结构（System Data Schema）

> 本文档梳理评估系统中所有数据结构的字段定义。

---

## 1. 评估工具（Assessment Tool）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 工具唯一标识 |
| name | string | 是 | 工具名称，如"PEP-3" |
| desc | string | 否 | 工具描述 |
| type | string | 是 | 工具类型：pep3 / cpep / vbmapp / common |
| questionCount | number | 是 | 题目总数 |
| status | string | 是 | active=启用, inactive=停用 |
| updatedAt | string | 是 | 最后更新日期 |
| iconClass | string | 否 | 图标CSS类名 |
| avatar | string | 否 | 自定义头像（base64） |
| intro | string | 否 | 工具介绍（HTML富文本） |

---

## 2. 题目配置（Question Config）

按 `{一级分类}__{二级分类}` 分组，每组包含一个题目数组。

### 2.1 题目（Question）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 题目唯一标识 |
| number | number | 是 | 排序号 |
| itemName | string | 是 | 评估项目名称 |
| desc | string | 否 | 操作描述（`\n` 表示换行） |
| materials | string | 否 | 所需材料 |
| ageRange | string | 否 | 适用年龄 |
| required | boolean | 是 | 是否必答 |
| enabled | boolean | 是 | 是否启用 |
| scores | Score[] | 是 | 评分等级数组 |

### 2.2 评分等级（Score）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| value | number | 是 | 分值，如 0, 0.5, 1, 2 |
| label | string | 否 | 标签，如"通过""萌芽""错误" |
| desc | string | 否 | 评分说明 |

---

## 3. 评估记录（Assessment Record）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 记录唯一标识 |
| toolId | string | 是 | 关联的评估工具ID |
| toolName | string | 是 | 工具名称 |
| status | string | 是 | ongoing=评估中, completed=已完成 |
| createdAt | string | 是 | 创建时间 |
| completedAt | string | 否 | 完成时间 |
| assessor | string | 否 | 评估师 |

---

## 4. 答题数据（Answer Data）

以题目ID为key，值为答题项对象。特殊key `_marks` 存储待定标记。

### 4.1 答题项（Answer Item）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| value | number | 是 | 评分分值 |
| label | string | 否 | 评分标签 |
| notes | string | 否 | 备注文字 |
| rounds | Round[] | 否 | 回合统计数据（回合模式时存在） |

### 4.2 回合（Round）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| round | number | 是 | 回合序号 |
| result | string | 否 | independent=独立, error=错误, prompted=辅助, null=未答 |

---

## 5. 评估类型配置（Eval Type Config）

### 5.1 类型（Type）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | string | 是 | 类型标识：pep3 / cpep / vbmapp / common |
| name | string | 是 | 类型名称 |
| description | string | 否 | 类型描述 |
| answerConfig | AnswerConfig | 是 | 答题交互配置 |
| reportConfig | ReportConfig | 否 | 报告配置 |

### 5.2 答题交互配置（AnswerConfig）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| listMode | string | 是 | byDomain=按领域分页, byOrder=按排序号合并 |
| cardFields | string[] | 是 | 卡片展示字段：itemName / desc / materials / ageRange |
| showScoreDesc | boolean | 是 | 是否展示评分说明 |
| navCollapsedByDefault | boolean | 是 | 导航分组默认折叠 |
| quickActions | string[] | 是 | 快捷操作：failAll / passAll / nextDomain |
| allowPartialSubmit | boolean | 是 | 允许部分提交 |

### 5.3 报告配置（ReportConfig）

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| reportPage | string | 是 | 报告页面文件名 |
| reportTitle | string | 是 | 报告标题 |
