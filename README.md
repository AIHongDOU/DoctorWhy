<p align="center">
  <img src="docs/images/logo.png" width="280" alt="DoctorWhy mascot"/>
</p>

<h1 align="center">DoctorWhy</h1>

<p align="center">
  <em>说不清的医疗需求,它替你一点一点问清楚,然后出示意骨架方案。</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Claude%20Skill-ready-2f81f7?style=flat-square" alt="Claude Skill">
  <img src="https://img.shields.io/badge/Claude%20Code%20%7C%20Codex%20%7C%20Trae%20%7C%20Cursor-2f81f7?style=flat-square" alt="Works with">
  <img src="https://img.shields.io/badge/MIT%20License-3fb950?style=flat-square" alt="MIT license">
  <img src="https://img.shields.io/github/stars/AIHongDOU/DoctorWhy?style=flat-square" alt="Stars">
</p>

---

还在为"怎么跟 AI 讲医疗需求"发愁?你不是一个人。

你会说"我要在 100X 扫描的时候分类细胞",但说不清要**边拍边分**还是**拍完再分**、分类到什么粒度、结果给谁看。你说了一大段,AI 点头,然后写出一堆你不知道对不对的东西。

DoctorWhy 换个方式:它**不急着写**,它问你。

## 它怎么干活

你的需求越模糊,它越来劲:

```
开发者:我想在100X扫描的时候,可以分类细胞类别。

→ 分类是"边拍边分"还是"拍完再分"?
→ 你要分到什么程度?(粗分类 / 40分类骨髓学)
→ 结果给谁看?(出报告 / 辅助技师)
→ 扫描时分类拖慢0.5秒一张,能接受吗?

开发者:边拍边分,40分类,出报告医生看,不能拖慢。

→ 输出:数据流图 + 接口骨架 + 缓存/坐标方案
```

```
开发者:登录界面太普通不美观。

→ 这个登录界面是谁在用?
→ "太普通"具体是哪不满意?
→ 要显示产品名/型号/版本号吗?
→ 将来要支持工牌扫码/刷卡吗?

开发者:值班技师用,重新设计一版,要产品号,预留扫码。

→ 输出:一版能直接跑的医疗质感登录界面(HTML)
```

它问到你没想清楚的部分全想清楚,然后才动手。更多实弹产物在 [examples/](examples/)。

## 工作方式

它不是"每次都要追问"。需求进来,它**先判断类型**再决定走哪条路:

```mermaid
flowchart TD
    A[医疗/扫描/影像需求] --> B{需求类型?}
    B -- 明确指令(操作清单,无模糊点) --> C[直行:不追问,直接执行]
    B -- 首轮澄清(模糊/新项目) --> D[完整追问流程]
    B -- 迭代轮(已有澄清基础,增量改) --> E[简化输出:改了什么+验证]
    D --> F[教学/落地模式]
    F --> G[输出方案]
```

**三种类型的处理:**

| 类型 | 何时 | 怎么做 |
|---|---|---|
| **明确指令** | 你给的是操作清单("两列排版、去掉标题") | 跳过追问,直接执行,避免"为了问而问" |
| **首轮澄清** | 新项目 / 需求模糊 | 走完整追问流程,产出数据流 + 决策表 + 自检表 |
| **迭代轮** | 已有澄清基础,只做增量修改 | 只输出"改了什么 + 验证结果",不重复问 |

**首轮澄清时选模式:**

- **教学模式**:产出示意骨架,侧重展示医疗暗规则如何影响设计。适合学习/原型。
- **落地模式**:产出真实可用代码,交付时附"合规/验证缺失项清单"(缺哪些才能上线)。

**完整追问流程**(首轮澄清时):

```mermaid
flowchart TD
    A[模糊的医疗需求] --> B[复述理解,确认对齐]
    B --> C[按框架维度推进]
    C --> D[点破隐含矛盾]
    D --> E[补全领域现实]
    E --> F{能画出完整数据流?}
    F -- 否 --> B
    F -- 是 --> G[输出方案]
```

- **追问规则**:小问题、具体到界面/操作、一次一个、医学术语用大白话、按优先级、拆目标、收敛就停。
- **提问框架**:通用(目标→用户→主流程→数据→边界→交付),叠加扫描/影像、UI/登录两个品类。
- **推进机制**:复述对齐 → 按维度走 → 抓矛盾 → 注入现实 → 收敛。

框架决定"往哪问",机制决定"怎么问"。它不靠堆问题碰运气,而是接住任何需求。

## 为什么不能直接丢给通用 AI

描述医疗需求时,开发者往往说出的是**手段**,不是**目的**:

> "我要在 20x 扫描时加模型识别,存细胞坐标转真实物理坐标到缓存库,选区时一瞬间知道区域细胞构成。"

