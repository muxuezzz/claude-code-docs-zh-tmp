> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 数据使用

> 了解 Anthropic 对 Claude 数据使用的政策

<h2 id="data-policies">
  数据政策
</h2>

<h3 id="data-training-policy">
  数据训练政策
</h3>

**消费者用户（免费、Pro 和 Max 计划）**：
我们让您可以选择是否允许您的数据用于改进未来的 Claude 模型。当此设置打开时，我们将使用来自免费、Pro 和 Max 账户的数据来训练新模型（包括当您从这些账户使用 Claude Code 时）。

**商业用户**：（Team 和 Enterprise 计划、API、第三方平台和 Claude Gov）维持现有政策：除非客户选择向我们提供数据以改进模型（例如，[开发者合作伙伴计划](https://support.claude.com/en/articles/11174108-about-the-development-partner-program)），否则 Anthropic 不会使用在商业条款下发送到 Claude Code 的代码或提示来训练生成模型。

<h3 id="development-partner-program">
  开发者合作伙伴计划
</h3>

如果您明确选择加入向我们提供材料以进行训练的方法，例如通过[开发者合作伙伴计划](https://support.claude.com/en/articles/11174108-about-the-development-partner-program)，我们可能会使用这些提供的材料来训练我们的模型。组织管理员可以明确选择为其组织加入开发者合作伙伴计划。请注意，此计划仅适用于 Anthropic 第一方 API，不适用于 Amazon Bedrock 或 Google Cloud 的 Agent Platform 用户。

<h3 id="feedback-using-the-/feedback-command">
  使用 `/feedback` 命令的反馈
</h3>

如果您选择使用 `/feedback` 命令向我们发送有关 Claude Code 的反馈，我们可能会使用您的反馈来改进我们的产品和服务。通过 `/feedback` 共享的文稿，或通过 `/bug` 和 `/share` 共享的文稿（这些命令通过相同的路径报告），将保留 5 年。

使用[Claude 起草的反馈](/docs/zh-CN/tools-reference#sendfeedback-tool-behavior)，Claude 还可以起草反馈报告并在您的机器上将其排队供您审查。Claude Code 在您选择发送草稿之前不会发送任何内容，发送的草稿会通过与其他 `/feedback` 报告相同的提交路径和保留期。

<h3 id="session-quality-surveys">
  会话质量调查
</h3>

当您在 Claude Code 中看到"Claude 在此会话中表现如何？"提示时，对此调查的响应（包括选择"关闭"）仅记录您的评分。作为评分提示本身的一部分，我们不收集或存储任何对话文稿、输入、输出或其他会话数据。与竖起大拇指/竖起大拇指向下反馈或 `/feedback` 报告不同，此会话质量调查是一个简单的产品满意度指标。

在评分提示之后，您可能会看到一个单独的后续问题，询问"Anthropic 可以查看您的会话文稿以帮助我们改进 Claude Code 吗？"。这是与评分不同的可选第二步：

* **是**：将您的对话文稿、任何子代理文稿和来自磁盘的原始会话日志文件上传到 Anthropic。已知的 API 密钥和令牌模式在上传前被编辑。源代码、文件内容和其他对话内容按原样上传。共享的文稿保留最多 6 个月。在 Amazon Bedrock、Google Cloud 的 Agent Platform、Microsoft Foundry 和已登录的 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway) 会话上，"是"会将相同的有效负载写入 `~/.claude/feedback-bundles/` 下的本地存档，而不是上传；在您转发该文件之前，没有任何内容离开您的机器。
* **否**：拒绝而不发送任何内容
* **不再询问**：拒绝并停止此后续在未来会话中出现

除非您明确选择**是**，否则不会上传任何内容。具有[零数据保留](/docs/zh-CN/zero-data-retention)的组织，或组织政策禁用产品反馈的组织，或设置了 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 的组织，永远不会看到此后续。您对此调查的响应（包括评分提示后提交的会话文稿）不会影响您的数据训练偏好，也不能用于训练我们的 AI 模型。

要禁用这些调查，请设置 `CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1`。当设置了 `DISABLE_TELEMETRY`、`DO_NOT_TRACK` 或 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 时，调查也会被禁用。通过自己的 [OpenTelemetry 收集器](/docs/zh-CN/monitoring-usage)阻止非必要流量但捕获调查响应的组织可以通过设置 `CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL=1` 来选择重新启用调查。然后调查仅将评分记录到配置的收集器。文稿共享后续和所有其他 Anthropic 绑定的反馈流量保持禁用。要控制频率而不是禁用，请在您的设置文件中将 [`feedbackSurveyRate`](/docs/zh-CN/settings-reference#feedbacksurveyrate) 设置为 `0` 到 `1` 之间的概率。

<h3 id="data-retention">
  数据保留
</h3>

Anthropic 根据您的账户类型和偏好保留 Claude Code 数据。

**消费者用户（免费、Pro 和 Max 计划）**：

* 允许数据用于模型改进的用户：5 年保留期以支持模型开发和安全改进
* 不允许数据用于模型改进的用户：30 天保留期
* 隐私设置可以随时在 [claude.ai/settings/data-privacy-controls](https://claude.ai/settings/data-privacy-controls) 更改。

**商业用户（Team、Enterprise 和 API）**：

* 标准：30 天保留期
* [零数据保留](/docs/zh-CN/zero-data-retention)：适用于 Claude for Enterprise 上 Claude Code 的合格账户。ZDR 不包含在标准 Enterprise 计划中；它由您的账户团队在确认符合条件后按组织启用
* 本地缓存：Claude Code 客户端默认在 `~/.claude/projects/` 下以纯文本形式本地存储会话文稿 30 天，以启用会话恢复。使用 `cleanupPeriodDays` 调整该期间。有关存储的内容以及如何清除的信息，请参阅[应用程序数据](/docs/zh-CN/claude-directory#application-data)。

  在 Claude Desktop 或 Cowork 中启动或最近继续的会话的文稿[默认情况下不受该限制](/docs/zh-CN/claude-directory#cleaned-up-automatically)。

您可以随时删除单个云会话。删除会话会永久删除该会话的事件数据。有关如何删除会话的说明，请参阅[删除会话](/docs/zh-CN/claude-code-on-the-web#delete-sessions)。

在我们的[隐私中心](https://privacy.anthropic.com/)了解有关数据保留实践的更多信息。

有关完整详情，请查看我们的[商业服务条款](https://www.anthropic.com/legal/commercial-terms)（适用于 Team、Enterprise 和 API 用户）或[消费者条款](https://www.anthropic.com/legal/consumer-terms)（适用于免费、Pro 和 Max 用户）和[隐私政策](https://www.anthropic.com/legal/privacy)。

<h2 id="data-access">
  数据访问
</h2>

对于所有第一方用户，您可以了解更多关于为[本地 Claude Code](#local-claude-code-data-flow-and-dependencies) 和[远程 Claude Code](#cloud-execution-data-flow-and-dependencies) 记录的数据。[Remote Control](/docs/zh-CN/remote-control) 会话遵循本地数据流，因为所有执行都发生在您的机器上；连接时，会话记录也存储在 Anthropic 服务器上以在设备间同步对话，如[连接和安全](/docs/zh-CN/remote-control#connection-and-security)中所述。请注意，对于远程 Claude Code，Claude 访问您启动 Claude Code 会话的存储库。Claude 不访问您已连接但未在其中启动会话的存储库。

<h2 id="local-claude-code-data-flow-and-dependencies">
  本地 Claude Code：数据流和依赖关系
</h2>

下面的图表显示了 Claude Code 在安装和正常操作期间如何连接到外部服务。实线表示必需的连接，而虚线表示可选或用户启动的数据流。

<img src="https://mintcdn.com/claude-code/YR4DRZyI3CdsXkiT/images/claude-code-data-flow.svg?fit=max&auto=format&n=YR4DRZyI3CdsXkiT&q=85&s=2846ea92cfc2297b8620c31c82b482ad" className="dark:hidden" alt="显示 Claude Code 外部连接的图表：安装/更新连接到分发服务器，用户请求连接到 Anthropic 的 Console 身份验证和 public-api，可选的遥测流将指标和错误报告发送到 Anthropic 和第三方服务。通过 /feedback 发送的反馈转到 Google Cloud Storage，并可选择创建 GitHub issue" width="720" height="520" data-path="images/claude-code-data-flow.svg" />

<img src="https://mintcdn.com/claude-code/_xqph1dUOslCOwsj/images/claude-code-data-flow-dark.svg?fit=max&auto=format&n=_xqph1dUOslCOwsj&q=85&s=4fb6e8c88a9740845217bf2a2b040877" className="hidden dark:block" alt="显示 Claude Code 外部连接的图表：安装/更新连接到分发服务器，用户请求连接到 Anthropic 的 Console 身份验证和 public-api，可选的遥测流将指标和错误报告发送到 Anthropic 和第三方服务。通过 /feedback 发送的反馈转到 Google Cloud Storage，并可选择创建 GitHub issue" width="720" height="520" data-path="images/claude-code-data-flow-dark.svg" />

Claude Code 在本地运行。为了与 LLM 交互，Claude Code 通过网络发送数据。此数据包括所有用户提示和模型输出，通过 TLS 1.2+ 在传输中加密。Claude Code 与大多数流行的 VPN 和 LLM 代理兼容。

静止时的加密取决于您的模型提供商：

| 提供商 | 静止时加密 |
| - | - |
| Anthropic API | 基础设施级磁盘加密 (AES-256)。启用 [Zero Data Retention](/docs/zh-CN/zero-data-retention) 以实现无服务器端持久化。 |
| Amazon Bedrock | AES-256，使用 AWS 管理的密钥。可通过 AWS KMS 获得客户管理的密钥。 |
| Google Cloud 的 Agent Platform | Google 管理的加密密钥。CMEK 可用。 |
| Microsoft Foundry | 取决于部署的[托管选项](https://platform.claude.com/docs/en/build-with-claude/claude-in-microsoft-foundry#hosting-options)。对于在 Azure 上托管的部署，提示和完成内容保留在 Azure 内；只有使用情况元数据和由 Anthropic 安全系统标记的内容才会流向 Anthropic。对于在 Anthropic 上托管的部署，请求路由到 Anthropic 基础设施，使用 AES-256 磁盘加密。 |

Claude Code 基于 Anthropic 的 API 构建。有关 API 安全控制的详情，包括 API 日志记录程序，请参阅 [Anthropic 信任中心](https://trust.anthropic.com)中的合规工件。

<h3 id="cloud-execution-data-flow-and-dependencies">
  云执行：数据流和依赖关系
</h3>

使用[网络上的 Claude Code](/docs/zh-CN/claude-code-on-the-web)时，会话默认在 Anthropic 管理的虚拟机中运行，而不是在本地运行。您的组织路由到[自托管环境](/docs/zh-CN/self-hosted-environments)的会话在您控制的基础设施上运行；有关哪些内容保留在您的机器上以及哪些内容仍然流向 Anthropic，请参阅[哪些内容保留在您的基础设施上](/docs/zh-CN/self-hosted-environments#what-stays-on-your-infrastructure)。在 Anthropic 托管的云会话中：

* \*\*代码和数据存储：\*\*您的存储库被克隆到隔离的 VM。Anthropic 存储会话记录，以便您稍后可以返回该会话。代码和会话数据受您的账户类型的[数据保留](#data-retention)和使用政策约束
* \*\*凭证：\*\*GitHub 凭证在 Anthropic 的服务器上加密存储，永远不会进入 VM。来自 VM 的 GitHub 流量通过 Anthropic 代理，该代理在服务器端附加凭证
* \*\*网络流量：\*\*所有出站流量都通过安全代理进行审计日志记录和滥用防止
* \*\*会话数据：\*\*提示、代码更改和输出遵循与本地 Claude Code 使用相同的数据政策

有关云执行的安全详情，请参阅[安全](/docs/zh-CN/security#cloud-execution-security)。

<h2 id="telemetry-services">
  遥测服务
</h2>

Claude Code 发送两种操作遥测：使用指标和错误报告。您可以使用下面的环境变量分别关闭每一种，或通过设置 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 一次性禁用所有非必要流量。设置 `DISABLE_TELEMETRY` 或 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 也会禁用 [Remote Control](/docs/zh-CN/remote-control#requirements) 所依赖的功能标志评估；`DISABLE_ERROR_REPORTING` 则不会。

**指标**：延迟、可靠性和使用模式，通过 TLS 发送到 Anthropic 和第三方日志记录基础设施。指标永远不包括您的代码、提示或文件路径。设置 `DISABLE_TELEMETRY=1` 以选择退出。

**错误报告**：来自 Claude Code 自身内部的错误消息和堆栈跟踪，通过 TLS 发送到第三方错误跟踪服务。Claude Code 在任何内容离开您的机器之前会编辑已知的密钥、文件路径、电子邮件地址和其他个人信息的模式。设置 `DISABLE_ERROR_REPORTING=1` 以选择退出。

错误报告仅在以下所有条件都适用时才启用：

* 您使用 Claude Pro 或 Max 订阅登录
* 您运行的是 Claude Code v2.1.198 或更高版本
* 您直接连接到 Claude API
* 您的组织没有零数据保留或 HIPAA 协议

当您运行 `/feedback` 命令时，您的对话历史记录（包括代码）的副本被发送到 Anthropic。`/bug` 和 `/share` 命令通过相同的路径提交。在从反馈对话框提交报告之前，您可以选择包含多少历史记录：仅当前会话（这是默认设置），或者也包括来自同一项目在过去 24 小时或 7 天内的其他会话。Claude Code 通过相同的路径提交 [Claude 起草的反馈](/docs/zh-CN/tools-reference#sendfeedback-tool-behavior)，包括当您在草稿的审查屏幕上选择包含它时的记录。数据通过 TLS 在传输中加密并存储在 Google Cloud Storage 中，Google Cloud Storage 默认对静止数据进行加密。可选地，在公共存储库中创建 GitHub 问题。要选择退出，请将 `DISABLE_FEEDBACK_COMMAND` 环境变量设置为 `1`。

当您使用第三方提供商（如 Amazon Bedrock 或 Google Cloud 的 Agent Platform），或未配置 Anthropic 凭据时，`/feedback` 会将报告写入 `~/.claude/feedback-bundles/` 下的本地存档，而不是将其发送到 Anthropic。已知的 API 密钥和令牌模式在写入存档之前被编辑。在您将该文件发送给您的 Anthropic 账户代表或将其附加到支持请求之前，没有任何内容离开您的机器。

<h2 id="default-behaviors-by-api-provider">
  按 API 提供商的默认行为
</h2>

默认情况下，当使用 Amazon Bedrock、Google Cloud 的 Agent Platform、Microsoft Foundry 或 Claude Platform on AWS 时，错误报告、遥测和错误报告被禁用。会话质量调查和 WebFetch 域安全检查是例外，无论提供商如何都会运行。在已登录的 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway) 会话上，使用分析、错误报告和向 Anthropic 的调查评分由网关凭证本身禁用，没有重新启用的设置。您可以通过设置 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 一次选择退出所有非必需的流量，包括调查。此变量不影响 WebFetch 检查或官方插件市场自动安装；每个都有自己的选择退出选项：[settings](/docs/zh-CN/settings) 中的 `skipWebFetchPreflight` 用于 WebFetch，`CLAUDE_CODE_DISABLE_OFFICIAL_MARKETPLACE_AUTOINSTALL` 用于市场。以下是完整的默认行为：

| 服务 | Claude API | Google Cloud 的 Agent Platform API | Amazon Bedrock API | Microsoft Foundry API | Claude Platform on AWS |
| - | - | - | - | - | - |
| **Metrics** | 默认开启。<br />`DISABLE_TELEMETRY=1` 禁用。 | 默认关闭。<br />`CLAUDE_CODE_USE_VERTEX` 必须为 1。 | 默认关闭。<br />`CLAUDE_CODE_USE_BEDROCK` 必须为 1。 | 默认关闭。<br />`CLAUDE_CODE_USE_FOUNDRY` 必须为 1。 | 默认关闭。<br />`CLAUDE_CODE_USE_ANTHROPIC_AWS` 必须为 1。 |
| **Error reports** | v2.1.198+ 上 Pro 和 Max 登录默认开启，否则关闭。<br />`DISABLE_ERROR_REPORTING=1` 禁用。 | 默认关闭。<br />`CLAUDE_CODE_USE_VERTEX` 必须为 1。 | 默认关闭。<br />`CLAUDE_CODE_USE_BEDROCK` 必须为 1。 | 默认关闭。<br />`CLAUDE_CODE_USE_FOUNDRY` 必须为 1。 | 默认关闭。<br />`CLAUDE_CODE_USE_ANTHROPIC_AWS` 必须为 1。 |
| **Claude API（`/feedback` 报告）** | 默认开启。<br />`DISABLE_FEEDBACK_COMMAND=1` 禁用。 | 默认关闭。<br />`CLAUDE_CODE_USE_VERTEX` 必须为 1。 | 默认关闭。<br />`CLAUDE_CODE_USE_BEDROCK` 必须为 1。 | 默认关闭。<br />`CLAUDE_CODE_USE_FOUNDRY` 必须为 1。 | 默认关闭。<br />`CLAUDE_CODE_USE_ANTHROPIC_AWS` 必须为 1。 |
| **会话质量调查** | 默认开启。<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` 禁用。 | 默认开启。<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` 禁用。 | 默认开启。<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` 禁用。 | 默认开启。<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` 禁用。 | 默认开启。<br />`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY=1` 禁用。 |
| **WebFetch 域安全检查** | 默认开启。<br />[settings](/docs/zh-CN/settings) 中 `skipWebFetchPreflight: true` 禁用。 | 默认开启。<br />[settings](/docs/zh-CN/settings) 中 `skipWebFetchPreflight: true` 禁用。 | 默认开启。<br />[settings](/docs/zh-CN/settings) 中 `skipWebFetchPreflight: true` 禁用。 | 默认开启。<br />[settings](/docs/zh-CN/settings) 中 `skipWebFetchPreflight: true` 禁用。 | 默认开启。<br />[settings](/docs/zh-CN/settings) 中 `skipWebFetchPreflight: true` 禁用。 |

所有环境变量都可以检查到 `settings.json`（请参阅 [settings 参考](/docs/zh-CN/settings-reference)）。

当主机平台设置 `CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST` 时，Google Cloud 的 Agent Platform、Amazon Bedrock、Microsoft Foundry 和 Claude Platform on AWS 的指标默认开启，并遵循标准的 `DISABLE_TELEMETRY` 选择退出。错误报告和 `/feedback` 报告在这些提供商上仍然默认关闭。

<h3 id="webfetch-domain-safety-check">
  WebFetch 域安全检查
</h3>

在获取 URL 之前，WebFetch 工具将请求的主机名发送到 `api.anthropic.com` 以根据 Anthropic 维护的安全阻止列表进行检查。仅发送主机名，不发送完整 URL、路径或页面内容。Claude Code 将通过检查的主机名缓存五分钟，并在下一个请求时重新检查被阻止或失败的主机名。

无论您使用哪个模型提供商，此检查都会运行，不受 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC` 影响。如果您的网络阻止 `api.anthropic.com`，WebFetch 请求将失败，直到您允许列表该域或在 [settings](/docs/zh-CN/settings) 中设置 `skipWebFetchPreflight: true`。禁用检查意味着 WebFetch 尝试检索任何 URL 而不咨询阻止列表，因此如果您需要限制 Claude 可以访问的域，请将其与 [`WebFetch` 权限规则](/docs/zh-CN/permissions#webfetch) 结合使用。
