> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 插件加载参考

> 追踪 Claude Code 从何处加载每个插件，哪个设置文件决定是否加载，以及为什么更新没有产生任何变化。

当插件未加载、加载了与预期不同的副本，或未获取更新时，使用此页面查看哪个源、设置范围或磁盘上的文件决定了这一点。它提供了 Claude Code 在会话启动时和每次运行 `/reload-plugins` 时应用的规则。您也可以要求 Claude 阅读此页面并诊断您的设置。

<Note>
  这些情况在其他页面上有介绍：

  * **安装、启用、禁用和更新步骤**：请参阅[安装和管理插件](/docs/zh-CN/plugins/install)
  * **您有特定的错误消息**：请参阅[插件故障排除](/docs/zh-CN/plugins/troubleshooting)
</Note>

从[检查插件达到的阶段](#check-which-stage-a-plugin-reached)开始，了解已安装插件经过的三个阶段，或转到与您看到的情况相匹配的部分：

* 您关闭的插件仍然加载：[查找插件的启用位置](#find-where-a-plugin-is-enabled)
* 更新没有产生任何变化：[版本和更新](#versions-and-updates)
* 您正在查看 `~/.claude/plugins/` 下的文件：[查找磁盘上的插件](#find-plugins-on-disk)
* `--plugin-dir` 插件未加载，或加载了同名插件：[名称冲突](#name-conflicts)

<h2 id="check-which-stage-a-plugin-reached">
  检查插件达到的阶段
</h2>

`enabledPlugins` 条目分阶段成为您可以使用的插件：您的设置声明它，Claude Code 将其获取到磁盘，运行中的会话加载它。当插件的行为与设置文件建议的不符时，检查它达到了哪个阶段：

* **已声明，在设置中**：`enabledPlugins` 说明哪些插件应该打开，`extraKnownMarketplaces` 说明哪些市场应该存在。当您运行 `claude plugin marketplace add` 时，Claude Code 将市场写入您的用户设置中的 `extraKnownMarketplaces` 以及磁盘
* **已获取，在 `~/.claude/plugins/` 下的磁盘上**：Claude Code 已获取的记录和获取的文件本身：
  * `known_marketplaces.json` 记录 Claude Code 已获取的每个市场，包括其 `source`、`installLocation`、`lastUpdated` 和 `autoUpdate`。每个用户有一个 `known_marketplaces.json`，因此您在一个项目中添加的市场在每个项目中都可用
  * `installed_plugins.json` 记录每个安装及其 `scope`、`installPath` 和 `version`
  * `cache/` 保存插件文件
* **已加载，在运行中的会话中**：Claude Code 在启动时或最后一次 `/reload-plugins` 时加载的插件集。对设置或磁盘的更改不会到达此层，直到您运行 `/reload-plugins` 或启动新会话。这就是为什么 `claude plugin update` 以 `Restart to apply changes.` 结尾，背景更新会提示您 `Run /reload-plugins to apply`

<h3 id="plugins-and-marketplaces-that-aren’t-on-disk-at-session-start">
  会话启动时磁盘上没有的插件和市场
</h3>

插件在会话启动时从 `installed_plugins.json` 和缓存加载，不使用网络。会话启动后，Claude Code 在后台检查声明的市场：

* **设置声明但 `known_marketplaces.json` 缺少的市场**：Claude Code 克隆它，然后重新加载插件并下载未缓存的已启用插件
* **声明的市场其源在设置中更改**：Claude Code 从新源重新获取它并显示 `Plugins changed. Run /reload-plugins to activate.`

既未被任何路径获取且没有可用缓存目录的已启用插件在 `/plugin` **Errors** 选项卡中显示 `Plugin "<name>" not cached at <path>`，`claude plugin list` 在同一行添加 `— run /plugin to refresh`。有关修复，请参阅[`Plugin "<name>" not cached at <path>`](/docs/zh-CN/plugins/troubleshooting#plugin-not-cached-at)。

<h2 id="find-where-a-plugin-came-from">
  查找插件的来源
</h2>

每个插件都有形式为 `<name>@<origin>` 的 id，这是您在设置文件和 `claude plugin list --json` 中看到的。`@` 之后的部分告诉您 Claude Code 在哪里找到了插件：

| ID 结尾 | 插件如何到达 | 如何打开或关闭 |
| :- | :- | :- |
| `@<marketplace>` | 您从添加的市场安装了它 | 在设置文件中的 `enabledPlugins` 下设置 `"<name>@<marketplace>": true` 或 `false` |
| `@inline` | 您使用 `--plugin-dir` 或 `--plugin-url` 启动了 Claude Code，设置了 [`CLAUDE_CODE_PLUGIN_DIRS`](/docs/zh-CN/env-vars#variables)，或 Agent SDK 应用传递了 `plugins` 选项。它仅为该会话加载 | 除非清单设置 `defaultEnabled: false` 或设置文件设置 `"<name>@inline": false`，否则为会话打开 |
| `@skills-dir` | 您在 `~/.claude/skills/` 或项目的 `.claude/skills/` 下保存了具有 `.claude-plugin/plugin.json` 的插件目录 | 清单的 `defaultEnabled`，除非设置文件将 `"<name>@skills-dir"` 设置为 `true` 或 `false` |
| `@synced` | 您或您的组织为您的 claude.ai 账户打开了它，Claude Code [下载了它](#synced-plugins) | 除非清单设置 `defaultEnabled: false` 或设置文件设置 `"<name>@synced": false`，否则打开。您的组织标记为必需的插件无论如何都会加载 |

对于市场插件，`<name>` 是 `marketplace.json` 中的条目名称；对于 `@inline` 和 `@skills-dir`，它是插件清单中的 `name`。

此表中的源名称是保留的，因此没有市场可以命名为 `inline`、`skills-dir` 或 `synced`。

<h3 id="entry-name-and-manifest-name">
  条目名称和清单名称
</h3>

市场插件有两个名称，它们可能不同：

* **`marketplace.json` 中的条目名称**：安装和启用密钥。这是您在 `enabledPlugins` 中写入的内容，缓存目录的命名依据，以及 `claude plugin list` 显示的内容
* **清单中的 `name`**：插件组件命名空间所在的位置，以及[名称冲突](#name-conflicts)比较的内容

<h3 id="plugins-shared-through-a-repository">
  通过存储库共享的插件
</h3>

要通过存储库共享插件，请在 `.claude/settings.json` 中的 `enabledPlugins` 下列出它，或将其放在 `.claude/skills/` 下。Claude Code 不扫描项目的 `.claude/plugins/` 目录。

云会话不会添加存储库在 [`extraKnownMarketplaces`](/docs/zh-CN/settings-reference#extraknownmarketplaces) 下列出的市场，因为这需要工作区信任对话框，云会话永远不会显示。

项目范围的技能目录插件仅从会话[主工作目录](/docs/zh-CN/permissions#working-directories)的 `.claude/skills/` 加载，并且仅在您接受该文件夹的[工作区信任对话框](/docs/zh-CN/permissions#what-runs-before-you-trust-a-folder)后加载。它不会[搜索从存储库根目录向上的父目录](/docs/zh-CN/skills#discovery-from-parent-and-nested-directories)，就像普通技能和命令那样。如果您从子目录启动，存储库根目录中的插件不会加载。改为从存储库根目录启动，或 [使用 `/cd` 将会话移到那里](/docs/zh-CN/permissions#move-the-session-to-another-directory)（v2.1.246 或更高版本）。

项目范围的插件被检入存储库，并到达克隆它的每个协作者。因为该内容来自存储库而不是来自您，它仅在应用于 `.claude/settings.json` 中项目允许规则的相同信任检查后加载。信任父文件夹或使用 `-p` 运行是不够的。运行代码的组件受到进一步限制：

* 它声明的 MCP 服务器经过[与项目 `.mcp.json` 相同的每服务器批准](/docs/zh-CN/mcp)
* 它声明为[MCP 包](/docs/zh-CN/plugins/manifest-reference#mcpservers)、`.mcpb` 或 `.dxt` 文件或来自插件目录外文件的 MCP 服务器被跳过。内联声明它们或在插件目录内的 `.mcp.json` 中声明
* [后台监视器](/docs/zh-CN/plugins/components#monitors)不加载

个人范围的插件没有这些限制。

有关如何编写 `--plugin-dir` 和技能目录插件，请参阅[创建插件](/docs/zh-CN/plugins/create)。

<h3 id="synced-plugins">
  从 claude.ai 同步的插件
</h3>

您为 claude.ai 账户打开的插件也会在 Claude Code 中加载，与您从市场安装的插件一起。这包括您的组织为其成员打开的插件。这些插件中的每一个都作为 `<name>@synced` 加载，没有市场，也没有[安装记录](#check-which-stage-a-plugin-reached)。

在终端会话中，同步插件的技能、代理、hooks、MCP 服务器和 LSP 服务器都加载，具有与您安装的市场插件相同的信任。

有关 Cowork 加载的组件，请参阅 claude.com 上的[组件支持表](https://claude.com/docs/plugins/platform-support#compare-component-support-by-app)。

同步插件在 Cowork 会话和您使用 claude.ai 账户登录的终端会话中加载：

* **[Cowork](https://claude.com/product/cowork)**：Claude Code 在会话启动时将它们下载到会话自己的环境中
* **终端会话**：每次启动 Claude Code 时，它在后台同步一次，下载新的和更新的插件，并删除您或您的组织关闭的插件。终端会话中的同步需要 Claude Code v2.1.273 或更高版本

<h4 id="sync-timing-in-terminal-sessions">
  终端会话中的同步时间
</h4>

因为终端同步在后台运行，它可能在您的会话启动后完成。当它在交互式会话中添加、更新或删除同步插件时，您会看到 `Plugins changed. Run /reload-plugins to activate.` 运行 `/reload-plugins` 以在该会话中加载更改，或将其留到下次启动 Claude Code 时。

如果您在会话运行时在 claude.ai 上启用插件，该插件将在下次启动 Claude Code 时下载。

<h4 id="sign-in-requirements-for-terminal-sync">
  终端同步的登录要求
</h4>

在您的终端中，插件仅在您使用 claude.ai 账户登录的会话中同步。

Claude Code 在这些终端会话中既不下载也不加载同步插件，即使您使用 `/login` 登录后也是如此：

* 一个会话，其中 `ANTHROPIC_AUTH_TOKEN`、`CLAUDE_CODE_OAUTH_TOKEN` 或 `apiKeyHelper` 脚本提供凭证来代替该登录
* 一个不[从 Anthropic 获取功能标志](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching)的会话，例如您设置 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 的会话
* 一个处于[裸模式](/docs/zh-CN/headless#start-faster-with-bare-mode)的会话或您使用 `--safe-mode` 启动的会话
* 一个您使用[`--setting-sources`](/docs/zh-CN/cli-reference#cli-flags)列表启动的会话，该列表遗漏了 `user`

如果您在早期版本的 Claude Code 上登录，该登录不会覆盖插件，直到 Claude Code 在后台续期。要更快获得访问权限，请再次运行 `/login`。插件同步然后在下次启动 Claude Code 时开始。

<h4 id="control-which-synced-plugins-load">
  控制哪些同步插件加载
</h4>

您可以逐个关闭同步插件，除了您的组织要求的插件，或关闭机器上的每个同步插件：

* **一个插件**：在您的 shell 中运行 `claude plugin disable <name>@synced`，会话中 `/plugin` **Installed** 选项卡都在您的用户级[`enabledPlugins`](/docs/zh-CN/settings-reference#enabledplugins)中保存 `"<name>@synced": false`。要在每个环境中将插件排除在项目之外，请在项目的已提交 `.claude/settings.json` 中设置相同的密钥
* **机器上的每个同步插件**：在您的用户设置中设置 [`syncClaudeAiPlugins`](/docs/zh-CN/settings-reference#syncclaudeaiplugins) 为 `false`，或您的组织在[托管设置](/docs/zh-CN/managed-settings)中设置它。Claude Code 停止下载，下次启动时，它将已同步的插件移到 `~/.claude/plugins/.trash/`，不再加载它们。如果您的组织在 claude.ai 上关闭技能，插件也会停止同步
* **您的组织要求的插件**：您的组织在 claude.ai 上标记为必需的插件即使您之前禁用了它也会加载。`claude plugin disable` 拒绝它，显示 `Plugin "<name>@synced" is required by your organization and can't be disabled here. Contact your admin to change it.`，`claude plugin list` 将其标记为 `required by your org`

有关在 claude.ai 上删除插件，请参阅[管理已安装的插件](/docs/zh-CN/plugins/install#manage-installed-plugins)。

<h2 id="find-where-a-plugin-is-enabled">
  查找插件的启用位置
</h2>

您可以在六个源中的任何一个中设置 `enabledPlugins` 条目。该表从最低优先级到最高优先级列出它们，以及每个适用于谁。有关设置文件本身，请参阅[设置文件及其影响的人](/docs/zh-CN/settings#where-settings-live)。

| 源 | 您在哪里设置它 | 到达 |
| :- | :- | :- |
| `--add-dir` | 您使用 `--add-dir` 传递的目录中的 `.claude/settings.json` 或 `.claude/settings.local.json` | 仅此会话。仅 `true` 值有效，每个其他源都会覆盖它 |
| `user` | `~/.claude/settings.json` | 您，在每个项目中 |
| `project` | `.claude/settings.json` | 克隆存储库的每个人 |
| `local` | `.claude/settings.local.json` | 您，仅在此存储库中 |
| `flag` | 您在启动时传递的 `--settings` 值 | 仅此会话 |
| `managed` | [托管设置](/docs/zh-CN/managed-settings) | 策略覆盖的每个用户。`true` 强制启用，`false` 阻止，没有其他源覆盖它们 |

这些源逐个密钥合并。对于每个插件 id，应用的值来自提及该 id 的最高优先级源。不提及该 id 的源将较低优先级源的值保留在有效状态。

<h3 id="disabled-in-user-settings-but-still-loads">
  在用户设置中禁用但仍然加载
</h3>

如果您在 `~/.claude/settings.json` 中将插件设置为 `false` 并且它仍然加载，较高优先级源中的 `true` 正在覆盖它。插件在 `claude plugin list` 和 `/plugin` 中的行显示 `Disabled in ~/.claude/settings.json but still loads — project settings enable it, which overrides your user setting`。该消息命名覆盖您的源：`project`、`project, gitignored`（对于 `.claude/settings.local.json`）、`cli flag` 或 `managed`。

要在您的机器上选择退出项目启用的插件，请在 `.claude/settings.local.json` 中将 id 设置为 `false`，它的优先级高于项目文件。

<h3 id="enabled-in-project-settings-but-not-installed">
  在项目设置中启用但未安装
</h3>

当插件的唯一 `true` 在项目的 `.claude/settings.json` 中时，Claude Code 不会在未安装它的机器上获取它，除非其市场条目具有[相对路径源](/docs/zh-CN/plugins/marketplace-reference#plugin-sources)或[种子目录](/docs/zh-CN/plugins/org#seed-containers-and-ci)已经保存它。相反，`/plugin` **Errors** 选项卡显示 `Plugin "<name>" is enabled in project settings but isn't installed here`。

相对路径插件不需要安装记录，因为它从市场本身加载。

Claude Code 仅当以下源之一将其设置为 `true` 时才获取具有外部源的插件：

* 您的用户设置
* git 不跟踪的 `.claude/settings.local.json`
* `--settings` 标志
* 托管设置

<h2 id="find-plugins-on-disk">
  查找磁盘上的插件
</h2>

Claude Code 在一个插件根目录下保存插件文件和状态记录，该目录是 `~/.claude/plugins`，除非您设置了 [`CLAUDE_CODE_PLUGIN_CACHE_DIR`](/docs/zh-CN/env-vars)。表中的每个路径都相对于该根目录。

| 路径 | 它保存什么 |
| :- | :- |
| `cache/<marketplace>/<plugin>/<version>/` | 市场插件的每个已安装版本一个目录。`<plugin>` 是市场条目名称，`<version>` 是[已解析版本](#versions-and-updates)。`${CLAUDE_PLUGIN_ROOT}` 指向此目录 |
| `data/<plugin-id>/` | 插件的持久目录，公开为 `${CLAUDE_PLUGIN_DATA}`。有关如何形成 `<plugin-id>`，请参阅[路径变量和持久数据](/docs/zh-CN/plugins/components#path-variables-and-persistent-data)。Claude Code 在插件组件首次使用它时创建它，并在更新中保留它。默认情况下，当您从其最后一个范围卸载插件时，Claude Code 会删除它。有关 `--keep-data` 和它保留的其他情况，请参阅[插件卸载](/docs/zh-CN/plugins/cli-reference#plugin-uninstall) |
| `marketplaces/<name>/` | 从 GitHub、另一个 Git 主机或 URL 添加的市场的克隆或下载。从本地 `file` 或 `directory` 源添加的市场在此处没有副本，其 `installLocation` 在 `known_marketplaces.json` 中是您给定的路径 |
| `synced/` | Claude Code [从您的 claude.ai 账户同步的](#synced-plugins)插件 |
| `.trash/` | claude.ai 同步删除的插件，例如在您在 claude.ai 上关闭一个或停止同步后 |
| `installed_plugins.json` 和 `known_marketplaces.json` | Claude Code 已安装的内容和已获取的市场的记录，在[检查插件达到的阶段](#check-which-stage-a-plugin-reached)下描述。[托管在 claude.ai 上的市场](/docs/zh-CN/plugins/install#add-from-claude-ai)改为记录在 `known_marketplaces_claudeai.json` 中 |
| `flagged-plugins.json` | Claude Code 卸载的插件，因为其市场将其除名。它们出现在 `/plugin` 的 **Flagged** 部分；请参阅[托管市场](/docs/zh-CN/plugins/host-marketplace) |
| `installed_plugins.set-aside.<date>.<hash>.json` 和 `installed_plugins.unreadable.<date>.<hash>.kept` | Claude Code 在删除任何版本的 Claude Code 都无法使用的安装记录或重建不可读的 `installed_plugins.json` 之前保留的日期副本。请参阅[恢复说明](/docs/zh-CN/plugins/troubleshooting#installed-plugins-json-could-not-be-read-and-was-rebuilt)。它们按照 [`cleanupPeriodDays`](/docs/zh-CN/settings-reference#cleanupperioddays) 计划老化 |

因为 `${CLAUDE_PLUGIN_ROOT}` 指向版本目录，插件的根路径随每个版本更改。改为在 `${CLAUDE_PLUGIN_DATA}` 中保留插件的持久文件。

<h3 id="in-place-and-copied-plugins">
  就地和复制的插件
</h3>

Claude Code 根据插件的来源，从您保存它们的位置就地加载某些插件，并将其余的复制到缓存中：

* **`--plugin-dir` 和技能目录插件**：目录就地加载，永远不会被复制。`--plugin-url` 存档或 `--plugin-dir` `.zip` 首先被提取到会话临时目录中
* **您从本地路径添加的市场中的相对路径插件**：插件从市场文件夹内的其路径就地加载。您对源目录的编辑在下次会话启动或 `/reload-plugins` 时生效，您不需要增加版本。插件的 hook 进程以及 MCP 和 LSP 服务器接收指向源目录的 `CLAUDE_PLUGIN_ROOT`。有关其 Node.js 包依赖项，请参阅[依赖项安装何时运行](#when-the-dependency-install-runs)
* **[链接模式](/docs/zh-CN/plugins/marketplace-reference#command-plugin-source)中的 `command` 源插件**：命令打印的目录通过缓存条目中的链接就地加载
* **每个其他市场插件**：Claude Code 在安装时将插件复制到 `cache/<marketplace>/<plugin>/<version>/` 中，并从该副本加载。插件目录外的文件不会被复制，因此当复制的插件内的脚本读取插件根目录上方的路径（如 `../shared`）时，它找不到它们

<h3 id="paths-that-escape-the-plugin-directory">
  逃逸插件目录的路径
</h3>

无论插件就地加载还是从缓存副本加载，Claude Code 都不允许它声明其自己目录外的组件。它拒绝解析到插件根目录外的组件路径，无论路径是在 `plugin.json` 还是市场条目中声明的：

* **按书写指向插件外的路径**，例如 `../shared-utils`
* **导致插件外的符号链接**，除了[市场内插件之间的链接](/docs/zh-CN/plugins/host-marketplace#share-files-within-a-marketplace-with-symlinks)
* **在 macOS 和 Linux 上，路径中任何地方包含反斜杠的路径**，即使路径保留在插件内。因此使用反斜杠路径声明的组件仅在 Windows 上加载，所以使用正斜杠编写组件路径，例如 `./commands/deploy.md`

被拒绝的路径显示为[`path escapes plugin directory`](/docs/zh-CN/errors#path-escapes-plugin-directory)错误，插件加载时不包含该组件。

<h3 id="cleanup-of-previous-versions">
  以前版本的清理
</h3>

当您更新或卸载插件时，Claude Code 将 `.orphaned_at` 标记写入以前的版本目录。它在 14 天后的后台清理中删除该目录，因此已加载旧版本的会话继续运行。

扫描仅在 `installed_plugins.json` 记录至少一个安装时运行。卸载最后一个插件后，孤立目录保留到您安装另一个。

<h3 id="node-js-package-dependencies">
  Node.js 包依赖项
</h3>

当 Claude Code 将插件复制到缓存中时，它也会在那里安装插件的 Node.js 包依赖项，以便插件的 hooks 和 MCP 服务器可以加载它们。

本部分涵盖插件在其自己的 `package.json` 中声明的 npm 和 Bun 包。对于依赖其他插件的插件，请参阅[插件依赖项版本](/docs/zh-CN/plugins/dependencies)。

<h4 id="when-the-dependency-install-runs">
  依赖项安装何时运行
</h4>

Claude Code 每次创建复制的版本目录时，都会将依赖项安装到其中：

* 当您安装插件时
* 当 Claude Code 将插件更新到新版本时
* 在会话启动时，当已启用的插件未缓存时，例如在新机器上

对于从您通过本地路径添加的市场中[就地加载](#in-place-and-copied-plugins)的相对路径插件，Claude Code 不会将依赖项安装到源目录中。自己在那里安装它们，或从 hook 安装到[`${CLAUDE_PLUGIN_DATA}`](/docs/zh-CN/plugins/components#path-variables-and-persistent-data)。

安装仅在插件的根目录同时包含 `package.json` 和支持的锁定文件时运行。

锁定文件决定 Claude Code 运行哪个包管理器：

| 锁定文件 | 包管理器 |
| :- | :- |
| `bun.lock` | Bun |
| `npm-shrinkwrap.json` 或 `package-lock.json` | npm |

如果插件包含这些锁定文件中的多个，Claude Code 使用第一个匹配项，按顺序检查：`bun.lock`、`npm-shrinkwrap.json`、`package-lock.json`。

在以下锁定文件情况下，Claude Code 会跳过安装：

* **`bun.lockb`**：Bun 的二进制锁定文件无法被检查。请改为提供文本格式的 `bun.lock` 或 npm 锁定文件
* **`yarn.lock` 或 `pnpm-lock.yaml`**：请将其替换为 npm 锁定文件
* **Claude Code 无法读取的格式的锁定文件**：npm 锁定文件需要 `lockfileVersion` 为 `2` 或 `3`（由 npm 7 或更高版本写入），`bun.lock` 需要 `lockfileVersion` 不高于 `2`

包含 npm 锁定文件以到达最多用户。Claude Code 从用户的 PATH 运行匹配的锁定文件的包管理器，如果缺少该包管理器，不会尝试其他锁定文件。

对于通过 npm 源分发的插件，使用 `npm-shrinkwrap.json`，因为 npm 从已发布的包中排除 `package-lock.json`。

<h4 id="limits-on-the-dependency-install">
  依赖项安装的限制
</h4>

Claude Code 限制此依赖项安装，以便插件或其包中的任何代码在安装期间不执行，并限制其运行时间：

* **仅限注册表包**：每个依赖项都必须是在锁定文件中固定到精确版本的注册表包。具有 git、GitHub、文件夹、工作区或链接依赖项的插件不会进行安装。
* **`https` 下载**：锁定文件中的下载链接必须使用 `https`，除非它指向执行安装的用户自己的默认 npm 注册表。
* **单独的安装文件夹**：包管理器在其专用的文件夹中运行，该文件夹仅包含经过检查的依赖项列表的副本，因此 npm 和 Bun 不会读取插件的 `.npmrc`、`.env` 或 `bunfig.toml`。安装成功后，Claude Code 会将生成的 `node_modules` 移入插件中。
* **冻结解析**：安装严格使用锁定文件固定的版本，当 `package.json` 和锁定文件列出的依赖项不一致时，Claude Code 会跳过安装
* **无生命周期脚本**：`--ignore-scripts` 防止 `preinstall`、`install` 和 `postinstall` 脚本运行，因此在这些脚本中构建本机模块的依赖项在此安装期间下载但不编译
* **无覆盖或补丁**：`package.json` 设置了 npm `overrides` 的插件不会从 npm 锁定文件进行安装，设置了 Bun `patchedDependencies` 的插件不会从 `bun.lock` 进行安装
* **60 秒超时**：Claude Code 停止运行超过 60 秒的安装并将其视为失败

Claude Code 在此依赖项安装之前获取 npm 源插件，包的任何自己的安装脚本在获取期间不运行。请参阅 [npm 插件源](/docs/zh-CN/plugins/marketplace-reference#npm-plugin-source)。

您无法关闭自动安装。没有设置或环境变量禁用它。

在受限网络中，请参阅[网络访问要求](/docs/zh-CN/network-config#network-access-requirements)以允许的主机。

<h4 id="when-the-dependency-install-fails-or-is-skipped">
  依赖项安装失败或被跳过时
</h4>

如果安装失败或被跳过，插件仍会加载，但其中需要缺失包的部分可能无法正常工作。

对于已启用的插件，如果其缓存副本包含锁定文件和列出运行时依赖项的 `package.json`，但没有 `node_modules` 目录，`/plugin` 和 `claude plugin list` 会在该插件上显示一条说明。该说明会指出安装是未完成，还是无法针对此插件运行。有关每种情况的处理方法，请参阅[故障排除条目](/docs/zh-CN/plugins/troubleshooting#the-packages-it-lists-are-not-installed)。

当自动安装无法提供依赖项时，从 hook 安装到[持久数据目录](/docs/zh-CN/plugins/components#path-variables-and-persistent-data)。这包括需要其生命周期脚本来构建的包、Python 依赖项、使用 Yarn 或 pnpm 锁定的插件，以及不是注册表包的依赖项（例如 git 依赖项）。

<h2 id="versions-and-updates">
  版本和更新
</h2>

如果插件的作者推送了新提交，`claude plugin update` 打印 `<name> is already at the latest version (<version>).`，Claude Code 为插件计算的版本未更改，因此插件在磁盘上的文件不会更改。

Claude Code 为它安装的每个插件计算一个版本，这就是它如何检测更新的方式。`claude plugin update` 和后台自动更新会重新计算版本，当它与 `installed_plugins.json` 记录的内容匹配时，不会替换缓存副本。由您发起的更新仍可在该副本中[重试未完成的依赖安装](/docs/zh-CN/plugins/troubleshooting#the-packages-it-lists-are-not-installed)。

版本也命名插件的缓存目录。

固定 `"version"` 的清单是计算的版本在提交中保持相同的一种方式。有关解析顺序，请参阅[Claude Code 如何计算版本](#how-claude-code-computes-the-version)。

从您通过本地路径添加的市场中[就地加载](#in-place-and-copied-plugins)的插件在每次会话启动时加载其当前源文件，无论其版本字符串说什么。对于来自[托管在 claude.ai 上的市场](/docs/zh-CN/plugins/install#add-from-claude-ai)的插件，claude.ai 为插件记录的版本是其版本，清单的 `version` 不被读取。

<h3 id="how-claude-code-computes-the-version">
  Claude Code 如何计算版本
</h3>

对于您添加的市场，Claude Code 按插件市场条目的 `source` 类型选择规则。[市场参考](/docs/zh-CN/plugins/marketplace-reference#plugin-sources)列出源类型。对于该列表中除 `command` 外的每个源类型：

1. 插件清单中的 `version` 字段首先出现
2. 然后是插件市场条目中的 `version` 字段
3. 当都未设置时，版本来自源类型：

| 源类型 | 未设置 `version` 字段时的版本 |
| :- | :- |
| `github`、`url` 或 `git-subdir` | 源的提交 SHA，缩短为 12 个字符。`git-subdir` 版本也包含子目录路径的哈希 |
| `archive` | SHA-256 摘要，缩短为 12 个字符：市场条目中的 `sha256` 固定，或没有固定时下载文件的摘要 |
| Git 托管市场内的相对路径 | 已安装目录的提交 SHA |
| 本地目录，当插件目录和其市场都不是 git 存储库时 | `unknown` |
| `npm` | `unknown` |

Claude Code 不从包含安装路径的存储库（如 git 管理的 `~/.claude`）获取版本。

对于 `command` 源，Claude Code 始终从命令生成的内容派生版本：单独的 12 字符哈希，或当清单设置一个时的 `<manifest version>-<hash>`。市场条目的 `version` 对命令源被忽略。有关哈希覆盖的内容，请参阅[复制模式和链接模式](/docs/zh-CN/plugins/marketplace-reference#copy-mode-and-link-mode)。

因为清单首先出现，固定 `"version": "1.0.0"` 的清单将每个用户保留在缓存副本上，直到其作者更改字符串，无论他们推送多少提交。要让用户跟踪提交，请从清单和条目中都省略 `version`。[托管市场](/docs/zh-CN/plugins/host-marketplace)涵盖哪个选择适合哪个发布设置。

<h3 id="when-claude-code-refreshes-a-marketplace-before-an-install">
  Claude Code 在安装前何时刷新市场
</h3>

当您安装插件时，Claude Code 在其市场目录的本地副本中查找它。您可以在会话中运行 `/plugin install` 或在 shell 中运行 `claude plugin install`，并使用或不使用其市场命名插件。该表显示这些组合中哪些刷新本地副本。

| 插件名称 | 命令 | Claude Code 刷新什么 |
| :- | :- | :- |
| `name@marketplace` | `/plugin install` 或 `claude plugin install` | 命名的市场，在查找之前 |
| 仅 `name` | `/plugin install` | 仅具有自动更新的市场，仅在查找失败后 |
| 仅 `name` | `claude plugin install` | 无。它读取缓存的目录而不刷新 |

`name@marketplace` 安装之前的刷新不取决于市场的自动更新设置或 `DISABLE_AUTOUPDATER`。

当刷新失败时，安装从缓存的目录进行，`claude plugin install` 报告 `marketplace not refreshed`。

Claude Code 在以下情况下跳过 `name@marketplace` 安装之前的刷新：

* 市场是从本地 `file` 或 `directory` 源添加的，或在设置中使用[`settings` 源](/docs/zh-CN/settings-reference#extraknownmarketplaces)内联定义
* [种子目录](/docs/zh-CN/env-vars)提供市场
* Claude Code 在过去 30 秒内刷新了市场
* 您设置了 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`
* [托管设置](/docs/zh-CN/plugins/org#restrict-what-users-can-install)阻止市场，在这种情况下 Claude Code 也拒绝安装

<h3 id="when-auto-update-runs">
  自动更新何时运行
</h3>

在交互式会话中，在您发送第一条消息后，Claude Code 等待最多十分钟的随机延迟。然后它刷新每个启用自动更新的市场，并更新从它们安装的磁盘上的插件。

运行中的会话保留它加载的版本，您会看到 `Plugin updated: <name> · Run /reload-plugins to apply`。无论您是否重新加载，新版本都会在下次启动时加载。

<h4 id="which-marketplaces-and-plugins-auto-update">
  哪些市场和插件自动更新
</h4>

市场是否自动更新遵循首先设置的以下内容：

1. **其 `extraKnownMarketplaces` 条目中的 `autoUpdate`** 在设置文件中
2. **其 `known_marketplaces.json` 条目中的 `autoUpdate`**，`/plugin` **Marketplaces** 下的 **Enable auto-update** 切换写入。当设置文件也在 `extraKnownMarketplaces` 下声明市场时，切换也将 `autoUpdate` 写入该设置条目
3. **默认值**：对于 Anthropic 的官方市场（如 `claude-plugins-official`）打开，对于 `knowledge-work-plugins` 和 `first-party-plugins` 关闭，对于[从 claude.ai 添加的市场](/docs/zh-CN/plugins/install#add-from-claude-ai)打开，对于每个其他市场关闭

如果您设置 `DISABLE_UPDATES=1`、`DISABLE_AUTOUPDATER=1` 或 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC=1`，整个传递关闭，**Enable auto-update** 切换被隐藏，除非您也设置 `FORCE_AUTOUPDATE_PLUGINS=1`。[环境变量参考](/docs/zh-CN/env-vars)涵盖每个变量的更广泛影响。

自动更新也跳过其市场条目声明 `headersHelper` 的插件。[拒绝命令而不是询问的安装和更新](/docs/zh-CN/plugins/host-marketplace#installs-and-updates-that-refuse-the-command-instead-of-asking)解释何时这样的插件出现在 `/plugin` **Errors** 选项卡中以及如何从那里更新它。

当复制的插件在会话中期更新时，hook 命令、监视器、MCP 服务器和 LSP 服务器继续使用以前版本的路径。运行 `/reload-plugins` 以将 hooks、MCP 服务器和 LSP 服务器切换到新路径。监视器需要会话重启。

<h3 id="when-a-command-source-re-runs">
  何时命令源重新运行
</h3>

具有 `command` 源的插件不等待[自动更新传递](#when-auto-update-runs)。打印的目录反映工具在命令运行时的状态，因此 Claude Code 在以下时间再次运行[您接受的命令](/docs/zh-CN/plugins/host-marketplace#change-the-command-of-a-command-source)：

* 每次安装或更新插件时
* 每个已启用的命令源插件每个会话一次，在会话启动后不久在后台。此运行不取决于市场的自动更新设置或 `DISABLE_AUTOUPDATER`
* 在启动或 `/reload-plugins` 时，当已启用的插件的已安装版本在插件缓存中丢失时

当您设置 [`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`](/docs/zh-CN/env-vars) 时，Claude Code 跳过两个后台运行。显式安装和更新仍然使用该变量集运行命令。

当命令的哈希输出已更改时，Claude Code 将结果安装为新版本并在运行中的交互式会话中重新加载它，切换[`/reload-plugins` 切换的相同组件](/docs/zh-CN/plugins/cli-reference#reload-plugins)。您会看到插件已重新加载的通知。

如果就地重新加载会使会话的提示缓存失效，Claude Code 改为提示您运行 `/reload-plugins`，它[警告缓存成本并在使用 `--force` 重新运行时应用](/docs/zh-CN/prompt-caching#enabling-or-disabling-a-plugin)。

<h2 id="name-conflicts">
  名称冲突
</h2>

当来自不同来源的已启用插件共享清单名称时，此顺序决定哪个加载，从最高优先级到最低：

1. 其 id 出现在托管设置 `enabledPlugins` 中的插件，作为 `true` 或 `false`。其清单名称与 id 的名称部分匹配的 `--plugin-dir` 副本不被加载，您会看到 `--plugin-dir copy of "<name>" ignored: plugin is locked by managed settings`
2. 已启用的 `--plugin-dir`、`--plugin-url` 或 `CLAUDE_CODE_PLUGIN_DIRS` 插件。它替换同名的已安装市场插件或技能目录插件：
   * **已安装的市场插件**：无声替换。`claude plugin list` 仍然显示市场行为已启用，因为该行反映您的设置。仅当您使用 `--debug` 启动时 Claude Code 在 `~/.claude/debug/` 下写入的日志记录 `Plugin "<name>" from --plugin-dir overrides installed version`
   * **技能目录插件**：替换为 `/plugin` **Errors** 选项卡行，读取 `Not loaded — the name "<name>" is already taken by a session-only plugin (--plugin-dir / --plugin-url), which takes precedence`
3. 已安装的市场插件。同名的技能目录插件获得相同的 `Not loaded` 行，命名已安装的插件
4. 技能目录插件。在这两者之间，`~/.claude/skills/` 下的副本加载，项目的 `.claude/skills/` 副本被删除，带有一行说明哪个路径遮蔽了它
5. [从 claude.ai 同步的](#synced-plugins)插件。当来自任何其他来源的已启用插件与其名称匹配时，Claude Code 加载该插件并报告同步副本未加载。要改为使用 claude.ai 副本，请禁用您自己的副本

因为顺序比较清单名称，名为 `hello-plugin` 的 `--plugin-dir` 插件在该插件的清单也说 `"name": "hello-plugin"` 时替换 `hello@example-marketplace`。

<h3 id="keep-a-session-only-plugin-from-loading">
  防止会话专用插件加载
</h3>

要防止 `--plugin-dir` 插件遮蔽任何内容，或在父进程为您传递标志时关闭一个，请在任何设置文件中将其 id 设置为 `false`。对于清单名称为 `hello-plugin` 的插件，条目是 `"enabledPlugins": {"hello-plugin@inline": false}`。禁用的会话专用插件不遮蔽，因此市场或技能目录副本加载。

<h2 id="next-steps">
  后续步骤
</h2>

* [安装和管理插件](/docs/zh-CN/plugins/install)：安装、启用、禁用和更新步骤本身
* [插件故障排除](/docs/zh-CN/plugins/troubleshooting)：按生成它们的阶段分类的错误消息
* [插件命令参考](/docs/zh-CN/plugins/cli-reference)：此页面上命名的标志和命令
* [为您的组织管理插件](/docs/zh-CN/plugins/org)：强制启用或阻止插件的托管设置
