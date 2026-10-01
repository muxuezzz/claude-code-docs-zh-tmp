> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 使用 agent view 管理多个代理

> 从一个屏幕调度和管理多个 Claude Code 会话。Agent view 显示每个会话正在做什么以及哪些会话需要你的输入。

Agent view 通过 `claude agents` 打开，是所有后台会话的一个屏幕：什么正在运行、什么需要你的输入、什么已完成。调度新会话，一目了然地查看它们的状态而不是滚动浏览记录，只在需要时才介入。每个后台会话都是一个完整的 Claude Code 对话，在没有终端连接的情况下继续运行，所以你可以随时打开它、回复并离开。

<img src="https://mintcdn.com/claude-code/HDAmBwgbrZVk0pOt/images/agent-view-light.png?fit=max&auto=format&n=HDAmBwgbrZVk0pOt&q=85&s=d6905012bee31f3e6b3920b09c05dd02" className="dark:hidden" alt="终端中的 Agent view。顶部的一行计算等待输入、正在工作和已完成的会话。四个会话分组在'需要输入'、'正在工作'和'已完成'下。每行显示会话的名称、其最新状态或问题以及时间。底部是用于描述新任务的输入和一行键盘提示。" width="1872" height="680" data-path="images/agent-view-light.png" />

<img src="https://mintcdn.com/claude-code/HDAmBwgbrZVk0pOt/images/agent-view-dark.png?fit=max&auto=format&n=HDAmBwgbrZVk0pOt&q=85&s=fc3c195bfc57e313ced1f1beb36cee93" className="hidden dark:block" alt="终端中的 Agent view。顶部的一行计算等待输入、正在工作和已完成的会话。四个会话分组在'需要输入'、'正在工作'和'已完成'下。每行显示会话的名称、其最新状态或问题以及时间。底部是用于描述新任务的输入和一行键盘提示。" width="1872" height="680" data-path="images/agent-view-dark.png" />

当你有多个独立任务 Claude 可以在不需要你观看每一步的情况下处理时，使用 agent view。调度一个 bug 修复、一个拉取请求审查和一个不稳定测试调查作为三行，在另一个窗口中继续工作，当一行显示它需要你或有结果时检查回来。

当你想在任何代理的会话中更直接地工作时，附加到该行以进入完整对话。

要比较 agent view 与 subagents、agent teams 和 worktrees，请参阅 [并行运行代理](/docs/zh-CN/agents)。Agent view 在你的机器上运行会话，你调度每一个；要让 Claude 从一个对话中在云端启动和跟踪并行会话，请参阅 [Projects](/docs/zh-CN/claude-projects)。

<Note>
  Agent view 处于研究预览阶段。随着功能的发展，界面和快捷键可能会改变。
</Note>

<h2 id="quick-start">
  快速开始
</h2>

本演练涵盖核心 agent view 循环：调度一个任务，观看其行在 Claude 工作时更新，窥视以检查它并回复，以及附加到完整对话。你调度的会话在关闭 agent view 后继续运行，所以你可以离开并稍后回到它。

