> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 探索 .claude 目录

> Claude Code 读取 CLAUDE.md、settings.json、hooks、skills、commands、subagents、workflows、rules 和自动内存的位置。探索项目中的 .claude 目录和主目录中的 ~/.claude。

Claude Code 从您的项目目录和主目录中的 `~/.claude` 读取指令、设置、skills、subagents 和内存。将项目文件提交到 git 以与您的团队共享；`~/.claude` 中的文件是个人配置，适用于您的所有项目。

在 Windows 上，`~/.claude` 解析为 `%USERPROFILE%\.claude`。如果您设置了 [`CLAUDE_CONFIG_DIR`](https://code.claude.com/docs/zh-CN/env-vars)，此页面上的每个 `~/.claude` 路径都将位于该目录下。这同样适用于 `.claude.json`，否则它位于 `~/.claude.json`。

大多数用户只编辑 `CLAUDE.md` 和 `settings.json`。如果您的仓库已经有一个供其他编码 Agent 使用的 `AGENTS.md`，Claude Code [可以读取它](https://code.claude.com/docs/zh-CN/memory.md#agents-md)来代替 `CLAUDE.md`。目录的其余部分是可选的：根据需要添加 skill、规则或子代理。

## 探索目录

单击树中的文件以查看每个文件的作用、何时加载以及示例。

Configuration files

**`CLAUDE.md`**

**When it loads**: 在会话开始时加载到上下文中

项目特定的指令，决定 Claude 在此仓库中的工作方式。请将您的约定、常用命令和架构背景放在这里。

**`.mcp.json`**

**When it loads**: 在交互式会话中，您已[批准](https://code.claude.com/docs/zh-CN/mcp.md#project-scope)的 MCP 服务器会在会话开始时加载。工具 schema 默认延迟加载，并通过[工具搜索](https://code.claude.com/docs/zh-CN/mcp.md#scale-with-mcp-tool-search)按需加载

配置 Model Context Protocol (MCP) 服务器，使 Claude 能够访问外部工具：数据库、API、浏览器等。此文件保存整个团队使用的项目级服务器。仅供自己使用的个人服务器应放在 `~/.claude.json` 中。

**`.worktreeinclude`**

**When it loads**: 当 Claude 通过 `--worktree`、`EnterWorktree` 工具或子代理 `isolation: worktree` 创建 [git worktree](https://code.claude.com/docs/zh-CN/worktrees.md) 时读取

列出要从主仓库复制到每个新 worktree 中的被 gitignore 的文件。worktree 是全新检出的副本，因此 `.env` 等未跟踪文件默认不存在。此处的模式使用 `.gitignore` 语法。只有与某个模式匹配且同时被 gitignore 的文件才会被复制。

**`.claude/`**

项目设置、规则、skill、子代理和其他配置。如果您使用 git，请提交其中的大部分文件以便团队共享，并将 `settings.local.json` 等个人文件排除在提交之外。

**`.claude/settings.json`**

**When it loads**: 在会话开始时读取。大多数编辑会[应用于正在运行的会话](https://code.claude.com/docs/zh-CN/settings.md#when-edits-take-effect)

由 Claude Code 直接应用的设置。权限控制 Claude 可以使用哪些命令和工具；hook 在会话的特定时间点运行您的脚本。与 Claude 作为指导来阅读的 CLAUDE.md 不同，这些设置无论 Claude 是否遵循都会被强制执行。

在[设置优先级](https://code.claude.com/docs/zh-CN/settings.md#settings-precedence)中，此文件的优先级高于 `~/.claude/settings.json`，低于 `.claude/settings.local.json`、`--settings` 标志和托管设置。对于大多数单值键（例如 `model`），Claude Code 使用优先级最高的值。大多数列表（例如 `permissions.allow`）会[跨文件合并](https://code.claude.com/docs/zh-CN/settings.md#lists-merge-instead-of-overriding)。

**`.claude/settings.local.json`**

**When it loads**: 在会话开始时读取。大多数编辑会[应用于正在运行的会话](https://code.claude.com/docs/zh-CN/settings.md#when-edits-take-effect)

您针对此项目的个人设置。JSON 格式与 `settings.json` 相同，当 Claude Code 将设置保存到此文件时会将其加入 gitignore。

在[设置优先级](https://code.claude.com/docs/zh-CN/settings.md#settings-precedence)中，此文件的优先级高于 `.claude/settings.json`，低于 `--settings` 标志和托管设置。对于大多数单值键（例如 `model`），Claude Code 使用优先级最高的值。大多数列表（例如 `permissions.allow`）会[跨文件合并](https://code.claude.com/docs/zh-CN/settings.md#lists-merge-instead-of-overriding)。

**`.claude/rules/`**

**When it loads**: 没有 `paths:` frontmatter 的规则在会话开始时加载。带有 `paths:` 的规则在 Claude 读取、写入或编辑匹配的文件时加载

按主题拆分为多个文件的项目指令。与 CLAUDE.md 一样，规则是 Claude Code 不会强制执行的指导。如需强制执行的行为，请使用 [hook](https://code.claude.com/docs/zh-CN/hooks.md) 或[权限](https://code.claude.com/docs/zh-CN/permissions.md)。

**`.claude/skills/`**

**When it loads**: 通过 `/skill-name` 调用，或在 Claude 将任务与某个 skill 匹配时调用

每个 skill 是一个文件夹，包含一个 `SKILL.md` 文件以及所需的任何支持文件。默认情况下，您和 Claude 都可以调用 skill。使用 [frontmatter](https://code.claude.com/docs/zh-CN/skills.md#frontmatter-reference) 来控制这一点：设置 `disable-model-invocation: true` 可使 Claude 无法自行调用 `/deploy` 之类的 skill，设置 `user-invocable: false` 则只有 Claude 可以调用该 skill。

**`.claude/commands/`**

**When it loads**: 通过 `/command-name` 调用，或在 Claude 将任务与某个命令匹配时调用

存放单文件命令：保存为 `.claude/commands/deploy.md` 的提示词会以 `/deploy` 运行。对于新命令，请使用 [skill](#ce-skills)，它可以将参考文档、模板或脚本与提示词捆绑在一起。

**`.claude/output-styles/`**

**When it loads**: 在终端启动时读取，因此添加或编辑样式后请重启 Claude Code

每个 Markdown 文件定义一种[输出样式](https://code.claude.com/docs/zh-CN/output-styles.md#how-output-styles-work)，即一组调整 Claude 工作方式的指令。如果某个样式由团队共享（例如所有人都使用的审查模式），请将其放在这里。有关如何选择样式，请参阅 [`~/.claude/output-styles/`](#ce-global-output-styles)。

**`.claude/agents/`**

**When it loads**: 当您或 Claude 调用子代理时，每个子代理在其自己的上下文窗口中运行

每个带有 `name` 和 `description` frontmatter 的 Markdown 文件定义一个子代理，该子代理拥有自己的系统提示词、工具访问权限，还可以选择使用自己的模型。适用于并行工作或隔离任务。

**`.claude/workflows/`**

**When it loads**: 当[工作流已启用](https://code.claude.com/docs/zh-CN/workflows.md)时在启动时加载。每个已保存的工作流以 `/<name>` 命令运行

每个 `.js` 文件是一个[动态工作流](https://code.claude.com/docs/zh-CN/workflows.md)：由运行时执行的脚本，用于生成并协调多个子代理。要添加工作流，请让 Claude 编写一个工作流，然后在会话中运行 `/workflows` 并将其保存在此处。

**`.claude/agent-memory/`**

**When it loads**: 子代理运行时，其 `MEMORY.md` 的前 200 行（上限 25KB）会加载到其系统提示词中

在[自动记忆](https://code.claude.com/docs/zh-CN/memory.md#auto-memory)开启时，frontmatter 中带有 [`memory: project`](https://code.claude.com/docs/zh-CN/sub-agents#enable-persistent-memory) 的子代理会在此处获得专用的记忆目录。每个子代理读写自己的 `MEMORY.md`，与主会话在 `~/.claude/projects/` 中的自动记忆相互独立。

**`.claude/agent-memory/<agent-name>/MEMORY.md`**

**When it loads**: 子代理运行时，前 200 行（上限 25KB）会加载到该子代理的系统提示词中

子代理已保存笔记的索引。子代理会自行创建和更新此文件，格式与您主会话的[自动记忆](https://code.claude.com/docs/zh-CN/memory.md#storage-location)索引相同。

**`~/.claude.json`**

**When it loads**: 在会话开始时读取，以获取您的偏好和 MCP 服务器。当您在 `/config` 中更改[全局配置选项](https://code.claude.com/docs/zh-CN/settings-reference.md#global-config-settings)或信任某个项目文件夹时，Claude Code 会写回此文件

保存账户详细信息、各项目的信任决定、您的个人 MCP 服务器以及 UI 开关。

**`~/.claude/`**

与项目 [`.claude/`](#ce-dot-claude) 目录对应的全局目录。此目录中的配置文件会在这台机器上的每个项目中对您生效。

**`~/.claude/CLAUDE.md`**

**When it loads**: 在这台机器上的每个项目中于会话开始时加载

您的全局指令文件。与项目 CLAUDE.md 一同加载。如果两者冲突，Claude 可能遵循其中任意一个。此文件应只包含适用于所有地方的偏好：回复风格、提交格式、个人约定。

**`~/.claude/settings.json`**

**When it loads**: 在会话开始时读取。大多数编辑会[应用于正在运行的会话](https://code.claude.com/docs/zh-CN/settings.md#when-edits-take-effect)

格式与项目 `settings.json` 相同：权限、hook、模型和环境变量。将您希望在每个项目中使用的设置放在这里，例如允许规则、首选模型或通知 hook。

在[设置优先级](https://code.claude.com/docs/zh-CN/settings.md#settings-precedence)中，此文件的优先级低于项目的设置文件、`--settings` 标志和托管设置。对于大多数单值键（例如 `model`），Claude Code 使用优先级最高的值。大多数列表（例如 `permissions.allow`）会[跨文件合并](https://code.claude.com/docs/zh-CN/settings.md#lists-merge-instead-of-overriding)。

**`~/.claude/keybindings.json`**

**When it loads**: 在会话开始时读取，并在您编辑该文件时热重载

在交互式 CLI 中重新绑定快捷键。在会话中运行 `/keybindings` 以创建或打开此文件。在选择按键之前，请查看[保留的快捷键](https://code.claude.com/docs/zh-CN/keybindings.md#reserved-shortcuts)。

**`~/.claude/themes/`**

**When it loads**: 在会话开始时读取，并在文件更改时[热重载](https://code.claude.com/docs/zh-CN/terminal-config.md#create-a-custom-theme)。列在 `/theme` 中

每个 `.json` 文件定义一个自定义颜色主题：一个内置的 `base` 预设加上一个由颜色标识组成的 `overrides` 映射。在会话中运行 `/theme` 来创建主题，或自行编写 JSON。选择自定义主题会将 `custom:<slug>` 存储为您的主题偏好。

**`~/.claude/projects/`**

**When it loads**: 在自动记忆开启时，当前项目的 `memory/MEMORY.md` 会在会话开始时加载。其中列出的主题文件按需读取

保存[自动记忆](https://code.claude.com/docs/zh-CN/memory.md#auto-memory)，即 Claude 跨会话保存的笔记：您的角色和偏好、您给出的纠正、项目决策，以及在项目之外何处查找信息。每个项目都有自己的记忆目录，以仓库路径作为键。

**`~/.claude/projects/<project>/memory/MEMORY.md`**

**When it loads**: 在[自动记忆](https://code.claude.com/docs/zh-CN/memory.md#auto-memory)开启时，前 200 行（上限 25KB）会在会话开始时加载

指向主题文件以获取详细信息的索引。Claude 会在工作过程中创建和更新此文件。您可以编辑或删除它。

**`~/.claude/projects/<project>/memory/user_role.md`**

**When it loads**: 当出现相关任务时，Claude 会读取此文件

主题文件的一个示例。Claude 会将每条记忆保存在各自的主题文件中，自行选择文件名，并在 `MEMORY.md` 中列出。

**`~/.claude/rules/`**

**When it loads**: 没有 `paths:` frontmatter 的规则在会话开始时加载。带有 `paths:` 的规则在 Claude 读取、写入或编辑匹配的文件时加载

格式与项目 [`.claude/rules/`](#ce-rules) 相同，应用于这台机器上的每个项目。用于您希望在所有工作中遵循的约定，例如个人代码风格或提交信息格式。

**`~/.claude/skills/`**

**When it loads**: 通过 `/skill-name` 调用，或在 Claude 将任务与某个 skill 匹配时调用

您为自己构建的 skill，可在这台机器上的所有项目中使用。格式与项目 [`.claude/skills/`](#ce-skills) 相同。

**`~/.claude/commands/`**

**When it loads**: 通过 `/command-name` 调用，或在 Claude 将任务与某个命令匹配时调用

格式与项目 [`.claude/commands/`](#ce-commands) 相同，可在这台机器上的所有项目中使用。

**`~/.claude/output-styles/`**

**When it loads**: 在终端启动时读取，因此添加或编辑样式后请重启 Claude Code

每个 Markdown 文件定义一种[输出样式](https://code.claude.com/docs/zh-CN/output-styles.md#how-output-styles-work)，即一组调整 Claude 工作方式的指令。使用样式可将 Claude Code 适配到编程以外的用途，或添加教学或审查模式。

在会话中通过 `/output-style` 或 `/config`，或通过设置中的 `outputStyle` 键选择内置或自定义样式。此处的样式可在这台机器上的每个项目中使用。如果某个项目样式具有相同名称，Claude Code 会使用该项目的样式。

**`~/.claude/agents/`**

**When it loads**: 当您或 Claude 调用子代理时，每个子代理在其自己的上下文窗口中运行

此处定义的子代理可在这台机器上的所有项目中使用。格式与项目 [`.claude/agents/`](#ce-agents) 相同。

**`~/.claude/workflows/`**

**When it loads**: 当[工作流已启用](https://code.claude.com/docs/zh-CN/workflows.md)时在启动时加载。每个已保存的工作流以 `/<name>` 命令运行

保存在此处的工作流脚本可在这台机器上的所有项目中使用。`.claude/workflows/` 中同名的项目工作流优先。

**`~/.claude/agent-memory/`**

**When it loads**: 子代理运行时，其 `MEMORY.md` 的前 200 行（上限 25KB）会加载到其系统提示词中

在[自动记忆](https://code.claude.com/docs/zh-CN/memory.md#auto-memory)开启时，frontmatter 中带有 `memory: user` 的子代理会将知识存储在此处。这些知识在所有项目中持久保留。有关项目级子代理记忆，请参阅 [`.claude/agent-memory/`](#ce-agent-memory)。

## 未显示的内容

浏览器涵盖您创作和编辑的文件。一些相关文件位于其他位置：

| 文件 | 位置 | 用途 |
| - | - | - |
| `managed-settings.json` | 系统级别，因操作系统而异 | 企业强制执行的设置，您自己的设置文件和 `--settings` 值无法覆盖这些设置，除了[狭窄的例外](https://code.claude.com/docs/zh-CN/settings.md#exceptions-to-managed-settings-precedence)。请参阅[保存文件的位置](https://code.claude.com/docs/zh-CN/managed-settings.md#deploy-a-managed-settings-file)和[Claude Code 使用的托管源](https://code.claude.com/docs/zh-CN/managed-settings.md#precedence-within-the-managed-tier)。 |
| `CLAUDE.local.md` | 项目根目录 | 您对此项目的私人偏好，与 CLAUDE.md 一起加载。手动创建它并将其添加到 `.gitignore`。 |
| `AGENTS.md` | 项目根目录、`.claude/` 或任何目录 | 您为 AI 编码 Agent 编写的项目说明。Claude Code 可以[加载它](https://code.claude.com/docs/zh-CN/memory.md#agents-md)来代替 `CLAUDE.md`。 |
| 已安装的插件 | `~/.claude/plugins` | 克隆的市场、已安装的插件版本、`installed_plugins.json` 安装记录和每个插件的数据，由 `claude plugin` 命令管理。从您的 claude.ai 账户[同步的插件](https://code.claude.com/docs/zh-CN/plugins/loading.md#synced-plugins)下载到 `~/.claude/plugins/synced/`。对于从市场[`command` 源](https://code.claude.com/docs/zh-CN/plugins/marketplace-reference#command-plugin-source)以链接模式安装的插件，Claude Code 在此处存储链接而不是副本，插件的文件保留在命令打印的目录中。`command` 源需要 Claude Code v2.1.229 或更高版本。在您从本地路径添加的市场中按相对路径列出的插件也会[从其源目录就地加载](https://code.claude.com/docs/zh-CN/plugins/loading.md#find-plugins-on-disk)，而不是从缓存副本加载。请参阅[插件缓存](https://code.claude.com/docs/zh-CN/plugins/loading.md#find-plugins-on-disk)了解孤立版本如何被清理。 |

`~/.claude` 还保存 Claude Code 在您工作时写入的数据：记录、提示历史、文件快照、缓存和日志。请参阅下面的[应用数据](#application-data)。

## 选择正确的文件

不同类型的自定义位于不同的文件中。使用此表找到更改应该放在哪里。

| 您想要 | 编辑 | 范围 | 参考 |
| :- | :- | :- | :- |
| 为 Claude 提供项目上下文和约定 | `CLAUDE.md` | 项目或全局 | [Memory](https://code.claude.com/docs/zh-CN/memory.md) |
| 允许或阻止特定工具调用 | `settings.json` `permissions` 或 `hooks` | 项目或全局 | [Permissions](https://code.claude.com/docs/zh-CN/permissions.md)、[Hooks](https://code.claude.com/docs/zh-CN/hooks.md) |
| 在工具调用前后运行脚本 | `settings.json` `hooks` | 项目或全局 | [Hooks](https://code.claude.com/docs/zh-CN/hooks.md) |
| 为会话设置环境变量 | `settings.json` `env` | 项目或全局 | [Settings](https://code.claude.com/docs/zh-CN/settings-reference.md#all-settings) |
| 将个人覆盖保留在 git 之外 | `settings.local.json` | 仅项目 | [Settings scopes](https://code.claude.com/docs/zh-CN/settings.md#where-settings-live) |
| 添加使用 `/name` 调用的提示或功能 | `skills/<name>/SKILL.md` | 项目或全局 | [Skills](https://code.claude.com/docs/zh-CN/skills.md) |
| 定义具有自己工具的专门 subagent | `agents/*.md` | 项目或全局 | [Subagents](https://code.claude.com/docs/zh-CN/sub-agents.md) |
| 通过脚本编排许多 subagent | `workflows/*.js` | 项目或全局 | [Dynamic workflows](https://code.claude.com/docs/zh-CN/workflows.md) |
| 通过 MCP 连接外部工具 | `.mcp.json` | 仅项目 | [MCP](https://code.claude.com/docs/zh-CN/mcp.md) |
| 更改 Claude 格式化响应的方式 | `output-styles/*.md` | 项目或全局 | [Output styles](https://code.claude.com/docs/zh-CN/output-styles.md) |

## 文件参考

此表列出浏览器涵盖的每个文件。项目范围的文件位于您的仓库中的 `.claude/` 下（或 `CLAUDE.md`、`.mcp.json` 和 `.worktreeinclude` 的根目录）。全局范围的文件位于 `~/.claude/` 中，适用于所有项目。

> [!NOTE]
>
> 有几件事可以覆盖您在这些文件中放入的内容：
>
> * 您的组织部署的[托管设置](https://code.claude.com/docs/zh-CN/server-managed-settings.md)优先于所有设置文件和 `--settings` 值，[设置优先级下的例外](https://code.claude.com/docs/zh-CN/settings.md#exceptions-to-managed-settings-precedence)除外
> * CLI 标志（如 `--permission-mode` 或 `--settings`）在该会话中覆盖 `settings.json`
> * 某些环境变量优先于其等效设置，但这会有所不同：检查[环境变量参考](https://code.claude.com/docs/zh-CN/env-vars.md)以了解每个变量
>
> 请参阅[设置优先级](https://code.claude.com/docs/zh-CN/settings.md#settings-precedence)以了解完整顺序。

单击文件名以在上面的浏览器中打开该节点。

| 文件 | 范围 | 提交 | 作用 | 参考 |
| - | - | - | - | - |
| [`CLAUDE.md`](#ce-claude-md) | 项目和全局 | ✓ | 每个会话加载的指令 | [内存](https://code.claude.com/docs/zh-CN/memory.md) |
| [`rules/*.md`](#ce-rules) | 项目和全局 | ✓ | 主题范围的指令，可选择路径门控 | [Rules](https://code.claude.com/docs/zh-CN/memory.md#organize-rules-with-claude/rules/) |
| [`settings.json`](#ce-settings-json) | 项目和全局 | ✓ | 权限、hooks、环境变量、模型默认值 | [设置](https://code.claude.com/docs/zh-CN/settings.md) |
| [`settings.local.json`](#ce-settings-local-json) | 仅项目 | | 您的个人覆盖，当 Claude Code 将设置保存到其中时自动 gitignored | [设置范围](https://code.claude.com/docs/zh-CN/settings.md#where-settings-live) |
| [`.mcp.json`](#ce-mcp-json) | 仅项目 | ✓ | 团队共享的 MCP 服务器 | [MCP 范围](https://code.claude.com/docs/zh-CN/mcp.md#mcp-installation-scopes) |
| [`.worktreeinclude`](#ce-worktreeinclude) | 仅项目 | ✓ | Gitignored 文件以复制到新的 worktrees | [Worktrees](https://code.claude.com/docs/zh-CN/worktrees.md#copy-gitignored-files-into-worktrees) |
| [`skills/<name>/SKILL.md`](#ce-skills) | 项目和全局 | ✓ | 可重用的提示，使用 `/name` 调用或自动调用 | [Skills](https://code.claude.com/docs/zh-CN/skills.md) |
| [`commands/*.md`](#ce-commands) | 项目和全局 | ✓ | 单文件提示；与 skills 相同的机制 | [Skills](https://code.claude.com/docs/zh-CN/skills.md) |
| [`output-styles/*.md`](#ce-output-styles) | 项目和全局 | ✓ | 自定义指令集，调整 Claude 的工作方式 | [输出样式](https://code.claude.com/docs/zh-CN/output-styles.md) |
| [`agents/*.md`](#ce-agents) | 项目和全局 | ✓ | Subagent 定义及其自己的提示和工具 | [Subagents](https://code.claude.com/docs/zh-CN/sub-agents.md) |
| [`workflows/*.js`](#ce-workflows) | 项目和全局 | ✓ | 由 Claude 编写并从 `/workflows` 保存的动态工作流脚本；每个已保存的工作流都作为一个 `/<name>` 命令运行 | [动态工作流](https://code.claude.com/docs/zh-CN/workflows.md) |
| [`agent-memory/<name>/`](#ce-agent-memory) | 项目和全局 | ✓ | Subagents 的持久内存 | [持久内存](https://code.claude.com/docs/zh-CN/sub-agents.md#enable-persistent-memory) |
| [`~/.claude.json`](#ce-claude-json) | 仅全局 | | 应用状态、账户详情、UI 切换、个人 MCP 服务器。如果该文件不存在，Claude Code 会在您启动会话或运行 `claude auth status` 等子命令时创建它，但运行 `--version` 或 `--help` 时不会创建。 | [全局配置](https://code.claude.com/docs/zh-CN/settings-reference.md#global-config-settings) |
| [`projects/<project>/memory/`](#ce-global-projects) | 仅全局 | | 自动内存：Claude 在会话间对自己的笔记 | [自动内存](https://code.claude.com/docs/zh-CN/memory.md#auto-memory) |
| [`keybindings.json`](#ce-keybindings) | 仅全局 | | 自定义快捷键 | [快捷键](https://code.claude.com/docs/zh-CN/keybindings.md) |
| [`themes/*.json`](#ce-themes) | 仅全局 | | 自定义颜色主题 | [自定义主题](https://code.claude.com/docs/zh-CN/terminal-config.md#create-a-custom-theme) |

## 按文件分类的 Frontmatter 字段

Skills、命令文件、subagents、输出样式和规则从文件顶部的 YAML [frontmatter](https://code.claude.com/docs/zh-CN/glossary.md#frontmatter) 读取其配置，每个都接受自己的一组字段。此表列出了每个文件的字段名称，并链接到描述它们的参考资料。

| 文件 | Frontmatter 字段 | 参考资料 |
| - | - | - |
| `skills/<name>/SKILL.md` | `name`, `description`, `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `allowed-tools`, `disallowed-tools`, `model`, `effort`, `context`, `agent`, `background`, `hooks`, `paths`, `shell`, `metadata`, `license`, `compatibility` | [Skill frontmatter](https://code.claude.com/docs/zh-CN/skills.md#frontmatter-reference) |
| `commands/*.md` | 除 `name` 和 `paths` 外的 skill 字段 | [Skill frontmatter](https://code.claude.com/docs/zh-CN/skills.md#frontmatter-reference) |
| `agents/*.md` | `name`, `description`, `tools`, `disallowedTools`, `model`, `permissionMode`, `maxTurns`, `autoCompactWindow`, `skills`, `mcpServers`, `hooks`, `memory`, `background`, `effort`, `isolation`, `color`, `initialPrompt`, `omitClaudeMd`, `experimental` | [子代理 frontmatter](https://code.claude.com/docs/zh-CN/sub-agents.md#supported-frontmatter-fields) |
| `output-styles/*.md` | `name`, `description`, `keep-coding-instructions`, `force-for-plugin` | [Output style frontmatter](https://code.claude.com/docs/zh-CN/output-styles.md#frontmatter) |
| `rules/*.md` | `paths` | [Rule frontmatter](https://code.claude.com/docs/zh-CN/memory.md#rules-frontmatter-reference) |

在 [plugin](https://code.claude.com/docs/zh-CN/plugins/components.md#agents) 中提供的 Agents 遵守 subagent 字段的一个子集。

## 排查配置问题

如果设置、hook 或文件未生效，请参阅[调试您的配置](https://code.claude.com/docs/zh-CN/debug-your-config.md)以获取检查命令和症状优先查找表。

## 应用数据

除了您创作的配置外，`~/.claude` 还保存 Claude Code 在会话期间写入的数据。这些文件是纯文本。通过工具传递的任何内容都会在磁盘上的记录中：文件内容、命令输出、粘贴的文本。

会话记录还可能包含 Claude Code 随您的消息一起发送给模型的内容：

* 系统提示词
* 工具定义
* 请求参数
* 它加载的指令文件，例如 CLAUDE.md

### 自动清理

Claude Code 删除下面路径中的文件，一旦它们的年龄超过 [`cleanupPeriodDays`](https://code.claude.com/docs/zh-CN/settings-reference#cleanupperioddays)，只要它能安全地确定保留期。默认值为 30 天，最小值为 1；设置 `0` 会导致验证错误。相同的年龄截止值也适用于 [孤立 worktrees](https://code.claude.com/docs/zh-CN/worktrees.md#clean-up-subagent-and-background-session-worktrees) 的自动删除。

| `~/.claude/` 下的路径 | 内容 |
| - | - |
| `projects/<project>/<session>.jsonl` | 对话的会话记录：消息、工具调用和工具结果，以及 Claude Code 发送给模型的请求中的系统提示词、工具定义和参数 |
| `projects/<project>/<session>.orphaned-<timestamp>-<suffix>.jsonl`、`projects/<project>/<session>.jsonl.superseded-<timestamp>` | 会话的先前记录，Claude Code 将其搁置而不是覆盖或删除它。它不会出现在会话选择器中 |
| `projects/<project>/<session>/subagents/` | [子代理](https://code.claude.com/docs/zh-CN/sub-agents.md)的会话记录，格式与会话的会话记录相同，当父会话记录过期时随之删除 |
| `projects/<project>/<session>/tool-results/` | 大型工具输出溢出到单独的文件，以及 [MCP 工具返回的图像](https://code.claude.com/docs/zh-CN/mcp.md#images-in-tool-results) 的完整大小副本 |
| `projects/<project>/<session>/mcp-tasks/` | 恢复的会话重新跟踪其正在运行的 [MCP 任务](https://code.claude.com/docs/zh-CN/mcp.md#mcp-tasks-that-run-on-the-server)所需的内容，以及 Claude 尚未读取的已完成任务的结果 |
| `file-history/<session>/` | Claude 更改的文件的编辑前快照，用于 [checkpoint 恢复](https://code.claude.com/docs/zh-CN/checkpointing.md)。保存最近 100 个 checkpoint 的快照；没有保留 checkpoint 引用的快照文件被删除，除了每个文件的第一个快照 |
| `plans/` | 在 [Plan Mode](https://code.claude.com/docs/zh-CN/permission-modes.md#analyze-before-you-edit-with-plan-mode) 期间写入的计划文件 |
| `debug/` | 每个会话的调试日志，在启用调试日志时写入，例如当您使用 [`--debug`](https://code.claude.com/docs/zh-CN/cli-reference#cli-flags) 启动或运行 `/debug` 时 |
| `paste-cache/` | 大型粘贴的内容 |
| `image-cache/<session>/` | Claude Code v2.1.274 及更早版本保存的附加图像。更高版本将粘贴和附加的图像保存在 `~/.claude` 之外，在 [`CLAUDE_CODE_TMPDIR`](https://code.claude.com/docs/zh-CN/env-vars) 控制的临时目录下每个会话的 `images/` 目录中。扫描会删除其他会话在此处留下的目录，无论其年龄如何。 |
| `uploads/<session>/` | 您从网络或移动应用附加的文件，以及从移动应用附加的照片，当向 [Remote Control](https://code.claude.com/docs/zh-CN/remote-control.md) 会话发送消息时。对 [cloud session](https://code.claude.com/docs/zh-CN/claude-code-on-the-web.md) 的附件保存在该会话自己的云环境中，而不是在您的机器上。 |
| `dev-mods/<session>/` | [Claude 在会话期间编写的 Mods](https://code.claude.com/docs/zh-CN/plugins/mods/create.md#ask-claude-for-a-mod) |
| `session-env/` | 每个会话的环境元数据 |
| `tasks/` | 由 task 工具写入的任务列表，每个列表一个目录 |
| `shell-snapshots/` | 由 [Bash 工具](https://code.claude.com/docs/zh-CN/tools-reference.md#bash-tool-behavior)应用于每个命令的别名、函数和 shell 选项。在正常退出时删除。扫描会清理崩溃后留下的任何内容。 |
| `backups/` | `~/.claude.json` 的早期版本，在 Claude Code 重写文件时复制。Claude Code 保留五个最新的版本，加上它无法解析的任何版本的副本。超过年龄截止值后，保存您配置的最后一个副本也会被删除。如果当前文件可以解析、保存了您的配置且小于 8 MiB，则会为其留下一个新副本。 |
| `feedback-bundles/` | 由 `/feedback` 在第三方提供商上或当未配置 Anthropic 凭证时写入的编辑后的记录存档，用于发送到您的 Anthropic 账户团队 |
| `feedback/drafts/` | 排队的 [Claude 起草的反馈](https://code.claude.com/docs/zh-CN/tools-reference.md#sendfeedback-tool-behavior)，等待您在 `/feedback` 中审查。在 `cleanupPeriodDays` 或 30 天后扫除，以较短者为准。当队列达到其 10 个草稿的限制时，Claude Code 删除最旧的草稿以腾出空间。 |
| `usage-data/` | `report.html` 和由 [`/insights`](https://code.claude.com/docs/zh-CN/costs#analyze-your-usage-patterns) 写入的时间戳报告副本，加上用于构建它们的缓存的每个会话分析数据 |
| `skills/.trash/`、`plugins/.trash/` | claude.ai 同步删除的 [skill](https://code.claude.com/docs/zh-CN/skills.md#how-synced-skills-behave) 和[插件](https://code.claude.com/docs/zh-CN/plugins/loading.md#synced-plugins)，例如在您于 claude.ai 上关闭其中某一项或停止同步之后。可在此处恢复它们。当某个文件夹存在超过 7 天且已有三个更新的副本时，或者当 `.trash/` 中的文件夹超过 1,024 个时，Claude Code 可能会在达到时间截止值之前删除该文件夹 |
| `plugins/installed_plugins.set-aside.<date>.<hash>.json`、`plugins/installed_plugins.unreadable.<date>.<hash>.kept` | Claude Code 在重写 [`installed_plugins.json`](https://code.claude.com/docs/zh-CN/plugins/loading#find-plugins-on-disk) 之前制作的日期副本：它删除的安装记录，以及它无法读取的文件的内容。 |
| `plugins/data/.set-aside/` | 来自某个市场的插件的数据目录，该市场已被您的组织替换为同名市场。其年龄从 Claude Code 移动它们的那天开始计算，项目设置中较短的 `cleanupPeriodDays` 不适用。要保留其中某个目录，请在扫描删除它之前将其移动到其他位置。 |
| `plugins/mcpb/` | Claude Code 从插件声明的 [MCP 捆绑包](https://code.claude.com/docs/zh-CN/plugins/components.md#include-a-packaged-mcpb-server)中提取的文件。捆绑包的年龄从最后一个使用它的会话开始计算。 |
| `todos/`、`statsig/`、`logs/` | 来自旧版本的旧版目录。不再写入。扫描删除其内容，然后删除空目录。 |

`sessions/` 中的会话文件、自动内存以及 Claude Desktop 和 Cowork 记录各自遵循自己的保留规则：

* **`sessions/`**：为每个运行的会话保存一个小文件，用于检测并发会话和崩溃。它不是基于年龄的扫描的一部分：Claude Code 在其会话退出时删除每个文件，并在下次启动时清理崩溃遗留物。
* **`seed-admin/`**：Claude Code 在为 [ultrareview](https://code.claude.com/docs/zh-CN/ultrareview.md) 或[云端会话上传](https://code.claude.com/docs/zh-CN/claude-code-on-the-web.md#send-local-repositories-without-github)打包您的仓库时创建的临时 git 目录。当上传结束时（如果上传被中断，则在之后的某个会话中），Claude Code 会删除该上传的目录，并保留 `seed-admin/` 本身。
* **自动内存**：扫描不删除项目 [自动内存](https://code.claude.com/docs/zh-CN/memory.md#auto-memory) 目录中的内存文件，`projects/<project>/memory/`。Claude Code 仅在整个保留期内该目录为空时才删除该目录。在 v2.1.228 之前，扫描将内存目录内的文件夹视为会话数据，可能删除其下的旧文件。
* **Claude Desktop 和 Cowork 会话记录**：Claude Code 保留您在 Claude Desktop 或 Cowork 中启动或最近继续的会话的会话记录，无论其年龄如何。要给这些会话记录设置年龄限制，请设置 [`desktopSessionCleanupPeriodDays`](https://code.claude.com/docs/zh-CN/settings-reference#desktopsessioncleanupperioddays)。需要 Claude Code v2.1.248 或更高版本；早期版本在 `cleanupPeriodDays` 后删除它们。

  在以下情况下，Claude Code 会改为在 `cleanupPeriodDays` 之后删除这些会话记录：

  * [托管设置](https://code.claude.com/docs/zh-CN/managed-settings.md)设置了 `cleanupPeriodDays`
  * [HIPAA 配置适用于您的会话](https://code.claude.com/docs/zh-CN/hipaa-setup.md#check-how-developers-sign-in-and-connect)

Claude Code 在这些情况下跳过基于年龄的扫描：

* **Bare mode**：当您使用 [`--bare`](https://code.claude.com/docs/zh-CN/headless#start-faster-with-bare-mode) 运行 `claude -p` 时，Claude Code 不会在该会话中运行扫描。
* **暂停扫描**：如果 Claude Code 无法安全地确定保留期，它会暂停扫描；[`retention_sweep` 事件](https://code.claude.com/docs/zh-CN/monitoring-usage#retention-sweep-event)会报告原因。当原因是无法读取或解析的设置文件，或者在设置了 `cleanupPeriodDays` 或 `desktopSessionCleanupPeriodDays` 的情况下存在设置错误时，`/status` 会显示警告，直到您修复该原因。

当[托管设置](https://code.claude.com/docs/zh-CN/managed-settings.md)提供 `cleanupPeriodDays` 时，即使较低优先级的设置文件存在错误，Claude Code 也会以托管值运行扫描。

要检查您组织中的机器是否按您设置的保留期运行扫描，请参阅[检查保留扫描](https://code.claude.com/docs/zh-CN/monitoring-usage.md#check-the-retention-sweep)。

### 会话暂存目录

暂存是 Claude Code 为 Claude 提供的每个会话目录，用于临时文件：中间结果、辅助脚本和不属于您的项目的草稿。当 Claude 说它将某些内容保存"到暂存"时，该文件就在那里。Claude 使用它而不是 `/tmp`，可以在其中创建、编辑和读取文件而无需权限提示。

暂存位于 Claude Code 的临时目录下，而不是 `~/.claude`。找到您的平台的当前会话路径：

* **macOS**：`/private/tmp/claude-<uid>/<project>/<session-id>/scratchpad/`
* **Linux**：`/tmp/claude-<uid>/<project>/<session-id>/scratchpad/`，或当您的系统设置 `$TMPDIR` 时在其下的相同形状
* **Windows**：`%TEMP%\claude\<project>\<session-id>\scratchpad\`

`<project>` 是您的工作目录路径，其中除字母和数字外的每个字符都被替换为 `-`，例如 `-Users-you-my-project`。在 Windows 上，`<project>` 是该字符串的 16 个字符的哈希值，例如 `73295dabccd14c56`。在 Desktop 应用会话中，它可以是该字符串本身。要获取确切路径，请询问 Claude。如果您设置了 [`CLAUDE_CODE_TMPDIR`](https://code.claude.com/docs/zh-CN/env-vars)，树会改为移动到该目录下。hook 接收当前会话的路径作为 [`scratchpad_dir`](https://code.claude.com/docs/zh-CN/hooks#common-input-fields)。

暂存文件的生命周期与会话的会话记录相同：[保留扫描](#cleaned-up-automatically)在删除会话记录时删除该目录，而 [`claude purge`](#clear-local-data) 不会触及临时目录。由于该目录位于系统临时位置下，您的操作系统也可能清除它，例如在重启时。要保留 Claude 在那里写入的内容，请让 Claude 将其移动到您的项目中。

会话仅在以下所有条件成立时才有暂存：

* 您使用 claude.ai 账户而不是 API 密钥登录
* 会话使用 Anthropic API，而不是 Amazon Bedrock、Google Cloud 的 Agent Platform 或 Microsoft Foundry
* [`enableArtifact`](https://code.claude.com/docs/zh-CN/settings-reference#enableartifact) 未设置为 `false`

### 保留直到您删除它们

除表中另有说明的行外，保留清理扫描不会删除下面的路径，Claude Code 会保留它们，直到您删除它们。

| `~/.claude/` 下的路径 | 内容 |
| - | - |
| `history.jsonl` | 您输入过的提示词，附带时间戳和项目路径。用于上箭头调取历史、`Ctrl+R` 历史搜索以及 `!` shell 命令补全。当 [HIPAA 配置适用于您的会话](https://code.claude.com/docs/zh-CN/hipaa-setup.md#check-how-developers-sign-in-and-connect)时，每次清理都会删除早于 `cleanupPeriodDays` 的条目。 |
| `stats-cache.json` | 由 `/usage` 显示的聚合令牌和成本计数 |
| `remote-settings.json` | [server-managed settings](https://code.claude.com/docs/zh-CN/server-managed-settings.md) 的缓存副本，用于您的组织，或当您的组织未配置任何设置时为 `{}`。仅在会话 [获取它们](https://code.claude.com/docs/zh-CN/server-managed-settings.md#platform-availability) 时存在。Claude Code 在启动时和会话期间每小时检查更新。Claude Code 在您注销时删除它。 |
| `cache/changelog.md` | Claude Code changelog 的缓存副本，由 `/release-notes` 显示。在后台刷新。 |
| `policy-limits.json` | 为您的组织缓存的功能策略设置。仅对某些账户类型存在。自动刷新。`policy-limits.json.stamp.json` sidecar 记录缓存属于哪个账户或 API 密钥。Claude Code 在您注销时删除两个文件。 |

#### 需保留的状态文件

根据您使用的功能，`~/.claude/` 中还会保存[应用数据](#application-data)下各表未列出的文件。其中，缓存和锁定文件可以安全删除。请保留以下状态文件：

* `.credentials.json`：您的 [login credentials](https://code.claude.com/docs/zh-CN/authentication.md#credential-management)
* `agent-memory/`：[subagent memory](https://code.claude.com/docs/zh-CN/sub-agents.md#enable-persistent-memory)
* `jobs/` 和 `daemon/`：[background session](https://code.claude.com/docs/zh-CN/agent-view.md#where-state-is-stored) 状态

### 纯文本存储

记录和历史在静止时未加密。操作系统文件权限是唯一的保护。如果工具读取 `.env` 文件或命令打印凭证，该值将写入 `projects/<project>/<session>.jsonl`。要减少暴露：

* 降低 `cleanupPeriodDays` 以缩短 Claude Code 保留记录的时间
* 设置 [`desktopSessionCleanupPeriodDays`](https://code.claude.com/docs/zh-CN/settings-reference#desktopsessioncleanupperioddays) 以给 Claude Desktop 和 Cowork 记录设置年龄限制
* 设置 [`CLAUDE_CODE_SKIP_PROMPT_HISTORY`](https://code.claude.com/docs/zh-CN/env-vars) 环境变量以跳过在任何模式下写入记录和提示历史。在非交互模式下，您可以改为在 `-p` 旁边传递 `--no-session-persistence`，或在 TypeScript Agent SDK 中设置 `persistSession: false`；Python SDK 没有等效选项。
* 使用 [权限规则](https://code.claude.com/docs/zh-CN/permissions.md) 拒绝读取凭证文件

### 清除本地数据

运行 `claude purge` 以删除 Claude Code 为某个项目保存的状态。它会删除：

* `projects/` 下的记录和自动内存
* 每个会话的 `tasks/`、`debug/` 和 `file-history/` 条目
* `history.jsonl` 中的匹配提示行
* `~/.claude.json` 中的项目条目

您在项目会话中粘贴或附加的图像以及每个会话的 [暂存](#session-scratchpad-directory) 存储在 Claude Code 的临时目录下，而不是 `~/.claude`，因此清除不会删除它们。[保留扫描](#cleaned-up-automatically) 仍会在它们的年龄超过 `cleanupPeriodDays` 时删除图像；清除的会话的暂存会保留，直到您删除它或您的操作系统清除临时目录。

该命令打印完整的删除计划，并在删除任何内容之前要求确认。

在 v2.1.288 之前，该命令为 `claude project purge`。

下面的示例使用 `~/work/my-repo` 作为占位符。将其替换为您的项目的路径。如果没有状态与路径匹配，该命令打印错误并以状态 1 退出。

预览计划而不删除任何内容：

```bash theme={null}
claude purge ~/work/my-repo --dry-run
```

该计划列出每个匹配项及其包含的原因：

```text theme={null}
Purge plan for /home/user/work/my-repo:

  dir:    /home/user/.claude/projects/-home-user-work-my-repo
           project transcripts (.jsonl) and memory/
  config: projects["/home/user/work/my-repo"]
           project entry in ~/.claude.json (trust, history, MCP servers)
  filter: /home/user/.claude/history.jsonl
           12 prompt(s) typed in this project

shell-snapshots/ are not project-scoped and will not be touched
backups/ may still contain this project entry in old .claude.json snapshots (/home/user/.claude/backups); at most 5 are kept and they rotate out automatically
Dry run: 3 item(s) would be deleted.
```

通过单个确认提示删除：

```bash theme={null}
claude purge ~/work/my-repo
```

该命令打印相同的计划，然后询问 `Delete 3 item(s) for /home/user/work/my-repo? This cannot be undone. [y/N]` 并仅在您回答 `y` 时删除。

省略路径以从交互式列表中选择项目。

跳过确认提示以在脚本中使用：

```bash theme={null}
claude purge ~/work/my-repo --yes
```

其他选项：

* 传递 `--all` 而不是路径，以一次清除所有项目的状态，这会直接删除 `history.jsonl` 而不是对其进行过滤。
* 传递 `-i` 以逐项执行删除计划。

该命令不理会 `shell-snapshots/` 和 `backups/`，因为这些不是项目范围的，并在计划输出中警告它们。如果有人在该机器上运行过 [`/heapdump`](https://code.claude.com/docs/zh-CN/troubleshooting#high-cpu-or-memory-usage)，也请删除它写入的 `.heapsnapshot` 文件。堆快照包含完整的对话以及进程持有的所有凭据，保留扫描和清除都不会触及它。

除[需保留的状态文件](#state-files-to-keep)外，您也可以自行删除上面的任何应用数据路径。

| 删除 | 您失去 |
| - | - |
| `~/.claude/projects/` | 恢复、继续和倒回过去的会话，以及每个项目的自动内存 |
| `~/.claude/history.jsonl` | 向上箭头提示回忆、`Ctrl+R` 历史搜索和 `!` shell 命令补全 |
| `~/.claude/paste-cache/` | 回忆的提示中的粘贴文本；请参阅 [paste large content](https://code.claude.com/docs/zh-CN/terminal-config.md#paste-large-content) |
| `~/.claude/uploads/` | 过去 [Remote Control](https://code.claude.com/docs/zh-CN/remote-control.md) 会话按路径引用的附件 |
| `~/.claude/file-history/` | 过去会话的 checkpoint 恢复 |
| `~/.claude/stats-cache.json` | 由 `/usage` 显示的历史总计 |
| `~/.claude/usage-data/` | 过去的 [`/insights`](https://code.claude.com/docs/zh-CN/costs#analyze-your-usage-patterns) 报告和用于构建它们的缓存分析数据 |
| `~/.claude/feedback-bundles/` | 您尚未发送给您的 Anthropic 账户团队的反馈和错误报告存档 |
| `~/.claude/feedback/drafts/` | 您尚未发送的 [Claude 起草的反馈](https://code.claude.com/docs/zh-CN/tools-reference.md#sendfeedback-tool-behavior) |
| `~/.claude/remote-settings.json` | 无。在下次启动时重新获取。 |
| `~/.claude/cache/changelog.md` | 无。在后台刷新。 |
| `~/.claude/policy-limits.json` | 无。自动刷新。 |
| `~/.claude/tasks/` | 您的[任务列表](https://code.claude.com/docs/zh-CN/interactive-mode.md#task-list)，包括仍在使用中的列表 |
| `~/.claude/skills/.trash/`、`~/.claude/plugins/.trash/` | 恢复 [synced skills](https://code.claude.com/docs/zh-CN/skills.md#how-synced-skills-behave) 和 [synced plugins](https://code.claude.com/docs/zh-CN/plugins/loading.md#synced-plugins) 的机会，Claude Code 已删除 |
| `~/.claude/plugins/installed_plugins.set-aside.<date>.<hash>.json`、`~/.claude/plugins/installed_plugins.unreadable.<date>.<hash>.kept` | Claude Code 删除的 plugin 安装记录副本或无法读取的文件副本。没有任何内容读取它们 |
| `~/.claude/debug/`、`~/.claude/plans/`、`~/.claude/session-env/`、`~/.claude/shell-snapshots/` | 没有面向用户的内容 |
| `~/.claude/backups/` | 可用于[恢复 `~/.claude.json`](https://code.claude.com/docs/zh-CN/errors#configuration-error-in-claude-json) 的早期副本 |
| `~/.claude/todos/`、`~/.claude/statsig/`、`~/.claude/logs/`、`~/.claude/image-cache/` | 无。旧版目录不由当前版本写入。 |

不要删除 `~/.claude.json`、`~/.claude/settings.json` 或 `~/.claude/plugins/`：这些保存您的账户详细信息、偏好和已安装的插件。

## 相关资源

* [管理 Claude 的内存](https://code.claude.com/docs/zh-CN/memory.md)：编写和组织 CLAUDE.md、rules 和自动内存
* [配置设置](https://code.claude.com/docs/zh-CN/settings.md)：设置权限、hooks、环境变量和模型默认值
* [创建 skills](https://code.claude.com/docs/zh-CN/skills.md)：构建可重用的提示和工作流
* [配置 subagents](https://code.claude.com/docs/zh-CN/sub-agents.md)：定义具有自己上下文的专门代理
