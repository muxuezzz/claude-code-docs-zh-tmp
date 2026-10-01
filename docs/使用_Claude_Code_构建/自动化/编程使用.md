> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 以编程方式运行 Claude Code

> 使用 Agent SDK 从 CLI、Python 或 TypeScript 以编程方式运行 Claude Code。

[Agent SDK](/docs/zh-CN/agent-sdk/overview) 为您提供了与 Claude Code 相同的工具、agent 循环和上下文管理。它可作为 CLI 用于脚本和 CI/CD，或作为 [Python](/docs/zh-CN/agent-sdk/python) 和 [TypeScript](/docs/zh-CN/agent-sdk/typescript) 包供完整的编程控制。

要以非交互模式运行 Claude Code，请使用 `-p` 传递您的提示和任何 [CLI 选项](/docs/zh-CN/cli-reference)：

```bash theme={null}
claude -p "Find and fix the bug in auth.py" --allowedTools "Read,Edit,Bash"
```

本页面涵盖通过 CLI (`claude -p`) 使用 Agent SDK。对于具有结构化输出、工具批准回调和原生消息对象的 Python 和 TypeScript SDK 包，请参阅 [完整 Agent SDK 文档](/docs/zh-CN/agent-sdk/overview)。

<h2 id="basic-usage">
  基本用法
</h2>

