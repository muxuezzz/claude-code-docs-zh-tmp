> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 管理会话

> 命名、恢复、分支和在 Claude Code 对话之间切换。涵盖 `--continue`、`--resume`、`--from-pr`、`/resume` 选择器、会话命名、导出文本记录和文本记录存储位置。

会话是与项目目录关联的已保存对话。Claude Code 在您工作时将其本地存储，因此您可以从中断处恢复、分支以尝试不同的方法，或在任务之间切换。

[桌面应用](/docs/zh-CN/desktop#work-in-parallel-with-sessions)、[claude.ai/code](/docs/zh-CN/claude-code-on-the-web) 和 [VS Code 扩展](/docs/zh-CN/vs-code#resume-past-conversations)各自维护自己的会话列表，桌面应用还可以[恢复 CLI 会话](/docs/zh-CN/desktop#coming-from-the-cli)。本页涵盖 CLI。

<h2 id="resume-a-session">
  恢复会话
</h2>

会话在您工作时持续保存到[本地文本记录文件](#export-and-locate-session-data)，因此您可以在退出或运行 `/clear` 后返回到一个会话。使用这些入口点：

| 命令 | 功能 |
| :- | :- |
| `claude --continue` | 恢复当前目录中最近的会话 |
| `claude --resume` | 打开[会话选择器](#use-the-session-picker) |
| `claude --resume <name>` | 直接恢复命名的会话 |
| `claude --resume <transcript-path>` | 恢复存储在该绝对路径的 `.jsonl` [文本记录文件](#where-transcripts-are-stored)中的对话 |
| `claude --from-pr <number>` | 打开会话选择器，筛选链接到该拉取请求的会话 |
| `/resume` | 从活跃会话内切换到不同的对话 |

Claude Code 将使用 [`claude -p`](/docs/zh-CN/headless) 或 [Agent SDK](/docs/zh-CN/agent-sdk/overview) 创建的会话排除在会话选择器和 `claude --continue` 之外。您仍然可以通过将其会话 ID 传递给 `claude --resume <session-id>` 来恢复它。使用 `claude --continue` 时，Claude Code 也会跳过[第一个提示是 `/loop` 的会话](#where-the-session-picker-looks)。当您运行 [`claude -p --continue`](/docs/zh-CN/headless#continue-conversations) 时，Claude Code 包括 `-p`、SDK 和 `/loop` 会话。

`claude --continue` 打开已完成的[后台会话](/docs/zh-CN/agent-view)，但不打开仍在运行的会话；打开已完成的后台会话需要 Claude Code v2.1.257 或更高版本。如果您最近的对话是您[移到后台](/docs/zh-CN/agent-view#send-the-session-to-the-background)的会话，并且它仍在那里运行，Claude Code 会以 `Your most recent conversation is running in the background` 和该会话的 ID 退出。从 [`claude agents`](/docs/zh-CN/agent-view#attach-to-a-session) 附加到会话，或运行 `claude --resume` 选择另一个。

<span id="resume-a-running-background-session" />

当您使用 `claude --resume` 或 `/resume` 恢复的对话属于仍在运行的[后台会话](/docs/zh-CN/agent-view)时，Claude Code 会打开运行中的会话本身。在命令行上使用 `--bg` 时，恢复是[后台调度](/docs/zh-CN/agent-view#from-your-shell)。在 v2.1.285 之前，Claude Code 拒绝并告诉您使用 `claude attach <id>` 打开会话，或首先使用 `claude stop <id>` 停止它。

* **从您的 shell**：`claude --resume <session>` 在同一终端中对该会话运行 [`claude attach`](/docs/zh-CN/agent-view#attach-to-a-session)，而不是加载文本记录本身。您在命令行上传递的提示，如 `claude --resume <session> "check the tests too"`，首先作为其下一轮转到会话，Claude Code 在附加之前打印 `Sent your prompt to the background session (<id>); opening it…`。`claude -p --resume <session> "prompt"` 在终端中输入时执行相同操作，因此 `-p` 不会保持该运行非交互式。

  当命令行具有以下任何内容时，Claude Code 不会打开会话：

  * 管道或重定向的输入或输出
  * 配置会话的标志，例如 `--permission-mode`、`--model` 或 `--settings`
  * 读取输出的标志，例如 `--output-format json` 或 `--json-schema`
  * 限制或倒带运行的标志，例如 `--max-turns` 或 `--max-budget-usd`

  使用这些中的任何一个，或当[代理视图被关闭](/docs/zh-CN/agent-view#turn-off-agent-view)时，Claude Code 不发送任何内容并以状态 1 退出，打印会话在后台运行以及打开它的 `claude attach <id>` 命令，或当它无法确定 ID 时告诉您在 `claude agents` 中找到它。添加 `--fork-session` 以恢复对话的副本。要在您自己的会话中继续对话本身，应用您的标志，运行 `claude stop <id>`，然后重复该命令。

  以 `/` 或 `!` 开头的提示不会被发送，会话等待您回答问题时的任何提示也不会。在这两种情况下，Claude Code 都不会打开会话，消息包括 `Your prompt was not sent to it` 和原因。
* **从会话内**：`/resume` 将您当前的对话移到后台，并将此终端附加到运行中的会话，打印 `Opening "<title>", running in the background (<id>)`。在空提示上按 `←` 返回代理视图，这也列出您离开的对话。当当前对话无法移到后台时，例如因为您已附加到后台会话或会话持久性已关闭，`/resume` 会打印 `claude attach` 命令以改为运行。

您可以从任何目录运行 `claude --resume <session-id>`：Claude Code 首先在当前项目目录及其 git worktrees 中查找 ID，然后在此计算机上的所有其他项目中查找，因此它会找到在其他地方启动或使用 [`/cd`](/docs/zh-CN/commands) 移动的会话。跨项目搜索仅在恰好一个其他项目持有具有该 ID 的消息的文本记录时解析 ID，因此手动复制的重复项会导致 Claude Code 报告未找到，而不是恢复任意副本。如果没有存储的会话与 ID 匹配，Claude Code 会报告 `No conversation found with session ID: <session-id>`。在 v2.1.223 之前，查找在当前项目目录及其 git worktrees 处停止，因此您必须从会话最后工作的目录恢复。

<h3 id="what-a-resumed-session-restores">
  恢复的会话恢复的内容
</h3>

当 Claude Code 从其文本记录加载对话时，恢复的会话会恢复对话以及保存在其中的状态：

* 对话历史：完整历史，包括工具调用和结果。如果工具在上一个进程结束时仍在运行（例如在崩溃中），当您恢复时它不会完成或再次运行。Claude 会看到该调用被标记为在记录其结果之前被切断，并被告知在再次运行之前检查它是否生效，除非设置了 [`CLAUDE_CODE_RESUME_INTERRUPTED_TURN`](/docs/zh-CN/env-vars#variables)。在 v2.1.281 之前，Claude Code 会从对话中删除切断的调用或将其显示为您中断的调用。
* 模型：会话继续使用它正在使用的模型。当模型已被停用或不被 `availableModels` 允许时，模型不会被恢复；当在启动时通过 `--model` 标志或 `ANTHROPIC_MODEL` 系列环境变量选择模型时；或在使用特定于提供商的部署 ID 的提供商上，例如 [Amazon Bedrock、Google Cloud 的 Agent Platform 和 Microsoft Foundry](/docs/zh-CN/third-party-integrations)；请参阅[模型配置](/docs/zh-CN/model-config#setting-your-model)了解解析顺序。
* Agent：使用 [`--agent`](/docs/zh-CN/sub-agents#invoke-subagents-explicitly) 或 `agent` 设置启动的会话继续作为该 agent，保持其工具限制和模型。在恢复时传递 `--agent` 以选择不同的；对于任一情况下的系统提示，请参阅[恢复对话中的系统提示标志](/docs/zh-CN/cli-reference#system-prompt-flags-in-resumed-conversations)。Claude Code 在两个地方查找 agent：会话的原始目录（前提是您已[信任该工作区](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust)）和您恢复的目录，因此项目范围的 agent 在您从另一个目录恢复时仍会加载。如果 Claude Code 在任一位置都找不到 agent，会话会以默认工具恢复并显示[警告，命名该 agent](/docs/zh-CN/errors#session-agent-no-longer-available)。
* 权限模式：如果您从终端使用 `claude --continue`、`claude --resume <session-id>` 或 `claude --resume <name>`（当名称与一个会话匹配时）恢复，不带 `-p`，Claude Code 会恢复会话所在的权限模式，除了[恢复时的权限模式](#permission-mode-on-resume)中的情况，这也涵盖会话选择器、`/resume` 和使用 `claude -p` 恢复。传递 `--permission-mode` 或 `--dangerously-skip-permissions` 以覆盖恢复的模式。
* 活跃目标：会话结束时仍然活跃的[目标](/docs/zh-CN/goal#resume-with-an-active-goal)会继续；其轮次计数、计时器和令牌支出基线重置。
* 计划任务：[未过期的任务](/docs/zh-CN/scheduled-tasks#limitations)会被恢复。后台 Bash 和监视任务不会。
* 后台工作：[后台子 agent](/docs/zh-CN/sub-agents#run-subagents-in-foreground-or-background)、后台 Bash 命令或[工作流](/docs/zh-CN/workflows)在上一个进程结束时未完成，会在恢复的文本记录中显示为未完成的注记。Claude Code 不会从这些注记启动轮次；Claude 会在您的下一个提示中读取它们。

并非原始启动的每个配置标志都会被恢复。如果会话依赖于 `--mcp-config`、`--settings`、`--plugin-dir`、`--fallback-model` 或使用 `--add-dir` 添加的目录，在恢复时再次传递它们；使用 `/add-dir` 在会话中期添加的目录也不会被恢复，尽管会话选择器仍然使用它们来定位会话。标准设置文件（如 `settings.json` 和 `settings.local.json`）在启动时重新读取，因此驻留在其中的配置不需要再次传递。对于 `--system-prompt` 和 `--append-system-prompt`，请参阅[恢复对话中的系统提示标志](/docs/zh-CN/cli-reference#system-prompt-flags-in-resumed-conversations)。

<h4 id="permission-mode-on-resume">
  恢复时的权限模式
</h4>

Claude Code 启动恢复会话的权限模式取决于您如何恢复。下面的情况适用于 Claude Code 从其文本记录加载对话时；当您[打开仍在运行的后台会话](#resume-a-running-background-session)时，该会话保持它所在的权限模式。

* 终端：`claude --continue`、`claude --resume <session-id>` 或 `claude --resume <name>`（当名称与一个会话匹配时），不带 `-p`。Claude Code 恢复会话所在的权限模式，除了表中的情况。传递 `--permission-mode` 或 `--dangerously-skip-permissions` 以覆盖恢复的模式。
* 非交互式：`claude -p --resume` 或 `claude -p --continue`。Claude Code 在新 `claude -p` 运行会启动的权限模式中启动运行，除了在[下面的条件](#resume-in-plan-mode-with-p)下以计划模式结束的会话在计划模式中恢复。
* VS Code：扩展的对话面板。该表仅涵盖以计划模式结束的对话；对于其余部分，请参阅[恢复过去的对话](/docs/zh-CN/vs-code#resume-past-conversations)。
* 启动时的会话选择器：您从[会话选择器](#use-the-session-picker)中选择的会话，无论您是使用 `claude --resume` 单独打开它、`claude --from-pr` 还是与多个会话匹配的名称。Claude Code 不恢复存储的权限模式。它在从同一命令行启动新会话的权限模式中启动会话。
* 会话内的 `/resume`，带或不带参数：Claude Code 不恢复存储的权限模式。您切换到的对话继续在您当前会话所在的权限模式中。

在非交互式和 VS Code 路径上恢复计划模式需要 Claude Code v2.1.246 或更高版本。每一行命名会话结束的权限模式、您通过哪个终端、非交互式和 VS Code 路径恢复它，以及 Claude Code 启动恢复会话的权限模式。

| 会话结束于 | 您如何恢复 | 恢复后的权限模式 |
| :- | :- | :- |
| `bypassPermissions` | 终端 | 新会话会启动的权限模式。要再次[绕过权限](/docs/zh-CN/permission-modes#skip-all-checks-with-bypasspermissions-mode)，在启动时使用其启动标志之一或[用户、`--settings` 或托管设置](/docs/zh-CN/settings-reference#permissions-defaultmode)中的 `permissions.defaultMode: "bypassPermissions"` 启用它 |
| `plan` | 终端 | 新会话会启动的权限模式 |
| `auto` | 终端 | `auto`，仅当您的帐户仍然满足[自动模式要求](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)时 |
| Manual | 终端 | 当新会话会从[内置默认值](/docs/zh-CN/permission-modes#which-mode-a-session-starts-in)以自动模式启动时，手动模式。当来自设置文件的 `defaultMode` [生效](/docs/zh-CN/permission-modes#which-mode-a-session-starts-in)时，Claude Code 在该模式中启动恢复的会话 |
| `plan` | 非交互式，在[下面的条件](#resume-in-plan-mode-with-p)下 | 计划模式 |
| 任何模式 | 非交互式，在任何其他情况下 | 新 `claude -p` 运行会启动的权限模式 |
| `plan` | VS Code | 计划模式，带有 [VS Code 页面上的例外](/docs/zh-CN/vs-code#resume-past-conversations) |

<h5 id="resume-in-plan-mode-with-p">
  使用 `-p` 在计划模式中恢复
</h5>

`claude -p --resume` 或 `claude -p --continue` 运行仅在所有这些条件都成立时才在计划模式中恢复：

* 您传递 [`--permission-prompt-tool`](/docs/zh-CN/cli-reference#cli-flags)，不传递 [`--permission-prompts none`](/docs/zh-CN/headless#turn-off-permission-prompts-in-unattended-runs)，以便 Claude Code 可以呈现计划以供批准
* 您不传递 `--permission-mode` 或 `--dangerously-skip-permissions`
* 您不传递 `--fork-session`
* 运行不是通过[频道](/docs/zh-CN/channels)启动的

<h3 id="resume-from-a-summary">
  从摘要恢复
</h3>

在 Pro 或 Max 计划上，当您恢复已不活跃超过约一小时且超过 100,000 个令牌的会话时，Claude Code 会恢复对话，然后在您发送第一条消息之前打开一个对话框。到那时，会话的[提示缓存](/docs/zh-CN/prompt-caching#cache-lifetime)已过期，因此无论您选择对话框的哪个选项，下一个请求都会处理完整历史一次。

对话框提供三种方式来继续会话。它们在每个会话向后续请求转发多少对话方面有所不同，这是在保留每个细节和每个请求发送更少令牌之间的权衡：

* **从摘要恢复**：立即运行 [`/compact`](/docs/zh-CN/context-window#what-survives-compaction)。Claude Code 通过完整历史发送一个摘要请求，然后用摘要、您最近的交换和最多五个最近读取的文件替换历史。后续请求会转发摘要而不是完整历史。
* **按原样恢复完整会话**：加载未更改的对话。在您发送第一条消息后，Claude Code 重新处理并重新缓存完整历史，然后在缓存保持温暖时从缓存中重新读取它以进行后续请求。
* **不再问我**：恢复完整会话并停止在所有未来恢复中显示对话框。

按原样恢复会保持对话的每个细节可用，每个请求的成本随对话的大小而扩展。从摘要恢复在每个后续请求上成本更低，因为它转发摘要而不是完整历史，但摘要遗漏的任何内容都不再在 Claude 的上下文中。请参阅[为什么长会话中的使用量会增加](/docs/zh-CN/costs#why-usage-climbs-in-a-long-session)了解该每个请求成本的来源。

<h3 id="where-the-session-picker-looks">
  会话选择器查看的位置
</h3>

Claude Code 按项目目录存储会话。默认情况下，会话选择器显示：

* 来自当前 worktree 的会话，包括[后台会话](/docs/zh-CN/agent-view)，在列表中标记为 `bg`
* 在其他地方启动但使用 `/add-dir` 添加了当前目录的会话

使用 `Ctrl+W` 扩展到存储库的所有 worktrees，或使用 `Ctrl+A` 扩展到此计算机上的每个项目。

第一个提示是 [`/loop`](/docs/zh-CN/scheduled-tasks#run-a-prompt-repeatedly-with-%2Floop) 命令的会话不会出现在选择器中，`claude --continue` 也会跳过它们。在对话中稍后运行 `/loop` 不会隐藏会话。在 v2.1.211 之前，对话早期的 `/loop` 运行会永久隐藏选择器中的会话。

使用 [`/cd`](/docs/zh-CN/commands) 移动会话会将其重新定位到新目录的项目存储，因此之后它会出现在该目录的选择器中。从 v2.1.196 开始，移动的会话在崩溃或强制退出后会保持不在旧目录的选择器中。在较早的版本中，当旧路径包含下划线等特殊字符时，在不干净的退出后，它也可能在旧目录的列表中重新出现。

从同一存储库的另一个 worktree 选择会话时，Claude Code 会在原地恢复它；当会话自己的 worktree 不再存在时，Claude Code [在您的当前目录中恢复它](/docs/zh-CN/worktrees#resume-a-worktree-session)。从不相关项目选择会话时，Claude Code 会将 `cd` 和恢复命令复制到您的剪贴板。如果该项目的目录不再存在，Claude Code 会在您的当前目录中恢复会话，而不是复制会失败的 `cd` 命令。

按名称恢复会跨当前存储库及其 worktrees 解析。两种形式都查找精确匹配并直接恢复它，即使它位于不同的 worktree 中：

| 命令 | 精确匹配 | 模糊名称 |
| :- | :- | :- |
| `claude --resume <name>` | 直接恢复 | 打开会话选择器，名称预填充为搜索词 |
| `/resume <name>` | 直接恢复 | 报告错误；运行不带参数的 `/resume` 打开会话选择器 |

<h2 id="name-your-sessions">
  命名您的会话
</h2>

为会话提供描述性名称，以便在会话选择器中可以找到它们，并可以按名称恢复。当您并行处理多个任务时，这一点最重要。

| 时间 | 如何设置名称 |
| :- | :- |
| 启动时 | `claude -n auth-refactor` |
| 在会话期间 | `/rename auth-refactor`。名称也会出现在提示栏上 |
| 从会话选择器 | 突出显示会话并按 `Ctrl+R` |
| 在计划接受时 | 在 [Plan Mode](/docs/zh-CN/permission-modes#analyze-before-you-edit-with-plan-mode) 中接受计划会从计划内容命名会话，除非您已经设置了一个 |
| 从 claude.ai 或 Claude 应用 | 重命名 [Remote Control 会话](/docs/zh-CN/remote-control#connect-from-another-device)；Claude Code 在 CLI 中应用相同的名称。需要 Claude Code v2.1.221 或更高版本 |
| 从桌面应用 | 在 [桌面应用](/docs/zh-CN/desktop#work-in-parallel-with-sessions) 中重命名会话 |

通过 CLI 路由或从 claude.ai 命名会话后，使用 `claude --resume <name>` 或 `/resume <name>` 返回到它；桌面应用会话在 [桌面应用](/docs/zh-CN/desktop#work-in-parallel-with-sessions) 中恢复。有关名称解析如何跨 worktrees 工作的信息，请参阅[恢复会话](#resume-a-session)。

当您使用此计算机上另一个活跃会话已经使用的名称启动或恢复交互式会话，或将会话重命名为这样的名称时，Claude Code 会将该名称保留给已经拥有它的会话，将您的会话重命名为带有两个单词后缀的变体，例如 `auth-refactor-graceful-unicorn`，并告知您。如果您想自己选择一个名称，请使用新名称运行 `/rename`。在 v2.1.232 之前，两个会话都保留该名称。

在三种情况下，Claude Code 不会重命名重复项，因此您仍然可以在列表中看到两个具有相同名称的会话：

* 它不检查 AI 生成的标题或默认显示名称。
* 它不检查启动时 [后台](/docs/zh-CN/agent-view#from-your-shell) 或 `-p` 会话的 `--name`。
* 它无法重命名早期版本 Claude Code 上的会话。

您未命名的会话仍会获得 Claude Code 分配的两个标签。只有生成的标题可用作恢复句柄：

* 默认显示名称：您从未命名的交互式会话在启动时仍会获得默认显示名称。需要 Claude Code v2.1.196 或更高版本。默认名称将工作目录的名称与两个字符的后缀组合在一起，例如 `my-app-3f`，并在运行会话的列表中标识会话，例如 [agent view](/docs/zh-CN/agent-view) 和 `claude agents --json` 输出。默认名称不是恢复句柄。如果您将其传递给 `claude --resume` 或 `/resume`，Claude Code 不会找到该会话。命名会话会替换这些列表中的默认名称，接受计划也会这样做。
* 生成的标题：如果您不命名会话，Claude Code 会为其生成会话标题。该标题是您第一个提示的简短摘要，由对小型/快速模型（通常是 Haiku 级别的模型）的后台请求编写。您直接从 shell 或脚本启动的 `claude -p` 运行不会获得一个。

  接受计划会将生成的标题替换为基于计划的标题。命名会话也会替换它。

  您可以在 [会话选择器](#use-the-session-picker) 中和未设置名称时的状态行 [`session_name`](/docs/zh-CN/statusline) 字段中看到第一个提示标题。计划标题显示在相同的两个位置，也显示在运行会话的列表中，其中它取代了默认显示名称。

  您可以将任一标题传递给 `claude --resume` 或 `/resume`，Claude Code 会以与您设置的名称相同的方式解析它。

<h2 id="use-the-session-picker">
  使用会话选择器
</h2>

在会话内运行 `/resume`，或不带参数运行 `claude --resume`，以打开交互式会话选择器。使用这些快捷键导航、搜索和扩展列表：

| 快捷键 | 操作 |
| :- | :- |
| `↑` / `↓` | 在会话之间导航 |
| `→` / `←` | 展开或折叠分组的会话 |
| `Enter` | 恢复突出显示的会话 |
| `Space` | 预览会话内容。在不将其捕获为粘贴的终端上也可以使用 `Ctrl+V` |
| `Ctrl+R` | 重命名突出显示的会话 |
| `/` 或除 `Space` 外的任何可打印字符 | 进入搜索模式并过滤会话。粘贴 GitHub、GitHub Enterprise、GitLab 或 Bitbucket 拉取或合并请求 URL 以查找创建它的会话 |
| `Ctrl+A` | 显示此计算机上所有项目的会话。再次按下以返回到当前存储库 |
| `Ctrl+W` | 显示当前存储库所有 worktrees 的会话。再次按下以返回到当前 worktree。仅在多 worktree 存储库中显示 |
| `Ctrl+B` | 过滤到当前 git 分支的会话。再次按下以显示所有分支 |
| `Esc` | 退出会话选择器或搜索模式 |

每行显示会话名称（如果已设置），否则显示 AI 生成的会话标题、对话摘要或第一个提示，以及自上次活动以来的时间、git 分支和文件大小。使用 `Ctrl+A` 扩展到所有项目后，还会显示每个会话的项目路径。

使用 `/branch` 或 `--fork-session` 创建的会话会获得自己的会话 ID 并显示为单独的行。当选择器为同一会话找到多个条目时，它会将它们分组在单个行下。按 `→` 展开一个组。

如果 Claude Code 无法从 `claude --resume` 选择器加载您选择的会话，它会打印 [`Failed to resume the conversation`](/docs/zh-CN/errors#failed-to-resume-the-conversation) 并显示重试命令，然后以代码 1 退出。从会话内的 `/resume` 选择器，Claude Code 会报告失败，您当前的对话会继续运行。

<h2 id="branch-a-session">
  分支会话
</h2>

分支创建迄今为止对话的副本并将您切换到其中，保持原始对话完整。使用它来尝试不同的方法而不会丢失您所在的路径。

从会话内，运行带有可选名称的 `/branch`：

```text theme={null}
/branch try-streaming-approach
```

如果您省略名称，Claude Code 会根据对话中的第一个提示为新分支命名。从 v2.1.198 开始，这也适用于 [compaction](/docs/zh-CN/how-claude-code-works#when-context-fills-up) 之后；较早的版本会回退到字面名称 `Branched conversation`，而不是查看 compaction 摘要之外的原始第一个提示。

从命令行，将 `--continue` 或 `--resume` 与 `--fork-session` 结合：

```bash theme={null}
claude --continue --fork-session
```

`/branch` 确认打印两个会话 ID：您现在所在的新分支和原始分支。原始分支在磁盘上保持不变，并在会话选择器中保持可用；使用 `/resume <original-name>` 返回到它，或将其 ID 传递给 `/resume`。

`/branch` 复制文本记录并将运行的 Claude Code 进程切换为写入到它。这种区别决定了分支继承的内容：

| 状态 | 在 `/branch` 之后 |
| :- | :- |
| 对话历史 | 复制到分支中，直到您运行 `/branch` 的点 |
| "允许此会话"权限授予 | 转移；分支在同一进程中运行，因此您现有的授予仍然适用。如果您使用 `--fork-session` 分叉到单独的进程中，新进程启动时没有它们，您在那里重新批准 |
| 进行中的 [background subagents](/docs/zh-CN/sub-agents#run-subagents-in-foreground-or-background) 和 [background Bash commands](/docs/zh-CN/interactive-mode#background-bash-commands) | 继续运行。它们的输出出现在您切换到的新分支中，而不是在原始会话中 |
| [Remote Control](/docs/zh-CN/remote-control) 连接 | 保持连接。连接到会话的手机或浏览器跟随您进入分支，并在那里继续接收新消息 |

如果您在两个终端中恢复同一会话而不分叉，来自两者的消息会交错到一个文本记录中。对于单个会话内基于 checkpoint 的回退，请参阅 [Checkpointing](/docs/zh-CN/checkpointing)。

<h2 id="manage-context-within-a-session">
  管理会话内的上下文
</h2>

这些命令控制上下文窗口中的内容而不离开会话：

* **`/clear`**：以空上下文重新开始。Claude Code 保存之前的对话；可通过 `/resume` 恢复它，或在同一个 Claude Code 进程中，从[倒带菜单的上一个会话条目](/docs/zh-CN/checkpointing#rewind-past-a-cleared-conversation)恢复。不带参数时，新对话保留您使用 `--name` 或 `/rename` 设置的名称，但不保留 AI 生成的会话标题。要为您要离开的对话命名，请传递名称，如 `/clear release-prep`；新对话随后将以未命名状态开始
* **`/compact [instructions]`**：用摘要替换历史记录，可选地专注于您指定的内容
* **`/context`**：显示当前消耗的上下文

有关压缩如何与 CLAUDE.md、skills 和规则交互的信息，请参阅[上下文窗口指南](/docs/zh-CN/context-window)。有关何时清除与压缩的策略，请参阅[最佳实践](/docs/zh-CN/best-practices#manage-your-session)。

<h2 id="export-and-locate-session-data">
  导出和定位会话数据
</h2>

运行 `/export` 打开一个菜单，让您将当前对话复制到剪贴板或将其保存为纯文本文件，消息和工具输出呈现为可读文本。传递文件名以跳过菜单并直接写入该文件。

<h3 id="access-conversations-from-scripts">
  从脚本访问对话
</h3>

`/export` 生成一个供人阅读的呈现文本记录。下面的接口生成结构化数据供脚本解析：运行的 JSON 结果、会话文本记录文件的路径或事件的实时流。根据触发脚本的内容选择：

* **运行 Claude 一次并捕获结果**：使用 [`--output-format json` 或 `stream-json`](/docs/zh-CN/headless#get-structured-output) 调用 `claude -p` 以捕获非交互式运行的结果、会话 ID、使用情况和成本作为结构化 JSON。
* **向现有会话提问**：将会话 ID 传递给 [`claude -p --resume`](/docs/zh-CN/headless#continue-conversations) 以发送后续提示（例如摘要请求），并捕获结构化响应。
* **对会话事件做出反应**：读取 [hooks](/docs/zh-CN/hooks#common-input-fields) 和 [status line commands](/docs/zh-CN/statusline#available-data) 作为输入接收的 `transcript_path` 字段。`SessionEnd` hook 可以在会话结束时存档文本记录。
* **在 TypeScript 或 Python 应用中嵌入 Claude**：使用 [Agent SDK](/docs/zh-CN/agent-sdk/overview) 以编程方式接收每条消息。

下面的示例使用第二个接口。它向现有会话发送后续提示，并使用 `jq` 读取答案：

```bash theme={null}
claude -p --resume <session-id> --output-format json "summarize what we changed" | jq -r '.result'
```

<h3 id="where-transcripts-are-stored">
  文本记录存储位置
</h3>

默认情况下，Claude Code 将文本记录存储为 JSONL，位置为 `~/.claude/projects/<project>/<session-id>.jsonl`，其中 `<project>` 是您的工作目录路径，非字母数字字符被替换为 `-`。对于转换后的名称超过 200 个字符的工作目录，Claude Code 将名称截断为 200 个字符，并附加完整路径的哈希值，以便目录名称保持在文件系统限制范围内。

每行是消息、工具使用或元数据条目的 JSON 对象。条目格式是 Claude Code 的内部格式，在版本之间会发生变化，因此直接解析这些文件的脚本可能在任何版本上中断。要基于会话数据构建，请改用 `/export` 或 [脚本接口](#access-conversations-from-scripts)。

位置、保留期和写入行为是可配置的：

| 目的 | 设置 | 位置 |
| - | - | - |
| 将存储移出 `~/.claude` | [`CLAUDE_CONFIG_DIR`](/docs/zh-CN/env-vars) | 环境变量 |
| [自己命名 `<project>` 目录](#name-the-project-directory-yourself) | [`CLAUDE_CODE_PROJECT_DIR_NAME`](/docs/zh-CN/env-vars) | 环境变量 |
| 更改 30 天保留期 | [`cleanupPeriodDays`](/docs/zh-CN/settings-reference#cleanupperioddays) | `settings.json` |
| 为 [Claude Desktop 和 Cowork 文本记录](/docs/zh-CN/claude-directory#cleaned-up-automatically) 设置年龄限制 | [`desktopSessionCleanupPeriodDays`](/docs/zh-CN/settings-reference#desktopsessioncleanupperioddays) | 用户设置、托管设置或 `--settings` |
| 在所有模式下禁止文本记录写入 | [`CLAUDE_CODE_SKIP_PROMPT_HISTORY`](/docs/zh-CN/env-vars) | 环境变量 |
| 禁止一次非交互式运行的写入 | [`--no-session-persistence`](/docs/zh-CN/cli-reference) | 与 `claude -p` 一起使用的 CLI 标志 |

<h3 id="delete-session-data">
  删除会话数据
</h3>

文本记录在 [保留扫描规则](/docs/zh-CN/claude-directory#cleaned-up-automatically) 下过期。要更快地删除项目的文本记录和相关状态，请运行 [`claude project purge`](/docs/zh-CN/claude-directory#clear-local-data)。如果您使用 [`claude rm <id>`](/docs/zh-CN/agent-view#what-deleting-a-session-removes) 删除 [后台会话](/docs/zh-CN/agent-view)，其文本记录保留在磁盘上，并且仍可通过 `claude --resume` 访问。

<h3 id="name-the-project-directory-yourself">
  自己命名项目目录
</h3>

默认情况下，Claude Code 从整个工作目录路径派生 `<project>` 名称。要自己选择名称，请将 `CLAUDE_CODE_PROJECT_DIR_NAME` 与 `CLAUDE_CONFIG_DIR` 一起设置。Claude Code 然后将该会话的文本记录和 [自动内存](/docs/zh-CN/memory#auto-memory) 存储在您的名称下。这适合嵌入 Claude Code 的主机，并为每个会话提供自己的配置目录。需要 Claude Code v2.1.234 或更高版本。

例如，此启动将租户 A 的数据保留在 `/srv/tenant-a` 下，并将其项目目录命名为 `work`：

```bash theme={null}
CLAUDE_CONFIG_DIR=/srv/tenant-a CLAUDE_CODE_PROJECT_DIR_NAME=work claude
```

Claude Code 将会话的文本记录写入 `/srv/tenant-a/projects/work/`，将其自动内存写入 `/srv/tenant-a/projects/work/memory/`，无论工作目录是什么。

设置时适用三条规则：

* **也设置 `CLAUDE_CONFIG_DIR`**：名称不随工作目录变化，因此在默认 `~/.claude` 下，它会将每个项目的文本记录和自动内存合并到一个目录中。当 `CLAUDE_CONFIG_DIR` 未设置时，Claude Code 忽略 `CLAUDE_CODE_PROJECT_DIR_NAME`。
* **使用 1-64 个字母、数字、连字符或下划线**：不要使用 Windows 设备名称，例如 `con`。Claude Code 忽略任何其他值，并使用派生的名称。
* **在启动 `claude` 的 shell 环境中设置它**：Claude Code 在启动时从该环境读取一次，因此设置文件中的 `env` 块无法设置它。

一旦您命名了配置目录的项目目录，请继续使用该名称启动。如果您使用相同的 `CLAUDE_CONFIG_DIR` 但没有 `CLAUDE_CODE_PROJECT_DIR_NAME` 启动 Claude Code，它会再次读取和写入派生目录。存储在您的名称下的会话保留在磁盘上：在 [会话选择器](#use-the-session-picker) 中按 `Ctrl+A` 以列出该配置目录下每个项目目录中的会话（包括固定的会话），无论您如何启动，[`claude --resume <session-id>`](#resume-a-session) 都会找到存储在任一名称下的会话。

<h2 id="see-also">
  另请参阅
</h2>

这些页面涵盖相关的会话和并行性机制：

* [Worktrees](/docs/zh-CN/worktrees)：在单独的分支上运行隔离的并行会话
* [Checkpointing](/docs/zh-CN/checkpointing)：将代码和对话回退到较早的点
* [Context window](/docs/zh-CN/context-window)：什么填充上下文以及什么在压缩中保留
* [Non-interactive mode](/docs/zh-CN/headless)：`claude -p` 下的会话行为
