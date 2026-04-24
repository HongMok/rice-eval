---
inclusion: auto
---

# 飞书 CLI (lark-cli) 操作指南

本项目已配置飞书 CLI，可直接通过命令行操作飞书文档、多维表格等。

## 环境信息

- CLI 版本：lark-cli 1.0.17
- App ID：cli_a96361aa4879dceb
- 授权用户：Mok (ou_754a42d0dda49f2659bb6b1f4f8d15a8)
- 身份模式：所有命令默认加 `--as user`

## 核心规则

1. 所有文档操作命令必须加 `--as user`（默认 bot 身份无文档权限）
2. 文档定位用 `--doc`（接受 URL 或 doc_token），不是 `--doc-token`
3. 多维表格定位用 `--app-token`
4. 内容格式统一用 Markdown
5. **标题层级严格递进**：写入飞书文档的 Markdown 标题必须严格按层级递进，不允许在同一父标题下出现跨级标题。例如 `##` 下只能出现 `###`，不能直接出现 `##` 或 `####`。将本地 config 文件内容追加到飞书文档时，必须将原文件的标题降级（如原 `##` 降为 `####`），确保嵌入后不破坏文档整体目录结构

---

## 文档操作 (docs)

### 创建文档

```bash
# 基础创建
lark-cli docs +create --as user --title "文档标题" --markdown "# 标题\n正文内容"

# 指定文件夹创建
lark-cli docs +create --as user --folder-token "文件夹token" --title "文档标题" --markdown "# 内容"

# 创建到知识库
lark-cli docs +create --as user --wiki-space "空间ID" --wiki-node "节点token" --title "标题" --markdown "# 内容"
```

返回 `doc_id` 和 `doc_url`，务必保存 `doc_id`。

### 读取文档内容

```bash
# 通过 doc_token
lark-cli docs +fetch --as user --doc "doc_token"

# 通过 URL
lark-cli docs +fetch --as user --doc "https://www.feishu.cn/docx/xxxxxx"
```

返回 JSON，`data.markdown` 字段为完整 Markdown 全文，`data.title` 为标题。

### 更新文档

```bash
# 追加内容（在文档末尾添加）
lark-cli docs +update --as user --doc "doc_token" --mode append --markdown "## 新增内容\n追加的段落"

# 全量覆写（清空原文，写入新内容）
lark-cli docs +update --as user --doc "doc_token" --mode overwrite --markdown "# 全新内容\n替换后的正文"

# 替换全部内容（保留文档属性）
lark-cli docs +update --as user --doc "doc_token" --mode replace_all --markdown "# 替换内容"

# 按标题定位替换某个段落
lark-cli docs +update --as user --doc "doc_token" --mode replace_range --selection-by-title "## 目标段落标题" --markdown "替换后的段落内容"

# 按内容定位替换（用省略号标记范围）
lark-cli docs +update --as user --doc "doc_token" --mode replace_range --selection-with-ellipsis "开始文本...结束文本" --markdown "替换后的内容"

# 在某标题前/后插入
lark-cli docs +update --as user --doc "doc_token" --mode insert_after --selection-by-title "## 某标题" --markdown "插入的内容"

# 同时更新标题
lark-cli docs +update --as user --doc "doc_token" --mode append --new-title "新标题" --markdown "追加内容"
```

update mode 可选值：
- `append` — 末尾追加
- `overwrite` — 全量覆写
- `replace_all` — 替换全部
- `replace_range` — 替换指定范围（需配合 selection 参数）
- `insert_before` — 在定位点前插入
- `insert_after` — 在定位点后插入
- `delete_range` — 删除指定范围

### 搜索文档

```bash
lark-cli docs +search --as user --query "搜索关键词"
```

### 从本地文件写入

markdown 参数支持 `@file` 语法读取本地文件：

