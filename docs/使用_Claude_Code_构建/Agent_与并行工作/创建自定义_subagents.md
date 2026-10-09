> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 创建自定义 subagents

> 在 Claude Code 中创建和使用专门的 AI subagents，用于特定任务的工作流和改进的上下文管理。

Subagents 是处理特定类型任务的专门 AI 助手。当一个辅助任务会用搜索结果、日志或文件内容充斥您的主对话，而您不会再次引用这些内容时，请使用一个 subagent：该 subagent 在自己的上下文中完成这项工作，仅返回摘要。当您不断生成相同类型的工作者并使用相同的指令时，定义一个自定义 subagent。

每个 subagent 在自己的 context window 中运行，具有自定义系统提示、特定的工具访问权限和独立的权限。它还发送自己的请求，这些请求计入与您的主对话相同的[使用限制](/docs/zh-CN/costs#plan-usage-breakdown)。当 Claude 遇到与 subagent 描述相匹配的任务时，它会委托给该 subagent，该 subagent 独立工作并返回结果。要在实践中看到上下文节省，[context window 可视化](/docs/zh-CN/context-window)演示了一个 subagent 在自己的独立窗口中处理研究的会话。

<Note>
  Subagents 在单个会话中工作。要在并行运行许多独立会话并从一个地方监控它们，请参阅 [background agents](/docs/zh-CN/agent-view)。对于相互传递消息的单独会话，请参阅 [cross-session messaging](/docs/zh-CN/cross-session-messaging)。对于 Claude 生成和监督的协调团队会话，请参阅 [agent teams](/docs/zh-CN/agent-teams)。
</Note>

Subagents 帮助您：

* **保留上下文**，通过将探索和实现保持在主对话之外
* **强制执行约束**，通过限制 subagent 可以使用的工具
* **跨项目重用配置**，使用用户级 subagents
* **专门化行为**，为特定领域使用专注的系统提示
* **控制成本**，通过将任务路由到更快、更便宜的模型（如 Haiku）

Claude 使用每个 subagent 的描述来决定何时委托任务。创建 subagent 时，请编写清晰的描述，以便 Claude 知道何时使用它。

这些描述会占用上下文，因此请保持简洁。当您的 subagents（除了内置的 subagents）的组合描述超过 15,000 个 token 时，Claude Code 会在启动时显示 [包含总 token 计数的警告](/docs/zh-CN/errors#agent-descriptions-are-over-the-15000-token-limit)。修剪您的 subagents 的 `description` 字段，并将详细信息移到每个 subagent 的系统提示中，该提示仅在该 subagent 运行时加载。

<h2 id="built-in-subagents">
  内置 subagents
</h2>

Claude Code 包括内置 subagents，Claude 在适当时自动使用。每个都继承父对话的权限规则；大多数运行时工具集受限。

Explore 和 Plan 会跳过您的 CLAUDE.md 文件和 git 状态快照，以保持研究快速且成本低廉。所有其他内置和[自定义 subagent](#configure-subagents) 都会加载两者，除非其定义设置了 [`omitClaudeMd`](#supported-frontmatter-fields) 字段以跳过用户、项目和本地 CLAUDE.md 文件。有关到达 subagent 的内容的完整分解，请参阅[启动时加载的内容](#what-loads-at-startup)。

<Tabs>
  <Tab title="Explore">
    一个快速的、只读的代理，针对搜索和分析代码库进行了优化。

    * **Model**: 主对话的模型。当主对话运行 Fable 时，Explore 的模型取决于您的连接方式：
      * 使用 Claude 订阅、Anthropic Console 账户，或通过 `ANTHROPIC_BASE_URL` 访问的 [LLM 网关](/docs/zh-CN/llm-gateway)时，Explore 在 [`opus` 别名](/docs/zh-CN/model-config#model-aliases)解析到的 Opus 模型上运行。
      * 在 Amazon Bedrock、Google Cloud 的 Agent Platform、Microsoft Foundry、[AWS 上的 Claude Platform](/docs/zh-CN/claude-platform-on-aws) 或 [Claude apps 网关](/docs/zh-CN/claude-apps-gateway)上，Explore 保持使用主对话的模型。
    * **Tools**: 只读工具；拒绝访问 Write 和 Edit
    * **Purpose**: 文件发现、代码搜索、代码库探索

    名为 `Explore` 的[用户或项目子代理](#choose-the-subagent-scope)会覆盖内置的子代理，并保持其自己的 `model` 字段，因此可以定义一个带有 `model: haiku` 的子代理，在较低成本的模型上运行探索。要将同一个模型强制应用于每个子代理（包括 Explore），请参阅[在一个模型上运行每个子代理](#run-every-subagent-on-one-model)。

    当 Claude 需要搜索或理解代码库而不进行更改时，它会委托给 Explore。这样可以将探索结果保持在主对话上下文之外。

    调用 Explore 时，Claude 指定一个彻底程度级别：**quick** 用于有针对性的查找，**medium** 用于平衡的探索，或 **very thorough** 用于全面分析。
  </Tab>

  <Tab title="Plan">
    一个研究代理，在 [plan mode](/docs/zh-CN/permission-modes#analyze-before-you-edit-with-plan-mode) 期间使用，以在呈现计划之前收集上下文。

    * **Model**: 从主对话继承，除非您设置 `CLAUDE_CODE_SUBAGENT_MODEL` 并[强制将其应用于每个 subagent](#run-every-subagent-on-one-model)
    * **Tools**: 只读工具；拒绝访问 Write 和 Edit
    * **Purpose**: 用于规划的代码库研究

    当您处于 plan mode 并且 Claude 需要理解您的代码库时，它会将研究委托给 Plan subagent，以便探索输出保持在单独的上下文窗口中，而主对话保持只读。
  </Tab>

  <Tab title="General-purpose">
    一个能够处理复杂、多步骤任务的代理，需要探索和操作。

    * **Model**: 如果您设置了 [`CLAUDE_CODE_SUBAGENT_MODEL`](#choose-a-model) 模型且没有其他方式分配模型，则使用该模型，否则使用主对话的模型；[选择模型](#choose-a-model) 说明了完整的顺序，[在一个模型上运行每个 subagent](#run-every-subagent-on-one-model) 展示了如何使变量覆盖这些来源
    * **Tools**: 所有[可用于 subagents 的工具](#available-tools)
    * **Purpose**: 复杂研究、多步骤操作、代码修改

    当任务需要探索和修改、复杂推理来解释结果或多个依赖步骤时，Claude 会委托给 general-purpose。
  </Tab>

  <Tab title="Other">
    Claude Code 包括用于特定任务的其他辅助代理。这些通常会自动调用，因此您不需要直接使用它们。

    | Agent | Model | Claude 何时使用它 |
    | :- | :- | :- |
    | claude | 没有自己的；当 Claude 将其生成为 subagent 时遵循[模型顺序](#choose-a-model) | 当任务不适合更专业的代理时。一个具有所有[可用于 subagents 的工具](#available-tools)的通用代理。也是调度的[后台会话](/docs/zh-CN/agent-view)的默认代理；[它启动的权限模式](/docs/zh-CN/agent-view#permission-mode-model-and-effort)取决于会话的启动方式 |
    | statusline-setup | Sonnet | 当您运行 `/statusline` 来配置您的状态行时 |
    | claude-code-guide | Haiku | 当您提出关于 Claude Code 功能的问题时 |
  </Tab>
</Tabs>

内置 subagents 在交互式会话中默认被注册。要限制它们：

* 要阻止特定的内置类型，请将其添加到 `permissions.deny`，如[禁用特定 subagents](#disable-specific-subagents) 中所示。
* 要防止 Claude 委托给任何 subagent，请使用 [`permissions.deny`](/docs/zh-CN/permissions#tool-specific-permission-rules) 拒绝 `Agent` 工具本身。
* 要仅移除内置的 `Explore` 和 `Plan` subagents，请设置 [`CLAUDE_CODE_DISABLE_EXPLORE_PLAN_AGENTS=1`](/docs/zh-CN/env-vars)。Claude 直接读取和探索文件，而不是委托给它们。需要 Claude Code v2.1.198 或更高版本。
* 在[非交互模式](/docs/zh-CN/headless) 和 [Agent SDK](/docs/zh-CN/agent-sdk/overview) 中，设置 [`CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS=1`](/docs/zh-CN/env-vars) 以移除所有内置类型并仅提供您自己的。

当会话没有 `general-purpose` subagent 可回退时，省略 `subagent_type` 的 Agent 工具调用会失败，并显示 [`subagent_type is required`](/docs/zh-CN/errors#subagent-type-is-required)。

除了这些内置 subagents，您可以创建自己的，具有自定义提示、工具限制、权限模式、hooks 和 skills。以下部分展示了如何开始和自定义 subagents。

<h2 id="quickstart-create-your-first-subagent">
  快速入门：创建您的第一个子代理
</h2>

子代理是带有 YAML frontmatter 的 Markdown 文件。要创建一个，请要求 Claude 为您编写，或者 [自己编写文件](#write-subagent-files)。

本演练创建一个用户级子代理，用于审查代码并建议改进。

<Steps>
  <Step title="要求 Claude 创建子代理">
    在 Claude Code 中，描述您想要的子代理及其保存位置：

    ```text wrap theme={null}
    Create a personal code-improver subagent in ~/.claude/agents/ that scans
    files and suggests improvements for readability, performance, and best
    practices. It should explain each issue, show the current code, and
    provide an improved version. Make it read-only and have it use Sonnet.
    ```

    Claude 使用 `name`、`description`、`tools` 列表、`model` 和系统提示词来编写文件。
  </Step>

  <Step title="审查文件">
    打开 `~/.claude/agents/code-improver.md` 并确认 frontmatter 与您的要求相符。结果如下所示：

    ```markdown theme={null}
    ---
    name: code-improver
    description: Scans files and suggests improvements for readability, performance, and best practices. Use after writing or modifying code.
    tools: Read, Grep, Glob
    model: sonnet
    ---

    You are a code improvement specialist. For each issue you find, explain
    the problem, show the current code, and provide an improved version.
    ```

    因为该文件位于 `~/.claude/agents/`，所以该子代理在您机器上的每个项目中都可用。要将其限定在一个项目中，请将其移动到该项目的 `.claude/agents/` 目录。[选择子代理作用域](#choose-the-subagent-scope) 比较了两者。
  </Step>

  <Step title="尝试一下">
    要求 Claude 委托给新的子代理：

    ```text wrap theme={null}
    Use the code-improver agent to suggest improvements in this project
    ```

    Claude 委托给您的新子代理，它扫描代码库并返回改进建议。在会话记录中，委托显示为工具调用行，显示子代理的名称后跟简短的任务描述，例如 `code-improver(Suggest code improvements)`。

    如果 Claude 找不到新的子代理，请重新启动 Claude Code 并重试。这仅在会话开始前 `~/.claude/agents/` 不存在时发生，因为运行中的会话不会检测到新创建的 `agents` 目录。
  </Step>
</Steps>

现在您有了一个子代理，可以在您机器上的任何项目中使用它来分析代码库并建议改进。

您也可以手动编写子代理文件、通过 CLI 标志定义它们，或通过插件分发它们。以下部分涵盖所有配置选项。

<Note>
  运行 `/agents` 会打印一个提醒，提示您询问 Claude 或直接编辑 `.claude/agents/` 和 `~/.claude/agents/`。
  在 Claude Code v2.1.197 及更早版本中，`/agents` 打开一个交互式向导，其中有一个 **Running** 选项卡列出实时子代理，以及一个 **Library** 选项卡用于创建、编辑和删除它们。
</Note>

<h2 id="configure-subagents">
  配置 subagents
</h2>

一个 subagent 的文件位置决定了谁可以使用它，其 frontmatter 决定了它可以做什么。本节涵盖 subagent 文件的位置以及它们支持的每个字段。

<h3 id="choose-the-subagent-scope">
  选择 subagent 范围
</h3>

根据范围将 subagent 文件存储在不同的位置。当多个 subagents 共享相同的名称时，Claude Code 使用来自更高优先级位置的那个。

| Location | Scope | Priority | 如何创建 |
| :- | :- | :- | :- |
| 托管设置 | 组织范围 | 1（最高） | 通过 [managed settings](/docs/zh-CN/settings) 部署 |
| `--agents` CLI 标志 | 当前会话 | 2 | 启动 Claude Code 时传递 JSON |
| `.claude/agents/` | 当前项目 | 3 | 询问 Claude，或手动创建文件 |
| `~/.claude/agents/` | 所有您的项目 | 4 | 询问 Claude，或手动创建文件 |
| Plugin 的 `agents/` 目录 | 启用 plugin 的位置 | 5（最低） | 与 [plugins](/docs/zh-CN/plugins/overview) 一起安装 |

**项目 subagents**（`.claude/agents/`）非常适合特定于代码库的 subagents。将它们检入版本控制，以便您的团队可以协作使用和改进它们。

项目 subagents 通过从当前工作目录向上遍历来发现，因此会扫描那里和存储库根目录之间的每个 `.claude/agents/`。当这些嵌套目录中的多个目录定义相同的 `name` 时，Claude Code 使用最接近工作目录的定义。

使用 `--add-dir` 或 `/add-dir` 添加目录时，Claude Code 也会加载其 `.claude/agents/` 文件夹，与您的项目 subagents 一起。有关哪些其他配置类型从 `--add-dir` 加载，请参阅 [Additional directories](/docs/zh-CN/permissions#additional-directories-grant-file-access-not-configuration)。要在没有 `--add-dir` 的情况下跨项目共享 subagents，请使用 `~/.claude/agents/` 或 [plugin](/docs/zh-CN/plugins/overview)。

**用户 subagents**（`~/.claude/agents/`）是在所有项目中可用的个人 subagents。

Claude Code 递归扫描 `.claude/agents/` 和 `~/.claude/agents/`，因此您可以将定义组织到子文件夹中，例如 `agents/review/` 或 `agents/research/`。子目录路径不会影响 subagent 的识别或调用方式，因为身份仅来自 `name` frontmatter 字段。

在整个树中保持 `name` 值唯一：如果同一 `.claude/agents/` 目录下的两个文件（包括其子文件夹）声明相同的名称，Claude Code 仅加载其中一个，由文件系统读取顺序选择，而不是有文档记录的优先级。在嵌套项目目录中，最接近工作目录的定义获胜，如上所述。[`/doctor`](/docs/zh-CN/commands#all-commands) 设置检查报告同一目录中共享名称的文件，并建议重命名或删除除一个之外的所有文件。在 v2.1.205 之前，`/doctor` 打开一个诊断屏幕，列出重复项并显示哪个定义是活跃的。

Plugin `agents/` 目录也会被递归扫描。与项目和用户范围不同，plugin 的 `agents/` 目录内的子文件夹成为 [scoped identifier](#invoke-subagents-explicitly) 的一部分：plugin `my-plugin` 中位于 `agents/review/security.md` 的文件注册为 `my-plugin:review:security`。

**CLI 定义的 subagents** 在启动 Claude Code 时作为 JSON 传递。它们仅存在于该会话中，不会保存到磁盘，使其对快速测试或自动化脚本很有用。您可以在单个 `--agents` 调用中定义多个 subagents：

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    claude --agents '{
      "code-reviewer": {
        "description": "Expert code reviewer. Use proactively after code changes.",
        "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
        "tools": ["Read", "Grep", "Glob", "Bash"],
        "model": "sonnet"
      },
      "debugger": {
        "description": "Debugging specialist for errors and test failures.",
        "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
      }
    }'
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    claude --agents @'
    {
      "code-reviewer": {
        "description": "Expert code reviewer. Use proactively after code changes.",
        "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
        "tools": ["Read", "Grep", "Glob", "Bash"],
        "model": "sonnet"
      },
      "debugger": {
        "description": "Debugging specialist for errors and test failures.",
        "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
      }
    }
    '@
    ```
  </Tab>
</Tabs>

在 [non-interactive mode](/docs/zh-CN/headless) 中，`--agents` 也接受保存相同对象的 JSON 文件的路径，用于定义太大而无法在命令行上传递的情况。例如，`claude -p --agents ./agents.json "Review my changes"` 从该文件读取定义。在交互式会话中，Claude Code 拒绝文件路径。文件形式需要 Claude Code v2.1.281 或更高版本。

JSON 中的每个顶级键是代理的名称，其值是该代理的定义。不要以 `-` 开头的名称。定义采用这些字段：

* **`prompt`**：代理的系统提示，等同于基于文件的 subagents 中的 markdown 正文。`prompt` 可能为空。如果您选择一个具有空 `prompt` 且没有 `memory` 字段的代理作为会话的代理，使用 `--agent`，会话的系统提示保持不变。空 `prompt` 需要 Claude Code v2.1.281 或更高版本。
* **[Frontmatter 字段](#supported-frontmatter-fields)**：`description`、`tools`、`disallowedTools`、`model`、`permissionMode`、`mcpServers`、`hooks`、`maxTurns`、`skills`、`initialPrompt`、`memory`、`effort`、`background`、`omitClaudeMd` 和 `isolation`。
* **忽略的字段**：`color` 和 `experimental` 在此处不被接受，被忽略而不是拒绝。

有关 Claude Code 对无法加载的值的处理，以及跳过该检查的标志和环境变量，请参阅 [`Invalid --agents configuration`](/docs/zh-CN/errors#invalid-agents-configuration)。

**托管 subagents** 由组织管理员部署。在 [managed settings directory](/docs/zh-CN/managed-settings#delivery-mechanisms) 内的 `.claude/agents/` 中放置 markdown 文件，使用与项目和用户 subagents 相同的 frontmatter 格式。托管定义优先于具有相同名称的项目和用户 subagents。

**Plugin subagents** 来自您已安装的 [plugins](/docs/zh-CN/plugins/overview)。它们与您的自定义 subagents 一起自动加载，并在 @-mention 类型提前中以其范围名称出现。有关创建 plugin subagents 的详细信息，请参阅 [plugin 组件参考](/docs/zh-CN/plugins/components#agents)。

<Note>
  出于安全原因，插件子代理不支持 `hooks`、`mcpServers` 或 `permissionMode` frontmatter 字段。从插件加载 Agent 时，这些字段会被忽略。如果您需要它们，请将 Agent 文件复制到 `.claude/agents/` 或 `~/.claude/agents/`。您也可以在 `settings.json` 或 `settings.local.json` 中向 [`permissions.allow`](/docs/zh-CN/settings-reference#permissions-allow) 添加规则，但这些规则适用于整个会话，而不仅仅是该插件子代理。

  如果您是插件的作者，请改为在插件的 [`hooks/hooks.json`](/docs/zh-CN/plugins/components#hooks) 中提供 hook，并在其 [`.mcp.json`](/docs/zh-CN/plugins/components#mcp-servers) 中提供 MCP 服务器。它们会在插件启用时始终生效，而不仅仅在子代理内部生效。
</Note>

您还可以将子代理定义复用为 [agent team](/docs/zh-CN/agent-teams) 的队友：在要求 Claude 生成队友时指定子代理类型，Claude Code 会将该定义的部分内容应用于该队友。[将子代理定义用于队友](/docs/zh-CN/agent-teams#use-subagent-definitions-for-teammates)说明了在每种显示模式下适用哪些作用域以及哪些部分。

<h3 id="write-subagent-files">
  编写 subagent 文件
</h3>

Subagent 文件使用 YAML frontmatter 进行配置，然后是 Markdown 中的系统提示：

<Note>
  Claude Code 监视 `~/.claude/agents/` 和 `.claude/agents/`。当您在磁盘上添加或编辑 subagent 文件，或要求 Claude 为您编写一个时，Claude Code 会在几秒内检测到更改，下一次委托使用更新的定义，无需重启。

  三种情况仍然需要重启：

  * 监视器仅涵盖会话启动时存在的目录，因此在新 `agents` 目录中创建范围的第一个代理文件后，重启以加载它。
  * Claude Code 不监视通过 `--add-dir` 或 `/add-dir` 添加的目录内的 `.claude/agents/`，因此在那里添加或编辑 subagent 后，重启以加载更改。
  * 使用 `--disable-slash-commands` 启动的会话根本不监视这些目录。
</Note>

```markdown .claude/agents/code-reviewer.md theme={null}
---
name: code-reviewer
description: Reviews code for quality and best practices
tools: Read, Glob, Grep
model: sonnet
---

You are a code reviewer. When invoked, analyze the code and provide
specific, actionable feedback on quality, security, and best practices.
```

Frontmatter 定义了 subagent 的元数据和配置。正文成为指导 subagent 行为的系统提示。Subagents 仅接收此系统提示加上基本环境详细信息（如工作目录），而不是 Claude Code 系统提示。

在 [non-interactive mode](/docs/zh-CN/headless) 中，传递 [`--append-subagent-system-prompt`](/docs/zh-CN/cli-reference#cli-flags) 以将您的文本附加到每个 subagent 的系统提示末尾，包括嵌套 subagents，除了 [forked subagent](#fork-the-current-conversation)，它重用对话自己的提示。需要 Claude Code v2.1.205 或更高版本。如果您的文本太长而无法在命令行上传递，请将其保存到文件并使用 `--append-subagent-system-prompt-file` 传递路径。文件标志需要 Claude Code v2.1.261 或更高版本。

一个 subagent 在主对话的当前工作目录中启动。在 subagent 中，`cd` 命令不会在 Bash 或 PowerShell 工具调用之间持续，也不会影响主对话的工作目录。要给 subagent 一个隔离的存储库副本，请改为设置 [`isolation: worktree`](#supported-frontmatter-fields)。

具有 `isolation: worktree` 的 subagent 在其 worktree 内运行其 Bash 和 PowerShell 命令。一个工作目录解析到您的主检出的命令，例如因为 worktree 目录在 subagent 运行时被删除，会失败并出现错误。在 v2.1.203 之前，这样的命令可能在主检出中运行。

此工作目录检查涵盖包含您启动 Claude Code 的目录的整个存储库。当您的会话在其自己的链接 [worktree](/docs/zh-CN/worktrees) 中运行时，检查也涵盖该 worktree 链接的主检出。在 v2.1.210 之前，检查仅涵盖启动目录本身。一个工作目录解析到同一存储库中其他地方的命令，例如当您从 monorepo 子目录启动 Claude Code 时的存储库根目录，会在那里运行而不是失败。

对于 Bash 命令，Claude Code 还以两种方式检查命令本身：

* 它阻止将 git 重定向到主检出的命令。
* 当它无法从命令文本验证命令运行的任何 git 都保留在 worktree 内时，它拒绝命令，例如当命令名称在运行时计算时。

重定向向量和形状规则列在 [How Claude Code enforces isolation](/docs/zh-CN/worktrees#how-claude-code-enforces-isolation) 下。PowerShell 命令仅获得工作目录检查。

[Monitor](/docs/zh-CN/tools-reference#monitor-tool) 命令通过与 Bash 命令相同的工作目录和命令内容检查。

当主对话本身在 worktree 中隔离运行时，Claude Code 对会话和它生成的每个 subagent 应用相同的检查，包括没有 `isolation: worktree` 的 subagents；请参阅 [How Claude Code enforces isolation](/docs/zh-CN/worktrees#how-claude-code-enforces-isolation)。

<h3 id="supported-frontmatter-fields">
  Frontmatter 参考
</h3>

配置一个 subagent 时，使用 YAML [frontmatter](/docs/zh-CN/glossary#frontmatter) 在其文件顶部的 `---` 标记之间，并在关闭 `---` 后将其系统提示写为 Markdown。只有 `name` 和 `description` 是必需的。

多字段名称使用 camelCase，例如 `maxTurns` 和 `disallowedTools`，必须与表格完全匹配：Claude Code 忽略它不识别的字段而不报告错误。要找出为什么 subagent 文件没有加载，请参阅 [Subagent files Claude Code skips](#subagent-files-claude-code-skips)。

| Field | 必需 | Description |
| :- | :- | :- |
| `name` | 是 | 最多 256 个字符的唯一标识符，例如 `code-reviewer` 或 `reviewer-v2`。[Hook](/docs/zh-CN/hooks#subagentstart) 以 `agent_type` 的形式接收此值。文件名不必与之一致。名称不能包含 `:`，该字符保留用于[插件作用域标识符](/docs/zh-CN/plugins/overview)，例如 `my-plugin:reviewer` |
| `description` | 是 | Claude 何时应该委托给此 subagent |
| `tools` | 否 | [Tools](#available-tools) subagent 可以使用，作为逗号分隔的字符串，例如 `Read, Grep, Bash` 或 YAML 列表。如果省略，继承 subagents 可用的每个工具。如果列表中没有条目解析为工具，subagent 通常 [fails to launch](/docs/zh-CN/errors#agent-would-be-spawned-with-zero-tools) 并出现错误，命名条目。要将 Skills 预加载到上下文中，请使用 `skills` 字段而不是在此处列出 `Skill` |
| `disallowedTools` | 否 | 要拒绝的工具，从继承或指定的列表中删除。格式与 `tools` 相同。带有说明符的条目，例如 `Bash(git push *)`，仍然 [removes the whole tool](#available-tools) |
| `model` | 否 | [Model](#choose-a-model) 使用：`sonnet`、`opus`、`haiku`、`fable`、完整模型 ID（例如，`claude-opus-5-5`）或 `inherit`。当您省略它时，Claude Code 在 [subagent model order](#choose-a-model) 中选择模型 |
| `permissionMode` | 否 | [权限模式](#permission-modes)：`default`、`acceptEdits`、`auto`、`dontAsk`、`bypassPermissions`、`plan`，或作为 `default` 别名的 `manual`。对[插件子代理](#choose-the-subagent-scope)会被忽略 |
| `maxTurns` | 否 | subagent 停止前的最大代理轮数。当 subagent 达到限制时，Claude Code 返回其输出标记为部分，Claude 可以 [resume it](#resume-subagents) 继续。部分标记需要 Claude Code v2.1.246 或更高版本 |
| `skills` | 否 | [Skills](/docs/zh-CN/skills) 在启动时预加载到 subagent 的上下文中。注入完整的技能内容，而不仅仅是描述。Subagents 仍然可以通过 Skill 工具调用未列出的项目、用户和 plugin 技能 |
| `mcpServers` | 否 | [MCP servers](/docs/zh-CN/mcp) 对此 subagent 可用。每个条目要么是引用已配置服务器的服务器名称（例如，`"slack"`），要么是内联定义，其中服务器名称为键，完整的 [MCP server config](/docs/zh-CN/mcp#installing-mcp-servers) 为值。对于 [plugin subagents](#choose-the-subagent-scope) 被忽略 |
| `hooks` | 否 | [Lifecycle hooks](#define-hooks-for-subagents) 限定于此 subagent。对于 [plugin subagents](#choose-the-subagent-scope) 被忽略 |
| `memory` | 否 | [Persistent memory scope](#enable-persistent-memory)：`user`、`project` 或 `local`。启用跨会话学习 |
| `background` | 否 | 设置为 `true` 以即使 Claude 要求在前台运行也保持此 subagent 在后台。其中 [fork mode](#turn-fork-mode-on-or-off) 打开时，Claude Code 已经在 [background](#run-subagents-in-foreground-or-background) 中运行 Claude 生成的 subagents |
| `omitClaudeMd` | 否 | 设置为 `true` 以启动此 subagent 而不使用用户、项目和本地 CLAUDE.md 文件；[managed policy files](/docs/zh-CN/memory#how-claude-md-files-load) 仍然加载，除了 [managed subagents](#choose-the-subagent-scope)。对于从 [delegation prompt](#what-loads-at-startup) 获取所需一切的 subagents 使用它。当代理通过 `--agent` 或 `agent` 设置作为主会话代理运行时被忽略。需要 Claude Code v2.1.271 或更高版本 |
| `effort` | 否 | 此子代理活跃时的 effort 级别。覆盖会话的 effort 级别，但不覆盖 [`CLAUDE_CODE_EFFORT_LEVEL`](/docs/zh-CN/env-vars#variables) 环境变量。选项：`low`、`medium`、`high`、`xhigh`、`max`；可用级别取决于模型。请参阅[选择 effort 级别](#choose-an-effort-level) |
| `isolation` | 否 | 设置为 `worktree` 以在临时 [git worktree](/docs/zh-CN/worktrees) 中运行 subagent，为其提供存储库的隔离副本，默认从您的 [default branch](/docs/zh-CN/worktrees#choose-the-base-branch) 分支，而不是父会话的 `HEAD`。如果 subagent 不进行任何更改，worktree 会自动清理 |
| `color` | 否 | Subagent 在任务列表和转录中的显示颜色。接受 `red`、`blue`、`green`、`yellow`、`purple`、`orange`、`pink` 或 `cyan` |
| `initialPrompt` | 否 | 当此代理作为主会话代理运行时（通过 `--agent` 或 `agent` 设置），自动提交为第一个用户轮次。[Commands](/docs/zh-CN/commands) 和 [skills](/docs/zh-CN/skills) 被处理。前置于任何用户提供的提示。对于 [plugin subagents](#choose-the-subagent-scope) 被忽略 |
| `experimental` | 否 | 实验选项的映射。将其 `cacheTtl` 键设置为 `5m` 或 `1h` 以选择此 subagent 请求的 [prompt cache lifetime](/docs/zh-CN/prompt-caching#choose-the-ttl-yourself)，在 frontmatter 的 [cache lifetime precedence](/docs/zh-CN/prompt-caching#choose-the-ttl-yourself) 中的位置。Claude Code 忽略任何其他值，在您的 Claude 订阅使用使用额度时忽略 `1h`，并仅从 subagent 文件读取字段。需要 Claude Code v2.1.248 或更高版本 |

在 `experimental` 映射内写入 `cacheTtl`，而不是在 frontmatter 的顶级。

```yaml theme={null}
---
name: repo-auditor
description: Audits a large repository and reports what it finds
experimental:
  cacheTtl: 1h
---
```

<h4 id="subagent-files-claude-code-skips">
  Subagent 文件 Claude Code 跳过
</h4>

Claude Code 跳过项目、用户或托管 `agents` 目录中的文件，或在您使用 `--add-dir` 添加的目录下的文件，而不在会话中报告它，当 frontmatter 有以下任何问题时：

* **没有 `name`**：Claude Code 将文件视为保存在您的代理旁边的文档。
* **一个开始 `---` 不是文件的第一行**：Claude Code 读取文件为没有 frontmatter，并将其视为文档。
* **`name` 以 `-` 开头、包含 `:` 或超过 256 个字符**：Claude Code 跳过该文件，并向调试日志写入一条错误。
* **一个 `name` 但没有 `description`**：Claude Code 跳过文件并向调试日志写入原因。
* **不解析的 YAML**：Claude Code 从文件读取没有字段，跳过它，并向调试日志写入解析错误。

要查看调试日志，使用 `--debug` 运行 Claude Code。

一个 [plugin subagent](/docs/zh-CN/plugins/components#agents)，其 frontmatter 没有 `name` 或不解析，仍然加载，在其文件名下。

<h5 id="check-an-agents-directory-before-a-session">
  在会话前检查 `agents` 目录
</h5>

要查找 `agents` 目录中 frontmatter 不解析的文件，针对目录运行 `claude plugin validate`，例如 `.claude/agents` 或 `~/.claude/agents`。Claude Code 仅检查 [您命名的目录](/docs/zh-CN/plugins/cli-reference#validate-a-directory)，并不标记 frontmatter 解析但没有 `name` 的文件。需要 Claude Code v2.1.233 或更高版本。

<h3 id="choose-a-model">
  选择模型
</h3>

`model` 字段控制 subagent 使用的模型：

* **Model alias**：使用可用的别名之一：`sonnet`、`opus`、`haiku` 或 `fable`
* **Full model ID**：使用完整的模型 ID，例如 `claude-opus-5-5` 或 `claude-sonnet-5`。接受与 `--model` 标志相同的值
* **inherit**：使用与主对话相同的模型

当 Claude 调用 subagent 时，它也可以为该特定调用传递 `model` 参数。Claude Code 按以下顺序解析 subagent 的模型：

1. 每次调用的 `model` 参数
2. Subagent 定义的 `model` frontmatter，其中 `inherit` 选择主对话的模型
3. [`CLAUDE_CODE_SUBAGENT_MODEL`](/docs/zh-CN/model-config#environment-variables) 环境变量，当您将其设置为模型别名或模型 ID 时
4. 主对话的模型

如果已安装的 [mod](/docs/zh-CN/plugins/mods/overview) 在其 [`agent.spawn`](/docs/zh-CN/plugins/mods/reference#subagents) hook 中设置了模型，Claude Code 会使用该模型来代替每次调用的参数。

在两种情况下，家族别名（例如 frontmatter 或每次调用的参数中的 `opus`）解析到主对话的模型，而不是 [alias points to](/docs/zh-CN/model-config#model-aliases) 的版本：

* **主对话的模型属于该家族**：subagent 在主对话的确切模型上运行，包括任何 `[1m]` 后缀，因此它获得与主对话相同的 [extended context](/docs/zh-CN/model-config#extended-context) 窗口。
* **Claude Code 无法告诉主对话的模型家族，在 [a provider other than the Anthropic API](/docs/zh-CN/third-party-integrations) 上**：这可能发生在 Amazon Bedrock 上的 [application inference profile ARN](/docs/zh-CN/amazon-bedrock#iam-configuration)，Claude Code 尚未解析为支持模型。这种情况仅涵盖 `opus` 别名，当您设置 [`ANTHROPIC_DEFAULT_OPUS_MODEL`](/docs/zh-CN/model-config#environment-variables) 时不适用，因为 `opus` 然后解析到您设置的模型。

`CLAUDE_CODE_SUBAGENT_MODEL` 中的别名始终解析到别名指向的版本，即使它命名主对话的家族。

设置 `CLAUDE_CODE_SUBAGENT_MODEL` 本身不会改变内置 Explore 和 Plan subagents 运行的模型。要改变它，请参阅 [Run every subagent on one model](#run-every-subagent-on-one-model)。

在 v2.1.251 之前，`CLAUDE_CODE_SUBAGENT_MODEL` 在此顺序中排在第一位，并覆盖每次调用的参数和 frontmatter，包括 `model: inherit`。

将变量设置为 `inherit` 与不设置它相同。在 v2.1.196 之前，该值强制 subagents 使用主对话的模型并忽略其他来源。

Claude Code 根据您组织的 [`availableModels`](/docs/zh-CN/model-config#restrict-model-selection) 允许列表检查每次调用的参数、frontmatter 和环境变量值。对于被阻止的值，它替换另一个模型：

* 当被阻止的值是家族别名（例如 `opus`）时，Claude Code 在允许列表允许的该家族的最新版本上运行 subagent，遵循与 `/model` 相同的 [substitution rules and provider scope](/docs/zh-CN/model-config#restrict-model-selection)。在 v2.1.222 之前，Claude Code 也在继承的模型上为被阻止的家族别名运行 subagent。
* 对于任何其他被阻止的值，在该替换不运行的提供商上，或当允许列表允许该家族的没有版本时，Claude Code 改为在继承的模型上运行 subagent。如果您设置 `CLAUDE_CODE_SUBAGENT_MODEL`，Claude Code 首先尝试该模型，在这些相同的规则下。

在交互式会话中，Claude Code 显示一个警告，命名请求的模型和 subagent 运行的模型，对于任一替换。

要检查子代理运行在哪个模型上，请运行 [`/tasks`](/docs/zh-CN/commands)。Claude Code 会在子代理所在行显示模型名称，并在为该子代理设置了 [effort 级别](/docs/zh-CN/model-config#adjust-effort-level)时一并显示。需要 Claude Code v2.1.242 或更高版本。

每次调用的 `model` 参数也适用于 subagent 何时 [resumed or sent a follow-up message](#resume-subagents)，因此 subagent 保持在该模型上。在 v2.1.211 之前，恢复删除了每次调用的值，subagent 恢复到其定义的 `model` 字段或，没有一个，主对话的模型。

从 v2.1.198 开始，subagents 也继承主对话的 [extended thinking](/docs/zh-CN/model-config#extended-thinking) 配置：如果在您的会话中启用了思考，对于 subagent 也启用，如果关闭，则保持关闭。没有每个 subagent 的思考设置。在 v2.1.198 之前，subagents 运行时禁用了扩展思考，无论主对话的设置如何。

<h4 id="run-every-subagent-on-one-model">
  在一个模型上运行每个 subagent
</h4>

`CLAUDE_CODE_SUBAGENT_MODEL` 是一个默认值，因此 subagent 的定义或 Claude 传递的模型仍然优先于它。要将一个模型应用于每个 subagent、[teammate](/docs/zh-CN/agent-teams#specify-teammates-and-models) 和 [workflow agent](/docs/zh-CN/workflows)，也设置 `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` 为 `1`。需要 Claude Code v2.1.257 或更高版本。

* 如果您设置两个变量，subagents 在 `CLAUDE_CODE_SUBAGENT_MODEL` 中的模型上运行。
* 如果仅设置 `CLAUDE_CODE_SUBAGENT_MODEL_FORCE`，子代理将在主对话的模型上运行，但内置 Explore 子代理除外，它会在[内置子代理下为其列出的模型](#built-in-subagents)上运行。

例如，要在 Haiku 上运行每个 subagent，在 [settings file](/docs/zh-CN/settings) 的 `env` 块中设置两个变量：

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_SUBAGENT_MODEL": "haiku",
    "CLAUDE_CODE_SUBAGENT_MODEL_FORCE": "1"
  }
}
```

要检查设置是否生效，在 subagent 运行时运行 [`/tasks`](/docs/zh-CN/commands)。Subagent 的行显示它运行的模型。

当 `CLAUDE_CODE_SUBAGENT_MODEL_FORCE` [启用](/docs/zh-CN/env-vars)时，Claude Code 会忽略子代理定义中的 `model` 字段，Claude 在启动子代理时也无法传递模型。以下子代理仍在主对话的模型上运行：

* 一个 [fork](#fork-the-current-conversation)
* 一个 [skill that runs in a subagent](/docs/zh-CN/skills#run-skills-in-a-subagent)，带有 `model: inherit`

<h3 id="choose-an-effort-level">
  选择 effort 级别
</h3>

要让子代理以其自身的 [effort 级别](/docs/zh-CN/model-config#adjust-effort-level)运行，请在其定义中设置 [`effort`](#supported-frontmatter-fields) 字段。

当您要求 Claude 以特定 effort 级别运行非分叉子代理时，Claude 也可以为该次调用传递一个 `effort` 参数。该参数会覆盖 `effort` 字段，并在子代理被[恢复](#resume-subagents)时保持有效。[`CLAUDE_CODE_EFFORT_LEVEL`](/docs/zh-CN/env-vars#variables) 环境变量优先于这两者。每次调用的参数需要 Claude Code v2.1.292 或更高版本。

<h3 id="control-subagent-capabilities">
  控制 subagent 能力
</h3>

您可以通过工具访问、权限模式和条件规则来控制 subagents 可以做什么。

<h4 id="available-tools">
  可用工具
</h4>

Subagents 继承主对话中可用的 [built-in tools](/docs/zh-CN/tools-reference) 和 MCP 工具，由两个过滤器缩小：第一个从每个 subagent 删除工具的短列表，第二个为在 [background](#run-subagents-in-foreground-or-background) 中运行的 subagents 减少内置工具集，这是默认值。在 macOS、Linux 和 WSL 上，当主对话没有 Glob 和 Grep 工具时，subagent 也可以接收它们，如 [Glob tool behavior](/docs/zh-CN/tools-reference#glob-tool-behavior) 下所述。[Forks](#fork-the-current-conversation) 跳过两个过滤器并接收主对话的确切工具池。第一个过滤器删除这些工具，即使在 `tools` 字段中列出：

* `Agent`，当 subagent 在 [depth limit](#let-subagents-spawn-their-own-subagents)；在 [fork](#fork-the-current-conversation) 中工具保持列出但返回错误而不是生成
* `AskUserQuestion`
* `EndConversation`，只能结束主对话；请参阅 [EndConversation tool behavior](/docs/zh-CN/tools-reference#endconversation-tool-behavior)
* `EnterPlanMode`
* `ExitPlanMode`，除非 subagent 的 [`permissionMode`](#permission-modes) 是 `plan`
* `ScheduleWakeup`
* `WaitForMcpServers`
* `Workflow`

第二个过滤器适用于在后台运行的 subagents。除了 `Agent` 和 `ExitPlanMode`，它们遵循第一个过滤器的条件，无论 subagent 在哪里运行，后台 subagent 保留每个 MCP 工具但仅这些内置工具：`Read`、`Grep`、`Glob`、`LSP`、`Bash`、`PowerShell`、`Edit`、`Write`、`NotebookEdit`、`WebFetch`、`WebSearch`、`TodoWrite`、`Skill`、`ToolSearch`、`EnterWorktree`、`ExitWorktree`、`Monitor`、`TaskStop`、`SendMessage` 和 `Artifact`，加上 [`SubagentHandback`](/docs/zh-CN/tools-reference) 用于通过它报告的 subagent。Claude Code 从后台 subagent 删除每个其他内置工具，无论继承还是在 `tools` 字段中列出，因此相同的定义可以在前台和后台解析为不同的工具。删除报告没有错误，除非它使 `tools` 列表 [resolving to nothing](/docs/zh-CN/errors#agent-would-be-spawned-with-zero-tools)。

在 v2.1.280 之前，后台 subagents 无法使用 `LSP`。

[`ListAgents`](/docs/zh-CN/cross-session-messaging) 遵循这些过滤器，如任何内置工具：前台 subagent 在启用跨会话消息的会话中继承它，后台 subagent 不保留它。

[agent teams](/docs/zh-CN/agent-teams) 中的队友另外保留任务工具和 cron 工具：`TaskCreate`、`TaskGet`、`TaskList`、`TaskUpdate`、`CronCreate`、`CronDelete` 和 `CronList`。

在 [session without the Task tools](/docs/zh-CN/tools-reference#task-tool-availability) 中，Claude Code 也不向 subagents 提供任务工具，即使 subagent 运行不同的模型。进程内队友遵循您的会话相同的方式，而在其自己的 [split pane](/docs/zh-CN/agent-teams#choose-a-display-mode) 中的队友作为单独的 Claude Code 进程运行，因此其自己的模型决定。

要限制工具，使用 `tools` 字段作为允许列表或 `disallowedTools` 字段作为拒绝列表。此示例使用 `tools` 来仅允许 Read、Grep、Glob 和 Bash。Subagent 无法编辑文件、写入文件或使用任何 MCP 工具：

```yaml theme={null}
---
name: safe-researcher
description: Research agent with restricted capabilities
tools: Read, Grep, Glob, Bash
---
```

此示例使用 `disallowedTools` 来继承 subagent 的工具池，除了 Write 和 Edit。Subagent 保留 Bash、MCP 工具和其他所有内容：

```yaml theme={null}
---
name: no-writes
description: Inherits the available tools except file writes
disallowedTools: Write, Edit
---
```

如果两者都设置，`disallowedTools` 首先应用，然后 `tools` 针对剩余的池进行解析。同时列在两者中的工具被删除。

当 `tools` 列表中没有任何内容解析为工具时，例如因为每个条目都拼写错误或命名了对 subagents 不可用的工具，Claude Code 通常拒绝启动 subagent，Agent 工具返回一个错误，命名未解析的条目；请参阅 [Agent would be spawned with zero tools](/docs/zh-CN/errors#agent-would-be-spawned-with-zero-tools) 了解消息和如何修复每个条目。在 v2.1.208 之前，该 subagent 启动时没有工具，可能返回空的或令人困惑的结果。

除了精确的工具名称之外，两个字段还接受 MCP 服务器级别的模式：`mcp__<server>` 或 `mcp__<server>__*` 授予或删除来自命名服务器的每个工具。在 `disallowedTools` 中，`mcp__*` 也删除来自任何服务器的每个 MCP 工具。此示例删除来自 `github` MCP 服务器的每个工具，同时保留来自其他服务器的工具和其池中的内置工具：

```yaml theme={null}
---
name: local-only
description: Inherits every tool except those from the github MCP server
disallowedTools: mcp__github
---
```

一个 `disallowedTools` 条目带有说明符，例如 `Bash(git push *)`，仍然从 subagent 删除整个工具，而不仅仅是匹配的命令。要保留 Bash 并阻止特定命令，请在您的设置中向 `permissions.deny` 添加 [Bash deny rule](/docs/zh-CN/permissions#bash)，例如 `Bash(git push *)`。该规则适用于主对话和 subagents。

<h4 id="restrict-which-subagents-can-be-spawned">
  限制可以生成哪些 subagents
</h4>

当代理作为主线程运行时，使用 `claude --agent`，它可以使用 Agent 工具生成 subagents。要限制它可以生成的 subagent 类型，在 `tools` 字段中使用 `Agent(agent_type)` 语法。

<Note>在版本 2.1.63 中，Task 工具被重命名为 Agent。设置和代理定义中的现有 `Task(...)` 引用仍然作为别名工作。</Note>

```yaml theme={null}
---
name: coordinator
description: Coordinates work across specialized agents
tools: Agent(worker, researcher), Read, Bash
---
```

这是一个允许列表：只有 `worker` 和 `researcher` subagents 可以被生成。如果代理尝试生成任何其他类型，请求失败，代理在其提示中仅看到允许的类型。要在允许所有其他类型的同时阻止特定代理，请改用 [`permissions.deny`](#disable-specific-subagents)。

要允许生成任何 subagent 而不受限制，使用不带括号的 `Agent`：

```yaml theme={null}
tools: Agent, Read, Bash
```

如果 `Agent` 完全从 `tools` 列表中省略，代理无法生成任何 subagents。

`Agent(agent_type)` 允许列表语法仅适用于作为主线程运行的代理，使用 `claude --agent`。在 subagent 定义中，在 `tools` 中列出 `Agent` 让该 subagent 生成自己的 subagents，同时 [depth limit](#let-subagents-spawn-their-own-subagents) 允许它，但括号内的任何类型列表都被忽略。

<h4 id="scope-mcp-servers-to-a-subagent">
  将 MCP 服务器限定于 subagent
</h4>

使用 `mcpServers` 字段为 subagent 提供对主对话中不可用的 [MCP](/docs/zh-CN/mcp) 服务器的访问。此处定义的内联服务器在 subagent 启动时连接，受 [trust rule for the agent file's folder](#inline-server-trust) 约束，并在完成时断开连接。字符串引用共享父会话的连接。

<Note>
  `mcpServers` 字段适用于代理文件可以运行的两个上下文：

  * 作为 subagent，通过 Agent 工具或 @-mention 生成
  * 作为主会话，使用 [`--agent`](#invoke-subagents-explicitly) 或 `agent` 设置启动

  当代理是主会话时，内联服务器定义与来自 [`.mcp.json`](/docs/zh-CN/mcp) 和设置文件的服务器一起在启动时连接，在 [trust rule for the agent file's folder](#inline-server-trust) 下。在 `/mcp` 中，您之前使用过的远程（HTTP 或 SSE）服务器可以显示 [`cached` status](/docs/zh-CN/mcp#managing-your-servers) 而不是；Claude Code 在 Claude 首次调用其工具之一时连接它。
</Note>

列表中的每个条目要么是内联服务器定义，要么是引用会话中已配置的 MCP 服务器的字符串：

```yaml theme={null}
---
name: browser-tester
description: Tests features in a real browser using Playwright
mcpServers:
  # Inline definition: scoped to this subagent only
  - playwright:
      type: stdio
      command: npx
      args: ["-y", "@playwright/mcp@latest"]
  # Reference by name: reuses an already-configured server
  - github
---

Use the Playwright tools to navigate, screenshot, and interact with pages.
```

内联定义使用与 `.mcp.json` 服务器条目相同的架构，由服务器名称键入，并支持 `stdio`、`http`、`sse` 和 `ws` 类型。

要将 MCP 服务器保持在主对话之外，并避免其工具描述消耗那里的上下文，请在此处内联定义它，而不是在 `.mcp.json` 中。Subagent 获得工具；父对话不获得。

适用于主会话的 MCP 限制同样涵盖子代理 frontmatter 中声明的服务器：

* [`--strict-mcp-config`](/docs/zh-CN/cli-reference) 和 [`--bare`](/docs/zh-CN/cli-reference)
* [企业托管 MCP 配置](/docs/zh-CN/managed-mcp)
* [`allowedMcpServers` 和 `deniedMcpServers` 策略](/docs/zh-CN/managed-mcp#policy-based-control-with-allowlists-and-denylists)

当其中任一项阻止某个服务器时，Claude Code 会跳过它，并显示一条列出被阻止服务器的警告。

托管设置限制适用于每个子代理，无论其如何定义。`--strict-mcp-config` 不会过滤您通过 `--agents` 或 SDK `agents` 选项内联传递的服务器，因为这些属于调用方的显式输入。

<h4 id="inline-server-trust">
  内联 MCP 服务器需要信任
</h4>

只有在您[信任 Agent 文件所在的文件夹](/docs/zh-CN/permissions#what-runs-before-you-trust-a-folder)之后，Claude Code 才会从项目 `.claude/agents/` 目录或 `--add-dir` 目录的 `.claude/agents/` 中的 Agent 文件加载[内联 MCP 服务器](#scope-mcp-servers-to-a-subagent)。在 v2.1.238 之前，Claude Code 加载这些服务器时不检查信任。

* **不计数的信任**：父文件夹的信任，以及 `-p` 或 SDK 会话为 [hooks in settings files](/docs/zh-CN/permissions#what-runs-before-you-trust-a-folder) 获得的自动信任
* **直到那时**：Claude Code 跳过该代理文件中的每个内联服务器，并将确切的 `projects["<path>"].hasTrustDialogAccepted` 键写入调试日志，用于 `~/.claude.json`
* **`--add-dir` 目录**：您受信任工作区的存储库外的目录需要其自己的信任条目，因为其 `.claude/agents/` 文件不继承您的工作区的信任

Claude Code 加载两种服务器而不检查代理文件来自的文件夹的信任：

* 一个引用您已配置的服务器的名称
* 一个代理文件中的内联服务器，来自 `~/.claude/agents/`，在您使用 `--agents` 或 SDK `agents` 选项传递的一个中，或托管设置提供的一个中

<h4 id="permission-modes">
  权限模式
</h4>

设置 `permissionMode` 以选择 subagent 运行的权限模式。使用模式的配置值，因此手动模式是 `default`。如果您不设置它，subagent 继承主对话的 [permission mode](/docs/zh-CN/permission-modes)。

主对话的权限模式决定 Claude Code 是否使用您设置的值：

* 当主对话在 `bypassPermissions`、`acceptEdits` 或 [auto mode](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode) 时，subagent 在该相同模式中运行，Claude Code 忽略您设置的 `permissionMode`。在自动模式下，分类器使用主对话的块和允许规则评估 subagent 的工具调用。当 subagent 完成时，分类器也会在报告被传递之前审查其工作和最终报告，如 [How auto mode handles subagents](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode) 所述。
* 当主对话处于 `default`、`dontAsk` 或 `plan` 模式时，子代理会在您设置的权限模式下运行。在以下情况下，它会改为保持主对话的权限模式：
  * 您设置了 `bypassPermissions`。`bypassPermissions` 例外需要 Claude Code v2.1.267 或更高版本。
  * 您设置了 `auto`，但子代理[无法使用自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)，例如某个设置文件设置了 [`disableAutoMode`](/docs/zh-CN/settings-reference#disableautomode)，或子代理的模型不支持自动模式。

`permissionMode` 接受这些值，以及 `manual` 作为 `default` 的别名：

| Mode | Behavior |
| :- | :- |
| `default` | 手动模式：提示权限 |
| `acceptEdits` | 自动接受文件编辑和工作目录或 `additionalDirectories` 中路径的常见文件系统命令 |
| `auto` | [Auto mode](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)：后台分类器审查命令和受保护目录的写入 |
| `dontAsk` | 自动拒绝权限提示。显式允许的工具仍然工作；`AskUserQuestion`、标记为 [`requiresUserInteraction`](/docs/zh-CN/mcp#require-approval-for-a-specific-tool) 的 MCP 工具，以及[您的组织设置为 `ask`](/docs/zh-CN/mcp#organization-controls-on-connector-tools) 的连接器工具（在该设置到达 Claude Code 的会话中）会被拒绝，即使您已允许它们 |
| `bypassPermissions` | [Skip permission prompts](/docs/zh-CN/permission-modes#skip-all-checks-with-bypasspermissions-mode)。Subagent 仅在主对话也这样做时在此模式中运行 |
| `plan` | Plan mode（只读探索） |

<h4 id="preload-skills-into-subagents">
  将技能预加载到 subagents
</h4>

使用 `skills` 字段在启动时将技能内容注入到 subagent 的上下文中。这为 subagent 提供领域知识，而无需在执行期间发现和加载技能。

```yaml theme={null}
---
name: api-developer
description: Implement API endpoints following team conventions
skills:
  - api-conventions
  - error-handling-patterns
---

Implement API endpoints. Follow the conventions and patterns from the preloaded skills.
```

每个列出的技能的完整内容被注入到 subagent 的上下文中。此字段控制哪些技能被预加载，而不是 subagent 可以访问哪些技能：没有它，subagent 仍然可以在执行期间通过 Skill 工具发现和调用项目、用户和 plugin 技能。要防止 subagent 完全调用技能，请从 [`tools`](#available-tools) 列表中省略 `Skill` 或将其添加到 `disallowedTools`。

您无法预加载设置了 [`disable-model-invocation: true`](/docs/zh-CN/skills#control-who-invokes-a-skill) 的 skill，因为预加载的来源与 Claude 可以调用的 skill 集合相同。这包括内置的 `/verify` skill，Claude 无法自行运行它。

如果列出的技能缺失或被禁用，例如由您的组织的策略，Claude Code 会跳过它并向调试日志记录警告。

<Note>
  这与 [running a skill in a subagent](/docs/zh-CN/skills#run-skills-in-a-subagent) 相反。使用 subagent 中的 `skills`，subagent 控制系统提示并加载技能内容。使用技能中的 `context: fork`，技能内容被注入到您指定的代理中。两者都使用相同的底层系统。
</Note>

<h4 id="enable-persistent-memory">
  启用持久内存
</h4>

`memory` 字段为 subagent 提供一个在对话中幸存的持久目录。Subagent 使用此目录随时间积累知识，例如代码库模式、调试见解和架构决策。

```yaml theme={null}
---
name: code-reviewer
description: Reviews code for quality and best practices
memory: user
---

You are a code reviewer. As you review code, update your agent memory with
patterns, conventions, and recurring issues you discover.
```

根据内存应该应用的广泛程度选择范围：

| Scope | Location | 使用时机 |
| :- | :- | :- |
| `user` | `~/.claude/agent-memory/<name-of-agent>/` | subagent 应该在所有项目中记住学习 |
| `project` | `.claude/agent-memory/<name-of-agent>/` | subagent 的知识是特定于项目的并可通过版本控制共享 |
| `local` | `.claude/agent-memory-local/<name-of-agent>/` | subagent 的知识是特定于项目的但不应检入版本控制 |

Subagent 内存是 [auto memory](/docs/zh-CN/memory#auto-memory) 的一部分：如果您关闭自动内存，使用 `autoMemoryEnabled` 设置或 `CLAUDE_CODE_DISABLE_AUTO_MEMORY`，`memory` 字段没有效果，subagent 启动时没有内存说明或下面描述的内存工具访问。

启用内存时：

* Subagent 的系统提示包括读取和写入内存目录的说明。
* Subagent 的系统提示还包括内存目录中 `MEMORY.md` 的前 200 行或 25KB，以先到者为准，以及如果 `MEMORY.md` 超过该限制则策划 `MEMORY.md` 的说明。
* Read、Write 和 Edit 工具会自动启用，以便 subagent 可以管理其内存文件。

<h5 id="persistent-memory-tips">
  持久内存提示
</h5>

* `project` 是推荐的默认范围。它使 subagent 知识可通过版本控制共享。
* 要求 subagent 在开始工作前查阅其内存："Review this PR, and check your memory for patterns you've seen before."
* 要求 subagent 在完成任务后更新其内存："Now that you're done, save what you learned to your memory." 随着时间的推移，这会建立一个知识库，使 subagent 更有效。
* 直接在 subagent 的 markdown 文件中包含内存说明，以便它主动维护自己的知识库：

  ```markdown theme={null}
  Update your agent memory as you discover codepaths, patterns, library
  locations, and key architectural decisions. This builds up institutional
  knowledge across conversations. Write concise notes about what you found
  and where.
  ```

<h4 id="conditional-rules-with-hooks">
  使用 hooks 的条件规则
</h4>

为了更动态地控制工具使用，使用 `PreToolUse` hooks 在执行前验证操作。当您需要允许工具的某些操作同时阻止其他操作时，这很有用。

此示例创建一个仅允许只读数据库查询的 subagent。`PreToolUse` hook 在每个 Bash 命令执行前运行 `command` 中指定的脚本：

```yaml theme={null}
---
name: db-reader
description: Execute read-only database queries
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---
```

Claude Code [通过 stdin 将 hook 输入作为 JSON 传递](/docs/zh-CN/hooks#pretooluse-input) 给 hook 命令。验证脚本读取此 JSON，提取 Bash 命令，并 [以代码 2 退出](/docs/zh-CN/hooks#exit-code-2-behavior-per-event) 以阻止写入操作：

```bash theme={null}
#!/bin/bash
# ./scripts/validate-readonly-query.sh

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Block SQL write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE)\b' > /dev/null; then
  echo "Blocked: Only SELECT queries are allowed" >&2
  exit 2
fi

exit 0
```

在 macOS 和 Linux 上，使脚本可执行，否则 hook 失败而不是阻止任何内容：

```bash theme={null}
chmod +x ./scripts/validate-readonly-query.sh
```

要测试规则，要求 subagent 运行 `UPDATE` 语句：脚本以代码 2 退出，Claude Code 阻止命令，subagent 看到 `Blocked: Only SELECT queries are allowed` 消息。

有关完整的输入架构，请参阅 [Hook input](/docs/zh-CN/hooks#pretooluse-input)，有关退出代码如何影响行为，请参阅 [exit codes](/docs/zh-CN/hooks#exit-code-output)。在 Windows 上，在 PowerShell 中编写 hook 脚本，并在 hook 条目中添加 `shell: powershell`，如 [running hooks in PowerShell](/docs/zh-CN/hooks#windows-powershell-tool) 中所示。

<h4 id="disable-specific-subagents">
  禁用特定 subagents
</h4>

您可以通过将 subagents 添加到您的 [settings](/docs/zh-CN/settings-reference#permission-settings) 中的 `deny` 数组来防止 Claude 使用特定 subagents。使用格式 `Agent(subagent-name)`，其中 `subagent-name` 与 subagent 的 name 字段匹配。

```json theme={null}
{
  "permissions": {
    "deny": ["Agent(Explore)", "Agent(my-custom-agent)"]
  }
}
```

这对内置和自定义 subagents 都有效。您也可以使用 `--disallowedTools` CLI 标志：

```bash theme={null}
claude --disallowedTools "Agent(Explore)"
```

有关权限规则的更多详细信息，请参阅 [Permissions documentation](/docs/zh-CN/permissions#tool-specific-permission-rules)。

<h3 id="define-hooks-for-subagents">
  为 subagents 定义 hooks
</h3>

Subagents 可以定义在 subagent 的生命周期中运行的 [hooks](/docs/zh-CN/hooks)。有两种方式来配置 hooks：

* **在 subagent 的 frontmatter 中**：定义仅在该 subagent 活跃时运行的 hooks
* **在 `settings.json` 中**：定义会话范围的 hooks，也在 subagents 内部触发。工具事件，例如 `PreToolUse` 和 `PostToolUse`，为 subagent 的工具调用触发，与它们在主对话中的方式相同，`SubagentStart` 和 `SubagentStop` 在 subagent 启动或完成时触发

来自 [settings files, managed policy settings, and plugins](/docs/zh-CN/hooks#hook-locations) 的 Hooks 都适用于 subagents 内部，因此 `settings.json` 中的 `PreToolUse` hook 也在 subagent 使用的每个工具之前运行。

<h4 id="hooks-in-subagent-frontmatter">
  Subagent frontmatter 中的 Hooks
</h4>

直接在 subagent 的 markdown 文件中定义 hooks。这些 hooks 仅在该特定 subagent 活跃时运行，并在完成时清理。

<Note>
  Frontmatter hooks 在代理通过 Agent 工具或 @-mention 作为 subagent 生成时触发，以及当代理通过 [`--agent`](#invoke-subagents-explicitly) 或 `agent` 设置作为主会话运行时触发。在主会话情况下，它们与在 [`settings.json`](/docs/zh-CN/hooks) 中定义的任何 hooks 一起运行。
</Note>

要让项目级 subagent 的 frontmatter hooks 运行，接受包含代理文件的文件夹的 [workspace trust dialog](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust)。来自 `~/.claude/agents/` 中的用户级 subagents 的 Hooks 和来自您使用 `--agents` 传递的定义的 Hooks 无需此步骤即可运行。如果您从受信任工作区的存储库外使用 `--add-dir` 添加了文件夹，单独信任该文件夹：其 `.claude/agents/` hooks 不继承工作区的授予。

直到您信任文件夹，subagent 仍然运行，但 Claude Code 跳过其 frontmatter hooks 并向调试日志记录错误，解释如何信任文件夹。这是比 settings 文件中的 hooks 的规则更严格的规则：信任父文件夹不够，`-p` 会话不计为受信任。[What runs before you trust a folder](/docs/zh-CN/permissions#what-runs-before-you-trust-a-folder) 比较两者。在 v2.1.218 之前，frontmatter hooks 可以从您未信任的文件夹运行，包括在非交互式会话中。

所有 [hook events](/docs/zh-CN/hooks#hook-events) 都被支持。subagents 最常见的事件是：

| Event | Matcher input | 何时触发 |
| :- | :- | :- |
| `PreToolUse` | Tool name | 在 subagent 使用工具之前 |
| `PostToolUse` | Tool name | 在 subagent 使用工具之后 |
| `Stop` | (none) | 当 subagent 完成时（在运行时转换为 `SubagentStop`） |

此示例使用 `PreToolUse` hook 验证 Bash 命令，并在文件编辑后使用 `PostToolUse` 运行 linter：

```yaml theme={null}
---
name: code-reviewer
description: Review code changes with automatic linting
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-command.sh"
  PostToolUse:
    - matcher: "Edit|Write"
      hooks:
        - type: command
          command: "./scripts/run-linter.sh"
---
```

当代理作为 subagent 调用时，frontmatter 中的 `Stop` hooks 会自动转换为 `SubagentStop` 事件。

<h4 id="project-level-hooks-for-subagent-events">
  用于 subagent 事件的项目级 hooks
</h4>

在 `settings.json` 中配置 hooks，以响应主会话中的 subagent 生命周期事件。

| Event | Matcher input | 何时触发 |
| :- | :- | :- |
| `SubagentStart` | Agent type name | 当 subagent 开始执行时 |
| `SubagentStop` | Agent type name | 当 subagent 完成时 |

两个事件都支持匹配器以按名称针对特定代理类型。匹配器值是项目级和用户级 subagents 的代理 frontmatter `name`，或 [plugin subagents](/docs/zh-CN/plugins/components#agents) 的 plugin 范围标识符，例如 `my-plugin:db-agent`。范围名称包含冒号，因此它被评估为 [unanchored regular expression](/docs/zh-CN/hooks#matcher-patterns)；使用 `^` 和 `$` 锚定它，如 `^my-plugin:db-agent$`，以仅匹配该代理。

此示例仅在 `db-agent` subagent 启动时运行设置脚本，并在任何 subagent 停止时运行清理脚本：

```json theme={null}
{
  "hooks": {
    "SubagentStart": [
      {
        "matcher": "db-agent",
        "hooks": [
          { "type": "command", "command": "./scripts/setup-db-connection.sh" }
        ]
      }
    ],
    "SubagentStop": [
      {
        "hooks": [
          { "type": "command", "command": "./scripts/cleanup-db-connection.sh" }
        ]
      }
    ]
  }
}
```

有关完整的 hook 配置格式，请参阅 [Hooks](/docs/zh-CN/hooks)。

<h2 id="work-with-subagents">
  使用子代理
</h2>

<h3 id="understand-automatic-delegation">
  理解自动委托
</h3>

Claude 根据您请求中的任务描述、子代理配置中的 `description` 字段以及当前上下文自动委托任务。要鼓励主动委托，请在子代理的 description 字段中包含"use proactively"之类的短语。

请保持描述简洁：当您的子代理描述总和超过 [15,000 token 限制](/docs/zh-CN/errors#agent-descriptions-are-over-the-15000-token-limit)时，Claude Code 会显示启动警告，但仍会加载每个子代理。

如果子代理由[插件](/docs/zh-CN/plugins/overview)提供，您可以在一组贴近实际的提示词上衡量 Claude 委托给它的可靠程度，而无需逐个检查：[`claude plugin eval`](/docs/zh-CN/plugin-evals) 会在启用和不启用该插件的情况下分别运行每个提示词，并对结果进行评分。

<h3 id="invoke-subagents-explicitly">
  显式调用子代理
</h3>

当自动委托不够用时，您可以自行请求使用子代理。以下三种模式从一次性建议逐步升级到整个会话的默认设置：

* **自然语言**：在提示词中点名子代理；由 Claude 决定是否委托
* **@-mention**：保证该子代理为某一个任务运行
* **会话范围**：通过 `--agent` 标志或 `agent` 设置，让整个会话以该子代理的身份运行

使用自然语言时没有特殊语法。点名子代理，Claude 通常就会委托：

```text wrap theme={null}
Use the test-runner subagent to fix failing tests
Have the code-reviewer subagent look at my recent changes
```

**@-mention 子代理。** 输入 `@` 并从自动补全列表中选择子代理，方式与 @-mention 文件相同。这可以确保运行指定的子代理，而不是将选择权交给 Claude：

```text wrap theme={null}
@"code-reviewer (agent)" look at the auth changes
```

您的完整消息仍会发送给 Claude，由 Claude 根据您的要求为子代理编写任务提示词。@-mention 控制的是 Claude 调用哪个子代理，而不是子代理收到什么提示词。

已启用[插件](/docs/zh-CN/plugins/overview)提供的子代理会以其作用域名称显示在自动补全列表中，例如 `my-plugin:code-reviewer`；当插件[将 Agent 组织到子文件夹中](#choose-the-subagent-scope)时，则显示为 `my-plugin:review:security` 这样的名称。当前在会话中运行的已命名后台子代理也会出现在自动补全列表中，并在名称旁显示其状态。

您也可以不使用选择器而手动输入提及：本地子代理使用 `@agent-<name>`，插件子代理使用 `@agent-` 后跟作用域名称，例如 `@agent-my-plugin:code-reviewer`。输入这种形式时，自动补全列表显示的是匹配的文件而不是 Agent，但提交时该 Agent 提及仍会被正确解析。

**以子代理身份运行整个会话。** 传递 [`--agent <name>`](/docs/zh-CN/cli-reference) 可启动一个会话，让主线程本身采用该子代理的工具限制和模型：

```bash theme={null}
claude --agent code-reviewer
```

除非该 Agent 的[提示词为空](#choose-the-subagent-scope)，否则自定义子代理的系统提示词会完全替换默认的 Claude Code 系统提示词，效果与 [`--system-prompt`](/docs/zh-CN/cli-reference) 相同。`CLAUDE.md` 文件和项目记忆仍会通过正常的消息流加载，即使该 Agent 的定义设置了 [`omitClaudeMd`](#supported-frontmatter-fields) 也是如此。

Agent 名称会以 `@<name>` 的形式显示在启动标题中，方便您确认其已生效。

这适用于内置和自定义子代理，并且在恢复会话时该选择会保留：Claude Code 会随对话一起恢复该 Agent 的工具限制和模型。如果恢复时该 Agent 已不存在，会话将使用默认工具继续，并显示一条[指明该 Agent 的警告](/docs/zh-CN/errors#session-agent-no-longer-available)。关于这两种情况下的系统提示词，请参阅[已恢复对话中的系统提示词标志](/docs/zh-CN/cli-reference#system-prompt-flags-in-resumed-conversations)。

对于插件提供的子代理，您可以只传递 Agent 名称，Claude Code 会自行找到它：

```bash theme={null}
claude --agent security-reviewer
```

如果多个插件提供了同名的 Agent，请传递作用域名称以消除歧义：

```bash theme={null}
claude --agent my-plugin:security-reviewer
```

如果插件将 Agent 放在其 `agents/` 目录的子文件夹中，请在作用域名称中包含该子文件夹，例如 `claude --agent my-plugin:review:security`。

要使其成为项目中每个会话的默认值，请在 `.claude/settings.json` 中设置 `agent`：

```json theme={null}
{
  "agent": "code-reviewer"
}
```

如果两者同时存在，CLI 标志会覆盖该设置。

<h3 id="run-subagents-in-foreground-or-background">
  在前台或后台运行子代理
</h3>

子代理可以在前台或后台运行：

* **前台子代理**会阻塞主对话直到完成。权限提示会在出现时传递给您。
* **后台子代理**在您继续工作时并发运行。当后台子代理遇到需要权限的工具调用时，Claude Code 会在您的主会话中显示该提示，并指明发出请求的子代理。批准即可让子代理继续；按 Esc 则拒绝该单个工具调用，而不会停止子代理。

对于 Claude 使用 Agent 工具生成的每个子代理，Claude Code 会按以下情况中第一个适用的情况来决定前台还是后台：

* 如果是进程内的 [agent team](/docs/zh-CN/agent-teams#limitations) 队友生成了该子代理，Claude Code 会在前台运行它。如果队友要生成的子代理的定义设置了 [`background: true`](#supported-frontmatter-fields)，Claude Code 会拒绝并报错。在 [fork 模式](#turn-fork-mode-on-or-off)关闭且您未[关闭后台任务](/docs/zh-CN/env-vars)的情况下，如果队友设置了 `run_in_background: true`，Claude Code 也会拒绝并报错。
* 如果您将 [`CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`](/docs/zh-CN/env-vars) 设置为 `1`，Claude Code 会在前台运行子代理，适用于所有类型的会话，且无论 fork 模式是否开启。
* 当 [fork 模式](#turn-fork-mode-on-or-off)开启时（交互式会话中默认开启），Claude Code 会在后台运行子代理，fork 和非 fork 子代理都是如此，且 Claude 无法要求在前台运行。
* 当 fork 模式关闭时，Claude 默认在后台运行子代理，并在需要先拿到结果才能继续时在前台运行。在使用 `-p` 的[非交互模式](/docs/zh-CN/headless)和 Agent SDK 中，fork 模式默认关闭，除非您将其开启。要让某个子代理即使在 Claude 需要其结果时也保持在后台运行，请将其 frontmatter 中的 [`background`](#supported-frontmatter-fields) 字段设置为 `true`。

对于带有 `context: fork` 的 skill，Claude Code 改为遵循[在子代理中运行 skill](/docs/zh-CN/skills#run-skills-in-a-subagent) 中的规则，无论 fork 模式是否开启。

后台子代理使用的[内置工具集](#available-tools)比前台子代理更小，但对话 fork 和[已恢复](#resume-subagents)的前台子代理除外。

后台子代理会在您的主会话中显示每一个权限提示。当您对其中某个提示所作的选择会在该次工具调用之后继续生效（例如在会话剩余时间内持续有效的授予）时，Claude Code 会将您的答复应用于整个会话，包括您的主对话。

后台子代理可以让后台 [Bash 或 PowerShell 命令](/docs/zh-CN/tools-reference#background-commands)[在其轮次结束后继续运行](/docs/zh-CN/interactive-mode#how-backgrounding-works)。该命令结束时，Claude Code 会向该子代理发送通知。

后台子代理的结果会在之后的某个轮次中以完成通知的形式送达 Claude。Claude 会等待该通知后再报告子代理的结果；如果您先询问进度，它会告知子代理仍在运行。在 v2.1.211 之前，Claude 有时会报告尚未完成的后台子代理的结果。

您也可以自行控制：

* 当 fork 模式关闭时，要求 Claude 在后台或前台运行任务
* 按 **Ctrl+B** 将正在运行的任务转到后台

Claude Code 会以两种方式之一从输入框下方的子代理面板中清除后台子代理所在的行，具体取决于子代理的结束方式：

* 当子代理成功完成时，Claude Code 会立即移除其所在行，并在页脚显示 `/tasks to see subagents` 30 秒（[屏幕阅读器模式](/docs/zh-CN/accessibility)下除外）。在这 30 秒内，运行 [`/tasks`](/docs/zh-CN/commands) 并在该子代理上按 `Enter` 即可打开其会话记录。在 v2.1.232 之前，Claude Code 会在子代理完成后将该行保留 30 秒（与失败的子代理相同），且不显示页脚提示。
* 当子代理失败或被您停止时，Claude Code 会将其所在行保留 30 秒。要更早清除该行，请选中它并按 `x`。

已完成的后台子代理会继续列在 [`/tasks`](/docs/zh-CN/commands) 中，标记为已完成并排在正在运行的工作下方，持续时间与页脚提示相同，为 30 秒。子代理完成时，其详情视图保持打开。失败或被您停止的子代理会从列表中移除。在 v2.1.208 之前，已完成的子代理会在完成的那一刻离开列表，其详情视图也会关闭。

<h3 id="subagent-names">
  子代理名称
</h3>

Claude 可以在 Agent 工具调用中传递 `name` 参数来为子代理命名，并且可能会自行这样做，而不事先询问您。名称使子代理可被寻址：在子代理完成后，Claude 可以[按名称向其发送消息或恢复它](#resume-subagents)。

在启用了 [agent teams](/docs/zh-CN/agent-teams) 的交互式会话中，Claude 从主对话生成的带有 `name` 的子代理会改为以队友身份启动，除非该调用是 [fork](#fork-the-current-conversation) 或在调用本身中传递了 `isolation`。子代理 frontmatter 中的 `isolation` 值无法阻止这一点，此时该队友会在主会话的工作目录中运行。请参阅 [Claude 如何启动 agent teams](/docs/zh-CN/agent-teams#how-claude-starts-agent-teams)。

<h3 id="api-errors-in-subagents">
  子代理中的 API 错误
</h3>

当某种原因[在流式传输中途截断了子代理的响应](/docs/zh-CN/errors#the-response-above-may-be-incomplete)，且部分响应包含文本但没有工具调用时，Claude Code 会提示子代理继续，而不是结束运行。这在交互式会话中同样适用。只有当这些继续次数用完后，运行才会因该错误而结束。

因 API 错误（例如用量限制或反复出现的服务器错误）而结束运行的子代理会将该失败报告给 Claude。Claude 收到的内容取决于子代理的运行位置：

* **前台**：如果速率限制、过载或服务器错误截断了已经产生文本输出的子代理，Agent 工具会返回该部分输出，并附注说明子代理被截断、未完成其任务。未产生任何输出、或输出仅包含工具调用的子代理会以 [`Agent terminated early due to an API error`](/docs/zh-CN/errors#agent-terminated-early-due-to-an-api-error) 失败，后跟错误详情。
* **后台**：子代理会被标记为失败，Claude 在其结束时收到的消息会指明该 API 错误，并包含子代理的最后输出，因此部分工作不会丢失。

当您配置了[备用模型链](/docs/zh-CN/model-config#fallback-model-chains)，且子代理遇到该链所覆盖的失败（例如其模型不可用）时，Claude Code 会将子代理切换到链中第一个接受请求的模型。子代理会继续工作，而不是因错误而结束。

底层 API 错误消除后，请让 Claude 重试该任务或[恢复子代理](#resume-subagents)。

<h3 id="subagent-output-scanning">
  子代理输出扫描
</h3>

Claude Code 会在 Claude 读取每个子代理的最终报告之前对其进行扫描。子代理可能读取过您从未审查过的文件、网页或命令输出，而这些来源中的文本可能携带针对主对话的指令。扫描从不删除或改写任何内容；它会做出两种您可能在报告中注意到的更改：

* **插入反斜杠**：扫描会在模仿 Claude Code 自身输出的文本中插入反斜杠，例如 `<system-reminder>` 标签，或以 `Human:` 或 `Assistant:` 开头的行，使这些模仿内容被当作普通文本读取，而不会被误认为是对话的一部分。
* **标记行**：当报告模仿了 `<system-reminder>` 之类的标签，或提及 `bypassPermissions` 或 `--dangerously-skip-permissions` 等权限设置时，扫描会在开头添加一行以 `[harness: subagent output matched instruction-shaped pattern(s):` 开头的内容。提及权限设置的报告会获得标记行，但文本本身保持原样。

扫描不会判断内容是否恶意，也不会改变报告中的指令所能产生的效果：报告促使 Claude 发起的工具调用仍然要经过会话的[权限检查](/docs/zh-CN/permissions)和[沙箱隔离](/docs/zh-CN/sandboxing)。它不能替代[限制子代理可访问的范围](#control-subagent-capabilities)。

作为子代理结果返回给 Claude 的报告还会带有一个标题，将其标记为子代理输出。该标题说明报告中的指令或批准声明是子代理的话语，并不具备来自您的任何权威。

[后台子代理的报告](#run-subagents-in-foreground-or-background)会包含在完成通知中送达，该通知被标记为自动化事件，而不是来自您的消息。

<Note>
  子代理输出扫描需要 Claude Code v2.1.210 或更高版本。
</Note>

<h3 id="common-patterns">
  常见模式
</h3>

<h4 id="isolate-high-volume-operations">
  隔离高输出量操作
</h4>

子代理最有效的用途之一是隔离会产生大量输出的操作。运行测试、获取文档或处理日志文件可能会消耗大量上下文。将这些操作委托给子代理后，冗长的输出会留在子代理的上下文中，只有相关摘要会返回到您的主对话。

```text wrap theme={null}
Use a subagent to run the test suite and report only the failing tests with their error messages
```

<h4 id="run-parallel-research">
  并行研究
</h4>

对于相互独立的调查，可以生成多个子代理同时工作：

```text wrap theme={null}
Research the authentication, database, and API modules in parallel using separate subagents
```

每个子代理独立探索各自的领域，然后由 Claude 综合这些发现。当各条研究路径互不依赖时，这种方式效果最好。

<Warning>
  子代理完成后，其结果会返回到您的主对话。运行许多各自返回详细结果的子代理可能会消耗大量上下文，而且每个子代理在运行时也会消耗自己的 token。
</Warning>

对于需要持续并行运行或无法容纳在一个上下文窗口中的工作，请在[单独的会话](/docs/zh-CN/agents)中运行，并让 Claude [在会话之间传递发现](/docs/zh-CN/cross-session-messaging)。

<h4 id="chain-subagents">
  串联子代理
</h4>

对于多步骤工作流，可以要求 Claude 依次使用多个子代理。每个子代理完成其任务后将结果返回给 Claude，再由 Claude 将相关上下文传递给下一个子代理。

```text wrap theme={null}
Use the code-reviewer subagent to find performance issues, then use the optimizer subagent to fix them
```

<h3 id="choose-between-subagents-and-main-conversation">
  在子代理和主对话之间选择
</h3>

在以下情况下使用**主对话**：

* 任务需要频繁来回交流或迭代完善
* 多个阶段（例如规划、实现和测试）共享大量上下文
* 您要进行快速、有针对性的更改
* 延迟很重要。非 [fork](#fork-the-current-conversation) 的子代理从零开始，可能需要时间来收集上下文

在以下情况下使用**子代理**：

* 任务会产生您在主上下文中不需要的冗长输出
* 您想强制执行特定的工具限制或权限
* 工作是自成一体的，可以返回一份摘要

如果您想要可复用的提示词或工作流，并希望它们在主对话上下文中而不是隔离的子代理上下文中运行，请考虑改用 [Skills](/docs/zh-CN/skills)。

对于关于对话中已有内容的问题，请使用 [`/btw`](/docs/zh-CN/interactive-mode#side-questions-with-%2Fbtw) 而不是子代理。它能看到您的完整上下文，但无法使用工具，且答案不会添加到历史记录中。

<h3 id="let-subagents-spawn-their-own-subagents">
  让子代理生成自己的子代理
</h3>

默认情况下，子代理可以生成自己的子代理，最多可达主对话之下三层。达到深度限制时，Claude Code 会从除 [fork](#fork-the-current-conversation) 之外的所有子代理中移除 `Agent` 工具，因此处于限制层级的子代理会自己完成委托的工作并返回一份摘要。处于限制层级的 fork 在其继承的工具列表中仍保留 `Agent`，但该工具会返回错误而不是生成子代理。

嵌套子代理适用于本身可拆分为并行子任务的委托任务，例如一个审查子代理为每项发现分派一个验证者。在交互式会话中，只有顶层子代理的摘要会返回给您，中间输出不会进入您的主对话：启动后台子代理的子代理会等待它们的结果后再结束。在[非交互模式](/docs/zh-CN/headless)和 Agent SDK 中，发起启动的子代理不会等待，因此如果嵌套的后台子代理在其启动者结束后才完成，它会改为向您的主对话报告。

要更改该限制，请将 [`CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH`](/docs/zh-CN/env-vars) 设置为您希望在主对话之下允许的子代理层数。例如，[`settings.json`](/docs/zh-CN/settings) 中的以下条目将嵌套限制为两层：

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH": "2"
  }
}
```

使用此值时，您的子代理可以委托给它们自己的第二层子代理，而第二层无法再进一步委托。设置为 `1` 可关闭嵌套。

嵌套子代理的配置方式与顶层子代理相同，并从相同的[作用域](#choose-the-subagent-scope)中解析。要在嵌套开启时阻止某个子代理生成子代理（例如应保持只读的审查者），请从其 [`tools`](#available-tools) 列表中省略 `Agent`，或将其添加到 `disallowedTools`。

在终端中，Claude Code 会在输入框下方的子代理面板中以树形显示嵌套子代理，并为面板中仍有后代的每一行标注 `(+N)`，表示其后代数量。打开某一行即可查看该子代理的同级和直接子级，以及返回 `main` 的路径。

<Note>
  早期版本使用不同的默认值：

  * **v2.1.172 至 v2.1.216**：子代理默认可以嵌套，最多五层，且该限制无法更改。
  * **v2.1.217 至 v2.1.218**：该限制默认为一，因此除非您调高，否则子代理无法生成自己的子代理；v2.1.219 将默认值提高到三。
</Note>

<h3 id="concurrent-subagent-limit">
  并发子代理限制
</h3>

有两个限制控制子代理的使用，各自对应一个变量：本限制在运行中的子代理过多时阻止 Claude 生成更多子代理，而[深度限制](#let-subagents-spawn-their-own-subagents)则限制子代理的嵌套深度。Claude 在一个会话中可以生成的子代理总数没有限制。

默认情况下，当会话中有 20 个子代理正在运行时，使用 Agent 工具再生成一个会失败并返回 `Concurrent subagent limit reached`，且该错误会告知 Claude 不要重试。当运行数量降到限制以下时，即可再次成功生成。要更改该限制，请将 [`CLAUDE_CODE_MAX_CONCURRENT_SUBAGENTS`](/docs/zh-CN/env-vars) 设置为任意正整数。启用了 [ultracode](/docs/zh-CN/model-config#adjust-effort-level) 的会话不受此限制约束。需要 Claude Code v2.1.217 或更高版本。

该限制只阻止 Claude 使用 Agent 工具生成的子代理，但其他运行也会占用相同的槽位：

* 您通过 [`/subtask`](#fork-the-current-conversation) 启动的会话内 fork 在运行时会占用一个槽位，且永远不会被该限制阻止。
* [恢复](#resume-subagents)已完成的子代理会占用一个新槽位，且不检查限制，因此恢复操作可能使运行数量超过限制。

其他功能运行的 Agent，例如[工作流](/docs/zh-CN/workflows) Agent 和 [agent team](/docs/zh-CN/agent-teams) 队友，则遵循各自的限制。

<h3 id="manage-subagent-context">
  管理子代理上下文
</h3>

<h4 id="what-loads-at-startup">
  启动时加载的内容
</h4>

每个子代理都从一个全新的、隔离的上下文窗口开始。它看不到您的对话历史、您已调用的 skill 或 Claude 已读取的文件。Claude 会编写一条概括任务的委托消息，子代理以此为起点开展工作。例外是 [fork](#fork-the-current-conversation)，它会继承父对话，而不是从零开始。

非 fork 子代理的初始上下文包含：

* **系统提示词**：Agent 自身的提示词加上 Claude Code 附加的环境详情，而不是 Claude Code 系统提示词。自定义子代理在 [markdown 正文](#write-subagent-files)或 `prompt` 字段中定义其系统提示词。内置 Agent 具有预定义的提示词。
* **任务消息**：Claude 在移交工作时编写的委托提示词。
* **CLAUDE.md 文件**：主对话所加载的 [CLAUDE.md 层级结构](/docs/zh-CN/memory#how-claude-md-files-load)中的每一级，包括 `~/.claude/CLAUDE.md`、项目规则、`CLAUDE.local.md`、托管策略文件，以及作为项目指令加载的任何 [`AGENTS.md` 文件](/docs/zh-CN/memory#agents-md)。内置的 Explore 和 Plan Agent 会跳过这些。定义中设置了 [`omitClaudeMd`](#supported-frontmatter-fields) 的子代理只加载托管策略文件；如果该定义来自[托管设置](#choose-the-subagent-scope)，则一个也不加载。
* **Git 状态**：子代理启动时 Claude Code 从您的仓库读取的快照。在 Git 仓库之外或快照被关闭时不存在；请参阅 [`includeGitInstructions`](/docs/zh-CN/settings-reference#includegitinstructions)。Explore 和 Plan 无论如何都会跳过它。
* **预加载的 skill**：Agent 的 [`skills` 字段](#preload-skills-into-subagents)中列出的每个 skill 的完整内容。内置 Agent 不预加载 skill。
* **同级名单**：一条[系统提醒](/docs/zh-CN/glossary#system-reminder)，列出 `main` 以及会话中所有其他已命名的 Agent，每一个都是 [`SendMessage`](#resume-subagents) 的有效 `to` 值。需要 Claude Code v2.1.206 或更高版本。仅当子代理的工具包含 `SendMessage` 且至少有一个其他 Agent 拥有名称时才会出现该名单，无论该名称是 Claude 在生成时指定的，还是该 Agent 作为 [agent team](/docs/zh-CN/agent-teams) 队友运行。名单是子代理启动时拍摄的快照，因此之后命名的 Agent 不会出现在其中。

要在不加载用户、项目和本地 CLAUDE.md 文件的情况下启动您自己的某个子代理，请在其 frontmatter 或 `--agents` JSON 中设置 [`omitClaudeMd: true`](#supported-frontmatter-fields)。

主对话在读取这些子代理的结果时仍拥有您的完整 CLAUDE.md，因此大多数规则无需传达给子代理本身。如果某条规则必须传达，例如"忽略 `vendor/` 目录"，请在委托时给 Claude 的提示词中重新说明。

您无法更改哪些子代理会接收 Git 状态。只有 Explore 和 Plan 会跳过它。

某些主对话状态永远不会传递给非 fork 子代理：

* **输出样式**：子代理运行自己的系统提示词，因此您的[输出样式](/docs/zh-CN/output-styles)不会影响其回复，[fork](#fork-the-current-conversation) 除外。
* **自动记忆**：不会加载主对话的[自动记忆](/docs/zh-CN/memory#auto-memory)。要为子代理提供其自身的持久记忆，请使用 [`memory` 字段](#enable-persistent-memory)。
* **上下文窗口大小**：子代理的上下文窗口大小由其自身的模型决定，而不是由父级决定。委托给上下文窗口较小的模型时，该子代理获得的也是较小的窗口。

<h4 id="resume-subagents">
  恢复子代理
</h4>

每次调用子代理都会创建一个新实例，而不是延续之前的实例。要继续某个现有子代理的工作而不是从头开始，请让 Claude 恢复它。

恢复的子代理会保留其完整的对话历史，包括之前所有的工具调用、结果和推理。如果该子代理生成过[自己的后台子代理](#let-subagents-spawn-their-own-subagents)，该历史还包括这些后台子代理在其运行期间交付的结果。子代理会从停止的地方继续，而不是从零开始。

* 子代理完成时，Claude 会收到其 Agent ID。
* 内置的 Explore 和 Plan Agent 是一次性的，不返回 Agent ID，因此 Claude 无法恢复它们。需要继续工作时，请使用 `general-purpose` 或自定义子代理。
* 当子代理因达到 [`maxTurns`](#supported-frontmatter-fields) 限制而停止时，Claude Code 会将返回的输出标记为部分结果，Claude 可以恢复该子代理以继续其工作。

Claude 使用 `SendMessage` 工具，以 Agent 的 ID 或名称作为 `to` 字段来恢复它。`SendMessage` 不要求启用 [agent teams](/docs/zh-CN/agent-teams)；只有 `shutdown_request` 和 `plan_approval_response` 等结构化团队协议消息才需要。除了子代理和队友之外，在启用了跨会话消息的会话中，Claude 还可以使用同一工具向[您的其他 Claude Code 会话](/docs/zh-CN/cross-session-messaging)发送消息，无论它们在本机还是[其他机器上](/docs/zh-CN/cross-session-messaging#message-sessions-on-other-machines)。

要恢复子代理，请让 Claude 继续之前的工作：

```text wrap theme={null}
Use the code-reviewer subagent to review the authentication module
[Agent completes]

Continue that code review and now analyze the authorization logic
[Claude resumes the subagent with full context from previous conversation]
```

当 Claude 使用 `SendMessage` 工具向已完成的子代理发送消息时，该子代理会在后台恢复，无需新的 `Agent` 调用。对于 Claude 使用 `TaskStop` 工具停止的子代理，在其被停止的运行退出后同样适用。恢复后的运行会保留[子代理首次运行时的工具集](#run-subagents-in-foreground-or-background)，并且可以继续读取[原始运行预热的提示缓存](/docs/zh-CN/prompt-caching#subagents-and-the-cache)。

拥有 `SendMessage` 工具的子代理也可以发送这种消息。在交互式会话中，被恢复的 Agent 随后会向恢复它的那个子代理汇报，而不是向您的主对话汇报。该子代理会等待结果后再完成自己的工作。当子代理向它所汇报的 Agent（例如其自身的启动者）发送消息时，Claude Code 会恢复该 Agent，且不会重定向其结果。

由您亲自停止的子代理（通过在 `/tasks` 中按 `x` 或发出 SDK `stop_task` 请求）不会自动恢复。如果 Claude 向它发送消息，该消息会被拒绝，并告知 Claude 该 Agent 已被取消。

当[该子代理所在的行仍在子代理面板中](#run-subagents-in-foreground-or-background)时，您可以在其会话记录中输入内容来亲自恢复它。此后，来自 Claude 的消息即可再次自动恢复它。

恢复会在同一 ID 下启动该 Agent 的一次新运行，因此已失败或已完成的子代理会在任务列表和 Agent SDK 的任务事件中再次显示为运行中。在 v2.1.205 之前，在恢复的运行进行期间，它仍会显示之前的失败或已完成状态。

`SendMessage` 会检查某个名称是否仍指向对话中先前通过该名称联系到的同一个 Agent。如果该名称已被较新的 Agent 占用（例如重新生成的后台 Agent 复用了该名称），Claude Code 会拒绝发送，而不是将消息送达错误的 Agent，并且错误会报告该名称现在指向哪个 Agent，以便 Claude 重新指定目标。要在较早的 Agent 仍在运行时联系它，Claude 会使用生成该 Agent 时收到的 Agent ID 来寻址。此检查仅限于当前对话，并会在 `/clear` 时重置。

子代理会将来自启动它的 Agent 的消息视为正常的任务指示，包括任务进行中的方向修正，并在其自身的权限设置范围内执行。无论消息由谁发送，以下两项限制始终有效：任何 Agent 发来的消息都不算作您对待处理权限提示的批准；任何 Agent 消息都无法更改子代理的权限设置、`CLAUDE.md` 或配置。只有权限系统或您本人的消息才能给予批准。

如果您想明确引用某个子代理，也可以向 Claude 询问其 Agent ID，或在 `~/.claude/projects/{project}/{sessionId}/subagents/` 下的会话记录文件中查找 ID。每份会话记录存储为 `agent-{agentId}.jsonl`。

子代理会话记录独立于主对话持久保存：

* **主对话压缩**：主对话压缩时，子代理会话记录不受影响。它们存储在单独的文件中。
* **会话持久性**：子代理会话记录在其所属会话内持久保存。重启 Claude Code 后，您可以通过恢复同一会话来[恢复子代理](#resume-subagents)。
* **自动清理**：Claude Code 会在 `cleanupPeriodDays` 保留期（默认为 30 天）过后删除子代理会话记录，遵循[保留清理规则](/docs/zh-CN/claude-directory#cleaned-up-automatically)。

<h4 id="auto-compaction">
  上下文自动压缩
</h4>

子代理支持使用与主对话相同的逻辑进行自动压缩。压缩在相同条件下触发，`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` 同样适用于子代理。有关该覆盖何时生效，请参阅[环境变量](/docs/zh-CN/env-vars)。

压缩事件会记录在子代理会话记录文件中：

```json theme={null}
{
  "type": "system",
  "subtype": "compact_boundary",
  "compactMetadata": {
    "trigger": "auto",
    "preTokens": 167189
  }
}
```

`preTokens` 值表示压缩发生前已使用的 token 数量。

<h2 id="fork-the-current-conversation">
  分叉当前对话
</h2>

<Note>
  使用 `/subtask` 运行分叉 subagent，需要 Claude Code v2.1.212 或更高版本。当[代理视图被关闭](/docs/zh-CN/agent-view#turn-off-agent-view)时，`/subtask` 不可用，`/fork` 启动分叉 subagent；否则 `/fork` 将整个会话复制到新的[后台会话](/docs/zh-CN/agent-view#from-inside-a-session)中。
</Note>

分叉是一个 subagent，它继承到目前为止的整个对话，而不是从头开始。这消除了 subagents 通常提供的输入隔离：分叉看到与主会话相同的系统提示、工具、模型和消息历史，因此您可以将其交给一个辅助任务而无需重新解释情况。分叉自己的工具调用仍然保持在您的对话之外，只有其最终结果返回，因此您的主 context window 保持干净。当任何其他 subagent 需要太多背景才能有用时，或当您想从相同的起点并行尝试多种方法时，使用分叉。

Claude 通过 Agent 工具请求 `fork` subagent 类型来启动分叉。您可以通过[分叉模式](#turn-fork-mode-on-or-off)控制是否可以这样做，在交互式会话中默认启用。

您可以使用 `/subtask` 后跟任务自己启动分叉，无论分叉模式是否启用。在 v2.1.161 到 v2.1.211 版本中，命令是 `/fork`。Claude Code 从任务的前几个单词命名分叉。以下示例分叉对话以在您继续主会话中的实现时草拟测试用例：

```text wrap theme={null}
/subtask draft unit tests for the parser changes so far
```

分叉出现在提示下方的面板中，并在您继续工作时在后台运行。完成后，其结果作为消息到达您的主对话。下一部分涵盖了在分叉运行时观察和引导它们的面板控制。

<h3 id="observe-and-steer-running-forks">
  观察和引导运行中的分叉
</h3>

运行中的分叉出现在提示输入下方的面板中，主会话有一行，每个分叉有一行。

当分叉成功完成时，Claude Code 会移除其行。Claude Code 保留失败或您停止的分叉的行 30 秒，[与任何其他后台 subagent 相同](#run-subagents-in-foreground-or-background)。在 v2.1.232 之前，Claude Code 也会将完成的分叉的行保留 30 秒。

使用这些键与面板交互：

| Key | Action |
| :- | :- |
| `↑` / `↓` | 在行之间移动 |
| `Enter` | 打开所选分叉的转录并向其发送后续消息 |
| `x` | 如果分叉正在运行，停止它；如果不再运行，关闭其行。在主会话行或您使用 `Enter` 打开其转录的分叉行上，`x` 会输入到提示中 |
| `Esc` | 将焦点返回到提示输入 |

打开分叉或子代理的会话记录后，后续消息和 [skill](/docs/zh-CN/skills) 会发送到该 Agent，而内置命令会发送到您的主对话，并有以下保护措施：

* `/compact`、`/clear` 和 `/rewind` 作用于主对话，因此 Claude Code 在从该视图运行其中任何一个之前会要求您确认。
* `/model` 和 `/fast` 设置的是主对话的模型和快速模式，而不是所查看 Agent 的，因此它们不会从该视图运行。一条通知会告诉您原因。

要让所查看的 Agent 在其等待的工作完成之前读取您的消息，请使用 [`Ctrl+Enter` 或 `Ctrl+X Ctrl+S`](/docs/zh-CN/keybindings#chat-actions) 发送。该 Agent 正在等待的任何可以移至[后台](/docs/zh-CN/tools-reference#background-commands)的 shell 命令或子代理都会移至后台并继续运行。当该 Agent 正在编写回复，或正在等待无法移至后台的工作时，它会继续进行，并在完成后读取您的消息。需要 Claude Code v2.1.286 或更高版本。

<h3 id="how-forks-differ-from-other-subagents">
  分叉与其他 subagents 的区别
</h3>

分叉继承主会话在生成时拥有的一切。任何其他 subagent 从其定义开始。

| | 分叉 | 非分叉 subagent |
| :- | :- | :- |
| 上下文 | 完整的对话历史 | 新鲜上下文，带有您传递的提示 |
| 系统提示和工具 | 与主会话相同 | 来自 subagent 的[定义文件](#write-subagent-files)，[为后台运行过滤](#available-tools) |
| 模型 | 与主会话相同 | 来自 subagent 的 `model` 字段 |
| 权限 | 提示在您的终端中出现 | [提示在后台运行时在您的主会话中出现](#run-subagents-in-foreground-or-background) |
| Prompt cache | 与主会话共享 | 单独的缓存 |

因为分叉的系统提示词和工具定义与父级相同，其第一个请求重用父级的[提示缓存](/docs/zh-CN/prompt-caching#subagents-and-the-cache)。由于这种重用，对于需要相同上下文的任务，分叉的成本低于新的子代理。

当 Claude 通过 Agent 工具生成分叉时，它可以传递 `isolation: "worktree"` 以便分叉的文件编辑被写入单独的 git worktree 而不是您的检出。分叉无法生成进一步的分叉。

<h3 id="turn-fork-mode-on-or-off">
  打开或关闭分叉模式
</h3>

Claude Code 在交互式会话中默认打开分叉模式，在[非交互模式](/docs/zh-CN/headless)中使用 `-p` 和 Agent SDK 中默认关闭。交互式默认值需要 Claude Code v2.1.232 或更高版本。在早期版本中，设置 `CLAUDE_CODE_FORK_SUBAGENT` 为 `1` 以打开分叉模式。

您可以从 Claude Code 处理 Agent 工具的方式判断分叉模式是否打开：

* Claude 可以通过请求 `fork` subagent 类型来生成分叉。当 Claude 不请求类型时，如果会话仍然有该类型，它会获得[通用](#built-in-subagents) subagent。从定义生成的 subagents，例如 Explore，照常工作。
* Claude Code 在后台运行 Claude 生成的 subagents，分叉和非分叉 subagents 都是如此，除了[保持在前台的情况](#run-subagents-in-foreground-or-background)。Claude Code 也会移除 Agent 工具的 `run_in_background` 参数，因此 Claude 无法请求前台。

设置 [`CLAUDE_CODE_FORK_SUBAGENT`](/docs/zh-CN/env-vars) 环境变量以覆盖默认值：

* `1` 在非交互模式和 Agent SDK 中打开分叉模式
* `0` 在每种会话中关闭分叉模式

要保持分叉模式打开但阻止 Claude 生成分叉，使用 `Agent(fork)` 规则[禁用 `fork` subagent 类型](#disable-specific-subagents)。Claude Code 仍然在后台运行 Claude 生成的 subagents，除了相同的[保持在前台的情况](#run-subagents-in-foreground-or-background)。

<h2 id="example-subagents">
  示例 subagents
</h2>

这些示例演示了构建 subagents 的有效模式。将它们用作起点，或使用 Claude 生成自定义版本。

<Tip>
  **最佳实践：**

  * **设计专注的 subagents：** 每个 subagent 应该在一个特定任务中表现出色
  * **编写单独突出一个 subagent 的描述：** Claude 使用描述来决定何时委托。使每个描述具体到足以路由到正确的 subagent，并将组合集保持在 [15,000 令牌描述预算](#understand-automatic-delegation) 内
  * **限制工具访问：** 仅授予必要的权限以确保安全和专注
  * **检入版本控制：** 与您的团队共享项目 subagents
</Tip>

<h3 id="code-reviewer">
  代码审查者
</h3>

一个只读 subagent，审查代码而不修改它。此示例展示了如何设计一个专注的 subagent，具有有限的工具访问（排除 Edit 和 Write）和详细的提示，指定确切要查找的内容以及如何格式化输出。

```markdown theme={null}
---
name: code-reviewer
description: Expert code review specialist. Proactively reviews code for quality, security, and maintainability. Use immediately after writing or modifying code.
tools: Read, Grep, Glob, Bash
model: inherit
---

You are a senior code reviewer ensuring high standards of code quality and security.

When invoked:
1. Run git diff to see recent changes
2. Focus on modified files
3. Begin review immediately

Review checklist:
- Code is clear and readable
- Functions and variables are well-named
- No duplicated code
- Proper error handling
- No exposed secrets or API keys
- Input validation implemented
- Good test coverage
- Performance considerations addressed

Provide feedback organized by priority:
- Critical issues (must fix)
- Warnings (should fix)
- Suggestions (consider improving)

Include specific examples of how to fix issues.
```

<h3 id="debugger">
  调试器
</h3>

一个可以分析和修复问题的 subagent。与代码审查者不同，这个包括 Edit，因为修复错误需要修改代码。提示提供了从诊断到验证的清晰工作流。

```markdown theme={null}
---
name: debugger
description: Debugging specialist for errors, test failures, and unexpected behavior. Use proactively when encountering any issues.
tools: Read, Edit, Bash, Grep, Glob
---

You are an expert debugger specializing in root cause analysis.

When invoked:
1. Capture error message and stack trace
2. Identify reproduction steps
3. Isolate the failure location
4. Implement minimal fix
5. Verify solution works

Debugging process:
- Analyze error messages and logs
- Check recent code changes
- Form and test hypotheses
- Add strategic debug logging
- Inspect variable states

For each issue, provide:
- Root cause explanation
- Evidence supporting the diagnosis
- Specific code fix
- Testing approach
- Prevention recommendations

Focus on fixing the underlying issue, not the symptoms.
```

<h3 id="data-scientist">
  数据科学家
</h3>

一个用于数据分析工作的特定领域 subagent。此示例展示了如何为典型编码任务之外的专门工作流创建 subagents。它明确设置 `model: sonnet` 以获得更强大的分析能力。

```markdown theme={null}
---
name: data-scientist
description: Data analysis expert for SQL queries, BigQuery operations, and data insights. Use proactively for data analysis tasks and queries.
tools: Bash, Read, Write
model: sonnet
---

You are a data scientist specializing in SQL and BigQuery analysis.

When invoked:
1. Understand the data analysis requirement
2. Write efficient SQL queries
3. Use BigQuery command line tools (bq) when appropriate
4. Analyze and summarize results
5. Present findings clearly

Key practices:
- Write optimized SQL queries with proper filters
- Use appropriate aggregations and joins
- Include comments explaining complex logic
- Format results for readability
- Provide data-driven recommendations

For each analysis:
- Explain the query approach
- Document any assumptions
- Highlight key findings
- Suggest next steps based on data

Always ensure queries are efficient and cost-effective.
```

<h3 id="database-query-validator">
  数据库查询验证器
</h3>

一个允许 Bash 访问但验证命令以仅允许只读 SQL 查询的 subagent。此示例展示了当您需要比 `tools` 字段提供的更精细的控制时如何使用 `PreToolUse` hooks。

```markdown theme={null}
---
name: db-reader
description: Execute read-only database queries. Use when analyzing data or generating reports.
tools: Bash
hooks:
  PreToolUse:
    - matcher: "Bash"
      hooks:
        - type: command
          command: "./scripts/validate-readonly-query.sh"
---

You are a database analyst with read-only access. Execute SELECT queries to answer questions about the data.

When asked to analyze data:
1. Identify which tables contain the relevant data
2. Write efficient SELECT queries with appropriate filters
3. Present results clearly with context

You cannot modify data. If asked to INSERT, UPDATE, DELETE, or modify schema, explain that you only have read access.
```

Claude Code [通过 stdin 将 hook 输入作为 JSON 传递](/docs/zh-CN/hooks#pretooluse-input) 给 hook 命令。验证脚本读取此 JSON，提取正在执行的命令，并根据 SQL 写入操作列表检查它。如果检测到写入操作，脚本 [以代码 2 退出](/docs/zh-CN/hooks#exit-code-2-behavior-per-event) 以阻止执行，并通过 stderr 向 Claude 返回错误消息。

在您的项目中的任何位置创建验证脚本。路径必须与您的 hook 配置中的 `command` 字段匹配：

```bash theme={null}
#!/bin/bash
# Blocks SQL write operations, allows SELECT queries

# Read JSON input from stdin
INPUT=$(cat)

# Extract the command field from tool_input using jq
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [ -z "$COMMAND" ]; then
  exit 0
fi

# Block write operations (case-insensitive)
if echo "$COMMAND" | grep -iE '\b(INSERT|UPDATE|DELETE|DROP|CREATE|ALTER|TRUNCATE|REPLACE|MERGE)\b' > /dev/null; then
  echo "Blocked: Write operations not allowed. Use SELECT queries only." >&2
  exit 2
fi

exit 0
```

在 macOS 和 Linux 上，使脚本可执行：

```bash theme={null}
chmod +x ./scripts/validate-readonly-query.sh
```

在 Windows 上，用 PowerShell 编写验证脚本，并在 hook 条目中添加 `shell: powershell`。请参阅 [在 PowerShell 中运行 hooks](/docs/zh-CN/hooks#windows-powershell-tool)。

Hook 通过 stdin 接收 JSON，Bash 命令在 `tool_input.command` 中。退出代码 2 阻止操作并将错误消息反馈给 Claude。有关退出代码和输出的详细信息，请参阅 [Hooks](/docs/zh-CN/hooks#exit-code-output)，有关完整的输入架构，请参阅 [Hook input](/docs/zh-CN/hooks#pretooluse-input)。

系统提示告诉 subagent 拒绝写入请求，因此 hook 是一个后备：如果 subagent 尝试写入，Claude Code 会阻止该命令，subagent 会看到 `Blocked: Write operations not allowed. Use SELECT queries only.` 消息。

<h2 id="next-steps">
  后续步骤
</h2>

现在您了解了 subagents，探索这些相关功能：

* [使用 plugins 分发 subagents](/docs/zh-CN/plugins/components#agents) 以在团队或项目中共享 subagents
* [以编程方式运行 Claude Code](/docs/zh-CN/headless)，使用 Agent SDK 进行 CI/CD 和自动化
* [使用 MCP 服务器](/docs/zh-CN/mcp) 为 subagents 提供对外部工具和数据的访问
