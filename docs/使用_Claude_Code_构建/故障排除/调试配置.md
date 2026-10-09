> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 调试你的配置

> 诊断为什么 CLAUDE.md、settings、hooks、MCP 服务器或 skills 没有生效。使用 /context、/doctor、/hooks 和 /mcp 来查看实际加载了什么。

当 Claude 忽略了一条指令或你配置的功能没有出现时，通常是因为文件没有加载、从你预期之外的位置加载，或者被另一个文件覆盖了。本指南展示了如何检查 Claude Code 实际加载了什么，以便你能够缩小范围。

对于安装、身份验证和连接问题，请参阅[故障排除安装和登录](/docs/zh-CN/troubleshoot-install)。

<h2 id="see-what-loaded-into-context">
  查看加载到上下文中的内容
</h2>

`/context` 命令会显示当前会话中占用上下文窗口的所有内容，并按类别细分：系统提示词、系统工具、MCP 工具、自定义子代理（及其各自的加载来源）、记忆文件、skill 以及对话消息。请首先运行此命令，以确认您的 `CLAUDE.md`、规则或 skill 描述是否已加载。`/context` 中的 skill 部分还包括 [随附 skill](/docs/zh-CN/skills#bundled-skills)，而 `/skills` 不会列出这些内容。

如需查看特定类别的详细信息，请继续使用相应的专用命令：

| 命令 | 显示内容 |
| :- | :- |
| `/memory` | 用户和项目作用域中的记忆文件位置，可选择在编辑器中打开每个文件，还可访问自动记忆文件夹以及自动记忆开关 |
| `/skills` | 来自项目、用户和插件来源的可用 skill |
| `/hooks` | 当前生效的 hook 配置 |
| `/mcp` | 已连接的 MCP 服务器及其状态 |
| `/permissions` | 当前生效的已解析允许和拒绝规则 |
| `/doctor` | 设置检查：安装健康状况、无效的设置文件、未使用的扩展、同一目录中重复的[子代理](/docs/zh-CN/sub-agents)名称，以及已签入的、Claude 可以从代码库中推导出的 `CLAUDE.md` 内容，并提供建议的修复方案 |
| `/debug [issue]` | 为会话启用调试日志，并提示 Claude 利用日志输出和设置路径进行诊断 |
| `/status` | 当前生效的设置来源，包括托管设置是否生效 |

如果某个记忆文件未出现在 `/context` 的细分列表中，请对照[CLAUDE.md 文件的加载方式](/docs/zh-CN/memory#how-claude-md-files-load)检查其位置。子目录中的 `CLAUDE.md` 文件是按需加载的，而不是在会话开始时加载，因此它们不会出现在该细分列表中。

如果 `/context` 确认文件已加载，但 Claude 仍未遵循某条特定指令，那么问题很可能在于指令的编写方式，而非是否已加载。CLAUDE.md 非常适合用于提供您会给新团队成员的那类指导，例如项目约定、构建命令以及文件应放置的位置。

当指令含糊到可以有多种理解方式、两个文件给出相互冲突的指示，或者文件变得过长以致单条规则得到的关注减少时，遵循度就会下降。[编写有效的指令](/docs/zh-CN/memory#write-effective-instructions)介绍了有助于保持高遵循度的具体性、篇幅和结构模式。

<Note>
  CLAUDE.md 和权限解决的是不同的问题。CLAUDE.md 告诉 Claude 您的项目如何运作，以便其做出良好的决策。[权限](/docs/zh-CN/permissions)和 [hook](/docs/zh-CN/hooks) 则无论 Claude 做出何种决定都会强制执行限制。请将 CLAUDE.md 用于"我们这里是这样做的"这类内容。对于安全边界以及任何绝不能发生的事情，即您需要的是保证而非指导的情况，请使用权限或 hook。
</Note>

<h2 id="check-resolved-settings">
  检查已解析的设置
</h2>

设置在托管、用户、项目和本地范围内合并。当存在时，托管设置总是优先。在其余的中，更接近的范围按本地、项目、用户的顺序覆盖更广泛的范围。某些设置也可以由命令行标志或[环境变量](/docs/zh-CN/env-vars)设置，它们充当另一个覆盖层。当设置似乎不适用时，你设置的值通常被另一个范围或环境变量覆盖。

要查找无效的设置文件，请从终端运行 `claude doctor`。它打印只读安装和设置诊断，而不启动会话。要进行完整检查，同时提议修复并在应用前询问，请在会话内运行 [`/doctor`](/docs/zh-CN/commands#all-commands)。

运行 `/status` 来查看哪些设置源是活跃的，包括是否启用了托管设置。要了解 Claude Code 对给定键使用哪个范围，请参阅[设置优先级](/docs/zh-CN/settings#settings-precedence)。

<h2 id="check-mcp-servers">
  检查 MCP 服务器
</h2>

运行 `/mcp` 来查看每个配置的服务器、其连接状态以及你是否为当前项目批准了它。服务器可以定义正确但仍然不提供工具，原因有几个常见的：

* `.mcp.json` 中的项目范围服务器需要一次性批准。如果提示被关闭，服务器将保持禁用状态，直到你从 `/mcp` 批准它。
* 启动失败的服务器在 `/mcp` 中显示为失败。`command` 或 `args` 中的相对文件路径是一个常见原因，因为它们相对于你启动 Claude Code 的目录而不是 `.mcp.json` 的位置进行解析。
* 显示为已连接但列出零个工具的服务器已成功启动但没有返回工具列表。从 `/mcp` 选择**重新连接**。如果计数保持为零，运行 `claude --debug=mcp` 并在 `~/.claude/debug/<session-id>.txt` 的调试日志中读取服务器的 stderr。

对于配置位置和范围规则，请参阅 [MCP](/docs/zh-CN/mcp)。

<h2 id="check-hooks">
  检查 hook
</h2>

运行 `/hooks` 来列出当前会话注册的每个 hook，按事件分组。如果您定义的 hook 没有出现，说明 Claude Code 没有加载它。请检查以下原因：

* 该 hook 定义在独立文件中。hook 应位于[设置文件](/docs/zh-CN/settings#settings-files)中的 `"hooks"` 键下。
* `matcher` 值是数组而不是单个字符串。在您启动交互式会话时以及在 `claude doctor` 中，Claude Code 会将该条目列为无效设置。如果该数组位于 `PreToolUse` 或 `PermissionRequest` 下，该文件中的其他 hook 也都不会加载。

如果 hook 出现但没有触发，匹配器通常是原因。检查它是否有这些错误：

* `matcher` 字段是一个使用 `|` 来匹配多个工具名称的单个字符串，例如 `"Edit|Write"`。`,` 分隔符是等效的，所以 `"Edit,Write"` 匹配相同的工具。在 v2.1.191 之前，逗号会进入正则表达式评估，匹配器永远不会匹配，所以如果您尚未使用 v2.1.191，请使用 `|`。
* 拼写错误的工具名称会产生一个不匹配任何内容的匹配器，所以 hook 会无声地失败。

当您编辑 `settings.json` 时，更改在短暂的文件稳定延迟后在运行的会话中生效，即使您在会话启动后创建了文件或项目的 `.claude/` 文件夹。您不需要重新启动。在 v2.1.257 之前，Claude Code 没有检测到在会话启动后创建的 `.claude/` 文件夹中的编辑。

如果保存后几秒钟 `/hooks` 仍然显示旧定义，再次运行 `/hooks` 来刷新视图。

如果 `/hooks` 显示 hook 但它仍然没有触发，下一步是实时观察 hook 评估。使用 `claude --debug` 启动会话并触发工具调用。调试日志记录每个事件、检查了哪些匹配器以及 hook 的退出码和输出。有关日志格式，请参阅[调试 hook](/docs/zh-CN/hooks#debug-hooks)，有关常见失败模式，请参阅[hook 故障排除](/docs/zh-CN/hooks-guide#limitations-and-troubleshooting)。

<h2 id="test-against-a-clean-configuration">
  针对干净配置进行测试
</h2>

首先使用 [`claude --safe-mode`](/docs/zh-CN/cli-reference#cli-flags)，它会启动一个禁用您的自定义内容的会话，包括：

* `CLAUDE.md`
* Skill、插件和 hook
* MCP 服务器
* 自定义命令和 Agent
* 自定义输出样式
* 自定义快捷键

身份验证、模型选择、内置工具和权限正常工作。如果问题在安全模式下消失，则说明原因已缩小到您关闭的某一项。要找出具体是哪一项，请使用该项对应的检查，例如[查看加载到上下文中的内容](#see-what-loaded-into-context)、[检查 MCP 服务器](#check-mcp-servers)或[检查 hook](#check-hooks)。

安全模式仍然应用来自您组织的托管 hook 和设置策略。托管插件、skill、`CLAUDE.md` 和 MCP 服务器会被关闭。

如果问题在安全模式下仍然存在，或你的设置本身可疑，请与从你的常规设置中不加载任何内容的会话进行比较。将 [`CLAUDE_CONFIG_DIR`](/docs/zh-CN/env-vars) 指向一个空目录以绕过 `~/.claude` 下的所有内容，并从没有 `.claude` 文件夹、`.mcp.json` 或 `CLAUDE.md` 的目录启动，以便也跳过项目配置。

```bash theme={null}
cd /tmp && CLAUDE_CONFIG_DIR=/tmp/claude-clean claude
```

干净会话没有用户或项目设置、hooks、MCP 服务器、plugins 或内存。在首次启动时，预期会看到首次运行设置屏幕，从主题选择开始。如果你看到它们，说明干净配置目录已生效。后续使用同一目录的启动会跳过这些屏幕，因为 Claude Code 会在那里保存入门状态。

* 如果你的组织部署了托管设置，它们仍然适用。Claude Code 读取 MDM 配置文件、注册表策略和来自配置目录外部位置的 `managed-settings.json`，并在干净会话获得凭证后[再次获取服务器管理的设置](/docs/zh-CN/server-managed-settings#fetch-and-caching-behavior)
* 你将被提示再次登录

如果问题在这里消失，原因在你的真实 `~/.claude` 或项目 `.claude` 文件中的某处。一次重新引入一个，通过将文件复制到临时目录或从你的项目启动，来找到哪一个。如果它在干净会话中持续存在，原因在你的用户和项目配置之外。运行 `/status` 来检查是否启用了托管设置，查找影响 Claude Code 的[环境变量](/docs/zh-CN/env-vars)，然后参阅[故障排除](/docs/zh-CN/troubleshooting)。

<h2 id="check-common-causes">
  检查常见原因
</h2>

大多数配置意外可以追溯到一小组位置和语法规则。在假设存在错误之前检查这些：

| 症状 | 原因 | 修复 |
| :- | :- | :- |
| Hook 永远不触发 | `matcher` 是 JSON 数组而不是字符串 | 使用单个字符串，其中 `\|` 匹配多个工具，例如 `"Edit\|Write"`。请参阅[匹配器模式](/docs/zh-CN/hooks#matcher-patterns)。 |
| Hook 永远不触发 | `matcher` 在 v2.1.191 之前的版本中使用 `,` 作为分隔符 | Claude Code v2.1.191 或更高版本将 `,` 视为列表分隔符，如 `\|`。早期版本将逗号评估为字面字符，因此 `"Edit,Write"` 不匹配任何内容。改用 `\|`，或升级 Claude Code。 |
| Hook 永远不触发 | `matcher` 值是小写的，例如 `"bash"` | 匹配是区分大小写的。工具名称是大写的：`Bash`、`Edit`、`Write`、`Read`。 |
| Hook 永远不触发 | Hooks 在独立文件而不是 `settings.json` 中定义 | 项目或用户配置没有独立的 hooks 文件。在 `settings.json` 中的 `"hooks"` 键下定义 hooks。只有[plugins](/docs/zh-CN/plugins/components#hooks)加载单独的 `hooks/hooks.json`。请参阅[hook 配置](/docs/zh-CN/hooks)。 |
| 全局设置的权限、hooks 或 env 被忽略 | 配置被添加到 `~/.claude.json` | `~/.claude.json` 保存应用状态和 UI 切换。`permissions`、`hooks` 和 `env` 属于 `~/.claude/settings.json`。这是两个不同的文件。 |
| `settings.json` 值似乎被忽略 | 相同的键在 `settings.local.json` 中设置 | `settings.local.json` 覆盖 `settings.json`，两者都覆盖 `~/.claude/settings.json`。请参阅[设置优先级](/docs/zh-CN/settings#settings-precedence)。 |
| Skill 没有出现在 `/skills` 中 | Skill 文件在 `.claude/skills/name.md` 而不是在文件夹中 | 使用包含 `SKILL.md` 的文件夹：`.claude/skills/name/SKILL.md`。 |
| Skill 出现在 `/skills` 中但 Claude 从不调用它 | Skill 在其 frontmatter 中有 `disable-model-invocation: true`，或其描述与你表述请求的方式不匹配 | 检查 `/skills` 中的徽章：一个"user-only"标签意味着 Claude 不会自动触发它。请参阅[skill 调用](/docs/zh-CN/skills)。 |
| 子目录 `CLAUDE.md` 指令似乎被忽略 | 子目录文件按需加载，而不是在会话开始时加载 | 请参阅[子目录文件何时加载](/docs/zh-CN/memory#how-claude-md-files-load)。在 v2.1.288 之前，只有 Read 工具会加载它们。 |
| 子代理忽略 `CLAUDE.md` 指令 | 内置的 Explore 和 Plan 代理跳过 `CLAUDE.md`。自定义子代理以与主对话相同的方式加载它，除非其定义设置了 [`omitClaudeMd`](/docs/zh-CN/sub-agents#supported-frontmatter-fields) | 对于 Explore 或 Plan，在你的委派提示中重新陈述指令。对于设置 `omitClaudeMd` 的子代理，删除该字段。对于任何其他自定义子代理，将关键指令放在代理文件体中，它成为代理的系统提示。请参阅[启动时加载的内容](/docs/zh-CN/sub-agents#what-loads-at-startup)。 |
| 清理逻辑在会话结束时永远不运行 | 没有配置 `SessionEnd` hook | 在 `settings.json` 中添加 `SessionEnd` hook。请参阅[hook 事件列表](/docs/zh-CN/hooks#hook-events)。 |
| `.mcp.json` 中的 MCP 服务器永远不加载 | 文件在 `.claude/` 下，或其服务器位于顶级 `servers` 键下，如 VS Code 的 `mcp.json` 中那样，而不是 `mcpServers` | 项目 MCP 配置在存储库根目录下作为 `.mcp.json`，而不是在 `.claude/` 内，服务器位于 `mcpServers` 键下。请参阅[MCP 配置](/docs/zh-CN/mcp)。 |
| 在 `settings.json` 中的 `mcpServers` 下添加的 MCP 服务器永远不出现 | `settings.json` 不读取 `mcpServers` 键 | 在存储库根目录的 `.mcp.json` 中定义项目服务器，或运行 `claude mcp add --scope user` 来添加用户范围的服务器。请参阅[MCP 配置](/docs/zh-CN/mcp)。 |
| 添加的项目 MCP 服务器没有出现 | 一次性批准提示被关闭 | 项目范围的服务器需要批准。运行 `/mcp` 来查看状态并批准。 |
| MCP 服务器从某些目录启动失败 | `command` 或 `args` 使用相对文件路径 | 对本地脚本使用绝对路径。你的 `PATH` 上的可执行文件如 `npx` 或 `uvx` 可以按原样工作。 |
| MCP 服务器启动时没有预期的环境变量 | 服务器的配置条目没有设置它们，它们不在 Claude Code 传递给 stdio 服务器的环境中：它自己的环境，减去[它从子进程中剥离的变量](/docs/zh-CN/monitoring-usage#administrator-configuration) | 在服务器的 `.mcp.json` 条目内设置每个服务器的 `env`，这不依赖于启动环境或工作区信任。 |
| `Bash(rm *)` 拒绝规则不阻止 `/bin/rm` 或 `find -delete` | Bash 规则匹配字面命令字符串，而不是底层可执行文件；请参阅[Bash 规则不匹配的内容](/docs/zh-CN/permissions#bash-rule-limits) | 使用[PreToolUse hook](/docs/zh-CN/hooks-guide)或[sandbox](/docs/zh-CN/sandboxing)来获得硬保证。 |

<h2 id="related-resources">
  相关资源
</h2>

有关每个配置表面的完整参考，请参阅专用页面：

* **[`.claude` 目录参考](/docs/zh-CN/claude-directory)**：每个配置文件位置及其读取方式
* **[Settings](/docs/zh-CN/settings)**：使用哪个文件以及 Claude Code 使用哪个值；[settings 参考](/docs/zh-CN/settings-reference)包含完整的键列表
* **[Hooks 参考](/docs/zh-CN/hooks)**：事件名称、有效负载和 `--debug` 输出格式
* **[MCP](/docs/zh-CN/mcp)**：服务器配置、批准和 `/mcp` 输出
* **[故障排除安装和登录](/docs/zh-CN/troubleshoot-install)**：`command not found`、PATH 和身份验证问题
* **[故障排除](/docs/zh-CN/troubleshooting)**：性能、挂起和搜索问题