在任何 `claude` 命令中添加 `-p`（或 `--print`）标志以非交互方式运行它。并非每个 [CLI 选项](/docs/zh-CN/cli-reference) 都与 `-p` 兼容。Claude Code 拒绝 `--bg`，并在任务描述中拒绝 `--cloud`，会报错说明冲突；`--cloud` 与会话 ID 和 `-p` 一起使用时，会 [将消息排队到该云会话](/docs/zh-CN/claude-code-on-the-web#send-follow-ups-from-the-cli) 并退出。你通常会与 `-p` 结合使用的选项包括：

* `--continue` 用于 [继续对话](#continue-conversations)
* `--allowedTools` 用于 [自动批准工具](#auto-approve-tools)
* `--output-format` 用于 [获取结构化输出](#get-structured-output)

此示例向 Claude 询问有关你的代码库的问题并打印响应：

```bash theme={null}
claude -p "What does the auth module do?"
```

Claude Code 在成功时以代码 0 退出，在运行失败时以非零代码退出，因此你的脚本可以根据退出状态进行分支。如果你传递无效标志，Claude Code 会在运行开始前向 stderr 报告错误。当运行内部发生故障（例如缺少身份验证）时，Claude Code 会将故障作为结果打印到 stdout。

<h3 id="start-faster-with-bare-mode">
  使用裸模式更快启动
</h3>

添加 `--bare` 以通过跳过 hooks、skills、自定义命令、[subagents](/docs/zh-CN/sub-agents)、已安装的插件、MCP 服务器、自动内存和 CLAUDE.md 的自动发现来减少启动时间。没有它，`claude -p` 会加载交互式会话相同的 [context](/docs/zh-CN/how-claude-code-works#the-context-window)，包括在工作目录或 `~/.claude` 中配置的任何内容。

裸模式对于 CI 和脚本很有用，你需要在每台机器上获得相同的结果。队友的 `~/.claude` 中的 hook 或项目的 `.mcp.json` 中的 MCP 服务器不会运行，因为裸模式永远不会读取它们。你用 `--add-dir` 命名的目录是一个部分例外：裸模式从其 `.claude/skills/` 文件夹加载 skills，但仍然跳过其 `.claude/commands/` 和 `.claude/agents/` 文件夹。[来自其他目录的 Skills](/docs/zh-CN/skills#skills-from-additional-directories) 涵盖了加载和不加载的内容。

没有 `--bare`，`-p` 会话会运行项目的 `.claude/settings.json` 中的 hooks 并连接其 `.mcp.json` 中的服务器，即使在你从未信任的文件夹中也是如此。`-p` 会话不显示工作区信任对话框和每个服务器的批准提示。[在你信任文件夹之前运行的内容](/docs/zh-CN/permissions#what-runs-before-you-trust-a-folder) 涵盖了 `-p` 下每种类型的存储库内容以及如何将其排除在外。

此示例在裸模式下运行一次性摘要任务，并预先批准 Read 工具，以便调用完成而无需权限提示。运行前设置 `ANTHROPIC_API_KEY`，因为裸模式不使用你的订阅登录：

```bash theme={null}
claude --bare -p "Summarize README.md" --allowedTools "Read"
```

在裸模式下，Claude Code 永远不会读取 OAuth 凭证或系统密钥链。对于 Anthropic API，在环境中设置 `ANTHROPIC_API_KEY`，使用在 [Claude Console](https://platform.claude.com) 中创建的密钥，或在 `--settings` JSON 中提供 `apiKeyHelper`。Amazon Bedrock、Google Cloud 的 Agent Platform 和 Microsoft Foundry 继续照常读取它们自己的提供商凭证。

在裸模式下，Claude 可以访问 Bash、文件读取和文件编辑工具。使用标志传递你需要的任何 context：

| 要加载 | 使用 |
| - | - |
| 系统提示添加 | `--append-system-prompt`, `--append-system-prompt-file` |
| 设置 | `--settings <file-or-json>` |
| MCP 服务器 | `--mcp-config <file-or-json>` |
| 自定义 agents | `--agents <json>` |
| 一个插件 | `--plugin-dir <path>`, `--plugin-url <url>` |

<Note>
  `--bare` 是脚本和 SDK 调用的推荐模式，将在未来版本中成为 `-p` 的默认值。
</Note>

<h3 id="background-tasks-at-exit">
  退出时的后台任务
</h3>

如果 Claude 在 `claude -p` 运行期间启动 [后台 Bash 任务](/docs/zh-CN/tools-reference#bash-tool-behavior)（例如开发服务器或监视构建），该 shell 将在 Claude 返回其最终结果并关闭 stdin 后约五秒钟被终止。宽限期允许在结果之后立即完成的任务仍然传递其输出。

如果 Claude 启动后台 [subagent](/docs/zh-CN/sub-agents) 或工作流，`claude -p` 会改为保持打开状态，直到该工作完成，因为其结果是最终输出的一部分。

默认情况下，等待在连续空闲等待 10 分钟后结束，因此卡住的 subagent 或工作流无法无限期地保持进程打开。此时 Claude Code 停止仍在运行的任何内容并丢弃其部分结果。要更改限制，请设置 [`CLAUDE_CODE_PRINT_BG_WAIT_CEILING_MS`](/docs/zh-CN/env-vars)，或将其设置为 `0` 以无限期等待。

如果 Claude 在 `claude -p` 运行期间启动 [Monitor](/docs/zh-CN/tools-reference#monitor-tool) 监视，Claude Code 会等待监视直到它超时或十分钟的上限结束等待，以先发生者为准。在等待期间，Claude 继续响应监视报告的内容。默认情况下，监视在 Claude 启动后五分钟超时。

<h3 id="stop-a-run-with-sigterm">
  使用 SIGTERM 停止运行
</h3>

如果你使用 SIGTERM 停止 `claude -p` 运行，例如使用 `kill` 或从进程监督程序，Claude Code 以代码 143 退出。Claude Code 将正在进行的转向保持未完成状态，并且不为其记录任何结果。要改为结束转向，请发送 SIGINT，或在停止进程之前调用 Agent SDK 的 `interrupt()`。

在 SIGTERM 上，Claude Code 终止仍在运行的任何 Bash 命令的进程树。Claude Code 然后运行 [`SessionEnd` hooks](/docs/zh-CN/hooks#sessionend) 并退出。退出时，Claude Code 不启动新的工具调用，不发送新的模型请求，也不运行除 `SessionEnd` 之外的任何 hook。如果运行在信号到达时处于命令中间或等待权限提示的答案，Claude Code 按如下方式处理该步骤：

* **运行命令**：Claude Code 在会话中将命令记录为已杀死。
* **等待权限提示的答案**：如果你向进程发送 SIGTERM，Claude Code 会将提示保持未回答状态。如果你的程序通过 Agent SDK 关闭会话，SDK 会在发送任何信号之前结束 Claude Code 的输入，Claude Code 会在输入结束后立即取消提示。

当你 [恢复会话](#continue-conversations) 时，Claude Code 将中断的转向保持原样，你的下一个提示驱动对话。要让 Claude Code 在恢复时继续中断的转向，请设置 [`CLAUDE_CODE_RESUME_INTERRUPTED_TURN=1`](/docs/zh-CN/env-vars)。

<h3 id="if-the-working-directory-is-deleted">
  如果工作目录被删除
</h3>

如果 `claude -p` 或 Agent SDK 会话的工作目录在会话中间被删除，会话继续运行。当转向在目录缺失时启动时，Claude Code 在 `stream-json` 输出中发出 [警告消息](/docs/zh-CN/agent-sdk/typescript#sdkinformationalmessage)，shell 命令失败，直到目录再次存在。

<h2 id="examples">
  示例
</h2>

这些示例突出了常见的 CLI 模式。对于命名文件（如 `auth.py` 或 `build-error.txt`）的命令，请替换来自您自己项目的文件。在 CI 或其他脚本环境中，添加 [`--bare`](#start-faster-with-bare-mode) 以便 Claude Code 启动时不加载主机的 hooks、plugins、auto memory 或 `CLAUDE.md`。

<h3 id="pipe-data-through-claude">
  通过 Claude 管道传输数据
</h3>

非交互模式读取 stdin，因此您可以像任何其他命令行工具一样管道传输数据并重定向响应。

此示例将构建日志管道传输到 Claude 并将说明写入文件：

```bash theme={null}
cat build-error.txt | claude -p 'concisely explain the root cause of this build error' > output.txt
```

使用 `--output-format json`，响应有效负载包括 `total_cost_usd` 和按模型的成本分解，因此脚本调用者可以跟踪支出而无需查询 [使用情况仪表板](/docs/zh-CN/costs)。当您使用 `--continue` 或 `--resume` 继续较早的对话时，运行报告对话的整体总计，[包括较早运行的支出](/docs/zh-CN/agent-sdk/cost-tracking#accumulate-costs-across-multiple-calls)。两个数字都是 [客户端估计](/docs/zh-CN/agent-sdk/cost-tracking)，可能与您的实际账单不同。

<Note>
  管道 stdin 的上限为 10MB。如果超过上限，Claude Code 会以清晰的错误和非零状态退出。要处理更大的输入，请将内容写入文件并在提示中引用文件路径，而不是管道传输它。
</Note>

如果 Claude Code 无法读取 stdin，例如因为启动它的进程断开了其端点，Claude Code 会向 stderr 打印警告并继续使用命令行中的提示。在 v2.1.211 之前，Windows 上不可读的 stdin 会导致会话崩溃或无输出地静默退出。

<h3 id="add-claude-to-a-build-script">
  将 Claude 添加到构建脚本
</h3>

您可以在脚本中包装非交互调用，以将 Claude 用作项目特定的 linter 或审查者。

此 `package.json` 脚本将针对 `main` 的 diff 管道传输到 Claude，并要求它报告拼写错误。管道传输 diff 意味着 Claude 不需要 Bash 权限来读取它，转义的双引号使脚本可移植到 Windows：

```json theme={null}
{
  "scripts": {
    "lint:claude": "git diff main | claude -p \"you are a typo linter. for each typo in this diff, report filename:line on one line and the issue on the next. return nothing else.\""
  }
}
```

使用 `npm run lint:claude` 运行它。

<h3 id="get-structured-output">
  获取结构化输出
</h3>

使用 `--output-format` 控制响应的返回方式：

* `text`（默认）：纯文本输出
* `json`：包含结果、会话 ID 和元数据的结构化 JSON
* `stream-json`：用于实时流式传输的换行符分隔的 JSON

此示例以 JSON 格式返回项目摘要以及会话元数据，文本结果在 `result` 字段中：

```bash theme={null}
claude -p "Summarize this project" --output-format json
```

要获得符合特定架构的输出，请使用 `--output-format json` 与 `--json-schema` 和 [JSON Schema](https://json-schema.org/) 定义。响应包括关于请求的元数据（会话 ID、使用情况等），结构化输出在 `structured_output` 字段中。

此示例从 auth.py 中提取函数名称并将其作为字符串数组返回：

```bash theme={null}
claude -p "Extract the main function names from auth.py" \
  --output-format json \
  --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}'
```

如果该值不是有效的 JSON Schema，`claude` 会以 `Error: --json-schema is not a valid JSON Schema` 退出，后跟验证器的诊断。Claude Code 接受使用 `format` 关键字的架构，例如 `"format": "email"`，但将 `format` 视为注释，不强制执行它。在 v2.1.205 之前，Claude Code 会静默忽略无效的架构并返回非结构化文本，并将任何包含 `format` 的架构视为无效。

<Tip>
  使用 [jq](https://jqlang.org/) 之类的工具来解析响应并提取特定字段：

  ```bash theme={null}
  # Extract the text result
  claude -p "Summarize this project" --output-format json | jq -r '.result'

  # Extract structured output
  claude -p "Extract function names from auth.py" \
    --output-format json \
    --json-schema '{"type":"object","properties":{"functions":{"type":"array","items":{"type":"string"}}},"required":["functions"]}' \
    | jq '.structured_output'
  ```
</Tip>

<h3 id="stream-responses">
  流式传输响应
</h3>

使用 `--output-format stream-json` 与 `--verbose` 和 `--include-partial-messages` 来接收生成的令牌。每一行都是代表一个事件的 JSON 对象：

```bash theme={null}
claude -p "Explain recursion" --output-format stream-json --verbose --include-partial-messages
```

流的最后一行是包含最终响应文本、成本和会话元数据的 `result` 消息。

如果您的消费者缓慢读取流，Claude Code 会等待队列中的输出排空后再退出，根据仍然队列中的数量缩放等待时间，上限为 30 秒。在 v2.1.214 之前，退出等待的上限约为两秒，这可能会截断大型响应的末尾。

以下示例使用 [jq](https://jqlang.org/) 来过滤文本增量并仅显示流式文本。`-r` 标志输出原始字符串（无引号），`-j` 不带换行符连接，以便令牌连续流式传输：

```bash theme={null}
claude -p "Write a poem" --output-format stream-json --verbose --include-partial-messages | \
  jq -rj 'select(.type == "stream_event" and .event.delta.type? == "text_delta") | .event.delta.text'
```

对于具有回调和消息对象的编程流式传输，请参阅 Agent SDK 文档中的 [实时流式传输响应](/docs/zh-CN/agent-sdk/streaming-output)。

<h4 id="follow-subagent-messages">
  跟踪 subagent 消息
</h4>

来自 [subagents](/docs/zh-CN/sub-agents) 的消息在流中显示为 `assistant` 和 `user` 消息，其 `parent_tool_use_id` 字段是生成 subagent 的工具调用的 ID。来自主对话的消息在该字段中携带 `null`。

来自在 [前台](/docs/zh-CN/sub-agents#run-subagents-in-foreground-or-background) 运行的 subagent 的第一条消息是携带驱动它的提示的 `user` 消息。在该第一条消息之后，Claude Code 发出：

* **默认情况下**：subagent 的 `tool_use` 和 `tool_result` 块。
* **使用 [`--forward-subagent-text`](/docs/zh-CN/cli-reference#cli-flags) 或 [`CLAUDE_CODE_FORWARD_SUBAGENT_TEXT`](/docs/zh-CN/env-vars)**：subagent 的文本和思考块也是如此，因此您可以重建每个 subagent 的记录。这需要 Claude Code v2.1.211 或更高版本。

当您启用任一选项时，Claude Code 从 [每个嵌套深度的 subagents](/docs/zh-CN/sub-agents#let-subagents-spawn-their-own-subagents) 转发消息，无论每个 subagent 是使用 Agent 工具生成的还是作为 [forked skill](/docs/zh-CN/skills#run-skills-in-a-subagent) 启动的。forked skill 生成的 subagents 的消息，以及在 subagent 或另一个 forked skill 内启动的 forked skills，需要 Claude Code v2.1.275 或更高版本。在 `parent_tool_use_id` 中，嵌套 subagent 的消息携带启动它的 Agent 或 Skill 工具调用的 ID，因此您可以通过跟踪这些 ID 来重建完整的嵌套树。在 v2.1.219 之前，来自嵌套 subagents 的消息不会出现在流中。

[在 subagent 中运行](/docs/zh-CN/skills#run-skills-in-a-subagent) 的 Skills 在流中以相同的方式出现：forked skill 的第一条消息是携带驱动运行的 skill 内容的 `user` 消息。如果您启用任一选项，流也会携带 forked skill 的文本和思考块。在 v2.1.265 之前，只有 forked skill 的 `tool_use` 和 `tool_result` 块出现在流中。

<h4 id="handle-api-retries">
  处理 API 重试
</h4>

当 API 请求因可重试错误而失败时，Claude Code 在重试前发出 `system/api_retry` 事件。在 v2.1.246 或更高版本上，当 `401` 或 `403` 拒绝 [`apiKeyHelper`](/docs/zh-CN/settings-reference#apikeyhelper) 凭证时，Claude Code 会静默进行前两次重试，没有事件，然后从第三次连续重试开始照常发出事件。静默重试仍然计入 `attempt`。您可以使用该事件在您自己的界面中显示重试进度。

| 字段 | 类型 | 描述 |
| - | - | - |
| `type` | `"system"` | 消息类型 |
| `subtype` | `"api_retry"` | 将其标识为重试事件 |
| `attempt` | 整数 | 当前尝试次数，从 1 开始 |
| `max_retries` | 整数 | 允许的总重试次数，对于此失败的原因可能少于会话范围的预算 |
| `retry_delay_ms` | 整数 | 毫秒直到下一次尝试 |
| `error_status` | 整数或 null | 失败尝试的 HTTP 状态代码，或 `null` 当尝试从 API 没有获得 HTTP 响应时 |
| `no_response` | 对象，可选 | 仅当失败的尝试 [及时没有获得响应头](/docs/zh-CN/errors#no-response-from-api) 时存在。`waited_ms` 是该尝试等待的时间，`retry_wait_ms` 是重试将等待的时间。在这些事件中，`max_retries` 反映此原因通常获得的一次重试，而不是会话范围的预算。需要 Claude Code v2.1.261 或更高版本 |
| `error` | 字符串 | 错误类别：`authentication_failed`、`oauth_org_not_allowed`、`account_on_hold`、`billing_error`、`rate_limit`、`overloaded`、`invalid_request`、`model_not_found`、`server_error`、`max_output_tokens`、`cloud_credential_error` 或 `unknown` |
| `uuid` | 字符串 | 唯一事件标识符 |
| `session_id` | 字符串 | 事件所属的会话 |

<h4 id="read-session-metadata">
  读取会话元数据
</h4>

`system/init` 事件报告会话元数据，包括模型、工具、MCP 服务器和加载的 plugins。它是流中的第一个事件，除非启动事件在其之前：

* `plugin_install` 事件，当设置了 [`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`](/docs/zh-CN/env-vars) 时。
* [`hook_started`、`hook_progress` 和 `hook_response` 事件](/docs/zh-CN/agent-sdk/typescript#sdkhookstartedmessage)，当配置的 [`SessionStart`](/docs/zh-CN/hooks#sessionstart) 或 [`Setup`](/docs/zh-CN/hooks#setup) hook 运行时。这些事件在 hook 生成时流式传输。Claude Code v2.1.169 至 v2.1.203 在 hook 完成后以一个批次传递它们，仍然在 `system/init` 之前；v2.1.204 恢复了实时传递。

该事件还携带一个可选的 `capabilities` 字符串数组，命名此 Claude Code 版本实现的协议行为，例如 `interrupt_receipt_v1` 或 `interrupt_cancel_queued_v1`。检查它以进行功能检测，而不是比较版本字符串，并忽略您不认识的值。该字段需要 Claude Code v2.1.205 或更高版本，在早期版本中不存在。有关功能列表，请参阅 [`SDKSystemMessage`](/docs/zh-CN/agent-sdk/typescript#sdksystemmessage)。

<h4 id="fail-ci-when-a-plugin-or-mcp-server-doesn’t-load">
  当 plugin 或 MCP 服务器未加载时使 CI 失败
</h4>

使用 `system/init` 事件中的 plugin 字段来捕获未加载的 plugin：

| 字段 | 类型 | 描述 |
| - | - | - |
| `plugins` | 数组 | 成功加载的 plugins，每个都有 `name` 和 `path` |
| `plugin_errors` | 数组 | plugin 加载时错误，每个都有 `plugin`、`type` 和 `message`。包括不满足的依赖版本和 `--plugin-dir` 加载失败，例如缺失路径或无效存档。未加载的 plugin 从 `plugins` 中缺失。当没有错误时，该键被省略 |

当 `--plugin-dir` 目录或存档本身加载失败时，其 `plugin_errors` 条目包括解析的绝对路径作为 `path`。使用它来判断哪个 `--plugin-dir` 值失败。`path` 字段需要 Claude Code v2.1.283 或更高版本。

以相同的方式使用 MCP 服务器字段。当您使用 `-p` 传递 [`--mcp-config`](/docs/zh-CN/cli-reference#cli-flags) 时，Claude Code 在运行第一轮之前等待仍然待处理的服务器，最多等待 [`MCP_TIMEOUT`](/docs/zh-CN/env-vars) 启动超时，默认为 30 秒。具有 [缓存工具列表](/docs/zh-CN/agent-sdk/mcp#connection-timing) 的远程服务器跳过等待，在 `system/init` 中显示 `pending`，并在其第一次工具调用时连接。等待需要 Claude Code v2.1.221 或更高版本。

Claude Code 在启动时验证每个 `--mcp-config` 条目并跳过验证失败的条目，例如没有 `type` 的 `url` 条目。运行继续并干净地退出，因此检查这些字段以捕获从未加载的服务器：

| 字段 | 类型 | 描述 |
| - | - | - |
| `mcp_servers` | 数组 | 会话中的 MCP 服务器，每个都有 `name` 和 `status` |
| `mcp_server_errors` | 数组 | `--mcp-config` 条目被配置验证跳过，每个都有 `name`、`type` 和 `message`。`type` 是跳过类别，例如 `unknown_type`、`url_missing_type`、`invalid_config` 或 `reserved_name`；将您不认识的值视为通用跳过。受影响的服务器从 `mcp_servers` 中缺失。当没有错误时，该键被省略，因此 CI 门可以在非空数组上失败。需要 Claude Code v2.1.219 或更高版本 |

当您在终端中手动运行命令时，Claude Code 也会向 stderr 打印启动警告，例如 `Warning: 1 MCP server skipped due to invalid config:`，后跟每个跳过条目的原因。当您重定向 stderr 或当 CI 运行器或 SDK 主机等程序捕获它时，Claude Code 不打印警告，仅在 `mcp_server_errors` 字段中报告跳过的条目。警告需要 Claude Code v2.1.219 或更高版本。

<h4 id="track-plugin-installs">
  跟踪 plugin 安装
</h4>

当设置了 [`CLAUDE_CODE_SYNC_PLUGIN_INSTALL`](/docs/zh-CN/env-vars) 时，Claude Code 在第一轮之前安装市场 plugins 时发出 `system/plugin_install` 事件。使用这些在您自己的 UI 中显示安装进度。

| 字段 | 类型 | 描述 |
| - | - | - |
| `type` | `"system"` | 消息类型 |
| `subtype` | `"plugin_install"` | 将其标识为 plugin 安装事件 |
| `status` | `"started"`、`"installed"`、`"failed"` 或 `"completed"` | `started` 和 `completed` 括住整体安装；`installed` 和 `failed` 报告单个市场 |
| `name` | 字符串，可选 | 市场名称，在 `installed` 和 `failed` 上存在 |
| `error` | 字符串，可选 | 失败消息，在 `failed` 上存在 |
| `uuid` | 字符串 | 唯一事件标识符 |
| `session_id` | 字符串 | 事件所属的会话 |

<h3 id="auto-approve-tools">
  自动批准工具
</h3>

使用 `--allowedTools` 让 Claude 使用某些工具而无需提示。列出 `Read` 和 `Edit` 让 Claude 读取和编辑文件而无需请求权限。列出 `Bash` 对 shell 命令执行相同操作，除了在 [auto 模式](/docs/zh-CN/permission-modes#how-auto-mode-evaluates-actions) 中启动的运行，其中 Claude Code 删除裸 `Bash` 条目作为广泛允许规则，auto 模式改为评估每个命令。此示例运行测试套件并修复失败，允许这三个工具：

```bash theme={null}
claude -p "Run the test suite and fix any failures" \
  --allowedTools "Bash,Read,Edit"
```

要为整个会话设置基线而不是列出单个工具，请传递 [权限模式](/docs/zh-CN/permission-modes)。对于不设置权限模式的运行，采用 [内置启动权限模式](/docs/zh-CN/permission-modes#which-mode-a-session-starts-in)，可能是 `auto`，因此传递您想要的权限模式：

* **`auto`**：传递 `--permission-mode auto` 以让分类器审查大多数操作而不是您
* **`dontAsk`**：Claude Code 拒绝每个原本会提示的调用，这对于锁定的 CI 运行很有用。在 Manual 模式下无需批准的操作仍会运行，例如工作目录中的文件读取和 [只读命令集](/docs/zh-CN/permissions#read-only-commands)，您的 `--allowedTools` 条目或 `permissions.allow` 规则涵盖的操作也是如此。`AskUserQuestion`、连接器工具 [您的组织设置为 `ask`](/docs/zh-CN/mcp#organization-controls-on-connector-tools) 和标记为 [`requiresUserInteraction`](/docs/zh-CN/mcp#require-approval-for-a-specific-tool) 的 MCP 工具即使当允许规则匹配时也被拒绝
* **`acceptEdits`**：Claude 写入文件而无需提示，Claude Code 自动批准常见的文件系统命令，例如 `mkdir`、`touch`、`mv` 和 `cp`。[任何模式都不自动批准的操作](/docs/zh-CN/permission-modes#actions-no-mode-auto-approves) 仍然适用。除了只读命令集，其他 shell 命令和网络请求仍然需要 `--allowedTools` 条目或 `permissions.allow` 规则。有关 `acceptEdits` 自动批准的内容，请参阅 [使用 acceptEdits 模式自动批准文件编辑](/docs/zh-CN/permission-modes#auto-approve-file-edits-with-acceptedits-mode)

此示例使用 `acceptEdits` 作为基线应用 lint 修复：

```bash theme={null}
claude -p "Apply the lint fixes" --permission-mode acceptEdits
```

<h3 id="turn-off-permission-prompts-in-unattended-runs">
  在无人值守运行中关闭权限提示
</h3>

当没有人可用来回答权限提示时，传递 `--permission-prompts none`，例如在计划的作业中。当您的运行有权限主机时，该标志最重要：具有 [`canUseTool` 回调](/docs/zh-CN/agent-sdk/user-input) 的 Agent SDK 应用，或您使用 [`--permission-prompt-tool`](/docs/zh-CN/cli-reference#cli-flags) 传递的 MCP 工具。没有该标志，您的运行会等待该主机回答每个权限请求。

使用该标志，您的运行不会查询主机或等待它。任何会提示的内容都被拒绝，除非 `PermissionRequest` hook 允许它，Claude 被告知没有人可以批准请求且不要重试它，运行继续。在没有主机的 `-p` 运行中，这些请求无论如何都被拒绝，该标志也告诉 Claude 不要重试它们。权限规则、[`PermissionRequest` hooks](/docs/zh-CN/hooks#permissionrequest) 和您设置的权限模式仍然首先决定每个调用；Claude Code 仅拒绝其他任何内容都不解决的请求。

此示例在 [auto 模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode) 中运行无人值守任务。分类器照常审查每个操作，Claude Code 拒绝任何会回退到提示的内容：

```bash theme={null}
claude -p "Update the dependency pins and run the tests" --permission-mode auto --permission-prompts none
```

使用 `--permission-prompts none`，Claude Code 移除需要来自人的答案的工具，例如 [`AskUserQuestion`](/docs/zh-CN/tools-reference#askuserquestion-tool-behavior)，因此 Claude 无法调用它们。任何没有 [`Elicitation` hook](/docs/zh-CN/hooks#elicitation) 回答的 [MCP 引出请求](/docs/zh-CN/mcp#respond-to-mcp-elicitation-requests) 都被取消。

使用 `--output-format stream-json`，拒绝显示为 `permission_denied` 系统消息，最终结果消息在 `permission_denials` 中列出它们。

<Note>
  `--permission-prompts` 标志需要 Claude Code v2.1.259 或更高版本。早期版本以未知选项错误拒绝它。
</Note>

<h3 id="create-a-commit">
  创建提交
</h3>

此示例审查暂存的更改并创建具有适当消息的提交：

```bash theme={null}
claude -p "Look at my staged changes and create an appropriate commit" \
  --allowedTools "Bash(git diff *),Bash(git log *),Bash(git status *),Bash(git commit *)"
```

`--allowedTools` 标志使用 [权限规则语法](/docs/zh-CN/settings-reference#permission-rule-syntax)。尾部的 ` *` 启用前缀匹配，因此 `Bash(git diff *)` 允许任何以 `git diff` 开头的命令。空格在 `*` 之前很重要：没有它，`Bash(git diff*)` 也会匹配 `git diff-index`。

<Note>
  命令支持在 `-p` 模式下有所不同：

  * 用户调用的 [skills](/docs/zh-CN/skills) 和自定义命令工作。在提示字符串中包含 `/skill-name`，Claude Code 会在运行前展开它。
  * 仅在终端界面中运行的内置命令，例如 `/login`，在 `-p` 模式下不可用。
  * `/model`、`/effort`、`/fast`、`/color` 和 `/rename` 接受该值作为参数，例如 `/model sonnet`，`/mcp` 不带参数打印服务器状态的文本摘要。这些形式需要 Claude Code v2.1.205 或更高版本，并遵循每个命令的 [可用性说明](/docs/zh-CN/commands#all-commands)。
  * 要从 `-p` 调用更改设置，请将 `key=value` 传递给 `/config`，例如 `/config thinking=false`。
  * `/output-style <style>` 切换 [输出样式](/docs/zh-CN/output-styles)，`/output-style` 单独列出它们。需要 Claude Code v2.1.269 或更高版本。
</Note>

<h3 id="customize-the-system-prompt">
  自定义系统提示
</h3>

使用 `--append-system-prompt` 添加指令同时保持 Claude Code 的默认行为。此示例将 PR diff 传递给 Claude 并指示它审查安全漏洞。将其保存为 shell 脚本，例如 `review.sh`：

```bash theme={null}
gh pr diff "$1" | claude -p \
  --append-system-prompt "You are a security engineer. Review for vulnerabilities." \
  --output-format json
```

在脚本中，`"$1"` 代表您在命令行上传递的第一个参数。运行 `bash review.sh 123`，shell 将 `"$1"` 替换为 `123`，因此脚本获取 PR 123 的 diff。Claude Code 将审查打印为 JSON，文本在 `result` 字段中。

有关更多选项（包括 `--system-prompt` 以完全替换默认提示），请参阅 [系统提示标志](/docs/zh-CN/cli-reference#system-prompt-flags)。

<h3 id="continue-conversations">
  继续对话
</h3>

使用 `--continue` 继续最近的对话，或使用 `--resume` 与会话 ID 继续特定对话。在 Claude Code v2.1.257 或更高版本上，当您传递 `--continue` 时，Claude Code 会打开已完成的 [后台会话](/docs/zh-CN/sessions#resume-a-session)，但不会打开仍在运行的后台会话。此示例运行审查，然后发送后续提示：

```bash theme={null}
# First request
claude -p "Review this codebase for performance issues"

# Continue the most recent conversation
claude -p "Now focus on the database queries" --continue
claude -p "Generate a summary of all issues found" --continue
```

如果您运行多个对话，请捕获会话 ID 以恢复特定对话：

```bash theme={null}
session_id=$(claude -p "Start a review" --output-format json | jq -r '.session_id')
claude -p "Continue that review" --resume "$session_id"
```

您可以从不同的目录运行两个命令：Claude Code [按其 ID 查找会话](/docs/zh-CN/sessions#resume-a-session) 在此机器上的任何项目中。在 v2.1.223 之前，Claude Code 仅在当前项目目录及其 git worktrees 中查找 ID，因此您必须从同一目录运行两个命令。

代替会话 ID，您可以将 `--resume` 传递会话的 `.jsonl` [记录文件](/docs/zh-CN/sessions#where-transcripts-are-stored) 的绝对路径，Claude Code 继续存储在该文件中的对话。

<h2 id="next-steps">
  后续步骤
</h2>

* [Agent SDK 快速入门](/docs/zh-CN/agent-sdk/quickstart)：使用 Python 或 TypeScript 构建您的第一个 agent
* [CLI 参考](/docs/zh-CN/cli-reference)：所有 CLI 标志和选项
* [GitHub Actions](/docs/zh-CN/github-actions)：在 GitHub 工作流中使用 Agent SDK
* [GitLab CI/CD](/docs/zh-CN/gitlab-ci-cd)：在 GitLab 管道中使用 Agent SDK