<Steps>
  <Step title="打开 agent view">
    从你的 shell，运行：

    ```bash theme={null}
    claude agents
    ```

    如果你还没有接受该目录的[工作区信任对话框](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust)，Claude Code 会在 agent view 打开前显示它，与 `claude` 显示的对话框相同。接受以保存工作区的信任并继续。如果你拒绝，Claude Code 会退出而不打开 agent view。

    Agent view 打开，底部有一个输入框，当会话启动时表格会填充。随时按 `Esc` 返回你的 shell；如果你通过后台会话 `←` 打开了 agent view，`Esc` 会返回到该对话框。你的会话在你离开时继续运行，下次打开 agent view 时会重新出现。
  </Step>

  <Step title="调度一个会话">
    输入描述任务的提示并按 `Enter`。一个新的后台会话在该任务上启动并显示为一行，显示它是否正在工作、等待你或已完成。新会话使用 agent view 标题中显示的模型。[它启动的权限模式](#permission-mode-model-and-effort)取决于你如何打开 agent view。

    你在此输入的每个提示都会启动自己的新会话。输入另一个提示并按 `Enter` 会启动第二个会话，与第一个会话并行运行，而不是向其发送后续消息。你可以通过这种方式并行运行多个会话。

    每个会话独立使用你的订阅配额，所以在一次调度多个会话之前，请查看[限制](#limitations)。
  </Step>

  <Step title="窥视和回复">
    用箭头键选择一行并按 `Space` 打开窥视面板。它显示会话的最近输出，或它正在等待的问题，而不是完整的记录。输入回复并按 `Enter` 发送，无需离开 agent view。
  </Step>

  <Step title="附加和分离">
    在一行上按 `Enter` 或 `→` 在你想要完整对话时附加。会话接管终端，就像一个完整的交互式 Claude Code 会话。在空提示上按 `←` 分离并返回表格。
  </Step>

  <Step title="将现有会话引入">
    这一步需要一个运行中的会话。如果你遵循了之前的步骤，你在此终端中没有打开的会话，所以在另一个终端中打开一个常规 `claude` 会话并先向其发送一条消息。

    要将你已经打开的会话移入 agent view，在其中运行 `/bg`，或在空提示上按 `←` 以后台会话并在一步中打开 agent view。在没有消息的新会话中，`/bg` 会要求你先发送一条消息，而 `←` 可以立即工作。会话继续运行并显示为一行，与你调度的会话并排。
  </Step>
</Steps>

在常规 `claude` 会话内，提示页脚的 `←` 提示计算正在等待你的后台 agent 数量，例如 `← 2 agents`，当没有 agent 需要输入时返回 `← for agents`。超过 99 的计数显示为 `99+`。当终端获得焦点时，计数大约每十秒刷新一次，当焦点返回时立即刷新。当计数移动和 agent 完成时，它会短暂改变颜色，当后台会话完成而没有 agent 需要你的输入时，它会短暂显示完成的数量，例如 `← 2 done`。当启用了[`prefersReducedMotion` 设置](/docs/zh-CN/settings-reference#prefersreducedmotion)时，两个闪烁都关闭，并且在[屏幕阅读器模式](/docs/zh-CN/accessibility)中隐藏提示。

<h3 id="open-agent-view-by-default">
  默认打开 agent view
</h3>

要让 `claude` 不带参数打开 agent view 而不是新对话，请打开一个 `/config` 设置。

<Steps>
  <Step title="打开设置">
    在常规 `claude` 会话中，运行 `/config` 并打开**默认打开 agents view**。要跳过菜单，直接设置 [`defaultToAgentsView`](/docs/zh-CN/settings-reference#defaulttoagentsview) 键：

    ```text theme={null}
    /config defaultToAgentsView=true
    ```
  </Step>

  <Step title="启动 Claude Code">
    退出会话，然后不带参数运行 `claude`：

    ```bash theme={null}
    claude
    ```

    Agent view 打开，代替新对话。
  </Step>
</Steps>

要在设置打开时启动常规会话，请传递一个提示：`claude "fix the login test"`。要关闭设置，在常规会话中或在从 agent view 附加的会话中运行 `/config defaultToAgentsView=false`。

<h2 id="monitor-sessions-with-agent-view">
  使用 agent view 监控会话
</h2>

运行 `claude agents` 打开 agent view。它接管整个终端并列出按状态分组的每个会话，固定的会话和需要你的会话在顶部。每行显示会话的名称、当前活动和其年龄，从会话创建时开始计算；已完成的会话的年龄冻结在运行花费的时间。

名称用该会话中由 [`/color`](/docs/zh-CN/commands) 设置的颜色着色。包括当你用 `←` 或 `/background` [后台会话](#from-inside-a-session)时。

默认情况下，列表显示你启动的每个后台会话，跨越所有项目。在一个存储库中工作的会话和在不同 worktree 中工作的另一个会话都会出现在这里，无论你从哪个目录打开 agent view。要将列表限制到一个项目，请传递 `--cwd`：

```bash theme={null}
claude agents --cwd ~/projects/my-app
```

这只显示在该目录下启动的会话。它仍然列出已[移入 worktree](#how-file-edits-are-isolated) 到 `~/projects/my-app/.claude/worktrees/` 下的会话。

你在其他终端中打开的交互式会话不会出现，直到你[后台它们](#from-inside-a-session)。[Subagents](/docs/zh-CN/sub-agents) 和 [teammates](/docs/zh-CN/agent-teams) 会话生成的不会列为单独的行。

```text theme={null}
Pinned
  ✽ clawd walk cycle          Drawing the walk-cycle sprite frames          3m

Ready for review
  ∙ jump physics              Opened PR with collision fix                 #2048  2h

Needs input
  ✻ power-up design           double jump or wall climb?                    1m

Working
  ✽ collision detection       Adding swept-AABB checks to CollisionSystem   2m
  ✢ playtest level 3          run 12 · all checkpoints cleared           in 4m

Completed
  ✻ title screen              result: menu, options, and credits done       9m
  ∙ sound effects             result: 14 SFX exported to assets/audio       4h
  … 6 more
```

<h3 id="read-session-state">
  读取会话状态
</h3>

每行以一个图标开头，其颜色和动画显示会话的状态：

| 状态 | 图标显示为 | 含义 |
| :- | :- | :- |
| 工作中 | 动画 | Claude 正在积极运行工具或生成响应 |
| 需要输入 | 黄色 | Claude 等待你提供的特定内容：问题的答案、权限决定或只有你能回答的另一个提示，例如 [sandbox](/docs/zh-CN/sandboxing) 提示以允许网络主机或 MCP 服务器的[请求输入](/docs/zh-CN/mcp#respond-to-mcp-elicitation-requests)。需要附加终端的命令，例如 `/install-github-app` 或 `/mcp` 设置列表，[也在此处保持无人值守的会话](#attach-to-a-session) |
| 空闲 | 暗淡 | 会话没有任何事情要做，准备好接收你的下一个提示 |
| 已完成 | 绿色 | 任务成功完成 |
| 失败 | 红色 | 任务以错误结束 |
| 已停止 | 灰色 | 你用 `Ctrl+X` 或 `claude stop` 停止了会话，[其进程从 Claude Code 外部结束](#the-supervisor-process)，或[它在后台服务关闭时结束](#sessions-show-as-failed-after-shutdown) |

另外，图标的形状显示底层进程是否正在运行：

| 形状 | 含义 |
| :- | :- |
| `✻` 或动画 `✽` | 会话进程处于活跃状态并立即回复 |
| `∙` | 进程已退出。你仍然可以窥视该行，当你回复或附加时，Claude 从中断处重新启动 |
| `✢` | 一个 [`/loop`](/docs/zh-CN/scheduled-tasks) 会话在迭代之间休眠。该行显示其运行计数和倒计时 |

行右边缘可能出现的 `#N` 或 `!N` 标签是[会话的拉取请求或合并请求](#pull-request-status)的链接，不是状态图标的一部分。

终端标签标题在 agent view 打开时显示等待输入的计数：当会话需要输入时显示 `2 awaiting input · claude agents`，或当没有会话需要输入时显示 `claude agents`。

要从脚本或另一个程序读取会话状态，请使用 [`claude agents --json`](#read-session-state-from-a-script) 而不是 `~/.claude/jobs/` 下的文件。

当 agent view 打开时，Claude Code 还会通过你配置的[终端通知频道](/docs/zh-CN/terminal-config#get-a-terminal-bell-or-notification)发送通知，当本地后台会话开始需要你的输入、完成或失败时。在计划上运行的会话，例如 [`/loop`](/docs/zh-CN/scheduled-tasks) 会话，仅在需要你的输入时通知。通知使用与 Claude Code 其余部分相同的 [`preferredNotifChannel` 设置](/docs/zh-CN/settings-reference#preferrednotifchannel)，并使用 `agent_needs_input` 或 `agent_completed` 类型触发 [`Notification` hook](/docs/zh-CN/hooks#notification)。

后台会话不需要任何打开的终端来继续工作。一个单独的[监督进程](#the-supervisor-process)运行它们，所以你可以关闭 agent view、关闭你的 shell 或启动一个新的交互式会话，你的调度工作继续进行。

会话状态通过自动更新和监督进程重启在磁盘上持久化。会话在你的机器休眠时也会被保留。它们的进程在唤醒时恢复，监督进程重新连接到它们，而不是将时间间隙视为空闲。关闭仍然会停止运行中的会话；请参阅[关闭后会话显示为失败或停止](#sessions-show-as-failed-after-shutdown)了解如何恢复它们。

当机器在会话中途响应时休眠时，会话可能会陷入无响应状态。当你打开一个已停止响应的会话时，监督进程重启其进程，会话从中断处继续中断的响应。

<h3 id="row-summaries">
  行摘要
</h3>

每行中的单行摘要由 [Haiku-class 模型](/docs/zh-CN/model-config)生成，所以该行可以告诉你会话正在做什么、需要什么或生成了什么，无需打开记录。当会话正在积极工作时，摘要最多每 15 秒从会话自己的最近输出刷新一次，无需发送模型请求，每个回合结束时模型写入新摘要。

工作中的行显示会话说它正在做什么，被阻止的行显示它提出的问题。在长回合期间，模型也大约每分钟重写一次摘要，所以繁忙的行不会继续显示过时的摘要。摘要文本填充行的剩余宽度；打开[窥视面板](#peek-and-reply)读取终端边缘裁剪的句子。

当列表[按目录分组](#organize-the-list)时，摘要以会话的状态作为彩色单词开头，例如 `Needs input · double jump or wall climb?`。在默认状态分组中，组标题已经命名了状态，所以行只显示摘要。

结束回合摘要和每次中途重写是通过你的正常提供商的一个短 Haiku-class 请求，按与会话本身相同的[数据使用条款](/docs/zh-CN/data-usage)计费和处理。15 秒的模型重写之间的更新重用会话自己的输出，不发送请求。在没有配置 Haiku-class 模型的第三方提供商或网关上，请求使用会话的主模型；设置 [`ANTHROPIC_DEFAULT_HAIKU_MODEL`](/docs/zh-CN/model-config#environment-variables) 以选择一个。

<h3 id="pull-request-status">
  拉取请求状态
</h3>

当会话[打开拉取请求](#how-file-edits-are-isolated)时，Claude Code 在行的右边缘添加一个标签，链接到拉取请求：

* Claude Code 将标签写为 `#1234` 用于拉取请求，`!1234` 用于 GitLab 合并请求。
* Claude Code 即使无法检测到超链接支持（例如通过 SSH 或 tmux）也会发出链接。设置 [`FORCE_HYPERLINK=0`](/docs/zh-CN/env-vars) 将标签呈现为纯文本。
* 在你向会话发送后续内容后，Claude Code 保持标签，同时行返回到实时进度。

处理现有拉取请求的会话以相同方式链接到它。Claude Code 根据 Claude 运行的命令以不同方式查找拉取请求：

* 当 Claude 用 `gh` 编辑、评论、关闭或标记拉取请求为就绪时，Claude Code 链接命令自己的输出命名的拉取请求。捕获的输出不命名拉取请求的 `gh` 命令不创建链接；`gh pr merge` 是常见情况，因为它仅将其结果打印到交互式终端。
* 当 Claude 用 `gh pr checkout` 检出拉取请求或推送到分支时，Claude Code 用 `gh pr view` 查找分支并链接其打开的拉取请求。
* 当 Claude 推送时拉取请求不需要已存在：Claude Code 在同一目录中最多五个后续 `git`、`gh`、`glab` 或 `curl` 命令运行后重试分支查找，所以在推送后创建的拉取请求，包括 Claude 通过 GitHub REST API 创建的，在重试找到它时链接。

当会话链接到多个拉取请求时，标签显示计数，例如 `3 PRs`，按最需要关注的打开拉取请求着色。打开[窥视面板](#peek-and-reply)查看它们全部。

拉取请求编号由其状态着色：

| 颜色 | 拉取请求状态 |
| :- | :- |
| 黄色 | 等待检查或审查，或检查失败 |
| 绿色 | 检查通过且没有审查阻止 |
| 紫色 | 已合并 |
| 灰色 | 草稿或已关闭 |

对于以拉取请求结束的任务，检查此标签以获取结果：当其编号变绿时审查和合并拉取请求。

<h3 id="peek-and-reply">
  窥视和回复
</h3>

在选定的行上按 `Space` 打开窥视面板。它打开时显示行截断的句子，该句子是什么取决于会话的状态：

* 等待你的会话：它提出的确切问题，在回复输入上方
* 已完成的会话：其结果
* 工作中的会话：其完整状态句子

任何链接到会话的拉取请求都列在下面。对于等待你的会话，下面的一行，例如 `waiting 3m` 显示它已经等待多长时间，这是面板中唯一显示的时间。行右边缘的年龄是一个不同的数字：它从会话启动时开始计算。

大多数时候窥视面板就足够了，你不需要打开完整的记录。

在窥视面板中输入回复并按 `Enter` 将其发送到该会话。当会话提出带有预定义选择的问题时，窥视面板将它们显示为编号列表，你可以按数字键选择一个。权限提示显示为描述会话想要运行的内容的文本，没有编号选项。输入回复以回答它，或附加以用标准提示回答。对于其他被阻止的会话，按 `Tab` 用建议的回复填充输入，你可以在发送前编辑。用 `!` 前缀回复以发送 Bash 命令。

当 [`PermissionRequest`](/docs/zh-CN/hooks#permissionrequest) 或 [`PreToolUse`](/docs/zh-CN/hooks#pretooluse) hook 返回 Claude Code 无法为会话询问的调用验证的输出时，行显示 hook 事件和 `hook output invalid:` 以及验证错误，然后是待处理请求的文本。对于以其他方式失败的 hook，行说 hook 失败。会话仍然等待相同的请求。

无法传递的回复，因为后台服务无法访问或发送失败，会被保存并在其进程再次启动时作为其下一个提示发送到会话，错误消息说回复已保存。前缀为 `!` 的回复不会被保存，因为保存的文本会作为纯提示而不是 Bash 命令到达会话。

启用[语音听写](/docs/zh-CN/voice-dictation)后，在回复输入获得焦点时按住或点击你的推送通话键以听写回复而不是输入。同样的功能在 agent view 底部的调度输入中也有效。

使用 `↑` 和 `↓` 窥视相邻会话而不关闭面板，或 `→` 附加。

<h3 id="attach-to-a-session">
  附加到会话
</h3>

在选定的行上按 `Enter` 或 `→` 附加。Agent view 被完整的交互式会话替换。当你附加时，Claude 发布一个关于你离开时发生的事情的简短回顾。

附加时，会话的行为像任何其他 Claude Code 会话：[命令](/docs/zh-CN/commands)、快捷键和功能都有效，除了下面的例外。

当你附加时，`/install-github-app` 和 [`/mcp`](/docs/zh-CN/mcp) 设置列表正常工作，因为终端上有人可以完成它们的对话。当没有人附加时，这些命令无法打开它们的对话，所以会话在 agent view 中显示在 `Needs input` 下，行如 `open this session to manage MCP servers`，记录回复说相同的内容。附加并再次运行命令以继续；当你附加时需要输入的行清除。`/mcp reconnect <server>`、`/mcp enable` 和 `/mcp disable` 无论哪种方式都无需附加即可工作。

附加的会话始终以[全屏模式](/docs/zh-CN/fullscreen)呈现，无论你的 `tui` 设置如何，因为后台会话没有终端滚动历史可追加。使用 `PgUp`、`PgDn` 或鼠标滚轮滚动，按 `Ctrl+O` 进入记录模式。你的终端的原生滚动和 tmux 复制模式仅显示当前视口，与运行任何全屏应用程序时相同。

在空提示上按 `←` 或运行 `/exit` 分离并返回 agent view，无论你从 agent view 打开会话还是从 shell 用 `claude attach <id>` 运行。

当 [`/btw` overlay](/docs/zh-CN/interactive-mode#side-questions-with-%2Fbtw) 打开时，`←` 也分离。需要 Claude Code v2.1.257 或更高版本。仍在回答的侧问题在你离开时继续运行。下次你附加时，overlay 会重新打开它，或带有它的答案。

在 Windows 上，如果你在附加后约半秒内按 `←`，Claude Code 显示 `Ambiguous ←, press again to detach`，因为在该窗口中终端可以重新传递附加前的按压。再按一次 `←` 以分离。

`Ctrl+Z` 也分离但返回到你开始的地方：如果你从那里附加则返回 agent view，或如果你运行了 `claude attach` 则返回你的 shell。当对话有焦点且不响应 `←` 时使用 `Ctrl+Z`。

`Ctrl+C` 在附加时保持其标准中断行为：它取消运行中的响应或 `!` shell 命令，而不是分离。在空提示上按两次 `Ctrl+C` 分离，与任何会话中的相同。

分离永远不会停止后台会话：`←`、`Ctrl+Z`、`/exit` 和双 `Ctrl+C` 或双 `Ctrl+D` 都让它运行。要从内部结束会话，运行 `/stop`。

<h4 id="switch-sessions-without-leaving-the-terminal">
  在不离开终端的情况下切换会话
</h4>

在前台运行的会话中，一个你在终端中启动的而不是从 agent view 附加的，在空提示上按 `←` 会后台它并打开 agent view，该行被选中，所以你可以在不离开终端的情况下切换会话。同样的单次按压分离附加的会话。

如果你在删除提示的最后文本或通过提示历史移动后立即按 `←`，Claude Code 会要求你确认：第一次按压显示 `Press ← again to open agents`，或在附加的会话中显示 `Press ← again to go back to agents`，第二次按压切换。

当 `←` 后台前台会话时，agent view 显示 `Your conversation moved to the background` 在列表上方，该会话的行已被选中。从那里：

* 按 `Enter` 重新打开对话。
* 按 `Esc` 撤销切换并返回对话。如果 `Esc` 显示 `Still starting — try again in a moment`，后台会话还没有准备好，所以稍后再按一次 `Esc`。
* 按 `Ctrl+C` 两次以退出到你的 shell。

当 Claude Code 无法重新打开对话时，它退出并打印一个 `claude --resume` 命令来恢复它。

[Claude 的任务列表](/docs/zh-CN/interactive-mode#task-list)随对话移动到后台会话，所以当你返回该行时清单是完整的。

你按 `←` 的行也在你用箭头键或鼠标移动选择后保持粗体、未暗淡的名称，所以你可以告诉你来自哪个会话。

如果在你按 `←` 时工具正在运行，Claude Code 会等待大约十秒钟让它完成后台，响应在后台会话中继续。再按一次 `←` 以立即后台而不是等待。当进行中的工作无法转移到后台会话时，Claude Code 首先显示 `Background this session?` 对话，与 [`/background`](#from-inside-a-session) 相同。

十秒限制在[前台 subagents](/docs/zh-CN/sub-agents#run-subagents-in-foreground-or-background) Claude 在对话中启动的仍在运行时不适用。Claude Code 继续等待以便它们的工作转移，并在等待时显示 `Still backgrounding after the current tool` 通知。再按一次 `←` 以立即后台而不等待，这会从头重新启动这些 subagents。Claude Code 不等待[动态工作流](/docs/zh-CN/workflows)正在运行的 subagents。当工作流有 subagents 运行时，Claude Code 显示 `Background this session?` 对话。

Claude Code 不会在你的提示输入中有未发送的文本时后台会话，因为文本会留在你的终端输入框中，不会移动到后台会话。如果你在 Claude Code 等待后台会话时输入到输入中，它会用 `Backgrounding cancelled — you have unsent text in the input. Send it or clear it, then press ← again.` 取消切换。

按 `←` 创建会话的行，即使对话还没有消息，所以 `→` 仍然返回到它。

你可以在 `/config` 中用 [`leftArrowOpensAgents`](/docs/zh-CN/settings-reference#leftarrowopensagents) 设置关闭此快捷键。

<h3 id="organize-the-list">
  组织列表
</h3>

Agent view 按状态分组会话，需要输入的会话在顶部，`Ready for review` 和 `Needs input` 在 `Working` 和 `Completed` 上方。这些组名不与上面的[状态](#read-session-state)一一对应：当会话有打开的拉取请求时，它移动到 `Ready for review`，`Completed` 收集已完成、失败和已停止的会话。

按 `Ctrl+S` 改为按目录分组。你的选择在运行中保存。

在一个组内：

* 按 `Ctrl+T` 将会话固定到顶部并[在空闲时保持其进程运行](#the-supervisor-process)
* 按 `Shift+↑` 或 `Shift+↓` 重新排序会话
* 按 `Ctrl+R` 重命名会话
* 在组标题上按 `Enter` 折叠它

要从列表中删除会话，按 `Ctrl+X` 停止它，在两秒内再按 `Ctrl+X` 删除它。在组标题上按 `Ctrl+X` 在确认后删除该组中的每个会话。

第二次按压删除会话，即使停止尝试失败，例如因为[后台服务没有响应](#agent-view-says-the-background-service-did-not-respond)：确认保持活跃另外两秒，删除结束会话的进程本身。按 `Esc` 关闭确认而不删除。

除了[删除会话删除什么](#what-deleting-a-session-removes)中涵盖的保留情况外，删除会从列表中删除会话，Claude 为其创建的 worktree 会被删除、保留或留在原地，取决于你如何删除以及 worktree 保留什么。对话记录始终保留在你的本地机器上，可通过 `claude --resume` 访问。

要在 Claude Code v2.1.212 或更高版本上恢复会话，在调度输入中输入 `/resume`。一个选择器打开，显示你打开 agent view 的存储库的过去会话，最新的在前，包括你从列表中删除的会话；已有行的会话不会列出。`↑`/`↓` 移动选择，`Enter` 恢复选定的会话作为后台会话，所以它重新加入列表作为行，`Esc` 关闭选择器。

选择器仅对裸 `/resume` 打开。有针对性的、作用域的或受限的恢复无法由选择器提供，所以当以下情况时 agent view 显示 `attach to a session to run it` 提示：

* `/resume` 命名一个 id 或搜索项
* 视图用 `--cwd` 作用域
* 视图用 [`--safe-mode`](/docs/zh-CN/cli-reference#cli-flags) 启动
* 视图用 `--permission-mode` 或 `--settings` 等标志打开

不适合屏幕的已完成会话折叠成 `… N more` 行。失败和有打开拉取请求的会话始终保持可见。`Completed` 组填充活跃组之后剩余的垂直空间，在短终端上标题压缩为单个摘要行，以便正在工作或需要输入的会话保持可见。

<h3 id="filter-sessions">
  过滤会话
</h3>

在调度输入中输入以过滤而不是调度：

| 过滤 | 显示 |
| :- | :- |
| `a:<name>` | 运行命名代理的会话 |
| `s:<state>` | 给定状态的会话，例如 `s:working`。也接受 `s:blocked` 用于等待你的所有内容 |
| `#<number>` 或拉取或合并请求 URL | 处理该拉取请求或合并请求的会话 |
| 任何其他 URL | 其第一个提示包含该 URL 的会话 |

<h3 id="keyboard-shortcuts">
  快捷键
</h3>

在 agent view 中按 `?` 查看每个快捷键的上下文。下表总结了它们。

| 快捷键 | 操作 |
| :- | :- |
| `↑` / `↓` | 在行之间移动 |
| `Enter` | 附加到选定的会话，或如果输入中有文本则调度 |
| `Space` | 打开或关闭选定会话的窥视面板 |
| `Shift+Enter` | 在调度输入中插入换行符，[如在主提示中](/docs/zh-CN/terminal-config#enter-multiline-prompts) |
| `Ctrl+Enter` | 调度并立即附加，在终端中 `?` overlay 列出 `ctrl+enter to start and open` |
| `→` | 附加到选定的会话 |
| `Alt+1`..`Alt+9` | 附加到焦点会话目录中的第 1–9 个会话 |
| `Tab` | 在空输入上浏览所有 subagents。否则应用突出显示的建议 |
| `Ctrl+S` | 在状态和目录之间切换分组 |
| `Ctrl+T` | 固定或取消固定选定的会话 |
| `Ctrl+R` | 重命名选定的会话 |
| `Ctrl+G` | 在你的 `$VISUAL` 或 `$EDITOR` 中打开调度提示 |
| `Ctrl+J` | 在调度输入中插入换行符 |
| `Ctrl+X` | 停止会话；在两秒内再按一次删除它 |
| `Shift+↑` / `Shift+↓` | 重新排序选定的会话 |
| `Esc` | 关闭窥视面板、清除输入或退出。当你通过用 `←` 后台会话打开 agent view 时，最后的 `Esc` 返回该对话而不是退出。启用[vim 编辑器模式](/docs/zh-CN/interactive-mode#vim-editor-mode)时，在输入中按 `Esc` 从 INSERT 切换到 NORMAL 模式并保留你的文本，如在主提示中 |
| `Ctrl+C` | 清除输入；按两次退出 |
| `?` | 显示所有快捷键 |

`Ctrl+S`、`Ctrl+T` 和 `Ctrl+G` 遵循你的 [`keybindings.json`](/docs/zh-CN/keybindings)。在 [`Agents` 上下文](/docs/zh-CN/keybindings#agents-actions)中用 `agents:switchView` 和 `agents:togglePin` 操作重新绑定或取消绑定 `Ctrl+S` 和 `Ctrl+T`，以及通过 `Chat` 上下文的 `chat:externalEditor` 绑定的 `Ctrl+G`。表中的其他快捷键无法重新绑定。

<h2 id="dispatch-new-agents">
  分派新的 agents
</h2>

您可以从 agent 视图分派新的后台会话，将现有的交互式会话发送或复制到后台，或直接从 shell 启动一个。

<h3 id="from-agent-view">
  从 agent 视图
</h3>

在 agent 视图底部的输入框中输入提示，然后按 `Enter` 启动新的后台会话。会话会根据提示自动命名；稍后可以使用 `Ctrl+R` 重命名。

自动名称是由 [Haiku-class model](/docs/zh-CN/model-config) 生成的简短标签。会话稍后获得的名称也会显示在其行上，包括当您在该会话中 [接受计划](/docs/zh-CN/permission-modes#review-and-approve-a-plan) 时会话获得的 [生成的标题](/docs/zh-CN/sessions#name-your-sessions)。

将图像粘贴到提示中以包含屏幕截图或图表与任务。

粘贴的文本超过 800 个字符或超过三行时会折叠为 `[Pasted text #N]` 占位符，以便输入保持在一行；完整文本在您分派时发送。要在分派前查看或编辑折叠的文本，请再次粘贴相同的文本，占位符会展开回输入框。

在提示的前缀或提及部分来控制会话如何启动：

| 输入 | 效果 |
| :- | :- |
| `<agent-name> <prompt>` | 如果第一个单词与自定义 [subagent](/docs/zh-CN/sub-agents) 名称匹配，该 subagent 将作为会话的主 agent 运行，使用其 frontmatter 中的配置 |
| `@<agent-name>` | 在提示中的任何位置提及自定义 subagent 以将其作为主 agent 运行 |
| `@<repo>` | 提及一个存储库以在该处运行会话。请参阅 [分派到特定目录](#dispatch-to-a-specific-directory) 了解列出了哪些存储库 |
| `/<command>` | 建议 [skills](/docs/zh-CN/skills) 和 [commands](/docs/zh-CN/commands) 作为提示分派 |
| `! <command>` | 运行 shell 命令作为后台作业，而不是启动 Claude 会话。该作业显示为一行，您可以附加到、观看和分离 |
| `#<number>` 或 pull 或 merge request URL | 如果会话已在处理该 pull request 或 merge request，Claude Code 会选择其行而不是分派新会话 |

一小组命令在 agent 视图本身中运行，而不是分派：

* `/exit` 和 `/quit` 关闭 agent 视图
* `/logout` 将您登出
* `/model` 设置 [分派模型](#set-the-model)
* `/login` 打开登录对话框，以便您可以重新登录而无需附加到会话
* 裸 `/resume` 或其 `/continue` 别名打开存储库过去会话的选择器，以 [恢复一个](#organize-the-list) 作为后台会话。需要 Claude Code v2.1.212 或更高版本

Skills、您自己的命令和提示扩展内置命令（如 `/init`）作为其第一个提示发送到新的后台会话。其他内置命令显示 `attach to a session to run it` 提示。您输入的所有内容都保留在提示旁边的输入中，以便您可以编辑。

将重复任务打包为 [skill](/docs/zh-CN/skills) 可让您从 agent 视图重复启动相同的工作流，而无需重新输入提示。

当相同的 `@name` 同时匹配 subagent 和同级存储库时，subagent 优先。裸第一个单词匹配也适用，因此恰好以您的 subagent 名称之一开头的提示会分派该 subagent，而不是将该单词视为纯文本。当您想要明确时使用 `@` 形式，或以不同的单词开头提示以避免匹配。

<h4 id="dispatch-to-a-specific-directory">
  分派到特定目录
</h4>

新会话在您打开 agent 视图的目录中运行。要针对不同的目录，请使用以下任何一种：

* 在该目录中打开 `claude agents`。
* 在父目录中打开 `claude agents` 并在提示中使用 `@<repo>` 提及子存储库。输入 `@` 列出这些目标：

  * 启动目录下一级的 Git 存储库
  * 您启动的存储库的已注册 [git worktrees](/docs/zh-CN/worktrees)，位于其目录树内，例如 Claude 在 `.claude/worktrees/` 下创建的，标记有其检出的分支。在存储库外添加的 Worktrees，例如使用 `git worktree add ../feature`，不会列出
  * 列表中已有会话的任何目录

  名称包含空格的目录不会列出。
* 从 shell，`cd` 进入目录并运行 `claude --bg "<prompt>"`。

当 agent 视图按目录分组时，分派会将提示发送到所选行的目录，因此您可以选择一个组并分派到其中，而无需重新输入路径。

<h3 id="from-inside-a-session">
  从会话内部
</h3>

两个命令将工作从您所在的会话移到后台：`/background` 将当前对话发送到那里并释放您的终端，`/fork` 发送一个副本，同时您继续在原处工作。

<h4 id="send-the-session-to-the-background">
  将会话发送到后台
</h4>

运行 `/background` 或其别名 `/bg` 将当前对话移到后台会话。传递一个提示，例如 `/bg run the test suite and fix any failures` 以首先给出一个更多指令。如果您运行 `/bg` 时 Claude 正在响应，响应会在后台会话中继续。

退出仍有后台工作运行的会话（例如 subagents、后台 shell 命令、工作流或 [monitors](/docs/zh-CN/tools-reference#monitor-tool)）会显示 `Background work is running` 对话框，而不是立即退出。选择 `Move to background and exit` 以与 `/background` 相同的方式将会话移到后台并返回到您的 shell。当 agent 视图 [关闭](#turn-off-agent-view) 时不显示该选项。

如果列表上的后台会话已具有对话的名称，Claude Code 会对新行的名称进行编号，例如 `my-session (2)`，并保持现有行的名称不变。要重命名新行，在 agent 视图中选择它并按 `Ctrl+R`。

<h4 id="copy-the-session-with-/fork">
  使用 /fork 复制会话
</h4>

运行 `/fork` 将当前对话复制到新的后台会话，同时原始会话继续运行。副本从对话中到该点的所有内容开始；请参阅下面的项目符号了解副本运行的位置。它还继承模型、权限模式、努力级别以及您在会话期间添加的任何目录或"不再询问"权限授予。副本在 agent 视图中显示为其自己的行。

在 fork 之后，两个对话是独立的：副本所做的任何事情都不会自动进入原始对话，尽管在启用 [cross-session messaging](/docs/zh-CN/cross-session-messaging) 的会话中，任一会话的 Claude 都可以显式地向另一个发送消息。

复制会话需要 Claude Code v2.1.212 或更高版本；在 v2.1.161 到 v2.1.211 上，`/fork` 启动 [forked subagent](/docs/zh-CN/sub-agents#fork-the-current-conversation)，现在是 `/subtask`。当 [agent 视图关闭](#turn-off-agent-view) 时，`/fork` 保持 forked-subagent 行为，`/subtask` 不可用。

传递一个提示，例如 `/fork open a draft pull request with the work so far`，副本立即开始处理它。没有提示的情况下，副本等待其第一个指令：在 `claude agents` 中选择其行并按 `Space` 发送一个，或运行 `claude attach <id>`。所选行在等待时显示 `space to send it a prompt`。

`/fork` 确认是一行，显示副本的状态，例如 `session running`、其 agent-view 行的名称和其会话 ID（用于 `claude attach`）。单击名称以切换到副本：此会话移到后台，与按 `←` 相同，agent 视图打开副本的会话。

除非副本 [就地编辑](#how-file-edits-are-isolated)，Claude Code 会指示它在进行代码更改前创建自己的 worktree。在 git 存储库外，只有从 hook 创建的 worktree 移出的副本才会获得该指令；没有 [`WorktreeCreate` hook](/docs/zh-CN/hooks#worktreecreate)，副本就地编辑。从您的 worktree 移出的副本也被告知永远不要编辑、在其中运行命令或进入该 worktree，无论隔离设置如何。

副本启动的位置取决于当前会话运行的位置：

* 像任何分派的会话一样，副本 [在编辑文件前移到自己的 worktree](#how-file-edits-are-isolated)。在这种情况下，确认不会提及副本运行的位置。
* 当您的会话在启动后移到其链接的 [worktree](/docs/zh-CN/worktrees) 时，副本从会话移动前的位置开始，除非它 [就地编辑](#how-file-edits-are-isolated)，在那里进行其代码更改到自己的 worktree。当您的 worktree 在分支上检出时，该指令也告诉副本（其任务建立在您的工作基础上）将其新分支基于您的分支，因为您的分支在您的 worktree 中保持检出。确认以 `runs in the origin tree` 结尾。
* 当您在具有主工作树的存储库的链接 worktree 内启动会话时，副本从该主工作树开始，具有相同的 worktree-of-its-own 规则但没有分支指令。确认也以 `runs in the origin tree` 结尾。
* 在裸存储库布局的 worktree 内启动的会话没有主工作树可返回，因此副本保持原位，确认以 `edits this checkout` 结尾。当 worktree 隔离在不在链接 worktree 内的会话中 [关闭](#how-file-edits-are-isolated) 时，也会出现相同的注释，因为副本随后编辑您打开的文件。

使用启动标志启动的会话副本不会继承，例如替换的系统提示或 `--tools` 允许列表，无法 fork；Claude Code 会说明这一点，而不是进行部分副本。从 agent 视图分派的会话正常 fork：副本使用与其来自的会话相同的 [agent 定义](/docs/zh-CN/sub-agents) 和附加指令启动。

<h4 id="what-carries-over-when-you-background">
  后台处理时的继承内容
</h4>

后台处理启动一个新进程，从保存的对话恢复，进行中的工作移到其中：运行后台 shell 命令、后台 subagents、动态工作流、使用 [`/loop`](/docs/zh-CN/scheduled-tasks) 创建的计划任务以及 Claude 对 [artifact 注释的自动回复](/docs/zh-CN/artifacts#let-claude-reply-to-comments-on-its-own) 都会继承并继续在那里运行。Subagent 与它启动的所有内容一起移动，因此仅当所有该工作也能移动时才会继承。要停止进行中的工作而不是继承它，请设置 [`CLAUDE_DISABLE_ADOPT=1`](/docs/zh-CN/env-vars#variables) 环境变量；Claude Code 随后会在后台处理前要求您确认。

当 [dynamic workflow](/docs/zh-CN/workflows) 仍有 subagents 运行时，Claude Code 在后台处理前询问 `Background this session?` 对话框，其中说明有多少 subagents 会重新启动。选择 `Stay` 让它们先完成。如果您确认，Claude Code 会在后台会话中重放运行：仍在运行的 subagents 从头开始，因此它们迄今为止使用的令牌会再次花费。请参阅 [Resume after a pause](/docs/zh-CN/workflows#resume-after-a-pause) 了解哪些已完成的 subagents 返回其保存的结果，哪些再次运行。

Claude Code 停止无法继承的工作，例如运行的 [monitor](/docs/zh-CN/tools-reference#monitor-tool)，并停止拥有 monitor 的后台 subagent 及其一起。当任何此类工作运行时，Claude Code 显示 `Background this session?` 对话框，以便您可以在停止工作前确认。

一旦在后台，会话可以启动新的 subagents、monitors 和后台命令，这些在稍后分离和重新附加时继续运行。

来自原始启动的配置标志通过到后台会话，因此其 MCP 服务器、设置和回退模型保持有效：

* `--mcp-config` 和 `--strict-mcp-config`
* `--settings`
* `--setting-sources`
* `--add-dir`
* `--plugin-dir`
* `--fallback-model`
* `--allow-dangerously-skip-permissions`

您在会话期间使用 [`/add-dir`](/docs/zh-CN/permissions#additional-directories-grant-file-access-not-configuration) 添加的目录也会继承。继承 `--allow-dangerously-skip-permissions` 使 `bypassPermissions` 在后台会话中可访问，但它不授予任何新内容：该模式仍需要 [Permission mode, model, and effort](#permission-mode-model-and-effort) 中描述的一次性交互式接受。

<h3 id="from-your-shell">
  从您的 shell
</h3>

传递 `--bg` 或其长形式 `--background` 启动直接进入后台的会话：

```bash theme={null}
claude --bg "investigate the flaky SettingsChangeDetector test"
```

提示是位置参数，不是 `-p` 值。Claude Code 拒绝 `--bg` 与 `-p` 或 `--print` 组合在任何会话创建前，因为 `--print` 永远不会启动 `claude agents` 附加到的交互式会话。

如果您从您未 [信任](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust) 的目录中的终端运行 `claude --bg`，工作区信任对话框会首先出现，会话在您接受后启动。如果您拒绝，Claude Code 会退出而不启动会话。在没有对话框可以出现的地方，例如在脚本中，命令会以 [`Workspace not trusted`](/docs/zh-CN/errors#workspace-not-trusted-when-dispatching-a-background-session) 错误退出。

要运行您定义的特定 [subagent](/docs/zh-CN/sub-agents)（例如 `code-reviewer`）作为会话的主 agent，将 `--bg` 与 `--agent` 组合：

```bash theme={null}
claude --agent code-reviewer --bg "address review comments on PR 1234"
```

如果名称与您的任何 subagents 不匹配，启动失败：Claude Code 打印 `no agent named` 警告，仍然报告会话为后台，但会话立即以 `--agent '<name>' not found` 错误退出。

当后台会话稍后恢复或重新启动时，Claude Code 恢复 agent 及其工具限制；对于其系统提示，请参阅 [System prompt flags in resumed conversations](/docs/zh-CN/cli-reference#system-prompt-flags-in-resumed-conversations)。它首先在会话自己的目录中搜索 agent，前提是您已 [信任该工作区](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust)，因此项目范围的 agent 在从另一个目录恢复会话时仍会加载。如果 agent 不再存在，会话继续使用默认工具，其记录打开时带有 [warning naming the agent](/docs/zh-CN/errors#session-agent-no-longer-available)。

要在后台继续现有对话，使用 `--resume` 传递其完整会话 ID：

```bash theme={null}
claude --resume 1f0e2c9a-6d0b-4c11-9f39-2a77c1d4e8b5 --bg "pick up where you left off and finish the migration"
```

在 Claude Code v2.1.257 或更高版本上，Claude Code 要么在相同 ID 下继续该会话，要么在新 ID 下启动副本并打印 `note:` 行解释为什么它无法就地继续。当会话就地继续时，`claude agents` 为其显示一行。

当您将 `--bg` 与 `--continue`、裸 `--resume` 或 `--resume` 与名称或文件路径组合时，Claude Code 总是启动这样的副本。添加 `--fork-session` 以有目的地启动副本，不带注释。

传递 `--name` 以在 agent 视图中设置会话的显示名称，而不是自动生成的名称：

```bash theme={null}
claude --bg --name "flaky-test-fix" "investigate the flaky SettingsChangeDetector test"
```

后台处理后，Claude 打印会话的短 ID 和用于管理它的命令。当托管后台会话的服务尚未运行时，`--bg` 可能首先在此输出上方打印 `Starting background service…`。当您传递 `--name` 时，名称显示在短 ID 后：

```text theme={null}
backgrounded · 7c5dcf5d · flaky-test-fix
  claude agents             list sessions
  claude attach 7c5dcf5d    open in this terminal
  claude logs 7c5dcf5d      show recent output
  claude stop 7c5dcf5d      stop this session
```

<h4 id="run-a-shell-command">
  运行 shell 命令
</h4>

要运行 shell 命令作为后台作业而不是 Claude 会话，传递 `--exec`。以下示例运行 `pytest -x` 作为后台作业：

```bash theme={null}
claude --bg --exec 'pytest -x'
```

从 agent 视图，通过在分派输入的第一个字符中输入 `!` 分派相同类型的作业：`!` 显示为前缀，其后的所有内容是命令，`Enter` 启动作业。

命令作为 PTY 支持的作业运行，在 agent 视图中显示为一行，最近的输出行作为其状态。Shell 作业运行命令代替 Claude，因此不调用任何模型，输出不发送到任何会话。

要查看输出，附加到行，按 `Space` 在不附加的情况下查看，或从您的 shell 运行 `claude logs <id>`。捕获的输出保留在内存中，不写入磁盘。行及其输出在命令退出后约五分钟自动清理，因此如果您需要结果，请在那之前读取。

<h3 id="how-file-edits-are-isolated">
  文件编辑如何隔离
</h3>

每个后台会话，无论是从 agent 视图、`/bg` 还是 `claude --bg` 启动，都在您打开的工作目录中启动。在编辑文件前，Claude 将会话移到 `.claude/worktrees/` 下的隔离 [git worktree](/docs/zh-CN/worktrees) 中，因此并行会话可以读取相同的检出，但每个写入自己的。一旦会话在其 worktree 中，Claude Code [为会话和它生成的任何 subagents 强制 worktree 隔离](/docs/zh-CN/worktrees#how-claude-code-enforces-isolation)。

Claude 在以下情况下跳过 worktree：

* 会话已在链接的 git worktree 内，无论 Claude 在 `.claude/worktrees/` 下创建它还是您使用 `git worktree add` 在其他地方创建它
* Claude 编辑的文件在链接的 git worktree 内，例如会话或其 subagent 使用 `git worktree add` 创建的
* 工作目录不是 git 存储库，且没有配置 [`WorktreeCreate` hook](/docs/zh-CN/hooks#worktreecreate)
* 写入在工作目录外

要为 git worktrees 不实用的存储库关闭 worktree 隔离，将 [`worktree.bgIsolation`](/docs/zh-CN/settings-reference#worktree-bgisolation) 设置为 `"none"`。后台会话随后直接编辑您的工作副本，而无需先移到 worktree。将设置添加到项目的 `.claude/settings.json`：

```json theme={null}
{
  "worktree": {
    "bgIsolation": "none"
  }
}
```

在 git 存储库外，会话直接写入工作目录，彼此之间不隔离，因此避免分派编辑相同文件的并行会话。如果您使用不同的版本控制系统，配置 [`WorktreeCreate` hook](/docs/zh-CN/worktrees#non-git-version-control)，Claude 以与 git 相同的方式隔离编辑。

当 hook 在不是 git 存储库的目录中失败时，Claude 跳过该目录的隔离，就地编辑工作目录。在 git 存储库内，Claude Code 阻止对共享检出的写入，直到 Claude 将会话移到 worktree。

要找到会话的 worktree 路径，查看会话或附加并检查其工作目录。

后台会话生成的 [subagent](/docs/zh-CN/sub-agents) 继承会话的工作目录，因此其文件编辑落在会话的 worktree 中，而不是您的工作副本。要给 subagent 其自己的单独 worktree，在其 frontmatter 中设置 [`isolation: worktree`](/docs/zh-CN/sub-agents#supported-frontmatter-fields) 或在生成它时传递 `isolation: "worktree"`。

当后台会话在 Claude 进入的 worktree 中进行了代码更改时，Claude Code 指示 Claude 在完成前保留工作，因此如果您删除会话及其 worktree，它会存活：

* **提交并推送**：Claude 无需询问即可提交，当存储库有远程时推送分支。
* **草稿 pull request**：Claude 在任务要求时打开一个，[`#N` 标签](#pull-request-status) 出现在行上。
* **永不**：推送到 `main` 或 `master`、强制推送和合并。
* **您的 git 指令优先**：如果任务、`CLAUDE.md` 或 [memory](/docs/zh-CN/memory) 说您自己处理提交或推送，Claude 将 git 留给您。

编辑未自己隔离的检出的会话仍在提交或切换分支前询问。这适用于隔离设置为 `"none"` 时、worktree 移动失败时或会话在已存在的 worktree 内启动时。

无论任务如何，Claude 以报告结束作业，说明它做了什么以及工作在哪里：路径、分支、pull request 或答案本身。

<h4 id="what-deleting-a-session-removes">
  删除会话会移除什么
</h4>

在 [agent 视图](#organize-the-list) 中使用 `Ctrl+X` 两次或使用 [`claude rm`](#manage-sessions-from-the-shell) 删除会话。除了下面保留的情况外，会话离开列表。其记录通过 `claude --resume` 保留在您的机器上，移除在主管重新启动后存活。

Claude 为会话创建的 worktree 会发生什么：

* Agent 视图移除它，包括未提交的更改，因此首先提交您想保留的内容。
* `claude rm` 在它有未提交的更改时保留它，以及会话行。
* Agent 视图和 `claude rm` 都不会移除另一个运行中的会话正在使用或已锁定的 worktree，再次删除不会改变这一点。Claude Code 保留 worktree 和会话，并命名保留的目录和原因；在 agent 视图中，会话的行显示 `not deleted`。关闭另一个会话，然后再次删除。
* 当您删除其 worktree 有 Claude Code 无法确认保存在其他地方的提交的会话时，Claude Code 保留 worktree 和会话，消息命名 worktree 的分支和有多少未推送的提交。消息还提供两种前进方式：推送提交或再次删除以丢弃它们。

  远程上的提交不会阻止删除。本地副本上的提交也不会，您的 `origin` 远程的默认分支，只要该分支在您的主检出中检出，存储库目录本身而不是 worktree。

  在该拒绝后，您选择：

  * 要保留提交，推送它们或将它们合并到该默认分支，然后再次删除会话。
  * 要丢弃它们，再次删除会话而不推送：在 agent 视图中的其行上按 `Ctrl+X` 两次，或运行拒绝打印的 `claude rm <id> --discard-unpushed` 命令。这移除会话和 worktree 及其分支，丢弃未推送的提交和任何未提交的更改。

  当您再次删除时，Claude Code 仅丢弃拒绝显示的内容：如果 worktree 自那以后获得了提交，Claude Code 再次保留它并显示更新的状态。

  当另一个已完成的会话的记录也命名 worktree 时，它在您再次删除时保留；推送提交，然后再次删除。
* git 不再识别的 worktree，例如在 `git worktree prune` 后，不会阻止删除。Claude Code 删除会话并将目录留在磁盘上。
* 当 git 或您的 [`WorktreeRemove` hook](/docs/zh-CN/hooks#worktreeremove) 无法移除 worktree 时，Claude Code 保留 worktree 和会话，消息命名原因。对于 hook，消息说它如何结束，例如 `exited 1`，并引用其 stderr 的开始。消息还告诉您接下来要做以下哪一个：

  * 再次删除会话以无论如何移除目录，通过在 agent 视图中的其行上按 `Ctrl+X` 两次或运行 `claude rm` 拒绝打印的 `claude rm <id> --force-remove-worktree <worktree-id>` 命令。Worktree 的分支保留在存储库中。

    Claude Code 仅在可以确认以下所有内容时提供此选项：

    * 目录是存储库在 `.claude/worktrees/` 下的链接 worktrees 之一
    * Worktree 和检出的子模块都没有对跟踪文件的未提交更改
    * 没有其他会话的记录命名它

    当 Claude Code 无法验证子模块检出的状态时，例如被单独的 git 存储库替换的，它也不提供此选项。
  * 修复阻碍的内容，例如提交或隐藏未提交的更改、将单独的 git 存储库移出 worktree、关闭使用目录的任何内容或修复 hook，然后再次删除会话。
  * 自己移除目录，然后再次删除会话。

您自己创建并在其内启动会话的 worktree 无论如何都会保留。

其 worktree 目录不属于任何 git 存储库的会话，因为存储库被删除或 [`WorktreeCreate` hook](/docs/zh-CN/hooks#worktreecreate) 在其他地方创建了目录，仍然可以删除。当目录中仍有文件时：

* Agent 视图在丢弃它们前要求相同的 `Ctrl+X` 双按。对于 hook 创建的目录，它运行您的 [`WorktreeRemove` hook](/docs/zh-CN/hooks#worktreeremove)，没有一个它拒绝删除并保留会话。
* `claude rm` 保留会话和 worktree，并命名原因。

任一路径保留另一个已完成的会话的记录命名的目录。

<h3 id="set-the-model">
  设置模型
</h3>

agent 视图标题中显示的模型名称是分派默认值。您从输入启动的新会话使用此模型，它来自您的用户设置中的 [`model` 设置](/docs/zh-CN/settings-reference#model)。通过在 [`/model` 选择器](/docs/zh-CN/model-config) 中选择模型或直接编辑设置来设置它。

要为整个 agent 视图会话覆盖分派默认值，在打开 agent 视图 时传递 `--model`。请参阅 [Permission mode, model, and effort](#permission-mode-model-and-effort)。

要从 agent 视图内更改分派默认值，在分派输入中输入 `/model` 后跟模型名称并按 `Enter`。标题更新以显示该模型，带有 `(session)` 标记，您之后分派的会话使用它。输入 `/model default` 清除覆盖并返回分派默认值。此覆盖持续当前 `claude agents` 运行的其余部分，不写入您的设置文件。以下示例在 Opus 上分派一个会话，在 Sonnet 上分派下一个：

```text theme={null}
/model opus
refactor auth
/model sonnet
run the test suite
```

每个后台会话可以在不同的模型上运行。要为一个会话覆盖它：

* 从 shell，使用 `claude --bg` 传递 `--model`。
* 附加到运行中的会话并运行 `/model` 以切换：从选择器中选择或输入 `/model <name>` 保存为您的新会话默认值，除非您在选择器中按 `s` 进行仅会话切换。仅会话切换在会话重新生成时持续。
* 分派其 frontmatter 设置 `model` 字段的 [subagent](/docs/zh-CN/sub-agents)。

<h3 id="permission-mode-model-and-effort">
  权限模式、模型和努力
</h3>

后台会话从您分派它的位置和方式获取其设置、提供者、权限模式、模型和努力。下面的小节涵盖每个来源，以及主管重新启动会话时持续的内容。

<h4 id="settings-and-provider">
  设置和提供者
</h4>

后台会话从它运行的目录读取其 [settings](/docs/zh-CN/settings)，与您在该目录启动 `claude` 时相同，使用 [它继承的配置标志](#what-carries-over-when-you-background)。这包括项目设置中的 [`env` 值](/docs/zh-CN/settings-reference#env)，因此在那里设置的 `ANTHROPIC_MODEL` 或提供者变量适用于该目录中的每个后台会话。

后台会话也使用您分派它的 shell 的 `PATH` 运行，因此它运行的命令找到与您的终端相同的工具。它也保留该 shell 的云提供者选择，例如 `CLAUDE_CODE_USE_BEDROCK` 或 `CLAUDE_CODE_USE_VERTEX`，以及其 `ANTHROPIC_DEFAULT_*_MODEL` 别名和您在那里导出的任何 [`CLAUDE_CODE_EXTRA_BODY`](/docs/zh-CN/env-vars) 覆盖。

<h4 id="llm-gateway">
  LLM gateway
</h4>

如果您通过 [LLM gateway](/docs/zh-CN/llm-gateway) 路由 Claude Code，将 gateway 变量放在设置文件的 `env` 块中，而不是在您的 shell 中导出它们，后台会话与其余设置一起读取它们。[Set in a settings file](/docs/zh-CN/llm-gateway-connect#set-in-a-settings-file) 显示块和要使用哪个设置文件作为凭证。

如果您仅在 shell 中导出 gateway `ANTHROPIC_BASE_URL`，它到达后台会话，以及您与它导出的 `ANTHROPIC_CUSTOM_HEADERS` 和凭证，仅当 [supervisor](#the-supervisor-process) 本身从导出相同 gateway 的 shell 启动时，仅在这些情况下：

* 您使用 `←` 或 `/background` 后台处理您自己的会话
* 您分派会话到您所在的目录
* 您通过附加或回复来唤醒您所在目录中的停止会话

Claude Code 在云提供者前转发 gateway。如果您分派的 shell 选择提供者并使用其 auth-bypass 标志导出其 gateway 端点，Claude Code 在适用于 `ANTHROPIC_BASE_URL` 的条件下转发端点和标志对，以及 `ANTHROPIC_CUSTOM_HEADERS`。例如，导出 `CLAUDE_CODE_USE_VERTEX=1` 与 `ANTHROPIC_VERTEX_BASE_URL` 和 `CLAUDE_CODE_SKIP_VERTEX_AUTH=1`，Claude Code 转发该端点和标志。

Claude Code 仅将转发的 gateway 应用于该会话的运行进程，永远不写入磁盘。

<h4 id="permission-mode">
  权限模式
</h4>

[permission mode](/docs/zh-CN/permissions) 取决于您如何启动会话：

* **使用 `/bg` 或 `←` 后台处理**：Claude Code 保留会话所在的权限模式，因此您切换到 `acceptEdits` 或 `auto` 的模式在分离后保留在那里
* **从使用 `←` 打开的 agent 视图分派**：目标自己的配置优先，您来自的会话的权限模式在没有其他设置时适用
* **从 shell 中启动的 `claude agents` 或使用 `claude --bg` 分派**：新会话以新 `claude` 会话在该目录中的方式启动，除非您从使用 [dispatch defaults](#dispatch-defaults) 打开的 agent 视图分派。[Which permission mode a session starts in](/docs/zh-CN/permission-modes#which-mode-a-session-starts-in) 列出顺序

对于您从使用 `←` 打开的 agent 视图分派的会话，Claude Code 从适用的第一个中获取权限模式：

1. 目标目录的 [`permissions.defaultMode`](/docs/zh-CN/settings-reference#permissions-defaultmode)。两个源规则适用：
   * `auto` 和 `bypassPermissions` [仅从托管设置、`--settings` 文件或 `~/.claude/settings.json` 生效](/docs/zh-CN/settings-reference#permissions-defaultmode)。
   * Claude Code 拒绝来自项目的 `.claude/settings.json` 或 `.claude/settings.local.json` 的 `defaultMode`，选择比您来自的会话所在的权限模式更宽松的模式。
2. 您来自的会话的权限模式

当 Claude Code 拒绝源的模式为过于宽松时，列表中的下一个源决定。例如，如果您从计划模式会话分派到其检入的设置要求 `acceptEdits` 的目录，新会话在计划模式中启动。如果您将该 `defaultMode` 移到 `~/.claude/settings.json`，它无论您来自的会话的权限模式如何都适用。

宽松性运行计划，然后手动和 `dontAsk`，然后 `acceptEdits` 和 auto，每个计为比另一个更宽松，然后 `bypassPermissions`。

<h4 id="dispatch-defaults">
  分派默认值
</h4>

要为您从 agent 视图分派的每个会话设置默认值，在打开它时传递 `--permission-mode`、`--model`、`--effort` 或 `--agent` 中的任何一个：

```bash theme={null}
claude agents --permission-mode plan --model opus --effort high
```

`--effort` 这里接受与 [top-level `--effort` 标志](/docs/zh-CN/cli-reference#cli-flags) 相同的值，包括 `ultracode`。

`--agent` 设置当分派提示不命名一个时使用的 [subagent](/docs/zh-CN/sub-agents)，要么使用 `@name` 要么作为第一个单词。它默认为 [`agent` 设置](/docs/zh-CN/settings-reference#agent)（如果设置了），否则为内置的 catch-all `claude` agent。在分派输入中命名 subagent 覆盖两者。

`claude agents` 也接受 `--dangerously-skip-permissions` 作为 `--permission-mode bypassPermissions` 的简写，和 `--allow-dangerously-skip-permissions` 使 `bypassPermissions` 在每个分派会话的 `Shift+Tab` 循环中可用，而不在该模式中启动。两者都匹配 [top-level CLI flags](/docs/zh-CN/cli-reference)。

传递 `--restricted` 以在 [restricted mode](/docs/zh-CN/cli-reference#cli-flags) 中启动您从视图分派的每个会话，就像每个都使用 top-level `--restricted` 标志启动一样。需要 Claude Code v2.1.248 或更高版本。

活跃的默认值出现在分派输入下方的页脚中。

Claude Code 拒绝 `claude --bg --permission-mode bypassPermissions` 直到您通过运行 `claude --dangerously-skip-permissions` 一次交互式接受 bypass 免责声明，因为该模式让您不观看的会话无需批准即可行动。将 `--dangerously-skip-permissions` 或 `--permission-mode bypassPermissions` 传递给 `claude agents` 在您之前未接受时显示相同的免责声明，接受将 `bypassPermissions` 应用于您从视图启动的会话。传递 `--allow-dangerously-skip-permissions` 也显示相同的免责声明，接受使 `bypassPermissions` 在这些会话的 `Shift+Tab` 循环中可用，而不在其中启动它们。

<h4 id="what-persists-across-restarts">
  跨重新启动持续的内容
</h4>

您为后台会话选择的权限模式、模型和努力，以及 [它继承的配置标志](#what-carries-over-when-you-background)，在主管稍后 [停止并重新启动](#the-supervisor-process) 其进程时都持续。您使用 `claude --bg --dangerously-skip-permissions` 或 `claude --bg --permission-mode bypassPermissions` 启动的会话在该重新启动后保留在 `bypassPermissions` 中。您在会话中期使用 `/model` 或 `/effort` 更改的模型或努力也保留。

如果会话从您的设置而不是从 `--effort` 或 `/effort` 获取其努力，Claude Code 每次为会话启动进程时都会再次读取您的设置。在您编辑 `settings.json` 中保存的努力后，更改到达您使用 `←` 或 `/bg` 后台处理的会话，及其稍后的重新启动。保存的努力是 [`effortLevel`](/docs/zh-CN/settings-reference#effortlevel) 键或 [`modelSettings`](/docs/zh-CN/settings-reference#modelsettings) 条目。

Claude Code 也保留您使用 [`/rename`](/docs/zh-CN/commands) 或 `Ctrl+R` 设置的名称跨该重新启动，因此您仍然可以运行 [`claude --resume <name>`](/docs/zh-CN/sessions#name-your-sessions) 到达会话。

您使用 [`Ctrl+S`](/docs/zh-CN/interactive-mode#general-controls) 在附加时隐藏的提示与会话一起保留。在其进程停止或重新启动后重新打开会话，`Ctrl+S` 恢复隐藏的文本。隐藏内容中的粘贴内容不会在重新启动中存活。

<h3 id="settings-plugins-and-mcp-servers">
  设置、plugins 和 MCP 服务器
</h3>

Agent 视图接受与 `claude` 相同的配置标志以加载设置、plugins、MCP 服务器和其他目录。Agent 视图将 `--settings`、`--setting-sources` 和 `--plugin-dir` 应用于自己，并将每个配置标志传递给您从它分派的会话，因此您以这种方式加载的 plugin 或 MCP 服务器在这些会话中可用。

| 标志 | 效果 |
| :- | :- |
| [`--settings <file-or-json>`](/docs/zh-CN/settings) | 覆盖 agent 视图和分派会话的设置 |
| [`--setting-sources <sources>`](/docs/zh-CN/cli-reference#cli-flags) | 仅加载命名的设置源，在 agent 视图和分派会话中 |
| [`--add-dir <path>`](/docs/zh-CN/permissions#additional-directories-grant-file-access-not-configuration) | 授予对其他目录的文件访问权限 |
| [`--plugin-dir <path>`](/docs/zh-CN/plugins/create#load-a-directory-or-archive-for-one-session) | 从本地目录加载 plugin |
| [`--mcp-config <file-or-json>`](/docs/zh-CN/mcp) | 从配置文件或 JSON 字符串加载 MCP 服务器 |
| `--strict-mcp-config` | 仅使用来自 `--mcp-config` 的 MCP 服务器，忽略其他 MCP 配置。请参阅 [Exclusive control with managed-mcp.json](/docs/zh-CN/managed-mcp#exclusive-control-with-managed-mcp-json) 了解标志在托管 MCP 文件下的作用 |

每个值重复 `--add-dir`、`--plugin-dir` 或 `--mcp-config` 一次。`claude agents` 不支持空格分隔的形式，例如 `--add-dir a b c`。

您可以在 `agents` 前或后放置 `--settings`、`--setting-sources` 和 `--plugin-dir`。将 `--add-dir` 和 `--mcp-config` 保留在 `agents` 后：如果您在 `agents` 前放置任何一个，[`claude agents --json`](#manage-sessions-from-the-shell) 失败，出现 `unknown option` 错误。

以下示例使用设置覆盖和一个额外目录打开 agent 视图：

```bash theme={null}
claude agents --settings ./ci-settings.json --add-dir ../shared-lib
```

`--settings` 接受文件路径或内联 JSON 字符串。文件路径必须指向现有文件；如果不存在，Claude Code 以 `Settings file not found` 错误退出。

<h2 id="manage-sessions-from-the-shell">
  从 shell 管理会话
</h2>

每个后台会话有一个短 ID，你可以从 shell 使用。当你使用 `claude --bg` 启动会话时会打印该 ID，每个会话的 ID 是其在 `~/.claude/jobs/` 下的目录名。这些命令对于脚本编写或当你不想打开 agent view 时很有用。

| 命令 | 目的 |
| :- | :- |
| `claude agents` | 打开 agent view |
| `claude agents --cwd <path>` | 打开 agent view，范围限定为在 `<path>` 下启动的会话 |
| `claude agents --json` | 将会话打印为 JSON 数组并退出。参见 [将会话列为 JSON](#list-sessions-as-json) |
| `claude attach <id>` | 在此终端附加到会话 |
| `claude logs <id>` | 打印会话的最近输出 |
| `claude stop <id>` | 停止会话。也接受 `claude kill` |
| `claude respawn <id>` | 重新启动会话，运行中或已停止，例如用于获取更新的 Claude Code 二进制文件。重新启动的会话恢复其保存的对话；当磁盘上没有对话时，它会再次运行其原始提示作为新对话 |
| `claude respawn --all` | 重新启动每个运行中的会话，例如一次性将所有会话移至更新的 Claude Code 二进制文件 |
| `claude rm <id>` | 从列表中删除会话，以及 Claude 为其创建的 worktree（当安全删除时）；参见 [删除会话会删除什么](#what-deleting-a-session-removes)。对话记录保存在你的本地机器上，并且仍然可以通过 `claude --resume` 访问 |
| `claude rm <id> --discard-unpushed <commit>@<worktree-id>` | 删除因未推送提交而删除被拒绝的会话，丢弃 worktree 及其分支和提交。传递拒绝打印的确切值；参见 [删除会话会删除什么](#what-deleting-a-session-removes)。需要 v2.1.260 或更高版本 |
| `claude rm <id> --force-remove-worktree <worktree-id>` | 删除因 git 或 `WorktreeRemove` hook 无法删除其 worktree 而删除被拒绝的会话，无论如何删除 worktree 目录并在存储库中保留其分支。传递拒绝打印的确切值；参见 [删除会话会删除什么](#what-deleting-a-session-removes)。需要 v2.1.268 或更高版本 |
| `claude daemon status` | 打印 [supervisor](#the-supervisor-process) 的状态、版本、socket 目录和 worker 数量 |
| `claude daemon stop --any` | 停止 supervisor 进程及其托管的后台会话。传递 `--keep-workers` 以保持后台会话运行，以便下一个 supervisor 重新连接到它们。下一个 `claude agents` 或 `claude --bg` 启动一个新的 supervisor |

<h3 id="list-sessions-as-json">
  将会话列为 JSON
</h3>

`claude agents --json` 将活跃会话打印为 JSON 数组并退出：每个活跃会话，加上仍在工作或被阻止的后台会话，即使其进程已退出。添加 `--all` 以也包括已完成的后台会话，添加 `--cwd <path>` 以将列表限制为在该目录下启动的会话。

每个条目描述一个会话：

| 字段 | 出现时机 | 描述 |
| :- | :- | :- |
| `cwd`、`kind`、`startedAt` | 总是 | 工作目录、`interactive` 或 `background`，以及 Unix 毫秒为单位的启动时间 |
| `id` | 后台会话 | 短 ID，可与 `claude attach`、`claude logs` 和 `claude stop` 一起使用 |
| `state` | 后台会话 | `working`、`blocked`、`done`、`failed` 或 `stopped` 之一。参见 [从脚本读取会话状态](#read-session-state-from-a-script) 了解每个值的含义 |
| `pid`、`status` | 进程活跃时 | 进程 ID 和 `busy`、`waiting` 或 `idle` 之一 |
| `waitingFor` | 当 `status` 为 `waiting` 时 | 会话被阻止的原因：`permission prompt` 表示需要批准，`input needed` 表示来自 Claude 或 MCP 服务器的输入请求的问题，`sandbox request`、`worker request` 或 `dialog open` |
| `sessionId`、`name` | 当设置时 | `sessionId` 是完整的会话 UUID，可与 [`claude --resume`](/docs/zh-CN/sessions) 一起使用。交互式会话的 `name` 是其 [默认显示名称](/docs/zh-CN/sessions#name-your-sessions)，直到你命名会话或在其中接受计划 |

<h3 id="read-session-state-from-a-script">
  从脚本读取会话状态
</h3>

`claude agents --json` 是从 Claude Code 外部读取会话状态的受支持方式，例如从状态栏、调度程序或监督后台工作的另一个 Claude 会话。轮询 `claude agents --json --all`，它会继续列出进程已退出的会话，并读取每个条目的 `state`、`status` 和 `waitingFor`。

| `state` | 含义 |
| :- | :- |
| `working` | 一个回合正在运行，或会话在其自己驱动的工作步骤之间，例如 [`/loop`](/docs/zh-CN/scheduled-tasks) 迭代或对 CI 的等待。`status` 告诉你其进程现在是否 `busy` |
| `blocked` | 会话在等待你：它提出的问题、权限或沙箱决定、只有你能清除的错误（例如过期的登录），或如果你在没有提示的情况下启动它，则为其第一个提示。当等待是活跃进程中的开放提示时，`waitingFor` 会命名它 |
| `done` | 最后一个回合完成了你要求的内容，会话已准备好接收你的下一个提示，无论其进程是否仍然活跃 |
| `failed`、`stopped` | 任务以错误结束，或会话被停止 |

完成其回合并等待你的下一条指令的会话读取 `done`，而不是 `blocked`。`blocked` 总是意味着会话在继续之前需要你提供的东西。

`~/.claude/jobs/<id>/` 下的文件不是稳定的接口。会话或其他程序写入 `state`、`detail`、`tempo` 或 `needs` 的值会在下一次更新时被替换。

如果你想让会话用自己的话报告进度，让它写一个自己的文件，例如在 `$CLAUDE_JOB_DIR/tmp` 下，而不是编辑 `state.json`。

<h2 id="how-background-sessions-are-hosted">
  后台会话如何被托管
</h2>

Claude Code 将 agent view 中列出的每个会话都视为后台会话，无论你当前是否连接到它。相比之下，通过直接运行 `claude` 启动的会话与该终端绑定，并在终端关闭时结束，除非你[将其发送到后台](#from-inside-a-session)。

要检查你所在的会话类型，请运行 [`/status`](/docs/zh-CN/commands)。在后台会话中，`Session kind` 行显示 `background job · attached` 或 `background job · unattended`，具体取决于是否连接了终端，在任何其他会话中显示 `interactive`。

<h3 id="the-supervisor-process">
  监督进程
</h3>

监督进程是一个后台服务，运行你的后台会话，使其在你关闭 agent view 或终端后继续工作。Claude Code 在你第一次后台化会话或打开 agent view 时启动它，你不需要自己管理它。

每个会话都是监督进程下的自己的 Claude Code 进程，该进程发生的情况取决于会话的状态：

* **工作中、暂停在权限提示或其他对话上，或已连接**：进程继续运行。运行中的子代理、工作流或监视器计为工作中。
* **已完成或等待你的下一条消息，且未连接约一小时**：监督进程停止该进程以释放资源。以向你提问结束其轮次的会话计为等待你的下一条消息。对话保存在磁盘上，下次你连接或回复时，会话从中断处恢复。使用 `Ctrl+T` 固定会话以保持其进程运行。
* **在监督进程运行时意外退出**：监督进程重新启动该进程。使用 `←` 或 `/background` 后台化的会话（例如使用 `kill`）标记为已停止而不是重新启动。对于以关闭结束的会话，请参阅[会话在关闭后显示为失败或已停止](#sessions-show-as-failed-after-shutdown)。
* **自动更新后**：监督进程重新启动自身到新版本，并在后台移动空闲会话。工作中、等待你或已连接的会话不会被中断。

当会话的进程停止或重新启动时，Claude 在其中启动的后台 shell 命令、动态工作流和后台子代理会转移到其下一个进程；运行中的监视器和子代理启动的 shell 命令会随进程停止。删除会话会停止它转移的所有内容。要改为让所有内容随进程停止而不是转移，请将 [`CLAUDE_CODE_DISABLE_BG_EXIT_HANDOFF`](/docs/zh-CN/env-vars#variables) 设置为 `1`。

监督进程及其会话使用与你的交互式会话相同的存储凭证进行身份验证。关于哪些设置和 shell 变量到达会话（包括 `PATH`），请参阅[设置和提供商](#settings-and-provider)。关于网关端点，请参阅 [LLM 网关](#llm-gateway)。

<h3 id="where-state-is-stored">
  状态存储位置
</h3>

会话状态存储在你的 Claude Code 配置目录下。如果你设置了 [`CLAUDE_CONFIG_DIR`](/docs/zh-CN/env-vars)，监督进程使用该目录而不是 `~/.claude`，并作为单独的实例运行，具有其自己的会话。

| 路径 | 内容 |
| :- | :- |
| `~/.claude/daemon.log` | 监督进程日志 |
| `~/.claude/daemon/roster.json` | 运行中的后台会话列表，用于在重新启动后重新连接 |
| `~/.claude/jobs/<id>/state.json` | 在 agent view 中显示的每会话状态。通过 [`claude agents --json`](#read-session-state-from-a-script) 读取它，而不是解析文件 |
| `~/.claude/jobs/<id>/tmp/` | 每会话临时目录。Claude 的 `Write` 和 `Edit` 调用此处不会提示权限。会话删除时移除 |

每个后台会话都设置了 `CLAUDE_JOB_DIR` 环境变量指向其 `~/.claude/jobs/<id>` 目录，因此会话运行的 shell 命令可以将临时文件写入 `$CLAUDE_JOB_DIR/tmp` 而不会与并行会话冲突。

要在不直接读取文件的情况下检查此状态，请运行 `claude daemon status`。它报告监督进程是否可达、其进程 ID 和版本、套接字目录以及有多少后台会话处于活跃状态。

该命令还会在运行的监督进程版本与你调用的 `claude` 版本不同时发出警告，这发生在监督进程尚未重新启动到新版本的更新之后。警告显示两个版本，并告诉你运行 `claude daemon stop --any` 以获取新版本。当 Claude Code 作为操作系统服务安装时，建议的命令是 `claude daemon stop` 不带该标志。

会话完整地保留该版本不匹配：更新会话 `state.json` 的较旧 Claude Code 版本会保留它不识别的字段并保持会话列出。`roster.json` 中的会话列表遵循相同的规则，因此由较新版本启动的会话保持可达并在监督进程重新启动后继续接受输入。

<h3 id="turn-off-agent-view">
  关闭 agent view
</h3>

要完全关闭后台代理和 agent view，将 `disableAgentView` [设置](/docs/zh-CN/settings)设为 `true` 或设置 `CLAUDE_CODE_DISABLE_AGENT_VIEW` 环境变量。管理员可以通过[托管设置](/docs/zh-CN/managed-settings)强制执行这个。

<h2 id="troubleshooting">
  Troubleshooting
</h2>

<h3 id="claude-agents-lists-subagents-instead-of-opening-agent-view">
  `claude agents` 列出子代理而不是打开代理视图
</h3>

如果 `claude agents` 打印一个计数，然后是您配置的子代理，然后退出，说明代理视图在您的环境中不可用。运行 `claude update` 来安装最新版本。

如果更新后代理视图仍然没有打开，请检查它是否已被设置或环境变量[关闭](#turn-off-agent-view)。

<h3 id="agent-view-opens-with-no-sessions">
  代理视图打开时没有会话
</h3>

在您分派第一个会话之前，代理视图显示空的部分标题，每个标题下有一个描述，以及在输入上方有一行说明，代替会话列表。在底部的输入中输入提示，然后按 `Enter` 来分派您的第一个会话。

<h3 id="backgrounding-shows-a-background-this-session-dialog">
  后台处理显示 `Background this session?` 对话框
</h3>

如果您按 `←` 来后台处理当前会话，而 Claude Code 显示 `Background this session?` 对话框，说明该会话有正在进行的工作，后台处理会停止、重新启动或让其无人值守地运行，Claude Code 在执行这些操作之前会询问：

* **无法移动的工作**：该会话有无法移动到后台会话的工作，例如正在运行的[监视器](/docs/zh-CN/tools-reference#monitor-tool)。对话框命名 Claude Code 会停止的工作，并分别计算转移的任务数。
* **具有运行子代理的工作流**：[动态工作流](/docs/zh-CN/workflows)仍然有子代理在运行。工作流本身会转移，但其运行的子代理从头开始重新启动，对话框会说明有多少个。
* **自动工件回复**：Claude [自动回复工件上的评论](/docs/zh-CN/artifacts#let-claude-reply-to-comments-on-its-own)。这些回复在后台会话中继续，对话框会说明这一点。

运行 `/tasks` 来查看正在运行的所有内容，然后确认后台处理或选择 `Stay` 来让工作先完成。请参阅[后台处理时转移的内容](#what-carries-over-when-you-background)，了解哪些类型的工作会转移，哪些 Claude Code 会停止。

<h3 id="prompt-rejected-as-too-short">
  提示被拒绝为过短
</h3>

分派输入期望一个任务描述，而不是对话开场白。短于四个字符的提示会被拒绝，并显示 `Too short` 提示，以防止误触发启动会话。描述您希望会话执行的操作，例如 `investigate the flaky checkout test`。

<h3 id="sessions-show-as-failed-after-shutdown">
  会话在关闭后显示为失败或已停止
</h3>

关闭或重新启动您的机器会停止运行的后台会话。等待您输入的会话在您返回时仍会显示在 `Needs input` 下。对于任何其他运行的会话，代理视图显示的内容取决于它上次取得进展的时间：

* 在 48 小时内，会话显示为失败。附加或回复它，它会从中断的地方重新启动。
* 超过 48 小时，例如机器关闭数天后，会话显示为已停止，并显示 `ended while the background service was off`。在该行上按 `Enter`，页脚会显示 `Press enter again to resume this session (it ended while the background service was off), or ctrl+x to delete it.` 在同一行上再次按 `Enter` 来恢复其保存的对话。回复或 `claude attach <id>` 会在没有该页脚提示的情况下恢复它。

当[转录清理](/docs/zh-CN/settings-reference#cleanupperioddays)删除了已停止会话的保存对话时，Claude Code 拒绝打开该行：消息说没有可恢复的内容。`claude rm <id>` 删除该行，除了[保留的情况](#what-deleting-a-session-removes)中描述的情况，`claude respawn <id>` 再次运行其原始提示。请参阅[此会话的保存对话不再在磁盘上](/docs/zh-CN/errors#this-sessions-saved-conversation-is-no-longer-on-disk)。

仅睡眠不会停止会话。会话在睡眠中被保留，主管在唤醒时重新连接到它们。

<h3 id="opening-a-session-says-the-conversation-is-already-open">
  打开会话说对话已经打开
</h3>

两个进程不能写入同一个转录。当已停止会话的保存对话已在另一个活跃的 Claude Code 进程中打开时，Claude Code 拒绝启动该会话自己的进程。您看到的内容取决于什么持有对话：

* 您恢复对话的终端，例如使用 `claude --resume` 或 `/resume`：该行显示 `Open in a terminal`，并提示在那里继续，打开该行显示 `Can't open — this session is running in another terminal`。在该终端中继续，或退出它并再次打开该行。
* 另一个非交互式 Claude Code 进程，例如同一对话的后台会话进程，尚未退出：打开该行显示 `This conversation is already open in another running Claude session`。使用该进程，或等待它退出并再次打开该行。

Claude Code 保存您在拒绝的尝试中输入的回复，并在会话下次启动时发送它。

<h3 id="opening-a-session-says-it-has-no-saved-transcript">
  打开会话说它没有保存的转录
</h3>

已停止的会话[从另一个对话后台处理](#from-inside-a-session)并在其第一个响应完成之前停止，没有任何可恢复的内容：在该第一个响应完成之前，对话仍然只存在于它被后台处理的会话中。`claude attach` 拒绝打开它，显示 `This session has no saved transcript`。

在代理视图中，打开该行在列表下显示 `Press enter again to restart this session fresh`。在同一行上再次按 `Enter` 来使用空对话重新启动会话，或从 shell 运行 `claude respawn <id>`。

原始对话完整无损；使用 `claude --resume` 恢复它或继续在其中工作。有关详细信息，请参阅[错误参考](/docs/zh-CN/errors#this-session-has-no-saved-transcript)。

<h3 id="the-terminal-host-died-or-the-session-stopped-responding">
  终端主机已死亡或会话停止响应
</h3>

[主管](#the-supervisor-process)在其自己的主机进程中运行每个后台会话的终端。当该进程死亡或停止响应时，Claude Code 显示原因并提供重新启动；在两种情况下，对话都被保存，重新启动会恢复它。[错误参考](/docs/zh-CN/errors#terminal-host-process-died)引用完整消息。

Claude Code 永远不会重新启动运行[shell 命令](#run-a-shell-command)的行，无论是从 `Enter` 还是从 `claude attach`，因为那样会再次运行该命令；该行的消息和 `claude attach` 都说该命令不会再次运行。

<h4 id="terminal-host-died">
  终端主机已死亡
</h4>

在 Linux 和 WSL 上，主管每隔几秒检查一次每个主机进程，无论您是否打开会话，当进程已退出但其与主管的连接从未关闭时，将会话标记为失败。

* 在代理视图中，该行显示 `terminal host process died — press Enter to restart`。在它上面按 `Enter`，Claude Code 在新的主机进程上重新启动会话。
* 从 shell，`claude attach <id>` 重新启动已标记为失败的会话。否则它报告原因并退出，告诉您运行 `claude attach <id>`。

<h4 id="session-isn’t-responding">
  会话没有响应
</h4>

当主管接受打开但约十秒内没有输出到达时，Claude Code 结束尝试并提供重新启动。仅仅停滞的会话，例如跨机器睡眠，不会达到此提议：主管[在打开时自己重新启动它](#read-session-state)。

* 在代理视图中，页脚显示 `Press enter again to restart this session — it isn't responding (its conversation is saved and resumes).` 在同一行上再次按 `Enter`，Claude Code 停止无响应的进程并重新启动会话；没有第二次按下，它不会停止任何内容。
* 从 shell，`claude attach <id>` 报告原因并退出，告诉您运行 `claude stop <id>`，然后 `claude attach <id>`。

<h3 id="a-session-fails-before-starting-with-a-possibly-low-memory-note">
  会话在启动前失败，并显示 `possibly low memory` 注释
</h3>

当后台会话的进程在完成启动之前退出，且主机内存不足时，该行的状态命名退出并添加 `possibly low memory — free some up and retry`。

该注释是一个假设，而不是确认的原因。Claude Code 仅在进程无声退出时添加它，没有写入错误，也没有被信号停止，且主机在那一刻报告内存不足。当进程在退出前确实写入了错误时，该行显示该错误。

释放机器上的内存，然后附加或回复该行，主管为会话启动新进程。当内存保持不足时，主管也会[停止空闲会话](#the-supervisor-process)来自行释放资源，如果停止其他会话没有释放任何内容，也会停止空闲的固定会话。

<h3 id="agent-view-says-the-background-service-did-not-respond">
  代理视图说后台服务没有响应
</h3>

如果附加、查看或 `claude logs` 报告后台服务没有响应，主管进程可能已停滞。停止它并让下一个 `claude agents` 启动新的。要在重新启动期间保持后台会话运行，请传递 `--keep-workers`：

```bash theme={null}
claude daemon stop --any --keep-workers
```

新的主管重新连接到运行的会话。没有 `--keep-workers`，该命令也会结束后台会话。`--any` 标志确认您想停止按需启动的主管，而不是作为已安装的服务，这是默认值。

启动但无法接受连接的主管会自行退出并释放其锁，所以下一个 `claude agents` 会启动新的，无需此手动停止。上述步骤适用于运行的主管停滞的情况。

如果该命令改为退出，说记录的进程无法验证为主管，请检查报告的进程 ID：如果它是您拥有的主管，自己停止它，然后删除 `~/.claude/daemon.lock`，以便下一个 `claude agents` 启动新的。

在 Windows 上，如果主管不响应停止请求，该命令会打印其进程 ID。使用 `taskkill /PID <pid>` 结束该进程以完成恢复。当您传递 `--keep-workers` 时，后台会话仍然被保留。

<h3 id="dispatch-fails-with-could-not-resolve-authentication-method">
  分派失败，显示 `Could not resolve authentication method`
</h3>

如果后台分派失败，显示 `Could not resolve authentication method`，而交互式会话正常进行身份验证，接收分派的工作人员没有获取凭据。后台会话从[主管](#the-supervisor-process)获取其凭据，所以此错误意味着主管进程本身没有可用的存储凭据。确认您已运行 `/login` 或配置了 API 密钥，然后停止主管：

```bash theme={null}
claude daemon stop --any --keep-workers
```

下一个 `claude agents` 或 `claude --bg` 启动读取您存储凭据的新主管。如果您使用环境变量（如 `ANTHROPIC_API_KEY`）而不是 `/login` 进行身份验证，请从设置了该变量的 shell 运行该下一个命令。

有关原因和修复的完整列表，请参阅[错误参考](/docs/zh-CN/errors#could-not-resolve-authentication-method)。

<h3 id="background-sessions-can’t-read-desktop-documents-or-downloads-on-macos">
  后台会话无法在 macOS 上读取 Desktop、Documents 或 Downloads
</h3>

在 macOS 上，后台会话主机作为其自己的进程运行，并与您的终端分别请求对受保护文件夹的访问。如果后台会话在读取 `~/Desktop`、`~/Documents`、`~/Downloads` 或其他受保护位置时报告 `Operation not permitted`，请在系统设置中的隐私和安全 > 文件和文件夹下授予访问权限，或为该条目启用完全磁盘访问。

使用本机安装程序，该条目显示为 Claude Code，授予在更新中持续。使用其他安装方法（如 Homebrew 或 npm），该条目显示二进制路径，更新后可能需要再次授予。

<h3 id="background-sessions-can’t-reach-local-network-hosts-on-macos">
  后台会话无法在 macOS 上访问本地网络主机
</h3>

在 macOS 15 及更高版本上，系统会阻止进程访问本地网络上的设备，直到您授予本地网络权限，因此针对 LAN 地址的命令可能在后台会话中失败，显示 `connect: no route to host`，即使它在前台终端中有效。后台会话中连接到本地网络地址的第一个命令会触发 Claude Code 的 macOS 本地网络权限提示。授予一次，这些命令就能像在前台终端中一样访问 LAN 主机。

<h3 id="a-session-is-slow-to-respond-after-attaching">
  附加后会话响应缓慢
</h3>

当已完成或等待您下一条消息的会话保持未附加约一小时时，主管停止其进程以释放资源。附加从中断的地方启动新进程，并在进程重新启动时立即切换到会话。正在工作、暂停在权限提示或其他对话上的会话，或[固定](#organize-the-list)的会话不会以这种方式停止，所以使用 `Ctrl+T` 固定会话以保持其响应性。

进程启动时，Claude Code 显示会话转录的尾部，格式化为实时会话呈现的方式，带有 markdown、突出显示的代码块和工具调用作为暗淡的行，上方是带有 `Session is starting` 注释的暗淡提示区域。实时会话在准备好后立即替换它。

<h3 id="claude/worktrees/-is-filling-up">
  `.claude/worktrees/` 正在填满
</h3>

在代理视图中删除会话会删除 Claude 为其创建的 worktree，但[某些删除会保留 worktree 或在磁盘上留下其目录](#what-deleting-a-session-removes)，所以剩余目录可能会累积。Git 不再识别的目录不会出现在 `git worktree list` 中，所以手动删除这些目录。

在项目目录中使用 `git worktree list` 列出剩余条目，并使用 `git worktree remove <path>` 删除每一个。请参阅[清理 worktrees](/docs/zh-CN/worktrees#clean-up-worktrees)。

<h2 id="limitations">
  限制
</h2>

Agent view 处于研究预览阶段，存在以下限制：

* **速率限制适用**：后台会话消耗你的订阅使用量，与交互式会话相同，因此并行运行十个代理的配额消耗速度大约是运行一个代理的十倍。
* **会话是本地的**：后台会话在你的机器上运行。它们在机器睡眠时保留，但在机器关闭时停止。
* **Claude 创建的 worktrees 在 agent view 中随会话删除**：在删除在其自己的 worktree 中编辑文件的会话之前，请提交更改。[某些删除会保留 worktree](#what-deleting-a-session-removes)。

<h2 id="related-resources">
  相关资源
</h2>

有关以并行方式运行 Claude 的其他方法，以及在运行的会话之间传递发现的方法，请参阅：

* [并行运行代理](/docs/zh-CN/agents)：比较 agent view 与 subagents、agent teams 和 worktrees
* [跨会话消息传递](/docs/zh-CN/cross-session-messaging)：让您的会话相互传递发现
* [Agent teams](/docs/zh-CN/agent-teams)：协调相互发送消息的多个会话
* [在云端使用 Claude Code](/docs/zh-CN/claude-code-on-the-web)：在托管的云环境中运行会话而不是本地
* [Projects](/docs/zh-CN/claude-projects)：让 Claude 从一个对话中协调并行云会话，并告诉您哪些需要您

<h2 id="version-history">
  版本历史
</h2>

Agent view 在研究预览期间发展迅速。如果你使用较旧的 Claude Code 版本，本页上的某些行为可能会有所不同；特别是，`claude agents` 拒绝它尚不支持的标志，出现 `unknown option` 错误。下表列出了何时添加每个标志和行为。

| 版本 | 更改 |
| - | - |
| v2.1.281 | [`--setting-sources`](/docs/zh-CN/cli-reference#cli-flags) 限制[转移](#what-carries-over-when-you-background)到你使用 `←` 或 `/bg` 后台的会话，以及你从 agent view 调度的会话。在此版本之前，生成的会话加载每个设置源。 |
| v2.1.281 | `claude --bg` 和重启会话的命令首先检查会话目录的工作区信任。从该目录中的终端，如果你尚未接受，[信任对话框出现](#from-your-shell)；在无法出现对话框的地方，例如在脚本中，命令以 [`Workspace not trusted`](/docs/zh-CN/errors#workspace-not-trusted-when-dispatching-a-background-session) 错误退出。 |
| v2.1.274 | 自动更新后，你离开约一小时的 agent view 可以将自己重新启动到新的构建上。当它这样做时，它保留你打开它时的[调度默认值](#dispatch-defaults)：`--model`、`--effort`、`--permission-mode`、`--allow-dangerously-skip-permissions` 和 `--agent`。在此版本之前，重新启动的 view 仅保留 `--cwd` 和配置标志，例如 `--settings` 和 `--mcp-config`，所以你之后调度的会话启动时没有这些默认值。 |
| v2.1.274 | 当[删除被拒绝](#what-deleting-a-session-removes)因为 git 或你的 `WorktreeRemove` hook 无法删除 worktree 时，Claude Code 验证的已检出子模块没有对跟踪文件的未提交更改不会阻止再次删除的提议，并删除目录。已检出子模块内的未提交工作计为未提交更改，消息会命名子模块。在此版本之前，worktree 中的任何子模块检出都会阻止提议，消息说 worktree 包含嵌套存储库。 |
| v2.1.268 | 当[删除被拒绝](#what-deleting-a-session-removes)因为 git 或你的 `WorktreeRemove` hook 无法删除 worktree 时，消息会说明原因，包括 hook 如何结束以及其 stderr 的开始。对于位于存储库的 `.claude/worktrees/` 下的链接 worktree，没有对跟踪文件的未提交更改，其中没有嵌套存储库，也没有其他会话的记录命名它，再次删除会话会从 agent view 或使用 `claude rm <id> --force-remove-worktree <worktree-id>` 删除目录。在此版本之前，该行仅显示 `worktree could not be removed (WorktreeRemove hook failed)` 或 git 的错误，hook 的 stderr 仅进入调试日志，再次删除被以相同方式拒绝。 |
| v2.1.268 | 在第一个 `←` 显示 `Press ← again to open agents` 或在附加的会话中 `Press ← again to go back to agents` 后，[至少一秒后到达的第一次按压会切换](#switch-sessions-without-leaving-the-terminal)，即使中间更快的按压被忽略。在此版本之前，每次被忽略的按压都会重新启动等待，所以以稳定的速度再次按 `←` 直到你暂停超过一秒才会切换。 |
| v2.1.260 | 当你[后台会话](#from-inside-a-session)时，你的其他会话的[代理列表](/docs/zh-CN/cross-session-messaging#see-which-sessions-claude-can-reach)显示对话一次，作为其后台会话，它们对它的消息不再到达你移动它的终端。在此版本之前，该终端可能在 `claude agents --json` 中显示为对话名称下的第二个交互式会话，在移动前已向对话发送消息的会话继续传递到该终端。 |
| v2.1.260 | 当[删除因未推送的提交被拒绝](#what-deleting-a-session-removes)时，消息会说明 worktree 的分支以及有多少提交未推送，再次删除会话会丢弃 worktree 及其提交。在此版本之前，拒绝仅说 `worktree has commits that are not pushed anywhere`，再次删除被以相同方式拒绝，删除会话需要推送提交或手动删除 worktree。 |
| v2.1.257 | `←` [从附加的会话分离，即使 `/btw` 覆盖层打开](#attach-to-a-session)，甚至在回答中途，覆盖层在你下次附加时重新打开。在此版本之前，当覆盖层打开时 `←` 不分离。 |
| v2.1.257 | 当你运行 [`claude --resume <session-id> --bg`](#from-your-shell) 时，Claude Code 在其自己的 ID 下继续该会话，或在新 ID 下启动副本并打印 `note:` 行解释原因。`--continue`、裸 `--resume` 和带名称或路径的 `--resume` 启动具有相同注记的副本。在此版本之前，`--resume` 与 `--bg` 总是在新 ID 下启动副本且不说任何内容。 |
| v2.1.257 | 当你从使用 `←` 打开的 agent view 调度会话时，Claude Code 在[目标目录通过 `permissions.defaultMode` 配置](#permission-mode)的权限模式下启动它。当目录未设置时，你来自的会话的权限模式适用。在此版本之前，调度的会话总是在你来自的会话的权限模式下启动，覆盖它。 |
| v2.1.257 | agent view 中的 `Ctrl+S`、`Ctrl+T` 和 `Ctrl+G` [遵循你的 `keybindings.json`](#keyboard-shortcuts)：`Ctrl+S` 和 `Ctrl+T` 通过 `Agents` 上下文的 `agents:switchView` 和 `agents:togglePin` 操作，`Ctrl+G` 通过 `Chat` 上下文的 `chat:externalEditor` 绑定。在此版本之前，agent view 忽略 `keybindings.json`，这些键是固定的。 |
| v2.1.257 | 启动[后台服务](#the-supervisor-process)从两个失败原因恢复。在 macOS npm 安装上，自更新期间的启动[等待安装](/docs/zh-CN/errors#eacces-when-starting-a-background-session)而不是运行 npm 在替换二进制文件时放下的占位符。在 Windows 上，在机器上次启动前写入的陈旧 `daemon.lock`，或其记录的进程 ID 现在属于不同进程的，被替换。在此版本之前，macOS 启动在安装窗口期间失败，出现 `Error: claude native binary not installed.`，Windows 锁使每次启动都失败，出现 [`exited before it became reachable`](/docs/zh-CN/errors#background-service-exited-before-it-became-reachable)，直到你删除 `~/.claude/daemon.lock`。 |
| v2.1.257 | 当你在另一个 Claude Code 进程下载 npm 更新时打开或调度后台会话时，Claude Code [继续等待长达两分钟](/docs/zh-CN/errors#eacces-when-starting-a-background-session)，同时安装运行，然后失败，说 `Claude Code is being updated by npm on this machine`。在此版本之前，等待在十秒时停止，所以在下载仍在运行时打开失败，出现 `Couldn't start the background service`。 |
| v2.1.257 | 持有[跨会话消息](/docs/zh-CN/cross-session-messaging#control-inbound-messages)等待你批准的后台会话在其 `Needs input` 行上显示 `approve message from`，带有发送者的地址和发送者声称的名称。在此版本之前，该行移到 `Needs input` 但保留其前一个文本，所以 `claude agents` 中没有任何内容命名等待的消息或其发送者。 |
| v2.1.257 | 在打开的后台会话内使用 `Ctrl+S` 隐藏的提示[与会话一起保留](#what-persists-across-restarts)，所以 `Ctrl+S` 在会话的进程停止并再次启动后恢复它。在此版本之前，隐藏仅存在于运行的进程中，当会话空闲足够长时间使其进程停止时丢失，或当它停止然后重新打开时丢失。 |
| v2.1.251 | 在尚未[移入 worktree](#how-file-edits-are-isolated) 的后台会话中，Claude 和它生成的子代理可以编辑链接 git worktree 内的文件。 |
| v2.1.251 | Claude Code 转发在你调度的 shell 中导出的云提供商网关，例如 `ANTHROPIC_VERTEX_BASE_URL` 或 `ANTHROPIC_BEDROCK_BASE_URL` 及其身份验证绕过标志，到[会话的工作进程](#llm-gateway)，条件与 `ANTHROPIC_BASE_URL` 相同。在此版本之前，如果你仅通过此类网关进行身份验证后台或从 shell 调度，会话进行的每个请求都失败，因为端点和标志从其环境中删除。 |
| v2.1.251 | 当后台会话在另一个 Claude Code 进程刷新[插件市场](/docs/zh-CN/plugins/overview)时启动，例如运行[市场自动更新](/docs/zh-CN/plugins/install#keep-plugins-updated)的同级会话，Claude Code 保持该市场的插件可用。在此版本之前，此类会话可能启动时没有该市场的任何 skills、agents、hooks 和 MCP 服务器，并在整个运行期间保持这样。 |
| v2.1.248 | 在[调度输入](#keyboard-shortcuts)中 `Shift+Enter` 插入换行符，与主提示匹配，`Ctrl+Enter` 在 `?` 覆盖层列出 `ctrl+enter to start and open` 的终端中立即调度并附加。在此版本之前，`Shift+Enter` 调度并附加。 |
| v2.1.248 | [删除会话](#what-deleting-a-session-removes)在 worktree 的提交已经在你的 `origin` 远程的默认分支的本地副本上且你的主检出已检出该分支时成功；在此版本之前，删除被拒绝，出现 `has commits that are not pushed anywhere`。 |
| v2.1.248 | 使用 `←` 或 `/background` 后台的会话在运行时在其 worktree 上持有 [`git worktree lock`](/docs/zh-CN/worktrees#clean-up-subagent-and-background-session-worktrees)；在此版本之前，后台释放锁，清理或 `git worktree remove` 可以在运行的会话下删除 worktree。 |
| v2.1.248 | 未等待你的输入且在其最后活动后超过 48 小时被发现已死的后台会话，例如在机器关闭数天后，[显示为已停止](#sessions-show-as-failed-after-shutdown)，出现 `ended while the background service was off`，`Enter` 在它上面询问后恢复其保存的对话。在此版本之前，此类会话重新出现为新鲜失败，排序到列表顶部，单个 `Enter` 将数周前的对话拉入前台。 |
| v2.1.248 | 打开一个已停止的行，其对话[你在另一个终端中恢复](#opening-a-session-says-the-conversation-is-already-open)被拒绝，出现 `Can't open — this session is running in another terminal`，该行显示 `Open in a terminal` 而不是显示在 `Working` 下。在此版本之前，打开该行启动第二个进程写入相同的对话。 |
| v2.1.248 | 等待权限决定的后台会话，同时 `PermissionRequest` 或 `PreToolUse` hook 打印了无效答案[在其行上命名 hook 事件和架构错误](#peek-and-reply)。在此版本之前，该行仅显示待处理请求。 |
| v2.1.248 | 在 Windows 上，`claude agents` 在早期程序留在 win32-input-mode 的终端标签中启动时响应键盘。在此版本之前，Claude Code 没有解码此类标签发送的关键记录。 |
| v2.1.247 | 在 Linux 和 WSL 上，[其终端主机进程已死](#the-terminal-host-died-or-the-session-stopped-responding)的会话在几秒内失败，出现原因。没有输出的打开在约十秒后以重启提议结束，行上的 `Enter` 使用其对话重启会话；`claude attach <id>` 报告原因并退出。在此版本之前，打开此类会话无限期显示 `opening… · esc to cancel`，`claude attach <id>` 等待而不报告错误。 |
| v2.1.246 | 在 npm 安装上，当[后台服务](#the-supervisor-process)在 `npm install -g @anthropic-ai/claude-code` 替换二进制文件时启动失败时，Claude Code 等待长达十秒以完成安装并重试，然后报告 [`EACCES: permission denied`](/docs/zh-CN/errors#eacces-when-starting-a-background-session)。 |
| v2.1.246 | 当[后台服务](#the-supervisor-process)进程在打印错误后死亡时，Claude Code 报告失败并[引用服务的第一个错误行](/docs/zh-CN/errors#background-service-exited-before-it-became-reachable)。 |
| v2.1.246 | 如果你的机器在[后台服务](#the-supervisor-process)启动时睡眠，Claude Code 重试启动一次而不是失败。 |
| v2.1.246 | Claude Code 等待约两分钟而不是 45 秒以获得新启动的[后台服务](#the-supervisor-process)，该服务活跃但接受连接缓慢。 |
| v2.1.246 | [后台服务](#the-supervisor-process)从你的主目录启动，所以在 macOS 和 Linux 上已删除或移动的启动目录不再阻止启动。 |
| v2.1.246 | `/fork` [复制完整对话](#copy-the-session-with-%2Ffork)来自本身作为副本启动且未记录新提示的会话：你附加到的 `/fork` 副本、在 `←` 或 `/background` 将其移到后台后重新附加的会话，或使用 `claude --resume <id> --fork-session` 启动的会话。在此版本之前，如果你在此类会话中运行 `/fork` 然后向其发送新提示，Claude Code 打印正常确认但使用空对话启动副本。使用 `←` 或 `/background` 将此类会话移到后台以相同方式丢失对话。 |
| v2.1.246 | 当你打开刚调度的会话，同时其工作进程仍在启动时，例如通过按其行上的 `Enter`，Claude Code 等待进程然后附加。在此版本之前，如果你在进程仍在启动时按 `Enter`，Claude Code 可能停止会话，出现 [`Session <id> was stopped while the respawn was in flight`](/docs/zh-CN/errors#session-was-stopped-while-the-respawn-was-in-flight)。 |
| v2.1.246 | 当你[后台](#from-inside-a-session)一个命名的会话时，Claude Code 列出它一次，当你再次后台相同的对话时，它对新行的名称进行编号，例如 `my-session (2)`，现有行保留其名称。在此版本之前，你按 `←` 的终端可能在 `claude agents --json` 中显示为相同名称下的第二个会话，如果你再次后台相同的对话，Claude Code 在相同名称下添加另一行。 |
| v2.1.239 | 启用[vim 编辑器模式](/docs/zh-CN/interactive-mode#vim-editor-mode)时，在 agent view 的输入中按 `Esc` 从 INSERT 切换到 NORMAL 模式并保留你的文本，与主提示匹配；在 NORMAL 模式下，输入中仍有文本时，按 `Esc` 清除它，在空输入上按 `Esc` 退出，如[`Esc` 快捷键](#keyboard-shortcuts)描述。在此版本之前，`Esc` 清除输入。 |
| v2.1.233 | 对于链接到 GitLab 合并请求的会话，Claude Code 在 GitLab 的 `!1234` 参考语法中写入行的标签。你也可以将合并请求的 URL 粘贴到[调度输入](#filter-sessions)中以选择该会话。在此版本之前，标签呈现为 `#1234`，粘贴的合并请求 URL 仅在其第一个提示包含 URL 时与会话匹配。 |
| v2.1.227 | [删除会话](#what-deleting-a-session-removes)在另一个活跃的 Claude Code 会话在该 worktree 目录内运行时保留会话及其 worktree。Agent view 在行上显示 `not deleted` 和页脚中的原因，`claude rm` 打印 `kept <id>` 及原因，其命名另一个会话的进程 ID。在此版本之前，删除会话在另一个会话仍在其中工作时删除 worktree。 |
| v2.1.225 | 在你未信任的目录中 `claude agents` 显示与 `claude` 在启动时显示相同的[工作区信任对话框](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust)，在 agent view 打开之前。接受保存该工作区的信任；拒绝退出而不打开 agent view。在此版本之前，`claude agents` 打开而不询问，所以你从它调度的会话在你从未被要求信任的目录中运行。<br /><br />列表按目录分组时，将鼠标悬停在行上突出显示它而不改变[调度目标](#dispatch-to-a-specific-directory)；使用箭头键或点击选择行仍然改变目标。在此版本之前，将鼠标移到另一个项目中的会话上无声地改变下一个调度的会话启动的目录。 |
| v2.1.221 | `/status` 显示 `Session kind` 行：后台会话中的 `background job · attached` 或 `background job · unattended`，取决于是否附加了终端，任何其他会话中的 `interactive`。在此版本之前，`/status` 没有报告会话类型。<br /><br />`/fork`：Claude Code 指示[副本](#from-inside-a-session)隔离其工作与原始会话的：副本在进行代码更改前创建自己的 worktree，远离原始会话的 worktree，当其任务建立在该工作基础上时基于原始分支的新分支。查看链接部分了解确切条件。在此版本之前，副本没有收到隔离指令，可能最终编辑原始会话仍在工作的 worktree 或检出。<br /><br />启用[vim 编辑器模式](/docs/zh-CN/interactive-mode#vim-editor-mode)时，在使用 `u` 撤销提示回到空后立即按 `←` 要求与删除文本或通过提示历史移动相同的确认，仅在第二次按压时切换；在此版本之前按压立即切换。 |
| v2.1.219 | 启用[vim 编辑器模式](/docs/zh-CN/interactive-mode#vim-editor-mode)时，在空提示上按 `←` 从 NORMAL 模式以及 INSERT 打开 agent view，页脚的 `←` 提示在 NORMAL 模式中显示；在此版本之前手势和提示仅限 INSERT，在 NORMAL 模式中空提示上的 `←` 不做任何事。在 Claude Code 等待后台会话时在输入中键入取消切换，出现 `Backgrounding cancelled — you have unsent text in the input. Send it or clear it, then press ← again.` 所以键入的草稿不会丢失。 |
| v2.1.218 | 在清空提示的删除后两秒内或通过提示历史移动后按 `←` 显示 `Press ← again to open agents`，或在附加的会话中 `Press ← again to go back to agents`，仅在至少一秒后的第二次按压时切换；在此版本之前按压立即切换。在粘贴或脚本输入内到达的 `←` 不再触发切换。使用 `←` 后台前台会话显示 `Your conversation moved to the background` 在列表上方，agent view 根部的 `Esc` 返回到该对话而不是退出到 shell，双 `Ctrl+C` 保持退出；如果对话无法重新打开，Claude Code 退出并为其打印 `claude --resume` 命令。在 Windows 上，在附加后约半秒内按下的 `←` 显示 `Ambiguous ←, press again to detach` 并在第二次按压时分离。 |
| v2.1.217 | 会话行上的拉取请求徽章呈现为超链接，即使 Claude Code 无法检测到终端超链接支持，例如通过 SSH 或 tmux；设置 [`FORCE_HYPERLINK=0`](/docs/zh-CN/env-vars) 将其呈现为纯文本。在此版本之前，当未检测到支持时徽章呈现为纯文本。 |
| v2.1.216 | `/fork`：[确认](#from-inside-a-session)是一行，显示副本的状态、其 agent-view 行的名称和其会话 ID 用于 `claude attach`，仅当副本在主工作树中运行或编辑你打开的检出时以 `runs in the origin tree` 或 `edits this checkout` 结尾。点击名称后台此会话并在副本的会话中打开 agent view。确认不再重述副本的继承权限模式；早期版本打印了多行确认，没有可点击的名称。<br /><br />需要输入：`/install-github-app` 和 `/mcp` 设置列表，在没有人附加时运行，在 `Needs input` 下显示会话，带有命名命令的行，附加并重新运行命令继续；从 v2.1.208 到 v2.1.215 它们在该状态下被直接拒绝。<br /><br />`--agent` 恢复：恢复或重启[后台 `--agent` 会话](#from-your-shell)恢复代理的系统提示和工具限制，在会话自己的目录中搜索代理首先，当其工作区被信任时；代理不再存在的会话继续使用默认工具和系统提示，并以可见警告打开，而不是无声地恢复到默认代理。<br /><br />`Ctrl+X`：按两次删除会话，即使停止尝试失败，而不是失败的停止取消待处理删除，已删除的会话其工作进程已死不再在下一次刷新时重新出现。<br /><br />Worktree 删除：其 worktree 目录不属于任何 git 存储库的会话可以被删除；在此版本之前每次删除此类会话的尝试都被拒绝。已经消失的目录立即清除。agent view 双按删除仍有文件的目录，为 hook 创建的目录运行你的 `WorktreeRemove` hook，除非另一个会话的记录也命名它。`claude rm` 在文件仍然存在时保留此类目录。 |
| v2.1.214 | 使用 `←` 或 `/background` 后台的会话，空闲时没有任何运行，其进程停止，如同任何其他空闲会话，而不是保持其进程和后台服务无限期运行。已完成的会话可以在后台服务空闲后使用 `claude rm` 或从 agent view 删除，从不是 git 存储库的目录调度后进入 worktree 的会话，例如多存储库工作区文件夹，当 worktree 本身属于 git 存储库时可以从 agent view 删除，因为清理从 worktree 而不是会话调度的目录解决；两个删除在此版本之前都被拒绝。重新打开已停止的会话恢复其保存的对话，即使记录存储中的文件夹无法读取。 |
| v2.1.213 | `/install-github-app`、[`/mcp`](/docs/zh-CN/mcp) 设置列表和 MCP 身份验证操作在附加了终端的后台会话中工作，仅在没有人附加时被拒绝，带有告诉你附加并再次运行命令的消息；从 v2.1.208 到 v2.1.212 即使附加了终端也被拒绝。 |
| v2.1.212 | [交互式会话中的 `/fork`](#from-inside-a-session)将对话复制到显示为其自己行的新后台会话中，以来自的会话命名或，对于未命名会话的提示 fork，以 fork 提示命名，而原始保持运行；`/fork` 的早期 forked-subagent 行为移到 `/subtask`。启用[关闭 agent view](#turn-off-agent-view) 时，`/fork` 保持 forked-subagent 行为。等待其第一个提示的聚焦行显示 `space to send it a prompt`。`Ctrl+J` 在具有扩展键报告的终端上在调度输入中插入换行符，其中按键之前被忽略，`?` 覆盖层列出快捷键。当后台会话完成而没有任何需要你的输入时，交互式会话中的 `←` 页脚提示简要显示 `N done`。在 agent view 中键入裸 `/resume` 打开你打开 agent view 的存储库的过去会话的选择器，包括从列表中删除的会话，选择一个将其恢复为后台会话；在此版本之前 `/resume` 在 agent view 中不可用，已删除的会话仅通过 `claude --resume` 或交互式会话中的 `/resume` 可达。目标、范围和受限形式保留 `attach to a session to run it` 提示，早期版本为每个形式显示。等待沙箱网络主机提示、MCP 输入请求或托管设置提示的会话显示为 `Needs input` 而不是 `Working`，在 agent view 和 `claude agents --json` 中，Claude 的问题报告 `waitingFor: input needed` 而不是 `permission prompt`。附加到其进程已停止的会话显示其记录格式化为活跃会话呈现的方式，而不是原始文本。已停止的会话其记录在意外位置通过你保存的记录的最后手段扫描恢复，打开没有保存记录的行显示 `Press enter again to restart this session fresh`，在第二次按压时新鲜重启；v2.1.211 显示拒绝而没有从 agent view 重启的方式。 |
| v2.1.211 | 通过附加或从其运行的目录回复唤醒已停止的会话再次转发你的 shell 的网关 `ANTHROPIC_BASE_URL`，条件与新鲜调度相同，所以通过网关 `ANTHROPIC_AUTH_TOKEN` 身份验证的会话在网关上恢复而不是报告 `Not logged in`。附加到已停止的会话，该会话在其第一个响应完成前从另一个对话后台，被拒绝，出现 `This session has no saved transcript` 而不是无声地在相同会话 id 下启动空白对话；从 agent view 打开相同行显示页脚中的拒绝。从 Claude Code 外部结束 `←` 或 `/background` 会话的进程将其标记为已停止，而不是监督进程重新启动它，已记录在磁盘上的停止被尊重，除非你发送的回复仍在等待传递，崩溃后重新启动的会话被告知它被重新启动，重新启动的 `←` 或 `/background` 会话不恢复超过约一小时的中断响应。回答或拒绝提示而不是标记它的会话命名回复，例如对于主要是链接的提示，被丢弃，行保留从提示文本获取的名称。删除其 worktree git 不再识别的会话成功，在磁盘上留下 worktree 目录并命名其路径，而不是每次尝试都被拒绝。拒绝的删除在会话行上显示原因，包括 worktree 无法删除时的基础 git 错误，而不是行无声地重新出现。 |
| v2.1.210 | `claude attach` 在后台服务启动或重新连接时等待，而不是失败，出现 `job not found` 或 `still starting` 错误，报告在附加期间完成的会话为已退出，并应用在缓慢附加期间进行的终端调整大小，当附加完成时。提示页脚的 `←` 需要输入计数出现在每个提供商上，包括以前显示纯 `← for agents` 形式的第三方提供商。使用 `←` 后台会话将 Claude 的任务列表转移到后台会话，而不是丢弃它。你按 `←` 的行在选择移动后保留粗体、未变暗的名称。`claude agents --effort` 接受 `ultracode` 而不是无声地丢弃它。 |
| v2.1.208 | 附加到其进程已停止的会话显示其记录的最后屏幕，同时进程启动，而不是仅显示 `Session is starting` 注记。无法传递的回复，因为后台服务无法访问或发送失败，被保存并在其进程再次启动时作为会话的下一个提示发送；在此版本之前，后台服务无法访问时丢失的回复被丢弃。其自身二进制文件被更新替换的进程仍然可以从已安装的 `claude` 启动器或磁盘上的最新版本启动监督进程，而不是在 Claude Code 重新启动前失败。运行较旧版本的监督进程永远不会将由较新版本启动的空闲会话重新启动到其自身的较旧二进制文件上。删除会话删除其 worktree，即使会话将 worktree 移到了不同的分支，并在 worktree 有未推送到任何地方的提交或另一个会话声称它时将 worktree 与会话行保持在一起，而不是销毁提交或孤立 worktree。`/install-github-app` 和 `/mcp` 设置列表及其身份验证操作在后台会话中被拒绝，带有命名替代方案的消息；仅在 v2.1.208 中，`/model` 选择器以相同方式被拒绝，键入的 `/model <name>` 仅切换该会话，而不是也保存你的默认模型。 |
| v2.1.207 | 窥视面板以行截断的句子打开，例如等待你的会话的确切问题，并显示被阻止的会话已等待多长时间作为单个 `waiting 3m` 行，而不是将相同的时间戳前缀添加到状态句子和问题。在调度输入中再次粘贴相同的文本展开折叠的 `[Pasted text #N]` 占位符，而不是添加第二个。按名称接受计划的后台会话在其行上显示该名称。移入 worktree 的后台会话在其进程从 agent view 重新启动时保持其对话。 |
| v2.1.206 | 行摘要填充行的剩余宽度，仅在终端的右边缘截断，而不是在 64 列处。监督进程重新启动到新的 Claude Code 版本后，它在后台将剩余的空闲后台会话重新启动到该版本，而不是每分钟几个。使用 `Ctrl+X` 或 `claude rm` 删除会话也会将其从监督进程的会话列表中清除，所以行在监督进程重新启动后不再重新出现。在调度 shell 中导出的 `CLAUDE_CODE_EXTRA_BODY` 请求体覆盖到达后台会话，而不是被忽略。 |
| v2.1.205 | 提示页脚的 `←` 提示在常规 `claude` 会话中计数等待你的后台代理，例如 `← 2 agents`。行摘要显示会话自己的单行报告，在 64 列处截断，而不是原始工具调用或 `done/total` 计数；按目录分组的行以彩色状态词打开。窥视面板以完整状态句子打开，对于等待你的会话，其精确问题显示在回复输入上方。编辑、评论、关闭或使用 `gh` 标记拉取请求为就绪的会话与其关联，不仅仅是创建或检出拉取请求的会话，推送即使本地分支名称不匹配也会关联拉取请求，创建命令的输出超过内联限制的拉取请求也会关联。没有可读文本的转向保持会话的前一个状态，而不是将其翻转回 `Working`。`claude attach` 等待重新启动的会话长达约 60 秒，带有命名原因的状态行，而不是失败。 |
| v2.1.203 | 在调度 shell 中导出的网关 `ANTHROPIC_BASE_URL` 当监督进程共享该网关环境时，到达从它调度的会话进入同一目录，而不是在保留随之导出的 API 密钥时被丢弃。调度 shell 的 `PATH` 应用于每个会话的工作进程。在子代理运行时按 `←` 等待它们，而不是在十秒后重新启动它们。空列表始终显示部分标题及其下方的描述。在调度输入中键入 `@` 也列出启动存储库内其目录树中的已注册 git worktrees。从 `effortLevel` 设置继承的工作量在该设置的后续编辑后跟随，而不是在调度时固定。打开一个已停止的会话（其对话已在另一个运行中的会话中打开）被拒绝并显示消息，而不是导致行失败。在 agent view 中不可用的命令在输入中保留已键入的文本。在 git 存储库外失败的 `WorktreeCreate` hook 不再阻止会话编辑文件。 |
| v2.1.202 | 使用 `/rename` 或 `Ctrl+R` 在后台会话上设置的名称在监督进程停止并重新启动其进程时保持不变，而不是恢复为会话调度时的名称。 |
| v2.1.200 | 重写 `roster.json` 中会话列表的较旧 Claude Code 版本保留由较新版本写入的字段，与现有的 `state.json` 保证相匹配，因此由较新版本启动的会话在监督进程重新启动后继续接受输入。当你打开已停止响应的会话时，监督进程重新启动其进程，会话从中断处继续响应。Agent view 应用放在 `agents` 后的 `--plugin-dir` 标志到其自己的子代理和 skill 自动完成在调度输入中以及调度的会话。 |
| v2.1.199 | 后台会话的进程在低内存主机上完成启动前退出时，其行状态显示 `possibly low memory — free some up and retry` 而不仅仅是裸退出原因。使用 `←` 或 `/background` 后台会话时将其 `/color` 转移到新行。 |
| v2.1.198 | Agent view 在后台会话需要输入、完成或失败时通过 `preferredNotifChannel` 发送通知，并使用 `agent_needs_input` 或 `agent_completed` 类型触发 `Notification` hook。`←` 和 `/exit` 在 `claude attach <id>` 内返回 agent view 而不是退出到 shell；`Ctrl+Z` 返回到 shell。后台会话在 worktree 中隔离其工作，提交、推送其自己的隔离分支，从不 `main` 或 `master`，并在完成时打开草稿拉取请求而不是先询问。`/login` 在 agent view 中运行并打开登录对话框。`Background work is running` 退出对话框提供 `Move to background and exit`。退出交付也涵盖后台子代理，它们在下次唤醒时从其记录恢复，而不是被报告为失败。`claude --bg` 与 `-p` 或 `--print` 结合被拒绝并出现错误。后台会话主机在首次 LAN 访问时请求 macOS 本地网络权限，而不是失败，出现 `connect: no route to host`。 |
| v2.1.196 | 单次 `←` 按压后台前台会话；早期版本需要两次按压，带有页脚提示和确认。`--dangerously-skip-permissions` 传递给 `claude agents` 显示绕过免责声明，而不是被无声地丢弃。你从未命名的交互式会话在会话列表和 `claude agents --json` 中携带默认名称，例如 `my-app-3f`。后台 shell 命令和动态工作流在会话的进程被停止、重新启动或更新时存活，包括在 Windows 上；设置 `CLAUDE_CODE_DISABLE_BG_EXIT_HANDOFF=1` 关闭交付。在重新启动时误读为空的记录被重命名为 `.orphaned-` 后缀，而不是删除。 |
| v2.1.195 | 进行中的工作在 Windows 上后台会话时也转移；设置 `CLAUDE_DISABLE_ADOPT=1` 改为停止它。`Completed` 组填充剩余的垂直空间，标题在短终端上压缩。较旧的 Claude Code 版本不再丢弃较新会话的 `state.json` 字段或从 `claude agents` 隐藏这些会话。附加到停止的会话立即切换，而不是显示空白屏幕长达五秒。无法接受连接的监督进程自行退出并释放其锁。 |
| v2.1.191 | `claude --bg` 与不匹配你任何子代理的 `--agent` 名称失败启动：会话立即退出，出现 `--agent '<name>' not found` 错误，而不是使用默认代理运行。 |
| v2.1.174 | 后台会话不再从监督进程的启动 shell 继承网关端点变量如 `ANTHROPIC_BASE_URL`；监督进程向预热工作进程提供新的凭证快照，修复虚假的 `Could not resolve authentication method` 错误。 |
| v2.1.172 | 调度输入中的 `/model` 设置会话范围的调度模型覆盖。 |
| v2.1.161 | 行摘要显示并行工作项的 `done/total` 计数；窥视面板命名最长运行的并行工作项。 |
| v2.1.157 | `claude agents` 接受 `--agent`；调度的会话尊重 `agent` 设置。 |
| v2.1.145 | 窥视面板回复输入和调度输入中支持语音听写。 |
| v2.1.143 | 添加 `worktree.bgIsolation` 设置；`claude agents` 接受 `--allow-dangerously-skip-permissions`。 |
| v2.1.142 | `claude agents` 接受 `--permission-mode`、`--model`、`--effort`、`--dangerously-skip-permissions`、`--settings`、`--add-dir`、`--plugin-dir`、`--mcp-config` 和 `--strict-mcp-config`。 |
| v2.1.141 | `claude agents` 接受 `--cwd` 以将列表范围限定到一个项目。 |
| v2.1.139 | Agent view 作为研究预览版引入。 |
