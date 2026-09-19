# Command: Career Update

当用户发送 **Career Update** 时，按本协议执行。

## 1. 读取状态

读取：

- `README.md`
- `config/eligibility_rules.md`
- `config/scoring_rules.md`
- `config/target_companies.json`
- `profile/matching_profile.md`
- `data/known_jobs.json`
- `data/company_status.json`
- `data/scan_history.jsonl`

## 2. 来源与扫描顺序

1. 逐个检查 `target_companies.json` 中公司的官方 Karriere/Jobs 页面；
2. 对职位实际打开官方详情页或官方 PDF，核验职位、地点、工作形式、职位类型、截止时间和任务；
3. 用定向 Web Search 补漏；搜索结果只能用于发现，不能单独证明职位当前开放；
4. 不得只因页面访问失败或搜索不到就判定职位关闭。

## 3. 新鲜度过滤

- 主推荐榜仅接受可核验发布日期距离扫描日 **不超过 20 个自然日** 的岗位；
- 使用职位官方页面、官方招聘系统或官方 PDF 的发布日期；搜索引擎抓取日期不能作为发布日期；
- 超过 20 天、或官方页面未显示可靠发布日期的岗位，记录为 `excluded_stale_or_undated`，保留用于去重，但不进入推荐榜；
- 若职位被公司明确标记为 newly posted / recently posted，但未给出绝对日期，仍标为 `status_unclear`，不作为合格推荐。

## 4. 资格过滤

仅处理 `Werkstudent`、`Working Student`、`Student Worker`、`freiwilliges Praktikum`、`voluntary internship`。

### 强制排除

- 明确仅限 `Pflichtpraktikum` / mandatory / curricular internship；
- 小型企业，且无可验证的中大型集团归属；
- 与匹配画像无实质关联；
- A 类：通勤超过 60 分钟，或无法确认办公地点与通勤时间；
- B 类：未明确 100% remote in Germany；Hybrid、mobile work、occasional remote 均不符合；
- 已关闭、过期或只剩历史页面的岗位。

若岗位同时接受 freiwillig 与 Pflichtpraktikum，可保留；必须在记录中写明该证据。

## 5. A / B 分类

### A — Stuttgart Local

- 以 Stuttgart Mitte / Hbf 为出发参照；
- 默认使用工作日早高峰公共交通的单程估算；
- 只有地点可确认且通勤 `<= 60` 分钟，才可进入 A 类；
- 线上办公不是硬筛选：未提及、纯现场或无法确认远程方式的职位仍可进入 A 类；但必须如实记录 `remote_mode`，并在排序中低于明确 hybrid/Homeoffice 的职位。

### B — Fully Remote Germany

- 必须有职位页面的 `fully remote`、`100% remote`、`remote within Germany` 或同等明确表述；
- 若公司可远程但职位指定固定办公天数，归为不合格；
- 记录合法工作地点限制，例如仅德国境内 remote。

## 6. 去重与状态

`known_jobs.json` 是所有已见职位数据库，不是 shortlist。

按顺序判断重复：

1. 相同官方 URL；
2. 相同公司 + 标准化标题 + 工作地点/remote 类别；
3. 标题改写但招聘编号、任务、联系人、地点明显相同。

分类：`NEW`、`UPDATED`、`KNOWN`、`EXCLUDED`、`CLOSED`。

所有第一次见到的可识别岗位均写入数据库，包括不合格岗位，以防重复报告。只有 NEW/UPDATED 且满足硬条件的岗位进入推荐榜。

## 7. 输出

报告保存为 `reports/YYYY-MM-DD.md`，用中文说明，并保留职位原文和中文对照。报告分别给出：

1. A 类合格岗位（含明确 hybrid 与未说明/现场的工作形式标记）；
2. B 类合格岗位；
3. 新发现但被排除的岗位及具体原因；
4. 已知职位的状态变化；
5. 来源覆盖和无法确认项；
6. 去重自检结果。

只有明显合适的岗位才在 `Werkstudent/` 或 `Freiwilliges-Praktikum/` 建立详细 MD。

## 8. 写回与复检

完成后：

1. 更新 `known_jobs.json`；
2. 更新 `company_status.json`；
3. 追加 `scan_history.jsonl`；
4. 创建本次报告；
5. 复检数据库条数、每个新增职位的唯一性、报告存在性及链接可访问性。
