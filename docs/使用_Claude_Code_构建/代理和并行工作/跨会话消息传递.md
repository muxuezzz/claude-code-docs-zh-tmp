> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 消息传递到您的其他 Claude Code 会话

> 让 Claude 列出并消息传递到您在此机器上的其他 Claude Code 会话，并到达您在其他机器或网络上的会话。

<Note>
  跨会话消息传递需要 macOS 和 Linux 上的 Claude Code v2.1.224 或更高版本，包括 WSL 2 内的 Linux。在原生 Windows 上，它需要 Claude Code v2.1.234 或更高版本。当会话满足要求时，消息传递功能默认启用，无需任何配置。请参阅[可用性](#availability)了解提供商要求以及如何确认会话具有此功能。
</Note>

跨会话消息传递让 Claude 能够将消息从您的一个 Claude Code 会话传递到另一个。当一个会话中的更改破坏了另一个会话正在构建的内容时，Claude 可以在您注意到之前警告该会话。当一个会话解决了另一个会话被阻止的问题时，Claude 可以跨会话发送答案。

消息是一个 Claude 写给另一个 Claude 的文本片段，永远不包括发送者的对话历史或文件。要移动整个对话或其上下文，请[恢复会话](/docs/zh-CN/sessions#resume-a-session)。

<h2 id="when-to-use-cross-session-messaging">
  何时使用跨会话消息传递
</h2>

当您的一个会话有另一个会话在任务中期需要的内容时，使用消息传递。Claude 可以在看到需要时自动发送消息，例如在进行影响另一个会话正在进行的工作的更改后，或者您可以要求它发送一条。常见情况包括：

* **移交发现**：当一个会话发现破坏性更改或做出决定时，Claude 为处理受影响区域的会话总结它，而不是您在那里重新解释。
* **协调并行 worktrees**：当会话在单独的 [worktrees](/docs/zh-CN/worktrees) 中处理同一存储库时，Claude 可以告诉其他会话已合并的内容。
* **获取长期运行工作的状态**：让迁移或测试运行报告回您正在观看的会话，或从那里自己询问。如果该会话在此机器上，Claude 还可以[在它下次空闲或退出时要求一条通知](#get-a-notice-when-another-session-goes-idle)。
* **跨机器发送消息**：到达您在另一台机器或网络上的一个会话。

<h2 id="message-another-session">
  向另一个会话发送消息
</h2>

当你的一个会话学到另一个会话需要的东西时，比如一个发现、一个状态或一个决定，Claude 会将其传递过去，而不是让你在终端之间复制粘贴。Claude 使用 `ListAgents` 发现目标，并使用 `SendMessage` 发送，所以你永远不需要自己调用这两个工具。Claude 可以在没有被要求的情况下决定发送消息，你也可以提示它发送一条消息。

要自己提示一条消息，告诉 Claude 你想让另一个会话知道或做什么。这个例子是你输入的提示，而不是 Claude 发送的消息：

```text wrap theme={null}
询问在我的另一个终端中运行的会话迁移是否完成
```

Claude 会自己编写实际的消息，所以你的提示可以将内容留给 Claude。这个提示要求一个摘要而不指定其措辞，Claude 发送的内容会有所不同：

```text wrap theme={null}
向处理支付 API 的会话解释我们刚刚做了什么
```

要自己命名目标，在你的提示中提及会话：输入 `@` 后跟会话名称的首字母，然后从类型提示中选择会话，方式与 [@-提及子代理](/docs/zh-CN/sub-agents#invoke-subagents-explicitly) 相同。需要 Claude Code v2.1.232 或更高版本。Claude Code 会插入提及，例如 `@api-worker`，并告诉 Claude 它命名的是哪个会话，这样 Claude 可以向该会话发送消息而无需先列出你的会话。这个提示用提及命名目标：

```text wrap theme={null}
让 @api-worker 知道架构迁移已完成
```

类型提示列出你在这台机器上的其他活跃会话。两种情况需要超过名称的首字母：

* **这台机器之外的会话**：云会话或远程控制会话仅在 Claude 列出或向你这台机器之外的会话发送消息后才会出现在类型提示中，所以请先要求 Claude 列出它们。
* **包含空格或字母、数字、连字符和下划线以外字符的名称**：用双引号输入，例如 `@"release notes"`。当你从类型提示中选择会话时，Claude Code 会为你插入引号。

你也可以不使用选择器直接输入提及。当多个活跃会话响应提及的名称时，Claude 会在发送前询问你指的是哪一个。

关于 Claude 编写的消息到达时的样子，包括一个例子，请参见 [消息看起来像什么](#what-a-message-looks-like)。

<h3 id="message-delivery">
  消息传递
</h3>

接收 Claude 在活跃轮次中的工具调用之间读取消息，所以运行中的工具永远不会被中断。当接收会话处于空闲状态时，Claude Code 会用消息启动新的轮次。

来自另一个会话的消息以纯文本形式到达。如果它用 `@` 提及文件或 [MCP 资源](/docs/zh-CN/mcp#use-mcp-resources)，Claude 会看到按原样写的提及，Claude Code 不会附加任何内容，无论消息是启动新轮次还是在现有轮次中到达。Claude 仍然可以用自己的工具在接收机器上打开提及的路径，受该会话的权限限制。

Claude Code 在以下情况下拒绝消息：

* 消息 [超过大小限制](#limitations)。Claude Code 在发送会话中拒绝它，在它离开之前。
* 对这台机器上的会话的快速突发已达到 [该会话的收件箱接受的内容](#limitations)。Claude Code 拒绝向该会话发送进一步的消息。
* 这台机器上的回复目标未通过安全检查，例如符号链接目标。[拒绝发送跨会话消息](/docs/zh-CN/errors#refusing-to-send-a-cross-session-message) 列出了这些检查。

接收会话根据其自己的 [入站控制](#control-inbound-messages) 检查每条到达的消息，检查以三种结果之一结束：

* **已传递**：Claude Code 将消息传递给接收 Claude。
* **已保留**：Claude Code 将消息搁置未传递。保留的消息仅在你批准它或稍后的模式或设置更改允许它时才到达 Claude。
* **已拒绝**：Claude Code 丢弃消息而不传递它。

一旦传递，消息计入 [使用情况](/docs/zh-CN/costs)，就像你输入的提示一样，接收 Claude 可以以相同的方式回复发送者，除了 [单向跨机器情况](#message-sessions-on-other-machines)。

权限边界保持按会话。Claude 被指示永远不要要求另一个会话执行在其自己的会话中被拒绝或阻止的操作，或其自己的权限设置会阻止的操作，而是将该工作路由回你。在接收端，[接收会话自己的权限提示和规则仍然适用](#how-a-session-treats-an-incoming-message) 于消息要求的任何内容。

<h3 id="get-a-notice-when-another-session-goes-idle">
  当另一个会话变为空闲时获得通知
</h3>

Claude 可以要求你在这台机器上的一个会话在该会话下一次变为空闲或退出时发回一条通知。这里的空闲意味着会话完成了一个轮次，没有任何排队的内容。当你在另一个会话中等待长任务并想听到它完成时而不是检查时使用它。需要两个会话中都有 Claude Code v2.1.236 或更高版本。

<h4 id="ask-for-a-notice">
  请求通知
</h4>

告诉 Claude 你在等什么。这个提示要求来自迁移会话的通知：

```text wrap theme={null}
告诉我迁移会话何时完成它正在处理的工作
```

Claude 使用 `SendMessage` 工具的 `notify_when_idle` 输入订阅，要么附加到它正在发送的消息，要么单独订阅。单独订阅时，Claude Code 订阅而不在被监视的会话中启动轮次或花费令牌，如果该会话已经空闲，会立即发送通知。附加到消息时，Claude Code 先传递消息，然后稍后发送通知。

<h4 id="what-each-session-shows">
  每个会话显示什么
</h4>

被监视的会话显示一行说另一个进程要求在会话下一次空闲时被告知。要求会话显示通知为一行命名被监视的会话。该行可以包括该会话轮次完成的时间和该轮次的单行状态。如果要求会话处于空闲状态，Claude Code 会用通知启动新的轮次。

<h4 id="limits">
  限制
</h4>

如果在 12 小时内没有通知到达，Claude Code 会删除订阅并告诉 Claude，所以它不会继续等待。

每一方的 [入站控制](#control-inbound-messages) 适用于像消息一样的通知：

* **任一方的 `refuse`**：什么都不会到达。被监视的会话删除请求而不记录或回答它，所以订阅在 12 小时后无答复过期，具有 `refuse` 的要求会话永远不会订阅。
* **任一方的 `hold`**：通知到达时内容较少。被监视的会话省略单行状态，要求会话在你的记录中显示通知而不将其传递给 Claude。

只有你主要对话中的 Claude 可以订阅，并且仅订阅你在这台机器上的会话。当 Claude 要求来自任何其他目标的通知时，例如队友、子代理或这台机器之外的会话，Claude Code 拒绝整个调用，包括附加到它的任何消息。

<h3 id="see-which-sessions-claude-can-reach">
  查看 Claude 可以到达的会话
</h3>

Claude 自己找到消息的目标，所以你不需要在要求它发送之前运行任何东西。要自己查看 Claude 可以到达的会话，运行 `/list-agents` 命令。第一行（如果存在）是这个会话自己的名称，你的其他会话用来向它发送消息的名称。下面的行是 Claude 可以到达的会话：

* **子代理**：在当前会话内运行的代理。
* **队友**：这个会话自己的 [代理团队](/docs/zh-CN/agent-teams) 队友。
* **你的其他本地会话**：在同一台机器上运行的 Claude Code 会话，包括 [后台会话](/docs/zh-CN/agent-view)。会话仅在绑定 [收件箱套接字](#the-sessions-inbox-socket) 时出现。
* **你的 [云会话](/docs/zh-CN/claude-code-on-the-web)**：在此会话连接到 [远程控制](/docs/zh-CN/remote-control) 时显示。
* **你在其他机器上的远程控制会话**：在此会话连接到 [远程控制](/docs/zh-CN/remote-control) 时显示，并标记为 `Remote Control`。Claude Code 显示 `offline` 作为远程控制连接已断开的会话的状态。

当此会话连接到 [远程控制](/docs/zh-CN/remote-control) 时，Claude Code 从 `/list-agents` 输出中隐瞒你的本地会话的一些详细信息，而不改变 Claude 本身在寻找要向其发送消息的会话时看到的内容：

* **工作目录**：它省略每个本地会话的工作目录。
* **会话名称**：它省略任何它不能归属于某个人的会话名称，所以没有名称的行读作 `(unnamed session)`。
* **第一行**：它省略包含此会话自己名称的行，除非你在此终端用 `--name` 或 `/rename` 和名称输入了该名称，自从你启动或最后恢复会话以来。

当输出列出任何内容时，它以一条说明详细信息被隐瞒的注释结束。在会话自己的键盘上运行 `/rename` 后跟未使用的名称会给该会话一个出现在输出中的名称。

会话响应你用 [`/rename`](/docs/zh-CN/commands) 命令或 [`--name`](/docs/zh-CN/cli-reference#cli-flags) 标志设置的名称。当你不设置一个时，Claude Code 自己命名会话。对于交互式会话，这是在 [运行会话的列表](/docs/zh-CN/sessions#name-your-sessions) 中显示的名称。

当你重命名会话，或用另一个活跃会话在这台机器上已经使用的名称启动或恢复交互式会话时，Claude Code 将名称留给已经拥有它的会话，并 [将你的重命名为变体](/docs/zh-CN/sessions#name-your-sessions)。会话仍然可以共享名称，例如当其中一个运行早期版本的 Claude Code 或共享名称是 Claude Code 生成的名称时。除非此会话连接到远程控制，Claude Code 在 `/list-agents` 输出中显示每个本地会话的工作目录，所以当它们在不同目录中运行时，你可以区分同名会话。Claude 根据有多少活跃会话响应该名称，以两种方式之一寻址消息：

* **一个会话响应该名称**：Claude Code 仅在名称上传递消息。
* **多个会话共享该名称，或 Claude Code 无法检查你的会话运行的所有地方**：Claude 为其列表的每一行添加一个短标识符，并在地址中使用该标识符。

<h3 id="message-sessions-on-other-machines">
  向其他机器上的会话发送消息
</h3>

消息如何传播，以及它是否通过 Anthropic 服务器，取决于目标会话运行的位置：

| 其他会话运行的位置 | 消息如何传播 |
| :- | :- |
| 在这台机器上 | 在 macOS 和 Linux 上通过每个会话的套接字，或在本机 Windows 上通过每个会话的命名管道，永远不通过 Anthropic 服务器 |
| 在你的另一台机器上 | 通过 Anthropic 服务器，通过该机器的 [远程控制](/docs/zh-CN/remote-control) 连接到达 |
| 在 [云中](/docs/zh-CN/claude-code-on-the-web) | 通过 Anthropic 服务器，直接到云会话 |

启动与你另一台机器上的会话的对话需要 Claude Code v2.1.225 或更高版本和一个 [出现在列表中](#see-which-sessions-claude-can-reach) 的目标。

你可以向显示为 [列表](#see-which-sessions-claude-can-reach) 中 `offline` 的会话发送消息，其远程控制连接已断开的会话。发送通过，但消息仅在该会话的机器重新连接后到达。

容器内的会话和主机上的会话无法相互到达。同一容器内的两个会话仍然可以相互发送消息，包括在 [自托管运行器](/docs/zh-CN/self-hosted-environments) 上。WSL 2 内的会话和同一计算机上的本机 Windows 会话也无法相互到达。

如果此会话在 Claude 发送到这台机器之外的会话时未连接到远程控制，消息仍然通过，但没有 [回复地址](#what-a-message-looks-like)，所以接收 Claude 无法回答它。

要在任何消息超出这台机器之前要求你的批准，设置 [`isolatePeerMachines`](#require-approval-for-cross-machine-messages)。

<h2 id="how-a-session-treats-an-incoming-message">
  会话如何处理传入消息
</h2>

当会话 A 向会话 B 发送消息时，Claude Code 告诉 B 的 Claude 消息来自另一个会话，而不是来自您，并限制消息可以做什么：

* **它不能批准任何内容**：来自另一个会话的消息永远不计为您的同意，因此它不能代表您回答待处理的权限提示。
* **它不能改变配置**：Claude Code 指示接收 Claude 永远不要改变权限设置、`CLAUDE.md` 或其他配置，因为另一个会话要求。
* **命令不运行**：消息文本中的命令，如 `/compact`，作为纯文本到达。Claude Code 永远不执行它。
* **权限提示仍然触发**：如果对消息进行操作需要接收会话没有的权限，您会看到与任何其他工作相同的提示。

<h3 id="what-a-message-looks-like">
  消息的样子
</h3>

当消息到达时，Claude Code 在对话中将其显示为暗淡的单行预览，预览行之后保留在对话中。预览包含发送者的名称和消息的第一行，当它很长时用 `…` 切割，如 `› Message from @api-worker: Schema migration finished (ctrl+o to expand)`。

这两个中的任何一个都显示您完整的文本：

* 按 `Ctrl+O` 打开[成绩单查看器](/docs/zh-CN/interactive-mode#transcript-viewer)并在发送者的会话名称下读取完整文本。
* 在使用 [`--verbose`](/docs/zh-CN/cli-reference#cli-flags) 启动的会话中，Claude Code 显示完整文本而不是预览。

预览仅缩短您看到的内容。无论您是否展开它，Claude 都读取完整消息。

Claude 接收消息时带有发送者的名称和回复地址，除了[单向跨机器消息](#message-sessions-on-other-machines)，它不携带回复地址。

这个例子是一个 Claude 写给另一个的消息，当您展开它时其完整文本读作：

```text wrap theme={null}
架构迁移已完成
新列是 tenant_id，在 main 上变基现在是安全的。
```

<h3 id="control-inbound-messages">
  控制入站消息
</h3>

设置 [`crossSessionInbound`](/docs/zh-CN/settings-reference#crosssessioninbound) 以选择会话对来自您的其他会话的到达消息做什么：

| 值 | 行为 |
| :- | :- |
| `accept` | Claude Code 将每条消息传递给 Claude |
| `hold` | Claude Code 为每条消息显示通知，不传递它。如果稍后应用 `accept`，根据[优先级规则](/docs/zh-CN/settings-reference#crosssessioninbound)，Claude Code 释放保留的消息 |
| `refuse` | Claude Code 删除每条消息而不传递它 |

除了编辑设置文件，您可以在 `/config` 行**来自您的其他会话的消息**中选择值。Claude Code 将您选择的值写入您的用户设置。该行需要 Claude Code v2.1.232 或更高版本，当托管设置或 `--settings` 标志设置密钥时不出现，因为用户设置值不会应用。Claude Code 拒绝此密钥的 `/config crossSessionInbound=value` 快捷方式。

要查看哪个值适用，请遵循[设置参考](/docs/zh-CN/settings-reference#crosssessioninbound)中的 `crossSessionInbound` 优先级规则。当没有值适用时，Claude Code 根据两个会话的权限模式按消息决定。它将[绕过权限提示](/docs/zh-CN/permission-modes#skip-all-checks-with-bypasspermissions-mode)的会话分组为一个类，每个其他会话分组为另一个。Plan Mode 在具有可用绕过权限的交互式终端会话中计为绕过，[auto](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)、`acceptEdits` 和 `dontAsk` 计为提示：

* **接收会话提示权限**：Claude Code 传递每条消息。它仅当发送会话将自己标识为绕过权限提示时才为您的批准保留一条。
* **接收会话绕过权限提示**：Claude Code 为您的批准保留每条消息。它仅当发送会话也标识为绕过时才传递一条。

当默认保留消息时，Claude Code 在接收会话中打开批准对话。对话显示发送者和预览：

* **批准**将该条消息传递给 Claude。
* **拒绝**，或关闭对话，删除它。
* 当对话在 [`dialogExpiry`](/docs/zh-CN/settings-reference#dialogexpiry) 截止日期后保持无答案时，Claude Code 关闭它并删除消息。截止日期默认为五分钟。
* 当没有终端附加到[后台会话](/docs/zh-CN/agent-view)时，Claude Code 将对话保留在截止日期之后。在您附加后，如果对话在完整截止日期期间保持无答案，Claude Code 关闭它并删除消息。
* 如果此会话的权限模式类在消息被保留时改变，Claude Code 重新应用入站规则，传递它们现在接受的消息，并显示通知。

Claude Code 最多保留 100 条消息，超过那个删除最旧的。

<h3 id="non-interactive-sessions">
  非交互式会话
</h3>

Claude Code 为 [`claude -p`](/docs/zh-CN/headless) 会话绑定收件箱套接字，如交互式会话，因此长期运行的 `-p` 工作者可以接收消息并出现在列表中。当您在[裸模式](/docs/zh-CN/headless#start-faster-with-bare-mode)中启动会话时，Claude Code 不绑定套接字，因此该会话无法接收消息，不出现在代理列表中。

`-p` 会话无法显示批准对话。当[入站默认](#control-inbound-messages)在那里保留消息时，Claude Code 为相同的 [`dialogExpiry`](/docs/zh-CN/settings-reference#dialogexpiry) 截止日期保留它，对话使用的默认值为五分钟：

* **在截止日期之前**：如果模式或设置更改允许消息，Claude Code 传递它。
* **在截止日期之后**：Claude Code 删除消息并向它可以到达的发送者报告它已过期。

设置 `dialogExpiry` 为 `"never"` 以保留默认保留的消息直到会话结束。由显式 `hold` 设置保留的消息不过期；Claude Code 仅当稍后应用 `accept` 时才传递它。

要让 `-p` 工作者无人值守地接收消息，使用 `crossSessionInbound` 设置为 `accept` 在其 `--settings` 值中启动它。您的用户设置中的 `accept` 也有效，但适用于您运行的每个会话。

<h3 id="the-sessions-inbox-socket">
  会话的收件箱套接字
</h3>

当您期望的会话不在代理列表中时，当您想要脚本或钩子发布到会话中时，或当沙箱命令无法到达套接字时，阅读本部分。

Claude Code 为启用跨会话消息传递的每个会话绑定收件箱套接字，同一机器上的其他会话在其中传递消息。套接字是 macOS 和 Linux 上的 Unix 域套接字，包括 WSL 2 内的 Linux，以及原生 Windows 上的命名管道。对于哪些会话类型绑定一个，请参阅[非交互式会话](#non-interactive-sessions)。

您可以在两个地方找到套接字的路径：

* `/status` 在 `Peer address` 行中显示它。路径以 `uds:` 为前缀。
* Claude Code 将其导出到[钩子](/docs/zh-CN/hooks)和 Bash 命令作为 [`CLAUDE_CODE_MESSAGING_SOCKET`](/docs/zh-CN/env-vars#variables) 环境变量：
  * 在以消息传递启动的会话中，Claude Code 在任何钩子运行之前导出变量，包括 `SessionStart`。

在 macOS 和 Linux 上，Claude Code 将套接字限制为您的操作系统用户。在原生 Windows 上，它改为要求每个连接首先使用只有您的操作系统用户可以读取的密钥进行身份验证。无论哪种方式，在共享机器上，另一个用户的会话无法传递给它。

在 macOS 和 Linux 上，Claude Code 也拒绝在它无法接受的目录中创建套接字，例如另一个用户拥有的目录，并改为使用私有的每用户目录 `/tmp/cc-socks-<uid>`。当它无法接受任何目录时，会话运行而没有收件箱：Claude Code 显示通知，`/status` 在其 `Peer address` 行中显示 `unavailable` 和原因，[`--debug`](/docs/zh-CN/cli-reference#cli-flags) 日志记录完整拒绝。

除了套接字的路径，Claude Code 导出每个会话令牌作为 [`CLAUDE_CODE_MESSAGING_TOKEN`](/docs/zh-CN/env-vars#variables)。发布到自己会话的套接字的脚本可以发送 `{"type":"auth","token":"<token>"}` 作为其连接的第一行，其中 `<token>` 是 `CLAUDE_CODE_MESSAGING_TOKEN` 的值。Claude Code 是否需要该行取决于平台：

* **macOS 和 Linux，包括 WSL 2**：该行是可选的。Claude Code 接受有或没有它的连接。
* **原生 Windows**：该行是必需的。Claude Code 关闭任何第一行不是有效身份验证行的连接，不从该连接传递任何内容。

仅在您发布的消息准备好时打开连接。Claude Code 关闭在 30 秒内未发送完整行的连接，因此首先捕获慢速命令的输出，然后打开连接以发送它。

<span id="own-child-messages" />Claude Code 通过套接字上到达的消息运行与任何其他对等消息相同的[入站控制](#control-inbound-messages)，有一个例外和一个先决条件：

* **自己的子消息**：当没有 `crossSessionInbound` 值适用时，Claude Code 传递它验证来自会话自己的子进程的消息，如钩子或 Bash 命令发布回自己会话的套接字。
  * 在 Linux 上，包括 WSL 2 内，Claude Code 可以通过进程证据验证，即使对于已经退出的子进程。在 macOS 上，它只能在发布进程仍在运行时通过这种方式验证，在 Claude Code 作为进程 ID 1 运行的容器中，它根本没有进程证据。在原生 Windows 上它也没有。
  * 在 macOS 上发布进程已退出后，在 Claude Code 作为进程 ID 1 运行的容器中，该进程证据丢失，Claude Code 改为验证发送会话导出的 [`CLAUDE_CODE_MESSAGING_TOKEN`](/docs/zh-CN/env-vars#variables) 在打开其连接的身份验证行中的子进程。在原生 Windows 上，该令牌是 Claude Code 验证自己的子消息的唯一方式。
  * 当 Claude Code 无法以任何方式验证时，它将消息视为任何其他声称没有权限类的消息，因此绕过权限提示的会话为您的批准保留它。
* **沙箱会话**：使用沙箱的 Unix 套接字设置 [`sandbox.network.allowAllUnixSockets` 和 `sandbox.network.allowUnixSockets`](/docs/zh-CN/settings-reference#sandbox-settings) 控制 Bash 命令是否可以从[沙箱](/docs/zh-CN/sandboxing)内到达套接字。

<h2 id="restrict-cross-session-messaging">
  限制跨会话消息传递
</h2>

除了每条消息的默认值，您可以通过两种方式缩小消息传递。在任何消息离开机器之前要求您的批准，或为会话或组织关闭消息传递。

<h3 id="require-approval-for-cross-machine-messages">
  要求批准跨机器消息
</h3>

设置 [`isolatePeerMachines`](/docs/zh-CN/settings-reference#isolatepeermachines) 为 `true` 以要求您的明确批准，在任何 `SendMessage` 到达超出此机器的会话之前：

```json theme={null}
{
  "isolatePeerMachines": true
}
```

设置此项后，Claude Code 在 Claude 的消息到达超出此机器的会话之前要求您的批准，即使在 `bypassPermissions` 模式中，它跳过普通权限提示。任何设置范围中的 `true` 适用，因此检查的项目文件可以打开要求但不关闭。Claude Code 不提示同一机器上的会话之间的消息。

<h3 id="turn-off-cross-session-messaging">
  关闭跨会话消息传递
</h3>

接收和发送是单独的控制，因此关闭您需要的任何方向，或两者。对到达的消息使用 `crossSessionInbound`，对 Claude 可以发送或列出的内容使用权限规则：

* **停止接收**：设置 `crossSessionInbound` 为 `refuse`，Claude Code 删除入站对等消息而不传递它们。从项目或本地设置，`refuse` 适用于每个其他来源，从您的用户设置它适用，除非托管设置或 `--settings` 标志设置值。
* **停止发送和列出**：添加[权限拒绝规则](/docs/zh-CN/permissions#tool-specific-permission-rules)命名 `SendMessage` 和 `ListAgents`。两者都采用没有说明符的裸工具名称。

管理员可以在[托管设置](/docs/zh-CN/managed-settings)中为组织关闭两个方向，结合拒绝规则与 `refuse`：

```json theme={null}
{
  "permissions": {
    "deny": ["SendMessage", "ListAgents"]
  },
  "crossSessionInbound": "refuse"
}
```

设置此项后，Claude Code 仍然为每个会话绑定收件箱套接字，但删除到达它的每条消息而不向 Claude 传递任何内容。拒绝 `SendMessage` 也删除向子代理和代理团队队友的消息传递，因为相同的工具服务两者。拒绝的会话在其自己的 `/status` 或同一机器上其他会话的列表中显示无可见更改，因此要确认它，检查适用于该会话的设置文件而不是其状态。

<h2 id="availability">
  可用性
</h2>

跨会话消息传递需要 macOS、Linux 和 WSL 2 上的 Claude Code v2.1.224 或更高版本，以及原生 Windows 上的 v2.1.234 或更高版本。可用性以及 Claude 可以向其发送消息的会话也取决于您的操作系统、提供商和配置：

* **操作系统**：在 macOS、Windows 和 Linux 上可用，包括 WSL 2 内的 Linux。

* **此机器上的会话**：在每个提供商上可用，包括 Amazon Bedrock、Claude Platform on AWS、Google Cloud 的 Agent Platform 和 Microsoft Foundry，以及在[功能标志获取](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching)关闭的会话中运行。在这些提供商上，以及标志获取关闭时，同机器消息传递需要 Claude Code v2.1.248 或更高版本。Claude Code 通过您机器上的[每个会话套接字](#the-sessions-inbox-socket)传递这些消息，永远不通过 Anthropic 服务器。

  要停止会话接收它们，设置 [`crossSessionInbound`](#turn-off-cross-session-messaging) 为 `refuse`。

* **超出此机器的会话**：Claude 从连接到远程控制的会话找到您的[网络上的 Claude Code](/docs/zh-CN/claude-code-on-the-web) 会话和您在其他机器上的会话，这需要 claude.ai 登录作为此会话的活跃身份验证和其他[远程控制要求](/docs/zh-CN/remote-control#requirements)。Claude 无法在 Amazon Bedrock、Claude Platform on AWS、Google Cloud 的 Agent Platform 和 Microsoft Foundry 上使用 API 密钥或找到这些会话。

要检查会话，输入 `/list-agents`，也可用作 `/peers`。结果将没有该功能的会话与更窄的东西阻止消息的会话分开，如缺少 `SendMessage` 工具或拒绝的发送：

* **`/list-agents` 无法识别**：会话没有跨会话消息传递。通过上面的要求工作，从 `claude --version` 开始获取版本要求。
* **`/list-agents` 有效但发送未到达**：消息传递启用，更窄的东西适用：
  * **拒绝规则**：[权限拒绝规则](#turn-off-cross-session-messaging)删除 `SendMessage` 和 `ListAgents` 工具。
  * **入站控制**：[接收会话的入站控制](#control-inbound-messages)可以保留或删除您发送给它的内容。
  * **云会话缺失**：云会话仅在此会话连接到[远程控制](/docs/zh-CN/remote-control)时出现。
  * **其他机器会话缺失**：您另一台机器上的会话仅在它使用[远程控制](/docs/zh-CN/remote-control)运行且此会话也连接时出现。
  * **其他机器会话 `offline`**：向列为 `offline` 的会话发送消息通过，但[仅在该会话的机器重新连接后到达](#message-sessions-on-other-machines)。
  * **较旧的云或其他机器会话缺失**：Claude Code 首先读取这些会话列表最新的并在有限数量的页面后停止，因此 Claude 无法按名称向超过它们的会话发送消息。

在具有消息传递的会话中，`/status` 也显示 `Peer address` 行，带有会话自己的收件箱地址，或 `unavailable` 和原因，当 Claude Code [无法设置收件箱](#the-sessions-inbox-socket)时。

<h2 id="limitations">
  限制
</h2>

这里的限制是消息传递通道本身的属性，在该功能运行的任何地方适用。对于平台和提供商差距，请改为参阅[可用性](#availability)。

* **仅纯文本**：Claude 仅在会话之间发送纯文本。结构化[代理团队](/docs/zh-CN/agent-teams)协议消息保留在团队内。
* **同机器消息大小有上限**：Claude Code 拒绝到此机器上的会话的消息，一旦其序列化形式超过约一百万个字符。拒绝[命名确切大小](/docs/zh-CN/errors#message-too-large-for-cross-session-delivery)。什么都不到达接收会话。
* **对一个会话的快速突发在发送者处被拒绝**：一旦对此机器上的会话的快速突发消息达到该会话的收件箱接受的内容，Claude Code 拒绝发送会话中的进一步发送。[拒绝命名突发](/docs/zh-CN/errors#too-many-messages-to-this-session-just-now)并告诉 Claude 将其余的批处理为一条消息或等待。
* **消息循环被限制**：在接收会话中，Claude Code 对每个发送者的重复消息进行速率限制，删除在短窗口内到达的相同重复，并最多为 Claude 读取排队 50 条接受的消息。因此两个会话之间的消息循环自己停止。

<h2 id="related-resources">
  相关资源
</h2>

* [子代理](/docs/zh-CN/sub-agents#resume-subagents)和[代理团队](/docs/zh-CN/agent-teams#messages-between-agents)：单个会话或团队内的消息传递
* [后台代理](/docs/zh-CN/agent-view)：分派和监控您可能向其发送消息的并行会话
* [远程控制](/docs/zh-CN/remote-control)：连接此会话以到达您在其他机器上的会话
* [频道](/docs/zh-CN/channels)：将外部事件（如 CI 结果或聊天消息）推送到会话中
* [设置](/docs/zh-CN/settings-reference#all-settings)：`crossSessionInbound`、`isolatePeerMachines` 和 `dialogExpiry`
* [权限模式](/docs/zh-CN/permission-modes)：入站默认的两个类背后的模式
* [工具参考](/docs/zh-CN/tools-reference)：工具表中的 `ListAgents` 和 `SendMessage` 行
* [并行运行代理](/docs/zh-CN/agents)：比较 Claude Code 运行多个代理的方式