这句话里藏着真正的目标:"选区时一瞬间知道区域构成"。但通用 AI 缺医疗/硬件领域知识,补不上"坐标怎么换算""缓存和正式库什么关系""识别要跑在哪"这些隐含约束。它替你把这些缺口一个个问出来。

## 医疗暗规则库

它比通用模型多知道的医疗现实,沉淀在 `references/` 下 9 类、97 条规则 —— 每条都标注"为什么问(医学现实)+ 踩过什么坑(真实事故)",并在追问时用它点破需求里的隐含矛盾。

| 类别 | 覆盖 |
|---|---|
| 器械 UI 规范 | 高对比/色盲警示/防误触/数据布局 |
| 数据与合规 | PHI/日志/审计/权限/加密/存储边界 |
| LIS/HL7 对接 | 消息结构/ORM-ORU/项目映射/ACK |
| 质控与校准 | 质控门槛/失控/试剂批次/校准追溯 |
| 监管记录与注册 | NMPA/21 CFR Part 11/IEC 62304 |
| 硬件约束 | 低倍先行/坐标标定/机械漂移/油镜异步 |
| 影像 pipeline | 金字塔切片/16-bit/重叠对齐 |
| 临床验证 | 敏感性/特异性/金标准/防泄漏 |
| 标本前处理与样本变量 | 禁欲/液化/稀释/抗凝/温控/双样本 |

**这是通用 AI 抄不走的护城河** —— 抄一套追问流程容易,积累 9 类医疗暗规则难。它来自真实医疗器械开发(MC-01 骨髓分析仪、精子分析、血细胞分析等真实项目)踩过的坑。

## 快速开始

最快的用法,一句话:

> 让 AI 读 `SKILL.md`,然后描述一个模糊的医疗需求,它就开始追问你。

完整安装见下方各工具分节。

## 安装

DoctorWhy 三种形态,按你的环境选择:

1. **读即用(所有环境,最稳,推荐)** —— 把 `SKILL.md` 交给任何 AI 助手,读完即生效。零安装、零依赖、任何环境都能用。**如果下面的插件安装遇到问题,直接用它兜底。**
2. **插件安装(仅标准终端 Claude Code)** —— 像正规软件一样 `/plugin install`,有斜杠命令、可自动触发。
3. **user skill(托管环境,如桌面 App/IDE)** —— 拷进 `~/.claude/skills/`,这个环境原生支持。

### 方式一 · 读即用(所有环境,推荐)

在任意 AI 助手会话里,说一句:

> **"读 `SKILL.md`,按它的规则追问我的医疗需求"**

把本仓库的 `SKILL.md` 交给它(或告诉它路径),读完即生效。**这是对所有人最稳的方式** —— 不依赖网络、不依赖插件系统、不依赖具体工具。

### 方式二 · 插件安装(标准终端 Claude Code)

> 适用:你在**独立终端**里运行 `claude`(标准用法)。若你是桌面 App / IDE 托管环境,请用方式三或方式一。

```bash
# 添加 marketplace
/plugin marketplace add AIHongDOU/DoctorWhy

# 安装插件
/plugin install doctorwhy
```

安装后输入 `/doctorwhy:doctorwhy` 手动进入追问;或抛一个模糊的医疗需求自动触发。

### 方式三 · user skill(托管环境:桌面 App / IDE)

> 适用:你运行 Claude 时**不是**独立终端,而是桌面应用 / IDE 内置(宿主接管了插件系统,`/plugin` 可能报"Unrecognized token"或"not available")。

把 skill 拷进标准 skills 目录(此目录所有环境原生支持):

```bash
git clone git@github.com:AIHongDOU/DoctorWhy.git
mkdir -p ~/.claude/skills/doctorwhy
cp DoctorWhy/SKILL.md ~/.claude/skills/doctorwhy/
cp -r DoctorWhy/references ~/.claude/skills/doctorwhy/
```

新开会话,斜杠命令 **`/doctorwhy`** 即可用;或直接抛一个模糊的医疗需求自动触发。

### Codex (OpenAI)

**插件安装(推荐,支持斜杠调用):**

```bash
codex plugin marketplace add AIHongDOU/DoctorWhy
codex plugin add doctorwhy@DoctorWhy
```

装完在 Codex 会话里可用 `@doctorwhy`(Codex 的 skill 调用方式)触发。

**读即用(备选):**

```bash
git clone git@github.com:AIHongDOU/DoctorWhy.git
cd DoctorWhy
codex
```

进入后说:**"把 SKILL.md 当成系统提示,然后按它的流程追问我的需求"**。

### Trae

Trae 有原生 skill 安装路径(`.trae/skills/`),仓库里已内置适配文件:

```bash
git clone git@github.com:AIHongDOU/DoctorWhy.git
cp -r DoctorWhy/.trae/skills/DoctorWhy .trae/skills/DoctorWhy
```

把 `.trae/skills/DoctorWhy` 拷进你项目的 `.trae/skills/` 目录,Trae 会自动识别。然后:

