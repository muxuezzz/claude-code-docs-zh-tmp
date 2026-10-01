> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# Anthropic 的插件市场

> Anthropic 官方、社区和演示插件市场的 Claude Code：它们的名称、存储库、如何添加每个市场，以及在哪里浏览它们的插件。

Anthropic 为 Claude Code 发布了三个通用插件市场：[官方](https://github.com/anthropics/claude-plugins-official)、[社区](https://github.com/anthropics/claude-plugins-community)和[演示](https://github.com/anthropics/claude-code)。每个都是其自己的 GitHub 存储库中的插件目录。当你在 Claude Code 会话中从其中一个安装插件时，你在 `@` 后面输入市场的名称，如 `/plugin install commit-commands@claude-plugins-official`。

使用此页面来区分这三个市场，并找到检查官方市场是否包含给定插件的位置。

<Note>
  这些情况在其他页面上有介绍：

  * **如何安装插件**：请参阅[安装插件](/docs/zh-CN/plugins/install)
  * **安装失败**：请参阅[插件故障排除](/docs/zh-CN/plugins/troubleshooting)
</Note>

转到你需要的页面部分：

* 要按存储库、市场名称和获取方式来区分这三个市场，请参阅 [Anthropic 的插件市场](#anthropic%E2%80%99s-marketplaces)。
* 要在官方市场中查找插件，请参阅[在官方市场中查找插件](#find-plugins-in-the-official-marketplace)。

<h2 id="anthropic’s-marketplaces">
  Anthropic 的插件市场
</h2>

市场是一个插件目录，由存储库在其 `.claude-plugin/marketplace.json` 文件中定义。官方、社区和演示市场各自来自自己的 GitHub 存储库。Anthropic 还发布主题特定的市场，例如 `anthropics/skills` 和 `anthropics/knowledge-work-plugins`，你可以在 Claude Code 会话中使用 `/plugin marketplace add <owner>/<repo>` 添加。

此表给出了每个市场的存储库和市场名称，这是你从该市场安装插件时在 `@` 后面输入的内容。社区市场的名称是 `claude-community`，而不是其存储库名称。

| | 官方 | 社区 | 演示 |
| :- | :- | :- | :- |
| 存储库 | [`anthropics/claude-plugins-official`](https://github.com/anthropics/claude-plugins-official) | [`anthropics/claude-plugins-community`](https://github.com/anthropics/claude-plugins-community) | [`anthropics/claude-code`](https://github.com/anthropics/claude-code/tree/main/plugins) |
| 市场名称 | `claude-plugins-official` | `claude-community` | `claude-code-plugins` |
| 其中包含的内容 | Anthropic 维护的插件，加上来自合作伙伴和其他作者的插件 | 第三方插件，由其作者提交给 Anthropic | 一小组示例插件，展示插件可以包含的内容 |
| 获取方式 | Claude Code 在你首次启动交互式终端会话时添加它，除非[托管策略](/docs/zh-CN/plugins/org#allow-the-official-marketplace-and-your-own)或 `CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL` 阻止它。如果缺少，请参阅[市场 `claude-plugins-official` 未找到](/docs/zh-CN/plugins/troubleshooting#marketplace-claude-plugins-official-not-found) | 你在 Claude Code 会话中使用 `/plugin marketplace add anthropics/claude-plugins-community` 添加它 | 你在 Claude Code 会话中使用 `/plugin marketplace add anthropics/claude-code` 添加它 |

如果你编写了插件并希望其他人安装它，请参阅[发布插件](/docs/zh-CN/plugins/publish)，其中涵盖了你自己的市场和提交到 Anthropic 的目录。

<h3 id="the-demo-marketplace-in-anthropics/claude-code">
  `anthropics/claude-code` 中的演示市场
</h3>

如果教程或较旧的说明告诉你运行 `/plugin marketplace add anthropics/claude-code`，这会添加演示市场，名为 `claude-code-plugins`。这不是官方市场，Claude Code 已经为你添加了。

演示市场的大多数插件也在官方市场中以相同的名称存在。例如，`code-review`、`feature-dev`、`commit-commands` 和 `security-guidance` 都在两者中。从 `claude-plugins-official` 安装这些，这样你就不会安装两个副本。

<h2 id="find-plugins-in-the-official-marketplace">
  在官方市场中查找插件
</h2>

官方市场 `claude-plugins-official` 是 Claude Code 为你添加的市场。它列出的大部分内容来自合作伙伴和其他作者，而不是来自 Anthropic：工具供应商发布连接 Claude Code 到其服务的插件，Anthropic 维护一个较小的自己的插件集，例如 `commit-commands`、`code-review`、`feature-dev` 和[语言服务器插件](/docs/zh-CN/plugins/code-intelligence)。目录经常变化，所以此页面不列出它。

要查看其中的内容，请在 Claude Code 会话中使用 `/plugin` 的 **Discover** 选项卡（你可以搜索），或在网络上浏览 [Claude Marketplace](https://claude.com/marketplace/plugins)。

<h2 id="browse-and-install-from-anthropic’s-marketplaces">
  从 Anthropic 的市场浏览和安装
</h2>

你可以在 Claude Code、网络或 GitHub 上搜索 Anthropic 的市场中的插件：

* **在 Claude Code 中，通过浏览**：在交互式会话中运行 `/plugin`。其 **Discover** 选项卡列出了你添加的市场中的插件。
* **在 Claude Code 中，按名称**：在会话中运行 `/plugin install <name>`，它会在你添加的市场中查找该名称。如果插件在其中一个中，其详细信息会在 `/plugin` 面板中打开，在你选择[安装范围](/docs/zh-CN/plugins/install#install-a-plugin)并在那里确认之前，不会安装任何内容。如果不在，你会看到 `Plugin "<name>" not found in any marketplace`。
* **在网络上**：在 [Claude Marketplace](https://claude.com/marketplace/plugins) 上搜索完整目录，它显示安装计数并标记一些插件为 **Anthropic verified**。
* **在 GitHub 上**：打开市场存储库中的 `.claude-plugin/marketplace.json`，例如 [`anthropics/claude-plugins-official`](https://github.com/anthropics/claude-plugins-official)。该文件就是目录本身。

Anthropic 的目录与这些市场分开。该目录是 claude.ai 上的目录，`/plugin` 不会列出它。你从 claude.ai 上的目录添加的插件通过[账户同步](/docs/zh-CN/plugins/loading#synced-plugins)到达 Claude Code。要在那里列出你自己的插件，请参阅[提交到 Anthropic 的目录](/docs/zh-CN/plugins/publish#submit-to-anthropics-directory)。

要从桌面应用或脚本安装，或查看云会话加载的内容，请参阅[安装插件](/docs/zh-CN/plugins/install)。

<h3 id="add-the-community-or-demo-marketplace">
  添加社区或演示市场
</h3>

社区和演示市场在你在 Claude Code 会话中添加它们之前不会注册：

* **社区**：运行 `/plugin marketplace add anthropics/claude-plugins-community`，然后使用 `@claude-community` 后缀安装。
* **演示**：运行 `/plugin marketplace add anthropics/claude-code`，然后使用 `@claude-code-plugins` 后缀安装。

如果 `claude-plugins-official` 不在 `/plugin` 的 **Marketplaces** 选项卡上，用 `/plugin marketplace add anthropics/claude-plugins-official` 以相同的方式添加它。

对于 `not found` 错误和无法添加的市场，请参阅[插件故障排除](/docs/zh-CN/plugins/troubleshooting#install-a-plugin)。

<h2 id="third-party-marketplaces">
  第三方市场
</h2>

许多流行的插件不在任何 Anthropic 市场中。它们在其作者自己的市场中，通常是一个 GitHub 存储库，其根目录中有 `.claude-plugin/marketplace.json`。

Anthropic 不审查第三方市场，所以在添加一个之前，请阅读[插件安全和信任](/docs/zh-CN/plugins/security)。

要使用第三方市场，在 Claude Code 会话中使用 `/plugin marketplace add <owner>/<repo>` 添加其存储库，然后使用 `/plugin install <plugin>@<marketplace-name>` 安装。市场名称是该 `marketplace.json` 的 `name` 字段，Claude Code 在添加市场后会打印它。

有关添加市场的其他方式，请参阅[添加市场](/docs/zh-CN/plugins/install#add-a-marketplace)。

<h2 id="next-steps">
  后续步骤
</h2>

* [安装和管理插件](/docs/zh-CN/plugins/install)：从这些市场之一安装插件并选择范围
* [插件安全和信任](/docs/zh-CN/plugins/security)：插件可以在你的机器上做什么，以及在安装前如何审查插件
* [代码智能插件](/docs/zh-CN/plugins/code-intelligence)：安装官方市场的语言服务器插件之一
* [创建市场](/docs/zh-CN/plugins/create-marketplace)：在 Anthropic 的市场旁边运行你自己的市场
