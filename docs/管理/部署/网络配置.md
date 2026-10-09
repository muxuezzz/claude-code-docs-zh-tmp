> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 企业网络配置

> 为企业环境配置 Claude Code，支持代理服务器、自定义证书颁发机构 (CA) 和相互传输层安全 (mTLS) 身份验证。

Claude Code 通过环境变量支持各种企业网络和安全配置。这包括通过公司代理服务器路由流量、信任自定义证书颁发机构 (CA)，以及使用相互传输层安全 (mTLS) 证书进行身份验证以增强安全性。

在启动 Claude Code 之前设置这些环境变量。在 shell 中导出的变量在启动时读取一次，因此运行中的会话不会获取 shell 环境的后续更改。

<Note>
  本页面显示的所有环境变量也可以在 [`settings.json`](/docs/zh-CN/settings) 中配置。
</Note>

<h2 id="proxy-configuration">
  代理配置
</h2>

<h3 id="environment-variables">
  环境变量
</h3>

Claude Code 遵守标准代理环境变量。在 Claude Desktop 会话中，当应用管理提供商连接时，Claude Code 仅从托管设置和 `~/.claude/settings.json` 中读取它们；有关范围规则，请参阅 [mTLS 身份验证](#mtls-authentication)。

```bash theme={null}
# HTTPS 代理（推荐）
export HTTPS_PROXY=https://proxy.example.com:8080

# HTTP 代理（如果 HTTPS 不可用）
export HTTP_PROXY=http://proxy.example.com:8080

# 绕过特定请求的代理 - 空格分隔格式
export NO_PROXY="localhost 192.168.1.1 example.com .example.com"
# 绕过特定请求的代理 - 逗号分隔格式
export NO_PROXY="localhost,192.168.1.1,example.com,.example.com"
# 绕过所有请求的代理
export NO_PROXY="*"
```

小写变体也可以工作，Claude Code 按照 `https_proxy`、`HTTPS_PROXY`、`http_proxy`、`HTTP_PROXY` 的顺序使用第一个已设置的变量。

Claude Code 永远不会通过代理发送其 WebSocket 连接到 `localhost`、`::1` 或 `127.0.0.0/8`，因此您不需要在 `NO_PROXY` 中为它们添加环回条目。

<Note>
  Claude Code 不支持 SOCKS 代理。
</Note>

<h3 id="basic-authentication">
  基本身份验证
</h3>

如果您的代理需要基本身份验证，请在代理 URL 中包含凭证：

```bash theme={null}
export HTTPS_PROXY=http://username:password@proxy.example.com:8080
```

<Warning>
  避免在脚本中硬编码密码。改用环境变量或安全凭证存储。
</Warning>

<Tip>
  对于需要高级身份验证（NTLM、Kerberos 等）的代理，请考虑使用支持您的身份验证方法的 LLM 网关服务。
</Tip>

<h2 id="ca-certificate-store">
  CA 证书存储
</h2>

默认情况下，Claude Code 信任其捆绑的 Mozilla CA 证书和您的操作系统的证书存储。读取操作系统存储需要具有 `tls.getCACertificates` 的运行时：本机安装程序始终具有它，npm 安装需要 Node 22.15 或更高版本。在较旧的 Node 版本上，仅捆绑的集合和 `NODE_EXTRA_CA_CERTS` 适用。企业 TLS 检查代理在其根证书安装在操作系统信任存储中且运行时可以读取它时无需额外配置即可工作。如果此类代理无法正确处理 gzip 压缩的请求正文，请设置 [`CLAUDE_CODE_GZIP_REQUEST_BODIES=0`](/docs/zh-CN/env-vars)，以关闭 Claude API、遥测和 Artifact 发布请求的压缩。

`CLAUDE_CODE_CERT_STORE` 接受逗号分隔的源列表。识别的值为 `bundled`（Claude Code 附带的 Mozilla CA 集）和 `system`（操作系统信任存储）。默认值为 `bundled,system`。

仅信任捆绑的 Mozilla CA 集：

```bash theme={null}
export CLAUDE_CODE_CERT_STORE=bundled
```

仅信任操作系统证书存储：

```bash theme={null}
export CLAUDE_CODE_CERT_STORE=system
```

<Note>
  `CLAUDE_CODE_CERT_STORE` 没有专用的 `settings.json` 架构密钥。通过 `~/.claude/settings.json` 中的 `env` 块或直接在进程环境中设置它。
</Note>

<h2 id="custom-ca-certificates">
  自定义 CA 证书
</h2>

如果您的企业环境使用自定义 CA，请配置 Claude Code 以直接信任它：

```bash theme={null}
export NODE_EXTRA_CA_CERTS=/path/to/ca-cert.pem
```

<h2 id="mtls-authentication">
  mTLS 身份验证
</h2>

对于需要客户端证书身份验证的企业环境：

```bash theme={null}
# 用于身份验证的客户端证书
export CLAUDE_CODE_CLIENT_CERT=/path/to/client-cert.pem

# 客户端私钥
export CLAUDE_CODE_CLIENT_KEY=/path/to/client-key.pem

# 可选：加密私钥的密码短语
export CLAUDE_CODE_CLIENT_KEY_PASSPHRASE="your-passphrase"
```

Claude Code 在启动时读取证书和密钥文件，并在每次应用设置时重新读取它们，例如当您的组织在会话中期更改[托管设置](/docs/zh-CN/server-managed-settings)中的 `env` 块时。

要轮换证书和密钥，请替换相同路径上的文件。Claude Code 在运行会话中无需重启即可获取替换。当 API 请求因连接级错误（如连接重置或 TLS 握手错误）失败时，它会重新读取两个文件并使用新的密钥对重试请求。在 v2.1.232 之前，Claude Code 不会在连接错误时重新读取，因此它会保持已加载的密钥对，直到下次应用设置或您重启为止。

Claude Code 根据失败的请求重新读取文件，而不是通过监视文件更改：

* **时间**：Claude Code 在您替换文件时不执行任何操作。它在符合条件的失败后的重试时或在下次应用设置时呈现新的密钥对，以先发生者为准。
* **网关拒绝**：当您的网关重置连接或在停止接受旧密钥对后拒绝 TLS 握手时，Claude Code 会重新读取。当网关完成握手并用 HTTP 错误响应时，它不会重新读取。在这种情况下，Claude Code 在下次应用设置时或重启时加载新的密钥对。
* **半写入轮换**：当 Claude Code 在您的轮换进行中期重新读取时，例如读取不匹配的证书和密钥，它会保持之前的密钥对并在下次失败时重新读取。
* **OTLP 遥测导出器**：Claude Code 保持[导出器](/docs/zh-CN/monitoring-usage#mtls-authentication)在首次使用时加载的证书，因此请重启 Claude Code 以使轮换的证书到达您的遥测收集器。
* **关闭重新加载**：设置 [`CLAUDE_CODE_DISABLE_MTLS_RELOAD_ON_STALE_CONNECTION=1`](/docs/zh-CN/env-vars#variables) 以关闭连接错误重新读取。Claude Code 然后仅在下次应用设置或下次启动时获取轮换的文件。

要确认 Claude Code 已获取轮换，请[使用调试日志启动会话](#verify-your-configuration)并在日志中查找 `Stale connection — reloaded rotated mTLS client material`。当 Claude Code 在应用设置时获取轮换时，它不会记录此行，因此仅缺少一行并不意味着轮换失败。

在当前密钥对过期之前替换文件，以便 Claude Code 在下次启动时不会加载已过期的密钥对。

在[云会话](/docs/zh-CN/claude-code-on-the-web)中，托管环境管理与 API 的连接，因此当这些变量来自设置文件 `env` 块时，Claude Code 会忽略以下变量：

* `CLAUDE_CODE_CLIENT_CERT`
* `CLAUDE_CODE_CLIENT_KEY`
* `CLAUDE_CODE_CLIENT_KEY_PASSPHRASE`
* `NODE_EXTRA_CA_CERTS`
* `NODE_TLS_REJECT_UNAUTHORIZED`
* `CLAUDE_CODE_OAUTH_SCOPES`

Claude Code 在会话的调试日志中记录每个被忽略的密钥。

在[Claude Desktop](/docs/zh-CN/desktop)会话中，应用管理提供商连接，例如[第三方提供商](/docs/zh-CN/third-party-integrations)上的代码选项卡和 Cowork 会话，Claude Code 仅从[托管设置](/docs/zh-CN/managed-settings)和 `~/.claude/settings.json` 读取这些变量和代理变量 `HTTP_PROXY`、`HTTPS_PROXY` 和 `NO_PROXY`：它忽略存储库自己的设置文件中的这些变量，因此已检出的存储库无法重定向凭证来自应用的会话的 TLS 或代理路径。在通过 claude.ai 登录的本地、SSH 或 WSL 代码选项卡会话中，应用不管理连接，Claude Code 从每个设置范围读取这些变量，就像任何终端会话一样；[云会话](/docs/zh-CN/claude-code-on-the-web)无论您在何处启动它们，都遵循上述云会话规则。在 v2.1.217 之前，当应用管理连接时，Claude Code 忽略每个设置文件中的这些变量。

<h2 id="verify-your-configuration">
  验证你的配置
</h2>

你通常会从后续请求中的[连接或证书错误](/docs/zh-CN/errors#network-and-connection-errors)发现代理地址错误或证书路径不正确的问题，因为 Claude Code 在读取这些设置时不会验证大多数设置。它在启动时检查的唯一设置是代理 URL：当它无法解析该值（例如缺少 `http://` 方案）时，Claude Code 会停止启动并显示一个错误，指出需要修复的变量。

要在发送请求之前确认你的配置已加载，请使用调试日志启动 Claude Code：

```bash theme={null}
claude --debug
```

调试输出会进入 `~/.claude/debug/<session-id>.txt` 而不是终端，或进入你使用 `--debug-file <path>` 设置的路径。在日志中，查找确认每个文件已加载的行：

```text theme={null}
CA certs: Appended extra certificates from NODE_EXTRA_CA_CERTS (/etc/ssl/certs/corp-ca.pem)
mTLS: Loaded client certificate from CLAUDE_CODE_CLIENT_CERT
mTLS: Loaded client key from CLAUDE_CODE_CLIENT_KEY
```

如果 Claude Code 无法读取其中一个文件，日志会显示 `Failed to read` 或 `Failed to load` 行以及原因。

你也可以在交互式会话中运行 `/status` 并检查这些行：

* **Proxy**：显示活跃的代理 URL，并将无法解析的值标记为无效且被忽略。
* **mTLS client cert** 和 **mTLS client key**：仅在文件加载时出现，所以缺少该行意味着加载失败，调试日志中有原因。
* **Additional CA cert(s)**：显示 `NODE_EXTRA_CA_CERTS` 路径而不检查文件是否已加载，所以请在调试日志中确认这一项。

<h2 id="apply-network-settings-to-background-agents">
  为后台代理应用网络设置
</h2>

[后台代理](/docs/zh-CN/agent-view)不在分派它们的终端内运行。一个按用户的监督进程按需启动，生命周期超过你的 shell，并托管每个 `claude agents`、`--bg` 和 `/background` 会话。请参阅[后台会话如何被托管](/docs/zh-CN/agent-view#how-background-sessions-are-hosted)。这改变了此页面上的配置如何到达这些会话的方式。

<h3 id="set-network-variables-in-settings-not-the-shell">
  在设置中设置网络变量，而不是在 shell 中
</h3>

监督进程是由每个终端共享的一个进程。它继承启动它的第一个 shell 的环境，而操作系统安装的监督进程根本不接收任何 shell 环境。如果你仅在 shell 中导出代理、CA 路径或 mTLS 变量，当该 shell 碰巧冷启动监督进程时，它会到达后台代理，而当不同的 shell 启动时，它会无声地失败。

将相同的变量放在 `~/.claude/settings.json` 的 `env` 块中或[托管设置](/docs/zh-CN/settings)中。此页面上的每个变量都可以在那里设置，设置是唯一到达每台机器上每个后台会话的配置。

<h3 id="configure-a-corporate-launcher-as-a-setting">
  将企业启动器配置为设置
</h3>

某些组织要求每个 Claude Code 进程都通过应用沙箱、网络控制或凭证注入的企业启动器启动。监督进程及其工作进程从固定路径启动 Claude Code，而不是在 `PATH` 上查找 `claude`，因此每个后台代理都绕过你在 `PATH` 上放置的包装器。

设置 [`processWrapper`](/docs/zh-CN/settings-reference#processwrapper) 设置以使用你的启动器为监督进程、其工作进程和[启动器覆盖的内容](/docs/zh-CN/corporate-launcher#what-the-launcher-covers)下列出的其他后台进程添加前缀。等效的 [`CLAUDE_CODE_PROCESS_WRAPPER`](/docs/zh-CN/env-vars) 环境变量在两者都设置时优先，它受相同规则约束：通过托管设置或 `~/.claude/settings.json` 传递它，而不是 shell 导出。[在企业启动器后面运行 Claude Code](/docs/zh-CN/corporate-launcher)涵盖启动器必须满足的合同、它做什么和不做什么，以及如何推出它。

<Note>
  已运行的监督进程保持它启动时的启动配置。部署启动器设置后，运行 [`claude daemon stop --any`](/docs/zh-CN/agent-view#the-supervisor-process)，以便下一个 `claude agents` 或 `--bg` 启动一个尊重它的监督进程。已安装的服务采用 `claude daemon stop` 而不需要 `--any`。
</Note>

<h2 id="streaming-idle-watchdogs">
  流式空闲监视器
</h2>

Claude Code 运行四个独立的计时器，当流式模型响应变得安静时会中止该响应，因此死连接会失败并重试，而不是挂起。首字节截止时间涵盖等待响应头的时间，在响应到达之前。其他三个监视器各自监视实时响应的不同信号。

| 计时器 | 中止条件 | 运行位置 | 默认超时 |
| :- | :- | :- | :- |
| 首字节截止时间 | Claude Code 发送请求后没有响应头到达 | 直接 Anthropic API 和 [Claude Platform on AWS](/docs/zh-CN/claude-platform-on-aws)，包括通过 HTTPS 代理，但不包括当 `ANTHROPIC_BASE_URL` 或 `ANTHROPIC_AWS_BASE_URL` 通过 [gateway](/docs/zh-CN/gateways) 路由时。在 Amazon Bedrock 上可选，使用 `CLAUDE_ENABLE_BYTE_WATCHDOG_BEDROCK=1`；不在 Google Cloud 的 Agent Platform 或 Microsoft Foundry 上运行 | 直接 Anthropic API 上为 180 秒，其他地方为 300 秒，加上每 32KB 请求体一秒 |
| 事件级监视器 | 没有响应事件解析。在字节级监视器运行在 Amazon Bedrock 以外的连接上的情况下，到达的字节（包括保活 ping）也会重置此监视器，最多约五分钟内没有解析的事件 | 每个提供商 | 300 秒 |
| 字节级监视器 | 线路上没有字节到达，包括 SSE 保活 ping | 直接 Anthropic API、[Claude Platform on AWS](/docs/zh-CN/claude-platform-on-aws) 和 [网关](/docs/zh-CN/gateways) 连接，包括自定义 `ANTHROPIC_BASE_URL`。在 Amazon Bedrock `vnd.amazon.eventstream` 响应上可选，使用 `CLAUDE_ENABLE_BYTE_WATCHDOG_BEDROCK=1`；不在 Google Cloud 的 Agent Platform 或 Microsoft Foundry 上运行 | 直接 Anthropic API 上为 180 秒。通过自定义 `ANTHROPIC_BASE_URL` 时，如果 Claude Code 已[获取功能标志](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching)则为 180 秒，未获取则为 300 秒。其他地方为 300 秒 |
| 主体空闲超时 | 5 分钟内没有字节到达 | 除了直接 Anthropic API、Claude Platform on AWS 和设置了 `CLAUDE_ENABLE_BYTE_WATCHDOG_BEDROCK=1` 的 Amazon Bedrock 之外的提供商，除非 [`API_FORCE_IDLE_TIMEOUT`](/docs/zh-CN/env-vars) 改变这一点 | 5 分钟 |

如果设置 `CLAUDE_ENABLE_BYTE_WATCHDOG_BEDROCK=1`，字节级监视器会在 Bedrock 上替换主体空闲超时，而不是与其并行运行。`CLAUDE_STREAM_IDLE_TIMEOUT_MS` 随后也会控制 Bedrock 流在 Claude Code 将连接视为死连接之前可以保持沉默多长时间，在下面列出的限制范围内。到达的字节仍然不会在 Bedrock 上重置事件级监视器。启用调试日志后，每个 Bedrock 流随后会记录一条以 `wire-heartbeat: _chunkTimes absent` 开头的调试消息。

使用这些变量配置计时器，每个变量在 [环境变量参考](/docs/zh-CN/env-vars) 中详细说明：

* `CLAUDE_ENABLE_STREAM_WATCHDOG` 和 `CLAUDE_ENABLE_BYTE_WATCHDOG` 在表列出的连接范围内，使用 `1` 强制打开相应的监视器或使用 `0` 关闭；这两个变量都不会将监视器扩展到它不覆盖的连接类型。`CLAUDE_ENABLE_BYTE_WATCHDOG` 设置为 `0` 也会关闭首字节截止时间。
* `CLAUDE_STREAM_IDLE_TIMEOUT_MS` 设置两个监视器的超时。Claude Code 将低于 5 分钟的值提高到 5 分钟，并将字节级监视器的值上限设为 30 分钟。
* `CLAUDE_BYTE_STREAM_IDLE_TIMEOUT_MS` 设置字节级监视器的超时，而不改变事件级监视器的超时，限制在 10 秒到 30 分钟之间，并优先于 `CLAUDE_STREAM_IDLE_TIMEOUT_MS` 用于该监视器。
* `CLAUDE_STREAM_FIRST_BYTE_TIMEOUT_MS` 直接设置首字节截止时间。保持未设置状态，Claude Code 使用字节级监视器的超时，因此 `CLAUDE_STREAM_IDLE_TIMEOUT_MS` 和 `CLAUDE_BYTE_STREAM_IDLE_TIMEOUT_MS` 也会改变截止时间。有关限制、上传额度、`API_TIMEOUT_MS` 上限以及重试在无响应中止后等待多长时间，请参阅 [API 无响应](/docs/zh-CN/errors#no-response-from-api)。
* `API_FORCE_IDLE_TIMEOUT` 设置为 `0` 会关闭主体空闲超时，设置为 `1` 会为每个提供商打开它。监视器独立于它运行，因此要让流暂停超过其阈值，也要提高或禁用它们。

当监视器中止停滞的流时，Claude Code 将中止视为中流失败，你看到的内容取决于响应已进行到多远。Claude Code 重试请求或以错误结束轮次，保留已完成的输出并显示 [不完整响应通知](/docs/zh-CN/errors#the-response-above-may-be-incomplete)，或正常结束轮次。[自动重试](/docs/zh-CN/errors#automatic-retries) 说明每个结果适用的位置。

在 [非交互式会话](/docs/zh-CN/headless) 中，以及在任何会话中的子代理响应中，Claude Code 可能首先提示 Claude 继续被切断的响应；[该通知的条目](/docs/zh-CN/errors#the-response-above-may-be-incomplete) 说明何时执行此操作以及何时仍然看到通知。

当首字节截止时间触发时，没有响应已开始，因此没有部分输出可保留。有关 Claude Code 如何重新发送请求以及何时轮次改为结束，请参阅 [API 无响应](/docs/zh-CN/errors#no-response-from-api)。

<h2 id="network-access-requirements">
  网络访问要求
</h2>

Claude Code 需要访问以下 URL。在代理配置和防火墙规则中将这些 URL 加入白名单，特别是在容器化或受限网络环境中。当首次运行设置无法连接到 `api.anthropic.com` 或 `platform.claude.com` 时，连接性检查会指向这里；有关检查消息和恢复步骤，请参阅[无法连接到 Anthropic 服务](/docs/zh-CN/errors#unable-to-connect-to-anthropic-services)。

| URL | 用途 |
| - | - |
| `api.anthropic.com` | Claude API 请求，包括 WebFetch [域名安全检查](/docs/zh-CN/data-usage#webfetch-domain-safety-check)、功能标志获取和遥测事件日志记录 |
| `claude.ai` | claude.ai 账户身份验证 |
| `claude.com` | claude.ai 账户登录在浏览器中打开 `claude.com` 页面，该页面重定向到 `claude.ai`；预先批准的 WebFetch 文档查询也从 CLI 访问此主机 |
| `platform.claude.com` | Anthropic Console 账户身份验证。OAuth 令牌交换、刷新和撤销也会转到此主机以用于 claude.ai 账户，因此 Console 和 claude.ai 登录都需要它 |
| `mcp-proxy.anthropic.com` | [来自 claude.ai 的 MCP 连接器](/docs/zh-CN/mcp#use-mcp-servers-from-claude-ai)，包括组织管理员配置的连接器。连接器流量通过此代理路由；对于 claude.ai 认证用户，连接器默认启用。要停止 Claude Code 获取它们，请设置 [`ENABLE_CLAUDEAI_MCP_SERVERS=false`](/docs/zh-CN/env-vars) 或 [`disableClaudeAiConnectors`](/docs/zh-CN/settings-reference#disableclaudeaiconnectors) 设置 |
| `downloads.claude.ai` | 插件可执行文件下载；本机安装程序、本机自动更新程序和更新版本检查 |
| `storage.googleapis.com` | `/plugin` 中显示的插件安装计数和元数据 |
| `storage.googleapis.com` | 2.1.116 之前版本的本机安装程序和本机自动更新程序 |
| `registry.npmjs.org` | 插件安装（获取 npm 源插件包和安装插件的 Node.js 包依赖项）、`npx` 启动的 MCP 服务器以及 npm 和 bun 安装 Claude Code 本身的包注册表 |
| `bridge.claudeusercontent.com` | [Chrome 中的 Claude](/docs/zh-CN/chrome) 扩展 WebSocket 桥接 |
| `*.frame.claudeusercontent.com` | [Artifact](/docs/zh-CN/artifacts) 内容读取。当 Claude 打开 Artifact 时，CLI 从此主机获取 Artifact 的文件，仅当 Artifact 工具对您的账户[可用](/docs/zh-CN/artifacts#availability)时。要关闭该工具并删除此要求，请设置 [`"enableArtifact": false`](/docs/zh-CN/settings-reference#enableartifact) 或 [`CLAUDE_CODE_DISABLE_ARTIFACT=1`](/docs/zh-CN/env-vars) |
| `github.com` | 克隆 GitHub 托管的[插件市场](/docs/zh-CN/plugins/overview)和插件，包括官方 Anthropic 市场，通过 HTTPS 或 SSH。要仅通过 HTTPS 克隆 GitHub `owner/repo` 源，请设置 [`CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1`](/docs/zh-CN/env-vars) |
| `raw.githubusercontent.com` | [`/release-notes`](/docs/zh-CN/commands) 的更新日志源。在交互式会话中，当 Claude Code 的缓存更新日志尚未涵盖运行版本时（例如更新后的首次启动），Claude Code 也会在启动时在后台获取它；非交互式和云会话永远不会获取它 |
| `*-review.googlesource.com` | `googlesource.com` 检出上的 Gerrit 更改查询。当 Claude Desktop Code 标签会话在[受信任](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust)的检出上启动或恢复，且其 `origin` 是 `googlesource.com` 主机时，Claude Code 会匿名向该主机的 `-review` 服务器查询与 HEAD 的 `Change-Id` 匹配的开放更改，每次启动或恢复一次。其他会话类型跳过查询，不会联系其他 Gerrit 主机。可选：使用 [`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`](/docs/zh-CN/env-vars) 禁用 |
| `http-intake.logs.us5.datadoghq.com` | 操作遥测事件，仅在 CLI 直接使用 Anthropic API 时发送，不适用于 Amazon Bedrock、Google Cloud 的 Agent Platform 或 Microsoft Foundry。可选：使用 [`DISABLE_TELEMETRY`](/docs/zh-CN/data-usage#telemetry-services) 或 `DO_NOT_TRACK` 禁用 |
| `browser-intake-us5-datadoghq.com` | 操作错误报告，在 CLI 直接使用 Anthropic API 且服务器端推出门启用时发送。可选：使用 `DISABLE_ERROR_REPORTING` 或 `DISABLE_TELEMETRY` 禁用；请参阅[遥测服务](/docs/zh-CN/data-usage#telemetry-services) |
| `formulae.brew.sh` | Homebrew 安装上的更新版本检查。其他安装方法不会联系此主机 |
| `code.claude.com` | 内置 claude-code-guide 代理和预先批准的 WebFetch 请求进行的 Claude Code 文档查询。阻止此主机仅影响文档查询 |

如果您通过 npm 安装 Claude Code 或管理自己的二进制分发，最终用户不需要 `downloads.claude.ai` 的本机安装程序和自动更新程序用途，但 npm 和 bun 安装需要其包注册表 `registry.npmjs.org`，除非您的组织镜像它。表中的其他用途适用于任何安装方法。

两个 Datadog 摄取主机仅携带可选的操作遥测，设置 [`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`](/docs/zh-CN/env-vars) 会禁用两者。第三方提供商上的会话永远不会发送到这些主机，即使平台设置了 [`CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST`](/docs/zh-CN/env-vars) 且遥测指标默认启用。有关 Claude Code 发送的所有内容以及如何在最终确定白名单之前禁用它，请参阅[遥测服务](/docs/zh-CN/data-usage#telemetry-services)。

使用 [Amazon Bedrock](/docs/zh-CN/amazon-bedrock)、[Google Cloud 的 Agent Platform](/docs/zh-CN/google-vertex-ai)、[Microsoft Foundry](/docs/zh-CN/microsoft-foundry) 或已登录的 [Claude 应用网关](/docs/zh-CN/claude-apps-gateway)会话时，模型流量和身份验证转到您的提供商或网关，而不是 `api.anthropic.com`、`claude.ai` 或 `platform.claude.com`。WebFetch 工具仍会调用 `api.anthropic.com` 进行其[域名安全检查](/docs/zh-CN/data-usage#webfetch-domain-safety-check)，除非您在[设置](/docs/zh-CN/settings)中设置 `skipWebFetchPreflight: true`。

通过带有 [`ANTHROPIC_BASE_URL`](/docs/zh-CN/llm-gateway-connect#set-the-base-url-and-credential) 的 [LLM 网关](/docs/zh-CN/llm-gateway)路由时，[快速模式](/docs/zh-CN/fast-mode)可用性检查仍会调用 `api.anthropic.com` 而不是网关基础 URL。检查确实遵守配置的 HTTP 代理，因此当网络阻止是原因时，代理中 `api.anthropic.com` 的白名单条目是修复。网络阻止仅在主机即使通过代理也无法访问时才会导致检查失败，快速模式随后会报告连接错误。当检查呈现网关颁发的凭证而 Anthropic 拒绝时，也会出现相同的连接错误；白名单在那里无法帮助，因为没有任何内容被阻止。有关恢复它的变量，请参阅[在代理和 LLM 网关后面使用快速模式](/docs/zh-CN/fast-mode#use-fast-mode-behind-proxies-and-llm-gateways)。

<h3 id="organization-ip-allowlists-and-proxy-egress">
  组织 IP 白名单和代理出口
</h3>

如果您的组织为 Claude 启用了 [IP 白名单](https://support.claude.com/en/articles/13200993-restrict-access-to-claude-with-ip-allowlisting)，请通过与 `claude.ai` 和 `api.anthropic.com` 相同的代理出口路由 `bridge.claudeusercontent.com`，例如将其放在相同的 Zscaler 应用段或 Netskope 转向策略中。如果您无法以这种方式路由它，请将代理用于该主机的出口地址添加到您的组织的 IP 白名单中，但仅当该地址专用于您的组织时：共享代理出口范围也允许代理供应商的其他客户。

Anthropic 使用它们到达的地址检查与您的组织 IP 白名单的 `bridge.claudeusercontent.com` 连接。如果您的代理通过不在该白名单上的地址为该主机发送流量，Claude Code 无法连接到 [Chrome 中的 Claude](/docs/zh-CN/chrome) 扩展，即使 Claude Code 的其余部分有效。

<h3 id="github-allow-lists-and-firewalls">
  GitHub 白名单和防火墙
</h3>

Anthropic 托管环境中的 [Web 上的 Claude Code](/docs/zh-CN/claude-code-on-the-web) 和 [Code Review](/docs/zh-CN/code-review) 从 Anthropic 管理的基础设施连接到您的存储库；[自托管环境](/docs/zh-CN/self-hosted-environments)中的会话从您的网络内部连接，除非运行程序选择加入 [Anthropic git 代理](/docs/zh-CN/self-hosted-environments-deploy#use-the-anthropic-git-proxy)，该代理从 Anthropic 一侧获取。

如果您的 GitHub Enterprise Cloud 组织按 IP 地址限制访问，请启用[已安装 GitHub App 的 IP 白名单继承](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#allowing-access-by-github-apps)，并且还要[添加白名单条目](https://docs.github.com/en/enterprise-cloud@latest/organizations/keeping-your-organization-secure/managing-security-settings-for-your-organization/managing-allowed-ip-addresses-for-your-organization#adding-an-allowed-ip-address)以用于 Anthropic 的[出站 IP 地址](https://platform.claude.com/docs/en/api/ip-addresses#outbound-ip-addresses)。继承仅涵盖 Claude GitHub App 作为安装进行的请求，不涵盖它代表您的用户进行的请求。对于其他防火墙，请参阅 [Anthropic API IP 地址](https://platform.claude.com/docs/en/api/ip-addresses)。

对于防火墙后的自托管 [GitHub Enterprise Server](/docs/zh-CN/github-enterprise-server) 实例，白名单 Anthropic 的[出站 IP 地址](https://platform.claude.com/docs/en/api/ip-addresses#outbound-ip-addresses)，以便 Anthropic 基础设施可以访问您的 GHES 主机来克隆存储库和发布审查评论。[自托管环境](/docs/zh-CN/self-hosted-environments-deploy#configure-git)中的会话从您的网络内部访问您的 GHES 主机，因此该暴露仅适用于 Anthropic 托管会话、托管的会话前流程（如存储库选择器）以及选择加入 [Anthropic git 代理](/docs/zh-CN/self-hosted-environments-deploy#use-the-anthropic-git-proxy)的自托管运行程序，该代理从 Anthropic 一侧获取。[SCM 连接器](/docs/zh-CN/self-hosted-environments-reference#scm-connector-flags)不可用，因此托管的会话前流程无法访问仅在您的网络内可路由的 GHES 主机。

<h3 id="desktop-and-claude-ai">
  Desktop 和 claude.ai
</h3>

前面的表格涵盖了独立 CLI。Claude Desktop 应用和浏览器中的 claude.ai 从其他 Anthropic CDN 主机加载其应用代码和用户内容，包括 `assets-proxy.anthropic.com` 和其他在这些应用中提供 [Artifact](/docs/zh-CN/artifacts) 的 `*.claudeusercontent.com` 源。允许 `claude.ai` 同时阻止这些主机会产生空白页面而不是错误。请参阅 Desktop 页面上的[网络访问要求](/docs/zh-CN/desktop#network-access-requirements)。

Claude Desktop 和 claude.ai 还会将对话中的某些工具结果呈现为交互式小组件，例如某些连接器提供的 [MCP Apps](https://claude.com/docs/connectors/building/mcp-apps/getting-started)。这些小组件从 `claudemcpcontent.com` 的生成子域加载，因此请允许 `*.claudemcpcontent.com` 并保留通配符。如果您阻止它，应用的其余部分仍可正常工作，但这些小组件不会加载。

<h4 id="third-party-hosts-for-artifact-fonts-and-libraries">
  用于 Artifact 字体和库的第三方主机
</h4>

从 [Google Fonts](/docs/zh-CN/artifacts#improve-the-visual-design) 加载字体的 [Artifact](/docs/zh-CN/artifacts) 也会请求 `fonts.googleapis.com` 和 `fonts.gstatic.com`。两个主机都是可选的。如果您阻止它们，Artifact 会以备用字体呈现。使用快速拒绝而不是静默丢弃来阻止，以便字体请求立即失败，而不是延迟页面的首次呈现。

Artifact 还可以从 `cdnjs.cloudflare.com`、`cdn.jsdelivr.net`、`cdn.tailwindcss.com`、`code.jquery.com` 和 `unpkg.com` 加载 JavaScript 库（如 React 或图表包），而不能从其他外部主机加载。如果您阻止这些主机，Artifact 中依赖库的部分将无法工作，与阻止的字体不同，阻止的库没有备用。也在这里使用快速拒绝，以便阻止的库请求立即失败，而不是挂起直到超时。

<h2 id="additional-resources">
  其他资源
</h2>

* [设置文件和优先级](/docs/zh-CN/settings)
* [环境变量参考](/docs/zh-CN/env-vars)
* [故障排除指南](/docs/zh-CN/troubleshooting)
