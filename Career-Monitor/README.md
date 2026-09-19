# Career Monitor

用于持续监控符合个人背景的 **Werkstudent** 与 **freiwilliges Praktikum** 岗位。

## 执行命令

**Career Update**

执行时读取已有状态、扫描官方公司招聘页和定向 Web 搜索、核验当前职位、去重，并生成中文报告。

## 两个严格类别

| 类别 | 地点要求 | 工作形式 |
|---|---|---|
| A — Stuttgart Local | 从 Stuttgart Mitte 出发，公共交通单程不超过 30 分钟 | 线上办公不是硬条件；有明确 Homeoffice/hybrid 会提高排序 |
| B — Fully Remote Germany | 公司办公地不在 Stuttgart 也可 | 岗位必须明确可在德国境内 100% remote；仅 Hybrid 不合格 |

## 所有类别的硬条件

- 职位类型仅限 Werkstudent 或明确接受 freiwilliges Praktikum；
- 仅要求 Pflichtpraktikum 的岗位直接排除；
- 中大型企业：默认至少 250 名员工，或有可核验的中大型集团归属；
- 与个人的 Fahrzeugtechnik、Python、AI/ML/LLM、数据处理、自动化、机器人、仿真、工程数据背景相关；
- 只把当前官方来源能核验为开放、且发布时间不超过 20 天的岗位放入推荐清单。

## 目录

- `config/`：筛选、评分、公司池
- `profile/`：匹配画像
- `data/`：已见岗位、公司扫描状态、历史
- `reports/`：每次扫描报告
- `Werkstudent/`、`Freiwilliges-Praktikum/`：仅保存明显合适且需要长期跟进的详细岗位 MD