```bash
lark-cli docs +create --as user --title "从文件创建" --markdown @./path/to/file.md
lark-cli docs +update --as user --doc "doc_token" --mode overwrite --markdown @./path/to/file.md
```

---

## 多维表格操作 (base)

### 创建多维表格

```bash
lark-cli base +base-create --as user --json '{"name":"表格名称"}'
```

### 表结构管理

```bash
# 列出所有数据表
lark-cli base +table-list --as user --app-token "表格token"

# 创建数据表
lark-cli base +table-create --as user --app-token "表格token" --json '{"table":{"name":"表名","fields":[{"field_name":"字段1","type":1}]}}'

# 列出字段
lark-cli base +field-list --as user --app-token "表格token" --table-id "表ID"

# 创建字段
lark-cli base +field-create --as user --app-token "表格token" --table-id "表ID" --json '{"field_name":"新字段","type":1}'
```

### 数据操作

```bash
# 查询记录
lark-cli base +record-list --as user --app-token "表格token" --table-id "表ID"

# 搜索记录
lark-cli base +record-search --as user --app-token "表格token" --table-id "表ID" --json '{"filter":{"conjunction":"and","conditions":[{"field_name":"字段名","operator":"is","value":["值"]}]}}'

# 批量创建记录
lark-cli base +record-batch-create --as user --app-token "表格token" --table-id "表ID" --json '{"records":[{"fields":{"字段1":"值1","字段2":"值2"}}]}'

# 批量更新记录
lark-cli base +record-batch-update --as user --app-token "表格token" --table-id "表ID" --json '{"records":[{"record_id":"记录ID","fields":{"字段1":"新值"}}]}'

# 删除记录
lark-cli base +record-delete --as user --app-token "表格token" --table-id "表ID" --record-id "记录ID"

# 数据聚合查询
lark-cli base +data-query --as user --app-token "表格token" --table-id "表ID" --json '{"...DSL查询..."}'
```

字段类型编号：1=文本, 2=数字, 3=单选, 4=多选, 5=日期, 7=复选框, 11=人员, 13=电话, 15=链接, 17=附件, 18=关联, 20=公式, 21=创建时间, 22=更新时间, 23=创建人, 24=更新人

---

## 其他可用模块

| 模块 | 命令前缀 | 用途 |
|------|---------|------|
| drive | `lark-cli drive` | 文件/文件夹管理、权限、上传 |
| sheets | `lark-cli sheets` | 电子表格操作 |
| wiki | `lark-cli wiki` | 知识库空间和节点管理 |
| im | `lark-cli im` | 消息和群聊 |
| calendar | `lark-cli calendar` | 日历和日程 |
| contact | `lark-cli contact` | 通讯录 |
| task | `lark-cli task` | 任务管理 |
| approval | `lark-cli approval` | 审批流程 |
| mail | `lark-cli mail` | 邮件 |

查看任意模块帮助：`lark-cli <模块> --help`

---

## Token 获取方式

| Token 类型 | 从哪里获取 |
|-----------|-----------|
| doc_token | 飞书文档 URL 中 `/docx/` 后面的字符串 |
| folder_token | 飞书文件夹 URL 中 `/folder/` 后面的字符串 |
| app_token | 多维表格 URL 中 `/base/` 后面的字符串 |
| wiki_space_id | 知识库设置页面 |

---

## 常用工作流

### 读取文档 → 处理 → 回写

```bash
# 1. 读取
lark-cli docs +fetch --as user --doc "token" -q '.data.markdown'

# 2. 处理内容（AI 分析/总结/改写）

# 3. 回写
lark-cli docs +update --as user --doc "token" --mode append --markdown "处理后的内容"
```

### 本地 Markdown 文件同步到飞书

```bash
lark-cli docs +create --as user --title "文件名" --markdown @./本地文件.md
```

### 飞书文档内容导出到本地

```bash
lark-cli docs +fetch --as user --doc "token" -q '.data.markdown' > 导出文件.md
```
