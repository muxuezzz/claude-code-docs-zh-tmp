> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 使用 Code Mode 通过代码运行工具调用

> 试用 Code Mode，这是一项实验性功能，Claude 会在其中编写 JavaScript，在一个步骤中进行多次工具调用。

Code Mode 改变了 Claude 使用其[工具](https://code.claude.com/docs/zh-CN/tools-reference.md)的方式。不使用 Code Mode 时，Claude 会直接请求 Bash、Read 或 Edit 等工具调用，并在决定下一步操作之前读取每个结果。使用 Code Mode 时，Claude 会编写一段 JavaScript 来进行这些工具调用，然后由 Claude Code 在您的会话中运行这段代码。

> [!NOTE]
>
> Code Mode 是一项实验性功能，默认处于关闭状态。它可能会在任何版本中发生变化或被移除。如需分享反馈，请运行 `/feedback`。

## Code Mode 的工作原理

在 Code Mode 会话中，您仍然通过提示词描述任务，Claude 会编写 JavaScript 来执行该任务。一段代码可以并行运行命令、在下一次调用中使用上一次的结果，并返回 Claude 需要读取的那部分输出。

例如，如果您让 Claude 提高重试次数上限，Claude 可能会编写以下代码来查找文件、编辑文件并运行测试。最后一行将文件路径和测试输出返回给 Claude：

```javascript theme={null}
const files = await $`rg -l "function retryPolicy" src`.text();
const target = files.trim().split("\n")[0];
await edit(target, "maxAttempts: 3", "maxAttempts: 5");
({ edited: target, tests: $`npm test -- retryPolicy`.nothrow() });
```

在对话中，您看到的是工具调用（例如编辑的 diff），而不是代码。要阅读代码，请按 `Ctrl+O` 打开[会话记录查看器](https://code.claude.com/docs/zh-CN/interactive-mode.md#transcript-viewer)。每段代码在其中显示为一个折叠的 **Code** 行，并附有如何展开的提示。

### 何时使用 Code Mode

对于需要大量相关工具调用的任务，可以尝试使用 Code Mode，例如：

* 需要在许多文件中重复进行的更改
* 需要在 Claude 读取之前先过滤结果的搜索
* 可以同时运行的多个独立命令

### Code Mode 的限制

在启用 Code Mode 之前，请确认您可以接受以下限制：

* **恢复会话**：只能在终端中、并且在 Code Mode 开启的情况下恢复 Code Mode 会话
* **自动模式**：自动模式的分类器[审查的是代码，而不是每个工具调用](#permission-checks)
* **长时间运行的代码**：除非[代码可以在后台运行](#long-running-code)，否则您需要等待代码运行完成，并且代码会在十分钟后停止
* **Hook**：当 `PreToolUse` hook 未能完成时（例如超时后），您可能会看到[工具调用被拒绝](#tool-call-refused-by-a-hook)
* **不可用的功能**：无法使用 [Remote Control](https://code.claude.com/docs/zh-CN/remote-control.md)、[Claude in Chrome](https://code.claude.com/docs/zh-CN/chrome.md) 或[计算机使用](https://code.claude.com/docs/zh-CN/computer-use.md)
* **移动会话**：无法将会话移到 Desktop 应用，也无法将其转为[后台会话](https://code.claude.com/docs/zh-CN/agent-view.md)，并且 `/fork` 无法启动后台副本

## 要求

* **版本**：Claude Code v2.1.323 或更高版本，任一[发布频道](https://code.claude.com/docs/zh-CN/setup.md#configure-release-channel)均可。旧版本会在不启用 Code Mode 的情况下启动，可能附带也可能不附带原因 `it isn't open to your account yet`
* **账户**：Claude 订阅或 Console 账户。无法通过网关、Amazon Bedrock、Claude Platform on AWS、Google Cloud 的 Agent Platform、Microsoft Foundry 或 [Claude Models on Google Cloud (Anthropic managed)](https://code.claude.com/docs/zh-CN/claude-models-on-google-cloud-anthropic-managed.md) 使用 Code Mode
* **组织**：您的组织未使用 [HIPAA 配置](https://code.claude.com/docs/zh-CN/hipaa-setup.md)或[零数据保留](https://code.claude.com/docs/zh-CN/zero-data-retention.md)
* **模型**：Claude Opus 5.5、Sonnet 5.5、Haiku 5.5 或 Fable 5.2
* **使用入口**：终端中的交互式 `claude` 会话。Code Mode 不适用于 VS Code 面板、Desktop 应用或云端会话
* **Agent teams**：要在开启 [agent teams](https://code.claude.com/docs/zh-CN/agent-teams.md) 的情况下使用 Code Mode，需要 v2.1.326 或更高版本。在默认的[进程内显示模式](https://code.claude.com/docs/zh-CN/agent-teams.md#choose-a-display-mode)下，队友以 Code Mode 运行；在分屏窗格中，队友则在不启用 Code Mode 的情况下启动
* **Mods**：要在使用 hook 工具调用的 [mod](https://code.claude.com/docs/zh-CN/plugins/mods/overview.md) 时使用 Code Mode，需要 v2.1.327 或更高版本。如果您使用的是 `stable` 频道，且更新未达到该版本，请[切换到 `latest`](https://code.claude.com/docs/zh-CN/setup#configure-release-channel)
* **遥测设置**：要在[功能标志获取关闭](https://code.claude.com/docs/zh-CN/env-vars.md#features-that-need-feature-flag-fetching)或 [OpenTelemetry](https://code.claude.com/docs/zh-CN/monitoring-usage.md) 事件和指标开启的情况下使用 Code Mode，需要 v2.1.329 或更高版本。在任何版本上都请保持[追踪](https://code.claude.com/docs/zh-CN/monitoring-usage.md#traces-beta)关闭
* **安装**：Claude Code 的[原生构建版本](https://code.claude.com/docs/zh-CN/setup.md)
* **Windows**：已安装 [Git for Windows](https://git-scm.com/downloads/win)

此外，在某些设置开启时也无法启动 Code Mode，例如 API 密钥助手。有关每种情况的解决方法，请参阅 [Code Mode 无法启动](#code-mode-doesnt-start)。

## 试用 Code Mode

启用 Code Mode，给 Claude 一个任务，然后查看 Claude 编写的代码。

**1. 检查您的版本**

运行 `claude --version`。如果版本低于 v2.1.323，请运行 `claude update`。如果您使用的是 `stable` 频道，且更新后未达到 v2.1.323，请等待 `stable` 跟进，或[切换到 `latest`](https://code.claude.com/docs/zh-CN/setup#configure-release-channel)。

**2. 在开启 Code Mode 的情况下启动 Claude Code**

将 [`CLAUDE_CODE_EXPERIMENTAL_CODE_MODE`](https://code.claude.com/docs/zh-CN/env-vars#variables) 环境变量设置为 `1`。如需试用 Code Mode，请在 shell 中设置它。如需为每个新会话启用 Code Mode，请在用户设置中设置它。

> [tab] macOS, Linux, WSL
>
> ```bash theme={null}
> CLAUDE_CODE_EXPERIMENTAL_CODE_MODE=1 claude
> ```

> [tab] Windows PowerShell
>
> ```powershell theme={null}
> $env:CLAUDE_CODE_EXPERIMENTAL_CODE_MODE = "1"
> claude
> ```

> [tab] settings.json
>
> 将此 `env` 块保存到 `~/.claude/settings.json` 中，然后启动 `claude`：
>
> ```json theme={null}
> {
>   "env": {
>     "CLAUDE_CODE_EXPERIMENTAL_CODE_MODE": "1"
>   }
> }
> ```
>
> Claude Code [会忽略项目设置文件中的此变量](https://code.claude.com/docs/zh-CN/settings-reference.md#variables-claude-code-ignores-in-env)，因此您克隆的仓库无法替您启用 Code Mode。

**3. 确认您要使用 Code Mode**

在您的第一个 Code Mode 会话之前，Claude Code 会要求您确认。选择 **Yes, turn on Code Mode**。Claude Code 会重新启动，并在会话顶部附近显示以下这行内容：

```text theme={null}
Code Mode (experimental) is on · this session can be resumed only with Code Mode on
```

如果您看到的是其他内容或没有看到这行内容，请参阅 [Code Mode 无法启动](#code-mode-doesnt-start)。

**4. 给 Claude 一个需要大量工具调用的任务**

在您熟悉的项目中，发送如下提示词：

```text theme={null}
Read every Markdown file in this project and list the links that point to local files that don't exist.
```

**5. 阅读 Claude 编写的代码**

按 `Ctrl+O` 并展开一个 **Code** 行，查看工具调用背后的 JavaScript。再次按 `Ctrl+O` 返回对话。

> [!WARNING]
>
> 如需稍后恢复 Code Mode 会话，请在运行 `claude --continue` 或 `claude --resume` 时保持 `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE` 设置为 `1`。如果 Code Mode 处于关闭状态，Claude Code 会拒绝恢复该会话。在未启用 Code Mode 的情况下启动的会话，即使设置了该变量，也会在不启用 Code Mode 的情况下恢复。

### 关闭 Code Mode

从 shell 和 `~/.claude/settings.json` 中移除 `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE`，然后启动新会话。您也可以保留该变量，并在任一位置将其值改为 `0`。只要其中一处为 `0`，即使另一处设置为 `1`，Code Mode 也会保持关闭。

### 为您的组织禁用 Code Mode

将值为 `0` 的 `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE` 添加到您的[托管设置](https://code.claude.com/docs/zh-CN/managed-settings.md)中，这样您组织中的任何人都无法使用 Code Mode：

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_CODE_MODE": "0"
  }
}
```

正处于 Code Mode 会话中的用户会继续留在该会话中，直到他们退出或重新启动 Claude Code。此后，用户将在不启用 Code Mode 的情况下启动，并且在 `0` 生效期间无法恢复其 Code Mode 会话。您无法通过托管设置为用户启用 Code Mode。

### 使用 OpenTelemetry 监控 Code Mode

如果您收集 [OpenTelemetry 事件](https://code.claude.com/docs/zh-CN/monitoring-usage.md#events)，您的后端会收到 Claude 所编写代码中的工具调用对应的 `tool_decision` 和 `tool_result` 事件，这些事件使用各工具的常规名称，例如 `Bash`。请针对这些调用更新您的查询和设置：

* **查找来自代码的调用**：筛选以 `repl_` 或 `toolu_cc_` 开头的 `tool_use_id` 值。运行代码的 `REPL` 工具有其自身的事件，这些事件不带上述任一前缀
* **读取分类器判定结果**：在自动模式下，由分类器[对代码的审查](#permission-checks)所涵盖的调用没有 `classifier_verdict`。请在具有该调用 `request_id` 的 `REPL` 工具 `tool_decision` 事件上查找判定结果。如果找到多个，这些事件不会显示是哪一段代码发起了该调用
* **避免机密信息进入您的后端**：代码可以读取某个值（例如文件中的令牌），并将其传递给另一个调用。如果您的后端不应接收这些值，请不要设置 `OTEL_LOG_TOOL_DETAILS`

## 权限与长时间运行的代码

您的权限模式决定了 Claude 编写的代码如何被检查，以及代码运行期间您能否与 Claude 交谈。

### 权限检查

在自动模式和 `bypassPermissions` 模式下，代码可以从头到尾运行而不出现权限提示。某些调用仍会提示您，例如[任何模式都不会自动批准的操作](https://code.claude.com/docs/zh-CN/permission-modes.md#actions-no-mode-auto-approves)。

代码中的每个工具调用都会以该工具的常用名称（例如 `Bash` 或 [MCP 工具的名称](https://code.claude.com/docs/zh-CN/permissions.md#mcp)）经过您的 `deny` 和 `ask` [权限规则](https://code.claude.com/docs/zh-CN/permissions.md)以及 [`PreToolUse` hook](https://code.claude.com/docs/zh-CN/hooks#pretooluse)。除了规则和 hook 之外，在自动模式下，分类器会审查代码；在会进行询问的模式下，您需要回复提示：

* **[自动模式](https://code.claude.com/docs/zh-CN/permission-modes.md#eliminate-prompts-with-auto-mode)**：分类器会在每段代码运行之前对其进行审查，而不是审查每个工具调用。它看不到运行时计算出的值，例如从搜索输出中获取的路径，因此对于必须加以控制的调用，请保留规则或 hook。对于某些调用，您仍可能[收到提示](#permission-prompt-with-a-countdown)，例如在分类器多次阻止后由您亲自批准的代码中的调用
* **其他[权限模式](https://code.claude.com/docs/zh-CN/permission-modes.md)**：对于在该模式下会提示您的每个工具调用，您都会收到提示

如果您有一个允许或阻止 shell 命令的 `PreToolUse` hook，请让它检查命令的每个部分，就像 [Bash 规则所做的那样](https://code.claude.com/docs/zh-CN/permissions.md#compound-commands)。在 Code Mode 中，在名为 `app` 的文件夹中执行的 `git push` 可能会以 `cd 'app' && git push` 的形式到达您的 hook。

如需检查代码本身，请编写一个匹配 `REPL`（运行代码的工具）的 `PreToolUse` hook，并从 `tool_input.code` 中读取 JavaScript。如需检查代码返回的内容，请参阅[使用 hook 检查代码输出](#check-code-output-with-a-hook)。

> [!WARNING]
>
> Bash 规则匹配的是命令文本，因此无论是否使用 Code Mode，Claude 都可以[以规则不匹配的形式](https://code.claude.com/docs/zh-CN/permissions.md#bash-rule-limits)运行被拒绝的命令。如需不依赖命令文本的限制，请参阅[沙箱隔离](https://code.claude.com/docs/zh-CN/sandboxing.md)。

#### 要求对某个命令进行批准

如需在自动模式或 `bypassPermissions` 模式下针对特定命令显示提示，请为其添加一条 `ask` 规则。对于[该规则所匹配的命令形式](https://code.claude.com/docs/zh-CN/permissions.md#bash-rule-limits)，您会收到提示。如需在运行以 `git push` 开头的命令时收到提示，请将以下规则保存到 `~/.claude/settings.json` 中：

```json theme={null}
{
  "permissions": {
    "ask": ["Bash(git push *)"]
  }
}
```

如需测试该规则，请在一个没有远程仓库的仓库中以自动模式启动新会话，然后让 Claude 运行 `git push origin main`。您会看到针对该命令的提示。

#### 先批准每段代码

如需在代码开始运行之前阅读并批准代码，请为 `REPL`（运行代码的工具）添加一条 `ask` 规则。将以下规则保存到 `~/.claude/settings.json` 中：

```json theme={null}
{
  "permissions": {
    "ask": ["REPL"]
  }
}
```

如需测试该规则，请启动新会话并给 Claude 一个任务。您会看到一个不包含代码的提示。如需在回复之前阅读代码，请按 `Ctrl+O`，展开 **Code** 行，然后再次按 `Ctrl+O` 返回。在主对话中，您无法在该视图中看到[子代理](https://code.claude.com/docs/zh-CN/sub-agents.md)的代码。

如果您在自动模式下批准，即使分类器本会阻止该代码，代码也会开始运行，并且其项目编辑和只读命令会在没有提示的情况下运行。如果 Claude 报告代码无法启动子代理，请移除该规则。

#### 在代码运行时回复权限提示

如需在代码的某个工具调用的提示处停止代码，请回答 **No** 且不附加评论。以下结果适用于未标注为来自子代理的提示：

* **No 或 `Esc`**：代码停止，已完成的调用所做的更改保持不变
* **No 并附加[评论](https://code.claude.com/docs/zh-CN/permissions.md#add-a-comment-when-you-answer-a-permission-prompt)**：该调用被拒绝，代码可以继续执行其其他调用

### 使用沙箱限制 shell 命令

您的[沙箱](https://code.claude.com/docs/zh-CN/sandboxing.md)设置适用于代码所运行的 shell 命令。JavaScript 本身及其文件、网络和 MCP 工具调用在[沙箱之外](https://code.claude.com/docs/zh-CN/sandboxing.md#what-runs-outside-the-sandbox)运行。如需同时隔离 JavaScript 和这些调用，请在[容器或虚拟机](https://code.claude.com/docs/zh-CN/sandbox-environments.md)中运行 Claude Code。

如需在代码请求以非沙箱方式运行命令时仍将这些命令保留在沙箱中，请开启[严格沙箱模式](https://code.claude.com/docs/zh-CN/sandboxing.md#turn-off-the-retry-with-strict-sandbox-mode)。在自动模式下，分类器会审查发出该请求的代码，而该命令不会单独接受审查。

### 长时间运行的代码

当代码运行耗时较长的构建或测试时，Claude 要么等待它完成，要么让它在后台继续运行：

* **等待**：Claude 在代码完成后才回复，代码会在十分钟后停止。在 Manual 和 `acceptEdits` [模式](https://code.claude.com/docs/zh-CN/permission-modes.md#available-modes)下，您在工具权限提示上花费的时间不计入这十分钟。在 v2.1.328 之前，这段时间会被计入。
* **后台**：您可以继续与 Claude 交谈，代码最多可以运行两个小时

如需在后台运行代码，请以自动模式或 `bypassPermissions` 模式启动会话。如果 Claude 仍然在等待，请检查您当前的模式以及启动会话的方式：

* **您切换到了其他模式**：按 `Shift+Tab`，直到回到您启动时所用的模式
* **您以其他模式启动**：如果您可以[使用自动模式](https://code.claude.com/docs/zh-CN/permission-modes.md#eliminate-prompts-with-auto-mode)，请退出，然后在 Code Mode 开启的情况下运行 `claude --continue --permission-mode auto`
* **您使用的是 v2.1.328 之前的版本，并从 `claude --resume` 列表中选择了该会话**：请退出，[更新 Claude Code](https://code.claude.com/docs/zh-CN/setup.md#update-claude-code)，然后在 Code Mode 开启的情况下运行相同的 `claude --resume` 命令。如需保持当前版本，请将 `--resume` 替换为 `--continue`
* **您向 `--tools` 传递了工具名称**：以自动模式重新启动，不使用该标志

### 停止正在运行的代码

如需在 Claude 正在回复或等待代码时停止代码，请按 `Esc`。如需在 Claude 完成回复后停止后台代码，请在会话中运行 [`/tasks`](https://code.claude.com/docs/zh-CN/commands)，选择正在运行的任务，然后按 `x`。

停止代码后，请在 `/tasks` 中检查由该代码启动且仍在运行的[子代理](https://code.claude.com/docs/zh-CN/sub-agents.md)、[shell 命令](https://code.claude.com/docs/zh-CN/interactive-mode.md#background-bash-commands)和 [MCP 调用](https://code.claude.com/docs/zh-CN/mcp.md#automatic-backgrounding-of-long-tool-calls)。如需停止其中某一项，请选择它并按 `x`。

### 使用 hook 检查代码输出

如需检查代码返回的内容或对其进行脱敏，请编写一个匹配 `REPL`（运行代码的工具）的 [`PostToolUse` hook](https://code.claude.com/docs/zh-CN/hooks#posttooluse)。同一个 hook 也会在[后台代码](#long-running-code)完成时以及代码抛出错误时运行。

#### 在 hook 中读取代码输出

在您的 `PostToolUse` hook 中，从 `tool_response` 中读取输出，其中包含如下字段：

```json theme={null}
{
  "code": "(await $`cat notes.txt`.text())",
  "result": "deploy token: abc123",
  "stdout": "",
  "stderr": "",
  "toolsUsed": ["Bash"]
}
```

#### 对代码输出进行脱敏

如需隐藏部分输出，请将修改后的 `tool_response` 副本作为 [`updatedToolOutput`](https://code.claude.com/docs/zh-CN/hooks#posttooluse-decision-control) 返回，并按以下方式构建该副本：

* **修改文本**：对 `result`、`stdout`、`stderr` 和 `error` 进行脱敏。需处理 `result` 缺失或为 `null` 的情况，并且仅在代码失败或被停止时才会出现 `error`
* **保持结构**：以字符串形式返回 `code`、`stdout` 和 `stderr`，并以字符串形式返回 `error` 或将其省略。如果破坏了此结构，Claude 会获得原始输出
* **移除图片和 PDF**：如果副本中有需要隐藏的 `images` 或 `documents`，请将该字段设置为 `[]`

如需隐藏 `notes.txt` 结果中的部署令牌，请输出以下 JSON：

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "updatedToolOutput": {
      "code": "(await $`cat notes.txt`.text())",
      "result": "deploy token: REDACTED",
      "stdout": "",
      "stderr": "",
      "toolsUsed": ["Bash"]
    }
  }
}
```

如需测试该 hook，请创建一个包含您的 hook 会脱敏的值的文件。然后启动一个 Code Mode 会话，让 Claude 读取并引用该文件。输入路径时不要加 `@`，并检查 Claude 的回复是否显示了您的替换文本。

> [!WARNING]
>
> 不要依赖此 hook 来隐藏被拒绝的工具调用输入中的值，例如 Bash 命令。`refusedCalls` 字段可能会重复该输入，而 Claude 会原样读取它。

#### 在 hook 进行阻止或遇到错误时进行脱敏

即使您的 hook 进行了阻止或遇到错误，也要将修改后的 `tool_response` 副本作为 `updatedToolOutput` 返回：

* **您的 hook 进行阻止**：在与 [`"decision": "block"`](https://code.claude.com/docs/zh-CN/hooks#posttooluse-decision-control) 相同的 JSON 中输出[脱敏后的副本](#redact-code-output)。如果没有该副本，Claude 仍会读取原始输出
* **您的 hook 遇到错误**：捕获该错误，并输出一个在您脱敏的字段中填入占位文本的副本。如果 hook 崩溃、超时或输出无效的 JSON，Claude 会获得原始输出

#### 从 `UserPromptSubmit` hook 迁移检查

如果您在 [`UserPromptSubmit` hook](https://code.claude.com/docs/zh-CN/hooks#userpromptsubmit) 中检查代码输出，请将该检查移至您的 `PostToolUse` hook。在 v2.1.328 或更高版本中，`UserPromptSubmit` hook 不会接收代码输出，即使管理员在[托管设置](https://code.claude.com/docs/zh-CN/managed-settings.md)中设置了它们也是如此。

## 故障排除

### Code Mode 无法启动

会话顶部附近出现 `Code Mode (experimental) isn't available` 表示 Claude Code 在未启用 Code Mode 的情况下启动。原因显示在同一行中，`/status` 也会显示该原因。在下表中找到对应原因，进行相应更改，然后启动新会话。如果原因未在表中列出，请检查[要求](#requirements)。

| 原因包含 | 解决方法 |
| :- | :- |
| `it isn't open to your account in this version` 或 `it isn't open to your account yet` | 如果您的版本低于 v2.1.323，请[更新](#try-code-mode)。否则，请检查网络连接并重新启动。如果该原因仍然存在，请改日再试 |
| `Anthropic has turned it off for now` | [更新 Claude Code](https://code.claude.com/docs/zh-CN/setup.md#update-claude-code)，或稍后重新启动 |
| `it only works directly with the Anthropic API` 或 `it only works with the Anthropic API` | 移除通过云提供商、网关或自定义 `ANTHROPIC_BASE_URL` 路由请求的设置 |
| `it doesn't work with an API key helper` | 移除 `apiKeyHelper`、`ANTHROPIC_AUTH_TOKEN`，以及 `ANTHROPIC_CUSTOM_HEADERS` 中的任何 `Authorization` 或 `X-Api-Key` 标头。然后登录或设置 `ANTHROPIC_API_KEY` |
| `it only works with Opus 5.5, Sonnet 5.5 and later models` | 使用[受支持的模型](#requirements)启动，例如使用 `--model opus`。Haiku 5.5 和 Fable 5.2 也可以使用 |
| `it doesn't work in background jobs` | 在前台启动，不使用 `--remote-control`。如果该原因显示在队友的分屏窗格中，请使用[进程内显示模式](https://code.claude.com/docs/zh-CN/agent-teams.md#choose-a-display-mode)，以在 Code Mode 中运行队友 |
| `it needs settings that Claude Code downloads from Anthropic` | 将 [Claude Code 更新](https://code.claude.com/docs/zh-CN/setup.md#update-claude-code)以满足[遥测设置要求](#requirements)。如需继续使用当前版本，请取消设置[关闭功能标志获取](https://code.claude.com/docs/zh-CN/env-vars.md#features-that-need-feature-flag-fetching)的变量，例如 `DISABLE_TELEMETRY` |
| `OpenTelemetry tracing is on` | 如果您不需要[追踪](https://code.claude.com/docs/zh-CN/monitoring-usage.md#traces-beta)，请取消设置 `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA`、`ENABLE_ENHANCED_TELEMETRY_BETA` 和 `ENABLE_BETA_TRACING_DETAILED` |
| `OpenTelemetry is on` | 如需保持事件和指标启用，请[更新 Claude Code](https://code.claude.com/docs/zh-CN/setup.md#update-claude-code)并满足[遥测设置要求](#requirements)。如需继续使用当前版本，且您不需要 [OpenTelemetry 导出](https://code.claude.com/docs/zh-CN/monitoring-usage.md)，请取消设置 `CLAUDE_CODE_ENABLE_TELEMETRY` 和 `ENABLE_BETA_TRACING_DETAILED` |
| `it doesn't yet work with the plugin` | 将 [Claude Code 更新](https://code.claude.com/docs/zh-CN/setup.md#update-claude-code)以满足 [mod 要求](#requirements)。如需继续使用当前版本，请运行 `/plugin`，并禁用原因中指出的每个插件。如果某个插件是由您的组织启用的，请让您的管理员将其关闭 |
| `it doesn't yet work with an installed mod` | 将 [Claude Code 更新](https://code.claude.com/docs/zh-CN/setup.md#update-claude-code)以满足 [mod 要求](#requirements)。如需继续使用当前版本，请运行 `/plugin`，并禁用您安装的每个 mod |
| `it can't be used together with agent teams yet` | 如需保持 agent team 启用，请将 [Claude Code 更新](https://code.claude.com/docs/zh-CN/setup.md#update-claude-code)到 v2.1.326 或更高版本。如需继续使用当前版本，请取消设置 `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS` |
| `this launch's tool options` | 不使用 `--restricted` 启动，将 `REPL` 添加到 `--tools`，并从 `--disallowedTools` 和您的 `deny` 规则中移除 `REPL` |
| `couldn't save your answer` | 使 `~/.claude.json` 可写 |
| `your organization's settings don't allow it` | 向您的管理员咨询相关[托管设置](#block-code-mode-for-your-organization) |

如果您没有看到任何关于 Code Mode 的行，请运行 `claude --version`。如果您的版本低于 v2.1.323，请进行更新。然后检查 shell 或用户设置中的 `CLAUDE_CODE_EXPERIMENTAL_CODE_MODE` 是否为 `1`，并从这些位置以及任何 `--settings` 文件中移除所有 `0`。

### 带倒计时的权限提示

在自动模式下，如果您在[分类器多次阻止](https://code.claude.com/docs/zh-CN/permission-modes.md#when-auto-mode-falls-back)后自行批准代码，系统可能会就该代码以及仍在运行的先前代码中的工具调用询问您。在未连接 IDE 的情况下，提示可能会显示倒计时：

```text theme={null}
Claude Code will automatically block this request in 1:59, to avoid holding up an unattended session
```

请在倒计时结束前作答。否则该调用将被拒绝，并且之后本应显示倒计时的调用将在不提示的情况下被拒绝。如需再次看到这些提示，请向 Claude 发送一条消息。

在 v2.1.327 之前，在 Claude 启动新代码后，即使分类器允许了新代码，您也可能会被询问正在运行的代码中剩余的调用。如需减少此类提示，请将 [Claude Code 更新](https://code.claude.com/docs/zh-CN/setup.md#update-claude-code)到 v2.1.327 或更高版本。

### 工具调用被 hook 拒绝

如果 Claude 报告工具调用被拒绝，请让它提供错误文本。以下错误表示您的 [`PreToolUse` hook](https://code.claude.com/docs/zh-CN/hooks#pretooluse) 未给出决定：

* **`the hook did not finish`**：您的 hook 超时，或者您的 Agent hook 在未给出决定的情况下结束。发生超时后，请增大该 hook 的 [`timeout`](https://code.claude.com/docs/zh-CN/hooks#common-fields)。对于未给出决定的 Agent hook，请将检查移至 `command` hook。您可能会在来自代码的调用上看到此错误，也可能在 Claude 于会话中运行代码后的其他工具调用上看到此错误
* **`the hook failed`**：对于来自代码的调用，您的 hook 无法启动、被终止、以 126、127 或大于 128 的代码退出，或者返回了 HTTP 错误或无效输出。请修复该 hook。您可能会在 v2.1.329 之前的版本中看到此错误。在更高版本中，此错误很少见：其中一个原因是在 Claude 运行代码后，[功能标志获取](https://code.claude.com/docs/zh-CN/env-vars.md#features-that-need-feature-flag-fetching)在会话期间被关闭

在 v2.1.329 或更高版本中，当发生 `the hook did not finish` 以外的 hook 失败后，来自代码的调用默认会继续运行。如需选择是否运行该调用，请使用 `command` 或 `http` hook，并在其上设置 [`onFailure`](https://code.claude.com/docs/zh-CN/hooks#block-the-action-when-a-hook-fails)：

* **在超时或失败后阻止调用**：设置 `"onFailure": "block"`。对于用于把关调用的 hook，请这样设置
* **在超时或失败后允许调用运行**：设置 `"onFailure": "continue"`

### 代码输出被 hook 拦截

如果您预期看到代码输出，却在 Claude 的回复中看到 `UserPromptSubmit operation blocked by hook`，则表示您的 [`UserPromptSubmit`](https://code.claude.com/docs/zh-CN/hooks#userpromptsubmit) hook 将该输出作为提示词接收并阻止了它。如果 Claude 只报告了该 hook 的原因，请让它引用其收到的消息。

在 v2.1.328 或更高版本中，`UserPromptSubmit` hook 不会接收代码输出。如需在更早的版本上让输出通过，请更新 Claude Code 或修改该 hook：

* **更新**：如果您依赖该 hook 检查代码输出，请先[将检查移至 `PostToolUse` hook](#check-code-output-with-a-hook)。然后将 [Claude Code 更新](https://code.claude.com/docs/zh-CN/setup.md#update-claude-code)到 v2.1.328 或更高版本
* **继续使用当前版本**：修改该 hook，使其在输入中的 `source` 为 `poll_event` 时不进行阻止

## 相关资源

* [权限模式](https://code.claude.com/docs/zh-CN/permission-modes.md)：将自动模式与会提示您的模式进行比较
* [Hooks 参考](https://code.claude.com/docs/zh-CN/hooks.md)：编写 `PreToolUse` 和 `PostToolUse` hook
* [托管设置](https://code.claude.com/docs/zh-CN/managed-settings.md)：在整个组织中应用统一配置
