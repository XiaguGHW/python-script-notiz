# Eligibility Rules

## 职位类型

### 允许

- Werkstudent / Werkstudentin
- Working Student / Student Worker
- freiwilliges Praktikum / freiwillige:r Praktikant:in
- voluntary internship
- 同时明确接受 freiwillig 与 Pflichtpraktikum 的 Praktikum

### 硬排除

仅限 Pflichtpraktikum 的职位，包括：

- `Pflichtpraktikum`
- `mandatory internship`
- `curricular internship`
- 招聘页面明确写明只接受学校规定的必修实习

记录为：

```json
{
  "eligibility_status": "excluded_mandatory_internship",
  "exclusion_reason": "Only Pflichtpraktikum accepted"
}
```

## 公司规模

默认合格标准：

- 公司员工数至少约 250；或
- 为可核验的中大型集团、其德国子公司或专业业务单元。

不因广告页面未写员工数就猜测；无法可靠判断时标记 `company_size_unverified`，不进入主推荐榜。

## A 类：Stuttgart Hybrid

同时满足：

- 办公地点可确认；
- 从 Stuttgart Mitte/Hbf 的公共交通单程估算不超过 30 分钟；
- 职位页面明确支持 Homeoffice、mobile work、hybrid 或固定/弹性线上工作部分。

## B 类：Fully Remote Germany

同时满足：

- 职位页面明确为 fully remote / 100% remote / remote within Germany；
- 无固定到岗频率；
- 明确的工作地法律限制允许人在德国远程工作。

“Hybrid”、“mobile work possible”或“occasional home office”不满足 B 类。

## 不确定状态

任一硬条件无法由官方页面确认时：

- 不推断为合格；
- 记为 `status_unclear`；
- 可在报告的待确认区出现，但不进入推荐榜。

## 发布时间新鲜度

主推荐榜只接受**可核验发布日期不超过 20 个自然日**的职位。

- 以扫描日期减去官方发布日期计算；
- 官方招聘页、官方 ATS 系统或官方 PDF 的发布日期有效；
- 搜索引擎索引/抓取日期、网页更新日期、社交媒体转发日期不作为替代；
- 超过 20 天：`excluded_stale_posting`；
- 未显示可靠发布日期：`excluded_undated_posting`；
- 两种情况均写入 `known_jobs.json`，防止以后被误报为 NEW，但不进入推荐榜或详细岗位 MD。
