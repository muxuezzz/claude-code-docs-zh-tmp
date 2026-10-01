> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 使用 skills 扩展 Claude

> 创建、管理和共享 skills 以在 Claude Code 中扩展 Claude 的功能。包括自定义命令和捆绑的 skills。

Skills 扩展了 Claude 能做的事情。创建一个 `SKILL.md` 文件，其中包含说明，Claude 会将其添加到其工具包中。Claude 在相关时使用 skills，或者你可以使用 `/skill-name` 直接调用一个。

当你不断将相同的说明、检查清单或多步骤程序粘贴到聊天中时，或者当 CLAUDE.md 的某个部分已经演变成一个程序而不是事实时，就创建一个 skill。与 CLAUDE.md 内容不同，skill 的主体仅在使用时加载，因此长参考资料在你需要之前几乎不花费任何成本。

<Note>
  对于内置命令如 `/help` 和 `/compact`，以及捆绑的 skills 如 `/debug` 和 `/code-review`，请参阅[命令参考](/docs/zh-CN/commands)。

  **自定义命令已合并到 skills 中。** `.claude/commands/deploy.md` 中的文件和 `.claude/skills/deploy/SKILL.md` 中的 skill 都会创建 `/deploy` 并以相同的方式工作。你现有的 `.claude/commands/` 文件继续工作。Skills 添加了可选功能：支持文件的目录、用于[控制你或 Claude 是否调用它们](#control-who-invokes-a-skill)的 frontmatter，以及 Claude 在相关时自动加载它们的能力。
</Note>

Claude Code skills 遵循 [Agent Skills](https://agentskills.io) 开放标准，该标准适用于多个 AI 工具。Claude Code 使用额外功能扩展了该标准，如[调用控制](#control-who-invokes-a-skill)、[子代理执行](#run-skills-in-a-subagent)和[动态上下文注入](#inject-dynamic-context)。请参阅[在 Claude Code 外使用 skill frontmatter](#using-skill-frontmatter-outside-claude-code)，了解哪些 frontmatter 字段是标准的一部分，哪些是 Claude Code 扩展。

<h2 id="bundled-skills">
  捆绑技能
</h2>

Claude Code 包含一组捆绑技能，例如 `/doctor`、`/code-review`、`/batch`、`/debug`、`/loop` 和 `/claude-api`。捆绑技能是基于提示的：它们为 Claude 提供详细的指令，让它使用其工具来协调工作。大多数内置命令则直接执行固定逻辑。

您调用捆绑技能的方式与调用任何其他技能相同，即输入 `/` 后跟技能名称。Claude 在相关时会自动调用某些捆绑技能；其他技能（包括 `/verify`）仅在您调用它们时运行，这样可以让您控制这些耗时较长的检查何时花费时间和令牌。

大多数捆绑技能在每个会话中都可用。少数技能取决于特定功能：例如，`/workflow-authoring` 仅在[动态工作流](/docs/zh-CN/workflows)启用时可用。

要关闭捆绑技能，请使用 [`disableBundledSkills`](/docs/zh-CN/settings-reference#disablebundledskills) 设置。

<Note>
  在 Claude Code v2.1.205 及更高版本中，当 `disableBundledSkills` 打开时，[`/doctor`](/docs/zh-CN/commands#all-commands) 设置检查仍然可以输入。要隐藏它，请设置 `DISABLE_DOCTOR_COMMAND` 环境变量或 [`skillOverrides`](#override-skill-visibility-from-settings) 条目 `"doctor": "off"`。在 v2.1.205 之前，`/doctor` 是内置命令而不是捆绑技能。
</Note>

捆绑技能与内置命令一起列在[命令参考](/docs/zh-CN/commands)中，在"目的"列中标记为**技能**。

<h3 id="run-and-verify-your-app">
  运行并验证您的应用
</h3>

三个捆绑技能协同工作来启动您的应用并根据运行中的应用而不仅仅是测试来确认更改：

| 技能 | 目的 |
| :- | :- |
| `/run` | 启动并驱动您的应用以查看更改是否有效 |
| `/verify` | 构建并运行您的应用以确认代码更改是否按预期工作，无需回退到测试或类型检查 |
| `/run-skill-generator` | 教 `/run` 和 `/verify` 如何构建和启动您的项目 |

`/run` 和 `/verify` 无需设置即可工作。它们从您的项目类型（CLI、服务器、TUI、浏览器驱动）以及 README、`package.json` 或 `Makefile` 中的内容推断启动。对于需要超出标准启动范围的任何内容的项目，该推断变得不可靠：数据库、env 文件、图形会话、多步骤构建。

`/run-skill-generator` 改为记录配方。它从干净的环境中让您的应用运行，捕获有效的内容（安装命令、环境变量、启动脚本），并将其作为每个项目的技能提交到 `.claude/skills/run-<name>/`。之后，`/run`、`/verify` 和存储库中的任何其他代理都遵循记录的配方而不是重新发现它。每个项目运行一次 `/run-skill-generator`，如果构建或启动过程更改，则再次运行。

`/verify` 也可以记录自己的配方。当它必须在没有记录的配方的情况下构建和驱动您的应用时，它会将有效的内容写入存储库根目录的 `.claude/skills/verify/SKILL.md`，或在 monorepo 中的受触及的包目录中，以便后续运行和其他代理遵循相同的步骤。在存储库根目录，记录的技能替换捆绑的 `/verify`。这需要 Claude Code v2.1.200 或更高版本。

Claude 仅在它引导运行出错时编辑记录的文件，例如失败的命令或缺少的步骤，因此您可以提交文件而无需每个会话的差异。在 v2.1.205 之前，捆绑技能告诉 Claude 折叠运行学到的任何内容，这导致频繁的合并冲突。

<h3 id="work-on-claude-api-projects">
  处理 Claude API 项目
</h3>

捆绑的 `/claude-api` 技能为您的项目语言加载 [Claude API](https://platform.claude.com/docs/en/api/overview) 和[托管代理](https://platform.claude.com/docs/en/managed-agents/overview)参考资料。当您的代码导入 `anthropic` 或 `@anthropic-ai/sdk` 时，Claude 也会自动激活它。

要启动技能的工作流之一，请在 Claude Code 提示符处的技能名称后键入子命令，例如 `/claude-api migrate`。该表列出了每个子命令的作用以及包含它的最早 Claude Code 版本。`migrate` 和 `managed-agents-onboard` 早于 v2.1.221，这是该表跟踪的最早版本。

| 子命令 | 作用 | 最低版本 |
| :- | :- | :- |
| `migrate` | 将您现有的 Claude API 代码更新到更新的模型 | 早于 v2.1.221 |
| `upgrade` | 跨主要版本移动您的项目的 Anthropic SDK 依赖项，目前是 Python `anthropic` 包从 0.x 到 1.x | v2.1.236 或更高版本 |
| `managed-agents-onboard` | 逐步完成创建新的托管代理 | 早于 v2.1.221 |
| `prompt-audit` | 标记为旧模型编写的指令在您的提示、技能和工具描述中，并提议修复作为差异 | v2.1.221 或更高版本 |
| `cost-optimize` | 分析您的项目的 Claude API 支出去向，并提议从提示缓存、修剪不需要的输入和输出令牌、批处理、工作量和模型选择等选项中节省成本，一次一个更改 | v2.1.247 或更高版本 |
| `build-eval` | 为您的 Claude 驱动的应用构建评估集 | v2.1.259 或更高版本 |
| `hillclimb` | 针对现有评估迭代改进您的应用 | v2.1.259 或更高版本 |
| `preserved-thinking-migration` | 查找您的集成对早期轮次、其系统提示或其工具列表所做的编辑，这些编辑使[保留的思考](https://platform.claude.com/docs/en/build-with-claude/preserved-thinking)块失效，测量每个块丢弃多少推理，并提议一次一个修复，在每次更改后重新测量 | v2.1.282 或更高版本 |

<h2 id="getting-started">
  开始使用
</h2>

<h3 id="create-your-first-skill">
  创建你的第一个 skill
</h3>

这个示例创建了一个 skill，它总结你的 git 仓库中未提交的更改，并标记任何有风险的内容。它在 Claude 读取之前将实时差异拉入提示中，因此响应基于你的实际工作树，而不是 Claude 从打开的文件中猜测的内容。当你询问你的更改时，Claude 会自动加载该 skill，或者你可以使用 `/summarize-changes` 直接调用它。

<Steps>
  <Step title="创建 skill 目录">
    在你的个人 skills 文件夹中为该 skill 创建一个目录。个人 skills 在所有项目中都可用。

    ```bash theme={null}
    mkdir -p ~/.claude/skills/summarize-changes
    ```
  </Step>

  <Step title="编写 SKILL.md">
    每个 skill 都需要一个 `SKILL.md` 文件，包含两部分：`---` 标记之间的 YAML frontmatter，告诉 Claude 何时使用该 skill，以及包含 Claude 在 skill 运行时遵循的说明的 markdown 内容。目录名称或你设置的 frontmatter `name` 会成为你输入的命令，`description` 帮助 Claude 决定何时自动加载该 skill。

    将其保存到 `~/.claude/skills/summarize-changes/SKILL.md`：

    ```yaml theme={null}
    ---
    description: Summarizes uncommitted changes and flags anything risky. Use when the user asks what changed, wants a commit message, or asks to review their diff.
    ---

    ## Current changes

    !`git diff HEAD`

    ## Instructions

    Summarize the changes above in two or three bullet points, then list any risks you notice such as missing error handling, hardcoded values, or tests that need updating. If the diff is empty, say there are no uncommitted changes.
    ```

    `` !`git diff HEAD` `` 行使用[动态上下文注入](#inject-dynamic-context)：Claude Code 运行该命令，并在 Claude 看到 skill 内容之前将该行替换为其输出，因此说明会随着当前差异已内联而到达。
  </Step>

  <Step title="测试 skill">
    打开一个 git 项目，对任何文件进行小的编辑，并通过运行 `claude` 启动 Claude Code。你可以通过两种方式测试该 skill。

    **让 Claude 自动调用它**，通过询问与描述匹配的内容：

    ```text theme={null}
    What did I change?
    ```

    **或直接使用 skill 名称调用它**：

    ```text theme={null}
    /summarize-changes
    ```

    无论哪种方式，Claude 都应该用你的编辑的简短摘要和风险列表进行响应。
  </Step>
</Steps>

<h2 id="where-skills-live">
  选择 skills 的加载位置
</h2>

skills 的保存位置决定了哪些会话会加载它。将其保存在主目录下可在每个项目中使用，将其提交到存储库可与该处的所有人共享，或通过插件或托管设置分发以覆盖整个团队。

| 位置 | 路径 | 加载位置 |
| :- | :- | :- |
| Enterprise | `.claude/skills/<skill-name>/SKILL.md` 在 [托管设置目录](/docs/zh-CN/managed-settings#delivery-mechanisms) | 您的组织部署它的所有机器上的所有用户 |
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | 此机器上的所有项目，但不包括 [Cowork 或云会话](#skills-in-cowork-and-cloud-sessions) |
| Project | `.claude/skills/<skill-name>/SKILL.md` | 此存储库中的会话。提交它以便您的团队也能获得它 |
| Nested | `<subdir>/.claude/skills/<skill-name>/SKILL.md` | 在 `<subdir>` 中或其下方启动的会话。在其上方启动的会话在 Claude 处理该处的文件时加载该 skill。请参阅 [monorepos 和子目录](#discovery-from-parent-and-nested-directories) |
| Additional directory | `.claude/skills/<skill-name>/SKILL.md` 在使用 `--add-dir` 传递的目录中 | 该会话。请参阅 [项目外的目录](#skills-from-additional-directories) |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md` | 在 [插件](/docs/zh-CN/plugins/overview) 启用的任何位置，作为 `/plugin-name:skill-name` |
| claude.ai account | 为您的 claude.ai 账户启用的 skills | Cowork 会话、云会话和使用该账户登录的终端会话。请参阅 [从 claude.ai 同步的 Skills](#how-synced-skills-behave) |

Skill 文件夹还遵循以下规则：

* **符号链接文件夹**：enterprise、personal 或 project 位置中的 `<skill-name>` 条目可以是指向磁盘上其他位置的目录的符号链接。Claude Code 从目标读取 `SKILL.md` 并加载 skill，即使多个位置指向同一目标也只加载一次。插件 skills [以不同方式处理符号链接](/docs/zh-CN/plugins/host-marketplace#share-files-within-a-marketplace-with-symlinks)。
* **保留名称 `synced`**：不要将 skill 文件夹命名为 `synced`，无论大小写如何。Claude Code 使用 `~/.claude/skills/synced/` 来存放 [从 claude.ai 下载的 skills](#where-synced-skills-load)，并跳过您在 enterprise、personal 和 project 位置中以该名称创作的 skill。
* **保留名称 `anthropic-skills`**：在插件外，名称为 `anthropic-skills` 或以 `anthropic-skills:` 开头的 skill 文件夹或命令文件不会加载。请参阅 [为同步 skills 保留的名称](#names-reserved-for-synced-skills)。
* **命令文件**：`.claude/commands/` 中的 Markdown 文件是较旧的格式，仍然有效。它支持相同的 [frontmatter](#frontmatter-reference)，除了 `name` 和 `paths`。要找到您输入以调用它的名称，请参阅 [skill 如何获得其命令名称](#how-a-skill-gets-its-command-name)。对于新工作，更倾向于使用 skill，因为 skills 还支持 [支持文件](#add-supporting-files)。
* **Skill 文件夹作为插件**：将 `.claude-plugin/plugin.json` 添加到 skill 文件夹，它将作为 [插件](/docs/zh-CN/plugins/loading#plugins-shared-through-a-repository) 加载，名称为 `<name>@skills-dir`，因此它可以捆绑代理、hooks 和 MCP 服务器。在项目的 `.claude/skills/` 中，这需要首先接受工作区信任对话框。

<h3 id="discovery-from-parent-and-nested-directories">
  在 monorepos 和子目录中加载 skills
</h3>

Claude Code 从启动它的目录和每个父目录（直到存储库根目录）中的 `.claude/skills/` 加载项目 skills，因此在 `packages/frontend/` 中启动仍会获取在根目录定义的 skills。当您在 v2.1.246 或更高版本上 [使用 `/cd` 移动会话](/docs/zh-CN/permissions#move-the-session-to-another-directory) 时，Claude Code 会添加新目录的项目 skills。

在链接的 [git worktree](/docs/zh-CN/worktrees) 中运行的会话中，Claude Code 仅在 worktree 根目录之前搜索父目录。在 Claude Code v2.1.277 或更高版本上，当 worktree 检出在其根目录没有 `.claude/skills` 目录时，Claude Code 会改为加载主检出的项目 skills。请参阅 [worktrees 与主检出共享的内容](/docs/zh-CN/worktrees#what-worktrees-share-with-the-main-checkout)。

`.claude/skills/` 目录中启动位置下方的 skills 在启动时不会加载。它们在 Claude 首次读取或编辑该子目录中的文件时加载，并在会话的其余时间保持可用。在此之前，它们不会出现在 `/` 菜单中，您也无法按名称调用它们。要更早加载它们，请使用子目录的路径运行 `/add-dir`，这需要 Claude Code v2.1.257 或更高版本。

当嵌套 skill 的目录名称与另一个 skill 的名称匹配时，两者都保持可用。在存储库根目录有一个 `deploy` skill，在 `apps/web/.claude/skills/` 中有另一个：

* `/deploy` 运行根 skill。Claude Code 还为 Claude 列出目录限定的变体，并指示调用其目录包含它正在处理的文件的那个，因此嵌套 skill 仍然适用于 `apps/web/` 中的工作。
* `/apps/web:deploy` 单独运行嵌套 skill。其描述命名了它适用的目录。

<h3 id="skills-from-additional-directories">
  从项目外的目录加载 skills
</h3>

当您使用 `--add-dir` 或 `/add-dir` 添加目录时，Claude Code 会加载该目录的 `.claude/skills/` 中的 skills，以及其 `.claude/commands/` 和 `.claude/agents/`。Agent SDK 通过 TypeScript 中的 [`additionalDirectories`](/docs/zh-CN/agent-sdk/typescript#options) 或 Python 中的 [`add_dirs`](/docs/zh-CN/agent-sdk/python#claudeagentoptions) 添加的目录以相同方式加载，因为 SDK 将它们作为 `--add-dir` 传递。`settings.json` 中的 `permissions.additionalDirectories` 设置仅授予文件访问权限，不加载这些中的任何一个。

Claude Code 在启动时使用 `--add-dir` 传递的目录中监视 `.claude/skills/`，如 [在会话期间编辑 skill](#live-change-detection) 所述。它不监视添加目录的 `.claude/commands/` 或 `.claude/agents/`，因此在更改该处的文件后重新启动会话。

这些加载取决于 `project` [设置源](/docs/zh-CN/agent-sdk/claude-code-features#control-filesystem-settings-with-settingsources)，默认情况下处于启用状态。[`strictPluginOnlyCustomization`](/docs/zh-CN/settings-reference#strictpluginonlycustomization) 策略、[bare mode](/docs/zh-CN/headless#start-faster-with-bare-mode) 和 [`--safe-mode`](/docs/zh-CN/cli-reference#cli-flags) 各自进一步限制它们，如这些页面所述。请参阅 [其他目录授予文件访问权限，而不是配置](/docs/zh-CN/permissions#additional-directories-grant-file-access-not-configuration) 以获取添加目录加载的完整表格，包括 `CLAUDE.md` 和插件设置。

<h3 id="resolve-skills-that-share-a-name">
  解决共享名称的 skills
</h3>

当两个 skills 共享目录或文件名称时，每个来自的位置决定了 `/name` 运行哪一个。对于由 frontmatter `name` 字段设置的名称，请参阅 [skill 如何获得其命令名称](#how-a-skill-gets-its-command-name)。该表涵盖 enterprise、personal、project、nested、plugin 和 claude.ai 位置、捆绑 skills 和命令文件：

| 相同名称在 | 运行哪一个 |
| :- | :- |
| Enterprise、personal 和 project 中的两个 | Enterprise 优先于 personal，personal 优先于 project。在 `~/.claude/skills/` 和项目的 `.claude/skills/` 中都有 `deploy` 时，`/deploy` 运行 personal 的 |
| 这些位置中的任何一个和 [捆绑 skill](#bundled-skills) | 您的 skill 替换捆绑命令，但不替换其别名。项目 `code-review` skill 替换 `/code-review`，捆绑别名 `/review` 永远不会运行您的 skill |
| Skill 和 `.claude/commands/` 中的文件 | Skill |
| 项目根 skill 和嵌套 skill | 两者都加载。请参阅 [monorepos 和子目录](#discovery-from-parent-and-nested-directories) |
| 插件 skill 和上述任何位置的 skill | 两者都加载，因为插件 skills 被命名为 `/plugin-name:skill-name` |
| 上述任何一个和 [从您的 claude.ai 账户同步的 skill](#how-synced-skills-behave) 的短名称 | 其他 skill 或命令。同步 skill 随后被列出并仅在其完整名称下运行。请参阅 [当同步 skill 名称与另一个命令匹配时](#when-a-synced-skill-name-matches-another-command) |

<h3 id="skills-in-cowork-and-cloud-sessions">
  在 Cowork 和云会话中使用 skills
</h3>

[Cowork](https://claude.com/product/cowork) 会话和 [云会话](/docs/zh-CN/cloud-environments#what-carries-over-from-your-setup)（包括 [routines](/docs/zh-CN/routines)）不会读取您机器上的 `~/.claude/skills/`。交互式和计划的 Cowork 会话都加载为您的 claude.ai 账户启用的 skills，在会话启动时同步；从 Desktop 应用侧边栏中的 **Customize** 或从 claude.ai 上的 skills 设置管理它们。云会话另外加载提交到克隆存储库的 `.claude/skills/` 的项目 skills。

如果 skill 仅存在于您机器上的 `~/.claude/skills/` 中，当 [routine](/docs/zh-CN/routines) 调用它时，Claude Code 会报告找不到该 skill，因为每个 routine 运行都作为新的云会话启动。要在这些会话中使用个人 skill：

* 对于 Cowork 和云会话，为您的 claude.ai 账户启用该 skill。
* 对于云会话，您可以改为将 skill 提交到存储库的 `.claude/skills/`。在存储库的 `.claude/settings.json` 中声明的插件和仅在您的用户设置中启用的插件 [不会在云会话中加载](/docs/zh-CN/cloud-environments#what-carries-over-from-your-setup)。

[Desktop 计划任务](/docs/zh-CN/desktop-scheduled-tasks) 在您的机器上本地运行，因此它们确实加载 `~/.claude/skills/`。

<h3 id="how-synced-skills-behave">
  从 claude.ai 同步的 Skills
</h3>

如果您使用 Cowork 或云会话，或使用 claude.ai 账户在终端中登录 Claude Code，本部分适用于您。在这些会话中，Claude Code 加载为您的 claude.ai 账户启用的 skills，无需您进行任何设置，如 [同步 skills 加载的位置](#where-synced-skills-load) 所述。这些 skills 包括您在 claude.ai 设置中创建或打开的 skills、您的组织在那里提供的 skills 以及 Anthropic 的内置 skills，例如 `pdf` 和 `xlsx`。

Claude Code 从您的账户下载同步 skill，而不是读取您在会话运行的机器上编写的文件，因此它对同步 skills 应用不适用于您存储在 [skills 位置](#where-skills-live) 中的 skills 的规则。

<h4 id="where-synced-skills-load">
  同步 skills 加载的位置
</h4>

在 Cowork 或云会话中，Claude Code 加载为您的 claude.ai 账户启用的 skills，[Cowork 和云会话中的 Skills](#skills-in-cowork-and-cloud-sessions) 说明了如何选择这些会话获得哪些 skills。

在您的终端中，Claude Code 在您使用 claude.ai 账户登录的会话中同步这些 skills。会话启动时，Claude Code 在后台将您账户的 skills 下载到 `~/.claude/skills/synced/` 中，然后在会话运行时大约每 10 分钟检查一次 claude.ai 是否有更改。当检查发现 skill 在 claude.ai 上被添加、编辑或关闭时，Claude Code 在运行的会话中添加、更新或删除它，无需重新启动。终端会话中的同步需要 Claude Code v2.1.273 或更高版本。

同步永远不会延迟启动，因为 Claude 仅在调用 skill 时等待其下载。因此，短 [非交互式](/docs/zh-CN/headless) 运行可能在新添加的 skill 下载之前完成，在这种情况下，稍后的会话会下载它。要使非交互式运行下载您的 skills 并在回答提示之前等待列表，请将 [`CLAUDE_CODE_SYNC_SKILLS`](/docs/zh-CN/env-vars#variables) 设置为 `1`。

Claude Code 仅在使用您的 claude.ai 账户登录的会话中同步，并 [从 Anthropic 获取功能标志](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching)。它不在这些会话中同步：

* 不使用由 `/login` 存储的登录的会话，例如使用 API 密钥进行身份验证的会话，或 `ANTHROPIC_AUTH_TOKEN`、`CLAUDE_CODE_OAUTH_TOKEN` 或 `apiKeyHelper` 脚本提供凭证的会话
* 不获取功能标志的会话，例如 Amazon Bedrock 上的会话或您设置 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 的会话
* [bare mode](/docs/zh-CN/headless#start-faster-with-bare-mode) 中的会话或您使用 `--safe-mode` 启动的会话
* 您的组织的托管设置 [将 skills 锁定到插件源](/docs/zh-CN/settings-reference#strictpluginonlycustomization-skills) 的会话，或您使用 [`--setting-sources`](/docs/zh-CN/cli-reference#cli-flags) 列表启动的会话，该列表省略了 `user`

如果您在会话期间使用 `/login` 登录，请重新启动 Claude Code 以开始同步。

较早会话同步的 skills 保留在磁盘上。Claude Code 在稍后登录到同一账户的会话中加载它们，即使它无法到达 claude.ai。

Claude Code 下载同步 skills，从不上传它们。如果您或 Claude 编辑 `~/.claude/skills/synced/` 下的文件，更改不会保存到您的 claude.ai 账户，稍后的同步可能会覆盖或删除它。要更改同步 skill，请在 claude.ai 上更新它；下一次同步会下载新版本。

要查看哪些 skills 已同步，请运行 `/skills`。菜单在 `claude.ai sync` 下列出它们。

Anthropic 的某些 skills，例如 `pdf` 和 `xlsx`，总是同步。对于其余的，在 claude.ai 上的 skills 设置中打开或关闭 skill 以更改是否同步。

要停止在机器上同步，请在您的用户设置中将 [`syncClaudeAiSkills`](/docs/zh-CN/settings-reference#syncclaudeaiskills) 设置为 `false`。Claude Code 停止下载，下次启动时它会将已同步的 skills 移动到 `~/.claude/skills/.trash/`，不再加载它们。您的组织可以通过在 claude.ai 上关闭 Skills 来为所有人关闭同步。要在保持 Skills 打开的情况下停止同步，它可以在 [托管设置](/docs/zh-CN/managed-settings) 中设置相同的密钥。

如果您的组织在 claude.ai 上关闭 Skills，Claude Code 会删除下载的 skills，它们停止加载。删除的 skills 移动到 `~/.claude/skills/.trash/`，您可以在 [保留扫描](/docs/zh-CN/claude-directory#cleaned-up-automatically) 删除它们之前恢复文件。一旦您的组织重新打开 Skills，Claude Code 会在下一次同步时下载您启用的 skills。

<h4 id="when-a-synced-skill-name-matches-another-command">
  当同步 skill 名称与另一个命令匹配时
</h4>

您可以通过其短名称 `/<name>` 或完整名称 `/anthropic-skills:<name>` 调用同步 skill。当另一个命令使用短名称时，`/<name>` 运行另一个命令，同步 skill 仅作为 `/anthropic-skills:<name>` 运行。使用本地 `deploy` skill 和同步 `deploy` 时，`/deploy` 运行本地 skill，`/anthropic-skills:deploy` 运行同步的。在 v2.1.269 之前，同步 skill 仅有其短名称。

在 `/` 菜单、`/skills` 和 `/context` 中，同步 skill 出现在其短名称下，或在另一个命令使用短名称时出现在其完整名称下。在您的会话中运行 `/skills`。列表下的注释解释了每个失去其短名称的同步 skill。如果您在 `~/.claude/` 中的个人 skills 或命令文件之一使用该名称，注释还会说明要重命名或删除什么以释放它。

从 v2.1.269 到 v2.1.280，这些列表在其完整名称下显示每个同步 skill，`/skills` 没有这样的注释；两者都在 v2.1.281 中更改。

使用短名称的命令可以是以下任何一个：

* 内置命令或 [捆绑 skill](#bundled-skills)，包括在您的会话中不可用的，例如在您关闭捆绑 skills 后
* 任何 [本地级别](#where-skills-live) 的 skill 或 `.claude/commands/` 中的文件
* 插件 skill
* [MCP 提示](/docs/zh-CN/mcp#use-mcp-prompts-as-commands)

Claude Code 标记同步 skills，以便您可以看出它们来自何处。`/skills` 菜单和 `/context` 在 `claude.ai sync` 下分组同步 skills，`/` 命令菜单将它们标记为来自 claude.ai。

比较名称时，Claude Code 忽略大小写、间距和不可见字符，并将兼容性形式（如全宽字母和破折号变体）视为其纯等效形式。例如，名为 `Commit` 的同步 skill 和名为 `commit` 的本地 skill 计为相同名称，因此 `/commit` 继续运行您的本地 skill。

仅因另一个字母表中的相似字母而不同的名称计为不同名称，`claude.ai sync` 标签是您区分两者的方式。这些检查和标签需要 Claude Code v2.1.228 或更高版本。

<h4 id="names-reserved-for-synced-skills">
  为同步 skills 保留的名称
</h4>

Claude Code 保留名称 `anthropic-skills` 和该命名空间内的每个名称（例如 `anthropic-skills:pdf`）用于从 claude.ai 同步的 skills，因此同步 skill 的完整名称永远不会运行其他任何东西。该名称在每个会话中保留，无论您是否使用 claude.ai 账户登录。

* **Skill 文件夹、frontmatter `name`、`.claude/commands/` 中的文件或子文件夹，或 [保存的工作流](/docs/zh-CN/workflows#save-the-workflow-for-reuse)**：它不加载。[启动通知](/docs/zh-CN/errors#a-skill-command-or-workflow-wasnt-loaded-because-its-name-is-reserved) 命名要重命名或编辑的第一项。
* **名为 `anthropic-skills` 的插件**：它加载。当其 skills 之一和同步 skill 都命名为 `<name>` 时，`/anthropic-skills:<name>` 运行同步 skill。
* **名为 `anthropic-skills` 的 MCP 服务器**：它连接并且其工具有效，但 [其提示不显示为命令](/docs/zh-CN/mcp#use-mcp-prompts-as-commands)。在您的 MCP 配置中重命名服务器以列出它们。

<h4 id="how-claude-code-handles-the-frontmatter-of-a-synced-skill">
  Claude Code 如何处理同步 skill 的 frontmatter
</h4>

Claude Code 对同步 skill 的 frontmatter 应用两条规则：

* Claude Code 在每种会话中都遵守 frontmatter，因此 `allowed-tools` 授予通过正常 [权限流](/docs/zh-CN/permissions) 进行。
* Claude Code 清理 skill 提供的显示文本，例如其描述。它删除控制字符，在到达 Claude 的文本（例如描述）中，它还转义尖括号，以便文本无法模仿 Claude Code 的内部格式。此清理需要 Claude Code v2.1.228 或更高版本。

<h4 id="how-claude-code-handles-the-body-of-a-synced-skill">
  Claude Code 如何处理同步 skill 的正文
</h4>

Claude Code 对同步 skill 的正文的处理取决于会话运行的位置：

* 在云会话中，正文保持本地 skill 具有的行为，因为会话在隔离容器中运行。
* 在您桌面上的 Cowork 会话中，正文保持本地 skill 具有的行为，除了 Claude Code 将每个 `!` 命令行替换为 [`disableSkillShellExecution` 占位符](#inject-dynamic-context)，就像它对您在那里提供的每个 skill 所做的那样。
* 在您机器上的任何其他会话中，Claude Code 不运行 [`!` 命令](#inject-dynamic-context)，不附加 `@` 引用命名的文件（就像它对本地 skill 所做的那样），不替换 `${CLAUDE_PROJECT_DIR}` 和 `${CLAUDE_SESSION_ID}` 占位符，因此 `@` 引用和两个占位符都作为文字文本到达 Claude。`!` 命令行也作为文字文本到达 Claude，或当 `disableSkillShellExecution` 打开时作为该占位符。此处理需要 Claude Code v2.1.228 或更高版本。

<h3 id="live-change-detection">
  在会话期间编辑 skill
</h3>

Claude Code 监视 skill 目录的文件更改，除了在 [bare mode](/docs/zh-CN/headless#start-faster-with-bare-mode) 中。当您在 `~/.claude/skills/`、项目 `.claude/skills/` 或 `--add-dir` 目录内的 `.claude/skills/` 中添加、编辑或删除 skill 时，Claude Code 在当前会话中获取更改，无需重新启动。

如果您创建了会话启动时不存在的顶级 skills 目录，请运行 [`/reload-skills`](/docs/zh-CN/commands#all-commands) 以获取您放在那里的 skills。Claude Code 还没有监视该目录，因此在稍后每次更改后再次运行 `/reload-skills`。

实时更改检测仅涵盖 `SKILL.md` 文本。对于也是 [插件](/docs/zh-CN/plugins/loading#plugins-shared-through-a-repository) 的 skill 文件夹，对 `hooks/`、`.mcp.json`、`agents/` 和 `output-styles/` 的更改需要 `/reload-plugins` 才能生效。

<h3 id="remove-a-skill">
  删除 skill
</h3>

删除 skill 的方式取决于它来自何处：

* **Personal 或 project skill**：删除 skill 的目录，`~/.claude/skills/<skill-name>/` 或 `.claude/skills/<skill-name>/`。Claude Code [在当前会话中从 `/skills` 中删除它](#live-change-detection)；Claude Code 已从中加载的内容遵循 [skill 内容生命周期](#skill-content-lifecycle)。
* **Enterprise skill**：管理员从 [托管设置目录](/docs/zh-CN/managed-settings#delivery-mechanisms) 内的 `.claude/skills/` 删除 skill 的目录，例如 Linux 上的 `/etc/claude-code/.claude/skills/<skill-name>/`。
* **Plugin skill**：从 `/plugin` 菜单禁用或卸载提供它的插件，或使用 `/plugin uninstall <plugin-name>@<marketplace-name>`。Claude Code 在 [更改应用](/docs/zh-CN/plugins/cli-reference#reload-plugins) 时或重新启动时卸载插件的 skills。
* **从 claude.ai 同步的 Skill**：在您 [启用它](#skills-in-cowork-and-cloud-sessions) 的同一位置为您的 claude.ai 账户关闭该 skill。Claude Code 在下一次 [同步您的 skills](#where-synced-skills-load) 时从 `~/.claude/skills/synced/` 中删除它。如果您改为手动删除目录，下一次同步会在 skill 在 claude.ai 上保持启用时再次下载它。
* **Bundled skill**：将 [`disableBundledSkills`](#bundled-skills) 设置为 `true` 以关闭捆绑 skills，或在 [`skillOverrides`](#override-skill-visibility-from-settings) 中将一个 skill 设置为 `"off"` 以隐藏它。

要保留 personal 或 project skill 但阻止 Claude 自动调用它，请在其 frontmatter 中设置 [`disable-model-invocation: true`](#control-who-invokes-a-skill)，或在不想编辑文件时在 [`skillOverrides`](#override-skill-visibility-from-settings) 中设置 `"user-invocable-only"`。

<h2 id="configure-skills">
  配置 skills
</h2>

Skills 通过位于 `SKILL.md` 顶部的 YAML frontmatter 和随后的 markdown 内容进行配置。

<h3 id="types-of-skill-content">
  Skill 内容的类型
</h3>

Skill 文件可以包含任何说明，但思考你想如何调用它们有助于指导应该包含什么内容：

**参考内容**添加 Claude 应用于你当前工作的知识。约定、模式、风格指南、领域知识。此内容以内联方式运行，以便 Claude 可以将其与你的对话上下文一起使用。

```yaml theme={null}
---
name: api-conventions
description: API design patterns for this codebase
---

When writing API endpoints:
- Use RESTful naming conventions
- Return consistent error formats
- Include request validation
```

**任务内容**为 Claude 提供特定操作的分步说明，如部署、提交或代码生成。这些通常是你想直接使用 `/skill-name` 调用的操作，而不是让 Claude 决定何时运行它们。添加 `disable-model-invocation: true` 以防止 Claude 自动触发它。下面的示例添加了 `context: fork`，它在自己的子代理上下文中运行 skill；请参阅[在子代理中运行 skills](#run-skills-in-a-subagent)。

```yaml theme={null}
---
name: deploy
description: Deploy the application to production
context: fork
disable-model-invocation: true
---

Deploy the application:
1. Run the test suite
2. Build the application
3. Push to the deployment target
```

保持正文本身简洁。一旦 skill 加载，其内容[在多个回合中保持在上下文中](#skill-content-lifecycle)，所以每一行都是一个重复的令牌成本。说明要做什么，而不是叙述如何或为什么做，并应用与[CLAUDE.md 内容](/docs/zh-CN/best-practices#write-an-effective-claude-md)相同的简洁性测试。

<h3 id="frontmatter-reference">
  Frontmatter 参考
</h3>

使用位于 `SKILL.md` 文件顶部 `---` 标记之间的 YAML [frontmatter](/docs/zh-CN/glossary#frontmatter) 配置 skill，并在关闭 `---` 后将 skill 的说明写成 Markdown。字段名称使用由连字符分隔的小写单词，除了 `when_to_use`。`.claude/commands/` 中的[命令文件](#where-skills-live)接受相同的字段，除了 `name` 和 `paths`。此示例设置四个字段：

```yaml theme={null}
---
name: my-skill
description: What this skill does
disable-model-invocation: true
allowed-tools: Read Grep
---

Your skill instructions here...
```

所有字段都是可选的。只有 `description` 是推荐的，以便 Claude 知道何时使用该 skill。字段名称必须与表格完全匹配，包括连字符：Claude Code 会忽略它不识别的字段而不报告错误。

Claude Code 仅在开始 `---` 是文件的第一行时读取 frontmatter。否则，它将整个文件（包括 `---` 标记）视为 skill 内容。如果标记之间的 YAML 无法解析，skill 仍然加载但没有设置字段；请参阅[Skill 未触发](#skill-not-triggering)以查找并修复错误。

布尔字段接受 `yes`、`no`、`on`、`off`、`1` 和 `0`（任何字母大小写），以及 `true` 和 `false`。在 v2.1.218 之前，Claude Code 仅识别 `true` 和 `false`。

| 字段 | 必需 | 描述 |
| :- | :- | :- |
| `name` | 否 | 在 `/` 菜单中显示的命令名称。默认为目录名称。请参阅[skill 如何获得其命令名称](#how-a-skill-gets-its-command-name)以了解该字段如何与你键入以调用 skill 的名称交互。 |
| `description` | 推荐 | skill 的功能以及何时使用它。Claude 使用此信息来决定何时应用该 skill。如果省略，则使用 markdown 内容的第一个非空行。首先放置关键用例：组合的 `description` 和 `when_to_use` 文本在 skill 列表中被截断为 1,536 个字符以减少上下文使用。 |
| `when_to_use` | 否 | 关于 Claude 何时应调用该 skill 的其他上下文，例如触发短语或示例请求。附加到 skill 列表中的 `description`，并计入 1,536 字符的上限。 |
| `argument-hint` | 否 | 在自动完成期间显示的提示，以指示预期的参数。示例：`[issue-number]` 或 `[filename] [format]`。 |
| `arguments` | 否 | 用于 skill 内容中[`$name` 替换](#available-string-substitutions)的命名位置参数。接受以空格分隔的字符串或 YAML 列表。名称按顺序映射到参数位置。 |
| `disable-model-invocation` | 否 | 设置为 `true` 以防止 Claude 自动加载此 skill。用于你想使用 `/name` 手动触发的工作流。还防止 skill 被[预加载到子代理中](/docs/zh-CN/sub-agents#preload-skills-into-subagents)。从 v2.1.196 开始，还防止 skill 在[计划任务](/docs/zh-CN/scheduled-tasks)以该 skill 作为其提示触发时运行。默认值：`false`。 |
| `user-invocable` | 否 | 当仅 Claude 应调用该 skill 时设置为 `false`：Claude Code 将其从 `/` 菜单中隐藏，并且当你键入 `/name` 时不运行它。用于用户不应直接调用的背景知识。默认值：`true`。 |
| `allowed-tools` | 否 | Claude 在调用此 skill 的回合中可以使用而无需请求许可的工具。当你发送下一条消息时，授权将被清除。接受以空格或逗号分隔的字符串或 YAML 列表。请参阅[为 skill 预先批准工具](#pre-approve-tools-for-a-skill)。 |
| `disallowed-tools` | 否 | 此 skill 处于活动状态时从 Claude 的可用工具池中删除的工具。用于不应调用某些工具的自主 skills，例如用于后台循环的 `AskUserQuestion`。接受以空格或逗号分隔的字符串或 YAML 列表。当你发送下一条消息时，限制将被清除。与拒绝规则一样，该字段在任何其他工具保持时无法删除[`EndConversation`](/docs/zh-CN/tools-reference#endconversation-tool-behavior)。 |
| `model` | 否 | 此 skill 处于活动状态时要使用的模型。覆盖适用于当前回合的其余部分，不会保存到设置。当你发送下一个提示时，会话模型恢复。接受与[`/model`](/docs/zh-CN/model-config)相同的值，或 `inherit` 以保持活动模型。你的组织的[`availableModels`](/docs/zh-CN/model-config#restrict-model-selection)允许列表排除的值不会被使用，会话保持其当前模型。在[自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)中，以及在[计划模式中，当分类器审查命令时](/docs/zh-CN/permission-modes#analyze-before-you-edit-with-plan-mode)，自动模式不支持的模型也不会被使用，会话保持其当前模型。使用 `context: fork` 时，该值设置[分叉子代理的模型](#run-skills-in-a-subagent)，而被排除的值遵循[与子代理模型覆盖相同的规则](/docs/zh-CN/model-config#restrict-model-selection)。 |
| `effort` | 否 | 此 skill 处于活动状态时的[工作量级别](/docs/zh-CN/model-config#adjust-effort-level)。覆盖会话工作量级别。默认值：从会话继承。选项：`low`、`medium`、`high`、`xhigh`、`max`；可用级别取决于模型。 |
| `context` | 否 | 设置为 `fork` 以在分叉子代理上下文中运行。请参阅[在子代理中运行 skills](#run-skills-in-a-subagent)。 |
| `agent` | 否 | 设置 `context: fork` 时要使用的子代理类型。 |
| `background` | 否 | 仅适用于 `context: fork`。设置为 `false` 以在调用 skill 的回合中等待分叉子代理的结果，而不是[在后台运行它](#run-skills-in-a-subagent)。默认值：`true`。需要 Claude Code v2.1.218 或更高版本。 |
| `hooks` | 否 | Claude Code 在调用 skill 时注册并在会话的其余部分保持运行的 hooks。请参阅[skills 和代理中的 hooks](/docs/zh-CN/hooks#hooks-in-skills-and-agents)以了解配置格式和 `once` 选项。 |
| `paths` | 否 | 限制何时激活此 skill 的 Glob 模式。接受以逗号分隔的字符串或 YAML 列表。设置后，Claude 仅在处理与模式匹配的文件时自动加载该 skill。使用与[路径特定规则](/docs/zh-CN/memory#path-specific-rules)相同的格式。 |
| `shell` | 否 | 用于此 skill 中的 `` !`command` `` 和 ` ```! ` 块的 shell。接受 `bash`（默认）或 `powershell`。设置 `powershell` 在启用[PowerShell 工具](/zh-CN/tools-reference#powershell-tool)时通过 PowerShell 运行内联 shell 命令：在没有 Git Bash 的 Windows 上默认启用，在带有 Git Bash 的 claude.ai 和 Console 帐户上默认启用，在 Amazon Bedrock、Google Cloud 的 Agent Platform 和 Microsoft Foundry 会话以及 macOS、Linux 和 WSL 上需要 `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`。设置为 `0` 以关闭工具。 |
| `metadata` | 否 | 用于你自己的键值数据的自由格式 YAML 映射，例如权利或目录字段，由你自己的工具从 `SKILL.md` 读取。Claude Code 不对其内容进行操作，并删除不是映射的值。不要重用 frontmatter 字段名称（如 `paths`）作为键。 |
| `license` | 否 | 涵盖该 skill 的许可证。[Agent Skills](https://agentskills.io) 规范的一部分；请参阅[在 Claude Code 外使用 skill frontmatter](#using-skill-frontmatter-outside-claude-code)。Claude Code 接受该字段但不对其进行操作。 |
| `compatibility` | 否 | skill 的环境要求，例如预期的产品或系统先决条件，如[Agent Skills](https://agentskills.io) 规范所定义；请参阅[在 Claude Code 外使用 skill frontmatter](#using-skill-frontmatter-outside-claude-code)。接受最多 500 个字符的字符串。Claude Code 接受该字段但不对其进行操作。 |

<h4 id="using-skill-frontmatter-outside-claude-code">
  在 Claude Code 外使用 skill frontmatter
</h4>

Claude Code 接受上表中的每个字段。在 Claude Code 外，你只能使用[Agent Skills](https://agentskills.io) 规范中的字段：

| 分发路径 | 你可以使用的 Frontmatter 字段 |
| :- | :- |
| Claude Code skills 在[任何级别](#where-skills-live)，包括[插件](/docs/zh-CN/plugins/overview) skills | 上表中的每个字段 |
| claude.ai skill 上传、Skills API 和使用来自 [anthropics/skills](https://github.com/anthropics/skills) 的 `package_skill.py` 打包 | `name`、`description`、`license`、`compatibility`、`metadata`、`allowed-tools` |

当你为[Cowork 和云会话](#skills-in-cowork-and-cloud-sessions)启用个人 skill（包括例程）时，你将其上传到 claude.ai，因此适用相同的规则。

如果你包含规范不允许的任何字段，打包或上传将失败并出现硬错误，而不是忽略该字段：

```
Unexpected key(s) in SKILL.md frontmatter: argument-hint. Allowed properties are: allowed-tools, compatibility, description, license, metadata, name
```

将 frontmatter 限制为规范的六个字段可避免上述意外密钥错误。[Agent Skills 规范](https://agentskills.io)和[Skills API 要求](https://docs.claude.com/en/api/skills-guide)定义了这些路径验证的所有其他内容。Claude Code 特定的正文功能，例如[动态上下文注入](#inject-dynamic-context)，在 claude.ai 聊天或通过 API 中不起作用。Claude Code 接受所有六个字段，因此遵循规范的 frontmatter 在 Claude Code 中加载时无需更改。

<h4 id="how-a-skill-gets-its-command-name">
  skill 如何获得其命令名称
</h4>

你键入以调用 skill 的命令来自 skill 文件的位置，对于 skill 目录和插件 skills，还来自 frontmatter `name` 字段。在个人或项目 skill 目录中，`name` 设置 `/` 菜单显示的命令以及你键入的命令，除非另一个命令已使用该名称。目录名称也调用该 skill。在插件 skill 中，`name` 设置命令的最后一段，插件前缀保持不变。

下表显示了每个布局的命令名称来自何处：

| Skill 位置 | 命令名称来源 | 示例 |
| :- | :- | :- |
| `~/.claude/skills/` 或 `.claude/skills/` 下的 Skill 目录 | Frontmatter `name` 或目录名称 | `.claude/skills/deploy-staging/SKILL.md` → `/deploy-staging`，或使用 `name: deploy` 时为 `/deploy` |
| [嵌套](#where-skills-live)`.claude/skills/` 目录，当目录名称与另一个 skill 冲突时 | 相对于工作目录的子目录路径，然后是 skill 目录名称 | `apps/web/.claude/skills/deploy/SKILL.md` → `/apps/web:deploy` |
| `.claude/commands/` 下的文件 | 文件名（不含扩展名） | `.claude/commands/deploy.md` → `/deploy` |
| `.claude/commands/` 的子目录中的文件 | 相对于 `commands/` 的子目录路径，每个 `/` 替换为 `:`，然后是不含扩展名的文件名 | `.claude/commands/frontend/component.md` → `/frontend:component` |
| 插件 `skills/` 子目录 | Frontmatter `name` 或目录名称，由插件命名空间 | `my-plugin/skills/review/SKILL.md` → `/my-plugin:review`，或使用 `name: fancy` 时为 `/my-plugin:fancy` |
| 插件根 `SKILL.md` | Frontmatter `name`，以插件目录名称作为后备 | `my-plugin/SKILL.md` 带有 `name: review` → `/my-plugin:review`。请参阅[单个 skill 在插件根](/docs/zh-CN/plugins/components#skills) |
| 从 claude.ai [同步的 skill](#how-synced-skills-behave) | 你的 claude.ai 帐户上 skill 的名称，前缀为 `anthropic-skills:` | 帐户 skill `deploy` → `/anthropic-skills:deploy`，或在没有其他命令使用该名称时为 `/deploy` |

在插件 skill 中，frontmatter `name` 替换命令最后一段中的目录名称，因此 `my-plugin/skills/review/SKILL.md` 带有 `name: fancy` 变为 `/my-plugin:fancy`。裸 `/fancy` 也调用该 skill，除非另一个命令已使用该名称。如果你写的 `name` 已经以插件自己的前缀开头，Claude Code 在 v2.1.246 或更高版本上不会再次添加前缀。例如，`name: my-plugin:fancy` 仍然变为 `/my-plugin:fancy`。从 v2.1.216 到 v2.1.245，当 `name` 已经携带前缀时，Claude Code 会加倍前缀。

在[非交互式会话](/docs/zh-CN/headless)中，名称 `help` 和 `feedback` 不是为其仅限终端的内置命令保留的，因此具有其中一个名称的插件 skill 在那里保持其裸命令。每个其他仅限终端的内置命令的名称（如 `/login`）即使该命令无法在这些会话中运行，仍然保留。

对于插件根 `SKILL.md`，没有 skill 目录来获取名称，因此 `name` 提供整个最后一段。没有 `name` 字段，Claude Code 回退到插件的目录名称。

<h4 id="available-string-substitutions">
  可用的字符串替换
</h4>

Skills 支持 skill 内容中动态值的字符串替换：

| 变量 | 描述 |
| :- | :- |
| `$ARGUMENTS` | 调用 skill 时传递的所有参数。当没有占位符接收参数时，Claude Code 将它们附加为 `ARGUMENTS: <value>`。请参阅[将参数传递给 skills](#pass-arguments-to-skills)。 |
| `$ARGUMENTS[N]` | 按 0 基索引访问特定参数，例如 `$ARGUMENTS[0]` 表示第一个参数。 |
| `$N` | `$ARGUMENTS[N]` 的简写，例如 `$0` 表示第一个参数或 `$1` 表示第二个参数。 |
| `$name` | 在[`arguments`](#frontmatter-reference) frontmatter 列表中声明的命名参数。名称按顺序映射到位置，因此使用 `arguments: [issue, branch]`，占位符 `$issue` 扩展到第一个参数，`$branch` 扩展到第二个参数。 |
| `${CLAUDE_SESSION_ID}` | 当前会话 ID。用于日志记录、创建会话特定文件或将 skill 输出与会话关联。 |
| `${CLAUDE_EFFORT}` | 当前工作量级别：`low`、`medium`、`high`、`xhigh` 或 `max`。使用此来根据活动工作量设置调整 skill 说明。 |
| `${CLAUDE_SKILL_DIR}` | 包含 skill 的 `SKILL.md` 文件的目录。对于插件 skills，这是插件内 skill 的子目录，而不是插件根。在 bash 注入命令中使用此来引用与 skill 捆绑的脚本或文件，无论当前工作目录如何。 |
| `${CLAUDE_PROJECT_DIR}` | 项目根目录。这是与[hooks](/docs/zh-CN/hooks#reference-scripts-by-path)和 MCP 服务器相同的路径，作为 `CLAUDE_PROJECT_DIR` 接收。使用此来引用项目本地脚本或文件，例如 `${CLAUDE_PROJECT_DIR}/.claude/hooks/helper.sh`，独立于 skill 的安装位置。 |
| `${CLAUDE_PLUGIN_ROOT}` | 插件的安装目录。仅在插件 skills 中替换。使用此来引用插件中任何位置的脚本或文件，包括插件 skills 之间共享的资源。请参阅[插件环境变量](/docs/zh-CN/plugins/manifest-reference#environment-variables)。 |
| `${CLAUDE_PLUGIN_DATA}` | 插件的[持久数据目录](/docs/zh-CN/plugins/components#path-variables-and-persistent-data)，在插件更新后仍然存在。仅在插件 skills 中替换。使用此来引用已安装的依赖项、生成的文件或必须超过更新的缓存。 |

Claude Code 在两个地方替换 `${CLAUDE_SKILL_DIR}` 和 `${CLAUDE_PROJECT_DIR}`：skill 的 markdown 内容和[`allowed-tools`](#frontmatter-reference) frontmatter 中的 Bash 规则。在插件 skill 中，Claude Code 在相同的两个地方替换 `${CLAUDE_PLUGIN_ROOT}` 和 `${CLAUDE_PLUGIN_DATA}`。在两个地方使用相同的变量让 skill 运行捆绑的脚本而无需许可提示。以下 skill 显示了该模式：

```yaml theme={null}
---
name: render-chart
description: Render a chart from a CSV file
allowed-tools: Bash(${CLAUDE_SKILL_DIR}/scripts/render.sh *)
---

Run `${CLAUDE_SKILL_DIR}/scripts/render.sh <csv-file>` to render the chart.
```

如果此 skill 安装在 `~/.claude/skills/render-chart/`，`${CLAUDE_SKILL_DIR}` 的两个出现都扩展到该目录。`allowed-tools` 规则然后匹配 skill 正文告诉 Claude 运行的确切命令，因此脚本运行而无需提示。

`${CLAUDE_PROJECT_DIR}` 替换需要 Claude Code v2.1.196 或更高版本。

索引参数使用 shell 风格的引用，因此用引号包装多字值以将其作为单个参数传递。例如，`/my-skill "hello world" second` 使 `$0` 扩展到 `hello world`，`$1` 扩展到 `second`。`$ARGUMENTS` 占位符始终扩展到完整的参数字符串，如输入的那样。

没有对应参数的索引占位符，例如仅传递一个参数时的 `$2`，在内容中保持不变。来自[`arguments`](#frontmatter-reference) frontmatter 的没有匹配参数的命名占位符扩展为空字符串。

如果你传递的参数值本身包含文本（如 `$1` 或 `$ARGUMENTS`），Claude Code 将其作为文字文本插入，不会扩展它。例如，如果 skill 的正文包含 `Summarize $0`，你运行 `/summarize "$ARGUMENTS from yesterday"`，Claude 接收 `Summarize $ARGUMENTS from yesterday`。Claude Code 仍然在插入参数后替换 `${CLAUDE_*}` 变量（如 `${CLAUDE_SKILL_DIR}`）。

要在数字、`ARGUMENTS` 或声明的参数名称之前包含文字 `$`，例如散文中的 `$1.00`，用反斜杠转义它：`\$1.00`。任何其他 `$` 之前的反斜杠保持不变。仅直接在令牌之前的单个反斜杠转义它。双反斜杠（如 `\\$1`）在原地保留两个反斜杠，`$1` 仍然扩展到参数值。反斜杠转义仅涵盖这些参数占位符。反斜杠不会阻止 `${CLAUDE_*}` 变量的替换，其中变量适用。

**使用替换的示例：**

```yaml theme={null}
---
name: session-logger
description: Log activity for this session
---

Log the following to logs/${CLAUDE_SESSION_ID}.log:

$ARGUMENTS
```

<h3 id="add-supporting-files">
  添加支持文件
</h3>

Skills 可以在其目录中包含多个文件。这使 `SKILL.md` 专注于要点，同时让 Claude 仅在需要时访问详细的参考材料。大型参考文档、API 规范或示例集合不需要在每次 skill 运行时加载到上下文中。

```text theme={null}
my-skill/
├── SKILL.md (required - overview and navigation)
├── reference.md (detailed API docs - loaded when needed)
├── examples.md (usage examples - loaded when needed)
└── scripts/
    └── helper.py (utility script - executed, not loaded)
```

从 `SKILL.md` 引用支持文件，以便 Claude 知道每个文件包含什么以及何时加载它：

```markdown theme={null}
## Additional resources

- For complete API details, see [reference.md](reference.md)
- For usage examples, see [examples.md](examples.md)
```

<Tip>保持 `SKILL.md` 在 500 行以下。将详细的参考材料移到单独的文件。</Tip>

<h3 id="control-who-invokes-a-skill">
  控制谁调用 skill
</h3>

默认情况下，你和 Claude 都可以调用任何 skill。你可以键入 `/skill-name` 直接调用它，Claude 可以在与你的对话相关时自动加载它。两个 frontmatter 字段让你限制这一点：

* **`disable-model-invocation: true`**：仅你可以调用该 skill。用于具有副作用或你想控制时间的工作流，如 `/commit`、`/deploy` 或 `/send-slack-message`。你不希望 Claude 因为你的代码看起来准备好就决定部署。

* **`user-invocable: false`**：仅 Claude 可以调用该 skill。用于不可作为命令操作的背景知识。`legacy-system-context` skill 解释了旧系统的工作原理。Claude 在相关时应该知道这一点，但 `/legacy-system-context` 对用户来说不是一个有意义的操作。

此示例创建一个仅你可以触发的部署 skill。如果你设置 `disable-model-invocation: true`，Claude 无法自动运行该 skill：

```yaml theme={null}
---
name: deploy
description: Deploy the application to production
disable-model-invocation: true
---

Deploy $ARGUMENTS to production:

1. Run the test suite
2. Build the application
3. Push to the deployment target
4. Verify the deployment succeeded
```

如果 Claude 仍然尝试，Claude Code 会阻止该调用并指示它不要以另一种方式重现部署步骤，因此期望 Claude 建议你自己运行 `/deploy`。

以下是两个字段如何影响调用和上下文加载：

| Frontmatter | 你可以调用 | Claude 可以调用 | 何时加载到上下文中 |
| :- | :- | :- | :- |
| （默认） | 是 | 是 | 描述始终在上下文中，调用时加载完整 skill |
| `disable-model-invocation: true` | 是 | 否 | 描述不在上下文中，你调用时加载完整 skill |
| `user-invocable: false` | 否 | 是 | 描述始终在上下文中，调用时加载完整 skill |

<Note>
  在常规会话中，skill 描述被加载到上下文中，以便 Claude 知道什么可用，但完整 skill 内容仅在调用时加载。[具有预加载 skills 的子代理](/docs/zh-CN/sub-agents#preload-skills-into-subagents)的工作方式不同：完整 skill 内容在启动时注入。
</Note>

<h3 id="skill-content-lifecycle">
  Skill 内容生命周期
</h3>

当你或 Claude 调用 skill 时，渲染的 `SKILL.md` 内容作为单个消息进入对话，并在后续回合中保持在那里。此持久性适用于 skill 的说明，而不是其权限：[`allowed-tools`](#pre-approve-tools-for-a-skill) 授权在你发送下一条消息时被清除。Claude Code 不会在后续回合中重新读取 skill 文件，因此将应该在整个任务中应用的指导写成常设说明，而不是一次性步骤。

当 Claude 重新调用一个其渲染内容与已在上下文中的副本相同的 skill 时，Claude Code 添加一个简短的注释，说明该 skill 已加载，而不是内容的第二个副本。当渲染内容不同时，因为参数改变或[动态上下文](#inject-dynamic-context)命令产生了新输出，Claude Code 再次附加完整内容。

[自动压缩](/docs/zh-CN/how-claude-code-works#when-context-fills-up)在令牌预算内携带调用的 skills。当对话被总结以释放上下文时，Claude Code 在总结后重新附加每个 skill 的最新调用，保留每个的前 5,000 个令牌。重新附加的 skills 共享 25,000 个令牌的组合预算。Claude Code 从最近调用的 skill 开始填充此预算，因此如果你在一个会话中调用了许多，较旧的 skills 可能在压缩后完全被删除。

如果 skill 似乎在第一个响应后停止影响行为，内容通常仍然存在，模型选择其他工具或方法。加强 skill 的 `description` 和说明，以便模型继续偏好它，或使用[hooks](/docs/zh-CN/hooks)来确定性地强制行为。如果 skill 很大或你在它之后调用了其他几个，在压缩后重新调用它以恢复完整内容。

<h3 id="pre-approve-tools-for-a-skill">
  为 skill 预先批准工具
</h3>

`allowed-tools` 字段在调用 skill 的回合中为列出的工具授予权限，以便 Claude 可以使用它们而无需提示你批准。当你发送下一条消息时，授权被清除，即使 skill 内容[保持在上下文中](#skill-content-lifecycle)；再次调用 skill 会为该回合重新应用它。它不限制哪些工具可用：每个工具仍然可调用，你的[权限设置](/docs/zh-CN/permissions)仍然管理未列出的工具。要为整个会话而不是单个回合预先批准工具，请改为向这些权限设置添加允许规则。

工作区信任不会限制此字段。Claude Code 在你或 Claude 调用 skill 时应用项目 skill 的 `allowed-tools`，包括在你从未信任的文件夹中的 `-p` 运行。skill 可以授予自己广泛的工具访问权限，因此在你在那里运行 Claude Code 之前，查看检入存储库的 skills 的 `allowed-tools`。

此 skill 让 Claude 在你调用它时运行 git 命令而无需每次使用批准：

```yaml theme={null}
---
name: commit
description: Stage and commit the current changes
disable-model-invocation: true
allowed-tools: Bash(git add *) Bash(git commit *) Bash(git status *)
---
```

要在 skill 处于活动状态时从 Claude 的可用工具池中删除工具，在 skill 的 frontmatter 中的 `disallowed-tools` 中列出它们。当你发送下一条消息时，限制被清除。与拒绝规则一样，该字段在任何其他工具保持时无法删除[`EndConversation`](/docs/zh-CN/tools-reference#endconversation-tool-behavior)。要在所有 skills 和提示中阻止工具，在你的[权限设置](/docs/zh-CN/permissions)中添加拒绝规则。

<h3 id="pass-arguments-to-skills">
  将参数传递给 skills
</h3>

你和 Claude 都可以在调用 skill 时传递参数。参数可通过 `$ARGUMENTS` 占位符获得。

此 skill 按编号修复 GitHub 问题。`$ARGUMENTS` 占位符被替换为 skill 名称后面的任何内容：

```yaml theme={null}
---
name: fix-issue
description: Fix a GitHub issue
disable-model-invocation: true
---

Fix GitHub issue $ARGUMENTS following our coding standards.

1. Read the issue description
2. Understand the requirements
3. Implement the fix
4. Write tests
5. Create a commit
```

当你运行 `/fix-issue 123` 时，Claude 接收"Fix GitHub issue 123 following our coding standards..."

如果你使用参数调用 skill，但 skill 内容中没有占位符接收一个，Claude Code 将 `ARGUMENTS: <your input>` 附加到 skill 内容的末尾，以便 Claude 仍然看到你键入的内容。占位符是 `$ARGUMENTS`、索引形式（如 `$1`）或命名参数。没有其位置参数的索引占位符保持为文字文本，不计为接收一个。命名占位符计数，即使其位置没有参数，因为它扩展为空字符串。

你也可以在一条消息的开始处堆叠多个 skills。键入 `/write-tests /fix-issue 123` 加载两个 skills 并将尾随文本 `123` 作为 `$ARGUMENTS` 传递给每个。在 v2.1.199 之前，仅第一个 skill 加载并接收 `/fix-issue 123` 作为文字参数文本。

Claude Code 扩展第一个 skill 加上最多五个在其后堆叠的。扩展在第一个不是内联用户可调用 skill 的令牌处停止，因此作为[分叉子代理](#run-skills-in-a-subagent)运行的 skill（如[`/code-review`](/docs/zh-CN/code-review#review-a-diff-locally)）或其参数本身可能以斜杠命令开头的 skill（如 `/loop`）也在那里结束运行。该令牌和其后的所有内容成为每个扩展 skill 的参数文本。从 v2.1.218 开始，`/code-review` 作为分叉子代理运行；在早期版本上，它以内联方式运行并堆叠。

要按位置访问单个参数，使用 `$ARGUMENTS[N]` 或较短的 `$N`：

```yaml theme={null}
---
name: migrate-component
description: Migrate a component from one language to another
---

Migrate the $ARGUMENTS[0] component from $ARGUMENTS[1] to $ARGUMENTS[2].
Preserve all existing behavior and tests.
```

运行 `/migrate-component SearchBar JavaScript TypeScript` 将 `$ARGUMENTS[0]` 替换为 `SearchBar`，`$ARGUMENTS[1]` 替换为 `JavaScript`，`$ARGUMENTS[2]` 替换为 `TypeScript`。使用 `$N` 简写的相同 skill：

```yaml theme={null}
---
name: migrate-component
description: Migrate a component from one language to another
---

Migrate the $0 component from $1 to $2.
Preserve all existing behavior and tests.
```

<h2 id="advanced-patterns">
  高级模式
</h2>

<h3 id="inject-dynamic-context">
  注入动态上下文
</h3>

`` !`<command>` `` 语法在技能内容发送给 Claude 之前运行 shell 命令。命令输出替换占位符，因此 Claude 接收实际数据，而不是命令本身。当技能从你的 claude.ai 账户[同步](#how-claude-code-handles-the-body-of-a-synced-skill)时，Claude Code 不会在你的机器上运行这些命令。这个限制需要 Claude Code v2.1.228 或更高版本。

这个技能通过使用 GitHub CLI 获取实时 PR 数据来总结拉取请求。`` !`gh pr diff` `` 和其他命令首先运行，它们的输出被插入到提示中：

```yaml theme={null}
---
name: pr-summary
description: Summarize changes in a pull request
context: fork
agent: Explore
allowed-tools: Bash(gh *)
---

## Pull request context
- PR diff: !`gh pr diff`
- PR comments: !`gh pr view --comments`
- Changed files: !`gh pr diff --name-only`

## Your task
Summarize this pull request...
```

替换在原始文件上运行一次。命令输出作为纯文本插入，不会重新扫描以查找进一步的 `` !`<command>` `` 占位符，因此命令无法为后续传递发出占位符来扩展。

内联形式仅在 `!` 出现在行首或紧跟在空格后时被识别。如果 `!` 跟在另一个字符后面，如 `` KEY=!`cmd` ``，占位符保留为字面文本，命令不运行。

对于多行命令，使用以 ` ```! ` 开头的围栏代码块而不是内联形式：

````markdown theme={null}
## Environment
```!
node --version
git status --short
```
````

要为来自用户、项目、插件或[附加目录](#skills-from-additional-directories)源的技能和自定义命令禁用此行为，请在[设置](/docs/zh-CN/settings)中设置 `"disableSkillShellExecution": true`。每个命令都被替换为 `[shell command execution disabled by policy]` 而不是被运行。捆绑和托管技能不受影响。此设置在[托管设置](/docs/zh-CN/managed-settings)中最有用，用户无法覆盖它。

当命令出现在从你的 claude.ai 账户[同步](#how-synced-skills-behave)的技能中时，Claude Code 永远不会在你的机器上运行这些命令，无论此设置如何。这个限制需要 Claude Code v2.1.228 或更高版本。[Claude Code 如何处理同步技能的主体](#how-claude-code-handles-the-body-of-a-synced-skill)说明了在每种会话中 Claude 接收什么来代替命令。

<Tip>
  要在技能运行时请求更深入的推理，请在技能内容中的任何地方包含 `ultrathink`。请参阅[使用 ultrathink 进行一次性深入推理](/docs/zh-CN/model-config#use-ultrathink-for-one-off-deep-reasoning)。
</Tip>

<h4 id="how-injected-commands-run">
  注入命令如何运行
</h4>

Claude Code 从技能的 frontmatter 中的 `shell` 键和你的环境中选择运行技能的注入命令的工具。除了一个会直接导致调用失败的组合外，每个组合都通过 Bash 工具或 PowerShell 工具运行命令：

* `shell: powershell`，启用了 [PowerShell 工具](/docs/zh-CN/tools-reference#powershell-tool)：命令通过 PowerShell 工具运行。
* `shell: bash` 当 bash 不可用时：调用在任何命令运行之前失败。这发生在没有 Git Bash 的 Windows 上。Claude Code 显示 ``Skill <name> requires bash (`shell: bash` in frontmatter) but Git Bash was not found``。
* 任何其他组合：当 bash 可用时，命令通过 Bash 工具运行。当它不可用时，它们通过 PowerShell 工具运行。

任一工具运行命令的方式与它运行 Claude 自己的 shell 命令的方式相同。它们共享工作目录、超时和输出处理：

* **工作目录**：Claude Code 在会话 shell 的当前工作目录中运行每个命令。当 Claude 运行 `cd` 时，该目录会移动。在必须每次都以相同方式解析的路径中使用 [`${CLAUDE_SKILL_DIR}` 或 `${CLAUDE_PROJECT_DIR}`](#available-string-substitutions)。
* **stderr**：使用默认的 `bash` shell，Claude Code 将 stderr 合并到 stdout。命令写入 stderr 的任何内容都会出现在注入的文本中。
* **超时**：每个命令在 Bash 工具的默认 2 分钟[超时](/docs/zh-CN/tools-reference#timeout-and-output-limits)下运行。当 Bash 工具[将超时的命令移到后台](/docs/zh-CN/tools-reference#foreground-commands-that-move-to-the-background)时，技能仍然呈现。注入的文本报告移动并命名后台任务和收集命令输出的文件。当命令是 Bash 工具从不自动后台化的命令之一时，Claude Code 在超时时杀死它。该失败[中止调用](#when-an-injected-command-fails)。
* **输出大小**：超过 Bash 工具内联上限的输出作为文件路径加短预览到达，而不是截断的文本。[输出限制](/docs/zh-CN/tools-reference#output-limits)涵盖上限以及如何调整每个边界。

PowerShell 工具对它运行的命令应用相同的超时、后台化和输出上限行为。有关其具体信息，请参阅 [PowerShell 工具](/docs/zh-CN/tools-reference#powershell-tool)部分。

<h4 id="when-an-injected-command-fails">
  当注入命令失败时
</h4>

失败的命令中止整个技能调用，而不仅仅是其自己的占位符。Claude 永远看不到该调用的技能内容。中止显示 `Shell command failed for pattern "..."`。错误消息包括命令的输出在 `[stderr]` 下。

使用默认的 `bash` shell，任何非零退出代码都算作失败。一个例外适用：Claude Code 将来自[搜索和比较命令](/docs/zh-CN/tools-reference#output-limits)的退出代码 1 视为正常结果并注入其输出。退出代码 2 或更高的代码即使对于这些命令也会失败。

哪些命令获得例外取决于 shell：

* 默认 `bash` shell：[输出限制](/docs/zh-CN/tools-reference#output-limits)下列出的命令
* `shell: powershell`，当启用 PowerShell 工具时：一个[不同的集合](/docs/zh-CN/tools-reference#shell-selection-in-settings-hooks-and-skills)，包括 `grep` 和 `git diff` 但不包括 `find` 或 `diff`

使用默认的 `bash` shell，将 `|| true` 附加到任何你期望退出非零的其他命令。一个在发现问题时退出 1 的检查脚本就是一个例子。

<h4 id="permission-checks-on-injected-commands">
  注入命令的权限检查
</h4>

注入命令在技能呈现时永远不会提示权限。Claude Code 首先根据你的[权限规则](/docs/zh-CN/permissions)检查每一个。命令与拒绝规则匹配的命令会中止调用，显示 `Shell command permission check failed for pattern "..."`。

在[自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)之外，当命令的权限检查返回除允许之外的任何内容时，Claude Code 会中止调用。这包括通常会询问你的规则。要防止不匹配的命令在此处中止，请使用 [`allowed-tools`](#pre-approve-tools-for-a-skill) 预先批准它。拒绝和询问规则仍然会覆盖 `allowed-tools`。请参阅[管理权限](/docs/zh-CN/permissions#manage-permissions)。

在自动模式中，原本需要你批准的命令不会中止调用。技能加载时带有指令，告诉 Claude 首先运行该命令，然后 Claude 自己的调用通过[自动模式的常规检查](/docs/zh-CN/permission-modes#how-the-classifier-evaluates-actions)。调用仍然会在[分叉技能](#run-skills-in-a-subagent)中中止，该技能设置 `agent`，以及在 Claude 没有[运行注入命令的 shell 工具](#how-injected-commands-run)的会话中。

<h3 id="run-skills-in-a-subagent">
  在子代理中运行技能
</h3>

当你希望技能在隔离中运行时，将 `context: fork` 添加到你的 frontmatter。Claude Code 启动 `agent` 字段中设置的类型的新子代理，并将技能内容作为其提示提供给它。子代理看不到你的对话历史，因此技能的说明必须独立存在。

<Note>
  尽管名称如此，具有 `context: fork` 的技能不会在[当前对话的分叉](/docs/zh-CN/sub-agents#fork-the-current-conversation)中运行，这会将你迄今为止讨论的所有内容交给子代理。当任务依赖于该历史时，分叉对话而不是使用 `context: fork`。
</Note>

分叉的子代理在[后台](/docs/zh-CN/sub-agents#run-subagents-in-foreground-or-background)运行：你继续工作，而它运行，其结果在完成时到达你的对话。在 frontmatter 中设置 `background: false` 以改为在调用技能的轮次中等待结果。在 v2.1.218 之前，分叉的技能总是阻止轮次直到它们完成。

Claude Code 也会等待结果，即使技能没有设置 `background: false`，在这些情况下：

* 在非交互模式中，使用 `-p` 标志或 Agent SDK
* 当你将 [`CLAUDE_CODE_DISABLE_BACKGROUND_TASKS`](/docs/zh-CN/env-vars) 设置为 `1` 时，这也会关闭所有其他后台任务功能
* 当你在同一技能的早期调用仍在运行时调用分叉技能时
* 当[计划任务](/docs/zh-CN/scheduled-tasks)以技能作为其提示触发时

后台化的分叉也使用[适用于后台子代理的更窄工具集](/docs/zh-CN/sub-agents#run-subagents-in-foreground-or-background)运行：技能的子代理是常规代理类型，因此分叉对话的子代理的豁免不适用于它。如果你的技能的步骤依赖于该集合之外的工具，请设置 `background: false` 以保持完整的工具集。

在后台运行的分叉技能在你的会话的[检查点](/docs/zh-CN/checkpointing)之外应用其编辑，因此 `/rewind` 不会撤销它们；使用 git 来恢复它们。

<Warning>
  `context: fork` 仅对具有明确说明的技能有意义。如果你的技能包含"使用这些 API 约定"之类的指南而没有任务，子代理会收到指南但没有可操作的提示，并返回而没有有意义的输出。
</Warning>

技能和[子代理](/docs/zh-CN/sub-agents)在两个方向上协同工作：

| 方法 | 系统提示 | 任务 | 也加载 |
| :- | :- | :- | :- |
| 具有 `context: fork` 的技能 | 来自代理类型 | SKILL.md 内容 | CLAUDE.md，根据代理的[启动上下文](/docs/zh-CN/sub-agents#what-loads-at-startup) |
| 具有 `skills` 字段的子代理 | 子代理的 markdown 主体 | Claude 的委派消息 | 预加载的技能 + CLAUDE.md，根据子代理的[启动上下文](/docs/zh-CN/sub-agents#what-loads-at-startup) |

使用 `context: fork`，你在你的技能中编写任务并选择一个代理类型来执行它。内置的 Explore 和 Plan 代理[跳过 CLAUDE.md 和 git 状态](/docs/zh-CN/sub-agents#what-loads-at-startup)以保持其上下文较小，因此使用 `agent: Explore` 的分叉技能仅看到 SKILL.md 内容和代理自己的系统提示。对于相反的情况，你定义一个使用技能作为参考材料的自定义子代理，请参阅[子代理](/docs/zh-CN/sub-agents#preload-skills-into-subagents)。

<h4 id="example-research-skill-using-explore-agent">
  示例：使用 Explore 代理的研究技能
</h4>

这个技能在分叉的 Explore 代理中运行研究。技能内容成为任务，代理提供针对代码库探索优化的只读工具：

```yaml theme={null}
---
name: deep-research
description: Research a topic thoroughly
context: fork
agent: Explore
---

Research $ARGUMENTS thoroughly:

1. Find relevant files using Glob and Grep
2. Read and analyze the code
3. Summarize findings with specific file references
```

当这个技能运行时：

1. 创建一个新的隔离上下文
2. 子代理接收技能内容作为其提示（"Research \$ARGUMENTS thoroughly..."）
3. `agent` 字段确定执行环境（模型、工具和权限）
4. 子代理总结其结果并在完成时将其返回到你的主对话

`agent` 字段指定要使用的子代理配置。选项包括内置代理（`Explore`、`Plan`、`general-purpose`）或来自 `.claude/agents/` 的任何自定义子代理。如果省略，使用 `general-purpose`。

<h3 id="restrict-claude’s-skill-access">
  限制 Claude 的技能访问
</h3>

默认情况下，Claude 可以调用任何没有设置 `disable-model-invocation: true` 的技能。定义 `allowed-tools` 的技能在调用技能的轮次中授予 Claude 对这些工具的访问权限而无需逐次批准；当你发送下一条消息时，授权清除。你的[权限设置](/docs/zh-CN/permissions)仍然管理所有其他工具的基线批准行为。一些内置命令也可通过 Skill 工具获得，包括 `/init` 和 `/security-review`。其他内置命令如 `/compact` 则不可用。

控制 Claude 可以调用哪些技能的三种方法：

**通过在 `/permissions` 中拒绝 Skill 工具来禁用所有技能**：

```text theme={null}
# Add to deny rules:
Skill
```

**使用[权限规则](/docs/zh-CN/permissions)允许或拒绝特定技能**：

```text theme={null}
# Allow only specific skills
Skill(commit)
Skill(review-pr *)

# Deny specific skills
Skill(deploy *)
```

权限语法：`Skill(name)` 用于精确匹配，`Skill(name *)` 用于带任何参数的前缀匹配。

下表显示了你的 `deny` 规则命名的名称类型，Claude Code 除了你写的名称外还会阻止什么。

| 你的 `deny` 规则名称 | 示例规则 | Claude Code 也会阻止 |
| :- | :- | :- |
| 别名 | `Skill(review)` | 捆绑的 `/code-review`，通过其 `/review` 别名 |
| 不合格的名称 | `Skill(deploy)` | 列为 `apps/web:deploy` 的[嵌套技能](#where-skills-live) |
| [从 claude.ai 同步的技能](#how-synced-skills-behave) | `Skill(anthropic-skills:deploy)` | 当 Claude Desktop 将其作为插件交付给会话时的该技能 |
| 同步技能的插件形式 | `Skill(deploy:deploy)` | 同步的技能 |
| [参数形式](/docs/zh-CN/permissions#match-by-input-parameter)中的技能 | `Skill(skill:deploy)` | 该技能无论 Claude 以哪个名称调用它，包括其别名和显示名称 |

在 v2.1.260 之前，当拒绝规则仅命名不合格的名称时，Claude Code 不会阻止列在其合格名称下的嵌套技能。

Claude Code 仅针对技能自己的名称和 Claude 调用中的名称匹配 `allow` 规则。要在不提示的情况下批准[同步技能](#how-synced-skills-behave)，请在其[保留命名空间](#names-reserved-for-synced-skills)内命名它：

* `Skill(anthropic-skills:pdf)` 批准同步的 `pdf` 技能
* `Skill(anthropic-skills *)` 批准每个同步的技能
* `Skill(anthropic *)` 不涵盖 `anthropic-skills:pdf`，因为命名空间外的前缀不匹配其中的名称

**通过向其 frontmatter 添加 `disable-model-invocation: true` 来隐藏单个技能**。这将技能从 Claude 的上下文中完全删除。

<Note>
  使用 `user-invocable: false`，你无法调用该技能，但 Claude 仍然可以。要防止 Claude 通过 Skill 工具调用它，请设置 `disable-model-invocation: true`。
</Note>

<h3 id="override-skill-visibility-from-settings">
  从设置覆盖技能可见性
</h3>

`skillOverrides` 设置从你的[设置](/docs/zh-CN/settings)而不是技能自己的 frontmatter 控制技能可见性。将其用于你不想编辑 SKILL.md 的技能，例如检入共享项目仓库的技能。`/skills` 菜单为你编写它：突出显示一个技能并按 `Space` 循环状态，然后按 `Esc` 保存到 `.claude/settings.local.json`。

每个键是一个技能名称，每个值是四种状态之一：

| 值 | 列出给 Claude | 在 `/` 菜单中 |
| :- | :- | :- |
| `"on"` | 名称和描述 | 是 |
| `"name-only"` | 仅名称 | 是 |
| `"user-invocable-only"` | 隐藏 | 是 |
| `"off"` | 隐藏 | 隐藏 |

`/skills` 菜单将 `"user-invocable-only"` 状态标记为 `user-only`。

从 v2.1.199 开始，`"off"` 也会从广告给[远程控制](/docs/zh-CN/remote-control)客户端和[Agent SDK](/docs/zh-CN/agent-sdk/skills#discover-available-commands)调用者的命令列表中隐藏技能，除了终端 `/` 菜单。按其全名调用隐藏的技能仍然返回 `skillOverrides` 错误而不是运行它。

不在 `skillOverrides` 中的技能被视为 `"on"`。下面的示例将一个技能折叠为其名称，并完全关闭另一个：

```json theme={null}
{
  "skillOverrides": {
    "legacy-context": "name-only",
    "deploy": "off"
  }
}
```

一些捆绑的技能有别名，例如 `checkup` 用于 `/doctor`。如果你在[托管设置](/docs/zh-CN/managed-settings)中或在你使用 `--settings` 标志传递的文件中的别名下设置 `skillOverrides` 条目，Claude Code 会将其应用于别名后面的技能。你只能通过别名进一步限制技能，永远不能使其更可见，如果你也在托管设置中的技能自己的名称下设置条目，该条目优先。在 v2.1.260 之前，Claude Code 不会在任何设置源中的别名下应用条目到技能。

在用户、项目和本地设置中，Claude Code 仅针对技能名称匹配条目。如果你在那里为 `review` 设置条目，它适用于名为 `review` 的技能，而不是通过其 `/review` 别名的捆绑 `/code-review`。

插件技能不受 `skillOverrides` 影响。通过 `/plugin` 管理那些。

<h3 id="find-unused-skills">
  查找未使用的技能
</h3>

[技能列表](#skill-descriptions-are-cut-short)中的每个技能都会在每个轮次上添加到你的上下文中，无论 Claude 是否曾使用过它。运行 `/skill-doctor` 以查看每个技能的成本以及它被使用的频率，以便你可以决定关闭哪些。在交互式会话中，报告在 `/plugin` 管理器的 **Stats** 选项卡中打开。在[非交互模式](/docs/zh-CN/headless)中使用 `-p`，Claude Code 将其打印为文本。

该报告涵盖你的会话中的技能，除了捆绑技能和企业技能。它标记列表中从未被调用的技能，并说明在哪里关闭它们。在它告诉你在哪里关闭的技能中，从具有最高上下文成本的技能开始。该报告还列出你最近未使用的插件。

`/skill-doctor` 需要 Claude Code v2.1.252 或更高版本，在跳过[功能标志获取](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching)的会话中不可用。如果你从你的手机或浏览器通过[远程控制](/docs/zh-CN/remote-control)运行 `/skill-doctor`，Claude Code 回复[`Skill usage reports are not available on this connection.`](/docs/zh-CN/errors#skill-usage-reports-are-not-available-on-this-connection)。在运行会话的机器上的终端中运行 `/skill-doctor`。

<h2 id="evaluate-and-iterate-on-a-skill">
  评估和迭代技能
</h2>

看到技能触发告诉你 Claude 找到了它，但不代表它做了你想要的事情。要知道技能是否有效，需要分别测量两件事：Claude 是否在应该调用的提示上调用它，以及当它调用时输出是否与你的预期相符。

两者的检查都是基线比较。收集几个现实的提示，在启用技能的新会话中运行每个提示，然后在禁用技能的情况下再运行一次，并比较结果。新会话很重要，因为编写技能时留下的上下文会掩盖书面说明中的差距。

关闭技能进行第二次运行的方式取决于它来自何处：

* **个人或项目技能**：在 [`skillOverrides`](#override-skill-visibility-from-settings) 中将其设置为 `"off"`。
* **插件提供的技能**：`skillOverrides` 不适用于插件技能。改用 [`claude plugin eval`](/docs/zh-CN/plugin-evals#the-no-plugin-baseline)，它在没有加载任何插件的情况下重复每次运行。

两个工具可以自动化基线比较。对于在[插件](/docs/zh-CN/plugins/overview)中发布的技能，[`claude plugin eval`](/docs/zh-CN/plugin-evals) 在隔离会话中运行每个提示，既有插件也没有插件，使用你定义的或它为你编写的评分器对其进行评分，并在低于阈值时以非零状态退出，以便你可以在 CI 上对其进行门控。对于在 Claude Code 对话中迭代单个技能，下面的 skill-creator 插件使用其自己的 `evals/evals.json` 格式运行类似的循环。这两种格式不可互换。

<h3 id="run-evals-with-skill-creator">
  使用 skill-creator 运行评估
</h3>

[`skill-creator` 插件](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/skill-creator)在 Claude Code 内自动化比较循环。从官方市场安装它：

```text theme={null}
/plugin install skill-creator@claude-plugins-official
```

如果安装失败，请匹配 Claude Code 报告的消息：

* `Marketplace "claude-plugins-official" not found`：使用 `/plugin marketplace add anthropics/claude-plugins-official` 添加市场，然后重试安装。
* [插件在市场中找不到](/docs/zh-CN/plugins/install#install-a-plugin)：检查插件名称。

如果安装摘要报告 `Run /reload-plugins to activate.`，Claude Code 随后会为你运行该重新加载。如果重新加载警告你的下一条消息会重新读取对话，请运行 `/reload-plugins --force` 以在当前会话中使插件的技能可用。然后要求 Claude 评估现有技能，例如 `evaluate my summarize-changes skill with skill-creator`。该插件会引导你编写测试用例并运行循环：

* **测试用例**：在技能目录内的 `evals/evals.json` 中存储提示、输入文件和预期行为
* **隔离运行**：为每个测试用例生成一个[子代理](/docs/zh-CN/sub-agents)，以便每次运行都从干净的上下文开始，并记录令牌计数和持续时间
* **评分**：针对输出检查每个断言，并将通过或失败以及证据写入 `grading.json`
* **基准**：将有技能与无技能的通过率、时间和令牌聚合到 `benchmark.json` 中，以便你可以比较通过率改进与令牌和时间开销
* **版本比较**：在技能的两个版本之间运行盲 A/B 测试，以便你可以在提交编辑之前确认它是一个改进
* **描述调整**：生成应该触发和不应该触发的提示，测量命中率，并在技能在错误的请求上激活时提议描述编辑
* **审查查看器**：打开一个 HTML 报告，你可以在其中检查每个输出并记录下一次迭代读取的定性反馈

有关评估文件格式和完整迭代工作流，请参阅 agentskills.io 上的[评估技能输出质量](https://agentskills.io/skill-creation/evaluating-skills)。有关基准和比较模式的背景，请参阅 [skill-creator 公告](https://claude.com/blog/improving-skill-creator-test-measure-and-refine-agent-skills)。

<h2 id="share-skills">
  分享 skills
</h2>

Skills 可以根据你的受众在不同的范围内分发：

* **项目 skills**：将 `.claude/skills/` 提交到版本控制
* **Plugins**：在你的 [plugin](/docs/zh-CN/plugins/overview) 中创建 `skills/` 目录
* **托管**：通过 [托管设置](/docs/zh-CN/managed-settings) 在整个组织范围内部署

<h3 id="generate-visual-output">
  生成可视化输出
</h3>

Skills 可以捆绑并运行任何语言的脚本，为 Claude 提供超越单个提示符可能实现的功能。一种模式是生成可视化输出：在浏览器中打开的交互式 HTML 文件，用于探索数据、调试或创建报告。

此示例创建一个代码库浏览器：一个交互式树形视图，你可以在其中展开和折叠目录、一目了然地查看文件大小，并通过颜色识别文件类型。

创建 Skill 目录：

```bash theme={null}
mkdir -p ~/.claude/skills/codebase-visualizer/scripts
```

将其保存到 `~/.claude/skills/codebase-visualizer/SKILL.md`。描述告诉 Claude 何时激活此 Skill，说明告诉 Claude 运行捆绑的脚本。脚本路径使用 [`${CLAUDE_SKILL_DIR}`](#available-string-substitutions)，因此无论 skill 是在个人、项目还是 plugin 级别安装，它都能正确解析：

````yaml theme={null}
---
name: codebase-visualizer
description: Generate an interactive collapsible tree visualization of your codebase. Use when exploring a new repo, understanding project structure, or identifying large files.
allowed-tools: Bash(python3 *)
---

# Codebase Visualizer

Generate an interactive HTML tree view that shows your project's file structure with collapsible directories.

## Usage

Run the visualization script from your project root:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/visualize.py .
```

This creates `codebase-map.html` in the current directory and opens it in your default browser.

## What the visualization shows

- **Collapsible directories**: Click folders to expand/collapse
- **File sizes**: Displayed next to each file
- **Colors**: Different colors for different file types
- **Directory totals**: Shows aggregate size of each folder
````

将其保存到 `~/.claude/skills/codebase-visualizer/scripts/visualize.py`。此脚本扫描目录树并生成一个自包含的 HTML 文件，包含：

* 一个**摘要侧边栏**，显示文件计数、目录计数、总大小和文件类型数量
* 一个**条形图**，按文件类型（按大小排名前 8）分解代码库
* 一个**可折叠树**，你可以在其中展开和折叠目录，带有颜色编码的文件类型指示器

该脚本需要 Python 3，但仅使用内置库，因此无需安装任何包：

```python expandable theme={null}
#!/usr/bin/env python3
"""Generate an interactive collapsible tree visualization of a codebase."""

import json
import sys
import webbrowser
from html import escape
from pathlib import Path
from collections import Counter

IGNORE = {'.git', 'node_modules', '__pycache__', '.venv', 'venv', 'dist', 'build'}

def scan(path: Path, stats: dict) -> dict:
    result = {"name": path.name, "children": [], "size": 0}
    try:
        for item in sorted(path.iterdir()):
            if item.name in IGNORE or item.name.startswith('.'):
                continue
            if item.is_file():
                size = item.stat().st_size
                ext = item.suffix.lower() or '(no ext)'
                result["children"].append({"name": item.name, "size": size, "ext": ext})
                result["size"] += size
                stats["files"] += 1
                stats["extensions"][ext] += 1
                stats["ext_sizes"][ext] += size
            elif item.is_dir():
                stats["dirs"] += 1
                child = scan(item, stats)
                if child["children"]:
                    result["children"].append(child)
                    result["size"] += child["size"]
    except PermissionError:
        pass
    return result

def generate_html(data: dict, stats: dict, output: Path) -> None:
    ext_sizes = stats["ext_sizes"]
    total_size = sum(ext_sizes.values()) or 1
    sorted_exts = sorted(ext_sizes.items(), key=lambda x: -x[1])[:8]
    colors = {
        '.js': '#f7df1e', '.ts': '#3178c6', '.py': '#3776ab', '.go': '#00add8',
        '.rs': '#dea584', '.rb': '#cc342d', '.css': '#264de4', '.html': '#e34c26',
        '.json': '#6b7280', '.md': '#083fa1', '.yaml': '#cb171e', '.yml': '#cb171e',
        '.mdx': '#083fa1', '.tsx': '#3178c6', '.jsx': '#61dafb', '.sh': '#4eaa25',
    }
    lang_bars = "".join(
        f'<div class="bar-row"><span class="bar-label">{ext}</span>'
        f'<div class="bar" style="width:{(size/total_size)*100}%;background:{colors.get(ext,"#6b7280")}"></div>'
        f'<span class="bar-pct">{(size/total_size)*100:.1f}%</span></div>'
        for ext, size in sorted_exts
    )
    def fmt(b):
        if b < 1024: return f"{b} B"
        if b < 1048576: return f"{b/1024:.1f} KB"
        return f"{b/1048576:.1f} MB"

    html = f'''<!DOCTYPE html>
<html><head>
  <meta charset="utf-8"><title>Codebase Explorer</title>
  <style>
    body {{ font: 14px/1.5 system-ui, sans-serif; margin: 0; background: #1a1a2e; color: #eee; }}
    .container {{ display: flex; height: 100vh; }}
    .sidebar {{ width: 280px; background: #252542; padding: 20px; border-right: 1px solid #3d3d5c; overflow-y: auto; flex-shrink: 0; }}
    .main {{ flex: 1; padding: 20px; overflow-y: auto; }}
    h1 {{ margin: 0 0 10px 0; font-size: 18px; }}
    h2 {{ margin: 20px 0 10px 0; font-size: 14px; color: #888; text-transform: uppercase; }}
    .stat {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid #3d3d5c; }}
    .stat-value {{ font-weight: bold; }}
    .bar-row {{ display: flex; align-items: center; margin: 6px 0; }}
    .bar-label {{ width: 55px; font-size: 12px; color: #aaa; }}
    .bar {{ height: 18px; border-radius: 3px; }}
    .bar-pct {{ margin-left: 8px; font-size: 12px; color: #666; }}
    .tree {{ list-style: none; padding-left: 20px; }}
    details {{ cursor: pointer; }}
    summary {{ padding: 4px 8px; border-radius: 4px; }}
    summary:hover {{ background: #2d2d44; }}
    .folder {{ color: #ffd700; }}
    .file {{ display: flex; align-items: center; padding: 4px 8px; border-radius: 4px; }}
    .file:hover {{ background: #2d2d44; }}
    .size {{ color: #888; margin-left: auto; font-size: 12px; }}
    .dot {{ width: 8px; height: 8px; border-radius: 50%; margin-right: 8px; }}
  </style>
</head><body>
  <div class="container">
    <div class="sidebar">
      <h1>📊 Summary</h1>
      <div class="stat"><span>Files</span><span class="stat-value">{stats["files"]:,}</span></div>
      <div class="stat"><span>Directories</span><span class="stat-value">{stats["dirs"]:,}</span></div>
      <div class="stat"><span>Total size</span><span class="stat-value">{fmt(data["size"])}</span></div>
      <div class="stat"><span>File types</span><span class="stat-value">{len(stats["extensions"])}</span></div>
      <h2>By file type</h2>
      {lang_bars}
    </div>
    <div class="main">
      <h1>📁 {escape(data["name"])}</h1>
      <ul class="tree" id="root"></ul>
    </div>
  </div>
  <script>
    const data = {json.dumps(data)};
    const colors = {json.dumps(colors)};
    function fmt(b) {{ if (b < 1024) return b + ' B'; if (b < 1048576) return (b/1024).toFixed(1) + ' KB'; return (b/1048576).toFixed(1) + ' MB'; }}
    function esc(s) {{ return s.replace(/[&<>"']/g, c => ({{"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#39;"}}[c])); }}
    function render(node, parent) {{
      if (node.children) {{
        const det = document.createElement('details');
        det.open = parent === document.getElementById('root');
        det.innerHTML = `<summary><span class="folder">📁 ${{esc(node.name)}}</span><span class="size">${{fmt(node.size)}}</span></summary>`;
        const ul = document.createElement('ul'); ul.className = 'tree';
        node.children.sort((a,b) => (b.children?1:0)-(a.children?1:0) || a.name.localeCompare(b.name));
        node.children.forEach(c => render(c, ul));
        det.appendChild(ul);
        const li = document.createElement('li'); li.appendChild(det); parent.appendChild(li);
      }} else {{
        const li = document.createElement('li'); li.className = 'file';
        li.innerHTML = `<span class="dot" style="background:${{colors[node.ext]||'#6b7280'}}"></span>${{esc(node.name)}}<span class="size">${{fmt(node.size)}}</span>`;
        parent.appendChild(li);
      }}
    }}
    data.children.forEach(c => render(c, document.getElementById('root')));
  </script>
</body></html>'''
    output.write_text(html)

if __name__ == '__main__':
    target = Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
    stats = {"files": 0, "dirs": 0, "extensions": Counter(), "ext_sizes": Counter()}
    data = scan(target, stats)
    out = Path('codebase-map.html')
    generate_html(data, stats, out)
    print(f'Generated {out.absolute()}')
    webbrowser.open(f'file://{out.absolute()}')
```

要测试，在任何项目中打开 Claude Code 并询问"可视化此代码库。"Claude 运行脚本，该脚本打印生成的文件的路径，例如 `Generated /path/to/codebase-map.html`，并在浏览器中打开它。如果你在无浏览器环境中工作，其中没有浏览器打开，打印的路径确认脚本成功。

此模式适用于任何可视化输出：依赖关系图、测试覆盖率报告、API 文档或数据库架构可视化。捆绑的脚本完成工作，而 Claude 处理编排。

<h2 id="troubleshooting">
  故障排除
</h2>

<h3 id="skill-not-triggering">
  Skill 未触发
</h3>

如果 Claude 在预期时没有使用你的 skill：

1. 检查描述是否包含用户会自然说出的关键词
2. 验证 skill 是否出现在 `What skills are available?` 中
3. 尝试重新表述你的请求以更接近描述
4. 如果 skill 是用户可调用的，使用 `/skill-name` 直接调用它

如果 frontmatter YAML 格式不正确，Claude Code 会加载 skill 主体但元数据为空，所以 `/skill-name` 仍然有效，但 Claude 无法匹配你的 `description`。使用 `--debug` 运行以查看解析错误。

如果 skill 在 plugin 中，你可以在现实提示中测量它触发的频率，而不是逐个检查：使用 [`tool_used: Skill` grader](/docs/zh-CN/plugin-evals#create-your-first-eval-suite) 编写一个 eval case，并在每次描述更改后使用 `claude plugin eval` 运行它。

要找到 frontmatter 无法解析的 `SKILL.md` 文件，在 skills 目录上运行 [`claude plugin validate`](/docs/zh-CN/plugins/cli-reference#validate-a-directory)，例如对于项目 skills 运行 `claude plugin validate .claude/skills`，或对于个人 skills 运行 `claude plugin validate ~/.claude/skills`。需要 Claude Code v2.1.233 或更高版本。

<h3 id="skill-triggers-too-often">
  Skill 触发过于频繁
</h3>

如果 Claude 在你不想要的时候使用你的 skill：

1. 使描述更具体
2. 如果你只想要手动调用，添加 `disable-model-invocation: true`

<h3 id="claude-stops-following-a-skill">
  Claude 停止遵循 skill
</h3>

如果 Claude 在其第一个响应中遵循 skill，但之后停止遵循它，请从与你的情况相匹配的以下任何一种情况开始：

* **Claude 跳过了必须每次都成立的规则**：将规则移到 [hook](/docs/zh-CN/hooks-guide) 中。Claude Code 在其事件发生时每次都运行 hook，例如在每次文件编辑之前，无论 Claude 是否遵循 skill。要将规则与 skill 保持在一起，在 skill 的 [`hooks` frontmatter](/docs/zh-CN/hooks#hooks-in-skills-and-agents) 中定义 hook。该 hook 从 skill 被调用时开始应用，直到会话结束。
* **Claude 跳过了应该有判断力地应用的指导**：措辞指导使其适用于整个任务，例如"在每次编辑后运行测试"而不是"运行测试"。Claude Code 在 skill 被调用时将 skill 的内容添加到对话中，并且 [不会在后续轮次重新读取文件](#skill-content-lifecycle)。
* **对话被压缩了**：再次调用 skill 以恢复其完整内容。在 [压缩](/docs/zh-CN/how-claude-code-works#when-context-fills-up) 之后，Claude Code [只能保留被调用的 skill 的开始部分](#skill-content-lifecycle)，所以将最重要的说明放在 `SKILL.md` 的顶部。

<h3 id="skill-descriptions-are-cut-short">
  Skill 描述被截断
</h3>

Claude Code 将 skill 名称和描述的列表加载到上下文中，以便 Claude 知道有哪些可用。列表始终包含每个 skill 名称，但如果你有很多 skills，Claude Code 会缩短描述以适应列表的字符预算，这可能会删除 Claude 需要匹配你的请求的关键词。预算按模型上下文窗口的 1% 进行缩放。当列表溢出时，Claude Code 从你调用最少的 skills 开始删除描述，所以你使用最多的 skills 保持其完整文本。

运行 `/doctor` 以估计列表的上下文成本及其最大贡献者。要找到值得关闭的 skills，运行 [`/skill-doctor`](#find-unused-skills)。当列表超过其预算时，Claude Code 也会向调试日志写入警告，可通过 [`--debug`](/docs/zh-CN/cli-reference#cli-flags) 查看。

`/context` 中的 Skills 行报告应用预算后列表的大小，因此它与模型接收的内容相匹配。在 v2.1.196 之前，该行计算每个描述的完整文本，可能显示的值比配置的预算大几倍。

要提高预算，设置 [`skillListingBudgetFraction`](/docs/zh-CN/settings-reference#skilllistingbudgetfraction) 设置（例如 `0.02` = 2%）或 `SLASH_COMMAND_TOOL_CHAR_BUDGET` 环境变量为固定字符数。要为其他 skills 释放预算，在 [`skillOverrides`](#override-skill-visibility-from-settings) 中将低优先级条目设置为 `"name-only"`，以便它们在没有描述的情况下列出。你也可以在源处修剪 `description` 和 `when_to_use` 文本：将关键用例放在首位，因为每个条目的组合文本被限制在 1,536 个字符，无论预算如何。该上限可通过 [`skillListingMaxDescChars`](/docs/zh-CN/settings-reference#skilllistingmaxdescchars) 配置。

<h3 id="personal-skills-disappeared">
  个人 skills 消失了
</h3>

如果你在 `~/.claude/skills/` 中创建的 skill 文件夹消失了，请查看 `~/.claude/skills/.trash/`。当 Claude Code [从 claude.ai 同步 skills](#how-synced-skills-behave) 时，它会将它们下载到单独的 `synced` 子文件夹中，不会移动或删除你创建的文件夹。

在 v2.1.280 之前，`~/.claude/skills/` 中名为 `manifest.json` 的文件会导致 Claude Code 将该文件列出的 skill 文件夹移动到 `~/.claude/skills/.trash/` 下的带时间戳的文件夹中，这些 skills 停止加载。

要恢复一个 skill，将其文件夹从带时间戳的文件夹移回 `~/.claude/skills/`。在 [保留扫描](/docs/zh-CN/claude-directory#cleaned-up-automatically) 删除垃圾条目之前执行此操作，默认情况下在移动到垃圾箱后 30 天。

<h2 id="related-resources">
  相关资源
</h2>

* **[调试你的配置](/docs/zh-CN/debug-your-config)**：诊断为什么 skill 没有出现或触发
* **[在 agentskills.io 上评估 skill 输出质量](https://agentskills.io/skill-creation/evaluating-skills)**：eval 文件格式和迭代工作流
* **[Skill 创作最佳实践](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)**：适用于 Claude 产品的写作指导
* **[Subagents](/docs/zh-CN/sub-agents)**：将任务委派给专门的代理
* **[Plugins](/docs/zh-CN/plugins/overview)**：打包和分发 skills 与其他扩展
* **[Hooks](/docs/zh-CN/hooks)**：围绕工具事件自动化工作流
* **[Memory](/docs/zh-CN/memory)**：管理 CLAUDE.md 文件以获得持久上下文
* **[Commands](/docs/zh-CN/commands)**：内置命令和捆绑 skills 的参考
* **[Permissions](/docs/zh-CN/permissions)**：控制工具和 skill 访问
* **[Claude Tag skills](https://claude.com/docs/claude-tag/admins/skills-repo)**：提交到仓库的项目 skills 在该仓库在 Claude Tag 频道中使用时也会加载
