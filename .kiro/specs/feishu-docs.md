# 飞书文档索引

> 本文件记录飞书云端文档的结构索引，便于通过 lark-cli 快速读取和修改。

---

## 文件夹信息

- 父文件夹：评估系统
- folder_token：`Cd5MfnUzIlntStdWpoRc4YgAnOb`
- 飞书链接：https://lzp64bmueb.feishu.cn/drive/folder/Cd5MfnUzIlntStdWpoRc4YgAnOb

---

## 文档目录

| 文档名称 | doc_token | 飞书链接 | 对应本地文件 |
|---------|-----------|--------|-----------|
| 评估工具后台管理系统 — 产品需求文档 | BTncdy8GmoVxnIxOH8acfaaIncb | [打开](https://www.feishu.cn/docx/BTncdy8GmoVxnIxOH8acfaaIncb) | docs/assessment-admin.md |
| 康复师App端 — 评估答题与结果系统 产品需求文档 | Er68dImupozTDZx2bGOc3ehRnwh | [打开](https://www.feishu.cn/docx/Er68dImupozTDZx2bGOc3ehRnwh) | docs/assessment-app.md |

---

## 快速操作

### 读取文档内容
```bash
# 后台管理
lark-cli docs +fetch --as user --doc "BTncdy8GmoVxnIxOH8acfaaIncb" -q '.data.markdown'

# App端
lark-cli docs +fetch --as user --doc "Er68dImupozTDZx2bGOc3ehRnwh" -q '.data.markdown'
```

### 更新文档（从本地文件覆写）
```bash
# 后台管理
lark-cli docs +update --as user --doc "BTncdy8GmoVxnIxOH8acfaaIncb" --mode overwrite --markdown @./docs/assessment-admin.md

# App端
lark-cli docs +update --as user --doc "Er68dImupozTDZx2bGOc3ehRnwh" --mode overwrite --markdown @./docs/assessment-app.md
```

### 导出飞书文档到本地
```bash
# 后台管理
lark-cli docs +fetch --as user --doc "BTncdy8GmoVxnIxOH8acfaaIncb" -q '.data.markdown' > docs/assessment-admin.md

# App端
lark-cli docs +fetch --as user --doc "Er68dImupozTDZx2bGOc3ehRnwh" -q '.data.markdown' > docs/assessment-app.md
```
