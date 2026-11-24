> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 配置服务器管理的设置

> 通过服务器交付的设置为您的组织集中配置 Claude Code，无需设备管理基础设施。

服务器管理的设置允许组织所有者通过 claude.ai 控制台中的 [**Organization settings > Claude Code > Managed settings**](https://claude.ai/admin-settings/claude-code) 集中配置 Claude Code。Claude Code 客户端在用户使用符合条件的凭据在支持服务器管理交付的平台上进行身份验证时自动获取这些设置。请参阅[平台可用性](#platform-availability)了解符合条件的凭据和平台。

> [!NOTE]
>
> 服务器管理的设置可供 [Claude for Teams](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=server_settings_teams#team-&-enterprise) 和 [Claude for Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=server_settings_enterprise) 客户使用。
>
> 如果您在 claude.ai 的 **Organization settings > Desktop 3P** 下设置了提供商或网关，请改为按照 [Enterprise Admin Console 指南](https://claude.com/docs/third-party/claude-desktop/admin-console-claude-code)操作。

## 要求

要使用服务器管理的设置，您需要：

* Claude for Teams 或 Claude for Enterprise 计划
* 您的 Claude 组织中的所有者或主要所有者角色，以查看和编辑配置
* 对 `api.anthropic.com` 的网络访问

## 在服务器管理和端点管理的设置之间选择

Claude Code 支持两种集中配置方法。服务器管理的设置从 Anthropic 的服务器传递配置。[端点管理的设置](https://code.claude.com/docs/zh-CN/managed-settings.md#delivery-mechanisms)通过本机操作系统策略（macOS 托管首选项、Windows 注册表）或托管设置文件直接部署到设备。

| 方法 | 最适合 | 安全模型 |
| :- | :- | :- |
| **服务器管理的设置** | 没有 MDM 的组织，或非托管设备上的用户 | Claude Code 在启动时从 Anthropic 的服务器获取的设置，并在会话期间每小时刷新一次 |
| **[端点管理的设置](https://code.claude.com/docs/zh-CN/managed-settings.md#delivery-mechanisms)** | 具有 MDM 或端点管理的组织 | 通过 MDM 配置文件、注册表策略或托管设置文件部署到设备的设置 |

如果您的设备已在 MDM 或端点管理解决方案中注册，端点管理的设置提供更强的安全保证，因为设置文件可以在操作系统级别受到保护，防止用户修改。端点管理的设置不会到达 Anthropic 托管环境中的[云会话](https://code.claude.com/docs/zh-CN/model-config.md#surface-coverage)，因此在网络上使用 Claude Code 的组织也应该配置服务器管理的设置。[自托管环境](https://code.claude.com/docs/zh-CN/self-hosted-environments)中的会话也会读取运行器镜像中的托管设置文件。下面的[设置优先级](#settings-precedence)说明了该文件何时适用。

## 配置服务器管理的设置

**1. 打开管理控制台**

在 claude.ai 控制台中，转到 [**Organization settings > Claude Code > Managed settings**](https://claude.ai/admin-settings/claude-code)。

在 Team 或 Enterprise 组织中，如果页面显示您没有访问权限，请让 [Owner 或 Primary Owner](#access-control) 进行更改。

**2. 定义您的设置**

将您的配置添加为 JSON。支持 [`settings.json` 中可用的所有设置](https://code.claude.com/docs/zh-CN/settings-reference#all-settings)，除了限制于操作系统级别策略传递的设置外；有关该简短列表，请参阅[当前限制](#current-limitations)。这包括 [hooks](https://code.claude.com/docs/zh-CN/hooks.md)、[环境变量](https://code.claude.com/docs/zh-CN/env-vars.md) 和[仅限托管的设置](https://code.claude.com/docs/zh-CN/managed-settings.md#managed-only-settings)，如 `allowManagedPermissionRulesOnly`。

此示例强制执行权限拒绝列表，防止用户绕过权限，并将权限规则限制为在托管设置中定义的规则。`Bash(curl *)` 规则匹配 `curl` [如 Claude 编写的那样](https://code.claude.com/docs/zh-CN/permissions.md#bash-rule-limits)，而不是 `/usr/bin/curl` 或 `sh -c 'curl …'`；对于不依赖于命令文本的网络强制，添加一个[带有 `allowManagedDomainsOnly` 的 `sandbox` 块](https://code.claude.com/docs/zh-CN/sandboxing#configure-the-sandbox-for-your-organization)。

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

此示例在整个组织中每次 `Edit` 和 `Write` 工具调用后运行审计脚本：

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

要配置[自动模式](https://code.claude.com/docs/zh-CN/permission-modes.md#eliminate-prompts-with-auto-mode)分类器，使其了解您的组织信任的存储库、存储桶和域，以相同的方式传递 `autoMode` 块；有关 `autoMode` 条目如何影响分类器阻止的内容以及关于 `environment`、`allow`、`soft_deny` 和 `hard_deny` 字段的重要警告，请参阅[配置自动模式](https://code.claude.com/docs/zh-CN/auto-mode-config.md)。

**3. 保存并部署**

保存您的更改。Claude Code 客户端在下次启动或每小时轮询周期时接收更新的设置。

编辑器会根据已发布的 Claude Code 设置 JSON schema 检查您的 JSON。如果在可解析的 JSON 中发现问题，它会显示警告并更改保存按钮的标签。当已保存设置时，标签为 **Update with errors**；当尚未保存任何设置时，标签为 **Add with errors**。该按钮仍然会保存，因为 schema 警告不会阻止保存。

该 schema [可能落后于最新版本](https://code.claude.com/docs/zh-CN/settings.md#edit-a-settings-file)，因此编辑器可能会标记[设置参考](https://code.claude.com/docs/zh-CN/settings-reference.md#all-settings)中已记录的键或值。Claude Code 会接收您保存的键和值，并在加载它们时运行[自己的验证](#invalid-entries-in-delivered-settings)。

### 验证设置传递

要确认设置正在被应用，请要求用户重新启动 Claude Code。如果配置包含触发[安全批准对话框](#security-approval-dialogs)的设置，用户会在 Claude Code 下次获取它们时看到描述托管设置的提示：在下次启动时，或在运行的交互式会话中的一小时内。您还可以通过让用户运行 `/permissions` 来验证托管权限规则是否处于活动状态，以查看其有效的权限规则。

在会话中，请让用户运行 `/status`。当服务器管理的设置生效时，[`Setting sources` 行](https://code.claude.com/docs/zh-CN/managed-settings#read-the-source-in-/status)会列出 `Enterprise managed settings`，并在括号中注明 `remote`。

要检查特定机器上的获取结果，请让用户运行 `claude doctor` 并读取 `Managed settings (remote)` 行。需要 Claude Code v2.1.248 或更高版本。该行报告以下四种结果之一：

* 传递的设置已加载
* 您的组织没有配置服务器管理的设置
* 获取失败，包括原因以及缓存的策略是否仍然适用
* Claude Code 跳过了获取，包括原因。有关跳过它的提供商和配置，请参阅[平台可用性](#platform-availability)

在获取仍在进行中时，该行会报告这一点。

在运行的会话中，`/status` 在获取失败后显示相同的行，对于某些跳过获取的原因，例如第三方提供商变量或用户 shell 中导出的自定义 `ANTHROPIC_BASE_URL`。

### 为不同的组提供不同的设置

在 Enterprise 计划中，您可以为每个成员组提供各自的配置，而不是使用一个组织范围的配置。如果您的组织已[启用 HIPAA](https://code.claude.com/docs/zh-CN/hipaa-setup.md)，则组配置暂不可用。每个组都必须已经存在，可以是通过 SCIM 从您的身份提供商同步的组，也可以是您在管理控制台中管理的自定义组。

每个成员最多接收一个配置，并且在每台设备上都相同：

* **属于某个有配置的组的成员**：其所属组中排名最高的配置
* **其他任何人**，包括其唯一有配置的组已被删除的成员：通用配置（如果您设置了的话）

各配置之间不会合并，也不会与组织范围的配置合并，因此每个配置都必须包含您希望该组拥有的所有设置。要对每个成员应用某项限制，请将其放入每个组配置以及通用配置中。

在完成以下最后一个步骤之前，成员会继续接收组织范围的配置，因此您可以先设置并测试所有内容：

**1. 为每个组添加配置**

在 [**Organization settings > Claude Code > Managed settings**](https://claude.ai/admin-settings/claude-code) 中，点击 **Add configuration**，选择组，然后选择一个起点。要为某个组放宽策略，请选择由您的身份提供商同步的组，这样就没有人能在管理控制台中将自己添加到该组。

要保留成员当前拥有的内容并更改少数设置，请从组织范围配置的副本开始。编辑该配置并保存。

**2. 设置通用配置**

在 **Everyone else** 上点击 **Set**，并为不匹配任何组配置的成员添加 JSON。要让他们保持当前拥有的内容，请粘贴您的组织范围配置。如果您跳过此步骤，他们的本地会话将不会接收任何服务器管理的设置，而设备上的任何[端点托管设置](https://code.claude.com/docs/zh-CN/managed-settings.md#delivery-mechanisms)仍然适用。

**3. 对组进行排名**

拖动配置以调整顺序。属于多个组的成员只会接收排名最高的配置，因此请将限制最严格或最具体的组放在顶部。

**4. 检查谁会获得什么**

在页面底部的 **Check effective settings** 下，搜索某个成员以查看其将接收哪个配置。请分别检查每个组中的一个成员、属于多个组的一个成员，以及不匹配任何组配置的一个成员。

**5. 切换到基于组的模式**

点击页面顶部横幅中的 **Switch to group-based configurations** 并确认。成员会在大约一小时内接收其配置，但[仅在下次启动时生效的键](#fetch-and-caching-behavior)除外。要切换回去，请从同一横幅切换到组织范围模式：组织范围的配置将再次生效（如果您有的话），并且您的组配置会被保留。

组的模型限制仅在本地会话中有效。云端和远程 Cowork 会话使用通用配置中的 [`availableModels`](https://code.claude.com/docs/zh-CN/model-config#restrict-model-selection) 列表。如果您没有设置通用配置，该列表来自您的组织范围配置，即使在您切换到基于组的模式之后也是如此。如果您在通用配置中省略该键，则成员在这些会话中不受此列表限制。

如果您使用组的配置来设置 API 请求的去向，这仅适用于 Claude Code，而不适用于调用该 API 的其他工具。

### 访问控制

以下角色可以管理服务器管理的设置：

* **Primary Owner**
* **Owner**

限制对受信任人员的访问，因为设置更改可能会适用于组织中的所有用户。

### 仅限托管的设置

大多数[设置键](https://code.claude.com/docs/zh-CN/settings-reference.md#all-settings)可在任何范围内工作。少数几个键仅从托管设置中读取，当放置在用户或项目设置文件中时无效。有关权限和插件控制，请参阅[仅限托管的设置](https://code.claude.com/docs/zh-CN/managed-settings.md#managed-only-settings)，或读取[所有设置](https://code.claude.com/docs/zh-CN/settings-reference.md#all-settings)索引的 Scope 列以获取完整集合。

### 当前限制

服务器管理的设置有以下限制：

* 在 Team 计划中，设置统一应用于组织中的所有用户。[组配置](#give-groups-different-settings)需要 Enterprise 计划。
* 您无法通过服务器管理的设置分发 [`managed-mcp.json`](https://code.claude.com/docs/zh-CN/managed-mcp) 文件。改为在那里传递 `allowedMcpServers` 和 `deniedMcpServers` 策略键。在 Claude Code v2.1.259 或更高版本上，您还可以通过 [`managedMcpServers`](https://code.claude.com/docs/zh-CN/managed-mcp#provide-servers-through-managed-settings) 提供远程服务器，它仅接受 `http` 和 `sse` 服务器，并且不会像文件那样获得独占控制。

  Claude Code 在其[系统路径](https://code.claude.com/docs/zh-CN/managed-mcp.md#exclusive-control-with-managed-mcp-json)处部署的 `managed-mcp.json` 与托管设置层分开读取，因此当服务器管理的设置生效时，该文件仍然适用。
* 限制于操作系统级别策略源的设置，如 `policyHelper` 和 `wslInheritsWindowsSettings`，不被遵守。改为通过 MDM 或系统 `managed-settings.json` 文件部署它们。在[托管层内的优先级](https://code.claude.com/docs/zh-CN/managed-settings.md#precedence-within-the-managed-tier)下选择的源是该源时，以这种方式部署的 `policyHelper` 仅运行。

## 设置分发

### 设置优先级

服务器托管设置和[端点托管设置](https://code.claude.com/docs/zh-CN/managed-settings.md#delivery-mechanisms)都位于 Claude Code [设置层级结构](https://code.claude.com/docs/zh-CN/settings.md#settings-precedence)中的最高层级。您在此处设置的键优先于用户自己的设置文件或 `--settings` 值中的同名键，[托管设置优先级的例外情况](https://code.claude.com/docs/zh-CN/settings.md#exceptions-to-managed-settings-precedence)除外。用户的允许规则会[与您的规则合并](https://code.claude.com/docs/zh-CN/settings.md#lists-merge-instead-of-overriding)。要锁定该列表，请参阅[开发者可以更改的内容](https://code.claude.com/docs/zh-CN/managed-settings.md#what-a-developer-can-change)。

在托管层级内，Claude Code 默认使用第一个提供至少一个策略键的来源，先检查服务器托管设置，再检查端点托管设置，[下文所述的例外键](#per-key-exceptions-across-managed-sources)除外。[Claude Code 如何组合托管来源](https://code.claude.com/docs/zh-CN/managed-settings.md#precedence-within-the-managed-tier)介绍了完整的排序规则、控制键的特殊处理，以及应用所有来源的可选启用方式。

#### 当端点托管设置接管时

如果所选来源是一个 MDM 策略或托管设置文件，且其 `policyHelper` 提供托管设置，请参阅[该 helper 的输出会取代哪些内容](https://code.claude.com/docs/zh-CN/settings-reference.md#write-the-helper-output)。当服务器托管设置提供策略键时，Claude Code 不会参考在 MDM 或基于文件的设置中配置的 `policyHelper`。

如果后续的获取发现服务器托管设置已被移除，Claude Code 会立即运行该 helper，而不是等到下次启动时。[`policyHelper`](https://code.claude.com/docs/zh-CN/settings-reference#policyhelper) 条目介绍了该运行失败时会发生什么。

如果您在管理控制台中清除了服务器托管配置，意图回退到端点托管的 plist 或注册表策略，请注意：[缓存的设置](#fetch-and-caching-behavior)会在客户端机器上保留，直到下一次成功获取；而[仅在下次启动时生效](#fetch-and-caching-behavior)的键（例如 `model`）会一直有效，直到每个客户端重新启动。运行 `/status` 可查看当前生效的托管来源。

### 跨托管来源的按键例外

默认情况下，Claude Code 从[一个托管来源](#settings-precedence)读取大多数键。例外情况包括：

* **跨来源锁定键**：一小组键，例如沙箱允许列表锁定，[在托管设置页面中列出](https://code.claude.com/docs/zh-CN/managed-settings.md#precedence-within-the-managed-tier)。当任何由管理员控制的托管来源设置了这些键时，Claude Code 都会遵循它们；用户可写的 HKCU 注册表层级除外。

  当 [`policyHelper`](https://code.claude.com/docs/zh-CN/settings-reference#policyhelper) 提供托管设置时，其输出是这些检查读取的唯一来源，但 [`forceRemoteSettingsRefresh`](https://code.claude.com/docs/zh-CN/settings-reference#forceremotesettingsrefresh) 除外，Claude Code 会在启动时直接从管理员来源读取该键。
* **`env` 块**：除了与凭据键配对的遥测单元和路由变量（均在下文介绍）之外，它会在由管理员控制的来源之间按键合并。对于每个环境变量，定义它的最高优先级来源生效，较低的管理员来源会填补较高来源未设置的变量。因此，只要服务器托管配置未设置某个变量，或者该变量的缓存服务器值正处于[等待服务器确认而被暂缓](#fetch-and-caching-behavior)的状态，端点托管的 `env` 条目就会生效。需要 Claude Code v2.1.223 或更高版本。在 v2.1.223 之前，Claude Code 仅应用所选来源的整个 `env` 块。
  * **遥测单元**：`OTEL_EXPORTER_OTLP_*` 导出器键、`OTEL_LOG_*` 内容捕获开关、`OTEL_LOGS_EXPORTER`，以及 beta 追踪变量 `ENABLE_BETA_TRACING_DETAILED` 和 `BETA_TRACING_ENDPOINT`，作为一个整体跟随设置了其中任意一个的最高来源。提供 `otelHeadersHelper` 凭据键的来源也会占据该单元，但只有当它是所选来源时才会落地这些变量：一个未被选中但提供了该键的来源不会贡献其中任何变量，并且仍会阻止较低来源填补它们。无论哪种情况，来自一个来源的导出器端点都绝不会与来自另一个来源的凭据配对。
  * **与凭据配对的路由**：将路由变量与仅限所选来源的凭据键（例如 `apiKeyHelper` 或 `otelHeadersHelper`）配对的来源，只有在赢得该槽位时才会贡献这些路由变量。
* **`allowedProviders`**：机器上设置的列表与服务器托管列表按照[其条目的作用域说明](https://code.claude.com/docs/zh-CN/settings-reference.md#allowedproviders)进行组合。需要 Claude Code v2.1.285 或更高版本
* **第一方登录键**：[`forceLoginOrgUUID`](https://code.claude.com/docs/zh-CN/settings-reference#forceloginorguuid) 以及 [`forceLoginMethod`](https://code.claude.com/docs/zh-CN/settings-reference#forceloginmethod) 的 `"claudeai"` 和 `"console"` 值。如果您还部署了 MDM 策略或托管设置文件，请在其中以及在 claude.ai 的服务器托管设置中同时设置这些键，直到每个客户端都运行 v2.1.299 或更高版本。有关之后应在何处设置这些键以及哪个来源的值生效，请参阅[哪个托管来源提供登录键](https://code.claude.com/docs/zh-CN/managed-settings.md#which-managed-source-supplies-login-keys)。
* **`enforceAnthropicSignIn`**：[其条目的作用域说明](https://code.claude.com/docs/zh-CN/settings-reference.md#enforceanthropicsignin)说明了由哪些来源提供该键
* **网关登录键**：Claude Code 从不从服务器托管设置中读取 [`forceLoginGatewayUrl`](https://code.claude.com/docs/zh-CN/settings-reference#forcelogingatewayurl)、[`gatewayInternalNetworks`](https://code.claude.com/docs/zh-CN/settings-reference#gatewayinternalnetworks) 或 [`forceLoginMethod`](https://code.claude.com/docs/zh-CN/settings-reference#forceloginmethod) 的 `"gateway"` 值，因此那里的值既不会生效，也不会遮蔽在 MDM 策略或托管设置文件中设置的值。[`managedSourcesBehavior` 条目](https://code.claude.com/docs/zh-CN/settings-reference#managedsourcesbehavior)说明了由机器上的哪个管理员来源提供这些键。

#### 当机器的 `apiKeyHelper` 未生效时

当您的服务器托管设置是所选来源时，机器的托管设置文件或 MDM 策略中的 `apiKeyHelper` 不会生效。此时，只要以下两点同时成立，Claude Code 就会在将使用已保存 claude.ai 登录的会话中[拒绝提示词](https://code.claude.com/docs/zh-CN/errors.md#claude-code-didnt-send-your-claude-ai-login)：

* 该文件或策略启用了云提供商，或者任何来源设置了 Anthropic 以外的 API 地址
* 服务器托管设置未设置 helper，也未指定 Anthropic 的 API 地址

要解除拒绝，请保持该 helper 及其 API 地址生效，在服务器托管设置中指定 Anthropic 的 API 地址，或从机器的策略中移除该 helper。该拒绝行为需要 Claude Code v2.1.314 或更高版本。

### 获取和缓存行为

Claude Code 在启动时从 Anthropic 的服务器获取设置，并在活动会话期间每小时轮询一次更新。

通过 [Claude apps 网关](#platform-availability)登录的客户端会从网关获取其设置，并在会话开始前等待该获取完成，因此下面列表中的获取不适用于它。[强制失败即关闭的启动](#enforce-fail-closed-startup)介绍了该获取失败时会发生什么。

> [!NOTE]
>
> 对于存储在机器上的 Team 或 Enterprise claude.ai 登录，Anthropic 可能会要求在会话开始前获取您组织的设置。在这种情况下，无论下面的列表如何说明，开发者在以下情况下都[无法启动会话](https://code.claude.com/docs/zh-CN/errors.md#couldnt-load-your-organizations-settings)：
>
> * 其登录已过期，直到他们运行 `claude auth login`
> * Claude Code 既没有这些设置，也没有最近的缓存副本。请检查机器是否能够访问 `api.anthropic.com`
>
> 如果启动消息中包含 `before a session can start` 或 `Your Claude session has expired`，则表示该要求适用。

**首次启动且无缓存设置：**

* 当开发者在启动时登录（例如首次运行或执行 `/logout` 之后），Claude Code 会在打开会话前等待获取最多五秒。如果策略及时到达，Claude Code 会从第一个屏幕开始执行它，并在该屏幕上显示您的 [`companyAnnouncements`](https://code.claude.com/docs/zh-CN/settings-reference#companyannouncements)。当负载需要[安全批准](#security-approval-dialogs)时，Claude Code 会结束等待，并在开发者批准后应用该负载
* 在任何其他启动情况下，以及当这五秒等待结束时，Claude Code 会在获取继续进行的同时打开会话，因此在设置加载和限制生效之前会有一段短暂的时间窗口
* 如果获取失败，Claude Code 会在没有服务器托管设置的情况下继续运行，并在交互式会话和 [Claude Desktop 的 Code 标签页](https://code.claude.com/docs/zh-CN/desktop.md)中警告没有远程策略生效；端点托管设置仍然生效。如果某个托管来源设置了 [`forceRemoteSettingsRefresh`](#enforce-fail-closed-startup)，Claude Code 则会退出

**后续启动且有缓存设置：**

* 缓存的设置在启动时立即生效，但以下情况除外：缓存的 `modelPricing` 和 `managedMcpServers` 值；Claude Code 在服务器确认负载之前暂缓的环境变量；缓存的插件列表对[内置守卫](https://code.claude.com/docs/zh-CN/plugins/mods/admin.md#know-what-happens-by-default)的移除、重新定位或禁用；以及在端点托管来源自行列出或启用插件的机器上，仅由缓存列表启用的插件的[组织归属](https://code.claude.com/docs/zh-CN/plugins/mods/admin.md#install-your-organizations-mods)
* 缓存的 [`modelPricing`](https://code.claude.com/docs/zh-CN/settings-reference#modelpricing) 在会话的获取确认负载之前不会生效。在此之前，开发者在 `/usage` 和状态栏中看到的费用数据按标价计算
* 缓存的 [`managedMcpServers`](https://code.claude.com/docs/zh-CN/settings-reference#managedmcpservers) 块在会话的获取确认负载之前不会生效。Claude Code 会在连接 MCP 服务器之前等待该获取最多 30 秒。如果获取失败或超时，会话将在没有组织服务器的情况下启动，`/status` 会说明这一点，并且这些服务器会在后续获取确认它们后连接。有关完整行为（包括首次启动），请参阅[提供的服务器何时连接](https://code.claude.com/docs/zh-CN/managed-mcp.md#when-provided-servers-connect)。需要 Claude Code v2.1.259 或更高版本
* 缓存的 [`prependPlugins`](https://code.claude.com/docs/zh-CN/settings-reference#prependplugins)、[`appendPlugins`](https://code.claude.com/docs/zh-CN/settings-reference#appendplugins) 或 [`enabledPlugins`](https://code.claude.com/docs/zh-CN/settings-reference#enabledplugins) 值在会话的获取确认负载之前，无法移除内置守卫、更改其位置或将其关闭
* 在[端点托管来源](https://code.claude.com/docs/zh-CN/managed-settings.md#choose-a-delivery-mechanism)自行列出或启用插件的机器上，仅由缓存列表启用的插件在获取确认负载之前被视为[用户的](https://code.claude.com/docs/zh-CN/plugins/mods/admin.md#install-your-organizations-mods)插件，而不是您组织的插件
* Claude Code 在后台获取最新设置
* 如果会话的提供商不在缓存的 [`allowedProviders`](https://code.claude.com/docs/zh-CN/settings-reference#allowedproviders) 列表中，Claude Code 可能会等待该获取完成并再次检查，然后才决定是否拒绝。如果获取失败，会话将被拒绝
* 请按照缓存的设置在上次成功获取后 24 小时过期来进行规划
* 如果启动时的获取在缓存的设置过期之前失败，Claude Code 会在交互式会话和 Code 标签页中警告缓存的策略正在生效
* 如果启动时的获取在缓存的设置过期之后失败，会话将在没有服务器托管设置的情况下启动，并且警告会说明没有远程策略生效。要让 Claude Code 改为退出，请设置 [`forceRemoteSettingsRefresh`](#enforce-fail-closed-startup)
* 在获取成功之前，启动时暂缓的值保持暂缓

Claude Code 会暂缓缓存的 `env` 块中的若干类变量，直到服务器为该会话确认负载。这可以防止缓存的代理、证书颁发机构、端点或凭据值对确认负载的设置获取进行重定向、拦截或重新身份验证。这项加固仅适用于从服务器获取的设置缓存：通过 MDM 或 `managed-settings.json` 部署的[端点托管设置](https://code.claude.com/docs/zh-CN/managed-settings.md#delivery-mechanisms)不受影响。被暂缓的类别包括：

* 代理和 TLS 配置，例如 `HTTPS_PROXY`、`NODE_EXTRA_CA_CERTS`，以及 mTLS 客户端证书变量 `CLAUDE_CODE_CLIENT_CERT` 和 `CLAUDE_CODE_CLIENT_KEY`
* API 路由和提供商选择，包括 `ANTHROPIC_BASE_URL`、提供商选择变量（例如 `CLAUDE_CODE_USE_BEDROCK` 和 `CLAUDE_CODE_USE_VERTEX`），以及提供商端点 URL（例如 `ANTHROPIC_BEDROCK_BASE_URL`）
* 身份验证凭据，例如 `ANTHROPIC_API_KEY`、`ANTHROPIC_AUTH_TOKEN` 和 `CLAUDE_CODE_OAUTH_TOKEN`
* 配置目录选择器 `CLAUDE_CONFIG_DIR`
* 凭据来源和配置目录选择器（在 Claude Code v2.1.223 或更高版本中）：Workload Identity Federation 变量（例如 `ANTHROPIC_FEDERATION_RULE_ID` 和 `ANTHROPIC_IDENTITY_TOKEN`）、配置文件和配置目录选择器 `ANTHROPIC_PROFILE` 和 `ANTHROPIC_CONFIG_DIR`，以及操作系统目录变量 `HOME`、`XDG_CONFIG_HOME`、`APPDATA` 和 `USERPROFILE`

Claude Code 仅在启动时读取 Workload Identity Federation 变量以及 `ANTHROPIC_PROFILE` 和 `ANTHROPIC_CONFIG_DIR` 选择器，因此即使获取成功，服务器提供的这些值也不会切换会话的凭据来源。要在 Claude Code v2.1.223 或更高版本上提供这些选择器，请使用 MDM 或 `managed-settings.json` 等[端点托管设置](https://code.claude.com/docs/zh-CN/managed-settings.md#delivery-mechanisms)。对于 `CLAUDE_CONFIG_DIR` 和操作系统目录变量，暂缓本身就是保护措施：缓存的值在服务器确认负载之前不会进入环境。

缓存的 `env` 块中的其他所有键都在启动时生效。一旦服务器确认负载，并且在需要[安全批准](#security-approval-dialogs)时您已批准，被暂缓的变量将在会话的剩余时间内生效。

如果获取需要通过代理，请在以下位置之一设置 `HTTPS_PROXY`：

* 通过 MDM 或 `managed-settings.json` 设置的[端点托管](https://code.claude.com/docs/zh-CN/managed-settings.md#delivery-mechanisms) `env` 块。此来源需要 Claude Code v2.1.223 或更高版本。在 v2.1.223 之前，请使用 shell 环境或用户设置，使代理[与缓存的服务器负载同时生效](#per-key-exceptions-across-managed-sources)。
* shell 环境
* [用户设置](https://code.claude.com/docs/zh-CN/settings.md#where-settings-live)

即使 `ALL_PROXY` 已经指定了该代理，也请设置 `HTTPS_PROXY`。

Claude Code 会将大多数设置更新应用到正在运行的会话中，无需重启。某些更新仅在下次启动时生效，包括 OpenTelemetry 导出器配置、`model` 键，以及从 `env` 块中移除变量。

### 分发的设置中的无效条目

当负载的某部分未通过 schema 验证时，Claude Code 会显示验证错误，并应用其余所有有效设置；[托管设置中的无效条目](https://code.claude.com/docs/zh-CN/managed-settings.md#invalid-entries-in-managed-settings)说明了它会丢弃哪些内容，以及哪些键会回退到更严格的值。需要 Claude Code v2.1.169 或更高版本。

服务器托管分发额外具有以下行为：

* 基于 `~/.claude/remote-settings.json` 中的缓存运行的启动，会按照写入该缓存的那次获取的方式处理无效条目：
  * 未通过验证的条目保持被丢弃。
  * [失败即关闭的键](https://code.claude.com/docs/zh-CN/managed-settings.md#keys-that-fail-closed)保持其更严格的值。
  * 无效的 `cleanupPeriodDays` 或 `desktopSessionCleanupPeriodDays` 值保留在缓存副本中，且永远不会被应用。
* 当以下三点全部成立时，Claude Code 不会应用负载中的任何内容，并保持缓存不变：

  * 负载中的每个设置都未通过验证。
  * 其中没有任何设置回退到更严格的值。
  * 负载中包含除这两个保留期键之外的其他键。

  此时，启动通知、`/status` 和 `claude doctor` 会报告[加载失败](https://code.claude.com/docs/zh-CN/errors.md#remote-managed-settings-failed-to-load)，原因为 `no setting in the server response could be applied as written`，该条目会说明会话基于哪个策略运行。[强制失败即关闭的启动](#enforce-fail-closed-startup)的客户端则会在启动时退出。如果启动时停止并显示消息，提示您的组织要求 `before a session can start` 获取其设置，请参阅[Claude Code 无法加载您组织的设置](https://code.claude.com/docs/zh-CN/errors.md#couldnt-load-your-organizations-settings)。
* [安全批准对话框](#security-approval-dialogs)评估的是修复后的负载，因此被剥离的无效条目永远不会被提交批准，也永远不会执行。

要调试分发问题，请运行 `claude --debug-file <path>` 并在日志中搜索 `Remote settings`。在将负载更改推广到整个组织之前，请先在测试机器上使用 `claude doctor` 进行验证。

### 强制失败即关闭的启动

默认情况下，如果启动时远程设置获取失败，CLI 会使用上一次成功获取时缓存的设置继续运行，除非这些设置已[过期](#fetch-and-caching-behavior)。Claude Code [暂缓的值](#fetch-and-caching-behavior)在获取成功之前保持暂缓。在缓存的设置已过期或不存在时，CLI 会在没有服务器托管设置的情况下继续运行，并仍然应用设备上的任何[端点托管设置](https://code.claude.com/docs/zh-CN/managed-settings.md#delivery-mechanisms)。[Anthropic 也可能改为要求必须获取这些设置](#fetch-and-caching-behavior)。

要阻止客户端在使用缓存的或缺失的服务器托管设置时启动，请在您的托管设置中设置 `forceRemoteSettingsRefresh: true`。

通过 [Claude apps 网关](#platform-availability)登录的客户端无论是否设置此项都会等待启动时的获取，并按如下方式处理获取失败：

* 如果网关对有人值守的交互式启动返回 `401`，且此设置处于关闭状态，则表示网关已结束该登录。Claude Code 会打印 [`Cloud gateway session expired — run /login to reconnect.`](https://code.claude.com/docs/zh-CN/errors#cloud-gateway-session-expired)，并在用户运行 `/login` 之前以未登录网关的状态打开会话。
* 当获取以任何其他方式失败时，或在除 `claude auth` 子命令之外的任何其他类型的启动中，客户端会报错退出。

当此设置在获取服务器托管设置的会话中生效时，CLI 会在启动时阻塞，直到重新获取远程设置。如果获取失败，CLI 会退出，而不是在没有策略的情况下继续。[不获取服务器托管设置](#platform-availability)的会话会直接启动，无需等待。

要启用此功能，请将该键添加到您的托管设置配置中：

```json theme={null}
{
  "forceRemoteSettingsRefresh": true
}
```

您也可以在[端点托管](https://code.claude.com/docs/zh-CN/managed-settings.md#delivery-mechanisms)的 MDM 配置描述文件或系统 `managed-settings.json` 文件中设置此键，以便在任何服务器负载到达之前、在首次启动时就执行失败即关闭的行为。此标志是上述[优先级规则](#settings-precedence)的一个例外：当任何由管理员控制的托管来源设置了它时，即使同时存在缓存的服务器托管负载，Claude Code 也会遵循它，因此当存在服务器托管设置时，它不会忽略通过 MDM 下发的值。

在后续启动时，Claude Code 会从缓存的设置中读取服务器下发的值，因此该设置在新会话首次获取之前就已生效。要在不依赖缓存副本的情况下保持该设置生效，请同时在端点托管来源中设置此键。

设置获取还会发送 `Cache-Control: no-cache` 标头，以防止中间 HTTP 代理返回过期的响应。

在启用此设置之前，请确保您的网络策略允许连接到 `api.anthropic.com`。如果该端点无法访问，CLI 会在启动时退出，用户将无法启动 Claude Code。

`claude auth` 子命令（例如 `claude auth login`）不受此检查和网关启动退出的限制，因此当凭据过期导致设置获取失败时，用户可以重新进行身份验证。

### 安全批准对话框

某些可能带来安全风险的设置，在 Claude Code 于交互式会话中应用它们之前，需要用户明确批准：

* **Shell 命令设置**：执行 shell 命令的设置，例如 `apiKeyHelper`、`statusLine` 和 `otelHeadersHelper`
* **沙箱二进制文件设置**：`sandbox.bwrapPath`、`sandbox.socatPath` 和 `sandbox.ripgrep`。这些设置各自指向一个可执行文件，Claude Code 会运行该可执行文件
* **沙箱网络和隔离设置**：允许沙箱代理读取、重新路由流量或对流量进行身份验证，或削弱沙箱隔离的[沙箱](https://code.claude.com/docs/zh-CN/sandboxing.md)设置：`sandbox.network.tlsTerminate`、`sandbox.network.httpProxyPort`、`sandbox.network.socksProxyPort`、`sandbox.credentials`、`sandbox.allowAppleEvents`、`sandbox.allowNestedUserNamespaces`、`sandbox.enableWeakerNestedSandbox`、`sandbox.enableWeakerNetworkIsolation`、`sandbox.filesystem.disabled`、`sandbox.network.allowAllUnixSockets`、`sandbox.network.allowUnixSockets` 和 `sandbox.network.allowMachLookup`。仅包含 `deny` 规则的 `sandbox.credentials` 块不需要批准，因为它只限制沙箱，而不会向代理提供凭据。在 v2.1.251 之前，Claude Code 无需批准即可应用这些设置
* **自定义环境变量**：需要用户批准的下发 `env` 变量，例如代理和 base-URL 变量；请参阅[环境变量和批准对话框](#environment-variables-and-the-approval-dialog)
* **Hook 配置**：任何 hook 定义

当存在这些设置时，用户会看到一个安全对话框，说明正在配置的内容。用户必须批准才能继续。如果用户拒绝这些设置，Claude Code 会退出。

通过 [`claudeMd`](https://code.claude.com/docs/zh-CN/settings-reference#claudemd) 键下发的托管 CLAUDE.md 不需要批准，因为它是给 Claude 的指令文本，而不是 Claude Code 运行的命令。Claude Code 仍会检查 Claude 在遵循这些指令时所使用工具的[权限](https://code.claude.com/docs/zh-CN/permissions.md)。在 v2.1.260 之前，`claudeMd` 值也需要批准。

#### 批准记录

Claude Code 会将您的批准记录在您的配置目录中，除非您设置了 [`CLAUDE_CONFIG_DIR`](https://code.claude.com/docs/zh-CN/env-vars)，否则该目录为 `~/.claude`。记录的内容取决于设置获取所使用的凭据：

* **通过 `/login` 或 `claude auth login` 保存的 claude.ai 登录，或[无密钥 Console 登录](https://code.claude.com/docs/zh-CN/authentication.md#sign-in-without-an-api-key)**：每个组织一个批准，由最近一次批准的账户持有。
* **[Claude apps 网关](https://code.claude.com/docs/zh-CN/claude-apps-gateway)登录**：每个网关一个批准。

  如果您注销后重新登录到同一网关，只要需要批准的设置未发生变化，Claude Code 就不会再次显示该对话框。当这些设置发生变化、您登录到其他网关，或您为同一网关接受新证书时，Claude Code 会再次显示该对话框。

  对于通过纯 HTTP 访问的环回开发网关，Claude Code 不会保存批准，因此每次登录后都会再次出现该对话框。
* **任何其他凭据**，例如 API 密钥或 `CLAUDE_CODE_OAUTH_TOKEN`：对下发的设置记录一个批准，与该配置目录中设置的缓存副本保存在一起。当需要批准的设置发生变化时，以及在您运行 `/logout` 或 `claude auth logout`（两者都会删除缓存副本）之后，Claude Code 会再次显示该对话框。

对 `sandbox.credentials` 或 `sandbox.network.tlsTerminate` 的批准也涵盖同一批下发设置中的 [`sandbox.network.allowedDomains`](https://code.claude.com/docs/zh-CN/settings-reference#sandbox-network-alloweddomains) 条目，因为这两个设置都作用于该允许列表。当您的管理员添加或删除其中某个条目时，对话框会再次出现，即使 `sandbox.network.allowedDomains` 本身不需要批准。

使用已保存的 claude.ai 登录时：

* 如果您注销后重新登录，或切换到另一个组织后再切换回来，只要这些设置未发生变化，Claude Code 就不会再次显示该对话框，除非在此期间另一个账户在同一配置目录中为该组织批准了这些设置。
* 如果您使用其他账户登录到同一组织，即使设置未发生变化，Claude Code 也会再次显示该对话框。该账户的批准会取代之前的批准，因此当您切换回来时，Claude Code 会再次显示该对话框。

Claude Code 并非总能显示该对话框。以下各种情况说明了无法显示时哪些设置生效，以及您下次何时会看到该对话框：

* **无法显示对话框的交互式会话**：Claude Code 不应用下发的设置，并保留上次批准的设置。对话框会在下一个能够显示它的会话中出现。
* **`claude install` 或 `claude update`**：在这两个命令中的任何一个运行期间，Claude Code 都不会显示该对话框。命令会使用上次批准的设置运行，对话框会在您的下一个交互式会话中出现。如果 Claude Code 在启动时等待设置获取（例如设置了 [`forceRemoteSettingsRefresh`](#enforce-fail-closed-startup)，或在 [Claude apps 网关](https://code.claude.com/docs/zh-CN/claude-apps-gateway)部署中），它会改为在命令运行期间显示该对话框，并且从管道运行的安装会失败；请参阅[安装期间出现 `Raw mode is not supported`](https://code.claude.com/docs/zh-CN/troubleshoot-install#raw-mode-is-not-supported-during-install)。在 v2.1.246 之前，Claude Code 在这两个命令运行期间也会尝试显示该对话框。
* **输出到终端但无法从键盘读取的 `claude plugin` 命令**：当 Claude Code 在启动时不等待设置获取时，该命令不会应用下发的设置。在没有[缓存设置](#fetch-and-caching-behavior)的情况下，更改您的插件或市场的命令会[报错停止](https://code.claude.com/docs/zh-CN/errors.md#managed-settings-need-your-approval)。在有缓存设置的情况下，它会使用上次批准的设置运行。对话框会在您下次于终端中运行 `claude` 时出现。

  当您通过管道传入或重定向其输入，并且在 macOS 和 Linux 上它也无法打开 `/dev/tty` 时，该命令无法从键盘读取。如果您同时通过管道传出或重定向其输出，则该运行会变为非交互式，下发的设置仅对该次运行生效。
* **错误在您作答之前关闭了对话框**：Claude Code 不应用下发的设置，并保留上次批准的设置。它会在下一个能够显示该对话框的会话中再次显示它。
* **非交互式运行**，例如 `claude -p`、Agent SDK 会话，或 VS Code 扩展聊天面板或桌面应用 Code 标签页中的会话：Claude Code 无法显示该对话框。当下发的设置需要批准时，它们仅对该次运行生效。

  Claude Code 不会将这些设置记录为已批准，也不会将它们写入[本地缓存](#fetch-and-caching-behavior)，下一个交互式会话会显示该对话框。在用户于交互式会话中批准之前，每次非交互式运行都会在启动时重新获取设置。

#### 环境变量和批准对话框

Claude Code 会在不向用户显示批准对话框的情况下应用某些下发的 `env` 变量，包括：

* 功能和命令开关
* 模型选择和行为设置，例如 `ANTHROPIC_MODEL`、`DISABLE_PROMPT_CACHING` 和 `CLAUDE_CODE_EFFORT_LEVEL`
* 上下文窗口和压缩设置，例如 `DISABLE_AUTO_COMPACT`，但不包括 `CLAUDE_CODE_DISABLE_1M_CONTEXT`
* 终端 UI 和无障碍选项
* 数值限制、预算和超时时间

其他下发的变量可能需要用户批准后才能生效。例如，在交互式会话中，以下变量在任何非空值下都始终需要批准：

* 代理或 base-URL 变量
* `OTEL_EXPORTER_OTLP_ENDPOINT`
* `CLAUDE_CODE_DISABLE_1M_CONTEXT`

当某个下发的变量需要批准时，对话框会列出它的名称，以便用户确切了解策略要求设置的内容。

对于四个隐私开关，Claude Code 根据下发的值而不是变量名来决定是否需要批准：`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`、`DISABLE_ERROR_REPORTING`、`DISABLE_TELEMETRY` 和 `DO_NOT_TRACK`。真值（例如 `1` 或 `true`）只会关闭追踪、报告或其他非必要流量，因此 Claude Code 会在不询问用户的情况下应用它。对于任何其他非空值，Claude Code 会显示该对话框。

Claude Code 同样根据下发的值来决定 [`API_FORCE_IDLE_TIMEOUT`](https://code.claude.com/docs/zh-CN/env-vars) 是否需要批准：真值只会开启[响应体空闲超时](https://code.claude.com/docs/zh-CN/network-config.md#streaming-idle-watchdogs)，因此 Claude Code 会在不询问用户的情况下应用它。对于任何其他非空值，Claude Code 会显示该对话框。在 v2.1.248 之前，任何非空值都会触发该对话框。

[`ANTHROPIC_CUSTOM_HEADERS`](https://code.claude.com/docs/zh-CN/env-vars#variables) 是否需要批准也取决于下发的值。仅用于标记请求的标头（例如 `Accept-Language`）无需对话框即可生效。命名凭据、组织或租户选择器、路由或主机覆盖，或 API 行为标头的行（例如 `Authorization`、`X-Api-Key`、`Host`、`anthropic-beta` 或 `X-Amzn-Bedrock-*` 标头）需要批准。如果某行的名称不是有效的 HTTP 标头 token，或其值包含 HTTP 标头无法承载的字符，该行也需要批准。该检查会匹配标头名称中的单词，因此包含 `client` 和 `version` 的 `X-Client-Version` 也需要批准。在 v2.1.251 之前，任何 `ANTHROPIC_CUSTOM_HEADERS` 值都无需批准即可生效。

[`ENABLE_BETA_TRACING_DETAILED`](https://code.claude.com/docs/zh-CN/env-vars#variables) 或 [`OTEL_LOG_RAW_API_BODIES`](https://code.claude.com/docs/zh-CN/env-vars#variables) 的假值（例如 `0` 或 `false`）无需对话框即可生效，因为它只会关闭详细追踪或原始 API 请求体捕获。这两个变量的任何其他非空值都需要批准。

## 平台可用性

服务器管理的设置需要直接连接到 `api.anthropic.com`。交付还需要会话使用以下凭证之一进行身份验证：

* Team 或 Enterprise OAuth 登录
* 通过 `CLAUDE_CODE_OAUTH_TOKEN` 提供的 OAuth 令牌
* 直接配置的 API 密钥
* 一个 `user_oauth` [Anthropic 配置文件](https://code.claude.com/docs/zh-CN/authentication.md#anthropic-profiles-and-federation-credentials)，除非该配置文件设置了 Anthropic API 以外的 `base_url`。需要 Claude Code v2.1.257 或更高版本。

由 [`apiKeyHelper`](https://code.claude.com/docs/zh-CN/settings-reference#apikeyhelper) 脚本返回的密钥和 [Workload Identity Federation](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation) 凭据都不会触发设置获取。如果您在 Enterprise Admin Console 中设置提供商或网关，请参阅[控制台设置何时适用](https://claude.com/docs/third-party/claude-desktop/admin-console-claude-code#which-settings-take-priority)。

会话接收的是其身份验证所用凭据所属组织的托管设置。来自 [Claude Console](https://platform.claude.com) 的 API 密钥属于创建它的 Console 组织，该组织与您的 claude.ai Team 或 Enterprise 组织是相互独立的组织。因此，您在 claude.ai Admin Settings 中配置的设置不会到达使用该密钥进行身份验证的会话，例如使用您公司 Console API 密钥的 CI 作业。要将这些设置应用于该作业，请使用以下选项之一。OAuth 令牌选项不适用于使用 [`--bare`](https://code.claude.com/docs/zh-CN/headless#start-faster-with-bare-mode) 运行的作业，因为 bare 模式不会读取 `CLAUDE_CODE_OAUTH_TOKEN`。

* **OAuth 令牌**：使用 [`claude setup-token`](https://code.claude.com/docs/zh-CN/authentication#generate-a-long-lived-token) 生成令牌，为您的 Team 或 Enterprise 组织授权该令牌，并在作业环境中将其设置为 `CLAUDE_CODE_OAUTH_TOKEN`。从该环境中删除任何[优先于](https://code.claude.com/docs/zh-CN/authentication.md#authentication-precedence)该令牌的凭据，例如 `ANTHROPIC_API_KEY`。
* **端点管理的设置**：将[托管设置文件](https://code.claude.com/docs/zh-CN/managed-settings.md#delivery-mechanisms)部署到运行该作业的机器上。

在 Claude Desktop 应用中的 [Cowork](https://claude.com/docs/cowork/overview) 会话中，即使用户使用 Team 或 Enterprise 账户登录，Claude Code 也不会从 claude.ai 管理控制台获取服务器管理的设置。[策略应用的位置和时间](https://code.claude.com/docs/zh-CN/managed-settings.md#where-and-when-a-policy-applies) 涵盖了哪些策略到达用户机器上的 Cowork 会话和远程 Cowork 会话。当 Cowork 用户从 claude.ai 上的 git 仓库或从 Cowork 中的**自定义**添加市场时，claude.ai 仍会自行应用您的 [`strictKnownMarketplaces`](https://code.claude.com/docs/zh-CN/settings-reference#strictknownmarketplaces) 和 [`blockedMarketplaces`](https://code.claude.com/docs/zh-CN/settings-reference#blockedmarketplaces) 列表。[限制如何工作](https://code.claude.com/docs/zh-CN/plugins/org.md#restrict-what-users-can-install) 描述了该检查。

如果您在 shell 中导出 `CLAUDE_CODE_USE_*` 提供商变量或非默认的 `ANTHROPIC_BASE_URL`，Claude Code 将跳过您的会话的设置获取。[`claude doctor` 和 `/status` 报告跳过的获取及其原因](#verify-settings-delivery)。

您无法使用服务器管理的 `env` 块清除导出，因为该块通过导出阻止的获取到达。[端点管理的设置](https://code.claude.com/docs/zh-CN/managed-settings.md#delivery-mechanisms) `env` 块也不会恢复获取：Claude Code 在应用管理的 `env` 块之前检查资格，因此端点管理的值改变会话的提供商选择，但获取保持跳过。

要恢复服务器管理的交付，请从 shell 中删除导出，或在用户设置 `env` 块中将变量设置为 `""`，该块在资格检查之前应用。要在不依赖用户更改其 shell 的情况下强制执行策略，请改为通过端点管理的通道交付设置。

对于 Amazon Bedrock、Google Cloud 的 Agent Platform、Microsoft Foundry 和 [Claude Platform on AWS](https://code.claude.com/docs/zh-CN/claude-platform-on-aws.md) 部署，自托管的 [Claude apps gateway](https://code.claude.com/docs/zh-CN/claude-apps-gateway) 提供等效的远程管理设置交付：网关登录的客户端从网关而不是 `api.anthropic.com` 获取管理设置。启动时的失败语义不同：无法到达网关的网关客户端以错误退出，而不是回退到缓存的设置，而每小时的后台刷新在两个通道上都是故障开放的。

## 审计日志

设置更改的审计日志事件可通过合规 API 或审计日志导出获得。请联系您的 Anthropic 账户团队以获取访问权限。

审计事件包括执行的操作类型、执行操作的账户和设备，以及对先前值和新值的引用。

## 安全考虑

服务器管理的设置提供集中的策略强制执行，但它们作为客户端控制运行，而不是安全边界。在非托管设备上，用户不需要管理员或 sudo 访问权限来绕过它们。

| 场景 | 行为 |
| :- | :- |
| 用户编辑缓存的设置文件 | 篡改的文件可能在启动时应用，但 [Claude Code 在服务器确认负载前暂扣的值](#fetch-and-caching-behavior)除外。下次服务器获取会恢复正确的设置。对于[仅在下次启动时应用的键](#fetch-and-caching-behavior)（例如 `model` 或添加到 `env` 块的变量），篡改的值会一直保持有效，直到重新启动 |
| 用户删除缓存的设置文件 | 发生[首次启动行为](#fetch-and-caching-behavior) |
| 用户运行修改的 Claude Code 二进制文件 | 能够运行修改的客户端的用户可以绕过任何客户端控制 |
| 用户运行较旧的 Claude Code 版本 | 早于服务器管理设置的版本不会获取或应用它们 |
| API 不可用 | 如果缓存的设置可用且未[过期](#fetch-and-caching-behavior)，则应用缓存的设置。没有这样的缓存设置时，Claude Code 在下次成功获取前不强制执行任何服务器管理的设置。[获取和缓存行为](#fetch-and-caching-behavior)列出了例外情况，包括 Anthropic 要求这些设置的情况。使用 `forceRemoteSettingsRefresh: true` 时，CLI 退出而不是继续，但[`claude auth` 子命令](#enforce-fail-closed-startup)除外。通过[Claude 应用网关](#platform-availability)登录的客户端即使没有该设置也会在启动时退出，同样豁免 `claude auth` |
| 用户使用不同的组织进行身份验证 | 不为托管组织外的账户传递设置，包括使用 [Console API 密钥](#platform-availability)进行身份验证的会话 |
| 用户配置[第三方模型提供商](#platform-availability) | 服务器管理的设置被绕过。这包括设置 `CLAUDE_CODE_USE_BEDROCK`、`CLAUDE_CODE_USE_MANTLE`、`CLAUDE_CODE_USE_VERTEX`、`CLAUDE_CODE_USE_FOUNDRY`、`CLAUDE_CODE_USE_ANTHROPIC_AWS` 或非默认的 `ANTHROPIC_BASE_URL` |
| 网络流量被拦截或重定向 | 禁用的 TLS 验证或拦截的流量可以改变客户端接收的设置 |

要记录对本地设置文件（包括 `managed-settings.json`）的编辑，请使用 [`ConfigChange` hooks](https://code.claude.com/docs/zh-CN/hooks#configchange)。当服务器管理的设置到达或刷新时，或当 MDM 配置文件或注册表策略更改时，Claude Code 不会运行它们，并且 hook 无法阻止 `policy_settings` 更改。

要限制用户可以使用客户端提供的凭证访问的组织，请参阅 Claude 帮助中心中的[使用租户限制强制执行网络级访问控制](https://support.claude.com/en/articles/13198485-enforce-network-level-access-control-with-tenant-restrictions)。为了获得更强的强制执行保证，请在已在 MDM 解决方案中注册的设备上使用[端点管理的设置](https://code.claude.com/docs/zh-CN/managed-settings.md#delivery-mechanisms)。

## 另请参阅

用于管理 Claude Code 配置的相关页面：

* [所有设置](https://code.claude.com/docs/zh-CN/settings-reference.md)：每个设置键
* [Endpoint-managed settings](https://code.claude.com/docs/zh-CN/managed-settings.md#delivery-mechanisms)：由 IT 部门部署到设备的托管设置
* [Authentication](https://code.claude.com/docs/zh-CN/authentication.md)：设置用户对 Claude Code 的访问
* [Security](https://code.claude.com/docs/zh-CN/security.md)：安全保障和最佳实践
