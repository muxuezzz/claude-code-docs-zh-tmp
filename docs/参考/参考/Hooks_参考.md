> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Hooks 参考

> Claude Code hook 事件、配置架构、JSON 输入/输出格式、退出代码、异步 hooks、HTTP hooks、提示 hooks 和 MCP 工具 hooks 的参考。

<Tip>
  有关包含示例的快速入门指南，请参阅[使用 hooks 自动化工作流](/docs/zh-CN/hooks-guide)。
</Tip>

Hooks 是用户定义的 shell 命令、HTTP 端点、MCP 工具调用、LLM 提示或子代理，在 Claude Code 生命周期中的特定点自动执行。Claude Code 在其运行的任何地方都会触发相同的 hook 事件：终端中的会话、IDE 扩展、[桌面应用](/docs/zh-CN/desktop-quickstart)和[云会话](/docs/zh-CN/claude-code-on-the-web)。使用此参考查找事件架构、配置选项、JSON 输入/输出格式以及异步 hooks、HTTP hooks 和 MCP 工具 hooks 等高级功能。

<h2 id="hook-lifecycle">
  Hook 生命周期
</h2>

Claude Code 在会话期间的特定点运行 hooks。当事件触发且匹配器匹配时，Claude Code 会将关于该事件的 JSON 上下文传递给您的 hook 处理程序。对于命令 hooks，输入通过 stdin 到达。对于 HTTP hooks，它作为 POST 请求体到达。您的处理程序随后可以检查输入、采取行动并可选地返回决定。

事件分为三种频率：

