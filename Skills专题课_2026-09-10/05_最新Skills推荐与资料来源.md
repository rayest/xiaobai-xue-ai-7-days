# 最新 Skills 推荐与资料来源

核查日期：2026-09-09。这里的“推荐”是按本课学员用途做的选择，不是全网效果排名。已在线打开下列一手文档、仓库或具体 Skill 页面核对来源与用途；**没有在本机逐一安装和实测这些第三方技能**，不据此保证它们能直接在所有 Codex 环境运行。

## 1. 本班优先顺序

第一优先：本课的 meeting-actions → 自己的业务规则 → skill-creator。
第二优先：文档协作、办公文件类。
第三优先：营销、浏览器与技术类，按岗位选读。

不要把 20 个资源都装进课堂机器。非技术学员先掌握一个不依赖额外工具的业务 Skill，通常比先搭环境更容易完成学习目标。

## 2. 18 项精选：官方与社区分开看

表中的“试用任务”和“检查点”是课程建议；维护者和用途可从链接核对。名字相同不代表实现相同，安装时保留 owner/repo 和实际目录。

| # | Skill / 技能集合 | 来源与定位 | 可以试什么 | 依赖或检查点 |
| --- | --- | --- | --- | --- |
| 1 | skill-creator | [OpenAI 目录](https://github.com/openai/skills)；[Anthropic 实现](https://github.com/anthropics/skills/blob/main/skills/skill-creator/SKILL.md)，不同实现 | 把一个已成功的任务总结成技能 | 优先用当前 Codex 已提供的版本，仍需业务测试 |
| 2 | skill-installer | [OpenAI 官方说明](https://learn.chatgpt.com/docs/build-skills) | 从明确来源安装选中的技能 | 需要网络和文件权限；不等于授权执行包中任意动作 |
| 3 | find-skills | [Vercel Labs](https://github.com/vercel-labs/skills/blob/main/skills/find-skills/SKILL.md) | 查找某项任务的候选 Skill | 会用到发现/安装工具；不替代源码检查 |
| 4 | doc-coauthoring | [Anthropic](https://github.com/anthropics/skills/blob/main/skills/doc-coauthoring/SKILL.md) | 协作写一份内部提案 | 偏文档内容协作，不等同于 Word 排版引擎 |
| 5 | internal-comms | [Anthropic](https://github.com/anthropics/skills/blob/main/skills/internal-comms/SKILL.md) | 写项目更新和内部通知 | 应替换成自己公司的口径与格式 |
| 6 | docx | [Anthropic](https://github.com/anthropics/skills/blob/main/skills/docx/SKILL.md) | 创建或处理 Word 文档 | 文件工具与运行依赖，需打开成品检查 |
| 7 | pptx | [Anthropic](https://github.com/anthropics/skills/blob/main/skills/pptx/SKILL.md) | 把确定的讲稿做成演示稿 | 渲染和字体环境；检查溢出与可读性 |
| 8 | xlsx | [Anthropic](https://github.com/anthropics/skills/blob/main/skills/xlsx/SKILL.md) | 整理表格与公式 | 表格运行环境；抽查公式和口径 |
| 9 | pdf | [Anthropic](https://github.com/anthropics/skills/blob/main/skills/pdf/SKILL.md) | 提取、处理或生成 PDF | 扫描件可能要 OCR；版面与表格提取需检查 |
| 10 | frontend-design | [Anthropic](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md) | 做一个活动落地页 | 要有开发/预览环境；设计质量仍需人工判断 |
| 11 | webapp-testing | [Anthropic](https://github.com/anthropics/skills/blob/main/skills/webapp-testing/SKILL.md) | 验证页面交互 | 浏览器与测试依赖，不适合作为初学者首例 |
| 12 | React best practices | [Vercel 官方集合](https://github.com/vercel-labs/agent-skills) | 检查 React/Next.js 性能模式 | 技术岗位，具体技能名以仓库列表为准 |
| 13 | web-design-guidelines | [Vercel 官方集合](https://github.com/vercel-labs/agent-skills) | 检查网页体验与设计规范 | 适用网页审核，不等于完整用户研究 |
| 14 | agent-browser | [Vercel Labs 工具与配套技能](https://github.com/vercel-labs/agent-browser) | 浏览器任务、页面交互 | 配套 CLI/浏览器依赖；Skill 文件不能替代工具安装 |
| 15 | Marketing Skills | [Corey Haines 社区集合](https://github.com/coreyhaines31/marketingskills) | 文案、SEO、转化优化等营销任务 | 选具体技能；适配中文市场，验证事实和指标 |
| 16 | Superpowers | [obra 社区框架](https://github.com/obra/superpowers) | 开发中的规划、调试与验证流程 | 偏软件工程，会引入较完整工作方法；课后选修 |
| 17 | Supabase Agent Skills | [Supabase 官方集合](https://github.com/supabase/agent-skills) | 数据库与 Supabase 项目实践 | 需要相关技术背景，实际数据库权限另行管理 |
| 18 | Remotion Skills | [Remotion 官方集合](https://github.com/remotion-dev/skills) | 用代码制作视频的工作指导 | 要有 Remotion 开发和渲染环境，不是直接生成视频的模型 |

### 对这班学员，如何选“最好用”

用四个问题筛：我这周会用吗？我知道什么结果算好吗？我的 Codex 有对应工具吗？我愿意维护这套规则吗？四个问题中两项答不出来，先收藏，不急着安装。

本机已经列出 documents、presentations、spreadsheets、pdf、browser 等插件技能，也有个人中文写作等技能。这只能说明讲师当前环境提供了这些入口，**不代表学员安装 Codex 后都会自动拥有同样的插件和调用名**。课堂演示应先检查自己的实际清单。

## 3. 当前生态的几个变化

Agent Skills 已有公开的跨平台格式；Anthropic 原理文章注明 2025-12-18 发布开放标准。格式共享并没有消除宿主差异。[原理与更新](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)

Vercel 于 2026-01-20 发布 skills CLI 与 skills.sh 目录。目录提供发现与流行度线索，安装量不等于业务效果、维护质量或安全保证。[发布说明](https://vercel.com/changelog/introducing-skills-the-open-agent-skills-ecosystem)

当前 OpenAI 官方说明区分本地 Skill 编写与通过 Plugin 分发；Claude Code 也有自己的调用控制和扩展功能。因此教学上应保留“通用格式”和“平台实现”两层，而不把某平台的扩展字段写成全平台标准。[OpenAI](https://learn.chatgpt.com/docs/build-skills)、[Claude Code](https://code.claude.com/docs/en/skills)

不列实时下载量、Star 数或未经核对的“本周第一”，避免明天就过时。若课堂要展示趋势，现场打开目录并注明当时日期，不当作质量结论。[Skills 目录](https://www.skills.sh/)

## 4. 给有基础学员的查找与安装示例

以下命令是课后可选路线，已依据 CLI 官方 README 核对语法，但未在本课程制作过程中执行安装。需要 Node.js/npx、网络和相应写入权限。基础班优先使用本地实操包。[skills CLI](https://github.com/vercel-labs/skills)

```bash
# 查找候选
npx skills find writing

# 先列出仓库提供哪些技能，不安装
npx skills add anthropics/skills --list

# 阅读选中技能及附带文件之后，只安装一个到 Codex
npx skills add anthropics/skills --skill doc-coauthoring --agent codex

# 查看已安装项
npx skills list

# 不再需要时按提示选择范围移除
npx skills remove doc-coauthoring
```

默认不要加 `--all` 或为了省一步跳过所有确认。上面的范围交由 CLI 当前交互确定，安装结束检查实际落点。不要在授课前一刻批量更新；保留已演练的课堂版本。`npx` 自身也可能下载执行工具，预先阅读来源再使用。

## 5. 资料阅读路线

| 顺序 | 一手资料 | 建议阅读问题 |
| --- | --- | --- |
| 入门 1 | [Agent Skills 概览](https://agentskills.io/home) | 它是什么，解决什么 |
| 入门 2 | [Codex Build skills](https://learn.chatgpt.com/docs/build-skills) | 在本课平台如何使用 |
| 入门 3 | [Anthropic 原理文章](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) | 为什么按需加载 |
| 编写 1 | [格式规范](https://agentskills.io/specification) | 哪些是必须项 |
| 编写 2 | [Anthropic skills 目录](https://github.com/anthropics/skills/tree/main/skills) | 不同任务怎么拆文件 |
| 编写 3 | [OpenAI skills 目录](https://github.com/openai/skills) | Codex 的示例和安装来源 |
| 选型 | [Vercel 技能文档](https://vercel.com/docs/agent-resources/skills) | 技术场景可以找哪些技能 |
| 安装 | [skills CLI README](https://github.com/vercel-labs/skills) | 搜索、选择、范围和移除 |
| 对照 | [Claude Code Skills](https://code.claude.com/docs/en/skills) | 哪些字段是平台扩展 |
| 反思 | [Vercel 特定评测](https://vercel.com/blog/agents-md-outperforms-skills-in-our-agent-evals) | 为什么要看触发和任务条件 |

本课资料概述这些来源，不打包第三方仓库代码或全文。下载、改编和对外分发第三方 Skill 时，查看具体目录的 LICENSE；不要假设同一仓库中所有内容都使用相同许可。
