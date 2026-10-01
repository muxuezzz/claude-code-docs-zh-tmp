> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 监控

> 了解如何为 Claude Code 启用和配置 OpenTelemetry。

通过 OpenTelemetry (OTel) 导出遥测数据，跨组织跟踪 Claude Code 使用情况、成本和工具活动。Claude Code 通过标准指标协议导出指标作为时间序列数据，通过日志/事件协议导出事件，以及可选地通过 [traces 协议](#traces-beta) 导出分布式跟踪。

<h2 id="quick-start">
  快速开始
</h2>

使用环境变量配置 OpenTelemetry：

```bash theme={null}
# 1. 启用遥测
export CLAUDE_CODE_ENABLE_TELEMETRY=1

# 2. 选择导出器（两者都是可选的 - 仅配置您需要的）
export OTEL_METRICS_EXPORTER=otlp       # 选项：otlp、prometheus、console、none
export OTEL_LOGS_EXPORTER=otlp          # 选项：otlp、console、none

# 3. 配置 OTLP 端点（用于 OTLP 导出器）
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317

# 4. 设置身份验证（如果需要）
export OTEL_EXPORTER_OTLP_HEADERS="Authorization=Bearer your-token"

# 5. 用于调试：减少导出间隔，并为生产使用重置它们
export OTEL_METRIC_EXPORT_INTERVAL=10000  # 10 秒（默认：60000ms）
export OTEL_LOGS_EXPORT_INTERVAL=5000     # 5 秒（默认：5000ms）

# 6. 运行 Claude Code
claude
```

要验证导出指标的设置，请检查您的后端是否有 `claude_code.session.count` 指标，Claude Code 在会话启动时会发出该指标。要验证仅日志的设置，请提交提示并检查 `claude_code.user_prompt` 事件。

如果没有任何内容到达，请使用 `claude --debug-file <path>` 启动 Claude Code 并检查它写入该路径的日志。Claude Code 将您配置的导出器的失败报告为 `[3P telemetry]` 错误，其中 3P 表示第三方。以 `[Anthropic telemetry]` 为前缀的行描述 [Anthropic 的单独操作遥测](/docs/zh-CN/data-usage#telemetry-services)，不表示您的设置存在问题。

有关完整配置选项，请参阅 [OpenTelemetry 规范](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/protocol/exporter.md#configuration-options)。

<h2 id="administrator-configuration">
  管理员配置
</h2>

管理员可以通过 [托管设置文件](/docs/zh-CN/managed-settings#delivery-mechanisms) 为所有用户配置 OpenTelemetry 设置。有关设置如何应用的更多信息，请参阅 [设置优先级](/docs/zh-CN/settings#settings-precedence)。

示例托管设置配置：

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_METRICS_EXPORTER": "otlp",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_EXPORTER_OTLP_PROTOCOL": "grpc",
    "OTEL_EXPORTER_OTLP_ENDPOINT": "http://collector.example.com:4317",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer example-token"
  }
}
```

在 Claude Desktop 应用中，Code 标签页会话从 [到达每种 Desktop 会话的源](/docs/zh-CN/desktop#managed-settings) 读取这些托管设置。Cowork 在管理员控制台的 [数据和隐私设置](https://claude.ai/admin-settings/data-privacy-controls) 中的 **监控** 下的 OpenTelemetry 表单仅适用于 Cowork 会话，因此终端 CLI 和 Code 标签页都不会导出到您在那里设置的收集器。

Claude Code 忽略存储库的 `.claude/settings.json` 和 `.claude/settings.local.json` 中的 [OpenTelemetry 导出器变量](/docs/zh-CN/settings-reference#variables-claude-code-ignores-in-env)，因此存储库无法使用它们来打开遥测、选择其去向或捕获内容。在托管设置中设置它们，或让每个开发者在其 shell 或 `~/.claude/settings.json` 中设置它们。存储库仍然可以通过将其导出器选择器（如 `OTEL_LOGS_EXPORTER`）设置为 `none` 来关闭信号，除非托管设置、`--settings` 文件或启动 Claude Code 的环境设置了该变量。

Claude Code 不会将 `OTEL_*` 环境变量传递给它生成的子进程，包括 Bash 工具、hooks、MCP 服务器和语言服务器。通过 Bash 工具运行的已进行 OpenTelemetry 检测的应用程序不会继承 Claude Code 的导出器端点或标头，因此如果该应用程序需要导出自己的遥测，请直接在命令中设置这些变量。

<h3 id="how-managed-settings-lock-the-otlp-destination">
  托管设置如何锁定 OTLP 目标
</h3>

当您在托管设置中设置 `OTEL_EXPORTER_OTLP_*` 变量时，Claude Code 会在启动时删除冲突的开发者设置变量，并在调试日志中记录一条警告。它删除的内容取决于您设置的变量：

* **端点**：当您设置 `OTEL_EXPORTER_OTLP_ENDPOINT` 时，Claude Code 会删除每个开发者设置的每信号端点。开发者无法将一个信号指向不同的收集器，因此您不需要在托管设置中也设置每信号端点变量。
* **协议**：当您设置 `OTEL_EXPORTER_OTLP_PROTOCOL` 时，Claude Code 会删除每个开发者设置的每信号协议。
* **凭证**：当您设置 `OTEL_EXPORTER_OTLP_HEADERS`、`OTEL_EXPORTER_OTLP_CLIENT_KEY` 或 `OTEL_EXPORTER_OTLP_CLIENT_CERTIFICATE` 时，Claude Code 会删除开发者设置的该变量的每信号版本，以及每个开发者设置的端点变量（通用或每信号），因为这些凭证否则会到达托管设置未选择的收集器。
* **导出器选择器**：`OTEL_METRICS_EXPORTER`、`OTEL_LOGS_EXPORTER` 和测试版 `OTEL_TRACES_EXPORTER` 遵循正常的每键优先级。开发者的设置仍然可以禁用信号或将其切换到控制台导出器，因此如果您需要锁定选择器，也请在托管设置中设置它们。在 [管理员源](/docs/zh-CN/managed-settings#precedence-within-the-managed-tier) 中，`OTEL_LOGS_EXPORTER` 遵循 [遥测单元](/docs/zh-CN/server-managed-settings#per-key-exceptions-across-managed-sources)，而其他两个选择器按键合并。需要 Claude Code v2.1.223 或更高版本。
* **测试版追踪端点**：当 [详细测试版追踪](#traces-beta) 处于活动状态时，Claude Code 将日志和追踪导出到 `BETA_TRACING_ENDPOINT` 而不是通过日志和追踪导出器。因此，当这些托管设置中的任何一个决定任一信号的目标时，Claude Code 会删除开发者设置的 `BETA_TRACING_ENDPOINT`：

  * 通用或日志/追踪端点或凭证
  * 一个 [`otelHeadersHelper`](/docs/zh-CN/settings-reference#otelheadershelper)
  * 日志或追踪导出器选择器设置为 `none`、`console` 或空，这些值使信号远离收集器
  * `CLAUDE_CODE_ENABLE_TELEMETRY` 关闭

  仅限指标的端点或凭证不会删除它。在 v2.1.251 之前，开发者设置的 `BETA_TRACING_ENDPOINT` 会重定向详细测试版追踪导出的日志和追踪，即使托管设置固定了收集器。

Claude Code 不会删除您在托管设置中自己设置的每信号变量，因此您可以通过在那里设置其变量来将一个信号路由到不同的收集器，如 [SIEM 示例](#send-events-to-a-siem) 所示。如果您在那里设置每信号凭证，Claude Code 会删除该信号的开发者设置端点。

此删除行为改变了遥测的传递位置，而不是 Claude Code 收集的内容。

在 v2.1.217 之前，每个变量独立遵循每键设置优先级，因此在用户设置或 shell 中设置的信号特定端点会将该信号重定向到离开托管收集器。

当桌面应用或 [自托管环境](/docs/zh-CN/self-hosted-environments) 运行器启动 Claude Code 并在其提供的环境中命名 OTLP 端点时，Claude Code 以相同的方式固定目标：启动器的遥测变量删除开发者设置的变量，就像托管设置一样。Claude Code 不会删除启动器本身设置的变量。需要 Claude Code v2.1.251 或更高版本。

<h2 id="configuration-details">
  配置详情
</h2>

<h3 id="common-configuration-variables">
  常见配置变量
</h3>

这些变量为所有部署配置导出器、端点和导出行为。

如果您设置了按信号的端点或协议变量，例如 `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT`，Claude Code 会使用它而不是该信号的通用变量。如果您设置了按信号的标头变量，例如 `OTEL_EXPORTER_OTLP_METRICS_HEADERS`，Claude Code 会将其与该信号的通用 `OTEL_EXPORTER_OTLP_HEADERS` 合并。

在具有托管设置的机器上，请参阅[托管设置如何锁定 OTLP 目标](#how-managed-settings-lock-the-otlp-destination)了解 Claude Code 删除的内容。

| 环境变量 | 描述 | 示例值 |
| - | - | - |
| `CLAUDE_CODE_ENABLE_TELEMETRY` | 启用遥测收集（必需） | `1` |
| `OTEL_METRICS_EXPORTER` | 指标导出器类型，以逗号分隔。使用 `none` 禁用 | `console`、`otlp`、`prometheus`、`none` |
| `OTEL_LOGS_EXPORTER` | 日志/事件导出器类型，以逗号分隔。使用 `none` 禁用 | `console`、`otlp`、`none` |
| `OTEL_EXPORTER_OTLP_PROTOCOL` | OTLP 导出器的协议，适用于所有信号。Claude Code 没有默认协议，因此请为启用的每个 `otlp` 导出器设置此变量或按信号的协议变量 | `grpc`、`http/json`、`http/protobuf` |
| `OTEL_EXPORTER_OTLP_ENDPOINT` | 所有信号的 OTLP 收集器端点 | `http://localhost:4317` |
| `OTEL_EXPORTER_OTLP_METRICS_PROTOCOL` | 指标协议，覆盖常规设置 | `grpc`、`http/json`、`http/protobuf` |
| `OTEL_EXPORTER_OTLP_METRICS_ENDPOINT` | OTLP 指标端点，覆盖常规设置 | `http://localhost:4318/v1/metrics` |
| `OTEL_EXPORTER_OTLP_LOGS_PROTOCOL` | 日志协议，覆盖常规设置 | `grpc`、`http/json`、`http/protobuf` |
| `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT` | OTLP 日志端点，覆盖常规设置 | `http://localhost:4318/v1/logs` |
| `OTEL_EXPORTER_OTLP_HEADERS` | OTLP 的身份验证标头 | `Authorization=Bearer token` |
| `OTEL_EXPORTER_OTLP_METRICS_HEADERS` | 指标的身份验证标头，与常规标头合并 | `Authorization=Bearer token` |
| `OTEL_EXPORTER_OTLP_LOGS_HEADERS` | 日志的身份验证标头，与常规标头合并 | `Authorization=Bearer token` |
| `OTEL_METRIC_EXPORT_INTERVAL` | 导出间隔（毫秒）（默认值：60000） | `5000`、`60000` |
| `OTEL_LOGS_EXPORT_INTERVAL` | 日志导出间隔（毫秒）（默认值：5000） | `1000`、`10000` |
| `OTEL_LOG_USER_PROMPTS` | 启用用户提示内容的日志记录（默认值：禁用） | `1` 启用 |
| `OTEL_LOG_ASSISTANT_RESPONSES` | 在 `assistant_response` 事件上启用助手响应文本的日志记录（默认值：禁用）。未设置时，回退到 `OTEL_LOG_USER_PROMPTS` 的值。需要 Claude Code v2.1.193 或更高版本 | `1` 启用，`0` 保持编辑 |
| `OTEL_LOG_TOOL_DETAILS` | 在工具事件和跟踪跨度属性中启用工具参数和输入参数的日志记录：Bash 命令、MCP 服务器和工具名称、技能名称、用户编写的工作流名称和工具输入。还在 `user_prompt` 事件上启用自定义、插件和 MCP 命令名称，以及在[成本和令牌计数器](#cost-counter)上启用真实代理、技能、插件和 MCP 服务器和工具名称（默认值：禁用）。对于 Claude Desktop 的内置服务器，在 Claude Desktop 拥有的会话中，即使关闭标志，`mcp_server_name`/`mcp_tool_name` 也会在 `tool_decision`/`tool_result` 上发出。该异常需要 Claude Code v2.1.214 或更高版本 | `1` 启用 |
| `OTEL_LOG_TOOL_CONTENT` | 在 [`tool.output` 跨度事件](#tool-output-span-event)中启用工具内容的日志记录（默认值：禁用）。跨度属性在[其自己的门](#new-context-gates)下携带工具内容。需要[跟踪](#traces-beta)。内容在内容限制处截断（默认值 60 KB） | `1` 启用 |
| `OTEL_LOG_MANAGED_SETTINGS` | 将编辑的托管设置和编辑前设置的 SHA-256 摘要添加到[托管设置已解决](#managed-settings-resolved-event)事件（默认值：禁用）。项目或本地设置中的值不会将其打开。需要 Claude Code v2.1.274 或更高版本 | `1` 启用 |
| `OTEL_LOG_RAW_API_BODIES` | 将完整的 Anthropic Messages API 请求和响应 JSON 作为 `api_request_body` / `api_response_body` 日志事件发出（默认值：禁用）。正文包括整个对话历史记录。启用此选项意味着同意 `OTEL_LOG_USER_PROMPTS`、`OTEL_LOG_TOOL_DETAILS` 和 `OTEL_LOG_TOOL_CONTENT` 会揭示的所有内容 | `1` 表示在内容限制处截断的内联正文（默认值 60 KB），或 `file:<dir>` 表示磁盘上的未截断正文，事件中有 `body_ref` 指针 |
| `CLAUDE_CODE_OTEL_CONTENT_MAX_LENGTH` | 内容限制：内容承载属性（如模型响应、工具内容、系统提示和原始 API 正文）的最大长度，包括截断标记，以 UTF-16 代码单位为单位（默认值：61440，即 60 KB）。默认值针对将属性值上限设为 64 KB 的后端进行了调整；仅当您的后端接受更大的值时才提高它，或降低它以减少遥测量。当设置了 OpenTelemetry SDK 属性限制 `OTEL_ATTRIBUTE_VALUE_LENGTH_LIMIT` 或其日志记录和跨度变体之一时，Claude Code 在该较小的值处截断，以便 `[TRUNCATED ...]` 标记保持在 SDK 限制内。需要 Claude Code v2.1.214 或更高版本 | `262144` |
| `OTEL_EXPORTER_OTLP_METRICS_TEMPORALITY_PREFERENCE` | 指标时间性偏好（默认值：`delta`）。如果您的后端期望累积时间性，请设置为 `cumulative` | `delta`、`cumulative` |
| `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS` | 刷新动态标头的间隔（默认值：1740000ms / 29 分钟） | `900000` |

对于 `http/protobuf` 和 `http/json` 协议，Claude Code 使用 `Content-Length` 标头发送每个导出请求。在 v2.1.212 之前，v2.1.191 及更高版本的 Claude Code 版本使用分块传输编码发送这些请求；Azure Monitor 和其他需要声明长度的端点以 `411 Length Required` 或 `400` 错误拒绝它们。

<h3 id="mtls-authentication">
  mTLS 身份验证
</h3>

您如何为 OTLP 导出器配置客户端证书取决于用于该信号的 OTLP 协议，通过 `OTEL_EXPORTER_OTLP_PROTOCOL` 或按信号的覆盖设置。相同的配置适用于指标、日志和跟踪。

| 协议 | 客户端证书变量 | 信任收集器的 CA 使用 |
| :- | :- | :- |
| `http/protobuf`、`http/json` | `CLAUDE_CODE_CLIENT_CERT`、`CLAUDE_CODE_CLIENT_KEY` 和可选的 `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE`。请参阅[网络配置](/docs/zh-CN/network-config#mtls-authentication) | `NODE_EXTRA_CA_CERTS` |
| `grpc` | `OTEL_EXPORTER_OTLP_CLIENT_KEY` 和 `OTEL_EXPORTER_OTLP_CLIENT_CERTIFICATE`，或按信号的变体，例如 `OTEL_EXPORTER_OTLP_METRICS_CLIENT_KEY` 以对每个信号使用不同的证书 | `OTEL_EXPORTER_OTLP_CERTIFICATE` |

对于 `grpc`，OpenTelemetry SDK 直接读取标准 OTLP 变量，因此设置按信号指标变量的现有配置继续有效。在具有托管设置的机器上，Claude Code [可能在启动时删除开发人员设置的按信号凭证和端点](#how-managed-settings-lock-the-otlp-destination)。

<h3 id="metrics-cardinality-control">
  指标基数控制
</h3>

以下环境变量控制指标中包含哪些属性以管理基数：

| 环境变量 | 描述 | 默认值 | 禁用示例 |
| - | - | - | - |
| `OTEL_METRICS_INCLUDE_SESSION_ID` | 在指标中包含 session.id 和云会话上的 ccr.session.id 属性 | `true` | `false` |
| `OTEL_METRICS_INCLUDE_VERSION` | 在指标中包含 app.version 属性 | `false` | `true` |
| `OTEL_METRICS_INCLUDE_ACCOUNT_UUID` | 在指标中包含 user.account\_uuid 和 user.account\_id 属性 | `true` | `false` |
| `OTEL_METRICS_INCLUDE_ENTRYPOINT` | 在指标中包含 app.entrypoint 属性 | `false` | `true` |
| `OTEL_METRICS_INCLUDE_RESOURCE_ATTRIBUTES` | 将 `OTEL_RESOURCE_ATTRIBUTES` 中的键作为属性包含在指标数据点上 | `true` | `false` |
| `OTEL_METRICS_INCLUDE_REPOSITORY` | 在指标和事件上包含 `vcs.*` [存储库身份属性](#repository-attributes)。需要 Claude Code v2.1.269 或更高版本 | `false` | `true` |

较低的基数通常意味着更好的性能和更低的存储成本，但分析的数据粒度较低。

<h3 id="traces-beta">
  Traces（测试版）
</h3>

分布式跟踪导出跨度，将每个用户提示链接到它触发的 API 请求和工具执行，因此您可以在跟踪后端中将完整请求视为单个跟踪。

跟踪默认关闭。要启用它，请同时设置 `CLAUDE_CODE_ENABLE_TELEMETRY=1` 和 `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1`，然后设置 `OTEL_TRACES_EXPORTER` 以选择跨度的发送位置。跟踪重用[常见 OTLP 配置](#common-configuration-variables)用于端点、协议、标头和 [mTLS](#mtls-authentication)。在具有托管设置的机器上，Claude Code [可能在启动时删除开发人员设置的按信号凭证和端点](#how-managed-settings-lock-the-otlp-destination)。

| 环境变量 | 描述 | 示例值 |
| - | - | - |
| `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` | 启用跨度跟踪（必需）。也接受 `ENABLE_ENHANCED_TELEMETRY_BETA` | `1` |
| `OTEL_TRACES_EXPORTER` | 跟踪导出器类型，以逗号分隔。使用 `none` 禁用 | `console`、`otlp`、`none` |
| `OTEL_EXPORTER_OTLP_TRACES_PROTOCOL` | 跟踪协议，覆盖 `OTEL_EXPORTER_OTLP_PROTOCOL` | `grpc`、`http/json`、`http/protobuf` |
| `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT` | OTLP 跟踪端点，覆盖 `OTEL_EXPORTER_OTLP_ENDPOINT` | `http://localhost:4318/v1/traces` |
| `OTEL_EXPORTER_OTLP_TRACES_HEADERS` | 跟踪的身份验证标头，与 `OTEL_EXPORTER_OTLP_HEADERS` 合并 | `Authorization=Bearer token` |
| `OTEL_TRACES_EXPORT_INTERVAL` | 跨度批导出间隔（毫秒）（默认值：5000） | `1000`、`10000` |

跨度默认编辑用户提示文本、工具输入详情和工具内容。设置 `OTEL_LOG_USER_PROMPTS=1`、`OTEL_LOG_TOOL_DETAILS=1` 和 `OTEL_LOG_TOOL_CONTENT=1` 以包含它们。

当跟踪处于活动状态时，Bash 和 PowerShell 子进程会自动继承包含活动工具执行跨度的 W3C 跟踪上下文的 `TRACEPARENT` 环境变量。这允许任何读取 `TRACEPARENT` 的子进程在同一跟踪下将其自己的跨度作为父级，通过 Claude 运行的脚本和命令启用端到端分布式跟踪。

当跟踪处于活动状态且 Claude Code 直接连接到 Anthropic API 时，每个模型请求都携带设置为 `claude_code.llm_request` 跨度上下文的 W3C `traceparent` 标头，API 的 `traceresponse` 标头被记录为跨度链接。这些一起通过任何兼容的中介将 Claude Code 的客户端跨度连接到服务器端跟踪。出站 HTTP MCP 请求以相同方式携带 `traceparent`。标头不会发送给第三方提供商。

默认情况下，模型和 HTTP MCP 请求上的 `traceparent` 标头仅在 `ANTHROPIC_BASE_URL` 未设置或指向 Anthropic API 时发送，因为某些代理拒绝无法识别的标头。子进程 `TRACEPARENT` 变量由相同的开关控制以保持一致性。如果您通过自定义 `ANTHROPIC_BASE_URL` 代理运行 Claude Code 并希望传播跟踪上下文，请设置 `CLAUDE_CODE_PROPAGATE_TRACEPARENT=1`。

在 Agent SDK 和使用 `-p` 启动的非交互式会话中，Claude Code 还在启动每个交互跨度时从其自己的环境中读取 `TRACEPARENT` 和 `TRACESTATE`。这允许嵌入过程将其活动 W3C 跟踪上下文传递到子进程中，以便 Claude Code 的跨度显示为调用者分布式跟踪的子级。交互式会话忽略入站 `TRACEPARENT` 以避免意外继承来自 CI 或容器环境的环境值。

入站跟踪上下文也适用于[事件](#events)。在设置了 `TRACEPARENT` 的 Agent SDK 和 `-p` 会话中，每个 OTLP 事件日志记录都携带 `trace_id` 和 `span_id` 值，将其加入您的应用程序跟踪，即使未配置跟踪导出器，您的日志后端也可以将事件与跟踪的其余部分关联。

在交互处于活动状态时发出的记录携带交互跨度的 ID，即使 Claude Code 在跨度的异步上下文之外发出它，例如在权限提示回调中或对在启动期间缓冲并稍后导出的记录。在没有活动交互跨度的情况下发出的记录直接携带入站 `TRACEPARENT` ID。在 v2.1.214 之前，在跨度的异步上下文之外发出的记录携带入站 `TRACEPARENT` ID 而不是跨度的 ID。在 v2.1.212 之前，在活动跨度之外发出的事件记录不携带 `trace_id` 或 `span_id`。

<h4 id="span-hierarchy">
  跨度层次结构
</h4>

每个用户提示启动一个 `claude_code.interaction` 根跨度。API 调用、工具调用和钩子执行被记录为其子级。工具跨度有两个自己的子跨度：一个用于等待权限决定的时间，一个用于执行本身。当 Agent 工具或旧版 Task 工具生成子代理时，子代理的 API 和工具跨度嵌套在父级的 `claude_code.tool` 跨度下。

```text theme={null}
claude_code.interaction
├── claude_code.llm_request
├── claude_code.hook                    (requires detailed beta tracing)
└── claude_code.tool
    ├── claude_code.tool.blocked_on_user
    ├── claude_code.tool.execution
    └── (Agent tool) subagent claude_code.llm_request / claude_code.tool spans
```

在 Agent SDK 和 `claude -p` 会话中，当在环境中设置 `TRACEPARENT` 时，`claude_code.interaction` 本身成为调用者跨度的子级。

当 `PreToolUse` 钩子[延迟工具调用](/docs/zh-CN/hooks#defer-a-tool-call-for-later)时，Claude Code 保存延迟它的转向的跟踪上下文。当您恢复会话并且工具重新运行时，工具的跨度加入该较早转向的跟踪作为转向的 `claude_code.interaction` 跨度的子级。

<h4 id="span-attributes">
  跨度属性
</h4>

每个跨度都携带[标准属性](#standard-attributes)加上与其名称匹配的 `span.type` 属性。下表列出了在每个跨度上设置的其他属性。`llm_request`、`tool.execution` 和 `hook` 跨度在记录失败时设置 OpenTelemetry 状态 `ERROR`；其他跨度始终以状态 `UNSET` 结束。

**`claude_code.interaction`**

| 属性 | 描述 | 门控 |
| - | - | - |
| `user_prompt` | 提示文本。除非设置了门，否则值为 `<REDACTED>` | `OTEL_LOG_USER_PROMPTS` |
| `user_prompt_length` | 提示长度（字符） | |
| `interaction.sequence` | 交互的 1 基计数器，按 Claude Code 进程而不是按会话计数，如 [`event.sequence`](#event-correlation-attributes) 所述 | |
| `parent.source` | 跨度如何获得其跟踪父级：当它在入站 `TRACEPARENT` 下作为父级时为 `env`，当它启动自己的跟踪时为 `none`。需要 Claude Code v2.1.268 或更高版本 | |
| `interaction.duration_ms` | 转向的挂钟持续时间 | |

**`claude_code.llm_request`**

| 属性 | 描述 | 门控 |
| - | - | - |
| `model` | 模型标识符 | |
| `gen_ai.system` | 始终为 `anthropic`。OpenTelemetry GenAI 语义约定 | |
| `gen_ai.request.model` | 与 `model` 相同的值。OpenTelemetry GenAI 语义约定 | |
| `query_source` | 发出请求的子系统，例如 `repl_main_thread` 或子代理名称 | `ENABLE_BETA_TRACING_DETAILED` |
| `query_source_safe` | `query_source` 的有界形式，无论是否启用详细测试版跟踪都会发出，具有 `repl_main_thread` 或 `agent.builtin.general-purpose` 等值。`:` 变为 `.`，用户命名的代理显示为 `agent.custom`。需要 Claude Code v2.1.268 或更高版本 | |
| `agent_id` | 发出请求的子代理或队友的标识符。在主会话上不存在 | |
| `parent_agent_id` | 生成此代理的代理的标识符。对于主会话和直接从其生成的代理不存在 | |
| `workflow.run_id` | 生成此代理的[工作流](/docs/zh-CN/workflows)工具运行的运行标识符，前缀为 `wf_`。对于不是由工作流生成的代理不存在 | |
| `workflow.name` | 生成此代理的工作流的名称。用户编写的名称被替换为 `custom`，除非设置了门 | `OTEL_LOG_TOOL_DETAILS` |
| `speed` | `fast` 或 `normal` | |
| `effort` | 应用于请求的[努力级别](/docs/zh-CN/model-config#adjust-effort-level)：`low`、`medium`、`high`、`xhigh` 或 `max`。当 Claude Code 不发送努力级别时不存在，例如在不支持努力的模型上。需要 Claude Code v2.1.274 或更高版本 | |
| `llm_request.context` | `interaction`、`tool` 或 `standalone`，取决于父跨度 | |
| `duration_ms` | 包括重试的挂钟持续时间 | |
| `ttft_ms` | 首个令牌的时间（毫秒） | |
| `first_content_ms` | 从请求开始到成功尝试的第一个内容块的时间（毫秒）。在回退到非流式路径的请求上不存在。需要 Claude Code v2.1.268 或更高版本 | |
| `input_tokens` | API 使用块中的输入令牌计数 | |
| `output_tokens` | 输出令牌计数 | |
| `cache_read_tokens` | 从提示缓存读取的令牌 | |
| `cache_creation_tokens` | 写入提示缓存的令牌 | |
| `request_id` | API 请求 ID。与 `request_id` [事件关联属性](#event-correlation-attributes)相同的值 | |
| `gen_ai.response.id` | 与 `request_id` 相同的值。OpenTelemetry GenAI 语义约定 | |
| `client_request_id` | 最终尝试的客户端生成的 `x-client-request-id` | |
| `attempt` | 为此请求进行的总尝试次数 | |
| `success` | `true` 或 `false` | |
| `status_code` | 请求失败时的 HTTP 状态代码 | |
| `error` | 请求失败时的错误消息 | |
| `error_class` | 请求失败时的短错误类令牌，例如 `api_timeout` 或 `server_overload`。需要 Claude Code v2.1.268 或更高版本 | |
| `response.has_tool_call` | 当响应包含工具使用块时为 `true` | |
| `stop_reason` | API 响应 `stop_reason`，例如 `end_turn`、`tool_use`、`max_tokens`、`stop_sequence`、`pause_turn` 或 `refusal` | |
| `gen_ai.response.finish_reasons` | 与 `stop_reason` 相同的值，包装在字符串数组中。OpenTelemetry GenAI 语义约定 | |

每次重试尝试也被记录为具有 `attempt` 和 `client_request_id` 属性的 `gen_ai.request.attempt` 跨度事件。

**`claude_code.tool`**

| 属性 | 描述 | 门控 |
| - | - | - |
| `tool_name` | 工具名称 | |
| `tool_name_safe` | `tool_name` 的形式，不携带任何用户选择的名称。内置工具名称逐字通过。MCP 工具名称显示为 `mcp_other`，除了与几个固定形状匹配的工具名称，例如名为 `browser_*` 的 `playwright` 工具，它们逐字通过。需要 Claude Code v2.1.268 或更高版本 | |
| `bash_command_class` | 对于 Bash 工具：命令的第一个程序的类别，来自固定列表，例如 `vcs` 或 `package_manager`。`other` 表示列表外的程序，`unparsed` 表示无法解析该行。需要 Claude Code v2.1.268 或更高版本 | |
| `bash_argv0` | 对于 Bash 工具：当命令的第一个程序在同一固定列表上时，例如 `git` 或 `npm`。`other` 表示列表外的任何程序。需要 Claude Code v2.1.268 或更高版本 | |
| `duration_ms` | 包括权限等待和执行的挂钟持续时间 | |
| `result_tokens` | 工具结果的近似令牌大小 | |
| `agent_id` | 运行工具的子代理或队友的标识符。在主会话上不存在 | |
| `parent_agent_id` | 生成此代理的代理的标识符。对于主会话和直接从其生成的代理不存在 | |
| `workflow.run_id` | 生成此代理的工作流工具运行的运行标识符，前缀为 `wf_`。对于不是由工作流生成的代理不存在 | |
| `workflow.name` | 生成此代理的工作流的名称。用户编写的名称被替换为 `custom`，除非设置了门 | `OTEL_LOG_TOOL_DETAILS` |
| `tool_use_id` | 此调用的模型 `tool_use` 块 id。与[tool\_result](#tool-result-event)和[tool\_decision](#tool-decision-event)事件上的 `tool_use_id` 以及钩子有效负载中的匹配，因此您可以将跨度加入这些记录 | |
| `gen_ai.tool.call.id` | 与 `tool_use_id` 相同的值。OpenTelemetry GenAI 语义约定 | |
| `file_path` | Read、Edit 和 Write 工具的目标文件路径 | `OTEL_LOG_TOOL_DETAILS` |
| `full_command` | Bash 工具的命令字符串 | `OTEL_LOG_TOOL_DETAILS` |
| `skill_name` | Skill 工具的技能名称 | `OTEL_LOG_TOOL_DETAILS` |
| `subagent_type` | Agent 工具或旧版 Task 工具的子代理类型 | `OTEL_LOG_TOOL_DETAILS` |

<span id="tool-output-span-event" />**`claude_code.tool` 上的 `tool.output` 跨度事件**

如果您设置 `OTEL_LOG_TOOL_CONTENT=1`，Read 和 Bash 调用可以在 `claude_code.tool` 跨度上记录 `tool.output` 跨度事件。Edit 和 Write 调用仅在您也设置 `OTEL_LOG_TOOL_DETAILS=1` 时才记录一个。该变量不限于这两个工具，因此请检查其[配置表中的行](#common-configuration-variables)以了解它在其他地方添加的参数。

MCP 工具、WebFetch 和 WebSearch 也记录此事件，在 Claude Code v2.1.283 或更高版本上。

Claude Code 从工具调用的成功返回时写入此事件，因此引发错误的调用不记录任何内容，无论工具如何。在确实返回的调用中，它不为以下内容记录 `tool.output` 事件：

* 对除 Read、Edit、Write、Bash、WebFetch、WebSearch 和 MCP 工具之外的任何工具的调用
* 返回除文件文本之外的任何内容的 Read，例如图像、PDF 或重新读取内容未更改的文件
* Edit 或 Write 调用，除非您也设置 `OTEL_LOG_TOOL_DETAILS=1`
* Claude Code 移到后台的 WebFetch 或 WebSearch 调用，因为您中断了转向以[立即发送您排队的消息](/docs/zh-CN/interactive-mode#when-claude-code-sends-what-you-queued)，而调用运行。Claude 稍后在工具跨度结束后收到该结果

该事件携带这些属性，每个都在内容限制处截断（默认值 60 KB）。`门控` 命名变量一个属性需要在 `OTEL_LOG_TOOL_CONTENT=1` 之上，对于 Edit 和 Write，该变量门控事件本身而不是属性。

| 属性 | 描述 | 门控 |
| - | - | - |
| `content` | Read 工具返回的文本，或 Write 调用被要求写入的文本 | `OTEL_LOG_TOOL_DETAILS` 用于 Write 工具 |
| `output` | 对于 Bash 工具，命令的组合输出，stderr 交错到 stdout。对于 MCP 工具、WebFetch 或 WebSearch，工具返回的结果：文本块由换行符连接，图像或文档被替换为占位符，例如 `[image]` | |
| `diff` | Edit 工具应用的结构化补丁 | `OTEL_LOG_TOOL_DETAILS` |
| `file_path` | Read、Edit 和 Write 工具的目标文件路径，重复相同名称的跨度属性 | `OTEL_LOG_TOOL_DETAILS` |
| `bash_command` | Bash 工具的命令字符串 | `OTEL_LOG_TOOL_DETAILS` |

父跨度的 `tool_name` 属性告诉您事件来自哪个工具。在内容限制处切割的属性伴随 `<attribute>_truncated` 和 `<attribute>_original_length`。

**`claude_code.tool.blocked_on_user`**

| 属性 | 描述 | 门控 |
| - | - | - |
| `duration_ms` | 等待权限决定所花费的时间 | |
| `decision` | `accept` 或 `reject` | |
| `source` | 决定来源，与[工具决定事件](#tool-decision-event)匹配 | |

**`claude_code.tool.execution`**

| 属性 | 描述 | 门控 |
| - | - | - |
| `duration_ms` | 运行工具主体所花费的时间 | |
| `tool_use_id` | 与父 `claude_code.tool` 跨度上的相同值 | |
| `gen_ai.tool.call.id` | 与 `tool_use_id` 相同的值。OpenTelemetry GenAI 语义约定 | |
| `success` | `true` 或 `false` | |
| `error` | 执行失败时的错误类别字符串，例如 `Error:ENOENT` 或 `ShellError`。当设置了门时包含完整的错误消息 | `OTEL_LOG_TOOL_DETAILS` |
| `error_class` | 标识符形式的错误类别，字母、数字和下划线之外的字符被替换为 `_`，例如 `Error_ENOENT` 或 `ShellError`。即使 `error` 携带完整消息也携带类别。需要 Claude Code v2.1.268 或更高版本 | |

**`claude_code.hook`**

此跨度仅在启用详细测试版跟踪时出现，这需要 `ENABLE_BETA_TRACING_DETAILED=1` 和 `BETA_TRACING_ENDPOINT`，一对也[改变日志和跟踪的去向](/docs/zh-CN/env-vars#variables)。在您的 shell、用户设置或托管设置中设置该对；两个变量都在[项目和本地设置](/docs/zh-CN/settings-reference#variables-claude-code-ignores-in-env)中被忽略。`CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` 单独不会产生它。

在交互式 CLI 会话中，详细测试版跟踪还需要您的组织被列入该功能的白名单。Agent SDK 和非交互式 `-p` 会话不需要白名单。

| 属性 | 描述 | 门控 |
| - | - | - |
| `hook_event` | 钩子事件类型，例如 `PreToolUse` | |
| `hook_name` | 完整钩子名称，例如 `PreToolUse:Write` | |
| `num_hooks` | 执行的匹配钩子命令数 | |
| `hook_definitions` | JSON 序列化的钩子配置 | `OTEL_LOG_TOOL_DETAILS` |
| `duration_ms` | 所有匹配钩子的挂钟持续时间 | |
| `num_success` | 成功完成的钩子计数 | |
| `num_blocking` | 返回阻止决定的钩子计数 | |
| `num_non_blocking_error` | 失败而不阻止的钩子计数 | |
| `num_cancelled` | 在完成前取消的钩子计数 | |

<span id="new-context-gates" />

<Note>
  其他内容承载属性，例如 `new_context`、`system_prompt_preview`、`user_system_prompt`、`tool_input` 和 `response.model_output`，仅在启用详细测试版跟踪时发出。它们不是稳定跨度架构的一部分。

  `new_context` 上的门取决于哪个跨度携带它，每个副本都在内容限制处截断（默认值 60 KB）。在 `claude_code.tool` 跨度上，它携带该工具调用的结果，无论工具如何，并需要 `OTEL_LOG_TOOL_CONTENT=1`。在 `claude_code.interaction` 跨度上，它携带用户提示，在 `claude_code.llm_request` 跨度上，它携带该请求的新用户消息和工具结果。两者都需要 `OTEL_LOG_USER_PROMPTS=1`。

  `user_system_prompt` 另外需要 `OTEL_LOG_USER_PROMPTS=1`。它仅携带您通过 `systemPrompt` SDK 选项或 `--system-prompt` 和 `--append-system-prompt` 标志提供的系统提示文本，在内容限制处截断（默认值 60 KB），并且每个会话发出一次而不是每个请求。
</Note>

<h3 id="dynamic-headers">
  动态标头
</h3>

对于需要动态身份验证的企业环境，您可以配置脚本以动态生成标头。动态标头仅适用于 `http/protobuf` 和 `http/json` 协议。使用 `grpc` 协议，Claude Code 仅使用静态标头变量 `OTEL_EXPORTER_OTLP_HEADERS` 及其按信号的变体。

<h4 id="settings-configuration">
  设置配置
</h4>

添加到您的 `.claude/settings.json`，用您自己的脚本替换路径：

```json theme={null}
{
  "otelHeadersHelper": "/path/to/generate-otel-headers.sh"
}
```

该值可以是可执行文件的路径，包括包含空格的路径，或带有参数的 shell 命令行。在 Windows 上，该值始终通过 shell 运行，因此在 JSON 值内引用包含空格的路径。

<h4 id="script-requirements">
  脚本要求
</h4>

脚本必须输出有效的 JSON，其中包含代表 HTTP 标头的字符串键值对：

```bash theme={null}
#!/bin/bash
# 示例：多个标头
echo "{\"Authorization\": \"Bearer $(get-token.sh)\", \"X-API-Key\": \"$(get-api-key.sh)\"}"
```

如果助手失败或打印不符合这些要求的输出，导出失败，您的遥测后端在会话中不会收到任何内容，直到助手再次工作。Claude Code 在以下位置报告失败：

* 交互式会话中的警告通知，[`otelHeadersHelper failed; telemetry is not being exported`](/docs/zh-CN/errors#otelheadershelper-failed)，在助手首次失败时每个会话显示一次
* `/status` 输出
* 调试日志，当使用 [`--debug`](/docs/zh-CN/cli-reference#cli-flags) 运行或在会话中运行 `/debug` 后
* stderr，在使用 `-p` 启动的非交互式会话中

<h4 id="refresh-behavior">
  刷新行为
</h4>

标头助手脚本在启动时运行，然后定期运行以支持令牌刷新。默认情况下，脚本每 29 分钟运行一次。使用 `CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS` 环境变量自定义间隔。

<h3 id="multi-team-organization-support">
  多团队组织支持
</h3>

具有多个团队或部门的组织可以使用 `OTEL_RESOURCE_ATTRIBUTES` 环境变量添加自定义属性以区分不同的组：

```bash theme={null}
# 添加用于团队识别的自定义属性
export OTEL_RESOURCE_ATTRIBUTES="department=engineering,team.id=platform,cost_center=eng-123"
```

这些自定义属性包含在所有指标和事件中，允许您：

* 按团队或部门过滤指标
* 按成本中心跟踪成本
* 创建特定于团队的仪表板
* 为特定团队设置警报

Claude Code 将这些值作为属性附加到每个指标数据点和事件记录，除了在 OTLP 资源块中发送它们。因为大多数指标后端将数据点属性公开为可查询的标签，您可以直接按自定义键对指标进行分组和过滤。除了 `vcs.*` [存储库属性](#repository-attributes)，自定义键永远不会覆盖[标准属性](#standard-attributes)，例如 `user.id` 或 `session.id`：当键冲突时，Claude Code 保留内置值。

每个自定义键成为每个指标系列上的标签，因此高基数值会增加指标后端中的存储成本。要仅在资源块中发送自定义属性并从数据点标签中省略它们，请设置 `OTEL_METRICS_INCLUDE_RESOURCE_ATTRIBUTES=false`。请参阅[指标基数控制](#metrics-cardinality-control)。

<Warning>
  `OTEL_RESOURCE_ATTRIBUTES` 环境变量使用逗号分隔的键=值对，具有严格的格式要求：

  * **不允许空格**：值不能包含空格。例如，`user.organizationName=My Company` 无效
  * **格式**：必须是逗号分隔的键=值对：`key1=value1,key2=value2`
  * **允许的字符**：仅限 US-ASCII 字符，不包括控制字符、空格、双引号、逗号、分号和反斜杠
  * **特殊字符**：允许范围之外的字符必须进行百分比编码

  对于需要空格的值，请改用下划线或 camelCase。以下示例使用每种形式设置 `org.name`：

  ```bash theme={null}
  export OTEL_RESOURCE_ATTRIBUTES="org.name=Johns_Organization"
  export OTEL_RESOURCE_ATTRIBUTES="org.name=JohnsOrganization"
  ```

  您可以对任何字符进行百分比编码，而不仅仅是被排除的字符。此示例对空格和撇号进行编码：

  ```bash theme={null}
  export OTEL_RESOURCE_ATTRIBUTES="org.name=John%27s%20Organization"
  ```

  用引号包装值不会转义空格。例如，`org.name="My Company"` 导致文字值 `"My Company"`（包括引号），而不是 `My Company`。
</Warning>

<h3 id="example-configurations">
  示例配置
</h3>

在运行 `claude` 之前设置这些环境变量。下面的每个场景显示完整的配置，每个变量在[常见配置变量](#common-configuration-variables)下进行了描述。要确认配置生效，请在启动会话后检查后端中的 `claude_code.session.count` 指标；[快速入门](#quick-start)涵盖仅日志验证以及当没有内容到达时要检查的内容。

对于使用 1 秒导出间隔的控制台调试：

```bash theme={null}
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console
export OTEL_METRIC_EXPORT_INTERVAL=1000
```

对于 OTLP over gRPC：

```bash theme={null}
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

对于 Prometheus，从 `http://localhost:9464/metrics` 抓取：

```bash theme={null}
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=prometheus
```

在[自托管环境](/docs/zh-CN/self-hosted-environments-reference#pass-through-session-child-metrics)上，会话仅在运行器的默认容量为 1 时绑定端口 9464。在更高的容量下，运行器改为在其自己的 `/metrics` 端点上重新公开会话计数器和仪表。

要将指标发送到多个导出器：

```bash theme={null}
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=console,otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=http/json
```

要将指标和日志发送到不同的端点或后端：

```bash theme={null}
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_METRICS_PROTOCOL=http/protobuf
export OTEL_EXPORTER_OTLP_METRICS_ENDPOINT=http://metrics.example.com:4318
export OTEL_EXPORTER_OTLP_LOGS_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_LOGS_ENDPOINT=http://logs.example.com:4317
```

仅导出指标，不导出事件或日志：

```bash theme={null}
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_METRICS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

仅导出事件和日志，不导出指标：

```bash theme={null}
export CLAUDE_CODE_ENABLE_TELEMETRY=1
export OTEL_LOGS_EXPORTER=otlp
export OTEL_EXPORTER_OTLP_PROTOCOL=grpc
export OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4317
```

<h2 id="telemetry-from-cloud-sessions-and-claude-tag">
  云会话和 Claude Tag 的遥测
</h2>

[云会话](/docs/zh-CN/claude-code-on-the-web)（包括 [Claude Tag](https://claude.com/docs/claude-tag/overview) 频道会话）在[云环境](/docs/zh-CN/cloud-environments)中运行，而不是在用户的设备上运行，因此设备上的托管设置文件或 shell 配置文件不会配置其遥测。对于在 Anthropic 托管环境中的会话，本部分介绍了在何处设置遥测变量、如何使收集器可从环境访问，以及如何在导出的数据中区分云会话和 Claude Tag 会话。

要从这些会话导出遥测，请使用与[管理员配置](#administrator-configuration)示例相同的密钥，在以下两个位置之一中设置 `CLAUDE_CODE_ENABLE_TELEMETRY` 和 `OTEL_*` 变量：

* **服务器管理的设置**：将它们添加到您组织的[服务器管理的设置](/docs/zh-CN/server-managed-settings)的 `env` 块中。Claude Code 在启动时会在[服务器管理的设置适用](/docs/zh-CN/model-config#surface-coverage)的任何地方获取这些设置，这包括您用户的机器和除 Claude Tag 频道会话外的云会话。Claude Tag 会话不会接收您的服务器管理的设置，因此此路由不会配置它们。
* **环境的变量**：将它们添加到云环境的[环境变量](/docs/zh-CN/cloud-environments#set-environment-variables)中，以仅配置在该环境中运行的会话。这是到达 Claude Tag 会话的路由。

任何使用环境的人都可以读取其变量，因此不要在其中放置凭证，例如 `OTEL_EXPORTER_OTLP_HEADERS` 中的收集器令牌。环境上的 [API 凭证](/docs/zh-CN/cloud-environments#add-api-credentials)也无法帮助，因为 Claude Code 自己的遥测导出是[从不获得凭证的请求](/docs/zh-CN/cloud-environments#requests-that-never-get-the-credential)之一。如果您的收集器需要凭证，请改为通过服务器管理的设置配置整个导出，因为当您在那里设置凭证时，[Claude Code 会删除在托管设置外设置的端点变量](#how-managed-settings-lock-the-otlp-destination)。

在为云会话配置遥测时，请记住这些约束：

* **让会话到达收集器**：Claude Code 通过会话的网络发送导出，因此它是否到达您的 `OTEL_EXPORTER_OTLP_ENDPOINT` 中的主机取决于环境的[网络访问级别](/docs/zh-CN/cloud-environments#access-levels)。如果会话无法在您选择的级别上到达收集器的域，请[将域添加到环境的允许列表](/docs/zh-CN/cloud-environments#allow-specific-domains)，因为没有服务器管理的设置会将域添加到环境的网络允许列表。
* **Claude Tag 频道使用组织级别的环境**：频道会话在组织级别的环境中运行，而不是成员的个人环境中，因此请在[共享环境](/docs/zh-CN/cloud-environments#organization-shared-environments)上进行允许列表和任何环境变量更改，该环境设置为您组织的默认环境或固定到频道。
* **Cowork 单独配置**：如[表面覆盖表](/docs/zh-CN/model-config#surface-coverage)所示，Cowork 会话不会接收服务器管理的设置，因此服务器管理的 `env` 块不会配置其遥测。

<h3 id="attribute-telemetry-to-cloud-sessions">
  将遥测属性分配给云会话
</h3>

默认情况下，来自云会话的指标和事件携带[标准属性](#standard-attributes)，包括 `session.id`、`ccr.session.id` 和 `organization.id`，因此您可以按会话或组织进行筛选，无需额外配置。`ccr.session.id` 值是会话的 `CLAUDE_CODE_REMOTE_SESSION_ID`。要将其转换为会话的成绩单 URL，请参阅[将输出链接回会话](/docs/zh-CN/cloud-environments#link-output-back-to-the-session)。

要更详细地属性化遥测，请使用这些选项：

* **识别 Claude Tag 会话**：设置 `OTEL_METRICS_INCLUDE_ENTRYPOINT=true`，如[指标基数控制](#metrics-cardinality-control)下所述。指标随后会携带 `app.entrypoint`，其值对于 Claude Tag 会话为 `claude-in-slack`。
* **添加自定义属性**：在设置这些会话的其他 `OTEL_*` 变量的同一位置设置 [`OTEL_RESOURCE_ATTRIBUTES`](#multi-team-organization-support)。如果您改为在环境的[设置脚本](/docs/zh-CN/cloud-environments#setup-scripts)中 `export` 它，该值不会到达 Claude Code：设置脚本是在 Claude Code 启动前运行的单独 Bash 脚本，它导出的变量随之结束。

在 Claude Tag 频道会话中，Claude 作为您组织的[共享身份](/docs/zh-CN/cloud-environments#set-the-environment-a-claude-tag-channel-uses)工作，而不是作为任何成员，因此不要依赖 `user.*` 属性来识别谁标记了 Claude。

<h2 id="available-metrics-and-events">
  可用的指标和事件
</h2>

<h3 id="standard-attributes">
  标准属性
</h3>

所有指标和事件都共享这些标准属性：

| 属性 | 描述 | 控制方式 |
| - | - | - |
| `session.id` | 唯一的会话标识符 | `OTEL_METRICS_INCLUDE_SESSION_ID`（默认值：true） |
| `ccr.session.id` | 云会话标识符，`CLAUDE_CODE_REMOTE_SESSION_ID` 的值，在[云环境](/docs/zh-CN/cloud-environments)中运行的会话上 | `OTEL_METRICS_INCLUDE_SESSION_ID`（默认值：true） |
| `app.version` | 当前 Claude Code 版本 | `OTEL_METRICS_INCLUDE_VERSION`（默认值：false） |
| `app.entrypoint` | 会话的启动方式，例如 `cli`、`sdk-cli`、`sdk-ts`、`sdk-py`、`claude-vscode` 或 Claude Tag 会话的 `claude-in-slack` | `OTEL_METRICS_INCLUDE_ENTRYPOINT`（默认值：false） |
| `organization.id` | 组织 UUID（已认证时） | 可用时始终包含 |
| `user.account_uuid` | 账户 UUID（已认证时） | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID`（默认值：true） |
| `user.account_id` | 与 Anthropic 管理员 API 匹配的标记格式的账户 ID（已认证时），例如 `user_01BWBeN28...` | `OTEL_METRICS_INCLUDE_ACCOUNT_UUID`（默认值：true） |
| `user.id` | 在首次运行时生成并保存在 `~/.claude.json` 中的随机匿名标识符。它不包含任何个人信息，也不是从您的 Claude 账户派生的。删除该文件会在下次运行时生成一个新的无关值。 | 始终包含 |
| `user.email` | 用户电子邮件地址，来自您的登录或在[云会话](/docs/zh-CN/claude-code-on-the-web)中来自会话自己的凭证 | 可用时始终包含 |
| `terminal.type` | 终端类型，例如 `iTerm.app`、`vscode`、`cursor` 或 `tmux` | 检测到时始终包含 |
| `OTEL_RESOURCE_ATTRIBUTES` 中的键 | 您设置的自定义属性，例如 `department` 或 `team.id`。请参阅[多团队组织支持](#multi-team-organization-support) | `OTEL_METRICS_INCLUDE_RESOURCE_ATTRIBUTES`（默认值：true） |
| `vcs.repository.url.full`、`vcs.owner.name`、`vcs.repository.name`、`vcs.provider.name` | 会话存储库的身份，从其 `origin` 远程派生。请参阅[存储库属性](#repository-attributes) | `OTEL_METRICS_INCLUDE_REPOSITORY`（默认值：false）。需要 Claude Code v2.1.269 或更高版本 |

在通过 `/login` 登录到[Claude 应用网关](/docs/zh-CN/claude-apps-gateway)的会话中，CLI 会使用已认证身份标记导出：`user.id` 是 IdP 主体，`user.email` 是已登录的电子邮件，`user.groups` 以逗号分隔的字符串形式携带 IdP 组成员身份。每个导出还携带 `identity.source: gateway-oidc`。网关身份最后应用，因此通过 `OTEL_RESOURCE_ATTRIBUTES` 设置的 `user.*` 和 `identity.*` 键在这些会话上被忽略。

对于通过网关连接的 Claude Desktop 和 Cowork 会话上的身份属性，请参阅[网关 `telemetry` 参考](/docs/zh-CN/claude-apps-gateway-config#telemetry)。

事件另外包括以下属性。这些永远不会附加到指标，因为它们会导致无限的基数：

* `prompt.id`：UUID，将用户提示与所有后续事件关联到下一个提示。请参阅[事件关联属性](#event-correlation-attributes)。
* `workspace.host_paths`：在桌面应用中选择的主机工作区目录，作为字符串数组
* `workflow.run_id`：运行标识符，前缀为 `wf_`，在 API 和工具事件上，由属于[工作流](/docs/zh-CN/workflows)工具运行的代理发出。按一个 `workflow.run_id` 过滤事件可以重建该运行的 API 请求和工具结果。该标识符涵盖工作流脚本生成的代理以及这些代理依次生成的任何代理，例如技能调用。它与工作流工具结果中报告的运行标识符匹配。在所有其他事件上不存在。需要 Claude Code v2.1.202 或更高版本
* `workflow.name`：工作流的名称，其脚本的 `meta.name`，与 `workflow.run_id` 一起发出。内置工作流名称在运行未修改的内置脚本时逐字显示。用户创作的名称（包括内置脚本的编辑副本）被替换为 `custom`，除非设置了 `OTEL_LOG_TOOL_DETAILS=1`。需要 Claude Code v2.1.202 或更高版本

<h4 id="repository-attributes">
  存储库属性
</h4>

设置 `OTEL_METRICS_INCLUDE_REPOSITORY=true` 以使用会话存储库的身份标记指标和事件，以便共享收集器可以按存储库属性使用情况。需要 Claude Code v2.1.269 或更高版本。

Claude Code 每个会话从存储库的 `origin` 远程派生这些属性一次。当存储库的 HTTPS 和 SSH 远程命名相同的主机和相同的路径时（如在 GitHub、GitLab 和 Bitbucket Cloud 上一样），两者都会产生相同的值：

| 属性 | 值 |
| - | - |
| `vcs.repository.url.full` | 存储库的浏览器 URL，不带 `.git`，例如 `https://github.com/example-org/example-repo` |
| `vcs.owner.name` | 所有者或组路径，例如 `example-org`；当远程路径只有一个段时省略 |
| `vcs.repository.name` | 裸存储库名称，例如 `example-repo` |
| `vcs.provider.name` | 当 Claude Code 将远程的主机或 URL 形状识别为这些提供商之一时为 `github`、`gitlab`、`bitbucket` 或 `gitea`；否则省略 |

值被小写，远程 URL 中的凭证、查询字符串和片段永远不会出现在其中。当会话没有 `origin` 远程、远程不是 URL 形状或唯一的封闭存储库是您的主目录时，属性被省略。

要从[云会话](/docs/zh-CN/claude-code-on-the-web)获取这些属性，请在其[云环境](/docs/zh-CN/cloud-environments#set-environment-variables)上设置遥测变量，包括 `OTEL_METRICS_INCLUDE_REPOSITORY`。还要在环境的[网络访问](/docs/zh-CN/cloud-environments#network-access)中允许您的收集器域。

您在 [`OTEL_RESOURCE_ATTRIBUTES`](#multi-team-organization-support) 中声明的 `vcs.*` 键会替换该键的派生值。如果您声明 `vcs.repository.url.full`，Claude Code 永远不会读取远程，只报告您声明的键。

如果一个存储库的 HTTPS 和 SSH 克隆报告不同的值，例如在自托管安装中，其 HTTPS 克隆 URL 携带 SSH URL 缺少的路径前缀，请在 `OTEL_RESOURCE_ATTRIBUTES` 中声明 `vcs.repository.url.full` 以及您想要报告的所有其他 `vcs.*` 键。然后每个克隆都报告您声明的身份。

属性仅流向您自己的导出器；Anthropic 的遥测会删除每个 `vcs.*` 键。

<h3 id="metrics">
  指标
</h3>

Claude Code 导出以下指标。单位列显示附加到每个指标的 OpenTelemetry 单位字符串；计数指标不携带任何单位。

| 指标名称 | 描述 | 单位 |
| - | - | - |
| `claude_code.session.count` | 启动的 CLI 会话计数 | 无 |
| `claude_code.lines_of_code.count` | 修改的代码行计数 | 无 |
| `claude_code.pull_request.count` | 创建的拉取请求数 | 无 |
| `claude_code.commit.count` | 创建的 git 提交数 | 无 |
| `claude_code.cost.usage` | Claude Code 会话的成本 | USD |
| `claude_code.token.usage` | 使用的令牌数 | tokens |
| `claude_code.code_edit_tool.decision` | 代码编辑工具权限决策计数 | 无 |
| `claude_code.active_time.total` | 总活跃时间 | s |

当 `prometheus` 是 `OTEL_METRICS_EXPORTER` 中列出的唯一导出器时，Claude Code 会从导出的指标中省略 `USD`、`tokens` 和 `s` 单位，以便抓取保持有效的 Prometheus 文本格式。指标名称不会改变，组合导出器的配置（例如 `otlp,prometheus`）保留单位。在 v2.1.216 之前，Prometheus 抓取包含一些抓取器拒绝的仅 OpenMetrics 的 `# UNIT` 行。

<h3 id="metric-details">
  指标详情
</h3>

每个指标都包括上面列出的标准属性。具有额外上下文特定属性的指标如下所述。

<h4 id="session-counter">
  会话计数器
</h4>

在每个会话开始时递增。

**属性**：

* 所有[标准属性](#standard-attributes)
* `start_type`：会话的启动方式。`"fresh"`、`"resume"`、`"continue"` 或 `"agents_view"` 之一。`"agents_view"` 值标识 `claude agents` 仪表板进程，这是用户启动的本地 UI 而不是对话会话。在此值上过滤以在您的仪表板中将 UI 进程启动与对话会话分开。

<h4 id="lines-of-code-counter">
  代码行计数器
</h4>

当添加或删除代码时递增。

**属性**：

* 所有[标准属性](#standard-attributes)
* `type`：（`"added"`、`"removed"`）
* `model`：进行更改的模型的模型标识符（例如，"claude-sonnet-5"）

<h4 id="pull-request-counter">
  拉取请求计数器
</h4>

当 Claude Code 通过 shell 命令或 MCP 工具创建拉取请求或合并请求时递增。

**属性**：

* 所有[标准属性](#standard-attributes)

<h4 id="commit-counter">
  提交计数器
</h4>

通过 Claude Code 创建 git 提交时递增。

**属性**：

* 所有[标准属性](#standard-attributes)

<h4 id="cost-counter">
  成本计数器
</h4>

在每个 API 请求后递增。

`agent.name`、`skill.name`、`plugin.name`、`mcp_server.name` 和 `mcp_tool.name` 属性默认将某些名称编辑为 `"custom"` 或 `"third-party"` 占位符。如果您设置 `OTEL_LOG_TOOL_DETAILS=1`，它们会改为携带真实名称。在 v2.1.273 之前，成本和令牌计数器以及 `api_request`、`api_error` 和 `api_refusal` 事件即使设置了 `OTEL_LOG_TOOL_DETAILS=1` 也携带编辑后的值。

**属性**：

* 所有[标准属性](#standard-attributes)
* `model`：模型标识符（例如，"claude-sonnet-5"）
* `query_source`：发出请求的子系统的类别。`"main"`、`"subagent"` 或 `"auxiliary"` 之一
* `speed`：当请求使用快速模式时为 `"fast"`。否则不存在
* `effort`：应用于请求的[努力级别](/docs/zh-CN/model-config#adjust-effort-level)：`"low"`、`"medium"`、`"high"`、`"xhigh"` 或 `"max"`。当 Claude Code 不发送努力级别时不存在，例如在不支持努力的模型上。
* `agent.name`：发出请求的子代理类型。内置代理名称和来自官方市场插件的代理逐字显示。其他用户定义的代理名称被替换为 `"custom"`。当请求不是由命名的子代理类型发出时不存在。
* `skill.name`：对请求活跃的技能，由技能工具或 `/` 命令设置，或由生成的子代理继承。内置、捆绑、用户定义和官方市场插件技能名称逐字显示。第三方插件技能名称被替换为 `"third-party"`。当没有技能活跃时不存在。
* `plugin.name`：当活跃的技能或子代理由插件提供时的所有者插件。官方市场插件名称逐字显示。第三方插件名称被替换为 `"third-party"`。当技能和子代理都没有所有者插件时不存在。
* `marketplace.name`：所有者插件安装的市场。仅对官方市场插件发出，即使设置了 `OTEL_LOG_TOOL_DETAILS=1`。否则不存在。
* `mcp_server.name`：其工具结果此请求消耗的 MCP 服务器。内置、claude.ai 代理和官方注册表服务器名称逐字显示。用户配置的服务器名称被替换为 `"custom"`。当请求没有消耗 MCP 工具结果时不存在。在 v2.1.222 之前，Claude Code 在每个 MCP 工具调用后的请求上设置此属性，而不仅仅在消耗工具结果的请求上，因此聚合它的仪表板在升级后显示下降。
* `mcp_tool.name`：其结果此请求消耗的 MCP 工具，具有与 `mcp_server.name` 相同的编辑和版本行为。当请求没有消耗 MCP 工具结果时不存在。

<h4 id="token-counter">
  令牌计数器
</h4>

在每个 API 请求后递增。

**属性**：

* 所有[标准属性](#standard-attributes)
* `type`：（`"input"`、`"output"`、`"cacheRead"`、`"cacheCreation"`）
* `model`：模型标识符（例如，"claude-sonnet-5"）
* `query_source`：发出请求的子系统的类别。`"main"`、`"subagent"` 或 `"auxiliary"` 之一
* `speed`：当请求使用快速模式时为 `"fast"`。否则不存在
* `effort`：应用于请求的[努力级别](/docs/zh-CN/model-config#adjust-effort-level)。有关详情，请参阅[成本计数器](#cost-counter)。
* `agent.name`、`skill.name`、`plugin.name`、`marketplace.name`、`mcp_server.name`、`mcp_tool.name`：请求的技能、插件、代理和 MCP 属性。有关定义和编辑行为，请参阅[成本计数器](#cost-counter)。

<h4 id="code-edit-tool-decision-counter">
  代码编辑工具决策计数器
</h4>

当用户接受或拒绝 Edit、Write 或 NotebookEdit 工具使用时递增。

**属性**：

* 所有[标准属性](#standard-attributes)
* `tool_name`：工具名称（`"Edit"`、`"Write"`、`"NotebookEdit"`）
* `decision`：用户决策（`"accept"`、`"reject"`）
* `source`：决策来自何处。`"config"`、`"hook"`、`"user_permanent"`、`"user_temporary"`、`"user_abort"` 或 `"user_reject"` 之一。请参阅[工具决策事件](#tool-decision-event)了解每个值的含义。
* `language`：编辑文件的编程语言，例如 `"TypeScript"`、`"Python"`、`"JavaScript"` 或 `"Markdown"`。对于无法识别的文件扩展名返回 `"unknown"`。

<h4 id="active-time-counter">
  活跃时间计数器
</h4>

跟踪实际花费在积极使用 Claude Code 上的时间，不包括空闲时间。此指标在用户交互期间递增，例如键入和阅读响应，以及在 CLI 处理期间，例如工具执行和 AI 响应生成。

**属性**：

* 所有[标准属性](#standard-attributes)
* `type`：`"user"` 用于键盘交互，`"cli"` 用于工具执行和 AI 响应

<h3 id="events">
  事件
</h3>

Claude Code 通过 OpenTelemetry 日志/事件导出以下事件（当配置了 `OTEL_LOGS_EXPORTER` 时）：

<h4 id="event-correlation-attributes">
  事件关联属性
</h4>

当用户提交提示时，Claude Code 可能会进行多个 API 调用并运行多个工具。`prompt.id` 属性让您将所有这些事件与触发它们的单个提示联系起来。

| 属性 | 描述 |
| - | - |
| `prompt.id` | UUID v4 标识符，链接处理单个用户提示时产生的所有事件 |
| `event.sequence` | 用于排序事件的基于 0 的计数器，按 Claude Code 进程而不是按会话计数 |
| `message.uuid` | 消息的 UUID，如会话记录中保存的，`~/.claude/projects/*/*.jsonl` 文件。存在于 `assistant_response`、`api_response_body` 和 `user_prompt` 上，除了命令调度，它可以产生零个或多个消息。在 `assistant_response` 和 `api_response_body` 上，这是响应的最终记录条目，下一轮的 `parentUuid` 从其链接。需要 Claude Code v2.1.214 或更高版本，或在 `api_response_body` 上需要 v2.1.274 或更高版本 |
| `request_id` | 服务器分配的 API 请求 ID，从 `request-id` 响应头读取，例如 `req_011...`。在没有 `request-id` 头的响应上，如在 [Amazon Bedrock](/docs/zh-CN/amazon-bedrock) 上，值来自 `x-amzn-requestid` 头。存在于 `api_request`、`api_error`、`api_refusal`、`assistant_response` 和 `api_response_body` 上，当响应携带任一头时。与 `llm_request` 跟踪跨度上的相同属性匹配。`x-amzn-requestid` 源需要 Claude Code v2.1.282 或更高版本 |
| `client_request_id` | 作为 `x-client-request-id` 请求头发送的客户端生成的 UUID。存在于第一方 API 连接上的 `api_request` 和 `api_error` 上；在第三方提供商后端上不存在，当请求通过非流式回退重试时。将请求与其响应配对，并对于超时等从未产生服务器 `request_id` 的失败保持可用。与 `llm_request` 跟踪跨度上的相同属性匹配。需要 Claude Code v2.1.214 或更高版本 |

要跟踪由单个提示触发的所有活动，请按特定 `prompt.id` 值过滤您的事件。这会返回 user\_prompt 事件、任何 api\_request 事件以及处理该提示时发生的任何 tool\_result 事件。

`event.sequence` 在每次 Claude Code 进程启动时从 0 开始，并在该进程的生命周期内计数。它在 `/clear` 中继续计数，这会分配一个新的 `session.id`。如果您[恢复会话而不分叉](/docs/zh-CN/how-claude-code-works#resume-or-fork-sessions)，会话保留其 `session.id` 但从恢复它的进程获取其 `event.sequence` 值，因此在一个会话内，较晚的事件可以携带比较早的值更低的值，或重复一个。要排序会话的事件，按 `event.timestamp` 排序，并使用 `event.sequence` 排序共享时间戳的事件。

对于消息级别的重建，每个事件类都携带一个与会话记录中的字段匹配的键。记录条目格式是[Claude Code 内部的](/docs/zh-CN/sessions#where-transcripts-are-stored)，在版本之间变化，因此在这些字段上联接的管道可能在任何版本上中断；将联接视为版本特定的而不是稳定的合同：

* `message.uuid` 在 `user_prompt`、`assistant_response` 和 `api_response_body` 上
* `request_id` 在 API 事件上，在记录的助手条目上保存为 `requestId`
* `tool_use_id` 在 `tool_result` 和 `tool_decision` 事件上

<h4 id="user-prompt-event">
  用户提示事件
</h4>

当用户提交提示时记录。

**事件名称**：`claude_code.user_prompt`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"user_prompt"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `prompt_length`：提示的长度
* `prompt`：提示内容。默认编辑。设置 `OTEL_LOG_USER_PROMPTS=1` 以包含它
* `message.uuid`：生成的用户消息的 UUID，与保存的记录条目匹配。在命令调度上不存在，它可以产生零个或多个消息。需要 Claude Code v2.1.214 或更高版本
* `command_name`：当提示调用一个时的命令名称。内置和捆绑命令名称如 `compact` 或 `debug` 按原样发出；别名如 `reset` 按键入的方式发出而不是规范名称。自定义、插件和 MCP 命令名称折叠为 `custom` 或 `mcp`，除非设置了 `OTEL_LOG_TOOL_DETAILS=1`
* `command_source`：命令存在时的来源：`builtin`、`custom` 或 `mcp`。插件提供的命令报告为 `custom`

<h4 id="assistant-response-event">
  助手响应事件
</h4>

在返回来自模型的文本内容的每个 API 请求后记录。仅包括响应的文本块；思考块和工具使用块被排除。需要 Claude Code v2.1.193 或更高版本。

**事件名称**：`claude_code.assistant_response`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"assistant_response"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `response_length`：响应文本的长度（以字符为单位）
* `response`：响应文本，在内容限制处截断（默认 60 KB）。默认编辑为 `<REDACTED>`。设置 `OTEL_LOG_ASSISTANT_RESPONSES=1` 以包含它。当 `OTEL_LOG_ASSISTANT_RESPONSES` 未设置时，`OTEL_LOG_USER_PROMPTS` 控制它，因此设置 `OTEL_LOG_ASSISTANT_RESPONSES=0` 以在启用提示日志记录时保持响应编辑
* `model`：模型标识符（例如，"claude-sonnet-5"）
* `request_id`：API 请求 ID，在[事件关联属性](#event-correlation-attributes)下描述
* `message.uuid`：响应的最终记录条目的 UUID。API 响应作为每个内容块一个记录条目保存；这是最后一个，下一轮的 `parentUuid` 从其链接。需要 Claude Code v2.1.214 或更高版本
* `query_source`：发出请求的子系统，例如 `"repl_main_thread"`、`"compact"` 或子代理名称

<h4 id="tool-result-event">
  工具结果事件
</h4>

当工具完成执行时记录。如果工具调用被拒绝，则不发出；请参阅[工具决策事件](#tool-decision-event)了解拒绝。

**事件名称**：`claude_code.tool_result`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"tool_result"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `tool_name`：工具的名称
* `tool_use_id`：此工具调用的唯一标识符。与传递给钩子的 `tool_use_id` 匹配，允许 OTel 事件和钩子捕获数据之间的关联。
* `success`：`"true"` 或 `"false"`
* `duration_ms`：执行时间（以毫秒为单位）
* `error_type`：工具失败时的错误类别字符串，例如 `"Error:ENOENT"` 或 `"ShellError"`
* `error`（当 `OTEL_LOG_TOOL_DETAILS=1` 时）：工具失败时的完整错误消息
* `decision_type`：始终为 `"accept"`，因为此事件仅在工具运行后发出。拒绝的调用不产生工具结果
* `decision_source`：权限决策来自何处。`"config"`、`"hook"`、`"user_permanent"` 或 `"user_temporary"` 之一。请参阅[工具决策事件](#tool-decision-event)了解每个值的含义。仅拒绝的源 `"user_abort"` 和 `"user_reject"` 永远不会出现在此事件上。
* `tool_input_size_bytes`：JSON 序列化工具输入的大小（以字节为单位）
* `tool_result_size_bytes`：工具结果的大小（以字节为单位）
* `mcp_server_scope`：MCP 服务器范围标识符（对于 MCP 工具）
* `vcs.ref.head.revision`、`vcs.ref.head.name`、`vcs.ref.head.type`（当 `OTEL_LOG_TOOL_DETAILS=1` 时）：由 Bash 或 PowerShell 工具成功运行的 `git commit` 的提交身份。`vcs.ref.head.revision` 是提交 SHA，`vcs.ref.head.name` 是提交的分支，`vcs.ref.head.type` 是 `branch`。当提交在分离的 HEAD 上进行时，名称和类型被省略。需要 Claude Code v2.1.269 或更高版本
* `tool_parameters`（当 `OTEL_LOG_TOOL_DETAILS=1` 时）：包含工具特定参数的 JSON 字符串。对于 Claude Desktop 的内置服务器，在 Claude Desktop 拥有的会话中，`mcp_server_name`/`mcp_tool_name` 对即使在标志关闭时也包含，与[工具决策事件](#tool-decision-event)相同的主机创作异常，需要 Claude Code v2.1.214 或更高版本。参数因工具而异：
  * 对于 Bash 工具：包括 `bash_command`、`full_command`、`timeout`、`description` 和 `dangerouslyDisableSandbox`，加上 `git_commit_id` 和 `git_branch`（当 `git commit` 命令成功时）。`git_commit_id` 是完整的提交 SHA（当提交是会话工作目录的 HEAD 时），否则是 git 的缩写 SHA。`git_branch` 是提交的分支，在分离的 HEAD 上省略
  * 对于桌面应用的工作区 Bash 工具，它也将 `tool_name` 报告为 `Bash`：仅包括 `bash_command`、`full_command` 和 `timeout`
  * 对于 MCP 工具：包括 `mcp_server_name`、`mcp_tool_name`
  * 对于技能工具：包括 `skill_name`
  * 对于代理工具或旧版任务工具：包括 `subagent_type`
* `tool_input`（当 `OTEL_LOG_TOOL_DETAILS=1` 时）：JSON 序列化的工具参数。超过 512 个字符的单个值被截断，完整有效负载限制在约 4 K 字符。适用于所有工具，包括 MCP 工具。

<h4 id="api-request-event">
  API 请求事件
</h4>

为每个对 Claude 的 API 请求记录。

**事件名称**：`claude_code.api_request`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"api_request"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `model`：使用的模型（例如，"claude-sonnet-5"）
* `cost_usd`：以美元为单位的估计成本
* `cost_usd_micros`：以美元百万分之一为单位的估计成本，作为整数发出
* `duration_ms`：请求持续时间（以毫秒为单位）
* `input_tokens`：输入令牌数
* `output_tokens`：输出令牌数
* `cache_read_tokens`：从缓存读取的令牌数
* `cache_creation_tokens`：用于缓存创建的令牌数
* `request_id`：API 请求 ID，例如 `"req_011..."`，在[事件关联属性](#event-correlation-attributes)下描述。
* `client_request_id`：作为 `x-client-request-id` 请求头发送的客户端生成的 UUID；请参阅[事件关联属性](#event-correlation-attributes)表了解何时存在。需要 Claude Code v2.1.214 或更高版本
* `speed`：`"fast"` 或 `"normal"`，指示快速模式是否活跃
* `query_source`：发出请求的子系统，例如 `"repl_main_thread"`、`"compact"` 或子代理名称
* `effort`：应用于请求的[努力级别](/docs/zh-CN/model-config#adjust-effort-level)：`"low"`、`"medium"`、`"high"`、`"xhigh"` 或 `"max"`。当 Claude Code 不发送努力级别时不存在，例如在不支持努力的模型上。
* `agent.name`、`skill.name`、`plugin.name`、`marketplace.name`、`mcp_server.name`、`mcp_tool.name`：请求的技能、插件、代理和 MCP 属性。有关定义和编辑行为，请参阅[成本计数器](#cost-counter)。

<h4 id="api-error-event">
  API 错误事件
</h4>

当对 Claude 的 API 请求失败时记录。

**事件名称**：`claude_code.api_error`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"api_error"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `model`：使用的模型（例如，"claude-sonnet-5"）
* `error`：错误消息
* `status_code`：HTTP 状态代码作为数字。对于非 HTTP 错误（如连接失败）不存在。
* `duration_ms`：请求持续时间（以毫秒为单位）
* `attempt`：进行的总尝试次数，包括初始请求（`1` 表示没有重试发生）
* `request_id`：API 请求 ID，例如 `"req_011..."`，在[事件关联属性](#event-correlation-attributes)下描述。
* `client_request_id`：作为 `x-client-request-id` 请求头发送的客户端生成的 UUID。即使在超时或连接错误等失败从未产生服务器 `request_id` 时也可用；请参阅[事件关联属性](#event-correlation-attributes)表了解何时存在。需要 Claude Code v2.1.214 或更高版本
* `speed`：`"fast"` 或 `"normal"`，指示快速模式是否活跃
* `query_source`：发出请求的子系统，例如 `"repl_main_thread"`、`"compact"` 或子代理名称
* `effort`：应用于请求的[努力级别](/docs/zh-CN/model-config#adjust-effort-level)。当 Claude Code 不发送努力级别时不存在，例如在不支持努力的模型上。
* `agent.name`、`skill.name`、`plugin.name`、`marketplace.name`、`mcp_server.name`、`mcp_tool.name`：请求的技能、插件、代理和 MCP 属性。有关定义和编辑行为，请参阅[成本计数器](#cost-counter)。

<h4 id="api-refusal-event">
  API 拒绝事件
</h4>

当 API 请求返回 `stop_reason: "refusal"` 时记录。拒绝到达成功响应流而不是作为 HTTP 错误，因此 `api_error` 事件不会为它们触发。此事件让您跟踪拒绝频率并按与 `api_request` 和 `api_error` 相同的属性对拒绝进行分组。

**事件名称**：`claude_code.api_refusal`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"api_refusal"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `model`：来自请求的模型标识符
* `request_id`：API 请求 ID，例如 `"req_011..."`，在[事件关联属性](#event-correlation-attributes)下描述。
* `query_source`：发出请求的子系统，例如 `"repl_main_thread"`、`"compact"` 或子代理名称。有关定义，请参阅 [`api_request`](#api-request-event)。
* `speed`：当[快速模式](/docs/zh-CN/fast-mode)活跃时为 `"fast"`，或 `"normal"`
* `attempt`：重试尝试号。第一次尝试是 `1`。
* `effort`：应用于请求的[努力级别](/docs/zh-CN/model-config#adjust-effort-level)。当 Claude Code 不发送努力级别时不存在，例如在不支持努力的模型上。
* `server_fallback_hop`：当 API 的服务器端模型回退已经在不同的模型上重试此拒绝时为 `true`，因此用户没有看到此特定拒绝。当请求以拒绝结束时为 `false`。单个轮次可以发出一个 `true` 跳跃事件和稍后的 `false` 最终事件，当回退模型也拒绝时。
* `has_category`：当 API 响应携带 `stop_details.category` 为 `"cyber"`、`"bio"`、`"frontier_llm"` 或 `"reasoning_extraction"` 时为 `true`。当响应没有类别或值在该集合之外时为 `false`。当 `server_fallback_hop` 为 `true` 时不存在，因为跳跃块不携带 `stop_details`。
* `has_explanation`：当 API 响应携带 `stop_details.explanation` 时为 `true`，否则为 `false`。当 `server_fallback_hop` 为 `true` 时不存在。
* `category`：来自 API 响应的 `stop_details.category` 值。`"cyber"`、`"bio"`、`"frontier_llm"` 或 `"reasoning_extraction"` 之一。仅当设置了 `OTEL_LOG_TOOL_DETAILS=1` 且 `has_category` 为 `true` 时存在。
* `agent.name`、`skill.name`、`plugin.name`、`marketplace.name`、`mcp_server.name`、`mcp_tool.name`：请求的技能、插件、代理和 MCP 属性。有关定义和编辑行为，请参阅[成本计数器](#cost-counter)。

<h4 id="api-request-body-event">
  API 请求体事件
</h4>

当设置了 `OTEL_LOG_RAW_API_BODIES` 时，为每个 API 请求尝试记录。每个尝试发出一个事件，因此使用调整参数的重试各自产生自己的事件。

**事件名称**：`claude_code.api_request_body`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"api_request_body"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `body`：JSON 序列化的 Messages API 请求参数，例如系统提示、消息和工具，在内容限制处截断（默认 60 KB）。先前助手轮次中的扩展思考内容被编辑。仅在内联模式下发出（`OTEL_LOG_RAW_API_BODIES=1`）。
* `body_ref`：包含未截断体的 `<dir>/<uuid>.request.json` 文件的绝对路径。仅在文件模式下发出（`OTEL_LOG_RAW_API_BODIES=file:<dir>`）。
* `body_length`：未截断的体长度。当 `OTEL_LOG_RAW_API_BODIES=file:<dir>` 时为 UTF-8 字节，或当 `=1` 时为 UTF-16 代码单位
* `body_truncated`：当发生内联截断时为 `"true"`。在文件模式下不存在，当没有截断发生时不存在。
* `model`：来自请求参数的模型标识符
* `query_source`：发出请求的子系统（例如，`"compact"`）
* `request_body_id`：标识此尝试的请求体的 UUID。成功的尝试的 [`api_response_body` 事件](#api-response-body-event)携带相同的值，因此您可以将响应与产生它的确切请求配对。需要 Claude Code v2.1.274 或更高版本

<h4 id="api-response-body-event">
  API 响应体事件
</h4>

当设置了 `OTEL_LOG_RAW_API_BODIES` 时，为每个成功的 API 响应记录。

在文件模式下（`OTEL_LOG_RAW_API_BODIES=file:<dir>`），Claude Code 还为每个成功的响应向 `<dir>/index.jsonl` 追加一个 JSON 行，包含字段 `timestamp`、`session_id`、`query_source`、`model`、`request_id`、`message_id`、`message_uuid`、`request_file` 和 `response_file`。读取它以找到给定记录消息后面的请求和响应文件，而无需查询您的遥测后端。索引文件需要 Claude Code v2.1.274 或更高版本。

**事件名称**：`claude_code.api_response_body`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"api_response_body"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `body`：JSON 序列化的 Messages API 响应，包括 id、内容块、使用情况和停止原因，在内容限制处截断（默认 60 KB）。扩展思考内容被编辑。仅在内联模式下发出（`OTEL_LOG_RAW_API_BODIES=1`）。
* `body_ref`：包含未截断体的 `<dir>/<request_id>.response.json` 文件的绝对路径。仅在文件模式下发出（`OTEL_LOG_RAW_API_BODIES=file:<dir>`）。
* `body_length`：未截断的体长度。当 `OTEL_LOG_RAW_API_BODIES=file:<dir>` 时为 UTF-8 字节，或当 `=1` 时为 UTF-16 代码单位
* `body_truncated`：当发生内联截断时为 `"true"`。在文件模式下不存在，当没有截断发生时不存在。
* `model`：模型标识符
* `query_source`：发出请求的子系统
* `request_id`：API 请求 ID，例如 `"req_011..."`，在[事件关联属性](#event-correlation-attributes)下描述。
* `request_body_id`：此响应回答的 [`api_request_body` 事件](#api-request-body-event)的 `request_body_id`。需要 Claude Code v2.1.274 或更高版本
* `message.id`：API 分配给响应的消息 ID，响应体的 `id` 字段。需要 Claude Code v2.1.274 或更高版本
* `message.uuid`：响应的最终记录条目的 UUID。与 `request_body_id` 一起，它将记录消息链接到其后面的请求和响应体。需要 Claude Code v2.1.274 或更高版本

<h4 id="tool-decision-event">
  工具决策事件
</h4>

当进行工具权限决策时记录（接受/拒绝）。

**事件名称**：`claude_code.tool_decision`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"tool_decision"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `tool_name`：工具的名称（例如，"Read"、"Edit"、"Write"、"NotebookEdit"）
* `tool_use_id`：此工具调用的唯一标识符。与传递给钩子的 `tool_use_id` 匹配，允许 OTel 事件和钩子捕获数据之间的关联。
* `decision`：`"accept"` 或 `"reject"`
* `tool_source`：始终存在。工具的来源，作为 CLI 创作值的闭集。需要 Claude Code v2.1.214 或更高版本
  * `"builtin"`：CLI 自己的工具
  * `"mcp"`：MCP 服务器通常
  * `"sdk_host_builtin_mcp"`：内置于 Claude Desktop 本身的进程内服务器，在 Claude Desktop 拥有的会话中。Claude Desktop 拥有它从自己的入口点之一启动的会话，`claude-desktop`、`claude-desktop-3p` 或 `local-agent`，当该会话不是嵌套子时；嵌套会话，包括 Claude Code 本身生成的会话，将这些服务器报告为 `"mcp"`
* `source`：决策来自何处：
  * `"config"`：自动决定而不提示，基于项目设置、用户个人设置中的允许或拒绝规则、企业管理策略、`--allowedTools` 或 `--disallowedTools` 标志、活跃权限模式、来自同一交互式 CLI 会话中较早提示的会话范围授予，或因为工具本质上是安全的。事件不指示这些源中的哪一个匹配。Claude Code 还在权限提示请求本身失败时报告 `"config"`，例如当代理 SDK 的 [`canUseTool`](/docs/zh-CN/agent-sdk/typescript#canusetool) 回调或 [`--permission-prompt-tool`](/docs/zh-CN/cli-reference#cli-flags) 工具返回无效结果时，或当输入流在请求待处理时关闭时。在 v2.1.216 之前，Claude Code 将这些失败报告为 `"user_reject"`。
  * `"hook"`：`PreToolUse` 或 `PermissionRequest` 钩子返回了决策。
  * `"user_permanent"`：当用户在权限提示处选择"是，以后不要再问..."时发出，这会将允许规则保存到其个人设置。在交互式 CLI 中，这仅对该选择本身发出；稍后与保存的规则匹配的调用发出 `"config"`。在代理 SDK 或非交互式 `-p` 会话中，初始选择和稍后的规则匹配都发出 `"user_permanent"`。视为接受。
  * `"user_temporary"`：当用户在权限提示处选择"是"进行一次性批准时发出，或在文件编辑或读取提示处选择了为会话其余部分授予访问权限的选项时发出。在交互式 CLI 中，这仅对选择本身发出；稍后由该会话范围授予允许的调用发出 `"config"`。在代理 SDK 或非交互式 `-p` 会话中，选择和稍后的匹配都发出 `"user_temporary"`。视为接受。
  * `"user_abort"`：当用户在不回答的情况下关闭权限提示时发出。在代理 SDK 和非交互式 `-p` 会话中，这包括在 `canUseTool` 或 `--permission-prompt-tool` 权限请求待处理时中断轮次；在 v2.1.216 之前，Claude Code 将该中断报告为 `"user_reject"`。视为拒绝。
  * `"user_reject"`：当用户在提示时选择"否"时发出。在交互式 CLI 中，这仅对该选择本身发出；与用户个人设置中的拒绝规则匹配的调用发出 `"config"`。在代理 SDK 或非交互式 `-p` 会话中，与个人设置中的拒绝规则匹配的调用发出 `"user_reject"`。视为拒绝。
* `tool_parameters`（当 `OTEL_LOG_TOOL_DETAILS=1` 时）：包含工具特定参数的 JSON 字符串。与[工具结果事件](#tool-result-event)相同的形状，减去执行后字段如 `git_commit_id`。对于接受的调用，如果权限决策通过 `updatedInput` 重写工具输入，值可能与 `tool_result` 不同。使用此属性查看当 `decision` 为 `"reject"` 时哪个命令被拒绝。
  * 对于 `"sdk_host_builtin_mcp"` 工具：`mcp_server_name` 和 `mcp_tool_name` 即使在 `OTEL_LOG_TOOL_DETAILS` 关闭时也包含，因为主机应用定义这些名称；没有它们，对这些内置服务器之一的拒绝调用在默认流上将无法属性。对于用户配置的 MCP 服务器，事件的 `tool_name` 始终是字面 `"mcp_tool"`，服务器和工具名称仅在标志打开时出现在 `tool_parameters` 中；参数内容在任何地方都需要标志。需要 Claude Code v2.1.214 或更高版本
  * 对于 Bash 工具：包括 `bash_command`、`full_command`、`timeout`、`description`、`dangerouslyDisableSandbox`。桌面应用的工作区 bash 工具也将 `tool_name` 报告为 `Bash`，但仅包括 `bash_command`、`full_command` 和 `timeout`
  * 对于 MCP 工具：包括 `mcp_server_name`、`mcp_tool_name`
  * 对于技能工具：包括 `skill_name`
  * 对于代理工具或旧版任务工具：包括 `subagent_type`

<h4 id="permission-mode-changed-event">
  权限模式更改事件
</h4>

当权限模式更改时记录，例如从 `Shift+Tab` 循环、退出计划模式或自动模式门检查。

**事件名称**：`claude_code.permission_mode_changed`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"permission_mode_changed"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `from_mode`：前一个权限模式，例如 `"default"`、`"plan"`、`"acceptEdits"`、`"auto"` 或 `"bypassPermissions"`
* `to_mode`：新权限模式
* `trigger`：导致更改的原因。`"shift_tab"`、`"exit_plan_mode"`、`"auto_gate_denied"` 或 `"auto_opt_in"` 之一。当转换源自 SDK 或桥时不存在。

<h4 id="auth-event">
  认证事件
</h4>

当 `/login` 或 `/logout` 完成时记录。

**事件名称**：`claude_code.auth`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"auth"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `action`：`"login"` 或 `"logout"`
* `success`：`"true"` 或 `"false"`
* `auth_method`：认证方法，例如 `"oauth"`
* `error_category`：操作失败时的分类错误类型。原始错误消息永远不会包含
* `status_code`：操作因 HTTP 错误失败时的 HTTP 状态代码作为字符串

<h4 id="mcp-server-connection-event">
  MCP 服务器连接事件
</h4>

当 MCP 服务器连接、断开连接或连接失败时记录。

**事件名称**：`claude_code.mcp_server_connection`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"mcp_server_connection"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `status`：`"connected"`、`"failed"` 或 `"disconnected"`
* `transport_type`：服务器传输，例如 `"stdio"`、`"sse"` 或 `"http"`
* `server_scope`：服务器配置的范围，例如 `"user"`、`"project"` 或 `"local"`
* `duration_ms`：连接尝试持续时间（以毫秒为单位）
* `error_code`：连接失败时的错误代码
* `is_plugin`：当服务器由插件提供时为 `true`，否则为 `false`
* `plugin_id_hash`（当 `is_plugin` 为 `true` 时）：插件名称和市场的稳定哈希，用于按插件对事件进行分组而不暴露名称。Claude Code 按[插件加载事件](#plugin-loaded-event)下描述的方式计算它
* `plugin.name`（当 `is_plugin` 为 `true` 时）：提供服务器的插件的名称。对于第三方插件，除非设置了 `OTEL_LOG_TOOL_DETAILS=1`，否则值为字面字符串 `"third-party"`；这保护第三方插件名称默认不出现在日志中。来自官方 Anthropic 源的插件始终按名称标识。`plugin_id_hash` 和 `plugin.name` 属性流向您自己的监控后端，不会发送给 Anthropic
* `server_name`（当 `OTEL_LOG_TOOL_DETAILS=1` 时）：配置的服务器名称
* `error`（当 `OTEL_LOG_TOOL_DETAILS=1` 时）：连接失败时的完整错误消息

<h4 id="internal-error-event">
  内部错误事件
</h4>

当 Claude Code 捕获意外的内部错误时记录。仅记录错误类名和 errno 风格代码。错误消息和堆栈跟踪永远不会包含。在针对 Amazon Bedrock、Google Cloud 的代理平台或 Microsoft Foundry 运行时，或当设置了 `DISABLE_ERROR_REPORTING` 时，不发出此事件。

**事件名称**：`claude_code.internal_error`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"internal_error"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `error_name`：错误类名，例如 `"TypeError"` 或 `"SyntaxError"`
* `error_code`：Node.js errno 代码，例如 `"ENOENT"`（当存在于错误上时）

<h4 id="plugin-installed-event">
  插件已安装事件
</h4>

当插件完成安装时记录，来自 `claude plugin install` CLI 命令和交互式 `/plugin` UI。

**事件名称**：`claude_code.plugin_installed`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"plugin_installed"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `marketplace.is_official`：如果市场是官方 Anthropic 市场则为 `"true"`，否则为 `"false"`
* `install.trigger`：`"cli"` 或 `"ui"`
* `plugin.name`：已安装插件的名称。对于第三方市场，仅当设置了 `OTEL_LOG_TOOL_DETAILS=1` 时才包含
* `plugin.version`：在市场条目中声明时的插件版本。对于第三方市场，仅当设置了 `OTEL_LOG_TOOL_DETAILS=1` 时才包含
* `marketplace.name`：插件安装的市场。对于第三方市场，仅当设置了 `OTEL_LOG_TOOL_DETAILS=1` 时才包含

<h4 id="plugin-loaded-event">
  插件加载事件
</h4>

在会话开始时为每个启用的插件记录一次。使用此事件来清点您的整个舰队中哪些插件处于活跃状态，作为记录安装操作本身的 `plugin_installed` 的补充。

**事件名称**：`claude_code.plugin_loaded`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"plugin_loaded"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `plugin.name`：插件的名称。对于官方市场和内置捆绑之外的插件，除非设置了 `OTEL_LOG_TOOL_DETAILS=1`，否则值为 `"third-party"`
* `marketplace.name`：插件安装的市场（已知时）。在与 `plugin.name` 相同的条件下编辑为 `"third-party"`
* `plugin.version`：来自插件清单的版本。仅当名称未被编辑且清单声明版本时才包含
* `plugin.scope`：插件的来源类别：`"official"`、`"community"`、`"org"`、`"user-local"` 或 `"default-bundle"`
* `enabled_via`：插件如何被启用的方式：`"default-enable"`、`"org-policy"`、`"admin-install"`、`"seed-mount"` 或 `"user-install"`。`"admin-install"` 值表示插件在[**组织设置 > 插件和技能**](https://claude.ai/admin-settings/skills?tab=inventory)中为您的组织设置为必需或自动安装。在 v2.1.246 之前，Claude Code 将这些插件报告为 `"user-install"` 或 `"seed-mount"`
* `plugin_id_hash`：插件名称和市场的确定性哈希，仅发送到您配置的导出器。让您计算整个舰队中加载的不同第三方插件，而无需记录其名称。对于[从 claude.ai 同步的插件](/docs/zh-CN/plugins/loading#synced-plugins)，Claude Code 使用 claude.ai 为插件报告的市场名称或 `synced` 哈希插件名称。在 v2.1.246 之前，Claude Code 在哈希中没有使用 claude.ai 报告的市场名称
* `has_hooks`：插件是否贡献钩子
* `has_mcp`：插件是否贡献 MCP 服务器
* `host_owned_mcp`：当 SDK 主机管理此插件的 MCP 连接且 Claude Code 跳过读取插件的 MCP 服务器配置时为 `true`，否则为 `false`。需要 Claude Code v2.1.172 或更高版本
* `skill_path_count`：插件声明的技能目录数
* `command_path_count`：插件声明的命令目录数
* `agent_path_count`：插件声明的代理目录数
* `safe_mode`：当会话以 [`--safe-mode`](/docs/zh-CN/cli-reference) 启动时为 `"true"`，否则为 `"false"`。在安全模式下，此事件仅报告配置的清单；插件的命令、技能、钩子和 MCP 服务器不加载。需要 Claude Code v2.1.169 或更高版本

<h4 id="skill-activated-event">
  技能激活事件
</h4>

当技能被调用时记录，无论 Claude 是通过技能工具调用它还是您将其作为 `/` 命令运行。

**事件名称**：`claude_code.skill_activated`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"skill_activated"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `skill.name`：技能的名称。对于用户定义和第三方插件技能，除非设置了 `OTEL_LOG_TOOL_DETAILS=1`，否则值为占位符 `"custom_skill"`
* `invocation_trigger`：技能如何被触发（`"user-slash"`、`"claude-proactive"` 或 `"nested-skill"`）
* `skill.source`：技能从何处加载（例如，`"bundled"`、`"userSettings"`、`"projectSettings"`、`"plugin"`）
* `skill.kind`：当技能是工作流技能时为 `"workflow"`。否则不存在
* `plugin.name`（当 `OTEL_LOG_TOOL_DETAILS=1` 或插件来自官方市场时）：当技能由插件提供时的所有者插件的名称
* `marketplace.name`（当 `OTEL_LOG_TOOL_DETAILS=1` 或插件来自官方市场时）：当技能由插件提供时，所有者插件安装的市场

<h4 id="at-mention-event">
  @提及事件
</h4>

当 Claude Code 解析提示中的 `@` 提及时记录。并非每个提及都发出事件：早期退出路径如权限拒绝、超大文件、PDF 参考附件和目录列表失败返回而不记录。

**事件名称**：`claude_code.at_mention`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"at_mention"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `mention_type`：提及的类型（`"file"`、`"directory"`、`"agent"`、`"mcp_resource"`、`"peer"`）。`"peer"` 值表示您提及了[您的其他 Claude Code 会话之一](/docs/zh-CN/cross-session-messaging)。需要 Claude Code v2.1.232 或更高版本
* `success`：提及是否成功解析（`"true"` 或 `"false"`）

<h4 id="api-retries-exhausted-event">
  API 重试耗尽事件
</h4>

当 API 请求在多次尝试后失败时记录一次。与最终 `api_error` 事件一起发出。

**事件名称**：`claude_code.api_retries_exhausted`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"api_retries_exhausted"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `model`：使用的模型
* `error`：最终错误消息
* `status_code`：HTTP 状态代码作为数字。对于非 HTTP 错误不存在。
* `total_attempts`：进行的总尝试次数
* `total_retry_duration_ms`：所有尝试中的总挂钟时间
* `speed`：`"fast"` 或 `"normal"`

<h4 id="hook-registered-event">
  钩子已注册事件
</h4>

在会话开始时为每个配置的钩子记录一次。使用此事件来清点您的整个舰队中哪些钩子处于活跃状态，作为每次执行 `hook_execution_start` 和 `hook_execution_complete` 事件的补充。

**事件名称**：`claude_code.hook_registered`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"hook_registered"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `hook_event`：钩子事件类型，例如 `"PreToolUse"` 或 `"PostToolUse"`
* `hook_type`：钩子实现类型：`"command"`、`"prompt"`、`"mcp_tool"`、`"http"` 或 `"agent"`
* `hook_source`：钩子定义的位置：`"userSettings"`、`"projectSettings"`、`"localSettings"`、`"flagSettings"`、`"policySettings"` 或 `"pluginHook"`
* `safe_mode`：当会话以 [`--safe-mode`](/docs/zh-CN/cli-reference) 启动时为 `"true"`，否则为 `"false"`。需要 Claude Code v2.1.169 或更高版本
* `hook_matcher`（当 `OTEL_LOG_TOOL_DETAILS=1` 时）：钩子配置中的匹配器字符串（当设置了一个时）
* `plugin.name`（当 `hook_source` 为 `"pluginHook"` 时）：贡献插件的名称。对于官方市场和内置捆绑之外的插件，除非设置了 `OTEL_LOG_TOOL_DETAILS=1`，否则值为 `"third-party"`
* `plugin_id_hash`（当 `hook_source` 为 `"pluginHook"` 时）：插件名称和市场的确定性哈希，仅发送到您配置的导出器。让您计算不同的贡献插件而无需记录其名称。Claude Code 按[插件加载事件](#plugin-loaded-event)下描述的方式计算它

<h4 id="hook-execution-start-event">
  钩子执行开始事件
</h4>

当一个或多个钩子开始为钩子事件执行时记录。

**事件名称**：`claude_code.hook_execution_start`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"hook_execution_start"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `hook_event`：钩子事件类型，例如 `"PreToolUse"` 或 `"PostToolUse"`
* `hook_name`：完整钩子名称包括匹配器，例如 `"PreToolUse:Write"`
* `num_hooks`：匹配钩子命令的数量
* `managed_only`：当仅允许管理策略钩子时为 `"true"`
* `hook_source`：`"policySettings"` 或 `"merged"`
* `safe_mode`：当会话以 [`--safe-mode`](/docs/zh-CN/cli-reference) 启动时为 `"true"`，否则为 `"false"`。需要 Claude Code v2.1.169 或更高版本
* `hook_definitions`：JSON 序列化的钩子配置。仅当启用了详细的 beta 跟踪和 `OTEL_LOG_TOOL_DETAILS=1` 时才包含

<h4 id="hook-execution-complete-event">
  钩子执行完成事件
</h4>

当钩子事件的所有钩子完成时记录。

**事件名称**：`claude_code.hook_execution_complete`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"hook_execution_complete"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `hook_event`：钩子事件类型
* `hook_name`：完整钩子名称包括匹配器
* `num_hooks`：匹配钩子命令的数量
* `num_success`：成功完成的计数
* `num_blocking`：返回阻止决策的计数
* `num_non_blocking_error`：失败而不阻止的计数
* `num_cancelled`：在完成前取消的计数
* `total_duration_ms`：所有匹配钩子的挂钟持续时间
* `stdout_chars`：成功的匹配钩子中的 stdout 总字符数。需要 Claude Code v2.1.280 或更高版本
* `additional_context_chars`：匹配钩子返回的 `additionalContext` 的总字符数。需要 Claude Code v2.1.280 或更高版本
* `system_message_chars`：匹配钩子返回的 `systemMessage` 的总字符数。需要 Claude Code v2.1.280 或更高版本
* `initial_user_message_chars`：匹配钩子返回的 `initialUserMessage` 的总字符数。需要 Claude Code v2.1.280 或更高版本
* `num_outputs_persisted`：超过[10,000 字符上限](/docs/zh-CN/hooks#json-output)的钩子输出数，Claude Code 保存到文件。需要 Claude Code v2.1.280 或更高版本
* `managed_only`：当仅允许管理策略钩子时为 `"true"`
* `hook_source`：`"policySettings"` 或 `"merged"`
* `safe_mode`：当会话以 [`--safe-mode`](/docs/zh-CN/cli-reference) 启动时为 `"true"`，否则为 `"false"`。需要 Claude Code v2.1.169 或更高版本
* `hook_definitions`：JSON 序列化的钩子配置。仅当启用了详细的 beta 跟踪和 `OTEL_LOG_TOOL_DETAILS=1` 时才包含

<h4 id="hook-plugin-metrics-event">
  钩子插件指标事件
</h4>

当官方市场插件钩子发出每次调用指标时记录。仅从官方 Anthropic 市场安装的插件可以发出这些。第三方市场插件和用户配置的钩子不发出到此事件。使用此事件从您自己的可观测性堆栈监控插件行为，例如查找率、成本和持续时间。

**事件名称**：`claude_code.hook_plugin_metrics`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"hook_plugin_metrics"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `plugin_id`：`<name>@<marketplace>` 形式的插件标识符
* `hook_event`：发出指标的钩子事件类型
* 最多 20 个插件发出的指标键。名称匹配 `^[a-z][a-z0-9_]{0,39}$`。值是布尔值或数字。

<h4 id="compaction-event">
  压缩事件
</h4>

当对话压缩完成时记录。

**事件名称**：`claude_code.compaction`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"compaction"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `trigger`：`"auto"` 或 `"manual"`
* `success`：`"true"` 或 `"false"`
* `duration_ms`：压缩持续时间
* `pre_tokens`：压缩前的近似令牌计数
* `post_tokens`：压缩后的近似令牌计数
* `error`：压缩失败时的错误消息
* `precompute_reuse`：仅当 `trigger` 为 `"manual"` 时设置。自动压缩可以在上下文窗口填满之前在后台准备摘要，此属性记录 `/compact` 是否重用了该准备的摘要。`"hit"` 表示它被重用；`"miss_custom_instructions"`、`"miss_hook"` 和 `"miss_not_ready"` 给出改为计算新摘要的原因。需要 Claude Code v2.1.153 或更高版本

<h4 id="subagent-completed-event">
  子代理完成事件
</h4>

当[子代理](/docs/zh-CN/sub-agents)完成并将其结果返回到启动它的对话时记录。使用它按子代理类型汇总工具使用和运行时间；对于令牌或成本汇总，使用按 `query_source` `"subagent"` 过滤的[令牌计数器](#token-counter)和[成本计数器](#cost-counter)，因为此事件的 `total_tokens` 仅涵盖最终请求。`"subagent"` 类别也计算来自代理钩子的请求，它不发出子代理事件。

**事件名称**：`claude_code.subagent_completed`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"subagent_completed"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `agent_type`：子代理类型。内置代理名称和来自官方市场插件的代理逐字显示；其他代理名称被替换为 `"custom"`，除非设置了 `OTEL_LOG_TOOL_DETAILS=1`
* `agent.source`：代理定义来自何处：`built-in`、`plugin` 或定义自定义代理的设置源，例如 `userSettings` 或 `projectSettings`
* `is_built_in`：子代理是否是内置代理类型
* `is_async`：子代理是否在[后台](/docs/zh-CN/sub-agents#run-subagents-in-foreground-or-background)运行
* `total_tokens`：子代理最终 API 请求的令牌足迹：该一个请求的输入、缓存创建、缓存读取和输出令牌，大致是子代理在完成时的上下文大小。不是整个运行的总和
* `total_tool_uses`：子代理在整个运行中进行的工具调用数
* `duration_ms`：运行时间（以毫秒为单位）
* `model`：子代理被解析为运行的模型
* `final_model`：产生子代理最终响应的模型，在中途切换（如回退）后与 `model` 不同。需要 Claude Code v2.1.212 或更高版本
* `model_swapped`：是否有多个模型为子代理的请求提供服务。需要 Claude Code v2.1.212 或更高版本
* `plugin_id_hash`、`plugin.name`：对于插件提供的代理存在。官方市场插件名称逐字显示；其他插件名称被替换为 `"third-party"`，除非设置了 `OTEL_LOG_TOOL_DETAILS=1`

<h4 id="feedback-survey-event">
  反馈调查事件
</h4>

当显示或回答会话质量调查时记录。请参阅[会话质量调查](/docs/zh-CN/data-usage#session-quality-surveys)了解调查收集的内容以及如何控制它们。

**事件名称**：`claude_code.feedback_survey`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"feedback_survey"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `event_type`：调查生命周期事件，例如 `"appeared"`、`"responded"` 或 `"transcript_prompt_appeared"`
* `appearance_id`：链接为一个调查实例发出的事件的唯一 ID
* `survey_type`：哪个调查产生了事件。`"session"` 是"Claude 做得怎么样？"评分提示
* `response`：用户在 `responded` 事件上的选择
* `enabled_via_override`：当设置了 [`CLAUDE_CODE_ENABLE_FEEDBACK_SURVEY_FOR_OTEL`](/docs/zh-CN/env-vars) 时为 `true`。作为布尔值而不是字符串发出。存在于 `session` 调查事件上。在此属性上过滤以确认覆盖在整个舰队中应用

<h4 id="retention-sweep-event">
  保留扫描事件
</h4>

每次运行保留清理扫描时记录一次，该扫描删除[会话记录和其他应用数据](/docs/zh-CN/claude-directory#cleaned-up-automatically)早于 [`cleanupPeriodDays`](/docs/zh-CN/settings-reference#cleanupperioddays) 设置的数据。Claude Code 在后台最多每个会话运行一次扫描，删除任何内容的运行仍会发出事件。如果 Claude Code 在过去 24 小时内在同一台机器的任何会话中运行了扫描，它会将此会话的扫描延迟至少 10 分钟，因此更早退出的会话不发出任何内容。当您使用 `--bare` 运行 `claude -p` 时，Claude Code 不运行扫描，不发出任何内容。

像此页面上的每个 OTel 事件一样，它仅流向您配置的遥测后端。需要 Claude Code v2.1.227 或更高版本。

当 Claude Code 无法安全地确定保留期时，它暂停扫描并发出事件，`result` 设置为 `"skipped"` 和 `skip_reason`。当[管理设置](/docs/zh-CN/server-managed-settings)设置 `cleanupPeriodDays` 时，管理值固定保留期，扫描即使在较低优先级范围内的设置文件损坏或无效时也运行。当 `managed-settings.json` 本身无法读取时，Claude Code 仍暂停扫描，除非[管理层](/docs/zh-CN/managed-settings#how-claude-code-combines-managed-sources)从其他地方（如服务器管理设置或损坏文件旁的 `managed-settings.d/` 放入）提供 `cleanupPeriodDays`。删除计数器属性仅当 `result` 为 `"complete"` 时存在。

**事件名称**：`claude_code.retention_sweep`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"retention_sweep"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `result`：当扫描运行时为 `"complete"`，当 Claude Code 暂停它时为 `"skipped"`
* `period_days`：来自合并设置的 `cleanupPeriodDays` 值（以天为单位），或当没有源设置它时为 `30`。在跳过的事件上，扫描会使用的值，从 Claude Code 可以读取的设置源计算
* `used_default`：当没有可读的设置源设置 `cleanupPeriodDays` 时为 `"true"`，否则为 `"false"`。在完成事件上，`"true"` 表示应用了 30 天默认值
* `skip_reason`：Claude Code 暂停扫描的原因。仅当 `result` 为 `"skipped"` 时存在：
  * `"user_source_disabled"`：用户设置被排除，例如通过 [`--setting-sources`](/docs/zh-CN/cli-reference#cli-flags) 标志或 SDK 的 [`settingSources`](/docs/zh-CN/agent-sdk/typescript#options) 选项，且没有启用的源提供 `cleanupPeriodDays`
  * `"settings_unknowable"`：设置文件无法读取或解析，因此 `cleanupPeriodDays` 或 `desktopSessionCleanupPeriodDays` 可能设置为 Claude Code 无法看到的值
  * `"settings_invalid_key_set"`：设置有验证错误且 `cleanupPeriodDays` 或 `desktopSessionCleanupPeriodDays` 被显式设置，因此回退到默认值可能会删除或保留违反该设置的文件
* `transcripts_deleted`：扫描删除的会话记录数，顶级 `~/.claude/projects/*/*.jsonl` 文件
* `transcripts_exempted_desktop`：超过保留期的记录数，扫描在[Claude Desktop 和 Cowork 规则](/docs/zh-CN/claude-directory#cleaned-up-automatically)下保留。这些不计入 `files_past_cutoff`。需要 Claude Code v2.1.248 或更高版本
* `session_files_deleted`：会话文件扫描删除的工件数：记录加上每个会话的伴随文件，如侧边栏、录音和工具结果
* `artifacts_deleted`：扫描删除的数据目录中的总项目数，包括会话文件。某些扫描将整个删除的目录树计为一项，少数清理通过不贡献计数器，因此将值视为下限而不是精确文件计数
* `files_retained_fresh`：检查并保留在原地的文件，因为它们仍在保留期内。仅每个文件扫描计数这些，因此值是下限；非零值是正常稳定状态
* `files_past_cutoff`：早于保留期的文件，扫描无法删除，例如由于权限错误或文件被打开。值高于零表示文件超过了配置的保留期；零不是证明没有任何文件，因为整个目录的删除失败计入 `error_count`
* `error_count`：扫描在列出或删除文件时遇到的错误数

<h4 id="managed-settings-resolved-event">
  管理设置已解析事件
</h4>

使用会话解析的[管理设置](/docs/zh-CN/managed-settings)记录：在会话开始时一次，当管理设置或[策略助手](/docs/zh-CN/managed-settings#compute-the-policy-with-a-helper-program)的状态在会话期间更改时再次，以及当 Claude Code 拒绝启动或因 `error.type` 属性列出的原因之一而结束会话时。
使用此事件查找在意外管理源上运行的机器、策略助手失败的机器以及机器拒绝启动的原因。
需要 Claude Code v2.1.274 或更高版本。

默认情况下，事件携带管理源和策略助手的状态，但不携带设置本身。要添加编辑的 `managed_settings.settings` 属性和 `managed_settings.resolved_sha256` 摘要，请设置 `OTEL_LOG_MANAGED_SETTINGS=1`：

* 在管理设置、用户设置或 `--settings` 的 `env` 块中设置它，或在启动 Claude Code 的环境中。项目或本地设置中的值不会打开它，因为克隆的存储库可以写入它们。
* 服务器管理设置可以在不显示[安全批准对话](/docs/zh-CN/server-managed-settings#security-approval-dialogs)的情况下设置它，因为变量仅将您组织自己的编辑策略添加到您的组织已接收的事件。

在您尚未[信任](/docs/zh-CN/permissions#what-runs-before-you-trust-a-folder)的文件夹中的交互式会话中，Claude Code 不导出拒绝事件。

**事件名称**：`claude_code.managed_settings_resolved`

**属性**：

* 所有[标准属性](#standard-attributes)
* `event.name`：`"managed_settings_resolved"`
* `event.timestamp`：ISO 8601 时间戳
* `event.sequence`：用于排序事件的每进程计数器，在[事件关联属性](#event-correlation-attributes)下描述
* `managed_settings.trigger`：会话启动事件为 `"startup"`，当管理设置或策略助手的状态在会话后期更改时为 `"change"`，或当管理设置策略停止会话时为 `"refused"`。Claude Code 仅在属性与它发送的最后一个事件不同时发送 `change` 事件，更改的设置值即使 `OTEL_LOG_MANAGED_SETTINGS` 关闭也计数
* `error.type`：Claude Code 停止会话的原因。仅在 `refused` 事件上存在：
  * `"helper_failed"`：[策略助手运行失败](/docs/zh-CN/settings-reference#helper-failures)
  * `"policy_invalid"`：管理设置包含停止 Claude Code 启动的错误，或管理源无法加载，因此 Claude Code 无法检查组织登录强制
  * `"provider_not_allowed"`：会话将使用 API 提供商，或将提供商的流量发送到管理的 [`allowedProviders`](/docs/zh-CN/settings-reference#allowedproviders) 列表不允许的主机。需要 Claude Code v2.1.285 或更高版本
  * `"consent_rejected"`：用户拒绝了服务器管理设置的[安全批准对话](/docs/zh-CN/server-managed-settings#security-approval-dialogs)
  * `"force_refresh_failed"`：[`forceRemoteSettingsRefresh`](/docs/zh-CN/settings-reference#forceremotesettingsrefresh) 需要的设置获取失败
  * `"gateway_rejected"`：[Claude 应用网关](/docs/zh-CN/claude-apps-gateway)用 HTTP 403 回答了管理设置加载
  * `"version_below_minimum"`：此版本的 Claude Code 低于 [`requiredMinimumVersion`](/docs/zh-CN/settings-reference#requiredminimumversion) 或高于 [`requiredMaximumVersion`](/docs/zh-CN/settings-reference#requiredmaximumversion)
  * `"_OTHER"`：Claude 应用网关管理设置加载因另一个原因失败
* `managed_settings.sources`：每个传递至少一个[策略键](/docs/zh-CN/managed-settings#how-claude-code-combines-managed-sources)的管理源，优先级最高的优先，包括其键在 `first-wins` 下不生效的源。值为 `"remote"`、`"plist"` 或 `"hklm"` 用于 MDM 或 OS 级策略、`"file"` 用于管理设置文件和放入、`"parent"` 当[嵌入主机](/docs/zh-CN/managed-settings#let-an-embedding-host-add-policy)提供设置时，以及 `"hkcu"` 用于 Claude Code [读取](/docs/zh-CN/managed-settings#how-claude-code-combines-managed-sources)时的 [Windows HKCU 注册表值](/docs/zh-CN/managed-settings#where-each-mechanism-stores-the-policy)。仅携带策略键或 Claude Code 无法读取的源不列出。作为字符串数组发出，当没有管理源传递策略键时为空
* `managed_settings.source_behavior`：Claude Code 读取的 [`managedSourcesBehavior`](/docs/zh-CN/settings-reference#managedsourcesbehavior) 值，`"first-wins"` 或 `"merge"`。当没有源设置键时为 `"first-wins"`
* `managed_settings.helper.state`：所选 MDM 或文件源配置的策略助手的状态：
  * `"ok"`：助手的输出作为管理设置
  * `"bad_path"`、`"not_a_file"`、`"exit_nonzero"`、`"timed_out"`、`"oversize"`、`"parse_failed"`、`"envelope_invalid"` 或 `"schema_rejected"`：助手的最后一次运行失败。[助手失败](/docs/zh-CN/settings-reference#helper-failures)描述了这些情况
  * `"none"`：没有配置助手，或配置它的源不是 MDM 策略或管理设置文件
* `managed_settings.helper.applied`：当助手自己的输出作为管理设置时为 `"output"`，当它不时为 `"none"`
* `managed_settings.helper.entry`：当 Claude Code 选择了 [`policyHelper`](/docs/zh-CN/settings-reference#policyhelper) 时为 `"policyHelper"`。当它选择了没有助手时不存在
* `managed_settings.helper.path`：助手的配置 [`path`](/docs/zh-CN/settings-reference#policyhelper-path)。每当 Claude Code 选择了助手时存在，无论 `OTEL_LOG_MANAGED_SETTINGS` 是否设置
* `managed_settings.resolved_sha256`（当 `OTEL_LOG_MANAGED_SETTINGS=1` 时）：编辑前解析的管理设置的 SHA-256，序列化为 JSON，键递归排序，无空格。具有相同摘要的机器运行相同的策略。Claude Code 仅使用选择加入发送摘要，因为短策略可以通过哈希猜测恢复。当没有管理设置解析时不存在，在 `refused` 事件上不存在
* `managed_settings.settings`（当 `OTEL_LOG_MANAGED_SETTINGS=1` 时）：解析的管理设置的名称和形状作为 JSON 字符串，值被编辑。在 `refused` 事件上不存在。Claude Code 从其设置架构构建它：

  * 架构声明导出的设置名称，架构不声明的键被留出
  * 布尔值、数字和字符串值，架构限制为固定选项集，例如 `permissions.defaultMode`，按原样导出。`sandbox.network.httpProxyPort` 和 `sandbox.network.socksProxyPort` 导出为 `"[REDACTED]"`
  * 每个其他字符串，例如 `model`、`apiKeyHelper`、每个 `env` 值、每个 URL 和每个命令，导出为 `"[REDACTED]"`
  * 地图的条目名称，例如 `env` 变量名称和插件 ID，按原样导出。架构不键入其条目的设置，例如 `vimInsertModeRemaps`，导出为单个 `"[REDACTED]"`，`sandbox.ignoreViolations` 导出为其路径列表的列表，不带命令模式
  * 列表保留其长度，每个条目按相同规则编辑
  * `permissions.allow`、`permissions.deny` 或 `permissions.ask` 规则导出为其工具名称，内容编辑，例如 `Read([REDACTED])`，当工具内置于此版本的 Claude Code 或是 `mcp__` 参考（如 `mcp__jira__create_issue`）时。任何其他规则导出为 `"[REDACTED]"`
  * 钩子遵循相同的规则，因此固定选项和数字字段（如 `type` 和 `timeout`）显示，而每个命令、URL、`matcher` 和 `if` 条件导出为 `"[REDACTED]"`

  例如，具有 `apiKeyHelper`、两个 `env` 变量和拒绝规则的管理设置导出为 `{"apiKeyHelper":"[REDACTED]","env":{"HTTPS_PROXY":"[REDACTED]","CLAUDE_CODE_ENABLE_TELEMETRY":"[REDACTED]"},"permissions":{"deny":["Read([REDACTED])"]}}`.

  Claude Code 在 8 KB UTF-8 处切割值，切割值不是有效的 JSON
* `managed_settings.settings_truncated`（当 `managed_settings.settings` 存在时）：当 Claude Code 在 8 KB 处切割 `managed_settings.settings` 时为 `true`，否则为 `false`。作为布尔值而不是字符串发出

<h2 id="interpret-metrics-and-events-data">
  解释指标和事件数据
</h2>

导出的指标和事件支持一系列分析：

<h3 id="usage-monitoring">
  使用情况监控
</h3>

| 指标 | 分析机会 |
| - | - |
| `claude_code.token.usage` | 按 `type`（输入/输出）、用户、团队、模型、`skill.name`、`plugin.name` 或 `agent.name` 分解 |
| `claude_code.session.count` | 跟踪随时间推移的采用和参与度 |
| `claude_code.lines_of_code.count` | 通过跟踪代码添加和删除来衡量生产力，按模型分解 |
| `claude_code.commit.count` & `claude_code.pull_request.count` | 了解对开发工作流的影响 |

<h3 id="cost-monitoring">
  成本监控
</h3>

`claude_code.cost.usage` 指标有助于：

* 跟踪团队或个人的使用趋势
* 识别高使用会话以进行优化
* 通过 `skill.name`、`plugin.name` 和 `agent.name` 属性将支出归属于特定技能、插件或子代理类型

<Note>
  成本指标是近似值。有关官方计费数据，请参阅您的 API 提供商（Claude 控制台、Amazon Bedrock 或 Google Cloud 的 Agent Platform）。
</Note>

Claude Code 将每个流式响应计入成本和令牌指标，恰好一次，包括当网关或代理在 `ANTHROPIC_BASE_URL` 后面跨多个帧逐步流式传输使用情况时。在 v2.1.214 之前，在多个帧中携带使用情况的流会使 `claude_code.cost.usage` 和 `claude_code.token.usage` 膨胀，大约每个额外帧增加一个完整请求。

<h3 id="alerting-and-segmentation">
  警报和分段
</h3>

要考虑的常见警报：

* 成本激增
* 异常的令牌消耗
* 来自特定用户的高会话量

所有指标都可以按[标准属性](#standard-attributes)进行分段。`model` 属性在 `claude_code.token.usage`、`claude_code.cost.usage` 上可用，以及 从 v2.1.172 开始，`claude_code.lines_of_code.count` 上也可用。

按模型的提交分解只能通过在 `session.id` 上与令牌或成本指标进行联接来近似，因为一个会话可以跨越多个模型。筛选令牌或成本端的行，使 `query_source` 为 `"main"`，以便辅助和子代理请求不会将会话的提交归属于未进行这些提交的模型。

<h3 id="detect-retry-exhaustion">
  检测重试耗尽
</h3>

Claude Code 在内部重试失败的 API 请求，仅在放弃后才发出单个 `claude_code.api_error` 事件，因此事件本身是该请求的终端信号。中间重试尝试不会作为单独的事件记录。

事件上的 `attempt` 属性记录进行的总尝试次数。`CLAUDE_CODE_MAX_RETRIES` 默认为 10，上限为 15。在 v2.1.199 或更高版本上，您可以设置 `CLAUDE_CODE_RETRY_WATCHDOG` 来提高默认值并移除上限。

当请求在瞬时错误上耗尽所有重试时，`attempt` 等于该有效限制加一：默认为 11，除非设置了看门狗，否则永远不超过 16。较低的值表示不可重试的错误，例如 `400` 响应，或具有自己较小重试预算的原因。例如，Claude Code 最多重试两次加载 AWS 或 Google Cloud 凭证的失败。

要区分从一个恢复的会话与停滞的会话，按 `session.id` 分组事件，并检查错误后是否存在更晚的 `api_request` 事件。

<h3 id="event-analysis">
  事件分析
</h3>

事件数据提供了对 Claude Code 交互的详细见解：

**工具使用模式**：分析工具结果事件以识别：

* 最常用的工具
* 工具成功率
* 平均工具执行时间
* 按工具类型的错误模式

**性能监控**：跟踪 API 请求持续时间和工具执行时间以识别性能瓶颈。

<h2 id="audit-security-events">
  审计安全事件
</h2>

OpenTelemetry 事件是 Claude Code 活动的审计数据源。每个事件都携带身份属性，将工具调用、MCP 活动和权限决策与触发它们的用户联系起来。OTLP 日志导出器可以将这些事件传递到任何具有 OTLP 接收器的安全信息和事件管理 (SIEM) 平台，或转发到您的 SIEM 的 OpenTelemetry Collector。

<h3 id="attribute-actions-to-users">
  将属性操作归属于用户
</h3>

每个事件上的 [标准属性](#standard-attributes) 包括已认证用户的身份：`user.email`、`user.account_uuid`、`user.account_id` 和 `organization.id`（使用 Claude 账户登录时或在 [云会话](/docs/zh-CN/claude-code-on-the-web) 中，当会话自己的凭证携带它们时），加上 `user.id` 和每会话的 `session.id`。`user.id` 是安装范围的标识符，除了在 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway) 会话上通过 `/login` 登录时，其中它是来自网关颁发的令牌的 IdP 主体。

在开发人员启动的会话中，MCP 工具调用、Bash 命令和文件编辑因此归属于该开发人员。Claude Code 不在单独的服务账户下运行；每个事件上记录的身份是开发人员自己的 Claude 账户，或开发人员在 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway) 会话上的 IdP 身份。在 Claude Tag 频道会话中，Claude 改为作为您组织的 [共享身份](/docs/zh-CN/cloud-environments#set-the-environment-a-claude-tag-channel-uses) 工作。

当 Claude Code 使用直接 API 密钥进行身份验证，或针对 Amazon Bedrock、Google Cloud 的 Agent Platform 或 Microsoft Foundry 进行身份验证时，会话中没有 Claude 账户，仅填充 `user.id` 和 `session.id`。在这些部署中，使用 `OTEL_RESOURCE_ATTRIBUTES` 自己附加用户身份，通过 [托管设置](#administrator-configuration) 文件或启动包装器按用户设置。Claude apps gateway 会话不需要任何这些：请参阅 [标准属性](#standard-attributes) 了解其导出携带的身份。

```bash theme={null}
export OTEL_RESOURCE_ATTRIBUTES="enduser.id=jdoe@example.com,enduser.directory_id=S-1-5-21-..."
```

<h3 id="audit-mcp-activity">
  审计 MCP 活动
</h3>

要使用完整的调用详情捕获 MCP 服务器活动，启用日志导出器并设置 `OTEL_LOG_TOOL_DETAILS=1`。每个 MCP 操作然后产生结构化事件，携带服务器名称、工具名称和调用参数以及标准身份属性：

| 事件 | 它为 MCP 记录的内容 |
| - | - |
| `mcp_server_connection` | 服务器连接、断开连接和连接失败，带有 `server_name`、`transport_type`、`server_scope` 和错误详情 |
| `tool_result` | 每个 MCP 工具调用，带有 `tool_name` 和 `mcp_server_scope`，包含 `mcp_server_name` 和 `mcp_tool_name` 的 `tool_parameters` 有效负载，以及包含调用参数的 `tool_input` 有效负载 |
| `tool_decision` | 调用是否被允许或拒绝，以及决策是来自配置、hook 还是用户，以及包含 `mcp_server_name` 和 `mcp_tool_name` 的 `tool_parameters` 有效负载 |

没有 `OTEL_LOG_TOOL_DETAILS`，这些事件会丢弃识别详情：

* `tool_result`：保留 `mcp_server_scope` 和一个对用户配置的服务器编辑为字面值 `"mcp_tool"` 的 `tool_name`，省略参数内容。对于 Claude Desktop 的内置服务器，在 Claude Desktop 拥有的会话中，它还保留 `tool_parameters` 内的 `mcp_server_name`/`mcp_tool_name` 对，与 `tool_decision` 相同的主机编写异常，需要 Claude Code v2.1.214 或更高版本
* `tool_decision`：保留 `tool_source` 和一个对用户配置的服务器编辑为字面值 `"mcp_tool"` 的 `tool_name`，省略参数内容。对于 Claude Desktop 的内置服务器，在 Claude Desktop 拥有的会话中，它还保留 `tool_parameters` 内的 `mcp_server_name`/`mcp_tool_name` 对；`tool_source` 和名称对都需要 Claude Code v2.1.214 或更高版本
* `mcp_server_connection`：省略 `server_name` 和错误消息，但保留 `is_plugin`、`plugin_id_hash` 和 `plugin.name`，非 Anthropic 插件名称被编辑为字面值 `"third-party"`，因此插件提供的服务器在没有详细日志的情况下仍然可以区分

<h3 id="map-security-questions-to-events">
  将安全问题映射到事件
</h3>

构建检测规则时，查找您想要监控的信号并查询您的后端以获取相应的事件和属性：

| 信号 | 事件 | 关键属性 |
| - | - | - |
| 工具调用被允许或拒绝，以及通过什么 | `tool_decision` | `decision`、`source`、`tool_name`、`tool_parameters` |
| 权限模式升级 | `permission_mode_changed` | `from_mode`、`to_mode`、`trigger` |
| 策略 hook 阻止了操作 | `hook_execution_complete` | `hook_event`、`num_blocking` |
| 登录、登出和身份验证失败 | `auth` | `action`、`success`、`error_category` |
| MCP 服务器连接或失败 | `mcp_server_connection` | `status`、`server_name`、`is_plugin`、`error_code` |
| 插件已安装及其来源 | `plugin_installed` | `plugin.name`、`marketplace.name`、`marketplace.is_official` |
| 运行的命令和触及的文件 | `tool_result`（已执行）或 `tool_decision`（已拒绝），带有 `OTEL_LOG_TOOL_DETAILS=1` | `tool_parameters`；`tool_input`（仅 `tool_result`） |
| 托管设置源机器运行的内容、其策略助手是否健康，以及机器拒绝启动的原因 | `managed_settings_resolved` | `managed_settings.trigger`、`managed_settings.sources`、`managed_settings.source_behavior`、`managed_settings.helper.state`、`error.type`；`managed_settings.settings` 和 `managed_settings.resolved_sha256`，带有 `OTEL_LOG_MANAGED_SETTINGS=1` |

Claude Code 仅发出原始事件流。异常检测、基线化、跨会话关联和警报是您的 SIEM 或可观测性后端的责任。

<h3 id="send-events-to-a-siem">
  将事件发送到 SIEM
</h3>

将 `OTEL_EXPORTER_OTLP_LOGS_ENDPOINT` 指向您的 SIEM 的 OTLP 接收器，或指向转发到您的 SIEM 的本机摄取 API 的 OpenTelemetry Collector。以下托管设置示例仅导出事件，启用了完整的工具详情用于 MCP 和 Bash 审计：

```json theme={null}
{
  "env": {
    "CLAUDE_CODE_ENABLE_TELEMETRY": "1",
    "OTEL_LOGS_EXPORTER": "otlp",
    "OTEL_LOG_TOOL_DETAILS": "1",
    "OTEL_EXPORTER_OTLP_LOGS_PROTOCOL": "http/protobuf",
    "OTEL_EXPORTER_OTLP_LOGS_ENDPOINT": "https://siem.example.com:4318/v1/logs",
    "OTEL_EXPORTER_OTLP_HEADERS": "Authorization=Bearer your-siem-token"
  }
}
```

要确认事件到达，在运行此配置的会话中提交提示，并在您的 SIEM 中检查 `claude_code.user_prompt` 事件。如果没有任何内容到达，使用 `claude --debug-file <path>` 启动 Claude Code 并在该日志中检查 `[3P telemetry]` 导出错误。

<h2 id="backend-considerations">
  后端考虑事项
</h2>

您选择的指标、日志和跟踪后端决定了您可以执行的分析类型：

<h3 id="for-metrics">
  对于指标
</h3>

* **时间序列数据库**：速率计算、聚合指标
* **列式存储**：复杂查询、唯一用户分析
* **全功能可观测性平台**：高级查询、可视化、警报

<h3 id="for-events/logs">
  对于事件/日志
</h3>

* **日志聚合系统**：全文搜索、日志分析
* **列式存储**：结构化事件分析
* **全功能可观测性平台**：指标和事件之间的关联

<h3 id="for-traces">
  对于跟踪
</h3>

选择支持分布式跟踪存储和 span 关联的后端：

* **分布式跟踪系统**：Span 可视化、请求瀑布、延迟分析
* **全功能可观测性平台**：跟踪搜索和与指标和日志的关联

对于需要日活跃用户/周活跃用户/月活跃用户 (DAU/WAU/MAU) 指标的组织，请考虑支持高效唯一值查询的后端。

<h2 id="service-information">
  服务信息
</h2>

所有指标和事件都使用以下资源属性导出：

* `service.name`：终端会话为 `claude-code`，从 [Claude Desktop 应用](/docs/zh-CN/desktop)中的代码选项卡启动的会话为 `claude-code-desktop`
* `service.version`：当前 Claude Code 版本，或代码选项卡会话的 Desktop 应用版本
* `os.type`：操作系统类型（例如，`linux`、`darwin`、`windows`）
* `os.version`：操作系统版本字符串
* `host.arch`：主机架构（例如，`amd64`、`arm64`）
* `wsl.version`：WSL 版本号（仅在 Windows Subsystem for Linux 上运行时出现）
* 仪表名称：`com.anthropic.claude_code`

如果您的收集器管道或仪表板在 `service.name = claude-code` 上进行过滤，请将 `claude-code-desktop` 添加到过滤器中，以便也捕获来自代码选项卡会话的遥测数据。

<h2 id="roi-measurement-resources">
  ROI 测量资源
</h2>

有关测量 Claude Code 投资回报率的综合指南，包括遥测设置、成本分析、生产力指标和自动化报告，请参阅 [Claude Code ROI 测量指南](https://github.com/anthropics/claude-code-monitoring-guide)。此存储库提供了现成的 Docker Compose 配置、Prometheus 和 OpenTelemetry 设置，以及用于生成与 Linear 等工具集成的生产力报告的模板。

<h2 id="security-and-privacy">
  安全和隐私
</h2>

* OpenTelemetry 导出到您的后端是可选的，需要显式配置。有关 Anthropic 的单独操作遥测以及如何禁用它，请参阅 [数据使用](/docs/zh-CN/data-usage#telemetry-services)
* 原始文件内容和代码片段不包含在指标或事件中。Trace spans 是一个单独的数据路径：请参阅下面的 `OTEL_LOG_TOOL_CONTENT` 项目符号
* 通过 OAuth 认证时，`user.email` 包含在遥测属性中，仅发送到您配置的 OTel 端点，永远不会发送到 Anthropic。如果这对您的组织是一个问题，请与您的遥测后端合作以过滤或编辑此字段
* 默认情况下不收集用户提示内容。仅记录提示长度。要包含提示内容，请设置 `OTEL_LOG_USER_PROMPTS=1`。在详细的 beta 追踪下，此变量的作用范围更广：它还控制 [`new_context` span 属性](#new-context-gates)，该属性在 `claude_code.llm_request` span 上携带工具结果
* 默认情况下不收集助手响应文本。仅记录响应长度。要包含响应文本，请设置 `OTEL_LOG_ASSISTANT_RESPONSES=1`。与来自 Claude Code 的所有 OpenTelemetry 数据一样，响应文本仅发送到您配置的 OTel 端点，永远不会发送到 Anthropic。当此变量未设置时，`OTEL_LOG_USER_PROMPTS` 用作后备，因此如果您想要提示内容而不要响应内容，请设置 `OTEL_LOG_ASSISTANT_RESPONSES=0`
* 默认情况下不记录工具输入参数和参数。要包含它们，请设置 `OTEL_LOG_TOOL_DETAILS=1`。对于 Claude Desktop 的内置服务器，在 Claude Desktop 拥有的会话中，`tool_decision` 和 `tool_result` 携带 `mcp_server_name`/`mcp_tool_name` 对，即主机编写的名称而非参数内容，即使关闭该标志也是如此。此异常需要 Claude Code v2.1.214 或更高版本。此数据仅发送到您配置的 OTEL 端点，永远不会发送到 Anthropic。参数仍可能包含敏感值，因此请根据需要配置您的遥测后端以过滤或编辑这些属性。启用后：
  * `tool_result` 和 `tool_decision` 事件包含 `tool_parameters` 属性，其中包含 Bash 命令、MCP 服务器和工具名称以及技能名称。`full_command` 等字段以未截断的形式发出
  * `tool_result` 事件另外包含 `tool_input` 属性，其中包含文件路径、URL、搜索模式和其他参数。超过 512 个字符的单个值被截断，总数限制为约 4 K 字符
  * `user_prompt` 事件包含自定义、插件和 MCP 命令的逐字 `command_name`
  * [成本和令牌计数器](#cost-counter)以及 `api_request`、`api_error` 和 `api_refusal` 事件在其归属属性中携带真实的代理、技能、插件和 MCP 服务器以及工具名称
  * Trace spans 包含相同的 `tool_input` 属性和输入派生属性（如 `file_path`），与 `tool_input` 的截断方式相同
* 默认情况下，trace spans 中不记录工具内容。要包含它，请设置 `OTEL_LOG_TOOL_CONTENT=1`。`claude_code.tool` span 随后携带一个 [`tool.output` span 事件](#tool-output-span-event)，其中包含原始文件内容、Bash 命令输出以及 MCP 工具、WebFetch 和 WebSearch 返回的内容，在内容限制处截断（默认为 60 KB）每个属性。来自 MCP 工具、WebFetch 和 WebSearch 的结果需要 Claude Code v2.1.283 或更高版本。工具内容也通过 [`new_context` 到达 spans，其门控因 span 而异](#new-context-gates)。根据需要配置您的遥测后端以过滤或编辑这些属性
* 默认情况下不记录原始 Anthropic Messages API 请求和响应主体。要包含它们，请在您的 shell、用户设置或托管设置中设置 `OTEL_LOG_RAW_API_BODIES`。在 [项目和本地设置](/docs/zh-CN/settings-reference#variables-claude-code-ignores-in-env) 中被忽略。主体包含完整的对话历史，包括系统提示、每个先前的用户和助手轮次以及工具结果，因此启用此选项意味着同意其他 `OTEL_LOG_*` 内容标志会揭示的所有内容。Claude Code 始终从这些主体中编辑 Claude 的扩展思考内容，无论其他设置如何。您设置的值决定了 Claude Code 如何传递主体：
  * 使用 `=1` 时，Claude Code 为每个 API 调用发出 `api_request_body` 和 `api_response_body` 日志事件。事件的 `body` 属性携带 JSON 序列化的有效负载，在内容限制处截断（默认为 60 KB）
  * 使用 `=file:<dir>` 时，Claude Code 将未截断的主体写入该目录下的 `.request.json` 和 `.response.json` 文件，事件携带 `body_ref` 路径而不是内联主体。使用日志收集器或 sidecar 传输目录，而不是通过遥测流

    对于每个成功的响应，Claude Code 还会在该目录中的 `index.jsonl` 中追加一行，将响应文件链接到生成它的请求文件以及它成为的记录消息。每行不包含任何消息内容，[API 响应主体事件](#api-response-body-event)部分列出了其字段。索引文件需要 Claude Code v2.1.274 或更高版本

<h2 id="monitor-claude-code-on-amazon-bedrock">
  在 Amazon Bedrock 上监控 Claude Code
</h2>

有关 Amazon Bedrock 的 Claude Code 使用情况监控指南的详细信息，请参阅 [Claude Code 监控实现 (Amazon Bedrock)](https://github.com/aws-solutions-library-samples/guidance-for-claude-code-with-amazon-bedrock/blob/main/assets/docs/MONITORING.md)。