* 每个会话一次：`SessionStart` 和 `SessionEnd`
* 每轮一次：`UserPromptSubmit`、`Stop` 和 `StopFailure`
* 代理循环内的每个工具调用：`PreToolUse` 和 `PostToolUse`，除了 [`EndConversation`](/docs/zh-CN/tools-reference#endconversation-tool-behavior) 调用，它们跳过两者

<div style={{maxWidth: "500px", margin: "0 auto"}}>
  <Frame>
    <img src="https://mintcdn.com/claude-code/x7pO8l4XcvAXCoVc/images/hooks-lifecycle.svg?fit=max&auto=format&n=x7pO8l4XcvAXCoVc&q=85&s=81b9256c1bbe8832553485f5d9e9c746" className="dark:hidden" alt="Hook 生命周期图，显示可选的 Setup 流入 SessionStart，然后是每轮循环，包含 UserPromptSubmit、用于 slash commands 的 UserPromptExpansion、嵌套的代理循环（PreToolUse、PermissionRequest、PostToolUse、PostToolUseFailure、PostToolBatch、SubagentStart/Stop、TaskCreated、TaskCompleted）和 Stop 或 StopFailure，然后是 TeammateIdle、PreCompact、PostCompact 和 SessionEnd，Elicitation 和 ElicitationResult 嵌套在 MCP 工具执行内，PermissionDenied 作为 PermissionRequest 的副分支用于自动模式拒绝，WorktreeCreate、WorktreeRemove、Notification、ConfigChange、InstructionsLoaded、CwdChanged、FileChanged 和 DirectoryAdded 作为独立异步事件，PreModelSwitch 作为独立顺序事件，在请求的模型切换之前运行，PostModelSwitch 作为独立异步事件，在会话的模型更改后运行，MessageDisplay 作为仅显示事件，在助手消息文本流式传输时运行" width="520" height="1336" data-path="images/hooks-lifecycle.svg" />

    <img src="https://mintcdn.com/claude-code/x7pO8l4XcvAXCoVc/images/hooks-lifecycle-dark.svg?fit=max&auto=format&n=x7pO8l4XcvAXCoVc&q=85&s=c9b3d88487335f58cce0b52e2f9e7531" className="hidden dark:block" alt="Hook 生命周期图，显示可选的 Setup 流入 SessionStart，然后是每轮循环，包含 UserPromptSubmit、用于 slash commands 的 UserPromptExpansion、嵌套的代理循环（PreToolUse、PermissionRequest、PostToolUse、PostToolUseFailure、PostToolBatch、SubagentStart/Stop、TaskCreated、TaskCompleted）和 Stop 或 StopFailure，然后是 TeammateIdle、PreCompact、PostCompact 和 SessionEnd，Elicitation 和 ElicitationResult 嵌套在 MCP 工具执行内，PermissionDenied 作为 PermissionRequest 的副分支用于自动模式拒绝，WorktreeCreate、WorktreeRemove、Notification、ConfigChange、InstructionsLoaded、CwdChanged、FileChanged 和 DirectoryAdded 作为独立异步事件，PreModelSwitch 作为独立顺序事件，在请求的模型切换之前运行，PostModelSwitch 作为独立异步事件，在会话的模型更改后运行，MessageDisplay 作为仅显示事件，在助手消息文本流式传输时运行" width="520" height="1336" data-path="images/hooks-lifecycle-dark.svg" />
  </Frame>
</div>

下表总结了每个事件何时触发。[Hook 事件](#hook-events)部分记录了每个事件的完整输入架构和决定控制选项。

| 事件 | 触发时机 |
| :- | :- |
| `SessionStart` | 当会话开始或恢复时 |
| `Setup` | 当你使用 `--init-only` 启动 Claude Code，或在 `-p` 模式下使用 `--init` 或 `--maintenance` 时。用于 CI 或脚本中的一次性准备 |
| `UserPromptSubmit` | 当你提交提示词时，在 Claude 处理之前 |
| `UserPromptExpansion` | 当用户输入的命令扩展为提示词时，在到达 Claude 之前。可以阻止扩展 |
| `PreToolUse` | 在工具调用执行之前。可以阻止它 |
| `PermissionRequest` | 当工具调用需要权限决策时 |
| `PermissionDenied` | 当自动模式拒绝工具调用时，包括没有分类器判决的拒绝。使用 JSON `hookSpecificOutput.retry: true` 来告诉模型它可以重试被拒绝的工具调用。Claude Code 在分类器未产生判决时忽略 `retry` |
| `PostToolUse` | 在工具调用成功后 |
| `PostToolUseFailure` | 在工具调用失败后 |
| `PostToolBatch` | 在一整批并行工具调用解决后，在下一次模型调用之前 |
| `Notification` | 当 Claude Code 发送通知时 |
| `MessageDisplay` | 当助手消息文本正在显示时 |
| `SubagentStart` | 当子代理被生成时 |
| `SubagentStop` | 当子代理完成时 |
| `TaskCreated` | 当通过 `TaskCreate` 创建任务时 |
| `TaskCompleted` | 当任务被标记为已完成时 |
| `Stop` | 当 Claude 完成响应时 |
| `StopFailure` | 当轮次因 API 错误而结束时 |
| `TeammateIdle` | 当[代理团队](/docs/zh-CN/agent-teams)队友即将空闲时 |
| `InstructionsLoaded` | 当 CLAUDE.md 或 `.claude/rules/*.md` 文件被加载到上下文中时。在会话开始时和文件在会话期间被延迟加载时触发 |
| `ConfigChange` | 当配置文件在会话期间更改时 |
| `CwdChanged` | 当工作目录更改时，例如当 Claude 执行 `cd` 命令时。对于使用 direnv 等工具的反应式环境管理很有用 |
| `DirectoryAdded` | 当工作目录在会话中期通过 `/add-dir` 或 SDK `register_repo_root` 控制请求添加时 |
| `FileChanged` | 当监视的文件在磁盘上更改时。`matcher` 字段指定要监视的文件名 |
| `WorktreeCreate` | 当通过 `--worktree`、`isolation: "worktree"` 创建工作树时，或用于后台会话。替换默认的 git 行为 |
| `WorktreeRemove` | 当在会话退出时、子代理完成时或删除后台会话时移除工作树 |
| `PreCompact` | 在上下文压缩之前 |
| `PostCompact` | 在上下文压缩完成后 |
| `PreModelSwitch` | 在 Claude Code 应用你或客户端请求的模型切换之前。可以阻止切换 |
| `PostModelSwitch` | 在会话的模型更改后，包括 Claude Code 自己进行的更改，例如在你恢复会话时恢复模型 |
| `Elicitation` | 当 MCP 服务器在工具调用期间请求用户输入时 |
| `ElicitationResult` | 在用户响应 MCP 引出后，在响应发送回服务器之前 |
| `SessionEnd` | 当会话终止时 |

<h3 id="how-a-hook-resolves">
  Hook 如何解析
</h3>

要了解事件、匹配器和处理程序如何组合在一起，请考虑这个 `PreToolUse` hook，它阻止破坏性 shell 命令。

<Tabs>
  <Tab title="macOS/Linux">
    `matcher` 缩小到 Bash 工具调用，`if` 条件进一步缩小到匹配 `rm *` 的 Bash 子命令，因此 `block-rm.sh` 仅在两个过滤器都匹配时生成：

    ```json theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Bash",
            "hooks": [
              {
                "type": "command",
                "if": "Bash(rm *)",
                "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-rm.sh",
                "args": []
              }
            ]
          }
        ]
      }
    }
    ```

    该脚本从 stdin 读取 JSON 输入，提取命令，如果包含 `rm -rf`，则返回 `permissionDecision` 为 `"deny"`。将其保存到项目中的 `.claude/hooks/block-rm.sh`，并使用 `chmod +x .claude/hooks/block-rm.sh` 使其可执行，以便 Claude Code 可以运行它：

    ```bash theme={null}
    #!/bin/bash
    # .claude/hooks/block-rm.sh
    COMMAND=$(jq -r '.tool_input.command')

    if echo "$COMMAND" | grep -q 'rm -rf'; then
      jq -n '{
        hookSpecificOutput: {
          hookEventName: "PreToolUse",
          permissionDecision: "deny",
          permissionDecisionReason: "Destructive command blocked by hook"
        }
      }'
    else
      exit 0  # no decision; normal permission flow applies
    fi
    ```

    此脚本与本页面上解析 JSON 输入的其他 Bash 示例一样，使用 `jq`，因此在尝试它们之前，请安装 `jq` 并确保它在您的 `PATH` 上。
  </Tab>

  <Tab title="Windows (PowerShell)">
    匹配器 `Bash|PowerShell` 涵盖 [PowerShell 工具](#powershell)以及 Bash。单个 `if` 规则仅匹配一个工具的调用，因此每个工具都有自己的处理程序：第一个缩小到匹配 `rm *` 的 Bash 子命令，第二个缩小到匹配 `Remove-Item *` 的 PowerShell 命令。两者都通过 `powershell.exe` 运行相同的脚本：

    ```json theme={null}
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Bash|PowerShell",
            "hooks": [
              {
                "type": "command",
                "if": "Bash(rm *)",
                "command": "powershell.exe",
                "args": [
                  "-NoProfile",
                  "-ExecutionPolicy",
                  "Bypass",
                  "-File",
                  "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-rm.ps1"
                ]
              },
              {
                "type": "command",
                "if": "PowerShell(Remove-Item *)",
                "command": "powershell.exe",
                "args": [
                  "-NoProfile",
                  "-ExecutionPolicy",
                  "Bypass",
                  "-File",
                  "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-rm.ps1"
                ]
              }
            ]
          }
        ]
      }
    }
    ```

    `-NoProfile` 标志跳过加载您的 PowerShell 配置文件，以便 hook 快速启动，`-ExecutionPolicy Bypass` 让 PowerShell 运行本地脚本文件。

    该脚本从 stdin 读取 JSON 输入，提取命令，如果包含 `rm -rf` 或 `Remove-Item` 后跟 `-Recurse`，则返回 `permissionDecision` 为 `"deny"`。将其保存到项目中的 `.claude/hooks/block-rm.ps1`：

    ```powershell theme={null}
    # .claude/hooks/block-rm.ps1
    $callInput = [Console]::In.ReadToEnd() | ConvertFrom-Json
    $command = $callInput.tool_input.command

    if ($command -match 'rm -rf|Remove-Item.*-Recurse') {
      @{
        hookSpecificOutput = @{
          hookEventName = "PreToolUse"
          permissionDecision = "deny"
          permissionDecisionReason = "Destructive command blocked by hook"
        }
      } | ConvertTo-Json
    } else {
      exit 0  # no decision; normal permission flow applies
    }
    ```
  </Tab>
</Tabs>

现在假设 Claude Code 决定针对 macOS/Linux 配置运行 `Bash "rm -rf /tmp/build"`。以下是发生的情况：

<Frame>
  <img src="https://mintcdn.com/claude-code/ikqp3_70mqIahteV/images/hook-resolution.svg?fit=max&auto=format&n=ikqp3_70mqIahteV&q=85&s=be0bf3053550c26de5f54cd64674c197" className="dark:hidden" alt="Hook 解析流程图：PreToolUse 触发，匹配器检查 Bash 匹配，然后 if 条件检查 Bash(rm *) 匹配。如果两者都匹配，hook 命令运行并返回 permissionDecision deny，因此工具调用被阻止，Claude Code 继续。如果任一检查未能匹配，hook 被跳过，工具调用被允许继续。" width="930" height="270" data-path="images/hook-resolution.svg" />

  <img src="https://mintcdn.com/claude-code/_xqph1dUOslCOwsj/images/hook-resolution-dark.svg?fit=max&auto=format&n=_xqph1dUOslCOwsj&q=85&s=e80af91f8507cee6bd51ac3c2dd92f63" className="hidden dark:block" alt="Hook 解析流程图：PreToolUse 触发，匹配器检查 Bash 匹配，然后 if 条件检查 Bash(rm *) 匹配。如果两者都匹配，hook 命令运行并返回 permissionDecision deny，因此工具调用被阻止，Claude Code 继续。如果任一检查未能匹配，hook 被跳过，工具调用被允许继续。" width="930" height="270" data-path="images/hook-resolution-dark.svg" />
</Frame>

<Steps>
  <Step title="事件触发">
    `PreToolUse` 事件触发。Claude Code 将工具输入作为 JSON 通过 stdin 发送到 hook：

    ```json theme={null}
    { "tool_name": "Bash", "tool_input": { "command": "rm -rf /tmp/build" }, ... }
    ```
  </Step>

  <Step title="匹配器检查">
    匹配器 `"Bash"` 与工具名称匹配，因此此 hook 组激活。如果您省略匹配器或使用 `"*"`，该组在事件的每次出现时激活。
  </Step>

  <Step title="If 条件检查">
    `if` 条件 `"Bash(rm *)"` 匹配，因为 `rm -rf /tmp/build` 是匹配 `rm *` 的子命令，因此此处理程序生成。如果命令是 `npm test`，`if` 检查会失败，`block-rm.sh` 永远不会运行，避免进程生成开销。`if` 字段是可选的；没有它，匹配组中的每个处理程序都运行。
  </Step>

  <Step title="Hook 处理程序运行">
    脚本检查完整命令并找到 `rm -rf`，因此它将决定打印到 stdout：

    ```json theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Destructive command blocked by hook"
      }
    }
    ```

    如果命令是更安全的 `rm` 变体，如 `rm file.txt`，脚本会改为执行 `exit 0`。退出代码 0 且无输出意味着 hook 没有决定要报告，因此工具调用继续通过正常的[权限流程](/docs/zh-CN/permissions)。hook 可以拒绝调用，但保持沉默不会批准它。
  </Step>

  <Step title="Claude Code 对结果采取行动">
    Claude Code 读取 JSON 决定，阻止工具调用，并向 Claude 显示原因。
  </Step>
</Steps>

下面的[配置](#configuration)部分记录了完整的架构，每个[hook 事件](#hook-events)部分记录了您的命令接收的输入以及它可以返回的输出。

<h2 id="configuration">
  配置
</h2>

Hooks 在 JSON 设置文件中定义。配置有三个嵌套级别：

1. 选择一个 [hook 事件](#hook-events) 来响应，如 `PreToolUse` 或 `Stop`
2. 添加一个 [匹配器组](#matcher-patterns) 来过滤何时触发，如"仅针对 Bash 工具"
3. 定义一个或多个 [hook 处理程序](#hook-handler-fields) 在匹配时运行

有关完整的演练和带注释的示例，请参阅上面的 [Hook 如何解析](#how-a-hook-resolves)。

<Note>
  本页对每个级别使用特定术语：**hook 事件**表示生命周期点，**匹配器组**表示过滤器，**hook 处理程序**表示运行的 shell 命令、HTTP 端点、MCP 工具、提示或代理。"Hook"本身指的是一般功能。
</Note>

<h3 id="hook-locations">
  Hook 位置
</h3>

定义 hook 的位置决定了其范围：

| 位置 | 范围 | 可共享 |
| :- | :- | :- |
| `~/.claude/settings.json` | 所有项目 | 否，仅限本地计算机 |
| `.claude/settings.json` | 单个项目 | 是，可以提交到仓库 |
| `.claude/settings.local.json` | 单个项目 | 否，当 Claude Code 保存设置时被 gitignored |
| 托管策略设置 | 组织范围 | 是，由管理员控制 |
| [Plugin](/docs/zh-CN/plugins/overview) `hooks/hooks.json` | 启用插件时 | 是，与插件捆绑 |
| [Skill](/docs/zh-CN/skills) frontmatter | 调用技能后的会话其余部分。请参阅 [Hooks in skills and agents](#hooks-in-skills-and-agents) | 是，在技能文件中定义 |
| [Subagent](/docs/zh-CN/sub-agents) frontmatter | 该子代理运行时 | 是，在子代理文件中定义 |

[云会话](/docs/zh-CN/claude-code-on-the-web) 不读取本地 `~/.claude/settings.json`。在 [自托管环境](/docs/zh-CN/self-hosted-environments-configuration#permissions-and-tool-approval) 中，Claude Code 还运行操作员从运行程序主机的 `~/.claude/` 中植入的 hooks，并在该文件属于 [Claude Code 应用的托管源](/docs/zh-CN/managed-settings#how-claude-code-combines-managed-sources) 时运行运行程序镜像的托管设置文件中的 hooks，这默认意味着仅当服务器托管设置和 MDM 交付的 Claude Code 策略都不提供托管层时。有关哪些设置文件和插件（以及因此哪些 hooks）到达云会话的信息，请参阅 [从设置中携带的内容](/docs/zh-CN/cloud-environments#what-carries-over-from-your-setup)。

有关设置文件解析的详细信息，请参阅 [settings](/docs/zh-CN/settings)。

来自设置文件、托管策略设置和插件的 Hooks 也在 [subagents](/docs/zh-CN/sub-agents) 内运行。当子代理调用工具时，工具事件（如 `PreToolUse` 和 `PostToolUse`）触发与主对话中相同的配置 hooks，输入包含标识子代理的 `agent_id` 和 `agent_type` [通用输入字段](#common-input-fields)。

管理员可以使用 [`allowManagedHooksOnly`](/docs/zh-CN/settings-reference#allowmanagedhooksonly) 在 [托管设置](/docs/zh-CN/managed-settings) 中限制哪些 hooks 运行：

* 用户、项目、本地和插件 hooks 被阻止。托管设置 `enabledPlugins` 中强制启用的插件中的 Hooks 除外
* Claude Code 还将 [`statusLine`](/docs/zh-CN/statusline)、[`fileSuggestion`](/docs/zh-CN/settings-reference#filesuggestion) 和 [`subagentStatusLine`](/docs/zh-CN/statusline#subagent-status-lines) 设置限制为托管设置
* Claude Code 还禁用具有 [`command` 源](/docs/zh-CN/plugins/marketplace-reference#command-plugin-source) 的插件，包括托管设置 `enabledPlugins` 中强制启用的插件，除非 [`disableCommandPluginSources`](/docs/zh-CN/settings-reference#disablecommandpluginsources) 明确设置为 `false`。`command` 源需要 Claude Code v2.1.229 或更高版本
* Claude Code 还阻止市场 [`headersHelper` 命令](/docs/zh-CN/plugins/host-marketplace#authenticate-archive-downloads)，除非 [`disableCommandPluginSources`](/docs/zh-CN/settings-reference#disablecommandpluginsources) 明确设置为 `false`，托管设置本身声明的市场除外

请参阅 [在 `allowManagedHooksOnly` 下运行的内容](/docs/zh-CN/settings-reference#what-runs-under-allowmanagedhooksonly)。

Hook 条目在设置级别之间合并而不是相互替换：用户、项目和本地设置添加自己的 hooks 而不删除托管的 hooks，[`disableAllHooks`](#disable-or-remove-hooks) 设置无法禁用来自托管设置外部的托管 hooks。

[HTTP hook 允许列表](/docs/zh-CN/settings-reference#hook-and-skill-settings) 适用于来自每个源的 hooks，包括托管策略设置：

* `allowedHttpHookUrls`：在任何设置级别定义时，Claude Code 仅在其 URL 与合并的允许列表匹配时运行 HTTP hook 处理程序
* `httpHookAllowedEnvVars`：定义时，Claude Code 仅将该列表上的环境变量插值到 hook 标头中

<h3 id="matcher-patterns">
  匹配器模式
</h3>

`matcher` 字段过滤何时触发 hooks。匹配器的评估方式取决于它包含的字符：

| 匹配器值 | 评估为 | 示例 |
| :- | :- | :- |
| `"*"`、`""` 或省略 | 匹配所有 | 在事件的每次出现时触发 |
| 仅字母、数字、`_`、`-`、空格、`,` 和 `\|` | 精确字符串或由 `\|` 或 `,` 分隔的精确字符串列表，可选周围空格 | `Bash` 仅匹配 Bash 工具；`Edit\|Write` 和 `Edit, Write` 各匹配任一工具；`code-reviewer` 仅匹配该代理类型 |
| 包含任何其他字符 | JavaScript 正则表达式，未锚定 | `^Notebook` 匹配任何名称以 `Notebook` 开头的工具；`mcp__memory__.*` 匹配来自 `memory` 服务器的每个工具 |

在正则表达式路径上的匹配器使用 JavaScript 的 `RegExp.prototype.test` 进行测试，该测试在值中任何位置的匹配时成功。`Edit.*` 匹配 `Edit` 和 `NotebookEdit`；当需要整个字符串匹配时，用 `^` 和 `$` 包装模式，如 `^Edit$`。

`FileChanged` 和 `StopFailure` 使用更窄的精确匹配集，仅包含字母、数字、`_` 和 `|`。这两个事件的匹配器中的连字符、空格或逗号将其保留在正则表达式路径上，仅 `|` 分隔替代项。下表中支持匹配器的其他每个事件接受 `|` 或 `,`。

`FileChanged` 事件在构建其监视列表时不遵循这些规则。请参阅 [FileChanged](#filechanged)。

每个事件类型在不同的字段上匹配：

| 事件 | 匹配器过滤的内容 | 示例匹配器值 |
| :- | :- | :- |
| `PreToolUse`、`PostToolUse`、`PostToolUseFailure`、`PermissionRequest`、`PermissionDenied` | 工具名称 | `Bash`、`Edit\|Write`、`mcp__.*` |
| `SessionStart` | 会话如何启动 | `startup`、`resume`、`clear`、`compact`、`fork` |
| `Setup` | 哪个 CLI 标志触发了设置 | `init`、`maintenance` |
| `SessionEnd` | 会话为什么结束 | `clear`、`resume`、`logout`、`prompt_input_exit`、`other` |
| `Notification` | 通知类型 | `permission_prompt`、`idle_prompt`、`auth_success`、`elicitation_dialog`、`elicitation_url_dialog`、`elicitation_complete`、`elicitation_response`、`agent_needs_input`、`agent_completed`、`quota_auto_resume_fired`、`quota_auto_resume_stale`、`quota_auto_resume_disabled` |
| `SubagentStart` | 代理类型 | `general-purpose`、`Explore`、`Plan`、自定义代理名称或插件范围的名称如 `^my-plugin:reviewer$` |
| `PreCompact`、`PostCompact` | 什么触发了压缩 | `manual`、`auto` |
| `PreModelSwitch`、`PostModelSwitch` | 会话切换到的模型的规范名称，如 [PreModelSwitch](#premodelswitch) 下所述 | `claude-opus-5`、`claude-opus-4-6\|claude-opus-5`、`.*opus.*` |
| `SubagentStop` | 代理类型 | 与 `SubagentStart` 相同的值 |
| `ConfigChange` | 配置源 | `user_settings`、`project_settings`、`local_settings`、`policy_settings`、`skills` |
| `CwdChanged` | 无匹配器支持 | 总是在每次出现时触发 |
| `DirectoryAdded` | 目录如何添加 | `slash_command`、`register_repo_root` |
| `FileChanged` | 要监视的文字文件名（请参阅 [FileChanged](#filechanged)） | `.envrc\|.env` |
| `StopFailure` | 错误类型 | `rate_limit`、`overloaded`、`authentication_failed`、`oauth_org_not_allowed`、`account_on_hold`、`billing_error`、`invalid_request`、`model_not_found`、`server_error`、`max_output_tokens`、`cloud_credential_error`、`unknown` |
| `InstructionsLoaded` | 加载原因 | `session_start`、`nested_traversal`、`path_glob_match`、`include`、`compact` |
| `UserPromptExpansion` | 命令名称 | 你的技能或命令名称 |
| `Elicitation` | MCP 服务器名称 | 你配置的 MCP 服务器名称 |
| `ElicitationResult` | MCP 服务器名称 | 与 `Elicitation` 相同的值 |
| `UserPromptSubmit`、`PostToolBatch`、`Stop`、`TeammateIdle`、`TaskCreated`、`TaskCompleted`、`WorktreeCreate`、`WorktreeRemove`、`MessageDisplay` | 无匹配器支持 | 总是在每次出现时触发 |

在 `cloud_credential_error` 上匹配 `StopFailure` 需要 Claude Code v2.1.267 或更高版本，这是第一个在该值下报告凭证加载失败而不是 `server_error` 或 `unknown` 的版本。

对于大多数事件，Claude Code 根据它在 stdin 上发送给 hook 的 [JSON 输入](#hook-input-and-output) 中的字段评估匹配器。对于工具事件，该字段是 `tool_name`。对于 `PreModelSwitch` 和 `PostModelSwitch`，Claude Code 根据它从 `to_model` 派生的规范名称评估匹配器，如 [PreModelSwitch](#premodelswitch) 下所述。每个 [hook 事件](#hook-events) 部分列出了完整的匹配器值集和该事件的输入架构。

此示例仅在 Claude 写入或编辑文件时运行 linting 脚本：

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/lint-check.sh"
          }
        ]
      }
    ]
  }
}
```

如果向不支持匹配器的事件添加 `matcher` 字段，它会被静默忽略。

对于工具事件，可以通过在单个 hook 处理程序上设置 [`if` 字段](#common-fields) 来更狭隘地过滤。`if` 使用 [权限规则语法](/docs/zh-CN/permissions) 来匹配工具名称和参数，因此 `"Bash(git *)"` 在任何 Bash 输入的子命令匹配 `git *` 时运行，`"Edit(*.ts)"` 仅对 TypeScript 文件运行。

<h4 id="match-mcp-tools">
  匹配 MCP 工具
</h4>

[MCP](/docs/zh-CN/mcp) 服务器工具在工具事件中显示为常规工具（`PreToolUse`、`PostToolUse`、`PostToolUseFailure`、`PermissionRequest`、`PermissionDenied`），因此可以像匹配任何其他工具名称一样匹配它们。

MCP 工具遵循命名模式 `mcp__<server>__<tool>`，例如：

* `mcp__memory__create_entities`：Memory 服务器的创建实体工具
* `mcp__filesystem__read_file`：Filesystem 服务器的读取文件工具
* `mcp__github__search_repositories`：GitHub 服务器的搜索工具

要匹配来自服务器的每个工具，请将 `.*` 附加到服务器前缀。`.*` 是必需的：像 `mcp__memory` 或 `mcp__brave-search` 这样的匹配器仅包含精确匹配字符，因此它被比较为精确字符串，不匹配任何工具。

* `mcp__memory__.*` 匹配来自 `memory` 服务器的所有工具
* `mcp__brave-search__.*` 匹配来自名称包含连字符的服务器的所有工具
* `mcp__.*__write.*` 匹配来自任何服务器的名称以 `write` 开头的任何工具

来自 [插件捆绑的 MCP 服务器](/docs/zh-CN/mcp#plugin-provided-mcp-servers) 的工具使用包含插件名称的范围服务器段：`mcp__plugin_<plugin-name>_<server-name>__<tool>`。针对裸服务器密钥编写的匹配器永远不会对这些工具触发。对于名为 `my-plugin` 的插件，在密钥 `db` 下捆绑服务器，`query` 工具显示为 `mcp__plugin_my-plugin_db__query`，因此来自该服务器的每个工具的匹配器是 `mcp__plugin_my-plugin_db__.*`。在处理程序的 [`if` 字段](#common-fields) 中使用相同的范围工具名称。有关如何构建范围名称的信息，请参阅 [插件提供的 MCP 服务器](/docs/zh-CN/mcp#plugin-provided-mcp-servers)。

此示例记录所有内存服务器操作并验证来自任何 MCP 服务器的写入操作：

```json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "mcp__memory__.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'Memory operation initiated' >> ~/mcp-operations.log"
          }
        ]
      },
      {
        "matcher": "mcp__.*__write.*",
        "hooks": [
          {
            "type": "command",
            "command": "/home/user/scripts/validate-mcp-write.py"
          }
        ]
      }
    ]
  }
}
```

<h3 id="hook-handler-fields">
  Hook 处理程序字段
</h3>

内部 `hooks` 数组中的每个对象都是一个 hook 处理程序：当匹配器匹配时运行的 shell 命令、HTTP 端点、MCP 工具、LLM 提示或代理。有五种类型：

* **[命令 hooks](#command-hook-fields)**（`type: "command"`）：运行 shell 命令。脚本在 stdin 上接收事件的 [JSON 输入](#hook-input-and-output)，并通过退出代码和 stdout 传回结果。
* **[HTTP hooks](#http-hook-fields)**（`type: "http"`）：将事件的 JSON 输入作为 HTTP POST 请求发送到 URL。端点通过响应体使用与命令 hooks 相同的 [JSON 输出格式](#json-output) 传回结果。
* **[MCP 工具 hooks](#mcp-tool-hook-fields)**（`type: "mcp_tool"`）：在已连接的 [MCP 服务器](/docs/zh-CN/mcp) 上调用工具。工具的文本输出被视为命令 hook stdout。
* **[提示 hooks](#prompt-and-agent-hook-fields)**（`type: "prompt"`）：向 Claude 模型发送提示以进行单轮评估。模型以 JSON 形式返回其决定。请参阅 [基于提示的 hooks](#prompt-based-hooks)。
* **[代理 hooks](#prompt-and-agent-hook-fields)**（`type: "agent"`）：生成一个子代理，可以使用 Read、Grep 和 Glob 等工具来验证条件，然后返回决定。代理 hooks 是实验性的，可能会改变。请参阅 [基于代理的 hooks](#agent-based-hooks)。

所有匹配的 hooks 并行运行。如果在多个设置文件中定义相同的处理程序，它运行一次。插件或技能的相同处理程序副本保持分离。

处理程序在当前目录中使用 Claude Code 的环境运行。如果当前目录不再存在，例如另一个 shell 在会话中途删除的 worktree 或临时目录，Claude Code 从以下第一个仍然存在的目录运行命令 hooks：会话启动的目录、项目根目录、主目录或系统临时目录。Claude Code 在 [调试日志](#debug-hooks) 中记录一条警告，命名回退目录。

`$CLAUDE_CODE_REMOTE` 环境变量在远程 web 环境中为 `"true"`，在本地 CLI 中未设置。Claude Code v2.1.199 及更高版本在本地会话具有活跃的 Remote Control 连接时将 [`$CLAUDE_CODE_BRIDGE_SESSION_ID`](/docs/zh-CN/env-vars) 设置为 [Remote Control](/docs/zh-CN/remote-control) 会话 ID。

<h4 id="common-fields">
  通用字段
</h4>

这些字段适用于所有 hook 类型：

| 字段 | 必需 | 描述 |
| :- | :- | :- |
| `type` | 是 | `"command"`、`"http"`、`"mcp_tool"`、`"prompt"` 或 `"agent"` |
| `if` | 否 | 权限规则语法来过滤此 hook 何时运行，如 `"Bash(git *)"` 或 `"Edit(*.ts)"`。hook 命令仅在工具调用与模式匹配时运行。有关 Bash 模式如何针对子命令、`$()` 和反引号评估的信息，请参阅下面的 [Bash 匹配表](#bash-if-matching)。仅在工具事件上评估：`PreToolUse`、`PostToolUse`、`PostToolUseFailure`、`PermissionRequest` 和 `PermissionDenied`。在其他事件上，设置了 `if` 的 hook 永远不会运行。使用与 [权限规则](/docs/zh-CN/permissions) 相同的语法 |
| `timeout` | 否 | 取消前的秒数。Claude Code 不在使用 [`async: true`](#run-hooks-in-the-background) 运行的命令 hook 上强制执行。默认值：`command`、`http` 和 `mcp_tool` 为 600；`prompt` 为 30；`agent` 为 60。Claude Code 在 [`UserPromptSubmit`](#userpromptsubmit)、[`PreModelSwitch`](#premodelswitch) 和 [`PostModelSwitch`](#postmodelswitch) 上将 `command`、`http` 和 `mcp_tool` 默认值降低到 30，在 [`MessageDisplay`](#messagedisplay) 上降低到 10。[`SessionEnd`](#sessionend) hooks 共享 1.5 秒的预算；如果设置设置了更长的每个 hook `timeout`，Claude Code 将预算提高到匹配，最多 60 秒 |
| `statusMessage` | 否 | hook 运行时显示的自定义微调器消息 |
| `once` | 否 | 如果为 `true`，Claude Code 在第一次成功运行后删除 hook。失败、以退出代码 2 阻止或超时的运行将 hook 保留在原位，因此它在下一个匹配事件上再次运行。仅对在 [技能 frontmatter](#hooks-in-skills-and-agents) 中声明的 hooks 有效；在设置文件和代理 frontmatter 中被忽略 |

`if` 字段恰好包含一个权限规则。没有 `&&`、`||` 或列表语法来组合规则；要应用多个条件，为每个定义一个单独的 hook 处理程序。

在文件工具的 `if` 条件中，单段目录模式如 `"Edit(src/**)"` 仅匹配工作目录中的 `src` 目录及其下的文件。要匹配工作目录下任何深度的名为 `src` 的目录，请写 `"Edit(**/src/**)"`。在 v2.1.214 之前，`"Edit(src/**)"` 匹配工作目录下任何深度的名为 `src` 的目录。

<span id="bash-if-matching" />对于 Bash 模式，hook 命令是否运行取决于模式的形状和 Claude 调用的 Bash 命令。在匹配前剥离前导 `VAR=value` 赋值。

| `if` 模式 | Bash 命令 | Hook 运行？ | 为什么 |
| :- | :- | :- | :- |
| `Bash(git *)` | `FOO=bar git push` | 是 | 前导赋值被剥离；`git push` 匹配 |
| `Bash(git *)` | `npm test && git push` | 是 | 每个子命令被检查；`git push` 匹配 |
| `Bash(rm *)` | `echo $(rm -rf /)` | 是 | `$()` 和反引号内的命令被检查；`rm -rf /` 匹配 |
| `Bash(rm *)` | `echo $(date)` | 否 | 没有子命令匹配 `rm *` |
| `Bash(cat *)` | `echo before $(date) after` | 否 | 替换可以位于任何参数位置，因此检查完整命令和 `date`；都不匹配 `cat *` |
| `Bash(git *)` | `$TOOL git push` | 是 | Claude Code 无法判断命令名称扩展到什么，因此它运行 hook |
| `Bash(git push *)` | `echo $(date)` | 是 | 指定超过命令名称的模式在 `$()`、反引号或 `$VAR` 上无论如何都运行 hook |

当 Claude Code 无法确定 Bash 输入运行哪些命令时，它无论模式如何都运行 hook。因为 `if` 过滤是尽力而为的，使用 [权限系统](/docs/zh-CN/permissions) 而不是 hook 来强制执行硬允许或拒绝。

<h4 id="command-hook-fields">
  命令 hook 字段
</h4>

除了 [通用字段](#common-fields)，命令 hooks 接受这些字段：

| 字段 | 必需 | 描述 |
| :- | :- | :- |
| `command` | 是 | 要执行的 shell 命令。使用 `args` 时，直接生成的可执行文件。请参阅 [Exec 形式和 shell 形式](#exec-form-and-shell-form) |
| `args` | 否 | 参数列表。存在时，`command` 被解析为可执行文件并直接使用 `args` 作为参数向量生成，不涉及 shell。请参阅 [Exec 形式和 shell 形式](#exec-form-and-shell-form) |
| `async` | 否 | 如果为 `true`，在后台运行而不阻止。请参阅 [在后台运行 hooks](#run-hooks-in-the-background) |
| `asyncRewake` | 否 | 如果为 `true`，在后台运行并在退出代码 2 时唤醒 Claude。hook 的 stderr 或 stdout（如果 stderr 为空）显示给 Claude 作为 [系统提醒](/docs/zh-CN/glossary#system-reminder)，以便它可以对长时间运行的后台失败做出反应 |
| `shell` | 否 | 用于此 hook 的 shell。接受 `"bash"` 或 `"powershell"`。默认为 `"bash"`，或在未安装 Git Bash 时在 Windows 上默认为 `"powershell"`。设置 `"powershell"` 在 Windows 上通过 PowerShell 运行命令。不需要 `CLAUDE_CODE_USE_POWERSHELL_TOOL`，因为 hooks 直接生成 PowerShell。设置 `args` 时被忽略 |

<a id="exec-form-and-shell-form" />

<h5 id="exec-form-and-shell-form">
  Exec 形式和 shell 形式
</h5>

当设置 `args` 时，命令 hook 以 exec 形式运行，当省略 `args` 时以 shell 形式运行。每当 hook 引用 [路径占位符](#reference-scripts-by-path) 时设置 `args`，因为每个元素作为一个参数传递，不带引号。当需要 shell 功能如管道或 `&&` 时省略 `args`，或当两个问题都不适用时。

**Exec 形式**在设置 `args` 时运行。Claude Code 在 `PATH` 上解析 `command` 作为可执行文件，并直接使用 `args` 作为参数向量生成它。没有 shell，因此每个 `args` 元素恰好是一个参数，完全按照编写的方式，路径占位符如 `${CLAUDE_PLUGIN_ROOT}` 被替换为 `command` 和每个 `args` 元素中的纯字符串。特殊字符如撇号、`$` 和反引号逐字传递，因为没有 shell 来解释它们。在任何平台上都不会发生 shell 标记化。

**Shell 形式**在省略 `args` 时运行。`command` 字符串被传递到 shell：在 macOS 和 Linux 上为 `sh -c`，在 Windows 上为 Git Bash，或在未安装 Git Bash 时为 PowerShell。设置 `shell` 字段来明确选择。shell 标记化字符串、扩展变量并解释管道、`&&`、重定向和 globs。

<Note>
  在 Windows 上，exec 形式需要 `command` 解析为真实可执行文件如 `.exe`。npm、npx、eslint 和其他工具在 `node_modules/.bin` 中安装的 `.cmd` 和 `.bat` 垫片不是可执行文件，不能在没有 shell 的情况下生成。要在 exec 形式中运行它们，直接使用 `node` 调用底层脚本，例如 `"command": "node", "args": ["${CLAUDE_PLUGIN_ROOT}/node_modules/eslint/bin/eslint.js"]`。`node` 加脚本路径模式在每个平台上都有效，因为 `node.exe` 是真实二进制文件。要按名称运行 `.cmd` 或 `.bat` 垫片，使用 shell 形式。
</Note>

此示例运行与插件捆绑的 Node 脚本。Exec 形式将解析的脚本路径作为一个参数传递，不带引号：

```json theme={null}
{
  "type": "command",
  "command": "node",
  "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/format.js", "--fix"]
}
```

等效的 shell 形式需要引号来处理带空格或特殊字符的路径：

```json theme={null}
{
  "type": "command",
  "command": "node \"${CLAUDE_PLUGIN_ROOT}\"/scripts/format.js --fix"
}
```

两种形式都支持相同的 [路径占位符](#reference-scripts-by-path)，并且都将它们导出为生成过程上的环境变量 `CLAUDE_PROJECT_DIR`、`CLAUDE_PLUGIN_ROOT` 和 `CLAUDE_PLUGIN_DATA`，因此脚本可以读取 `process.env.CLAUDE_PLUGIN_ROOT` 无论如何启动。

插件 hooks 另外替换 [`${user_config.*}`](/docs/zh-CN/plugins/manifest-reference#user-configuration) 值，仅在 exec 形式中：值被替换为 `command` 和每个 `args` 元素中的纯字符串，因此没有 shell 重新解析它。

shell 形式的插件 hook，其 `command` 引用 `${user_config.*}` 失败并出现 [错误](/docs/zh-CN/errors#plugin-command-references-user-config) 而不是运行。要从 shell 形式的 hook 使用选项值，读取 `$CLAUDE_PLUGIN_OPTION_<KEY>` 环境变量，如 `webhook_url` 选项的 `$CLAUDE_PLUGIN_OPTION_WEBHOOK_URL`，或设置 `args` 来将 hook 切换到 exec 形式。在 v2.1.207 之前，shell 形式的插件 hook 命令也替换 `${user_config.*}`。

<Note>
  在 exec 形式中，`command` 仅是可执行文件名或路径。如果 `command` 是没有路径分隔符的裸名称，并且与 `args` 一起包含空格，Claude Code 记录一条警告，因为生成将失败：没有名为 `node script.js` 的可执行文件。将额外的标记移到 `args` 中。带空格的绝对路径，如 `C:\Program Files\nodejs\node.exe`，是单个有效的可执行文件，不会触发警告。
</Note>

<h4 id="http-hook-fields">
  HTTP hook 字段
</h4>

除了 [通用字段](#common-fields)，HTTP hooks 接受这些字段：

| 字段 | 必需 | 描述 |
| :- | :- | :- |
| `url` | 是 | 发送 POST 请求的 URL |
| `headers` | 否 | 其他 HTTP 标头作为键值对。值支持使用 `$VAR_NAME` 或 `${VAR_NAME}` 语法的环境变量插值。仅解析 `allowedEnvVars` 中列出的变量 |
| `allowedEnvVars` | 否 | 可能被插值到标头值中的环境变量名称列表。对未列出变量的引用被替换为空字符串。任何环境变量插值都需要 |

Claude Code 将 hook 的 [JSON 输入](#hook-input-and-output) 作为 POST 请求体发送，`Content-Type: application/json`。响应体使用与命令 hooks 相同的 [JSON 输出格式](#json-output)。

错误处理与命令 hooks 不同；请参阅 [HTTP 响应处理](#http-response-handling)。

此示例将 `PreToolUse` 事件发送到本地验证服务，使用来自 `MY_TOKEN` 环境变量的令牌进行身份验证：

```json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "http",
            "url": "http://localhost:8080/hooks/pre-tool-use",
            "timeout": 30,
            "headers": {
              "Authorization": "Bearer $MY_TOKEN"
            },
            "allowedEnvVars": ["MY_TOKEN"]
          }
        ]
      }
    ]
  }
}
```

<h4 id="mcp-tool-hook-fields">
  MCP 工具 hook 字段
</h4>

除了 [通用字段](#common-fields)，MCP 工具 hooks 接受这些字段：

| 字段 | 必需 | 描述 |
| :- | :- | :- |
| `server` | 是 | 配置的 MCP 服务器的名称。对于 [插件捆绑的服务器](/docs/zh-CN/mcp#plugin-provided-mcp-servers)，这是范围名称 `plugin:<plugin-name>:<server-name>`，如 `plugin:my-plugin:db`，不是裸服务器密钥 |
| `tool` | 是 | 在该服务器上调用的工具的名称 |
| `input` | 否 | 传递给工具的参数。字符串值支持来自 hook 的 [JSON 输入](#hook-input-and-output) 的 `${path}` 替换，如 `"${tool_input.file_path}"` |

此示例在每个 `Write` 或 `Edit` 后在 `my_server` MCP 服务器上调用 `security_scan` 工具，传递编辑文件的路径：

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "mcp_tool",
            "server": "my_server",
            "tool": "security_scan",
            "input": { "file_path": "${tool_input.file_path}" }
          }
        ]
      }
    ]
  }
}
```

<h5 id="how-the-tool’s-result-is-read">
  工具结果如何被读取
</h5>

Claude Code 读取工具的文本内容的方式与读取命令 hook stdout 相同，遵循 [退出代码 0 下的解析规则](#exit-code-0)。如果工具返回 `isError: true`，hook 产生非阻止错误，执行继续。

<h5 id="when-the-server-is-still-connecting">
  当服务器仍在连接时
</h5>

在 hook 可以阻止或改变结果的事件上，如 `PreToolUse` 或 `Stop`，Claude Code 在调用工具之前等待连接的服务器，最多 [`MCP_TIMEOUT`](/docs/zh-CN/env-vars) 和在 hook 自己的 [`timeout`](#common-fields) 内。在观察事件上，如 `Notification` 或 `SessionEnd`，它不等待。

显示 [`cached` 状态](/docs/zh-CN/mcp#server-status-detail) 的服务器在 hook 调用其工具时连接。如果服务器在该点未连接，hook 产生非阻止错误，执行继续。hook 永远不会启动 OAuth 流，因此 [从 `/mcp` 先验证服务器](/docs/zh-CN/mcp#authenticate-with-remote-mcp-servers)。

<h5 id="events-that-fire-before-mcp-servers-are-available">
  MCP 服务器可用之前触发的事件
</h5>

`SessionStart` 在启动时（包括使用 `--continue` 或 `--resume`）和每个 `Setup` 事件在会话的 MCP 服务器对 hooks 可用之前触发。Claude Code 跳过其 `mcp_tool` hooks 而不调用工具，[调试日志](#debug-hooks) 记录 `mcp_tool hooks are not available for the 'SessionStart' hook event (no MCP client context)`，或相同的消息命名 `Setup`。当 `SessionStart` 稍后在会话中再次触发时，在 `/clear` 或压缩后，其 `mcp_tool` hooks 运行。对于会话在启动时需要的任何东西，改用 `SessionStart` 上的 `type: "command"` hook。

<h4 id="prompt-and-agent-hook-fields">
  提示和代理 hook 字段
</h4>

除了 [通用字段](#common-fields)，提示和代理 hooks 接受这些字段：

| 字段 | 必需 | 描述 |
| :- | :- | :- |
| `prompt` | 是 | 发送给模型的提示文本。使用 `$ARGUMENTS` 作为 hook 输入 JSON 的占位符。用反斜杠转义以包含文字文本：`\$1.00` 呈现为 `$1.00` |
| `model` | 否 | 用于评估的模型。默认为 Claude Code 用于 [后台功能](/docs/zh-CN/costs#background-token-usage) 的模型 |

<h3 id="reference-scripts-by-path">
  按路径引用脚本
</h3>

使用这些占位符来相对于项目或插件根目录引用 hook 脚本，无论 hook 运行时的工作目录如何：

* `${CLAUDE_PROJECT_DIR}`：会话启动的项目根目录。Claude Code 还在 [stdio MCP 服务器](/docs/zh-CN/mcp#option-3-add-a-local-stdio-server) 和插件 LSP 服务器的环境中设置此变量。
* `${CLAUDE_PLUGIN_ROOT}`：插件的安装目录，用于与 [插件](/docs/zh-CN/plugins/overview) 捆绑的脚本。有关路径在更新中的行为方式，请参阅 [插件环境变量](/docs/zh-CN/plugins/manifest-reference#environment-variables)。
* `${CLAUDE_PLUGIN_DATA}`：插件的 [持久数据目录](/docs/zh-CN/plugins/components#path-variables-and-persistent-data)，用于应该在插件更新中存活的依赖项和状态。

<Note>
  **Worktrees 是不同的。** 如果 Claude 在会话期间进入 [worktree](/docs/zh-CN/worktrees)，Claude Code 将 `${CLAUDE_PROJECT_DIR}` 保持在原位，并以不同的方式将 worktree 路径传递给 hooks：

  * **`${CLAUDE_PROJECT_DIR}` 保持不变**：它仍然指向会话启动的项目根目录，因此像 `${CLAUDE_PROJECT_DIR}/.claude/hooks/check-style.sh` 这样的命令仍然在主检出中运行脚本。
  * **`cwd` 跟随 Claude**：hook 的 [输入 JSON](#common-input-fields) 中的 `cwd` 字段在 Claude 进入 worktree 后是 worktree 根目录，在 Claude 运行 `cd` 后是新目录。当 hook 需要知道 Claude 正在处理哪个目录时读取它。
</Note>

对于任何引用路径占位符的 hook，优先使用 [exec 形式](#exec-form-and-shell-form)。在 shell 形式中，用双引号包装每个占位符。

<Tabs>
  <Tab title="项目脚本">
    此示例使用 `${CLAUDE_PROJECT_DIR}` 在任何 `Write` 或 `Edit` 工具调用后从项目的 `.claude/hooks/` 目录运行样式检查器：

    ```json theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/check-style.sh",
                "args": []
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="插件脚本">
    在 `hooks/hooks.json` 中定义插件 hooks，带有可选的顶级 `description` 字段。启用插件时，其 hooks 与用户和项目 hooks 合并。

    此示例运行与插件捆绑的格式化脚本：

    ```json theme={null}
    {
      "description": "自动代码格式化",
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Write|Edit",
            "hooks": [
              {
                "type": "command",
                "command": "${CLAUDE_PLUGIN_ROOT}/scripts/format.sh",
                "args": [],
                "timeout": 30
              }
            ]
          }
        ]
      }
    }
    ```

    有关创建插件 hooks 的详细信息，请参阅 [插件组件参考](/docs/zh-CN/plugins/components#hooks)。
  </Tab>
</Tabs>

<h3 id="hooks-in-skills-and-agents">
  Hooks in skills and agents
</h3>

除了设置文件和插件，hooks 可以直接在 [skills](/docs/zh-CN/skills) 和 [subagents](/docs/zh-CN/sub-agents) 中使用 frontmatter 定义，采用与基于设置的 hooks 相同的配置格式。Claude Code 保持它们注册多长时间取决于组件：

* **Subagent hooks**：Claude Code 仅在该子代理运行时运行它们，并在完成时删除它们。Claude Code 在此处将 `Stop` hook 转换为 `SubagentStop`，这是它在子代理完成时触发的事件。
* **Skill hooks**：Claude Code 在调用技能时注册它们，并在会话的其余部分保持运行它们，在技能自己的轮次之后的轮次上也是如此。要让 Claude Code 在第一次成功运行后删除 hook，请在其上设置 [`once: true`](#common-fields)。

此技能定义了一个 `PreToolUse` hook，在每个 `Bash` 命令之前运行安全验证脚本：

```yaml theme={null}
---
name: secure-operations
description: 执行具有安全检查的操作
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/security-check.sh"
---
```

Subagents 在其 YAML frontmatter 中使用相同的格式。

项目技能中的 Frontmatter hooks 遵循与设置文件中的 hooks 相同的 [工作区信任规则](#workspace-trust)。Claude Code 在调用技能时注册它们，包括在未信任的文件夹中的 `-p` 运行。

项目子代理中的 Frontmatter hooks 仅在接受代理文件来自的文件夹的 [工作区信任对话](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust) 后运行。`-p` 会话不计为接受它。[在信任文件夹之前运行的内容](/docs/zh-CN/permissions#what-runs-before-you-trust-a-folder) 将此与设置文件规则进行比较，subagents 页面列出 [哪些范围被豁免](/docs/zh-CN/sub-agents#hooks-in-subagent-frontmatter)。在 v2.1.218 之前，这些 hooks 可以从未信任的文件夹运行。

<h3 id="the-/hooks-menu">
  `/hooks` 菜单
</h3>

在 Claude Code 中键入 `/hooks` 以打开配置的 hooks 的只读浏览器。菜单显示每个 hook 事件及其配置的 hooks 计数，让你深入了解匹配器，并显示每个 hook 处理程序的完整详细信息。使用它来验证配置、检查 hook 来自哪个设置文件或检查 hook 的命令、提示或 URL。

菜单显示所有五种 hook 类型：`command`、`prompt`、`agent`、`http` 和 `mcp_tool`。每个 hook 都标有 `[type]` 前缀和指示其定义位置的源：

* `User Settings`：来自 `~/.claude/settings.json`
* `Project Settings`：来自 `.claude/settings.json`
* `Local Settings`：来自 `.claude/settings.local.json`
* `Plugin Hooks`：来自插件的 `hooks/hooks.json`
* `Session Hooks`：为当前会话在内存中注册

选择 hook 打开详细视图，显示其事件、匹配器、类型、源文件和完整命令、提示或 URL。菜单是只读的：要添加、修改或删除 hooks，直接编辑设置 JSON 或要求 Claude 进行更改。

<h3 id="disable-or-remove-hooks">
  禁用或删除 hooks
</h3>

要删除 hook，从设置 JSON 文件中删除其条目。

要临时禁用所有 hooks 而不删除它们，在设置文件中设置 `"disableAllHooks": true`。Claude Code 读取 [设置优先级](/docs/zh-CN/settings#settings-precedence) 应用后留下的值，因此项目的 `.claude/settings.json` 中的 `"disableAllHooks": false` 覆盖用户设置中的 `true`。要关闭一次运行，无论项目的设置如何，传递 `--settings '{"disableAllHooks": true}'`，这优先于项目和本地设置。没有办法禁用单个 hook 同时将其保留在配置中。

`disableAllHooks` 设置尊重托管设置层次结构。如果管理员通过托管策略设置配置了 hooks，在用户、项目或本地设置中设置的 `disableAllHooks` 无法禁用这些托管 hooks。仅在托管设置级别设置的 `disableAllHooks` 可以禁用托管 hooks。有关每个级别的完整范围，请参阅 [`disableAllHooks`](/docs/zh-CN/settings-reference#disableallhooks)。

设置文件中对 hooks 的直接编辑通常由文件监视程序自动拾取。

<h2 id="hook-input-and-output">
  Hook 输入和输出
</h2>

命令 hook 通过 stdin 接收 JSON 数据，并通过退出代码、stdout 和 stderr 传达结果。HTTP hook 接收与 POST 请求体相同的 JSON，并通过 HTTP 响应体传达结果。本节涵盖所有事件通用的字段和行为。[Hook 事件](#hook-events)下的每个事件部分包括其特定的输入架构和决策控制选项。

在 macOS 和 Linux 上，命令 hook 在没有控制终端的自己的会话中运行。hook 进程和任何子进程无法打开 `/dev/tty` 或直接向 Claude Code 界面发送转义序列。Windows 没有 `/dev/tty`。

要在任何平台上向用户显示消息，请在 JSON 输出中返回 [`systemMessage`](#json-output)。某些事件会丢弃它或将其传递到其他地方，每个[事件部分](#hook-events)都会说明这一点。要触发桌面通知、设置窗口标题或响铃，请改为返回 [`terminalSequence`](#emit-terminal-notifications)。

<h3 id="common-input-fields">
  通用输入字段
</h3>

Hook 事件接收这些字段作为 JSON，除了每个 [hook 事件](#hook-events)部分中记录的事件特定字段。对于命令 hook，此 JSON 通过 stdin 到达。对于 HTTP hook，它作为 POST 请求体到达。

| 字段 | 描述 |
| :- | :- |
| `session_id` | 当前会话标识符 |
| `prompt_id` | 标识当前正在处理的用户提示的 UUID。与 [OpenTelemetry 事件上的 `prompt.id` 属性](/docs/zh-CN/monitoring-usage#event-correlation-attributes)匹配，因此您可以将 hook 输出与单个提示的遥测关联起来。在第一个用户输入之前不存在。需要 Claude Code v2.1.196 或更高版本 |
| `transcript_path` | 对话 JSON 的路径。转录文件异步写入，可能滞后于内存中的对话，因此当 hook 触发时，它可能还不包括当前轮次的最新消息。需要当前轮次最终助手文本的 hook 应在 [Stop](#stop) 和 [SubagentStop](#subagentstop) 上使用 `last_assistant_message`，而不是读取转录 |
| `cwd` | 调用 hook 时的当前工作目录 |
| `scratchpad_dir` | 会话的 [scratchpad 目录](/docs/zh-CN/claude-directory#session-scratchpad-directory)的路径，Claude 在其中保存临时工作文件。当会话没有 scratchpad 或 temp 目录不可用时不存在。需要 Claude Code v2.1.257 或更高版本 |
| `permission_mode` | 当前[权限模式](/docs/zh-CN/permissions#permission-modes)：`"default"`、`"plan"`、`"acceptEdits"`、`"auto"`、`"dontAsk"` 或 `"bypassPermissions"`。标记为**手动**的模式作为 `"default"` 到达，从不作为 `"manual"`，因此匹配 `"default"` 的脚本继续工作。并非所有事件都接收此字段。检查每个 [hook 事件](#hook-events)部分中的 JSON 示例 |
| `effort` | 对象，其 `level` 字段保存 hook 运行时生效的[工作量级别](/docs/zh-CN/model-config#adjust-effort-level)：`"low"`、`"medium"`、`"high"`、`"xhigh"` 或 `"max"`。如果您设置了活跃模型不支持的级别，`level` 会报告 Claude Code 运行的级别；[调整工作量级别](/docs/zh-CN/model-config#adjust-effort-level)说明它如何选择该级别。该对象与[状态行](/docs/zh-CN/statusline#available-data) `effort` 字段匹配。对于在工具使用上下文中触发的事件（如 `PreToolUse`、`PostToolUse`、`Stop` 和 `SubagentStop`），当当前模型支持工作量参数时存在。该级别也可作为 `$CLAUDE_EFFORT` 环境变量供 hook 命令和 Bash 工具使用。 |
| `hook_event_name` | 触发的事件的名称 |

使用 `--agent` 运行或在 subagent 内部时，包括两个额外字段：

| 字段 | 描述 |
| :- | :- |
| `agent_id` | subagent 的唯一标识符。仅当 hook 在 subagent 调用内触发时存在。使用此来区分 subagent hook 调用和主线程调用。 |
| `agent_type` | Agent 名称（例如，`"Explore"` 或 `"security-reviewer"`）。当会话使用 `--agent` 或 hook 在 subagent 内触发时存在。对于 subagent，subagent 的类型优先于会话的 `--agent` 值。请参阅 [SubagentStart](#subagentstart) 了解自定义和插件 subagent 报告的值以及如何针对插件范围的名称编写匹配器。 |

只有 [`SessionStart`](#sessionstart) hook 可以接收 `model` 字段，Claude Code 并不总是包括它。[`PreModelSwitch`](#premodelswitch) 和 [`PostModelSwitch`](#postmodelswitch) hook 改为接收 `from_model` 和 `to_model`，因此使用 PostModelSwitch hook 来跟踪模型在会话期间的变化。

没有 `$CLAUDE_MODEL` 环境变量。如果您在 shell 中设置了 hook，可以读取 `$ANTHROPIC_MODEL`，但该值在您使用 `/model` 在会话期间切换模型时不会改变。

hook 进程继承父环境，除了 Claude Code [从它生成的每个子进程中删除](/docs/zh-CN/monitoring-usage#administrator-configuration)的 `OTEL_*` 导出器变量，以及当 [`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB`](/docs/zh-CN/env-vars#variables) 设置为 `1` 时它剥离的变量。

例如，Bash 命令的 `PreToolUse` hook 在 stdin 上接收以下内容：

```json theme={null}
{
  "session_id": "abc123",
  "prompt_id": "550e8400-e29b-41d4-a716-446655440000",
  "transcript_path": "/home/user/.claude/projects/.../transcript.jsonl",
  "cwd": "/home/user/my-project",
  "scratchpad_dir": "/tmp/claude-1000/-home-user-my-project/abc123/scratchpad",
  "permission_mode": "default",
  "hook_event_name": "PreToolUse",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test",
    "description": "Run test suite",
    "timeout": 120000,
    "run_in_background": false
  },
  "tool_use_id": "toolu_01ABC123..."
}
```

`tool_name`、`tool_input` 和 `tool_use_id` 字段是事件特定的。每个 [hook 事件](#hook-events)部分记录该事件的额外字段。

<h3 id="exit-code-output">
  退出代码输出
</h3>

来自 hook 命令的退出代码告诉 Claude Code 该操作是否应继续、被阻止或被忽略。退出代码不单独起作用。Claude Code 从 stdout 读取[JSON 输出字段](#json-output)，无论退出代码是什么，对于使用标准决策模型的事件，通过架构验证的解析对象与代码一起生效。退出 2 的阻止是 JSON 无法覆盖的唯一结果。

两个表拥有每个事件的例外：[每个事件的退出代码 2 行为](#exit-code-2-behavior-per-event)说明退出代码对每个事件的作用，[决策控制](#decision-control)说明每个事件接受哪些决策字段。通用字段如 `systemMessage` 在大多数事件中工作，并在 [JSON 输出](#json-output)表中列出。

<h4 id="exit-code-0">
  退出代码 0
</h4>

退出 0 表示成功，是您打印 JSON 进行结构化控制时的预期退出代码。

对于大多数事件，Claude Code 将 stdout 写入调试日志，不在转录中显示。例外是 `UserPromptSubmit`、`UserPromptExpansion`、`SessionStart` 和 `PostModelSwitch`，其中 Claude Code 添加纯文本 stdout 作为 Claude 可以看到和作用的上下文。

Claude Code 是否将您的 stdout 读取为 [JSON 输出](#json-output)或纯文本取决于它如何开始和结束，忽略周围的空格：

* **以 `{` 开始并以 `}` 结束**：Claude Code 将其解析为 JSON。当输出是两行或更多行，每行本身都解析为 JSON，且没有行是设置字段的 [JSON 输出](#json-output)对象时，Claude Code 将整个输出视为纯文本。当其中一行确实设置了字段时，整个输出是解析失败，如下所述。
* **以 `{` 开始但不以 `}` 结束**：Claude Code 将其视为纯文本。
* **以其他任何内容开始**：Claude Code 将其视为纯文本、JSON 数组或包含的引用 JSON 字符串。

对于使用标准决策模型的事件，退出 0 且解析对象未通过架构验证是非阻止错误：操作继续，转录显示 `<hook name> hook error` 通知，带有验证消息。在任何退出代码（除 2 外）上都会发生相同情况，而[退出 2 仍然阻止](#exit-code-2)。

对于使用标准决策模型的事件，当 Claude Code 尝试将您的 stdout 解析为 JSON 且无法解析时，它在除 2 外的每个退出代码上报告非阻止错误。转录显示 `<hook name> hook error` 通知，带有解析消息。在添加纯文本 stdout 作为上下文的事件上，Claude Code 不添加文本。在 v2.1.248 之前，Claude Code 将该 stdout 视为纯文本。

来自退出 0 的 hook 的 Stderr 仅进入调试日志，从不进入转录，Claude 从不看到它。要自己读取它，请启用[调试日志](#debug-hooks)。要从 `PostToolUse` 或 `PostToolUseFailure` hook 向 Claude 显示警告，请改为退出 2，以便[Claude 看到 stderr](#exit-code-2-behavior-per-event)，即使工具已经运行。

<h4 id="exit-code-2">
  退出代码 2
</h4>

退出 2 表示阻止错误。在[可以阻止的事件](#exit-code-2-behavior-per-event)上，退出 2 无论您是否打印 JSON 都会阻止：即使 JSON `permissionDecision` 为 `"allow"` 也无法覆盖它。Claude Code 仍然读取 stdout 上的任何有效 [JSON 输出](#json-output)。在 `Elicitation` 和 `ElicitationResult` 上，退出 2 hook 的 `hookSpecificOutput` 被忽略。

阻止消息是您的 JSON 的阻止决策的原因（当它做出一个时），否则是您的 stderr 文本。阻止做什么因事件而异：`PreToolUse` 阻止工具调用，`UserPromptSubmit` 拒绝提示，等等。[每个事件的退出代码 2 行为](#exit-code-2-behavior-per-event)列出每个事件的效果，每个事件的部分说明消息去向。

退出 2 的 hook 同时打印 JSON 且未通过 [JSON 输出](#json-output)架构验证仍然阻止：Claude Code 使用 stderr 作为阻止原因，并在调试日志中记录验证失败。在 v2.1.214 之前，Claude Code 将该组合视为非阻止错误，操作继续。

此脚本通过退出 2 阻止 `rm` 命令，并将所有其他命令留给正常权限流：

```bash theme={null}
#!/bin/bash
# Reads JSON input from stdin, checks the command
input=$(cat)
command=$(jq -r '.tool_input.command' <<<"$input")

if [[ "$command" == rm* ]]; then
  echo "Blocked: rm commands are not allowed" >&2
  exit 2  # Blocking error: tool call is prevented
fi

exit 0  # No decision: the normal permission flow applies
```

<h4 id="other-exit-codes">
  其他退出代码
</h4>

任何其他退出代码对于大多数 hook 事件本身不会阻止。发生什么取决于您的 stdout：

* 使用通过架构验证的解析对象，对于使用标准决策模型的事件，Claude Code 忽略退出代码，JSON 单独决定结果：
  * 事件支持的每个字段都被接受，包括 `permissionDecision`、`additionalContext`、`updatedInput` 和 `systemMessage`，hook 不被报告为错误。
  * [决策控制](#decision-control)列出每个事件的决策字段；通用字段如 `systemMessage` 遵循 [JSON 输出](#json-output)表。
* 使用未通过架构验证的解析对象，对于使用标准决策模型的事件，它与[退出 0 上](#exit-code-0)相同的非阻止错误：操作继续，`<hook name> hook error` 通知带有验证消息。
* 使用 Claude Code [尝试解析为 JSON](#exit-code-0)且无法解析的 stdout，Claude Code 报告与退出 0 上相同的非阻止错误，用于使用标准决策模型的事件。操作继续，通知带有解析消息。
* 使用 Claude Code [视为纯文本](#exit-code-0)的 stdout，或使用空 stdout，对于大多数 hook 事件是非阻止错误：操作继续，转录显示 `<hook name> hook error` 通知，后跟 stderr 的第一行，前缀为 `Failed with non-blocking status code:`。要捕获完整 stderr，请启用[调试日志](#debug-hooks)。

标准决策模型之外的事件在[每个事件表](#exit-code-2-behavior-per-event)中保持自己的行：`WorktreeCreate` 在任何非零退出时失败创建，无论您的 JSON 说什么，事件丢弃 hook 输出（如 `StopFailure`）在每个退出代码上忽略您的 JSON，除了副作用字段如 `terminalSequence`，它仍然触发。

无法启动的 hook 落入相同的非阻止桶。当脚本路径不存在或不可执行时，shell 以代码（如 127）退出，您看到相同的通知，带有解释器的消息，例如 `Failed with non-blocking status code: /bin/sh: /path/to/hook.sh: No such file or directory`。对于大多数 hook 事件，操作继续。当您设置策略 hook 时，在其第一次运行时观察此通知：`settings.json` 中的拼写错误的路径使门无声地禁用。

<Warning>
  对于大多数 hook 事件，退出代码 2 是唯一通过代码单独阻止的退出代码。没有 stdout 上的有效 JSON，Claude Code 将退出代码 1 视为非阻止错误并继续操作，即使 1 是传统的 Unix 失败代码。如果您的 hook 旨在强制执行策略，请使用 `exit 2`。worktree 事件不同：来自 `WorktreeCreate` 的任何非零退出代码中止 worktree 创建，来自 `WorktreeRemove` 的任何非零退出代码使 worktree 移除失败（如果目录仍然存在）。
</Warning>

<h4 id="timeouts">
  超时
</h4>

除了您使用 [`async: true`](#run-hooks-in-the-background) 运行的命令 hook，Claude Code 取消达到其 [`timeout`](#common-fields) 的 `command`、`http` 或 `mcp_tool` hook，丢弃 hook 的输出，因此在大多数事件上超时的 hook 不呈现决策。

在 [`PreModelSwitch`](#premodelswitch) 上，在其超时处取消的 hook 阻止模型切换。在 `PreToolUse` 上，两个 hook 系列不同：

* 超时的 `command`、`http` 或 `mcp_tool` hook 不阻止工具调用。调用通过正常[权限流](/docs/zh-CN/permissions)继续，因此不要指望停滞的 hook 充当门。
* 超过其超时的 [Agent SDK 回调 hook](/docs/zh-CN/agent-sdk/hooks) [阻止工具调用](#pretooluse)。

<h4 id="exit-code-2-behavior-per-event">
  每个事件的退出代码 2 行为
</h4>

退出代码 2 是 hook 发出"停止，不要这样做"信号的方式。效果取决于事件，因为某些事件代表可以被阻止的操作（如尚未发生的工具调用），而其他事件代表已经发生或无法防止的事情。

| Hook 事件 | 可以阻止？ | 退出 2 时发生什么 |
| :- | :- | :- |
| `PreToolUse` | 是 | 阻止工具调用 |
| `PermissionRequest` | 否 | 此事件不接受退出代码 2，权限流程保持不变。改为通过 [`decision` 对象](#permissionrequest-decision-control)拒绝 |
| `UserPromptSubmit` | 是 | 阻止提示，所以它永远不会到达 Claude。请参阅[被阻止的提示留下什么](#what-a-blocked-prompt-leaves-behind) |
| `UserPromptExpansion` | 是 | 阻止扩展 |
| `Stop` | 是 | 防止 Claude 停止，继续对话 |
| `SubagentStop` | 是 | 防止 subagent 停止 |
| `TeammateIdle` | 是 | 防止队友空闲，因此它继续工作 |
| `TaskCreated` | 是 | 回滚任务创建 |
| `TaskCompleted` | 是 | 防止任务被标记为已完成 |
| `ConfigChange` | 是 | 阻止配置更改生效（除 `policy_settings` 外） |
| `StopFailure` | 否 | 输出和退出代码被忽略，除 `terminalSequence` 外 |
| `PostToolUse` | 否 | 向 Claude 显示 stderr；工具已经运行 |
| `PostToolUseFailure` | 否 | 向 Claude 显示 stderr；工具已经失败 |
| `PostToolBatch` | 是 | 在下一个模型调用之前停止代理循环 |
| `PermissionDenied` | 否 | 退出代码和 stderr 被忽略，因为拒绝已经发生。使用 JSON `hookSpecificOutput.retry: true` 告诉模型它可能重试；Claude Code 对[无判决拒绝](#permissiondenied-decision-control)忽略 `retry: true` |
| `Notification` | 否 | 退出代码和 stderr 被忽略 |
| `SubagentStart` | 否 | 仅向用户显示 stderr |
| `SessionStart` | 否 | 仅向用户显示 stderr |
| `Setup` | 否 | 退出代码和 stderr 被忽略 |
| `SessionEnd` | 否 | 仅向用户显示 stderr |
| `CwdChanged` | 否 | 仅向用户显示 stderr |
| `DirectoryAdded` | 否 | Stderr 进入调试日志；目录已经添加 |
| `FileChanged` | 否 | 仅向用户显示 stderr |
| `PreCompact` | 是 | 阻止压缩 |
| `PostCompact` | 否 | 仅向用户显示 stderr |
| `PreModelSwitch` | 是 | 阻止模型切换并向用户显示 stderr |
| `PostModelSwitch` | 否 | 仅向用户显示 stderr；模型已经切换 |
| `Elicitation` | 是 | 拒绝引出 |
| `ElicitationResult` | 是 | 阻止响应（操作变为拒绝） |
| `WorktreeCreate` | 是 | 任何非零退出代码导致 worktree 创建失败 |
| `WorktreeRemove` | 是 | 任何非零退出代码导致 worktree 移除失败（如果目录仍然存在）。请参阅 [WorktreeRemove](#worktreeremove) 了解目录发生什么 |
| `InstructionsLoaded` | 否 | 退出代码被忽略 |
| `MessageDisplay` | 否 | 显示原始文本 |

对于 `SessionStart`、`SubagentStart` 和 `PostModelSwitch`，Claude Code 在转录中呈现退出代码 2 stderr 作为 `<hook name> hook error` 通知，与呈现[非阻止错误](#exit-code-output)的方式相同。Claude 看不到它，会话或 subagent 继续。对于 `SubagentStart`，通知出现在 subagent 自己的转录中，而不是在父对话中。

<h3 id="http-response-handling">
  HTTP 响应处理
</h3>

HTTP hook 使用 HTTP 状态代码和响应体而不是退出代码和 stdout。下面的结果适用于大多数事件；在[每个事件表](#exit-code-2-behavior-per-event)中有自己的失败合约的事件（如 `WorktreeCreate`）将该合约应用于失败的 HTTP hook：

* **2xx 且空体**：成功，等同于退出代码 0 且无输出
* **2xx 且 JSON 对象体**：使用与命令 hook 相同的 [JSON 输出](#json-output)架构解析。未通过架构验证的体是非阻止错误
* **2xx 且任何其他体，如纯文本**：非阻止错误，处理方式与非 2xx 状态相同。Claude Code 不将文本添加到 Claude 的上下文
* **非 2xx 状态**：非阻止错误，执行继续
* **连接失败**：非阻止错误，执行继续
* **超时**：hook 被取消，如 [Timeouts](#timeouts) 下所述

与命令 hook 不同，HTTP hook 无法仅通过状态代码发出阻止错误信号。要阻止工具调用或拒绝权限，返回 2xx 响应，其 JSON 体包含适当的决策字段。

<h3 id="json-output">
  JSON 输出
</h3>

退出代码只让您阻止或保持沉默，但 JSON 输出给您更细粒度的控制。与其退出代码 2 来阻止，不如退出 0 并将 JSON 对象打印到 stdout。Claude Code 从该 JSON 读取特定字段来控制行为，包括[决策控制](#decision-control)来阻止、允许或升级给用户。

<Note>
  每个 hook 选择一种方法：要么单独使用退出代码进行信号，要么退出 0 并打印 JSON 进行结构化控制。如果您混合它们，退出 2 保持其[阻止效果](#exit-code-2-behavior-per-event)，Claude Code 仍然读取 JSON 字段，除了 [Exit code 2](#exit-code-2) 下注明的一个引出例外。
</Note>

您的 hook 的 stdout 必须仅包含 JSON 对象。如果您的 shell 配置文件在启动时打印文本，它可能会干扰 JSON 解析。请参阅故障排除指南中的 [Hook JSON 无效](/docs/zh-CN/hooks-guide#hook-json-has-no-effect)。

hook 的 `additionalContext`、`systemMessage` 和 `initialUserMessage` 字符串，以及其纯 stdout，限制为 10,000 个字符：

* **范围**：Claude Code 单独测量每个字符串，即使多个 hook 为同一事件运行。对于 JSON 输出，每个字段单独测量；纯 stdout 整体测量。
* **超过限制**：Claude Code 将输出保存到会话目录中的文件，并用文件路径和最多前 2,000 个字符的预览替换它。大型有效 Bash 结果的处理方式相同，在 [Output limits](/docs/zh-CN/tools-reference#output-limits) 下描述。与该 Bash 上限不同，此上限没有设置或环境变量来提高它。
* **读取文件**：Claude Code 不要求 Claude 读取文件，因此将 Claude 必须始终看到的任何内容保持在上限内。

JSON 对象支持三种字段：

* **通用字段**如 `continue` 在下表中列出。每个事件都接受它们，但某些事件丢弃它们或将 `systemMessage` 传递到转录以外的地方。每个事件的部分说明这一点。`terminalSequence` 也在这些事件上工作，除了 [Emit terminal notifications](#emit-terminal-notifications) 下列出的例外。
* **顶级 `decision` 和 `reason`** 由某些事件用来阻止或提供反馈。
* **`hookSpecificOutput`** 是需要更丰富控制的事件的嵌套对象。它需要一个 `hookEventName` 字段设置为事件名称。

| 字段 | 默认 | 描述 |
| :- | :- | :- |
| `continue` | `true` | 如果 `false`，Claude 在 hook 运行后完全停止处理。优先于任何事件特定的决策字段 |
| `stopReason` | 无 | 当 `continue` 为 `false` 时向用户显示的消息。它保留在对话中，因此如果对话继续，Claude 会看到它 |
| `suppressOutput` | `false` | 无效果：Claude Code 接受字段但不作用。成功的 hook 的 stdout 从不在转录中显示，并在调试日志中记录 |
| `systemMessage` | 无 | 向用户显示的警告消息。在 [Agent SDK](/docs/zh-CN/agent-sdk/overview) 和 [`--output-format stream-json`](/docs/zh-CN/headless) 输出中，它可以作为 [`SDKInformationalMessage`](/docs/zh-CN/agent-sdk/typescript#sdkinformationalmessage) 到达 |
| `terminalSequence` | 无 | Claude Code 代表您发出的终端转义序列，如桌面通知、窗口标题或响铃。限制为 OSC `0`/`1`/`2`/`9`/`99`/`777` 和 BEL。如果值包含允许列表外的任何内容，字段被忽略。使用此而不是写入 `/dev/tty`，这对 hook 不可用 |

要完全停止 Claude：

```json theme={null}
{ "continue": false, "stopReason": "Build failed, fix errors before continuing" }
```

对于 `PreToolUse` 和 `PostToolUse` hook，停止适用，即使工具调用失败或在 Claude 仍在流式传输响应时完成。

<h4 id="emit-terminal-notifications">
  发出终端通知
</h4>

Hook 运行时没有控制终端，因此直接写入转义序列到 `/dev/tty` 失败。改为在 `terminalSequence` 字段中返回转义序列，Claude Code 通过其自己的终端写入路径代表您发出它。这是无竞争的，在 tmux 和 GNU screen 内工作，并在 Windows 上工作，其中没有 `/dev/tty`。

该字段接受一个或多个允许列表转义序列的字符串：

* OSC `0`、`1`、`2`：窗口和图标标题
* OSC `9`：iTerm2、ConEmu、Windows Terminal 和 WezTerm 通知，包括 `9;4` 任务栏进度
* OSC `99`：Kitty 通知
* OSC `777`：urxvt、Ghostty 和 Warp 通知
* 裸 BEL

序列可以用 BEL 或 ST 终止。允许列表外的任何内容，包括 CSI 光标和颜色序列、OSC 调色板序列、OSC 8 超链接、OSC 52 剪贴板写入和 OSC 1337，被拒绝，字段被忽略。

Claude Code 在处理您的 hook 输出时写入序列本身，因此字段在丢弃 `systemMessage` 和 `continue` 的事件上工作，如 `Notification` 和 `StopFailure`。它有两个限制：

* Claude Code 仅在交互式会话中写入序列，仅当其界面在屏幕上时。在使用 `-p` 标志的非交互式模式和 Agent SDK 中，它忽略字段。
* `WorktreeCreate` 命令 hook 无法返回 JSON，因为 Claude Code 将其 stdout 读取为 worktree 路径。HTTP `WorktreeCreate` hook 返回 JSON 并可以包括字段。

下面的示例从 `Notification` hook 触发桌面通知。转义序列用 `printf` 八进制转义构建，因此控制字节从不出现在 shell 命令行上，`jq -n --arg` 构建 JSON 输出，因此通知消息中的引号、反斜杠和换行符被正确转义：

```bash theme={null}
#!/bin/bash
# Notification hook: ping the desktop when Claude Code needs attention.
input=$(cat)
title="Claude Code"
body=$(jq -r '.message // "Needs your attention"' <<<"$input")
seq=$(printf '\033]777;notify;%s;%s\007' "$title" "$body")
jq -nc --arg seq "$seq" '{terminalSequence: $seq}'
```

`{ "terminalSequence": "..." }` 形状从任何 shell 或语言都相同。

<h4 id="add-context-for-claude">
  为 Claude 添加上下文
</h4>

`additionalContext` 字段将字符串从您的 hook 传递到 Claude 的上下文窗口。Claude Code 将字符串包装在[系统提醒](/docs/zh-CN/glossary#system-reminder)中，并在 hook 触发的点将其插入对话。Claude 在下一个模型请求时读取提醒，但它不作为聊天消息出现在界面中。

在 `hookSpecificOutput` 中返回 `additionalContext` 以及事件名称：

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "This file is generated. Edit src/schema.ts and run `bun generate` instead."
  }
}
```

提醒出现的位置取决于事件：

* [SessionStart](#sessionstart) 和 [SubagentStart](#subagentstart)：在对话开始，在第一个提示之前
* [UserPromptSubmit](#userpromptsubmit) 和 [UserPromptExpansion](#userpromptexpansion)：与提交的提示一起
* [PreToolUse](#pretooluse)、[PostToolUse](#posttooluse)、[PostToolUseFailure](#posttoolusefailure) 和 [PostToolBatch](#posttoolbatch)：在工具结果旁边
* [Stop](#stop) 和 [SubagentStop](#subagentstop)：在轮次末尾。对话继续，因此 Claude 可以对反馈采取行动。请参阅 [Stop decision control](#stop-decision-control)
* [PostModelSwitch](#postmodelswitch)：与切换后的下一个请求一起。请参阅 [PostModelSwitch decision control](#postmodelswitch-decision-control) 了解时间

当多个 hook 为同一事件返回 `additionalContext` 时，Claude 接收所有值。

如果值超过 10,000 个字符，Claude Code 将文本写入会话目录中的文件，并改为传递 Claude 文件路径，带有最多前 2,000 个字符的预览。Claude 可以读取文件，但 Claude Code 不要求它。

使用 `additionalContext` 获取 Claude 应该知道的关于您的环境当前状态或刚刚运行的操作的信息：

* **环境状态**：当前分支、部署目标或活跃功能标志
* **条件项目规则**：哪个测试命令适用于刚编辑的文件，哪些目录在此 worktree 中是只读的
* **外部数据**：分配给您的开放问题、最近的 CI 结果、从内部服务获取的内容

对于从不改变的说明，更喜欢 [CLAUDE.md](/docs/zh-CN/memory)。它加载而不运行脚本，是静态项目约定的标准位置。

将文本写成事实陈述而不是命令式系统说明。措辞如"部署目标是生产"或"此 repo 使用 `bun test`"读作项目信息。框架为带外系统命令的文本可以触发 Claude 的提示注入防御，这导致 Claude 向您显示文本而不是将其视为上下文。

Claude Code 在会话转录中保存注入的文本。对于 `PostToolUse` 或 `UserPromptSubmit` 等中期会话事件，当您使用 `--continue` 或 `--resume` 恢复时，Claude Code 重放保存的文本而不是为过去的轮次重新运行 hook，因此时间戳或提交 SHA 等值变得陈旧。`SessionStart` hook 在使用 `source` 设置为 `"resume"` 或 `"fork"`（如果您添加了 `--fork-session`）恢复时再次运行，因此它们可以刷新其上下文。

<h4 id="decision-control">
  决策控制
</h4>

并非每个事件都支持通过 JSON 阻止或控制行为。支持的事件各自使用不同的字段集来表达该决策。在编写 hook 之前，使用此表作为快速参考：

| 事件 | 决策模式 | 关键字段 |
| :- | :- | :- |
| UserPromptSubmit、UserPromptExpansion、PostToolUse、PostToolUseFailure、PostToolBatch、Stop、SubagentStop、ConfigChange、PreCompact | 顶级 `decision` | `decision: "block"`、`reason`。Stop 和 SubagentStop 也接受 `hookSpecificOutput.additionalContext` 用于[继续对话的非错误反馈](#stop-decision-control) |
| TeammateIdle、TaskCompleted | 退出代码或 `continue: false` | 退出代码 2 用 stderr 反馈阻止操作。JSON `{"continue": false, "stopReason": "..."}` 也完全停止队友，匹配 `Stop` hook 行为；[TaskCompleted 在 `TaskUpdate` 工具触发事件时忽略它](#taskcompleted-decision-control) |
| TaskCreated | 退出代码或顶级 `decision` | 退出代码 2 或 `decision: "block"` [取消任务](#taskcreated-decision-control)并将消息返回给 Claude。`continue: false` 被忽略 |
| PreToolUse | `hookSpecificOutput` | `permissionDecision`（allow/deny/ask/defer）、`permissionDecisionReason` |
| PreModelSwitch | `hookSpecificOutput` 或顶级 `decision` | `permissionDecision`（allow/deny/ask）、`permissionDecisionReason`。`decision: "block"` 也[取消切换](#premodelswitch-decision-control) |
| PermissionRequest | `hookSpecificOutput` | `decision.behavior`（allow/deny） |
| PermissionDenied | `hookSpecificOutput` | `retry: true` 告诉模型它可能重试被拒绝的工具调用；Claude Code 对[无判决拒绝](#permissiondenied-decision-control)忽略它 |
| WorktreeCreate | 路径返回 | 命令 hook 在 stdout 上打印路径；HTTP hook 返回 `hookSpecificOutput.worktreePath`。Hook 失败或缺少路径失败创建 |
| WorktreeRemove | 退出代码 | 任何非零退出代码使移除失败（如果目录仍然存在）。JSON 输出被丢弃 |
| Elicitation | `hookSpecificOutput` | `action`（accept/decline/cancel）、`content`（接受的表单字段值） |
| ElicitationResult | `hookSpecificOutput` | `action`（accept/decline/cancel）、`content`（表单字段值覆盖） |
| MessageDisplay | `hookSpecificOutput` | `displayContent` 替换屏幕上显示的文本。仅显示：转录和 Claude 看到的保持原始 |
| SessionStart、SubagentStart、PostModelSwitch | 仅上下文 | `hookSpecificOutput.additionalContext` 为 Claude 添加上下文。SessionStart 也接受 [`initialUserMessage`、`watchPaths`、`sessionTitle` 和 `reloadSkills`](#sessionstart-decision-control)。无阻止或决策控制 |
| Setup、Notification、SessionEnd、PostCompact、InstructionsLoaded、StopFailure、CwdChanged、DirectoryAdded、FileChanged | 无 | 无决策控制。用于日志或清理等副作用 |

少数事件也可以重写内容而不仅仅允许或阻止它：

* `PreToolUse`：`updatedInput` 直接在 `hookSpecificOutput` 下替换工具的参数，然后它运行。请参阅 [PreToolUse decision control](#pretooluse-decision-control)
* `PermissionRequest`：`updatedInput` 在 `decision` 对象内。请参阅 [PermissionRequest decision control](#permissionrequest-decision-control)
* `PostToolUse`：`updatedToolOutput` 替换工具的结果。请参阅 [PostToolUse decision control](#posttooluse-decision-control)
* `UserPromptSubmit`：无法替换提示；它仅在其旁边注入 `additionalContext`

对于编辑或转换用例，在 `PreToolUse` 处拦截出站工具输入，在 `PostToolUse` 处拦截入站工具结果。

以下是每种模式的实际示例：

<Tabs>
  <Tab title="顶级 decision">
    `decision` 的唯一值是 `"block"`。要允许操作继续，从您的 JSON 中省略 `decision`，或退出 0 而不带任何 JSON：

    ```json theme={null}
    {
      "decision": "block",
      "reason": "Test suite must pass before proceeding"
    }
    ```
  </Tab>

  <Tab title="PreToolUse">
    使用 `hookSpecificOutput` 进行更丰富的控制：允许、拒绝或升级给用户。您也可以在运行前修改工具输入或为 Claude 注入额外上下文。请参阅 [PreToolUse decision control](#pretooluse-decision-control) 了解完整的选项集。

    ```json theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason": "Database writes are not allowed"
      }
    }
    ```
  </Tab>

  <Tab title="PermissionRequest">
    使用 `hookSpecificOutput` 代表用户允许或拒绝权限请求。允许时，您也可以修改工具的输入或应用权限规则，以便用户不会再次被提示。请参阅 [PermissionRequest decision control](#permissionrequest-decision-control) 了解完整的选项集。

    ```json theme={null}
    {
      "hookSpecificOutput": {
        "hookEventName": "PermissionRequest",
        "decision": {
          "behavior": "allow",
          "updatedInput": {
            "command": "npm run lint"
          }
        }
      }
    }
    ```
  </Tab>
</Tabs>

有关扩展示例，包括 Bash 命令验证、提示过滤和自动批准脚本，请参阅指南中的 [What you can automate](/docs/zh-CN/hooks-guide#what-you-can-automate) 和 [Bash command validator reference implementation](https://github.com/anthropics/claude-code/blob/main/examples/hooks/bash_command_validator_example.py)。

<h2 id="hook-events">
  Hook 事件
</h2>

每个事件对应于 Claude Code 生命周期中的一个点，hooks 可以在该点运行。下面的部分按照生命周期顺序排列：从会话设置到 agentic 循环再到会话结束。每个部分描述事件何时触发、它支持哪些匹配器、它接收的 JSON 输入以及如何通过输出控制行为。

<h3 id="sessionstart">
  SessionStart
</h3>

在 Claude Code 启动新会话或恢复现有会话时运行。对于加载开发上下文（如现有问题或代码库的最近更改）或设置环境变量很有用。对于不需要脚本的静态上下文，请改用 [CLAUDE.md](/docs/zh-CN/memory)。

SessionStart 在每个会话上运行，因此请保持这些 hooks 快速。仅支持 `type: "command"` 和 `type: "mcp_tool"` hooks。有关 `mcp_tool` hooks 何时运行，请参阅 [MCP tool hook 字段](#mcp-tool-hook-fields)。

匹配器值对应于会话的启动方式：

| 匹配器 | 何时触发 |
| :- | :- |
| `startup` | 新会话 |
| `resume` | `--resume`、`--continue` 或 `/resume` |
| `clear` | `/clear` |
| `compact` | 自动或手动压缩 |
| `fork` | 从现有会话分叉的新会话：`--fork-session` 与 `--resume` 或 `--continue`、`/fork` 后台副本、`/branch` 或您 [移到后台](/docs/zh-CN/agent-view#from-inside-a-session) 的对话 |

在 v2.1.214 之前，分叉的会话报告源为 `"resume"`。

当您启动交互式会话、使用 `--continue` 或 `--resume` 在启动时恢复对话或运行 `/clear` 时，SessionStart hooks 在后台运行。您可以立即输入，恢复的对话显示时无需等待 hooks。Claude 的第一个响应仍然等待 hooks 完成，因此它们的上下文到达 Claude。

当您在会话内使用 `/resume` 切换对话时，切换等待 hooks 完成。如果您在后台 hooks 仍在运行时运行 `/clear` 或切换到另一个对话，它们返回的任何内容都不适用于该会话。

在启动时也适用相同的等待，包括恢复的会话：您在 SessionStart hooks 仍在运行时发送的提示不会到达 Claude，直到它们完成。

在任一等待期间，按 `Esc` 将提示返回到输入中而不发送它。hooks 继续运行。

<h4 id="sessionstart-input">
  SessionStart 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，SessionStart hooks 还接收 `source` 和可选的 `model`、`agent_type` 和 `session_title`：

| 字段 | 描述 |
| :- | :- |
| `source` | 会话如何启动：新会话为 `"startup"`、恢复的会话为 `"resume"`、`/clear` 后为 `"clear"`、压缩后为 `"compact"` 或从现有会话分叉的新会话为 `"fork"` |
| `model` | 活跃的模型标识符。例如在 `/clear` 后或通过对话恢复恢复会话时可能被省略，因此在读取前检查该字段 |
| `agent_type` | agent 名称，当您使用 `claude --agent <name>` 启动 Claude Code 时出现 |
| `session_title` | 当前会话标题（如果已设置），例如通过 `--name`、`/rename`、发出 `sessionTitle` 的 hook 或 Agent SDK 的 `renameSession()`。发出 `sessionTitle` 的 hook 可以先检查此字段以避免覆盖现有的自定义标题 |

一个您未命名的会话仍然可以有 [生成的标题](/docs/zh-CN/sessions#name-your-sessions)。该标题不是自定义标题，不出现在 `session_title` 中。

当 `source` 为 `"resume"` 或 `"fork"` 且成绩单包含至少一个来自 Claude 的响应时，SessionStart hooks 也会接收下面的四个字段。您的 hook 可以使用它们在第一个请求之前报告恢复陈旧对话的成本，例如在 [`systemMessage`](#json-output) 中。这些字段需要 Claude Code v2.1.251 或更高版本。

| 字段 | 描述 |
| :- | :- |
| `seconds_since_last_response` | 自恢复成绩单中最后一个响应以来的挂钟秒数 |
| `context_tokens` | 恢复会话的第一个请求作为其提示重新发送的令牌 |
| `prompt_cache_likely_expired` | 当最后一个响应早于会话的 [prompt cache 生命周期](/docs/zh-CN/prompt-caching#cache-lifetime) 或更晚的压缩替换了缓存的对话时为 `true` |
| `estimated_cache_write_usd` | 将 `context_tokens` 写入会话模型的 prompt cache 的估计成本（美元），不包括响应 |

此示例显示了在最后一个响应后 90 分钟恢复的会话的输入：

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionStart",
  "source": "resume",
  "model": "claude-opus-5",
  "seconds_since_last_response": 5400,
  "context_tokens": 182340,
  "prompt_cache_likely_expired": true,
  "estimated_cache_write_usd": 1.1396
}
```

<h4 id="sessionstart-decision-control">
  SessionStart 决策控制
</h4>

Claude Code 将它 [视为纯文本](#exit-code-0) 的 stdout 添加到 Claude 的上下文中。除了所有 hooks 可用的 [JSON 输出字段](#json-output) 外，您还可以返回这些事件特定的字段：

| 字段 | 描述 |
| :- | :- |
| `additionalContext` | 在对话开始时添加到 Claude 上下文的字符串，在第一个提示之前。有关文本如何传递以及放入其中的内容，请参阅 [为 Claude 添加上下文](#add-context-for-claude) |
| `initialUserMessage` | 用作会话第一个用户消息的字符串。适用于 [非交互模式](/docs/zh-CN/headless)，带有 `-p` 标志，即使未提供提示，它也成为第一个回合。如果提供了提示，它作为下一个回合跟随。与 `additionalContext` 不同，后者附加到现有回合，这会创建回合 |
| `sessionTitle` | 设置会话标题，效果与 `/rename` 相同。用于从启动文件夹、git 分支或 worktree 名称自动命名会话。当 `source` 为 `"startup"`、`"resume"` 或 `"fork"` 时适用；在 `"clear"` 和 `"compact"` 上被忽略 |
| `watchPaths` | 绝对路径数组，用于在此会话期间监视 [FileChanged](#filechanged) 事件 |
| `reloadSkills` | 布尔值。当为 `true` 时，Claude Code 在 SessionStart hooks 完成后重新扫描 [skill](/docs/zh-CN/skills) 和命令目录，因此 hook 安装的 skills 在同一会话中可用，从第一个提示开始 |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SessionStart",
    "additionalContext": "Current branch: feat/auth-refactor\nUncommitted changes: src/auth.ts, src/login.tsx\nActive issue: #4211 Migrate to OAuth2",
    "sessionTitle": "auth-refactor"
  }
}
```

由于纯 stdout 已经为此事件到达 Claude，仅加载上下文的 hook 可以直接打印到 stdout 而无需构建 JSON。当您需要将上下文与其他字段（如 `sessionTitle`）结合时，使用 JSON 形式。

当 SessionStart hook 安装或更新 skills 时使用 `reloadSkills`。Skill 发现通常在 SessionStart hooks 完成之前运行，因此 hook 写入 `~/.claude/skills/` 或 `.claude/skills/` 的文件否则只会在下一个会话中出现。此示例同步共享 skills 存储库并请求重新扫描：

```bash theme={null}
#!/bin/bash

git -C ~/.claude/skills/team-skills pull --quiet 2>/dev/null || \
  git clone --quiet https://git.example.com/your-org/team-skills.git ~/.claude/skills/team-skills

echo '{"hookSpecificOutput": {"hookEventName": "SessionStart", "reloadSkills": true}}'
```

存储库 URL 是占位符；将其替换为您自己的 skills 存储库。使用占位符，克隆失败并打印 `fatal:` 消息到 stderr。来自退出 0 的 SessionStart hook 的 stderr 仅供参考，因此 `reloadSkills` 请求仍然适用。

<h4 id="persist-environment-variables">
  持久化环境变量
</h4>

SessionStart hooks 可以访问 `CLAUDE_ENV_FILE` 环境变量，它提供一个文件路径，您可以在其中为后续 Bash 命令持久化环境变量。

要设置单个环境变量，请将 `export` 语句写入 `CLAUDE_ENV_FILE`。使用追加 (`>>`) 来保留由其他 hooks 设置的变量：

```bash theme={null}
#!/bin/bash

if [ -n "$CLAUDE_ENV_FILE" ]; then
  echo 'export NODE_ENV=production' >> "$CLAUDE_ENV_FILE"
  echo 'export DEBUG_LOG=true' >> "$CLAUDE_ENV_FILE"
  echo 'export PATH="$PATH:./node_modules/.bin"' >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

要捕获设置命令中的所有环境更改，请比较之前和之后导出的变量：

```bash theme={null}
#!/bin/bash

ENV_BEFORE=$(export -p | sort)

# Run your setup commands that modify the environment
source ~/.nvm/nvm.sh
nvm use 20

if [ -n "$CLAUDE_ENV_FILE" ]; then
  ENV_AFTER=$(export -p | sort)
  comm -13 <(echo "$ENV_BEFORE") <(echo "$ENV_AFTER") >> "$CLAUDE_ENV_FILE"
fi

exit 0
```

<Note>
  `CLAUDE_ENV_FILE` 可用于 SessionStart、[Setup](#setup)、[CwdChanged](#cwdchanged) 和 [FileChanged](#filechanged) hooks。其他 hook 类型无法访问此变量。
</Note>

<h3 id="setup">
  Setup
</h3>

仅当您使用 `--init-only` 启动 Claude Code，或在 [非交互模式](/docs/zh-CN/headless) 中使用 `--init` 或 `--maintenance` 与 `-p` 标志时触发。它不会在正常启动时触发。用于一次性依赖安装或您从 CI 或脚本显式触发的计划清理，与正常会话启动分开。对于每个会话的初始化，请改用 [SessionStart](#sessionstart)。

匹配器值对应于触发 hook 的 CLI 标志：

| 匹配器 | 何时触发 |
| :- | :- |
| `init` | `claude --init-only` 或 `claude -p --init` |
| `maintenance` | `claude -p --maintenance` |

当您运行 `claude --init-only` 时，Claude Code 运行 Setup hooks 和带有 `startup` 匹配器的 `SessionStart` hooks，然后退出而不启动对话。

当您使用 `-p` 启动或继续对话时，您还需要提供提示，作为参数或通过 stdin 管道传输。当 `SessionStart` hook 提供 [`initialUserMessage`](#sessionstart-decision-control) 或当您恢复带有 [延迟工具调用](#defer-a-tool-call-for-later) 的会话时，您可以跳过提示。

成功时，`--init-only` 不向终端打印任何内容。要确认 hooks 运行，请使用 `claude --debug-file <path> --init-only` 启动，将 `<path>` 替换为日志文件位置，并检查日志中的 Setup 和 SessionStart hook 条目。

由于 Setup 不会在每次启动时触发，需要安装依赖的插件不能仅依赖 Setup。实际的模式是在首次使用时检查依赖并在缺失时安装，例如测试 `${CLAUDE_PLUGIN_DATA}/node_modules` 的 hook 或 skill，如果不存在则运行 `npm install`。有关存储已安装依赖的位置，请参阅 [持久数据目录](/docs/zh-CN/plugins/components#path-variables-and-persistent-data)。如果您通过市场分发插件，您可能不需要此模式：Claude Code [在缓存插件时自动安装符合条件的 Node.js 包依赖](/docs/zh-CN/plugins/loading#node-js-package-dependencies)。

<h4 id="setup-input">
  Setup 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，Setup hooks 接收设置为 `"init"` 或 `"maintenance"` 的 `trigger` 字段：

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Setup",
  "trigger": "init"
}
```

<h4 id="setup-decision-control">
  Setup 决策控制
</h4>

Setup hooks 无法阻止；执行在任何退出代码上继续。在每个退出代码上，Claude Code 丢弃 Setup hook 的 [JSON 输出字段](#json-output)，如 `systemMessage`、`continue` 和 `hookSpecificOutput.additionalContext`。使用 `-p`，Setup hook 的 stdout、stderr 和退出代码仅在您使用 `--output-format stream-json --verbose` 启动时作为 [`hook_response` 事件](/docs/zh-CN/headless#read-session-metadata) 出现在运行的输出中。

Setup hooks 可以访问 `CLAUDE_ENV_FILE`。写入该文件的变量持久化到会话的后续 Bash 命令中，就像在 [SessionStart hooks](#persist-environment-variables) 中一样。仅 `type: "command"` hooks 在 `Setup` 上运行。`type: "mcp_tool"` hook 在 `Setup` 上总是被跳过，如 [MCP tool hook 字段](#mcp-tool-hook-fields) 下所述。

<h3 id="instructionsloaded">
  InstructionsLoaded
</h3>

当 `CLAUDE.md` 或 `.claude/rules/*.md` 文件加载到上下文中时触发。此事件在会话启动时对于急切加载的文件触发，稍后当文件被懒加载时再次触发，例如当 Claude 访问包含嵌套 `CLAUDE.md` 的子目录或当带有 `paths:` frontmatter 的条件规则匹配时。hook 不支持阻止或决策控制。它异步运行以用于可观测性目的。

当 Claude [直接通过 **Project instructions** 设置读取 `AGENTS.md`](/docs/zh-CN/memory#agents-md) 时，此事件不触发。当 `CLAUDE.md` 导入您的 `AGENTS.md` 时它会触发，`load_reason` 设置为 `include`（与任何其他导入文件一样），以及当 `CLAUDE.md` 是它的符号链接时，作为正常的 `CLAUDE.md` 加载。

匹配器针对 `load_reason` 运行。例如，使用 `"matcher": "session_start"` 仅对在会话启动时加载的文件触发，或 `"matcher": "path_glob_match|nested_traversal"` 仅对懒加载触发。

<h4 id="instructionsloaded-input">
  InstructionsLoaded 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，InstructionsLoaded hooks 接收这些字段：

| 字段 | 描述 |
| :- | :- |
| `file_path` | 加载的指令文件的绝对路径 |
| `memory_type` | 文件的范围：`"User"`、`"Project"`、`"Local"` 或 `"Managed"` |
| `load_reason` | 文件加载的原因：`"session_start"`、`"nested_traversal"`、`"path_glob_match"`、`"include"` 或 `"compact"`。`"compact"` 值在压缩事件后重新加载指令文件时触发 |
| `globs` | 文件 `paths:` frontmatter 中的路径 glob 模式（如果有）。仅对 `path_glob_match` 加载出现 |
| `trigger_file_path` | 触发此加载的文件的路径，用于懒加载 |
| `parent_file_path` | 包含此文件的父指令文件的路径，用于 `include` 加载 |

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "InstructionsLoaded",
  "file_path": "/Users/my-project/CLAUDE.md",
  "memory_type": "Project",
  "load_reason": "session_start"
}
```

<h4 id="instructionsloaded-decision-control">
  InstructionsLoaded 决策控制
</h4>

InstructionsLoaded hooks 没有决策控制。它们无法阻止或修改指令加载。Claude Code 丢弃它们的 [JSON 输出字段](#json-output)，如 `systemMessage` 和 `continue`。使用此事件进行审计日志、合规性跟踪或可观测性。

<h3 id="userpromptsubmit">
  UserPromptSubmit
</h3>

在用户提交提示时运行，在 Claude 处理它之前。这允许您根据提示/对话添加额外上下文、验证提示或阻止某些类型的提示。

`UserPromptSubmit` hooks 对 `command`、`http` 和 `mcp_tool` 类型的默认超时为 30 秒，比大多数其他事件的 600 秒默认值更短。因为此 hook 在每个提示之前运行并阻止模型处理直到它完成，卡住的 hook 会停滞会话。如果您的 hook 需要更多时间，请在 hook 条目中设置 `timeout` 字段。

除了您使用 [`async: true`](#run-hooks-in-the-background) 运行的命令 hook，达到超时的 `UserPromptSubmit` 命令、HTTP 或 MCP tool hook 被取消，其输出（包括任何 `additionalContext`）被丢弃。提示仍然到达 Claude 而没有该上下文。成绩单显示一个通知，命名 hook、触发的超时以及输出被丢弃。

在 `UserPromptSubmit` 上达到超时的 [Agent SDK 回调 hook](/docs/zh-CN/agent-sdk/hooks) 用命名 hook 和超时的消息阻止提示，因为那里的回调可能充当必须不能失败打开的策略门。会话继续。在 v2.1.208 之前，该事件上的回调超时以执行错误结束回合。

<h4 id="userpromptsubmit-input">
  UserPromptSubmit 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，UserPromptSubmit hooks 接收包含用户提交的文本的 `prompt` 字段。折叠为 `[Pasted text #N]` 占位符的粘贴内容在原位展开到达。在 Claude Code [为 Claude 标记粘贴文本](/docs/zh-CN/terminal-config#how-claude-treats-pasted-text) 的会话中，该展开的内容位于 `<pasted_content id="…">` 行和 `</pasted_content id="…">` 行之间，因此如果您的 hook 解析提示，请考虑这些行。

UserPromptSubmit hooks 也在会话有自定义标题时接收 `session_title`，含义与 [SessionStart `session_title` 字段](#sessionstart-input) 相同。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "UserPromptSubmit",
  "prompt": "Write a function to calculate the factorial of a number"
}
```

<h4 id="userpromptsubmit-decision-control">
  UserPromptSubmit 决策控制
</h4>

`UserPromptSubmit` hooks 可以控制是否处理用户提示并添加上下文。所有 [JSON 输出字段](#json-output) 都可用。

有两种方式在退出代码 0 上向对话添加上下文：

* **纯文本 stdout**：Claude Code 添加它 [视为纯文本](#exit-code-0) 的 stdout 到 Claude 的上下文
* **带有 `additionalContext` 的 JSON**：使用下面的 JSON 格式以获得更多控制。`additionalContext` 字段作为上下文添加

两个通道都不产生可见的成绩单条目。纯 stdout 和 `additionalContext` 值各自作为以 hook 名称开头的系统提醒注入；Claude 读取两者。要确认传递，请检查 [调试日志](#debug-hooks)。

要阻止提示，返回一个 JSON 对象，其中 `decision` 设置为 `"block"`：

| 字段 | 描述 |
| :- | :- |
| `decision` | `"block"` 防止提示被处理。省略以允许提示继续 |
| `reason` | 当 `decision` 为 `"block"` 时显示给用户。不添加到上下文 |
| `additionalContext` | 与提交的提示一起添加到 Claude 上下文的字符串。有关如何传递文本以及放入其中的内容，请参阅 [为 Claude 添加上下文](#add-context-for-claude) |
| `sessionTitle` | 设置会话标题。用于根据提示内容自动命名会话 |
| `suppressOriginalPrompt` | 如果在 hook 阻止提示时为 `true`，则从阻止消息中省略原始提示文本。请参阅 [被阻止的提示留下什么](#what-a-blocked-prompt-leaves-behind) |

通过退出 2 阻止的 hook 路由方式与 `reason` 相同：阻止消息向用户显示 stderr 文本，它不添加到上下文。

```json theme={null}
{
  "decision": "block",
  "reason": "Explanation for decision",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptSubmit",
    "additionalContext": "My additional context here",
    "sessionTitle": "My session title",
    "suppressOriginalPrompt": true
  }
}
```

<h4 id="what-a-blocked-prompt-leaves-behind">
  被阻止的提示留下什么
</h4>

被阻止的提示永远不会到达 Claude，但其文本不会从任何地方删除。默认情况下，显示给用户的阻止消息以 `Original prompt:` 结尾，后跟提交的文本，Claude Code 将该消息写入会话的成绩单文件。要从消息中省略文本，打印 JSON，其中 `hookSpecificOutput` 中的 `"suppressOriginalPrompt": true`。无论 hook 是用 `decision: "block"` 还是通过退出 2 阻止，这都有效。不打印 JSON 的退出 2 hook 总是在其阻止消息中获得提示文本。

`suppressOriginalPrompt` 仅更改阻止消息。提交的文本仍然可以出现在本地文件中，如会话成绩单和您的提示历史，因此阻止 hook 不是将秘密保留在磁盘外的方式。要限制或删除这些文件，请参阅 [纯文本存储](/docs/zh-CN/claude-directory#plaintext-storage) 和 [清除本地数据](/docs/zh-CN/claude-directory#clear-local-data)。

<h3 id="userpromptexpansion">
  UserPromptExpansion
</h3>

当用户输入的命令在到达 Claude 之前展开为提示时运行。使用此来阻止特定命令的直接调用、为特定 skill 注入上下文或记录用户调用哪些命令。例如，匹配 `deploy` 的 hook 可以阻止 `/deploy`，除非存在批准文件，或匹配审查 skill 的 hook 可以将团队的审查清单附加为 `additionalContext`。

此事件涵盖 `PreToolUse` 不涵盖的路径：匹配 `Skill` 工具的 `PreToolUse` hook 仅在 Claude 调用工具时触发，但直接输入 `/skillname` 绕过 `PreToolUse`。`UserPromptExpansion` 在该直接路径上触发。

在 `command_name` 上匹配。将匹配器留空以对每个提示类型命令触发。

<h4 id="userpromptexpansion-input">
  UserPromptExpansion 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，UserPromptExpansion hooks 接收 `expansion_type`、`command_name`、`command_args`、`command_source` 和原始 `prompt` 字符串。`expansion_type` 字段对于 skill 和自定义命令为 `slash_command`，或对于 MCP 服务器提示为 `mcp_prompt`。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../00893aaf.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "UserPromptExpansion",
  "expansion_type": "slash_command",
  "command_name": "example-skill",
  "command_args": "arg1 arg2",
  "command_source": "plugin",
  "prompt": "/example-skill arg1 arg2"
}
```

<h4 id="userpromptexpansion-decision-control">
  UserPromptExpansion 决策控制
</h4>

`UserPromptExpansion` hooks 可以阻止展开或添加上下文。所有 [JSON 输出字段](#json-output) 都可用。

| 字段 | 描述 |
| :- | :- |
| `decision` | `"block"` 防止命令展开。省略以允许它继续 |
| `reason` | 当 `decision` 为 `"block"` 时显示给用户 |
| `additionalContext` | 与展开的提示一起添加到 Claude 上下文的字符串。有关如何传递文本以及放入其中的内容，请参阅 [为 Claude 添加上下文](#add-context-for-claude) |

通过退出 2 阻止的 hook 路由方式与 `reason` 相同：阻止消息向用户显示 stderr 文本。

```json theme={null}
{
  "decision": "block",
  "reason": "This slash command is not available",
  "hookSpecificOutput": {
    "hookEventName": "UserPromptExpansion",
    "additionalContext": "Additional context for this expansion"
  }
}
```

<h3 id="messagedisplay">
  MessageDisplay
</h3>

在助手消息流向屏幕时运行。Claude Code 分批显示消息：每次一批新完成的行准备好渲染时，hook 运行一次，这些行和 Claude Code 渲染 hook 的替换文本代替它们。长消息产生多个调用；短消息可能只产生一个。

使用 MessageDisplay 来：

* 为最小显示剥离 markdown
* 转换 Agent SDK 应用程序向其用户显示的文本
* 从 Claude 的响应中编辑 API 密钥或内部主机名

Claude Code 保持每个批次直到您的 hook 返回，因此保持 hook 快速。如果 hook 失败或超时，Claude Code 显示原始文本。此事件的默认超时为 10 秒；如果您的 hook 需要更多时间，请在 hook 条目中设置 `timeout` 字段。

MessageDisplay 仅用于显示：替换文本仅更改屏幕上呈现的内容。成绩单和 Claude 看到的内容保持原始文本，因此 Claude 永远看不到替换，详细模式显示原始。hook 仅接收助手消息文本，因此工具结果和您输入的文本呈现不变。

MessageDisplay 不支持匹配器，对每个流文本的助手消息触发；没有文本的消息（如仅工具调用响应）不触发它。

在非交互式运行中，包括 Agent SDK 查询和 `claude -p`，MessageDisplay 每个助手消息运行一次而不是每批行运行一次。单个调用在消息完成后到达并携带完整消息文本：`index` 为 `0`，`final` 为 `true`，`delta` 保持整个消息。为每个消息收集 `delta` 文本的 hook 在两种模式中接收相同的总文本。

<h4 id="messagedisplay-input">
  MessageDisplay 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，MessageDisplay hooks 接收回合和消息的标识符、此调用在消息中的位置以及 `delta` 中的新文本。批次边界取决于文本如何流，因此使用 `index` 和 `final` 来跟踪通过消息的进度，而不是期望行以特定方式分组。

| 字段 | 描述 |
| :- | :- |
| `turn_id` | 当前回合的 UUID |
| `message_id` | 正在显示的助手消息的 UUID。在同一消息的每个批次中稳定。这不是 API `msg_…` id，因此无法与成绩单消息 ids 关联 |
| `index` | 此批次在消息中的零基索引 |
| `final` | 在消息的最后一个批次上为 `true`。每个消息恰好有一个最终批次 |
| `delta` | 自上一个批次以来新完成的行，包括终止换行符。始终是完整行，除了可能以行中间结束的最终批次。在交互式运行中，当消息以换行符结束时最终批次的 delta 为空，因此将 `final` 而不是非空 delta 视为消息结束信号。在 Agent SDK 和 `claude -p` 运行中，单个调用携带整个消息 |

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "MessageDisplay",
  "turn_id": "0c9e6a2f-7d41-4f4e-9a15-3f4f7c2b8d10",
  "message_id": "5b2a9c8e-1f63-4d8a-b7c4-9e0d2a6f1c3b",
  "index": 0,
  "final": false,
  "delta": "Here is the plan:\n"
}
```

<h4 id="messagedisplay-output">
  MessageDisplay 输出
</h4>

除了所有 hooks 可用的 [JSON 输出字段](#json-output) 外，MessageDisplay hooks 可以返回 `displayContent` 来替换屏幕上的 delta：

| 字段 | 描述 |
| :- | :- |
| `displayContent` | 显示代替 delta 的文本。省略以显示原始 |

MessageDisplay hooks 没有决策控制。它们无法阻止消息或更改存储在成绩单中或发送给 Claude 的内容。Claude Code 作用于它们的 JSON 输出中的 `displayContent` 并丢弃 `systemMessage` 和 `continue`。

此示例从 Claude 的响应中剥离 markdown 格式以获得纯文本显示。脚本从 stdin 读取每个批次，从 `delta` 中删除粗体标记和内联代码反引号，并将结果作为 `displayContent` 返回。

<Tabs>
  <Tab title="macOS/Linux">
    在您的设置文件中为事件注册命令 hook：

    ```json theme={null}
    {
      "hooks": {
        "MessageDisplay": [
          {
            "hooks": [
              {
                "type": "command",
                "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/plain-display.sh",
                "args": []
              }
            ]
          }
        ]
      }
    }
    ```

    将此脚本保存到项目中的 `.claude/hooks/plain-display.sh` 并使用 `chmod +x` 使其可执行：

    ```bash theme={null}
    #!/bin/bash
    jq '{hookSpecificOutput: {hookEventName: "MessageDisplay", displayContent: (.delta | gsub("\\*\\*"; "") | gsub("`"; ""))}}'
    ```
  </Tab>

  <Tab title="Windows (PowerShell)">
    注册一个命令 hook，通过 PowerShell 运行脚本：

    ```json theme={null}
    {
      "hooks": {
        "MessageDisplay": [
          {
            "hooks": [
              {
                "type": "command",
                "command": "powershell.exe",
                "args": [
                  "-NoProfile",
                  "-ExecutionPolicy",
                  "Bypass",
                  "-File",
                  "${CLAUDE_PROJECT_DIR}/.claude/hooks/plain-display.ps1"
                ]
              }
            ]
          }
        ]
      }
    }
    ```

    `-NoProfile` 标志跳过加载您的 PowerShell 配置文件，以便 hook 快速启动，`-ExecutionPolicy Bypass` 让 PowerShell 运行本地脚本文件。

    将此脚本保存到项目中的 `.claude/hooks/plain-display.ps1`：

    ```powershell theme={null}
    $batch = [Console]::In.ReadToEnd() | ConvertFrom-Json
    $text = $batch.delta -replace '\*\*', '' -replace '`', ''
    @{
      hookSpecificOutput = @{
        hookEventName = "MessageDisplay"
        displayContent = $text
      }
    } | ConvertTo-Json
    ```
  </Tab>
</Tabs>

没有 markdown 的批次通过不变。如果脚本失败，例如因为 `jq` 缺失，Claude Code 显示原始文本并仅在 [调试输出](#debug-hooks) 中注意失败，而不是在会话中。

<h3 id="pretooluse">
  PreToolUse
</h3>

在 Claude 创建工具参数之后和处理工具调用之前运行。在除 `EndConversation` 之外的任何工具名称上匹配：内置工具如 `Bash`、`PowerShell`、`Edit`、`Write`、`Read`、`Glob`、`Grep`、`Agent`、`Workflow`、`WebFetch`、`WebSearch`、`AskUserQuestion` 和 `ExitPlanMode`，以及任何 [MCP 工具名称](#match-mcp-tools)。

要在特定文件在磁盘上更改时运行 hook，无论什么写入它，请使用 [FileChanged](#filechanged) 而不是按名称匹配文件编辑工具。与 PreToolUse 不同，Claude Code 在更改后运行 FileChanged hooks，它们没有决策控制，因此它们无法阻止写入。

<Warning>
  PreToolUse 仅在 Claude 调用工具时运行。您 [在提示中使用 `@` 引用的文件](/docs/zh-CN/common-workflows#reference-files-and-directories) 添加时没有任何工具调用：Claude Code 在构建提示时插入它们的内容，因此没有 PreToolUse hook 为它们触发，包括匹配 `Read` 的 hooks。要阻止特定路径的 `@` 引用，请改用 [`Read` 拒绝规则](/docs/zh-CN/permissions#read-and-edit)。

  PreToolUse 也不为 [`EndConversation`](/docs/zh-CN/tools-reference#endconversation-tool-behavior) 触发。
</Warning>

使用 [PreToolUse 决策控制](#pretooluse-decision-control) 来允许、拒绝、询问或延迟工具调用。

在 `PreToolUse` 上超过其超时的 [Agent SDK 回调 hook](/docs/zh-CN/agent-sdk/hooks) 阻止工具调用，Claude 接收命名超时的错误结果。另一个 hook 返回的显式拒绝仍然优先。

<h4 id="pretooluse-input">
  PreToolUse 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，PreToolUse hooks 接收 `tool_name`、`tool_input` 和 `tool_use_id`。

对于 [MCP 工具](#match-mcp-tools)，输入也携带 `mcp_server`，一个包含服务器 `name` 和 `source` 的对象，说明服务器定义来自何处。`source` 值包括 `plugin`、`sdk` 和配置范围如 `user` 和 `project`。Agent SDK 参考中的 [`McpServerProvenance`](/docs/zh-CN/agent-sdk/typescript#mcpserverprovenance) 列出了所有内容并说明如何处理您不认识的内容。基于 `source` 而不是 `name` 或 `mcp__<server>__` 工具名称前缀做出信任决定。`mcp_server` 字段需要 Claude Code v2.1.274 或更高版本。

对于文件工具 `Write`、`Edit` 和 `Read`，`tool_input.file_path` 始终是绝对的：

* Claude Code 在 hooks 运行之前展开 `~` 和相对路径，因此匹配路径的 hook 无法通过 `~` 或相同路径的相对拼写绕过
* 在 Windows 上，路径到达时带有反斜杠分隔符，即使您的 hook 在 Git Bash 下运行，其中 `$PWD` 看起来像 `/c/project`
* 用正斜杠编写的比较（如 `/src/` 检查）永远不会匹配反斜杠路径，工具调用继续，就像 hook 没有什么要阻止的一样
* 在比较前规范化分隔符：Bash 中的 `FILE_PATH="${FILE_PATH//\\//}"` 或 Python 中的 `file_path.replace("\\", "/")`，然后匹配路径段如 `/src/` 而不是用 `^` 锚定，因为路径是绝对的

Windows 上的 `Write` 调用传递：

```json theme={null}
{
  "hook_event_name": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "C:\\project\\src\\index.ts",
    "content": "..."
  },
  ...
}
```

`tool_input` 字段取决于工具：

<a id="bash" />

<h5 id="bash">
  Bash
</h5>

执行 shell 命令。

| 字段 | 类型 | 示例 | 描述 |
| :- | :- | :- | :- |
| `command` | string | `"npm test"` | 要执行的 shell 命令 |
| `description` | string | `"Run test suite"` | 命令执行内容的可选描述 |
| `timeout` | number | `120000` | 可选超时（毫秒）。高于 [最大值](/docs/zh-CN/tools-reference#bash-tool-behavior) 的值被减少到最大值而不是被拒绝 |
| `run_in_background` | boolean | `false` | 是否在后台运行命令 |

当 Bash 命令更改 Git 存储库中的文件时，Claude Code 可以记录更改的内容。当 [`bashEditDiffEnabled`](/docs/zh-CN/settings-reference#basheditdiffenabled) 设置打开记录时，它在每个权限模式中记录；该设置的条目说明哪些文件可以设置它。否则它仅在自动模式和 `bypassPermissions` 模式中记录，并且仅当 Claude Code 指导 Claude 通过 Bash 编辑文件时。设置 `bashEditDiffEnabled` 为 `false` 以关闭记录。后台命令和只读命令不携带 diff。

您的 [PostToolUse hook](#posttooluse) 然后在 `tool_response.bashEditDiff` 中接收更改的文件。列表涵盖命令运行时存储库下更改的内容。Git 忽略的文件和子模块中的文件不列出。需要 Claude Code v2.1.269 或更高版本。

<Note>
  列表是尽力而为的，处于公开测试版。Claude Code 可能会错过更改、包含另一个进程同时更改的文件或在其大小限制处停止。字段形状可能会改变。使用列表查找要审查的内容，而不是强制执行策略。
</Note>

`changedFiles` 和 `files` 列出命令更改的内容；其余字段说明该列表的完整性和可靠性。

| 字段 | 类型 | 示例 | 描述 |
| :- | :- | :- | :- |
| `changedFiles` | array | `["/path/to/src/app.ts"]` | 命令更改的文件的绝对路径，最多 200 个。每当 `files` 保持 diff 或 `moreFiles` 高于零时出现 |
| `files` | array | `[{"filePath": "/path/to/src/app.ts", "hunks": [...]}]` | 最多 5 个更改文件的 diffs，用于显示。对于命令添加或删除的文件，`created` 或 `deleted` 为 `true` |
| `moreFiles` | number | `2` | 在 `files` 中没有 diff 的更改文件计数 |
| `unavailable` | boolean | `true` | 当 diff 不完整或无法获取时设置 |
| `skipped` | boolean | `true` | 对于移动工作树的 Git 命令设置，如 `git checkout` 或 `git stash`，因此 Claude Code 不取 diff |
| `shared` | boolean | `true` | 当另一个 Bash 工具调用（如子 agent 的）同时在同一存储库中运行时设置，因此某些列出的更改可能是该命令的 |

<a id="powershell" />

<h5 id="powershell">
  PowerShell
</h5>

执行 PowerShell 命令。有关按平台的可用性，请参阅 [PowerShell 工具](/docs/zh-CN/tools-reference#powershell-tool)。

字段与 Bash 工具匹配，命令字符串在 `command` 中：

| 字段 | 类型 | 示例 | 描述 |
| :- | :- | :- | :- |
| `command` | string | `"Get-ChildItem -Recurse"` | 要执行的 PowerShell 命令 |
| `description` | string | `"List files recursively"` | 命令执行内容的可选描述 |
| `timeout` | number | `120000` | 可选超时（毫秒） |
| `run_in_background` | boolean | `false` | 是否在后台运行命令 |

在检查 shell 命令的 hooks 中匹配 `Bash|PowerShell`，以便它们涵盖两个工具：

* 在 Windows 上，无论 PowerShell 工具在何处启用，Claude 将 PowerShell 视为主 shell 并通过它路由 shell 命令。
* 在没有 Git Bash 的 Windows 上，工具自动启用，Claude Code 根本不注册 Bash 工具。
* 仅匹配 `Bash` 的 hook 永远不会在那里触发。

<h5 id="write">
  Write
</h5>

创建或覆盖文件。

| 字段 | 类型 | 示例 | 描述 |
| :- | :- | :- | :- |
| `file_path` | string | `"/path/to/file.txt"` | 要写入的文件的绝对路径 |
| `content` | string | `"file content"` | 要写入文件的内容 |

<h5 id="edit">
  Edit
</h5>

替换现有文件中的字符串。

| 字段 | 类型 | 示例 | 描述 |
| :- | :- | :- | :- |
| `file_path` | string | `"/path/to/file.txt"` | 要编辑的文件的绝对路径 |
| `old_string` | string | `"original text"` | 要查找和替换的文本 |
| `new_string` | string | `"replacement text"` | 替换文本 |
| `replace_all` | boolean | `false` | 是否替换所有出现 |

<h5 id="read">
  Read
</h5>

读取文件内容。

| 字段 | 类型 | 示例 | 描述 |
| :- | :- | :- | :- |
| `file_path` | string | `"/path/to/file.txt"` | 要读取的文件的绝对路径 |
| `offset` | number | `10` | 可选行号以开始读取 |
| `limit` | number | `50` | 可选要读取的行数 |

<h5 id="glob">
  Glob
</h5>

查找与 glob 模式匹配的文件。

| 字段 | 类型 | 示例 | 描述 |
| :- | :- | :- | :- |
| `pattern` | string | `"**/*.ts"` | 要匹配文件的 glob 模式 |
| `path` | string | `"/path/to/dir"` | 可选要搜索的目录。默认为当前工作目录 |

<h5 id="grep">
  Grep
</h5>

使用正则表达式搜索文件内容。

| 字段 | 类型 | 示例 | 描述 |
| :- | :- | :- | :- |
| `pattern` | string | `"TODO.*fix"` | 要搜索的正则表达式模式 |
| `path` | string | `"/path/to/dir"` | 可选要搜索的文件或目录 |
| `glob` | string | `"*.ts"` | 可选 glob 模式以过滤文件 |
| `output_mode` | string | `"content"` | `"content"`、`"files_with_matches"` 或 `"count"`。默认为 `"files_with_matches"` |
| `-i` | boolean | `true` | 不区分大小写的搜索 |
| `multiline` | boolean | `false` | 启用多行匹配 |

<h5 id="webfetch">
  WebFetch
</h5>

获取和处理网络内容。

| 字段 | 类型 | 示例 | 描述 |
| :- | :- | :- | :- |
| `url` | string | `"https://example.com/api"` | 要从中获取内容的 URL |
| `prompt` | string | `"Extract the API endpoints"` | 在获取的内容上运行的提示 |

<h5 id="websearch">
  WebSearch
</h5>

搜索网络。

| 字段 | 类型 | 示例 | 描述 |
| :- | :- | :- | :- |
| `query` | string | `"react hooks best practices"` | 搜索查询 |
| `allowed_domains` | array | `["docs.example.com"]` | 可选：仅包含来自这些域的结果 |
| `blocked_domains` | array | `["spam.example.com"]` | 可选：排除来自这些域的结果 |

<h5 id="agent">
  Agent
</h5>

生成 [子 agent](/docs/zh-CN/sub-agents)。

| 字段 | 类型 | 示例 | 描述 |
| :- | :- | :- | :- |
| `prompt` | string | `"Find all API endpoints"` | agent 要执行的任务 |
| `description` | string | `"Find API endpoints"` | 任务的简短描述 |
| `subagent_type` | string | `"Explore"` | 要使用的专门 agent 类型 |
| `model` | string | `"sonnet"` | 可选模型别名以覆盖默认值 |

当前台 Agent 调用完成时，您的 [PostToolUse hook](#posttooluse) 在 `tool_response` 中接收子 agent 的结果和运行遥测。读取这些字段以检查运行；对于跨子 agents 的令牌和成本汇总，使用 [令牌和成本计数器](/docs/zh-CN/monitoring-usage#token-counter) 过滤到 `query_source` `"subagent"`，因为 `totalTokens` 和 `usage` 仅涵盖最终请求：

| 字段 | 类型 | 示例 | 描述 |
| :- | :- | :- | :- |
| `status` | string | `"completed"` | 前台子 agents 为 `"completed"`，后台子 agents 为 `"async_launched"`。从 v2.1.198 起，子 agents 默认在后台运行，因此省略的 `run_in_background` 也产生 `"async_launched"` |
| `agentId` | string | `"a4d2c8f1e0b3a297"` | 子 agent 运行的标识符 |
| `content` | array | `[{"type": "text", "text": "Found 12 endpoints..."}]` | 子 agent 的最终文本块，或对于其报告通过 `SubagentHandback` 的子 agent，关于该交接的简短说明代替 |
| `resolvedModel` | string | `"claude-sonnet-4-5"` | 子 agent 启动的模型，可能与请求的模型不同 |
| `modelsUsed` | array | `["claude-sonnet-4-5", "claude-haiku-4-5"]` | 按顺序使用的模型，连续重复折叠；仅在模型在运行中交换时设置。需要 Claude Code v2.1.212 或更高版本 |
| `totalTokens` | number | `12450` | 子 agent 最终 API 请求的令牌计数：输入、输出和缓存令牌合并。这不是整个运行的总计 |
| `totalDurationMs` | number | `48211` | 子 agent 运行的挂钟持续时间 |
| `totalToolUseCount` | number | `7` | 子 agent 进行的工具调用计数 |
| `usage` | object | `{"input_tokens": 8320, ...}` | 最终 API 请求的每类型令牌分解：`input_tokens`、`output_tokens`、`cache_creation_input_tokens`、`cache_read_input_tokens` |

在 Claude Code v2.1.271 或更高版本上，使用 [`SubagentHandback`](/docs/zh-CN/tools-reference) 工具运行的子 agent（Claude Code 在 [自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode) 中提供）通过该工具而不是作为文本返回其报告。其 `completed` 结果的 `content` 字段然后携带关于该交接的简短说明而不是报告本身。要读取报告，匹配 `PreToolUse` 或 `PostToolUse` hook 在 `SubagentHandback` 上并读取 `tool_input.message`。

对于后台子 agents，工具在任务移到后台时返回，因此 `tool_response` 不携带使用字段：后台启动立即返回，前台任务在 Claude Code 在运行中将其后台化时返回。它有 `status: "async_launched"`、`agentId`、`description`、`prompt`、`outputFile` 和 `resolvedModel`。

在 `completed` 响应上，`resolvedModel` 命名子 agent 启动的模型，可能与 `tool_input` 中的 `model` 值不同，如当 `availableModels` 或另一个覆盖适用时。在 `async_launched` 响应上，`resolvedModel` 命名 agent 移到后台时使用的模型，因此在后台化之前发生的交换反映在那里。`modelsUsed` 和后台化时间 `resolvedModel` 行为需要 Claude Code v2.1.212 或更高版本。

<a id="askuserquestion" />

<h5 id="askuserquestion">
  AskUserQuestion
</h5>

向用户提出一到四个多选问题。

| 字段 | 类型 | 示例 | 描述 |
| :- | :- | :- | :- |
| `questions` | array | `[{"question": "Which framework?", "header": "Framework", "options": [{"label": "React"}], "multiSelect": false}]` | 要呈现的问题，每个都有 `question` 字符串、简短 `header`、`options` 数组和可选 `multiSelect` 标志 |
| `answers` | object | `{"Which framework?": "React"}` | 可选。将问题文本映射到选定的选项标签。多选答案用逗号连接标签。Claude 不设置此字段；通过 `updatedInput` 提供它以以编程方式回答 |

<h5 id="exitplanmode">
  ExitPlanMode
</h5>

呈现计划并要求用户在 Claude 离开 [plan mode](/docs/zh-CN/permission-modes#analyze-before-you-edit-with-plan-mode) 之前批准它。Claude 在调用工具之前将计划写入磁盘上的文件，因此来自模型的字面 `tool_input` 通常为空。Claude Code 在将输入传递给 hooks 之前注入计划内容和文件路径。

| 字段 | 类型 | 示例 | 描述 |
| :- | :- | :- | :- |
| `plan` | string | `"## Refactor auth\n1. Extract..."` | Markdown 中的计划内容。从磁盘上的计划文件注入 |
| `planFilePath` | string | `"/Users/.../plans/refactor-auth.md"` | 计划文件的路径。注入 |
| `allowedPrompts` | array | `[{"tool": "Bash", "prompt": "run tests"}]` | 已弃用。Claude Code 接受该字段但忽略它。在 v2.1.205 之前，它携带 Claude 请求以实现计划的基于提示的权限 |

在 `PostToolUse` 中，`tool_response` 是一个包含 `plan` 和 `filePath` 字段的对象，保持批准的计划，加上内部状态标志。读取 `tool_response.plan` 以获取计划内容，而不是从磁盘重新读取文件。

<h4 id="pretooluse-decision-control">
  PreToolUse 决策控制
</h4>

`PreToolUse` hooks 可以控制工具调用是否继续。与使用顶级 `decision` 字段的其他 hooks 不同，PreToolUse 在 `hookSpecificOutput` 对象内返回其决策。这给了它更丰富的控制：四个结果（允许、拒绝、询问或延迟）加上在执行前修改工具输入的能力。

| 字段 | 描述 |
| :- | :- |
| `permissionDecision` | `"allow"` 跳过权限提示，除了 [任何模式自动批准的操作](/docs/zh-CN/permission-modes#actions-no-mode-auto-approves) 和 `AskUserQuestion` 和 `ExitPlanMode`，它们需要 [`updatedInput` 与其配对](#allow-with-updatedinput)。`"deny"` 防止工具调用。`"ask"` 提示用户确认。`"defer"` 优雅地退出，以便稍后可以恢复工具。[拒绝和询问规则](/docs/zh-CN/permissions#manage-permissions) 仍然被评估，无论 hook 返回什么 |
| `permissionDecisionReason` | 对于 `"ask"`，显示给用户但不显示给 Claude。对于 `"deny"`，显示给 Claude。对于 `"allow"` 和 `"defer"`，仅写入 [调试日志](#debug-hooks) |
| `updatedInput` | 在执行前修改工具的输入参数。替换整个输入对象，因此在修改的输入旁边包含未更改的字段。Claude Code 根据您的 hook 返回的输入而不是 Claude 发送的输入评估权限规则和 Bash 命令的 [自动后台资格](/docs/zh-CN/tools-reference#background-commands)。与 `"allow"` 结合以自动批准，或与 `"ask"` 结合以向用户显示修改的输入。对于 `"defer"`，被忽略 |
| `additionalContext` | 与工具结果一起添加到 Claude 上下文的字符串。当 `permissionDecision` 为 `"defer"` 时被忽略。有关如何传递文本以及放入其中的内容，请参阅 [为 Claude 添加上下文](#add-context-for-claude) |

当多个 PreToolUse hooks 返回不同的决策时，优先级为 `deny` > `defer` > `ask` > `allow`。

通过退出 2 阻止的 hook 路由方式与 `"deny"` 相同：Claude 看到 stderr 消息作为拒绝原因。

当 hook 返回 `"ask"` 时，显示给用户的权限提示包含一个标签，标识 hook 来自何处：`[settings]` 对于来自任何设置文件或 agent frontmatter 的 hook，`[plugin:<name>]` 对于插件的 hook，或 `[skill]` 对于来自 skill frontmatter 的 hook。这帮助用户理解哪个配置源请求确认。

hook 的 `"ask"` 也在 [自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode) 中强制权限提示：分类器仍然可以拒绝工具调用，但它无法静默批准调用。在 v2.1.211 之前，分类器可以批准在 [沙箱](/docs/zh-CN/sandboxing) 外运行的 Bash 命令而不显示 hook 请求的提示；分类器仍然对该命令应用了自己的安全规则，hook `"deny"` 总是被尊重。

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PreToolUse",
    "permissionDecision": "allow",
    "permissionDecisionReason": "My reason here",
    "updatedInput": {
      "field_to_modify": "new value"
    },
    "additionalContext": "Current environment: production. Proceed with caution."
  }
}
```

<span id="allow-with-updatedinput" />

在 [非交互模式](/docs/zh-CN/headless) 中使用 `-p` 标志，Claude Code 仅在运行有 [权限主机](/docs/zh-CN/headless#turn-off-permission-prompts-in-unattended-runs) 来接收提示时提供 `AskUserQuestion` 和 `ExitPlanMode`，如 Agent SDK `canUseTool` 回调。这些工具需要用户交互。返回 `permissionDecision: "allow"` 与 `updatedInput` 一起满足该要求：hook 从 stdin 读取工具的输入，通过您自己的 UI 收集答案，并在 `updatedInput` 中返回它，以便工具运行而不提示。仅返回 `"allow"` 对这些工具不充分。对于 `AskUserQuestion`，回显原始 `questions` 数组并添加一个 [`answers`](#askuserquestion) 对象，将每个问题的文本映射到选定的答案。

从 v2.1.199 起，一个 MCP 工具，其服务器用 [`_meta["anthropic/requiresUserInteraction"]`](/docs/zh-CN/mcp#require-approval-for-a-specific-tool) 标记它，更严格：hook 无法用 `"allow"` 跳过其批准提示，无论是否有 `updatedInput`，因为 Claude Code 无法确认 hook 收集了工具需要的交互。

<Note>
  PreToolUse 以前使用顶级 `decision` 和 `reason` 字段，但这些对此事件已弃用。改用 `hookSpecificOutput.permissionDecision` 和 `hookSpecificOutput.permissionDecisionReason`。已弃用的值 `"approve"` 和 `"block"` 映射到 `"allow"` 和 `"deny"` 分别。PostToolUse 和 Stop 等其他事件继续使用顶级 `decision` 和 `reason` 作为其当前格式。
</Note>

<h4 id="defer-a-tool-call-for-later">
  延迟工具调用以供稍后使用
</h4>

`"defer"` 用于运行 `claude -p` 作为子进程并读取其 JSON 输出的集成，如 Agent SDK 应用或构建在 Claude Code 之上的自定义 UI。它让该调用进程在工具调用处暂停 Claude，通过其自己的界面收集输入，并从中断处恢复。Claude Code 仅在 [非交互模式](/docs/zh-CN/headless) 中使用 `-p` 标志时尊重此值。在交互式会话中，它记录警告并忽略 hook 结果。

`AskUserQuestion` 工具是典型情况：Claude 想问用户什么，但没有终端来回答。`-p` 运行仅当它有 [权限主机](/docs/zh-CN/headless#turn-off-permission-prompts-in-unattended-runs) 时提供 `AskUserQuestion`，如您使用 `--permission-prompt-tool` 传递的 MCP 工具，因此使用一个启动运行。往返工作如下：

1. Claude 调用 `AskUserQuestion`。`PreToolUse` hook 触发。
2. hook 返回 `permissionDecision: "defer"`。工具不执行。进程以 `stop_reason: "tool_deferred"` 退出，待处理的工具调用保留在成绩单中。
3. 调用进程从 SDK 结果读取 `deferred_tool_use`，在其自己的 UI 中呈现问题，并等待答案。
4. 调用进程运行 `claude -p --resume <session-id>`，带有相同的权限主机。相同的工具调用再次触发 `PreToolUse`。
5. hook 返回 `permissionDecision: "allow"`，答案在 `updatedInput` 中。工具执行，Claude 继续。

`deferred_tool_use` 字段携带工具的 `id`、`name` 和 `input`。`input` 是 Claude 为工具调用生成的参数，在执行前捕获：

```json theme={null}
{
  "type": "result",
  "subtype": "success",
  "stop_reason": "tool_deferred",
  "session_id": "abc123",
  "deferred_tool_use": {
    "id": "toolu_01abc",
    "name": "AskUserQuestion",
    "input": { "questions": [{ "question": "Which framework?", "header": "Framework", "options": [{"label": "React"}, {"label": "Vue"}], "multiSelect": false }] }
  }
}
```

没有超时或重试限制。会话保留在磁盘上直到您恢复它，受 [`cleanupPeriodDays`](/docs/zh-CN/settings-reference#cleanupperioddays) 保留扫描的约束，默认情况下在 30 天后删除会话文件，遵循 [保留扫描规则](/docs/zh-CN/claude-directory#cleaned-up-automatically)。如果恢复时答案还没准备好，hook 可以再次返回 `"defer"`，进程以相同方式退出。调用进程通过最终从 hook 返回 `"allow"` 或 `"deny"` 来控制何时打破循环。

`"defer"` 仅在 Claude 在回合中进行单个工具调用时有效。如果 Claude 一次进行多个工具调用，`"defer"` 被忽略并带有警告，工具通过正常权限流程进行。约束存在是因为恢复只能重新运行一个工具：没有办法从批次中延迟一个调用而不留下其他未解决的。

如果恢复时延迟的工具不再可用，进程以 `stop_reason: "tool_deferred_unavailable"` 和 `is_error: true` 退出，hook 触发前。这发生在为恢复的会话未连接提供工具的 MCP 服务器时。`deferred_tool_use` 有效负载仍然包含，以便您可以识别哪个工具丢失。

<Note>
  要在 plan mode 中恢复延迟会话，请与 `--resume` 一起传递 [`--permission-prompt-tool`](/docs/zh-CN/cli-reference#cli-flags)，以便 Claude Code 可以呈现计划以供批准。如果您传递某些其他启动标志，恢复的运行不会返回到 plan mode；请参阅 [使用 `-p` 在 plan mode 中恢复](/docs/zh-CN/sessions#resume-in-plan-mode-with-p)。需要 Claude Code v2.1.246 或更高版本。

  当您使用 `-p` 恢复时，Claude Code 不会恢复任何其他存储的权限模式。它在新 `claude -p` 运行会启动的权限模式中启动运行，因此如果延迟会话使用了一个，请再次传递 `--permission-mode` 或 `--dangerously-skip-permissions`。当您使用 `claude --resume <session-id>` 恢复而不使用 `-p` 时，Claude Code 恢复存储的权限模式，除了 [恢复时的权限模式](/docs/zh-CN/sessions#permission-mode-on-resume) 中列出的例外。
</Note>

<h3 id="permissionrequest">
  PermissionRequest
</h3>

在 Claude Code 即将要求您许可使用工具时运行。在无法显示提示的会话中，如 [非交互模式](/docs/zh-CN/headless) 中的后台子 agents，Claude Code 仍然运行这些 hooks，如果没有 hook 返回决策，它拒绝工具调用。
使用 [PermissionRequest 决策控制](#permissionrequest-decision-control) 代表用户允许或拒绝。

当您需要 Claude 要求许可使用工具的时刻的信号时使用此事件。Claude Code 仅在提示等待约六秒后才运行 [Notification](#notification) hook，带有 `permission_prompt` 类型。

Claude Code 不为沙箱命令的 [网络请求](/docs/zh-CN/sandboxing#network-isolation) 运行 PermissionRequest hooks。要获得该提示的信号，请使用 `permission_prompt` 通知类型。

在工具名称上匹配，与 PreToolUse 相同的值。

<h4 id="permissionrequest-input">
  PermissionRequest 输入
</h4>

PermissionRequest hooks 接收 `tool_name` 和 `tool_input` 字段，如 PreToolUse hooks，但没有 `tool_use_id`。对于 MCP 工具，它们也接收 [`mcp_server`](#pretooluse-input) 对象。可选的 `permission_suggestions` 数组包含 Claude Code 为此请求建议的 [权限更新](#permission-update-entries)，如添加允许规则或更改权限模式。

`permission_suggestions` 数组不是您看到的选项的精确列表，因为每个权限对话构建自己的选项。某些对话（如文件编辑的对话）根本不读取数组，并从请求本身派生其选项。读取它的对话仍然可以保留一个选项，其建议保留在数组中，例如当 [`allowManagedPermissionRulesOnly`](/docs/zh-CN/settings-reference#allowmanagedpermissionrulesonly) 隐藏规则保存选项时。它也可以提供没有建议条目的选项，如 [**Yes, and switch to auto mode**](/docs/zh-CN/permission-modes#switch-permission-modes)，它直接更改权限模式而不是通过权限更新。

PreToolUse hooks 在每个工具调用之前运行，无论它是否需要权限。PermissionRequest hooks 仅在 Claude Code 即将要求您许可时运行，或当它会以其他方式自动拒绝无法提示的调用时。两个事件都不为 [`EndConversation`](/docs/zh-CN/tools-reference#endconversation-tool-behavior) 触发。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PermissionRequest",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf node_modules",
    "description": "Remove node_modules directory"
  },
  "permission_suggestions": [
    {
      "type": "addRules",
      "rules": [{ "toolName": "Bash", "ruleContent": "rm -rf node_modules" }],
      "behavior": "allow",
      "destination": "localSettings"
    }
  ]
}
```

<h4 id="permissionrequest-decision-control">
  PermissionRequest 决策控制
</h4>

`PermissionRequest` hooks 可以允许或拒绝权限请求。除了所有 hooks 可用的 [JSON 输出字段](#json-output) 外，您的 hook 脚本可以返回一个 `decision` 对象，带有这些事件特定的字段：

| 字段 | 描述 |
| :- | :- |
| `behavior` | `"allow"` 授予权限，`"deny"` 拒绝它。[拒绝和询问规则](/docs/zh-CN/permissions#manage-permissions) 仍然被评估，因此返回 `"allow"` 的 hook 不会覆盖匹配的拒绝规则 |
| `updatedInput` | 仅对 `"allow"`：在执行前修改工具的输入参数。替换整个输入对象，因此在修改的输入旁边包含未更改的字段。修改的输入针对拒绝和询问规则重新评估 |
| `updatedPermissions` | 仅对 `"allow"`：[权限更新条目](#permission-update-entries) 数组以应用，如添加允许规则或更改会话权限模式 |
| `message` | 仅对 `"deny"`：告诉 Claude 为什么权限被拒绝 |
| `interrupt` | 仅对 `"deny"`：如果 `true`，停止 Claude |

不带 `decision` 对象退出 2 的 hook 保持权限流程不变，其 stderr 被丢弃。仅 `decision` 对象可以授予或拒绝请求。

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionRequest",
    "decision": {
      "behavior": "allow",
      "updatedInput": {
        "command": "npm run lint"
      }
    }
  }
}
```

<h4 id="permission-update-entries">
  权限更新条目
</h4>

`updatedPermissions` 输出字段和 [`permission_suggestions` 输入字段](#permissionrequest-input) 都使用相同的条目对象数组。每个条目有一个 `type` 来确定其他字段，以及一个 `destination` 来控制更改写入的位置。

| `type` | 字段 | 效果 |
| :- | :- | :- |
| `addRules` | `rules`、`behavior`、`destination` | 添加权限规则。`rules` 是 `{toolName, ruleContent?}` 对象的数组。省略 `ruleContent` 以匹配整个工具。`behavior` 是 `"allow"`、`"deny"` 或 `"ask"` |
| `replaceRules` | `rules`、`behavior`、`destination` | 用提供的 `rules` 替换 `destination` 处给定 `behavior` 的所有规则 |
| `removeRules` | `rules`、`behavior`、`destination` | 删除给定 `behavior` 的匹配规则 |
| `setMode` | `mode`、`destination` | 更改权限模式。有效模式为 `default`、`auto`、`acceptEdits`、`dontAsk`、`bypassPermissions`、`plan` 和 `manual` 作为 `default` 的别名。`manual` 别名需要 Claude Code v2.1.200 或更高版本 |
| `addDirectories` | `directories`、`destination` | 添加工作目录。`directories` 是路径字符串的数组 |
| `removeDirectories` | `directories`、`destination` | 删除工作目录 |

<Note>
  `setMode` 与 `bypassPermissions` 仅在您使用已可用的绕过模式启动会话时生效：`--dangerously-skip-permissions`、`--permission-mode bypassPermissions`、`--allow-dangerously-skip-permissions` 或 [用户、`--settings` 或托管设置](/docs/zh-CN/settings-reference#permissions-defaultmode) 中的 `permissions.defaultMode: "bypassPermissions"`。否则更新是无操作。当 [`permissions.disableBypassPermissionsMode`](/docs/zh-CN/permissions#managed-settings) 禁用模式或会话在 [受限模式](/docs/zh-CN/cli-reference#cli-flags) 中启动时，更新也是无操作。

  `bypassPermissions` 永远不会作为 `defaultMode` 持久化，无论 `destination` 如何。
</Note>

每个条目上的 `destination` 字段确定更改是保留在内存中还是持久化到设置文件。

| `destination` | 写入 |
| :- | :- |
| `session` | 仅在内存中，会话结束时丢弃 |
| `localSettings` | `.claude/settings.local.json` |
| `projectSettings` | `.claude/settings.json` |
| `userSettings` | `~/.claude/settings.json` |

hook 可以回显它接收的 `permission_suggestions` 之一作为其自己的 `updatedPermissions` 输出。

<h3 id="posttooluse">
  PostToolUse
</h3>

在工具成功完成后立即运行。

在工具名称上匹配，与 PreToolUse 相同的值。

当工具名称不是正确的过滤器时更广泛地匹配：

* 要在任何工具成功完成后运行 hook，省略 `matcher` 或将其设置为 `"*"`。您的 hook 然后可以自己发现更改了什么，例如通过运行 `git status --porcelain`，它也列出 `git diff` 错过的未跟踪文件。对于失败的工具调用，在 [PostToolUseFailure](#posttoolusefailure) 下添加相同的 hook。
* 要在特定文件更改时运行 hook，无论什么写入它，请使用 [FileChanged](#filechanged)。当 `Bash` 命令或 Claude Code 外的进程重写同一文件时，Claude Code 不运行匹配 `Edit|Write` 的 `PostToolUse` hook。

<h4 id="posttooluse-input">
  PostToolUse 输入
</h4>

`PostToolUse` hooks 在工具已经成功执行后触发。输入包括 `tool_input`（发送给工具的参数）和 `tool_response`（它返回的结果）。两者的确切模式取决于工具。文件工具 `tool_input` 路径以与 [PreToolUse](#pretooluse-input) 相同的格式到达：始终绝对，带有平台的本机分隔符，因此 Windows 上的反斜杠。对于 MCP 工具，输入也携带 [`mcp_server`](#pretooluse-input) 对象。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/file.txt",
    "content": "file content"
  },
  "tool_response": {
    "filePath": "/path/to/file.txt",
    "type": "create"
  },
  "tool_use_id": "toolu_01ABC123...",
  "duration_ms": 12
}
```

| 字段 | 描述 |
| :- | :- |
| `duration_ms` | 可选。工具执行时间（毫秒）。不包括权限提示和 PreToolUse hooks 中花费的时间 |

<h4 id="posttooluse-decision-control">
  PostToolUse 决策控制
</h4>

`PostToolUse` hooks 可以在工具执行后提供反馈给 Claude。除了所有 hooks 可用的 [JSON 输出字段](#json-output) 外，您的 hook 脚本可以返回这些事件特定的字段：

| 字段 | 描述 |
| :- | :- |
| `decision` | `"block"` 在工具结果旁边添加 `reason`。Claude 仍然看到原始输出；要替换它，使用 `updatedToolOutput` |
| `reason` | 当 `decision` 为 `"block"` 时显示给 Claude 的解释 |
| `additionalContext` | 与工具结果一起添加到 Claude 上下文的字符串。有关如何传递文本以及放入其中的内容，请参阅 [为 Claude 添加上下文](#add-context-for-claude) |
| `classifierContext` | 关于此调用结果的简短说明，用于 [自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode) 分类器而不是 Claude。有关如何传递文本以及放入其中的内容，请参阅 [为自动模式分类器注释结果](#annotate-a-result-for-the-auto-mode-classifier)。需要 Claude Code v2.1.236 或更高版本 |
| `updatedToolOutput` | 在将工具的输出发送给 Claude 之前用提供的值替换它。该值必须与工具的输出形状匹配 |
| `updatedMCPToolOutput` | 仅替换 [MCP 工具](#match-mcp-tools) 的输出。优先使用 `updatedToolOutput`，它适用于所有工具 |

下面的示例替换 `Bash` 调用的输出。替换值与 `Bash` 工具的输出形状匹配：

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "additionalContext": "Additional information for Claude",
    "updatedToolOutput": {
      "stdout": "[redacted]",
      "stderr": "",
      "interrupted": false,
      "isImage": false
    }
  }
}
```

<Warning>
  `updatedToolOutput` 仅更改 Claude 看到的内容。工具已经在 hook 触发时运行，因此任何写入的文件、执行的命令或发送的网络请求已经生效。遥测如 OpenTelemetry 工具跨度和分析事件也在 hook 运行之前捕获原始输出。要在运行前防止或修改工具调用，请改用 [PreToolUse](#pretooluse) hook。

  替换值必须与工具的输出形状匹配。内置工具返回结构化对象而不是纯字符串。例如，`Bash` 返回一个带有 `stdout`、`stderr`、`interrupted` 和 `isImage` 字段的对象。对于内置工具，不与工具的输出模式匹配的值被忽略，使用原始输出。MCP 工具输出通过而不进行模式验证。剥离 Claude 需要的错误详情可能导致它在错误的假设下继续。
</Warning>

<h4 id="annotate-a-result-for-the-auto-mode-classifier">
  为自动模式分类器注释结果
</h4>

返回 `classifierContext` 以向 [自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode) 分类器发送关于工具调用结果的简短说明，而不是向 Claude。分类器 [永远不接收工具结果本身](/docs/zh-CN/permission-modes#how-the-classifier-evaluates-actions)，因此此字段是告诉它在审查后续操作之前关于调用返回的内容的支持方式。该字段需要 Claude Code v2.1.236 或更高版本。

下面的示例告诉分类器查询的输出来自何处：

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUse",
    "classifierContext": "This query ran against the staging database, not production."
  }
}
```

分类器给予说明的权重取决于您配置 hook 的位置：

* **在 Claude Code 中配置的 Hooks**：对于来自设置文件、插件、skills 和 agent frontmatter 的 hooks，分类器将说明视为未验证的、应用程序提供的上下文。说明永远不会建立用户意图，如果它声称您批准或请求了什么，分类器会根据您在对话中的自己的消息检查该声明
* **进程内 Agent SDK 回调**：当应用程序嵌入 Claude Code 将 hook 注册为 [TypeScript SDK 回调](/docs/zh-CN/agent-sdk/hooks) 并在实时会话期间返回说明时，分类器可能会将用户语句（在说明中中继）视为用户意图。这样的语句可以满足分类器会接受来自您发送的消息的同意要求，但它永远不会解除您自己的消息也无法解除的阻止。会话恢复后，Claude Code 将恢复的说明视为未验证的上下文。当两个组的 hooks 注释同一调用时，分类器将组合说明视为未验证

Claude Code 在传递说明时应用这些限制：

* **长度**：Claude Code 将一个工具调用的说明上限为 2,000 个字符，并截断其余部分。上限在响应该调用的每个 hook 中共享
* **仅同步响应**：Claude Code 忽略 [在后台运行](#run-hooks-in-the-background) 的 hook 响应中的字段，因为该响应在 Claude Code 记录工具结果后到达
* **分类器不记录的调用**：分类器的成绩单省略只读查找，如文件读取和搜索。Claude Code 丢弃附加到其中一个调用的说明
* **与重写的交互**：当说明描述您用 `updatedToolOutput` 替换的输出时，在同一 hook 响应中返回两个字段。如果该重写被拒绝或另一个 hook 的重写替换它，Claude Code 丢弃说明。Claude Code 传递您返回的说明而不重写，即使另一个 hook 重写输出

<Warning>
  分类器读取您放入 `classifierContext` 的内容作为来自托管会话的应用程序的信息，因此不要将不受信任的工具输出或第三方文本复制到其中。将说明保持为关于此一个调用的简短断言，如关于其来源的事实或关于它的用户语句；不要使用该字段传递不相关的消息或事件流。
</Warning>

<h3 id="posttoolusefailure">
  PostToolUseFailure
</h3>

在启动执行的工具失败时运行：工具抛出错误或 MCP 工具返回错误结果。使用此来记录失败、发送警报或向 Claude 提供纠正反馈。

在工具名称上匹配，与 PreToolUse 相同的值。

<Note>
  此事件不为执行前被拒绝的工具调用触发：未知工具名称、失败模式或工具特定验证的输入，或权限拒绝。验证拒绝作为 `tool_use_error` 结果返回，发生在 hooks 运行之前，因此它们既不触发 `PreToolUse` 也不触发此事件。权限拒绝触发 `PreToolUse` 但不触发此事件；请参阅 [PermissionDenied](#permissiondenied)。
</Note>

<h4 id="posttoolusefailure-input">
  PostToolUseFailure 输入
</h4>

PostToolUseFailure hooks 接收与 PostToolUse 相同的 `tool_name` 和 `tool_input` 字段，以及错误信息作为顶级字段。对于 MCP 工具，它们也接收 [`mcp_server`](#pretooluse-input) 对象。例如，失败的 `npm test` 命令可能传递：

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolUseFailure",
  "tool_name": "Bash",
  "tool_input": {
    "command": "npm test",
    "description": "Run test suite"
  },
  "tool_use_id": "toolu_01ABC123...",
  "error": "Exit code 1\nError: Cannot find module 'express'",
  "is_interrupt": false,
  "duration_ms": 4187
}
```

| 字段 | 描述 |
| :- | :- |
| `error` | 描述出错内容的字符串。格式取决于失败的工具 |
| `is_interrupt` | 可选布尔值。当失败作为中止到达 Claude Code 而不是工具报告的错误时为 True。取消运行的工具不触发此 hook；工具结果携带中断消息 |
| `duration_ms` | 可选。工具执行时间（毫秒）。不包括权限提示和 PreToolUse hooks 中花费的时间 |

`error` 字符串通常与 Claude 接收的失败工具结果相同的文本。其格式因工具和失败而异。在 `tool_name`、`is_interrupt` 和第一行 `Exit code N` 上键入您的 hook；将字符串的其余部分视为显示文本，而不是稳定格式。

* 对于 Bash 和 PowerShell，运行并退出的命令产生第一行 `Exit code N`，然后是命令产生的任何输出作为一个块，stdout 和 stderr 交错
* 有效负载也可能携带裸失败消息，没有退出代码行，当 Claude Code 无法启动 shell 进程本身时
* Claude Code 中间截断长字符串，围绕 `... [N characters truncated] ...` 标记，并可以插入自己的行，如 `Command timed out after 2m 0s`

<h4 id="posttoolusefailure-decision-control">
  PostToolUseFailure 决策控制
</h4>

`PostToolUseFailure` hooks 可以在工具失败后向 Claude 提供上下文。除了所有 hooks 可用的 [JSON 输出字段](#json-output) 外，您的 hook 脚本可以返回这些事件特定的字段：

| 字段 | 描述 |
| :- | :- |
| `additionalContext` | 与错误一起添加到 Claude 上下文的字符串。有关如何传递文本以及放入其中的内容，请参阅 [为 Claude 添加上下文](#add-context-for-claude) |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolUseFailure",
    "additionalContext": "Additional information about the failure for Claude"
  }
}
```

<h3 id="posttoolbatch">
  PostToolBatch
</h3>

在批次中的每个工具调用都已解决后运行一次，在 Claude Code 向模型发送下一个请求之前。`PostToolUse` 每个工具触发一次，这意味着当 Claude 进行并行工具调用时它并发触发。`PostToolBatch` 恰好触发一次，带有完整批次，因此它是注入取决于运行的工具集而不是任何单个工具的上下文的正确位置。此事件没有匹配器。

<h4 id="posttoolbatch-input">
  PostToolBatch 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，PostToolBatch hooks 接收 `tool_calls`，一个描述批次中每个工具调用的数组：

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "PostToolBatch",
  "tool_calls": [
    {
      "tool_name": "Read",
      "tool_input": {"file_path": "/.../ledger/accounts.py"},
      "tool_use_id": "toolu_01...",
      "tool_response": "1\tfrom __future__ import annotations\n2\t..."
    },
    {
      "tool_name": "Read",
      "tool_input": {"file_path": "/.../ledger/transactions.py"},
      "tool_use_id": "toolu_02...",
      "tool_response": "1\tfrom __future__ import annotations\n2\t..."
    }
  ]
}
```

`tool_response` 包含模型在相应 `tool_result` 块中接收的相同内容。该值是序列化字符串或内容块数组，完全如工具发出的那样。对于 `Read`，这意味着行号前缀文本而不是原始文件内容。响应可能很大，因此仅解析您需要的字段。

<Note>
  `tool_response` 形状与 `PostToolUse` 的不同。`PostToolUse` 传递工具的结构化 `Output` 对象，如 `Write` 的 `{filePath: "...", type: "create"}`；`PostToolBatch` 传递模型看到的序列化 `tool_result` 内容。
</Note>

<h4 id="posttoolbatch-decision-control">
  PostToolBatch 决策控制
</h4>

`PostToolBatch` hooks 可以为 Claude 注入上下文。除了所有 hooks 可用的 [JSON 输出字段](#json-output) 外，您的 hook 脚本可以返回这些事件特定的字段：

| 字段 | 描述 |
| :- | :- |
| `additionalContext` | 在下一个模型调用之前注入一次的上下文字符串。有关传递详情、放入其中的内容以及恢复的会话如何处理过去的值，请参阅 [为 Claude 添加上下文](#add-context-for-claude) |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PostToolBatch",
    "additionalContext": "These files are part of the ledger module. Run pytest before marking the task complete."
  }
}
```

返回 `decision: "block"` 或 `continue: false` 在下一个模型调用之前停止 agentic 循环。阻止消息来自 JSON `reason` 或 `stopReason`，或来自退出 2 的 stderr。您在成绩单中看到它作为警告，它保留在对话中，因此当对话继续时 Claude 看到它。

<h3 id="permissiondenied">
  PermissionDenied
</h3>

在 [自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode) 拒绝工具调用时运行，包括当它拒绝而没有分类器判决时，因为 [与自动模式分开的安全检查拒绝了分类器自己的请求](/docs/zh-CN/errors#auto-mode-cannot-determine-the-safety-of-an-action) 或其响应没有解析。此 hook 仅在自动模式中触发：当您手动拒绝权限对话、`PreToolUse` hook 阻止调用或 `deny` 规则匹配时不运行。使用它来记录拒绝、调整配置或告诉模型它可能重试工具调用。

在工具名称上匹配，与 PreToolUse 相同的值。

<h4 id="permissiondenied-input">
  PermissionDenied 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，PermissionDenied hooks 接收 `tool_name`、`tool_input`、`tool_use_id` 和 `reason`。对于 MCP 工具，它们也接收 [`mcp_server`](#pretooluse-input) 对象。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "auto",
  "hook_event_name": "PermissionDenied",
  "tool_name": "Bash",
  "tool_input": {
    "command": "rm -rf /tmp/build",
    "description": "Clean build directory"
  },
  "tool_use_id": "toolu_01ABC123...",
  "reason": "[Irreversible Local Destruction]"
}
```

| 字段 | 描述 |
| :- | :- |
| `reason` | 拒绝原因。对于分类器判决，在大多数会话中它命名方括号中的匹配规则，如 `[Data Exfiltration]`；有关其他形式，请参阅 [审查拒绝](/docs/zh-CN/auto-mode-config#review-denials)。对于 [无判决拒绝](#permissiondenied-decision-control)，它以 `Auto mode could not evaluate this action and is blocking it for safety` 开头。对于拒绝因为分类器模型不可用，它是固定文本 `Classifier unavailable` |

<h4 id="permissiondenied-decision-control">
  PermissionDenied 决策控制
</h4>

PermissionDenied hooks 可以告诉模型它可能重试被拒绝的工具调用。返回一个 JSON 对象，其中 `hookSpecificOutput.retry` 设置为 `true`：

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PermissionDenied",
    "retry": true
  }
}
```

当 `retry` 为 `true` 时，Claude Code 向对话添加一条消息，告诉模型它可能重试工具调用。Claude Code 不反转拒绝本身。如果您的 hook 不返回 JSON 或返回 `retry: false`，拒绝成立，模型接收原始拒绝消息。

当分类器对操作产生 [无判决](/docs/zh-CN/errors#auto-mode-cannot-determine-the-safety-of-an-action) 时，Claude Code 忽略 `retry: true`：其响应没有解析，或与自动模式分开的安全检查拒绝了分类器自己的请求。对于这些拒绝，Claude Code 已经在拒绝消息中告诉模型是否稍后重试或继续。

<h3 id="notification">
  Notification
</h3>

在 Claude Code 发送通知时运行。在通知类型上匹配。省略匹配器以对所有通知类型运行 hooks。

您即使关闭桌面通知也接收这些 hook 事件：`preferredNotifChannel` 设置，包括 `notifications_disabled`，仅更改您如何被警报，而不是您的 hook 是否运行。

| 匹配器 | 何时触发 |
| :- | :- |
| `permission_prompt` | Claude 需要您批准工具使用或沙箱命令的 [网络请求](/docs/zh-CN/sandboxing#network-isolation)，提示已等待约六秒 |
| `idle_prompt` | Claude 约 60 秒前完成响应，您自那以后没有输入 |
| `auth_success` | 身份验证完成 |
| `elicitation_dialog` | MCP 服务器打开引出表单，您约六秒没有输入 |
| `elicitation_url_dialog` | MCP 服务器要求您打开浏览器 URL，您约六秒没有输入 |
| `elicitation_complete` | MCP 服务器报告 [URL 模式引出](#elicitation-input) 完成 |
| `elicitation_response` | MCP 引出响应被发送回服务器 |
| `agent_needs_input` | 后台会话在 [agent view](/docs/zh-CN/agent-view) 在终端中打开时开始等待您的输入，或当前会话要求您一个 [agent team 队友的终端设置问题](/docs/zh-CN/agent-teams#choose-a-display-mode) 或自动模式的 [分类器请求费用](/docs/zh-CN/auto-mode-classifier-billing) 通知，您约六秒没有输入 |
| `agent_completed` | 后台会话完成或失败。仅在 [agent view](/docs/zh-CN/agent-view) 在终端中打开时触发 |
| `quota_auto_resume_fired` | Claude Code 在 claude.ai 使用限制暂停它后继续您的任务：在重置时，或更早当您在 Claude Code 中做的某事（如添加使用信用、升级您的计划或切换模型）在等待期间使使用可用时，带有 [模型设置异常](/docs/zh-CN/interactive-mode#wait-for-a-usage-limit-to-reset) |
| `quota_auto_resume_stale` | claude.ai 使用限制在您的计算机睡眠超过约 30 分钟时重置。Claude Code 等待您按 `Enter` 而不是继续。在更短的睡眠后它继续并改为触发 `quota_auto_resume_fired` |
| `quota_auto_resume_disabled` | Claude Code 结束其对 claude.ai 使用限制的等待而不继续您的任务：[`autoContinueAtUsageLimit`](/docs/zh-CN/settings-reference#autocontinueatusagelimit) 关闭或重置在 Claude Code 自己启动的等待期间移动超过 24 小时，继续的任务继续命中限制，或继续在到达模型之前被阻止。当您按 `Esc` 或 `Ctrl+C` 或选择 **Don't continue automatically** 时不触发 |

`agent_needs_input` 和 `agent_completed` 类型需要 Claude Code v2.1.198 或更高版本。

`quota_auto_resume_fired`、`quota_auto_resume_stale` 和 `quota_auto_resume_disabled` 类型需要 Claude Code v2.1.234 或更高版本。

在终端会话中，沙箱命令的网络请求的 `permission_prompt` 需要 Claude Code v2.1.246 或更高版本。

队友的终端设置问题的 `agent_needs_input` 需要 Claude Code v2.1.248 或更高版本。

<Note>
  `permission_prompt`、`idle_prompt`、`elicitation_dialog` 和 `elicitation_url_dialog` 类型与桌面通知共享其时序，因此在终端会话中您仅在您似乎远离终端时看到它们：

  * 期望 `permission_prompt` 一旦您约六秒没有输入。计时器在权限提示出现时启动，每次按键推迟它。要在 Claude 要求许可使用工具时立即运行 hook，请改用 [PermissionRequest](#permissionrequest)。
  * 期望 `idle_prompt` 约 60 秒后 Claude 完成响应，仅当您自那以后没有输入时。Claude Code 在等待 claude.ai 使用限制重置时不发送 `idle_prompt`。当等待自己结束时，其中一个 `quota_auto_resume_*` 类型触发。
  * 期望 `elicitation_dialog` 对于引出表单或 `elicitation_url_dialog` 对于浏览器 URL 请求，一旦您约六秒没有输入。两者共享与 `permission_prompt` 相同的六秒门：计时器在对话出现时启动，每次按键推迟它。

  权限请求或引出在另一个对话在屏幕上时到达保持相同的六秒门，从请求到达时计时。其通知可以在请求仍在等待打开的对话后面时到达您。
</Note>

Claude Code 在会话中以不同方式计时 `permission_prompt`，其中它向 Agent SDK 的 [`canUseTool` 回调](/docs/zh-CN/agent-sdk/user-input) 发送权限请求，这是 Claude Desktop 和 VS Code 扩展如何托管 Claude Code 的方式：

* 期望 `permission_prompt` 约六秒后 Claude 要求权限。Claude Code 在您输入时不推迟它。
* 如果您或 [PermissionRequest](#permissionrequest) hook 更早回答，Claude Code 不运行 `permission_prompt`。
* 设置 [`CLAUDE_CODE_DISABLE_PERMISSION_PROMPT_NOTIFY_HOOKS`](/docs/zh-CN/env-vars) 为 `1` 以在这些会话中关闭 `permission_prompt`。

在 v2.1.233 之前，`permission_prompt` 在这些会话中不触发。

使用单独的匹配器根据通知类型运行不同的处理程序。此配置在 Claude 需要权限批准时触发权限特定的警报脚本，在 Claude 空闲时触发不同的通知：

```json theme={null}
{
  "hooks": {
    "Notification": [
      {
        "matcher": "permission_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/permission-alert.sh"
          }
        ]
      },
      {
        "matcher": "idle_prompt",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/idle-notification.sh"
          }
        ]
      }
    ]
  }
}
```

<h4 id="notification-input">
  Notification 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，Notification hooks 接收 `message` 与通知文本、可选 `title` 和 `notification_type` 指示哪个类型触发。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Notification",
  "message": "Claude needs your permission",
  "title": "Permission needed",
  "notification_type": "permission_prompt"
}
```

Notification hooks 无法阻止或修改通知。Claude Code 丢弃它们的 `systemMessage` 和 `continue` 字段，但仍然发出 [`terminalSequence`](#emit-terminal-notifications)，这是桌面通知示例所依赖的。Notification hooks 用于副作用，如将通知转发到外部服务。

<h3 id="subagentstart">
  SubagentStart
</h3>

在 Claude 使用 Agent 工具生成子 agent 时运行，当 Claude [恢复子 agent](/docs/zh-CN/sub-agents#resume-subagents) 时，以及每次进程内 [agent team](/docs/zh-CN/agent-teams) 队友处理新消息时。支持匹配器以按 agent 类型名称过滤。对于内置 agents，这是 agent 名称如 `general-purpose`、`Explore` 或 `Plan`。对于 [自定义子 agents](/docs/zh-CN/sub-agents)，这是 agent 的 frontmatter 中的 `name` 字段，而不是文件名。

对于由 [插件](/docs/zh-CN/plugins/overview) 提供的子 agents，agent 类型是插件范围的标识符，如 `my-plugin:reviewer`，而不是裸 frontmatter 名称。冒号将插件范围的名称放在正则表达式路径上，因此用 `^` 和 `$` 锚定匹配器以获得精确匹配：`^my-plugin:reviewer$`。

<h4 id="subagentstart-input">
  SubagentStart 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，SubagentStart hooks 接收 `agent_id` 与子 agent 的唯一标识符和 `agent_type` 与匹配器过滤的 agent 名称。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SubagentStart",
  "agent_id": "agent-abc123",
  "agent_type": "Explore"
}
```

SubagentStart hooks 无法阻止子 agent 创建，但它们可以向子 agent 注入上下文。除了所有 hooks 可用的 [JSON 输出字段](#json-output) 外，您可以返回：

| 字段 | 描述 |
| :- | :- |
| `additionalContext` | 在子 agent 对话开始时添加到子 agent 上下文的字符串，在其第一个提示之前。有关如何传递文本以及放入其中的内容，请参阅 [为 Claude 添加上下文](#add-context-for-claude) |

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "SubagentStart",
    "additionalContext": "Follow security guidelines for this task"
  }
}
```

当 hook 再次为同一子 agent 运行时，Claude Code 仅在子 agent 的上下文还不包含来自早期运行的副本时注入返回的上下文。在启动时注入的副本保留在原位，保持子 agent 的 [prompt cache](/docs/zh-CN/prompt-caching#subagents-and-the-cache) 完整。在 [自动压缩](/docs/zh-CN/sub-agents#auto-compaction) 丢弃该副本后，Claude Code 再次注入下一个运行的上下文。

<h3 id="subagentstop">
  SubagentStop
</h3>

在 Claude Code 子 agent 完成响应时运行。在 agent 类型上匹配，与 SubagentStart 相同的值。

<h4 id="subagentstop-input">
  SubagentStop 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，SubagentStop hooks 接收 `stop_hook_active`、`agent_id`、`agent_type`、`agent_transcript_path` 和 `last_assistant_message`。`agent_type` 字段是用于匹配器过滤的值。`transcript_path` 是主会话的成绩单，而 `agent_transcript_path` 是子 agent 自己的成绩单，存储在嵌套 `subagents/` 文件夹中。`last_assistant_message` 字段包含子 agent 最终响应的文本内容，因此 hooks 可以访问它而不解析成绩单文件。

不是每个 SubagentStop 事件都来自 Claude 生成的子 agent。Claude Code 也为其自己的某些功能运行内部 agents，如 [提示建议](/docs/zh-CN/interactive-mode#prompt-suggestions) 和 [`/btw` 侧问题](/docs/zh-CN/interactive-mode#side-questions-with-%2Fbtw)，当其中一个完成时 SubagentStop 触发。对于这些事件，`agent_type` 是会话本身运行的 agent 名称，如用 [`--agent`](/docs/zh-CN/cli-reference#cli-flags) 或 [`agent` 设置](/docs/zh-CN/settings-reference#agent) 设置的，当会话运行而不带一个时为空字符串。

命名 agent 类型的 `matcher` 不匹配空 `agent_type`。一个 matcher 被省略、`""`、`"*"` 或是匹配空字符串的正则表达式的 hook 也为带有空 `agent_type` 的事件运行。

在 Claude Code v2.1.271 或更高版本上，使用 [`SubagentHandback`](/docs/zh-CN/tools-reference) 工具运行的子 agent 在它停止之前通过该工具传递其报告。`last_assistant_message` 字段然后保持子 agent 的结束文本（如果有），这不是传递的报告。报告是该调用的 `message` 输入，`PreToolUse` 或 `PostToolUse` hook 匹配 `SubagentHandback` 接收作为 `tool_input.message`。

SubagentStop hooks 也接收 [Stop 输入](#stop-input) 下描述的 `background_tasks` 和 `session_crons` 数组。两个数组都限定于父会话，而不是子 agent。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../abc123.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "SubagentStop",
  "stop_hook_active": false,
  "agent_id": "def456",
  "agent_type": "Explore",
  "agent_transcript_path": "~/.claude/projects/.../abc123/subagents/agent-def456.jsonl",
  "last_assistant_message": "Analysis complete. Found 3 potential issues...",
  "background_tasks": [],
  "session_crons": []
}
```

SubagentStop hooks 使用与 [Stop hooks](#stop-decision-control) 相同的决策控制格式，包括 `hookSpecificOutput.additionalContext`，`hookEventName` 设置为 `"SubagentStop"`，用于保持子 agent 运行的非错误反馈。返回 `decision: "block"` 与 `reason` 保持子 agent 运行并将 `reason` 作为其下一个指令传递给子 agent。通过退出 2 阻止的 hook 以相同方式传递其 stderr 消息。要在子 agent 返回后向父会话注入上下文，请改用 `Agent` 工具上的 [`PostToolUse`](#posttooluse) hook。

<h3 id="taskcreated">
  TaskCreated
</h3>

在通过 `TaskCreate` 工具创建任务时运行。使用此来强制命名约定、要求任务描述或防止某些任务被创建。在 [没有 Task 工具的会话](/docs/zh-CN/tools-reference#task-tool-availability) 中，此事件不触发。

TaskCreated hooks 不支持匹配器，对每个出现触发。

<h4 id="taskcreated-input">
  TaskCreated 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，TaskCreated hooks 接收 `task_id`、`task_subject` 和可选的 `task_description`、`teammate_name` 和 `team_name`。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "TaskCreated",
  "task_id": "task-001",
  "task_subject": "Implement user authentication",
  "task_description": "Add login and signup endpoints",
  "teammate_name": "implementer",
  "team_name": "session-a1b2c3d4"
}
```

| 字段 | 描述 |
| :- | :- |
| `task_id` | 正在创建的任务的标识符 |
| `task_subject` | 任务的标题 |
| `task_description` | 任务的详细描述。可能不存在 |
| `teammate_name` | 创建任务的队友的名称。可能不存在 |
| `team_name` | 已弃用。会话派生的团队名称；将在未来版本中删除 |

<h4 id="taskcreated-decision-control">
  TaskCreated 决策控制
</h4>

TaskCreated hook 可以以两种方式阻止创建。任一方式，Claude Code 删除任务并将您的消息返回给 Claude 作为工具的错误。Claude Code 忽略此事件的 `continue: false`，Claude 继续工作。

* **退出代码 2**：Claude Code 将 stderr 文本作为消息返回。
* **JSON `{"decision": "block", "reason": "..."}`**：Claude Code 将 `reason` 作为消息返回。

此示例阻止主题不遵循所需格式的任务：

```bash theme={null}
#!/bin/bash
INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

if [[ ! "$TASK_SUBJECT" =~ ^\[TICKET-[0-9]+\] ]]; then
  echo "Task subject must start with a ticket number, e.g. '[TICKET-123] Add feature'" >&2
  exit 2
fi

exit 0
```

<h3 id="taskcompleted">
  TaskCompleted
</h3>

在任务被标记为完成时运行。这在两种情况下触发：当任何 agent 通过 TaskUpdate 工具显式标记任务为完成时，或当 [agent team](/docs/zh-CN/agent-teams) 队友完成其回合与进行中的任务时。使用此来强制完成标准，如通过测试或 lint 检查，然后任务才能关闭。

TaskCompleted hooks 不支持匹配器，对每个出现触发。

<h4 id="taskcompleted-input">
  TaskCompleted 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，TaskCompleted hooks 接收 `task_id`、`task_subject` 和可选的 `task_description`、`teammate_name` 和 `team_name`。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TaskCompleted",
  "task_id": "task-001",
  "task_subject": "Implement user authentication",
  "task_description": "Add login and signup endpoints",
  "teammate_name": "implementer",
  "team_name": "session-a1b2c3d4"
}
```

| 字段 | 描述 |
| :- | :- |
| `task_id` | 正在完成的任务的标识符 |
| `task_subject` | 任务的标题 |
| `task_description` | 任务的详细描述。可能不存在 |
| `teammate_name` | 完成任务的队友的名称。可能不存在 |
| `team_name` | 已弃用。会话派生的团队名称；将在未来版本中删除 |

<h4 id="taskcompleted-decision-control">
  TaskCompleted 决策控制
</h4>

TaskCompleted hooks 支持两种方式来控制任务完成：

* **退出代码 2**：任务不被标记为完成，stderr 消息被反馈给模型作为反馈。
* **JSON `{"continue": false, "stopReason": "..."}`**：当队友完成其回合触发事件时，完全停止队友，匹配 `Stop` hook 行为。`stopReason` 显示给用户。当 `TaskUpdate` 工具触发事件时，Claude Code 忽略 `continue: false`；退出代码 2 仍然阻止完成。

此示例运行测试并在它们失败时阻止任务完成：

```bash theme={null}
#!/bin/bash
INPUT=$(cat)
TASK_SUBJECT=$(echo "$INPUT" | jq -r '.task_subject')

# Run the test suite
if ! npm test 2>&1; then
  echo "Tests not passing. Fix failing tests before completing: $TASK_SUBJECT" >&2
  exit 2
fi

exit 0
```

<h3 id="stop">
  Stop
</h3>

在主 Claude Code agent 完成响应时运行。如果停止由于用户中断而发生，不运行。API 错误触发 [StopFailure](#stopfailure)。

<Tip>
  [`/goal`](/docs/zh-CN/goal) 命令是会话范围的基于提示的 Stop hook 的内置快捷方式。当您想让 Claude 在不编写 hook 配置的情况下继续朝着条件工作时使用它。
</Tip>

<h4 id="stop-input">
  Stop 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，Stop hooks 接收 `stop_hook_active`、`last_assistant_message`、`background_tasks` 和 `session_crons`。`stop_hook_active` 字段在 Claude Code 已经作为 stop hook 的结果继续时为 `true`。检查此值或处理成绩单以避免在永远不会解决的条件上阻止。Claude Code 应用 8 连续继续上限：在 stop hooks 连续继续回合 8 次后，Claude Code 覆盖下一个阻止并结束回合。要提高上限，设置 [`CLAUDE_CODE_STOP_HOOK_BLOCK_CAP`](/docs/zh-CN/env-vars)。

`last_assistant_message` 字段包含 Claude 最终响应的文本内容，因此 hooks 可以访问它而不解析成绩单文件。对于作用于刚完成的回合的 hooks，如朗读或通知 hooks，使用此字段而不是读取 `transcript_path`：成绩单文件不保证在所有版本的 Stop 时包含最终消息。

`background_tasks` 和 `session_crons` 数组让 hooks 区分"会话完成"与"会话暂停等待后台工作唤醒它"。当任务注册表可达时两个数组都出现，当没有任何东西在飞行或计划时为空。

`background_tasks` 中的每个条目描述一个进行中的任务，并使用这些字段：

| 字段 | 描述 |
| :- | :- |
| `id` | 任务标识符 |
| `type` | 友好的任务类型标签，如 `shell`、`subagent`、`monitor`、`workflow`、`teammate`、`cloud session` 或 `MCP task`。每个标签标识哪个 Claude Code 功能创建了任务。对于无法识别的类型回退到原始判别式 |
| `status` | 当前任务状态 |
| `description` | 自由文本描述，上限为 1000 个字符，当剪裁时在字符串中带有 `… [+N chars]` 标记 |
| `command` | Shell 命令行，上限为 1000 个字符。仅对 `shell` 任务出现 |
| `agent_type` | 子 agent 类型名称。仅对 `subagent` 任务出现 |
| `server` | MCP 服务器名称。仅对 `monitor` 和 `MCP task` 任务出现 |
| `tool` | MCP 工具名称。仅对 `monitor` 和 `MCP task` 任务出现 |
| `name` | 工作流名称。仅对 `workflow` 任务出现 |

`session_crons` 中的每个条目描述一个会话范围的计划唤醒，来自 `CronCreate`、`ScheduleWakeup` 和 `/loop`：

| 字段 | 描述 |
| :- | :- |
| `id` | Cron 任务标识符 |
| `schedule` | Cron 表达式，例如 `0 9 * * 1-5` |
| `recurring` | 对于一次性唤醒（其计划编码单个触发时间）为 `false`，对于在每个匹配上重新触发的任务为 `true` |
| `prompt` | 当 cron 触发时提交的提示，上限为 1000 个字符，带有相同的 `… [+N chars]` 标记 |

此示例显示了一个 Stop 输入，带有一个进行中的 shell 任务和一个循环 cron：

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "~/.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "Stop",
  "stop_hook_active": true,
  "last_assistant_message": "I've completed the refactoring. Here's a summary...",
  "background_tasks": [
    {
      "id": "task-001",
      "type": "shell",
      "status": "running",
      "description": "tail logs",
      "command": "tail -f /var/log/syslog"
    }
  ],
  "session_crons": [
    {
      "id": "cron-001",
      "schedule": "0 9 * * 1-5",
      "recurring": true,
      "prompt": "check the build"
    }
  ]
}
```

<h4 id="stop-decision-control">
  Stop 决策控制
</h4>

`Stop` 和 `SubagentStop` hooks 可以控制 Claude 是否继续。除了所有 hooks 可用的 [JSON 输出字段](#json-output) 外，您的 hook 脚本可以返回这些事件特定的字段：

| 字段 | 描述 |
| :- | :- |
| `decision` | `"block"` 防止 Claude 停止。省略以允许 Claude 停止 |
| `reason` | 当 `decision` 为 `"block"` 时需要。告诉 Claude 为什么它应该继续 |
| `hookSpecificOutput.additionalContext` | Claude 的非错误反馈。对话继续，以便 Claude 可以作用于它，但与 `decision: "block"` 不同，它在成绩单中显示为 hook 反馈而不是 hook 错误 |

通过退出 2 阻止的 hook 路由方式与 `reason` 相同：Claude 接收 stderr 消息作为为什么它应该继续的解释。

```json theme={null}
{
  "decision": "block",
  "reason": "Must be provided when Claude is blocked from stopping"
}
```

当 hook 按设计工作并给 Claude 指导时使用 `additionalContext`，如"在完成前运行测试套件"。它通过与 `decision: "block"` 相同的循环保护保持对话进行，即 `stop_hook_active` 输入和 8 连续继续上限，但成绩单将其标记为 `Stop hook feedback`，不显示 hook 错误通知：

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "Stop",
    "additionalContext": "Please run the test suite before finishing"
  }
}
```

<h3 id="stopfailure">
  StopFailure
</h3>

在回合由于 API 错误而结束时运行，而不是 [Stop](#stop)。Claude Code 忽略 hook 的输出和退出代码，除了 [`terminalSequence`](#emit-terminal-notifications)。使用此来记录失败、发送警报或当 Claude 由于速率限制、身份验证问题或其他 API 错误无法完成响应时采取恢复操作。

<h4 id="stopfailure-input">
  StopFailure 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，StopFailure hooks 接收 `error`、可选的 `error_details` 和可选的 `last_assistant_message`。`error` 字段标识错误类型，用于匹配器过滤。

| 字段 | 描述 |
| :- | :- |
| `error` | 错误类型：`rate_limit`、`overloaded`、`authentication_failed`、`oauth_org_not_allowed`、`account_on_hold`、`billing_error`、`invalid_request`、`model_not_found`、`server_error`、`max_output_tokens`、`cloud_credential_error` 或 `unknown` |
| `error_details` | 关于错误的额外详情，当可用时 |
| `last_assistant_message` | 在对话中显示的渲染错误文本。与 `Stop` 和 `SubagentStop` 不同，其中此字段保持 Claude 的对话输出，对于 `StopFailure` 它包含 API 错误字符串本身，如 `"API Error: Rate limit reached"` |

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "StopFailure",
  "error": "rate_limit",
  "error_details": "429 Too Many Requests",
  "last_assistant_message": "API Error: Rate limit reached"
}
```

StopFailure hooks 没有决策控制。它们仅为通知和日志目的运行。

<h3 id="teammateidle">
  TeammateIdle
</h3>

在 [agent team](/docs/zh-CN/agent-teams) 队友在完成其回合后即将空闲时运行。使用此来强制质量门，如在队友停止工作前要求通过 lint 检查或验证输出文件存在。

TeammateIdle hooks 不支持匹配器，对每个出现触发。

<h4 id="teammateidle-input">
  TeammateIdle 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，TeammateIdle hooks 接收 `teammate_name` 和 `team_name`。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "permission_mode": "default",
  "hook_event_name": "TeammateIdle",
  "teammate_name": "researcher",
  "team_name": "session-a1b2c3d4"
}
```

| 字段 | 描述 |
| :- | :- |
| `teammate_name` | 即将空闲的队友的名称 |
| `team_name` | 已弃用。会话派生的团队名称；将在未来版本中删除 |

<h4 id="teammateidle-decision-control">
  TeammateIdle 决策控制
</h4>

TeammateIdle hooks 支持两种方式来控制队友行为：

* **退出代码 2**：队友接收 stderr 消息作为反馈并继续工作而不是空闲。
* **JSON `{"continue": false, "stopReason": "..."}`**：完全停止队友，匹配 `Stop` hook 行为。`stopReason` 显示给用户。

此示例检查构建工件存在，然后允许队友空闲：

```bash theme={null}
#!/bin/bash

if [ ! -f "./dist/output.js" ]; then
  echo "Build artifact missing. Run the build before stopping." >&2
  exit 2
fi

exit 0
```

<h3 id="configchange">
  ConfigChange
</h3>

在会话期间配置文件更改时运行。使用此来审计设置更改、强制安全策略或阻止对配置文件的未授权修改。

Claude Code 在设置文件、托管策略文件或 skill 文件更改时运行 ConfigChange hooks。对于托管策略，它仅在 `managed-settings.json` 或 `managed-settings.d/` 中的文件更改时运行它们。它应用 [服务器托管设置](/docs/zh-CN/server-managed-settings) 和对 macOS 托管首选项或 Windows 注册表策略的更改而不运行它们。在带有 [`wslInheritsWindowsSettings`](/docs/zh-CN/settings-reference#wslinheritswindowssettings) 的 WSL 上，它也在其策略轮询上应用更改的 Windows 端托管设置文件而不运行它们。

匹配器在配置源上过滤：

| 匹配器 | 何时触发 |
| :- | :- |
| `user_settings` | `~/.claude/settings.json` 更改 |
| `project_settings` | `.claude/settings.json` 更改 |
| `local_settings` | `.claude/settings.local.json` 更改 |
| `policy_settings` | `managed-settings.json` 或 `managed-settings.d/` 中的文件更改 |
| `skills` | `.claude/skills/` 中的 skill 文件更改 |

此示例记录所有配置更改以进行安全审计：

```json theme={null}
{
  "hooks": {
    "ConfigChange": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/audit-config-change.sh",
            "args": []
          }
        ]
      }
    ]
  }
}
```

<h4 id="configchange-input">
  ConfigChange 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，ConfigChange hooks 接收 `source` 和可选的 `file_path`。`source` 字段指示哪个配置类型更改，`file_path` 提供被修改的特定文件的路径。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "ConfigChange",
  "source": "project_settings",
  "file_path": "/Users/.../my-project/.claude/settings.json"
}
```

<h4 id="configchange-decision-control">
  ConfigChange 决策控制
</h4>

ConfigChange hooks 可以阻止配置更改生效。使用退出代码 2 或 JSON `decision` 来防止更改。当被阻止时，新设置不应用于运行的会话。

| 字段 | 描述 |
| :- | :- |
| `decision` | `"block"` 防止配置更改被应用。省略以允许更改 |
| `reason` | 被接受但永远不显示 |

```json theme={null}
{
  "decision": "block",
  "reason": "Configuration changes to project settings require admin approval"
}
```

`policy_settings` 更改无法被阻止。当机器上的托管设置文件更改时，hooks 仍然为 `policy_settings` 源触发，因此您可以使用它们来记录这些编辑，但任何阻止决策都被忽略。这确保企业托管设置始终生效。当 [服务器托管设置](/docs/zh-CN/server-managed-settings) 到达或刷新时，Claude Code 不运行 `ConfigChange` hooks。

Claude Code 作用于 ConfigChange hook 的 JSON 输出中的阻止决策，并丢弃 `systemMessage` 和 `continue`。被阻止的更改不向您或 Claude 呈现任何消息，无论您是用 `reason` 还是退出 2 的 stderr 阻止。Claude Code 仅向调试日志写入一行。

<h3 id="cwdchanged">
  CwdChanged
</h3>

在主对话中的 shell 命令更改工作目录时运行，例如当 Claude 执行 `cd` 命令时。使用此来对目录更改做出反应：重新加载环境变量、激活项目特定的工具链或自动运行设置脚本。与 [FileChanged](#filechanged) 配对，用于像 [direnv](https://direnv.net/) 这样管理每个目录环境的工具。

CwdChanged hooks 可以访问 [`CLAUDE_ENV_FILE`](#persist-environment-variables)。写入该文件的变量持久化到后续 Bash 命令，直到下一个 CwdChanged 事件，当 Claude Code 清除它们时。

CwdChanged 不支持匹配器，对每个出现触发。

<h4 id="cwdchanged-input">
  CwdChanged 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，CwdChanged hooks 接收 `old_cwd` 和 `new_cwd`。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project/src",
  "hook_event_name": "CwdChanged",
  "old_cwd": "/Users/my-project",
  "new_cwd": "/Users/my-project/src"
}
```

<h4 id="cwdchanged-output">
  CwdChanged 输出
</h4>

除了所有 hooks 可用的 [JSON 输出字段](#json-output) 外，CwdChanged hooks 可以返回 `watchPaths` 来动态设置 [FileChanged](#filechanged) 监视哪些文件路径：

| 字段 | 描述 |
| :- | :- |
| `watchPaths` | 绝对路径数组。替换当前动态监视列表。来自您 `matcher` 配置的路径始终被监视。返回空数组清除动态列表，这在进入新目录时是典型的 |

CwdChanged hooks 没有决策控制。它们无法阻止目录更改。

Claude Code 从它们的 JSON 输出读取 `watchPaths` 和 `systemMessage`，并丢弃 `continue`。在交互式会话中，它显示 `systemMessage` 作为简短的终端通知。消息不到达 SDK 消息流。

<h3 id="directoryadded">
  DirectoryAdded
</h3>

在您使用 `/add-dir` 命令在会话中添加工作目录后运行，或在 SDK 客户端使用 `register_repo_root` 控制请求添加一个后运行。使用此来准备新添加的存储库，例如安装其依赖。

Claude Code 在以下情况下不触发此事件：

* 您使用 `--add-dir` 启动标志传递目录；[SessionStart](#sessionstart) 涵盖这些目录
* 您在 `/permissions` Workspace 标签上添加目录
* 您添加已经是工作目录或在一个内部的目录

Claude Code 在刷新沙箱和权限状态后触发 DirectoryAdded，因此沙箱工具已经在您的 hook 运行时看到新目录。Hook 命令本身运行未沙箱化。

Claude Code 不等待 hook：添加立即完成，hook 在后台以 600 秒默认超时运行。

匹配器在目录添加方式上过滤：

| 匹配器 | 何时触发 |
| :- | :- |
| `slash_command` | 您使用 `/add-dir` 添加目录 |
| `register_repo_root` | SDK 客户端使用 `register_repo_root` 控制请求添加目录 |

<h4 id="directoryadded-input">
  DirectoryAdded 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，DirectoryAdded hooks 接收 `directory` 和 `source`。

| 字段 | 描述 |
| :- | :- |
| `directory` | 添加的目录的绝对路径 |
| `source` | 目录如何添加，`/add-dir` 为 `"slash_command"` 或 SDK 控制请求为 `"register_repo_root"` |

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "DirectoryAdded",
  "directory": "/Users/my-other-repo",
  "source": "slash_command"
}
```

DirectoryAdded hooks 没有决策控制。它们无法阻止添加，这在 hook 运行时已经完成。Claude Code 从它们的 JSON 输出丢弃 `continue` 字段，并根据源以不同方式呈现其余部分：

* `slash_command`：Claude Code 将 hook 的 `systemMessage` 作为上下文传递给 Claude，在下一个对话回合上，而不是向您显示。失败 hooks 的计数出现在成绩单中。完整失败输出进入调试日志
* `register_repo_root`：Claude Code 仅将 `systemMessage` 输出和失败输出写入调试日志

<h3 id="filechanged">
  FileChanged
</h3>

在监视的文件在磁盘上更改时运行。Claude Code 使用文件系统监视器检测更改，而不是通过检查工具调用，因此它运行 hook，无论什么更改了文件：`Edit` 或 `Write` 工具调用、Claude 使用 `Bash` 运行的脚本或 Claude Code 外的进程。常见用途是在项目配置文件更改时重新加载环境变量。

此事件的 `matcher` 有两个角色：

* **构建监视列表**：值在 `|` 上分割，每个段注册为工作目录中的字面文件名，因此 `".envrc|.env"` 恰好监视这两个文件。正则表达式模式在这里不有用：像 `^\.env` 这样的值会监视字面名为 `^\.env` 的文件。
* **过滤哪些 hooks 运行**：当监视的文件更改时，相同的值使用标准 [匹配器规则](#matcher-patterns) 针对更改文件的基名过滤哪个 hook 组运行。

此示例在任何更改后规范化 `data.csv` 中的行结尾，包括 `Bash` 命令或外部脚本重写文件：

```json theme={null}
{
  "hooks": {
    "FileChanged": [
      {
        "matcher": "data.csv",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/normalize-line-endings.sh"
          }
        ]
      }
    ]
  }
}
```

hook 从 stdin 上的 [JSON 输入](#filechanged-input) 的 `file_path` 字段读取更改文件的绝对路径。其 `grep` 守卫测试与 `perl` 删除的相同内容，行末的 CR，因此规范化后的运行退出而不触及文件。更松散的守卫循环永远，因为 `perl -i` 重写文件，即使它替换了什么，Claude Code 在每次重写后运行 hook。将此脚本保存在 `/path/to/normalize-line-endings.sh` 并使其可执行：

```bash theme={null}
#!/bin/bash
FILE=$(jq -r .file_path)
if grep -q $'\r$' "$FILE"; then
  perl -pi -e 's/\r$//' "$FILE"
fi
```

要确认 hook 有效，要求 Claude 使用 `Bash` 命令将 CRLF 行附加到 `data.csv`。Claude Code 运行 hook，文件最终以 LF 结尾。

要监视您无法提前命名的文件，从 hook 返回 [`watchPaths`](#filechanged-output) 来动态更新监视列表。Claude Code 仅在某个东西命名要监视的文件时启动监视器，因此使用命名至少一个文件的 FileChanged 组为列表播种，或使用 [SessionStart](#sessionstart-decision-control) 或 [CwdChanged](#cwdchanged) hook 返回 `watchPaths`。匹配器仍然过滤当监视的文件更改时哪个 hook 组运行，因此给处理动态路径的组一个省略的匹配器，它匹配每个监视的文件并不向监视列表添加任何内容。`"*"` 匹配器也匹配每个文件，但 Claude Code 像任何其他值一样在监视列表中注册它，作为字面名为 `*` 的文件。

FileChanged hooks 可以访问 [`CLAUDE_ENV_FILE`](#persist-environment-variables)。写入该文件的变量持久化到后续 Bash 命令，直到下一个 [CwdChanged](#cwdchanged) 事件，当 Claude Code 清除它们时。

<h4 id="filechanged-input">
  FileChanged 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，FileChanged hooks 接收 `file_path` 和 `event`。

| 字段 | 描述 |
| :- | :- |
| `file_path` | 更改的文件的绝对路径 |
| `event` | 发生了什么：修改文件为 `"change"`、创建的文件为 `"add"` 或删除的文件为 `"unlink"` |

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../transcript.jsonl",
  "cwd": "/Users/my-project",
  "hook_event_name": "FileChanged",
  "file_path": "/Users/my-project/.envrc",
  "event": "change"
}
```

<h4 id="filechanged-output">
  FileChanged 输出
</h4>

除了所有 hooks 可用的 [JSON 输出字段](#json-output) 外，FileChanged hooks 可以返回 `watchPaths` 来动态更新监视的文件路径：

| 字段 | 描述 |
| :- | :- |
| `watchPaths` | 绝对路径数组。替换当前动态监视列表。来自您 `matcher` 配置的路径始终被监视。当您的 hook 脚本根据更改的文件发现要监视的额外文件时使用此 |

FileChanged hooks 没有决策控制。它们无法阻止文件更改发生。

Claude Code 从它们的 JSON 输出读取 `watchPaths` 和 `systemMessage`，并丢弃 `continue`。在交互式会话中，它显示 `systemMessage` 作为简短的终端通知。消息不到达 SDK 消息流。

<h3 id="worktreecreate">
  WorktreeCreate
</h3>

在创建 worktree 时运行，无论是从 `claude --worktree`、从 [使用 `isolation: "worktree"` 的子 agent](/docs/zh-CN/sub-agents#choose-the-subagent-scope) 还是为 Claude Code 在其自己的 worktree 中隔离的 [后台会话](/docs/zh-CN/agent-view#how-file-edits-are-isolated)。默认情况下 Claude Code 使用 `git worktree` 创建隔离的工作副本。配置 WorktreeCreate hook 替换该默认 git 行为，让您使用不同的版本控制系统，如 SVN、Perforce 或 Mercurial。

因为 hook 完全替换默认行为，[`.worktreeinclude`](/docs/zh-CN/worktrees#copy-gitignored-files-into-worktrees) 不被处理。如果您需要将本地配置文件（如 `.env`）复制到新 worktree，请在您的 hook 脚本内执行。

hook 必须返回创建的 worktree 目录的路径。Claude Code 使用此路径作为隔离会话的工作目录。有关每个 hook 类型如何返回路径，请参阅 [WorktreeCreate 输出](#worktreecreate-output)。

Claude Code 作用于 hook 的成功和返回的路径，并丢弃 `systemMessage` 和 `continue`。

此示例创建 SVN 工作副本并打印路径供 Claude Code 使用。将存储库 URL 替换为您自己的：

```json theme={null}
{
  "hooks": {
    "WorktreeCreate": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'NAME=$(jq -r .name); DIR=\"$HOME/.claude/worktrees/$NAME\"; svn checkout https://svn.example.com/repo/trunk \"$DIR\" >&2 && echo \"$DIR\"'"
          }
        ]
      }
    ]
  }
}
```

hook 从 stdin 上的 JSON 输入读取 worktree `name`，检出一个新副本到新目录，并打印目录路径。最后一行的 `echo` 是 Claude Code 读取为 worktree 路径的内容。将任何其他输出重定向到 stderr，以便它不干扰路径。

<h4 id="worktreecreate-input">
  WorktreeCreate 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，WorktreeCreate hooks 接收 `name` 字段。这是新 worktree 的 slug 标识符，由用户指定或自动生成，例如 `bold-oak-a3f2`。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeCreate",
  "name": "feature-auth"
}
```

<h4 id="worktreecreate-output">
  WorktreeCreate 输出
</h4>

WorktreeCreate hooks 不使用标准允许/阻止决策模型。相反，hook 的成功或失败确定结果。hook 必须返回创建的 worktree 目录的路径：

* **命令 hooks** (`type: "command"`)：将路径打印为 stdout 的最后一个非空行。Claude Code 在读取该行之前剥离 ANSI 转义代码，因此在您的 `echo` 之前打印的 shell 启动横幅被忽略。将任何其他 hook 输出重定向到 stderr。
* **HTTP hooks** (`type: "http"`)：在响应体中返回 `{ "hookSpecificOutput": { "hookEventName": "WorktreeCreate", "worktreePath": "/absolute/path" } }`。

如果 hook 失败或产生无路径，worktree 创建失败并出现错误。

Claude Code 根据 hook 运行的目录解析相对路径，折叠其中的任何 `.` 或 `..` 段。如果结果路径不是 Claude Code 可以进入的目录，会话打印命名路径的错误并以代码 1 退出。

Claude Code 拒绝包含 `.` 或 `..` 段的绝对路径，以及通过存储库根下的符号链接的任何路径，因为提交到存储库的符号链接可能将 worktree 重定向到其外。错误命名被拒绝的组件。返回不通过存储库内符号链接的规范化路径。在 v2.1.216 之前，worktree 创建遵循 hook 的路径而不进行此筛选。

<h3 id="worktreeremove">
  WorktreeRemove
</h3>

在删除 worktree 时运行。这是 [WorktreeCreate](#worktreecreate) 的清理对应物。事件在以下情况下触发：

* 您退出 `--worktree` 会话并选择删除它
* 带有 `isolation: "worktree"` 的子 agent 完成
* 您删除 [后台会话](/docs/zh-CN/agent-view#what-deleting-a-session-removes)，其 worktree hook 创建

对于基于 git 的 worktrees，Claude Code 使用 `git worktree remove` 自动处理清理。如果您配置了 WorktreeCreate hook，将其与 WorktreeRemove hook 配对来控制它创建的 worktrees 的清理：

* **无 WorktreeRemove hook**：当您退出 `--worktree` 会话并选择删除时，Claude Code 回退到您的 WorktreeCreate hook 返回的路径上的 `git worktree remove --force`，因此 git 识别的 worktree 被删除。git 不识别的 worktree，例如您的 hook 使用非 git 版本控制系统创建的，保留在磁盘上。对于删除 [后台会话](/docs/zh-CN/agent-view#what-deleting-a-session-removes) 对 hook 创建的 worktree 做什么，请参阅 agent view 的删除规则。
* **Hook 退出 0**：worktree 计为已删除。Claude Code 从 hook 读取其他任何内容，因此确保您的 hook 删除了目录。
* **Hook 退出非零**：如果 `worktree_path` 处的目录在之后仍然存在，删除失败，worktree 保留在磁盘上，没有 git 回退。在退出非零前删除目录的 hook 计为已删除。对于失败如何报告，请参阅 [WorktreeRemove 输入](#worktreeremove-input)。

Claude Code 永远不删除属于 hook 创建的 worktree 的分支，因为它仅知道您的 WorktreeCreate hook 返回的路径。如果您的 WorktreeCreate hook 创建分支，在您的 WorktreeRemove hook 中删除它。

Claude Code 丢弃 WorktreeRemove hook 的 [JSON 输出字段](#json-output)，如 `systemMessage` 和 `continue`。

对于后台会话删除，Claude Code 在运行 hook 之前验证存储的 worktree 路径，并拒绝是符号链接或通过存储库根下的符号链接的路径。hook 仅对仍包含文件的 worktree 运行，当您在 [agent view](/docs/zh-CN/agent-view#what-deleting-a-session-removes) 中确认删除时；对于这样的 worktree，[`claude rm`](/docs/zh-CN/agent-view#manage-sessions-from-the-shell) 保持会话和 worktree。在 v2.1.216 之前，hook 在存储的路径上运行而不进行这些检查。

Claude Code 将 WorktreeCreate 返回的路径作为 `worktree_path` 在 hook 输入中传递。此示例读取该路径并删除目录：

```json theme={null}
{
  "hooks": {
    "WorktreeRemove": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'jq -r .worktree_path | xargs rm -rf'"
          }
        ]
      }
    ]
  }
}
```

<h4 id="worktreeremove-input">
  WorktreeRemove 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，WorktreeRemove hooks 接收 `worktree_path` 字段，这是被删除的 worktree 的绝对路径。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "WorktreeRemove",
  "worktree_path": "/Users/.../my-project/.claude/worktrees/feature-auth"
}
```

WorktreeRemove hook 的退出代码决定结果。当 hook 退出非零且 `worktree_path` 处的目录在之后仍然存在时，删除失败：

* worktree 保留在磁盘上，hook 的命令和 stderr 进入 [调试日志](#debug-hooks)。
* 如果您删除后台会话，会话也保留。[agent view](/docs/zh-CN/agent-view#what-deleting-a-session-removes) 中的拒绝消息报告 hook 如何结束，如 `exited 1`，引用其 stderr 的开头，并说删除会话是否再次删除目录。

<h3 id="precompact">
  PreCompact
</h3>

在 Claude Code 即将运行压缩操作之前运行。

匹配器值指示压缩是手动还是自动触发：

| 匹配器 | 何时触发 |
| :- | :- |
| `manual` | `/compact` |
| `auto` | 当对话到达 [自动压缩窗口](/docs/zh-CN/model-config#set-the-auto-compact-window) 时自动压缩 |

使用代码 2 退出以阻止压缩。对于手动 `/compact`，stderr 消息显示给用户。您也可以通过返回带有 `"decision": "block"` 的 JSON 来阻止。

阻止自动压缩有不同的效果，取决于它何时触发。如果压缩在上下文限制之前主动触发，Claude Code 跳过它，对话继续未压缩。如果压缩被触发以从 API 已经返回的上下文限制错误恢复，底层错误浮出并且当前请求失败。

Claude Code 丢弃 PreCompact hook 的 `systemMessage` 和 `continue` 字段。

<h4 id="precompact-input">
  PreCompact 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，PreCompact hooks 接收 `trigger` 和 `custom_instructions`。对于 `manual`，`custom_instructions` 包含用户传递到 `/compact` 的内容，当他们不传递任何内容时为 `null`。对于 `auto`，`custom_instructions` 为 `null`。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PreCompact",
  "trigger": "manual",
  "custom_instructions": null
}
```

<h3 id="postcompact">
  PostCompact
</h3>

在 Claude Code 完成压缩操作后运行。使用此事件对新压缩状态做出反应，例如记录生成的摘要或更新外部状态。Claude Code 丢弃 PostCompact hook 的 `systemMessage` 和 `continue` 字段。

与 `PreCompact` 相同的匹配器值适用：

| 匹配器 | 何时触发 |
| :- | :- |
| `manual` | 在 `/compact` 后 |
| `auto` | 当对话到达 [自动压缩窗口](/docs/zh-CN/model-config#set-the-auto-compact-window) 时自动压缩后 |

<h4 id="postcompact-input">
  PostCompact 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，PostCompact hooks 接收 `trigger` 和 `compact_summary`。`compact_summary` 字段包含压缩操作生成的对话摘要。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PostCompact",
  "trigger": "manual",
  "compact_summary": "Summary of the compacted conversation..."
}
```

PostCompact hooks 没有决策控制。它们无法影响压缩结果，但可以执行后续任务。

<h3 id="premodelswitch">
  PreModelSwitch
</h3>

在 Claude Code 应用您或客户端请求的模型切换之前运行。使用它来阻止切换、要求确认或在切换发生前显示成本。

PreModelSwitch 需要 Claude Code v2.1.251 或更高版本。Claude Code 为这些请求运行它：

* `/model <name>` 和 `/model` 选择器
* `Option+P` 或 `Alt+P` 模型选择器
* `/config` 中的 Model 设置
* 当那改变会话的模型时打开 [fast mode](/docs/zh-CN/fast-mode)
* 来自 [Agent SDK](/docs/zh-CN/agent-sdk/typescript#query-object) 主机或 [Remote Control](/docs/zh-CN/remote-control) 的 `set_model` 请求，或 `apply_flag_settings` 请求中的模型更改

Claude Code 不为它自己进行的切换运行 PreModelSwitch hooks，如 [自动模型回退](/docs/zh-CN/model-config#automatic-model-fallback) 或恢复会话时恢复模型。这些更改仅到达 [PostModelSwitch](#postmodelswitch)。

Claude Code 根据会话切换到的模型的规范名称比较匹配器，忽略任何 `[1m]` 后缀。别名如 `opus`、日期模型 ID 和提供商特定 ID（如 Amazon Bedrock 模型 ID）都匹配它们解析到的一个规范名称，因此 `claude-opus-5` 涵盖 Opus 5 的每个拼写。

当 Claude Code 无法确定目标的规范名称时，例如仅您的 [LLM gateway](/docs/zh-CN/llm-gateway) 知道的自定义模型 ID，它运行每个 PreModelSwitch hook，无论匹配器如何。阻止的 hook 应该从其输入检查 `to_model` 而不是仅依赖匹配器。

将匹配器写为精确名称、`|` 分隔列表如 `claude-opus-4-6|claude-opus-5` 或正则表达式如 `.*opus.*`。此示例使用精确名称匹配器并也从 hook 输入检查 `to_model`，因此它拒绝切换到 Opus 4.6，通过退出代码 2，并让任何其他目标通过：

<Tabs>
  <Tab title="macOS/Linux">
    命令使用 `jq` 检查 `to_model`：

    ```json theme={null}
    {
      "hooks": {
        "PreModelSwitch": [
          {
            "matcher": "claude-opus-4-6",
            "hooks": [
              {
                "type": "command",
                "command": "jq -e '.to_model | test(\"opus-4-6\")' > /dev/null && { echo 'Opus 4.6 is retired for this project. Use a newer model.' >&2; exit 2; }; exit 0"
              }
            ]
          }
        ]
      }
    }
    ```
  </Tab>

  <Tab title="Windows (PowerShell)">
    注册一个命令 hook，通过 PowerShell 运行脚本：

    ```json theme={null}
    {
      "hooks": {
        "PreModelSwitch": [
          {
            "matcher": "claude-opus-4-6",
            "hooks": [
              {
                "type": "command",
                "command": "powershell.exe",
                "args": [
                  "-NoProfile",
                  "-ExecutionPolicy",
                  "Bypass",
                  "-File",
                  "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-opus-46.ps1"
                ]
              }
            ]
          }
        ]
      }
    }
    ```

    将此脚本保存到项目中的 `.claude/hooks/block-opus-46.ps1`：

    ```powershell theme={null}
    $hookInput = [Console]::In.ReadToEnd() | ConvertFrom-Json
    if ($hookInput.to_model -match 'opus-4-6') {
      [Console]::Error.WriteLine('Opus 4.6 is retired for this project. Use a newer model.')
      exit 2
    }
    exit 0
    ```
  </Tab>
</Tabs>

要确认 hook 有效，从运行不同模型的会话运行 `/model claude-opus-4-6`。Claude Code 保持当前模型并报告 PreModelSwitch hook 阻止了切换，以您的消息作为原因。

<h4 id="premodelswitch-input">
  PreModelSwitch 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，PreModelSwitch hooks 接收此表中的字段。最后五个描述重新发送对话到新模型的成本，因此 hook 可以在切换发生前显示该数字。

| 字段 | 类型 | 描述 |
| :- | :- | :- |
| `from_model` | string | 切换改变的模型 ID |
| `to_model` | string | 切换改变到的模型 ID。匹配器根据此模型的规范名称比较 |
| `requested_model` | string or `null` | 请求命名的模型：别名如 `opus`、完整模型 ID 或当请求是默认模型时为 `null` |
| `source` | string | 请求来自何处：`/model <name>`、`/config` 中的 Model 设置或打开 fast mode 的 `"command"`；模型选择器的 `"picker"`；来自 Agent SDK 主机或 Remote Control 的 `set_model` 请求或 `apply_flag_settings` 请求中的模型更改的 `"sdk"` |
| `context_tokens` | number | 下一个请求重新发送作为其提示的令牌：主对话中最后响应的输入、缓存读取、缓存创建和输出令牌，合并。第一个响应前为 `0` |
| `prompt_cache_warm` | boolean | 当前模型的 prompt cache 是否可能仍然温暖，意味着切换放弃它 |
| `cache_ttl` | string | [Prompt cache 生命周期](/docs/zh-CN/prompt-caching#cache-lifetime) Claude Code 为此会话请求：`"5m"` 或 `"1h"` |
| `estimated_cache_write_usd` | number | 在 `to_model` 上以 `cache_ttl` 速率将 `context_tokens` 写入 prompt cache 的估计成本（美元），不包括下一个响应。服务器可能不需要重新缓存整个上下文，因此将其视为估计 |
| `pricing` | string | Claude Code 如何定价 `estimated_cache_write_usd`：当您的组织配置了自己的速率时为 `"configured"`，列表价格为 `"catalog"`，或当 `to_model` 没有已知价格且 Claude Code 假设默认速率时为 `"default"` |

此示例显示了在运行 Sonnet 5 的会话中 `/model opus` 的输入：

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "PreModelSwitch",
  "from_model": "claude-sonnet-5",
  "to_model": "claude-opus-5",
  "requested_model": "opus",
  "source": "command",
  "context_tokens": 182340,
  "prompt_cache_warm": true,
  "cache_ttl": "5m",
  "estimated_cache_write_usd": 1.1396,
  "pricing": "catalog"
}
```

<h4 id="premodelswitch-decision-control">
  PreModelSwitch 决策控制
</h4>

`PreModelSwitch` hooks 可以取消切换、要求用户确认或让它继续。退出代码 2 或顶级 `decision: "block"` 取消切换。

为了更精细的控制，在 `hookSpecificOutput` 对象中返回 `permissionDecision` 和 `permissionDecisionReason`，如 [PreToolUse](#pretooluse-decision-control)。`PreModelSwitch` 接受 `"allow"`、`"deny"` 和 `"ask"`。它不接受 `"defer"`、`updatedInput` 或 `additionalContext`。下表描述两个字段：

| 字段 | 描述 |
| :- | :- |
| `permissionDecision` | `"allow"` 继续并跳过 [Claude Code 在 prompt cache 温暖时显示的确认](/docs/zh-CN/prompt-caching#switching-models)。`"deny"` 取消切换。`"ask"` 提示用户确认它 |
| `permissionDecisionReason` | 对于 `"deny"`，显示给用户作为切换被阻止的原因，或作为 `set_model` 请求的错误返回。对于 `"ask"`，显示在确认提示中。对于 `"allow"` 被忽略 |

仅交互式会话中的 `/model` 可以显示 `"ask"` 提示。在每个其他表面，包括带有 `-p` 标志的非交互模式、`/config` 和 `set_model` 请求，Claude Code 将 `"ask"` 视为拒绝。

此示例要求用户确认并引用来自 `context_tokens` 的令牌计数：

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "PreModelSwitch",
    "permissionDecision": "ask",
    "permissionDecisionReason": "Switching now re-sends about 180k tokens to the new model. Continue?"
  }
}
```

当多个 PreModelSwitch hooks 返回不同的决策时，优先级为 `deny` > `ask` > `allow`。

Claude Code 显示用户您的 hook 返回的任何 `systemMessage`，无论决策如何，因此成本报告 hook 可以返回 `{"systemMessage": "..."}` 并退出 0。

在其超时前不响应的 PreModelSwitch hook 阻止切换。在 [PreToolUse](#timeouts) 上，相比之下，超时的命令 hook 让工具调用继续。此事件的默认超时为 30 秒。`PreModelSwitch` 仅运行 `command`、`http` 和 `mcp_tool` hooks，因此 `prompt` 和 `agent` 默认不适用。

退出代码不是 0 或 2 且打印无 JSON 决策的 hook 不阻止：Claude Code 显示其 stderr 并应用切换，如 [其他退出代码](#other-exit-codes) 下所述。

<h3 id="postmodelswitch">
  PostModelSwitch
</h3>

在会话的模型更改后运行。使用它来给 Claude 模型特定的指导，而不编辑每个 CLAUDE.md，例如仅在某些模型上适用的组织范围指令。

PostModelSwitch 需要 Claude Code v2.1.251 或更高版本。它无法阻止，因为模型已经更改。Claude Code 在这些更改后运行 PostModelSwitch hooks：

* 您或客户端请求的切换
* [自动模型回退](/docs/zh-CN/model-config#automatic-model-fallback)，改变会话的模型
* 设置如 [`opusplan`](/docs/zh-CN/model-config#opusplan-model-setting) 进入或离开 plan mode
* Claude Code 恢复会话时恢复模型

当 [回退模型链](/docs/zh-CN/model-config#fallback-model-chains) 中的模型服务回合时，Claude Code 不运行 PostModelSwitch hooks，因为该替换持续一个回合并保持会话的模型不变。

匹配器遵循与 [PreModelSwitch](#premodelswitch) 相同的规则：Claude Code 根据会话切换到的模型的规范名称比较它。

此示例在会话的模型更改为任何 Opus 模型时添加指导：

```json theme={null}
{
  "hooks": {
    "PostModelSwitch": [
      {
        "matcher": ".*opus.*",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'On Opus, delegate implementation work to subagents and keep this conversation for planning and review.'"
          }
        ]
      }
    ]
  }
}
```

要确认 hook 有效，从运行不同模型的会话切换到 Opus 模型，例如从 Sonnet 会话运行 `/model opus`，然后要求 Claude 关于当前模型的指导。

<h4 id="postmodelswitch-input">
  PostModelSwitch 输入
</h4>

PostModelSwitch hooks 接收与 [PreModelSwitch](#premodelswitch-input) 相同的字段，`hook_event_name` 设置为 `"PostModelSwitch"` 和两个更多 `source` 值：`"auto"` 对于自动回退或 Claude Code 自己进行的其他更改，`"resume"` 对于恢复会话时恢复的模型。

当 `source` 为 `"auto"` 时，`requested_model` 为 `null`。当 `source` 为 `"resume"` 时，它是 Claude Code 恢复的保存模型设置。

<h4 id="postmodelswitch-decision-control">
  PostModelSwitch 决策控制
</h4>

Claude Code 获取您的 hook 在退出 0 时的 [纯文本 stdout](#exit-code-0)，或来自 JSON 输出的 `additionalContext`，并在切换后的下一个请求中将其传递给 Claude。除了所有 hooks 可用的 [JSON 输出字段](#json-output) 外，您可以返回：

| 字段 | 描述 |
| :- | :- |
| `additionalContext` | 与下一个请求一起添加到 Claude 上下文的字符串。有关如何传递文本以及放入其中的内容，请参阅 [为 Claude 添加上下文](#add-context-for-claude) |

如果 hook 在您发送下一个提示后五秒内未完成，Claude Code 发送该请求而不输出，并将其附加到以下请求。如果模型在下一个请求之前更改多次，Claude Code 仅传递最后一个切换目标模型的输出。

<h3 id="sessionend">
  SessionEnd
</h3>

在 Claude Code 会话结束时运行。对于清理任务、记录会话统计或保存会话状态很有用。支持匹配器以按退出原因过滤。

`reason` 字段在 hook 输入中指示会话为什么结束：

| 原因 | 描述 |
| :- | :- |
| `clear` | 会话使用 `/clear` 命令清除 |
| `resume` | 会话通过交互式 `/resume` 切换 |
| `logout` | 用户登出 |
| `prompt_input_exit` | 用户在提示输入可见时退出 |
| `other` | 其他退出原因 |
| `bypass_permissions_disabled` | 在 v2.1.234 中删除；Claude Code 不发送它。从您的 `SessionEnd` 匹配器中删除它 |

<h4 id="sessionend-input">
  SessionEnd 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，SessionEnd hooks 接收指示会话为什么结束的 `reason` 字段。有关所有值，请参阅上面的 [原因表](#sessionend)。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "SessionEnd",
  "reason": "other"
}
```

SessionEnd hooks 没有决策控制。它们无法阻止会话终止，但可以执行清理任务。Claude Code 丢弃它们的 [JSON 输出字段](#json-output)，如 `systemMessage`。

SessionEnd hooks 的默认超时为 1.5 秒。它在您退出、运行 `/clear` 或使用交互式 `/resume` 切换会话时适用。您可以通过两种方式给 hook 更多时间：

* **每个 hook `timeout`**：在该 hook 的配置中设置 `timeout`。总体预算自动上升以匹配您的设置文件中最高的每个 hook `timeout`，最多 60 秒。如果您以这种方式提高预算，没有自己的 `timeout` 的 hook 仍然保持默认。在插件提供的 hooks 上设置的超时不提高预算。
* **`CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS`**：设置此环境变量（毫秒）以显式覆盖预算。您设置的值也成为每个没有自己的 `timeout` 的 hook 的超时。

此示例将预算设置为 5 秒：

```bash theme={null}
CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS=5000 claude
```

在 v2.1.268 之前，`CLAUDE_CODE_SESSIONEND_HOOKS_TIMEOUT_MS` 仅提高总体预算，没有自己的 `timeout` 的 hook 仍然在 1.5 秒后被取消。

<h3 id="elicitation">
  Elicitation
</h3>

在 MCP 服务器请求用户输入中任务时运行。默认情况下，Claude Code 显示交互式对话供用户响应。Hooks 可以拦截此请求并以编程方式响应，完全跳过对话。

匹配器字段根据 MCP 服务器名称匹配。

<h4 id="elicitation-input">
  Elicitation 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，Elicitation hooks 接收 `mcp_server_name`、`message` 和可选的 `mode`、`url`、`elicitation_id` 和 `requested_schema` 字段。

对于表单模式引出，最常见的情况：

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Elicitation",
  "mcp_server_name": "my-mcp-server",
  "message": "Please provide your credentials",
  "mode": "form",
  "requested_schema": {
    "type": "object",
    "properties": {
      "username": { "type": "string", "title": "Username" }
    }
  }
}
```

对于 URL 模式引出，用于基于浏览器的身份验证：

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "Elicitation",
  "mcp_server_name": "my-mcp-server",
  "message": "Please authenticate",
  "mode": "url",
  "url": "https://auth.example.com/login"
}
```

<h4 id="elicitation-output">
  Elicitation 输出
</h4>

要以编程方式响应而不显示对话，返回一个带有 `hookSpecificOutput` 的 JSON 对象：

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "Elicitation",
    "action": "accept",
    "content": {
      "username": "alice"
    }
  }
}
```

| 字段 | 值 | 描述 |
| :- | :- | :- |
| `action` | `accept`、`decline`、`cancel` | 是否接受、拒绝或取消请求 |
| `content` | object | 要提交的表单字段值。仅在 `action` 为 `accept` 时使用 |

退出代码 2 拒绝引出。Claude Code 不在任何地方显示您的 stderr 消息。

Claude Code 作用于 Elicitation hook 的 JSON 输出中的 `hookSpecificOutput` 并丢弃 `systemMessage` 和 `continue`。

<h3 id="elicitationresult">
  ElicitationResult
</h3>

在用户响应 MCP 引出后运行。Hooks 可以观察、修改或阻止响应，然后将其发送回 MCP 服务器。

匹配器字段根据 MCP 服务器名称匹配。

<h4 id="elicitationresult-input">
  ElicitationResult 输入
</h4>

除了 [常见输入字段](#common-input-fields) 外，ElicitationResult hooks 接收 `mcp_server_name`、`action` 和可选的 `mode`、`elicitation_id` 和 `content` 字段。

```json theme={null}
{
  "session_id": "abc123",
  "transcript_path": "/Users/.../.claude/projects/.../00893aaf-19fa-41d2-8238-13269b9b3ca0.jsonl",
  "cwd": "/Users/...",
  "hook_event_name": "ElicitationResult",
  "mcp_server_name": "my-mcp-server",
  "action": "accept",
  "content": { "username": "alice" },
  "mode": "form",
  "elicitation_id": "elicit-123"
}
```

<h4 id="elicitationresult-output">
  ElicitationResult 输出
</h4>

要覆盖用户的响应，返回一个带有 `hookSpecificOutput` 的 JSON 对象：

```json theme={null}
{
  "hookSpecificOutput": {
    "hookEventName": "ElicitationResult",
    "action": "decline",
    "content": {}
  }
}
```

| 字段 | 值 | 描述 |
| :- | :- | :- |
| `action` | `accept`、`decline`、`cancel` | 覆盖用户的操作 |
| `content` | object | 覆盖表单字段值。仅在 `action` 为 `accept` 时有意义 |

退出代码 2 阻止响应，将有效操作更改为 `decline`。Claude Code 不在任何地方显示您的 stderr 消息。

Claude Code 作用于 ElicitationResult hook 的 JSON 输出中的 `hookSpecificOutput` 并丢弃 `systemMessage` 和 `continue`。

<h2 id="prompt-based-hooks">
  基于提示的 hooks
</h2>

除了命令、HTTP 和 MCP tool hooks 外，Claude Code 还支持基于提示的 hooks（`type: "prompt"`），使用 LLM 来评估是否允许或阻止操作，以及代理 hooks（`type: "agent"`），生成具有工具访问权限的代理验证器。并非所有事件都支持每种 hook 类型。

支持所有五种 hook 类型（`command`、`http`、`mcp_tool`、`prompt` 和 `agent`）的事件：

* `PermissionDenied`
* `PostToolBatch`
* `PostToolUse`
* `PostToolUseFailure`
* `PreToolUse`
* `Stop`
* `SubagentStop`
* `TaskCompleted`
* `TaskCreated`
* `TeammateIdle`
* `UserPromptExpansion`
* `UserPromptSubmit`

`PermissionRequest` 支持 `command`、`http`、`mcp_tool` 和 `prompt` hooks，但不支持 `agent` hooks。如果您在此事件上配置代理 hook，Claude Code 会跳过它，权限流程保持不变。要从 hook 允许或拒绝，请从命令或 HTTP hook 返回[决定对象](#permissionrequest-decision-control)。

支持 `command`、`http` 和 `mcp_tool` hooks 但不支持 `prompt` 或 `agent` 的事件：

* `ConfigChange`
* `CwdChanged`
* `DirectoryAdded`
* `Elicitation`
* `ElicitationResult`
* `FileChanged`
* `InstructionsLoaded`
* `MessageDisplay`
* `Notification`
* `PostCompact`
* `PostModelSwitch`
* `PreCompact`
* `PreModelSwitch`
* `SessionEnd`
* `StopFailure`
* `SubagentStart`
* `WorktreeCreate`
* `WorktreeRemove`

`SessionStart` 和 `Setup` 支持 `command` 和 `mcp_tool` hooks，[MCP tool hook 字段](#mcp-tool-hook-fields)描述了它们的 `mcp_tool` hooks 何时运行。它们不支持 `http`、`prompt` 或 `agent` hooks。

<h3 id="how-prompt-based-hooks-work">
  基于提示的 hooks 如何工作
</h3>

基于提示的 hooks 不执行 Bash 命令，而是：

1. 将 hook 输入和您的提示发送到 Claude 模型，默认为 Claude Code 用于[后台功能](/docs/zh-CN/costs#background-token-usage)的模型
2. LLM 使用包含决定的结构化 JSON 响应
3. Claude Code 自动处理决定

<h3 id="prompt-hook-configuration">
  提示 hook 配置
</h3>

将 `type` 设置为 `"prompt"` 并提供 `prompt` 字符串而不是 `command`。使用 `$ARGUMENTS` 占位符将 hook 的 JSON 输入数据注入到您的提示文本中。

此 `Stop` hook 要求 LLM 在允许 Claude 完成之前评估是否应该停止：

```json theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "Evaluate if Claude should stop: $ARGUMENTS. Check if all tasks are complete."
          }
        ]
      }
    ]
  }
}
```

| 字段 | 必需 | 描述 |
| :- | :- | :- |
| `type` | 是 | 必须是 `"prompt"` |
| `prompt` | 是 | 要发送给 LLM 的提示文本。使用 `$ARGUMENTS` 作为 hook 输入 JSON 的占位符。如果 `$ARGUMENTS` 不存在，输入 JSON 被追加到提示 |
| `model` | 否 | 用于评估的模型。默认为 Claude Code 用于[后台功能](/docs/zh-CN/costs#background-token-usage)的模型 |
| `timeout` | 否 | 超时（秒）。默认值：30 |
| `continueOnBlock` | 否 | 在适用的事件上，`true` 将 `ok: false` 原因反馈给 Claude 并继续而不是结束转轮。默认值：`false`。有关每个事件的行为，请参阅[响应架构](#response-schema) |

<h3 id="response-schema">
  响应架构
</h3>

LLM 必须使用包含以下内容的 JSON 响应：

```json theme={null}
{
  "ok": true | false,
  "reason": "Explanation for the decision",
  "impossible": true | false
}
```

| 字段 | 描述 |
| :- | :- |
| `ok` | `true` 允许。对于 `false`，请参阅下面的每个事件行为 |
| `reason` | 当 `ok` 为 `false` 时必需 |
| `impossible` | 可选。当模型判断条件永远无法满足时，模型使用 `ok: false` 返回它。在 `Stop` 和 `SubagentStop` 上，Claude Code 随后让转轮结束而不是反馈原因。代理 hooks 和其他事件忽略它 |

`ok: false` 时发生的情况取决于事件：

* `Stop` 和 `SubagentStop`：原因被反馈给 Claude 作为其下一条指令，转轮继续，除非响应也设置 `impossible: true`，在这种情况下 Claude Code 允许停止，转轮结束
* `PreToolUse`：工具调用被拒绝；默认情况下转轮结束，拒绝原因在聊天中显示为警告行。设置 `continueOnBlock: true` 以改为将原因返回给 Claude 作为工具错误，以便它可以调整并继续，等同于命令 hook 的 `permissionDecision: "deny"`。在 v2.1.210 之前，拒绝原因被返回给 Claude 作为工具错误，转轮继续
* `PostToolUse`：默认情况下转轮结束，原因在聊天中显示为警告行。设置 `continueOnBlock: true` 以将原因反馈给 Claude 并继续转轮
* `PostToolBatch`、`UserPromptSubmit` 和 `UserPromptExpansion`：转轮结束，原因显示为警告行。这些事件在 `decision: "block"` 上结束转轮，无论 `continue` 如何
* `PostToolUseFailure` 和 `TaskCreated`：原因作为工具错误返回给 Claude，转轮继续，无论 `continueOnBlock` 如何
* `TaskCompleted`：当任务在转轮期间被标记为完成时触发时，原因作为工具错误返回给 Claude，转轮继续，无论 `continueOnBlock` 如何。当它因队友停止而触发时，它的行为类似于 `TeammateIdle` 并默认停止队友
* `TeammateIdle`：默认情况下队友停止，原因显示为警告行。设置 `continueOnBlock: true` 以将原因反馈给队友并保持其继续工作
* `PermissionRequest`：`ok: false` 无效。要从 hook 拒绝批准，请使用[命令 hook](#command-hook-fields)，返回 `hookSpecificOutput.decision.behavior: "deny"`
* `PermissionDenied`：`ok: false` 无效，因为拒绝已经发生。此事件读取的唯一输出是 `hookSpecificOutput.retry`，提示和代理 hooks 无法设置。它们在此事件上运行，但其输出被丢弃。使用[命令 hook](#command-hook-fields)返回 `retry`

如果您需要对任何事件进行更精细的控制，请使用[命令 hook](#command-hook-fields)，其中包含[决定控制](#decision-control)中描述的每个事件字段。

<h3 id="check-multiple-conditions-before-stopping">
  检查多个条件后再停止
</h3>

此 `Stop` hook 使用详细提示检查三个条件，然后允许 Claude 停止。`SubagentStop` hooks 使用相同的格式来评估[子代理](/docs/zh-CN/sub-agents)是否应该停止。如果模型因条件尚未满足而返回 `"ok": false`，Claude 继续工作，提供的原因作为其下一条指令：

```json theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "prompt",
            "prompt": "You are evaluating whether Claude should stop working. Context: $ARGUMENTS\n\nAnalyze the conversation and determine if:\n1. All user-requested tasks are complete\n2. Any errors need to be addressed\n3. Follow-up work is needed\n\nRespond with JSON: {\"ok\": true} to allow stopping, or {\"ok\": false, \"reason\": \"your explanation\"} to continue working.",
            "timeout": 30
          }
        ]
      }
    ]
  }
}
```

<h2 id="agent-based-hooks">
  基于代理的 hooks
</h2>

<Warning>
  代理 hooks 是实验性的。行为和配置可能在未来版本中更改。对于生产工作流，建议使用[命令 hooks](#command-hook-fields)。
</Warning>

基于代理的 hooks（`type: "agent"`）类似于基于提示的 hooks，但具有多轮工具访问。代理 hook 生成一个可以读取文件、搜索代码和检查代码库以验证条件的 subagent，而不是单个 LLM 调用。代理 hooks 支持与[基于提示的 hooks](#prompt-based-hooks) 相同的事件，除了 `PermissionRequest`。

<h3 id="how-agent-hooks-work">
  基于代理的 hooks 如何工作
</h3>

当代理 hook 触发时：

1. Claude Code 生成一个 subagent，带有您的提示和 hook 的 JSON 输入
2. Subagent 可以使用 Read、Grep 和 Glob 等工具进行调查
3. 在最多 50 轮后，subagent 返回结构化的 `{ "ok": true/false }` 决定
4. Claude Code 允许该操作（如果 `ok` 是 `true`）。如果 `ok` 是 `false`，Claude Code 处理阻止的方式与提示 hook 在该事件上具有 `continueOnBlock: true` 的方式相同，如[响应架构](#response-schema)下所列

代理 hooks 在验证需要检查实际文件或测试输出时很有用，而不仅仅是单独评估 hook 输入数据。

<h3 id="agent-hook-configuration">
  代理 hook 配置
</h3>

将 `type` 设置为 `"agent"` 并提供 `prompt` 字符串，使用 `$ARGUMENTS` 作为 hook 输入 JSON 的占位符。配置字段与[提示 hooks](#prompt-hook-configuration)相同，除了代理 hooks 具有更长的默认超时时间 60 秒，并且没有 `continueOnBlock` 字段。

响应架构是 `{ "ok": true }` 允许或 `{ "ok": false, "reason": "..." }` 阻止。在 `ok: false` 时，Claude Code 处理代理 hook 的方式与处理同一事件上具有 `continueOnBlock: true` 的[提示 hook](#response-schema) 的方式相同；代理 hooks 没有 `continueOnBlock` 字段，并且不支持提示 hook 的 `impossible` 字段。

此 `Stop` hook 验证所有单元测试通过，然后允许 Claude 完成：

```json theme={null}
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "agent",
            "prompt": "Verify that all unit tests pass. Run the test suite and check the results. $ARGUMENTS",
            "timeout": 120
          }
        ]
      }
    ]
  }
}
```

<h2 id="run-hooks-in-the-background">
  在后台运行 Hooks
</h2>

默认情况下，hooks 阻止 Claude 的执行，直到它们完成。对于长时间运行的任务，如部署、测试套件或外部 API 调用，设置 `"async": true` 以在后台运行 hook，同时 Claude 继续工作。异步 hooks 无法阻止或控制 Claude 的行为：响应字段如 `decision`、`permissionDecision` 和 `continue` 无效，因为它们会控制的操作已经完成。

<h3 id="configure-an-async-hook">
  配置异步 Hook
</h3>

将 `"async": true` 添加到命令 hook 的配置以在后台运行它而不阻止 Claude。此字段仅在 `type: "command"` hooks 上可用。

此 hook 在每个 `Write` 工具调用后运行测试脚本。Claude 立即继续工作，同时 `run-tests.sh` 执行。脚本完成时，其输出在下一个对话轮次上传递：

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "command": "/path/to/run-tests.sh",
            "async": true
          }
        ]
      }
    ]
  }
}
```

一旦异步 hook 在后台运行，Claude Code 不会对其强制执行 `timeout`。Claude Code 仍然对使用 `asyncRewake` 运行的 hook 强制执行 `timeout`。

Claude Code 仅在会话运行时传递异步 hook 的结果：

* 在[非交互模式](/docs/zh-CN/headless)中使用 `-p` 标志，Claude Code 在拆卸时杀死任何仍在运行的异步 hook，并以 `cancelled` 结果完成它
* 如果你的 hook 的工作必须超越 `claude -p` 会话，从它启动一个完全分离的进程

<h3 id="how-async-hooks-execute">
  异步 Hooks 如何执行
</h3>

当异步 hook 触发时，Claude Code 启动 hook 进程并立即继续，不等待其完成。Hook 通过 stdin 接收与同步 hook 相同的 JSON 输入。

后台进程退出后，Claude Code 从 hook 的 JSON 响应中传递 `additionalContext` 和 `systemMessage` 字段给 Claude 在下一个对话轮次。与同步 hook 的 `systemMessage` 不同，这两个字段都不会显示给你。

Claude Code 根据与同步 hooks 相同的[输出架构](#json-output)验证 JSON 响应，并删除任何值类型错误的字段，例如不是字符串的 `systemMessage`，而不是传递它。使用 `--debug` 运行以查看命名每个删除字段的警告。在 v2.1.202 之前，来自异步 hook 的格式错误的 JSON 输出可能会导致会话崩溃，并且每次恢复会话时崩溃都会重复发生。

异步 hook 完成通知默认被抑制。要查看它们，请使用 `Ctrl+O` 启用详细模式或使用 `--verbose` 启动 Claude Code。

<h3 id="run-tests-after-file-changes">
  文件更改后运行测试
</h3>

此 hook 在 Claude 写入文件时在后台启动测试套件，然后在测试完成时将结果报告回 Claude。将此脚本保存到项目中的 `.claude/hooks/run-tests-async.sh` 并使用 `chmod +x` 使其可执行：

```bash theme={null}
#!/bin/bash
# run-tests-async.sh

# 从 stdin 读取 hook 输入
INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# 仅对源文件运行测试
if [[ "$FILE_PATH" != *.ts && "$FILE_PATH" != *.js ]]; then
  exit 0
fi

# 运行测试并通过 additionalContext 向 Claude 报告结果
RESULT=$(npm test 2>&1)
EXIT_CODE=$?

if [ $EXIT_CODE -eq 0 ]; then
  MSG="Tests passed after editing $FILE_PATH"
else
  MSG="Tests failed after editing $FILE_PATH: $RESULT"
fi
jq -nc --arg msg "$MSG" '{hookSpecificOutput: {hookEventName: "PostToolUse", additionalContext: $msg}}'
```

然后将此配置添加到项目根目录中的 `.claude/settings.json`。`async: true` 标志让 Claude 在测试运行时继续工作：

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/run-tests-async.sh",
            "args": [],
            "async": true
          }
        ]
      }
    ]
  }
}
```

<h3 id="limitations">
  限制
</h3>

异步 hooks 与同步 hooks 相比有额外的约束：

* Hook 输出在下一个对话轮次传递。如果会话空闲，响应等待直到下一个用户交互。例外：退出代码为 2 的 `asyncRewake` hook 即使在会话空闲时也会立即唤醒 Claude。
* 每次执行创建一个单独的后台进程。同一异步 hook 的多个触发之间没有去重。

<h2 id="security-considerations">
  安全考虑
</h2>

<h3 id="disclaimer">
  免责声明
</h3>

<Warning>
  命令 hooks 使用您的完整用户权限执行 shell 命令。它们可以修改、删除或访问您的用户帐户可以访问的任何文件。在将任何 hook 命令添加到您的配置之前，请审查并测试它们。
</Warning>

<h3 id="workspace-trust">
  工作区信任
</h3>

Claude Code 在运行来自设置文件的任何 hook 之前会检查工作区信任。什么被视为受信任取决于会话类型：

* **交互式会话**：Claude Code 会保留来自每个设置文件的 hooks，包括您自己的 `~/.claude/settings.json`，直到您为该文件夹接受[工作区信任对话框](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust)，或为其信任扩展到的父目录接受
* **`-p` 或 SDK 会话**：Claude Code 从不显示对话框，并将该文件夹视为受信任的，因此在您从未信任过的文件夹中运行存储库的 `.claude/settings.json` 中提交的 hooks

在您对存储库进行脚本化 `claude -p` 之前，如果您没有编写该存储库，请审查其 `.claude/` 设置文件，使用 [`--bare`](/docs/zh-CN/headless#start-faster-with-bare-mode) 开始，或[为该运行关闭 hooks](#disable-or-remove-hooks)，使用 `--settings '{"disableAllHooks": true}'`。项目子代理中的 Frontmatter hooks 遵循比设置文件 hooks 更严格的规则。[在您信任文件夹之前运行的内容](/docs/zh-CN/permissions#what-runs-before-you-trust-a-folder)按会话类型列出每种存储库内容。

<h3 id="security-best-practices">
  安全最佳实践
</h3>

编写 hooks 时请记住这些实践：

* **验证和清理输入**：永远不要盲目信任输入数据
* **始终引用 shell 变量**：使用 `"$VAR"` 而不是 `$VAR`
* **阻止路径遍历**：检查文件路径中的 `..`
* **使用绝对路径**：为脚本指定完整路径。在 exec 形式中，使用 `${CLAUDE_PROJECT_DIR}` 且路径无需引用。在 shell 形式中，将其包装在双引号中
* **跳过敏感文件**：避免 `.env`、`.git/`、密钥等

<h2 id="windows-powershell-tool">
  Windows PowerShell 工具
</h2>

在 Windows 上，您可以通过在命令 hook 上设置 `"shell": "powershell"` 在 PowerShell 中运行单个 hooks。Claude Code 自动检测 `pwsh.exe`（PowerShell 7 及更高版本的可执行文件），并回退到 `powershell.exe`（Windows PowerShell 5.1）。

```json theme={null}
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write",
        "hooks": [
          {
            "type": "command",
            "shell": "powershell",
            "command": "Write-Host 'File written'"
          }
        ]
      }
    ]
  }
}
```

要从 PowerShell shell 形式命令引用项目根目录，请写入 `${CLAUDE_PROJECT_DIR}` 或 `$env:CLAUDE_PROJECT_DIR`。从 v2.1.198 开始，Claude Code 会将 PowerShell shell 形式命令中的 `${CLAUDE_PROJECT_DIR}`、`${CLAUDE_PLUGIN_ROOT}` 和 `${CLAUDE_PLUGIN_DATA}` 占位符重写为 PowerShell 的 `${env:NAME}` 形式，无论 hook 是在 `settings.json`、插件还是技能中定义。PowerShell 在解析后从导出的环境中解析该值，因此占位符在双引号字符串内有效，但在单引号字符串内无效，PowerShell 在单引号字符串中永远不会展开变量。

在 v2.1.198 之前，此重写仅适用于插件 hooks。在早期版本上，`settings.json` hook 需要 `$env:` 形式或 [exec 形式](#exec-form-and-shell-form)，其中 `${CLAUDE_PROJECT_DIR}` 在每个 `args` 元素中被替换，无论 hook 在何处定义。

不要在 PowerShell hook 中写入裸 `$CLAUDE_PROJECT_DIR` 拼写。PowerShell 将其解析为未定义的本地变量，并将其解析为 `$null`，这会导致脚本路径没有其项目根前缀。Claude Code 不会重写该形式；它会在 [debug log](#debug-hooks) 中记录警告。

下面的示例显示了一个 `settings.json` hook，它使用 `$env:` 形式运行项目脚本，该形式在每个版本上都有效：

```json theme={null}
{
  "type": "command",
  "shell": "powershell",
  "command": "& \"$env:CLAUDE_PROJECT_DIR\\.claude\\hooks\\check.ps1\""
}
```

<h2 id="debug-hooks">
  调试 hooks
</h2>

Hook 执行详细信息被写入调试日志文件。使用 `claude --debug-file <path>` 启动 Claude Code 以将日志写入已知位置，或运行 `claude --debug` 并在 `~/.claude/debug/<session-id>.txt` 读取日志。`--debug` 标志不打印到终端。

例如，在 `Write` 上的 `PostToolUse` hook，其命令打印 `hook-ran` 会产生如下条目：

```text theme={null}
2026-07-19T02:03:24.382Z [DEBUG] Hook output does not start with {, treating as plain text
2026-07-19T02:03:24.382Z [DEBUG] "Hook PostToolUse:Write (PostToolUse) success:\nhook-ran"
```

对于更细粒度的 hook 匹配详细信息，设置 `CLAUDE_CODE_DEBUG_LOG_LEVEL=verbose` 以查看额外的日志行，例如 hook 匹配器计数和查询匹配。

有关故障排除常见问题，如 hooks 不触发、Stop hooks 持续阻止或配置错误，请参阅指南中的[限制和故障排除](/docs/zh-CN/hooks-guide#limitations-and-troubleshooting)。有关涵盖 `/context`、`/doctor` 和设置优先级的更广泛的诊断演练，请参阅[调试你的配置](/docs/zh-CN/debug-your-config)。
