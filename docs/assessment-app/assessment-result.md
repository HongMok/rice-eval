## 界面4：评估结果路由页 (assessment-result.html)

### 界面路径

```
评估记录列表页
  ├─ [查看报告] ──→ 评估结果路由页 ← 当前界面
  └─ ... ──→ 评估答题页
        └─ [提交评估] ──→ 评估结果路由页 ← 当前界面
```

### 线框图

```
+------------------------------------------------------------------------+
|                                                                         |
|                                                                         |
|                          ⟳ 正在加载评估报告...                          |
|                                                                         |
|                                                                         |
+------------------------------------------------------------------------+
```

### 功能说明

**路由逻辑**

```javascript
const REPORT_PAGES = {
  pep3:   'assessment-result-pep3.html',
  cpep:   'assessment-result-cpep.html',
  vbmapp: 'assessment-result-vbmapp.html'
};

// 匹配优先级：
// 1. URL 参数 tool 直接匹配 REPORT_PAGES
// 2. 从工具列表查找工具 type 再匹配
// 3. 从评估类型配置查找 reportConfig.reportPage
// 4. 均未匹配 → 留在当前页作为通用报告 fallback
```

- 匹配成功：`location.replace(targetPage + '?' + params)`（不留历史记录）
- 跳转通常毫秒级完成，用户几乎无感知

### 新旧功能关系

新功能

---
