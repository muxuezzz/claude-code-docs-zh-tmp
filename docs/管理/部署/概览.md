> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 企业部署概览

> 了解 Claude Code 如何与各种第三方服务和基础设施集成，以满足企业部署需求。

export const ContactSalesCard = ({surface}) => {
  const utm = content => `utm_source=claude_code&utm_medium=docs&utm_content=${surface}_${content}`;
  const iconArrowRight = (size = 13) => <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <line x1="5" y1="12" x2="19" y2="12" />
      <polyline points="12 5 19 12 12 19" />
    </svg>;
  const STYLES = `
.cc-cs {
  --cs-slate: #141413;
  --cs-clay: #d97757;
  --cs-clay-deep: #c6613f;
  --cs-gray-000: #ffffff;
  --cs-gray-700: #3d3d3a;
  --cs-border-default: rgba(31, 30, 29, 0.15);
  font-family: inherit;
}
.dark .cc-cs {
  --cs-slate: #f0eee6;
  --cs-gray-000: #262624;
  --cs-gray-700: #bfbdb4;
  --cs-border-default: rgba(240, 238, 230, 0.14);
}
.cc-cs-card {
  display: flex; align-items: center; justify-content: space-between;
  gap: 16px; padding: 14px 16px; margin: 0;
  background: var(--cs-gray-000); border: 0.5px solid var(--cs-border-default);
  border-radius: 8px; flex-wrap: wrap;
}
.cc-cs-text { font-size: 13px; color: var(--cs-gray-700); line-height: 1.5; flex: 1; min-width: 240px; }
.cc-cs-text strong { font-weight: 550; color: var(--cs-slate); }
.cc-cs-actions { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.cc-cs-btn-clay {
  display: inline-flex; align-items: center; gap: 8px;
  background: var(--cs-clay-deep); color: #fff; border: none;
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
  transition: background-color 0.15s; white-space: nowrap;
}
.cc-cs-btn-clay:hover { background: var(--cs-clay); }
.cc-cs-btn-ghost {
  display: inline-flex; align-items: center; gap: 8px;
  background: transparent; color: var(--cs-gray-700);
  border: 0.5px solid var(--cs-border-default);
  border-radius: 8px; padding: 8px 14px;
  font-size: 13px; font-weight: 500;
}
.cc-cs-btn-ghost:hover { background: rgba(0, 0, 0, 0.04); }
.dark .cc-cs-btn-ghost:hover { background: rgba(255, 255, 255, 0.04); }
@media (max-width: 720px) {
  .cc-cs-actions { width: 100%; }
}
`;
  return <div className="cc-cs not-prose">
      <style>{STYLES}</style>
      <div className="cc-cs-card">
        <div className="cc-cs-text">
          <strong>Deploying Claude Code across your organization?</strong> Talk to sales about enterprise plans, SSO, and centralized billing.
        </div>
        <div className="cc-cs-actions">
          <a href={`https://claude.com/pricing?${utm('view_plans')}#plans-business`} className="cc-cs-btn-ghost">
            View plans
          </a>
          <a href={`https://claude.com/contact-sales?${utm('contact_sales')}`} className="cc-cs-btn-clay">
            Contact sales {iconArrowRight()}
          </a>
        </div>
      </div>
    </div>;
};

组织可以直接通过 Anthropic 或通过云提供商部署 Claude Code。本页面帮助您选择正确的配置。

<ContactSalesCard surface="third_party_overview" />

<h2 id="compare-deployment-options">
  比较部署选项
</h2>

对于大多数组织，Claude for Teams 或 Claude for Enterprise 提供最佳体验。团队成员可以通过单一订阅访问 Claude Code 和网页版 Claude，具有集中计费和无需基础设施设置的优势。

**Claude for Teams** 是自助服务，包括协作功能、管理工具、SSO、计费管理和[服务器管理的设置](/docs/zh-CN/server-managed-settings)，用于组织范围内的 Claude Code 配置。最适合需要快速启动的小型团队。

