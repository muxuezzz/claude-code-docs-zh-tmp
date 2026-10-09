> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 配置服务器管理的设置

> 通过服务器交付的设置为您的组织集中配置 Claude Code，无需设备管理基础设施。

服务器管理的设置允许组织所有者通过 claude.ai 控制台中的 [**Organization settings > Claude Code > Managed settings**](https://claude.ai/admin-settings/claude-code) 集中配置 Claude Code。Claude Code 客户端在用户使用符合条件的凭据在支持服务器管理交付的平台上进行身份验证时自动获取这些设置。请参阅[平台可用性](#platform-availability)了解符合条件的凭据和平台。

<Note>
  服务器管理的设置可供 [Claude for Teams](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=server_settings_teams#team-&-enterprise) 和 [Claude for Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=server_settings_enterprise) 客户使用。
</Note>

<h2 id="requirements">
  要求
</h2>

要使用服务器管理的设置，您需要：

* Claude for Teams 或 Claude for Enterprise 计划
* 您的 Claude 组织中的所有者或主要所有者角色，以查看和编辑配置
* 对 `api.anthropic.com` 的网络访问

<h2 id="choose-between-server-managed-and-endpoint-managed-settings">
  在服务器管理和端点管理的设置之间选择
</h2>

Claude Code 支持两种集中配置方法。服务器管理的设置从 Anthropic 的服务器传递配置。[端点管理的设置](/docs/zh-CN/managed-settings#delivery-mechanisms)通过本机操作系统策略（macOS 托管首选项、Windows 注册表）或托管设置文件直接部署到设备。

| 方法 | 最适合 | 安全模型 |
| :- | :- | :- |
| **服务器管理的设置** | 没有 MDM 的组织，或非托管设备上的用户 | Claude Code 在启动时从 Anthropic 的服务器获取的设置，并在会话期间每小时刷新一次 |
| **[端点管理的设置](/docs/zh-CN/managed-settings#delivery-mechanisms)** | 具有 MDM 或端点管理的组织 | 通过 MDM 配置文件、注册表策略或托管设置文件部署到设备的设置 |

如果您的设备已在 MDM 或端点管理解决方案中注册，端点管理的设置提供更强的安全保证，因为设置文件可以在操作系统级别受到保护，防止用户修改。端点管理的设置不会到达 Anthropic 托管环境中的[云会话](/docs/zh-CN/model-config#surface-coverage)，因此在网络上使用 Claude Code 的组织也应该配置服务器管理的设置。[自托管环境](/docs/zh-CN/self-hosted-environments)中的会话也会读取运行器镜像中的托管设置文件。下面的[设置优先级](#settings-precedence)说明了该文件何时适用。

<h2 id="configure-server-managed-settings">
  配置服务器管理的设置
</h2>

<Steps>
  <Step title="打开管理控制台">
    在 claude.ai 控制台中，转到 [**Organization settings > Claude Code > Managed settings**](https://claude.ai/admin-settings/claude-code)。

    在 Team 或 Enterprise 组织中，如果页面显示您没有访问权限，请让 [Owner 或 Primary Owner](#access-control) 进行更改。
  </Step>

  <Step title="定义您的设置">
    将您的配置添加为 JSON。支持 [`settings.json` 中可用的所有设置](/docs/zh-CN/settings-reference#all-settings)，除了限制于操作系统级别策略传递的设置外；有关该简短列表，请参阅[当前限制](#current-limitations)。这包括 [hooks](/docs/zh-CN/hooks)、[环境变量](/docs/zh-CN/env-vars) 和[仅限托管的设置](/docs/zh-CN/managed-settings#managed-only-settings)，如 `allowManagedPermissionRulesOnly`。

    此示例强制执行权限拒绝列表，防止用户绕过权限，并将权限规则限制为在托管设置中定义的规则。`Bash(curl *)` 规则匹配 `curl` [如 Claude 编写的那样](/docs/zh-CN/permissions#bash-rule-limits)，而不是 `/usr/bin/curl` 或 `sh -c 'curl …'`；对于不依赖于命令文本的网络强制，添加一个[带有 `allowManagedDomainsOnly` 的 `sandbox` 块](/docs/zh-CN/sandboxing#configure-the-sandbox-for-your-organization)。

    ```json theme={null}
    {
      "permissions": {
        "deny": [
          "Bash(curl *)",
          "Read(./.env)",
          "Read(./.env.*)",
          "Read(./secrets/**)"
        ],
        "disableBypassPermissionsMode": "disable"
      },
      "allowManagedPermissionRulesOnly": true
    }
    ```

    Hooks 使用与 `settings.json` 中相同的格式。

    此示例在整个组织中每次文件编辑后运行审计脚本：

    ```json theme={null}
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Edit|Write",
            "hooks": [
              { "type": "command", "command": "/usr/local/bin/audit-edit.sh" }
            ]
          }
        ]
      }
    }
    ```

    由于 hooks 执行 shell 命令，交互式会话中的用户在 Claude Code 应用它们之前会看到[安全批准对话框](#security-approval-dialogs)。

    要配置[自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)分类器，使其了解您的组织信任的存储库、存储桶和域，以相同的方式传递 `autoMode` 块；有关 `autoMode` 条目如何影响分类器阻止的内容以及关于 `environment`、`allow`、`soft_deny` 和 `hard_deny` 字段的重要警告，请参阅[配置自动模式](/docs/zh-CN/auto-mode-config)。
  </Step>

  <Step title="保存并部署">
    保存您的更改。Claude Code 客户端在下次启动或每小时轮询周期时接收更新的设置。

    编辑器会根据已发布的 Claude Code 设置 JSON schema 检查您的 JSON。如果在可解析的 JSON 中发现问题，它会显示警告并更改保存按钮的标签。当已保存设置时，标签为 **Update with errors**；当尚未保存任何设置时，标签为 **Add with errors**。该按钮仍然会保存，因为 schema 警告不会阻止保存。

    该 schema [可能落后于最新版本](/docs/zh-CN/settings#edit-a-settings-file)，因此编辑器可能会标记[设置参考](/docs/zh-CN/settings-reference#all-settings)中已记录的键或值。Claude Code 会接收您保存的键和值，并在加载它们时运行[自己的验证](#invalid-entries-in-delivered-settings)。
  </Step>
</Steps>

<h3 id="verify-settings-delivery">
  验证设置传递
</h3>

要确认设置正在被应用，请要求用户重新启动 Claude Code。如果配置包含触发[安全批准对话框](#security-approval-dialogs)的设置，用户会在 Claude Code 下次获取它们时看到描述托管设置的提示：在下次启动时，或在运行的交互式会话中的一小时内。您还可以通过让用户运行 `/permissions` 来验证托管权限规则是否处于活动状态，以查看其有效的权限规则。

要检查特定机器上的获取结果，请让用户运行 `claude doctor` 并读取 `Managed settings (remote)` 行。需要 Claude Code v2.1.248 或更高版本。该行报告以下四种结果之一：

* 传递的设置已加载
* 您的组织没有配置服务器管理的设置
* 获取失败，包括原因以及缓存的策略是否仍然适用
* Claude Code 跳过了获取，包括原因。有关跳过它的提供商和配置，请参阅[平台可用性](#platform-availability)

在获取仍在进行中时，该行会报告这一点。

在运行的会话中，`/status` 在获取失败后显示相同的行，对于某些跳过获取的原因，例如第三方提供商变量或用户 shell 中导出的自定义 `ANTHROPIC_BASE_URL`。

<h3 id="access-control">
  访问控制
</h3>

以下角色可以管理服务器管理的设置：

* **Primary Owner**
* **Owner**

限制对受信任人员的访问，因为设置更改适用于组织中的所有用户。

<h3 id="managed-only-settings">
  仅限托管的设置
</h3>

大多数[设置键](/docs/zh-CN/settings-reference#all-settings)可在任何范围内工作。少数几个键仅从托管设置中读取，当放置在用户或项目设置文件中时无效。有关权限和插件控制，请参阅[仅限托管的设置](/docs/zh-CN/managed-settings#managed-only-settings)，或读取[所有设置](/docs/zh-CN/settings-reference#all-settings)索引的 Scope 列以获取完整集合。

<h3 id="current-limitations">
  当前限制
</h3>

服务器管理的设置有以下限制：

* 设置统一应用于组织中的所有用户。尚不支持按组配置。
* 您无法通过服务器管理的设置分发 [`managed-mcp.json`](/docs/zh-CN/managed-mcp) 文件。改为在那里传递 `allowedMcpServers` 和 `deniedMcpServers` 策略键。在 Claude Code v2.1.259 或更高版本上，您还可以通过 [`managedMcpServers`](/docs/zh-CN/managed-mcp#provide-servers-through-managed-settings) 提供远程服务器，它仅接受 `http` 和 `sse` 服务器，并且不会像文件那样获得独占控制。

  Claude Code 在其[系统路径](/docs/zh-CN/managed-mcp#exclusive-control-with-managed-mcp-json)处部署的 `managed-mcp.json` 与托管设置层分开读取，因此当服务器管理的设置生效时，该文件仍然适用。
* 限制于操作系统级别策略源的设置，如 `policyHelper` 和 `wslInheritsWindowsSettings`，不被遵守。改为通过 MDM 或系统 `managed-settings.json` 文件部署它们。在[托管层内的优先级](/docs/zh-CN/managed-settings#precedence-within-the-managed-tier)下选择的源是该源时，以这种方式部署的 `policyHelper` 仅运行。

<h2 id="settings-delivery">
  设置传递
</h2>

<h3 id="settings-precedence">
  设置优先级
</h3>

服务器管理的设置和[端点管理的设置](/docs/zh-CN/managed-settings#delivery-mechanisms)都占据 Claude Code [设置层次结构](/docs/zh-CN/settings#settings-precedence)中的最高层。您在此处设置的键优先于用户自己的设置文件中或 `--settings` 值中的同一键，[托管设置优先级的例外](/docs/zh-CN/settings#exceptions-to-managed-settings-precedence)除外。

在托管层内，Claude Code 默认使用首先传递至少一个策略键的源，首先检查服务器管理的设置，然后检查端点管理的设置，除了[接下来涵盖的例外键](#per-key-exceptions-across-managed-sources)。[Claude Code 如何组合托管源](/docs/zh-CN/managed-settings#precedence-within-the-managed-tier)包含完整的排名、控制键的例外以及适用于每个源的选择加入。

如果选定的源是 MDM 策略或托管设置文件，其 [`policyHelper`](/docs/zh-CN/settings-reference#policyhelper) 提供托管设置，则该助手的输出替换该源，成为该运行的唯一托管配置。当服务器管理的设置传递策略键时，Claude Code 不会查询在 MDM 或基于文件的设置中配置的 `policyHelper`。

如果后续获取发现服务器管理的设置已被移除，Claude Code 会立即运行该助手，而不是在下次启动时运行。[`policyHelper`](/docs/zh-CN/settings-reference#policyhelper) 条目涵盖该运行失败时会发生什么。

如果您在管理控制台中清除服务器管理的配置，意图回退到端点管理的 plist 或注册表策略，请注意[缓存的设置](#fetch-and-caching-behavior)在客户端机器上持久化，直到下次成功获取，而[仅在下次启动时应用](#fetch-and-caching-behavior)的键（例如 `model`）保持有效，直到每个客户端重新启动。运行 `/status` 查看哪个托管源处于活动状态。

<h3 id="per-key-exceptions-across-managed-sources">
  跨托管源的每键例外
</h3>

这些键是无合并规则的例外：

* **跨源锁定键**：一小组键，例如沙箱允许列表锁，[列在托管设置页面上](/docs/zh-CN/managed-settings#precedence-within-the-managed-tier)。当任何管理员控制的托管源设置它们时，Claude Code 会遵守它们；用户可写的 HKCU 注册表层被排除。

  当 [`policyHelper`](/docs/zh-CN/settings-reference#policyhelper) 提供托管设置时，其输出是这些检查读取的唯一源，除了 [`forceRemoteSettingsRefresh`](/docs/zh-CN/settings-reference#forceremotesettingsrefresh)，Claude Code 在启动时直接从管理员源读取它。
* **`env` 块**：除了与凭证键配对的遥测单元和路由变量（下面涵盖）外，它在管理员控制的源之间按键合并。对于每个环境变量，定义它的最高优先级源获胜，较低的管理员源填充较高源未设置的变量。因此，端点管理的 `env` 条目在服务器管理的配置未设置该变量时应用，或在该变量的缓存服务器值[等待服务器确认而被暂扣](#fetch-and-caching-behavior)期间应用。需要 Claude Code v2.1.223 或更高版本。在 v2.1.223 之前，Claude Code 仅应用选定源的整个 `env` 块。
  * **遥测单元**：`OTEL_EXPORTER_OTLP_*` 导出器键、`OTEL_LOG_*` 内容捕获切换、`OTEL_LOGS_EXPORTER` 以及测试版跟踪变量 `ENABLE_BETA_TRACING_DETAILED` 和 `BETA_TRACING_ENDPOINT` 遵循设置其中任何一个的最高源作为一个单元。传递 `otelHeadersHelper` 凭证键的源也声称该单元，但仅在它是选定源时才放置这些变量：未被选定但传递该键的源不贡献其中任何一个，仍然阻止较低源填充它们。无论哪种方式，来自一个源的导出器端点永远不能与来自另一个源的凭证配对。
  * **凭证配对的路由**：将路由变量与选定源专用凭证键（例如 `apiKeyHelper` 或 `otelHeadersHelper`）配对的源仅在它赢得该槽位时贡献这些路由变量。
* **`allowedProviders`**：机器上设置的列表和服务器管理的列表按照[其条目的范围说明](/docs/zh-CN/settings-reference#allowedproviders)所述进行组合。需要 Claude Code v2.1.285 或更高版本
* **网关登录键**：Claude Code 永远不会从服务器管理的设置中读取 [`forceLoginGatewayUrl`](/docs/zh-CN/settings-reference#forcelogingatewayurl)、[`gatewayInternalNetworks`](/docs/zh-CN/settings-reference#gatewayinternalnetworks) 或 [`forceLoginMethod`](/docs/zh-CN/settings-reference#forceloginmethod) 的 `"gateway"` 值，因此服务器管理的设置中的值既不适用也不隐藏在 MDM 策略或托管设置文件中设置的值。[`managedSourcesBehavior` 条目](/docs/zh-CN/settings-reference#managedsourcesbehavior)说明机器上的哪个管理员源提供它们。

<h3 id="fetch-and-caching-behavior">
  获取和缓存行为
</h3>

Claude Code 在启动时从 Anthropic 的服务器获取设置，并在活动会话期间每小时轮询一次更新。

通过[Claude 应用网关](#platform-availability)登录的客户端从网关获取其设置，并在会话开始前等待该获取，因此下面列表中的获取不适用于它。[强制执行故障关闭启动](#enforce-fail-closed-startup)涵盖该获取失败时会发生什么。

**首次启动而无缓存的设置：**

* 当开发者在启动时登录时，例如在首次运行或 `/logout` 后，Claude Code 在打开会话前最多等待五秒钟以获取。当策略及时到达时，Claude Code 从第一个屏幕开始强制执行它，并在其上显示您的 [`companyAnnouncements`](/docs/zh-CN/settings-reference#companyannouncements)。当有效负载需要[安全批准](#security-approval-dialogs)时，Claude Code 结束等待，并在开发者批准后应用有效负载
* 在任何其他启动中，以及当该五秒钟等待超时时，Claude Code 在获取继续进行时打开会话，因此在设置加载和限制生效前会有一个简短的窗口
* 如果获取失败，Claude Code 继续运行而不使用服务器管理的设置，并在交互式会话中警告没有远程策略适用；端点管理的设置仍然适用。如果托管源设置了 [`forceRemoteSettingsRefresh`](#enforce-fail-closed-startup)，Claude Code 会退出

**后续启动且有缓存的设置：**

* 缓存的设置在启动时立即应用，除了缓存的 `modelPricing` 和 `managedMcpServers` 值以及 Claude Code 在服务器确认有效负载之前暂扣的环境变量
* 缓存的 [`modelPricing`](/docs/zh-CN/settings-reference#modelpricing) 在会话的获取确认有效负载前不适用。在那之前，开发者在 `/usage` 中看到的成本数字和状态行处于列表价格
* 缓存的 [`managedMcpServers`](/docs/zh-CN/settings-reference#managedmcpservers) 块在会话的获取确认有效负载前不适用。Claude Code 在连接 MCP 服务器前最多等待 30 秒以获取。如果获取失败或超时，会话启动时不使用组织的服务器，`/status` 会说明这一点，它们在后续获取确认它们后连接。有关完整行为（包括首次启动），请参阅[何时提供的服务器连接](/docs/zh-CN/managed-mcp#when-provided-servers-connect)。需要 Claude Code v2.1.259 或更高版本
* Claude Code 在后台获取新鲜设置
* 缓存的设置通过网络故障持久化。如果启动获取失败，Claude Code 在交互式会话中警告缓存的策略有效
* 在某次获取成功之前，启动时被暂扣的值保持暂扣状态

Claude Code 会暂扣缓存的 `env` 块中的多个变量类别，直到服务器确认该会话的有效负载。这可以防止缓存的代理、证书颁发机构、端点或凭证值重定向、拦截或重新身份验证确认有效负载的设置获取。加固仅适用于服务器获取的设置缓存：通过 MDM 或 `managed-settings.json` 部署的[端点管理的设置](/docs/zh-CN/managed-settings#delivery-mechanisms)不受影响。该暂扣机制需要 Claude Code v2.1.198 或更高版本；在 v2.1.198 之前，整个缓存的 `env` 块在启动时应用。被暂扣的类别包括：

* 代理和 TLS 配置，例如 `HTTPS_PROXY`、`NODE_EXTRA_CA_CERTS` 以及 mTLS 客户端证书变量 `CLAUDE_CODE_CLIENT_CERT` 和 `CLAUDE_CODE_CLIENT_KEY`
* API 路由和提供商选择，包括 `ANTHROPIC_BASE_URL`、提供商选择变量（例如 `CLAUDE_CODE_USE_BEDROCK` 和 `CLAUDE_CODE_USE_VERTEX`）以及提供商端点 URL（例如 `ANTHROPIC_BEDROCK_BASE_URL`）
* 身份验证凭证，例如 `ANTHROPIC_API_KEY`、`ANTHROPIC_AUTH_TOKEN` 和 `CLAUDE_CODE_OAUTH_TOKEN`
* 配置目录选择器 `CLAUDE_CONFIG_DIR`
* 凭证源和配置目录选择器，在 Claude Code v2.1.223 或更高版本中：工作负载身份联合变量（例如 `ANTHROPIC_FEDERATION_RULE_ID` 和 `ANTHROPIC_IDENTITY_TOKEN`）、配置文件和配置目录选择器 `ANTHROPIC_PROFILE` 和 `ANTHROPIC_CONFIG_DIR` 以及操作系统目录变量 `HOME`、`XDG_CONFIG_HOME`、`APPDATA` 和 `USERPROFILE`

Claude Code 仅在启动时读取工作负载身份联合变量以及 `ANTHROPIC_PROFILE` 和 `ANTHROPIC_CONFIG_DIR` 选择器，因此服务器传递的值不会在获取成功后切换会话的凭证源。要在 Claude Code v2.1.223 或更高版本上传递这些选择器，请使用[端点管理的设置](/docs/zh-CN/managed-settings#delivery-mechanisms)，例如 MDM 或 `managed-settings.json`。对于 `CLAUDE_CONFIG_DIR` 和操作系统目录变量，暂扣本身就是保护：缓存的值保持在环境之外，直到服务器确认有效负载。

缓存的 `env` 块中的所有其他键在启动时应用。一旦服务器确认有效负载，并且如果需要[安全批准](#security-approval-dialogs)您批准它，被暂扣的变量在会话的其余时间应用。

如果您的组织需要代理来访问 `api.anthropic.com`，暂扣仅影响服务器传递的 `env` 块本身：通过 MDM 或 `managed-settings.json` 在[端点管理的](/docs/zh-CN/managed-settings#delivery-mechanisms) `env` 块中设置的代理、在 shell 环境中或在[用户设置](/docs/zh-CN/settings#where-settings-live)中到达设置获取。端点管理的源需要 Claude Code v2.1.223 或更高版本：缓存的服务器管理的代理值会被暂扣，直到获取确认它，因此端点管理的值按键填充并到达获取本身。在 v2.1.223 之前，使用 shell 环境或用户设置，以便代理与缓存的服务器有效负载一起应用。首次启动没有缓存，因此端点管理的源、shell 环境或用户设置仍然需要初始获取。

Claude Code 将大多数设置更新应用于运行的会话而无需重新启动。某些更新仅在下次启动时应用，包括 OpenTelemetry 导出器配置、`model` 键以及从 `env` 块中移除变量。

<h3 id="invalid-entries-in-delivered-settings">
  已传递设置中的无效条目
</h3>

当有效负载的一部分未通过架构验证时，Claude Code 会显示验证错误并应用每个剩余的有效设置；[托管设置中的无效条目](/docs/zh-CN/managed-settings#invalid-entries-in-managed-settings)说明它删除了什么以及哪些键回退到更严格的值。需要 Claude Code v2.1.169 或更高版本。

服务器管理的传递添加了这些行为：

* 位于 `~/.claude/remote-settings.json` 的缓存上的启动会按照写入缓存的获取处理无效条目的方式处理它们：
  * 未通过验证的条目保持被删除。
  * [故障关闭的键](/docs/zh-CN/managed-settings#keys-that-fail-closed)保持其更严格的值。
  * 无效的 `cleanupPeriodDays` 或 `desktopSessionCleanupPeriodDays` 值保留在缓存副本中，永远不会被应用。
* 当以下三个条件都为真时，Claude Code 不应用有效负载中的任何内容，并保持缓存不变：

  * 有效负载中的每个设置都未通过验证。
  * 它们都不回退到更严格的值。
  * 有效负载包含除这两个保留键之外的键。

  启动通知、`/status` 和 `claude doctor` 然后报告[失败的加载](/docs/zh-CN/errors#remote-managed-settings-failed-to-load)，原因为 `no setting in the server response could be applied as written`，该条目说明会话运行的策略。[强制执行故障关闭启动](#enforce-fail-closed-startup)的客户端在启动时退出。
* [安全批准对话框](#security-approval-dialogs)评估已保存的有效负载，因此被删除的无效条目永远不会被呈现以供批准，也永远不会执行。

要调试传递问题，请运行 `claude --debug-file <path>` 并在日志中搜索 `Remote settings`。在向组织推出有效负载更改之前，使用 `claude doctor` 在测试机器上验证有效负载更改。

<h3 id="enforce-fail-closed-startup">
  强制执行故障关闭启动
</h3>

默认情况下，如果远程设置获取在启动时失败，CLI 继续运行，使用从上次成功获取缓存的设置，但 [Claude Code 在获取成功前暂扣的值](#fetch-and-caching-behavior)除外。在从未获取过它们的机器上，CLI 继续运行而不使用服务器管理的设置，仍然应用设备上的任何[端点管理的设置](/docs/zh-CN/managed-settings#delivery-mechanisms)。

要阻止客户端在缓存或缺失的服务器管理的设置上启动，请在您的托管设置中设置 `forceRemoteSettingsRefresh: true`。

通过[Claude 应用网关](#platform-availability)登录的客户端无论您是否设置此项都会等待启动获取，并按如下方式处理失败的获取：

* 如果网关用 `401` 回答有人值守的交互式启动，且此设置关闭，网关已结束该登录。Claude Code 打印 [`Cloud gateway session expired — run /login to reconnect.`](/docs/zh-CN/errors#cloud-gateway-session-expired) 并打开会话，从网关登出，直到用户运行 `/login`。
* 当获取以任何其他方式失败，或在除 `claude auth` 子命令外的任何其他类型的启动中，客户端以错误退出。

当此设置在获取服务器管理的设置的会话中处于活动状态时，CLI 在启动时阻止，直到远程设置被新鲜获取。如果获取失败，CLI 退出而不是继续运行而不使用策略。此设置自我延续：一旦从服务器传递，它也会在本地缓存，以便后续启动即使在新会话的首次成功获取之前也强制执行相同的行为。[不获取服务器管理的设置](#platform-availability)的会话启动时不等待。

要启用此功能，请将键添加到您的托管设置配置中：

```json theme={null}
{
  "forceRemoteSettingsRefresh": true
}
```

您也可以在[端点管理的](/docs/zh-CN/managed-settings#delivery-mechanisms) MDM 配置文件或系统 `managed-settings.json` 文件中设置此键，以在首次启动时强制执行故障关闭行为，在任何服务器有效负载被传递之前。此标志是上述[优先级规则](#settings-precedence)的例外：当任何管理员控制的托管源设置它时，Claude Code 会遵守它，即使也存在缓存的服务器管理有效负载，因此当服务器管理的设置存在时，MDM 传递的值不会被忽略。

当 [`policyHelper`](/docs/zh-CN/settings-reference#policyhelper) 提供托管设置时，其输出替换 Claude Code 在启动后读取的键的所有其他托管源。有关 Claude Code 从哪些源读取此键的信息，请参阅[其设置条目](/docs/zh-CN/settings-reference#forceremotesettingsrefresh)。`policyHelper` 条目说明 Claude Code 从哪些源读取助手以及何时运行它。

设置获取还发送 `Cache-Control: no-cache` 标头，以便中间 HTTP 代理不会提供陈旧的响应。

在启用此设置之前，请确保您的网络策略允许连接到 `api.anthropic.com`。如果该端点无法访问，CLI 在启动时退出，用户无法启动 Claude Code。

`claude auth` 子命令（例如 `claude auth login`）不受此检查和网关启动退出的限制，因此用户可以在过期的凭证是设置获取失败的原因时重新身份验证。

<h3 id="security-approval-dialogs">
  安全批准对话框
</h3>

某些可能带来安全风险的设置在 Claude Code 在交互式会话中应用它们之前需要明确的用户批准：

* **Shell 命令设置**：执行 shell 命令的设置，例如 `apiKeyHelper`、`statusLine` 和 `otelHeadersHelper`
* **沙箱二进制设置**：`sandbox.bwrapPath`、`sandbox.socatPath` 和 `sandbox.ripgrep`。这些设置中的每一个都指向一个可执行文件，Claude Code 运行该可执行文件
* **沙箱网络和隔离设置**：[沙箱](/docs/zh-CN/sandboxing)设置，让沙箱代理读取、重新路由或身份验证流量，或削弱沙箱的隔离：`sandbox.network.tlsTerminate`、`sandbox.network.httpProxyPort`、`sandbox.network.socksProxyPort`、`sandbox.credentials`、`sandbox.allowAppleEvents`、`sandbox.enableWeakerNestedSandbox`、`sandbox.enableWeakerNetworkIsolation`、`sandbox.filesystem.disabled`、`sandbox.network.allowAllUnixSockets`、`sandbox.network.allowUnixSockets` 和 `sandbox.network.allowMachLookup`。仅包含 `deny` 规则的 `sandbox.credentials` 块不需要批准，因为它限制沙箱而不给代理凭证。在 v2.1.251 之前，Claude Code 应用这些设置而无需批准
* **自定义环境变量**：传递的 `env` 变量，需要用户批准，例如代理和基础 URL 变量；请参阅[环境变量和批准对话框](#environment-variables-and-the-approval-dialog)
* **Hook 配置**：任何 hook 定义

当这些设置存在时，用户会看到一个安全对话框，解释正在配置的内容。用户必须批准才能继续。如果用户拒绝设置，Claude Code 会退出。

通过 [`claudeMd`](/docs/zh-CN/settings-reference#claudemd) 键传递的托管 CLAUDE.md 不需要批准，因为它是 Claude 的指令文本，而不是 Claude Code 运行的命令。Claude Code 仍然检查 Claude 在遵循这些指令时使用的工具的[权限](/docs/zh-CN/permissions)。在 v2.1.260 之前，`claudeMd` 值需要批准。

<h4 id="approval-memory">
  批准记忆
</h4>

Claude Code 在您的配置目录 `~/.claude` 中记录您的批准，除非您设置 [`CLAUDE_CONFIG_DIR`](/docs/zh-CN/env-vars)。它记录的内容取决于设置获取使用的凭证：

* **通过 `/login` 或 `claude auth login` 保存的 claude.ai 登录，或[无密钥控制台登录](/docs/zh-CN/authentication#sign-in-without-an-api-key)**：每个组织一个批准，由最近批准的账户持有。
* **[Claude 应用网关](/docs/zh-CN/claude-apps-gateway)登录**：每个网关一个批准。

  如果您登出并重新登录到同一网关，当需要批准的设置未更改时，Claude Code 不会再次显示对话框。当这些设置更改、您登录到不同的网关以及您为同一网关接受新证书时，Claude Code 会再次显示它。

  Claude Code 不为通过纯 HTTP 到达的环回开发网关保存批准，因此对话框在每次登录后再次出现。
* **任何其他凭证**，例如 API 密钥或 `CLAUDE_CODE_OAUTH_TOKEN`：一个批准用于传递的设置，与该配置目录中设置的缓存副本一起保留。当需要批准的设置更改时，Claude Code 会显示对话框，在您运行 `/logout` 或 `claude auth logout` 后，其中任何一个都会删除缓存副本。

对于 `sandbox.credentials` 或 `sandbox.network.tlsTerminate` 的批准也涵盖这些相同传递设置中的 [`sandbox.network.allowedDomains`](/docs/zh-CN/settings-reference#sandbox-network-alloweddomains) 条目，因为两个设置都作用于该允许列表。当您的管理员添加或移除其中一个条目时，对话框会再次出现，即使 `sandbox.network.allowedDomains` 本身不需要批准。

使用保存的 claude.ai 登录：

* 如果您登出并重新登录，或切换到另一个组织，稍后返回，当这些设置未更改时，Claude Code 不会再次显示对话框，除非另一个账户在同一配置目录中为该组织批准了它们。
* 如果您使用不同的账户登录到同一组织，即使设置未更改，Claude Code 也会再次显示对话框。该账户的批准替换前一个，因此当您切换回来时，Claude Code 会再次显示对话框。

Claude Code 无法始终显示对话框。下面的每种情况说明当它无法显示时哪些设置适用，以及您何时下次看到对话框：

* **无法显示对话框的交互式会话**：Claude Code 不应用传递的设置，保留最后批准的设置。对话框在下一个可以显示它的会话中出现。需要 Claude Code v2.1.211 或更高版本。
* **`claude install` 或 `claude update`**：Claude Code 在任何命令期间都不显示对话框。该命令使用最后批准的设置运行，对话框在您的下一个交互式会话中出现。如果 Claude Code 在启动时等待设置获取，例如设置了 [`forceRemoteSettingsRefresh`](#enforce-fail-closed-startup) 或在[Claude 应用网关](/docs/zh-CN/claude-apps-gateway)部署上，它会在命令期间显示对话框，从管道运行的安装失败；请参阅[安装期间 `Raw mode is not supported`](/docs/zh-CN/troubleshoot-install#raw-mode-is-not-supported-during-install)。在 v2.1.246 之前，Claude Code 也尝试在这些命令期间显示对话框。
* **错误在您回答前关闭对话框**：Claude Code 不应用传递的设置，保留最后批准的设置。它在下一个可以显示它的会话中再次显示对话框。
* **非交互式运行**，例如 `claude -p`、Agent SDK 会话或 VS Code 扩展的聊天面板或桌面应用的代码选项卡中的会话：Claude Code 无法显示对话框，因此当传递的设置需要批准时，它仅为该运行应用它们。它不将它们记录为已批准或写入[本地缓存](#fetch-and-caching-behavior)，下一个交互式会话会显示对话框。在用户在交互式会话中批准之前，每个非交互式运行都会在启动时再次获取设置。在 v2.1.207 之前，非交互式运行会将设置保存为已批准，因此后来的交互式会话永远不会为它们显示对话框。

<h4 id="environment-variables-and-the-approval-dialog">
  环境变量和批准对话框
</h4>

Claude Code 应用某些传递的 `env` 变量而不显示用户批准对话框，包括：

* 功能和命令切换
* 模型选择和行为设置，例如 `ANTHROPIC_MODEL`、`DISABLE_PROMPT_CACHING` 和 `CLAUDE_CODE_EFFORT_LEVEL`
* 上下文窗口和压缩设置，例如 `DISABLE_AUTO_COMPACT`
* 终端 UI 和可访问性选项
* 数字限制、预算和超时

其他传递的变量可能需要用户批准才能生效；非空代理、基础 URL 或 `OTEL_EXPORTER_OTLP_ENDPOINT` 值总是这样。当传递的变量需要批准时，对话框会命名它，因此用户会看到策略要求设置的确切内容。在 v2.1.218 之前，Claude Code 应用较少的变量而不询问用户，因此 `DISABLE_AUTO_COMPACT` 等设置在任何非空值时触发对话框。

Claude Code 根据传递的值而不是变量名称决定四个隐私切换是否需要批准：`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`、`DISABLE_ERROR_REPORTING`、`DISABLE_TELEMETRY` 和 `DO_NOT_TRACK`。真值（例如 `1` 或 `true`）仅关闭跟踪、报告或其他非必要流量，因此 Claude Code 应用它而不询问用户。对于任何其他非空值，Claude Code 会显示对话框。在 v2.1.218 之前，除了 `DO_NOT_TRACK` 外的所有这些都在任何值时应用而无需批准，`DO_NOT_TRACK` 在任何非空值时触发对话框。

Claude Code 也根据传递的值决定 [`API_FORCE_IDLE_TIMEOUT`](/docs/zh-CN/env-vars) 是否需要批准：真值仅打开[主体空闲超时](/docs/zh-CN/network-config#streaming-idle-watchdogs)，因此 Claude Code 应用它而不询问用户。对于任何其他非空值，Claude Code 会显示对话框。在 v2.1.248 之前，任何非空值都触发对话框。

[`ANTHROPIC_CUSTOM_HEADERS`](/docs/zh-CN/env-vars#variables) 是否需要批准也取决于传递的值。仅标记请求的标头（例如 `Accept-Language`）应用而无需对话框。命名凭证、组织或租户选择器、路由或主机覆盖或 API 行为标头（例如 `Authorization`、`X-Api-Key`、`Host`、`anthropic-beta` 或 `X-Amzn-Bedrock-*` 标头）的行需要批准。名称不是有效 HTTP 标头令牌的行，或其值包含 HTTP 标头无法携带的字符的行也需要。检查与标头名称内的单词匹配，因此包含 `client` 和 `version` 的 `X-Client-Version` 也需要批准。在 v2.1.251 之前，任何 `ANTHROPIC_CUSTOM_HEADERS` 值应用而无需它。

[`ENABLE_BETA_TRACING_DETAILED`](/docs/zh-CN/env-vars#variables) 或 [`OTEL_LOG_RAW_API_BODIES`](/docs/zh-CN/env-vars#variables) 的假值（例如 `0` 或 `false`）应用而无需对话框，因为它仅关闭详细跟踪或原始 API 主体捕获。任何其他非空值对于任一变量都需要批准。

<h2 id="platform-availability">
  平台可用性
</h2>

服务器管理的设置需要直接连接到 `api.anthropic.com`。交付还需要会话使用以下凭证之一进行身份验证：

* Team 或 Enterprise OAuth 登录
* 通过 `CLAUDE_CODE_OAUTH_TOKEN` 提供的 OAuth 令牌
* 直接配置的 API 密钥
* 一个 `user_oauth` [Anthropic 配置文件](/docs/zh-CN/authentication#anthropic-profiles-and-federation-credentials)，除非该配置文件设置了 Anthropic API 以外的 `base_url`。需要 Claude Code v2.1.257 或更高版本。

由 [`apiKeyHelper`](/docs/zh-CN/settings-reference#apikeyhelper) 脚本返回的密钥和 [Workload Identity Federation](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation) 凭证都不会触发设置获取。

会话接收的是其身份验证所用凭据所属组织的托管设置。来自 [Claude Console](https://platform.claude.com) 的 API 密钥属于创建它的 Console 组织，该组织与您的 claude.ai Team 或 Enterprise 组织是相互独立的组织。因此，您在 claude.ai Admin Settings 中配置的设置不会到达使用该密钥进行身份验证的会话，例如使用您公司 Console API 密钥的 CI 作业。要将这些设置应用于该作业，请使用以下选项之一。OAuth 令牌选项不适用于使用 [`--bare`](/docs/zh-CN/headless#start-faster-with-bare-mode) 运行的作业，因为 bare 模式不会读取 `CLAUDE_CODE_OAUTH_TOKEN`。

* **OAuth 令牌**：使用 [`claude setup-token`](/docs/zh-CN/authentication#generate-a-long-lived-token) 生成令牌，为您的 Team 或 Enterprise 组织授权该令牌，并在作业环境中将其设置为 `CLAUDE_CODE_OAUTH_TOKEN`。从该环境中删除任何[优先于](/docs/zh-CN/authentication#authentication-precedence)该令牌的凭据，例如 `ANTHROPIC_API_KEY`。
* **端点管理的设置**：将[托管设置文件](/docs/zh-CN/managed-settings#delivery-mechanisms)部署到运行该作业的机器上。

在 Claude Desktop 应用中的 [Cowork](https://claude.com/docs/cowork/overview) 会话中，即使用户使用 Team 或 Enterprise 账户登录，Claude Code 也不会从 claude.ai 管理控制台获取服务器管理的设置。[策略应用的位置和时间](/docs/zh-CN/managed-settings#where-and-when-a-policy-applies) 涵盖了哪些策略到达用户机器上的 Cowork 会话和远程 Cowork 会话。claude.ai 在 Cowork 用户从 git 存储库或从 Cowork 标签中的**自定义**添加市场时，仍然会应用您的 [`strictKnownMarketplaces`](/docs/zh-CN/settings-reference#strictknownmarketplaces) 和 [`blockedMarketplaces`](/docs/zh-CN/settings-reference#blockedmarketplaces) 列表。[限制如何工作](/docs/zh-CN/plugins/org#restrict-what-users-can-install) 描述了该检查。

如果您在 shell 中导出 `CLAUDE_CODE_USE_*` 提供商变量或非默认的 `ANTHROPIC_BASE_URL`，Claude Code 将跳过您的会话的设置获取。[`claude doctor` 和 `/status` 报告跳过的获取及其原因](#verify-settings-delivery)。

您无法使用服务器管理的 `env` 块清除导出，因为该块通过导出阻止的获取到达。[端点管理的设置](/docs/zh-CN/managed-settings#delivery-mechanisms) `env` 块也不会恢复获取：Claude Code 在应用管理的 `env` 块之前检查资格，因此端点管理的值改变会话的提供商选择，但获取保持跳过。

要恢复服务器管理的交付，请从 shell 中删除导出，或在用户设置 `env` 块中将变量设置为 `""`，该块在资格检查之前应用。要在不依赖用户更改其 shell 的情况下强制执行策略，请改为通过端点管理的通道交付设置。

对于 Amazon Bedrock、Google Cloud 的 Agent Platform、Microsoft Foundry 和 [Claude Platform on AWS](/docs/zh-CN/claude-platform-on-aws) 部署，自托管的 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway) 提供等效的远程管理设置交付：网关登录的客户端从网关而不是 `api.anthropic.com` 获取管理设置。启动时的失败语义不同：无法到达网关的网关客户端以错误退出，而不是回退到缓存的设置，而每小时的后台刷新在两个通道上都是故障开放的。

<h2 id="audit-logging">
  审计日志
</h2>

设置更改的审计日志事件可通过合规 API 或审计日志导出获得。请联系您的 Anthropic 账户团队以获取访问权限。

审计事件包括执行的操作类型、执行操作的账户和设备，以及对先前值和新值的引用。

<h2 id="security-considerations">
  安全考虑
</h2>

服务器管理的设置提供集中的策略强制执行，但它们作为客户端控制运行，而不是安全边界。在非托管设备上，用户不需要管理员或 sudo 访问权限来绕过它们。

| 场景 | 行为 |
| :- | :- |
| 用户编辑缓存的设置文件 | 篡改的文件在启动时应用，但 Claude Code 在服务器确认有效负载前暂扣的[值](#fetch-and-caching-behavior)除外。下次服务器获取会恢复正确的设置，但[仅在下次启动时应用的键](#fetch-and-caching-behavior)除外，例如 `model` 或添加到 `env` 块的变量，这些会保持有效直到重新启动 |
| 用户删除缓存的设置文件 | 发生[首次启动行为](#fetch-and-caching-behavior) |
| 用户运行修改的 Claude Code 二进制文件 | 能够运行修改的客户端的用户可以绕过任何客户端控制 |
| 用户运行较旧的 Claude Code 版本 | 早于服务器管理设置的版本不会获取或应用它们 |
| API 不可用 | 如果可用，缓存的设置应用，但 Claude Code 在获取成功前暂扣的[值](#fetch-and-caching-behavior)除外。没有缓存的情况下，Claude Code 在下次成功获取前不强制执行任何服务器管理的设置，但仍然在设备上应用任何[端点管理的设置](/docs/zh-CN/managed-settings#delivery-mechanisms)。使用 `forceRemoteSettingsRefresh: true` 时，CLI 退出而不是继续，但[`claude auth` 子命令](#enforce-fail-closed-startup)除外。通过[Claude 应用网关](#platform-availability)登录的客户端在启动时退出而没有该设置，具有相同的 `claude auth` 豁免 |
| 用户使用不同的组织进行身份验证 | 不为托管组织外的账户传递设置，包括使用 [Console API 密钥](#platform-availability)进行身份验证的会话 |
| 用户配置[第三方模型提供商](#platform-availability) | 服务器管理的设置被绕过。这包括设置 `CLAUDE_CODE_USE_BEDROCK`、`CLAUDE_CODE_USE_MANTLE`、`CLAUDE_CODE_USE_VERTEX`、`CLAUDE_CODE_USE_FOUNDRY`、`CLAUDE_CODE_USE_ANTHROPIC_AWS` 或非默认的 `ANTHROPIC_BASE_URL` |
| 网络流量被拦截或重定向 | 禁用的 TLS 验证或拦截的流量可以改变客户端接收的设置 |

要记录对本地设置文件（包括 `managed-settings.json`）的编辑，请使用 [`ConfigChange` hooks](/docs/zh-CN/hooks#configchange)。当服务器管理的设置到达或刷新时，或当 MDM 配置文件或注册表策略更改时，Claude Code 不会运行它们，并且 hook 无法阻止 `policy_settings` 更改。

要限制用户可以使用客户端提供的凭证访问的组织，请参阅 Claude 帮助中心中的[使用租户限制强制执行网络级访问控制](https://support.claude.com/en/articles/13198485-enforce-network-level-access-control-with-tenant-restrictions)。为了获得更强的强制执行保证，请在已在 MDM 解决方案中注册的设备上使用[端点管理的设置](/docs/zh-CN/managed-settings#delivery-mechanisms)。

<h2 id="see-also">
  另请参阅
</h2>

用于管理 Claude Code 配置的相关页面：

* [所有设置](/docs/zh-CN/settings-reference)：每个设置键
* [Endpoint-managed settings](/docs/zh-CN/managed-settings#delivery-mechanisms)：由 IT 部门部署到设备的托管设置
* [Authentication](/docs/zh-CN/authentication)：设置用户对 Claude Code 的访问
* [Security](/docs/zh-CN/security)：安全保障和最佳实践
