# Career Monitor — 第三方平台复核扫描（2026-09-19）

本次按放宽后的 A 类规则执行：**Stuttgart Mitte/Hbf 出发、公共交通/步行可在 30 分钟内到岗**为硬条件；职位未声明 Homeoffice 不再排除。B 类仍要求官网明确 **100% remote within Germany**。

## 结果

### A 类：推荐投递（2）

| 优先级 | 公司 | 职位 | 官方发布日期 | 匹配 | 通勤 | 工作形式 | 详情 |
|---:|---|---|---|---:|---|---|---|
| 1 | TransnetBW | Werkstudent Innovation / KI / Digitalisierung – Energiewirtschaft | 2026-08-31（19 天） | 5/5 | Hbf 至办公楼约 850 m，合格 | 未说明 | [详情](../Werkstudent/2026-09-19_transnetbw_innovation_ki_digitalisierung.md) |
| 2 | TransnetBW | Werkstudent Digitale Plattformen – Energiewende | 2026-09-15（4 天） | 4/5 | Hbf 至办公楼约 850 m，合格 | 未说明 | [详情](../Werkstudent/2026-09-19_transnetbw_digitale_plattformen.md) |

两条均为 TransnetBW 官方 ATS 的在读学生职位（Teilzeit/befristet），职位页给出了发布日期、Stuttgart 地址与申请联系人。办公地址是 Heilbronner Str. 51–55；公司官方到访指引说明其距 Stuttgart Hbf 约 850 米，故满足 30 分钟门槛。

### B 类：德国全远程

本轮**没有一条进入推荐**。在可访问的第三方结果和回查的官网页中，没有同时满足“Werkstudent/允许 freiwilliges Praktikum + 官网明确 100% remote Germany + 官网发布日期 ≤20 天 + 中大型公司 + 背景匹配”的岗位。

### 已记录但不推荐（避免下次重复）

| 公司 | 职位 | 状态 | 原因 |
|---|---|---|---|
| Mercedes-Benz Bank | Werkstudent*in Cyber Security, SIEM & AI Security | 排除（发布日期未核验） | 官网页面未展示可核验发布日期；第三方显示“2 天前”不能替代官网日期。内容本身匹配度高。 |
| Mercedes-Benz AG | Werkstudent*in Drive Systems Software & Calibration Engineering – Development Process Steering | 排除（发布日期未核验） | 官网页面未展示可核验发布日期；并且 Sindelfingen 的通勤未做独立核验。 |
| TransnetBW | Pflichtpraktikant Energiewirtschaft – Netzengpassmanagement | 硬排除 | 标题明确为 Pflichtpraktikant。 |

## 本轮来源与核验方式

- **第三方发现层**：Stepstone（检索 Werkstudent Python / Stuttgart，读取岗位卡中的职类、地点、相对新鲜度与链接）。
- **官方核验层**：TransnetBW 官方 ATS；Mercedes-Benz 官方职位页。
- **受限来源**：Indeed 对当前浏览会话要求额外安全验证，因此停止访问，未尝试绕过。
- **规则**：第三方的“x 天前”仅用于发现，绝不替代官网发布日期；官网未显示发布日期的职位已进入 known database，但不进推荐榜。

## 本轮自检

- [x] 每条推荐都有官方职位页、官方发布日期、允许合同类型、地点与公司规模依据。
- [x] 推荐条目已写入 `data/known_jobs.json`，后续扫描按稳定 ID 去重。
- [x] 明确 Pflichtpraktikum 已排除并记录。
- [x] 未把“未说明 Homeoffice”的斯图岗位排除。
- [x] 未把第三方相对发布日期当作官方发布日期。
