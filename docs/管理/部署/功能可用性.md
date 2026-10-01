> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 功能可用性

> 比较 Claude Code 功能在 Anthropic 订阅计划、Anthropic Console、Amazon Bedrock、AWS 上的 Claude Platform、Google Cloud 的 Agent Platform 和 Microsoft Foundry 中的可用性。

Claude Code CLI 和所有本地运行的功能在每个提供商上的工作方式完全相同。有关每个提供商的设置说明，请参阅[企业部署概述](/docs/zh-CN/third-party-integrations)。要直接跳到您的提供商上缺少的功能，请参阅[按提供商汇总](#summary-by-provider)选项卡。

在下表中，✓ 表示可用，✗ 表示不可用，"See note"链接到脚注以获取部分支持。✓ 后面的限定符将可用性缩小到该子集，"Admin-enabled"表示该功能处于关闭状态，直到组织管理员将其打开。

<h2 id="availability-by-model-provider">
  按模型提供商的可用性
</h2>

您的身份验证方式决定了 Claude Code 可以访问哪些功能。有关您的提供商上缺少的内容的单一列表，请参阅[按提供商汇总](#summary-by-provider)选项卡。要在表格中找到您的列：

* **Claude 订阅**：您使用 claude.ai 账户登录 Pro、Max、Team 或 Enterprise 计划
* **Anthropic Console**：您使用 Anthropic API 密钥进行身份验证，或者[在没有 API 密钥的情况下登录 Console 账户](/docs/zh-CN/authentication#sign-in-without-an-api-key)
* **Amazon Bedrock**：您从 Amazon Bedrock 模型目录中使用 Claude 模型并设置 `CLAUDE_CODE_USE_BEDROCK`。[Mantle 端点](/docs/zh-CN/amazon-bedrock#use-the-mantle-endpoint)（`CLAUDE_CODE_USE_MANTLE`）由此列涵盖
* **Claude Platform on AWS**：您通过 AWS Marketplace 购买了 Claude，但调用 Anthropic API，并设置 `CLAUDE_CODE_USE_ANTHROPIC_AWS`
* **Google Cloud's Agent Platform**：由 Google 运营；您设置 `CLAUDE_CODE_USE_VERTEX`
* **Microsoft Foundry**：由 Anthropic 运营；您设置 `CLAUDE_CODE_USE_FOUNDRY`

<h3 id="features-available-on-every-provider">
  每个提供商都可用的功能
</h3>

这些在每个提供商上都有效：

* [CLI](/docs/zh-CN/quickstart) 和 [Agent SDK](/docs/zh-CN/agent-sdk/overview)
* [VS Code](/docs/zh-CN/vs-code) 和 [JetBrains](/docs/zh-CN/jetbrains) 扩展
* [Subagents](/docs/zh-CN/sub-agents)、[hooks](/docs/zh-CN/hooks-guide)、[commands](/docs/zh-CN/commands) 和 [skills](/docs/zh-CN/skills)
* [CLAUDE.md memory](/docs/zh-CN/memory)、[plugins](/docs/zh-CN/plugins/overview) 和 [MCP servers](/docs/zh-CN/mcp)
* [Checkpoints](/docs/zh-CN/checkpointing)、[sandboxing](/docs/zh-CN/sandboxing) 和 [Workflows](/docs/zh-CN/workflows)
* [OpenTelemetry metrics](/docs/zh-CN/monitoring-usage) 和[托管设置文件](/docs/zh-CN/managed-settings#delivery-mechanisms)

这些有提供商特定的差异：

* **MCP servers**：[来自 claude.ai 的连接器](/docs/zh-CN/mcp#use-mcp-servers-from-claude-ai)仅在您的 claude.ai 订阅是活跃身份验证方法时加载。[工具搜索](/docs/zh-CN/mcp#configure-tool-search)在 `ANTHROPIC_BASE_URL` 指向非第一方主机时默认关闭，在 Google Cloud's Agent Platform 上早于 Claude 4.5 代的模型或在 Microsoft Foundry [部署在 Azure 上](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry#hosting-options)时不受支持
* **Subagents**：内置的 [Explore subagent](/docs/zh-CN/sub-agents#built-in-subagents) 在 Claude API 上将其继承的模型限制为 Opus，在任何其他提供商（包括 Claude Platform on AWS）上直接继承主对话的模型
* **[Commands](/docs/zh-CN/commands#all-commands)**：
  * `/design-sync` 和 `/import` 及其 `claude import` 子命令形式在 Amazon Bedrock、Google Cloud's Agent Platform、Microsoft Foundry 和 Claude Platform on AWS 上不可用，以及通过 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway#availability-and-limitations)
  * `/voice` 需要 claude.ai 账户
  * `/list-agents` 及其别名 `/peers` 仅在[启用了跨会话消息传递](/docs/zh-CN/cross-session-messaging#availability)的会话中可用

<h3 id="features-that-require-a-claude-subscription">
  需要 Claude 订阅的功能
</h3>

这些需要使用 claude.ai 账户登录，无法通过 Anthropic Console API 密钥或第三方提供商访问：

* [网络上的 Claude Code](/docs/zh-CN/claude-code-on-the-web)、移动设备上的 Claude Code 和 [Slack 中的 Claude Code](/docs/zh-CN/slack)
* [Claude Code Desktop](/docs/zh-CN/desktop)
* [Routines](/docs/zh-CN/routines)（`/schedule`）
* [Ultrareview](/docs/zh-CN/ultrareview)
* [Code Review](/docs/zh-CN/code-review)：Team 和 Enterprise 计划
* [Remote Control](/docs/zh-CN/remote-control)
* [Chrome 扩展](/docs/zh-CN/chrome)
* [Computer use](/docs/zh-CN/computer-use)：Pro 和 Max 计划
* [Artifacts](/docs/zh-CN/artifacts)：Pro、Max、Team 和 Enterprise 计划
* [Voice dictation](/docs/zh-CN/voice-dictation)

Desktop 是部分例外：[网关路由可以在应用中或由管理员配置](/docs/zh-CN/llm-gateway-connect#desktop-app)，Enterprise 部署可以通过[托管设置](https://claude.com/docs/third-party/claude-desktop/configuration)将 Desktop 路由到 Google Cloud's Agent Platform 或网关提供商，[Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/overview) 在 Amazon Bedrock、Google Cloud's Agent Platform、Microsoft Foundry 或自托管 LLM 网关上运行 Code 选项卡。有关这些功能的按计划可用性，请参阅[按订阅计划的可用性](#availability-by-subscription-plan)。

<h3 id="cli-capabilities-that-vary-by-provider">
  按提供商变化的 CLI 功能
</h3>

这些功能在本地 CLI 中工作，但取决于并非每个提供商都公开的服务器端功能。

<table>
  <thead>
    <tr>
      <th>功能</th>
      <th>Claude 订阅</th>
      <th>Anthropic Console</th>
      <th>Amazon Bedrock</th>
      <th>Claude Platform on AWS</th>
      <th>Google Cloud's Agent Platform</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>[Web search](/docs/zh-CN/tools-reference#websearch-tool-behavior)</td>
      <td>✓</td>
      <td>✓</td>
      <td>✗</td>
      <td>✓</td>
      <td>参见注释 <sup><a href="#fn1">1</a></sup></td>
      <td>✓（[部署在 Anthropic 上](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry#hosting-options)）</td>
    </tr>

    <tr>
      <td>[Fast mode](/docs/zh-CN/fast-mode)</td>
      <td>✓（[所有者启用](/docs/zh-CN/fast-mode#enable-fast-mode-for-your-organization) Team 和 Enterprise）</td>
      <td>✓（预配置的组织）</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
    </tr>

    <tr>
      <td>[Auto mode](/docs/zh-CN/auto-mode-config)</td>
      <td>✓</td>
      <td>✓</td>
      <td>参见注释 <sup><a href="#fn2">2</a></sup></td>
      <td>✓</td>
      <td>参见注释 <sup><a href="#fn2">2</a></sup></td>
      <td>参见注释 <sup><a href="#fn2">2</a></sup></td>
    </tr>

    <tr>
      <td>[Advisor](/docs/zh-CN/advisor)</td>
      <td>✓</td>
      <td>✓</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
    </tr>

    <tr>
      <td>[Cross-session messaging](/docs/zh-CN/cross-session-messaging)</td>
      <td>✓ <sup><a href="#fn5">5</a></sup></td>
      <td>✓（同一台机器）<sup><a href="#fn5">5</a></sup></td>
      <td>✓（同一台机器）<sup><a href="#fn5">5</a></sup></td>
      <td>✓（同一台机器）<sup><a href="#fn5">5</a></sup></td>
      <td>✓（同一台机器）<sup><a href="#fn5">5</a></sup></td>
      <td>✓（同一台机器）<sup><a href="#fn5">5</a></sup></td>
    </tr>

    <tr>
      <td>[Channels](/docs/zh-CN/channels)</td>
      <td>✓</td>
      <td>✓</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
    </tr>

    <tr>
      <td>[GitHub Actions](/docs/zh-CN/github-actions)</td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>✗</td>
      <td>✓</td>
      <td>✓</td>
    </tr>

    <tr>
      <td>[GitLab CI/CD](/docs/zh-CN/gitlab-ci-cd)</td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>✓</td>
      <td>✗</td>
    </tr>
  </tbody>
</table>

<h3 id="admin-and-analytics">
  管理和分析
</h3>

组织级别的控制和使用情况可见性。

<table>
  <thead>
    <tr>
      <th>功能</th>
      <th>Claude 订阅</th>
      <th>Anthropic Console</th>
      <th>Amazon Bedrock</th>
      <th>Claude Platform on AWS</th>
      <th>Google Cloud's Agent Platform</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>[Analytics dashboard and API](/docs/zh-CN/analytics)</td>
      <td>✓（仪表板：Team 和 Enterprise；API：Enterprise）</td>
      <td>✓ <sup><a href="#fn4">4</a></sup></td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
    </tr>

    <tr>
      <td>[Server-managed settings](/docs/zh-CN/server-managed-settings)</td>
      <td>✓（Team 和 Enterprise）</td>
      <td>✓（Team 和 Enterprise）</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
      <td>✗</td>
    </tr>

    <tr>
      <td>[Zero Data Retention](/docs/zh-CN/zero-data-retention)</td>
      <td>✓（合格的 Enterprise 账户）</td>
      <td>✓（合格的账户）</td>
      <td>参见注释 <sup><a href="#fn3">3</a></sup></td>
      <td>✓（合格的账户）</td>
      <td>参见注释 <sup><a href="#fn3">3</a></sup></td>
      <td>参见注释 <sup><a href="#fn3">3</a></sup></td>
    </tr>
  </tbody>
</table>

<span id="fn1" style={{display: 'block', position: 'relative', top: '-120px'}} /><sup>1</sup> 在 Google Cloud's Agent Platform 上，web search 适用于 Claude 4 及更高版本的模型。<br />
<span id="fn2" style={{display: 'block', position: 'relative', top: '-120px'}} /><sup>2</sup> 在这些提供商上，auto mode 仅支持 Claude Sonnet 5、Opus 4.7 或更高版本以及 Fable 模型。请参阅 [Auto mode 配置](/docs/zh-CN/auto-mode-config)。有关会话在这些提供商上启动时所处的权限模式，请参阅[会话启动时的模式](/docs/zh-CN/permission-modes#which-mode-a-session-starts-in)。在 v2.1.158 到 v2.1.206 中，这些提供商上的 auto mode 还需要设置 `CLAUDE_CODE_ENABLE_AUTO_MODE=1`；v2.1.207 移除了该要求。<br />
<span id="fn3" style={{display: 'block', position: 'relative', top: '-120px'}} /><sup>3</sup> 受您与云提供商的协议约束。<br />
<span id="fn4" style={{display: 'block', position: 'relative', top: '-120px'}} /><sup>4</sup> 仅限仪表板和 API。[贡献指标](/docs/zh-CN/analytics#enable-contribution-metrics)需要 claude.ai Team 或 Enterprise 组织。<br />
<span id="fn5" style={{display: 'block', position: 'relative', top: '-120px'}} /><sup>5</sup> 在 macOS 和 Linux 上需要 Claude Code v2.1.224 或更高版本，包括 WSL 2 内的 Linux。在原生 Windows 上，需要 Claude Code v2.1.234 或更高版本。使用 API 密钥身份验证时，消息传递仅限同一台机器。在 Amazon Bedrock、Claude Platform on AWS、Google Cloud's Agent Platform 和 Microsoft Foundry 上，消息传递仅限同一台机器，需要 Claude Code v2.1.248 或更高版本。Claude 只能从连接到 [Remote Control](/docs/zh-CN/remote-control) 的会话中找到您的 [cloud sessions](/docs/zh-CN/claude-code-on-the-web) 和其他机器上的会话。要连接，您需要 claude.ai 登录和其他 [Remote Control 要求](/docs/zh-CN/remote-control#requirements)。请参阅[在其他机器上发送消息](/docs/zh-CN/cross-session-messaging#message-sessions-on-other-machines)。

<Note>
  如果您通过 [LLM gateway](/docs/zh-CN/llm-gateway) 进行身份验证，功能可用性与网关转发到的基础提供商相匹配，除了 Claude Code 本身关闭的功能。每当 `ANTHROPIC_BASE_URL` 指向 `api.anthropic.com` 以外的主机时，Claude Code 会关闭功能，例如 [Remote Control](/docs/zh-CN/remote-control#requirements) 和 [server-managed settings](/docs/zh-CN/server-managed-settings#platform-availability)，无论网关转发什么。某些仅限 Anthropic 的功能，例如 [Advisor](/docs/zh-CN/advisor)，仅在网关将请求完整转发到 Anthropic API 时才有效。

  有关 Claude Code 发送的请求在 Amazon Bedrock 或 Agent Platform 格式网关、`ANTHROPIC_BASE_URL` 网关和 Claude apps gateway 登录之间如何不同，请参阅[按连接方法的客户端行为](/docs/zh-CN/llm-gateway-protocol#how-the-connection-method-changes-client-behavior)。
</Note>

<h3 id="summary-by-provider">
  按提供商汇总
</h3>

每个选项卡列出了该提供商上不可用或部分支持的内容，以及存在替代方案的地方。未列出的所有内容的工作方式与 Claude 订阅上相同，除了上面注明的[提供商特定的差异](#features-available-on-every-provider)。在 Amazon Bedrock、Google Cloud's Agent Platform、Microsoft Foundry 和 Claude Platform on AWS 上，错误报告和遥测到 Anthropic 默认处于关闭状态。请参阅[按 API 提供商的默认行为](/docs/zh-CN/data-usage#default-behaviors-by-api-provider)了解哪些流量仍然到达 Anthropic 以及如何选择退出。

<Tabs>
  <Tab title="Amazon Bedrock">
    **不可用：** 所有[需要 Claude 订阅的功能](#features-that-require-a-claude-subscription)，加上 [web search](/docs/zh-CN/tools-reference#websearch-tool-behavior)、[fast mode](/docs/zh-CN/fast-mode)、[Advisor](/docs/zh-CN/advisor)、[Channels](/docs/zh-CN/channels)、[analytics dashboard](/docs/zh-CN/analytics)、[server-managed settings](/docs/zh-CN/server-managed-settings) 和 [`/design-sync` 和 `/import` 命令](/docs/zh-CN/commands#all-commands)。

    **部分支持：**

    * [Desktop](/docs/zh-CN/desktop)：仅通过 [Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/overview)
    * [Auto mode](/docs/zh-CN/auto-mode-config)：仅 Sonnet 5、Opus 4.7 或更高版本以及 Fable 模型
    * [Cross-session messaging](/docs/zh-CN/cross-session-messaging)：仅在此机器上的您的会话之间 <sup><a href="#fn5">5</a></sup>
    * [Zero Data Retention](/docs/zh-CN/zero-data-retention)：受您的 AWS 协议约束

    **替代方案：** 对于调度，使用 [`/loop`](/docs/zh-CN/scheduled-tasks) 而不是 `/schedule`。对于云会话，使用 [GitHub Actions](/docs/zh-CN/github-actions) 或 [GitLab CI/CD](/docs/zh-CN/gitlab-ci-cd)。对于网络查询，使用带有特定 URL 的 [WebFetch tool](/docs/zh-CN/tools-reference#webfetch-tool-behavior)。
  </Tab>

  <Tab title="Claude Platform on AWS">
    **不可用：** 所有[需要 Claude 订阅的功能](#features-that-require-a-claude-subscription)，加上 [fast mode](/docs/zh-CN/fast-mode)、[Advisor](/docs/zh-CN/advisor)、[Channels](/docs/zh-CN/channels)、[GitHub Actions](/docs/zh-CN/github-actions)、[analytics dashboard](/docs/zh-CN/analytics)、[server-managed settings](/docs/zh-CN/server-managed-settings) 和 [`/design-sync` 和 `/import` 命令](/docs/zh-CN/commands#all-commands)。

    **Amazon Bedrock 不可用的地方可用：** [web search](/docs/zh-CN/tools-reference#websearch-tool-behavior)。

    **部分支持：**

    * [Cross-session messaging](/docs/zh-CN/cross-session-messaging)：仅在此机器上的您的会话之间 <sup><a href="#fn5">5</a></sup>

    **替代方案：** 对于调度，使用 [`/loop`](/docs/zh-CN/scheduled-tasks) 而不是 `/schedule`。对于云会话，使用 [GitLab CI/CD](/docs/zh-CN/gitlab-ci-cd)。
  </Tab>

  <Tab title="Google Cloud's Agent Platform">
    **不可用：** 所有[需要 Claude 订阅的功能](#features-that-require-a-claude-subscription)，加上 [fast mode](/docs/zh-CN/fast-mode)、[Advisor](/docs/zh-CN/advisor)、[Channels](/docs/zh-CN/channels)、[analytics dashboard](/docs/zh-CN/analytics)、[server-managed settings](/docs/zh-CN/server-managed-settings) 和 [`/design-sync` 和 `/import` 命令](/docs/zh-CN/commands#all-commands)。

    **部分支持：**

    * [Desktop](/docs/zh-CN/desktop)：通过[托管设置](https://claude.com/docs/third-party/claude-desktop/configuration)或 [Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/overview)
    * [Web search](/docs/zh-CN/tools-reference#websearch-tool-behavior)：Claude 4 及更高版本的模型
    * [Auto mode](/docs/zh-CN/auto-mode-config)：仅 Sonnet 5、Opus 4.7 或更高版本以及 Fable 模型
    * [Cross-session messaging](/docs/zh-CN/cross-session-messaging)：仅在此机器上的您的会话之间 <sup><a href="#fn5">5</a></sup>
    * [Zero Data Retention](/docs/zh-CN/zero-data-retention)：受您的 Google Cloud 协议约束

    **替代方案：** 对于调度，使用 [`/loop`](/docs/zh-CN/scheduled-tasks) 而不是 `/schedule`。对于云会话，使用 [GitHub Actions](/docs/zh-CN/github-actions) 或 [GitLab CI/CD](/docs/zh-CN/gitlab-ci-cd)。
  </Tab>

  <Tab title="Microsoft Foundry">
    **不可用：** 所有[需要 Claude 订阅的功能](#features-that-require-a-claude-subscription)，加上 [fast mode](/docs/zh-CN/fast-mode)、[Advisor](/docs/zh-CN/advisor)、[Channels](/docs/zh-CN/channels)、[GitLab CI/CD](/docs/zh-CN/gitlab-ci-cd)、[analytics dashboard](/docs/zh-CN/analytics)、[server-managed settings](/docs/zh-CN/server-managed-settings) 和 [`/design-sync` 和 `/import` 命令](/docs/zh-CN/commands#all-commands)。

    **部分支持：**

    * [Desktop](/docs/zh-CN/desktop)：仅通过 [Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/overview)
    * [Web search](/docs/zh-CN/tools-reference#websearch-tool-behavior)：[部署在 Anthropic 上](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry#hosting-options)仅
    * [Auto mode](/docs/zh-CN/auto-mode-config)：仅 Sonnet 5、Opus 4.7 或更高版本以及 Fable 模型
    * [Cross-session messaging](/docs/zh-CN/cross-session-messaging)：仅在此机器上的您的会话之间 <sup><a href="#fn5">5</a></sup>
    * [Zero Data Retention](/docs/zh-CN/zero-data-retention)：受您的 Azure 协议约束

    **替代方案：** 对于调度，使用 [`/loop`](/docs/zh-CN/scheduled-tasks) 而不是 `/schedule`。对于云会话，使用 [GitHub Actions](/docs/zh-CN/github-actions)。
  </Tab>

  <Tab title="Anthropic Console">
    **不可用：** 所有[需要 Claude 订阅的功能](#features-that-require-a-claude-subscription)。

    [按提供商变化的 CLI 功能](#cli-capabilities-that-vary-by-provider)中的所有内容都可用，除了 [fast mode](/docs/zh-CN/fast-mode) 需要[预配置访问](/docs/zh-CN/fast-mode#enable-fast-mode-for-your-organization)。当您的 API 密钥属于 Team 或 Enterprise 组织时，[Server-managed settings](/docs/zh-CN/server-managed-settings) 也可用。
  </Tab>
</Tabs>

<h2 id="availability-by-subscription-plan">
  按订阅计划的可用性
</h2>

如果您通过 Amazon Bedrock、Google Cloud 的 Agent Platform、Microsoft Foundry 或 Anthropic Console API 密钥进行身份验证，本部分不适用于您。当您使用 claude.ai 账户登录时，您的计划决定了以下哪些功能可用。

| 功能 | Pro | Max | Team | Enterprise |
| :- | :- | :- | :- | :- |
| [网络上的 Claude Code](/docs/zh-CN/claude-code-on-the-web) | ✓ | ✓ | ✓ | ✓ <sup><a href="#fn6">6</a></sup> |
| [Routines](/docs/zh-CN/routines) | ✓ | ✓ | ✓ | ✓ |
| [Remote Control](/docs/zh-CN/remote-control) | ✓ | ✓ | Admin-enabled | Admin-enabled |
| [Channels](/docs/zh-CN/channels) | ✓ | ✓ | Admin-enabled | Admin-enabled |
| [Computer use](/docs/zh-CN/computer-use) | ✓ | ✓ | ✗ | ✗ |
| Dispatch ([Desktop](/docs/zh-CN/desktop#sessions-from-dispatch)) | ✓ | ✓ | ✗ | ✗ |
| [Code Review](/docs/zh-CN/code-review) | ✗ | ✗ | ✓ | ✓ |
| [Artifacts](/docs/zh-CN/artifacts) | ✓ | ✓ | ✓ | ✓ |
| [分析仪表板和贡献指标](/docs/zh-CN/analytics) | ✗ | ✗ | ✓ | ✓ |
| [Enterprise Analytics API](/docs/zh-CN/analytics#access-data-programmatically) | ✗ | ✗ | ✗ | ✓ |
| [Server-managed settings](/docs/zh-CN/server-managed-settings) | ✗ | ✗ | ✓ | ✓ |
| [SSO](https://support.claude.com/en/articles/9266767-what-is-the-team-plan) | ✗ | ✗ | ✓ | ✓ |
| SCIM | ✗ | ✗ | ✗ | ✓ |
| [Compliance API](https://platform.claude.com/docs/en/api/compliance) | ✗ | ✗ | ✗ | ✓ |
| [Zero Data Retention](/docs/zh-CN/zero-data-retention) | ✗ | ✗ | ✗ | ✓ <sup><a href="#fn7">7</a></sup> |

<span id="fn6" style={{display: 'block', position: 'relative', top: '-120px'}} /><sup>6</sup> 在 Enterprise 上，需要高级座位或 Chat + Claude Code 座位。请参阅[网络上的 Claude Code](/docs/zh-CN/claude-code-on-the-web)。<br />
<span id="fn7" style={{display: 'block', position: 'relative', top: '-120px'}} /><sup>7</sup> 不包含在标准 Enterprise 计划中。需要 Anthropic 为合格账户单独启用。请参阅 [Zero Data Retention](/docs/zh-CN/zero-data-retention)。

有关定价和完整的计划比较，请参阅 [Team 计划](https://support.claude.com/en/articles/9266767-what-is-the-team-plan)和 [Enterprise 计划](https://support.claude.com/en/articles/9797531-what-is-the-enterprise-plan)。

<h2 id="model-availability">
  模型可用性
</h2>

有关每个提供商和地区可用的 Claude 模型和上下文窗口大小，请参阅[模型配置](/docs/zh-CN/model-config)和[模型概述](https://platform.claude.com/docs/en/about-claude/models/overview)。Vision、PDF 输入和扩展思考是模型功能而不是 Claude Code 功能，在提供该模型的每个提供商上都有效。[Prompt caching](/docs/zh-CN/prompt-caching) 在大多数提供商上的工作方式相同；在 Amazon Bedrock 上，支持因模型而异。

<h2 id="related-resources">
  相关资源
</h2>

* [企业部署概述](/docs/zh-CN/third-party-integrations)：比较提供商之间的身份验证、计费和地区
* 提供商设置指南：[Amazon Bedrock](/docs/zh-CN/amazon-bedrock)、[Claude Platform on AWS](/docs/zh-CN/claude-platform-on-aws)、[Google Cloud's Agent Platform](/docs/zh-CN/google-vertex-ai)、[Microsoft Foundry](/docs/zh-CN/microsoft-foundry)
* [平台和集成](/docs/zh-CN/platforms)：Claude Code 运行的地方，包括 CLI、Desktop、IDE 扩展、网络、移动和 CI/CD
