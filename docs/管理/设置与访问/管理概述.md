> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 为您的组织设置 Claude Code

> 针对部署 Claude Code 的管理员的决策地图，涵盖 API 提供商、托管设置、策略执行、使用情况监控和数据处理。

Claude Code 通过托管设置强制执行组织策略，这些设置优先于本地开发人员配置。您可以从 Claude 管理控制台、移动设备管理 (MDM) 系统或磁盘上的文件传递这些设置。这些设置控制 Claude 可以访问的工具、命令、服务器和网络目标。

本页按顺序介绍部署决策。每一行都链接到下面的部分和该区域的参考页面。

<Note>
  SSO、SCIM 预配和座位分配在 Claude 账户级别配置。有关这些步骤，请参阅 [Claude 企业管理员指南](https://claude.com/resources/tutorials/claude-enterprise-administrator-guide) 和 [座位分配](https://support.claude.com/en/articles/11845131-use-claude-code-with-your-team-or-enterprise-plan)。
</Note>

| 决策 | 您的选择 | 参考 |
| :- | :- | :- |
| [选择您的 API 提供商](#choose-your-api-provider) | Claude Code 的身份验证位置和计费方式 | [Authentication](/docs/zh-CN/authentication)、[Amazon Bedrock](/docs/zh-CN/amazon-bedrock)、[Google Cloud's Agent Platform](/docs/zh-CN/google-vertex-ai)、[Microsoft Foundry](/docs/zh-CN/microsoft-foundry) |
| [决定设置如何到达设备](#decide-how-settings-reach-devices) | 托管策略如何到达开发人员机器 | [Server-managed settings](/docs/zh-CN/server-managed-settings)、[Delivery mechanisms](/docs/zh-CN/managed-settings#delivery-mechanisms) |
| [决定要强制执行的内容](#decide-what-to-enforce) | 允许哪些工具、命令和集成 | [Permissions](/docs/zh-CN/permissions)、[Sandboxing](/docs/zh-CN/sandboxing) |
| [设置使用情况可见性](#set-up-usage-visibility) | 如何跟踪支出和采用情况 | [Analytics](/docs/zh-CN/analytics)、[Monitoring](/docs/zh-CN/monitoring-usage)、[Costs](/docs/zh-CN/costs) |
| [审查数据处理](#review-data-handling) | 数据保留和合规性态势 | [Data usage](/docs/zh-CN/data-usage)、[Security](/docs/zh-CN/security) |

<h2 id="choose-your-api-provider">
  选择您的 API 提供商
</h2>

Claude Code 通过多个 API 提供商之一连接到 Claude。您的选择会影响计费、身份验证、您继承的合规性态势，以及您的开发人员可以使用的 Claude Code 功能。

| 提供商 | 何时选择 |
| :- | :- |
| Claude for Teams / Enterprise | 您希望 Claude Code 和 claude.ai 在一个按座位订阅下，无需运行基础设施。这是默认建议。 |
| Claude Console | 您是 API 优先或希望按使用量付费 |
| Amazon Bedrock | 您希望继承现有的 AWS 合规控制和计费 |
| Google Cloud's Agent Platform | 您希望继承现有的 GCP 合规控制和计费 |
| Microsoft Foundry | 您希望继承现有的 Azure 合规控制和计费 |

某些 Claude Code 功能需要 claude.ai 账户。[Cloud sessions](/docs/zh-CN/claude-code-on-the-web)、[Routines](/docs/zh-CN/routines)、[Code Review](/docs/zh-CN/code-review)、[Remote Control](/docs/zh-CN/remote-control) 和 [Chrome extension](/docs/zh-CN/chrome) 不能仅通过 Console API 密钥或云提供商凭证使用。如果您通过 Amazon Bedrock、Google Cloud's Agent Platform 或 Microsoft Foundry 部署，请计划开发人员是否还需要 Claude for Teams 或 Enterprise 座位。每个功能页面都列出了其计划要求。

有关涵盖身份验证、区域和功能奇偶性的完整提供商比较，请参阅 [enterprise deployment overview](/docs/zh-CN/third-party-integrations)。每个提供商的身份验证设置在 [Authentication](/docs/zh-CN/authentication) 中。

[Network configuration](/docs/zh-CN/network-config) 中的代理和防火墙要求适用于所有提供商。如果您想要在多个提供商前面有单个端点或集中式请求日志记录，请参阅 [LLM gateway](/docs/zh-CN/llm-gateway)。

<h2 id="decide-how-settings-reach-devices">
  决定设置如何到达设备
</h2>

托管设置定义组织策略。Claude Code 按优先级顺序检查下表中的四个来源。[Claude Code 如何合并托管来源](/docs/zh-CN/managed-settings#precedence-within-the-managed-tier)说明其中哪些适用、策略助手更改什么，以及如何组合每个来源。该表是决策地图。

| 机制 | 传递 | 优先级 | 平台 |
| :- | :- | :- | :- |
| Server-managed | claude.ai 管理控制台，或用于网关登录的自托管 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway) | 最高 | 全部 |
| plist / registry policy | macOS: `com.anthropic.claudecode` plist<br />Windows: `HKLM\SOFTWARE\Policies\ClaudeCode` | 高 | macOS、Windows |
| File-based managed | macOS: `/Library/Application Support/ClaudeCode/managed-settings.json`<br />Linux 和 WSL: `/etc/claude-code/managed-settings.json`<br />Windows: `C:\Program Files\ClaudeCode\managed-settings.json` | 中 | 全部 |
| Windows user registry | `HKCU\SOFTWARE\Policies\ClaudeCode` | 最低 | 仅 Windows |

Claude Code 在启动时获取 server-managed 设置，并在会话期间每小时刷新一次，无需部署端点基础设施。通过 claude.ai 管理控制台传递需要 Claude for Teams 或 Enterprise 计划。在 Amazon Bedrock、Google Cloud 的 Agent Platform 或 Microsoft Foundry 上的部署可以通过运行 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway) 获得相同的远程传递，或改用基于文件或操作系统级别的机制之一。

如果您的组织混合使用提供商，请为 claude.ai 用户配置 [server-managed settings](/docs/zh-CN/server-managed-settings) 加上 [file-based 或 plist/registry 回退](/docs/zh-CN/managed-settings#delivery-mechanisms)，以便其他用户仍然接收托管策略。

plist 和 HKLM 注册表位置适用于任何提供商，并且由于需要管理员权限才能写入，因此可以抵抗篡改。Windows 用户注册表中的 HKCU 可以在没有提升权限的情况下写入，因此将其视为便利默认值而不是执行通道。

默认情况下，WSL 仅读取 `/etc/claude-code` 处的 Linux 文件路径。要将您的 Windows 注册表和 `C:\Program Files\ClaudeCode` 策略扩展到同一台机器上的 WSL，请在这些仅限管理员的 Windows 来源之一中设置 [`wslInheritsWindowsSettings: true`](/docs/zh-CN/settings-reference#wslinheritswindowssettings)。

无论您选择哪种机制，托管值都优先于用户和项目设置，除了一些安全敏感的[例外](/docs/zh-CN/settings#exceptions-to-managed-settings-precedence)。数组设置（如 `permissions.allow` 和 `permissions.deny`）合并来自所有源的条目，因此开发人员可以扩展托管列表但不能从中删除。对于 `fallbackModel`、`availableModels` 和 [`modelPicker`](/docs/zh-CN/settings-reference#modelpicker)，托管值替换较低层而不是合并。

<h3 id="wsl-sessions-in-claude-code-desktop">
  WSL 会话在 Claude Code Desktop 中
</h3>

在 Windows 上，[Claude Code Desktop 可以在 WSL 2 发行版内运行 Code 会话](/docs/zh-CN/desktop-wsl)。会话的 Claude Code 进程在发行版内运行，因此它通过上述 WSL 发现路径解析托管设置：除非部署了 `wslInheritsWindowsSettings: true`，否则仅限 Windows 的来源无法到达它。

Claude Desktop 在检测到设备为组织管理的设备上默认关闭 WSL 会话，例如当 `C:\Program Files\ClaudeCode\managed-settings.json` 存在时。要打开它们，请部署 Windows 注册表策略，这需要 Claude Desktop v1.19367.0 或更高版本：

* 在 `HKLM\SOFTWARE\Policies\Claude` 下创建一个名为 `disableWslSessions` 的值，并将其设置为 `REG_SZ` 字符串 `false` 或 `REG_DWORD` `0`。此值位于 Claude Desktop 策略键下，与携带托管设置的 `ClaudeCode` 键分开。在 HKLM 下部署该值，这需要管理员权限才能写入。HKCU 下的值不会启用 WSL 会话。
* 如果部署了 `C:\Program Files\ClaudeCode\managed-settings.json`，请保留它。一旦 HKLM 下的 `disableWslSessions` 为 `false`，Desktop 即使该文件存在也允许 WSL 会话。

Desktop 在每次 WSL 会话启动时读取策略，因此在部署后无需重启应用。

如果设备仍然拒绝 WSL 会话，请在该设备上的 Claude Desktop 中打开 **Help > Troubleshooting > Show Logs in File Explorer**，这会将其日志文件夹的副本保存到 Downloads。在该副本中搜索 `main.log` 中的 `[wslPolicyGate] denying WSL session`。拒绝的原因在括号中，例如 `(cli-file-present)`。

启用 WSL 会话后，将您的托管设置扩展到它们：

* 通过 HKLM 注册表或 `C:\Program Files\ClaudeCode` 文件部署 `wslInheritsWindowsSettings: true`，以便 WSL 会话继承与主机会话相同的策略。
* 通过在 WSL 会话内运行 `/status` 进行验证，并读取 `Setting sources` 行。要解释它列出的内容，请参阅[在 /status 中读取来源](/docs/zh-CN/managed-settings#read-the-source-in-/status)。

WSL 2 实用程序 VM 内的进程对 Windows 端端点检测传感器不可见。要观察发行版内的进程和文件活动，请查看您的端点检测供应商的 WSL 指南，了解您可以在发行版内运行的 Linux 传感器及其需要的排除项。Claude Code 的 [OpenTelemetry 工具执行遥测](/docs/zh-CN/monitoring-usage) 对 WSL 和本机会话的发出方式相同。

<h2 id="decide-what-to-enforce">
  决定要强制执行的内容
</h2>

托管设置可以锁定工具、沙箱执行、限制 MCP 服务器和插件源，以及控制哪些 hooks 运行。每一行都是一个控制表面，具有驱动它的设置键。

| 控制 | 它的作用 | 关键设置 |
| :- | :- | :- |
| [Permission rules](/docs/zh-CN/permissions) | 允许、询问或拒绝特定工具和命令 | `permissions.allow`、`permissions.deny` |
| [Permission lockdown](/docs/zh-CN/permissions#managed-only-settings) | 使托管设置成为[权限规则的唯一设置源](/docs/zh-CN/settings-reference#allowmanagedpermissionrulesonly)。禁用 `--dangerously-skip-permissions` | `allowManagedPermissionRulesOnly`、`permissions.disableBypassPermissionsMode` |
| [Starting permission mode](/docs/zh-CN/permission-modes#which-mode-a-session-starts-in) | 选择开发人员终端会话启动时的权限模式，而不是内置的启动权限模式，或删除自动模式。[Switch permission modes](/docs/zh-CN/permission-modes#switch-permission-modes) 列出 VS Code 扩展何时读取您设置的 `defaultMode` | `permissions.defaultMode`、`permissions.disableAutoMode` |
| [Sandboxing](/docs/zh-CN/sandboxing) | 具有域允许列表的操作系统级文件系统和网络隔离 | `sandbox.enabled`、`sandbox.network.allowedDomains` |
| [Managed policy CLAUDE.md](/docs/zh-CN/memory#deploy-organization-wide-claude-md) | 在每个会话中加载的组织范围指令，无法排除 | 托管策略路径处的文件 |
| [MCP server control](/docs/zh-CN/managed-mcp) | 限制用户可以添加或连接的 MCP 服务器、部署固定集合，或为每个用户提供远程服务器以及他们自己的服务器 | `allowedMcpServers`、`deniedMcpServers`、`allowManagedMcpServersOnly`、`managedMcpServers` 或已部署的 `managed-mcp.json` 文件 |
| [Plugin marketplace control](/docs/zh-CN/plugins/org#restrict-what-users-can-install) | 限制用户可以添加和安装的市场来源，拒绝为单次运行侧加载插件、agents 和 MCP 服务器的 CLI 标志，阻止[`command` 插件源](/docs/zh-CN/plugins/marketplace-reference#command-plugin-source)，并允许列出哪些市场的插件可以被建议 | `strictKnownMarketplaces`、`blockedMarketplaces`、`disableSideloadFlags`、`disableCommandPluginSources`、`pluginSuggestionMarketplaces` |
| [Customization lockdown](/docs/zh-CN/settings-reference#strictpluginonlycustomization) | 阻止 skills、agents、hooks 和 MCP 服务器来自用户和项目源，使它们只能来自插件或托管设置。锁定 skills 也会停止[您的开发人员在 claude.ai 上启用的 skills](/docs/zh-CN/skills#where-synced-skills-load) 的同步 | `strictPluginOnlyCustomization` |
| [Disable claude.ai sync](/docs/zh-CN/settings-reference#syncclaudeaiskills) | 停止 Claude Code 加载[您的开发人员在 claude.ai 上启用的 skills](/docs/zh-CN/skills#how-synced-skills-behave) 和[插件](/docs/zh-CN/plugins/loading#synced-plugins)。如果您为组织关闭 claude.ai 上的 Skills，Claude Code 会停止同步两者，在 v2.1.273 或更高版本上，它也会删除已同步的那些。要在不关闭 Skills 的情况下停止其中任一个，在托管设置中将其键设置为 `false` | `syncClaudeAiSkills`、`syncClaudeAiPlugins` |
| [Hook restrictions](/docs/zh-CN/settings-reference#allowmanagedhooksonly) | 限制哪些 hooks 运行并限制 HTTP hook URL；请参阅[`allowManagedHooksOnly` 下运行的内容](/docs/zh-CN/settings-reference#what-runs-under-allowmanagedhooksonly)了解完整的效果列表 | `allowManagedHooksOnly`、`allowedHttpHookUrls` |
| [Login enforcement](/docs/zh-CN/settings-reference#forceloginmethod) | 限制登录到特定方法或 Anthropic 组织。方法限制适用于 VS Code 扩展、Agent SDK、`claude setup-token` 和 `/install-github-app`，以及终端的交互式登录屏幕（通过 `/login` 或首次运行入门到达），预先选择方法但不强制执行；Claude Code 在终端、VS Code 扩展和 Agent SDK 中验证 claude.ai 账户登录的组织，不检查 Claude Console 登录或[网关](/docs/zh-CN/claude-apps-gateway)登录。在 v2.1.212 之前，仅终端登录应用任一密钥。设置后，由 `ANTHROPIC_API_KEY`、`ANTHROPIC_AUTH_TOKEN` 或 `apiKeyHelper` 进行身份验证的会话在启动时被阻止；云提供商会话不受影响，除非这些凭证之一或由较早的 Claude Console 登录保存的 API 密钥也存在 | `forceLoginMethod`、`forceLoginOrgUUID` |
| [Provider restrictions](/docs/zh-CN/settings-reference#allowedproviders) | 限制机器可以使用的 API 提供商。不在列表中的提供商上的会话在启动时、登录时以及下次联系 API 时被拒绝。需要 Claude Code v2.1.285 或更高版本 | `allowedProviders` |
| [Disable agent view](/docs/zh-CN/agent-view#how-background-sessions-are-hosted) | 关闭 `claude agents`、`--bg`、`/background` 和按需监督程序 | `disableAgentView` |
| [Configure the corporate launcher](/docs/zh-CN/corporate-launcher) | 使用必需的企业启动器作为[后台代理监督程序](/docs/zh-CN/agent-view#how-background-sessions-are-hosted)、其工作程序和[其他涵盖的后台进程](/docs/zh-CN/corporate-launcher#what-the-launcher-covers)的前缀，而不是关闭代理视图 | `processWrapper` |
| [Model restrictions](/docs/zh-CN/model-config#restrict-model-selection) | `availableModels` 筛选模型选择器中显示的模型。添加 `enforceAvailableModels` 也会限制自动选择的默认模型。请参阅[表面覆盖](/docs/zh-CN/model-config#surface-coverage)了解此设置如何到达 CLI、web 和 IDE | `availableModels`、`enforceAvailableModels` |
| [Effort cap](/docs/zh-CN/settings-reference#maxeffortlevel) | 为每个模型或每个提供商上的每个模型限制[工作量级别](/docs/zh-CN/model-config#adjust-effort-level) | `maxEffortLevel` |
| [Version floor](/docs/zh-CN/settings-reference#minimumversion) | 防止自动更新安装低于组织范围最小值的版本 | `minimumVersion` |
| [Required version range](/docs/zh-CN/settings-reference#requiredminimumversion) | 当运行版本超出组织批准的范围时拒绝启动。比 `minimumVersion` 更强大，后者仅阻止降级 | `requiredMinimumVersion`、`requiredMaximumVersion` |
| [Telemetry opt-out](/docs/zh-CN/data-usage#telemetry-services) | 在每台设备上关闭 Anthropic 绑定的使用指标、错误报告和调查 | `env` 设置 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 为 `1`；链接的部分列出了按类别的变量 |

如果您的成员通过 claude.ai 或 Anthropic API 登录，并且您在 Claude Enterprise 计划上，您还可以从组织的管理设置中管理模型，而无需部署任何内容：

* [Organization model restrictions](/docs/zh-CN/model-config#organization-model-restrictions)：禁用单个模型。在服务器端强制执行。
* [Organization default model](/docs/zh-CN/model-config#organization-default-model)：设置新会话启动时使用的模型。成员仍可切换模型。要在启动时将其恢复为您的默认模型，请启用该部分所述的覆盖设置。要限制成员可选择的模型，请使用[组织模型限制](/docs/zh-CN/model-config#organization-model-restrictions)。
* [Organization effort limits](/docs/zh-CN/model-config#organization-effort-limits)：按角色限制工作量级别。在服务器端强制执行。

这些控制都不会到达 Amazon Bedrock、Google Cloud 的 Agent Platform、Microsoft Foundry 或 [Claude Platform on AWS](/docs/zh-CN/claude-platform-on-aws) 上的会话。在这些提供商上，使用托管设置代替：`availableModels` 用于限制，`model` 用于默认值，[`maxEffortLevel`](/docs/zh-CN/settings-reference#maxeffortlevel) 用于工作量限制。

[Cloud sessions](/docs/zh-CN/claude-code-on-the-web) 在 claude.ai 上有其自己的管理入口：

* **Cloud environments 页面**：所有者创建[组织共享环境](/docs/zh-CN/cloud-environments#organization-shared-environments)，设置成员云端会话的[网络访问级别](/docs/zh-CN/cloud-environments#network-access)、环境变量和设置脚本。
* **默认环境**：所有者在 [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) 单独选择组织的默认环境。
* **Git providers 页面**：请参阅[已关联的 GitHub 账户](#connected-github-accounts)，了解关联到您组织的 GitHub 账户。

权限规则和沙箱覆盖不同的层。拒绝 WebFetch 会阻止 Claude 的 fetch 工具，但如果允许 Bash，`curl` 和 `wget` 仍然可以到达任何 URL。沙箱通过在操作系统级别强制执行的网络域允许列表来弥补这一差距。

有关这些控制防御的威胁模型，请参阅[安全性](/docs/zh-CN/security)。

<h3 id="connected-github-accounts">
  已关联的 GitHub 账户
</h3>

在 Team 和 Enterprise 计划中，[**Organization settings > Git providers**](https://claude.ai/admin-settings/source-control) 的 GitHub 部分列出了通过 [Claude GitHub App](https://github.com/apps/claude) 关联到您的 Claude 组织的 GitHub 组织和个人账户。Claude Code、[Claude Tag](https://claude.com/docs/claude-tag/admins/configure-github) 和 Claude Security 共享此列表。打开该页面需要在您的 Claude 组织中拥有管理员角色。

管理员或成员都可以关联账户：

* **管理员连接**：管理员在该部分点击 **Connect**（或在已连接账户后点击 **Add organization**），并在某个 GitHub 组织上安装 Claude GitHub App。以这种方式关联组织，需要一个既是该 GitHub 组织所有者、又是您 Claude 组织管理员的人来操作。
* **成员连接**：当成员将其 GitHub 账户连接到 Claude 时（例如在[设置云端会话](/docs/zh-CN/web-quickstart#connect-github)时），Claude 会关联该成员拥有且已安装 Claude GitHub App 的 GitHub 账户。这可能包括其个人账户以及其拥有的 GitHub 组织。

标记为 **Not linked** 的行来自您自己的 GitHub 登录。它是您在 GitHub 上可以看到且已安装 Claude GitHub App 的账户。

要将某个账户与您的 Claude 组织取消关联，请打开该行的菜单并选择 **Unlink from this workspace**。取消关联后，Claude GitHub App 仍安装在 GitHub 上，下次该账户的某个所有者将 GitHub 连接到 Claude 时，该账户会再次被关联。要防止其再次被关联，请在 GitHub 上从该账户卸载 Claude GitHub App。

在 Enterprise 计划中，用于关联和取消关联的 [Compliance API](https://platform.claude.com/docs/en/api/compliance/activities/list) 活动类型分别为 `github_app_installation_linked` 和 `github_app_installation_unlinked`。

<h2 id="set-up-usage-visibility">
  设置使用情况可见性
</h2>

根据您需要报告的内容选择监控。仪表板、API 和支出控制在 Claude for Teams 或 Enterprise 计划与 Claude Console 组织之间有所不同，因此在围绕某项功能规划报告之前，请检查"可用性"列。

| 功能 | 您获得的内容 | 可用性 | 从何处开始 |
| :- | :- | :- | :- |
| Usage monitoring | 会话、工具和令牌的 OpenTelemetry 导出 | 所有提供商 | [Monitoring usage](/docs/zh-CN/monitoring-usage) |
| Analytics dashboard | Teams / Enterprise 上具有排行榜的采用和贡献指标；Console 上的每用户使用情况和支出指标 | Teams / Enterprise 在 [claude.ai/analytics](https://claude.ai/analytics/claude-code)，Console 在 [platform.claude.com/claude-code](https://platform.claude.com/claude-code) | [Analytics](/docs/zh-CN/analytics) |
| Programmatic reporting | 通过 API 的每用户使用情况和成本数据 | Enterprise 的 [Enterprise Analytics API](https://platform.claude.com/docs/en/api/admin/analytics)，Console 的 [Claude Code Analytics API](https://platform.claude.com/docs/en/build-with-claude/claude-code-analytics-api) | [Costs](/docs/zh-CN/costs#manage-costs-for-your-organization) |
| Spend controls | 支出限制和速率限制 | Teams / Enterprise 的组织设置，Console 的工作区限制；在第三方云上，云预算控制或具有每用户[支出限制](/docs/zh-CN/claude-apps-gateway-spend-limits)的 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway) | [Costs](/docs/zh-CN/costs#manage-costs-for-your-organization) |

在 Teams 和 Enterprise 上，每用户使用情况和支出数字来自您组织的分析设置中的[支出报告](https://support.claude.com/en/articles/12883420-view-usage-analytics-for-team-and-enterprise-plans)，而不是分析仪表板。云提供商通过 AWS Cost Explorer、GCP Billing 或 Azure Cost Management 公开支出。有关跨 Claude chat、Claude Code 和 Cowork 规划企业预算的信息，请参阅 [Claude Enterprise consumption guide](https://support.claude.com/en/articles/14782391-claude-enterprise-consumption-guide)。

<h2 id="review-data-handling">
  审查数据处理
</h2>

在 Team、Enterprise、Claude API 和云提供商计划上，Anthropic 不会在您的代码或提示上训练模型。您的 API 提供商决定保留和合规性态势。

| 主题 | 需要了解的内容 | 从何处开始 |
| :- | :- | :- |
| Data usage policy | Anthropic 收集的内容、保留多长时间、永远不会用于训练的内容 | [Data usage](/docs/zh-CN/data-usage) |
| Zero Data Retention (ZDR) | 请求完成后不存储任何内容。适用于 Claude for Enterprise 上符合条件的账户 | [Zero data retention](/docs/zh-CN/zero-data-retention) |
| HIPAA configuration | 适用于已启用 HIPAA 的 Claude for Enterprise 组织。部分 Claude Code（本地模式）功能会被关闭，其他功能默认关闭 | [Set up Claude Code (local mode) for a HIPAA-ready organization](/docs/zh-CN/hipaa-setup) |
| Security architecture | 网络模型、加密、身份验证、审计跟踪 | [Security](/docs/zh-CN/security) |

如果您需要请求级别的审计日志或按数据敏感性路由流量，我们建议您在开发人员和您的提供商之间放置网关：自托管的 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway) 记录带有 IdP 身份的每个请求审计日志，或者您也可以使用另一个 [LLM gateway](/docs/zh-CN/llm-gateway)。通过网关的会话不符合 HIPAA 配置的条件。[Check how developers sign in and connect](/docs/zh-CN/hipaa-setup#check-how-developers-sign-in-and-connect) 列出了哪些登录和连接方式符合条件。有关监管要求和认证，请参阅 [Legal and compliance](/docs/zh-CN/legal-and-compliance)。

<h2 id="verify-and-onboard">
  验证和入职
</h2>

配置托管设置后，让开发人员在 Claude Code 中运行 `/status`。在 **Status** 选项卡上，`Setting sources` 行显示 `Enterprise managed settings` 后跟括号中的源；[验证执行](/docs/zh-CN/managed-settings#verify-enforcement) 列出了标签。

分享这些资源以帮助开发人员入门：

* [快速入门](/docs/zh-CN/quickstart)：从安装到使用项目的首次会话演练
* [常见工作流](/docs/zh-CN/common-workflows)：代码审查、重构和调试等日常任务的模式
* [Claude Code 101](https://academy.claude.com/courses/claude-code-101) 和 [Claude Code in Action](https://academy.claude.com/courses/claude-code-in-action)：[Claude Academy](https://academy.claude.com/) 上的免费自定进度课程

对于登录问题，请将开发人员指向 [身份验证故障排除](/docs/zh-CN/troubleshoot-install#login-and-authentication)。最常见的修复是：

* 运行 `/logout` 然后 `/login` 以切换账户
* 如果缺少企业身份验证选项，运行 `claude update`
* 更新后重启终端

如果开发人员看到"您还没有被添加到您的组织"，他们的座位不包括 Claude Code 访问权限，需要在管理控制台中更新。

<h2 id="next-steps">
  后续步骤
</h2>

选择提供商和传递机制后，继续进行详细配置：

* [Server-managed settings](/docs/zh-CN/server-managed-settings)：从 Claude 管理控制台传递托管策略
* [All settings](/docs/zh-CN/settings-reference)：每个设置键、文件位置和示例
* [Which value Claude Code uses](/docs/zh-CN/settings#which-value-claude-code-uses)：跨托管、项目、本地和用户设置的优先级规则
* [Monorepos and large repos](/docs/zh-CN/large-codebases)：为部署到 monorepo 的组织提供的按目录配置模式
* [Amazon Bedrock](/docs/zh-CN/amazon-bedrock)、[Google Cloud's Agent Platform](/docs/zh-CN/google-vertex-ai)、[Microsoft Foundry](/docs/zh-CN/microsoft-foundry)：提供商特定部署
* [Claude Enterprise Administrator Guide](https://claude.com/resources/tutorials/claude-enterprise-administrator-guide)：SSO、SCIM、座位管理和推出手册
