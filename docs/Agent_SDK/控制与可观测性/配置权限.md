> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 配置权限

> 使用权限模式、hooks 和声明式允许/拒绝规则来控制您的代理如何使用工具。

Claude Agent SDK 提供权限控制来管理 Claude 如何使用工具。使用权限模式和规则来定义自动允许的内容，并使用 [`canUseTool` 回调](https://code.claude.com/docs/zh-CN/agent-sdk/user-input) 处理仍需批准的调用。

## 权限如何被评估

> [!NOTE]
>
> 如果您加载的插件包含 [mod](https://code.claude.com/docs/zh-CN/plugins/mods/overview.md)，请参阅 [mod 的决定在规则和 hook 之间的位置](https://code.claude.com/docs/zh-CN/permissions.md#precedence-among-rules-hooks-and-mods)。

当 Claude 请求一个工具时，Claude Code 会在以下步骤中检查该调用。每个步骤都可以对调用作出决定、将其发送到您的 `canUseTool` 回调，或将其传递下去：

**1. Hooks**

运行 [hook](https://code.claude.com/docs/zh-CN/agent-sdk/hooks.md)。hook 可以直接拒绝该调用，也可以将其放行。返回 `allow` 的 hook 不会跳过拒绝规则和询问规则步骤，无论 hook 结果如何，这些步骤都会被评估。

返回 `allow` 的 `PreToolUse` hook 也不能批准目标被 Claude Code 识别为 [关键路径](https://code.claude.com/docs/zh-CN/permission-modes.md#critical-paths) 的 `rm` 或 `rmdir` 命令，例如 `rm -rf ~`。关于该 `allow` 在计划模式下的作用，请参阅 [计划模式下的 hook 批准](https://code.claude.com/docs/zh-CN/permissions.md#hook-approvals-in-plan-mode)。

**2. 拒绝规则**

如果来自 `disallowed_tools` 或 [SDK 加载的设置文件](#rules-in-settings-files) 的拒绝规则匹配，调用将被拒绝，且不会调用 [`canUseTool`](https://code.claude.com/docs/zh-CN/agent-sdk/user-input)。即使在 [`bypassPermissions`](#bypass-permissions-mode-bypasspermissions) 模式下、即使 hook 返回了 `allow`，调用也会以这种方式被拒绝。

**3. 询问规则**

检查来自 [settings.json](https://code.claude.com/docs/zh-CN/settings-reference.md#permission-settings) 的 `ask` 规则。如果询问规则匹配，调用会传递到您的 [`canUseTool` 回调](https://code.claude.com/docs/zh-CN/agent-sdk/user-input) 以获得确认，即使在 `bypassPermissions` 模式下也是如此。

需要用户交互的工具行为相同。`AskUserQuestion` 以及其服务器设置了 [`_meta["anthropic/requiresUserInteraction"]`](https://code.claude.com/docs/zh-CN/mcp#require-approval-for-a-specific-tool) 的 MCP 工具会传递到回调，即使允许规则匹配也是如此。在 `dontAsk` 模式下，这两种情况都会被拒绝，因为该模式会将每个权限提示转为拒绝。MCP 注解需要 Claude Code v2.1.199 或更高版本。

您的组织设置为 `ask` 的 [claude.ai connector](https://code.claude.com/docs/zh-CN/mcp.md#organization-controls-on-connector-tools) 工具也在此步骤离开流程。每个调用都传递到回调，即使在 `bypassPermissions` 模式下，即使当允许规则匹配时也是如此。回调接收原因 `Your organization requires approval for this tool`。在 `dontAsk` 模式下，调用被拒绝，因为该模式从不提示。

在 TypeScript SDK 中，如果您将自定义工具的 `permission_policy` 设置为 [`always_ask`](https://code.claude.com/docs/zh-CN/agent-sdk/custom-tools#require-approval-for-specific-tools)，任何允许规则都不会批准其调用，即使是 `allowedTools` 条目也不行。在 `dontAsk` 模式下，Claude Code 会拒绝这些调用；在 `auto`、`plan` 或 `bypassPermissions` 模式下，它[可以在您的回调运行之前批准它们](https://code.claude.com/docs/zh-CN/agent-sdk/typescript.md#permission-modes-that-can-approve-an-always_ask-call)。

**4. 权限模式**

应用活跃的 [权限模式](#permission-modes)：

* 在 `bypassPermissions` 模式下，Claude Code 批准到达此步骤的每个调用，除非它属于 [任何模式都不会自动批准的操作](https://code.claude.com/docs/zh-CN/permission-modes.md#actions-no-mode-auto-approves)。关于其中哪些操作会发送到您的 `canUseTool` 回调，请参阅 [绕过权限模式](#bypass-permissions-mode-bypasspermissions)。
* 在 `acceptEdits` 模式下，Claude Code 批准 [接受编辑模式](#accept-edits-mode-acceptedits) 下列出的文件操作。
* 在 `plan` 模式下，部分调用会到达您的回调；当自动模式可用时，其他调用则会转到其分类器。有关更多信息，请参阅 [计划模式](#plan-mode-plan)。
* 在 `default` 和 `dontAsk` 模式下，调用会继续进入允许规则。
* 关于 `auto` 模式，请参阅 [自动模式](#auto-mode-auto)。

**5. 允许规则**

检查 `allow` 规则（来自 `allowed_tools` 和 settings.json）。如果规则匹配，工具被批准。工具自己批准的调用也在此步骤被解决，无需规则：例如在您的工作目录内的文件读取或 [只读 Bash 命令](https://code.claude.com/docs/zh-CN/permissions.md#read-only-commands)。

被识别出的 [关键路径删除](https://code.claude.com/docs/zh-CN/permission-modes.md#critical-paths) 不会被允许规则批准，被标记为 `Dangerous rm operation not ruled out` 的命令也不会被 `Bash` 或 `Bash(*)` 规则批准。它们是否随后到达您的回调取决于权限模式：例如在 `auto` 模式的 Agent SDK 会话中，Claude Code 默认拒绝它们而不调用它。[关键路径模式表](https://code.claude.com/docs/zh-CN/permission-modes.md#critical-path-removals-in-each-permission-mode) 列出了每种模式对它们的处理方式。

允许规则不会批准从[网络路径](https://code.claude.com/docs/zh-CN/permissions.md#network-paths)进行的读取。

**6. canUseTool 回调**

如果前面的步骤都未能解决该请求，则调用您的 [`canUseTool` 回调](https://code.claude.com/docs/zh-CN/agent-sdk/user-input)来做出决定。在 `dontAsk` 模式下，此步骤会被跳过，工具将被拒绝，不过您安装的 [mod](https://code.claude.com/docs/zh-CN/plugins/mods/overview.md) 仍可以批准[某些此类调用](https://code.claude.com/docs/zh-CN/permissions.md#precedence-among-rules-hooks-and-mods)。

在 TypeScript SDK 中，如果您设置了 [`permissionPrompts: 'none'`](https://code.claude.com/docs/zh-CN/agent-sdk/typescript#options)，您的回调在此步骤不会被调用。[`PermissionRequest` hook](https://code.claude.com/docs/zh-CN/hooks#permissionrequest) 仍然有机会决定，如果它不决定，Claude Code 拒绝调用。该选项需要 Claude Code v2.1.259 或更高版本。

![六步权限评估流程的图表，与上述步骤匹配：工具请求通过 hooks、拒绝规则、询问规则、权限模式、允许规则和 canUseTool。Hooks、拒绝规则和 canUseTool 可以路由到被阻止；权限模式绕过、允许规则和 canUseTool 可以路由到执行；询问规则路由到 canUseTool。](https://mintcdn.com/claude-code/jYgs7qigNjO1Badj/images/agent-sdk/permissions-flow.svg?fit=max\&auto=format\&n=jYgs7qigNjO1Badj\&q=85\&s=c771ad9085b1277d3708027a49c744bc)

如果您在 TypeScript SDK 期望评估顺序在咨询回调之前自动批准调用的配置中传递 `canUseTool` 回调，SDK 在构造查询时会发出一次 Node.js 进程警告。警告的代码是 `CLAUDE_SDK_CAN_USE_TOOL_SHADOWED`。两个配置会触发它：

* `permissionMode: 'bypassPermissions'`：警告文本以 `canUseTool will not be invoked: permissionMode 'bypassPermissions'` 开头。工具调用在咨询 `canUseTool` 之前就已被批准，因此您的回调只会针对少数调用运行，例如 [绕过权限模式](#bypass-permissions-mode-bypasspermissions) 下列出的调用。若也要检查已批准的调用，请将回调中的检查放入 [`PreToolUse` hook](https://code.claude.com/docs/zh-CN/agent-sdk/hooks)
* 仅为工具名称的 `allowedTools` 条目，例如 `"Read"`：警告会在 `canUseTool will not be invoked for:` 之后列出每个此类条目。对所列工具的调用在咨询 `canUseTool` 之前就已被批准，[允许规则从不批准的调用](#calls-an-allow-rule-never-approves) 除外。若要让您的回调针对所列工具中需要批准的调用运行，请从 `allowedTools` 中删除该工具的条目

带有说明符的条目，如 `Bash(ls *)` 和 `acceptEdits` 模式不会触发它，来自设置文件的允许规则对检查不可见。

该警告不会阻止任何调用，也不会更改任何选项。如果您的回调已经能收到您想检查的每个调用，请保持配置不变。要记录该警告，请使用 `process.on('warning', ...)` 监听并匹配 `CLAUDE_SDK_CAN_USE_TOOL_SHADOWED` 代码。

此页面重点关注 **允许和拒绝规则** 和 **权限模式**。对于其他步骤：

* **Hooks：** 运行自定义代码以允许、拒绝或修改工具请求。请参阅 [使用 hooks 控制执行](https://code.claude.com/docs/zh-CN/agent-sdk/hooks.md)。
* **canUseTool 回调：** 在运行时提示用户批准，当没有更早的步骤解决调用时。请参阅 [处理批准和用户输入](https://code.claude.com/docs/zh-CN/agent-sdk/user-input.md)。

## 允许和拒绝规则

当您设置 `allowedTools` 和 `disallowedTools`（TypeScript）或 `allowed_tools` 和 `disallowed_tools`（Python）时，Claude Code 会将其中的条目添加到[权限评估流程](#how-permissions-are-evaluated)中的允许和拒绝规则列表。任何其他未在 `allowed_tools` 中列出的工具仍然可供 Claude 使用，对其的调用如果需要批准，则会进入权限模式。

| 选项 | 效果 |
| :- | :- |
| `allowed_tools=["Read", "Grep"]` | `Read` 和 `Grep` 被自动批准，[从网络路径读取](https://code.claude.com/docs/zh-CN/permissions.md#network-paths)除外。此处未列出的其他工具仍然存在，对它们的调用如果需要批准，则会进入权限模式和 `canUseTool`。 |
| `disallowed_tools=["Bash"]` | `Bash` 工具定义从请求中移除。 |
| `disallowed_tools=["Bash(rm *)"]` | `Bash` 保持可用。匹配 `rm *` [如所写](https://code.claude.com/docs/zh-CN/permissions.md#bash-rule-limits) 的调用在每种权限模式中都被拒绝，包括 `bypassPermissions`。其他 `Bash` 调用（包括 `/bin/rm`）会进入权限模式。 |
| `disallowed_tools=["*"]` | 拒绝规则中支持工具名称通配符：`"*"` 匹配每个工具，`"mcp__*"` 匹配所有服务器中的每个 MCP 工具。 |

允许规则仅在字面 `mcp__<server>__` 前缀之后接受工具名称通配符。服务器段必须无通配符，以便规则命名您配置的特定服务器：`mcp__puppeteer__*` 匹配来自 `puppeteer` 服务器的每个工具，`mcp__github__get_*` 匹配其 `get_` 工具。未锚定的条目（如 `allowed_tools=["*"]` 或 `allowed_tools=["mcp__*"]`）会被忽略，不会自动批准任何内容。

> [!WARNING]
>
> **自动批准的工具永远不会到达 `canUseTool`。** 在任何早期步骤中被批准的工具调用，通过 `acceptEdits` 或 `bypassPermissions`，或通过允许规则，会跳过你的 `canUseTool` 回调，因此你在那里放置的权限检查会被该工具无声地绕过。
>
> 如果对 `allowed_tools` 中某个工具的调用仍然到达您的 `canUseTool` 回调，或在 `dontAsk` 模式中被拒绝，请检查它们是否属于[从网络路径读取](https://code.claude.com/docs/zh-CN/permissions.md#network-paths)或以下调用之一。任何允许规则都不会批准这些调用。在从不提示的 `dontAsk` 模式中，Claude Code 会拒绝它们而不调用 `canUseTool`；在其他权限模式中，请按照各项说明处理它们：
>
> * `AskUserQuestion`、标记为 [`_meta["anthropic/requiresUserInteraction"]`](https://code.claude.com/docs/zh-CN/mcp#require-approval-for-a-specific-tool) 的 MCP 工具，以及[您的组织设置为 `ask`](https://code.claude.com/docs/zh-CN/mcp#organization-controls-on-connector-tools) 的连接器工具：在回调中应答它们。[处理澄清问题](https://code.claude.com/docs/zh-CN/agent-sdk/user-input.md#handle-clarifying-questions)展示了如何应答 `AskUserQuestion`，而连接器调用到达时附带的原因为 `Your organization requires approval for this tool`
>
> * 您的应用程序标记为 [`always_ask`](https://code.claude.com/docs/zh-CN/agent-sdk/custom-tools#require-approval-for-specific-tools) 的自定义工具：在回调中对该调用作出决定。要阻止这些调用到达，请[在会话中途更改策略](https://code.claude.com/docs/zh-CN/agent-sdk/typescript.md#mcpsdkserverconfigwithinstance)。在 `auto`、`plan` 和 `bypassPermissions` 模式中，该调用也可能在回调之前被批准，具体情况列于[可以批准 `always_ask` 调用的权限模式](https://code.claude.com/docs/zh-CN/agent-sdk/typescript#permission-modes-that-can-approve-an-always_ask-call)
>
> * 被识别出的 `rm` 和 `rmdir` [关键路径移除](https://code.claude.com/docs/zh-CN/permission-modes.md#critical-paths)：在 `default`、`acceptEdits` 和 `bypassPermissions` 模式中，在回调中允许或拒绝该移除操作，此时 [`decisionReason`](https://code.claude.com/docs/zh-CN/agent-sdk/typescript#canusetool) 以 `Dangerous rm` 开头。对于 `auto` 和 `plan` 模式，请参阅[各权限模式中的关键路径移除](https://code.claude.com/docs/zh-CN/permission-modes.md#critical-path-removals-in-each-permission-mode)
>
> * **裸名称**：像 `Read` 或 `mcp__github__get_issue` 这样的条目会自动批准对该工具的每个调用，[任何模式都不自动批准的操作](https://code.claude.com/docs/zh-CN/permission-modes.md#actions-no-mode-auto-approves)和[从网络路径读取](https://code.claude.com/docs/zh-CN/permissions.md#network-paths)除外。
>
> * **限定规则**：像 `Bash(npm test *)` 这样的条目会自动批准与其匹配的调用，其他需要批准的 `Bash` 调用会进入权限模式。
>
> 要检查由允许规则、`acceptEdits` 或 `bypassPermissions` 批准的调用，请使用 [`PreToolUse` hook](https://code.claude.com/docs/zh-CN/agent-sdk/hooks)，它也会针对这些调用运行。hook 拒绝即使在 `bypassPermissions` 模式中也适用。

对于锁定的代理，将 `allowedTools` 与 `permissionMode: "dontAsk"` 配对：

```typescript theme={null}
const options = {
  allowedTools: ["Read", "Glob", "Grep"],
  permissionMode: "dontAsk"
};
```

列出的 `Read`、`Glob` 和 `Grep` 调用被批准，[任何模式都不自动批准的操作](https://code.claude.com/docs/zh-CN/permission-modes.md#actions-no-mode-auto-approves)和[从网络路径读取](https://code.claude.com/docs/zh-CN/permissions.md#network-paths)除外。每个其他会提示的调用则会被拒绝，不过您安装的 [mod](https://code.claude.com/docs/zh-CN/plugins/mods/overview.md) 仍然可以批准[其中的部分调用](https://code.claude.com/docs/zh-CN/permissions.md#precedence-among-rules-hooks-and-mods)。

在 `default` 模式中不需要批准的调用会运行，无论您是否列出它们。其中包括[只读 Bash 命令](https://code.claude.com/docs/zh-CN/permissions.md#read-only-commands)、不在运行前询问的 `Agent` 等工具，以及工作目录内的文件读取。要对 Claude 完全隐藏某个内置工具而不是拒绝其调用，请将其裸名称添加到 `disallowedTools`。

> [!WARNING]
>
> **`allowed_tools` 不限制 `bypassPermissions`。** `allowed_tools` 预批准您列出的工具。在 `bypassPermissions` 模式中，Claude Code 会批准对未列出工具的调用，除非该调用属于[任何模式都不自动批准的操作](https://code.claude.com/docs/zh-CN/permission-modes.md#actions-no-mode-auto-approves)。
>
> 如果您将 `allowed_tools=["Read"]` 与 `permission_mode="bypassPermissions"` 一起设置，Claude Code 仍然会批准对 `Bash`、`Write` 和 `Edit` 等工具的调用。如果您需要 `bypassPermissions` 但想要阻止特定工具，请使用 `disallowed_tools`。关于在此模式中仍会到达您的 `canUseTool` 回调的调用，请参阅[绕过权限模式](#bypass-permissions-mode-bypasspermissions)。

你也可以在 `.claude/settings.json` 中声明式地配置允许、拒绝和询问规则。当启用 `project` 设置源时会读取这些规则，默认 `query()` 选项就是这样。如果你显式设置 `setting_sources`（TypeScript：`settingSources`），请包含 `"project"` 以使其应用。请参阅[权限设置](https://code.claude.com/docs/zh-CN/settings-reference.md#permission-settings)了解规则语法。

关于项目 `.claude/settings.json` 中的允许规则何时生效，请参阅[项目允许规则和工作区信任](https://code.claude.com/docs/zh-CN/permissions.md#project-allow-rules-and-workspace-trust)。

### 规则中的路径模式

`Read` 和 `Edit` 的限定规则采用路径模式。`Edit(path)` 规则管理所有写入文件的内置工具，包括 `Write` 和 `NotebookEdit`，因此对其中任何一个工具编写路径规则时，都请写成 `Edit(path)`。如果您将路径规则写成 `Write(path)` 或 `NotebookEdit(path)`，它[不会匹配任何调用](https://code.claude.com/docs/zh-CN/permissions.md#path-rules-that-never-match)，也不会产生任何效果。

在 `allowed_tools` 和 `disallowed_tools` 中，路径模式以 `//` 开头表示绝对路径，以单个 `/` 开头表示会话工作目录内的路径：

* **`//path`**：使用 `Edit(//secrets/**)` 的拒绝规则时，Claude Code 会阻止 Claude 的文件工具以及 [`tee` 和 `> file` 重定向等 Bash 命令](https://code.claude.com/docs/zh-CN/permissions#what-read-and-edit-rules-cover)写入磁盘上 `/secrets` 下的内容。Claude 运行的、自行打开文件的脚本仍然可以写入 `/secrets` 下的内容。如需由操作系统强制执行，请参阅[配置沙箱化的 Bash 工具](https://code.claude.com/docs/zh-CN/sandboxing.md)。
* **`/path`**：`Edit(/secrets/**)` 匹配工作目录内的 `secrets` 目录。

关于路径模式的其他开头形式，请参阅 [Read 和 Edit 规则](https://code.claude.com/docs/zh-CN/permissions.md#read-and-edit)。

## 权限模式

权限模式为 Claude 使用工具的方式提供全局控制。您可以在调用 `query()` 时设置权限模式，也可以在流式会话期间动态更改。

在 Claude Code v2.1.302 或更高版本中，除非您设置了权限模式，或应用从其设置文件中的 [`permissions.defaultMode`](https://code.claude.com/docs/zh-CN/settings-reference#permissions-defaultmode) 获取了权限模式，否则应用会以 `default` 模式启动。在 `default` 模式下，对于任何需要批准的工具调用，除非您通过允许规则、hook、`canUseTool` 回调或权限提示工具批准它，否则 Claude Code 都会拒绝。如果工具调用被拒绝，请参阅 [`claude -p` 和 Agent SDK 运行中的工具调用被拒绝](https://code.claude.com/docs/zh-CN/permission-modes#which-mode-a-non-interactive-run-starts-in)。

### 可用模式

SDK 支持以下权限模式：

| 模式 | 描述 | 工具行为 |
| :- | :- | :- |
| `default` | 标准权限行为 | 没有基于模式的自动批准；需要批准且不匹配任何允许规则的调用会触发您的 `canUseTool` 回调 |
| `dontAsk` | 拒绝而不是提示 | 任何原本会提示的调用都会被拒绝，且不调用 `canUseTool`，不过您安装的 [mod](https://code.claude.com/docs/zh-CN/plugins/mods/overview.md) 仍可批准[其中部分调用](https://code.claude.com/docs/zh-CN/permissions.md#precedence-among-rules-hooks-and-mods)。由 `allowed_tools` 或 `settings.json` 允许规则批准的调用会运行，在 `default` 模式下无需批准的调用也会运行。某些调用，例如[从网络路径读取](https://code.claude.com/docs/zh-CN/permissions.md#network-paths)，即使 `allowed_tools` 或允许规则与其匹配也会被拒绝。完整列表请参阅[不询问模式](#don’t-ask-mode-dontask) |
| `acceptEdits` | 自动接受文件编辑 | 您的[工作目录](https://code.claude.com/docs/zh-CN/permissions.md#working-directories)内的文件编辑和[文件系统操作](#accept-edits-mode-acceptedits)（`mkdir`、`rm`、`mv` 等）会被自动批准 |
| `bypassPermissions` | 绕过权限检查 | 工具无需权限提示即可运行，但[任何模式都不会自动批准的操作](https://code.claude.com/docs/zh-CN/permission-modes.md#actions-no-mode-auto-approves)，以及在[云端会话](https://code.claude.com/docs/zh-CN/claude-code-on-the-web.md)之外您的应用程序[标记为 `always_ask`](https://code.claude.com/docs/zh-CN/agent-sdk/custom-tools#require-approval-for-specific-tools) 的自定义工具除外。请谨慎使用 |
| `plan` | 计划模式 | Claude 进行探索和规划。使用 Claude 的文件工具所做的编辑会交给您的 `canUseTool` 回调，即使某条允许规则与之匹配也是如此 |
| `auto` | 由模型分类的批准 | 模型分类器会审查 shell 命令和网络请求等操作，对其审查的每个操作予以允许或阻止。有关可用性和决策顺序，请参阅[自动模式](https://code.claude.com/docs/zh-CN/permission-modes.md#eliminate-prompts-with-auto-mode) |

> [!WARNING]
>
> **子代理继承：** 如果您的主会话处于[计划模式](https://code.claude.com/docs/zh-CN/permission-modes.md#analyze-before-you-edit-with-plan-mode)，那么即使某个子代理的 [`AgentDefinition`](https://code.claude.com/docs/zh-CN/agent-sdk/typescript#agentdefinition) 设置了 `permissionMode: "acceptEdits"`，它仍会在计划模式下运行。该子代理对您源文件的 `Edit` 和 `Write` 调用仍会交给您的 `canUseTool` 回调。计划模式同样适用于您定义的子代理，这样将工作交给子代理就无法绕过先审查计划这一步。
>
> 子代理会从主会话继承 `plan`、`acceptEdits`、`auto` 或 `bypassPermissions`；当主会话处于 `default` 或 `dontAsk` 模式时，子代理会以您设置的模式运行。即便如此，Claude Code 也永远不会应用 `"bypassPermissions"` 值，并且仅当该子代理[可以使用自动模式](https://code.claude.com/docs/zh-CN/permission-modes.md#eliminate-prompts-with-auto-mode)时才会应用 `"auto"` 值。`bypassPermissions` 这一例外需要 Claude Code v2.1.267 或更高版本。
>
> 子代理可能具有与主 Agent 不同的系统提示词和更少约束的行为，因此继承 `bypassPermissions` 会授予它们完全、自主的系统访问权限。[任何模式都不会自动批准的操作](https://code.claude.com/docs/zh-CN/permission-modes.md#actions-no-mode-auto-approves)仍然适用。

### 设置权限模式

您可以在启动查询时一次性设置权限模式，也可以在会话活动期间动态更改。

> [tab] 查询时
>
> 在创建查询时传入 `permission_mode`（Python）或 `permissionMode`（TypeScript）。
>
> ```python Python theme={null}
> import asyncio
> from claude_agent_sdk import query, ClaudeAgentOptions
>
>
> async def main():
>     async for message in query(
>         prompt="Help me refactor this code",
>         options=ClaudeAgentOptions(
>             permission_mode="default",  # Set the mode here
>         ),
>     ):
>         if hasattr(message, "result"):
>             print(message.result)
>
>
> asyncio.run(main())
> ```
>
> ```typescript TypeScript theme={null}
> import { query } from "@anthropic-ai/claude-agent-sdk";
>
> async function main() {
>   for await (const message of query({
>     prompt: "Help me refactor this code",
>     options: {
>       permissionMode: "default" // Set the mode here
>     }
>   })) {
>     if ("result" in message) {
>       console.log(message.result);
>     }
>   }
> }
>
> main();
> ```

> [tab] 流式传输期间
>
> 调用 `set_permission_mode()`（Python）或 `setPermissionMode()`（TypeScript）可在会话中途更改模式。新模式会立即对所有后续工具请求生效。这样您可以先采用严格限制，随着信任建立再放宽权限，例如在审查 Claude 的初始方案后切换到 `acceptEdits`。
>
> ```python Python theme={null}
> import asyncio
> from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions
>
>
> async def main():
>     async with ClaudeSDKClient(
>         options=ClaudeAgentOptions(
>             permission_mode="default",  # Start in default mode
>         )
>     ) as client:
>         await client.query("Help me refactor this code")
>
>         # Change mode dynamically mid-session
>         await client.set_permission_mode("acceptEdits")
>
>         # Process messages with the new permission mode
>         async for message in client.receive_response():
>             if hasattr(message, "result"):
>                 print(message.result)
>
>
> asyncio.run(main())
> ```
>
> ```typescript TypeScript theme={null}
> import { query } from "@anthropic-ai/claude-agent-sdk";
>
> async function main() {
>   const q = query({
>     prompt: "Help me refactor this code",
>     options: {
>       permissionMode: "default" // Start in default mode
>     }
>   });
>
>   // Change mode dynamically mid-session
>   await q.setPermissionMode("acceptEdits");
>
>   // Process messages with the new permission mode
>   for await (const message of q) {
>     if ("result" in message) {
>       console.log(message.result);
>     }
>   }
> }
>
> main();
> ```

### 模式详情

#### 接受编辑模式（`acceptEdits`）

自动批准文件操作，使 Claude 无需提示即可编辑代码。其他工具（例如不属于文件系统操作的 Bash 命令）仍需要常规权限。

**自动批准的操作：**

* 使用 Edit、Write 和 NotebookEdit 工具进行的文件编辑
* 文件系统命令：`mkdir`、`touch`、`rm`、`rmdir`、`mv`、`cp`、`sed`

两者都适用于工作目录或您添加的目录内的路径。在 Python 中使用 `add_dirs` 添加目录，在 TypeScript 中使用 `additionalDirectories` 添加。在 `acceptEdits` 模式下，当 Claude 执行以下操作时，Claude Code 不会自动批准该请求：

* 处理该范围之外的路径
* 写入[受保护的路径](https://code.claude.com/docs/zh-CN/permission-modes.md#protected-paths)
* 使用 `rm` 或 `rmdir` 删除 Claude Code 识别为[关键路径](https://code.claude.com/docs/zh-CN/permission-modes.md#critical-paths)的路径
* 运行带有例如选项、glob 或 `timeout 5`、`LANG=C` 前缀的 [`touch`](https://code.claude.com/docs/zh-CN/permission-modes#auto-approve-file-edits-with-acceptedits-mode)

**适用场景：** 您信任 Claude 的编辑并希望加快迭代速度，例如在原型开发期间或在隔离目录中工作时。

#### 不询问模式（`dontAsk`）

将任何权限提示转换为拒绝，且不调用 `canUseTool`，不过您安装的 [mod](https://code.claude.com/docs/zh-CN/plugins/mods/overview.md) 仍可批准[其中部分调用](https://code.claude.com/docs/zh-CN/permissions.md#precedence-among-rules-hooks-and-mods)。由 `allowed_tools`、`settings.json` 允许规则或 hook 预先批准的工具会正常运行。在 `default` 模式下无需批准的调用也会运行，例如在工作目录内读取文件以及调用 `Agent`。

以下调用即使匹配允许规则也会被拒绝：

* [您的组织设置为 `ask`](https://code.claude.com/docs/zh-CN/mcp#organization-controls-on-connector-tools) 的连接器工具
* 需要用户交互的工具，例如 `AskUserQuestion`，以及其服务器设置了 [`_meta["anthropic/requiresUserInteraction"]`](https://code.claude.com/docs/zh-CN/mcp#require-approval-for-a-specific-tool) 的 MCP 工具
* 您的应用程序将其 `permission_policy` 设置为 [`always_ask`](https://code.claude.com/docs/zh-CN/agent-sdk/custom-tools#require-approval-for-specific-tools) 的自定义工具
* [从网络路径读取](https://code.claude.com/docs/zh-CN/permissions.md#network-paths)
* 被识别出的[关键路径删除](https://code.claude.com/docs/zh-CN/permission-modes.md#critical-paths)

如果您的 `PreToolUse` hook 对被识别出的关键路径删除、从网络路径读取或对标记为 `always_ask` 的工具的调用返回 `allow`，该调用仍会被拒绝。识别这些删除操作的检查[可能会漏掉某些命令](https://code.claude.com/docs/zh-CN/permission-modes.md#critical-paths)。

**适用场景：** 您运行无头 Agent，并希望对每个原本会提示的调用进行硬性拒绝。

#### 绕过权限模式（`bypassPermissions`）

无需提示即可自动批准工具使用，但[任何模式都不会自动批准的操作](https://code.claude.com/docs/zh-CN/permission-modes.md#actions-no-mode-auto-approves)除外。hook 仍会执行，并可在需要时阻止操作。在 Linux 和 macOS 上，如果不在[可识别的沙箱](https://code.claude.com/docs/zh-CN/permission-modes.md#skip-all-checks-with-bypasspermissions-mode)中，无论是以 root 身份还是在 `sudo` 下，Claude Code 都会拒绝以此模式启动，查询会在第一轮之前失败。

> [!WARNING]
>
> 请极其谨慎地使用。在此模式下，Claude 拥有完全的系统访问权限。仅在您信任所有可能操作的受控环境中使用。
>
> `allowed_tools` 不会约束此模式，对您未列出的工具的调用也会被批准。以下控制措施仍然适用：
>
> * 拒绝规则、显式 `ask` 规则和 hook 会在模式检查之前进行评估，仍然可以阻止工具。
> * [您的组织设置为 `ask`](https://code.claude.com/docs/zh-CN/mcp#organization-controls-on-connector-tools) 的连接器工具、需要用户交互的工具、被识别出的[关键路径删除](https://code.claude.com/docs/zh-CN/permission-modes.md#critical-paths)，以及被标记为 [`Dangerous rm operation not ruled out`](https://code.claude.com/docs/zh-CN/permission-modes#dangerous-rm-operation-not-ruled-out) 的 Bash 命令仍会交给您的 `canUseTool` 回调处理。识别关键路径删除的检查[可能会漏掉某些命令](https://code.claude.com/docs/zh-CN/permission-modes.md#critical-paths)，您也可以[关闭关键路径删除提示](https://code.claude.com/docs/zh-CN/permission-modes.md#turn-off-the-critical-path-removal-prompt-in-bypasspermissions-mode)。在[云端会话](https://code.claude.com/docs/zh-CN/claude-code-on-the-web.md)之外，对您的应用程序[标记为 `always_ask`](https://code.claude.com/docs/zh-CN/agent-sdk/custom-tools#require-approval-for-specific-tools) 的自定义工具的调用也会交给该回调处理。
> * [跨会话消息传递保护措施](https://code.claude.com/docs/zh-CN/permission-modes.md#skip-all-checks-with-bypasspermissions-mode)仍然适用。

#### 计划模式（`plan`）

Claude 会探索代码库并制定计划。在规划期间，使用 Claude 的文件工具在[受保护路径](https://code.claude.com/docs/zh-CN/permission-modes.md#protected-paths)之外所做的编辑会交给您的 `canUseTool` 回调，即使某条允许规则与之匹配或 `PreToolUse` hook 返回 `allow` 也是如此。[`AskUserQuestion`](https://code.claude.com/docs/zh-CN/agent-sdk/user-input#handle-clarifying-questions) 调用也会交给您的回调，即使某条允许规则指定了该工具。

当[自动模式](https://code.claude.com/docs/zh-CN/permission-modes.md#eliminate-prompts-with-auto-mode)可用时，对于没有允许规则批准的以下调用，Claude Code 会在规划期间将其发送给[自动模式的分类器](https://code.claude.com/docs/zh-CN/permission-modes.md#analyze-before-you-edit-with-plan-mode)进行审查，而不是交给您的回调：

* Shell 命令
* 网页获取
* 网页搜索
* 对其服务器标记为只读的 MCP 工具的调用

此审查默认开启。要关闭它，请在传递给 `query()` 的 `settings` 选项中或在您的用户设置中将 [`useAutoModeDuringPlan`](https://code.claude.com/docs/zh-CN/settings-reference#useautomodeduringplan) 设置为 `false`。审查关闭时，网页搜索以及对标记为只读的 MCP 工具的调用会交给您的回调。

对于 shell 命令和网页获取，下表显示了每个调用是否会交给您的回调：

| 规划期间的调用 | 审查开启 | 审查关闭，或自动模式不可用 |
| :- | :- | :- |
| [只读](https://code.claude.com/docs/zh-CN/permissions.md#read-only-commands) shell 命令，例如 `ls` | 直接运行，不会交给您的回调 | 直接运行，不会交给您的回调 |
| 没有允许规则批准的其他任何 shell 命令（[关键路径删除](https://code.claude.com/docs/zh-CN/permission-modes.md#critical-paths)除外） | 交给分类器，由其批准或拒绝，不经过您的回调 | 交给您的回调 |
| 对[预先批准的文档域名](https://code.claude.com/docs/zh-CN/tools-reference.md#webfetch-tool-behavior)的 `WebFetch` 调用 | 直接运行，不会交给您的回调 | 直接运行，不会交给您的回调 |
| 没有允许规则批准的其他任何 `WebFetch` 调用 | 交给分类器，由其批准或拒绝，不经过您的回调 | 交给您的回调 |

有关分类器连续拒绝多个调用后会发生什么，请参阅[重复阻止阈值](https://code.claude.com/docs/zh-CN/permission-modes.md#repeated-block-thresholds)。

> [!NOTE]
>
> 在 TypeScript SDK 中，如果您在设置 `permissionMode: 'plan'` 的同时设置了 `allowDangerouslySkipPermissions: true`，文件编辑仍会交给您的 `canUseTool` 回调。要在之后通过 `setPermissionMode()` 将以计划模式启动的会话切换到 `bypassPermissions`，您需要从一开始就设置 `allowDangerouslySkipPermissions`。

**适用场景：** 您希望 Claude 先制定计划，例如在代码审查期间或进行大型更改之前。

#### 自动模式（`auto`）

分类器模型会在 shell 命令和网络请求等操作运行之前对其进行审查，并对其审查的每个操作予以允许或阻止。有关自动模式所需的模型和提供商，以及它评估操作的顺序，请参阅[使用自动模式消除权限提示](https://code.claude.com/docs/zh-CN/permission-modes.md#eliminate-prompts-with-auto-mode)。

如果您使用 [`set_model()`](https://code.claude.com/docs/zh-CN/agent-sdk/python#claudesdkclient)、[`setModel()`](https://code.claude.com/docs/zh-CN/agent-sdk/typescript#query-object) 或 [`applyFlagSettings()`](https://code.claude.com/docs/zh-CN/agent-sdk/typescript#applyflagsettings) 将处于自动模式的会话切换到自动模式不支持的模型，该会话会变为 `default` 模式：

* **您会看到**：一条子类型为 `status`、`permissionMode` 设置为 `"default"` 的 `system` 消息，TypeScript SDK 将其类型定义为 [`SDKStatusMessage`](https://code.claude.com/docs/zh-CN/agent-sdk/typescript#sdkstatusmessage)。此后，需要批准且不匹配任何允许规则的调用会交给您的 `canUseTool` 回调。
* **要返回自动模式**：切换到受支持的模型，然后调用 `set_permission_mode("auto")` 或 `setPermissionMode("auto")`。如果您将模型切换回来但没有进行该调用，会话将保持在 `default` 模式。当不受支持的模型处于活动状态时，该调用会失败并显示 `Cannot set permission mode to auto: auto mode unavailable for this model`。

在调用 `set_model()`、`setModel()` 或 `applyFlagSettings()` 后变为 `default` 模式的行为需要 Claude Code v2.1.299 或更高版本。

## 相关资源

有关权限评估流程中的其他步骤：

* [处理批准和用户输入](https://code.claude.com/docs/zh-CN/agent-sdk/user-input.md)：交互式批准提示和澄清问题
* [Hooks 指南](https://code.claude.com/docs/zh-CN/agent-sdk/hooks.md)：在代理生命周期中的关键点运行自定义代码
* [权限规则](https://code.claude.com/docs/zh-CN/settings-reference.md#permission-settings)：`settings.json` 中的声明式允许/拒绝规则
