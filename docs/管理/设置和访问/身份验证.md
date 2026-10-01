> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 身份验证

> 登录 Claude Code 并为个人、团队和组织配置身份验证。

Claude Code 支持多种身份验证方法，具体取决于您的设置。个人用户可以使用 claude.ai 账户登录，而团队可以使用 Claude for Teams 或 Enterprise、Claude Console 或云提供商（如 Amazon Bedrock、Google Cloud 的 Agent Platform 或 Microsoft Foundry）。

<h2 id="log-in-to-claude-code">
  登录 Claude Code
</h2>

[安装 Claude Code](/docs/zh-CN/setup#install-claude-code) 后，在终端中运行 `claude`。首次启动时，Claude Code 会打开浏览器窗口供您登录。如果您已设置 `ANTHROPIC_API_KEY` 环境变量，Claude Code 会跳过登录提示，改为要求您批准该密钥。

如果浏览器没有自动打开，请按 `c` 将登录 URL 复制到剪贴板，然后将其粘贴到浏览器中。

如果您的浏览器在您登录后显示登录代码而不是重定向回来，请将其粘贴到终端的 `Paste code here if prompted` 提示符处。这种情况在浏览器无法访问 Claude Code 的本地回调服务器时会发生，这在 WSL2、SSH 会话和容器中很常见。

登录完成后，终端会显示 `Login successful`，并提示您按 `Enter` 继续。

您可以使用以下任何账户类型进行身份验证：

* **Claude Pro 或 Max 订阅**：使用您的 claude.ai 账户登录。在 [claude.com/pricing](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=authentication_pro_max) 订阅。
* **Claude for Teams 或 Enterprise**：使用您的团队管理员邀请您的 claude.ai 账户登录。
* **Claude Console**：使用您的 Console 凭证登录。您的管理员必须先 [邀请您](#claude-console-authentication)。您可以在有或没有 [创建 API 密钥](#sign-in-without-an-api-key) 的情况下登录。
* **云提供商**：如果您的组织使用 [Amazon Bedrock](/docs/zh-CN/amazon-bedrock)、[Google Cloud's Agent Platform](/docs/zh-CN/google-vertex-ai) 或 [Microsoft Foundry](/docs/zh-CN/microsoft-foundry)，请在运行 `claude` 之前设置所需的环境变量，或在登录提示符处选择 **3rd-party platform**，这将为 Bedrock 和 Vertex AI 启动交互式设置向导。不需要浏览器登录。
* **云网关**：如果您的组织运行自托管的 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway)，请通过 `/login` 使用企业 SSO 登录。网关颁发的令牌是会话的唯一凭证。

管理员可以指导开发人员使用哪种登录方法，并要求 claude.ai 登录属于特定组织；请参阅 [限制登录到您的组织](#restrict-login-to-your-organization)。

要登出并重新身份验证，请在 Claude Code 提示符处输入 `/logout`。登出还会重置您的首次启动设置状态，因此下次运行 `claude` 时，它会再次引导您完成登录和设置。

如果您在登录时遇到问题，请参阅 [身份验证故障排除](/docs/zh-CN/troubleshoot-install#login-and-authentication)。

<h3 id="log-in-with-multiple-accounts">
  使用多个账户登录
</h3>

要同时保持登录多个账户（例如工作和个人账户），请为每个账户提供自己的配置目录。启动 `claude` 时，将 [`CLAUDE_CONFIG_DIR`](/docs/zh-CN/env-vars#variables) 环境变量设置为您要使用的账户的目录。每个目录都有自己的设置、会话历史记录和 claude.ai 登录或 API 密钥。例如，在 Bash 或 Zsh 中，将此别名添加到 `~/.bashrc` 或 `~/.zshrc`，以便 `claude-work` 使用您的工作账户，而 `claude` 保持您的个人账户：

```bash theme={null}
alias claude-work='CLAUDE_CONFIG_DIR=~/.claude-work claude'
```

首次打开新终端并运行 `claude-work` 后，Claude Code 会引导您完成新目录的登录和设置。单独的目录不会将两个 Claude Console 登录 [不带 API 密钥](#sign-in-without-an-api-key) 分开，因为 Claude Code 将这种类型的登录存储在配置目录之外。

<h2 id="set-up-team-authentication">
  设置团队身份验证
</h2>

对于团队和组织，您可以通过以下方式之一配置 Claude Code 访问：

* [Claude for Teams 或 Enterprise](#claude-for-teams-or-enterprise)，推荐用于大多数团队
* [Claude Console](#claude-console-authentication)
* [Claude apps gateway](/docs/zh-CN/claude-apps-gateway)，一个自托管网关，使用您的 IdP 为开发人员签名，并将推理路由到您配置的云提供商
* [Amazon Bedrock](/docs/zh-CN/amazon-bedrock)
* [Google Cloud's Agent Platform](/docs/zh-CN/google-vertex-ai)
* [Microsoft Foundry](/docs/zh-CN/microsoft-foundry)

<h3 id="claude-for-teams-or-enterprise">
  Claude for Teams 或 Enterprise
</h3>

[Claude for Teams](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=authentication_teams#team-&-enterprise) 和 [Claude for Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=authentication_enterprise) 为使用 Claude Code 的组织提供最佳体验。团队成员可以访问 Claude Code 和网络版 Claude，具有集中式计费和团队管理。

* **Claude for Teams**：自助服务计划，具有协作功能、管理工具、SSO、计费管理和 [服务器托管设置](/docs/zh-CN/server-managed-settings)，用于组织范围的 Claude Code 配置。最适合较小的团队。
* **Claude for Enterprise**：添加域名捕获、基于角色的权限和合规性 API。最适合具有安全和合规性要求的大型组织。

<Steps>
  <Step title="订阅">
    订阅 [Claude for Teams](https://claude.com/pricing?utm_source=claude_code\&utm_medium=docs\&utm_content=authentication_teams_step#team-&-enterprise) 或联系销售部门了解 [Claude for Enterprise](https://anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=authentication_enterprise_step)。
  </Step>

  <Step title="邀请团队成员">
    从管理员仪表板邀请团队成员。
  </Step>

  <Step title="安装并登录">
    团队成员安装 Claude Code 并使用其 claude.ai 账户登录。
  </Step>
</Steps>

<h3 id="claude-console-authentication">
  Claude Console 身份验证
</h3>

对于偏好基于 API 的计费的组织，您可以通过 Claude Console 设置访问权限。

<Steps>
  <Step title="创建或使用 Console 账户">
    使用您现有的 Claude Console 账户或创建新账户。
  </Step>

  <Step title="添加用户">
    您可以通过以下任一方法添加用户：

    * 从 Console 内批量邀请用户：Settings -> Members -> Invite
    * [设置 SSO](https://support.claude.com/en/articles/13132885-setting-up-single-sign-on-sso)
  </Step>

  <Step title="分配角色">
    邀请用户时，分配以下角色之一：

    * **Claude Code** 角色：用户只能创建 Claude Code API 密钥
    * **Developer** 角色：用户可以创建任何类型的 API 密钥
  </Step>

  <Step title="用户完成设置">
    每个受邀用户需要：

    * 接受 Console 邀请
    * [检查系统要求](/docs/zh-CN/setup#system-requirements)
    * [安装 Claude Code](/docs/zh-CN/setup#install-claude-code)
    * 使用 Console 账户凭证登录
  </Step>
</Steps>

<h4 id="sign-in-without-an-api-key">
  无需 API 密钥登录
</h4>

您可以无需创建 API 密钥即可登录到您的 Console 账户，即使您的组织不允许开发人员创建 API 密钥。在 `/login` 提示符处选择 Anthropic Console 账户，Claude Code 会询问您想如何登录。需要 Claude Code v2.1.242 或更高版本。两种路由都会在浏览器中将您登录到 Console，但在 Claude Code 之后存储的内容不同：

* **使用您的 Console 账户登录**，标记为 `(recommended)`：Claude Code 保留该登录的 OAuth 令牌，并将其存储为 [Anthropic 配置文件](#anthropic-profiles-and-federation-credentials)。它不创建 API 密钥
* **创建 API 密钥**，标记为 `(legacy)`：Claude Code 为您创建 Console API 密钥，并将其与您的其他凭证一起存储

实际上，配置文件存储 OAuth 登录，而 API 密钥是静态凭证：Claude Code 自动刷新配置文件的登录，当刷新失败时，请求会失败并显示 [Anthropic 配置文件登录已过期](/docs/zh-CN/errors#anthropic-profile-login-expired)，直到您再次登录。

您不会在每台机器上都获得选择。Claude Code 在以下情况下会在不询问的情况下创建 API 密钥：

* 您针对云提供商运行，例如 [Amazon Bedrock、Google Cloud's Agent Platform 或 Microsoft Foundry](/docs/zh-CN/third-party-integrations) 或 [AWS 上的 Claude Platform](/docs/zh-CN/claude-platform-on-aws)
* 任何设置文件设置 [`forceLoginOrgUUID`](#restrict-login-to-your-organization)，或将 `forceLoginMethod` 设置为 `"claudeai"` 或 `"console"`
* 您机器上存在托管设置源（例如托管设置文件、MDM 配置文件或缓存的服务器托管设置），但 Claude Code [无法读取它](/docs/zh-CN/managed-settings#invalid-entries-in-managed-settings)，且没有其他托管源提供策略

在无密钥登录之前取消设置 `ANTHROPIC_API_KEY`。

无密钥登录后，您拥有配置文件而不是存储的 API 密钥：

* **它写入的配置文件**：Claude Code 写入由 `ANTHROPIC_PROFILE` 命名的配置文件，或您的活跃配置文件，或 `default`。如果该配置文件是联合配置文件，Claude Code 会拒绝登录而不是覆盖它
* **它将您登出的内容**：Claude Code 将您登出存储在机器上的任何 claude.ai 登录
* **如何撤销它**：运行 `/logout`，它会删除并撤销此登录写入的凭证

如果您的组织使用 [服务器托管设置](/docs/zh-CN/server-managed-settings)，它们会在 Claude Code v2.1.257 或更高版本上应用于此登录。

关于配置文件的所有其他内容都适用于此登录，包括它在您的其他凭证中的排名、您在 `/status` 中获得的 `Profile` 行，以及需要 claude.ai 登录的功能。请参阅 [Anthropic 配置文件和联合凭证](#anthropic-profiles-and-federation-credentials)。

<h3 id="cloud-provider-authentication">
  云提供商身份验证
</h3>

对于使用 Amazon Bedrock、Google Cloud's Agent Platform 或 Microsoft Foundry 的团队：

<Steps>
  <Step title="遵循提供商设置">
    遵循 [Amazon Bedrock 文档](/docs/zh-CN/amazon-bedrock)、[Google Cloud's Agent Platform 文档](/docs/zh-CN/google-vertex-ai) 或 [Microsoft Foundry 文档](/docs/zh-CN/microsoft-foundry)。
  </Step>

  <Step title="分发配置">
    将环境变量和生成云凭证的说明分发给您的用户。阅读有关如何 [在此处管理配置](/docs/zh-CN/settings) 的更多信息。
  </Step>

  <Step title="安装 Claude Code">
    用户可以 [安装 Claude Code](/docs/zh-CN/setup#install-claude-code)。
  </Step>
</Steps>

<h3 id="restrict-login-to-your-organization">
  限制登录到您的组织
</h3>

要求开发人员的 claude.ai 登录属于特定的 Anthropic 组织，请在 [托管设置](/docs/zh-CN/managed-settings) 中设置 [`forceLoginMethod`](/docs/zh-CN/settings-reference#forceloginmethod) 和 [`forceLoginOrgUUID`](/docs/zh-CN/settings-reference#forceloginorguuid)。将 `forceLoginOrgUUID` 设置为您的组织 ID，该 ID 显示在 [claude.ai 管理员设置](https://claude.ai/admin-settings/organization) 中，适用于 Claude for Teams 或 Enterprise 组织。Claude Code 会为任何其他组织的 claude.ai 登录报告错误，如果使用中的 claude.ai 凭证属于未列出的组织，则在启动时退出。

对于 Claude Console 登录，当您将其设置为单个 Console 组织 ID（显示在 [platform.claude.com/settings/organization](https://platform.claude.com/settings/organization)）时，Claude Code 使用 `forceLoginOrgUUID` 在 Console 登录页面上预选组织。它不检查生成的 Console 凭证属于哪个组织，无论是在登录时还是在启动时。在您部署密钥之前使用 Console 账户登录的开发人员会保持登录状态，该保存的密钥在同时需要 [网关](/docs/zh-CN/claude-apps-gateway) 登录的机器上被阻止，或在选择云提供商的会话中被阻止。

如果您在任何设置文件中设置 `forceLoginOrgUUID`，Claude Code 会停止在该文件适用的会话中提供 [无密钥 Console 登录](#sign-in-without-an-api-key)，而是创建 API 密钥。要将开发人员定向到 claude.ai 登录，请将 `forceLoginMethod` 设置为 `"claudeai"`。

在 Claude Code v2.1.212 或更高版本上，此处列出的每个登录路径都应用 `forceLoginMethod`。在终端的交互式登录屏幕上，通过 `/login` 或首次运行入门到达，Claude Code 预选 `claudeai` 或 `console` 方法而不强制执行，因此即使设置了 `forceLoginMethod` 为 `"claudeai"`，开发人员仍然可以在那里完成 Console 登录。

这些路径在 `forceLoginOrgUUID` 上有所不同：

* **终端、[VS Code 扩展](/docs/zh-CN/vs-code) 和 Agent SDK 登录**：验证 claude.ai 账户登录的 `forceLoginOrgUUID`
* **`claude setup-token` 和 `/install-github-app`**：仅强制执行 `forceLoginMethod`，因此它们可以在不同的组织中铸造令牌
* **[网关](/docs/zh-CN/claude-apps-gateway) 登录**：由 `forceLoginMethod: "gateway"` 选择而不是受其限制，并且不针对 Anthropic 组织进行身份验证，因此 `forceLoginOrgUUID` 不适用；使用您的网关身份提供商来限制访问

通过您的设备管理工具部署密钥。[服务器托管设置](/docs/zh-CN/server-managed-settings) 仅到达已经通过您的组织身份验证的账户，因此它们无法重定向开发人员的首次登录。如果您的组织也分发服务器托管设置，请在两个地方设置密钥：托管设置源 [不合并](/docs/zh-CN/server-managed-settings#settings-precedence)，缓存的服务器托管设置替换设备托管文件，除了几个 [按密钥例外](/docs/zh-CN/server-managed-settings#per-key-exceptions-across-managed-sources)。`forceLoginOrgUUID` 和 `forceLoginMethod` 的 `"claudeai"` 和 `"console"` 值不在这些例外中，因此在两个地方都保留它们。

在 [网关](/docs/zh-CN/claude-apps-gateway) 部署中，也要将 `forceLoginMethod` 和 `forceLoginOrgUUID` 保留在 [网关提供的设置](/docs/zh-CN/claude-apps-gateway-config#managed) 之外。

这些密钥还决定不使用登录凭证的会话是否可以启动。有关完整行为，请参阅设置参考中的 [`forceLoginOrgUUID`](/docs/zh-CN/settings-reference#forceloginorguuid)。

* **`ANTHROPIC_API_KEY`、`ANTHROPIC_AUTH_TOKEN` 或 `apiKeyHelper`**：在启动时被阻止。在 `forceLoginOrgUUID` 下，无法验证环境凭证的组织成员身份，在 `forceLoginMethod` 下，凭证会代替所需的登录。当托管设置也需要 [网关](/docs/zh-CN/claude-apps-gateway) 登录时，Claude Code 以相同方式阻止由早期 Claude Console 登录保存的 API 密钥。请参阅 [管理员策略需要云网关登录](/docs/zh-CN/errors#administrator-policy-requires-a-cloud-gateway-sign-in)
* **云提供商会话，例如 Amazon Bedrock**：仅在 `ANTHROPIC_API_KEY`、`ANTHROPIC_AUTH_TOKEN` 或 `apiKeyHelper` 凭证，或由早期 Claude Console 登录保存的 API 密钥仍然存在于机器上时被阻止。删除它，会话就会启动。这些会话针对您的云提供商进行身份验证，其访问策略管理它们
* **[Anthropic 配置文件或联合凭证](#anthropic-profiles-and-federation-credentials)**：不被阻止，除非 `ANTHROPIC_API_KEY`、`ANTHROPIC_AUTH_TOKEN` 或 `apiKeyHelper` 凭证，或由早期 Claude Console 登录保存的 API 密钥也存在于机器上。这些密钥不检查配置文件属于哪个组织

<h3 id="restrict-which-api-providers-a-machine-may-use">
  限制机器可能使用的 API 提供商
</h3>

[`allowedProviders`](/docs/zh-CN/settings-reference#allowedproviders) 在 [托管设置](/docs/zh-CN/managed-settings) 中列出托管机器可能通过哪些服务访问 Claude，例如 Anthropic API、Amazon Bedrock 或 LLM 网关。它补充 `forceLoginMethod` 和 `forceLoginOrgUUID`，它们管理会话在与 Anthropic 通信时使用的账户。需要 Claude Code v2.1.285 或更高版本。

```json managed-settings.json theme={null}
{
  "forceLoginMethod": "claudeai",
  "forceLoginOrgUUID": ["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"],
  "allowedProviders": ["anthropic", "bedrock"]
}
```

使用此文件，登录到您的 claude.ai 组织或为 Amazon Bedrock 配置的开发人员正常启动。为任何其他提供商设置的会话在启动时被拒绝，运行中切换到一个的会话在其下一个请求时被拒绝。[托管设置不允许此 API 提供商](/docs/zh-CN/errors#managed-settings-dont-allow-this-api-provider) 显示每条消息。

* **允许 LLM 网关或代理**：列出 `"customEndpoint"` 并在同一源的托管 `env` 块中设置网关的 URL。[设置参考](/docs/zh-CN/settings-reference#allowedproviders) 列出每个值并说明哪些端点变量需要托管 `env` 引脚。
* **在托管机器上部署**：将列表放在承载您的其余策略的托管源中。条目的 [范围说明](/docs/zh-CN/settings-reference#allowedproviders) 说明服务器托管列表如何与其结合。
* **仅服务器托管设置**：您仅在 [服务器托管设置](/docs/zh-CN/server-managed-settings) 中设置的列表仅到达获取您的组织设置的会话，因此将其视为您无法通过设备管理到达的机器的便利，而不是强制执行。[平台可用性](/docs/zh-CN/server-managed-settings#platform-availability) 列出哪些会话获取它们。

<h2 id="credential-management">
  凭证管理
</h2>

Claude Code 安全地管理您的身份验证凭证：

* **存储位置**：
  * 在 macOS 上，凭证存储在加密的 macOS Keychain 中。当 Keychain 拒绝写入时，例如在 SSH 会话中被锁定时，Claude Code 会改为将您的登录存储在 `~/.claude/.credentials.json` 中，文件模式为 `0600`，这与它在 Linux 上使用的存储相同。使用 Console 登录创建 API 密钥的操作会失败，直到 Keychain 可写。要将您的登录移回 Keychain，请按照[恢复步骤](/docs/zh-CN/troubleshoot-install#not-logged-in-or-token-expired)进行操作。
  * 在 Linux 上，凭证存储在 `~/.claude/.credentials.json` 中，文件模式为 `0600`。
  * 在 Windows 上，凭证存储在 `%USERPROFILE%\.claude\.credentials.json` 中，并继承您的用户配置文件目录的访问控制，默认情况下将文件限制为您的用户帐户。
  * 如果您设置了 `CLAUDE_CONFIG_DIR` 环境变量，Claude Code 会将 `.credentials.json` 文件保存在该目录下，包括 macOS 回退写入的文件，并且还会将 macOS Keychain 条目关键字设置为该目录，因此使用不同 `CLAUDE_CONFIG_DIR` 的会话会读取不同的条目。
  * Claude Code 通过 `/login` 和 `/logout` 管理 `.credentials.json`。要通过自定义 API 端点路由请求，请改为设置 [`ANTHROPIC_BASE_URL`](/docs/zh-CN/env-vars) 环境变量。
* **支持的身份验证类型**：claude.ai 凭证、Claude API 凭证、Microsoft Foundry Auth、Bedrock Auth、Vertex Auth、Anthropic 配置文件和 [Workload Identity Federation](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation) 凭证，以及 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway) 会话令牌。
* **自定义凭证脚本**：配置 [`apiKeyHelper`](/docs/zh-CN/settings-reference#apikeyhelper) 设置以运行返回 API 密钥的 shell 脚本。
* **刷新间隔**：请参阅 [`apiKeyHelper`](/docs/zh-CN/settings-reference#apikeyhelper) 了解 Claude Code 重新运行助手的情况。
* **缓慢助手通知**：如果 `apiKeyHelper` 返回密钥需要超过 10 秒，Claude Code 会在提示栏中显示警告通知，显示经过的时间。如果您经常看到此通知，请检查您的凭证脚本是否可以优化。
* **助手失败**：当脚本以错误退出、超时或不输出任何内容时，请求在三次尝试内失败，显示 [`Your apiKeyHelper script is failing`](/docs/zh-CN/errors#your-apikeyhelper-script-is-failing)。

`apiKeyHelper`、`ANTHROPIC_API_KEY` 和 `ANTHROPIC_AUTH_TOKEN` 适用于 CLI 和包装它的表面，包括 VS Code 扩展、Agent SDK 和 GitHub Actions。Claude Desktop 和云会话不会调用 `apiKeyHelper` 或读取这些环境变量：它们使用 OAuth，除了运行[第三方推理配置](/docs/zh-CN/llm-gateway-connect#desktop-app)的桌面会话外，这些会话使用该配置的凭证进行身份验证。

<h3 id="renew-an-expiring-login">
  续期即将过期的登录
</h3>

当您使用 `/login` 创建的登录在过期前三天内时，Claude Code 会在启动时显示警告：`Your login expires in 3 days · run /login to renew`。

运行 `/login` 以续期。该警告仅供参考，永远不会阻止请求：身份验证将继续工作，直到登录实际过期。

一旦存储的登录过期且无法刷新，每个模型请求都会失败，显示 [`Login expired · Please run /login`](/docs/zh-CN/errors#login-expired)，直到您再次登录。

您可以在请求失败之前检查此状态：[`/status`](/docs/zh-CN/commands) 显示 `Login` 行，读取 `Expired — log in again`，加上它为过期登录保存的组织和电子邮件。该行仅在保存的 claude.ai 登录是活跃凭证时出现。该行需要 Claude Code v2.1.210 或更高版本。

该警告仅在 claude.ai 登录是活跃凭证时出现，而不是在云提供商、`ANTHROPIC_API_KEY`、`ANTHROPIC_AUTH_TOKEN` 或 `apiKeyHelper` 提供凭证时出现。

对于运行无人值守的会话，提前续期最为重要。在 [agent view 中的后台会话](/docs/zh-CN/agent-view)或 [Remote Control](/docs/zh-CN/remote-control) 会话一旦凭证过期，就会停止进行，并且在您再次登录之前无法恢复。

<h3 id="authentication-precedence">
  身份验证优先级
</h3>

当存在多个凭证时，Claude Code 按以下顺序选择一个：

1. 云提供商凭证，当设置了 `CLAUDE_CODE_USE_BEDROCK`、`CLAUDE_CODE_USE_VERTEX` 或 `CLAUDE_CODE_USE_FOUNDRY` 时。有关设置，请参阅[第三方集成](/docs/zh-CN/third-party-integrations)。
2. `ANTHROPIC_AUTH_TOKEN` 环境变量。作为 `Authorization: Bearer` 标头发送。当通过[LLM 网关或代理](/docs/zh-CN/llm-gateway)进行路由时使用此选项，该网关或代理使用持有者令牌而不是 Anthropic API 密钥进行身份验证。
3. `ANTHROPIC_API_KEY` 环境变量。作为 `X-Api-Key` 标头发送。用于直接 Anthropic API 访问，使用来自 [Claude Console](https://platform.claude.com) 的密钥。在交互模式下，系统会提示您一次批准或拒绝该密钥，您的选择会被记住。要稍后更改它，请使用 `/config` 中的"使用自定义 API 密钥"切换。该切换仅在 `ANTHROPIC_API_KEY` 在您的环境中设置时出现。在非交互模式（`-p`）下，当密钥存在时始终使用该密钥。
4. [`apiKeyHelper`](/docs/zh-CN/settings-reference#apikeyhelper) 脚本输出。用于动态或轮换凭证，例如从保管库获取的短期令牌。
5. `CLAUDE_CODE_OAUTH_TOKEN` 环境变量。由 [`claude setup-token`](#generate-a-long-lived-token) 生成的长期 OAuth 令牌。用于 CI 管道和脚本，其中浏览器登录不可用。如果您在设置了该变量时运行 `/login`，Claude Code 会将当前会话切换到新登录，但在每个新会话中都会再次读取该变量，直到您从 shell 配置文件或[设置文件](/docs/zh-CN/settings)的 `env` 块中删除它。
6. Anthropic 配置文件和联合凭证，即 `ant` CLI 和 Workload Identity Federation 使用的凭证。`ant auth login` 写入的配置文件仅在您在 `ANTHROPIC_PROFILE` 中命名它时才排在此处；否则它排在 `/login` 下方。请参阅 [Anthropic 配置文件和联合凭证](#anthropic-profiles-and-federation-credentials)。
7. 来自 `/login` 的订阅 OAuth 凭证。这是 Claude Pro、Max、Team 和 Enterprise 用户的默认设置。

一个已签名的 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway) 会话位于此列表之外：它是一个提供商选择，如 Amazon Bedrock 或 Google Cloud 的 Agent Platform，并且它优先于它们。当网关会话存在时，即使设置了 `CLAUDE_CODE_USE_BEDROCK`、`CLAUDE_CODE_USE_VERTEX` 或 `CLAUDE_CODE_USE_FOUNDRY`，CLI 也会使用网关令牌进行身份验证，上面的持有者令牌、API 密钥、`apiKeyHelper` 和配置文件等凭证源不会被使用。

如果您的机器的[托管设置](/docs/zh-CN/managed-settings)将 [`forceLoginMethod`](/docs/zh-CN/settings-reference#forceloginmethod) 设置为 `"gateway"` 或设置 [`forceLoginGatewayUrl`](/docs/zh-CN/settings-reference#forcelogingatewayurl)，并且您没有通过 `CLAUDE_CODE_USE_BEDROCK` 或 `CLAUDE_CODE_USE_VERTEX` 等变量选择云提供商，您的会话仅使用网关登录。Claude Code 跳过其他凭证源并要求您使用 `/login` 登录。有关每个剩余凭证的情况，请参阅[管理员策略需要云网关登录](/docs/zh-CN/errors#administrator-policy-requires-a-cloud-gateway-sign-in)。需要 Claude Code v2.1.261 或更高版本，或在仅设置 `forceLoginGatewayUrl` 的机器上需要 v2.1.265 或更高版本。

如果您有活跃的 Claude 订阅，但环境中也设置了 `ANTHROPIC_API_KEY`，Claude Code 会在您批准后使用 API 密钥。如果密钥属于已禁用或过期的组织，这可能会导致身份验证失败。

运行 `unset ANTHROPIC_API_KEY` 以回退到您的订阅，并检查 `/status` 以确认哪种方法处于活跃状态。当登录和 API 密钥都已配置时，`/status` 会标记未在使用的凭证。

[Cloud sessions](/docs/zh-CN/claude-code-on-the-web) 始终使用您的订阅凭证。如果您在云环境中设置 `ANTHROPIC_API_KEY` 或 `ANTHROPIC_AUTH_TOKEN`，它不会覆盖您的订阅凭证。

<h4 id="anthropic-profiles-and-federation-credentials">
  Anthropic 配置文件和联合凭证
</h4>

配置文件是您的 [Anthropic 配置目录](https://platform.claude.com/docs/en/manage-claude/wif-reference#configuration-directory)中的命名凭证配置文件，在 macOS 和 Linux 上默认为 `~/.config/anthropic`，在 Windows 上为 `%APPDATA%\Anthropic`。当您为 [Workload Identity Federation (WIF)](https://platform.claude.com/docs/en/manage-claude/workload-identity-federation) 设置配置文件时，其身份验证模式为 `oidc_federation`，或当 [`ant auth login`](https://platform.claude.com/docs/en/cli-sdks-libraries/cli/authentication) 写入它或您[在没有 API 密钥的情况下登录到 Console 帐户](#sign-in-without-an-api-key)时为 `user_oauth`。

Claude Code 不在[裸模式](/docs/zh-CN/headless#start-faster-with-bare-mode)、Claude Desktop 或云会话中读取配置文件或联合变量。在这些会话中，`/status` 不显示 `Profile` 行。

Claude Code 按此顺序检查三个源，并在第一个设置的源处停止。该表显示设置每个源的内容以及它相对于您的 `/login` 凭证的排名。

| 源 | 设置者 | 相对于 `/login` 的排名 |
| :- | :- | :- |
| 命名配置文件 | `ANTHROPIC_PROFILE` | 上方，无论配置文件具有什么身份验证模式 |
| 联合变量 | `ANTHROPIC_FEDERATION_RULE_ID` 和 `ANTHROPIC_ORGANIZATION_ID`，两者都设置 | 上方 |
| 活跃配置文件 | 您的配置目录中的 [`active_config` 文件](https://platform.claude.com/docs/en/manage-claude/wif-reference#active-profile)，或名为 `default` 的配置文件 | 当其身份验证模式为 `oidc_federation` 时上方；当其身份验证模式为 `user_oauth` 时在工作的 `/login` 凭证下方 |

对于联合变量，Claude Code 还会在交换您的身份令牌时读取 [WIF 参考](https://platform.claude.com/docs/en/manage-claude/wif-reference#environment-variables)中的其他变量，例如 `ANTHROPIC_IDENTITY_TOKEN_FILE`。对于配置文件格式，请参阅 [WIF 参考](https://platform.claude.com/docs/en/manage-claude/wif-reference#profile-configuration-file)。

要确认 Claude Code 选择了哪个源，请运行 `/status`。`Profile` 行用源名称代替 `Login method` 行。当配置文件是正在使用的凭证时，`Organization` 和 `Email` 行显示其帐户。

当 `user_oauth` 配置文件的登录已过期且 Claude Code 无法续期时，请求会失败，显示 [Anthropic 配置文件登录已过期](/docs/zh-CN/errors#anthropic-profile-login-expired)。

需要您的 claude.ai 登录的功能，例如 [claude.ai 连接器](/docs/zh-CN/mcp#use-mcp-servers-from-claude-ai)和 [`/schedule`](/docs/zh-CN/routines)，在选择这些源之一时不可用。要停止 Claude Code 选择源：

* **命名配置文件或联合变量**：取消设置 `ANTHROPIC_PROFILE`，或取消设置任一联合变量
* **活跃配置文件**：对于通过[在没有 API 密钥的情况下登录到 Console 帐户](#sign-in-without-an-api-key)写入当前凭证的 `user_oauth` 配置文件运行 `/logout`，对于 `ant auth login` 写入当前凭证的配置文件运行 `ant auth logout`，或对于任一身份验证模式从您的配置目录中的 `configs/` 删除配置文件的文件

<h3 id="generate-a-long-lived-token">
  生成长期令牌
</h3>

对于 CI 管道、脚本或其他不可用交互式浏览器登录的环境，使用 `claude setup-token` 生成一年期 OAuth 令牌：

```bash theme={null}
claude setup-token
```

该命令会打开与 `/login` 相同的浏览器授权流程，在您在浏览器中批准访问后，令牌会打印到终端。它不会将令牌保存在任何地方；复制它并将其设置为 `CLAUDE_CODE_OAUTH_TOKEN` 环境变量，无论您想在何处进行身份验证：

<Tabs>
  <Tab title="macOS, Linux, WSL">
    ```bash theme={null}
    export CLAUDE_CODE_OAUTH_TOKEN=your-token
    ```
  </Tab>

  <Tab title="Windows PowerShell">
    ```powershell theme={null}
    $env:CLAUDE_CODE_OAUTH_TOKEN = "your-token"
    ```
  </Tab>

  <Tab title="Windows CMD">
    ```batch theme={null}
    set CLAUDE_CODE_OAUTH_TOKEN=your-token
    ```
  </Tab>
</Tabs>

此令牌使用您的 Claude 订阅进行身份验证，需要 Pro、Max、Team 或 Enterprise 计划。它只能进行模型请求，因此无法建立 [Remote Control](/docs/zh-CN/remote-control) 会话或获取 [claude.ai 连接器](/docs/zh-CN/mcp#use-mcp-servers-from-claude-ai)。您在本地配置的 MCP 服务器仍然有效。

[裸模式](/docs/zh-CN/headless#start-faster-with-bare-mode)不读取 `CLAUDE_CODE_OAUTH_TOKEN`。如果您的脚本传递 `--bare`，请改用 `ANTHROPIC_API_KEY` 或 `apiKeyHelper` 进行身份验证。
