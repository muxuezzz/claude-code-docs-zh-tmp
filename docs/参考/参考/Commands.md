> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Commands

> Claude Code 中可用命令的完整参考，包括内置命令和捆绑的 skills。

Commands 从会话内部控制 Claude Code。它们提供了一种快速方式来切换模型、管理权限、清除上下文、运行工作流等。

输入 `/` 查看可用的命令，或输入 `/` 后跟字母来筛选。[命令菜单如何匹配你输入的内容](#how-the-command-menu-matches-what-you-type)涵盖了高亮显示、拼写错误以及 Claude Code 在你输入完整名称之前隐藏的少数命令。

命令只在你的消息开头被识别。命令名称后面的文本成为其参数。从 v2.1.199 开始，[skills](/docs/zh-CN/skills#pass-arguments-to-skills)是例外：一个 skill 调用后跟更多 skills，例如 `/skill-a /skill-b do XYZ`，会加载开头命名的每个 skill，并将尾部文本作为参数传递给每个 skill。最多可以链接六个 skills。

如果你在 Claude 响应时发送命令，Claude Code 会将其排队，并在当前轮次完成后运行。Claude Code 会立即运行某些命令而不中断响应，例如 `/status`、`/tasks` 和 `/usage`。在[全屏渲染](/docs/zh-CN/fullscreen)中，Claude Code 也会立即打开对话命令，例如 `/theme` 和 `/help`。在 v2.1.234 之前，Claude Code 会将这些对话排队直到轮次完成。

<h2 id="commands-across-a-typical-workflow">
  典型工作流程中的命令
</h2>

大多数命令在会话的特定阶段很有用，从设置项目到发布更改。

**首次在仓库中的会话。** 运行 `/init` 生成一个启动 `CLAUDE.md`，然后运行 `/memory` 来完善它。使用 `/mcp` 设置项目需要的任何服务器，要求 Claude 创建你想要的任何 [subagents](/docs/zh-CN/sub-agents)，并运行 `/permissions` 来设置你的批准规则。

**执行任务期间。** `/plan` 在大型更改前切换到 plan mode。`/model` 和 `/effort` 调整你使用的模型以及它应用多少推理。当对话变得很长时，`/context` 显示什么在填充窗口，`/compact` 总结它以释放空间。使用 `/btw` 提出不应添加到对话历史的附带问题。

**并行运行工作。** Claude 将附带任务委派给 [subagents](/docs/zh-CN/sub-agents)，`/tasks` 列出当前会话的后台工作，包括已完成的 subagents。`/background` 分离整个会话以继续作为 [background agent](/docs/zh-CN/agent-view) 运行并释放你的终端。对于跨越代码库的大型更改，`/batch` 将其分解为独立单元并在各自的 [worktree](/docs/zh-CN/worktrees) 中运行每个单元。请参阅 [Run agents in parallel](/docs/zh-CN/agents) 了解这些方法如何相关。

**在你发布之前。** `/diff` 显示更改的内容。`/code-review` 检查当前 diff 是否存在正确性错误和清理，并可以使用 `--fix` 应用发现的问题；传递 PR 号码，例如 `/code-review high 1234`，以改为审查拉取请求。`/review` 是一个别名。`/code-review ultra` 在云中运行多代理审查。`/security-review` 检查 diff 是否存在安全漏洞。

**会话之间。** `/clear` 在保持项目内存的同时开始新任务。`/resume` 返回到较早的对话，`/branch` 分支当前对话以尝试不同的方向，`/fork` 将其复制到新的 [background session](/docs/zh-CN/agent-view)。`/teleport` 将网络会话拉入此终端，`/remote-control` 让你从另一台设备继续此本地会话。

**当出现问题时。** `/rewind` 将代码和对话回滚到检查点，或总结对话的一部分。`/doctor` 运行设置检查以诊断安装和配置问题并可以修复它们，`/debug` 诊断运行时问题，`/feedback` 报告附加会话上下文的错误。

<h2 id="all-commands">
  所有命令
</h2>

下表列出了 Claude Code 中包含的所有命令。大多数是内置命令，其行为被编码到 CLI 中。两种条目被标记：

* **[Skill](/docs/zh-CN/skills#bundled-skills)**：一个捆绑的 skill。它的工作方式与你自己编写的 skill 相同：一个提示词交给 Claude。
  * `/verify` 仅在你调用它时运行。在 v2.1.215 之前，Claude 也可以自己运行 `/verify`。
* **[Workflow](/docs/zh-CN/workflows#bundled-workflows)**：一个捆绑的[动态 workflow](/docs/zh-CN/workflows)，它将工作分散到许多子代理中，并在后台运行。
  * `/deep-research` 仅在你调用它时运行。在 v2.1.218 之前，Claude 也可以自己启动它。

要添加你自己的命令，请参阅 [skills](/docs/zh-CN/skills)。

在下表中，`<arg>` 表示必需的参数，`[arg]` 表示可选参数。

<Note>
  并非每个命令都对每个用户显示。可用性取决于你的平台、计划和环境。例如，`/desktop` 仅在 macOS 和 x64 Windows 上使用 Claude 订阅登录时显示，`/upgrade` 在企业计划上不显示。
</Note>

| 命令 | 目的 |
| :- | :- |
| `/add-dir <path>` | 添加一个工作目录以在当前会话期间进行文件访问。输入部分路径以查看匹配的目录建议；按 `Tab` 接受一个。大多数 `.claude/` 配置[不会从添加的目录中被发现](/docs/zh-CN/permissions#additional-directories-grant-file-access-not-configuration)。你无法添加大多数[网络路径](/docs/zh-CN/errors#working-directory-is-a-network-path)，例如 `\\server\share`。成功添加后，你的 [`DirectoryAdded` hooks](/docs/zh-CN/hooks#directoryadded) 会运行。当你在 Claude 响应时运行它时，Claude Code 会要求你立即确认目录，一旦你确认，Claude 在同一轮中的下一个工具调用就可以访问它。在 v2.1.234 之前，Claude Code 会将命令排队直到轮次完成 |
| `/advisor [model\|off]` | 启用或禁用[顾问工具](/docs/zh-CN/advisor)，它在任务期间的关键时刻咨询第二个模型以获得指导。接受 `fable`、`opus`、`sonnet` 或完整的模型 ID。`fable` 需要 [Fable 访问权限](/docs/zh-CN/advisor#choose-an-advisor-model)。没有参数时，打开一个选择器。在没有交互式终端的会话中，或通过 [Remote Control](/docs/zh-CN/remote-control#limitations)，将模型或 `off` 作为参数传递；在那里没有参数时，命令将当前顾问打印为文本。这些形式需要 Claude Code v2.1.260 或更高版本 |
| `/agents` | 从 v2.1.198 开始，运行 `/agents` 会打印一个提醒，要求你要求 Claude 创建或管理[子代理](/docs/zh-CN/sub-agents)，或直接编辑 `.claude/agents/` 或 `~/.claude/agents/`。在 v2.1.197 及更早版本上，打开一个交互式界面来创建和管理子代理配置 |
| `/artifact-capabilities` | **[Skill](/docs/zh-CN/skills#bundled-skills)。** 加载已发布[工件](/docs/zh-CN/artifacts)可以使用的运行时功能的参考，例如[调用你的连接器](/docs/zh-CN/artifacts#pull-live-data-with-mcp-connectors)或[提供文件下载](/docs/zh-CN/artifacts#offer-a-file-download)，包括你的账户拥有的功能。Claude 通常在构建使用其中一个的页面之前自己加载它。在[工件](/docs/zh-CN/artifacts#availability)可用的地方可用 |
| `/artifact-diagramming` | **[Skill](/docs/zh-CN/skills#bundled-skills)。** 为 Claude 在[工件](/docs/zh-CN/artifacts)中遵循的图表加载指导：何时图表有帮助、要绘制什么，以及如何编写在浅色和深色主题中保持清晰的内联 SVG。需要 Claude Code v2.1.221 或更高版本 |
| `/artifacts` | 列出你拥有或与你共享的[工件](/docs/zh-CN/artifacts#find-an-artifact-again)，然后将其附加到会话、在浏览器中打开或复制其链接。在[工件](/docs/zh-CN/artifacts#availability)可用的地方可用。需要 Claude Code v2.1.208 或更高版本；使用 `Enter` 附加需要 v2.1.216 |
| `/auto-mode-setup` | [从你的项目和最近的会话中起草 `autoMode.environment` 条目](/docs/zh-CN/auto-mode-config#generate-environment-entries)，然后审查草稿并将其保存到你的用户设置。需要 Pro、Max 或 Team 计划以及 Claude Code v2.1.228 或更高版本。在原生 Windows 上，需要 v2.1.233 或更高版本 |
| `/autocompact [auto\|<tokens>]` | 设置自动压缩窗口：在 Claude Code 自动压缩之前上下文窗口有多满。传递一个大小，例如 `500k`，或 `auto` 以返回为你的模型调整的窗口。Claude Code 将该值保存到用户设置并将其应用于当前会话。有关接受的值和覆盖它的内容，请参阅[设置自动压缩窗口](/docs/zh-CN/model-config#set-the-auto-compact-window)。没有参数时，打开一个显示当前窗口的对话框。需要 Claude Code v2.1.221 或更高版本 |
| `/autofix-pr [prompt]` | 生成一个 [cloud session](/docs/zh-CN/claude-code-on-the-web#auto-fix-pull-requests) 会话，监视当前分支的 PR 并在 CI 失败或审阅者留下评论时推送修复。使用 `gh pr view` 从你的检出分支检测打开的 PR；要监视不同的 PR，请先检出其分支。默认情况下，云会话被告知修复每个 CI 失败和审阅评论；传递一个提示词以给它不同的指令，例如 `/autofix-pr only fix lint and type errors`。需要 `gh` CLI 和访问 [cloud sessions](/docs/zh-CN/claude-code-on-the-web) |
| `/background [prompt]` | 分离当前会话以作为[后台代理](/docs/zh-CN/agent-view)运行并释放此终端。传递一个提示词以在分离前发送一个更多指令。使用 `claude agents` 监视会话。要将对话复制到新的后台会话中，同时此会话继续运行，请使用 `/fork`。别名：`/bg` |
| `/batch <instruction>` | **[Skill](/docs/zh-CN/skills#bundled-skills)。** 在整个代码库中并行编排大规模更改。研究代码库，将工作分解为 5 到 30 个独立单元，并呈现一个计划。获得批准后，在隔离的 [worktree](/docs/zh-CN/worktrees) 中为每个单元生成一个[后台子代理](/docs/zh-CN/sub-agents#run-subagents-in-foreground-or-background)。每个子代理实现其单元，运行测试，并发布其更改。需要一个 git 存储库或一个[`WorktreeCreate` hook](/docs/zh-CN/worktrees#non-git-version-control)来创建 worktree。在 git 存储库之外，`/batch` 需要 Claude Code v2.1.281 或更高版本。示例：`/batch migrate src/ from JavaScript to TypeScript` |
| `/branch [name]` | 在此点创建当前对话的一个分支，以便你可以尝试不同的方向而不会丢失对话。切换到分支并保留原始分支，你可以使用 `/resume` 返回到它。要运行一个副本作为单独的[后台会话](/docs/zh-CN/agent-view)而不是切换到它，请使用 `/fork`；要将一个侧面任务交给一个[子代理](/docs/zh-CN/sub-agents)，它报告回这个对话，请使用 `/subtask` |
| `/btw [question]` | 询问一个[侧面问题](/docs/zh-CN/interactive-mode#side-questions-with-%2Fbtw)关于当前会话而不添加到对话中。如果你运行 `/btw` 而没有问题，Claude Code 会显示你最近的侧面问题，以便你可以浏览早期的答案；如果你还没有问过，Claude Code 会打印一条使用行。在 v2.1.212 之前，`/btw` 需要一个问题 |
| `/bug [report]` | 报告一个错误或分享你的对话。你选择要包含多少会话历史记录，并在发送任何内容之前在同意屏幕上确认。当你在第一方连接上登录到 Anthropic 时，报告会发送到 Anthropic；在第三方提供商上，或没有 Anthropic 凭证，Claude Code 会将报告写入一个[本地存档在 `~/.claude/feedback-bundles/`](/docs/zh-CN/data-usage#telemetry-services)，你自己转发。在 [VS Code 扩展](/docs/zh-CN/vs-code#use-the-prompt-box)中，`/bug` 打开扩展自己的反馈对话框；需要 Claude Code v2.1.229 或更高版本。当你在 Claude 响应时运行它时，Claude Code 立即打开对话框。在 v2.1.232 之前，Claude Code 会将命令排队直到轮次完成。别名：`/share`。在 v2.1.212 之前，`/bug` 和 `/share` 是 `/feedback` 的别名 |
| `/cd <path>` | 将此会话移动到新的工作目录，保持对话。输入部分路径以查看匹配的目录建议；按 `Tab` 接受一个。建议需要 Claude Code v2.1.206 或更高版本。有关 Claude Code 在移动时立即应用的内容，以及 `/cd` 与 `/add-dir` 的区别，请参阅[将会话移动到另一个目录](/docs/zh-CN/permissions#move-the-session-to-another-directory) |
| `/chrome` | 配置 [Claude in Chrome](/docs/zh-CN/chrome) 设置 |
| `/claude-api [migrate\|upgrade\|managed-agents-onboard\|prompt-audit\|cost-optimize\|build-eval\|hillclimb\|preserved-thinking-migration]` | **[Skill](/docs/zh-CN/skills#bundled-skills)。** 为你的项目的语言加载 [Claude API](https://platform.claude.com/docs/en/api/overview) 和 [Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview) 参考资料。当你的代码导入 `anthropic` 或 `@anthropic-ai/sdk` 时也会自动激活。有关每个子命令的作用和它需要的版本，请参阅[在 Claude API 项目上工作](/docs/zh-CN/skills#work-on-claude-api-projects) |
| `/claude-in-chrome [task]` | **[Skill](/docs/zh-CN/skills#bundled-skills)。** 让 Claude 通过 [Claude in Chrome](/docs/zh-CN/chrome) 在你的浏览器中执行任务，例如测试页面、填充表单或读取控制台日志。当为会话启用 Chrome 集成时可用，例如使用 `claude --chrome`，或当 Claude Code 可以提供[安装扩展](/docs/zh-CN/chrome#install-the-extension-when-claude-asks)时 |
| `/clear [name]` | 使用空上下文启动新对话。传递一个名称以在 `/resume` 选择器中标记上一个对话。要在继续同一对话的同时释放上下文，请改用 `/compact`。使用 `/resume` 恢复上一个对话，或在同一 Claude Code 进程中，从[倒带菜单的上一个会话条目](/docs/zh-CN/checkpointing#rewind-past-a-cleared-conversation)恢复它。别名：`/reset`、`/new` |
| `/code-review [low\|medium\|high\|xhigh\|max\|ultra] [--fix] [--comment] [pr#\|branch\|path]` | **[Skill](/docs/zh-CN/skills#bundled-skills)。** 审查当前差异，或你传递的 PR 号、分支或路径，以查找正确性错误。根据你的模型和工作量级别，审查也涵盖清理机会。传递 `--fix` 以应用发现，`--comment` 以在 GitHub PR 或 GitLab 合并请求上发布它们，或 `ultra` 以运行深度[云审查](/docs/zh-CN/ultrareview)。发布到 GitLab 合并请求需要 Claude Code v2.1.257 或更高版本。在 `github.com` PR 目标上使用 `ultra` 时，传递 `--post` 以在启动对话框中预选[将完成的发现发布到 PR](/docs/zh-CN/ultrareview#post-findings-to-the-pull-request)；`--post` 需要 Claude Code v2.1.227 或更高版本。有关工作量级别、目标和它与 `/simplify` 的关系，请参阅[本地审查差异](/docs/zh-CN/code-review#review-a-diff-locally)。别名：`/review` |
| `/color [color\|default]` | 为当前会话设置提示栏颜色。可用颜色：`red`、`blue`、`green`、`yellow`、`purple`、`orange`、`pink`、`cyan`。使用 `default` 重置，或运行不带参数以选择随机颜色。当 [Remote Control](/docs/zh-CN/remote-control) 连接时，颜色同步到 claude.ai/code。也可在非交互模式 (`-p`) 中使用；需要 Claude Code v2.1.205 或更高版本 |
| `/compact [instructions]` | 通过总结到目前为止的对话来释放上下文。可选地为摘要传递焦点指令。请参阅[压缩如何处理规则、skill 和内存文件](/docs/zh-CN/context-window#what-survives-compaction) |
| `/config [key=value ...]` | 打开[设置](/docs/zh-CN/settings)界面以调整主题、模型、[输出样式](/docs/zh-CN/output-styles)和其他首选项。传递一个或多个 `key=value` 对以直接设置设置而不打开界面，例如 `/config thinking=false`、`/config theme=dark` 或 `/config model=sonnet`。`key=value` 形式也适用于非交互模式 (`-p`) 和来自 Claude 移动应用的 [Remote Control](/docs/zh-CN/remote-control)。`key=value` 形式无法打开需要你在面板中确认的设置，例如 [`autoContinueAtUsageLimit`](/docs/zh-CN/interactive-mode#turn-automatic-continue-off)，尽管它可以关闭一个。运行 `/config --help` 以列出它接受的键。别名：`/settings` |
| `/context [all]` | 将当前上下文使用情况可视化为彩色网格。显示上下文繁重工具、内存膨胀和容量警告的优化建议。当对话超过上下文窗口时，输出包括一个[警告](/docs/zh-CN/errors#context-exceeds-the-token-limit)，显示你超过限制的距离以及哪个命令释放空间。在[全屏模式](/docs/zh-CN/fullscreen)中，`/context` 折叠每项细目以保持网格可见。传递 `all` 以展开它 |
| `/copy [N]` | 将最后的助手响应复制到剪贴板。传递一个数字 `N` 以复制第 N 个最新响应：`/copy 2` 复制倒数第二个。当存在代码块时，显示一个交互式选择器以选择单个块或完整响应。在选择器中按 `w` 以将选择写入文件而不是剪贴板，这在 SSH 上很有用 |
| `/cost` | `/usage` 的别名 |
| `/dataviz [request]` | **[Skill](/docs/zh-CN/skills#bundled-skills)。** 为图表、图形和仪表板提供设计指导。Claude 为数据选择图表形式，按角色分配颜色，使用捆绑脚本验证调色板的色盲安全性和对比度，并应用标记、交互和可访问性规则。使用一个品牌中立的占位符调色板，你用自己的替换。需要 Claude Code v2.1.198 或更高版本 |
| `/debug [description]` | **[Skill](/docs/zh-CN/skills#bundled-skills)。** 为当前会话启用调试日志记录并通过读取会话调试日志来排查问题。调试日志记录默认关闭，除非你使用 `claude --debug` 启动，所以在会话中期运行 `/debug` 会从该点开始捕获日志。可选地描述问题以集中分析 |
| `/deep-research <question>` | **[Workflow](/docs/zh-CN/workflows#bundled-workflows)。** 在问题上扇出网络搜索，获取和交叉检查来源，并综合一个引用的报告 |
| `/design [brief]` | **[Skill](/docs/zh-CN/skills#bundled-skills)。** 在一个画布上起草 UI 模型、屏幕流、登陆页面或海报作为画板，发布为一个 Claude Design [工件](/docs/zh-CN/artifacts#draft-a-design-canvas)，例如 `/design a settings screen for a mobile banking app`。你在桌面浏览器中编辑画板，你的编辑会自动保存。你可以将每个画板导出为 PNG 或 PDF。需要 Claude Code v2.1.265 或更高版本、一个[工件可用](/docs/zh-CN/artifacts#availability)的会话，以及一个[设计模板可用](/docs/zh-CN/artifacts#start-from-a-slides-design-or-docs-template)的账户；如果你的组织已关闭该模板，`/design` 不会起草设计。在 Anthropic API 上可用。在 Amazon Bedrock、Google Cloud 的 Agent Platform、Microsoft Foundry 和 Claude Platform on AWS 上，工件不可用，所以命令在那里不可用 |
| `/design-login` | 使用你的 claude.ai 账户授权 `/design-sync` 的设计系统访问 |
| `/design-sync [hint]` | **[Skill](/docs/zh-CN/skills#bundled-skills)。** 转换你的 repo 的 React 设计系统并将其上传到 [Claude Design](https://claude.ai/design)，以便它生成的设计使用你的真实组件。可选地命名设计系统，例如 `/design-sync Acme DS`。首次同步验证每个组件，在大型 repo 上可能需要几个小时。在 Anthropic API 上可用。它需要 claude.ai，CLI 在 Amazon Bedrock、Google Cloud 的 Agent Platform、Microsoft Foundry 或 Claude Platform on AWS 上不联系，或通过 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway#availability-and-limitations)，所以命令在那里不可用 |
| `/desktop` | 在 Claude Code Desktop 应用中继续当前会话。需要 macOS 或 x64 Windows 和 Claude 订阅。别名：`/app` |
| `/diff` | 审查你的工作树中的更改，包括 Claude 到目前为止所做的编辑。请参阅[使用 /diff 审查更改](/docs/zh-CN/interactive-mode#review-changes-with-%2Fdiff) |
| `/doctor [prompt-audit [path]]` | **[Skill](/docs/zh-CN/skills#bundled-skills)。** 运行一个设置检查，诊断问题并可以修复它们。检查安装健康状况，包括重复或遗留安装、`PATH` 问题和无法解析的设置文件。查找未使用的 skill、MCP 服务器和插件与其上下文成本，标记缓慢的 [hooks](/docs/zh-CN/hooks)，并检查你的[发布频道](/docs/zh-CN/setup#configure-release-channel)上是否有更新版本。根据检入的本地 `CLAUDE.md` 文件进行重复数据删除，通过削减 Claude 可以从代码库派生的内容来修剪检入的 [`CLAUDE.md`](/docs/zh-CN/memory#my-claude-md-is-too-large) 文件，并将保留的始终加载的指导迁移到[skill](/docs/zh-CN/skills) 和按需加载的嵌套 `CLAUDE.md` 文件中。还提供使[自动模式](/docs/zh-CN/permissions#permission-modes)成为你的默认值和[预先批准](/docs/zh-CN/permissions)经常被拒绝的只读命令。首先报告发现并在更改任何内容之前要求确认。从终端，`claude doctor` 打印只读安装诊断而不启动会话。别名：`/checkup`。运行 `/doctor prompt-audit` 以让 Claude [审计你的 `CLAUDE.md` 文件、skill 和其他配置](/docs/zh-CN/memory#audit-your-instruction-files)以查找过时或冲突的指令，而不是运行检查。`prompt-audit` 子命令需要 Claude Code v2.1.283 或更高版本。`CLAUDE.md` 修剪检查需要 Claude Code v2.1.206 或更高版本。在 v2.1.205 之前，`/doctor` 打开一个只读诊断屏幕，按 `f` 将报告发送给 Claude |
| `/effort [level\|auto\|status\|ultracode [on\|off]]` | 设置[工作量级别](/docs/zh-CN/model-config#adjust-effort-level)：`low` 到 `xhigh`、`max` 或 `auto`；`status` 打印它。`ultracode` 或 `ultracode on` 在当前级别为会话打开 [ultracode](/docs/zh-CN/workflows#let-claude-decide-with-ultracode)，`ultracode off` 关闭它；[`ultracode`](/docs/zh-CN/settings-reference#ultracode) 键持久化。`max` 仅限会话。使用 `on` 和 `off` 参数以及保持当前级别需要 Claude Code v2.1.284 或更高版本。在 v2.1.284 之前，`/effort ultracode` 将会话设置为 `xhigh`，`/effort ultracode off` 失败并显示 `Invalid argument`。在 Claude 响应时运行它，一旦你确认[缓存警告](/docs/zh-CN/prompt-caching#changing-effort-level)（如果 Claude Code 显示一个），Claude Code 会将新级别应用于该轮中的下一个请求。在 v2.1.242 之前，Claude Code 从它从 Anthropic 获取的功能标志决定是在轮中期运行命令还是将其排队直到轮次完成，并始终在不[获取功能标志](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching)的会话中排队它，例如在[第三方提供商](/docs/zh-CN/third-party-integrations)上。在 `-p` 中工作 |
| `/exit` | 退出 CLI。在附加的[后台会话](/docs/zh-CN/agent-view#attach-to-a-session)中，这会分离，会话继续运行。别名：`/quit` |
| `/export [filename]` | 将当前对话导出为纯文本。使用文件名，直接写入该文件。没有，打开一个对话框以复制到剪贴板或保存到文件 |
| `/fast [on\|off]` | 切换[快速模式](/docs/zh-CN/fast-mode)打开或关闭。在 Claude 响应时运行它，Claude Code 切换快速模式而不等待轮次结束，尽管运行的轮次以其原始速度完成。在 v2.1.242 之前，Claude Code 从它从 Anthropic 获取的功能标志决定是在轮中期运行命令还是将其排队直到轮次完成，并始终在不[获取功能标志](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching)的会话中排队它。非交互模式中的可用性受限于 `-p`；请参阅[切换快速模式](/docs/zh-CN/fast-mode#toggle-fast-mode)。需要 Claude Code v2.1.205 或更高版本 |
| `/feedback [report]` | 发送关于 Claude Code 的产品反馈。打开与 [`/bug`](#all-commands) 相同的对话框，具有相同的同意步骤、发送规则和轮中期行为。在具有 [Claude 起草的反馈](/docs/zh-CN/tools-reference#sendfeedback-tool-behavior)的会话中，不带参数的 `/feedback` 打开草稿队列，你可以在其中审查、编辑、发送或丢弃 Claude 排队的草稿；队列包括一个选项来在对话框中写入新报告。使用参数，对于 `/bug` 总是，对话框直接打开 |
| `/fewer-permission-prompts` | **[Skill](/docs/zh-CN/skills#bundled-skills)。** 扫描你的记录以查找常见的只读 Bash 和 MCP 工具调用，然后将优先级允许列表添加到项目 `.claude/settings.json` 以减少权限提示 |
| `/focus` | 切换焦点视图，仅显示你的最后一个提示、一行工具调用摘要和最终响应。工具调用摘要也计算在轮中启动的子代理数量，并将完成的后台任务通知折叠为单个计数。选择在会话中持久化；在设置中设置 [`viewMode`](/docs/zh-CN/settings-reference#viewmode) 以覆盖它。仅在[全屏渲染](/docs/zh-CN/fullscreen)中可用。从 [Remote Control](/docs/zh-CN/remote-control) 客户端，运行 `/focus [on\|off]` 以仅为当前会话打开或关闭焦点视图，而不更改你的保存选择；这需要 Claude Code v2.1.281 或更高版本。[VS Code 扩展](/docs/zh-CN/vs-code#use-the-prompt-box)提供其自己的焦点视图作为命令菜单切换，存储为扩展设置，独立于 `viewMode` |
| `/fork [prompt]` | [将当前对话复制](/docs/zh-CN/agent-view#copy-the-session-with-%2Ffork)到新的后台会话并继续在这里工作。传递一个提示词，副本立即开始处理它；没有它，它在代理视图中等待其第一个提示词。除非副本[就地编辑](/docs/zh-CN/agent-view#how-file-edits-are-isolated)，Claude Code 指示它在进行代码更改之前创建自己的 worktree；隔离指令需要 Claude Code v2.1.221 或更高版本。要将侧面任务交给一个子代理，其结果返回到这个对话，请使用 `/subtask`；要自己切换到副本，请使用 `/branch`。需要 Claude Code v2.1.212 或更高版本；在 v2.1.161 到 v2.1.211，以及每当[代理视图关闭](/docs/zh-CN/agent-view#turn-off-agent-view)时，`/fork` 启动一个[分叉子代理](/docs/zh-CN/sub-agents#fork-the-current-conversation) |
| `/goal [condition\|clear]` | 设置一个[目标](/docs/zh-CN/goal)：Claude 跨轮继续工作直到条件满足或目标[因另一个原因清除](/docs/zh-CN/goal#how-evaluation-works)。没有参数时，显示当前或最近实现的目标。`clear`、`stop`、`off`、`reset`、`none` 或 `cancel` 提前移除活跃目标 |
| `/heapdump` | 写入 JavaScript 堆快照和内存细目到 `~/Desktop`，或 Linux 上没有 Desktop 文件夹的主目录，用于诊断高内存使用。报告内存问题时仅附加 `-diagnostics.json` 文件；`.heapsnapshot` 包含你的完整对话和凭证，所以不要共享它。[从命令菜单隐藏](#how-the-command-menu-matches-what-you-type)；完整输入它。请参阅[如何处理输出](/docs/zh-CN/troubleshooting#high-cpu-or-memory-usage) |
| `/help` | 显示帮助和可用命令 |
| `/hooks` | 查看工具事件的 [hook](/docs/zh-CN/hooks) 配置 |
| `/ide` | 管理 IDE 集成并显示状态 |
| `/import [codex\|gemini\|cursor] [--dry-run] [--yes]` | 将配置从你的机器上的 OpenAI Codex、Google Gemini CLI 或 Cursor 引入 Claude Code，包括指令文件、MCP 服务器、命令、子代理和 skill。在[非交互模式](/docs/zh-CN/headless)中使用 `-p`，`/import` 列出它找到的内容并给你确认导入的命令。添加 `--dry-run` 以预览而不写入任何内容，或 `--yes` 以跳过交互式选择器。在 Amazon Bedrock、Google Cloud 的 Agent Platform、Microsoft Foundry 或 Claude Platform on AWS 上不可用，或通过 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway#availability-and-limitations)。当你关闭[功能标志获取](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching)时也不可用。需要 Claude Code v2.1.213 或更高版本。从 Cursor 导入需要 v2.1.265 或更高版本 |
| `/init` | 使用 `CLAUDE.md` 指南初始化项目。设置 `CLAUDE_CODE_NEW_INIT=1` 以获得交互式流程，也会引导你完成 skill、hook 和个人内存文件。如果 `/init` 找到 OpenAI Codex 或 Google Gemini CLI 配置，它提供使用 `/import` 进行转移 |
| `/insights` | 生成一个 HTML 报告，分析你在这台机器上的最近会话：你在哪些项目中工作、你如何使用 Claude Code、事情出错的地方以及要尝试的功能。在[cloud sessions](/docs/zh-CN/claude-code-on-the-web)中不可用。有关报告位置、保留和成本，请参阅[分析你的使用模式](/docs/zh-CN/costs#analyze-your-usage-patterns) |
| `/install-github-app` | 为存储库安装 Claude GitHub App，可选步骤设置 [GitHub Actions](/docs/zh-CN/github-actions) 工作流和秘密。引导你完成选择 repo 和配置集成。仅适用于 github.com 存储库。当你的存储库的 git 远程在 gitlab.com 或 bitbucket.org 上时，命令打印通知并退出而不是启动设置。要从 GitLab 管道运行 Claude Code，请参阅 [GitLab CI/CD](/docs/zh-CN/gitlab-ci-cd) |
| `/install-slack-app` | 安装 Claude Slack 应用。打开浏览器以完成 OAuth 流程 |
| `/keybindings` | 打开你的[快捷键](/docs/zh-CN/keybindings)文件 |
| `/list-agents` | 列出子代理、[代理团队](/docs/zh-CN/agent-teams)队友和其他 Claude Code 会话 Claude 可以消息，以及每个要使用的名称。请参阅[跨会话消息](/docs/zh-CN/cross-session-messaging)。也可用作 `/peers`。需要 Claude Code v2.1.224 或更高版本；早期版本报告 `Unknown command: /list-agents`。队友行和显示此会话自己名称的第一行需要 v2.1.239 或更高版本。仅在[启用跨会话消息](/docs/zh-CN/cross-session-messaging#availability)的会话中可用 |
| `/login` | 登录到你的 Anthropic 账户 |
| `/logout` | 从你的 Anthropic 账户登出 |
| `/loop [interval] [prompt]` | **[Skill](/docs/zh-CN/skills#bundled-skills)。** 在会话保持打开时重复运行提示词。省略间隔，Claude [自我调整迭代之间的步伐](/docs/zh-CN/scheduled-tasks#let-claude-choose-the-interval)。省略提示词，Claude 运行[内置维护提示词](/docs/zh-CN/scheduled-tasks#run-the-built-in-maintenance-prompt)或你的 [`loop.md`](/docs/zh-CN/scheduled-tasks#customize-the-default-prompt-with-loop-md)。示例：`/loop 5m check if the deploy finished`。请参阅[按计划运行提示词](/docs/zh-CN/scheduled-tasks)。别名：`/proactive` |
| `/mcp [reconnect <server>\|enable\|disable [<server>\|all]]` | 管理 MCP 服务器连接和 OAuth 身份验证。运行不带参数以打开交互式列表，传递 `reconnect <server>` 以重新连接一个断开连接的服务器，或传递 `enable`/`disable` 带有服务器名称或 `all` 以更改连接状态而不打开对话框。也可在非交互模式 (`-p`) 中使用，其中运行不带参数会打印服务器状态的文本摘要而不是打开列表；需要 Claude Code v2.1.205 或更高版本 |
| `/memory` | 编辑 `CLAUDE.md` 文件，启用或禁用[自动内存](/docs/zh-CN/memory#auto-memory)，并查看自动内存条目 |
| `/mobile` | 显示 QR 代码以下载 Claude 移动应用。别名：`/ios`、`/android` |
| `/model [model]` | 切换 AI 模型并将其保存为新会话的默认值。对于支持它的模型，使用左/右箭头来[调整工作量级别](/docs/zh-CN/model-config#adjust-effort-level)。没有参数时，打开选择器；在行上按 `s` 仅为当前会话切换。请参阅[当 Claude Code 要求你确认切换时](/docs/zh-CN/prompt-caching#switching-models)。一旦你确认切换，如果 Claude Code 要求，Claude Code 会应用更改而不等待当前响应完成。在 v2.1.242 之前，Claude Code 从它从 Anthropic 获取的功能标志决定是在轮中期运行命令还是将其排队直到轮次完成，并始终在不[获取功能标志](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching)的会话中排队它，例如在[第三方提供商](/docs/zh-CN/third-party-integrations)上。也可在非交互模式 (`-p`) 中使用模型参数而不是选择器，其中它仅应用于当前会话并不保存为你的默认值；需要 Claude Code v2.1.205 或更高版本 |
| `/output-style [style]` | 列出[输出样式](/docs/zh-CN/output-styles)或切换到一个，例如 `/output-style concise`。请参阅[更改你的输出样式](/docs/zh-CN/output-styles#change-your-output-style)。需要 Claude Code v2.1.269 或更高版本 |
| `/passes` | 与朋友分享 Claude Code 的免费一周。仅在你的账户符合条件时可见 |
| `/permissions` | 管理工具权限的允许、询问和拒绝规则。打开一个交互式对话框，你可以按范围查看规则、添加或移除规则、管理工作目录，以及审查[最近的自动模式拒绝](/docs/zh-CN/auto-mode-config#review-denials)。你也可以从对话框的**自动模式**选项卡查看和编辑[自动模式分类器规则](/docs/zh-CN/auto-mode-config#edit-rules-from-permissions)。当你在 Claude 响应时运行它时，Claude Code 立即打开对话框并从 Claude 在同一轮中的下一个工具调用开始应用你的更改。在 v2.1.234 之前，Claude Code 会将命令排队直到轮次完成。别名：`/allowed-tools` |
| `/plan [description]` | 直接从提示词进入计划模式。传递可选描述以进入计划模式并立即开始该任务，例如 `/plan fix the auth bug` |
| `/plugin [subcommand]` | 管理 Claude Code [plugins](/docs/zh-CN/plugins/overview)。运行不带参数以打开插件菜单，或传递子命令如 `list`、`install`、`enable` 或 `disable` 以直接操作。Claude Code 可以在安装期间激活插件；[安装摘要](/docs/zh-CN/plugins/install#install-a-plugin)告诉你它是否做了或是否运行 `/reload-plugins` |
| `/powerup` | 通过带有动画演示的快速交互式课程发现 Claude Code 功能 |
| `/pr-comments [PR]` | 在 v2.1.91 中移除。直接要求 Claude 查看拉取请求评论。在早期版本上，从 GitHub 拉取请求获取和显示评论；自动检测当前分支的 PR，或传递 PR URL 或号码。需要 `gh` CLI |
| `/privacy-settings` | 查看和更新你的隐私设置。仅对 Pro 和 Max 计划订阅者可用 |
| `/radio` | 在浏览器中打开 Claude FM lo-fi 电台。当没有浏览器可用时打印流 URL |
| `/rate-limit-options` | 显示在 claude.ai 使用限制阻止请求时继续工作的方法：等待并[在限制重置时自动继续](/docs/zh-CN/interactive-mode#wait-for-a-usage-limit-to-reset)、添加[使用额度](/docs/zh-CN/costs#add-usage-credits-to-your-subscription)或升级你的计划。Claude Code 也可以在你在自己的终端上达到限制时自己打开此菜单。请参阅[关闭自动继续](/docs/zh-CN/interactive-mode#turn-automatic-continue-off)。需要 claude.ai 订阅。等待和继续行需要 Claude Code v2.1.234 或更高版本 |
| `/recap` | 按需生成当前会话的一行摘要。请参阅[会话摘要](/docs/zh-CN/interactive-mode#session-recap)以获得你离开后出现的自动摘要 |
| `/release-notes` | 在交互式版本选择器中查看更改日志。选择特定版本以查看其发布说明，或选择显示所有版本。说明出现在你的记录中而不进入 Claude 看到的对话 |
| `/reload-plugins [--force]` | 重新加载所有活跃[插件](/docs/zh-CN/plugins/overview)以应用待处理更改而不重新启动。报告每个重新加载组件的计数并标记任何加载错误。当重新加载会改变加载哪些 MCP 工具并使提示词缓存失效时，命令警告并跳过，除非你传递 `--force`。也可在非交互模式 (`-p`)、Agent SDK 和桌面应用中使用，其中它仅在直接输入到会话的输入上运行，不应用插件 MCP 服务器更改；需要 Claude Code v2.1.260 或更高版本。请参阅[应用插件更改而不重新启动](/docs/zh-CN/plugins/cli-reference#reload-plugins) |
| `/reload-skills` | 重新扫描 [skill](/docs/zh-CN/skills) 和命令目录，以便在会话期间添加或更改的 skill 在磁盘上变得可用而不重新启动。报告有多少 skill 可用以及添加或移除了多少 |
| `/remote-control` | 使此会话可从 claude.ai 进行 [Remote Control](/docs/zh-CN/remote-control)。在未登录时运行它会打印 Remote Control 需要 claude.ai 订阅并告诉你如何登录；在 v2.1.206 之前它报告 `Unknown command: /remote-control`。别名：`/rc` |
| `/remote-env` | 为你从 CLI 启动的 cloud sessions 选择默认[云环境](/docs/zh-CN/cloud-environments#select-an-environment-from-the-cli) |
| `/rename [name]` | 重命名当前会话并在提示栏上显示名称。没有名称，从对话历史自动生成一个。也可在非交互模式 (`-p`) 中使用；需要 Claude Code v2.1.205 或更高版本。从每个重命名表面，包括 claude.ai 和桌面应用，Claude Code 用空格替换新名称中的控制和不可见字符，并将名称限制在 200 个字符。如果名称在移除不可见字符后为空，Claude Code 拒绝它并显示 `That name is empty once invisible characters are removed. Usage: /rename <name>`。字符替换和长度限制需要 Claude Code v2.1.221 或更高版本。如果这台机器上的另一个活跃会话已经使用你传递的名称，Claude Code 应用[它的变体](/docs/zh-CN/sessions#name-your-sessions) |
| `/resume [session]` | 按 ID 或名称恢复对话，或打开会话选择器。[后台会话](/docs/zh-CN/agent-view)在选择器中标记为 `bg` 出现。恢复仍在运行的会话，从选择器或按 ID 或名称，[打开该会话](/docs/zh-CN/sessions#resume-a-running-background-session)：你的当前对话移到后台，此终端附加到运行的会话。在空提示符上按 `←` 返回代理视图，它也列出你离开的对话。在 v2.1.285 之前，Claude Code 拒绝并告诉你使用 `claude attach` 打开会话或先停止它。别名：`/continue` |
| `/review [low\|medium\|high\|xhigh\|max\|ultra] [--fix] [--comment] [pr#\|branch\|path]` | [`/code-review`](/docs/zh-CN/code-review#review-a-diff-locally) 的别名：审查当前差异，或你传递的 PR 号、分支或路径，例如 `/review 1234`，并采用相同的工作量级别和标志。没有给定级别时，审查重用你输入的最后一个 `low` 到 `max` 级别；有关确切规则，请参阅[本地审查差异](/docs/zh-CN/code-review#review-a-diff-locally)。对于深度云审查，使用 [`/code-review ultra`](/docs/zh-CN/ultrareview)。在 v2.1.223 之前，`/review` 是一个单独的命令，运行 GitHub 拉取请求号的单遍、只读审查，在运行不带参数时列出打开的 PR 以选择；从 v2.1.186 到 v2.1.201，它运行与 `/code-review medium` 相同的多代理引擎 |
| `/rewind` | 倒带对话和/或代码到上一个点，或从选定的消息总结。请参阅[检查点](/docs/zh-CN/checkpointing)。别名：`/checkpoint`、`/undo` |
| `/run` | **[Skill](/docs/zh-CN/skills#bundled-skills)。** 启动并驱动你的项目应用以查看更改工作，而不仅仅是通过测试。请参阅[运行和验证你的应用](/docs/zh-CN/skills#run-and-verify-your-app) |
| `/run-skill-generator` | **[Skill](/docs/zh-CN/skills#bundled-skills)。** 通过从干净环境编写每个项目的 [skill](/docs/zh-CN/skills#run-and-verify-your-app) 来教 `/run` 和 `/verify` 如何构建、启动和驱动你的项目应用 |
| `/sandbox` | 切换[沙箱模式](/docs/zh-CN/sandboxing)。仅在支持的平台上可用 |
| `/schedule [description]` | 创建、更新、列出或运行在云中执行的[例程](/docs/zh-CN/routines)。Claude 以对话方式引导你完成设置。你也可以询问[例程的最近运行](/docs/zh-CN/routines#manage-routines-from-the-cli)。别名：`/routines` |
| `/scroll-speed` | 交互式调整鼠标滚轮[滚动速度](/docs/zh-CN/fullscreen#mouse-wheel-scrolling)，带有一个标尺，你可以在对话框打开时滚动以预览更改。仅在[全屏渲染](/docs/zh-CN/fullscreen)中可用，在 JetBrains IDE 终端中不可用 |
| `/security-review` | 分析当前分支上的更改以查找安全漏洞。审查你的分支和 origin 默认分支之间的差异，识别注入、身份验证问题和数据暴露等风险。需要 `origin` 远程；如果审查失败并出现 `ambiguous argument` 错误，请参阅[错误参考](/docs/zh-CN/errors#security-review-fails-without-origin-head) |
| `/setup-bedrock` | 通过交互式向导配置 [Amazon Bedrock](/docs/zh-CN/amazon-bedrock) 身份验证、区域和模型引脚。[从命令菜单隐藏](#how-the-command-menu-matches-what-you-type)直到设置 `CLAUDE_CODE_USE_BEDROCK=1`；完整输入它。首次 Amazon Bedrock 用户也可以从登录屏幕访问此向导 |
| `/setup-vertex` | 通过交互式向导配置 [Google Cloud 的 Agent Platform](/docs/zh-CN/google-vertex-ai) 身份验证、项目、区域和模型引脚。[从命令菜单隐藏](#how-the-command-menu-matches-what-you-type)直到设置 `CLAUDE_CODE_USE_VERTEX=1`；完整输入它。首次 Google Cloud 的 Agent Platform 用户也可以从登录屏幕访问此向导 |
| `/simplify [target]` | **[Skill](/docs/zh-CN/skills#bundled-skills)。** 审查更改的代码以查找清理机会并应用修复。四个审查[代理](/docs/zh-CN/sub-agents)并行运行，涵盖现有帮助程序的重用、简化、效率以及更改是否处于正确的抽象级别。审查不查找正确性错误。使用 `/code-review` 查找错误。传递路径或 PR 参考以审查特定目标 |
| `/skill-doctor` | 显示你的每个 [skill](/docs/zh-CN/skills) 在上下文中的成本以及它被使用的频率，以便你可以[找到要关闭的 skill](/docs/zh-CN/skills#find-unused-skills)。需要 Claude Code v2.1.252 或更高版本和[功能标志获取](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching) |
| `/skills` | 列出可用的 [skill](/docs/zh-CN/skills)。输入以按名称、描述或来源过滤列表。按 `t` 按令牌计数排序，`Space` 或 `Enter` 以[循环 skill 对 Claude 和 `/` 菜单的可见性](/docs/zh-CN/skills#override-skill-visibility-from-settings)，`Esc` 保存并关闭。你无法循环插件 skill、frontmatter 设置 `disable-model-invocation: true` 的 skill 或在托管设置或 `--settings` 标志中有 `skillOverrides` 条目的 skill |
| `/slides [brief]` | **[Skill](/docs/zh-CN/skills#bundled-skills)。** 制作一个新的演示文稿作为 Claude Slides [工件](/docs/zh-CN/artifacts#make-a-slide-deck)，从你的简介中填充，例如 `/slides a quarterly review of the platform team`。需要 Claude Code v2.1.265 或更高版本、一个[工件可用](/docs/zh-CN/artifacts#availability)的会话，以及一个[Slides 模板可用](/docs/zh-CN/artifacts#start-from-a-slides-design-or-docs-template)的账户；否则命令不会出现。在 Anthropic API 上可用。在 Amazon Bedrock、Google Cloud 的 Agent Platform、Microsoft Foundry 和 Claude Platform on AWS 上，工件不可用，所以命令在那里不可用 |
| `/stats` | `/usage` 的别名。在 Stats 选项卡上打开 |
| `/status` | 在 Status 选项卡上打开设置界面，显示版本、模型、账户和连接性。一个 `Session kind` 行在[后台会话](/docs/zh-CN/agent-view)中读取 `background job · attached` 或 `background job · unattended`，取决于是否附加了终端，在任何其他会话中读取 `interactive`。在 v2.1.221 之前，`/status` 没有显示此行。在 Claude 响应时工作 |
| `/statusline` | 配置 Claude Code 的[状态行](/docs/zh-CN/statusline)。描述你想要的内容，或运行不带参数以从你的 shell 提示符自动配置 |
| `/stickers` | 订购 Claude Code 贴纸 |
| `/stop` | 停止当前[后台会话](/docs/zh-CN/agent-view)。仅在附加到后台会话时可用；记录和任何 worktree 都被保留。要分离而不停止，请使用 `/exit` 或按 `←` |
| `/subtask <task>` | 生成一个[分叉子代理](/docs/zh-CN/sub-agents#fork-the-current-conversation)：一个继承完整对话的后台子代理，在你继续工作时处理任务。其结果在完成时返回到这个对话。要将对话复制到单独的后台会话，请改用 `/fork`。需要 Claude Code v2.1.212 或更高版本；在 v2.1.161 到 v2.1.211，这个命令是 `/fork`。当[代理视图关闭](/docs/zh-CN/agent-view#turn-off-agent-view)时，`/subtask` 不可用，`/fork` 保持分叉子代理行为 |
| `/tasks` | 查看和管理当前会话中的后台工作，包括已完成的子代理。也可用作 `/bashes` |
| `/team-onboarding` | 从你的 Claude Code 使用历史生成团队入职指南。Claude 分析你过去 30 天的会话、命令和 MCP 服务器使用情况，并生成一个 markdown 指南，队友可以粘贴为第一条消息以快速设置。对于 Pro、Max、Team 和 Enterprise 计划上的 claude.ai 订阅者，也返回一个共享链接，队友可以直接在 Claude Code 中打开 |
| `/teleport` | 将 [cloud session](/docs/zh-CN/claude-code-on-the-web#from-cloud-to-terminal) 拉入此终端。打开选择器，然后获取分支和对话。也可用作 `/tp`。需要 claude.ai 订阅 |
| `/terminal-setup` | [在 VS Code、Cursor、Devin Desktop、Alacritty 或 Zed 中安装 Shift+Enter 快捷键以输入多行](/docs/zh-CN/terminal-config#enter-multiline-prompts)。在 Apple Terminal 中，[改为启用 Option+Enter 以输入多行并关闭可听铃声](/docs/zh-CN/terminal-config#enable-option-key-shortcuts-on-macos)。在 iTerm2 中，[打开剪贴板访问以便 `/copy` 工作](/docs/zh-CN/terminal-config#enable-option-key-shortcuts-on-macos) |
| `/theme` | 更改颜色主题。包括与你的终端的浅色或深色背景匹配的 `auto` 选项、浅色和深色变体、色盲无障碍（daltonized）主题、使用你的终端颜色调色板的 ANSI 主题，以及来自 `~/.claude/themes/` 或插件的任何[自定义主题](/docs/zh-CN/terminal-config#create-a-custom-theme)。选择\*\*新建自定义主题…\*\*以创建一个 |
| `/tui [default\|fullscreen]` | 设置终端 UI 渲染器并使用你的对话完整地重新启动到它。`fullscreen` 启用[无闪烁 alt-screen 渲染器](/docs/zh-CN/fullscreen)。没有参数时，打印活跃渲染器 |
| `/ultraplan <prompt>` | 已移除。改用[计划模式](/docs/zh-CN/permission-modes#analyze-before-you-edit-with-plan-mode)。以前将规划任务发送到 [cloud session](/docs/zh-CN/claude-code-on-the-web) 以在你的浏览器中审查 |
| `/ultrareview [PR or branch]` | 在云沙箱中运行深度、多代理代码审查，使用 [ultrareview](/docs/zh-CN/ultrareview)。传递 PR 参考以审查该拉取请求，或分支名称以更改比较基础。首选调用现在是 `/code-review ultra`，`/ultrareview` 保留为别名。在 Pro 和 Max 上包括 3 次免费运行，然后需要[使用额度](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) |
| `/update-config [request]` | **[Skill](/docs/zh-CN/skills#bundled-skills)。** 描述一个设置更改，例如允许一个命令、设置一个环境变量或添加一个 [hook](/docs/zh-CN/hooks)，Claude 编辑匹配的 [`settings.json`](/docs/zh-CN/settings) 文件。对于主题和模型等选项，改用 `/config` |
| `/upgrade` | 在浏览器中打开升级页面以切换到更高的计划层级。当浏览器无法打开时，命令显示登录提示而不打印 URL |
| `/usage` | 显示会话成本、计划使用限制和活动统计。在 Pro、Max、Team 或 Enterprise 计划上，包括[计入你的计划限制的内容的细目](/docs/zh-CN/costs#plan-usage-breakdown)。`/cost` 和 `/stats` 是别名 |
| `/usage-credits` | 配置使用额度，或在达到限制时从你的管理员请求它们。在浏览器中打开你的[使用额度计费设置](/docs/zh-CN/costs#add-usage-credits-to-your-subscription)，除了没有计费访问权限的 Team 和 Enterprise 成员改为从 CLI 向其管理员发送使用额度请求，在对话框中确认请求通知其管理员后。当没有浏览器可以打开计费页面时，例如通过 SSH，命令改为打印 URL 以访问；这需要 Claude Code v2.1.205 或更高版本，早期版本在这种情况下没有显示任何内容。以前 `/extra-usage` |
| `/verify` | **[Skill](/docs/zh-CN/skills#bundled-skills)。** 通过构建你的项目应用、运行它并观察结果来确认代码更改做了它应该做的事，而不是依赖测试或类型检查。请参阅[运行和验证你的应用](/docs/zh-CN/skills#run-and-verify-your-app) |
| `/vim` | 在 v2.1.92 中移除。要在 Vim 和 Normal 编辑模式之间切换，请使用 `/config` → 编辑器模式 |
| `/voice [hold\|tap\|off]` | 切换[语音听写](/docs/zh-CN/voice-dictation)，或在特定模式下启用它。需要 Claude.ai 账户 |
| `/web-setup` | 使用你的本地 `gh` CLI 凭证将你的 GitHub 账户连接到 [cloud sessions](/docs/zh-CN/web-quickstart#connect-from-your-terminal) |
| `/workflow-authoring` | **[Skill](/docs/zh-CN/skills#bundled-skills)。** 加载编写[动态 workflow](/docs/zh-CN/workflows) 脚本的参考：脚本 API、恢复行为、质量模式和工作示例。Claude 通常在编写脚本之前自己加载它；在[手动编辑保存的脚本](/docs/zh-CN/workflows#edit-a-saved-script)之前自己运行它。在启用动态 workflow 时可用，需要 Claude Code v2.1.248 或更高版本 |
| `/workflows` | 打开 [workflow](/docs/zh-CN/workflows#watch-the-run) 进度视图以监视、暂停、恢复或保存运行和已完成的 workflow |

<h2 id="how-the-command-menu-matches-what-you-type">
  命令菜单如何匹配你输入的内容
</h2>

Claude Code 在你输入时过滤 `/` 菜单。下面的每个要点涵盖了你在过滤时可能注意到的一件事：

* **高亮显示**：Claude Code 仅当 `/` 后面的字母与命令的名称或别名匹配时才高亮显示顶部建议，匹配可以从名称的开头或名称内的某个单词开始，忽略 `:`、`_` 和 `-` 分隔符。输入 `/adddir` 会高亮显示 `/add-dir`，输入 `/new` 会通过其别名高亮显示 `/clear`。按 `Enter` 运行高亮显示的建议。这些高亮显示规则需要 Claude Code v2.1.236 或更高版本。
* **打字错误后**：Claude Code 不高亮显示任何内容。接近的匹配项保持列出，你可以用 `Tab` 或箭头键选择一个，但 `Enter` 会按原样提交你的文本并报告[未知命令](/docs/zh-CN/errors#unknown-command)。
* **你无法使用的命令**：Claude Code 将它们排除在菜单之外。当没有任何内容匹配时，Claude Code 显示 `No commands match "/name"`。大多数不可用的命令在你提交时会返回[未知命令](/docs/zh-CN/errors#unknown-command)；少数几个，例如[`/schedule` 在 Console API 密钥上](/docs/zh-CN/routines#schedule-returns-unknown-command)，会改为返回自己的可用性消息。当你的组织的策略禁用某些命令时，这些命令也会返回自己的消息。
* **隐藏命令**：Claude Code 故意将一些可用命令（例如 `/heapdump`）排除在菜单之外。部分名称永远不会将隐藏命令带入菜单：如果部分匹配不到任何可见内容，Claude Code 会显示相同的不匹配消息。Claude Code 仅在你输入完整名称后才列出该命令，提交完整名称会运行它。

<h2 id="mcp-prompts">
  MCP prompts
</h2>

MCP 服务器可以公开显示为命令的提示。有关详细信息，请参阅 [MCP prompts](/docs/zh-CN/mcp#use-mcp-prompts-as-commands)。

<h2 id="see-also">
  另请参阅
</h2>

* [Skills](/docs/zh-CN/skills)：创建您自己的命令
* [Interactive mode](/docs/zh-CN/interactive-mode)：快捷键、Vim 模式和命令历史记录
* [CLI reference](/docs/zh-CN/cli-reference)：启动时标志