**Claude for Enterprise** 增加了域名捕获、基于角色的权限和合规性 API 访问。最适合具有安全和合规性要求的大型组织。

了解更多关于 [Team 计划](https://support.claude.com/en/articles/9266767-what-is-the-team-plan) 和 [Enterprise 计划](https://support.claude.com/en/articles/9797531-what-is-the-enterprise-plan)。

下面比较的部署选项涵盖模型推理运行的位置。要在您的组织运营的计算上运行 [Claude Code 网页版](/docs/zh-CN/claude-code-on-the-web) 会话，请参阅 [自托管环境](/docs/zh-CN/self-hosted-environments)。

如果您的组织有特定的基础设施要求，请比较以下选项：

<table>
  <thead>
    <tr>
      <th>功能</th>
      <th>Claude for Teams/Enterprise</th>
      <th>Anthropic Console</th>
      <th>Amazon Bedrock</th>
      <th>Claude Platform on AWS</th>
      <th>Google Cloud's Agent Platform，原名 Vertex AI</th>
      <th>Microsoft Foundry</th>
    </tr>
  </thead>

  <tbody>
    <tr>
      <td>最适合</td>
      <td>大多数组织（推荐）</td>
      <td>个人开发者</td>
      <td>AWS 原生部署</td>
      <td>AWS Marketplace 计费与 Claude API 功能</td>
      <td>GCP 原生部署</td>
      <td>Azure 原生部署</td>
    </tr>

    <tr>
      <td>计费</td>
      <td><strong>Teams：</strong> 按座位订阅，提供按使用量付费选项，请参阅<a href="https://claude.com/pricing?utm_source=claude_code&utm_medium=docs&utm_content=third_party_pricing#team-&-enterprise">定价</a><br /><strong>Enterprise：</strong> <a href="https://claude.com/contact-sales?utm_source=claude_code&utm_medium=docs&utm_content=third_party_enterprise">联系销售</a></td>
      <td>按使用量付费</td>
      <td>通过 AWS 按使用量付费</td>
      <td>通过 AWS Marketplace 按使用量付费</td>
      <td>通过 GCP 按使用量付费</td>
      <td>通过 Azure 按使用量付费</td>
    </tr>

    <tr>
      <td>地区</td>
      <td>支持的[国家/地区](https://www.anthropic.com/supported-countries)</td>
      <td>支持的[国家/地区](https://www.anthropic.com/supported-countries)</td>
      <td>多个 AWS [地区](https://docs.aws.amazon.com/bedrock/latest/userguide/models-regions.html)</td>
      <td>多个 AWS 地区</td>
      <td>多个 GCP [地区](https://cloud.google.com/vertex-ai/generative-ai/docs/learn/locations)</td>
      <td>多个 Azure [地区](https://azure.microsoft.com/en-us/explore/global-infrastructure/products-by-region/)</td>
    </tr>

    <tr>
      <td>Prompt caching</td>
      <td>默认启用</td>
      <td>默认启用</td>
      <td>默认启用</td>
      <td>默认启用</td>
      <td>默认启用</td>
      <td>默认启用</td>
    </tr>

    <tr>
      <td>身份验证</td>
      <td>claude.ai SSO 或电子邮件</td>
      <td>API 密钥或 [Console 无密钥登录](/docs/zh-CN/authentication#sign-in-without-an-api-key)</td>
      <td>API 密钥或 AWS 凭证</td>
      <td>API 密钥或 AWS 凭证</td>
      <td>GCP 凭证</td>
      <td>API 密钥或 Microsoft Entra ID</td>
    </tr>

    <tr>
      <td>成本跟踪</td>
      <td>使用情况仪表板</td>
      <td>使用情况仪表板</td>
      <td>AWS Cost Explorer</td>
      <td>AWS Cost Explorer</td>
      <td>GCP Billing</td>
      <td>Azure Cost Management</td>
    </tr>

    <tr>
      <td>包括网页版 Claude</td>
      <td>是</td>
      <td>否</td>
      <td>否</td>
      <td>否</td>
      <td>否</td>
      <td>否</td>
    </tr>

    <tr>
      <td>企业功能</td>
      <td>团队管理、SSO、使用情况监控</td>
      <td>无</td>
      <td>IAM 策略、CloudTrail</td>
      <td>IAM 策略、CloudTrail</td>
      <td>IAM 角色、Cloud Audit Logs</td>
      <td>RBAC 策略、Azure Monitor</td>
    </tr>
  </tbody>
</table>

有关每个选项上可用功能的逐项细分，请参阅[功能可用性](/docs/zh-CN/feature-availability)。

选择部署选项以查看设置说明：

* [Claude for Teams 或 Enterprise](/docs/zh-CN/authentication#claude-for-teams-or-enterprise)
* [Anthropic Console](/docs/zh-CN/authentication#claude-console-authentication)
* [Claude 应用网关](/docs/zh-CN/claude-apps-gateway)，一个自托管网关，在 Amazon Bedrock、Claude Platform on AWS、Google Cloud's Agent Platform、Microsoft Foundry 或 Anthropic API 前面添加 IdP 登录
* [Amazon Bedrock](/docs/zh-CN/amazon-bedrock)
* [Claude Platform on AWS](/docs/zh-CN/claude-platform-on-aws)
* [Google Cloud's Agent Platform](/docs/zh-CN/google-vertex-ai)
* [Microsoft Foundry](/docs/zh-CN/microsoft-foundry)

对于 Amazon Bedrock 和 Google Vertex AI，您也可以运行 `claude` 并在登录提示处选择 **3rd-party platform** 来启动交互式设置向导。

<h2 id="configure-proxies-and-gateways">
  配置代理和网关
</h2>

大多数组织可以直接使用云提供商，无需额外配置。但是，如果您的组织有特定的网络或管理要求，您可能需要配置企业代理或 LLM 网关。这些是可以一起使用的不同配置：

* **企业代理**：通过 HTTP/HTTPS 代理路由流量。如果您的组织要求所有出站流量通过代理服务器以进行安全监控、合规性或网络策略执行，请使用此选项。使用 `HTTPS_PROXY` 或 `HTTP_PROXY` 环境变量进行配置。在[企业网络配置](/docs/zh-CN/network-config)中了解更多。
* **LLM 网关**：位于 Claude Code 和云提供商之间的服务，用于处理身份验证和路由。如果您需要跨团队的集中使用情况跟踪、自定义速率限制或预算或集中身份验证管理，请使用此选项。使用 `ANTHROPIC_BASE_URL`、`ANTHROPIC_BEDROCK_BASE_URL`、`ANTHROPIC_AWS_BASE_URL`、`ANTHROPIC_VERTEX_BASE_URL` 或 `ANTHROPIC_FOUNDRY_BASE_URL` 环境变量进行配置。在[LLM 网关](/docs/zh-CN/llm-gateway)中了解更多。

有关通过 LLM 网关路由 Amazon Bedrock、Microsoft Foundry 或 Google Cloud's Agent Platform 的按提供商环境变量，请参阅[通过网关路由到云提供商](/docs/zh-CN/llm-gateway-connect#route-to-a-cloud-provider-through-a-gateway)。在 Claude Code 中运行 `/status` 以验证会话正在使用哪个提供商、基础 URL 和代理。

如果您的组织使用[客户管理的加密密钥](https://platform.claude.com/docs/en/manage-claude/cmek)（CMEK）并通过 LLM 网关或自定义 `ANTHROPIC_BASE_URL` 路由 Claude Code，CMEK 不适用于这些会话上 Claude Code 的操作遥测。要为每个开发人员关闭遥测，请通过托管设置传递 `DISABLE_TELEMETRY`，如[为您的组织关闭遥测](/docs/zh-CN/managed-settings#turn-telemetry-off-for-your-organization)中所示。

<h2 id="best-practices-for-organizations">
  组织的最佳实践
</h2>

<h3 id="invest-in-documentation-and-memory">
  投资文档和内存
</h3>

我们强烈建议投资文档，以便 Claude Code 理解您的代码库。组织可以在多个级别部署 CLAUDE.md 文件。请参阅[CLAUDE.md 文件可以存放的位置](/docs/zh-CN/memory#choose-where-to-put-claude-md-files)和[如何部署组织范围的 CLAUDE.md](/docs/zh-CN/memory#deploy-organization-wide-claude-md)。

<h3 id="simplify-deployment">
  简化部署
</h3>

如果您有自定义开发环境，我们发现创建一种"一键"安装 Claude Code 的方式是在组织中增加采用率的关键。

<h3 id="start-with-guided-usage">
  从引导式使用开始
</h3>

鼓励新用户尝试使用 Claude Code 进行代码库问答，或在较小的错误修复或功能请求上使用。要求 Claude Code 制定计划。检查 Claude 的建议，如果偏离轨道，请提供反馈。随着时间的推移，当用户更好地理解这种新范式时，他们将更有效地让 Claude Code 更自主地运行。

<h3 id="pin-model-versions-for-cloud-providers">
  为云提供商固定模型版本
</h3>

如果您通过 [Amazon Bedrock](/docs/zh-CN/amazon-bedrock)、[Google Cloud 的 Agent Platform](/docs/zh-CN/google-vertex-ai)、[Microsoft Foundry](/docs/zh-CN/microsoft-foundry) 或 [Claude Platform on AWS](/docs/zh-CN/claude-platform-on-aws) 部署，请使用 `ANTHROPIC_DEFAULT_FABLE_MODEL`、`ANTHROPIC_DEFAULT_OPUS_MODEL`、`ANTHROPIC_DEFAULT_SONNET_MODEL` 和 `ANTHROPIC_DEFAULT_HAIKU_MODEL` 固定特定模型版本。如果不固定，模型别名会解析为 Claude Code 为该提供商内置的默认值，这可能滞后于最新版本，并且可能尚未在您的账户中启用。固定让您可以控制用户何时迁移到新模型。有关每个提供商在默认值不可用时的行为，请参阅[模型配置](/docs/zh-CN/model-config#pin-models-for-third-party-deployments)。

<h3 id="configure-security-policies">
  配置安全策略
</h3>

安全团队可以配置托管权限，定义 Claude Code 允许和不允许做什么，这不能被本地配置覆盖。[了解更多](/docs/zh-CN/security)。

要限制托管机器可以使用的这些部署选项，请在托管设置中设置 [`allowedProviders`](/docs/zh-CN/settings-reference#allowedproviders)。例如，`["bedrock"]` 仅允许 Amazon Bedrock；同时启用 Mantle 端点的 Bedrock 队列也列出 `"mantle"`。该条目说明哪些端点变量还需要托管 `env` 固定。需要 Claude Code v2.1.285 或更高版本。

<h3 id="leverage-mcp-for-integrations">
  利用 MCP 进行集成
</h3>

MCP 是为 Claude Code 提供更多信息的好方法，例如连接到票证管理系统或错误日志。我们建议一个中央团队配置 MCP servers 并将 `.mcp.json` 配置检入代码库，以便所有用户受益。[了解更多](/docs/zh-CN/mcp)。

<h2 id="next-steps">
  后续步骤
</h2>

选择部署选项并为您的团队配置访问权限后：

1. **向您的团队推出**：分享安装说明，让团队成员[安装 Claude Code](/docs/zh-CN/setup) 并使用其凭证进行身份验证。
2. **设置共享配置**：在您的存储库中创建 [CLAUDE.md 文件](/docs/zh-CN/memory)，以帮助 Claude Code 理解您的代码库和编码标准。
3. **配置权限**：查看[安全设置](/docs/zh-CN/security)以定义 Claude Code 在您的环境中可以和不能做什么。
