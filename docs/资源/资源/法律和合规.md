> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 法律和合规

> Claude Code 的法律协议、合规认证和安全信息。

<h2 id="legal-agreements">
  法律协议
</h2>

<h3 id="license">
  许可证
</h3>

您对 Claude Code 的使用受以下条款约束：

* [商业条款](https://www.anthropic.com/legal/commercial-terms) - 适用于 Team、Enterprise 和 Claude API 用户
* [消费者服务条款](https://www.anthropic.com/legal/consumer-terms) - 适用于 Free、Pro 和 Max 用户

<h3 id="commercial-agreements">
  商业协议
</h3>

无论您是直接使用 Claude API（1P）还是通过 Amazon Bedrock 或 Google Cloud 的 Agent Platform（3P）访问，您现有的商业协议将适用于 Claude Code 的使用，除非我们已相互同意另行安排。

<h3 id="can-customers-offer-claude-code-in-their-products">
  客户可以在其产品中提供 Claude Code 吗？
</h3>

除非我们已相互同意另行安排，否则在您的产品或服务中预安装或运行 Claude Code（例如在托管沙箱或其他代理基础设施中）需要同意我们的[商业条款](https://www.anthropic.com/legal/commercial-terms)并遵守以下条件：

* **Claude Code 二进制文件不得被修改。** Claude Code 必须按照 Anthropic 发布的方式安装和运行，客户不得删除、禁用或限制其中内置的任何身份验证方法（包括允许使用 Claude 账户或用户自己的 API 密钥登录的方法）。
* **客户不得代表其最终用户支付、转售或中介 Claude 使用。** 每个最终用户必须使用自己的 Anthropic API 密钥、Claude 订阅计划凭证或第三方推理提供商凭证（Amazon Bedrock、Google Cloud 的 Agent Platform、Microsoft Foundry）进行身份验证。该使用情况直接按照最终用户与 Anthropic 的协议或与适用提供商的协议向最终用户计费。

**使用 Claude Code 名称和徽标。** 您可以用纯文本准确地说您的产品预安装了 Claude Code 或它运行 Claude Code。但您不能将 Claude Code 或 Anthropic 名称或徽标用作您自己的产品、功能或公司名称的一部分，在您自己的徽标中，或以任何暗示 Anthropic 构建、认可或与您的产品合作的方式使用。Anthropic 名称或徽标的任何其他使用受我们的[商标指南](https://www.anthropic.com/legal/trademark-guidelines)管制，需要我们的书面许可。

Claude Code 仍然受 Anthropic 的标准条款管制（请参阅上面的许可证和商业协议部分），无论通过哪个平台访问。

<h2 id="compliance">
  合规
</h2>

<h3 id="healthcare-compliance-baa">
  医疗保健合规（BAA）
</h3>

如果客户与 Anthropic 签订了业务关联协议（BAA），并为相关组织启用了[零数据保留（ZDR）](/docs/zh-CN/zero-data-retention)，该 BAA 将扩展到客户通过 Claude Code 的 API 流量。

<h2 id="usage-policy">
  使用政策
</h2>

<h3 id="acceptable-use">
  可接受的使用
</h3>

Claude Code 的使用受 [Anthropic 使用政策](https://www.anthropic.com/legal/aup) 约束。Pro 和 Max 计划的公布使用限制假设 Claude Code 和 Agent SDK 的普通个人使用。

<h3 id="authentication-and-credential-use">
  身份验证和凭证使用
</h3>

Claude Code 使用 OAuth 令牌或 API 密钥与 Anthropic 的服务器进行身份验证。这些身份验证方法有不同的用途：

* **OAuth 身份验证**仅供 Claude Free、Pro、Max、Team 和 Enterprise 订阅计划的购买者使用，旨在支持 Claude Code 和其他原生 Anthropic 应用程序的普通使用。有关登录步骤，请参阅 [登录您的 Claude 账户](https://support.claude.com/en/articles/13189465-logging-in-to-your-claude-account)；有关 Claude Code 如何执行 OAuth 身份验证，请参阅 [身份验证](/docs/zh-CN/authentication)。
* **开发者**构建与 Claude 功能交互的产品或服务，包括使用 [Agent SDK](/docs/zh-CN/agent-sdk/overview) 的产品或服务，应通过 [Claude Console](https://platform.claude.com/) 或受支持的云提供商使用 API 密钥身份验证。Anthropic 不允许第三方开发者提供 Claude.ai 登录到他们自己的应用程序，或代表其用户通过 Free、Pro 或 Max 计划凭证路由请求。此外，开发者不得收集、存储或中介 Claude.ai 凭证或会话令牌 — 登录到 Claude 账户必须通过 Anthropic 自己的流程完成。

这不限制客户如何配置和管理他们自己的 API 密钥或第三方推理提供商凭证 — 例如，在开发环境、密钥管理器或机器镜像中配置 API 密钥供客户自己的授权用户使用 — 前提是所产生的使用按照密钥所有者与 Anthropic（或适用提供商）的协议进行计费，并且不被转售或按上述方式中介。它也不妨碍最终用户使用他们自己的 Claude 订阅登录到未修改的 Claude Code 二进制文件，包括平台按照上述\*客户可以在他们的产品中提供 Claude Code 吗？\*部分所述方式托管 Claude Code 的情况。

Anthropic 保留采取措施执行这些限制的权利，并可能在不事先通知的情况下这样做。

如果您对您的使用案例的允许身份验证方法有疑问，请 [联系销售](https://www.anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=legal_compliance_contact_sales)。

<h2 id="security-and-trust">
  安全和信任
</h2>

<h3 id="trust-and-safety">
  信任和安全
</h3>

您可以在 [Anthropic 信任中心](https://trust.anthropic.com) 和 [透明度中心](https://www.anthropic.com/transparency) 中找到更多信息。

<h3 id="security-vulnerability-reporting">
  安全漏洞报告
</h3>

Anthropic 通过 HackerOne 管理我们的安全计划。[使用此表单报告漏洞](https://hackerone.com/4f1f16ba-10d3-4d09-9ecc-c721aad90f24/embedded_submissions/new)。

***

© Anthropic PBC。版权所有。使用受适用的 Anthropic 服务条款约束。
