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

## A 类：Stuttgart Local

同时满足：

- 办公地点可确认；
- 从 Stuttgart Mitte/Hbf 的公共交通单程估算不超过 60 分钟；
- 不要求职位页面明确支持 Homeoffice、mobile work 或 hybrid；
- 若有相关表述则记录为排序加分；若未说明或写明现场，也不因此排除。

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

## 新鲜度与截止日期

主推荐榜优先接受**可核验发布日期不超过 20 个自然日**的职位。

若官方页面没有发布日期，仍可接受满足下列全部条件的职位：

- 官方招聘页、官方 ATS 系统或官方 PDF 显示明确申请截止日期；
- 截止日期仍在扫描日之后；
- 截止日期不超过扫描日后的 **3 个月**。

证据规则：

- 官方发布日期和官方截止日期均有效；
- 搜索引擎索引/抓取日期、网页更新日期、社交媒体转发日期与第三方招聘网站日期只用于发现，不得替代官方证据；
- 发布日期超过 20 天但存在上述合格截止日期时，仍可进入推荐榜，并在记录中注明“基于截止日期合格”；
- 截止日期已过：`excluded_expired_deadline`；
- 没有符合条件的官方发布日期或官方截止日期：`status_unclear`；
- 所有这类职位均写入 `known_jobs.json` 防重；仅满足上述任一有效新鲜度证据的职位可进入推荐榜或建立详细岗位 MD。
