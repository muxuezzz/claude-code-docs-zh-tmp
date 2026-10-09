> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 零数据保留

> 了解 Claude Code 的零数据保留 (ZDR)，适用于 Claude for Enterprise 上符合条件的账户，包括范围、禁用功能以及如何请求启用。

Claude Code 的零数据保留 (ZDR) 适用于 Claude for Enterprise 上符合条件的账户。启用 ZDR 后，Claude Code 会话期间生成的提示词和模型响应会实时处理，在返回响应后不会由 Anthropic 存储，除非需要遵守法律或防止滥用。

<Note>
  ZDR 不包含在标准 Claude for Enterprise 计划中，也无法从您的管理员设置中启用。它仅适用于符合条件的账户，需要由 Anthropic 单独启用。如果您的组织需要 ZDR，请[联系销售](https://www.anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=zero_data_retention_request)或您的 Anthropic 账户团队以确认资格。
</Note>

已启用 HIPAA 的 Claude for Enterprise 组织，在将 HIPAA 配置应用于 Claude Code（本地模式）和 Cowork（本地模式）后，无需 ZDR 即可将 Claude Code CLI 和 Claude Desktop 中的 Code 标签页纳入其业务伙伴协议 (BAA) 的覆盖范围。请参阅[为符合 HIPAA 要求的组织设置 Claude Code（本地模式）](/docs/zh-CN/hipaa-setup)。未应用 HIPAA 配置的组织仍需要 ZDR 才能使 Claude Code 获得 BAA 覆盖。有关合格服务的列表，请参阅[实施指南](https://trust.anthropic.com/resources?s=l1wrssd9hsbi4gak0tp5a6\&name=%5Banthropic%5D-hipaa-ready-offering-implementation-guide)。

Claude for Enterprise 上的 ZDR 为企业客户提供了使用 Claude Code 并实现零数据保留的能力，同时可以访问管理功能：

* 按用户的成本控制
* [分析](/docs/zh-CN/analytics)仪表板
* [服务器管理的设置](/docs/zh-CN/server-managed-settings)
* 审计日志

Claude for Enterprise 上 Claude Code 的 ZDR 仅适用于 Anthropic 的直接平台。对于在 Amazon Bedrock、Google Cloud 的 Agent Platform 或 Microsoft Foundry 上的 Claude 部署，请参考这些平台的数据保留政策。

<h2 id="zdr-scope">
  ZDR 范围
</h2>

ZDR 涵盖 Claude for Enterprise 上的 Claude Code 推理。

<Warning>
  ZDR 在每个组织的基础上启用。每个新组织都需要由您的 Anthropic 账户团队单独启用 ZDR。ZDR 不会自动应用于在同一账户下创建的新组织。请联系您的账户团队为任何新组织启用 ZDR。
</Warning>

<h3 id="route-claude-code-traffic-to-your-zdr-organization">
  将 Claude Code 流量路由到您的 ZDR 组织
</h3>

ZDR 适用于向启用了 ZDR 的组织进行身份验证的请求。如果开发人员使用个人账户或来自不同组织的 API 密钥登录 Claude Code，这些会话不受保护。要求开发人员的 claude.ai 登录属于您的 ZDR 组织，请部署 `forceLoginMethod` 和 `forceLoginOrgUUID` 托管设置；请参阅[限制登录到您的组织](/docs/zh-CN/authentication#restrict-login-to-your-organization)，其中也解释了这些密钥如何处理 Claude Console 登录。

<h3 id="what-zdr-covers">
  ZDR 涵盖的内容
</h3>

ZDR 涵盖通过 Claude for Enterprise 上的 Claude Code 进行的模型推理调用。当您在终端中使用 Claude Code 时，您发送的提示和 Claude 生成的响应不会由 Anthropic 保留。这适用于 ZDR 组织可用的每个模型。某些模型默认需要数据保留；请参阅 [ZDR 下的模型可用性](#model-availability-under-zdr)。

<h3 id="what-zdr-does-not-cover">
  ZDR 不涵盖的内容
</h3>

ZDR 不适用于以下内容，即使对于启用了 ZDR 的组织也是如此。这些功能遵循[标准数据保留政策](/docs/zh-CN/data-usage#data-retention)：

| 功能 | 详情 |
| - | - |
| claude.ai 上的聊天 | 通过 Claude for Enterprise 网络界面的聊天对话不受 ZDR 保护。 |
| Cowork | Cowork 会话不受 ZDR 保护。 |
| Claude Code 分析 | 不存储提示或模型响应，但收集生产力元数据，如账户电子邮件和使用统计。对于 ZDR 组织，贡献指标不可用；[分析仪表板](/docs/zh-CN/analytics)仅显示使用指标。 |
| 用户和席位管理 | 管理数据，如账户电子邮件和席位分配，根据标准政策保留。 |
| 第三方集成 | 由第三方工具、MCP servers 或其他外部集成处理的数据不受 ZDR 保护。请独立审查这些服务的数据处理实践。 |

<h2 id="features-disabled-under-zdr">
  ZDR 下禁用的功能
</h2>

当为 Claude for Enterprise 上的 Claude Code 组织启用 ZDR 时，某些需要存储提示或完成的功能会在后端级别自动禁用：

| 功能 | 原因 |
| - | - |
| [网络上的 Claude Code](/docs/zh-CN/claude-code-on-the-web)，包括从 [Desktop 应用](/docs/zh-CN/desktop#cloud-sessions)启动的应用 | 需要服务器端存储会话数据，包括包含提示和完成的对话历史。 |
| [Claude Tag](https://claude.com/docs/claude-tag) | 保留频道内存和会话记录。 |
| [Artifacts](/docs/zh-CN/artifacts) | 需要在 Anthropic 运营的基础设施上存储已发布的页面内容。 |
| 反馈提交（`/feedback`、`/bug`、`/share`） | 提交反馈会将对话数据发送给 Anthropic。 |
| [Remote Control](/docs/zh-CN/remote-control) | 在 Anthropic 服务器上存储会话记录以跨设备同步对话。 |

这些功能在后端被阻止，无论客户端显示如何。如果您在启动期间在 Claude Code 终端中看到禁用的功能，尝试使用它会返回一个错误，指示组织的政策不允许该操作。

如果未来的功能需要存储提示或完成，它们也可能被禁用。

<h3 id="model-availability-under-zdr">
  ZDR 下的模型可用性
</h3>

Claude Fable 5.1 和 Fable 5 是[覆盖模型](https://support.claude.com/en/articles/15425695-covered-models)，[默认需要数据保留](https://platform.claude.com/docs/en/manage-claude/api-and-data-retention#model-specific-data-retention-requirements)，ZDR 组织或工作区是否可以使用它们由覆盖模型政策而非 Claude Code 管理。如果您的组织无法使用它们，这些模型要么在 `/model` 选择器中不存在，要么显示为禁用，服务器无论客户端配置如何都会拒绝对其的请求。

其他模型在 ZDR 下仍然可用。Fable 模型不是默认模型，`best` 别名在可用的地方解析为最新的 Fable 模型，在不可用的地方解析为 Opus。

<h2 id="data-retention-for-policy-violations">
  政策违规的数据保留
</h2>

即使启用了 ZDR，Anthropic 也可能在法律要求或解决使用政策违规时保留数据。如果会话因政策违规而被标记，Anthropic 可能会保留相关的输入和输出长达 2 年，与 Anthropic 的标准 ZDR 政策一致。

<h2 id="request-zdr">
  请求 ZDR
</h2>

要为 Claude for Enterprise 上的 Claude Code 请求 ZDR，请[联系销售](https://www.anthropic.com/contact-sales?utm_source=claude_code\&utm_medium=docs\&utm_content=zero_data_retention_request)或您的 Anthropic 账户团队。您的账户团队将在内部提交请求，Anthropic 将在确认符合条件后在您的组织上审查并启用 ZDR。所有启用操作都会被审计记录。

如果您当前通过按使用量付费的 API 密钥使用 Claude Code 的 ZDR，您可以过渡到 Claude for Enterprise 以获得对管理功能的访问权限，同时为 Claude Code 保持 ZDR。请联系您的账户团队以协调迁移。
