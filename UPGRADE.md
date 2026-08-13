# DoctorWhy v4.0 升级说明

> 基于 `docs/doctorwhy-evaluation.md` 测评整改。本次升级统一了仓库内两个分叉的 SKILL.md，修复规则库加载、索引与自评评测等问题。

## 升级内容（v3.0.0 → v4.0.0）

### P0 · 分发与工程化修复
1. **统一双版本**：根目录 `SKILL.md` 与 `skills/doctorwhy/SKILL.md` 统一为同一 v4.0.0 内容，消除之前"两套流程、互相打架"的维护分叉。
2. **规则库索引补全**：修正之前打包版漏掉 `rules-specimen.md` 的索引 bug，现为完整 9 库；修正"90 条 vs 80 条"数字歧义，统一为"9 类约 90 条"。
3. **强制加载规则库**：SKILL.md 明确"进入 Phase 3 必须读取对应 `references/rules-*.md`"，禁止仅凭内嵌摘要判断合规，避免 81 条规则成为死代码。
4. **description 触发词 + allowed-tools**：description 增加医疗/影像/检验/器械/LIS 等触发关键词；`allowed-tools` 给出 `Read, Grep, WebSearch, Glob`，提升自动触发率与读规则库能力。
5. **本地补装 references/**：完整 9 个规则库文件已装入 `.trae/skills/DoctorWhy/references/`，本地不再是"只有 9 条内嵌规则"的空壳。

### P1 · 提问体验与聚焦
6. **封闭式选项提问**：新增"封闭式选项优先"规范（2-3 互斥选项 + 逃生门），对齐 feature:interviewer 的提问方式，降低用户认知负担。
7. **砍 UI/登录越界**：设备 UI 维度收敛为"仅医疗特有约束"（高对比/隔距读屏/色盲警示/防误触/克制文案），明确消费级 UI 设计不在本 skill 范围，聚焦影像/检验/器械/LIS 护城河品类。

### P1 · 可信评测
8. **重建 evaluation/cases.md**：
   - 声明并废止"全部 15/15 自评满分"的偏差；
   - 每用例增加**无 SKILL 基线对照**与**独立评分人盲评**要求；
   - 新增 **C6 红线回归用例**（"AI 直接出报告不复核"必须拒绝），把安全承诺纳入回归；
   - 尚未独立复核的分数一律标 `待复核`，禁止填满分。

### P2 · 边界声明
9. 新增 `docs/doctorwhy-evaluation.md` 测评报告，明示"提示词级红线 ≠ 合规保障"的能力边界。

## 变更文件

| 文件 | 变更 |
|---|---|
| `SKILL.md` | v3.0.0 → v4.0.0（统一，含全部 P0/P1 修复） |
| `skills/doctorwhy/SKILL.md` | v3.0.0 → v4.0.0（与根目录一致） |
| `evaluation/cases.md` | 重建：基线对照 + C6 红线回归 + 待复核标记 |
| `docs/doctorwhy-evaluation.md` | 新增：严格模式测评报告 |
| `.trae/skills/DoctorWhy/references/` | 本地补装 9 个规则库（GitHub 侧 `references/` 内容不变） |

## 未做（留给后续）
- 多模型验证（Claude/GLM/豆包）与发布 CI。
- `eval_score.py` 的 CI 对接（等独立评分数据后做）。

---

## 热修复（v4.0.0 → v4.0.1）

> 基于 2026-08-13 严格复查：v4.0.0 声称"规则库索引补全"但**分发路径**仍有 2 处缺失，且各平台版本声明未同步。本次修复。

### P0 · 分发路径规则库补全
1. **`skills/doctorwhy/references/` 补 `rules-specimen.md`**：此前该打包路径只有 8 库（漏标本规则），现补全为 9 库，与根目录 `references/` 一致。
2. **`trae/skills/DoctorWhy/references/` 全量补装**：此前该路径只有 `SKILL.md`、无 `references/`（Phase 3 规则库加载在 Trae 侧为空壳），现复制完整 9 库。

### P0 · 版本声明同步
3. `.codex-plugin/plugin.json`：version `3.0.0` → `4.0.0`。
4. `gemini-extension.json`：version `3.0.0` → `4.0.0`。

### P1 · 口径与强制加载同步
5. `README.md`：规则数 `9 类、90 条` → `9 类、97 条`（实际纯规则 97 条，此前少报）。
6. `AGENTS.md`：Phase 3 明确"**必须读取 references/rules-*.md**"，与 SKILL.md 对齐。
7. `.cursor/rules/doctorwhy.mdc`：Phase 3 同样明确"必须读取 references/rules-*.md"。

### 变更文件
| 文件 | 变更 |
|---|---|
| `skills/doctorwhy/references/rules-specimen.md` | 新增（补全为 9 库） |
| `.trae/skills/DoctorWhy/references/` | 新增 9 个规则库 |
| `.codex-plugin/plugin.json` | version → 4.0.0 |
| `gemini-extension.json` | version → 4.0.0 |
| `README.md` | 90 条 → 97 条 |
| `AGENTS.md` | Phase 3 强制加载规则库 |
| `.cursor/rules/doctorwhy.mdc` | Phase 3 强制加载规则库 |

---

## 定位升级（v4.0.1 → v4.1.0）

> 应开发者质疑"产出示意骨架有什么意义"与"数据流没人看"，将 skill 定位从"只问清楚 + 示意骨架"升级为"辅助开发直到能交付"。

### 定位：示意骨架 → 向交付级靠拢
1. **能力边界重写**：产出"向交付级靠拢的可运行代码"——按真实工程标准写（错误处理/日志/数据安全/边界处理），目标辅助开发直到交付。**合规注册、临床验证、上市准入（NMPA/FDA）仍明确不在范围内**，交付时列出"上线缺口"，不宣称可直接上线。
2. **红线合规替代**："示意骨架 + 标注不可用于实际" → "降级为演示实现 + 明确标注上线缺口"。

### 数据流：强制输出 → 内部收敛工具
3. 数据流图不再作为**强制输出项**；Phase 4 收敛判定保留，但改为"能说清数据流/模块/接口（不必画图）"。
4. 输出协议第 1 项改为**架构概要**（1-3 句 + mermaid 可选），第 4 项代码改为"向交付级靠拢 + 标注上线缺口"，自检表项同步。

### 变更文件
| 文件 | 变更 |
|---|---|
| `SKILL.md` | v4.0.1 → v4.1.0（定位/输出协议/收敛措辞） |
| `skills/doctorwhy/SKILL.md` | 与根目录同步 v4.1.0 |
| `.trae/skills/DoctorWhy/SKILL.md` | 与根目录同步 v4.1.0 |
| `AGENTS.md` | 输出 schema + 收敛措辞同步 |
| `.cursor/rules/doctorwhy.mdc` | 输出 schema + Phase 4 措辞同步 |
| `README.md` | 定位/教学模式/落地模式/流程图措辞同步 |

---

## v5.0 · 品类框架扩展 + 规则库扩容（v4.1.0 → v5.0.0）

> 按 v5.0 升级方向落地：新增 3 个品类框架与 3 个规则库，规则从 9 类 91 条扩容至 12 类 151 条；同时纠正此前"97 条"虚报（实际 91 条）。

### 新增品类框架（SKILL.md 提问框架 + 各自追问维度）
| 品类 | 覆盖 | 对应规则库 |
|---|---|---|
| **病理学（切片/数字病理）** | 制片链路/切片质量/对照/判读复核/切缘/WSI/追溯 | `rules-pathology.md` |
| **AI 辅助诊断（模型/验证/监管）** | 用途定位/临床评价/人机协同/可解释/版本治理/漂移监控/失败安全 | `rules-ai-diagnosis.md` |
| **ICU 实时监测（重症/监护/报警）** | 采样率/伪差/报警分级/疲劳管理/趋势变化率/失效安全/审计 | `rules-icu-monitoring.md` |

### 新增规则库（各 20 条，格式与现有 9 库一致：规则+为什么+踩坑+标准来源+点破矛盾）
- `references/rules-pathology.md`（制片厚度/固定/染色对照/切缘/双重阅片/WSI 层级/色彩校准/AP-LIS 闭环等 20 条）
- `references/rules-ai-diagnosis.md`（辅助 vs 自动诊断监管/防泄漏/代表性/人机协同/可解释/版本治理/PMS/确定性/输入质控/OOD/亚组/审计等 20 条）
- `references/rules-icu-monitoring.md`（采样率/阈值个性化/报警疲劳/分级/伪差/变化率报警/失效安全/可追溯/EMR 转录/设备联动等 20 条）

### 修正与同步
- **条数实报**：纠正 README/SKILL.md 虚报"97 条"→ 实报 9 类 **91 条**；扩容后 12 类 **151 条**。
- 触发词增加：`ICU / 重症 / 监护 / 报警`；description 提到病理/AI诊断/ICU 隐含矛盾。
- 延迟加载示例新增 3 条品类→规则库映射。
- README 目录树、品类表、Roadmap 同步；AGENTS/.mdc 用通配 `rules-*.md` 自动覆盖新库，无需改。

### 变更文件
| 文件 | 变更 |
|---|---|
| `references/rules-pathology.md` | 新增（20 条） |
| `references/rules-ai-diagnosis.md` | 新增（20 条） |
| `references/rules-icu-monitoring.md` | 新增（20 条） |
| `SKILL.md` | v4.1.0 → v5.0.0（3 品类框架/索引 12 类 151 条/触发词/changelog） |
| `README.md` | 品类表/目录树/条数/Roadmap 同步 |