- 在 Trae 对话里说 **"用 DoctorWhy 帮我问清楚这个需求"**,或直接抛一个模糊的医疗需求自动触发。
- 也可以手动调用 skill(见 Trae 的 skill 面板)。

**读即用(备选)**:对话里粘贴 `SKILL.md` 全文,或说"按 DoctorWhy 的方式追问我的需求"。

### Cursor

```bash
git clone git@github.com:AIHongDOU/DoctorWhy.git
cp DoctorWhy/.cursor/rules/doctorwhy.mdc .cursor/rules/doctorwhy.mdc
```

把 `doctorwhy.mdc` 放进项目 `.cursor/rules/`(或全局),Cursor 会自动应用。然后说:"用 DoctorWhy 帮我问清楚这个需求"。

### Gemini CLI

```bash
gemini extensions install https://github.com/AIHongDOU/DoctorWhy
```

装后 `AGENTS.md` 作为常驻上下文自动加载,检测到模糊医疗需求即触发。

### 通用原则

无论哪个工具:**把 `SKILL.md` 交给 AI**,它就能按这套规则追问你的医疗需求。`references/` 和 `examples/` 是配套素材。

**描述清楚的需求不需要走追问** —— 只有说不清时才需要它。

### 卸载(Claude Code 插件)

```
/plugin uninstall doctorwhy
```

### 常见问题

**`/plugin marketplace add` 报 `Unrecognized token ''` / `not available` 怎么办?**
→ 你运行在**托管环境**(桌面 App / IDE 内置),宿主接管了插件系统,不认 marketplace。改用**方式三(user skill)**或**方式一(读即用)**,这两条在托管环境原生可用。

**装不上 / 报错怎么办?**
- 网络超时 → 优先 SSH 源,或直接用"读即用"(任何工具、任何环境,零安装)。
- marketplace 解析失败 → 如果你是标准终端,`/plugin marketplace update AIHongDOU/DoctorWhy` 后再装;若仍失败,走 user skill 或读即用。
- 命令名 → 插件 skill 是 `插件名:skill名` 格式(`/doctorwhy:doctorwhy`);user skill 是 `/doctorwhy`。或直接抛需求自动触发。

**核心原则:遇到任何安装问题,直接"读即用" —— 把 `SKILL.md` 交给 AI 即可,它一定能用。**

## 仓库结构

```
DoctorWhy/
├── SKILL.md              规则、框架、推进机制、输出协议
├── README.md
├── .claude-plugin/       Claude Code 插件(plugin.json / marketplace.json)
├── .codex-plugin/        Codex 插件(plugin.json)
├── .cursor/rules/        Cursor rules(doctorwhy.mdc)
├── .trae/skills/         Trae skill(DoctorWhy/SKILL.md)
├── gemini-extension.json Gemini CLI 扩展
├── AGENTS.md             Gemini/多工具常驻上下文
├── skills/               Codex skill 载体(doctorwhy/SKILL.md + references)
├── docs/images/          logo、演示图
├── references/
│   ├── rules-device-ui.md  暗规则库·器械 UI 规范(核心资产)
│   ├── rules-compliance.md 暗规则库·数据与合规(核心资产)
│   ├── rules-lis-hl7.md    暗规则库·LIS/HL7 对接(核心资产)
│   ├── rules-qc-calibration.md 暗规则库·质控与校准(核心资产)
│   ├── rules-regulatory.md  暗规则库·监管记录与注册(核心资产)
│   ├── rules-hardware.md    暗规则库·硬件约束(核心资产)
│   ├── rules-imaging.md     暗规则库·影像 pipeline(核心资产)
│   ├── rules-clinical-validation.md 暗规则库·临床验证(核心资产)
│   ├── rules-specimen.md    暗规则库·标本前处理与样本变量(核心资产)
└── examples/
    ├── 登录界面_新版.html  UI 输出示例(浏览器打开)
    └── stitch_demo.py     逻辑输出示例(python 自检)
```

## FAQ

**它和"直接把需求丢给通用 AI"有什么区别?**
通用 AI 会顺着你的话往下编。它会在你觉得对的时候停下来问你——问到你暴露真正的问题。

**要配置吗?**
不用。把 `SKILL.md` 交给 agent 就行。

**问烦了怎么办?**
它只问你没想清楚的部分。你想清楚的,它不重复问。

## Roadmap

- [x] 追问规则 + 提问框架(通用/扫描/UI)
- [x] 输出协议(数据流 + 示意骨架)
- [x] 插件化(Claude Code / Codex / Cursor / Gemini CLI)
- [ ] 更多品类框架(影像 / 检验报告 / 数据合规)
- [ ] 金字塔切片拼接查看器
- [ ] 更多工具适配(OpenCode / Copilot / 其他)

## License

[MIT](LICENSE)。允许自由使用、修改、商用(保留版权声明即可)。
