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
| 评估系统-后台 | BTncdy8GmoVxnIxOH8acfaaIncb | [打开](https://www.feishu.cn/docx/BTncdy8GmoVxnIxOH8acfaaIncb) | docs/assessment-admin.md |
| 评估系统-App | Er68dImupozTDZx2bGOc3ehRnwh | [打开](https://www.feishu.cn/docx/Er68dImupozTDZx2bGOc3ehRnwh) | docs/assessment-app.md |
| 评估系统-评分规则 | BjGwdQoz9o4e2GxTVJXcyK6ynMh | [打开](https://www.feishu.cn/docx/BjGwdQoz9o4e2GxTVJXcyK6ynMh) | config/scoring-mode-rules.md |
| 评估系统-通用报告规则 | WM9ldPP7fo2em7xSSXucn9ySnvb | [打开](https://www.feishu.cn/docx/WM9ldPP7fo2em7xSSXucn9ySnvb) | config/report-prompt-common.md |
| 评估系统-PEP3报告规则 | NT4PdWfBVo31K9xbwgNcRSVvnCb | [打开](https://www.feishu.cn/docx/NT4PdWfBVo31K9xbwgNcRSVvnCb) | config/report-prompt-pep3.md |
| 评估系统-CPEP报告规则 | SqW9dz8KyoOO4Sxdy9acavlVnie | [打开](https://www.feishu.cn/docx/SqW9dz8KyoOO4Sxdy9acavlVnie) | config/report-prompt-cpep.md |
| 评估系统-VBMAPP报告规则 | HtYkde3c3o8rA7xG9jbcyoxanrf | [打开](https://www.feishu.cn/docx/HtYkde3c3o8rA7xG9jbcyoxanrf) | config/report-prompt-vbmapp.md |
| 评估系统-通用IEP规则 | BHHjdfnRwoQJpyxmsNZc6S4snSe | [打开](https://www.feishu.cn/docx/BHHjdfnRwoQJpyxmsNZc6S4snSe) | config/iep-prompt-common.md |
| 评估系统-PEP3 IEP规则 | IRGbdbt4OowujBxiZ9LcaSlongb | [打开](https://www.feishu.cn/docx/IRGbdbt4OowujBxiZ9LcaSlongb) | config/iep-prompt-pep3.md |
| 评估系统-CPEP IEP规则 | UWfHdv2C8omDYhxQET0c0jpxnKg | [打开](https://www.feishu.cn/docx/UWfHdv2C8omDYhxQET0c0jpxnKg) | config/iep-prompt-cpep.md |
| 评估系统-VBMAPP IEP规则 | VTkodfXgtoLIhCxyubGc1JLcnTg | [打开](https://www.feishu.cn/docx/VTkodfXgtoLIhCxyubGc1JLcnTg) | config/iep-prompt-vbmapp.md |
| 评估系统-PEP3工具介绍 | Ol8rd7WrzoUpqdxLYcUcggYln3g | [打开](https://www.feishu.cn/docx/Ol8rd7WrzoUpqdxLYcUcggYln3g) | config/tool-intro-pep3.md |
| 评估系统-CPEP工具介绍 | AwfCdxLnIoHlm6xXdJec7rIlnJc | [打开](https://www.feishu.cn/docx/AwfCdxLnIoHlm6xXdJec7rIlnJc) | config/tool-intro-cpep.md |
| 评估系统-VBMAPP工具介绍 | E9dQdf1s2oWMHrx9HQkcioxBnib | [打开](https://www.feishu.cn/docx/E9dQdf1s2oWMHrx9HQkcioxBnib) | config/tool-intro-vbmapp.md |
| 评估系统-PEP3使用声明 | SRAkdJDvJoxHnnxC1wTc7hEMnMc | [打开](https://www.feishu.cn/docx/SRAkdJDvJoxHnnxC1wTc7hEMnMc) | config/tool-disclaimer-pep3.md |
| 评估系统-CPEP使用声明 | Fz6Hds452ohOLuxj8A0cNXMznGd | [打开](https://www.feishu.cn/docx/Fz6Hds452ohOLuxj8A0cNXMznGd) | config/tool-disclaimer-cpep.md |
| 评估系统-VBMAPP使用声明 | U2ECd9SP5oJMMzxMsgqco0kHn8e | [打开](https://www.feishu.cn/docx/U2ECd9SP5oJMMzxMsgqco0kHn8e) | config/tool-disclaimer-vbmapp.md |

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
