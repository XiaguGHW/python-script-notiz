# Command: HiWi Update

当用户发送 **`HiWi Update`** 时，按以下固定协议执行。

## 1. 读取项目状态

读取：

- `HiWi-Monitor/README.md`
- `HiWi-Monitor/config/faculties.yaml`
- `HiWi-Monitor/config/scoring_rules.md`
- `HiWi-Monitor/profile/matching_profile.md`
- `HiWi-Monitor/data/known_jobs.json`
- `HiWi-Monitor/data/institutes_status.json`
- `HiWi-Monitor/data/scan_history.jsonl`

## 2. 扫描范围

必须扫描：

- F01
- F02
- F03
- F04
- F05
- F06
- F07
- F08
- F10

每个 Fakultät：

1. 先打开 Fakultät 官方 Institute 列表，重新确认当前全部 Institute，避免因机构新增/合并而遗漏；
2. 对每个 Institute 检查官方主页；
3. 检查 Stellenangebote / Karriere / Jobs / Studentische Hilfskräfte / Aktuelles；
4. 搜索关键词 HiWi、studentische Hilfskraft、wissenschaftliche Hilfskraft、SHK、WHK、Student Assistant、Werkstudent；
5. 检查相关 PDF；
6. 使用 Web Search / site search 进行补漏。

## 3. 新旧岗位判断

将发现的岗位与 `data/known_jobs.json` 比较。

`known_jobs.json` 是 **seen-jobs database**，不是“感兴趣岗位清单”。其中必须保留所有已经看过的可识别岗位/旧公告/Initiativziel/低优先级/已排除项，以防后续误报为 NEW。

分类：

- 🆕 NEW：此前数据库中没有出现过的具体岗位
- 🔄 UPDATED：已有岗位但标题、内容、期限、联系人或工作形式发生重要变化
- ✅ KNOWN：已知且无重要变化
- ⛔ KNOWN-EXCLUDED：已知且 `interest_status=excluded`
- ◽ KNOWN-LOW-PRIORITY：已知且 `interest_status=low_priority`
- ❌ REMOVED/CLOSED：原岗位已无法在官网确认开放

### 去重规则

不能只按完整标题逐字比较。按以下顺序判断是否为已知岗位：

1. 相同官方岗位 URL（如果有）优先视为同一岗位；
2. 相同 Institute + 高度相似的 normalized title；
3. 标题轻微改写但 Aufgaben / Ansprechpartner / 项目明显相同，也视为同一岗位并标记 UPDATED；
4. Fakultät 不是唯一键：ILEK、IREUS 等可能在不同 Fakultät 扫描中交叉出现，不能因此重复认定为 NEW；
5. generic initiative target 不能屏蔽未来新出现的具体正式招聘。比如数据库已有 “MIB Data Analytics in Engineering – Initiativanfrage”，未来 MIB 发布一个具体 “Studentische Hilfskraft für ML” 时仍应标为 NEW。

不得因为搜索引擎没有结果就直接判定 CLOSED；优先以 Institute 官方页面为依据。

## 4. 每个岗位必须提取

尽量确认：

- Fakultät
- Institut
- 岗位标题
- 当前状态
- 发布时间
- Bewerbungsfrist
- Beginn
- Stunden/Monat 或 Stunden/Woche
- Aufgaben
- Anforderungen
- Ansprechpartner
- 官方 URL
- 是否明确 Homeoffice / Remote / Hybrid
- 如果没有明确说明，基于任务性质估计 Remote Score，并明确标记为推断

并维护：

- `record_type`
- `interest_status`
- `seen_status`
- `first_seen`
- `last_seen`

`interest_status` 可用：

- `interested`
- `low_priority`
- `excluded`
- `applied`

`record_type` 可区分：

- 正式当前岗位
- 旧公告 / 状态不明确
- initiative target
- Working Student / 非标准 Uni-HiWi
- 外部非 Uni 岗位

## 5. 评分

使用 `config/scoring_rules.md`：

- Remote Score 0–5
- Match Score 0–5
- Combined Score = 0.6 Match + 0.4 Remote

不得将“技术上可远程”写成“官网明确支持远程”。两者必须区分。

## 5.1 自动生成定制申请邮件

当一个岗位同时满足以下两个条件时：

- `Match Score >= 3`
- `Remote Score >= 3`

必须在扫描报告中为该岗位生成一封可直接修改后发送的德语定制申请/询问邮件。

邮件要求：

1. 必须结合 `profile/matching_profile.md`，只选择与该岗位实际任务相关的个人经历；
2. 必须针对岗位的具体 Aufgaben、Anforderungen、研究方向和 Institute 撰写，不能只套用通用模板；
3. 必须核实准确联系人：优先使用当前官方岗位页面或官方 PDF 中明确列出的 Ansprechpartner；
4. 若岗位公告没有联系人，只能在官方 Institute/Arbeitsgruppe 页面能够明确确认该岗位负责人的情况下使用其姓名；
5. 姓名、性别、学位或称谓不确定时不得猜测。无法确认个人联系人时使用 `Sehr geehrte Damen und Herren`，并在报告中标记“联系人未能可靠确认”；
6. 报告中同时列出联系人姓名、官方 E-Mail（如有）及其官方来源 URL，方便发送前复核；
7. 官网未明确 Remote/Homeoffice 时，邮件只能礼貌询问是否可部分线上工作，不能写成已经支持 Remote；
8. Remote/Homeoffice 询问必须作为一个完全独立的可选段落，不能使用依赖前后文的连接词、代词或编号。删除该段后，邮件的称呼、申请动机、附件说明和结尾仍须语法完整、逻辑连贯，可直接发送；
9. `Match Score < 3` 或 `Remote Score < 3` 时，默认不生成完整定制邮件。

## 6. 输出格式

输出两个层级：

### A. 本次新增/重要更新

优先列所有 🆕 NEW 和 🔄 UPDATED。

已经标记 `excluded` 或 `low_priority` 的旧岗位再次出现时，不进入 NEW 清单。

### B. 9 个 Fakultät 最新清单

分别给 F01、F02、F03、F04、F05、F06、F07、F08、F10 一个当前值得关注的排名清单。

表格至少包括：

| Faculty | Institute | Position | Status | Remote | Match | Combined |

每个 Fakultät 内按 Combined Score 排序。

默认主清单优先显示 `interested`；`excluded` 不进入推荐榜，除非岗位发生实质变化导致需要重新评估。

## 7. 更新项目

扫描完成后：

1. 将 **所有本次第一次见到的可识别岗位** 追加到 `data/known_jobs.json`，不论用户是否感兴趣；
2. 对不感兴趣的新岗位也必须登记为 `low_priority` 或 `excluded`，避免下一次再次被当成 NEW；
3. 更新已有岗位状态和 `last_seen`；
4. 更新 `data/institutes_status.json` 的 last_full_scan；
5. 在 `data/scan_history.jsonl` 追加本次扫描记录；
6. 在 `reports/YYYY-MM-DD.md` 保存完整扫描报告；
7. 对高价值的新岗位，如用户要求或明显值得长期保留，可在 `../HiWi/` 新建统一格式岗位 MD。

## 8. 稳定性原则

- 官网优先于搜索引擎
- 当前页面优先于旧 PDF
- PDF 内容需实际检查，不仅依赖搜索摘要
- 每个 Fakultät 必须有 coverage 结果
- 页面访问失败要显式记录，不能把访问失败当作无岗位
- 不重复推荐数据库里已知岗位作为“新岗位”
- `known_jobs.json` 必须记录“所有看过的岗位”，而不只是 shortlist
