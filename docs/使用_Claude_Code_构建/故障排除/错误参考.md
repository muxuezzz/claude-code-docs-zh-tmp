> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 错误参考

> 查找 Claude Code 运行时错误消息，了解每个错误的含义以及如何修复。

本页列出 Claude Code 显示的运行时错误以及如何从每个错误中恢复，以及当响应似乎有问题但没有错误时要检查的内容。对于安装错误（如 `command not found` 或设置期间的 TLS 失败），请参阅[排查安装和登录问题](/docs/zh-CN/troubleshoot-install)。

除了[包装器和 IDE 错误](#wrapper-and-ide-errors)（由启动程序打印而不是 Claude Code 本身打印）外，这些错误和恢复命令适用于 CLI、[桌面应用](/docs/zh-CN/desktop)和[云端会话](/docs/zh-CN/claude-code-on-the-web)，因为这三个都包装相同的 Claude Code CLI。对于其他特定于使用入口的问题，请参阅该使用入口页面上的故障排除部分。

<Note>
  Claude Code 调用 Claude API 来获取模型响应，因此大多数运行时错误映射到底层 API 错误代码。本页介绍每个错误在 Claude Code 中的含义以及如何恢复。有关原始 HTTP 状态代码定义，请参阅 [Claude Platform 错误参考](https://platform.claude.com/docs/en/api/errors)。
</Note>

<h2 id="find-your-error">
  查找您的错误
</h2>

将您看到的消息与下面的部分相匹配。

| 消息 | 部分 |
| :- | :- |
| `API Error: 500 Internal server error` | [服务器错误](#api-error-500-internal-server-error) |
| `API Error: Repeated 529 Overloaded errors` | [服务器错误](#api-error-repeated-529-overloaded-errors) |
| `Opus is experiencing high load` / `Fable is experiencing high load` | [服务器错误](#api-error-repeated-529-overloaded-errors) |
| `Request timed out` | [服务器错误](#request-timed-out)，或如果消息提到您的互联网连接，则为[网络](#unable-to-connect-to-api) |
| `API Error: No response from API` | [服务器错误](#no-response-from-api) |
| `Server error mid-response. The response above may be incomplete.` | [服务器错误](#the-response-above-may-be-incomplete) |
| `Connection lost mid-response` / `Your computer went to sleep mid-response` / `The response stopped arriving` | [服务器错误](#the-response-above-may-be-incomplete) |
| `Connection closed mid-response` / `Response stalled mid-stream` | [服务器错误](#the-response-above-may-be-incomplete) |
| `Part of the response never arrived` / `The response stream was malformed` | [服务器错误](#the-response-above-may-be-incomplete) |
| `API Error: Content block not found` / `API Error: Content block already closed` / `API Error: Stream event unreadable` | [服务器错误](#the-response-above-may-be-incomplete) |
| `Connection lost before a response was produced` / `Your computer went to sleep before a response was produced` / `The response stalled before a response was produced` | [自动重试](#automatic-retries) |
| `Connection closed while thinking` / `Response stalled while thinking` | [自动重试](#automatic-retries) |
| `Connection lost while your computer was asleep` | [自动重试](#automatic-retries) |
| `<model> is temporarily unavailable, so auto mode cannot determine the safety of...` | [服务器错误](#auto-mode-cannot-determine-the-safety-of-an-action) |
| `Auto mode could not evaluate this action and is blocking it for safety` | [服务器错误](#auto-mode-cannot-determine-the-safety-of-an-action) |
| `Auto mode classifier transcript exceeded context window` | [服务器错误](#auto-mode-cannot-determine-the-safety-of-an-action) |
| `Agent aborted: auto mode classifier request refused by the safety safeguard` | [服务器错误](#auto-mode-cannot-determine-the-safety-of-an-action) |
| `The server-side auto mode classifier gave no verdict` | [服务器错误](#the-server-returned-no-safety-verdict) |
| `Auto mode is unavailable — the server returned no safety verdict for the last 10 responses` | [服务器错误](#the-server-returned-no-safety-verdict) |
| `Agent terminated early due to an API error` | [服务器错误](#agent-terminated-early-due-to-an-api-error) |
| `You've hit your session limit` / `You've hit your weekly limit` / `You've hit your Opus limit` / `You've hit your Sonnet limit` | [使用限制](#youve-hit-your-session-limit) |
| `Usage credits required for 1M context` | [使用限制](#usage-credits-required-for-1m-context) |
| `the prompt to confirm went unanswered — nothing was sent` | [使用限制](#the-prompt-to-confirm-went-unanswered) |
| `Server is temporarily limiting requests` | [使用限制](#server-is-temporarily-limiting-requests) |
| `Request rejected (429)` | [使用限制](#request-rejected-429) |
| `Credit balance is too low` | [使用限制](#credit-balance-is-too-low) |
| `You've hit your monthly spend limit` / `You've hit your individual spend limit` / `You've hit your org's monthly spend limit` / `You've hit your channel's monthly spend limit` / `You've hit your team's shared budget` / `You've hit your individual usage limit` | [使用限制](#youve-hit-your-monthly-spend-limit) |
| `Could not update your spend limit` | [使用限制](#could-not-update-your-spend-limit) |
| `spend limit reached` / `spend limit unavailable` | [使用限制](#spend-limit-reached) |
| `Not logged in · Please run /login` | [身份验证](#not-logged-in) |
| `Couldn't save your login` | [身份验证](#couldnt-save-your-login) |
| `Authentication required · Sign in again to continue` | [身份验证](#not-logged-in) |
| `Could not resolve authentication method` | [身份验证](#could-not-resolve-authentication-method) |
| `Invalid API key` | [身份验证](#invalid-api-key) |
| `Your apiKeyHelper script is failing` | [身份验证](#your-apikeyhelper-script-is-failing) |
| `Invalid auth token · Fix external auth token` | [身份验证](#invalid-request-header-value) |
| `Invalid ANTHROPIC_CUSTOM_HEADERS · Fix the environment variable` | [身份验证](#invalid-request-header-value) |
| `Invalid request header from the environment · Fix the environment variable` | [身份验证](#invalid-request-header-value) |
| `This organization has been disabled` | [身份验证](#this-organization-has-been-disabled) |
| `Your organization has disabled API key authentication` | [身份验证](#your-organization-has-disabled-api-key-authentication) |
| `Your organization has disabled Claude subscription access` | [身份验证](#your-organization-has-disabled-claude-subscription-access) |
| `Routines are disabled by your organization's policy` | [身份验证](#routines-are-disabled-by-your-organizations-policy) |
| `Remote Control is only available when using Claude via api.anthropic.com` | [身份验证](#remote-control-requires-the-anthropic-api) |
| `OAuth token refresh failed — run /login to re-authenticate` | [身份验证](#remote-control-couldnt-refresh-your-login) |
| `JWT refresh failed: no OAuth token — run /login` | [身份验证](#remote-control-couldnt-refresh-your-login) |
| `Claude.ai login expired` | [身份验证](#remote-control-couldnt-refresh-your-login) |
| `Claude.ai login was rejected — run /login, then /remote-control` | [身份验证](#remote-control-couldnt-refresh-your-login) |
| `OAuth token unavailable — run /login to restore Remote Control` | [身份验证](#remote-control-couldnt-refresh-your-login) |
| `Signed out of Claude — run /login, then /remote-control` | [身份验证](#remote-control-couldnt-refresh-your-login) |
| `signed-in claude.ai account or organization changed on this machine` | [身份验证](#remote-control-stopped-because-the-signed-in-account-changed) |
| `Remote Control stopped — the app running this session is now signed in to a different Claude account` | [身份验证](#remote-control-stopped-because-the-app-running-the-session-signed-out-or-switched-accounts) |
| `Remote Control stopped — the app running this session is signed out of Claude` | [身份验证](#remote-control-stopped-because-the-app-running-the-session-signed-out-or-switched-accounts) |
| `Couldn't verify your organization's policy for remote control` | [Troubleshoot Remote Control](/docs/zh-CN/remote-control#couldnt-verify-your-organizations-policy-for-remote-control) |
| `Remote Control is disabled by your organization's policy` | [Troubleshoot Remote Control](/docs/zh-CN/remote-control#remote-control-is-disabled-by-your-organizations-policy) |
| `Remote Control was turned off by your organization's policy` | [Troubleshoot Remote Control](/docs/zh-CN/remote-control#remote-control-was-turned-off-by-your-organizations-policy) |
| `OAuth token revoked` / `OAuth token has expired` | [身份验证](#oauth-token-revoked-or-expired) |
| `Failed to authenticate: OAuth token revoked` | [身份验证](#oauth-token-revoked-or-expired) |
| `Your account does not have access to Claude. Please login again or contact your administrator.` | [身份验证](#oauth-token-revoked-or-expired) |
| `API Error: 401 Invalid authentication credentials` | [身份验证](#api-error-401-invalid-authentication-credentials) |
| `Login expired · Please run /login` | [身份验证](#login-expired) |
| `Failed to start OAuth callback server` | [身份验证](#failed-to-start-oauth-callback-server) |
| `Claude login not accepted · Run /login, then try again` | [身份验证](#claude-login-not-accepted) |
| `Artifacts need a claude.ai login` | [身份验证](#artifacts-need-a-claude-ai-login) |
| `Not signed in to the Cloud gateway — run /login.` | [身份验证](#administrator-policy-requires-a-cloud-gateway-sign-in) |
| `Administrator policy requires a Cloud gateway sign-in on this machine` | [身份验证](#administrator-policy-requires-a-cloud-gateway-sign-in) |
| `Failed to authenticate: OAuth session expired and could not be refreshed` | [身份验证](#login-expired) |
| `Could not refresh your login because another Claude Code process is refreshing it` | [身份验证](#could-not-refresh-your-login) |
| `Failed to refresh OAuth token: another Claude Code process is refreshing it or exited mid-refresh` | [身份验证](#could-not-refresh-your-login) |
| `Your account is on hold and can't use Claude Code. View details or appeal: https://claude.ai/restricted` | [身份验证](#your-account-is-on-hold) |
| `Your account is on hold and can't sign in to Claude Code. View details or appeal: https://claude.ai/restricted` | [身份验证](#your-account-is-on-hold) |
| `Anthropic profile login expired · Re-authenticate your Anthropic profile` | [身份验证](#anthropic-profile-login-expired) |
| `Anthropic profile login expired · Run /login to use your claude.ai account instead, or re-authenticate the profile` | [身份验证](#anthropic-profile-login-expired) |
| `does not meet scope requirement user:profile` | [身份验证](#oauth-scope-requirement) |
| `claude.ai rejected the session token` / `session token rejected` | [身份验证](#claude-ai-rejected-the-session-token) |
| `MCP server "<name>" needs you to sign in again (run /mcp to re-authenticate)` | [身份验证](#mcp-server-needs-you-to-sign-in-again) |
| `rejected the credential from its headersHelper` / `rejected the Authorization header in its config` | [身份验证](#mcp-server-needs-you-to-sign-in-again) |
| `MCP server "<name>" needs additional permissions (scope: "<scope>") — run /mcp to re-authenticate` | [身份验证](#mcp-server-needs-you-to-sign-in-again) |
| `MCP server "<name>" requires re-authorization (token expired)` | [身份验证](#mcp-server-needs-you-to-sign-in-again) |
| `This server's URL is missing or not a valid URL, so sign-in can't start` | [身份验证](#mcp-server-url-is-missing-or-not-a-valid-url) |
| `Issuer mismatch in authorization response (RFC 9207)` | [身份验证](#issuer-mismatch-in-authorization-response) |
| `Refusing to send credentials to non-https token endpoint` / `<short-name> from the MCP SDK for <server-url>` | [身份验证](#refusing-to-send-credentials-to-non-https-token-endpoint) |
| `Cloud gateway session expired — run /login to reconnect.` | [身份验证](#cloud-gateway-session-expired) |
| `Cloud gateway <url> no longer accepts this session` | [身份验证](#cloud-gateway-session-expired) |
| `Sign-in timed out while waiting for you to continue. Try again.` | [身份验证](#sign-in-timed-out-while-waiting-for-you-to-continue) |
| `AWS credentials expired or invalid` | [身份验证](#aws-credentials-expired-or-invalid) |
| `AWS authentication failed` | [身份验证](#aws-authentication-failed) |
| `Google Cloud credentials expired or invalid` | [身份验证](#google-cloud-credentials-expired-or-invalid) |
| `Google Cloud authentication failed` | [身份验证](#google-cloud-authentication-failed) |
| `Microsoft Foundry authentication failed` | [身份验证](#microsoft-foundry-authentication-failed) |
| `Gateway refused the request` | [身份验证](#gateway-refused-the-request) |
| `Could not load AWS credentials` / `Could not load Google Cloud credentials` | [身份验证](#could-not-load-aws-or-google-cloud-credentials) |
| `AWS default-chain credential resolve timed out` | [身份验证](#aws-default-chain-credential-resolve-timed-out) |
| `Timed out after 60s waiting for AWS` | [身份验证](#bedrock-setup-verification-timed-out-waiting-for-aws) |
| `A request to AWS timed out. Check your network and proxy settings, then try again.` | [身份验证](#bedrock-setup-verification-timed-out-waiting-for-aws) |
| `Could not load the default credentials` on Google Cloud's Agent Platform | [身份验证](#could-not-load-aws-or-google-cloud-credentials) |
| `Unable to connect to API` | [网络](#unable-to-connect-to-api) |
| `Connection refused —` / `Can't reach the API server —` / `No internet route —` / `Couldn't connect through your proxy` / `Connection dropped`，每个都带有括号中的错误代码 | [网络](#unable-to-connect-to-api) |
| `Unable to connect to Anthropic services` during setup | [网络](#unable-to-connect-to-anthropic-services) |
| `Socket is closed` | [网络](#socket-is-closed) |
| `Waiting for API response · will retry in` | [自动重试](#automatic-retries)，或如果持续存在，则为[网络](#unable-to-connect-to-api) |
| `API returned an empty or malformed response` | [网络](#api-returned-an-empty-or-malformed-response) |
| `Streaming response ended before any complete data was received` | [网络](#streaming-response-ended-before-any-complete-data-was-received) |
| `Bedrock streaming response has content-type "..."; expected "application/vnd.amazon.eventstream"` | [网络](#bedrock-streaming-response-has-an-unexpected-content-type) |
| `SSL certificate verification failed` | [网络](#ssl-certificate-errors) |
| `SSL certificate error (...)` during login or startup | [网络](#ssl-certificate-errors) |
| `unable to get local issuer certificate` | [网络](#ssl-certificate-errors) |
| `403` with `x-deny-reason: host_not_allowed` in a cloud or routine session | [网络](#host-not-allowed-in-a-cloud-session) |
| `proxy refused the connection` | [网络](#the-proxy-refused-the-connection) |
| `403` with `GitHub GraphQL is not available from Claude Code sessions` in a cloud session | [GitHub proxy](/docs/zh-CN/cloud-environments#github-proxy) |
| `The cloud environments service returned an empty response` / `The cloud environments service returned a response in an unexpected format` | [网络](#the-cloud-environments-service-returned-an-empty-or-unexpected-response) |
| `Couldn't reconnect to your Remote Control session` | [网络](#couldnt-reconnect-to-your-remote-control-session) |
| `N sessions ended while this machine was offline — the environment was cleaned up on the server and can't be resumed.` | [网络](#sessions-ended-while-this-machine-was-offline) |
| `Couldn't share the transcript.` | [网络](#couldnt-share-the-transcript) |
| `Couldn't send feedback` | [网络](#couldnt-send-feedback) |
| `Prompt is too long` / `Input is too long for requested model` | [请求错误](#prompt-is-too-long) |
| `Prompt is too long · automatic compaction failed:` | [请求错误](#prompt-is-too-long) |
| `Prompt is too long · this conversation is a single exchange` / `A single-exchange conversation cannot be compacted` | [请求错误](#prompt-is-too-long) |
| `Context limit reached · /compact or /clear to continue` | [请求错误](#prompt-is-too-long) |
| `Context limit reached · /clear to continue` | [请求错误](#prompt-is-too-long) |
| `capability_rejected: prompt_too_long` on a Claude apps gateway session | [请求错误](#prompt-is-too-long) |
| `upstream rejected the request` / `request too large for this upstream` on a Claude apps gateway session | [上游错误消息](/docs/zh-CN/claude-apps-gateway-config#upstream-error-messages) |
| `upstream rate limit exceeded` on a Claude apps gateway session | [上游错误消息](/docs/zh-CN/claude-apps-gateway-config#upstream-error-messages) |
| `all upstreams failed (N attempted)` on a Claude apps gateway session | [上游错误消息](/docs/zh-CN/claude-apps-gateway-config#upstream-error-messages) |
| `Claude Code may not be enabled for your organization` after a Claude apps gateway sign-in | [Claude apps gateway 故障排除](/docs/zh-CN/claude-apps-gateway-deploy#troubleshooting) |
| `Context exceeds the ...-token limit by ... tokens` in `/context` output | [请求错误](#context-exceeds-the-token-limit) |
| `Request too large` | [请求错误](#request-too-large) |
| `Request too large for the API's 32MB request limit` | [请求错误](#request-too-large) |
| `Image was too large` | [请求错误](#image-was-too-large) |
| `Unable to resize image` | [请求错误](#unable-to-resize-image) |
| `PDF too large` / `PDF is password protected` / `pdftoppm is not installed` | [请求错误](#pdf-errors) |
| `Extra inputs are not permitted` | [请求错误](#extra-inputs-are-not-permitted) |
| `API Error: 400 ... tools.N.custom.input_schema: JSON schema is invalid` / `Property keys should match pattern` | [请求错误](#tool-input-schema-is-invalid) |
| `tool_use.name: String should have at most 200 characters` | [请求错误](#tool-use-name-over-200-characters) |
| `There's an issue with the selected model` | [请求错误](#theres-an-issue-with-the-selected-model) |
| `Model ... is not a recognized model id` | [请求错误](#model-is-not-a-recognized-model-id) |
| `Model ... not found` | [请求错误](#model-not-found) |
| `Couldn't confirm model ... with the API` | [请求错误](#couldnt-confirm-model-with-the-api) |
| `API error: ... · model not changed` | [请求错误](#api-error-model-not-changed) |
| `Claude Opus is not available with the Claude Pro plan` | [请求错误](#claude-opus-is-not-available-with-the-claude-pro-plan) |
| `Claude Code ... does not support this model; version ... or newer is required` | [请求错误](#claude-code-does-not-support-this-model) |
| `Claude Code ... is older than the minimum version required by your organization's policy` | [请求错误](#claude-code-does-not-support-this-model) |
| `Model ... is restricted by your organization's settings` | [请求错误](#model-is-restricted-by-your-organizations-settings) |
| `Model ... is not available. Your organization restricts model selection.` | [请求错误](#model-is-restricted-by-your-organizations-settings) |
| `Can't switch to the default model` | [请求错误](#cant-switch-to-the-default-model) |
| `Model switch ... blocked by a PreModelSwitch hook` | [请求错误](#model-switch-was-blocked-by-a-premodelswitch-hook) |
| `couldn't save it as your default` / `couldn't confirm it was saved as your default` | [请求错误](#couldnt-save-it-as-your-default) |
| `is less capable than the current main model` / `Advisor will not activate on the main model` / `cannot advise` | [请求错误](#advisor-is-less-capable-than-the-current-main-model) |
| `thinking.type.enabled is not supported for this model` | [请求错误](#thinking-type-enabled-is-not-supported-for-this-model) |
| `Effort '<level>' isn't available with thinking turned off on this model` | [请求错误](#effort-isnt-available-with-thinking-turned-off) |
| `effort '<level>' is not supported when thinking is disabled` | [请求错误](#effort-isnt-available-with-thinking-turned-off) |
| `max_tokens must be greater than thinking.budget_tokens` | [请求错误](#thinking-budget-exceeds-output-limit) |
| `API Error: 400 due to tool use concurrency issues` | [请求错误](#tool-use-or-thinking-block-mismatch) |
| `API Error: 400 orphaned tool_result in conversation history` | [请求错误](#tool-use-or-thinking-block-mismatch) |
| `API Error: 400 duplicate tool_use ID in conversation history` | [请求错误](#tool-use-or-thinking-block-mismatch) |
| `Invalid data in redacted_thinking block` | [请求错误](#invalid-data-in-redacted-thinking-block) |
| `[Unsupported tool content removed]` | [请求错误](#unsupported-tool-content-removed) |
| `role 'system' must precede an 'assistant' message` | [请求错误](#role-system-must-precede-an-assistant-message) |
| `Invalid encrypted_content in search_result block` / `Invalid encrypted_index in text block` / `Failed to decrypt web search result content` | [请求错误](#invalid-encrypted-content-in-search-result-block) |
| `Invalid encrypted_stdout in encrypted_code_execution_result block` | [请求错误](#invalid-encrypted-content-in-search-result-block) |
| `server_tool_use.name: Input should be` on every turn of a resumed session | [请求错误](#unsupported-tool-content-removed) |
| `<model> can't help with this. Start a new session to continue` | [请求错误](#usage-policy-refusal) |
| `Claude Code is unable to respond to this request, which appears to violate our Usage Policy` | [请求错误](#usage-policy-refusal) |
| `<model>'s safeguards flagged this message` | [请求错误](#safety-measures-flagged-a-cybersecurity-topic) |
| `<model>'s safeguards flagged this session` | [请求错误](#safety-measures-flagged-a-cybersecurity-topic) |
| `<model> has safety measures that flagged this message for a cybersecurity topic` | [请求错误](#safety-measures-flagged-a-cybersecurity-topic) |
| `` Details: `[reasoning_extraction]` `` | [请求错误](#safeguards-flagged-a-request-for-claudes-reasoning) |
| `API Error: Output blocked by content filtering policy` | [请求错误](#output-blocked-by-content-filtering-policy) |
| `Installation was killed before it could finish (exit code 137)` | [安装错误](#installation-was-killed-before-it-could-finish) |
| `The connection dropped while downloading the update` | [安装错误](#the-connection-dropped-while-downloading-the-update) |
| `Download timed out: exceeded the total deadline` | [安装错误](#the-connection-dropped-while-downloading-the-update) |
| `--bg and --print conflict` | [命令行错误](#conflict-between-bg-and-print) |
| `Error: Cannot use both --append-subagent-system-prompt and --append-subagent-system-prompt-file. Please use only one.` | [命令行错误](#conflict-between-a-system-prompt-flag-and-its-file-form) |
| `Cloud sessions cannot be created from a --restricted session` | [命令行错误](#cloud-sessions-cannot-be-created-from-a-restricted-session) |
| `Cloud sessions are disabled by your organization's policy` | [命令行错误](#cloud-sessions-are-disabled-by-your-organizations-policy) |
| `Couldn't verify your organization's policy for cloud sessions` | [命令行错误](#cloud-sessions-are-disabled-by-your-organizations-policy) |
| `Cloud sessions need a claude.ai sign-in` | [无法获取组织 UUID](/docs/zh-CN/claude-code-on-the-web#unable-to-get-organization-uuid) |
| `Error: --json-schema is not a valid JSON Schema` | [命令行错误](#the-json-schema-value-is-not-a-valid-json-schema) |
| `Error: Invalid --agents configuration:` | [命令行错误](#invalid-agents-configuration) |
| `Error: --agents takes a JSON object, or a file path only with --print (-p)` | [命令行错误](#invalid-agents-configuration) |
| `Error: --agents file not found` | [命令行错误](#invalid-agents-configuration) |
| `Error: Settings file exceeds the 2MiB limit` | [命令行错误](#settings-file-exceeds-the-2mib-limit) |
| `The current directory no longer exists (it was deleted or moved)` / `Can't read the current directory` | [命令行错误](#the-current-directory-no-longer-exists) |
| `Temp directory <dir> ... Refusing to use it` / `ENOSPC: no space left on device, mkdir '<dir>'` | [命令行错误](#temp-directory-refused-or-cannot-be-created) |
| `couldn't be resolved to a real location, so its skills, commands, and agents weren't loaded` | [命令行错误](#directory-couldnt-be-resolved-to-a-real-location) |
| `Error: Workspace not trusted` when starting Remote Control | [命令行错误](#workspace-not-trusted-when-starting-remote-control) |
| `` `<flag>` before `remote-control` is not carried over to the sessions Remote Control starts `` | [命令行错误](#not-carried-over-to-the-sessions-remote-control-starts) |
| `` `claude import` is not yet available in this build `` | [命令行错误](#claude-import-is-not-yet-available-in-this-build) |
| `Could not read Claude Code config` | [命令行错误](#could-not-read-claude-code-config) |
| `Could not import <server>: <reason>` | [命令行错误](#could-not-import-a-server-from-claude-desktop) |
| `Cannot add MCP server to scope: managed` | [命令行错误](#cannot-add-mcp-server-to-the-managed-scope) |
| `Cannot add MCP server: your organization's managed settings allow only MCP servers that plugins provide` | [命令行错误](#cannot-add-mcp-server-when-managed-settings-allow-only-plugin-servers) |
| `is Anthropic-hosted and doesn't support local OAuth` | [命令行错误](#anthropic-hosted-and-doesnt-support-local-oauth) |
| `Can't read .mcp.json: it isn't a regular file or is larger than 2097152 bytes` | [命令行错误](#cant-read-mcp-json) |
| `MCP server "<name>" was not saved to` / `was not removed from` | [命令行错误](#mcp-server-was-not-saved-or-removed) |
| `MCP server "<name>" may not have been saved` / `may not have been removed` | [命令行错误](#mcp-server-may-not-have-been-saved-or-removed) |
| `Server rejected the Authorization header minted by the configured headersHelper` | [命令行错误](#server-rejected-the-authorization-header-minted-by-the-configured-headershelper) |
| `Error: MCP tool <name> (passed via --permission-prompt-tool) not found` | [命令行错误](#mcp-permission-prompt-tool-not-found) |
| `OAuth callback port <port> is already in use — another process may be holding it` | [命令行错误](#oauth-callback-port-is-already-in-use) |
| `No available ports for OAuth redirect` | [命令行错误](#no-available-ports-for-oauth-redirect) |
| `Shell command failed for pattern "..."`, from `/security-review` or any skill that injects dynamic context | [命令行错误](#security-review-fails-without-origin-head) |
| `Shell command permission check failed for pattern "..."`, from a skill that injects dynamic context | [命令行错误](#security-review-fails-without-origin-head) |
| ``Skill <name> requires bash (`shell: bash` in frontmatter) but Git Bash was not found`` | [命令行错误](#security-review-fails-without-origin-head) |
| `Input must be provided either through stdin or as a prompt argument when using --print` | [命令行错误](#input-must-be-provided-when-using-print) |
| `Claude Code can't read the keyboard here: stdin is not a terminal` | [命令行错误](#claude-code-cant-read-the-keyboard-here) |
| `Error: Input contained only whitespace` | [命令行错误](#input-contained-only-whitespace) |
| `Blank prompt — the message was only whitespace, so nothing was sent to the model.` | [命令行错误](#input-contained-only-whitespace) |
| `Error: stream-json input carried over 256M characters with no newline` | [命令行错误](#stream-json-input-carried-over-256m-characters-with-no-newline) |
| `Unknown command: /<name>`, with or without a `Did you mean` suggestion | [命令行错误](#unknown-command) |
| `Diff is too large for ultrareview` / `PR #<N> is too large for ultrareview` | [命令行错误](#diff-is-too-large-for-ultrareview) |
| `Could not find merge-base with <branch>` | [命令行错误](#could-not-find-merge-base-with-the-base-branch) |
| `Your checkout has no branches (detached HEAD only)` | [命令行错误](#your-checkout-has-no-branches) |
| `Ultrareview clones <owner>/<repo> in the cloud with the GitHub account connected to your Claude account, and none is connected` | [命令行错误](#no-github-account-is-connected-to-your-claude-account) |
| `Your connected GitHub account can't see <owner>/<repo>` | [命令行错误](#your-connected-github-account-cant-see-the-repository) |
| `The GitHub App preflight failed transiently (network or service hiccup) — retry in a moment to start from GitHub instead` | [命令行错误](#the-github-app-preflight-failed-transiently) |
| `Not uploading this working tree` with `the upload cannot follow that setting` | [命令行错误](#the-repository-upload-cant-follow-a-git-setting) |
| `GitHub isn't connected to your Claude account, so this repository can't be cloned in the cloud` | [命令行错误](#github-isnt-connected-to-your-claude-account) |
| `Your GitHub organization has an IP allowlist that is blocking Claude` | [命令行错误](#a-github-organization-policy-is-blocking-claude) |
| `Your GitHub organization requires single sign-on` | [命令行错误](#a-github-organization-policy-is-blocking-claude) |
| `Your GitHub organization's identity provider (Microsoft Entra ID) has a Conditional Access policy that is blocking Claude` | [命令行错误](#a-github-organization-policy-is-blocking-claude) |
| `Single sign-on authorization needed` | [命令行错误](#single-sign-on-authorization-needed) |
| `Failed to resume the conversation` | [命令行错误](#failed-to-resume-the-conversation) |
| `No conversation found with session ID: <session-id>` | [命令行错误](#no-conversation-found-with-the-session-id) |
| `Windows reported an error (EBADF) when Claude Code read this session's transcript file` | [命令行错误](#windows-reported-an-error-ebadf) |
| `Cannot switch renderers in this session` | [命令行错误](#cannot-switch-renderers-in-this-session) |
| `Cannot switch renderers while work is running in the background` | [命令行错误](#cannot-switch-renderers-in-this-session) |
| `Couldn't open Claude Desktop` | [命令行错误](#couldnt-open-claude-desktop) |
| `Failed to open Claude Desktop. Please try opening it manually.` | [命令行错误](#couldnt-open-claude-desktop) |
| `Couldn't read your Zed keymap` / `Couldn't back up your Zed keymap` / `Couldn't update your Zed keymap` | [命令行错误](#terminal-setup-left-your-zed-keymap-unchanged) |
| `Your Zed keymap isn't a readable list of keybindings` | [命令行错误](#terminal-setup-left-your-zed-keymap-unchanged) |
| `Skill usage reports are not available on this connection.` | [命令行错误](#skill-usage-reports-are-not-available-on-this-connection) |
| `Custom output styles can't be selected over Remote Control or from a relayed message` | [命令行错误](#custom-output-styles-cant-be-selected-over-remote-control) |
| `Output styles are saved to local settings (.claude/settings.local.json), which this session doesn't load` | [命令行错误](#output-styles-are-saved-to-local-settings-which-this-session-doesnt-load) |
| `/recap only runs when you ask for it yourself in this session` | [命令行错误](#recap-only-runs-when-you-ask-for-it-yourself) |
| `` `plugin eval` is currently in early access `` / `` `plugin eval` is currently unavailable `` | [Plugin 错误](#plugin-eval-is-currently-in-early-access) |
| `Marketplace "<name>" is registered from an untrusted source` | [Plugin 错误](#marketplace-is-registered-from-an-untrusted-source) |
| `Claude Code refuses the marketplace name "<name>"` | [Plugin 错误](#claude-code-refuses-the-marketplace-name) |
| `Marketplace name impersonates an official Anthropic/Claude marketplace` | [Plugin 错误](#claude-code-refuses-the-marketplace-name) |
| `Marketplace "<name>" is already added from a different source` | [Plugin 错误](#marketplace-is-already-added-from-a-different-source) |
| `"<name>" is another spelling of "<reserved>", a reserved marketplace name` | [Plugin 错误](#marketplace-name-is-another-spelling-of-a-reserved-name) |
| `Marketplace "<name>" is added but ignored` | [Plugin 故障排除](/docs/zh-CN/plugins/troubleshooting#marketplace-is-added-but-ignored) |
| `Marketplace "<name>" is registered but was refused (see the debug log)` | [Plugin 故障排除](/docs/zh-CN/plugins/troubleshooting#marketplace-is-added-but-ignored) |
| `references ${user_config.*} in a shell-form command` | [Plugin 错误](#plugin-command-references-user-config) |
| `Monitor "<name>" from plugin <plugin> references ${user_config.*} in its command` | [Plugin 错误](#plugin-command-references-user-config) |
| `headersHelper for MCP server '<name>' references ${user_config.*}` | [Plugin 错误](#plugin-command-references-user-config) |
| `Plugin archive integrity check failed` | [Plugin 错误](#plugin-archive-integrity-check-failed) |
| `An npm plugin source must name a registry package` | [Plugin 故障排除](/docs/zh-CN/plugins/troubleshooting#an-npm-plugin-source-must-name-a-registry-package) |
| `The packages it lists are not installed` / `The packages it lists were not installed, because` | [Plugin 故障排除](/docs/zh-CN/plugins/troubleshooting#the-packages-it-lists-are-not-installed) |
| `path escapes plugin directory` | [Plugin 错误](#path-escapes-plugin-directory) |
| `path could not be checked` | [Plugin 错误](#path-could-not-be-checked) |
| `its marketplace entry path does not stay inside the marketplace directory` | [Plugin 错误](#marketplace-entry-path-does-not-stay-inside-the-marketplace-directory) |
| `Plugin source path refused` | [Plugin 错误](#marketplace-entry-path-does-not-stay-inside-the-marketplace-directory) |
| `Failed to load marketplace configuration` | [Plugin 错误](#failed-to-load-marketplace-configuration) |
| `Marketplace configuration file is corrupted` | [Plugin 错误](#failed-to-load-marketplace-configuration) |
| `Plugin "<name>@synced" is required by your organization and can't be disabled here` | [Plugin 错误](#plugin-is-required-by-your-organization) |
| `"<plugin>" was not uninstalled: it is still switched on in <file>` | [Plugin 错误](#plugin-was-not-uninstalled) |
| `"<plugin>" was not uninstalled: <file> is there and could not be read` | [Plugin 错误](#plugin-was-not-uninstalled) |
| `Plugin "<plugin>" was not uninstalled: installed_plugins.json` | [Plugin 故障排除](/docs/zh-CN/plugins/troubleshooting#installed-plugins-json-holds-a-record-this-version-cannot-read) |
| `Error: No such tool available: <tool name>` | [工具错误](#no-such-tool-available) |
| `would be spawned with zero tools — refusing` | [工具错误](#agent-would-be-spawned-with-zero-tools) |
| `File is covered by a Read deny rule in your permission settings` | [工具错误](#file-is-covered-by-a-read-deny-rule) |
| `cannot contain null bytes (\0)` | [工具错误](#path-cannot-contain-null-bytes) |
| `Path contains null bytes` | [工具错误](#path-cannot-contain-null-bytes) |
| `subagent_type is required: the general-purpose agent is not available in this session` | [工具错误](#subagent-type-is-required) |
| `Error: this write left the memory index at MEMORY.md at ..., over its ... read limit` | [工具错误](#memory-index-is-over-its-read-limit) |
| `pkill: refusing to run` | [工具错误](#pkill-pattern-matches-the-claude-code-process) |
| `Failed to write to <name>'s inbox — nothing was sent` | [工具错误](#failed-to-write-to-a-teammate-inbox) |
| `Failed to write the plan approval request to the lead's inbox — plan not submitted` | [工具错误](#failed-to-write-to-a-teammate-inbox) |
| `Its agent definition was not restored: the folder its definition file came from is not trusted` | [工具错误](#teammate-agent-definition-not-restored) |
| `Message too large for cross-session delivery` | [工具错误](#message-too-large-for-cross-session-delivery) |
| `Too many messages to this session just now` | [工具错误](#too-many-messages-to-this-session-just-now) |
| `Cross-session message was dropped at the recipient session's inbox` | [工具错误](#cross-session-message-dropped-at-the-inbox) |
| `Refusing to send: reply target is a symlink` / `Refusing to send: cannot vet reply target` | [工具错误](#refusing-to-send-a-cross-session-message) |
| `Refusing to read <path>: its symlink resolution changed after permission was checked (<reason>)` / `Refusing to search <path>: its symlink resolution changed after permission was checked` | [工具错误](#refusing-after-a-symlink-changed) |
| `Refusing to write <path>: its parent-directory symlink resolution changed after permission was checked` / `Refusing to write <path>: it is a symbolic link. Write to the link's target path instead` | [工具错误](#refusing-after-a-symlink-changed) |
| `Refusing to write through symlink: <path>` / `Refusing to write into symlinked directory: <path>` | [工具错误](#refusing-after-a-symlink-changed) |
| `Refusing to write <path>: where it leads on disk could not be determined` / `Refusing to read <path>: where it leads on disk could not be determined` | [工具错误](#refusing-after-a-symlink-changed) |
| `Refusing to search <path>: a path one of its Read deny rules is written through changed while the search was being prepared` / `Refusing to search <path>: it could not be opened` | [工具错误](#refusing-after-a-symlink-changed) |
| `its permission check expired before it ran (too many concurrent file operations)` / `ripgrep was found only by name on PATH` | [工具错误](#refusing-after-a-symlink-changed) |
| `task output swap refused (tasks dir moved or linked)` | [工具错误](#task-output-swap-refused) |
| `Command killed: its output file was replaced or could no longer be verified` | [工具错误](#task-output-swap-refused) |
| `Your disk quota is full on the filesystem with Claude Code's temp directory <dir> (EDQUOT)` | [工具错误](#disk-quota-or-temp-filesystem-is-full) |
| `The filesystem with Claude Code's temp directory <dir>, or your disk quota on it, is full (ENOSPC)` | [工具错误](#disk-quota-or-temp-filesystem-is-full) |
| `Command output was lost: the temp filesystem at <dir> is full` / `is out of inodes` | [工具错误](#disk-quota-or-temp-filesystem-is-full) |
| `the source file is not valid UTF-8 text` / `the source file is not valid UTF-16 text` | [工具错误](#the-source-file-is-not-valid-utf-8-text) |
| `the source file has the replacement character U+FFFD` | [工具错误](#the-source-file-is-not-valid-utf-8-text) |
| `Not published: that file is on a network share` | [工具错误](#not-published-that-file-is-on-a-network-share) |
| `Reading a local file from outside this session's connected folders, or through a link, needs the approval card` | [工具错误](#reading-a-local-file-from-outside-the-connected-folders) |
| `cannot read file_path (...) — the file could not be examined, and no one can answer the approval card` | [工具错误](#reading-a-local-file-from-outside-the-connected-folders) |
| `WebFetch cannot fetch localhost or other hostnames without a dot` | [工具错误](#webfetch-cannot-fetch-localhost) |
| `The safety check for domain ... is rate-limited` | [工具错误](#webfetch-domain-safety-check-failed) |
| `The safety check for domain ... is temporarily rate-limited` | [工具错误](#webfetch-domain-safety-check-failed) |
| `Unable to verify if domain ... is safe to fetch` | [工具错误](#webfetch-domain-safety-check-failed) |
| `Can't open MCP settings while no terminal is attached to this background session` | [后台会话错误](#commands-refused-in-a-background-session) |
| `Can't open MCP settings in a background session` | [后台会话错误](#commands-refused-in-a-background-session) |
| `blocked because the path is spelled in a form that cannot be safely resolved` | [后台会话错误](#write-or-command-blocked-because-the-path-cannot-be-safely-resolved) |
| `blocked because the path is network-shaped` | [后台会话错误](#write-or-command-blocked-because-the-path-names-a-network-location) |
| `is isolated in the worktree <path>, but this command <reason>. Refusing to run it` | [后台会话错误](#command-blocked-by-the-worktree-isolation-checks) |
| `too complex to verify that it stays inside the worktree` | [后台会话错误](#command-blocked-by-the-worktree-isolation-checks) |
| `This session has no saved transcript` | [后台会话错误](#this-session-has-no-saved-transcript) |
| `Can't open — this session is running in another terminal` | [后台会话错误](#this-session-is-running-in-another-terminal) |
| `This conversation is already open in another running Claude session` | [后台会话错误](#this-session-is-running-in-another-terminal) |
| `This session's saved conversation is no longer on disk` | [后台会话错误](#this-sessions-saved-conversation-is-no-longer-on-disk) |
| `kept <id> — its worktree is still at <path>` | [后台会话错误](#worktree-has-commits-that-are-not-pushed-anywhere) |
| `kept <id> — <n> unpushed commits on <branch>` | [后台会话错误](#worktree-has-commits-that-are-not-pushed-anywhere) |
| `kept <id> — worktree has commits that are not pushed anywhere` | [后台会话错误](#worktree-has-commits-that-are-not-pushed-anywhere) |
| `terminal host process died — press Enter to restart` / `This session's terminal host process died` | [后台会话错误](#terminal-host-process-died) |
| `Session isn't responding` / `Press enter again to restart this session — it isn't responding` | [后台会话错误](#session-isnt-responding) |
| `Session <id> was stopped while the respawn was in flight` | [后台会话错误](#session-was-stopped-while-the-respawn-was-in-flight) |
| `This session was running agent '<name>', which is no longer available` | [后台会话错误](#session-agent-no-longer-available) |
| `CLAUDE_CODE_PROCESS_WRAPPER: launcher ...` | [后台会话错误](#claude_code_process_wrapper-launcher-errors) |
| `EUNKNOWN: unknown error, uv_spawn` | [后台会话错误](#eunknown-when-starting-a-background-session) |
| `EACCES: permission denied, posix_spawn` | [后台会话错误](#eacces-when-starting-a-background-session) |
| `exited before it became reachable` | [后台会话错误](#background-service-exited-before-it-became-reachable) |
| `Couldn't start a background session (working directory no longer exists or is not accessible: ...)` | [后台会话错误](#working-directory-no-longer-exists-when-starting-a-background-session) |
| `Workspace not trusted.` when starting or restarting a background session | [后台会话错误](#workspace-not-trusted-when-dispatching-a-background-session) |
| `Claude Code is being updated by npm on this machine (still not runnable after 2 min, ...)` | [后台会话错误](#eacces-when-starting-a-background-session) |
| `Claude Code process exited with code N` | [包装器和 IDE 错误](#claude-code-process-exited-with-code-n) |
| `The connection to Claude Code ended before this message completed` | [包装器和 IDE 错误](#the-connection-to-claude-code-ended-before-this-message-completed) |
| `Could not locate the Claude CLI on PATH` | [包装器和 IDE 错误](#could-not-locate-the-claude-cli-on-path) |
| `Restored the code, but skipped N files` | [Rewind 警告和错误](#restored-the-code-but-skipped-files) |
| `No files were restored: N files failed (backup missing, or the file could not be updated)` | [Rewind 警告和错误](#no-files-were-restored) |
| `Transcript writes are failing (...)` | [会话保存警告](#transcript-writes-are-failing) |
| `Transcript saving is off — CLAUDE_CODE_SKIP_PROMPT_HISTORY is set` | [会话保存警告](#transcript-saving-is-off-skip-prompt-history) |
| `Transcript saving is off — inherited CLAUDE_CODE_CHILD_SESSION marker` | [会话保存警告](#transcript-saving-is-off-child-session-marker) |
| `Claude Code's fullscreen renderer didn't finish starting last time on this machine` / `Claude Code's fullscreen renderer has repeatedly failed to start on this machine` | [全屏渲染](/docs/zh-CN/fullscreen#fullscreen-renderer-didnt-finish-starting) |
| `Claude Code exited after an unrecoverable interface error (...)` | [配置警告](#exited-after-an-unrecoverable-interface-error) |
| `Agent descriptions are over the 15.0k-token limit` | [配置警告](#agent-descriptions-are-over-the-15000-token-limit) |
| `Not loaded: rename <path>, then restart — its name uses "<name>", a name reserved for the skills synced from your claude.ai account` | [配置警告](#a-skill-command-or-workflow-wasnt-loaded-because-its-name-is-reserved) |
| `Ignoring N permissions.allow entries from ... this workspace has not been trusted` | [配置警告](#workspace-has-not-been-trusted) |
| `is a network path, which cannot be added as a working directory` | [配置警告](#working-directory-is-a-network-path) |
| `Remote managed settings failed to load (<cause>)` | [配置警告](#remote-managed-settings-failed-to-load) |
| `Managed settings were not approved; exiting without applying them.` | [配置警告](#managed-settings-were-not-approved) |
| `Claude Code can't start: your organization's managed settings block the default model` / `Claude Code can't start: your organization allows only the models listed in "availableModels"` | [配置警告](#managed-settings-block-the-default-model) |
| `Your organization's managed settings allow Claude Code to use: <providers>` | [配置警告](#managed-settings-dont-allow-this-api-provider) |
| `Your organization's managed settings allow Claude Code to use no API provider at all` | [配置警告](#managed-settings-dont-allow-this-api-provider) |
| `MCP server <name> is blocked by enterprise managed policy` | [配置警告](#mcp-server-is-blocked-by-enterprise-managed-policy) |
| `Managed settings document could not be parsed as a JSON object; none of its settings are in effect. Fix or remove it.` | [配置警告](#managed-settings-document-could-not-be-parsed) |
| `Managed settings drop-in directory could not be read` | [配置警告](#managed-settings-document-could-not-be-parsed) |
| `Unable to read managed policy settings` | [配置警告](#unable-to-read-managed-policy-settings) |
| `otelHeadersHelper failed; telemetry is not being exported. See /status: ...` | [配置警告](#otelheadershelper-failed) |
| `"crossSessionInbound" must be one of "accept", "hold", "refuse"` | [配置警告](#crosssessioninbound-must-be-one-of-accept-hold-refuse) |
| `API Error: ANTHROPIC_FOUNDRY_RESOURCE must be a Foundry resource name` | [配置警告](#anthropic-foundry-resource-must-be-a-foundry-resource-name) |
| `headersHelper not run — this workspace has no persisted trust` | [配置警告](#headershelper-not-run) |
| `Invalid permission rule "..." was skipped: Malformed Tool(content) rule` | [配置警告](#malformed-tool-content-rule) |
| `... is not matched by file permission checks` | [配置警告](#is-not-matched-by-file-permission-checks) |
| `... has a wildcard before the rest of the command` | [配置警告](#has-a-wildcard-before-the-rest-of-the-command) |
| `Denying Bash also turns off the PowerShell tool, so Claude has neither` | [配置警告](#denying-bash-also-turns-off-the-powershell-tool) |
| `CLAUDE_CODE_DISABLE_1M_CONTEXT is set, but the 200K limit isn't enforced` | [配置警告](#the-200k-limit-isnt-enforced) |
| `[claude-code:unrecognized_model]` | [配置警告](#unrecognized-model-id-on-a-request) |
| `Stale sandbox mask files left by a killed session` | [配置警告](#stale-sandbox-mask-files-left-by-a-killed-session) |
| 响应质量似乎比平时低 | [响应质量](#responses-seem-lower-quality-than-usual) |

<h2 id="automatic-retries">
  自动重试
</h2>

Claude Code 在显示错误之前，会以指数退避方式重试瞬时故障最多 10 次。它并不总是重试在 Claude 响应过程中途出现的故障。当您看到本页面上的错误之一时，Claude Code 已经对该故障进行了适用的重试。

Claude Code 重试这些故障：

* 在 Claude 响应开始流式传输之前到达的服务器错误、过载响应和请求超时。
* 在 Claude 完成思考之后、但在开始任何文本或工具调用之前到达的服务器错误或过载响应。Claude Code 会在该点重试服务器错误最多两次。在 v2.1.284 之前，Claude Code 会在该点以该错误结束轮次。
* 连接断开。当连接在请求过程中途断开，且 Claude 尚未完成其响应的任何部分（包括其思考过程）时，Claude Code 会使用相同的退避重新发送请求，轮次继续进行，即使某些文本已经开始流式传输。当连接在 Claude 完成思考之后但在开始任何文本或工具调用之前断开时，Claude Code 改为快速连续重新发送请求最多两次，如果连接在该点继续断开，则以 `Connection lost before a response was produced` 结束轮次。
* Claude Code 检测到的连接在您的计算机进入睡眠状态时在请求过程中途被破坏。Claude Code 将其计为上述规则下的断开连接；一旦重试标签命名了具体原因，它会读作 `Connection lost while your computer was asleep`，如果轮次在 Claude 完成思考之后但在任何文本或工具调用之前结束，消息会读作 `Your computer went to sleep before a response was produced`。
* 停滞的响应流，当响应头已到达但 Claude 响应的任何部分都未到达，或当 Claude 完成思考但尚未开始任何文本或工具调用时：Claude Code 中止停滞连接并最多重新发送一次请求，不计入上述 10 次尝试预算。如果响应在 Claude 完成思考之后但在任何文本或工具调用之前第二次停滞，Claude Code 以 `The response stalled before a response was produced` 结束轮次。
* 流式请求 API 从未用响应头回答，在 [first-byte deadline runs](/docs/zh-CN/network-config#streaming-idle-watchdogs) 的连接上：Claude Code 在截止时间中止它，并在重试预算内每个模型请求最多重新发送一次，然后如果该尝试也未得到回答，则以 [No response from API](#no-response-from-api) 结束轮次。在其他连接上，请求等待 `API_TIMEOUT_MS`。当您设置 `CLAUDE_CODE_RETRY_WATCHDOG` 时，一次重试上限不适用。
* 在 Claude 完成思考或开始任何文本或工具调用之前，被 API 输出内容过滤器拦截的流式响应。Claude Code 会在重试预算内重新发送一次请求，如果过滤器也拦截了第二次响应，则显示 [Output blocked by content filtering policy](#output-blocked-by-content-filtering-policy)。
* 临时 429 节流，但不是网关的支出限制 `429`，这不是节流；请参阅 [Spend limit reached](#spend-limit-reached)。
  * 当您使用 claude.ai 订阅登录时，这包括不携带您套餐配额头的 429 节流。在 v2.1.199 之前，Claude Code 仅对 API 密钥和企业登录重试这些节流。
* 因为输入加上 `max_tokens` 超过上下文限制而被拒绝的请求。以相同方式重新发送它会以相同方式失败，所以 Claude Code 使用减少的 `max_tokens` 重试，并在两种情况下停止重试并改为压缩：
  * 当没有减少可以适应时，例如当对话本身几乎填满上下文窗口时。
  * 当重试无法进一步缩小 `max_tokens` 时。在 v2.1.218 之前，Claude Code 可以重新发送仍然不适应的减少请求，例如当扩展思考预算超过剩余上下文时，直到重试预算用尽。
* [Google Cloud 的 Agent Platform](/docs/zh-CN/google-vertex-ai) 上过期或缺失的 Google Cloud 凭据，或在您的机器上加载失败的 AWS 凭据。Claude Code 丢弃其缓存的凭据并重试最多两次，然后报告错误以便您可以立即重新身份验证，如 [Could not load AWS or Google Cloud credentials](#could-not-load-aws-or-google-cloud-credentials) 下所述。在 v2.1.228 之前，Claude Code 通过完整重试预算重试失败的 Google Cloud 凭据，然后显示错误。
* 来自 Anthropic API 的 `401` 或 `403`，直接或通过 [LLM gateway](/docs/zh-CN/llm-gateway)，而 [`apiKeyHelper`](/docs/zh-CN/settings-reference#apikeyhelper) 脚本提供凭据。Claude Code 重新运行脚本并使用其新输出重试，在完整重试预算内。当脚本本身在重新运行时失败时，Claude Code 改为显示 [Your apiKeyHelper script is failing](#your-apikeyhelper-script-is-failing)。

在 v2.1.227 之前，`Connection lost before a response was produced` 读作 `Connection closed while thinking, before producing a response`，`The response stalled before a response was produced` 读作 `Response stalled while thinking, before producing a response`。

Claude Code 不重试这些故障：

* TLS 证书验证失败，例如 TLS 检查代理、缺失的 `NODE_EXTRA_CA_CERTS` 包或过期的证书。Claude Code 在第一次尝试时报告错误，以便您可以立即修复证书设置；请参阅 [SSL certificate errors](#ssl-certificate-errors)。Claude Code 仍然重试瞬时 TLS 条件，例如握手超时。在 v2.1.199 之前，Claude Code 通过完整重试预算重试证书失败，然后显示错误。
* 服务器错误、断开连接或停滞流在 Claude 完成文本块或工具调用之后到达，或在完成思考之后开始一个但在完成响应之前。Claude Code 不重新运行请求，因为这可能会执行相同的工具调用两次。它保留 Claude 完成的内容，运行 Claude 完成的任何工具调用，并从其结果继续轮次。对于您在交互式会话和非交互式会话中看到的内容，请阅读 [The response above may be incomplete](#the-response-above-may-be-incomplete)。在 v2.1.199 之前，当服务器错误在流中途到达时，Claude Code 丢弃部分输出并将整个轮次报告为错误。
* 在 Claude 完成响应之后到达的故障：无需重试任何内容，所以 Claude Code 保留完整响应并正常结束轮次。
* [Amazon Bedrock 流式响应具有意外的 content-type](#bedrock-streaming-response-has-an-unexpected-content-type)，因为重写响应的网关或代理会以相同方式重写重试。需要 Claude Code v2.1.208 或更高版本。
* 失败的流式请求的非流式重试获得成功状态但 [body 中没有 Claude API 消息](#api-returned-an-empty-or-malformed-response)。Claude Code 以该错误结束轮次。
* 您的组织的策略检查拒绝的请求，其表现为携带拒绝消息的 `API Error:` 行。您的组织管理员使用 [Inference hooks](https://platform.claude.com/docs/en/manage-claude/inference-hooks)（Claude Enterprise 功能）设置检查，消息以他们配置的说明结尾，或默认告诉您联系他们。Claude Code 不会将拒绝的请求重新发送到相同模型或 [备用模型](/docs/zh-CN/model-config#fallback-model-chains)，因为拒绝涉及请求的内容而不是模型。在 v2.1.239 之前，Claude Code 可以重新发送拒绝的请求，不流式传输或在配置的备用模型上，然后向您显示拒绝。

<h3 id="what-you-see-while-claude-code-retries-or-waits">
  Claude Code 重试或等待时您看到的内容
</h3>

重试时，微调器在错误标签后显示 `Retrying in Ns · attempt x/y` 倒计时。标签命名第一次尝试的具体原因，用于您可以立即采取行动的故障：网络已关闭、TLS 握手失败或您达到速率限制。对于其他错误，它最初读作 `API error`。从 v2.1.198 开始，它切换到第三次尝试的具体原因，或当 `CLAUDE_CODE_MAX_RETRIES` 允许少于三次时在最后一次尝试；较早版本仅在最后一次尝试时切换。

从 v2.1.198 开始，通常的微调器提示在重试期间被抑制。一旦错误原因被揭示，如果故障是 529 过载，倒计时下方的行也命名了检查服务状态的位置：Anthropic API 上的 `status.claude.com`，或其他配置上的提供商或网关主机。

如果在请求仍然待处理时响应流上 20 秒内没有数据到达，微调器显示 `Waiting for API response · will retry in … · check your network`，然后任何重试都尚未开始。请求尚未失败：倒计时运行到 Claude Code 中止停滞连接的点。中止后，您看到的内容取决于响应已进行的距离：

* 在 Claude 完成文本块或工具调用之前，或在完成思考之后开始一个，Claude Code 重试请求或以错误结束轮次。[Automatic retries](#automatic-retries) 说明它重试哪些停滞以及多少次。
* 在 Claude 完成文本块或工具调用之后，或在完成思考之后开始一个，但在 Claude 完成响应之前，Claude Code 保留 Claude 完成的内容，从 Claude 完成的任何工具调用继续轮次，并显示 [The response above may be incomplete](#the-response-above-may-be-incomplete)。在非交互式会话中，以及对于任何会话中的子代理响应，Claude Code 可能首先提示 Claude 继续响应；该条目说明何时执行以及何时您仍然在那里看到通知。
* 在 Claude 完成响应之后，Claude Code 正常结束轮次。

一旦数据恢复或重试成功，横幅会自动清除。如果它在每次尝试时重新出现，将其视为 [network issue](#unable-to-connect-to-api)。在 v2.1.185 之前，横幅在 10 秒后出现，措辞不同。

当 Claude 咨询 [advisor](/docs/zh-CN/advisor) 时，横幅在 90 秒无数据后出现，而不是 20 秒，因为长时间的顾问审查可能在远超 20 秒的时间内不发送任何数据。在 v2.1.214 之前，20 秒阈值也适用于顾问调用，所以横幅在顾问审查期间出现，即使没有任何问题。

<h3 id="tune-retry-behavior">
  调整重试行为
</h3>

您可以使用这些环境变量调整重试行为：

| 变量 | 默认值 | 效果 |
| :- | :- | :- |
| [`CLAUDE_CODE_MAX_RETRIES`](/docs/zh-CN/env-vars) | 10 | 重试尝试次数。从 v2.1.186 开始上限为 15；从 v2.1.199 开始 `CLAUDE_CODE_RETRY_WATCHDOG` 提高默认值并移除上限。降低它以在脚本中更快地显示故障。 |
| [`CLAUDE_CODE_RETRY_WATCHDOG`](/docs/zh-CN/env-vars) | 未设置 | 在 CI 作业等无人值守会话中设置为 `1`，以无限期重试 `429` 和 `529` 容量错误，而不是在 `CLAUDE_CODE_MAX_RETRIES` 尝试后失败。当标准速度请求获得报告支出限制或耗尽使用额度的 `429` 时，Claude Code 立即失败，即使来自 [gateway spend cap](#spend-limit-reached) 的也是如此，该上限按计划重置。在 v2.1.239 之前，看门狗无限期重试这些。对于快速模式请求，请参阅 [Handle rate limits](/docs/zh-CN/fast-mode#handle-rate-limits)。在 v2.1.199 或更高版本上，它还为其他瞬时错误（例如服务器错误、超时和断开连接）提高默认重试计数至 300，大约三小时的退避，如果您明确设置该变量，则移除 `CLAUDE_CODE_MAX_RETRIES` 的 15 上限。 |
| [`CLAUDE_CODE_OVERLOADED_RETRY_BASE_DELAY_MS`](/docs/zh-CN/env-vars) | 500 | 当 API 以 `529` 过载错误拒绝请求时，该请求各次重试之间退避的起始延迟（毫秒）。当 API 容量已满时，可将其提高（最高 32000），以便在更长的时间窗口内分散重试。当 `CLAUDE_CODE_RETRY_WATCHDOG` 设置为 `1`，或被拒绝的请求是在[快速模式](/docs/zh-CN/fast-mode#handle-rate-limits)下发送时，此变量无效。需要 Claude Code v2.1.292 或更高版本。 |
| [`API_TIMEOUT_MS`](/docs/zh-CN/env-vars) | 600000 | 每个请求的超时（毫秒）。为慢速网络或代理提高它。它还限制 Claude Code 等待响应头的时间，在 [No response from API](#no-response-from-api) 中描述。 |
| [`CLAUDE_CODE_NONSTREAMING_TIMEOUT_RETRIES`](/docs/zh-CN/env-vars) | 未设置 | 超时的[非流式请求](#streaming-response-ended-before-any-complete-data-was-received)的重新发送次数限制。达到该限制时，请求失败。生成时间超过超时时间的 Claude 响应在每次重新发送时都会再次超时，因此请设置较低的数值（例如 `0`）以更快地失败。在本地会话中，每次非流式尝试在 300 秒后超时；当您为 `API_TIMEOUT_MS` 设置正值时，则在该值指定的时间后超时。需要 Claude Code v2.1.285 或更高版本。 |
| [`CLAUDE_STREAM_FIRST_BYTE_TIMEOUT_MS`](/docs/zh-CN/env-vars) | 未设置 | 流式请求的第一个响应字节的截止时间（毫秒）。需要 Claude Code v2.1.242 或更高版本。对于当此未设置时 Claude Code 如何选择截止时间，请参阅 [No response from API](#no-response-from-api)。 |

<h2 id="server-errors">
  服务器错误
</h2>

这些错误中的大多数来自推理提供商：Anthropic API 上的 Anthropic 服务，以及 Amazon Bedrock、Google Cloud 的 Agent Platform、Microsoft Foundry 或自定义网关上该提供商端点后面的服务。[自动模式无法确定操作的安全性](#auto-mode-cannot-determine-the-safety-of-an-action)和[Agent 因 API 错误而提前终止](#agent-terminated-early-due-to-an-api-error)也涵盖了您这一方的原因，例如无法调用分类器模型的 Amazon Bedrock 账户或达到用量限制的子代理。

<h3 id="api-error-500-internal-server-error">
  API Error: 500 Internal server error
</h3>

Claude Code 显示任何 5xx 响应的状态代码和 API 的错误消息。下面的示例显示 Anthropic API 上的 500 响应：

```text theme={null}
API Error: 500 Internal server error. This is a server-side issue, usually temporary — try again in a moment. If it persists, check https://status.claude.com.
```

尾部句子指出了检查服务健康状况的位置，因提供商而异。Amazon Bedrock、Google Cloud 的 Agent Platform 和 Microsoft Foundry 配置会指出该提供商的服务状态。自定义 `ANTHROPIC_BASE_URL` 会指出网关主机。

API 本身的 5xx 表示 API 内部出现了意外故障。它不是由您的提示词、设置或账户引起的。

当代理、负载均衡器或网关用 HTML 错误页面回复时，消息显示状态代码和页面的标题，例如 `API Error: 502 Bad Gateway`。对于没有标题的页面，消息显示状态代码及其标准名称。在 v2.1.281 之前，当页面有标题时状态代码被丢弃，当页面没有标题时打印页面的原始标记。

**应该做什么：**

* 检查 [status.claude.com](https://status.claude.com) 或消息中指出的提供商状态页面，查看是否有活跃事件
* 等待一分钟，然后再次发送您的消息。您的原始消息仍在对话中，因此对于较长的提示词，您可以输入 `try again` 而不是粘贴整个内容。
* 如果错误持续存在且没有发布事件，请运行 `/feedback` 以便 Anthropic 可以使用您的请求详情进行调查。如果您的环境中 `/feedback` 不可用，请参阅[报告错误](#report-an-error)。

<h3 id="api-error-repeated-529-overloaded-errors">
  API Error: Repeated 529 Overloaded errors
</h3>

API 在所有用户中暂时处于容量限制。Claude Code 在显示此消息之前已经重试了多次：

```text theme={null}
API Error: Repeated 529 Overloaded errors. The API is at capacity — this is usually temporary. Try again in a moment. If it persists, check https://status.claude.com.
```

尾部句子因提供商而异，方式与上面的 500 错误相同。

529 不是您的用量限制，也不会计入您的配额。

**应该做什么：**

* 检查 [status.claude.com](https://status.claude.com) 或消息中指出的提供商状态页面，查看容量通知
* 几分钟后重试
* 运行 `/model` 并切换到不同的模型以继续工作，因为容量是按模型跟踪的。当一个模型处于特别高的负载下时，Claude Code 会提示您这样做，例如 `Opus is experiencing high load, please use /model to switch to Sonnet`。在 Fable 模型上，消息指出 Fable。

  在 Claude Desktop 应用运行的会话中，例如 Code 标签页或 Cowork，消息读作 `Opus is experiencing high load. Switch to Sonnet.`，您可以使用应用的模型选择器切换模型。

<h3 id="request-timed-out">
  Request timed out
</h3>

API 在连接截止时间之前没有响应。

```text theme={null}
Request timed out
```

这可能在高负载期间或模型生成非常大的响应时发生。默认请求超时时间为 10 分钟。

**应该做什么：**

* 重试请求
* 如果是缓慢的网络或代理导致，请按照[自动重试](#automatic-retries)中的说明提高 `API_TIMEOUT_MS`
* 如果超时频繁且您的网络状况良好，请参阅下面的[网络和连接错误](#network-and-connection-errors)

<h3 id="no-response-from-api">
  No response from API
</h3>

Claude Code 发送了流式请求，API 在第一个字节的截止时间内没有返回响应头，因此 Claude Code 中止了请求，而不是等待完整的 `API_TIMEOUT_MS` 请求超时时间（默认为 10 分钟）。Claude Code 最多再发送一次请求，如果[重试预算](#tune-retry-behavior)允许的话。当重试也没有得到回复时，该轮次以此消息结束，该消息显示每次尝试等待了多长时间。当您设置 [`CLAUDE_CODE_RETRY_WATCHDOG`](/docs/zh-CN/env-vars) 时，一次重试的上限不适用，Claude Code 在[调整重试行为](#tune-retry-behavior)中描述的预算下重试。

```text theme={null}
API Error: No response from API (waited 3m, then 10m on the retry). If a proxy or gateway on your network holds responses until they complete, raise API_TIMEOUT_MS or CLAUDE_STREAM_FIRST_BYTE_TIMEOUT_MS to wait longer.
```

Claude Code 分别为第一次尝试的等待响应头和重试的等待设置：

* **第一次尝试**：当您将其设置为 1 或更多时使用 [`CLAUDE_STREAM_FIRST_BYTE_TIMEOUT_MS`](/docs/zh-CN/env-vars)，限制在 10 秒到 30 分钟之间。否则 Claude Code 使用[流式空闲监视程序](/docs/zh-CN/network-config#streaming-idle-watchdogs)中列出的字节级监视程序超时时间，因此改变该超时时间的变量也会改变此等待。无论哪种方式，Claude Code 为请求体的每 32KB 添加一秒。
* **重试**：比 `API_TIMEOUT_MS` 少一秒，默认略低于 10 分钟，以便重试可以超过保持响应直到生成完成的代理或网关。在 Amazon Bedrock 上，重试使用与第一次尝试相同的截止时间，消息显示一个持续时间而不是两个。

两个等待都不超过正 `API_TIMEOUT_MS` 少一秒，正 `API_TIMEOUT_MS` 低于 11 秒会关闭截止时间。字节级监视程序仅在响应头到达后才开始，因此在此之后停止发送字节的响应遵循[停滞流规则](#automatic-retries)而不是此截止时间。

**应该做什么：**

* 再次发送您的消息。您的原始消息仍在对话中，因此对于较长的提示词，您可以输入 `try again` 而不是粘贴整个内容。
* 如果重复出现，将其视为[网络或代理问题](#unable-to-connect-to-api)。
* 如果您网络上的代理或网关保持响应直到完成，请提高 `API_TIMEOUT_MS` 以便重试等待更长时间。在 Amazon Bedrock 上，也提高 `CLAUDE_STREAM_FIRST_BYTE_TIMEOUT_MS`。
* 如果第一次尝试持续超时，然后重试成功，请提高 `CLAUDE_STREAM_FIRST_BYTE_TIMEOUT_MS` 以便第一次尝试也等待足够长的时间。

在 v2.1.242 之前，Claude Code 在未回复的流式请求失败之前等待完整的 `API_TIMEOUT_MS` 请求超时时间（默认为 10 分钟）。在 v2.1.261 之前，重试等待与第一次尝试相同的截止时间，消息没有显示持续时间。

<h3 id="the-response-above-may-be-incomplete">
  The response above may be incomplete
</h3>

流式请求在响应仍在进行中时失败，在 Claude 完成了一个文本块或工具调用之后，或在完成思考后开始了一个。重新发送请求可能会运行相同的工具调用两次，因此 Claude Code 保留 Claude 完成的输出并附加此通知，而不是丢弃该轮次。您看到的变体指出了原因：

```text theme={null}
API Error: Server error mid-response. The response above may be incomplete.
API Error: Connection lost mid-response. The response above may be incomplete.
API Error: Your computer went to sleep mid-response. The response above may be incomplete.
API Error: The response stopped arriving. The response above may be incomplete.
API Error: Part of the response never arrived. The response above may be incomplete.
API Error: The response stream was malformed. The response above may be incomplete.
```

* `Server error mid-response`：中流过载或 5xx 服务器错误。此变体需要 Claude Code v2.1.199 或更高版本；在此之前，该情况会丢弃部分输出并将整个轮次报告为错误。
* `Connection lost mid-response`：连接断开。您也会在代理或网关在响应完成之前干净地结束响应体时看到此变体。
* `Your computer went to sleep mid-response`：Claude Code 检测到您的计算机在响应流式传输时进入睡眠状态。一旦您的计算机唤醒，Claude Code 会将连接视为断开并停止从中读取。
* `Part of the response never arrived`：流事件在 API 和 Claude Code 之间被丢弃，因此后来的事件引用了从未到达的内容。在 v2.1.281 之前，此情况以 `API Error: Content block not found` 结束轮次。
* `The response stream was malformed`：为已完成的内容块到达了事件，或事件到达时已损坏。损坏的事件是指其数据不是有效 JSON、其内容缺失或其内容与事件类型不匹配的事件。在 v2.1.284 之前，当具有无效 JSON 的事件在 Claude 完成其思考、文本块或工具调用后到达时，解析器的原始错误（例如以 `API Error: JSON Parse error` 开头的错误）出现。
* `The response stopped arriving`：连接保持打开但停止传递数据，因此流式空闲监视程序中止了它。在 v2.1.222 之前，Claude Code 也可能在通过 `ANTHROPIC_BASE_URL` 或 `ANTHROPIC_AWS_BASE_URL` 到达的[网关](/docs/zh-CN/gateways)连接上报告此故障，同时服务器的保活 ping 仍在到达，因为它只在那里计算已解析的响应事件；升级会在这些路由上停止这些虚假超时。通过提供商基础 URL（如 `ANTHROPIC_BEDROCK_BASE_URL`）到达的网关不被字节监视程序包装；请参阅[流式空闲监视程序](/docs/zh-CN/network-config#streaming-idle-watchdogs)。

在 v2.1.227 之前，`Connection lost mid-response` 读作 `Connection closed mid-response`，`The response stopped arriving` 读作 `Response stalled mid-stream`。

当丢弃、重复或损坏的流事件在 Claude 开始任何文本或工具调用之前到达时，您看不到此通知：

* 如果 Claude 仅完成了其思考，Claude Code 会重新发出请求。当重新发出的流以相同方式中断时，轮次以 `Part of the response never arrived and no response was produced. Try again.` 或 `The response stream was malformed and no response was produced. Try again.` 结束。
* 如果没有完成任何内容，Claude Code 会改为重新发送请求而不流式传输。如果您使用 [`CLAUDE_CODE_DISABLE_NONSTREAMING_FALLBACK`](/docs/zh-CN/env-vars) 关闭了该回退，轮次以 `API Error: Content block not found`（对于丢弃的事件）或 `API Error: Content block already closed`（对于重复的事件）结束。对于损坏的事件且回退关闭，轮次以 `API Error: Stream event unreadable` 或解析器的原始错误结束。

在四种情况下，Claude Code 处理故障而不立即显示此通知：

* 在响应的早期，Claude Code 要么重试故障，要么以不同的错误结束轮次。请参阅[自动重试](#automatic-retries)。
* 当这些故障之一在 Claude 完成响应后到达时，Claude Code 保留完整响应并正常结束轮次，没有此通知。在 v2.1.222 之前，当连接在响应完成后断开或停滞时，Claude Code 显示此通知，并将轮次报告为错误，即使响应是完整的。
* 在[非交互式会话](/docs/zh-CN/headless)中，例如 `-p` 运行、[Agent SDK](/docs/zh-CN/agent-sdk/overview) 运行或[云端会话](/docs/zh-CN/claude-code-on-the-web)，当截断响应在主对话中且包含文本但没有工具调用时，您不必自己发送 `continue`：Claude Code 保留部分输出并提示 Claude 从停止的地方继续，最多连续三次。您只有在 Claude Code 用完这些继续后才会看到此通知。在 v2.1.246 之前，Claude Code 在第一次截断时以此通知结束非交互式轮次。
* 在[子代理](/docs/zh-CN/sub-agents#api-errors-in-subagents)中，无论会话是否交互式：当其截断响应包含文本但没有工具调用时，Claude Code 提示子代理继续。通知仅在这些继续用完后才成为子代理的最后一条消息。在 v2.1.257 之前，子代理在第一次截断时显示此通知。

**应该做什么：**

* 在交互式会话中，阅读屏幕上剩余的响应：Claude Code 保留 Claude 在错误前完成的每个块，但当轮次结束时丢弃中断的最后块，因此最后的句子或工具调用可能会丢失。回复 `continue` 以让 Claude 从其最后完成的块继续。
* 在[非交互模式](/docs/zh-CN/headless)（`-p`）中：
  * 使用默认文本输出，Claude Code 打印它仍然从轮次早期保留的最后完成的文本块，然后是此消息。当它不保留任何内容时，Claude Code 仅打印此消息，例如因为 Claude Code 在轮次中间压缩了对话并清除了该文本。在 v2.1.219 之前，Claude Code 仅在 `-p` 文本输出中打印此消息并丢弃它已经生成的响应。
  * 使用 `--output-format json` 或 `stream-json`，Claude Code 在 `result` 字段中报告此消息。
  * 一旦连接稳定，要继续该轮次，请恢复会话并按照[继续对话](/docs/zh-CN/headless#continue-conversations)中的说明发送 `continue`。

<h3 id="auto-mode-cannot-determine-the-safety-of-an-action">
  Auto mode cannot determine the safety of an action
</h3>

[自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)使用的模型无法对操作进行分类，因此自动模式没有自动批准该操作。您看到的消息取决于分类器如何失败。

对工作目录内的读取、搜索和编辑会跳过分类器，因此它们在所有这些情况下都继续工作。

当分类器模型不可用时：

```text theme={null}
<model> is temporarily unavailable, so auto mode cannot determine the safety of <tool> right now. Wait a moment and then try this action again.
```

当 Claude Code 可以确定故障类别时，它在 `temporarily unavailable` 后的括号中指出该类别，例如 `<model> is temporarily unavailable (rate-limited), so auto mode cannot determine the safety of <tool> right now`。类别为 `(rate-limited)`、`(overloaded)`、`(server error)`、`(timed out)` 和 `(connection failed)`。如果 `(timed out)` 或 `(connection failed)` 重复出现，请检查您的连接；请参阅[无法连接到 API](#unable-to-connect-to-api)。在 v2.1.229 之前，消息从不指出类别，读作 `Wait briefly and then try this action again`。

当没有类别适用时，消息出现时括号中没有类别；多个故障会产生该形式。在 [Amazon Bedrock](/docs/zh-CN/amazon-bedrock) 上，包括 [Mantle 端点](/docs/zh-CN/amazon-bedrock#use-the-mantle-endpoint)，当您的 AWS 账户无法调用消息中指出的模型时，它也会出现，该故障在每次重试时重复，直到您的账户被授予访问该模型的权限。

**应该做什么：**

* 几秒后重试；Claude 看到相同的消息，通常会自动重试。暂时故障与[自动模式资格](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)无关；您不需要更改设置
* 如果重试持续失败，继续进行只读任务，稍后回到被阻止的操作
* 在 Amazon Bedrock 上，如果消息在每次重试时返回，请检查您的账户是否可以调用它指出的模型：对于标准 Amazon Bedrock 模型，确认您的 [IAM 策略](/docs/zh-CN/amazon-bedrock#iam-configuration)允许调用它；对于 Mantle 模型 ID，[联系您的 AWS 账户团队](/docs/zh-CN/amazon-bedrock#mantle-endpoint-errors)

当分类器请求失败是因为您的 OAuth 令牌过期或被另一个会话轮换时，Claude Code 刷新令牌并重试请求一次，因此常规的令牌过期不会显示为此消息。在 v2.1.216 之前，过期或轮换的令牌会导致每个分类器请求失败，自动模式会以此消息拒绝每个检查的操作，直到令牌被刷新。

当分类器返回无法解析的响应时：

```text theme={null}
Auto mode could not evaluate this action and is blocking it for safety — run with --debug for details
```

**应该做什么：**

* 重试该操作；这通常在下一次尝试时成功
* 运行 `claude --debug` 并重复该操作以在调试日志中查看详情

当单独的 API 安全检查因早期对话内容而阻止分类器请求时：

```text theme={null}
Auto mode could not evaluate this action and is blocking it for safety — a safety check separate from auto mode blocked this request because of earlier conversation content — it isn't about the action itself — run with --debug for details
```

Claude Code 拒绝该操作，但告诉 Claude 这不是对该操作不安全的判断，并继续进行其他任务而不是重试。这些拒绝不计入[自动模式的暂停阈值](/docs/zh-CN/permission-modes#when-auto-mode-falls-back)。在[非交互式](/docs/zh-CN/headless) `-p` 运行中，Claude Code 不会停止运行。Claude 接收的内容取决于它请求操作的位置：

* 对于 `-p` 运行中没有 `--input-format stream-json` 的[后台子代理](/docs/zh-CN/sub-agents#run-subagents-in-foreground-or-background)，Claude Code 返回包含 `Agent aborted: auto mode classifier request refused by the safety safeguard in headless mode` 的错误结果
* 在其他地方，包括交互式会话和 `-p` 运行的主对话，Claude Code 将该拒绝返回给 Claude

在 v2.1.225 之前，Claude Code 将这些拒绝计入暂停阈值，并返回与真正分类器阻止相同的拒绝消息。

**应该做什么：**

* 这不是对您的操作的决定。您对话中已有的内容在自动模式将对话发送给分类器时触发了 API 上的安全过滤器
* 重试无法帮助；相同的对话内容将再次触发过滤器
* 在交互式会话中，切换到不同的[权限模式](/docs/zh-CN/permission-modes)，以便您可以在提示时批准该操作
* 开始一个新对话，不包含触发内容

当对话增长到超过分类器的上下文窗口时：

```text theme={null}
Auto mode classifier transcript exceeded context window — falling back to manual approval (try /compact to reduce conversation size)
```

操作发生的情况取决于 Claude 请求它的位置：

* 在交互式会话中，自动模式回退到该操作的正常权限提示，以便您可以手动批准或拒绝它
* 对于[非交互式](/docs/zh-CN/headless) `-p` 运行中没有 `--input-format stream-json` 的[后台子代理](/docs/zh-CN/sub-agents#run-subagents-in-foreground-or-background)，Claude Code 返回包含 `Agent aborted: auto mode classifier transcript exceeded context window in headless mode` 的错误结果，运行继续
* 在 `-p` 运行中的其他地方，没有 [`--permission-prompt-tool`](/docs/zh-CN/cli-reference#cli-flags)，没有提示可以回退到，因此操作不运行，运行继续

**应该做什么：**

* 在交互式会话中，在出现的提示中批准或拒绝该操作
* 在交互式会话中，运行 `/compact` 以减少对话大小，以便后续操作再次适应分类器窗口

<h3 id="the-server-returned-no-safety-verdict">
  The server returned no safety verdict
</h3>

在[服务器端分类器审查](/docs/zh-CN/permission-modes#server-side-classifier-review)下，当服务器对操作没有给出判决时，自动模式拒绝该操作。当 Claude Code 可以确定一个类别时，拒绝会在括号中指出一个类别，例如 `(timed out)`：

```text theme={null}
The server-side auto mode classifier gave no verdict (timed out), so auto mode cannot determine the safety of <tool>.
```

消息的其余部分告诉 Claude 一次重试是否可以帮助。在某些这些拒绝之前，Claude Code 会等待，以便 Claude 的下一次尝试不会立即跟随。在交互式会话中等待期间，微调器显示 `Auto mode check unavailable` 和倒计时，按 `Esc` 会中断轮次。

在连续十个响应都没有判决后，自动模式停止轮次：

```text theme={null}
Auto mode is unavailable — the server returned no safety verdict for the last 10 responses, so Claude stopped. Send a message to try again, or switch out of auto mode.
```

停止消息在每种会话中出现在不同的位置：

* 在交互式会话中，消息作为警告出现在会话记录中，轮次结束
* 在[非交互式](/docs/zh-CN/headless) `-p` 运行中，运行结束并报告执行错误。使用默认文本输出，消息在 stderr 上打印。
* 当[子代理](/docs/zh-CN/sub-agents)达到限制时，子代理在完成之前停止，Claude 接收它生成的任何内容，并附带自动模式停止它的说明

**应该做什么：**

* 发送另一条消息以让 Claude 重试。响应计数重新开始。
* 如果停止重复且您的请求通过[LLM 网关或代理](/docs/zh-CN/llm-gateway)，检查它是否截断流式响应或重写它们。[服务器端分类器审查](/docs/zh-CN/permission-modes#server-side-classifier-review)说明哪种网关行为会导致拒绝，[网关兼容性指南](/docs/zh-CN/llm-gateway-protocol#feature-pass-through)列出了要保持不变的内容。
* 在启动 Claude Code 之前设置 `CLAUDE_CODE_AUTO_MODE_SERVER=0` 以改用其自己的分类器请求。在 v2.1.281 之前，Claude Code 在直接连接到 Anthropic API 时不读取该变量。
* 要自己批准操作，请改为[切换出自动模式](/docs/zh-CN/permission-modes#switch-permission-modes)

在 v2.1.280 之前，Claude Code 立即拒绝来自没有判决的响应的每个操作，从不停止轮次。

<h3 id="agent-terminated-early-due-to-an-api-error">
  Agent terminated early due to an API error
</h3>

[子代理](/docs/zh-CN/sub-agents)的 API 请求终止失败，例如因为达到了用量限制或服务器错误的重试用尽，因此子代理在完成其任务之前停止。此消息需要 Claude Code v2.1.199 或更高版本；在此之前，API 错误文本被返回给 Claude，就像它是子代理的结果一样。

```text theme={null}
Agent terminated early due to an API error: <error detail>
```

**应该做什么：**

* 将冒号后的错误详情与此页面上的其自己的部分匹配，例如[用量限制](#usage-limits)或[服务器错误](#server-errors)，并按照该部分的步骤操作
* 一旦底层错误清除，请要求 Claude 重试任务或[恢复子代理](/docs/zh-CN/sub-agents#resume-subagents)

当速率限制、过载或服务器错误中断已经生成文本输出的前台子代理时，Claude 接收该部分输出标记为不完整，而不是此错误。仅输出为工具调用的子代理也会收到此错误；在 v2.1.199 中，该形状返回了空的部分结果。请参阅[子代理中的 API 错误](/docs/zh-CN/sub-agents#api-errors-in-subagents)。

<h2 id="usage-limits">
  用量限制
</h2>

本部分中的大多数错误意味着与您的账户或套餐相关的配额已达到。其中三个的工作方式不同：[`Server is temporarily limiting requests`](#server-is-temporarily-limiting-requests) 是与您的套餐配额无关的服务器端限流，[`Usage credits required for 1M context`](#usage-credits-required-for-1m-context) 是权限检查而非配额耗尽，[`The prompt to confirm went unanswered`](#the-prompt-to-confirm-went-unanswered) 表示使用额度同意提示未被回答而关闭，无论是否达到配额。

<h3 id="youve-hit-your-session-limit">
  You've hit your session limit
</h3>

订阅套餐包括滚动用量额度。当额度用完时，您会看到以下消息之一：

```text theme={null}
You've hit your session limit · resets 3:45pm
You've hit your weekly limit · resets Mon 12:00am
You've hit your Opus limit · resets 3:45pm
You've hit your Sonnet limit · resets 3:45pm
```

Claude Code 会阻止进一步的请求，直到消息中显示的重置时间。会话和周限制在所有模型中共享，因此切换模型不会恢复访问权限。Opus 和 Sonnet 限制各自仅适用于对该模型系列的请求，因此使用 `/model` 切换到该系列之外的模型可以继续工作。

在使用 claude.ai 订阅登录的交互式会话中，Claude Code 也可以在打开的会话中等待，并在重置后不久继续中断的任务。有关您看到的内容、如何开始或取消等待以及如何关闭自动继续的信息，请参阅 [Wait for a usage limit to reset](/docs/zh-CN/interactive-mode#wait-for-a-usage-limit-to-reset)。在 v2.1.234 之前，Claude Code 不提供此等待功能。

使用量同时计入会话和周额度。单次大量活动突发（例如大型工作流扇出）可能会在会话窗口重置之前耗尽周额度。

**要做什么：**

* 等待错误中显示的重置时间
* 在 [Desktop app](/docs/zh-CN/desktop) 的 Code 选项卡中，会话限制卡提供 **Auto-continue when limits reset** 复选框。周限制卡没有。选中后，Desktop app 会在重置后重试中断的轮次，并在卡上显示重试时间。Desktop 复选框和 CLI 中 `/config` 中的 **Continue automatically at usage limit** 设置是分开的，因此需要分别关闭每一个。
* 对于 Opus 或 Sonnet 限制，运行 `/model` 并切换到该系列之外的模型以继续工作。每个模型都有自己的提示缓存，因此下一个请求会重新读取整个对话，没有缓存命中；请参阅 [Switching models](/docs/zh-CN/prompt-caching#switching-models)
* 运行 `/usage` 查看您的套餐限制以及何时重置
* 运行 `/usage-credits` 在 Pro 和 Max 上购买额外用量，或在 Team 和 Enterprise 上向您的管理员请求。有关如何计费的信息，请参阅 [usage credits for paid plans](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans)。
* 要升级您的套餐以获得更高的基础限制，请参阅 [claude.com/pricing](https://claude.com/pricing)

在窗口用完之前，Claude Code 可以警告您已使用了大部分额度，显示类似 `You've used 85% of your session limit · resets 3:45pm` 的消息。要持续监视您的剩余额度，请将 `rate_limits` 字段添加到 [custom status line](/docs/zh-CN/statusline#rate-limit-usage)，或在 Desktop app 中单击模型选择器旁边的 [usage ring](/docs/zh-CN/desktop#check-usage)。

<h3 id="usage-credits-required-for-1m-context">
  Usage credits required for 1M context
</h3>

所选模型使用 1M token 扩展上下文窗口，而您的套餐仅通过使用额度包含它。

```text theme={null}
API Error: Usage credits required for 1M context · run /usage-credits to turn them on (they take effect after you restart Claude Code), or /model to switch to standard context
```

在 Claude Desktop app 运行的会话中，提示不命名任何命令：它指向 claude.ai 用量设置页面，或在 Team 和 Enterprise 套餐上说在 claude.ai/admin-settings/usage 启用使用额度或向您的管理员请求。

这是权限检查，而非配额耗尽。即使您的会话和周额度有剩余容量，它也会触发。有关哪些套餐直接包含 1M 上下文以及哪些需要使用额度的信息，请参阅 [Extended context](/docs/zh-CN/model-config#extended-context)。

当此错误因上下文增长超过 200K token 而在对话中途出现时，Claude Code 会自动将对话压缩回标准上下文限制以下，并在之后将会话保持在该限制，因此无需采取任何操作。在 v2.1.172 之前的版本中，错误会在每个后续请求（包括 `/compact`）上重复；在这些版本上运行 `/clear` 以恢复。以下步骤适用于您明确选择 `[1m]` 模型的情况。

**要做什么：**

* 运行 `/model` 并选择不带 `[1m]` 后缀的变体以回退到标准上下文窗口
* 在消息命名 `/usage-credits` 的地方，运行它以在 Pro 和 Max 上为 1M 变体启用按量计费，或在 Team 和 Enterprise 上向您的管理员请求使用额度。启用使用额度后，重启 Claude Code 或启动新会话，按消息所说的进行。在此之前，会话保持在标准上下文限制。
* 如果在 `/model` 后错误仍然存在，1M 模型 ID 可能在其他地方设置。有关要按优先级检查的配置位置，请参阅 [Setting your model](/docs/zh-CN/model-config#setting-your-model)。
* 要从模型选择器中完全删除 1M 变体，请设置 [`CLAUDE_CODE_DISABLE_1M_CONTEXT=1`](/docs/zh-CN/env-vars)

在 v2.1.268 之前，消息以 `run /usage-credits to turn them on, or /model to switch to standard context` 结尾，没有提及重启。

<h3 id="the-prompt-to-confirm-went-unanswered">
  The prompt to confirm went unanswered
</h3>

如果您的账户需要 [Fable usage-credits consent](/docs/zh-CN/model-config#fable-and-usage-credits)，Claude Code 会在 Fable 请求计费使用额度之前要求您确认。当同意提示关闭且没有人回答时，Claude Code 会以以下消息之一结束轮次：

```text theme={null}
Fable limit reached · continuing on Fable 5.1 uses usage credits, and the prompt to confirm went unanswered — nothing was sent · answer it where this session is running, or /model to change
Fable 5.1 now uses usage credits · the prompt to confirm went unanswered — nothing was sent · answer it where this session is running, or /model to change
```

消息命名会话的 Fable 模型，因此在 Fable 5 上它们读作 `continuing on Fable 5` 和 `Fable 5 now uses usage credits`。在 v2.1.257 之前，第一条消息以 `Fable 5 limit reached` 开头。

这发生在 [Remote Control](/docs/zh-CN/remote-control) 会话、[background sessions](/docs/zh-CN/agent-view)、[agent team](/docs/zh-CN/agent-teams) 队友会话以及另一个应用程序通过 Agent SDK 托管的会话中。有关 Claude Code 何时关闭提示，请参阅 [Fable and usage credits](/docs/zh-CN/model-config#fable-and-usage-credits)。

**要做什么：**

* 在会话运行的地方，在终端或托管它的应用程序中，发送另一个提示词并在同意提示重新出现时回答它。对于后台会话，首先从 [agents view](/docs/zh-CN/agent-view) 附加到它。从 Remote Control 客户端重新发送会再次显示此消息，因为客户端无法显示提示。
* 运行 `/model` 切换到不计费使用额度的模型
* 要给自己更多时间，请将 [`dialogExpiry`](/docs/zh-CN/settings-reference#dialogexpiry) 设置为更长的值或 `"never"`

在 v2.1.236 之前，此消息没有出现：当 Remote Control 客户端连接时，Claude Code 等待 60 秒以获得答案，然后在您的默认模型上继续轮次。

<h3 id="server-is-temporarily-limiting-requests">
  Server is temporarily limiting requests
</h3>

API 应用了与您的套餐配额无关的短期限流。

```text theme={null}
API Error: Server is temporarily limiting requests (not your usage limit)
```

Claude Code 通过真实限制响应所携带的统一配额标头的缺失来区分这些。从 v2.1.199 开始，无论您如何进行身份验证，此错误在显示之前都会以退避方式[自动重试](#automatic-retries)。在早期版本中，使用 claude.ai 订阅登录的会话在第一次出现时即使轮次失败；只有 API 密钥和 Enterprise 登录会重试它。

**要做什么：**

* 稍等片刻后重试
* 如果问题仍然存在，请检查 [status.claude.com](https://status.claude.com)

<h3 id="request-rejected-429">
  Request rejected (429)
</h3>

您已达到为您的 API 密钥、Amazon Bedrock 项目或 Google Cloud 项目配置的速率限制。

```text theme={null}
API Error: Request rejected (429) · this may be a temporary capacity issue. If it persists, check https://status.claude.com.
```

尾部句子命名检查服务健康的位置，并因提供商而异。Amazon Bedrock、Google Cloud 的 Agent Platform 和 Microsoft Foundry 配置命名该提供商的服务状态，而不是 Anthropic 状态页面。自定义 `ANTHROPIC_BASE_URL` 命名网关主机。

当代理、负载均衡器或 Claude Code 和 API 之间的网关用其自己的 HTML 429 页面回答时，`·` 后的文本是该页面的标题（如果有的话），例如 `Too Many Requests`。在 v2.1.281 之前，整个页面的标记被打印在 `·` 后。

**要做什么：**

* 运行 `/status` 并确认活跃凭据是您期望的。环境中残留的 `ANTHROPIC_API_KEY` 可能会通过低层级密钥而不是您的订阅路由请求。
* 检查您的提供商控制台以了解活跃限制，如果需要请求更高的层级
* 对于 Anthropic API 密钥，请参阅 [rate limits reference](https://platform.claude.com/docs/en/api/rate-limits) 了解层级如何工作以及如何设置每个工作区的上限
* 降低并发：降低 [`CLAUDE_CODE_MAX_TOOL_USE_CONCURRENCY`](/docs/zh-CN/env-vars)，避免运行许多并行子代理，或使用 `/model` 为高容量脚本运行切换到更小的模型

<h3 id="youve-hit-your-monthly-spend-limit">
  You've hit your monthly spend limit
</h3>

您的套餐包含的用量无法覆盖此请求，而本应为其付款的 [usage credits](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) 已达到支出限制。这发生在您的套餐的用量窗口之一用完时，或当请求是仅由使用额度支付的请求时，例如对 [bills to usage credits](/docs/zh-CN/model-config#fable-and-usage-credits) 的模型的请求。消息会指明是谁的限制阻止了您。`·` 后的文本说明如何增加该限制，并因您的套餐和您是否管理计费而异：

```text theme={null}
You've hit your monthly spend limit · raise it at https://claude.ai/settings/usage?from=cc_cli_limit_message
You've hit your individual spend limit · ask your admin for a higher limit
You've hit your org's monthly spend limit · visit https://claude.ai/admin-settings/usage to raise it
You've hit your team's shared budget · ask your admin to raise it at https://claude.ai/admin-settings/usage
You've hit your channel's monthly spend limit · an org owner or channel manager can raise it in the channel's Claude settings
```

`team's shared budget` 是管理员分配给您所属的组的汇总预算；消息不命名该组。`channel's monthly spend limit` 是会话运行的一个 Slack 频道的预算，因此您的组织可能在其外部仍有预算。

当您的套餐的窗口之一用完时，消息也会说该窗口何时重置，例如 `· your session limit resets 3:45pm`，访问权限会在那时恢复，无需任何人提高限制。在使用基于用量计费的组织中，消息说 `usage limit` 代替 `spend limit`，如 `You've hit your individual usage limit`。

如果您通过 Claude apps gateway 连接并看到小写 `spend limit reached`，那是您的网关操作员的上限；请参阅 [Spend limit reached](#spend-limit-reached)。

**要做什么：**

* 在 Pro 和 Max 上，在 claude.ai 的 [**Settings > Usage**](https://claude.ai/settings/usage) 中增加您的月度支出限制，或运行 `/usage-credits`
* 在 Team 和 Enterprise 上，如果您管理计费，在 [**Organization settings > Usage**](https://claude.ai/admin-settings/usage) 中增加限制，或要求管理员这样做。`/usage-credits` 会代您向管理员发送该请求
* 对于频道的限制，要求组织所有者或频道的管理员在 claude.ai 上提高它。请参阅 Claude Tag 文档中的 [Per-channel limits](https://claude.com/docs/claude-tag/admins/set-spend-limit#per-channel-limits)
* 如果消息命名您的套餐窗口的重置时间，您可以改为等待它
* 运行 `/usage` 查看您的套餐窗口以及每个何时重置

<h3 id="spend-limit-reached">
  Spend limit reached
</h3>

您通过 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway) 连接，并已超过您的网关操作员设置的 [spend cap](/docs/zh-CN/claude-apps-gateway-spend-limits)。网关阻止您的请求，直到命名的期间重置或操作员提高上限。它将每个被阻止的 `429` 响应标记为 `x-should-retry: false`，因此 Claude Code 显示此消息而不重试。

```text theme={null}
spend limit reached (daily; resets 2026-08-09 00:00 UTC)
```

消息命名上限的期间和重置时间，当操作员配置了 `blocked_message` 时，他们的说明跟在它后面。在 v2.1.225 之前，消息仅读作 `spend limit reached`；较旧版本上的网关仍然发送该较短的形式。

**要做什么：**

* 等待消息命名的重置时间，或如果消息包含说明，请遵循操作员的说明
* 如果您经常达到上限，要求您的网关操作员提高上限

一条相关消息 `spend limit unavailable` 意味着网关无法读取其支出记录，并作为预防措施而不是超过您的上限而阻止了请求。它通常会自行清除；如果它持续存在，请告诉您的网关操作员。

<h3 id="credit-balance-is-too-low">
  Credit balance is too low
</h3>

您的 Console 组织已用完预付额度，或 Claude Code 使用 Console API 密钥发送您的请求，而您打算使用您的订阅。

```text theme={null}
Credit balance is too low
```

**要做什么：**

* 如果您有 Pro、Max、Team 或 Enterprise 套餐并看到这个，运行 `/status` 并检查 `API key` 行。环境中已批准的 `ANTHROPIC_API_KEY` 通过该密钥而不是您的订阅路由请求。在当前 shell 中取消设置它并从您的 shell 配置文件中删除它，然后重新启动 `claude`。如果您还没有使用您的订阅登录，运行 `/login`。
* 在 [platform.claude.com/settings/billing](https://platform.claude.com/settings/billing) 添加额度，并考虑在那里启用自动充值，以便余额在达到零之前重新填充
* 在 Console 中设置每个工作区的支出上限，以防止单个项目耗尽组织余额。请参阅 [Manage costs effectively](/docs/zh-CN/costs)。

<h3 id="could-not-update-your-spend-limit">
  Could not update your spend limit
</h3>

服务器拒绝了您在达到支出限制时出现的提示中所做的支出限制更改。

```text theme={null}
Could not update your spend limit: <reason from the server>
```

当服务器解释拒绝时，消息以该原因结尾，重试相同的值会再次失败。当失败没有服务器提供的原因时，例如连接断开，消息读作 `Could not update your spend limit. Press Enter to retry.` 并且重试可能成功。在 v2.1.216 之前，Claude Code 为每个失败显示通用形式。

**要做什么：**

* 如果消息包含原因，选择满足它的限制，例如较低的金额
* 如果消息仅显示通用形式，重试；失败可能是暂时的
* 如果更改持续失败，改为从浏览器中的 [claude.ai billing settings](https://support.claude.com/en/articles/12429409-extra-usage-for-paid-claude-plans) 进行

<h2 id="authentication-errors">
  身份验证错误
</h2>

这些错误表示 Claude Code 无法向 API 证明您的身份。您可以随时运行 `/status` 查看当前生效的凭据。

<h3 id="not-logged-in">
  未登录
</h3>

此会话没有可用的有效凭据。

```text theme={null}
Not logged in · Please run /login
```

在由 Claude Desktop 应用运行的会话中（例如 Code 标签页或 Cowork），消息显示为 `Authentication required · Sign in again to continue`，您需要在应用中重新登录。

如果您在另一个使用相同[配置目录](/docs/zh-CN/claude-directory)的 Claude Code 窗口中使用 claude.ai 账户登录，显示此消息的交互式会话会自动开始使用该登录。您无需重启会话。

在 macOS 上的 v2.1.286 之前版本中，您在另一个窗口登录后，该会话可能仍会继续显示此消息。在这些版本中，请重启显示此消息的会话。

**解决方法：**

* 运行 `/login`，使用您的 Claude 订阅或 Console 账户进行身份验证
* 如果您原本希望通过环境变量进行身份验证，请确认在启动 `claude` 的 shell 中已设置并导出 `ANTHROPIC_API_KEY`
* 对于无法进行交互式登录的 CI 或自动化场景，请配置一个在启动时获取密钥的 [`apiKeyHelper`](/docs/zh-CN/settings-reference#apikeyhelper) 脚本
* 请参阅[身份验证优先级](/docs/zh-CN/authentication#authentication-precedence)，了解存在多个凭据时 Claude Code 使用哪一个

如果系统反复提示您登录，请参阅[未登录或令牌已过期](/docs/zh-CN/troubleshoot-install#not-logged-in-or-token-expired)，了解系统时钟检查以及 macOS 凭据存储的恢复步骤。

<h3 id="could-not-resolve-authentication-method">
  无法确定身份验证方法
</h3>

会话在没有任何凭据的情况下到达了 API 客户端。当工作进程在没有凭据的情况下启动时，[后台会话](/docs/zh-CN/agent-view)和云端会话会显示此消息。交互式运行、`-p` 运行和 Agent SDK 运行会将同样的情况报告为[未登录](#not-logged-in)，并且只将此字符串写入调试日志，因此如果您是在调试日志中发现的，请改为按照该条目操作。

```text theme={null}
Could not resolve authentication method. Expected one of apiKey, authToken, credentials, config, or profile to be set. Or for one of the "X-Api-Key" or "Authorization" headers to be explicitly omitted
```

在当前版本中，此错误表示工作进程没有可用的凭据。在 v2.1.174 之前，分配给空闲的预初始化工作进程的后台会话即使已配置有效凭据，也可能以这种方式失败。在 v2.1.176 之前，在被认领前处于空闲状态的云端会话也可能出现这种情况。升级即可恢复。

**解决方法：**

* 如果此错误出现在后台会话或云端会话中，且您的凭据已经配置好，请升级到 v2.1.176 或更高版本
* 确认 `ANTHROPIC_API_KEY`、`CLAUDE_CODE_OAUTH_TOKEN` 或您的云服务提供商凭据已在启动工作进程的环境中设置，而不仅仅是在您的交互式 shell 中设置
* 对于 Agent SDK，请参阅[快速入门中的身份验证设置](/docs/zh-CN/agent-sdk/quickstart#setup)
* 在同一环境中的交互式会话里运行 `/status`，确认解析到的是哪个凭据来源

<h3 id="invalid-api-key">
  API 密钥无效
</h3>

`ANTHROPIC_API_KEY` 环境变量或 `apiKeyHelper` 脚本返回了一个被 API 拒绝的密钥，或者 Claude Code 在发送前拦截了来自 `ANTHROPIC_API_KEY` 的密钥。

```text theme={null}
Invalid API key · Fix external API key
```

如果消息在 `Fix external API key` 之后还附有一段描述，例如 `Invalid X-Api-Key header value from ANTHROPIC_API_KEY: it contains a line break at character 41 (120 characters on 2 lines).`，则说明 API 从未收到该密钥。Claude Code 发现了一个 HTTP 标头无法承载的字符，并在发送前停止了请求。请参阅[请求标头值无效](#invalid-request-header-value)，了解如何解读该描述并修正该值。

**解决方法：**

* 检查是否有拼写错误，并在 [Console](https://platform.claude.com/settings/keys) 中确认该密钥未被撤销
* 在同一个 shell 中运行 `env | grep ANTHROPIC`，或在 PowerShell 中运行 `Get-ChildItem Env:ANTHROPIC*`。direnv、dotenv shell 插件以及 IDE 终端等工具可能会从项目中的 `.env` 文件加载过时的密钥，而您并未显式设置它。
* 取消设置 `ANTHROPIC_API_KEY` 并运行 `/login`，改用订阅身份验证
* 如果密钥来自 [`apiKeyHelper`](/docs/zh-CN/settings-reference#apikeyhelper) 脚本，请直接运行该脚本，确认它在 stdout 上输出了有效的密钥
* 运行 `/status`，确认 Claude Code 实际使用的是哪个凭据来源

<h3 id="your-apikeyhelper-script-is-failing">
  您的 apiKeyHelper 脚本运行失败
</h3>

Claude Code 运行了您的 [`apiKeyHelper`](/docs/zh-CN/settings-reference#apikeyhelper) 设置中的命令，但没有得到密钥。没有密钥时，请求会携带一个占位凭据到达 API，API 会以 `401` 拒绝它。终端中的 `Authentication` 面板会显示发生了以下哪种情况：

* 命令以错误退出或超时
* 命令没有向 stdout 输出任何内容
* 命令输出了密钥以外的内容，例如登录横幅或日志行。面板会显示 `returned output that cannot be used as an API key` 并说明问题所在，但不会重复输出内容。在 v2.1.227 之前，Claude Code 会在去除首尾空白后发送命令输出的任何内容。

```text theme={null}
Your apiKeyHelper script is failing · This usually means you need to re-authenticate with your provider · Run /status to see the script's error output
```

在[非交互模式](/docs/zh-CN/headless)下，stderr 也会带有具体原因，前缀为 `apiKeyHelper failed:`。

在显示此消息之前，Claude Code 会重新运行脚本并最多再重试请求两次，因此失败会在三次尝试内显现。在 v2.1.208 之前，Claude Code 会用完全部[重试预算](#automatic-retries)，用占位凭据反复重新发送请求，然后报告一个通用的 `401` 身份验证错误，而不是脚本失败。

此时运行 `/login` 没有帮助：只要该设置存在，helper 的输出就[优先于](/docs/zh-CN/authentication#authentication-precedence)已保存的登录。

**解决方法：**

* 在您的 shell 中直接运行 `apiKeyHelper` 中配置的命令，以复现该失败
* 如果命令报告会话已过期，请向您的凭据提供方重新进行身份验证，例如重新登录您的 SSO 或密钥保管库
* 修正命令，使其只向 stdout 输出密钥（一个由可打印 ASCII 字符组成、最多 16,384 个字符的单一令牌），并以退出码 0 退出。请参阅[使用 apiKeyHelper 轮换凭据](/docs/zh-CN/llm-gateway-connect#rotate-credentials-with-apikeyhelper)了解可用的设置方式。
* 运行 `/status` 查看失败情况，并确认 `apiKeyHelper` 是当前生效的凭据来源。`apiKeyHelper` 行会显示 `Failing` 以及上一次失败的详细信息，例如退出码和命令的错误输出，并会在下一次成功运行后消失。在 v2.1.274 之前，`/status` 只显示凭据来源，不显示失败情况。
* 每次命令失败时，其退出码和错误输出也会显示在终端的 `Authentication` 面板中。在 v2.1.212 之前，该面板的标题为 `Cloud authentication`。

<h3 id="invalid-request-header-value">
  请求标头值无效
</h3>

Claude Code 即将作为请求标头发送的某个值包含 HTTP 标头无法承载的字符：换行符、NUL 字节，或 `U+00FF` 以上的字符（例如弯引号或零宽空格）。Claude Code 会在发送任何内容之前停止请求，并指出需要修正的变量或设置。常见原因是从文档或聊天中粘贴的凭据带有不可见字符或多余的换行符。

当 Claude Code 直接或通过 [LLM 网关](/docs/zh-CN/llm-gateway)向 Claude API 发送请求时，会执行此检查。在 [Amazon Bedrock](/docs/zh-CN/amazon-bedrock) 等第三方云服务提供商上，Claude Code 不会在发送前执行此检查。

```text theme={null}
Invalid auth token · Fix external auth token
Invalid ANTHROPIC_CUSTOM_HEADERS · Fix the environment variable
Invalid request header from the environment · Fix the environment variable
```

消息的第一部分取决于错误值的来源：

* `Invalid auth token`：来自 [`ANTHROPIC_AUTH_TOKEN`](/docs/zh-CN/env-vars) 或 [`CLAUDE_CODE_OAUTH_TOKEN`](/docs/zh-CN/env-vars) 的 bearer 令牌
* `Invalid ANTHROPIC_CUSTOM_HEADERS`：您在 [`ANTHROPIC_CUSTOM_HEADERS`](/docs/zh-CN/env-vars) 中设置的标头名称或值。描述会指出出错的是第几个 `Name: Value` 对，例如 `distinct header 2 of 3 parsed from ANTHROPIC_CUSTOM_HEADERS`，但不会重复名称或值，因为两者都是您自己设定的。
* `Invalid request header from the environment`：Claude Code 从另一个环境变量（例如 `CLAUDE_AGENT_SDK_CLIENT_APP`）复制到请求标头中的值。描述会指出需要修正的变量。

此检查捕获到的错误 `ANTHROPIC_API_KEY` 会被 Claude Code 报告为 [API 密钥无效](#invalid-api-key)，并附带同样的尾部描述。错误的已保存 `/login` 凭据则会被报告为[未登录](#not-logged-in)；运行 `/login` 保存一个新的凭据即可。[`apiKeyHelper`](/docs/zh-CN/settings-reference#apikeyhelper) 脚本的输出永远不会进入此检查：Claude Code 在脚本运行时就会对其进行验证，HTTP 标头无法承载的输出会以[您的 apiKeyHelper 脚本运行失败](#your-apikeyhelper-script-is-failing)的形式失败。

在第二个 `·` 之后，消息会描述问题，完整示例如下：

```text theme={null}
Invalid auth token · Fix external auth token · Invalid Authorization header value from ANTHROPIC_AUTH_TOKEN: it contains a line break at character 41 (120 characters on 2 lines).
```

位置按字符计数，从 1 开始。描述由固定短语和字符计数组成，因此永远不会包含值本身。只有当问题字符是众所周知的不可见字符或排版字符（例如字节顺序标记、零宽空格或弯引号）时，描述才会指出该字符，其他字符一律报告为 `a non-ASCII character`。

**解决方法：**

* 重新设置消息中指出的变量或设置，手动重新输入所报告位置附近的字符，而不是再次从同一来源粘贴
* 对于 `ANTHROPIC_CUSTOM_HEADERS`，每行保留一个 `Name: Value` 对，并重写消息所指出的那一对
* 运行 `/status`，确认当前生效的凭据来源

<h3 id="this-organization-has-been-disabled">
  此组织已被停用
</h3>

Claude Code 正在使用来自已停用 Console 组织的过时 `ANTHROPIC_API_KEY`。当您有已保存的订阅登录时，该密钥会覆盖它。

```text theme={null}
Your ANTHROPIC_API_KEY belongs to a disabled organization · Unset the environment variable to use your subscription instead
Your ANTHROPIC_API_KEY belongs to a disabled organization · Update or unset the environment variable
API Error: 400 ... This organization has been disabled.
```

`·` 之后的提示取决于您已保存的凭据：当您取消设置该密钥后有已存储的 `/login` 可以接替时，显示第一种形式；当该密钥是您唯一的凭据时，显示第二种形式。

环境变量优先于 `/login`，因此即使您拥有可用的 Pro 或 Max 订阅，在 shell 配置文件中导出或从 `.env` 文件加载的密钥仍会被使用。在非交互模式（`-p`）下，只要存在该密钥，就总会使用它。

**解决方法：**

* 在当前 shell 中取消设置 `ANTHROPIC_API_KEY`，并将其从 shell 配置文件中删除，然后重新启动 `claude`
* 如果消息显示 `Update or unset`，说明您没有可回退的已保存登录。请取消设置该密钥并运行 `/login`，或将其替换为来自活跃 Console 组织的密钥。
* 之后运行 `/status`，确认当前生效的凭据是您的订阅
* 如果没有设置任何环境变量但错误仍然存在，请联系支持团队或使用其他账户登录。

<h3 id="your-organization-has-disabled-api-key-authentication">
  您的组织已禁用 API 密钥身份验证
</h3>

此消息需要 Claude Code v2.1.169 或更高版本。您的 Console 组织管理员已关闭 API 密钥身份验证，因此 API 会拒绝 Claude Code 发送的密钥。`·` 之后的恢复提示因密钥来源而异：

```text theme={null}
Your organization has disabled API key authentication · Run /login to sign in with your claude.ai account
Your organization has disabled API key authentication · Unset ANTHROPIC_API_KEY to use your claude.ai account instead
Your organization has disabled API key authentication · Unset ANTHROPIC_API_KEY and run /login to sign in with your claude.ai account
Your organization has disabled API key authentication · Unset the apiKeyHelper setting and run /login to sign in with your claude.ai account
Your organization has disabled API key authentication · Sign in again with your claude.ai account
```

最后一种形式出现在由 Claude Desktop 应用运行的会话中（例如 Code 标签页或 Cowork），此时您需要在应用中重新登录。

环境变量和 `apiKeyHelper` 优先于 `/login`，因此只要其中任何一个仍在提供密钥，单独运行 `/login` 是没有帮助的。请参阅[身份验证优先级](/docs/zh-CN/authentication#authentication-precedence)。

**解决方法：**

* 如果消息中提到 `ANTHROPIC_API_KEY`，请在当前 shell 中取消设置它，并将其从 shell 配置文件或 `.env` 文件中删除，然后重新启动 `claude`
* 如果消息中提到 `apiKeyHelper`，请从您的 `settings.json` 中删除 [`apiKeyHelper`](/docs/zh-CN/settings-reference#apikeyhelper) 设置
* 运行 `/login`，使用您的 claude.ai 账户登录
* 之后运行 `/status`，确认当前生效的凭据是您的订阅而不是 API 密钥
* 如果您的自动化流程需要 API 密钥身份验证，请让组织管理员在 Console 中重新启用它

<h3 id="your-organization-has-disabled-claude-subscription-access">
  您的组织已禁用 Claude 订阅访问
</h3>

您的 Claude 组织不允许使用订阅登录来登录 Claude Code。使用同一账户再次运行 `/login` 会返回相同的错误。

```text theme={null}
Your organization has disabled Claude subscription access for Claude Code · Use an Anthropic API key instead, or ask your admin to enable access
```

这是服务器端的组织设置，因此无法通过本地设置、环境变量或 CLI 标志覆盖。

Agent SDK 和 `-p` 非交互模式会将其呈现为 `oauth_org_not_allowed` 错误代码。

**解决方法：**

* 请管理员为您的组织启用 Claude Code 访问权限
* 改用 Console API 密钥而不是订阅进行身份验证。设置方法请参阅 [Claude Console 身份验证](/docs/zh-CN/authentication#claude-console-authentication)。
* 如果您是管理员但找不到启用访问的选项，请联系 [Anthropic 支持](https://support.claude.com)

<h3 id="routines-are-disabled-by-your-organizations-policy">
  Routine 已被您组织的策略禁用
</h3>

您所在的 Team 或 Enterprise 组织中的 Owner 已在组织级别关闭了 Routine。当您尝试创建或运行 Routine 时（例如通过 claude.ai/code 上的 [Routines](/docs/zh-CN/routines) 界面），会出现此错误。在 Claude Code v2.1.227 或更高版本中，同一设置还会在 CLI 中[隐藏 `/schedule`](/docs/zh-CN/routines#troubleshooting)。

```text theme={null}
Routines are disabled by your organization's policy.
```

这是服务器端设置，因此无法通过本地设置、环境变量或 CLI 标志覆盖。

**解决方法：**

* 请您组织中的 Owner 在 [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) 启用 **Routines** 开关
* 对于不需要组织级 Routine 的一次性定时工作，请参阅[定时任务](/docs/zh-CN/scheduled-tasks)

<h3 id="remote-control-requires-the-anthropic-api">
  Remote Control 需要 Anthropic API
</h3>

该会话没有直接与 Anthropic API 通信，而这是 [Remote Control](/docs/zh-CN/remote-control) 所必需的。

```text theme={null}
Remote Control is only available when using Claude via api.anthropic.com. CLAUDE_CODE_USE_BEDROCK is set, so this session is using Amazon Bedrock — unset it (or run in a shell without it) to use Remote Control.
```

第二句话解释了是什么让会话绕开了 Anthropic API；在 v2.1.219 之前，消息只有第一句话。根据原因不同，消息会指出：

* 某个 `CLAUDE_CODE_USE_*` 提供商变量，例如用于 [Amazon Bedrock](/docs/zh-CN/amazon-bedrock) 的 `CLAUDE_CODE_USE_BEDROCK` 或用于 [Google Cloud's Agent Platform](/docs/zh-CN/google-vertex-ai) 的 `CLAUDE_CODE_USE_VERTEX`
* [`ANTHROPIC_BASE_URL`](/docs/zh-CN/env-vars) 指向 `api.anthropic.com` 以外的主机，例如 [LLM 网关](/docs/zh-CN/llm-gateway)或代理，即使您使用 claude.ai 登录也是如此；在 v2.1.196 之前，自定义 base URL 不会阻止 Remote Control
* 设置了 `ANTHROPIC_UNIX_SOCKET`，因此会话通过本地套接字而不是发往 `api.anthropic.com` 来发送请求
* 通过 `/login` 完成的企业[云网关](/docs/zh-CN/claude-apps-gateway)登录，它不支持 Remote Control，也没有可以取消设置的变量

**解决方法：**

* 取消设置消息中指出的变量（例如 `CLAUDE_CODE_USE_BEDROCK` 或 `ANTHROPIC_BASE_URL`）并重启会话，或从直接与 Anthropic API 通信的会话中启动 Remote Control
* 如果该变量并未在您的 shell 中设置，请检查您[设置文件](/docs/zh-CN/settings#where-settings-live)中的 `env` 键，它会将环境变量应用到每个会话
* 关于此消息及其他 Remote Control 启动消息，请参阅[排除 Remote Control 故障](/docs/zh-CN/remote-control#troubleshooting)

<h3 id="remote-control-couldnt-refresh-your-login">
  Remote Control 无法刷新您的登录
</h3>

Claude Code 使用短期凭据运行实时的 [Remote Control](/docs/zh-CN/remote-control) 连接，这些凭据是它借助您已保存的 claude.ai 登录获取和续期的。当 claude.ai 不再接受该登录，或者 Claude Code 已没有任何已保存的登录时，Claude Code 会停止 Remote Control，需要您重新登录。这两种失败都可能发生在 Claude Code 仍在连接时，也可能发生在之后续期凭据时。

当 Claude Code 请求登录服务刷新您已保存的登录却没有得到响应时，它会保持 Remote Control 运行，并在连接的当前凭据仍然有效期间再次尝试刷新。当 Claude Code 无法访问登录服务、请求超时，或服务失败但并未拒绝您的登录时，刷新就会得不到响应。如果在该凭据过期时登录服务仍未响应，Claude Code 会停止 Remote Control 并报告 `OAuth token refresh failed`。

当 Claude Code 停止 Remote Control 时，它会在警告以及一条以 `Remote Control disconnected` 开头的会话记录行中显示原因。您的本地会话会在没有 Remote Control 的情况下继续运行。本节涵盖以下消息行：

```text theme={null}
Remote Control disconnected — Claude.ai login expired — run /login to restore Remote Control
Remote Control disconnected — Claude.ai login expired — run /login, then /remote-control
Remote Control disconnected — Claude.ai login was rejected — run /login, then /remote-control
Remote Control disconnected — OAuth token unavailable — run /login to restore Remote Control
Remote Control disconnected — OAuth token refresh failed — run /login to re-authenticate
Remote Control disconnected — JWT refresh failed: no OAuth token — run /login
Remote Control disconnected — Signed out of Claude — run /login, then /remote-control
```

Claude Code 会在消息中间部分说明原因：

* `Claude.ai login expired` 和 `Claude.ai login was rejected`：claude.ai 不再接受您已保存的登录令牌，因为它已过期或被撤销
* `OAuth token unavailable`：当连接的凭据到期需要续期时，Claude Code 没有已保存的登录令牌
* `OAuth token refresh failed`：Claude Code 重新连接时，claude.ai 拒绝了您已保存的登录令牌，且刷新令牌没有产生新令牌
* `JWT refresh failed: no OAuth token`：Claude Code 找不到可用于续期的已保存登录令牌
* `Signed out of Claude`：您在这台机器上退出了登录，例如在另一个终端中运行了 `/logout`，因此 Claude Code 已没有可用于续期连接的已保存登录

**解决方法：**

* 运行 `/login` 重新登录
* 运行 `/remote-control` 重新连接会话。以 `run /login to restore Remote Control` 结尾的消息不需要此步骤：您登录后 Claude Code 会自动重新连接。

在 v2.1.224 之前，`OAuth token refresh failed — run /login to re-authenticate` 显示为 `OAuth token refresh failed — re-authenticate, then re-enable Remote Control`，`JWT refresh failed: no OAuth token — run /login` 显示为 `no OAuth token available for recovery (code <N>)`。`Claude.ai login expired`、`Claude.ai login was rejected` 和 `OAuth token unavailable` 消息是在 v2.1.225 中添加的。

在 v2.1.238 之前，Claude Code 将现在显示为 `Signed out of Claude` 的情况报告为 `JWT refresh failed: no OAuth token — run /login`，并且只要有一次登录刷新未得到响应，就会以 `Claude.ai login expired — run /login to restore Remote Control` 停止 Remote Control。

<h3 id="remote-control-stopped-because-the-signed-in-account-changed">
  由于登录账户已更改，Remote Control 已停止
</h3>

在 [Remote Control](/docs/zh-CN/remote-control) 会话期间，当您在这台机器上登录到另一个 claude.ai 账户或组织时，Claude Code 会显示这行消息。这种切换是在 Claude Code 会话之外进行的，例如在另一个终端中运行了 `/login`。

您在通过 `/login` 登录状态下启动的 Remote Control 会话，属于启动时所登录的 claude.ai 账户和组织。

```text theme={null}
Remote Control disconnected — signed-in claude.ai account or organization changed on this machine — run /remote-control to start a session for the current account, or /login to switch back, then /remote-control
```

一旦 claude.ai 确认账户或组织已更改，Claude Code 就会停止 Remote Control 会话。您的本地会话会在没有 Remote Control 的情况下继续运行。

**解决方法：**

* 运行 `/remote-control`，在当前账户或组织下启动新的 Remote Control 会话
* 如需切换回去，请运行 `/login` 并重新登录之前的账户或组织，然后运行 `/remote-control`。

在 v2.1.234 之前，当您在 Claude Code 会话之外切换到其他账户或组织时，Claude Code 不会察觉。Claude Code 会保持 Remote Control 会话连接，直到之后某个发往 Remote Control 服务器的请求以 `Remote Control server rejected the request (HTTP 404)` 失败。该失败可能在切换后数小时才出现。

<h3 id="remote-control-stopped-because-the-app-running-the-session-signed-out-or-switched-accounts">
  由于运行会话的应用已退出登录或切换了账户，Remote Control 已停止
</h3>

当 Claude 桌面应用或 IDE 托管您的会话时，Claude Code 会从该应用而不是从 `/login` 获取登录令牌。当 claude.ai 拒绝该令牌时，Claude Code 会向应用请求新令牌。如果应用回复它已退出登录，或者现在登录的是另一个 Claude 账户，Claude Code 会结束 [Remote Control](/docs/zh-CN/remote-control) 会话，并向应用发送以下消息行之一：

```text theme={null}
Remote Control stopped — the app running this session is now signed in to a different Claude account
Remote Control stopped — the app running this session is signed out of Claude. Sign in there, then turn Remote Control back on
```

您的本地会话会在没有 Remote Control 的情况下继续运行。

**解决方法：**

* 如果应用已退出登录，请在应用中重新登录，然后在应用中重新打开 Remote Control
* 如果应用切换了账户，Claude Code 无法在新账户下继续已结束的会话。请在该账户下启动新的 Remote Control 会话。

在 v2.1.238 之前，这两种情况下 Claude Code 都会向应用发送[Remote Control 无法刷新您的登录](#remote-control-couldnt-refresh-your-login)中列出的 `run /login` 消息。

<h3 id="oauth-token-revoked-or-expired">
  OAuth 令牌已撤销或已过期
</h3>

您已保存的登录不再有效。令牌被撤销意味着您在所有位置都退出了登录，或者管理员移除了访问权限；令牌过期意味着会话中途的自动刷新失败了。

这两条消息报告的都是 API 对 Claude Code 所发送请求返回的拒绝。如果已保存的登录在刷新失败后已被清除，您看到的将是[登录已过期](#login-expired)。如果您在 [`CLAUDE_CODE_OAUTH_TOKEN`](/docs/zh-CN/env-vars) 中使用长期令牌进行身份验证，当该令牌过期或被撤销时，您也会看到同样的消息。

```text theme={null}
OAuth token revoked · Please run /login
Please run /login · API Error: 401 OAuth token has expired ...
```

在[非交互模式](/docs/zh-CN/headless)（`-p`）和 [Agent SDK](/docs/zh-CN/agent-sdk/overview) 中，消息如下，结构化错误代码为 `authentication_failed`：

```text theme={null}
Failed to authenticate: OAuth token revoked. Please log in again or contact your administrator.
Failed to authenticate. API Error: 401 OAuth token has expired ...
```

在 v2.1.287 之前，非交互模式和 Agent SDK 中的撤销消息为 `Your account does not have access to Claude. Please login again or contact your administrator.`

**解决方法：**

* 在 Claude Code 提示符下运行 `/login` 重新登录
* 如果您的 `-p` 命令或 Agent SDK 程序使用已保存的登录，请在同一环境中运行 `claude`，完成 `/login`，然后再次运行该命令或程序。对于无法交互式登录的自动化场景，请使用 [`ANTHROPIC_API_KEY`](/docs/zh-CN/env-vars) 进行身份验证，或[使用 `claude setup-token` 生成长期令牌](/docs/zh-CN/authentication#generate-a-long-lived-token)。
* 如果您使用 `CLAUDE_CODE_OAUTH_TOKEN` 环境变量进行身份验证，在请求以 401 失败后，Claude Code 会继续发送您设置的值，而不会切换到已存储登录的令牌。[`/status`](/docs/zh-CN/commands) 会将此凭据显示为一个 `Auth token` 行，内容为 `CLAUDE_CODE_OAUTH_TOKEN`。请使用 [`claude setup-token`](/docs/zh-CN/authentication#generate-a-long-lived-token) 生成新令牌并用它重启，或取消设置该变量并运行 `/login`。在 v2.1.225 之前，Claude Code 可能会在会话中途用已存储登录的短期访问令牌替换该变量的值，一旦该令牌过期，会话就会再次因 401 错误而失败。
* 如果每次启动都反复提示您登录，请参阅[故障排除](/docs/zh-CN/troubleshoot-install#not-logged-in-or-token-expired)中的系统时钟检查和 macOS 凭据存储恢复步骤
* 对于其他失败，包括 `403 Forbidden` 和 OAuth 浏览器问题，请参阅[登录和身份验证](/docs/zh-CN/troubleshoot-install#login-and-authentication)

<h3 id="api-error-401-invalid-authentication-credentials">
  API Error: 401 Invalid authentication credentials
</h3>

API 识别了您凭据的格式，但拒绝了其背后的账户或组织。当凭据最近被撤销、组织被停用或移除了您的访问权限，或账户本身被停用时，Anthropic 会返回此消息，因此原因并不是令牌过期。该凭据可能是您已保存的登录，也可能是已批准的 `ANTHROPIC_API_KEY`，两者的修复方法不同，因此请先运行 `/status` 查看当前生效的是哪一个。

```text theme={null}
Please run /login · API Error: 401 Invalid authentication credentials
```

**解决方法：**

* 如果 `/status` 显示一个未标记为未使用的 `API key` 行，说明已批准的 [`ANTHROPIC_API_KEY`](/docs/zh-CN/authentication#authentication-precedence) 是当前生效的凭据，并且优先于您的登录，因此 `/login` 不会替换它。请在 Claude Console 中轮换该密钥，或通过运行 `unset ANTHROPIC_API_KEY`（在 PowerShell 中为 `Remove-Item Env:ANTHROPIC_API_KEY`）回退到您的订阅。
* 如果 `/status` 只显示您的登录，请运行一次 `/login`。如果凭据已被撤销，新的登录会替换它。
* 如果同一登录账户再次出现相同消息，说明该账户或组织已不再活跃。请检查 `/status` 报告的账户和组织，并请您的组织管理员恢复访问权限。
* 如果 [`ANTHROPIC_BASE_URL`](/docs/zh-CN/env-vars) 指向 [LLM 网关](/docs/zh-CN/llm-gateway)，`401` 之后的文本是您网关的消息而不是 Anthropic 的消息，`/login` 不会改变它。请改为修正网关所需的凭据。

<h3 id="login-expired">
  登录已过期
</h3>

Claude Code 尝试续期您已保存的 claude.ai 登录，但 OAuth 服务拒绝了已存储的刷新令牌，因此 Claude Code 清除了已保存的凭据。此后，每个模型请求都会在到达 API 之前于本地以此消息停止，因为只有 `/login` 才能创建新凭据。

在 v2.1.206 之前，Claude Code 仍会使用环境中剩余的任何凭据发送模型请求，然后每个模型都会以[所选模型存在问题](#theres-an-issue-with-the-selected-model)或 401 失败，而不是提示您登录。

```text theme={null}
Login expired · Please run /login
```

在[非交互模式](/docs/zh-CN/headless)（`-p`）和 [Agent SDK](/docs/zh-CN/agent-sdk/overview) 中，消息如下，结构化错误代码为 `authentication_failed`：

```text theme={null}
Failed to authenticate: OAuth session expired and could not be refreshed
```

这与 [OAuth 令牌已撤销或已过期](#oauth-token-revoked-or-expired)并非同一状态。那些消息报告的是 API 返回的拒绝。而 `Login expired` 是 Claude Code 针对已续期失败的登录自行生成的，因此它不会发送任何请求。当续期失败是因为账户本身被暂停而不是登录过时，Claude Code 会改为显示[您的账户已被暂停](#your-account-is-on-hold)。

使用 API 密钥、[`CLAUDE_CODE_OAUTH_TOKEN`](/docs/zh-CN/env-vars) 或第三方提供商进行身份验证的会话不使用已保存的登录，永远不会看到此消息。

您可以在请求失败之前检查是否处于此状态：[`/status`](/docs/zh-CN/commands) 会显示一个 `Login` 行，内容为 `Expired — log in again`，以及它为该过期登录保存的组织和电子邮件。只有当已保存的登录是您当前生效的凭据且无法再刷新时，才会显示该行。以其他方式进行身份验证的会话不会显示该行，即使仍保存着已过期的登录。在 v2.1.210 之前，`/status` 在此状态下不会提供任何曾存在登录的迹象，因为凭据已被清除，没有可报告的内容。

**解决方法：**

* 运行 `/login` 重新登录。不登录而直接重试，每个请求都会显示相同的消息。
* 如果您在另一个 Claude Code 窗口中使用 claude.ai 账户登录，请参阅[未登录](#not-logged-in)，了解此会话何时会自动开始使用该登录。
* 在非交互模式下，请在同一环境中运行 `claude`，完成 `/login`，然后重新运行您的命令。对于无法交互式登录的自动化场景，请使用 `ANTHROPIC_API_KEY` 进行身份验证，或[使用 `claude setup-token` 生成长期令牌](/docs/zh-CN/authentication#generate-a-long-lived-token)。
* 如果登录一直失败，请参阅[登录和身份验证](/docs/zh-CN/troubleshoot-install#login-and-authentication)

<h3 id="could-not-refresh-your-login">
  由于另一个 Claude Code 进程正在刷新您的登录，无法刷新
</h3>

此消息并不表示您的登录被拒绝。您已保存的 claude.ai 登录已过期，需要续期。同一台机器上的另一个 Claude Code 进程持有共享的刷新锁，或者该进程已退出但遗留了该锁，在此会话等待期间刷新没有任何进展。Claude Code 会在发送前停止请求：

```text theme={null}
Could not refresh your login because another Claude Code process is refreshing it (or exited mid-refresh) · Try again in a minute; if it keeps happening, close other Claude Code windows or sign in again with /login
```

在[非交互模式](/docs/zh-CN/headless)（`-p`）和 [Agent SDK](/docs/zh-CN/agent-sdk/overview) 中，消息如下，结构化错误代码为 `server_error`：

```text theme={null}
Failed to refresh OAuth token: another Claude Code process is refreshing it or exited mid-refresh. This is usually transient; retry in a minute, and if it persists close other Claude Code processes or sign in again
```

使用 API 密钥、[`CLAUDE_CODE_OAUTH_TOKEN`](/docs/zh-CN/env-vars) 或第三方提供商进行身份验证的会话不使用已保存的登录，永远不会看到此消息。

**解决方法：**

* 一分钟后重试。如果另一个进程先完成了刷新，此会话会使用续期后的登录。
* 如果消息反复出现，请关闭其他 Claude Code 窗口和进程，然后重试。
* 如果在没有其他 Claude Code 进程运行的情况下仍出现该消息，请运行 `/login`。重新登录不会等待刷新锁。

<h3 id="couldnt-save-your-login">
  无法保存您的登录
</h3>

您已使用 claude.ai 登录，但 Claude Code 无法将登录保存到其凭据存储中，因此登录未完成。在 macOS 上，如果 Claude Code 在同一会话中已经读取或保存过登录钥匙串中的凭据，之后钥匙串被锁定（例如在睡眠或空闲时），就可能发生这种情况。

```text theme={null}
Couldn't save your login. If your Mac's keychain is locked, unlock it and log in again.
Couldn't save your login. Try logging in again.
```

第一种形式出现在 macOS 上，第二种形式出现在其他所有平台上。暂时性的凭据存储失败（例如超时或存储无法读取）也会产生同样的消息。

**解决方法：**

* 在 macOS 上，解锁登录钥匙串，然后再次运行 `/login`
* 在其他平台上，再次运行 `/login`
* 如果登录仍然无法保存，请参阅[未登录或令牌已过期](/docs/zh-CN/troubleshoot-install#not-logged-in-or-token-expired)，了解钥匙串解锁命令和其他凭据存储恢复步骤

<h3 id="failed-to-start-oauth-callback-server">
  无法启动 OAuth 回调服务器
</h3>

当 `/login`、`claude auth login` 或 `claude setup-token` 通过浏览器为您登录时，Claude Code 会在 `127.0.0.1` 上打开一个监听端口，以便浏览器将登录结果返回给它。此消息表示 Claude Code 无法打开该端口，登录会在浏览器窗口或登录 URL 出现之前停止：

```text theme={null}
Failed to start OAuth callback server: Failed to start server. Is port 0 in use?
```

如果您的消息以 `Is port 0 in use?` 结尾，说明在 IPv4 回环地址 `127.0.0.1` 上监听的尝试直接失败了。由于失败发生在登录 URL 生成之前，`Paste code here if prompted` 流程无法作为变通方案使用。

**解决方法：**

* 如需不使用本地监听器立即登录：如果您使用 claude.ai 订阅，请在可以正常登录的机器上运行 [`claude setup-token`](/docs/zh-CN/authentication#generate-a-long-lived-token)，并在这台机器上将它输出的令牌设置为 `CLAUDE_CODE_OAUTH_TOKEN`。否则，请将 `ANTHROPIC_API_KEY` 设置为来自 [Claude Console](https://platform.claude.com/settings/keys) 的密钥。[身份验证优先级](/docs/zh-CN/authentication#authentication-precedence)解释了 Claude Code 如何在多个凭据之间进行选择。
* 如果要改为在这台机器上使用浏览器登录，Claude Code 必须能够在 `127.0.0.1` 上监听。如果它在沙箱中运行，请检查沙箱策略是否允许监听本地端口，然后再次运行 `/login`。如果它本应能够监听却仍然失败，请运行 `/feedback`，以便报告中包含您的环境详细信息。

<h3 id="claude-login-not-accepted">
  Claude 登录未被接受
</h3>

您尝试启动一个[云端会话](/docs/zh-CN/claude-code-on-the-web)，服务器以 401 拒绝创建它：服务器不接受这台机器发送的 Claude 登录，通常是因为该登录已过期或被撤销。

如果服务器给出了原因，该行的第一部分就是服务器自己的原因。否则，该行显示为：

```text theme={null}
Claude login not accepted · Run /login, then try again
```

**解决方法：**

* 运行 `/login`，完成登录，然后再次启动会话

<h3 id="artifacts-need-a-claude-ai-login">
  Artifact 需要 claude.ai 登录
</h3>

Claude Code 拒绝了 [Artifact](/docs/zh-CN/artifacts) 的发布或读取，因为该会话没有可用于 Artifact 的 claude.ai 登录。

该消息的每种形式都以相同的文字开头，后面跟着的补救措施取决于您的会话如何进行身份验证。没有竞争凭据时，消息显示为：

```text theme={null}
Artifacts need a claude.ai login. Run /login and select "Claude account with subscription", then retry — the "Anthropic Console account" option does not provide claude.ai credentials.
```

**解决方法：**

* 运行 `/login` 并选择 **Claude account with subscription**。**Anthropic Console account** 选项不提供 claude.ai 凭据。
* 当消息指出某个优先级更高的凭据时，例如 `ANTHROPIC_API_KEY`、`apiKeyHelper` 设置或之前的 `/login` 保存的 Console 密钥，请按消息所述将其移除，然后运行 `/login`
* 当消息说明此远程会话通过启动它的机器进行身份验证时，请在那台机器上登录 claude.ai，然后重新连接会话
* 当消息说明凭据由会话的宿主环境注入时，您无法在该会话中更改它；请启动一个已登录 claude.ai 的会话
* 请参阅[可用性](/docs/zh-CN/artifacts#availability)，了解 Artifact 的其他要求，例如套餐、模型提供商和组织策略

<h3 id="administrator-policy-requires-a-cloud-gateway-sign-in">
  管理员策略要求使用云网关登录
</h3>

这台机器上管理员的[托管设置](/docs/zh-CN/managed-settings)将 [`forceLoginMethod`](/docs/zh-CN/settings-reference#forceloginmethod) 设置为 `"gateway"`，或设置了 [`forceLoginGatewayUrl`](/docs/zh-CN/settings-reference#forcelogingatewayurl)。除非您通过 `CLAUDE_CODE_USE_BEDROCK` 等变量选择了云服务提供商，否则 Claude Code 只接受 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway) 登录。您会看到以下两种消息之一：

```text theme={null}
Not signed in to the Cloud gateway — run /login.
```

当会话没有网关登录时，模型请求会以此消息失败，例如因为在该策略下发到这台机器后您还没有运行过 `/login`。

如果这台机器上还存在 Anthropic 签发的凭据，并且托管设置设置了 `forceLoginMethod` 或 `forceLoginOrgUUID`，Claude Code 则会在启动时退出。该凭据可能是 `ANTHROPIC_API_KEY` 或 `ANTHROPIC_AUTH_TOKEN` 变量、`apiKeyHelper` 设置，或之前的 Claude Console 登录保存的 API 密钥。

启动消息会指出会话所配置的凭据、它的设置位置以及移除它的步骤。例如，当您在 shell 中设置了 `ANTHROPIC_API_KEY` 变量时，消息显示为：

```text theme={null}
Administrator policy requires a Cloud gateway sign-in on this machine, but this session is configured with an API key from ANTHROPIC_API_KEY, which a gateway machine does not accept.

To continue: unset ANTHROPIC_API_KEY (or run in a shell without it), then run claude and sign in with /login.
```

**解决方法：**

* 对于 `Not signed in to the Cloud gateway`，请运行 `/login` 并在 **Cloud gateway** 界面上完成登录
* 对于启动消息，请按照消息末尾的步骤移除该凭据
* 如果您认为这台机器不应要求使用网关，请让管理该机器的管理员从其托管设置中移除 `forceLoginMethod` 和 `forceLoginGatewayUrl`

在 v2.1.284 之前，启动消息会列出可能的凭据，而不是指出已配置的那一个。它以 `Administrator policy requires a Cloud gateway sign-in on this machine; the Anthropic-issued credential configured here (ANTHROPIC_API_KEY, ANTHROPIC_AUTH_TOKEN, or apiKeyHelper) is not used.` 开头。如果您看到的是这种措辞且无法判断要移除哪个凭据，请更新到 v2.1.284 或更高版本，然后再次启动 `claude`。

在 v2.1.265 上，一个回归问题还会在某些使用 API 密钥、`apiKeyHelper` 或自定义标头进行身份验证的 LLM 网关和代理配置中显示第一条消息，即使机器上没有管理员要求也是如此。请更新到 v2.1.266 或更高版本。您无需更改配置。

在 v2.1.261 之前，在将 `forceLoginMethod` 设置为 `"gateway"` 的机器上，Claude Code 会使用遗留的已保存登录，而不是让模型请求失败，并且会以 `This machine's managed settings require a first-party login` 报告已配置的环境凭据，而不是显示启动消息。

<h3 id="your-account-is-on-hold">
  您的账户已被暂停
</h3>

您登录所用的 Claude 账户已被暂停。当 Claude Code 尝试续期您已保存的登录并获知暂停时，会显示第一条消息；当您在浏览器中完成的登录报告暂停时，会显示第二条消息：

```text theme={null}
Your account is on hold and can't use Claude Code. View details or appeal: https://claude.ai/restricted
Your account is on hold and can't sign in to Claude Code. View details or appeal: https://claude.ai/restricted
```

使用同一账户重新登录不会清除该消息，因为暂停针对的是账户而不是登录。在[非交互模式](/docs/zh-CN/headless)（`-p`）和 [Agent SDK](/docs/zh-CN/agent-sdk/overview) 中，结构化错误代码为 `account_on_hold`。在 v2.1.235 之前，Claude Code 会将被暂停的账户报告为 [Login expired · Please run /login](#login-expired)，而其恢复步骤无法解除暂停。

**解决方法：**

* 打开消息中的链接，查看暂停的详细信息或提出申诉
* 如果您有不受暂停影响的其他 Claude 账户或 API 密钥，可以在暂停解决期间继续工作：使用该账户运行 `/login`，或通过 `ANTHROPIC_API_KEY` 设置该密钥

<h3 id="anthropic-profile-login-expired">
  Anthropic 配置文件登录已过期
</h3>

Claude Code 正在通过一个 Anthropic 凭据配置文件进行身份验证，该配置文件中已保存的登录凭据已过期，并且配置文件中没有 Claude Code 可用于续期的刷新凭据。Claude Code 会在本地停止每个请求且不重试，因为重试只会读取同一个已过期的凭据。

```text theme={null}
Anthropic profile login expired · Re-authenticate your Anthropic profile
Anthropic profile login expired · Run /login to use your claude.ai account instead, or re-authenticate the profile
```

只有当生效的凭据来自 Anthropic 凭据配置文件时才会出现此消息，该配置文件可以是您通过 `ANTHROPIC_PROFILE` 环境变量选择的、Claude Code 在您的 Anthropic 配置目录中发现为活跃配置文件的，或是您[在没有 API 密钥的情况下登录](/docs/zh-CN/authentication#sign-in-without-an-api-key)时 Claude Code 写入的。使用 API 密钥、bearer 令牌（例如 `ANTHROPIC_AUTH_TOKEN`）或第三方提供商进行身份验证的会话永远不会看到此消息。

在[提供无密钥登录](/docs/zh-CN/authentication#sign-in-without-an-api-key)的机器上，运行 `/login`，选择 Anthropic Console 账户并重新登录，即可续期由无密钥 Console 登录或 Claude Platform CLI 的 `ant auth login` 写入的配置文件。Claude Code 会替换该配置文件中已过期的凭据。对于联合身份配置文件或由其他工具创建的配置文件，`/login` 不会续期凭据。您看到哪种形式，取决于配置文件是您选择的还是 Claude Code 发现的：

* 当您显式设置了 `ANTHROPIC_PROFILE` 时，消息以 `Re-authenticate your Anthropic profile` 结尾。
* 当 Claude Code 从您的配置目录中发现该配置文件时，消息会提供 `/login` 选项，因为 Claude Code 让可用的 `/login` 优先于所发现的配置文件，然后改用您的 claude.ai 或 Console 账户进行身份验证。在 v2.1.234 之前，这种情况下 Claude Code 也会显示 `Re-authenticate your Anthropic profile` 形式。

**解决方法：**

* 重新登录该配置文件，然后重试：在[提供无密钥登录](/docs/zh-CN/authentication#sign-in-without-an-api-key)的机器上，对于由无密钥 Console 登录或 Claude Platform CLI 的 `ant auth login` 写入的配置文件，运行 `/login` 并选择 Anthropic Console 账户；对于其他配置文件，请使用创建它们的工具
* 如果该配置文件的凭据由管理员预配，请让他们签发一个新的凭据
* 运行 `/status`，确认当前生效的凭据来源和配置文件名称
* 如需停止使用该配置文件，请取消设置 `ANTHROPIC_PROFILE`（如果您设置过），然后以其他方式进行身份验证，例如 `/login` 或 `ANTHROPIC_API_KEY`

<h3 id="oauth-scope-requirement">
  OAuth 作用域要求
</h3>

已存储的令牌早于某个新功能所需的权限作用域：

```text theme={null}
OAuth token does not meet scope requirement: user:profile
```

**解决方法：**

* 运行 `/login` 获取具有当前作用域的新令牌。您无需先注销。

<h3 id="claude-ai-rejected-the-session-token">
  claude.ai 拒绝了会话令牌
</h3>

[claude.ai 连接器](/docs/zh-CN/mcp#use-mcp-servers-from-claude-ai)请求失败，因为 claude.ai 拒绝了来自您 Claude Code 登录的令牌。被拒绝的令牌是您的登录，而不是该连接器在 claude.ai 中自身的授权，因此重新授权连接器并不能解决问题。在 `/mcp` 中，该连接器显示为 `session token rejected`，其详细信息视图显示：

```text theme={null}
claude.ai rejected the session token. Run /login, then reconnect.
```

**解决方法：**

* 运行 `/login` 重新登录
* 从 `/mcp` 重新连接该连接器，或运行 `/mcp reconnect <server>`。在重新登录之前重新连接，连接器会保持相同状态。`/mcp` 面板的 **Reconnect** 选项会报告 `your claude.ai session token was rejected`；而键入的 `/mcp reconnect <server>` 形式会报告重新连接成功，尽管令牌仍然被拒绝。

在 v2.1.222 之前，Claude Code 会将该连接器标记为需要身份验证，这会引导您进入连接器的授权流程，而完成该流程并不能解决此状态。

<h3 id="mcp-server-needs-you-to-sign-in-again">
  MCP 服务器需要您重新登录
</h3>

某个远程 [MCP 服务器](/docs/zh-CN/mcp)在会话中途的工具调用中拒绝了凭据，通常是因为登录或令牌已过期，或令牌缺少工具所需的权限。该工具调用失败，`/mcp` 会将该服务器标记为[需要身份验证](/docs/zh-CN/mcp#authenticate-with-remote-mcp-servers)。

对于您从 Claude Code 登录的服务器（包括 claude.ai 连接器），登录已过期或被撤销：

```text theme={null}
MCP server "<name>" needs you to sign in again (run /mcp to re-authenticate)
```

运行 `/mcp`，选择该服务器，然后从其菜单中重新登录。

对于配置了 [`headersHelper`](/docs/zh-CN/mcp#use-dynamic-headers-for-custom-authentication) 脚本的服务器，Claude Code 在显示以下消息之前已经重新运行过该 helper 并重试了一次调用：

```text theme={null}
MCP server "<name>" rejected the credential from its headersHelper (check the helper and run /mcp to reconnect, or to authenticate if the server also uses OAuth)
```

检查该 helper 是否返回服务器接受的凭据，然后从 `/mcp` 重新连接，这会再次运行该 helper。

对于在配置中带有静态 `Authorization` 标头的服务器：

```text theme={null}
MCP server "<name>" rejected the Authorization header in its config (update it, then run /mcp to reconnect)
```

在配置该服务器的位置更新标头值，然后从 `/mcp` 重新连接。

在 v2.1.273 之前，登录过期、`headersHelper` 和 `Authorization` 标头这几种情况都显示 `MCP server "<name>" requires re-authorization (token expired)`。

服务器也可能以 HTTP 403 `insufficient_scope` 拒绝工具调用，要求您授权某个作用域，有时该作用域甚至已列在您的令牌中。消息会指出该作用域：

```text theme={null}
MCP server "<name>" needs additional permissions (scope: "<scope>") — run /mcp to re-authenticate
```

运行 `/mcp`，选择该服务器，然后从其菜单中重新进行身份验证。

当服务器的配置既未设置 [`oauth.scopes`](/docs/zh-CN/mcp#restrict-oauth-scopes) 也未设置 [`authServerMetadataUrl`](/docs/zh-CN/mcp#override-oauth-metadata-discovery) 时，Claude Code 会请求服务器指出的作用域。如果设置了其中任一项，Claude Code 会改为请求该设置中的作用域。如果您固定了 `oauth.scopes`，请在重新进行身份验证之前将缺失的作用域添加到该列表中。

在 v2.1.274 之前，这种情况显示 `needs you to sign in again` 消息；在 v2.1.273 之前，它与其他情况一样显示 `requires re-authorization (token expired)`。

<h3 id="mcp-server-url-is-missing-or-not-a-valid-url">
  MCP 服务器 URL 缺失或不是有效的 URL
</h3>

Claude Code 拒绝为某个远程 MCP 服务器启动 OAuth 登录，因为该服务器配置的 `url` 无法解析为 URL。除非 Claude Code 对该服务器有更具体的配置问题需要报告，否则在您的 shell 中运行 [`claude mcp login <name>`](/docs/zh-CN/mcp#authenticate-from-the-command-line) 会将该拒绝输出为：

```text theme={null}
Couldn't complete authentication for "<name>": This server's URL is missing or not a valid URL, so sign-in can't start. Fix the URL in its MCP config (or set the environment variable it uses) and try again.
```

**解决方法：**

* 在配置该服务器的位置，将该条目的 `url` 设置为服务器的真实端点，或设置其 [`${VAR}` 引用](/docs/zh-CN/mcp#environment-variable-expansion-in-mcp-json)所指的环境变量，然后再次运行登录。

<h3 id="issuer-mismatch-in-authorization-response">
  授权响应中的颁发者不匹配
</h3>

在 [MCP OAuth 登录](/docs/zh-CN/mcp#authenticate-with-remote-mcp-servers)期间，授权服务器重定向回 Claude Code 时所携带的 `iss` 参数与 Claude Code 根据服务器 OAuth 元数据所期望的颁发者不一致。此步骤中出现错误的颁发者正是授权服务器混淆攻击（mix-up attack）的表现形式，因此 Claude Code 会让登录失败，而不是交换授权码。Claude Code 会在浏览器登录后，在 `/mcp` 服务器菜单中显示该错误：

```text theme={null}
Issuer mismatch in authorization response (RFC 9207): expected "https://auth.example.com", received "https://other.example.com"
```

`expected` 是来自服务器 OAuth 元数据的颁发者，`received` 是重定向所携带的 `iss` 值。重定向未携带 `iss` 参数的登录会通过检查，除非服务器的元数据设置了 `authorization_response_iss_parameter_supported`，这种情况下 Claude Code 会让登录失败。

**解决方法：**

* 从 `/mcp` 再次尝试登录
* 如果错误重复出现，请向服务器运营方报告。需要在服务器端修复：授权服务器必须在 `iss` 参数中返回与其元数据中公布的相同的颁发者
* 如需在服务器修复期间进行连接，请使用 [`MCP_SDK_GENERATION=v1`](/docs/zh-CN/env-vars) 启动 Claude Code，其[运行时](/docs/zh-CN/mcp#mcp-client-runtimes)不执行此检查。这会移除一项针对混淆攻击的防护，因此请优先采用服务器端修复

在 v2.1.232 之前，Claude Code 仅在逐步推出时或您设置 `MCP_SDK_GENERATION=v2` 时才使用 v2 运行时。

<h3 id="refusing-to-send-credentials-to-non-https-token-endpoint">
  拒绝向非 https 令牌端点发送凭据
</h3>

在 [v2 运行时](/docs/zh-CN/mcp#mcp-client-runtimes)上，Claude Code 只会将 [MCP OAuth](/docs/zh-CN/mcp#authenticate-with-remote-mcp-servers) 令牌请求发送到通过 HTTPS 提供服务的令牌端点，或位于 `localhost`、`127.0.0.1` 或 `::1` 的令牌端点。此消息表示服务器的令牌端点两者都不是，因此 Claude Code 在发送请求前就停止了。这发生在浏览器登录之后，因此浏览器步骤会先成功，并且每当 Claude Code 刷新该服务器的令牌时都会再次发生。

该消息的完整形式来自 MCP SDK，并会引用它拒绝的令牌端点。在调试日志中，对于登录，它跟在 `Error during auth completion:` 之后；对于刷新，它跟在 `Token refresh failed:` 之后。在您的 shell 中，`claude mcp login <name>` 会在 `Couldn't complete authentication for "<name>":` 之后输出它；在会话中，`/mcp` 会在服务器菜单下显示它：

```text theme={null}
Refusing to send credentials to non-https token endpoint 'http://192.168.1.50:8123/oauth/token'. OAuth token requests MUST use TLS (localhost / 127.0.0.1 / ::1 are exempt).
```

Claude Code 会将带有查询字符串或较长的随机外观路径段的服务器 URL 视为可能是机密的。对于此类服务器，它会在显示或记录 MCP SDK 引发的登录错误之前对其进行脱敏。此时该错误会显示为一个可能因版本而变化的简短名称（例如 `io`），后跟 `from the MCP SDK for` 和经过脱敏的服务器 URL。来自 MCP SDK 的其他错误在这种情况下也采用相同的形式。只有当服务器的令牌端点是位于 `localhost`、`127.0.0.1` 或 `::1` 以外地址的普通 `http://` 时，脱敏后的消息才可能是此错误。

**解决方法：**

* 通过 HTTPS 提供该令牌端点，例如将服务器置于终止 TLS 的反向代理或隧道之后，并配置服务器公布 `https://` 地址
* 如需在不更改服务器的情况下进行连接，请使用 [`MCP_SDK_GENERATION=v1`](/docs/zh-CN/env-vars) 启动 Claude Code，其[运行时](/docs/zh-CN/mcp#mcp-client-runtimes)不应用此规则，会通过普通 HTTP 发送令牌请求。该选择会持续到您退出为止，并适用于所有服务器。v1 运行时还会跳过[颁发者检查](#issuer-mismatch-in-authorization-response)，因此请优先通过 HTTPS 提供该端点

<h3 id="aws-credentials-expired-or-invalid">
  AWS 凭据已过期或无效
</h3>

您的 AWS 会话令牌已过期或被拒绝。当 [Claude Platform on AWS](/docs/zh-CN/claude-platform-on-aws) 或 [Mantle 端点](/docs/zh-CN/amazon-bedrock#use-the-mantle-endpoint)返回 401 时会出现此消息，这是这些提供商报告安全令牌过期的方式。

中间的操作提示因您的设置而异。稳定不变的部分是开头的 `AWS credentials expired or invalid`：

```text theme={null}
AWS credentials expired or invalid · run /login and select "Claude Platform on AWS · refresh credentials", or run `aws sso login --profile myprofile` in another terminal · API Error: 401 ...
```

在 v2.1.273 之前，只有在配置了 `awsAuthRefresh` 时才会出现此消息。

**解决方法：**

* 如果提示说明凭据由此环境管理，则凭据归启动 Claude Code 的应用所有，此处的其他步骤不适用：请重试，或联系您的管理员
* 如果设置了 [`awsAuthRefresh`](/docs/zh-CN/amazon-bedrock#advanced-credential-configuration)，请在另一个终端中运行消息中指出的命令（例如 `aws sso login --profile myprofile`）并完成浏览器登录，然后重试。否则，请自行刷新您所使用的 AWS 凭据：您的 SSO 登录、访问密钥、API 密钥或代理令牌
* 在设置了 `awsAuthRefresh` 的交互式会话中，您也可以运行 `/login`，选择 **3rd-party platform**，然后在 **Using 3rd-party platforms** 下选择 **Claude Platform on AWS · refresh credentials**，无需重启 Claude Code 即可运行同一命令。请参阅[配置 AWS 凭据](/docs/zh-CN/claude-platform-on-aws#1-configure-aws-credentials)
* 如果刷新命令成功后错误仍然重复出现，请在同一 shell 和 profile 中运行 `aws sts get-caller-identity`，确认该身份在 Claude Code 之外有效

<h3 id="aws-authentication-failed">
  AWS 身份验证失败
</h3>

您的 AWS 提供商返回了 403，或 [Amazon Bedrock](/docs/zh-CN/amazon-bedrock) 返回了 401。

Amazon Bedrock 将安全令牌过期报告为 403，但 403 也是它报告授权被拒绝的方式，例如因缺少 IAM 权限而产生的 `AccessDeniedException`。Claude Code 无法区分这两种原因。

来自 Amazon Bedrock 的 401 也会归到这里，而不是[AWS 凭据已过期或无效](#aws-credentials-expired-or-invalid)，因为 Amazon Bedrock 不会将令牌过期报告为 401。来自该端点的 401 通常来自请求路径中的其他环节，例如企业代理。

刷新凭据可以修复令牌过期，但无法修复其他原因，因此消息同时提供了两种方案：

```text theme={null}
AWS authentication failed · run /login and select "Claude Platform on AWS · refresh credentials", or run `aws sso login --profile myprofile` in another terminal · if credentials are current, check AWS permissions and model access · API Error: 403 ...
```

中间的操作提示因您的设置而异。稳定不变的部分是开头的 `AWS authentication failed`。

当 403 是 Amazon Bedrock 表示您无权访问指定模型 ID 的模型时，提示会改为告诉您在 Amazon Bedrock 控制台中为您的账户和区域启用该模型。

在 v2.1.273 之前，只有在配置了 `awsAuthRefresh` 时才会出现此消息。

**解决方法：**

* 如果提示说明凭据由此环境管理，则凭据归启动 Claude Code 的应用所有，此处的其他步骤不适用：请重试，或联系您的管理员
* 刷新您的 AWS 凭据，以防原因是凭据过期：如果设置了 [`awsAuthRefresh`](/docs/zh-CN/amazon-bedrock#advanced-credential-configuration)，请运行消息中指出的该命令；否则请自行刷新您的 SSO 登录、访问密钥、API 密钥或代理令牌
* 如果您的凭据是最新的，请确认 [IAM 配置](/docs/zh-CN/amazon-bedrock#iam-configuration)中的 IAM 权限已附加到您正在使用的身份，并且所选模型已为您的账户和区域启用
* 运行 `aws sts get-caller-identity`，确认您的请求使用的是哪个身份

<h3 id="google-cloud-credentials-expired-or-invalid">
  Google Cloud 凭据已过期或无效
</h3>

您用于 [Google Cloud's Agent Platform](/docs/zh-CN/google-vertex-ai) 的 Google Cloud 凭据已过期或被拒绝：请求返回了 401，这是 Agent Platform 报告凭据过期的方式。

中间的操作提示因您的设置而异。稳定不变的部分是开头的 `Google Cloud credentials expired or invalid`：

```text theme={null}
Google Cloud credentials expired or invalid · refresh your Google Cloud credentials (application default sign-in, or the key file in GOOGLE_APPLICATION_CREDENTIALS) and retry · API Error: 401 ...
```

**解决方法：**

* 如果提示说明凭据由此环境管理，则凭据归启动 Claude Code 的应用所有，此处的其他步骤不适用：请重试，或联系您的管理员
* 如果您使用应用默认凭据进行身份验证，请运行消息中指出的 [`gcpAuthRefresh`](/docs/zh-CN/google-vertex-ai#advanced-credential-configuration) 命令或 `gcloud auth application-default login` 并完成登录，然后重试
* 如果您在设置了 `CLAUDE_CODE_SKIP_VERTEX_AUTH` 的情况下通过 [LLM 网关](/docs/zh-CN/llm-gateway)路由，请刷新 `ANTHROPIC_AUTH_TOKEN` 或 `ANTHROPIC_CUSTOM_HEADERS` 中的网关令牌，然后重试
* 如果您使用服务账号密钥文件进行身份验证，请确认 `GOOGLE_APPLICATION_CREDENTIALS` 指向有效的密钥。请参阅[配置 GCP 凭据](/docs/zh-CN/google-vertex-ai#3-configure-gcp-credentials)
* 如果刷新后错误仍然重复出现，请在同一 shell 中运行 `gcloud auth application-default print-access-token`，确认该身份在 Claude Code 之外可以正常工作

在 v2.1.273 之前，来自 Agent Platform 的 401 会改为显示通用的 `Please run /login` 或 `Failed to authenticate` 消息，而这些消息无法刷新 Google Cloud 凭据。

<h3 id="google-cloud-authentication-failed">
  Google Cloud authentication failed
</h3>

[Google Cloud 的 Agent Platform](/docs/zh-CN/google-vertex-ai) 返回了 403，该平台使用此状态码表示授权被拒绝，而非凭据过期。通常是您用于身份验证的身份缺少某项 IAM 权限，或者您的项目未启用该模型。

中间的操作提示因您的设置而异。固定不变的部分是开头的 `Google Cloud authentication failed`：

```text theme={null}
Google Cloud authentication failed · refresh your Google Cloud credentials (application default sign-in, or the key file in GOOGLE_APPLICATION_CREDENTIALS) and retry · if credentials are current, check GCP IAM permissions and Vertex AI model access · API Error: 403 ...
```

**解决方法：**

* 如果提示表明凭据由当前环境管理，则凭据归启动 Claude Code 的应用所有，此处的其他步骤不适用：请重试，或联系您的管理员
* 确认 [IAM 配置](/docs/zh-CN/google-vertex-ai#iam-configuration)中的角色已授予您用于身份验证的身份
* 确认您的项目已启用该模型。请参阅[申请模型访问权限](/docs/zh-CN/google-vertex-ai#2-request-model-access)

在 v2.1.273 之前，来自 Agent Platform 的 403 会改为显示通用的 `Please run /login` 或 `Failed to authenticate` 消息，而这些操作无法刷新 Google Cloud 凭据。

<h3 id="microsoft-foundry-authentication-failed">
  Microsoft Foundry authentication failed
</h3>

[Microsoft Foundry](/docs/zh-CN/microsoft-foundry) 返回了 401 或 403：请求中的 Azure 凭据被拒绝，或者其背后的身份无权访问 Foundry 资源。`/login` 无法生成 Azure 凭据。中间的操作提示因您的设置而异。固定不变的部分是开头的 `Microsoft Foundry authentication failed`：

```text theme={null}
Microsoft Foundry authentication failed · refresh your Foundry credential (ANTHROPIC_FOUNDRY_AUTH_TOKEN, ANTHROPIC_FOUNDRY_API_KEY, Azure sign-in for Entra, or your proxy token) and retry · if credentials are current, check access to the Foundry resource · API Error: 401 ...
```

**解决方法：**

* 如果提示表明凭据由当前环境管理，则凭据归启动 Claude Code 的应用所有，此处的其他步骤不适用：请重试，或联系您的管理员
* 刷新您在[配置 Azure 凭据](/docs/zh-CN/microsoft-foundry#2-configure-azure-credentials)中配置的凭据：轮换 `ANTHROPIC_FOUNDRY_API_KEY`、生成新的 `ANTHROPIC_FOUNDRY_AUTH_TOKEN`，或运行 `az login` 以便默认的 Microsoft Entra 凭据链可以重新登录
* 如果凭据有效，请确认该身份有权访问 Foundry 资源。请参阅 [Azure RBAC 配置](/docs/zh-CN/microsoft-foundry#azure-rbac-configuration)

在 v2.1.273 之前，来自 Microsoft Foundry 的 401 或 403 会改为显示通用的 `Please run /login` 或 `Failed to authenticate` 消息，而这些操作无法刷新 Azure 凭据。

<h3 id="could-not-load-aws-or-google-cloud-credentials">
  Could not load AWS or Google Cloud credentials
</h3>

Claude Code 无法从其运行所在机器上的 AWS 凭据提供程序链或 Google 应用默认凭据中获取可用凭据，因此没有请求到达您的云提供商。`·` 之后的详细信息指明了具体原因，例如 SSO 会话已过期、缺少应用默认凭据（报告为 `Could not load the default credentials`），或登录已被撤销（报告为 `invalid_grant`）：

```text theme={null}
API Error: Could not load AWS credentials · Could not load credentials from any providers. Check or refresh your AWS credentials and try again.
API Error: Could not load Google Cloud credentials · invalid_grant. Check or refresh your Google Cloud credentials and try again.
```

在使用 `-p` 的[非交互模式](/docs/zh-CN/headless)和 [Agent SDK](/docs/zh-CN/agent-sdk/overview) 中，结构化错误代码为 `cloud_credential_error`。在 v2.1.267 之前，该消息仅显示 `API Error:` 之后的详细文本，结构化代码为 `server_error` 或 `unknown`。

**解决方法：**

* 运行您的提供商的登录命令，例如 `aws sso login --profile myprofile` 或 `gcloud auth application-default login`，然后重试。[Bedrock、Agent Platform 或 Foundry 凭据无法加载](/docs/zh-CN/troubleshoot-install#bedrock-agent-platform-or-foundry-credentials-not-loading)介绍了如何在 Claude Code 之外确认凭据
* 如果详细信息为 `AWS default-chain credential resolve timed out`，则表示凭据链卡住了而非失败，请改为按照 [AWS default-chain credential resolve timed out](#aws-default-chain-credential-resolve-timed-out) 进行处理

<h3 id="aws-default-chain-credential-resolve-timed-out">
  AWS default-chain credential resolve timed out
</h3>

AWS 默认凭据提供程序链未能在 60 秒内生成凭据，因此 Claude Code 停止了解析并使请求失败。此超时是 [Could not load AWS or Google Cloud credentials](#could-not-load-aws-or-google-cloud-credentials) 的原因之一。失败发生在本地凭据解析阶段：请求从未到达 [Amazon Bedrock](/docs/zh-CN/amazon-bedrock)、[Claude Platform on AWS](/docs/zh-CN/claude-platform-on-aws) 或 [Mantle 端点](/docs/zh-CN/amazon-bedrock#use-the-mantle-endpoint)。Claude Code 会在此错误出现之前清除其[凭据缓存](/docs/zh-CN/amazon-bedrock#credential-caching-and-resolution-timeout)并重试，因此当您看到此错误时，凭据链已在多次尝试中停滞。

```text theme={null}
API Error: Could not load AWS credentials · AWS default-chain credential resolve timed out. Check or refresh your AWS credentials and try again.
```

常见原因包括：AWS 配置文件中的 `credential_process` 命令在等待它无法接收的输入，以及容器或虚拟机的实例元数据服务（IMDS）始终未响应凭据链的探测。

在 v2.1.267 之前，该消息为 `API Error: AWS default-chain credential resolve timed out`。
在 v2.1.207 之前，停滞的凭据链会让请求无限期等待，而不是失败。

**解决方法：**

* 在同一 shell 中使用相同的 `AWS_PROFILE` 运行 `aws sts get-caller-identity`。如果它也卡住，请修复该配置文件；以交互方式提示输入的 `credential_process` 命令是常见原因。
* 在启动 Claude Code 之前完成登录步骤，例如 `aws sso login --profile myprofile`
* 如果您的凭据链运行的交互式登录确实需要超过 60 秒，例如通过 `aws-vault` 等包装工具进行带 MFA 的 SSO，请使用 [`CLAUDE_CODE_AWS_CHAIN_RESOLVE_TIMEOUT_MS`](/docs/zh-CN/env-vars) 以毫秒为单位提高该限制

<h3 id="bedrock-setup-verification-timed-out-waiting-for-aws">
  Bedrock setup verification timed out waiting for AWS
</h3>

在 [Bedrock 设置向导](/docs/zh-CN/amazon-bedrock#sign-in-with-bedrock)的凭据验证过程中，对 AWS 的某个调用（例如凭据查找或身份检查）未能在 60 秒限制内完成。向导停止等待，并使验证步骤失败：

```text theme={null}
Timed out after 60s waiting for AWS. Check your network and proxy settings; if a credential helper needs longer to prompt you, raise CLAUDE_CODE_AWS_CHAIN_RESOLVE_TIMEOUT_MS.
```

其中的数字反映您的限制：默认为 60 秒，或您在 [`CLAUDE_CODE_AWS_CHAIN_RESOLVE_TIMEOUT_MS`](/docs/zh-CN/env-vars) 中设置的值。

常见原因包括：网络或代理使发往 AWS 的请求（包括 SSO 令牌刷新）停滞，以及凭据助手仍在等待您看不到的输入。仅当助手确实需要更多时间时才提高该限制。

发往 AWS 的单个停滞请求也可能因其自身的单次请求超时而失败，此时同一步骤会显示一条较短的消息：

```text theme={null}
A request to AWS timed out. Check your network and proxy settings, then try again.
```

当相同的超时发生在模型固定步骤时，向导会将模型标记为 `unreachable`，而不显示上述任一消息。

**解决方法：**

* 在同一 shell 中运行 `aws sts get-caller-identity`。如果它也卡住，则停滞发生在 Claude Code 之外，位于您的网络、代理或 AWS 配置文件中的凭据助手；请先修复该问题。
* 在打开向导之前完成所有交互式登录，例如 `aws sso login --profile myprofile`
* 如果 AWS 配置文件中的凭据助手确实需要超过 60 秒来提示您，请使用 [`CLAUDE_CODE_AWS_CHAIN_RESOLVE_TIMEOUT_MS`](/docs/zh-CN/env-vars) 以毫秒为单位提高该限制

<h3 id="cloud-gateway-session-expired">
  Cloud gateway session expired
</h3>

您通过 [Claude apps 网关](/docs/zh-CN/claude-apps-gateway)登录，而保存在此机器上的网关会话已过期且无法续期，或者网关不再接受该会话，例如在网关的 [JWT 密钥被替换](/docs/zh-CN/claude-apps-gateway-deploy#jwt-secret-rotation)之后。如果您在以交互方式启动 `claude` 时看到这行消息，则表示会话已以未登录网关的状态打开：

```text theme={null}
Cloud gateway session expired — run /login to reconnect.
```

当网关凭据过期且 Claude Code 无法续期时，同一行消息也可能在会话中途出现。

在[非交互](/docs/zh-CN/headless)运行、后台或其他无人值守会话，或除 `claude auth` 以外的 `claude` 子命令中，当网关不再接受该会话时，Claude Code 会改为显示以下消息并退出：

```text theme={null}
Cloud gateway <url> no longer accepts this session. Start `claude` and sign in again with /login.
```

**解决方法：**

* 在会话中运行 `/login` 并完成浏览器登录
* 对于非交互式启动，请在同一环境中启动 `claude`，运行 `/login`，然后重新运行您的命令

<h3 id="sign-in-timed-out-while-waiting-for-you-to-continue">
  Sign-in timed out while waiting for you to continue
</h3>

在 [Claude apps 网关](/docs/zh-CN/claude-apps-gateway)登录过程中，网关给出了已登录的账户，Claude Code 在保存凭据之前请您确认该账户。您让确认界面保持打开的时间超过了该次登录自身的有效期，且网关未签发可用于续期的刷新令牌，因此当您继续时，Claude Code 未存储任何内容：

```text theme={null}
Sign-in timed out while waiting for you to continue. Try again.
```

**解决方法：**

* 再次运行 `/login`，并在登录过期之前确认账户

<h3 id="gateway-refused-the-request">
  Gateway refused the request
</h3>

您通过 [Claude apps 网关](/docs/zh-CN/claude-apps-gateway)登录，而某个请求返回了 403：网关或其背后的上游拒绝了该请求。重新登录不会改变拒绝结果，因此消息会提示您联系网关管理员：

```text theme={null}
Gateway refused the request · signing in again won't change this — check with your gateway administrator · API Error: 403 ...
```

**解决方法：**

* 请您的网关管理员查询该请求。`API Error:` 之后的部分包含网关返回的拒绝信息
* 对于管理员：网关上的[访问控制规则](/docs/zh-CN/claude-apps-gateway-config#http-tuning)会返回 403，[审计日志](/docs/zh-CN/claude-apps-gateway-deploy#logs)会记录该 403 及其原因；上游的授权拒绝会按照[上游错误消息](/docs/zh-CN/claude-apps-gateway-config#upstream-error-messages)中的说明透传

在 v2.1.273 之前，网关会话上的 403 会改为显示通用的 `Please run /login` 或 `Failed to authenticate` 消息，且重新登录无法消除该拒绝。

<h2 id="network-and-connection-errors">
  网络和连接错误
</h2>

大多数这些错误意味着来自 Claude Code 的网络请求未能到达其目的地，或者 Claude Code 和 API 之间的某些东西在返回时改变了响应；如果条目还有本地原因（例如存档写入失败），其正文会说明这一点。它们通常源于您的本地网络、代理或防火墙，或云环境的网络策略。

<h3 id="unable-to-connect-to-api">
  无法连接到 API
</h3>

到 API 的 TCP 连接失败或从未完成。对于常见的连接错误代码，消息名称指出失败的类型并在括号中保留代码：

```text theme={null}
Unable to connect to API. Check your internet connection
Connection refused — a firewall or proxy may be blocking it (ConnectionRefused)
Can't reach the API server — check your internet or DNS (ENOTFOUND)
No internet route — check your connection or VPN (EHOSTUNREACH)
Couldn't connect through your proxy (ERR_PROXY_TUNNEL) — the proxy refused the tunnel: check its credentials and that it allows this host
Connection dropped (ECONNRESET)
Request timed out. Check your internet connection and proxy settings
```

Claude Code 不识别的代码显示为 `Unable to connect to API` 后跟括号中的代码。某些这些消息可以显示多个代码：`Connection refused` 可以显示 `ConnectionRefused` 或 `ECONNREFUSED`，例如，`Can't reach the API server` 可以显示 `ENOTFOUND` 或 `FailedToOpenSocket`。

在 v2.1.227 之前，这些编码消息中的每一个都读作 `Unable to connect to API` 后跟代码，例如 `Unable to connect to API (ECONNREFUSED)`。

常见原因包括没有互联网访问、阻止 `api.anthropic.com` 的 VPN，或未配置的必需企业代理。

**要做什么：**

* 通过从同一 shell 运行 `curl -I https://api.anthropic.com` 来确认您可以到达 API 主机。在 Windows PowerShell 上使用 `curl.exe -I https://api.anthropic.com` 以便不使用内置的 `Invoke-WebRequest` 别名。
* 如果您在企业代理后面，在启动 Claude Code 之前设置 `HTTPS_PROXY` 并查看[网络配置](/docs/zh-CN/network-config)
* 如果您通过 LLM 网关或中继路由，将 [`ANTHROPIC_BASE_URL`](/docs/zh-CN/env-vars) 设置为其地址。有关设置，请参阅[将 Claude Code 连接到 LLM 网关](/docs/zh-CN/llm-gateway-connect)。
* 确保您的防火墙允许[网络访问要求](/docs/zh-CN/network-config#network-access-requirements)中列出的主机
* 间歇性故障会[自动重试](#automatic-retries)；持续故障指向本地网络问题

如果 `curl` 成功但 Claude Code 仍然失败，原因通常是运行时和网络之间的某些东西，而不是网络本身：

* 通过运行 `echo $ANTHROPIC_BASE_URL` 检查 `ANTHROPIC_BASE_URL` 是否已设置，或在 PowerShell 中运行 `echo $env:ANTHROPIC_BASE_URL`，并在您的[设置文件](/docs/zh-CN/settings)的 `env` 块中查找它。当它被设置时，Claude Code 将模型请求发送到该地址而不是 `api.anthropic.com`，因此指向不再运行的本地代理或网关的遗留值会产生 `Connection refused`，即使 `curl` 到达 API。从您的 shell 配置文件或设置中删除它，并从新终端启动 Claude Code。
* 在 Linux 和 WSL 上，检查 `/etc/resolv.conf` 是否有无法到达的名称服务器。WSL 特别可以从主机继承损坏的解析器。
* 在 macOS 上，已断开连接或卸载的 VPN 客户端可能会留下隧道接口或路由规则。检查 `ifconfig` 是否有陈旧的 `utun` 接口，并在系统设置中删除 VPN 的网络扩展。
* Docker Desktop 和类似的容器运行时可以拦截出站流量。退出它们并重试以排除这种可能性。

<h3 id="unable-to-connect-to-anthropic-services">
  无法连接到 Anthropic 服务
</h3>

在首次运行设置期间，Claude Code 检查它是否可以到达 `api.anthropic.com` 和 `platform.claude.com`，然后再显示登录步骤。当任一检查失败时，Claude Code 打印原因并退出。

```text theme={null}
Unable to connect to Anthropic services
Failed to connect to api.anthropic.com: ECONNREFUSED
Connection to api.anthropic.com timed out after 10 seconds
A proxy is configured via HTTPS_PROXY. Check that it allows connections to the host above.
```

Claude Code 通过与 API 请求相同的[代理配置](/docs/zh-CN/network-config)发送检查，并给每个探针 10 秒。当失败的探针通过代理时，消息名称配置它的环境变量，例如 `HTTPS_PROXY`。在 v2.1.222 之前，检查使用不同的代理传输，没有超时：在具有 `https://` 方案的代理 URL 后面，它可能会在 `Checking connectivity...` 上无限期停滞，然后即使通过同一代理的 API 请求成功也会失败。

当[托管设置文件、MDM 策略或策略助手](/docs/zh-CN/managed-settings)将 [`forceLoginMethod`](/docs/zh-CN/settings-reference#forceloginmethod) 设置为 `"gateway"` 或设置 [`forceLoginGatewayUrl`](/docs/zh-CN/settings-reference#forcelogingatewayurl) 而不设置 `forceLoginMethod` 时，Claude Code 会跳过此检查。使用任一配置，Claude Code 在**云网关**屏幕上打开登录步骤，而不是 Anthropic 登录方法。当机器上存在托管设置源但无法读取时，Claude Code 也会跳过检查，因为该源可能包含网关配置。在 v2.1.247 之前，Claude Code 在此配置下也运行检查，当 Anthropic 的端点无法到达时以此错误退出。

**要做什么：**

* 如果消息名称代理变量，检查其值是否指向正确的代理，并要求您的网络团队允许通过它进行 HTTPS 连接到消息中的主机。请参阅[网络配置](/docs/zh-CN/network-config)。
* 完成[无法连接到 API](#unable-to-connect-to-api) 中的检查。那里的 `curl` 测试和防火墙指导也适用于此检查。
* 如果您的网络是开放的，故障仍然存在，Claude Code 可能在您的国家[不可用](https://www.anthropic.com/supported-countries)

<h3 id="socket-is-closed">
  Socket 已关闭
</h3>

`Socket is closed` 意味着承载流式响应的连接在响应仍在到达时被关闭。最常见的原因是 Windows 上的企业代理在响应中途丢弃已建立的隧道。

根据响应的进度，Claude Code 重试请求、保留 Claude 生成的内容或结束轮次。请参阅[自动重试](#automatic-retries)。

在 v2.1.214 之前，Claude Code 不会重试此故障，轮次停止并显示包含 `Socket is closed` 的错误。

**要做什么：**

* 如果您看到此错误，使用 `claude update` 更新到 v2.1.214 或更高版本，然后再次发送您的消息
* 如果在更新后轮次在同一代理后面继续失败，请完成[无法连接到 API](#unable-to-connect-to-api) 并检查[网络配置](/docs/zh-CN/network-config)中的代理设置

<h3 id="api-returned-an-empty-or-malformed-response">
  API 返回了空的或格式错误的响应
</h3>

Claude Code 在失败的流式请求的非流式重试获得 HTTP 成功状态但正文不是 Claude API 消息时显示此错误：通常是 HTML 错误或登录页面、空正文或其他格式的 JSON。代理、网关或网络登录页面代替 API 回答是常见的来源。Claude Code 不会重试请求，轮次以此错误结束。

```text theme={null}
API returned an empty or malformed response (HTTP 200) — check for a proxy or gateway intercepting the request.
```

在该开头之后，消息报告返回的内容和哪个请求失败：

* 一个 `Response:` 子句，包含内容类型、正文类型（例如 `body is an HTML page` 或 `empty body`）、其大小（以字节为单位）以及响应是否携带 Anthropic 请求 id。当响应名称可识别的服务器（例如 `nginx` 或 `cloudflare`）或携带中介标头（例如 `cf-ray` 或 `via`）时，子句也会列出这些。
* 一个句子，名称失败的流式请求的 id 和触发重试的故障。当流在故障之前打开时，它也报告有多少流事件到达，如果有的话，当尝试失败时流已沉默多长时间。

在 v2.1.234 之前，消息在 `intercepting the request` 之后结束。

在 v2.1.271 之前，在非 JSON 内容类型（例如 `text/plain`）下携带有效 API 消息的回复也以此错误结束轮次。某些 LLM 网关对非流式回复使用该内容类型。

**要做什么：**

* 阅读 `Response:` 子句以查看哪个系统回答。HTML 正文、没有 Anthropic 请求 id 或名称服务器（例如 `nginx` 或 `cloudflare`）意味着 Claude Code 和 API 之间的某些东西代替回答
* 如果您通过[LLM 网关](/docs/zh-CN/llm-gateway-connect#troubleshoot-gateway-errors)路由，使用直接请求测试路由，并修复返回非 API 响应的跳跃
* 在具有登录页面的网络上（例如访客 Wi-Fi），在浏览器中完成登录，然后重试
* 如果只有通过您的网关的非流式路由被破坏，设置 [`CLAUDE_CODE_DISABLE_NONSTREAMING_FALLBACK=1`](/docs/zh-CN/env-vars#variables) 以关闭此回退，除非流式端点本身返回 `404`，Claude Code 仍然会回退

<h3 id="streaming-response-ended-before-any-complete-data-was-received">
  流式响应在接收任何完整数据之前结束
</h3>

来自您的模型提供商的流式响应完成而没有传递任何可用数据，因此 Claude Code 重新发送了没有流式的请求以完成轮次。Claude Code 在交互式会话中每个会话显示一次警告。在 v2.1.239 之前，Claude Code 无声地重试而不流式。

```text theme={null}
Streaming response ended before any complete data was received. Retrying without streaming. If this keeps happening, check any proxy or gateway between Claude Code and your model provider.
```

Claude Code 发送每个受影响的请求两次：空流式尝试和重试。常见原因是在返回时消耗或转换流式响应正文的代理或网关。

**要做什么：**

* 配置 Claude Code 和您的模型提供商之间的任何代理或网关，以通过未修改的流式响应正文和其标头
* 在[Amazon Bedrock](/docs/zh-CN/amazon-bedrock) 上，请参阅[网关或代理后面的流式错误](/docs/zh-CN/amazon-bedrock#streaming-errors-behind-a-gateway-or-proxy)了解标头和正文要求

<h3 id="bedrock-streaming-response-has-an-unexpected-content-type">
  Bedrock 流式响应具有意外的 content-type
</h3>

Claude Code 和[Amazon Bedrock](/docs/zh-CN/amazon-bedrock) 之间的网关或代理正在转换流式响应正文或其 `Content-Type` 标头。Amazon Bedrock 将响应流式传输为 `application/vnd.amazon.eventstream`。Claude Code 不会解码它无法读取的正文，而是拒绝报告不同 content-type 的成功流式响应。Claude Code 不会重试请求。

```text theme={null}
Bedrock streaming response has content-type "text/event-stream"; expected "application/vnd.amazon.eventstream". A gateway or proxy between Claude Code and Bedrock is likely transforming the response body — Bedrock's binary event-stream format must be passed through unmodified. Set CLAUDE_CODE_DISABLE_BEDROCK_CONTENT_TYPE_GUARD=1 to suppress this check while the gateway is being fixed.
```

在 v2.1.208 之前，相同的配置错误显示为 `API Error: Truncated event message received`，在整个响应被缓冲后。

**要做什么：**

* 配置网关以通过未修改的 `InvokeModelWithResponseStream` 响应正文及其 `Content-Type` 标头。将流重新发出为服务器发送事件的中介是常见原因。
* 设置 [`CLAUDE_CODE_DISABLE_BEDROCK_CONTENT_TYPE_GUARD=1`](/docs/zh-CN/env-vars) 隐藏此错误，但 Claude Code 不会在重写的标头下解码二进制正文，因此这些请求回退到较慢的非流式路径。请参阅[网关或代理后面的流式错误](/docs/zh-CN/amazon-bedrock#streaming-errors-behind-a-gateway-or-proxy)。

<h3 id="ssl-certificate-errors">
  SSL 证书错误
</h3>

您网络上的代理或安全设备正在用其自己的证书拦截 TLS 流量，Claude Code 不信任它。

```text theme={null}
Unable to connect to API: SSL certificate verification failed (UNABLE_TO_GET_ISSUER_CERT_LOCALLY). The certificate comes from an authority Claude Code doesn't trust, usually a TLS-inspecting corporate proxy or a gateway signed by a private CA: set NODE_EXTRA_CA_CERTS to that CA bundle, or add it to the system certificate store · see https://code.claude.com/docs/en/network-config
Unable to connect to API: Self-signed certificate detected (SELF_SIGNED_CERT_IN_CHAIN). The certificate comes from an authority Claude Code doesn't trust, usually a TLS-inspecting corporate proxy or a gateway signed by a private CA: set NODE_EXTRA_CA_CERTS to that CA bundle, or add it to the system certificate store · see https://code.claude.com/docs/en/network-config
```

在 v2.1.273 之前，两条消息都在 `Check your proxy or corporate SSL certificates` 处结束，没有 OpenSSL 代码或 `NODE_EXTRA_CA_CERTS` 提示。

从 v2.1.199 开始，证书验证失败不会重试，因此此错误出现在第一次尝试而不是完整[重试预算](#automatic-retries)之后。早期版本在显示它之前花费几分钟重试。瞬时 TLS 条件（例如握手超时）仍然重试。

在 `/login` 和启动连接检查期间，相同的故障产生不同的消息：

```text theme={null}
SSL certificate error (UNABLE_TO_GET_ISSUER_CERT_LOCALLY). If you are behind a corporate proxy or TLS-intercepting firewall, set NODE_EXTRA_CA_CERTS to your CA bundle path, or ask IT to allowlist *.anthropic.com. Run `claude doctor` for details.
```

在[Amazon Bedrock](/docs/zh-CN/amazon-bedrock) 上，Claude Code 本身发送给 AWS 的请求，例如 STS 和 SSO 角色凭证调用、模型发现和设置向导的检查，取决于相同的证书配置。请参阅[TLS 检查代理后面的证书错误](/docs/zh-CN/amazon-bedrock#certificate-errors-behind-a-tls-inspecting-proxy)。

**要做什么：**

* 导出您组织的 CA 包并使用 `NODE_EXTRA_CA_CERTS=/path/to/ca-bundle.pem` 指向 Claude Code
* 有关完整设置说明，请参阅[网络配置](/docs/zh-CN/network-config#custom-ca-certificates)
* 不要设置 `NODE_TLS_REJECT_UNAUTHORIZED=0`，这会完全禁用证书验证

<h3 id="host-not-allowed-in-a-cloud-session">
  云会话中不允许的主机
</h3>

来自云会话或例程的出站 HTTP 请求被环境的网络策略阻止。

```text theme={null}
HTTP 403
x-deny-reason: host_not_allowed
```

您也可能看到与目标的真实证书不匹配的 TLS 证书。云会话通过代理路由出站流量以强制执行网络策略，因此不匹配的证书意味着代理终止了连接，而不是目标。

这不是客户端网络问题。云会话和[例程](/docs/zh-CN/routines)在沙箱 VM 内运行，其通过会话网络的出站流量被过滤到[云环境的](/docs/zh-CN/cloud-environments)允许列表；[GitHub 操作](/docs/zh-CN/cloud-environments#github-proxy)和 MCP 连接器流量使用单独的通道，这就是为什么当其他主机被阻止时它们可以继续工作。**默认**环境使用**受信任**访问，允许[默认允许列表](/docs/zh-CN/cloud-environments#default-allowed-domains)的包注册表、云提供商 API、容器注册表和常见开发域，并阻止该路径上的其他域。

**要做什么：**

这些步骤更改您自己的环境之一。[组织共享环境](/docs/zh-CN/cloud-environments#organization-shared-environments)在选择器中以只读方式打开，因此请要求所有者从[管理设置](https://claude.ai/admin-settings)中的**云环境**页面更改其网络访问。

* 打开您的环境进行编辑，可以从[例程的表单](/docs/zh-CN/routines#environments-and-network-access)或从[环境选择器](/docs/zh-CN/cloud-environments#configure-your-environment)启动云会话。
* 在 **Edit environment** 对话框中，将 **Network access** 从 **Trusted** 更改为 **Custom**，然后将被阻止的域添加到 **Allowed domains**。每行输入一个域。勾选 **Also include default list of common package managers** 以将[默认允许列表](/docs/zh-CN/cloud-environments#default-allowed-domains)与您的自定义域保持在一起。如果您想要不受限制的访问，请改为选择 **Full**。
* 单击**保存更改**。下一次运行使用更新的允许列表。对于已打开的云会话，请参阅[网络访问更改何时到达现有会话](/docs/zh-CN/cloud-environments#network-access)。

有关访问级别和默认允许列表，请参阅[网络访问](/docs/zh-CN/cloud-environments#network-access)。本地 CLI 会话不受此策略影响。

<h3 id="the-proxy-refused-the-connection">
  代理拒绝了连接
</h3>

当 Claude 通过您在 `HTTPS_PROXY` 中设置的代理或相关[代理变量](/docs/zh-CN/network-config#environment-variables)读取[工件](/docs/zh-CN/artifacts)时，您会看到此消息。工件内容来自 `*.frame.claudeusercontent.com`，因此 Claude Code 首先向代理发送 `CONNECT` 请求，要求它打开到该主机的隧道。当代理拒绝时，没有任何东西到达主机，消息携带代理的 HTTP 状态：

```text theme={null}
artifact content fetch failed (proxy refused the connection: HTTP 407)
artifact content fetch failed (proxy refused the connection: HTTP 403)
the proxy refused the connection to the artifact's content host (HTTP 502)
```

状态是代理对 `CONNECT` 的答案。主机从未回答，因此每个状态指向不同的修复：

* `HTTP 407`：代理需要它没有获得的凭证。将它们放在代理 URL 中，如[基本身份验证](/docs/zh-CN/network-config#basic-authentication)所示。
* `HTTP 403`：代理拒绝隧道到 `*.frame.claudeusercontent.com`。要求运行代理的人允许该主机，[网络访问要求](/docs/zh-CN/network-config#network-access-requirements)列出了该主机。
* 任何其他状态，例如 `HTTP 502`：代理由于其自己的原因没有打开隧道，例如无法到达主机。在代理的日志中查找状态。
* `unreadable reply` 代替状态：代理地址处的任何东西都没有用 HTTP 状态行回答。检查地址是否是 HTTP 代理。

**要做什么：**

* 检查代理变量中的地址和凭证，如[代理配置](/docs/zh-CN/network-config#proxy-configuration)所述，然后从启动 Claude Code 的 shell 运行 `curl -x http://proxy.example.com:8080 -I https://api.anthropic.com`，使用您自己的代理 URL。在 Windows PowerShell 上，运行 `curl.exe`。如果此探针以相同方式失败，首先修复代理设置。如果成功，拒绝特定于工件主机。
* 如果您的网络让 Claude Code 直接到达工件主机，将 `.frame.claudeusercontent.com` 添加到 [`NO_PROXY`](/docs/zh-CN/network-config#environment-variables)。保持条目狭窄：更广泛的 `.claudeusercontent.com` 条目也会绕过 `bridge.claudeusercontent.com` 的代理，具有[IP 允许列表](/docs/zh-CN/network-config#organization-ip-allowlists-and-proxy-egress)的组织需要将其保留在代理上。

在 v2.1.238 之前，Claude Code 将拒绝的隧道报告为通用网络错误。

<h3 id="the-cloud-environments-service-returned-an-empty-or-unexpected-response">
  云环境服务返回了空的或意外的响应
</h3>

Claude Code 在多个点请求您的[云环境](/docs/zh-CN/cloud-environments)列表，例如当您从 CLI 创建云会话或运行 [`/remote-env`](/docs/zh-CN/cloud-environments#select-an-environment-from-the-cli) 时。当它无法读取服务器的答案时，它显示以下消息之一：

```text theme={null}
The cloud environments service returned an empty response (HTTP 200 with no body). This is usually temporary — try again in a moment.
The cloud environments service returned a response in an unexpected format (HTTP 200 with a non-JSON body). This is usually temporary — try again in a moment.
The cloud environments service returned a response in an unexpected format (HTTP 200 without a usable environments list). This is usually temporary — try again in a moment.
```

服务器接受了请求但用不是环境列表的正文回答：空、不是 JSON 或没有列表的 JSON。这通常伴随服务端中断，并自行清除。根据请求列表的表面，Claude Code 可能会添加前缀，例如 `/remote-env` 对话框中的 `couldn't list environments:`。

**要做什么：**

* 重试操作。Claude Code 每次都再次请求列表
* 如果消息继续出现，检查 [status.claude.com](https://status.claude.com) 是否有活跃事件

在 v2.1.236 之前，Claude Code 显示原始 JavaScript TypeError 而不是这些消息。

<h3 id="couldnt-reconnect-to-your-remote-control-session">
  无法重新连接到您的 Remote Control 会话
</h3>

```text theme={null}
Couldn't reconnect to your Remote Control session. Retry, or start a fresh session without --resume.
```

使用 `claude --resume` 或 `claude --continue` 恢复会重新连接到该对话中记录的[Remote Control](/docs/zh-CN/remote-control) 会话。此消息意味着重新连接因可能是临时的原因（例如网络中断或服务器错误）而失败，因此 Claude Code 无法确认远程会话是否仍然存在。您的本地会话继续运行而不使用 Remote Control。

**要做什么：**

* 运行 `/remote-control` 重试连接
* 使用 `claude --remote-control` 启动新会话以创建新的 Remote Control 会话
* 对于其他 Remote Control 启动消息，请参阅[Remote Control 故障排除](/docs/zh-CN/remote-control#troubleshooting)

如果服务器报告之前的会话已消失，您不会看到此消息。Claude Code 在其位置启动新会话或显示 [`Previous session is unavailable — run /remote-control to start a new one`](/docs/zh-CN/remote-control#previous-session-is-unavailable)。

<h3 id="sessions-ended-while-this-machine-was-offline">
  此机器离线时会话已结束
</h3>

Claude Code 在运行 [`claude remote-control`](/docs/zh-CN/remote-control#start-a-remote-control-session) 的终端中显示此消息，在您的机器离线足够长的时间后，服务器清理了您的机器正在服务的 Remote Control 环境。该环境中的会话已结束，您无法恢复它们。计数是已结束的会话数。

```text theme={null}
2 sessions ended while this machine was offline — the environment was cleaned up on the server and can't be resumed.
```

**要做什么：**

* 当 Claude Code 在此消息下列出保留的 worktrees 时，从它们中拾取任何未提交的工作
* 运行 `claude remote-control` 启动新环境

<h3 id="couldnt-share-the-transcript">
  无法共享成绩单
</h3>

在您同意从调查提示（例如[会话质量调查](/docs/zh-CN/data-usage#session-quality-surveys)）共享您的会话成绩单后，Claude Code 将其上传到 Anthropic，或在第三方提供商上、[Claude apps gateway](/docs/zh-CN/claude-apps-gateway) 会话上以及当没有 Anthropic 凭证可用时保存本地存档。此消息意味着共享未完成。

```text theme={null}
Couldn't share the transcript.
```

上传必须符合 8 MiB 限制。在长会话上，Claude Code 逐步删除共享的部分，最后一个请求的模型设置首先，然后是结构化对话和子代理成绩单，仅当没有减少的版本可以发送或网络或服务器错误停止上传时才显示此消息。当 Claude Code 保存本地存档时，消息意味着它无法写入存档。

**要做什么：**

* 运行 `/feedback` 发送成绩单并描述发生了什么。如果 `/feedback` 在您的环境中不可用，请参阅[报告错误](#report-an-error)
* 如果其他请求也失败，检查您的网络连接并查看[无法连接到 API](#unable-to-connect-to-api)

<h3 id="couldnt-send-feedback">
  无法发送反馈
</h3>

您从 [`/feedback`、`/bug` 或 `/share` 对话框](/docs/zh-CN/commands#all-commands)发送了报告，上传到 Anthropic 失败。对话框保留您的文本，以便您可以重试。

```text theme={null}
Couldn't send feedback (couldn't reach the service). If it keeps failing, you can file at https://github.com/anthropics/claude-code/issues instead.
```

前缀后的文本名称失败的内容：

* **`: not signed in. Run /login, then retry.`**：对话框仅在 Claude Code 打开时找到 Anthropic 凭证且到您发送时没有可用的凭证时上传。例如，您在此期间在此机器上注销，或您的登录不再可以刷新。
* **括号内容**：`(server returned <status>)` 是服务的响应代码；`(request timed out)` 和 `(couldn't reach the service)` 是网络故障。当 Claude Code 无法命名原因时，括号内容不存在。

在[反馈草稿队列](/docs/zh-CN/tools-reference#sendfeedback-tool-behavior)中，相同的故障以 `The draft is still queued. Try again later.` 结束，草稿保留在队列中以供另一次尝试。

**要做什么：**

* 对于未登录的措辞，运行 `/login` 并再次发送
* 否则，再次发送；如果其他请求也失败，检查您的网络连接并查看[无法连接到 API](#unable-to-connect-to-api)
* 如果它继续失败，在 [github.com/anthropics/claude-code/issues](https://github.com/anthropics/claude-code/issues) 提交报告，如消息所说

在 v2.1.281 之前，每次发送在 Remote Control **Stop** 或紧急跨会话消息在对话框打开时到达后都失败并显示此消息。在这些版本上，关闭对话框，重新打开它，然后再次发送。

<h2 id="request-errors">
  请求错误
</h2>

这些错误与您的请求内容有关。大多数来自 API 拒绝请求后的返回；少数是由 Claude Code 在发送任何请求之前在本地生成的。

<h3 id="prompt-is-too-long">
  提示词过长
</h3>

对话加上附加文件超过了模型的上下文窗口。

```text theme={null}
Prompt is too long
```

在交互式会话中，Claude Code 将此错误显示为：

```text theme={null}
Context limit reached · /compact or /clear to continue
```

当设置了 [`DISABLE_COMPACT`](/docs/zh-CN/env-vars) 时，该行仅显示 `/clear`。较长形式的错误，例如下面的压缩失败形式，保留 `Prompt is too long ·` 的措辞。在 `-p` 输出和会话记录中，文本保持为 `Prompt is too long`。

当您在[用户设置](/docs/zh-CN/settings-reference#autocompactenabled)中关闭自动压缩时，该行也会显示：

```text theme={null}
Context limit reached · /compact or /clear to continue · auto-compact is off · /config to turn it on
```

`/config` 中的**自动压缩**切换将 `autoCompactEnabled` 写入用户设置。该提示仅在 `/config` 更改会生效时出现。例如，当 [`DISABLE_AUTO_COMPACT`](/docs/zh-CN/env-vars) 或 [`DISABLE_COMPACT`](/docs/zh-CN/env-vars) 关闭自动压缩时，它不会出现。当更高优先级的作用域（如项目或托管设置）将 `autoCompactEnabled` 设置为 `false` 时，它也不会出现。在 v2.1.235 之前，该行没有自动压缩提示。

Amazon Bedrock 将此条件报告为 `Input is too long for requested model.`，Claude Code 以相同方式处理。在 v2.1.217 之前，Claude Code 不识别 Bedrock 的措辞，因此自动压缩从不在其上触发，`/compact` 失败并显示相同错误。

[Claude apps gateway](/docs/zh-CN/claude-apps-gateway-config#upstream-error-messages) 在云上游以提供商自己的错误形状拒绝请求时，将此条件报告为 `capability_rejected: prompt_too_long`。Claude Code 将该错误标识视为与 `Prompt is too long` 相同。在 v2.1.228 之前，Claude Code 不识别该错误标识，因此自动压缩不会在其上触发。

当自动压缩在此轮上运行并因底层错误（如不可用的模型或身份验证失败）而失败时，该消息在分隔符后命名该错误：

```text theme={null}
Prompt is too long · automatic compaction failed: <the underlying error>
```

首先解决命名的错误；在您这样做之前，`/compact` 会因相同错误而失败。在 v2.1.229 之前，失败的自动压缩显示 `Prompt is too long` 而不显示原因。

当自动压缩在此错误上运行时，它通常会总结您最早的交换并保留最新的。作为最后的手段，Claude Code 会以不同的方式总结：

* 当它无法总结任何完整交换时，Claude Code 会逐字保留您最新的提示词，并总结其前面的所有内容。
* 在这种情况下，当对话不以您的提示词结尾时，Claude Code 会改为总结整个对话。

当它将转发的内容不包含模型回复且您自己的文本少于约 1,000 个 token（如在超大粘贴后发送的短重试）时，Claude Code 会跳过此恢复。运行 `/clear` 以重新开始。在 v2.1.269 之前，每当压缩无法总结完整交换时就会失败，因此处于该状态的会话在每一轮都会再次遇到此错误。

单交换对话没有更早的轮次可总结。当自动压缩会在其上运行时，Claude Code 会跳过尝试并解释请求中填充的内容。当 API 在其错误中不报告 token 计数时，消息读取：

```text theme={null}
Prompt is too long · this conversation is a single exchange and cannot be compacted — the request size comes mostly from system prompt, tool definitions, or attachments.
```

当 API 在其错误中报告 token 计数时，Claude Code 将其与对话大小的自己估计进行比较，以判断请求的大部分是什么：对话自己的内容，还是 Claude Code 与其一起发送的系统提示词、工具定义和附件内容。当对话自己的内容是请求的大部分时，消息读取：

```text theme={null}
Prompt is too long · the request is ~<request tokens> tokens (limit <limit>) and this conversation's own content is most of it. A single-exchange conversation cannot be compacted; start with less content (smaller files or pasted text).
```

当请求的大部分在对话之外时，消息读取：

```text theme={null}
Prompt is too long · the request is ~<request tokens> tokens (limit <limit>) but this conversation is only ~<conversation tokens> tokens — the rest is system prompt, tool definitions, and attachment content. A single-exchange conversation cannot be compacted; reduce attached files/tools or start with less context.
```

在 v2.1.162 之前，Claude Code 仍会尝试压缩，并在失败时显示裸露的 `Prompt is too long`。

**要做什么：**

* 运行 `/compact` 以总结较早的轮次并释放空间，或运行 `/clear` 以重新开始。如果 `/compact` 回答 `Not enough messages to compact.`，则对话是单个交换，没有更早的内容可总结，因此空间由该单个提示词和 Claude Code 与每个请求一起发送的内容占用：运行 `/clear` 并使用较少的粘贴文本或较小的附件重新发送，或使用下面的步骤减少工具定义和记忆文件
* 运行 `/context` 以查看窗口消耗内容的分解：系统提示词、工具、记忆文件和消息
* 使用 `/mcp disable <name>` 禁用您未使用的 MCP 服务器，以从上下文中删除其工具定义
* 修剪大型 `CLAUDE.md` 记忆文件，或将说明移到仅在相关时加载的[路径范围规则](/docs/zh-CN/memory#path-specific-rules)中
* 自动压缩默认开启，通常可防止此错误。如果您在 `/config` 中或使用 [`DISABLE_AUTO_COMPACT`](/docs/zh-CN/env-vars) 关闭了它，请将其重新打开。如果您保持关闭，请在窗口填满之前自己运行 `/compact`。

有关上下文如何填满的交互式视图，请参阅[探索上下文窗口](/docs/zh-CN/context-window)。

<h3 id="context-exceeds-the-token-limit">
  上下文超过 token 限制
</h3>

当对话超过模型的上下文窗口时，`/context` 在其输出顶部显示此警告。在您释放空间之前，请求会失败并显示 [`Prompt is too long`](#prompt-is-too-long)。交互式会话将该错误显示为 `Context limit reached` 行。

```text theme={null}
Context exceeds the 200k-token limit by 94k tokens — run /compact or /clear to continue.
```

当您超过的限制是压缩窗口（如 1M 上下文模型上的 200K 边界）时，警告的读取方式不同。压缩窗口可以位于模型的上下文窗口下方，因此超过它的请求仍然可以成功。

```text theme={null}
Context is 94k tokens past the 200k-token compaction window — run /compact to reduce usage.
```

当您设置了 [`DISABLE_COMPACT`](/docs/zh-CN/env-vars) 时，两种形式都命名 `/clear` 而不是 `/compact`。

**要做什么：**

* 在多轮对话中，运行 `/compact` 以总结较早的轮次并释放空间。要重新开始，请运行 `/clear`
* 有关减少使用的更多方法，请参阅 [Prompt is too long](#prompt-is-too-long)

在 v2.1.216 之前，`/context` 显示超过 100% 的使用情况，没有警告行解释这意味着什么或如何恢复。

<h3 id="request-too-large">
  请求过大
</h3>

原始请求体在 token 化之前超过了 API 的 32MB 限制，通常是由于大型粘贴内容、工具结果或附件。此限制与[上下文窗口](#prompt-is-too-long)分开。

```text theme={null}
Request too large (max 32MB). Accumulated images and attachments in the conversation pushed the request over the limit. Run /compact, or double press esc to go back and remove attachments.
```

当请求直接进入 Claude API 且 API 本身拒绝了它时，Claude Code 会测量对话并根据恢复是否可行来表述消息。通过代理、网关或云提供商，您会获得一般消息。测量的形式：

* `Request too large (max 32MB; 20.1MB of about 33.4MB is images or documents).`：图像或文档将请求推过了限制。Claude Code 会在去除它们后重试。
* `Request too large for the API's 32MB request limit`：消息本身超过了限制，因此消息说 `compacting cannot make it fit`，Claude Code 不会重试。在[非交互模式](/docs/zh-CN/headless)中，消息告诉您减少输入或启动新会话。

在 v2.1.212 之前，具有足够累积图像的对话在每一轮都失败，显示 `Request too large (max 32MB). Double press esc to go back and try with a smaller file.` 在 v2.1.229 之前，Claude Code 为每次拒绝显示附件建议，即使压缩无法帮助。

**要做什么：**

* 如果消息说 `compacting cannot make it fit`，按 Esc 两次回退到添加大型内容的轮次之前，或运行 `/clear` 以重新开始
* 否则，运行 `/compact`，它会删除累积的图像和附件
* 按路径引用大型文件而不是粘贴其内容，以便 Claude 可以分块读取它们
* 对于图像，请参阅下面的[图像过大](#image-was-too-large)

<h3 id="image-was-too-large">
  图像过大
</h3>

粘贴或附加的图像超过了 API 的大小或尺寸限制。

```text theme={null}
Image was too large. Double press esc to go back and try again with a smaller image.
API Error: 400 ... image dimensions exceed max allowed size
```

Claude Code 用文本占位符替换无法处理的图像并重试，因此后续消息成功。在 2.1.142 之前的版本上，粘贴的图像可能保留在对话中，并在每个后续消息上重复相同的错误。要在这些版本上恢复，按 Esc 两次并回退到添加图像的轮次之前。

**要做什么：**

* 在粘贴之前调整图像大小。API 接受单个图像最长边最多 8000 像素的图像，或当上下文中有超过 20 张图像时最多 3000 像素。
* 拍摄相关区域的更紧密屏幕截图，而不是整个屏幕

<h3 id="unable-to-resize-image">
  无法调整图像大小
</h3>

Claude Code 无法在将附加图像发送到 API 之前对其进行缩小。

```text theme={null}
Unable to resize image — image processing is unavailable and dimensions could not be read from the file header. Please convert the image to PNG, JPEG, GIF, or WebP.
Unable to resize image — dimensions exceed the 2000x2000px limit and image processing failed. Please resize the image to reduce its pixel dimensions.
Unable to resize image (… raw, … base64). The image exceeds the … API limit and compression failed. Please resize the image manually or use a smaller image.
Unable to resize image — could not verify image dimensions are within the 2000x2000px API limit.
Unable to resize image — it is a CMYK JPEG, which Claude Code cannot decode, and at …px it is over the 2000x2000px limit, so it cannot be sent. Re-save it as an RGB PNG or JPEG and try again.
Unable to resize image — it is an animated WebP whose first frame Claude Code cannot decode, and at …px it is over the 2000x2000px limit, so it cannot be sent. Save its first frame as a PNG or JPEG and try again.
Unable to resize image — its pixels could not be decoded (the file may be damaged, or use an encoding Claude Code cannot read), and it is over the … API limit (… raw, … base64), so it cannot be sent. Re-save it as a PNG or JPEG and try again.
```

Claude Code 通常会自动调整大型图像的大小。这些错误意味着无法解码或调整图像大小以适应 API 限制。

**要做什么：**

* 如果消息要求您转换图像，请将其转换为 PNG、JPEG、GIF 或 WebP，然后再次附加。Claude Code 可以从文件头为这些格式验证尺寸，而无需解码图像。
* 如果消息报告尺寸或大小限制，请在附加之前将图像调整或重新压缩到该限制以下。
* 如果消息命名原因，例如 CMYK JPEG、动画 WebP 或可能损坏的文件，请以消息建议的格式重新保存图像并再次附加。

<h3 id="pdf-errors">
  PDF 错误
</h3>

您附加的 PDF 无法处理。消息在此处以非交互形式显示；在交互式会话中，它们会提示您按 Esc 两次并重试。

```text theme={null}
PDF too large (max 100 pages, 20MB). Try reading the file a different way (e.g., extract text with pdftotext).
PDF is password protected. Try using a CLI tool to extract or convert the PDF.
The PDF file was not valid. Try converting it to text first (e.g., pdftotext).
```

**要做什么：**

* 对于超大 PDF，要求 Claude 使用 Read 工具读取页面范围，而不是附加整个文件，或使用 `pdftotext` 等工具提取文本并按路径引用输出文件
* 对于受保护或无效的 PDF，删除密码或从其源应用程序重新导出文件，然后重试

当 Claude 使用 Read 工具从 PDF 读取页面范围时，读取可能失败，显示不同的消息：

```text theme={null}
pdftoppm is not installed. Install poppler-utils (e.g. `brew install poppler` or `apt-get install poppler-utils`) to enable PDF page rendering.
```

页面范围读取使用 `pdftoppm` 呈现页面。使用消息提供的命令安装 poppler-utils，或在其他平台上安装将 `pdftoppm` 放在您的 `PATH` 上的 poppler 构建版本。请参阅[Read 工具行为](/docs/zh-CN/tools-reference#read-tool-behavior)以了解哪些 PDF 按页面范围读取。

<h3 id="extra-inputs-are-not-permitted">
  不允许额外输入
</h3>

Claude Code 和 API 之间的代理或 LLM 网关删除了 `anthropic-beta` 请求头，因此 API 拒绝了依赖它的字段。

```text theme={null}
API Error: 400 ... Extra inputs are not permitted ... context_management
```

Claude Code 发送 `context_management` 等仅限测试版的字段，以及启用它们的 `anthropic-beta` 头。当网关转发正文但删除头时，API 会看到它不识别的字段。

**要做什么：**

* 配置您的网关以转发 `anthropic-beta` 头。有关网关必须转发的内容，请参阅[功能传递](/docs/zh-CN/llm-gateway-protocol#feature-pass-through)。
* 作为回退方案，在启动前设置 [`CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS=1`](/docs/zh-CN/env-vars)。[禁用预发布功能](/docs/zh-CN/llm-gateway-protocol#disable-pre-release-capabilities)涵盖确切范围。

<h3 id="tool-input-schema-is-invalid">
  工具输入 schema 无效
</h3>

请求中的工具声明了 `input_schema`，该 schema 未通过 API 的 JSON Schema 验证，因此 API 拒绝了整个请求。`tools.` 后的数字是失败工具在请求的工具列表中的位置，而不是您可以查找的名称。

```text theme={null}
API Error: 400 ... tools.N.custom.input_schema: JSON schema is invalid
API Error: 400 ... tools.N.custom.input_schema.properties: Property keys should match pattern '^[a-zA-Z0-9_.-]{1,64}$'
```

第一种形式意味着 schema 不是有效的 JSON Schema draft 2020-12。第二种意味着顶级属性名称与消息引用的模式不匹配。

Claude Code [在加载服务器的工具时排除其输入 schema 会失败此验证的 MCP 工具](/docs/zh-CN/mcp#tools-with-invalid-input-schemas)，因此请求通常永远不会包含一个。

在[禁用标志获取的部署](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching)上，或在标志从未到达的机器上，Claude Code 在服务器的日志中记录哪个工具会被拒绝，但仍然发送它，因此此错误仍然可能发生。

该错误也可能发生在其 schema 在 `$schema` 中声明 JSON Schema 方言（而不是 draft 2020-12）的工具上。Claude Code 不会根据 JSON Schema 元 schema 检查这些 schema，尽管顶级属性名称检查仍然适用。

在 v2.1.216 之前，没有部署运行排除检查。

**要做什么：**

* 如果您的 Claude Code 版本早于 v2.1.216，运行 `claude update`。
* 删除或[禁用](/docs/zh-CN/mcp#disable-a-server-without-removing-it)声明无效 schema 的 MCP 服务器。该错误仅按位置命名工具。在 v2.1.216 或更高版本上，检查每个服务器的日志，查找命名其输入 schema 会被拒绝的工具的行。如果没有日志命名一个，一次禁用一个服务器。
* 如果您维护服务器，请修复工具的 `input_schema`。schema 必须是有效的 JSON Schema，顶级属性名称必须为 1 到 64 个字符长，并仅使用 ASCII 字母和数字、`_`、`.` 和 `-`。请参阅[具有无效输入 schema 的工具](/docs/zh-CN/mcp#tools-with-invalid-input-schemas)。

<h3 id="tool-use-name-over-200-characters">
  tool\_use.name 超过 200 个字符
</h3>

对话历史中的工具调用携带的名称长度超过 API 在请求中接受的 200 个字符：

```text theme={null}
API Error: 400 ... tool_use.name: String should have at most 200 characters
```

Claude Code 在响应到达时以及加载保存的对话时将这样的名称截断为 200 个字符，因此该调用会失败并显示 [`No such tool available`](#no-such-tool-available) 工具错误，对话继续而不显示此 API 错误。

**要做什么：**

* 运行 `claude update`，然后恢复对话。更新的版本在加载会话记录时修复过长的名称，因此卡住的对话再次工作。

在 v2.1.281 之前，过长的名称保留在历史中，API 拒绝了重新发送对话的每个请求，包括 `/compact` 和 `--resume`，因此此错误重复，对话被卡住。

<h3 id="theres-an-issue-with-the-selected-model">
  所选模型存在问题
</h3>

配置的模型名称未被识别，或您的帐户无权访问它。从 v2.1.160 开始，尾部提示（此处以其交互形式显示）因使用入口而异。

```text theme={null}
There's an issue with the selected model (claude-...). It may not exist or you may not have access to it. Run /model to pick a different model.
```

**要做什么：**

* **交互式 CLI**：运行 `/model` 从您帐户可用的模型中选择。
* **非交互模式 (`-p`)**：使用有效的别名或 ID 传递 `--model`，或设置 [`ANTHROPIC_MODEL`](/docs/zh-CN/env-vars)。错误文本在此使用入口上显示 `Run --model`。
* **Agent SDK**：错误文本省略提示，因为模型是以编程方式设置的。在 TypeScript 中的 [`Options` 上设置 `model`](/docs/zh-CN/agent-sdk/typescript#options)，或在 Python 中设置 [`ClaudeAgentOptions(model=...)`](/docs/zh-CN/agent-sdk/python#claudeagentoptions)，并处理结构化的 `model_not_found` 错误以显示您自己的重试或模型选择器。
* 使用别名（如 `sonnet` 或 `opus`）而不是完整的版本化 ID。别名解析为维护的默认值，因此它们不会过时。请参阅[模型配置](/docs/zh-CN/model-config)。
* 如果错误的模型在 CLI 中不断返回，则某处设置了过时的 ID。按[优先级顺序](/docs/zh-CN/model-config#setting-your-model)检查您可以设置模型的位置，并删除过时的值。
* Claude Code 将过期的 claude.ai 登录报告为[登录过期](#login-expired)，而不是此错误。在 v2.1.206 之前，无法再刷新的过期登录对每个模型都失败，显示此错误；如果您在较旧版本上看到这种情况，请运行 `/login`。
* 对于 Google Cloud 的 Agent Platform 部署，请参阅 [Google Cloud 的 Agent Platform 故障排除](/docs/zh-CN/google-vertex-ai#troubleshooting)。

<h3 id="model-is-not-a-recognized-model-id">
  模型不是公认的模型 ID
</h3>

您传递给模型切换的字符串不是 Claude Code 可以用作模型的字符串，因此它拒绝了切换而不发送请求，会话保持其当前模型。您可以在通过 [Agent SDK](/docs/zh-CN/agent-sdk/typescript) `setModel()` 方法设置模型时获得此错误，通过运行 Claude Code CLI 的应用程序（如 [Desktop app](/docs/zh-CN/desktop)），或当您从通过 [Remote Control](/docs/zh-CN/remote-control) 连接的设备选择模型时。在 v2.1.200 之前，Claude Code 保存字符串并在下一个请求时失败，显示[所选模型存在问题](#theres-an-issue-with-the-selected-model)。

```text theme={null}
Model "Sonnet5" is not a recognized model id. Did you mean 'claude-sonnet-5'?
```

在此示例中，应用程序发送了显示名称 `Sonnet 5`，消息重复时不带其空格。尾部提示命名最接近的匹配别名或模型 ID。当没有足够接近的内容时，它读取 `Run /model to see available models.`。在 [Desktop app](/docs/zh-CN/desktop) 启动的会话中，无匹配提示读取 `Switch to a different model.`

当您通过 Agent SDK 或在 Anthropic API 上的应用程序切换时，只有无法成为模型 ID 的字符串（如显示名称或空字符串）会获得此错误。

当您从 Remote Control 设备选择模型时，Claude Code 在本地检查字符串。任何不是模型别名、Claude Code 列出或您配置的模型，或以 `claude-` 开头的 ID 的字符串都会获得此错误，包括拼写错误的 ID（如 `claud-sonnet-5`）。在 v2.1.260 之前，此检查不涵盖 Remote Control 选择，因此无法识别的字符串被应用，下一个请求失败。

**要做什么：**

* 运行 `/model` 不带参数以打开选择器并从您帐户可用的模型中选择，然后传递那里显示的别名或 ID
* 如果您使用了较新 Claude Code 版本支持的别名，运行 `claude update`，或传递模型的完整 ID。服务器仍然可能需要该模型的最低 Claude Code 版本；请参阅 [Claude Code 不支持此模型](#claude-code-does-not-support-this-model)。
* v2.1.200 之前保存的模型不会被此检查修复。如果过时的值不断返回，请从[设置您的模型](/docs/zh-CN/model-config#setting-your-model)下列出的位置删除它。
* 在 Anthropic API 以外的任何提供商上，或在网关或自定义 `ANTHROPIC_BASE_URL` 后面，只有空字符串会获得此错误。Claude Code 仍然可以在请求时写入[无法识别的模型诊断行](#unrecognized-model-id-on-a-request)，在每个提供商上。

<h3 id="model-not-found">
  模型未找到
</h3>

您使用名称切换到模型，Claude Code 无法确认存在具有该名称的模型。当名称不是[模型别名](/docs/zh-CN/model-config#model-aliases)或 Claude Code 在本地接受的另一种拼写时，Claude Code 使用最小 API 请求验证它，此错误通常是您的 API 端点的答案。使用 `/model <name>` 时，无法成为模型 ID 的名称（如包含空格的名称）会获得相同的消息。

```text theme={null}
Model 'claude-opus-9' not found
```

在具有提供商特定模型 ID 的提供商上，消息可能会添加 `Try '...' instead` 建议，该建议命名您提供商的备用模型 ID。

**要做什么：**

* 运行 `/model` 不带参数并从您帐户可用的模型中选择，或使用[模型别名](/docs/zh-CN/model-config#model-aliases)（如 `sonnet`），它解析为维护的默认值
* 如果您输入了完整 ID，请根据您提供商的模型目录检查它。新推出的模型可能在 Anthropic API 上可用，但您的提供商或地区尚未提供。
* 在 Agent SDK 中，`setModel()` 失败，显示此消息，会话继续在其前一个模型上运行。在 TypeScript SDK 中，调用 [`supportedModels()`](/docs/zh-CN/agent-sdk/typescript#query-object) 以列出您可以切换到的模型。
* 在 v2.1.265 之前，`/model` 也以此错误拒绝了 `opusplan[1m]` 别名拼写。在这些版本上，更新 Claude Code，或在[设置](/docs/zh-CN/model-config#setting-your-model)中或使用 `--model` 设置模型。

<h3 id="couldnt-confirm-model-with-the-api">
  无法通过 API 确认模型
</h3>

您通过 [Agent SDK](/docs/zh-CN/agent-sdk/typescript) `setModel()` 方法或运行 Claude Code CLI 的应用程序（如 [Desktop app](/docs/zh-CN/desktop)）切换了模型，向您的 API 端点确认模型 ID 的请求在五秒内没有得到答复。会话保持其当前模型。

```text theme={null}
Couldn't confirm model "claude-sonnet-5" with the API. Try again, or run /model to see available models.
```

在 [Desktop app](/docs/zh-CN/desktop) 启动的会话中，消息在 `Try again.` 处结束。

**要做什么：**

* 再次切换到模型
* 如果切换继续失败，检查 Claude Code 是否可以到达您的 API 端点；请参阅[网络和连接错误](#network-and-connection-errors)

<h3 id="api-error-model-not-changed">
  检查选择的模型时出现 API 错误
</h3>

您使用 `/model <name>` 选择了模型，或连接到会话的应用程序请求了切换。API 拒绝了 Claude Code 发送以验证模型的最小请求，原因没有自己的条目，例如速率限制或服务器错误。会话保持其当前模型，消息以说明这一点结尾：

```text theme={null}
API error: 429 <the server's explanation> · model not changed
```

消息的中间是 HTTP 状态和服务器自己的解释。

**要做什么：**

* 根据服务器的解释采取行动；对于速率限制或 5xx 状态，等待并再次选择模型
* 具有自己措辞的拒绝由周围条目涵盖，例如[模型未找到](#model-not-found)和[模型受您的组织设置限制](#model-is-restricted-by-your-organizations-settings)

<h3 id="claude-opus-is-not-available-with-the-claude-pro-plan">
  Claude Opus 在 Claude Pro 计划中不可用
</h3>

您的活跃订阅计划不包括您选择的模型。

```text theme={null}
Claude Opus is not available with the Claude Pro plan. If you have updated your subscription plan recently, run /logout and /login for the plan to take effect.
```

在 Claude Desktop app 运行的会话中，消息会提示 `sign out and sign in again`，而不是命名命令。

**要做什么：**

* 运行 `/model` 并选择您的计划包括的模型
* 如果您最近升级了计划但仍然看到这个，运行 `/logout` 然后 `/login`。存储的令牌反映您登录时的计划，因此在现有会话中升级 claude.ai 不会生效，直到您重新进行身份验证。
* 有关每个计划包括哪些模型，请参阅 [claude.com/pricing](https://claude.com/pricing)

<h3 id="claude-code-does-not-support-this-model">
  Claude Code 不支持此模型
</h3>

API 因您的 Claude Code 版本低于所需最低版本而拒绝了请求，返回 400。要么您选择的模型需要较新版本（服务器按模型检查），要么您的组织政策需要一个。400 携带错误代码 `claude_code_version_too_old`，消息说明适用的最低版本。

```text theme={null}
API Error: 400 Claude Code 2.1.219 does not support this model; version 2.1.255 or newer is required. Run 'claude update', or update the Claude desktop app, then try again.
```

组织政策措辞读取：

```text theme={null}
API Error: 400 Claude Code 2.1.240 is older than the minimum version required by your organization's policy. Run 'claude update', or update the Claude desktop app, to continue.
```

发出请求的 Claude Code 二进制文件报告的版本是 API 检查的版本。

**要做什么：**

更新该二进制文件，然后启动新会话。二进制文件的来源决定了如何更新，除了在[自托管环境](/docs/zh-CN/self-hosted-environments-deploy#pin-the-version)中：

| 发出请求的二进制文件 | 如何更新它 |
| :- | :- |
| 您安装的 Claude Code | 运行 `claude update` |
| Claude desktop app | 更新应用 |
| [VS Code extension](/docs/zh-CN/vs-code) 捆绑的二进制文件 | 更新扩展 |
| Agent SDK 包捆绑的二进制文件 | [升级 SDK 包](/docs/zh-CN/agent-sdk/hosting#runtime-dependencies)，然后重启您的应用程序。在[编译的单文件可执行文件](/docs/zh-CN/agent-sdk/typescript#compile-to-a-single-executable)中，重新构建它 |

* 如果您在[稳定版发布渠道](/docs/zh-CN/setup#configure-release-channel)上运行 `claude update`，它不会让您越过最新的稳定版本，而该版本仍可能低于所需的最低版本。请切换到 latest 渠道，然后再次更新。如果您的组织通过[托管设置](/docs/zh-CN/managed-settings)固定了您的渠道或版本，请让您的管理员进行更改
* 对于按模型措辞，您可以通过切换到另一个模型来继续在当前会话中工作：在 CLI 中运行 `/model`，在流式输入模式下的 TypeScript SDK 的 `Query` 对象上调用 [`setModel()`](/docs/zh-CN/agent-sdk/typescript#query-object)，或在 Python SDK 的 `ClaudeSDKClient` 上调用 [`set_model()`](/docs/zh-CN/agent-sdk/python#claudesdkclient)
* 对于组织政策措辞，在继续之前更新

<h3 id="model-is-restricted-by-your-organizations-settings">
  模型受您的组织设置限制
</h3>

您的组织管理员在 claude.ai 管理控制台中禁用了此模型，或托管设置中的 [`availableModels`](/docs/zh-CN/model-config#restrict-model-selection) 允许列表或 [`deniedModels`](/docs/zh-CN/model-config#block-specific-models-or-versions) 列表排除了它。当 `--model`、`ANTHROPIC_MODEL` 或 `model` 设置指定了受限制的模型时，通知在启动时出现，并命名会话改用的模型。如果托管设置没有为会话留下允许的模型，请参阅[托管设置阻止默认模型](#managed-settings-block-the-default-model)。在管理员于 claude.ai 管理控制台中禁用会话正在运行的模型之后，替换通知也可能在会话中途出现。

```text theme={null}
Model "claude-opus-4-8" is restricted by your organization's settings. Using claude-sonnet-4-6 instead.
```

为受限制的模型键入 `/model <name>` 被拒绝，会话保持其当前模型。对于在管理控制台中禁用的模型，拒绝读取 `Model '<name>' is restricted by your organization's settings. Run /model to choose a different model.`。对于托管设置排除的模型，它读取 `Model '<name>' is not available. Your organization restricts model selection.`

以 Agent、skill 或命令名称为前缀的通知意味着限制适用于该[子代理的请求模型](/docs/zh-CN/sub-agents#choose-a-model)：子代理在替换模型上运行，您的会话模型保持不变。在 v2.1.223 之前，Claude Code 仅为使用 Agent 工具启动的子代理显示通知。

Claude Code 将模型族别名（`opus`、`sonnet`、`haiku` 或 `fable` 之一）视为对该族的请求，而不是对其最新版本的请求。在 Anthropic API 和 [Claude Platform on AWS](/docs/zh-CN/claude-platform-on-aws) 上，受限制的族别名解析为您的组织的设置允许的族的最新版本，替换通知命名该版本。Claude Code 仅当族的每个版本都受限制时才拒绝 `/model <alias>`。在 v2.1.205 之前，族别名仅基于其最新版本被替换或拒绝，即使同一族的较旧版本被允许。

**要做什么：**

* 运行 `/model` 从您的组织允许的模型中选择。受限制的模型从选择器中隐藏。
* 如果受限制的模型在 `--model`、`ANTHROPIC_MODEL`、设置文件的 `model` 字段或[子代理](/docs/zh-CN/sub-agents#choose-a-model)、skill 或命令的 `model` frontmatter 中设置，删除或更新该值，以便通知不会再次出现
* 如果您需要访问受限制的模型，请要求您的组织管理员启用它。请参阅[组织模型限制](/docs/zh-CN/model-config#organization-model-restrictions)。

<h3 id="cant-switch-to-the-default-model">
  无法切换到默认模型
</h3>

您选择了默认模型，例如通过在 `/model` 选择器中选择默认行或键入 `/model default`。Claude Code 拒绝了切换，因此会话保持其当前模型。

```text theme={null}
Can't switch to the default model: your organization's managed settings block it (claude-opus-4-6) in "deniedModels", and none of the models they allow can be used as the default instead. Ask your administrator to update "deniedModels" or "availableModels".
```

冒号后的措辞命名阻止切换的内容：

* **`your organization's managed settings block it ... in "deniedModels"`**：托管拒绝列表阻止默认选项解析到的模型
* **`your organization allows only the models listed in "availableModels"`**：托管 [`availableModels`](/docs/zh-CN/model-config#restrict-model-selection) 允许列表，其 [`availableModelsMatch`](/docs/zh-CN/settings-reference#availablemodelsmatch) 设置为 `"exact"`，遗漏了默认选项解析到的模型
* **`Claude Code couldn't read your organization's managed settings to check which models they allow`**：[托管设置](/docs/zh-CN/managed-settings)无法读取，Claude Code 拒绝切换而不是未检查地应用它

**要做什么：**

* 对于 [`deniedModels`](/docs/zh-CN/settings-reference#deniedmodels) 和 `availableModels` 措辞，运行 `/model` 并按名称选择您的组织允许的模型
* 要求您的管理员更新消息命名的托管设置
* 对于 `couldn't read` 措辞，重启 Claude Code；如果它继续发生，要求您的管理员检查托管设置

如果会话改为在这些托管设置下以 `Claude Code can't start` 消息启动失败，请参阅[托管设置阻止默认模型](#managed-settings-block-the-default-model)。

<h3 id="model-switch-was-blocked-by-a-premodelswitch-hook">
  模型切换被 PreModelSwitch hook 阻止
</h3>

[PreModelSwitch hook](/docs/zh-CN/hooks#premodelswitch) 没有批准您或客户端请求的模型切换，因此会话保持其当前模型。当切换来自 [Agent SDK](/docs/zh-CN/agent-sdk/overview) 主机或 [Remote Control](/docs/zh-CN/remote-control) 而不是您键入的命令时，消息读取 `Model switch blocked by a PreModelSwitch hook` 而不命名目标模型。

```text theme={null}
Model switch to Opus 4.6 was blocked by a PreModelSwitch hook: Opus 4.6 is retired for this project. Use a newer model.
```

冒号后的原因说明拒绝切换的原因：

* **hook 写入的原因**：PreModelSwitch hook 在[拒绝切换或要求确认](/docs/zh-CN/hooks#premodelswitch-decision-control)时提供了该原因。解决它要求的内容，或选择您的 hook 允许的模型。
* **`PreModelSwitch hook <name> did not respond before its timeout`**：在其[超时](/docs/zh-CN/hooks#timeouts)之前不回答的 hook 阻止切换。修复挂起的命令或提高该 hook 的 `timeout`，然后再次切换。
* **`confirmation required, and this session cannot ask`**：hook 回答 `ask` 而没有原因，控制请求无法显示确认提示。[`-p` 运行](/docs/zh-CN/headless)中的 `/model` 命令以原因后的 `(run /model interactively to confirm)` 报告相同条件。从交互式会话进行切换，或更改 hook 对此模型的决定。
* **`so organization-managed PreModelSwitch hooks could not be checked`**：Claude Code 无法判断您的组织的[托管插件](/docs/zh-CN/settings-reference#enabledplugins)提供哪些 PreModelSwitch hook，例如因为托管插件加载失败。这些 hook 之一可能阻止切换，因此 Claude Code 拒绝而不是应用未检查的切换。原因的开头命名失败的内容。Claude Code 在每次切换尝试时重新检查，因此已清除的失败不再阻止；如果它继续失败，运行 `claude --debug` 并再次切换以捕获详细信息，然后修复插件或要求您的管理员修复它。
* **`a PreModelSwitch hook failed before answering`** 或 **`PreModelSwitch hooks were cancelled (the control stream closed) before answering`**：hook 运行在没有判决的情况下结束，Claude Code 不将其视为批准。运行 `claude --debug` 以查看失败的内容，然后再次切换。

在 v2.1.260 之前，托管插件拒绝读取 `plugin hooks could not be loaded, so PreModelSwitch hooks could not be checked; see the debug log`。Claude Code 重试了一次插件加载，然后在会话中拒绝了后来的切换，即使您的组织没有管理任何插件。在这些版本上重启会话以再次运行插件加载。

<h3 id="couldnt-save-it-as-your-default">
  无法将其保存为您的默认值
</h3>

您选择了一个模型以保存为您的默认值，例如使用 `/model <name>` 或 `/model` 选择器中的 `Enter`，Claude Code 无法将选择写入您的用户设置文件 `~/.claude/settings.json`。切换本身已应用，因此当前会话在您选择的模型上运行，但您的默认值保持不变，下一个会话在旧值上启动。

```text theme={null}
Set model to Fable 5.1 for this session only · couldn't save it as your default: ~/.claude/settings.json can't be written (EROFS)
```

文件路径后的原因说明失败的内容：

* **`can't be written (<code>)`**：写入失败，显示括号中的操作系统错误代码，如 `EROFS`（当文件或其链接到的文件位于拒绝写入的文件系统上时）。使文件可写并再次切换。如果另一个工具生成文件，请在该工具中设置 `model` 键；请参阅[您在 Claude Code 中所做的更改在新会话中丢失](/docs/zh-CN/settings#a-change-you-made-in-claude-code-is-lost-in-new-sessions)。
* **`isn't valid JSON`**：磁盘上的文件无法解析，Claude Code 保持不动而不是覆盖它无法读回的内容。修复语法错误，然后再次切换；请参阅[修复损坏的设置文件](/docs/zh-CN/settings#fix-a-broken-settings-file)。

以 `couldn't confirm it was saved as your default (~/.claude/settings.json is still being written)` 结尾的通知意味着写入在三秒后未完成。它在后台继续，因此默认值可能仍然被保存；检查您的下一个会话启动的模型，或再次运行 `/model <name>`。

在 v2.1.265 之前，即使写入失败，通知也会说模型已 `saved as your default for new sessions`。

<h3 id="advisor-is-less-capable-than-the-current-main-model">
  Advisor 的能力低于当前主模型
</h3>

您的 [advisor 模型](/docs/zh-CN/advisor)排名低于会话的主模型，因此 Claude Code 保留该选择，但不会将 advisor 附加到主模型的请求上。

```text theme={null}
Advisor set to Opus 4.8
Note: Opus 4.8 is less capable than the current main model (Sonnet 5.5), so the advisor will not activate. Choose a more capable advisor, or switch to a smaller main model.
```

其他消息报告相同的情况：

* 在交互式会话中，通知显示 `Advisor will not activate on the main model (advisor is less capable); subagents may still use it and may use more tokens · /advisor`。
* 使用 `--advisor` 标志启动时，警告显示 `"<advisor>" cannot advise "<main model>" (the advisor must be at least as capable as the main model). The advisor will not be used for the main model.`，会话仍会启动。

**要做什么：**

* 选择排名更高的 advisor 或排名更低的主模型。[选择 advisor 模型](/docs/zh-CN/advisor#choose-an-advisor-model)展示了排名，并列出每个主模型可接受的 advisor。
* 如果您希望该 advisor 能够为其模型提供建议的[子代理](/docs/zh-CN/sub-agents)继续使用它，请保留 advisor 设置

在 v2.1.287 之前，Claude Code 对若干组合的排名不同。它会在 Sonnet 5.5 advisor 搭配 Opus 4.7 或 Opus 4.8 主模型时显示此提示，而现在接受该组合。它还会附加一些现在会产生此提示的 advisor，例如 Opus 4.8 advisor 搭配 Sonnet 5.5 主模型。

<h3 id="thinking-type-enabled-is-not-supported-for-this-model">
  thinking.type.enabled 此模型不支持
</h3>

您的 Claude Code 版本早于所选模型的最低版本。CLI 发送了模型不再接受的思考配置。

```text theme={null}
API Error: 400 ... "thinking.type.enabled" is not supported for this model. Use "thinking.type.adaptive" and "output_config.effort" to control thinking behavior.
```

**要做什么：**

* 运行 `claude update` 并重启 Claude Code。Opus 4.7 需要 v2.1.111 或更高版本。Opus 4.8 需要 v2.1.154 或更高版本。Sonnet 5 需要 v2.1.197 或更高版本。Opus 5 需要 v2.1.219 或更高版本。Opus 5.5 需要 v2.1.280 或更高版本。Sonnet 5.5 需要 v2.1.284 或更高版本
* 在[稳定版发布渠道](/docs/zh-CN/setup#configure-release-channel)上，更新不会让您越过最新的稳定版本，而该版本仍可能早于这些版本。请切换到 latest 渠道，然后更新
* 如果您无法升级，运行 `/model` 并选择 Opus 4.6 或 Sonnet 4.6
* 如果您在 [Agent SDK](/docs/zh-CN/agent-sdk/overview) 中遇到这个，升级 SDK 包。Opus 4.8 需要 TypeScript SDK v0.3.154 或更高版本和 Python SDK v0.2.88 或更高版本。Sonnet 5 需要 TypeScript SDK v0.3.197 或更高版本。Opus 5 需要 TypeScript SDK v0.3.219 或更高版本。Opus 5.5 需要 TypeScript SDK v0.3.280 或更高版本。Sonnet 5.5 需要 TypeScript SDK v0.3.284 或更高版本

<h3 id="effort-isnt-available-with-thinking-turned-off">
  关闭思考时 effort 不可用
</h3>

您关闭了[扩展思考](/docs/zh-CN/model-config#extended-thinking)并以高于 `high` 的 [effort 级别](/docs/zh-CN/model-config#adjust-effort-level)运行。模型不接受该组合，因此 API 拒绝了请求。

```text theme={null}
API Error: Effort 'xhigh' isn't available with thinking turned off on this model · run /effort high to continue, or turn thinking back on (unset MAX_THINKING_TOKENS=0)
```

`·` 后的提示因会话而异：在非交互式会话中，它读取 `use --effort high (or the effortLevel setting)`，在 Claude Desktop app 运行的会话中，它读取 `you can lower effort to High`。

**要做什么：**

* [降低 effort 级别](/docs/zh-CN/model-config#set-the-effort-level)到 `high` 或以下。
* 重新打开思考，例如通过取消设置 [`MAX_THINKING_TOKENS`](/docs/zh-CN/env-vars) 或从您的设置中删除 [`"alwaysThinkingEnabled": false`](/docs/zh-CN/settings-reference#alwaysthinkingenabled)。

在 v2.1.242 之前，Claude Code 显示了 API 自己的消息：`API Error: 400 output_config.effort 'xhigh' is not supported when thinking is disabled on this model. Use effort 'high' or below, or enable thinking.` 在 v2.1.251 之前，Claude Code 以您设置的 effort 级别发送请求，因此 Opus 5 拒绝了关闭思考时高于 `high` 的每个请求。Claude Code 现在向它知道拒绝该组合的模型（如 Opus 5）改为发送 effort `high`。

<h3 id="thinking-budget-exceeds-output-limit">
  思考预算超过输出限制
</h3>

配置的扩展思考预算超过最大响应长度，因此实际答案没有剩余空间。

```text theme={null}
API Error: 400 ... max_tokens must be greater than thinking.budget_tokens
```

**要做什么：**

* 将 [`CLAUDE_CODE_MAX_OUTPUT_TOKENS`](/docs/zh-CN/env-vars) 提高到思考预算以上
* 请参阅[扩展思考](/docs/zh-CN/model-config#extended-thinking)以了解预算如何与输出长度交互

<h3 id="tool-use-or-thinking-block-mismatch">
  工具使用或思考块不匹配
</h3>

对话历史以不一致的状态到达 API。

```text theme={null}
API Error: 400 due to tool use concurrency issues. Run /rewind to recover the conversation.
API Error: 400 orphaned tool_result in conversation history. Run /rewind to recover the conversation.
API Error: 400 duplicate tool_use ID in conversation history. Run /rewind to recover the conversation.
API Error: 400 ... unexpected `tool_use_id` found in `tool_result` blocks
API Error: 400 ... thinking blocks ... cannot be modified
```

所有变体意味着相同的事情：历史中 `tool_use`、`tool_result` 和 `thinking` 块的序列不再与 API 期望的匹配。

**要做什么：**

* 如果您使用 Opus 4.7 或 Opus 4.8，首先运行 `claude update`。v2.1.156 之前的版本可能在正常工具使用期间触发此错误，`/rewind` 不会清除它。
* 运行 `/rewind`，或按 Esc 两次，回退到损坏轮次之前的检查点并从那里继续。请参阅[检查点](/docs/zh-CN/checkpointing)以了解如何创建和恢复检查点。

<h3 id="invalid-data-in-redacted-thinking-block">
  redacted\_thinking 块中的数据无效
</h3>

API 拒绝了请求，返回 400，因为它无法接受对话历史中较早轮次携带的 `redacted_thinking` 块。

```text theme={null}
API Error: 400 ... Invalid `data` in `redacted_thinking` block
```

Claude Code 将对话的较早思考排除在请求之外并重试一次，因此会话继续而不显示错误。在 v2.1.282 之前，Claude Code 保留被拒绝的块，每个后来的轮次都以相同错误失败。

**要做什么：**

* 如果您在 v2.1.281 或更早版本上，每一轮都失败，显示此错误，运行 `claude update` 并恢复会话
* 如果错误持续，运行 `/clear` 以启动不携带该块的对话

<h3 id="unsupported-tool-content-removed">
  删除了不支持的工具内容
</h3>

当 Claude Code 直接连接到 Anthropic API 并加载或预览保存的会话时，它删除 Anthropic API 不接受的工具内容，并在两个思考块之间被删除内容所在的位置留下此行：

```text theme={null}
[Unsupported tool content removed]
```

当 Anthropic API 以外的东西以 API 的格式回答时，这样的内容到达会话文件，通常是通过 [`ANTHROPIC_BASE_URL`](/docs/zh-CN/env-vars) 设置的第三方代理，它转换另一个提供商的工具调用。Claude Code 仅在会话直接连接到 Anthropic API 时删除它，并在会话通过代理或在另一个提供商上运行时按原样加载保存的历史。在 v2.1.246 之前，Claude Code 将工具使用及其结果发送回 API，恢复会话的每一轮都失败，显示 400 错误，如 `messages.1.content.0.server_tool_use.name: Input should be 'web_search', 'web_fetch', ...`。

**要做什么：**

* 当您看到占位符行时，无需任何操作。会话在没有已删除内容的情况下继续。
* 如果恢复会话的每一轮都失败，显示 400 错误，运行 `claude update` 并再次恢复会话。v2.1.246 之前的版本不删除内容。

<h3 id="role-system-must-precede-an-assistant-message">
  role 'system' 必须在 'assistant' 消息之前
</h3>

API 拒绝了请求，返回 400，因为系统消息位于对话中它不接受的位置：

```text theme={null}
API Error: 400 messages.6: role 'system' must precede an 'assistant' message or end the array; ...
```

Claude Code 将其一些提醒和附件文本作为系统消息发送到对话中。当 API 拒绝其中一条的位置时，Claude Code 重试请求一次，将该文本作为普通用户消息发送。API 的同类位置措辞，如 `use the top-level 'system' parameter for the initial system prompt`，获得相同的恢复。

当错误确实出现时，被拒绝的系统消息不是 Claude Code 可以删除的。这通常意味着 Claude Code 和 API 之间的代理或 [LLM gateway](/docs/zh-CN/llm-gateway) 添加了自己的系统消息。

**要做什么：**

* 如果错误在通过 [`ANTHROPIC_BASE_URL`](/docs/zh-CN/env-vars) 配置的代理或网关后的每一轮上重复，不使用代理进行连接以确认来源，并向运营它的人报告错误
* 运行 `/clear` 以启动新对话。如果错误也在那里返回，原因在请求路径上，而不在保存的对话中。

在 v2.1.280 之前，Claude Code 不识别此措辞，因此当被拒绝的系统消息是 Claude Code 本身发送的时，错误也出现，对话的每个后来轮次都以相同方式失败。

<h3 id="invalid-encrypted-content-in-search-result-block">
  search\_result 块中的 encrypted\_content 无效
</h3>

API 拒绝了请求，返回 400，因为对话历史包含它无法解密的托管网络搜索内容。措辞命名它无法读取的字段：

```text theme={null}
API Error: 400 ... Invalid `encrypted_content` in `search_result` block
API Error: 400 ... Invalid `encrypted_index` in `text` block
API Error: 400 ... Failed to decrypt web search result content
API Error: 400 ... Invalid `encrypted_stdout` in `encrypted_code_execution_result` block
```

来自 API 的托管[网络搜索工具](https://platform.claude.com/docs/en/agents-and-tools/tool-use/web-search-tool)的结果携带只有 API 可以读取的加密字段。`encrypted_stdout` 措辞命名读取这样的结果的托管代码执行程序的输出，API 也会对其加密。API 拒绝重放它无法解密的内容的请求，如为不同组织生成的内容。

Claude Code 自己的 [WebSearch 工具](/docs/zh-CN/tools-reference#websearch-tool-behavior)将搜索结果记录为纯文本，因此这些块通常通过自己运行了托管网络搜索的代理或 [LLM gateway](/docs/zh-CN/llm-gateway) 到达对话。

对于三个网络搜索措辞，Claude Code 将搜索调用、结果和引用排除在它发送的内容之外并重试请求一次，因此会话继续而不显示错误。`encrypted_stdout` 措辞没有这样的恢复，因此该消息仍然会显示给您。在 v2.1.282 之前，Claude Code 也保留了被拒绝的网络搜索块，每个后来的轮次和 `/compact` 都以相同方式失败。

**要做什么：**

* 如果您在 v2.1.281 或更早版本上，每一轮都失败，显示网络搜索措辞之一，运行 `claude update` 并恢复会话
* 如果错误持续，或消息命名 `encrypted_stdout`，运行 `/rewind` 回退到添加内容的轮次之前的检查点，或运行 `/clear` 启动不携带它的对话
* 如果您在代理或网关后运行 Claude Code，向运营它的人报告错误

<h3 id="usage-policy-refusal">
  使用政策拒绝
</h3>

API 拒绝了响应，因为对话中的内容触发了[使用政策](https://www.anthropic.com/legal/aup)检查。

如果消息包含 `` Details: `[reasoning_extraction]` `` 行，请参阅[保护措施标记了索取 Claude 推理过程的请求](#safeguards-flagged-a-request-for-claudes-reasoning)。

消息包括请求 ID 和消息 ID，如果您认为拒绝不正确，可以将其提供给支持人员。

```text theme={null}
API Error: Opus 4.6 can't help with this. Start a new session to continue.

Send feedback with /feedback or learn more: https://www.anthropic.com/legal/aup
```

消息命名拒绝的模型，或当没有记录模型时命名 `Claude`。

检查评估完整对话，而不仅仅是您的最新提示词，因此在同一会话中发送新消息通常会重新触发相同的拒绝。使用 `--continue` 或 `--resume` 退出并重新打开会话后也是如此，因为磁盘上的会话记录仍然包含触发内容。在 [Amazon Bedrock](/docs/zh-CN/amazon-bedrock)、[Google Cloud 的 Agent Platform](/docs/zh-CN/google-vertex-ai) 和 [Microsoft Foundry](/docs/zh-CN/microsoft-foundry) 上，此消息也涵盖模型的安全措施标记为网络安全主题的请求。请参阅[安全措施标记了网络安全主题](#safety-measures-flagged-a-cybersecurity-topic)。

在 v2.1.219 之前，消息读取 `Claude Code is unable to respond to this request, which appears to violate our Usage Policy (https://www.anthropic.com/legal/aup). Please double press esc to edit your last message or start a new session for Claude Code to assist with a different task.`

**要做什么：**

* 按 Esc 两次或运行 `/rewind` 回退到触发拒绝的轮次之前的检查点，然后重新表述或采取不同的方法。请参阅[检查点](/docs/zh-CN/checkpointing)。
* 如果您无法识别哪个轮次导致了它，运行 `/clear` 在同一项目中启动新对话。您之前的对话保留在磁盘上，并在 `/resume` 中保持可用。
* 在[非交互模式](/docs/zh-CN/headless)(`-p`) 中，由于无法回退，请在不带 `--continue` 的新会话中使用重新表述的提示词重试。政策检查因模型而异，因此使用 `--model` 切换到不同的模型在某些情况下也可能解决拒绝。

<h3 id="safety-measures-flagged-a-cybersecurity-topic">
  安全措施标记了网络安全主题
</h3>

模型的安全措施将对话中的内容标记为网络安全主题。消息命名标记请求的模型：

```text theme={null}
API Error: Opus 4.8's safeguards flagged this message. Our intentionally broad safeguards allow us to deliver more capabilities faster, but can sometimes flag legitimate cybersecurity work. Apply to the Cyber Verification Program to reduce these interruptions. Send feedback with /feedback or learn more: https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude
```

如果消息包含 `` Details: `[reasoning_extraction]` `` 行，请参阅[保护措施标记了索取 Claude 推理过程的请求](#safeguards-flagged-a-request-for-claudes-reasoning)。

此消息链接到[网络安全验证计划](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude)，该计划为合法网络安全工作授予访问权限。具有[自动模型回退](/docs/zh-CN/model-config#automatic-model-fallback)的模型会打印不同的消息，不含此链接；在 Opus 5.5 和 Sonnet 5.5 上，该消息以 `<model>'s safeguards flagged this session` 开头。该部分还介绍了 Claude Code 何时改为切换模型。

在 [Amazon Bedrock](/docs/zh-CN/amazon-bedrock)、[Google Cloud 的 Agent Platform](/docs/zh-CN/google-vertex-ai) 和 [Microsoft Foundry](/docs/zh-CN/microsoft-foundry) 上，网络安全标记会改为产生[使用政策拒绝](#usage-policy-refusal)消息。

保护措施本身是服务器端的，早于 v2.1.203；自那以后的客户端版本仅更改了消息的措辞。
从 v2.1.203 到 v2.1.218，消息读取 `<model> has safety measures that flagged this message for a cybersecurity topic. To learn about the Cyber Verification Program and apply for access, visit our help center:` 后跟相同的帮助中心链接，交互式会话附加 `If you were not engaging in a cybersecurity topic, please send feedback via /feedback.`
在 v2.1.203 之前，它读取 `<model>'s safeguards flagged this message for a cybersecurity topic. If your work requires this access, you can apply for an exemption:` 后跟豁免表单链接。

**要做什么：**

* 如果您的工作需要此内容，通过[网络安全验证计划](https://support.claude.com/en/articles/14604842-real-time-cyber-safeguards-on-claude)申请访问权限
* 如果您的请求不是关于网络安全主题，运行 `/feedback` 报告误报
* 要继续在同一会话中工作，按 Esc 两次或运行 `/rewind` 回退到触发标记的轮次之前的检查点，然后采取不同的方法。请参阅[检查点](/docs/zh-CN/checkpointing)。

<h3 id="safeguards-flagged-a-request-for-claudes-reasoning">
  保护措施标记了索取 Claude 推理过程的请求
</h3>

API 拒绝了该请求，因为保护措施将其标记为要求模型在响应中复述其内部推理过程。API 将此[拒绝类别](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#refusal-response)命名为 `reasoning_extraction`，拒绝消息包含以下行：

```text theme={null}
Details: `[reasoning_extraction]`
```

在 v2.1.234 之前，拒绝消息不包含 `Details` 行。

**要做什么：**

* 删除或改写任何要求 Claude 逐字或以固定格式写出其思考或推理过程的指令，例如 `<thinking>` 部分、草稿区部分或 JSON 输出中的 `reasoning` 字段。该指令可能位于您的提示词中，也可能位于 Claude Code 随其加载的自定义内容中，例如 CLAUDE.md、skill、子代理提示词、输出样式或 MCP 工具描述。
* 要检查某个自定义内容是否为触发原因，请在终端中运行 [`claude --safe-mode`](/docs/zh-CN/cli-reference#cli-flags) 以启动禁用自定义内容的会话，然后发送相同的提示词
* 更改自定义内容后，启动新会话
* 要改写您已发送的提示词，请参阅[回退并总结](/docs/zh-CN/checkpointing#rewind-and-summarize)
* 您仍然可以要求 Claude 解释其答案。可以要求简短的解释、结果背后的依据，或其所执行操作的摘要。要阅读 Claude 思考的摘要，请参阅 [`showThinkingSummaries`](/docs/zh-CN/settings-reference#showthinkingsummaries)。
* 有关更多示例，以及改写后的请求仍被拒绝时该怎么做，请参阅[将推理保留在思考块中](https://platform.claude.com/docs/en/build-with-claude/refusals-and-fallback#keep-reasoning-in-thinking-blocks)

<h3 id="output-blocked-by-content-filtering-policy">
  Output blocked by content filtering policy
</h3>

API 的输出内容过滤器中止了 Claude 正在生成的响应。消息文本来自 API：

```text theme={null}
API Error: Output blocked by content filtering policy
```

**要做什么：**

* 重新表述您的上一条消息或采取不同的方法
* 要回退到触发拦截的轮次之前的检查点，请按 Esc 两次或运行 `/rewind`。请参阅[检查点](/docs/zh-CN/checkpointing)

<h2 id="installation-errors">
  安装错误
</h2>

这些错误在安装或更新 Claude Code 时出现，来自 [安装脚本](/docs/zh-CN/setup#install-claude-code)、`claude install` 或 `claude update`。对于安装过程中的 `command not found`、PATH、权限和 TLS 问题，请参阅 [排查安装和登录问题](/docs/zh-CN/troubleshoot-install)。

<h3 id="installation-was-killed-before-it-could-finish">
  安装在完成前被中止
</h3>

当 `claude install` 步骤被信号终止时，安装脚本会报告。在 Linux 上，退出代码 137 表示进程收到了 SIGKILL，在低内存主机上通常是内核内存不足 (OOM) 杀手。脚本打印此说明并以代码 137 退出：

```text theme={null}
Installation was killed before it could finish (exit code 137). This usually means the system ran out of memory.
Claude Code needs roughly 512MB of free memory to install. Free up memory, then run this script again.
```

对于任何其他致命信号，以及 macOS 上的退出代码 137，脚本打印 `Installation was killed before it could finish (exit code <N>)`，其中包含实际的退出代码，并省略内存不足的说明。该消息来自 macOS 和 Linux 使用的安装脚本，该脚本也涵盖 WSL 内的安装；本机 Windows 安装脚本永远不会打印它。在 v2.1.200 之前，脚本仅以 shell 的裸 `Killed` 行退出。

**应该做什么：**

* 停止其他进程以释放内存，然后重新运行安装程序
* 添加交换空间或移至更大的实例。有关交换文件命令，请参阅 [在低内存 Linux 服务器上安装被中止](/docs/zh-CN/troubleshoot-install#install-killed-on-low-memory-linux-servers)。

<h3 id="the-connection-dropped-while-downloading-the-update">
  下载更新时连接断开
</h3>

与下载服务器的连接在 `claude install` 或 `claude update` 获取 Claude Code 二进制文件时关闭，重试也没有恢复。当连接断开、传输停滞或下载的文件校验和失败时，Claude Code 会重试下载，总共最多尝试三次。已完成的 HTTP 错误（例如 404）不会重试，因为服务器已经响应。在 v2.1.202 之前，单个断开的连接会立即导致下载失败，并显示裸错误 `aborted`，而不是重试。

```text theme={null}
The connection dropped while downloading the update (attempt 3/3: aborted). Check your network — proxies sometimes cut off large downloads.
```

括号中的文本命名失败的尝试和底层网络错误。`claude update` 在 stderr 上以 `Error: Failed to install native update` 开头的消息。

保持连接但在 10 分钟内未完成的下载失败，显示 `Download timed out: exceeded the total deadline`。Claude Code 不会重试超时的下载，因为连接速度太慢而无法在截止时间内完成，在立即重试时也不会完成。以下步骤适用于两条消息。

代理或网关可以在长传输完成前关闭它，而 Claude Code 二进制文件是一个大型下载。

**应该做什么：**

* 再次运行 `claude update`。在网络状况良好的情况下，下载通常在下一次运行时成功。对于超时消息，从更快或限制较少的网络再次运行它。
* 如果您的网络需要代理，请在运行安装程序或 `claude update` 之前设置 `HTTPS_PROXY`。请参阅 [检查网络连接](/docs/zh-CN/troubleshoot-install#check-network-connectivity)。
* 如果公司代理持续关闭传输，请要求您的网络团队允许从 `downloads.claude.ai` 进行完整下载。请参阅 [网络访问要求](/docs/zh-CN/network-config#network-access-requirements)。
* 从您的 shell 运行 `claude doctor` 以进行安装诊断

<h2 id="command-line-errors">
  命令行错误
</h2>

这些错误来自 `claude` 命令行及其子命令、您在提示符处提交的命令名称，以及 `/security-review` 等在其提示词运行前通过执行 shell 命令收集上下文的命令。它们也可能来自会重新启动 CLI 的 `/tui`。

<h3 id="conflict-between-bg-and-print">
  `--bg` 与 `--print` 冲突
</h3>

此消息需要 Claude Code v2.1.198 或更高版本。您在同一次 `claude` 调用中将 `--bg` 与 `-p` 或 `--print` 组合使用。`--bg` 会启动一个[后台会话](/docs/zh-CN/agent-view#from-your-shell)，您稍后可通过 `claude agents` 附加到该会话；而 `--print` 以[非交互方式](/docs/zh-CN/headless)运行，永远不会启动 `claude agents` 所附加的交互式会话。在 v2.1.198 之前，这种组合会静默创建一个永远无法附加的后台作业。

```text theme={null}
--bg and --print conflict: --print never starts the interactive session that `claude agents` attaches to, so the job would be unattachable. The prompt is the positional — drop --print: `claude --bg '<task>'`.
```

**解决方法：**

* 去掉 `-p` 或 `--print`。`--bg` 将提示词作为其位置参数，因此 `claude --bg "<task>"` 就是完整的命令。请参阅[从 shell 中 Dispatch 新的 Agent](/docs/zh-CN/agent-view#from-your-shell)。
* 若要以非交互方式运行提示词并打印结果，而不是创建后台会话，请去掉 `--bg` 并运行 `claude -p "<task>"`

<h3 id="conflict-between-a-system-prompt-flag-and-its-file-form">
  系统提示词标志与其文件形式冲突
</h3>

您在一次 `claude` 调用中同时传入了 [`--append-subagent-system-prompt`](/docs/zh-CN/cli-reference#cli-flags) 和 `--append-subagent-system-prompt-file`，因此 `claude` 以退出码 1 退出，而不是启动会话：

```text theme={null}
Error: Cannot use both --append-subagent-system-prompt and --append-subagent-system-prompt-file. Please use only one.
```

在 v2.1.283 之前，当您将 `--system-prompt` 与 `--system-prompt-file` 一起传入，或将 `--append-system-prompt` 与 `--append-system-prompt-file` 一起传入时，`claude` 也会以同样的方式退出，因为这些成对的标志会相互冲突，而不是[组合使用](/docs/zh-CN/cli-reference#system-prompt-flags)。在这些版本中，消息会指出您组合使用的那一对标志。

**解决方法：**

* 保留标志的一种形式并去掉另一种。若要将固定的提示词文件与每次运行的文本组合，请在启动前将文本合并到文件中，而不是同时传入两个标志

<h3 id="invalid-agents-configuration">
  无效的 `--agents` 配置
</h3>

您传给 `--agents` 的值无效，因此 `claude` 以退出码 1 退出，而不是启动会话。当您传入 `--safe-mode` 或设置 [`CLAUDE_CODE_SAFE_MODE`](/docs/zh-CN/env-vars#variables) 时，Claude Code 会完全忽略 `--agents`。使用 `--resume` 或 `--continue` 时，内联 JSON 值不会被检查，会话会正常启动；从文件读取的值则在每次启动时都会被检查。在 v2.1.242 之前，Claude Code 无论如何都会启动会话。

```text theme={null}
Error: Invalid --agents configuration:
<what failed>
```

第一行之后的内容取决于该值失败的方式。Claude Code 按顺序运行以下检查，并在第一个失败的检查处停止。如果您的值有两类问题，您只有在修复第一类问题后才会看到第二类：

1. 当值以 `{` 开头但无法解析为 JSON，或 `--agents` 文件的内容无法解析时，Claude Code 会打印一行 `invalid JSON:`，其中包含 JSON 解析器自身的消息
2. 当值可以解析，但某个 Agent 定义不符合 [CLI 定义的子代理](/docs/zh-CN/sub-agents#choose-the-subagent-scope)的 schema 时，Claude Code 会为每个问题打印一行
3. 当 Agent 名称以 `-` 开头时，Claude Code 会打印 `<name>: agent names must not start with '-'`

当问题行超过 20 行时，Claude Code 会打印前 20 行，并将其余部分替换为 `…and N more`。

使用 `--print` 时，`--agents` 还接受 [JSON 文件的路径](/docs/zh-CN/sub-agents#choose-the-subagent-scope)来代替内联对象。在 v2.1.281 之前，`--agents` 只接受内联 JSON，并将文件路径视为无效 JSON。文件形式有其自身的拒绝情况，会代替此消息打印出来，包括以下几种：

* **`Error: --agents takes a JSON object, or a file path only with --print (-p)`**：Claude Code 在交互式会话中将该值读取为文件路径。请以内联 JSON 的形式传入定义，或添加 `-p` 以从文件读取定义。
* **`Error: --agents file not found: <path>`**：该路径下不存在文件。不以 `{` 开头且不是有效 JSON 的值会被读取为路径，因此被 shell 破坏的内联 JSON 也可能以这种方式失败。请检查路径或引号，然后再次运行命令。

**解决方法：**

* 修复消息列出的每个问题，然后再次运行命令。请参阅 [CLI 定义的子代理可接受的字段](/docs/zh-CN/sub-agents#choose-the-subagent-scope)。

<h3 id="cloud-sessions-cannot-be-created-from-a-restricted-session">
  无法从 `--restricted` 会话创建云端会话
</h3>

当您使用 [`--restricted`](/docs/zh-CN/cli-reference#cli-flags) 启动会话时，Claude Code 会拒绝从该会话创建[云端会话](/docs/zh-CN/claude-code-on-the-web#from-terminal-to-cloud)，因为新会话将在受限进程之外运行，不会强制执行受限模式。Claude Code 在客户端拒绝，且发生在联系服务器之前，因此不会创建任何云端会话：

```text theme={null}
Cloud sessions cannot be created from a --restricted session: they would not enforce it.
```

**解决方法：**

* 在受限会话中本地运行该任务
* 如果您能控制会话的启动方式，请不带 `--restricted` 启动一个新的 `claude` 会话，并从那里创建云端会话

在 v2.1.248 之前，Claude Code 没有 `--restricted` 标志；更早的版本会以未知选项错误拒绝该标志本身。

<h3 id="cloud-sessions-are-disabled-by-your-organizations-policy">
  云端会话已被您组织的策略禁用
</h3>

您组织的 `allow_remote_sessions` 策略已关闭，因此[云端会话](/docs/zh-CN/claude-code-on-the-web)以及使用云端会话的命令均不可用：

```text theme={null}
Cloud sessions are disabled by your organization's policy. Contact your organization admin to enable them.
```

当您[从终端创建云端会话](/docs/zh-CN/claude-code-on-the-web#from-terminal-to-cloud)时，以及当您提交需要云端会话的命令（例如 `/teleport`、`/remote-env` 或 `/web-setup`）时，会出现此消息。在 v2.1.268 之前，提交这些命令之一会返回 [`Unknown command`](#unknown-command)。

这是服务器端的组织策略，因此无法通过本地设置、环境变量或 CLI 标志覆盖。

如果 Claude Code 尚未加载您组织的策略或无法获取该策略，这些命令会改为回复 `Couldn't verify your organization's policy for cloud sessions. Check your network connection, then restart Claude Code and try again.`。

**解决方法：**

* 请您组织中的 [Owner](/docs/zh-CN/server-managed-settings#access-control) 在 [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) 的 Claude Code 管理设置中启用云端会话
* 如果消息提示无法验证策略，请检查您的网络连接，然后重新启动 Claude Code 并重试

<h3 id="the-json-schema-value-is-not-a-valid-json-schema">
  `--json-schema` 的值不是有效的 JSON Schema
</h3>

您在[非交互模式](/docs/zh-CN/headless#get-structured-output)下传给 [`--json-schema`](/docs/zh-CN/cli-reference#cli-flags) 的 schema 未能通过 JSON Schema 编译，因此 `claude` 以退出码 1 退出，而不是运行提示词。在 v2.1.205 之前，无效的 schema 会产生非结构化输出且不报错，并且任何使用 `format` 关键字的 schema 都会被视为无效。

```text theme={null}
Error: --json-schema is not a valid JSON Schema: data/type must be equal to one of the allowed values
```

第二个冒号之后的文本是验证器的诊断信息，会指出失败的关键字或位置。使用 `format` 关键字的 schema（例如 `"format": "email"`）是有效的：Claude Code 将 `format` 作为注解接受，但不强制执行。

Claude Code 在 schema 编译之前会运行两项检查：对于无法解析为 JSON 的值，它会以 `Error: --json-schema is not valid JSON` 拒绝；对于是有效 JSON 但不是对象的值，它会以 `Error: --json-schema must be a JSON object` 拒绝。

**解决方法：**

* 修复诊断信息指出的 schema 部分，然后重新运行命令
* 请参阅[获取结构化输出](/docs/zh-CN/headless#get-structured-output)，了解可用的 schema 和命令示例

<h3 id="settings-file-exceeds-the-2mib-limit">
  设置文件超过 2MiB 限制
</h3>

您传给 [`--settings`](/docs/zh-CN/cli-reference#cli-flags) 的文件大于 2 MiB，因此 `claude` 在启动时以退出码 1 退出，而不是加载该文件。在 v2.1.214 之前，Claude Code 读取文件时不检查大小，数 GB 的文件或 `/dev/zero` 之类的设备文件会使内存无限增长。

```text theme={null}
Error: Settings file exceeds the 2MiB limit: /path/to/settings.json
```

对于不是常规文件的 `--settings` 路径，Claude Code 也会以同样方式拒绝：设备、FIFO 或套接字会报告 `Error: Cannot use settings file (Not a regular file (device, FIFO, or socket))`，后跟路径；目录则会报告 `EISDIR` 原因。

**解决方法：**

* 将 `--settings` 指向一个小于 2 MiB 的常规 JSON 设置文件。有关格式，请参阅[设置](/docs/zh-CN/settings)。

<h3 id="the-current-directory-no-longer-exists">
  当前目录已不存在
</h3>

您从一个在 shell 进入后被删除或移动的目录中启动了 `claude`，例如被另一个 shell 删除的 worktree 或临时目录。Claude Code 无法读取其工作目录，因此无论是交互模式还是[非交互](/docs/zh-CN/headless)模式，它都会在启动会话前以退出码 1 退出。在 v2.1.239 之前，Claude Code 会崩溃，并在 stderr 上输出压缩后的 bundle 源代码和原始的 `ENOENT ... uv_cwd` 堆栈，而不是此消息。

```text theme={null}
The current directory no longer exists (it was deleted or moved). Start Claude Code from an existing directory.
error: The current working directory was deleted, so that command didn't work. Please cd into a different directory and try again.
```

两种形式的原因和解决方法相同。

当 Claude Code 因其他原因（例如权限变更）无法读取工作目录时，消息会改为指出错误代码：`Can't read the current directory (EACCES). Start Claude Code from a different directory.`

在 macOS 上，如果 `~/Desktop`、`~/Documents`、`~/Downloads` 或 iCloud Drive 中的目录出现 `EPERM`，通常意味着 macOS 阻止了您的终端应用访问该文件夹。读取该文件夹的其他命令也会以同样方式失败：在那里运行 `ls` 会报告 `Operation not permitted`，即使使用 `sudo` 也是如此。

**解决方法：**

* 切换到一个存在的目录，例如您的主目录或项目目录，然后再次运行 `claude`
* 如果该目录已在同一路径下重新创建，您的 shell 仍持有已删除的那个目录。运行 `cd "$PWD"`，或离开后重新进入该目录，然后再次运行 `claude`
* 对于 macOS 上的 `EPERM`，请使用 Cmd+Q 退出终端应用，重新打开它，返回该文件夹，然后运行 `claude`。如果在该文件夹中运行 `ls` 仍然失败，请打开 **System Settings > Privacy & Security > Files and Folders**，为您的终端应用启用该文件夹，然后重新打开终端

<h3 id="temp-directory-refused-or-cannot-be-created">
  临时目录被拒绝或无法创建
</h3>

在 macOS 和 Linux 上，Claude Code 会在启动时创建一个私有临时目录，即系统临时目录下或 [`CLAUDE_CODE_TMPDIR`](/docs/zh-CN/env-vars) 覆盖路径下的 `claude-<uid>`。当该目录无法创建，或该路径上已存在的条目未通过安全检查时，Claude Code 会将失败信息打印到 stderr，并以退出码 1 退出，而不是启动会话：

```text wrap theme={null}
ENOSPC: no space left on device, mkdir '/tmp/claude-501'

Temp directory /tmp/claude-501 is not a directory (may be an attacker-planted symlink). Refusing to use it. Set CLAUDE_CODE_TMPDIR to a directory you control, or ask an administrator to remove it.

Temp directory /tmp/claude-501 is owned by uid 502, expected 501. Refusing to use it — another user may have pre-created it. Set CLAUDE_CODE_TMPDIR to a directory you control, or ask an administrator to remove it.

Temp directory /tmp/claude-501 is not readable (its mode may have been altered, or a path component denies search). Refusing to use it — restore its permissions (chmod 0700) or remove it. Set CLAUDE_CODE_TMPDIR to a directory you control, or ask an administrator to remove it.
```

**解决方法：**

* 对于 `ENOSPC`，请释放存放临时目录的卷上的磁盘空间
* 对于 `Refusing to use it` 形式，请删除所指出的条目本身（而不是链接指向的内容），然后再次启动 Claude Code；对于 `owned by uid` 形式，只有管理员或该用户才能删除它
* 对于 `is not readable`，请对所指出的目录运行 `chmod 0700`，或将其删除后重新启动
* 在上述任何情况下，都可以将 [`CLAUDE_CODE_TMPDIR`](/docs/zh-CN/env-vars) 设置为您控制的目录，然后再次启动 Claude Code，而不必处理被拒绝的路径

<h3 id="directory-couldnt-be-resolved-to-a-real-location">
  无法将目录解析为真实位置
</h3>

您对工作目录的某个子目录运行了 `/add-dir`，而 Claude Code 无法将该目录解析为其真实位置。

您对工作目录的子目录已有文件访问权限，因此 `/add-dir` 只会加载其中的 skill、命令和 Agent。在加载之前，Claude Code 会检查该目录解析所有符号链接后的真实位置是否位于工作目录内。当 Claude Code 无法解析该位置时，它不会加载任何内容，并显示以下消息：

```text theme={null}
packages/app couldn't be resolved to a real location, so its skills, commands, and agents weren't loaded. Check that it is a directory inside the working directory and try again.
```

**解决方法：**

* 检查该路径是否指向工作目录内的真实目录，然后再次运行 `/add-dir`
* 此消息不会改变您的文件访问权限；它只报告该目录的 `.claude/` 内容未被加载

在 v2.1.261 之前，当工作目录位于 `/net/<host>` 自动挂载点上时，每次运行 `/add-dir <subdirectory>` 都会出现此消息，因为 Claude Code 在设计上不会解析这类路径；目录本身没有问题，重试也无济于事。

<h3 id="workspace-not-trusted-when-starting-remote-control">
  启动 Remote Control 时工作区不受信任
</h3>

您在一个尚未信任的目录中使用 `claude remote-control` 或其别名 `claude rc` 启动了 [Remote Control](/docs/zh-CN/remote-control) 服务器模式，而该命令无法询问您是否信任该目录。例如，该命令的标准输入或标准输出不是终端，因为其中之一被重定向或通过管道传输。该命令以退出码 1 退出：

```text theme={null}
Error: Workspace not trusted. Please run `claude` in /Users/you/project first to review and accept the workspace trust dialog.
```

还有两个同样以 `Error: Workspace not trusted.` 开头的变体，会出现在太小而无法显示信任该目录将启用哪些内容的终端中，或出现在未报告其尺寸的终端中。请放大窗口或切换到普通终端窗口，然后再次运行 `claude rc`。

在您的主目录中，消息会有所不同，因为工作区信任对话框永远不会为主目录保存信任，所以在那里接受信任无法满足此检查。在 v2.1.214 之前，主目录会显示上面的消息，而其建议在那里无法奏效。

```text theme={null}
Error: Workspace not trusted. /Users/you is your home directory, and for security home-directory trust is never saved, so running `claude` here first won't help. Run `claude rc` from a project directory instead (run `claude` there once to accept the trust dialog).
```

如果您在 [`Trust <directory>?` 问题](/docs/zh-CN/remote-control#requirements)处回答 `n` 或按 Enter，该命令会打印一条指出该目录的 `Remote Control did not start` 消息，并以退出码 1 退出。再次运行 `claude rc` 即可回答 `y`。

**解决方法：**

* 先从终端信任该目录：在那里运行 `claude rc` 并回答 `y`，或在那里运行 `claude` 并接受[工作区信任对话框](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust)，然后再次运行您原来的命令
* 如果在主目录中，请切换到项目目录，并在那里启动 Remote Control

在 v2.1.284 之前，即使在终端中，该命令也从不询问。

<h3 id="not-carried-over-to-the-sessions-remote-control-starts">
  不会传递到 Remote Control 启动的会话
</h3>

您在 `remote-control` 动词之前使用了一个全局 `claude` 标志来启动 [Remote Control](/docs/zh-CN/remote-control)，而该标志会限制或配置 Remote Control 启动的会话，例如 `--settings`、`--setting-sources`、`--permission-mode`、`--disallowed-tools` 或 `--mcp-config`。放在动词之前的标志永远不会传递到这些会话。Claude Code 会拒绝启动，并指出该标志：

```text theme={null}
Error: `--settings` before `remote-control` is not carried over to the sessions Remote Control starts, so Remote Control refuses to start rather than drop it — remove it, and give Remote Control's own options after the verb (see `claude remote-control --help`).
```

对于丢弃后无害的全局标志，例如 `--verbose`、`--model`，或由包装器注入的 `--session-id` 或 `--plugin-dir`，Claude Code 不会拒绝：它会忽略这些标志，Remote Control 照常启动。

对于尚未被识别为无害的全局标志，Claude Code 也会拒绝启动，因此较新版本中新增的标志可能会出现在此消息中，直到后续版本将其标记为无害。

**解决方法：**

* 从动词之前移除该标志，并在动词之后传入 [Remote Control 自己的选项](/docs/zh-CN/remote-control#start-a-remote-control-session)；`claude remote-control --help` 会列出这些选项
* 当被拒绝的标志是 `--permission-mode` 时，请运行 `claude remote-control --permission-mode <mode>` 来为 Remote Control 启动的会话设置权限模式

在 v2.1.248 之前，当全局标志在前时，`claude remote-control` 不接受其自身的标志，命令会以 `unknown option` 错误失败。

<h3 id="claude-import-is-not-yet-available-in-this-build">
  claude import 在此版本中尚不可用
</h3>

您运行了 [`claude import`](/docs/zh-CN/cli-reference#cli-commands)，而 Claude Code 发现导入流程处于关闭状态，因此该命令以退出码 1 退出，而不是开始导入。在 v2.1.222 之前，关闭了导入流程的版本会将 `import` 视为提示词，并启动交互式会话，而不是打印此消息。

```text theme={null}
`claude import` is not yet available in this build. Run `claude` and use /mcp or edit ~/.claude/settings.json directly.
```

Claude Code 通过从 Anthropic 获取并缓存在磁盘上的功能标志来启用 `claude import`。此消息表示缓存的值为关闭。原因通常是以下之一：

* 安装后您尚未启动过会话，因此 Claude Code 还没有获取该标志。即使该功能对您可用，第一次运行 `claude import` 也可能打印此消息。
* 您通过 Amazon Bedrock、Google Cloud 的 Agent Platform、Microsoft Foundry 或 Claude Platform on AWS 使用 Claude Code，或通过 [Claude apps gateway](/docs/zh-CN/claude-apps-gateway#availability-and-limitations) 使用。Claude Code 在这些会话中不会获取功能标志，因此 `claude import` 始终不可用。
* 您设置了 `DISABLE_TELEMETRY`、`DO_NOT_TRACK`、`DISABLE_GROWTHBOOK` 或 [`CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`](/docs/zh-CN/env-vars)，这些会关闭功能标志的获取，因此 `claude import` 始终不可用。

**解决方法：**

* 在全新安装中，启动 `claude`，等待会话加载完成后退出，然后再次运行 `claude import`
* 在功能标志获取始终关闭的情况下，请自行进行配置：使用 [`claude mcp add`](/docs/zh-CN/mcp#installing-mcp-servers) 添加 MCP 服务器，并创建您想迁移的 [`CLAUDE.md` 文件](/docs/zh-CN/memory#how-claude-md-files-load)、[skill 和命令](/docs/zh-CN/skills#where-skills-live)以及[子代理](/docs/zh-CN/sub-agents#choose-the-subagent-scope)。消息中还提到了 `~/.claude/settings.json`。在 `claude import` 迁移的配置中，该文件只保存[权限模式](/docs/zh-CN/settings-reference#permission-settings)；Claude Code 不会从中读取 MCP 服务器。

<h3 id="could-not-read-claude-code-config">
  无法读取 Claude Code 配置
</h3>

您运行了 [`claude import`](/docs/zh-CN/cli-reference#cli-commands)，而此时 Claude Code 无法解析 `~/.claude.json`，即存储您的登录信息和各项目状态的文件。该子命令会读取此文件以检查可用性，但不会显示交互式会话中的恢复对话框，因此它以退出码 1 退出。在 v2.1.222 之前，配置文件不可读时运行 `claude import` 会启动交互式会话，由其恢复对话框处理该文件。

```text theme={null}
Could not read Claude Code config — run `claude` with no arguments to recover it.
```

**解决方法：**

* 不带参数运行 `claude`。Claude Code 会检测到无效文件并提供重置选项。然后再次运行 `claude import`。
* 若要保留您手动进行的编辑，请改为在编辑器中修复 `~/.claude.json` 中的 JSON 语法，然后重新运行 `claude import`

<h3 id="could-not-import-a-server-from-claude-desktop">
  无法从 Claude Desktop 导入服务器
</h3>

Claude Code 无法添加您在 `claude mcp add-from-claude-desktop` 中选择的某个服务器。该命令仍会导入其他选中的服务器，并为每个无法添加的服务器打印一行。在 v2.1.205 之前，第一个失败的服务器会中止导入。

```text theme={null}
Could not import my server: Invalid name my server. Names can only contain letters, numbers, hyphens, and underscores.
```

服务器名称之后的文本是原因。最常见的是名称检查：Claude Desktop 允许服务器名称中包含空格和句点等字符，而 `claude mcp` 将其限制为字母、数字、连字符和下划线。其他原因包括服务器配置未通过验证，以及服务器被您组织的 [MCP 策略](/docs/zh-CN/managed-mcp)阻止。

**解决方法：**

* 在 `claude_desktop_config.json` 中将服务器重命名为仅使用字母、数字、连字符和下划线，然后再次运行 `claude mcp add-from-claude-desktop`
* 使用 `claude mcp add` 或 `claude mcp add-json` 以有效名称直接添加该服务器。请参阅[从 Claude Desktop 导入 MCP 服务器](/docs/zh-CN/mcp#import-mcp-servers-from-claude-desktop)。

<h3 id="cannot-add-mcp-server-to-the-managed-scope">
  无法将 MCP 服务器添加到 managed 作用域
</h3>

您使用 `--scope managed` 运行了 `claude mcp add` 或 `claude mcp add-json`。该作用域保存的是您的组织通过 [`managedMcpServers`](/docs/zh-CN/settings-reference#managedmcpservers) 托管设置提供的服务器。Claude Code 只从托管设置中读取它们，因此该命令无法将服务器写入该作用域。

```text theme={null}
Cannot add MCP server to scope: managed
```

**解决方法：**

* 将服务器添加到您可以写入的作用域：`local`、`user` 或 `project`。不带 `--scope` 时，该命令使用 `local`。请参阅 [MCP 安装作用域](/docs/zh-CN/mcp#mcp-installation-scopes)
* 若要向组织中的每个用户提供该服务器，请将其添加到您部署的托管设置中的 [`managedMcpServers`](/docs/zh-CN/settings-reference#managedmcpservers)

<h3 id="cannot-add-mcp-server-when-managed-settings-allow-only-plugin-servers">
  托管设置仅允许插件服务器时无法添加 MCP 服务器
</h3>

您运行了 `claude mcp add` 或 `claude mcp add-json`，而您组织的托管设置将 [`strictPluginOnlyCustomization`](/docs/zh-CN/settings-reference#strictpluginonlycustomization) 设为 `true` 或设为包含 `mcp` 的列表。在该设置下，Claude Code 不会从 `~/.claude.json` 或 `.mcp.json` 加载 MCP 服务器，因此该命令以退出码 1 退出，而不是保存一个永远不会加载的服务器：

```text theme={null}
Cannot add MCP server: your organization's managed settings allow only MCP servers that plugins provide. Install a plugin that provides this server, or ask your administrator to make it available.
```

`claude mcp add-from-claude-desktop` 会将您选择的每个服务器报告为未导入，并以此消息作为原因。[`/import`](/docs/zh-CN/commands#all-commands) 会为其尝试添加的每个 MCP 服务器报告此消息，但仍会导入它找到的其他项目。

在 v2.1.284 之前，这些命令会保存服务器并报告成功，但该服务器永远不会加载。

**解决方法：**

* 安装一个提供该服务器的[插件](/docs/zh-CN/plugins/install)
* 请您的管理员通过[插件](/docs/zh-CN/plugins/org)分发该服务器；如果它是远程 HTTP 或 SSE 服务器，也可以通过 [`managedMcpServers`](/docs/zh-CN/settings-reference#managedmcpservers) 提供

<h3 id="cant-read-mcp-json">
  无法读取 .mcp.json
</h3>

读取项目 [`.mcp.json`](/docs/zh-CN/mcp#project-scope) 的命令（例如带 `--scope project` 的 `claude mcp add` 或 `claude mcp add-json`，或 `claude mcp remove`）发现当前目录中的该文件不是常规文件或大于 2 MiB，因此以此错误退出，而不是读取该文件。

```text theme={null}
Can't read .mcp.json: it isn't a regular file or is larger than 2097152 bytes. Fix or remove it, then run the command again.
```

在 v2.1.257 之前，`.mcp.json` 处的 FIFO 会使命令永远等待且没有任何输出，而指向 `/dev/zero` 等设备文件的符号链接会使内存持续增长，直到进程被终止。

**解决方法：**

* 检查当前目录中 `.mcp.json` 处是什么内容。将其替换为采用[项目作用域格式](/docs/zh-CN/mcp#project-scope)的普通 JSON 文件，或将其删除，然后再次运行命令。

<h3 id="mcp-server-was-not-saved-or-removed">
  MCP 服务器未被保存或移除
</h3>

您对 `user` 或 `local` [作用域](/docs/zh-CN/mcp#mcp-installation-scopes)中的服务器运行了 `claude mcp add`、`claude mcp add-json` 或 `claude mcp remove`。这两个作用域都存储在 `~/.claude.json` 中，而 Claude Code 在写入后回读该文件时，发现更改并不在其中。该命令以此错误退出，而不是输出成功信息。

```text theme={null}
MCP server "example" was not saved to /home/user/.claude.json. If that file is read-only or protected by a sandbox, make it writable or run the command outside the sandbox, then add the server again.
```

移除操作之后，消息会显示为 `was not removed from`，并以 `then remove the server again` 结尾。对于 `local` 作用域的服务器，路径之后会跟上该条目所属的项目目录，形式为 `(local scope for /path/to/project)`。

在 v2.1.283 之前，即使更改未写入文件，`claude mcp add`、`claude mcp add-json` 和 `claude mcp remove` 也会报告成功。

**解决方法：**

* 使消息中指出的文件可写，或在沙箱之外运行命令，然后再次运行相同的添加或移除命令。

<h3 id="mcp-server-may-not-have-been-saved-or-removed">
  MCP 服务器可能未被保存或移除
</h3>

您对 `user` 或 `local` [作用域](/docs/zh-CN/mcp#mcp-installation-scopes)中的服务器运行了 `claude mcp add`、`claude mcp add-json` 或 `claude mcp remove`，而 Claude Code 无法回读 `~/.claude.json` 来确认更改。更改可能已写入磁盘，也可能没有。括号中的文本是该读取操作的错误。

```text theme={null}
MCP server "example" may not have been saved: /home/user/.claude.json could not be read to confirm the change (EACCES: permission denied, open '/home/user/.claude.json'). Run `claude mcp get example` to check, then add the server again if it is missing.
```

移除操作之后，消息会显示为 `may not have been removed`，并以 `then remove the server again if it is still listed` 结尾。

在 v2.1.283 之前，即使无法确认更改，这些命令也会报告成功。

**解决方法：**

* 运行 `claude mcp get <name>` 检查更改是否已写入磁盘。对于 `local` 作用域的服务器，请从该服务器所属的项目目录运行，因为 local 作用域是按项目划分的。
* 如果添加后服务器缺失，或移除后仍被列出，请再次运行相同的添加或移除命令。

<h3 id="anthropic-hosted-and-doesnt-support-local-oauth">
  服务器由 Anthropic 托管，不支持本地 OAuth
</h3>

您为某个 MCP 服务器发起了登录，而其 URL 指向一个通过第三方身份提供商进行身份验证的 Anthropic 托管连接器主机。这些主机包括 `microsoft365.mcp.claude.com`、`gmail.mcp.claude.com` 和 `gcal.mcp.claude.com`。对于这些主机，Claude Code 在 `/mcp` 面板和 `claude mcp login` 中都会拒绝启动其本地 OAuth 流程，因为[它们的登录只能通过 claude.ai 完成](/docs/zh-CN/mcp#use-mcp-servers-from-claude-ai)。

```text theme={null}
"gmail" is Anthropic-hosted and doesn't support local OAuth. Connect it via Settings → Connectors on claude.ai (requires `claude login`), then it'll be available here automatically.
```

**解决方法：**

* 使用 `claude mcp remove <name>` 移除您的条目，以免它遮蔽同一 URL 上的 claude.ai 连接器
* 移除后，在登录您在 Claude Code 中使用的账户的情况下，前往 [claude.ai/customize/connectors](https://claude.ai/customize/connectors) 连接该服务。连接完成后，如果您当前的身份验证方式是 claude.ai 订阅登录，[该连接器会自动出现在 Claude Code 中](/docs/zh-CN/mcp#use-mcp-servers-from-claude-ai)

<h3 id="server-rejected-the-authorization-header-minted-by-the-configured-headershelper">
  服务器拒绝了由配置的 headersHelper 生成的 Authorization 标头
</h3>

某个由 [`headersHelper`](/docs/zh-CN/mcp#use-dynamic-headers-for-custom-authentication) 提供 `Authorization` 标头的 MCP 服务器以 HTTP 401 或 403 响应了连接，因此 Claude Code 报告连接失败。由于该辅助程序提供了 `Authorization` 标头，Claude Code 对该服务器[不会回退到 OAuth](/docs/zh-CN/mcp#authenticate-with-remote-mcp-servers)：

```text theme={null}
Server rejected the Authorization header minted by the configured headersHelper (HTTP 401). Check that the helper command returns a valid credential for this MCP endpoint — OAuth fallback is disabled when the helper supplies Authorization.
```

Claude Code 在每次连接尝试时都会重新运行该辅助程序，因此在暂时性拒绝（例如令牌轮换竞争）之后重试，可能会以新的凭据成功连接。

**解决方法：**

* 按照 Claude Code 运行它的方式自行运行 `headersHelper` 命令：在 [Claude Code 运行它的目录](/docs/zh-CN/mcp#where-the-helper-runs)中，使用 [Claude Code 为其设置的环境变量](/docs/zh-CN/mcp#use-dynamic-headers-for-custom-authentication)，并且对于来自项目 `.mcp.json`、插件或项目 Agent 文件的服务器，不包含 [Claude Code 移除的凭据变量](/docs/zh-CN/mcp#which-variables-a-helper-can-read)。检查它打印的 `Authorization` 值是否被服务器端点接受
* 修复辅助程序或其凭据来源后，在 `/mcp` 中选择该服务器并选择 **Reconnect**

在 v2.1.248 之前，对于由辅助程序提供 `Authorization` 标头的服务器，Claude Code 会运行 OAuth 发现。该发现过程可能以 `Incompatible auth server: does not support dynamic client registration` 失败，而不是报告被拒绝的凭据。

<h3 id="mcp-permission-prompt-tool-not-found">
  未找到 MCP 权限提示工具
</h3>

当运行首次需要权限决策时，您传给 [`--permission-prompt-tool`](/docs/zh-CN/cli-reference#cli-flags) 的工具不在已连接的 MCP 工具之中，原因可能是其服务器从未连接，或者没有任何已连接的服务器公开该名称的工具。Claude Code 仍会发送您的提示词：[非交互](/docs/zh-CN/headless)运行会在第一次工具调用时以此错误和退出码 1 退出，因此即使请求已经发出，也不会产生回答。在第一个提示词之前，Claude Code 会等待该服务器连接，最长等待由 [`MCP_TIMEOUT`](/docs/zh-CN/env-vars) 设置的每服务器连接超时时间 30 秒。在 v2.1.206 之前，启动时不会等待服务器完成连接，因此启动较慢但运行正常的服务器也会产生此错误。

```text theme={null}
Error: MCP tool mcp__permissions__approve (passed via --permission-prompt-tool) not found. Available MCP tools: none
```

`Available MCP tools:` 之后的列表列出了已连接的 MCP 工具。

**解决方法：**

* 检查服务器能否启动并保持连接：在同一目录中运行 `claude mcp list`，并确认该服务器被列为已连接
* 确认工具名称与服务器公开的 `mcp__<server>__<tool>` 名称一致
* 如果服务器需要超过 30 秒才能启动，请调高 [`MCP_TIMEOUT`](/docs/zh-CN/env-vars)

<h3 id="oauth-callback-port-is-already-in-use">
  OAuth 回调端口已被占用
</h3>

当您使用 OAuth 登录远程 MCP 服务器时，Claude Code 会启动一个本地监听器来接收登录回调。如果该监听器所需的端口被另一个进程占用，登录就会以此消息失败。这种情况主要发生在通过 [`MCP_OAUTH_CALLBACK_PORT`](/docs/zh-CN/env-vars) 变量或 `--callback-port` 设置了[固定回调端口](/docs/zh-CN/mcp#use-a-fixed-oauth-callback-port)时，因为如果没有设置，Claude Code 会选择一个可用端口。

```text theme={null}
OAuth callback port <port> is already in use — another process may be holding it. Run `lsof -ti:<port> -sTCP:LISTEN` to find it.
```

在 Windows 上，建议的命令改为 `netstat -ano | findstr :<port>`。

**解决方法：**

* 运行消息中的命令找到占用该端口的进程，然后将其停止或等待其结束
* 如果其他程序需要永久占用该端口，请向服务器注册一个不同的重定向 URI，并使用 `MCP_OAUTH_CALLBACK_PORT` 或 `--callback-port`（取决于您使用哪一个）设置其端口
* 然后重新开始登录，例如在 `/mcp` 中选择该服务器

<h3 id="no-available-ports-for-oauth-redirect">
  没有可用于 OAuth 重定向的端口
</h3>

当您使用 [OAuth](/docs/zh-CN/mcp#authenticate-with-remote-mcp-servers) 登录远程 MCP 服务器时，Claude Code 会启动一个本地监听器来接收登录回调。当 Claude Code 无法为其绑定本地端口时，登录会以此消息失败。机器上的某些东西阻止了它在 `127.0.0.1` 上监听，例如安全软件或拒绝本地监听器的沙箱策略。

```text theme={null}
No available ports for OAuth redirect
```

在 v2.1.268 之前，Claude Code 不会回退到由操作系统分配的端口，因此当仅是其自行选择的端口无法绑定时，也会出现此消息。这种情况可能发生在 Hyper-V 预留了覆盖 Claude Code 选择范围的端口区间的 Windows 主机上。

**解决方法：**

* 检查安全软件或沙箱策略是否阻止进程在 `127.0.0.1` 上监听，并允许 Claude Code 绑定本地端口
* 然后重新开始登录，例如在 `/mcp` 中选择该服务器

<h3 id="security-review-fails-without-origin-head">
  缺少 origin/HEAD 时 /security-review 失败
</h3>

[`/security-review`](/docs/zh-CN/commands#all-commands) 通过将您的分支与 `origin/HEAD` 进行 diff 来构建其审查上下文，`origin/HEAD` 是记录 `origin` 远程上哪个分支为默认分支的本地引用。当该引用不存在时，用于收集 diff 的 git 命令会失败，审查在开始之前就会停止。

```text theme={null}
Error: Shell command failed for pattern "!`git diff --name-only origin/HEAD...`": [stderr]
fatal: ambiguous argument 'origin/HEAD...': unknown revision or path not in the working tree.
Use '--' to separate paths from revisions, like this:
'git <command> [<revision>...] -- [<file>...]'
```

消息中引用的也可能是 `git log` 或其他 `git diff` 命令。只有当远程公布了默认分支且您的 fetch refspec 覆盖了它时，Git 才会创建 `origin/HEAD`；对包含提交的远程执行完整的 `git clone` 时就是如此。在以下设置中，该引用会缺失：

* 单分支或 CI 检出，其 fetch 的 refspec 范围过窄
* 服务器端 HEAD 指向一个从未有人推送过的分支的远程
* 没有 `origin` 远程的仓库，或您从未执行过 fetch 的仓库

对于任何[注入动态上下文](/docs/zh-CN/skills#when-an-injected-command-fails)的 skill，Claude Code 都会显示相同的错误，注入的命令失败会中止该 skill 的调用。还有两条相关字符串会在命令运行之前就触发：

* `Shell command permission check failed for pattern "..."`：该命令的权限检查未允许它运行。[注入命令的权限检查](/docs/zh-CN/skills#permission-checks-on-injected-commands)介绍了在每种权限模式下哪些结果会导致中止，以及如何使用 `allowed-tools` 预先批准命令
* ``Skill <name> requires bash (`shell: bash` in frontmatter) but Git Bash was not found``：该 skill 的 frontmatter 要求使用 bash，但机器上没有 bash。请安装 Git for Windows，或将 frontmatter 改为 `shell: powershell`。请参阅[注入命令的运行方式](/docs/zh-CN/skills#how-injected-commands-run)

**解决方法：**

* 通过指定远程的默认分支来创建该引用：`git remote set-head origin <default-branch>`。只要本地跟踪引用 `origin/<default-branch>` 存在，此方法就有效。如果它不存在（例如在单分支克隆中），请先 fetch 该分支：运行 `git remote set-branches --add origin <branch>`，然后运行 `git fetch origin`，再重新运行 set-head 命令。然后重新运行 `/security-review`。
* 如果您不想指定分支名，请运行 `git fetch origin`，然后运行 `git remote set-head origin --auto`，它会向远程询问哪个分支是默认分支。当远程未公布默认分支时（因为远程为空或其 HEAD 指向从未有人推送过的分支），它会以 `error: Cannot determine remote HEAD` 失败；此时请显式指定分支名。当您的克隆不 fetch 该分支时，它会以 `error: Not a valid ref` 失败；请先按上述方法扩大 refspec。
* 如果仓库没有远程，请使用 `git remote add origin <url>` 添加一个，并在创建引用之前执行 fetch。如果远程为空，请先使用 `git push -u origin HEAD` 推送您的分支，并在 set-head 命令中指定该分支；此后 `origin/HEAD` 指向您刚推送的分支，因此在该分支与其产生分歧之前，`/security-review` 看到的 diff 为空。

<h3 id="input-must-be-provided-when-using-print">
  使用 `--print` 时必须提供输入
</h3>

不带参数的 `claude` 需要 stdout 是终端才能启动交互式 UI。当 stdout 被重定向，或控制台不是真正的终端（例如 PowerShell ISE 和某些 IDE 输出窗格）时，`claude` 会改为以[非交互方式](/docs/zh-CN/headless)运行。这与 `claude -p` 是同一种模式，而该模式需要提示词，因此即使您没有传入该标志，消息中也会提到 `--print`。在任何环境中，传入 `-p`/`--print` 却没有提示词、也没有通过 stdin 管道传入内容，都会产生相同的错误。

```text theme={null}
Error: Input must be provided either through stdin or as a prompt argument when using --print
```

**解决方法：**

* 对于交互式使用，请在真正的终端中运行 `claude`：使用 Windows Terminal 或 PowerShell 控制台而非 ISE，使用 IDE 的集成终端而非输出窗格
* 对于一次性使用，请传入提示词：`claude -p "your question"`，或通过管道传入：`echo "your question" | claude -p`

<h3 id="claude-code-cant-read-the-keyboard-here">
  Claude Code 在此处无法读取键盘输入
</h3>

您在没有 [`-p`](/docs/zh-CN/headless) 的情况下运行了 `claude`，这会启动一个[交互式会话](/docs/zh-CN/interactive-mode)，但其标准输入不是终端。可能是某些东西通过管道传输或重定向了它，或者启动 `claude` 的程序提供了自己的输入流。

交互式会话需要一个终端来读取您的按键，而在没有终端时 Claude Code 的行为取决于您的平台：

* **Windows**：Claude Code 将消息打印到 stderr，并以退出码 1 退出，而不是启动界面
* **macOS 和 Linux**：Claude Code 从 `/dev/tty` 读取您的按键并启动会话，任何通过管道传入的文本都会作为您的第一个提示词。当 `/dev/tty` 无法打开时，您会看到此消息，其第一行会提到 `/dev/tty`，而不是 Windows 的措辞。

在 Windows 上，消息如下：

```text theme={null}
Claude Code can't read the keyboard here: stdin is not a terminal (it is piped, redirected, or supplied by the program that launched claude), and on Windows it can't fall back to the console for input yet.
Run claude directly in Windows Terminal, PowerShell, or Command Prompt, without piping or redirecting its input.
To send text as a prompt and print the reply instead, add -p; it also works with --continue and --resume <session-id> (for example: type notes.md | claude -p --continue).
```

**解决方法：**

* 若要以交互方式工作，请直接在终端中运行 `claude`，不要通过管道传输或重定向其输入
* 若要在不使用交互式界面的情况下获取回复（例如从脚本中），请添加 `-p`，并以参数或 stdin 的方式提供提示词，例如 `claude -p "your question"` 或 `echo "your question" | claude -p`。这同样适用于 `--continue` 和 `--resume <session-id>`。

在 v2.1.287 之前，Claude Code 会启动界面而不是打印此消息，然后要么屏幕上什么都不显示，要么以包含 `Raw mode is not supported` 的错误失败。

如果您是在 `claude install` 期间看到 `Raw mode is not supported`，请参阅[安装期间出现 `Raw mode is not supported`](/docs/zh-CN/troubleshoot-install#raw-mode-is-not-supported-during-install)。

<h3 id="input-contained-only-whitespace">
  输入仅包含空白字符
</h3>

在[非交互模式](/docs/zh-CN/headless)下，Claude Code 会拒绝完全由空格、制表符或换行符组成的提示词，而不是发送它，因为 API 会拒绝没有可见文本的消息。您看到哪条消息取决于空白提示词的来源：

* **`claude -p` 的提示词参数或通过管道传入的 stdin**：`claude` 以 `Error: Input contained only whitespace. Provide a prompt with text through stdin or as a prompt argument when using --print` 退出
* **提交到正在运行的 `--input-format stream-json` 或 [Agent SDK](/docs/zh-CN/agent-sdk/overview) 会话的消息**：Claude Code 会在不调用模型的情况下结束该轮次，会话仍可继续使用。拒绝信息会以一条提示性消息以及该轮次的结果文本的形式送达：`Blank prompt — the message was only whitespace, so nothing was sent to the model.`

在 v2.1.229 之前，Claude Code 会将仅含空白字符的消息发送给 API，API 会以 400 错误拒绝该请求。

**解决方法：**

* 在提示词中包含可见文本。如果脚本从变量或文件构建提示词，请在调用 Claude Code 之前检查来源是否为空。

<h3 id="stream-json-input-carried-over-256m-characters-with-no-newline">
  stream-json 输入包含超过 256M 个字符且没有换行符
</h3>

您的程序在没有换行符的情况下，向 `claude -p --input-format stream-json` 运行的 stdin 发送了超过 268,435,456 个字符，因此 Claude Code 将此错误打印到 stderr 并以退出码 1 退出，而不是继续缓冲更多输入。消息将该上限表述为 `256M`。在 v2.1.257 之前，Claude Code 会无限制地缓冲此类输入，使内存不断增长，直到进程崩溃或被终止。

```text theme={null}
Error: stream-json input carried over 256M characters with no newline. Each stream-json message must be a single newline-terminated JSON line: either the producer is not newline-terminating its messages, or one message exceeded this budget.
```

如此长且没有换行符的输入，通常意味着生产方根本不是 stream-json 生产方，例如误通过管道传入的二进制文件或纯日志输出。单条消息超过上限也会导致同样的检查失败。

**解决方法：**

* 检查通过管道传入 stdin 的内容。使用 [`--input-format stream-json`](/docs/zh-CN/cli-reference#cli-flags) 时，每条消息都必须是以换行符结尾的单行 JSON
* 若要改为发送纯文本，请去掉 `--input-format stream-json`；`claude -p` 默认从 stdin 读取纯文本提示词

<h3 id="unknown-command">
  Unknown command
</h3>

在交互式终端会话中，您提交的 `/` 名称与此会话中的任何命令都不匹配，因此 Claude Code 会报告该名称，而不运行任何内容：

```text theme={null}
Unknown command: /hepl. Did you mean /help?
```

Claude Code 会建议菜单在此会话中列出的最接近的命令名称或别名。如果没有接近的名称，消息会在该名称之后结束。原因通常是以下之一：

* 拼写错误，例如将 `/help` 输成 `/hepl`。[命令菜单如何匹配您输入的内容](/docs/zh-CN/commands#how-the-command-menu-matches-what-you-type)介绍了如何在提交前选择一个接近的匹配项
* 命令存在，但由于未满足某项要求（例如您的平台、套餐或身份验证方式）而在此会话中不可用。[`/web-setup`](/docs/zh-CN/web-quickstart#web-setup-shows-no-commands-match-or-unknown-command) 和 [`/schedule`](/docs/zh-CN/routines#schedule-returns-unknown-command) 的故障排除条目介绍了两种常见情况。某些命令在被您组织的策略禁用时会以自己的消息回复，例如 [`Cloud sessions are disabled by your organization's policy`](#cloud-sessions-are-disabled-by-your-organizations-policy)
* 来自[插件](/docs/zh-CN/plugins/overview)或 [MCP 服务器](/docs/zh-CN/mcp#use-mcp-prompts-as-commands)的命令，而该插件或服务器在此会话中未安装或未连接

只有在交互式终端会话中，Claude Code 才会以这种方式回复未匹配的 `/` 名称。在其他所有会话中，它会将该提示词作为普通消息发送给 Claude，并附上一条说明，指出该命令未运行，以及 Claude 在此会话中可以运行的命令列表。这些会话包括：

* `-p` 运行
* [Agent SDK](/docs/zh-CN/agent-sdk/overview) 应用程序
* [桌面应用](/docs/zh-CN/desktop)的 Code 标签页
* [VS Code 扩展](/docs/zh-CN/vs-code)的聊天面板
* [云端会话](/docs/zh-CN/claude-code-on-the-web)和 [Routine](/docs/zh-CN/routines)

对于无法在上述会话之一中运行的内置命令，Claude Code 仍会回复该命令不可用，而不是将其发送给 Claude。在 v2.1.274 之前，只有云端会话和 Routine 会将未匹配的名称发送给 Claude。在 v2.1.273 之前，它们也会回复 `Unknown command`。

Claude Code 不会将每个以 `/` 开头的提示词都视为命令。当 `/` 之后的第一个词以标点开头（例如开启 Lean 文档注释的 `/--`），或者是一个路径（例如 `/var/log/syslog`）时，它会将该提示词作为普通消息发送给 Claude。

在 v2.1.236 之前，如果在命令菜单列出与您输入的名称相近的匹配项时按下 `Enter`，Claude Code 会运行该匹配项，因此像 `/hepl` 这样的拼写错误会运行 `/help`，而不是产生此消息。

**解决方法：**

* 运行建议的名称，或输入 `/` 后跟名称的一部分，以查看此会话中可用的命令
* 如果 Claude Code 将文档中记载的命令报告为未知，请在[命令参考](/docs/zh-CN/commands)中查看其所在行列出的要求

<h3 id="diff-is-too-large-for-ultrareview">
  diff 过大，无法进行 ultrareview
</h3>

您的分支与基础分支之间的 diff（包括未提交和已暂存的更改）超出了 [ultrareview](/docs/zh-CN/ultrareview) 的大小限制，因此 `/code-review ultra` 和 `claude ultrareview` 子命令会在云端会话启动前拒绝审查。被拒绝的审查不会消耗免费次数，也不会计费使用额度。消息会指出生效的限制、您的 diff 大小，以及贡献最多更改行数的文件。在 v2.1.216 之前，消息只显示原始的 diff 统计信息。

```text theme={null}
Diff is too large for ultrareview: 812 files, 96,410 lines changed (limits: 500 files, 8,000 lines). Largest files: package-lock.json (41,904 lines), dist/bundle.js (18,210 lines), src/generated/api.ts (9,876 lines). Pass a closer base branch (`/code-review ultra <branch>`) to narrow the scope, or split the change.
```

审查 Pull Request 时适用相同的限制；该形式的消息以 `PR #<N> is too large for ultrareview` 开头，并指出该 PR 的文件数和行数。

**解决方法：**

* 传入一个更接近您工作的基础分支，例如 `/code-review ultra develop`，使审查仅覆盖相对于该分支的 diff
* 将更改拆分为更小的分支并分别审查。消息中指出的文件贡献了最多的更改行数，因此可以先将它们移到单独的分支中。

<h3 id="could-not-find-merge-base-with-the-base-branch">
  无法找到与基础分支的 merge-base
</h3>

`/code-review ultra` 和 `claude ultrareview` 子命令审查的是您的分支与基础分支之间的 diff，这需要两者共享一个提交。当 `git merge-base` 找不到共享提交时，Claude Code 会在云端会话启动前拒绝审查。在 Claude Code 能够验证是完整的、且至少有一个分支的克隆上，它会回退到[审查每个被跟踪的文件](/docs/zh-CN/ultrareview#diff-limits-and-fallbacks)，而不是拒绝。当根本找不到基础分支、Claude Code 无法验证您的克隆是否完整，或者在无法进行整棵树 diff 的少数仓库中（例如使用 SHA-256 对象格式的仓库），您会看到此拒绝信息。

```text theme={null}
Could not find merge-base with main. Pass the base branch explicitly (e.g. `/code-review ultra develop`) or make sure you're in a git repo with a main branch.
```

第一句之后的提示取决于 Claude Code 观察到的情况：

* **您没有传入基础分支**：Claude Code 与仓库的默认分支进行了比较，并建议您显式传入基础分支，如上例所示
* **您传入的基础分支已存在于您的克隆中**：提示为 ``Make sure <branch> exists locally or on origin (try `git fetch origin <branch>`)``
* **您传入的基础分支不在您的克隆中**：Claude Code 在比较前已从 origin fetch 了该分支。提示为 ``<branch> was fetched from origin but shares no history with HEAD. If another branch is your real base, pass it explicitly (`/code-review ultra <branch>`)``；当 Claude Code 无法判断您的克隆是否为浅克隆时，它会改为建议 `git fetch --unshallow origin`。在 v2.1.221 之前，对于每个被 fetch 的基础分支，提示都会建议 `git fetch --unshallow origin`，而在完整克隆上，该命令会以 `fatal: --unshallow on a complete repository does not make sense` 失败。

**解决方法：**

* 如果您真正的基础分支是另一个分支，请显式传入：`/code-review ultra <branch>`
* 如果您的克隆可能没有完整历史，请运行 `git fetch --unshallow origin` 并重新运行审查

<h3 id="your-checkout-has-no-branches">
  您的检出没有任何分支
</h3>

检出可能有提交却没有分支：如果您运行 `git init`，然后运行 `git fetch <url>` 和 `git checkout FETCH_HEAD`，就会得到一个没有任何引用的分离 HEAD。Claude Code 会将您的仓库打包为 git bundle 以上传用于 [ultrareview](/docs/zh-CN/ultrareview)，而它无法打包没有分支或其他引用的仓库，因此 `/code-review ultra` 和 `claude ultrareview` 子命令会在云端会话启动前拒绝审查。

```text theme={null}
Your checkout has no branches (detached HEAD only), which cloud review can't bundle. Create one first — `git checkout -b <name>` — then rerun /code-review ultra.
```

在 v2.1.221 之前，Claude Code 会尝试审查此检出中的每个被跟踪的文件，然后上传失败。

**解决方法：**

* 使用 `git checkout -b <name>` 在当前提交处创建一个分支，然后重新运行审查

<h3 id="no-github-account-is-connected-to-your-claude-account">
  您的 Claude 账户未连接 GitHub 账户
</h3>

您运行了 `/code-review ultra <PR#>` 或 `claude ultrareview <PR#>`，在创建云端会话之前，Claude Code 会询问服务器[连接到您 Claude 账户的 GitHub 账户](/docs/zh-CN/ultrareview#review-a-pull-request)是否能访问该 PR 的仓库。由于没有连接账户，或连接已过期，云端克隆将会失败，因此 Claude Code 拒绝启动。对于被拒绝的启动，Claude Code 不会消耗免费次数，也不会计费使用额度。

```text theme={null}
Ultrareview clones <owner>/<repo> in the cloud with the GitHub account connected to your Claude account, and none is connected (or the connection expired). To fix: run /web-setup to reuse your GitHub CLI login, or connect an account at https://claude.ai/connect-github — then re-run /code-review ultra 1234 (allow a minute after connecting).
```

当 [`/web-setup`](/docs/zh-CN/web-quickstart#connect-from-your-terminal) 在您的会话中不可用时，消息只会给出 claude.ai 链接。

**解决方法：**

* 运行 `/web-setup` 将您的 GitHub CLI 登录连接到您的 Claude 账户，或在 [claude.ai/connect-github](https://claude.ai/connect-github) 连接一个账户
* 连接后等待一分钟再重新运行审查

在 v2.1.248 之前，Claude Code 不会在启动前进行此检查。

<h3 id="your-connected-github-account-cant-see-the-repository">
  您连接的 GitHub 账户无法访问该仓库
</h3>

您运行了 `/code-review ultra <PR#>` 或 `claude ultrareview <PR#>`，而[连接到您 Claude 账户的 GitHub 账户](/docs/zh-CN/ultrareview#review-a-pull-request)无法读取该 PR 的仓库，因此云端克隆将会失败，Claude Code 拒绝启动。对于被拒绝的启动，Claude Code 不会消耗免费次数，也不会计费使用额度。

```text theme={null}
Your connected GitHub account can't see <owner>/<repo> — usually the Claude GitHub app isn't installed on <owner> or wasn't granted this repo (web-connected accounts need it for private repos), or a different GitHub account is connected. To fix: run /web-setup to reuse your GitHub CLI login, or install the app at https://github.com/apps/claude/installations/new — then re-run /code-review ultra 1234.
```

当 [`/web-setup`](/docs/zh-CN/web-quickstart#connect-from-your-terminal) 在您的会话中不可用时，消息只会给出应用安装方式。

**解决方法：**

* 如果您本地的 `gh` CLI 可以读取该仓库，请运行 `/web-setup` 将该登录连接到您的 Claude 账户
* 更改后重新运行审查

在 v2.1.248 之前，Claude Code 不会在启动前进行此检查。

<h3 id="the-github-app-preflight-failed-transiently">
  GitHub App 预检暂时失败
</h3>

您从本地仓库启动了一个[云端会话](/docs/zh-CN/claude-code-on-the-web)，而有两个步骤同时失败。Claude Code 无法构建或上传您仓库的 bundle。在上传之前，它检查了云服务能否从 GitHub 克隆该仓库，而该检查没有得到明确答复，而是以一个可通过重试消除的错误结束，例如网络错误、超时或临时服务器错误。完整消息以导致 bundle 失败的原因开头，例如 `Could not upload repo bundle (<error>)`，并以预检相关的句子结尾：

```text theme={null}
Could not upload repo bundle (<error>). The GitHub App preflight failed transiently (network or service hiccup) — retry in a moment to start from GitHub instead
```

**解决方法：**

* 稍后重新运行该命令。当 GitHub 检查通过时，Claude Code 可以从 GitHub 克隆启动会话，因此失败的上传不再阻止启动
* 如果重试持续失败，消息开头会指出导致上传失败的原因。如果该原因是您可以修复的，请修复它，使会话可以改为从您的本地仓库启动

在 v2.1.251 之前，即使 GitHub 检查只是暂时失败，Claude Code 也会以 `Please set up GitHub on https://claude.ai/code` 结束消息，而设置建议无法消除暂时性故障。

<h3 id="the-repository-upload-cant-follow-a-git-setting">
  仓库上传无法遵循某个 git 设置
</h3>

您启动了一个[上传本地仓库的云端会话](/docs/zh-CN/claude-code-on-the-web#send-local-repositories-without-github)，或对某个分支进行 [ultrareview](/docs/zh-CN/ultrareview)，而上传无法遵循用于决定哪些属性规则适用于您文件的某个 git 设置。如果上传继续进行并遗漏了某条规则，那么 git 在存储前会转换的文件（例如由 clean 过滤器加密的文件）可能会以其在磁盘上的原样上传到云端。因此 Claude Code 会拒绝上传，不会上传任何内容：

```text theme={null}
Not uploading this working tree: core.ignoreCase (which decides whether .gitattributes patterns match file names regardless of letter case) is set in <file>, and the upload cannot follow that setting, so a file git would change before storing it (to encrypt it, for example) could be uploaded as it is on disk. Move the core.ignoreCase line into this repository’s .git/config or directly into your ~/.gitconfig, then retry.
```

消息会指出该设置及其所在位置，并以适用于您所遇情况的解决方法结尾。对于 `core.attributesFile` 和 `attr.tree`，也会出现相同的拒绝信息，各自附带其对应的解决方法。

消息中指出的可能是您的 git 配置通过 `include` 或 `includeIf` 指令引入的配置文件，即使该指令的条件并不适用于此仓库。

**解决方法：**

* 按照消息最后一句中的解决方法操作

<h3 id="github-isnt-connected-to-your-claude-account">
  GitHub 未连接到您的 Claude 账户
</h3>

您从本地仓库启动了一个[云端会话](/docs/zh-CN/claude-code-on-the-web)，例如使用 `/autofix-pr`。您的 Claude 账户没有连接 GitHub 账户，或连接已过期，因此 Claude Code 拒绝启动：

```text theme={null}
GitHub isn't connected to your Claude account, so this repository can't be cloned in the cloud. Run /web-setup to connect with your GitHub CLI login, or connect on the web at https://claude.ai/connect-github
```

当您使用 [`/schedule`](/docs/zh-CN/routines) 创建 Routine 时，同样的消息会以指出该仓库的设置说明形式出现；该说明不会阻止创建 Routine。

**解决方法：**

* 运行 `/web-setup` 将您的 GitHub CLI 登录连接到您的 Claude 账户，或在 [claude.ai/connect-github](https://claude.ai/connect-github) 连接一个账户。有关两者的区别，请参阅 [GitHub 身份验证选项](/docs/zh-CN/claude-code-on-the-web#github-authentication-options)。
* 连接后等待一分钟再重新运行该命令

在 v2.1.268 之前，Claude Code 会将此报告为 Claude GitHub App 检查的暂时性失败，并建议重试或安装该应用；但这两种做法都不会连接 GitHub 账户。

<h3 id="a-github-organization-policy-is-blocking-claude">
  GitHub 组织策略阻止了 Claude
</h3>

您在 Claude Code 提示符下运行了一个会启动云端会话的命令，例如 [`/autofix-pr`](/docs/zh-CN/claude-code-on-the-web#auto-fix-pull-requests)。在创建会话之前，Claude Code 会检查 Claude 对 GitHub 上该仓库的访问权限，而 GitHub 拒绝了访问，因为您的 GitHub 组织有一项阻止 Claude 的策略。Claude Code 会就此停止，并显示一条指明该策略的消息。

当阻止访问的是 IP 允许列表时，消息内容为：

```text theme={null}
Your GitHub organization has an IP allowlist that is blocking Claude. Add Claude's IP ranges to your GitHub allowlist.
```

当阻止访问的是单点登录时，消息内容为：

```text theme={null}
Your GitHub organization requires single sign-on. Disconnect and reconnect GitHub on the Connectors page in Claude on the web, click Authorize next to your organization when GitHub asks, then try again.
```

当阻止访问的是 Microsoft Entra ID 条件访问策略时，消息内容为：

```text theme={null}
Your GitHub organization's identity provider (Microsoft Entra ID) has a Conditional Access policy that is blocking Claude. Ask your GitHub Enterprise or Entra ID admin to allow Claude in that policy.
```

**解决方法：**

* **IP 允许列表**：请您的 GitHub 组织或企业的所有者放行 Anthropic 的出站 IP 地址。有关这些地址以及需要更改的 GitHub 设置，请参阅 [GitHub 允许列表和防火墙](/docs/zh-CN/network-config#github-allow-lists-and-firewalls)。
* **单点登录**：在 [claude.ai/customize/connectors](https://claude.ai/customize/connectors) 断开 GitHub 连接，然后重新连接。当 GitHub 询问时，点击您的组织旁边的 **Authorize**，使新连接获得该组织单点登录的授权。
* **条件访问策略**：请您的 GitHub Enterprise 或 Microsoft Entra ID 管理员在该策略中放行 Claude
* 完成更改后，再次运行该命令

<h3 id="single-sign-on-authorization-needed">
  需要单点登录授权
</h3>

您运行了 [`/install-github-app`](/docs/zh-CN/github-actions#quick-setup)，并选择了一个所属组织强制执行 SAML 单点登录的仓库。在设置之前，Claude Code 会使用 GitHub CLI 检查您对该仓库的访问权限，而 GitHub 拒绝了该检查，因为您的 `gh` 令牌尚未获得该组织的授权。向导会显示警告以及授权步骤：

```text theme={null}
Single sign-on authorization needed
<owner>/<repo> belongs to an organization that enforces SAML single sign-on, and your GitHub CLI token isn't authorized for it yet.
```

**解决方法：**

* 运行 `gh auth refresh -h github.com -s repo,workflow`，以 `repo` 和 `workflow` 作用域重新授权您的 GitHub CLI 登录，并在 GitHub 提示单点登录时授权该组织
* 如果您使用 `GH_TOKEN` 中的个人访问令牌进行身份验证，请打开 [github.com/settings/tokens](https://github.com/settings/tokens)，在该令牌上选择 **Configure SSO**，然后授权该组织
* 再次运行 `/install-github-app`

在 v2.1.273 之前，Claude Code 在这种情况下显示的是 `Admin permissions required` 警告。

<h3 id="failed-to-resume-the-conversation">
  无法恢复对话
</h3>

Claude Code 无法读取或处理您从 [`claude --resume` 选择器](/docs/zh-CN/sessions#use-the-session-picker)中选择的会话的已保存会话记录，因此它会结束进程，而不是在部分加载的状态下继续运行。消息中包含用于重试的命令：

```text theme={null}
Failed to resume the conversation.
Run claude --resume <session-id> to retry, or claude to start a new session.
```

显示该消息后，Claude Code 以退出码 1 退出。而在运行中的会话内使用 `/resume` 选择器时，则会在对话中报告 `Failed to resume conversation`，您当前的会话会继续运行。在 v2.1.216 之前，从 `claude --resume` 选择器恢复失败时，会一直停留在 `Resuming conversation…` 加载动画上，而不是显示此消息。

**解决方法：**

* 使用消息中的会话 ID 运行 `claude --resume <session-id>` 进行重试
* 在 v2.1.285 之前的版本中，如果重试以同样的方式失败，请运行 `claude update` 后再次恢复。当已保存的会话记录包含这些版本无法读取的条目时，这些版本会恢复失败。
* 如果重试再次失败，请运行 `claude` 开始新会话

<h3 id="no-conversation-found-with-the-session-id">
  未找到具有该会话 ID 的对话
</h3>

您向 `claude --resume <session-id>` 传入了一个会话 ID，但没有匹配的已保存会话记录：

```text theme={null}
No conversation found with session ID: <session-id>
```

显示该消息后，Claude Code 以退出码 1 退出。Claude Code 会[先搜索当前项目，然后搜索这台机器上的所有其他项目](/docs/zh-CN/sessions#resume-a-session)来查找该 ID。在 v2.1.223 之前，查找仅限于当前项目目录及其 git worktree，因此需要从该会话最后工作的目录中进行恢复。

常见原因：

* **ID 输入错误**：对于非交互式运行，ID 是 [`--output-format json` 输出](/docs/zh-CN/headless#get-structured-output)中的 `session_id` 字段
* **会话记录已删除**：Claude Code 会在[保留期](/docs/zh-CN/sessions#where-transcripts-are-stored)（默认 30 天）结束后按照[保留清理规则](/docs/zh-CN/claude-directory#cleaned-up-automatically)删除会话记录
* **不同的机器**：Claude Code 将会话记录存储在本地，因此请在运行该会话的机器上恢复它
* **重复副本**：如果您在 `~/.claude/projects` 下复制了项目目录，导致两份会话记录带有相同的 ID，Claude Code 会报告此消息，而不是任意恢复其中一份

**解决方法：**

* 对于交互式会话，使用 `claude --resume` 打开[会话选择器](/docs/zh-CN/sessions#use-the-session-picker)，按 `Ctrl+A` 将其范围扩大到这台机器上的所有项目，然后选择该会话
* 使用 `claude -p` 或 [Agent SDK](/docs/zh-CN/agent-sdk/overview) 创建的会话不会出现在选择器中，因此请对照您最初运行时输出的 `session_id` 重新检查 ID

<h3 id="windows-reported-an-error-ebadf">
  Windows reported an error (EBADF) when Claude Code read this session's transcript file
</h3>

您在 Windows 上恢复了一个会话，其已保存的[会话记录文件](/docs/zh-CN/sessions#where-transcripts-are-stored)正常打开，但随后读取时因系统错误 EBADF 而失败。该系统错误并未说明读取失败的原因，因此消息会提示可能的原因以及可以尝试的操作：

```text theme={null}
Windows reported an error (EBADF) when Claude Code read this session's transcript file, although the file had opened normally. This can happen when other software intercepts file reads — security, encryption or endpoint-management tools, for example. If it keeps happening for this conversation, try excluding the folder that holds Claude Code's session transcripts from such software (the .claude folder in your user profile, unless the app or CLAUDE_CONFIG_DIR points Claude Code elsewhere), or adding Claude Code to its allowed applications, then resume again.
```

该消息跟在命令自身的失败行之后，例如 `Failed to resume session <session-id>`。`claude --resume` 或 [`claude -p`](/docs/zh-CN/headless) 命令在显示该消息后以退出码 1 退出。在会话内使用 `/resume` 后，您当前的会话会继续运行。

**解决方法：**

* 在扫描或拦截文件读取的软件（例如安全、加密或终端管理工具）中排除存放会话记录的文件夹。会话记录默认位于 `%USERPROFILE%\.claude\projects` 下，或位于 [`CLAUDE_CONFIG_DIR`](/docs/zh-CN/env-vars) 指定的目录下
* 如果无法添加排除项，请改为将 Claude Code 添加到该软件的允许应用程序中
* 再次恢复该会话

在 v2.1.282 之前，失败时没有任何说明：`claude --resume <session-id>` 以 `Failed to resume session <session-id>` 结束，而 `-p` 运行只输出系统错误文本，例如 `Failed to resume session: EBADF: bad file descriptor, read`。

<h3 id="cannot-switch-renderers-in-this-session">
  无法在此会话中切换渲染器
</h3>

切换渲染器时，Claude Code 会重启其进程。您在一个 Claude Code 拒绝重启的会话中运行了 [`/tui`](/docs/zh-CN/fullscreen#enable-fullscreen-rendering)，因此它不会切换，也不会保存任何内容。您看到的消息会指明原因：

* `Cannot switch renderers while work is running in the background`：您有正在后台运行的工作，重启会使其被放弃，例如后台 shell 或子代理。请等待工作完成或使用 [`/tasks`](/docs/zh-CN/commands) 停止它，然后再次运行 `/tui fullscreen` 或 `/tui default`
* `Cannot switch renderers in this session`：该会话带有 Claude Code 无法传递给重启后进程的限制。在 v2.1.234 之前，Claude Code 仍会重启，而重新启动的会话将不带这些限制运行

在限制消息中，括号内的部分指明了 Claude Code 发现的限制：

```text theme={null}
Cannot switch renderers in this session — it has restrictions a restart can't carry over (permission rules set for this session only). Nothing was changed. Running /tui fullscreen in a session started without them switches every later session too.
```

消息括号中可能显示的各项原因：

* `launch flags: a custom system prompt, a tool allowlist, or restricted settings`：您启动会话时使用了 Claude Code 不会传回给重启后进程的标志。这些标志包括 [`--system-prompt`](/docs/zh-CN/cli-reference#cli-flags)、`--system-prompt-file`、`--append-system-prompt-file`、[`--tools`](/docs/zh-CN/cli-reference#cli-flags) 允许列表、[`--setting-sources`](/docs/zh-CN/cli-reference#cli-flags) 和 [`--permission-prompt-tool`](/docs/zh-CN/cli-reference#cli-flags)
* `permission rules set for this session only`：来自 hook 或 SDK 调用方的[权限更新](/docs/zh-CN/hooks#permission-update-entries)添加了目标为 `session` 的拒绝或询问规则。会话作用域的允许规则不会触发拒绝。重启会丢弃这些规则，Claude Code 会改为再次提示
* `ask-before-running rules with no command-line form`：来自 hook 或 SDK 调用方的权限更新在 Claude Code 以 `--allowed-tools` 和 `--disallowed-tools` 传回的规则之外，还添加了询问规则。询问规则没有对应的标志
* `permission rules a command line cannot carry intact` 和 `added directories a command line cannot carry intact`：权限更新在会话中途添加了规则或目录路径。重启后进程的命令行无法将其文本作为相同的值传递

**解决方法：**

* 在不带这些限制启动的会话中运行 `/tui fullscreen`，或运行 `/tui default` 切换回来。Claude Code 会在那里保存 [`tui` 设置](/docs/zh-CN/settings-reference#tui)

<h3 id="couldnt-open-claude-desktop">
  无法打开 Claude Desktop
</h3>

您在会话中运行了 [`/desktop`](/docs/zh-CN/desktop#coming-from-the-cli) 或其别名 `/app`，或在 shell 中运行了 [`claude --desktop`](/docs/zh-CN/cli-reference#cli-flags)，而 Claude Code 用于打开 Claude Desktop 的系统命令失败了。运行 `/desktop` 后，会话会留在终端中；`claude --desktop` 会输出不带 `Error:` 前缀的消息，并以状态 1 退出。

括号中的文本指明了失败的命令，如果该命令产生了退出状态和错误输出，还会附上其退出状态和错误输出的第一行。在 macOS 上该命令是 `open`，如下例所示；在 Windows 上是 `rundll32`：

```text theme={null}
Error: Couldn't open Claude Desktop (`open` exited 1: LSOpenURLsWithRole() failed for the URL claude://resume?session=<session-id> with error -10814). Open Claude Desktop and try again.
```

**解决方法：**

* 手动打开 Claude Desktop，然后再次运行 `/desktop` 或 `claude --desktop`
* 要查看失败命令的完整错误输出，请使用 `/debug` 启用调试日志并再次运行 `/desktop`，或运行 `claude --desktop --debug-file <path>`，然后查看调试日志

在 v2.1.285 之前，消息以 `Open Claude Desktop and run /desktop again.` 结尾。在 v2.1.275 之前，消息为 `Failed to open Claude Desktop. Please try opening it manually.`，且不会说明失败的内容。

<h3 id="terminal-setup-left-your-zed-keymap-unchanged">
  /terminal-setup 未更改您的 Zed 键位映射
</h3>

您在 Zed 中运行了 [`/terminal-setup`](/docs/zh-CN/terminal-config#enter-multiline-prompts)，而 Claude Code 无法完成对您的 Zed `keymap.json` 的更新，因此保持该文件原样不变。

每条消息都会指明您的键位映射文件路径，并在末尾附上需要您自行添加的快捷键块：

```text theme={null}
Couldn't update your Zed keymap, so it was left unchanged.
To add the binding yourself, add this block to the keymap array in <path to keymap.json>:
{ "context": "Terminal", "bindings": { "shift-enter": ["terminal::SendText", "\u001b\r"] } }
```

消息的第一行指明了原因：

* `Couldn't read your Zed keymap, so it was left unchanged.`：Claude Code 无法读取该文件，例如由于文件权限问题
* `Your Zed keymap isn't a readable list of keybindings, so it was left unchanged.`：文件可以正常读取，但即使允许 `//` 注释和尾随逗号，也无法解析为快捷键块数组
* `Couldn't back up your Zed keymap; not modifying it.`：Claude Code 无法将该文件复制为其旁边的 `.bak` 备份，因此未做任何更改
* `Couldn't update your Zed keymap, so it was left unchanged.`：合并后的结果未能验证为包含该快捷键的有效键位映射，因此 Claude Code 将其丢弃而未写入。包含重复键的快捷键块可能导致这种情况

**解决方法：**

* 将消息中的块复制到消息所指明路径下 `keymap.json` 的顶层数组中
* 对于 `isn't a readable list of keybindings`，请修复语法错误，或将文件的顶层值改为数组，然后再次运行 `/terminal-setup`

在 v2.1.247 之前，`/terminal-setup` 无法解析使用了 `//` 注释或尾随逗号的 Zed 键位映射，它会用仅包含自身快捷键的内容替换整个文件，同时报告快捷键已安装。要恢复被早期版本替换的键位映射，请使用[输入多行提示词](/docs/zh-CN/terminal-config#enter-multiline-prompts)中所述的 `.bak` 备份文件。

<h3 id="skill-usage-reports-are-not-available-on-this-connection">
  此连接不支持 skill 使用情况报告
</h3>

您通过 [Remote Control](/docs/zh-CN/remote-control) 从手机或浏览器运行了 [`/skill-doctor`](/docs/zh-CN/skills#find-unused-skills)。Claude Code 不会通过 Remote Control 发送 skill 使用情况报告，而是回复以下消息：

```text theme={null}
Skill usage reports are not available on this connection.
```

**解决方法：**

* 在运行该会话的机器的终端中运行 `/skill-doctor`，或在该机器上运行 `claude -p "/skill-doctor"`

<h3 id="custom-output-styles-cant-be-selected-over-remote-control">
  无法通过 Remote Control 选择自定义输出样式
</h3>

您通过 [Remote Control](/docs/zh-CN/remote-control) 从移动应用或网页运行了 [`/output-style`](/docs/zh-CN/output-styles#change-your-output-style)，或者该命令出现在转发到会话中的消息里。由于这样的轮次可能并非来自账户所有者，Claude Code 在其中只会列出和选择[内置样式](/docs/zh-CN/output-styles#built-in-output-styles)，并且每当该命令列出样式或无法识别您提供的名称时，都会附加此通知。[自定义样式](/docs/zh-CN/output-styles#create-a-custom-output-style)名称得到的回复与不存在的名称相同：

```text theme={null}
Custom output styles can't be selected over Remote Control or from a relayed message. Select one in the session itself, or pick a built-in style here.
```

**解决方法：**

* 选择一个内置样式，例如 `/output-style concise`
* 要使用自定义样式，请在项目的 `.claude/settings.local.json` 中设置 [`outputStyle`](/docs/zh-CN/settings-reference#outputstyle)，或者如果会话有自己的终端，请在该终端中运行 `/output-style <style>`

<h3 id="output-styles-are-saved-to-local-settings-which-this-session-doesnt-load">
  输出样式保存在此会话不加载的本地设置中
</h3>

您在一个设置来源不包含 `local` 的会话中尝试使用 `/output-style <style>` 或 `/config outputStyle=<style>` 切换[输出样式](/docs/zh-CN/output-styles)。例如，[`settingSources`](/docs/zh-CN/agent-sdk/typescript#options) 省略了 `"local"` 的 [Agent SDK](/docs/zh-CN/agent-sdk/typescript) 会话，以及使用省略了 `local` 的 [`--setting-sources`](/docs/zh-CN/cli-reference#cli-flags) 值启动的 CLI 会话。这两个命令都会将样式保存到 `.claude/settings.local.json`，而这类会话永远不会读回该文件，因此 Claude Code 会拒绝操作，而不是写入一个不会生效的设置：

```text theme={null}
Output styles are saved to local settings (.claude/settings.local.json), which this session doesn't load, so the style can't be changed here.
```

**解决方法：**

* 将 `local` 添加到会话的设置来源中，然后再次切换
* 在会话确实会加载的设置文件中设置 [`outputStyle`](/docs/zh-CN/settings-reference#outputstyle) 键，例如项目中的 `.claude/settings.json` 或 `~/.claude/settings.json`。在 TypeScript SDK 中，请改为在内联 `settings` 对象中设置 `outputStyle`；请参阅[激活输出样式](/docs/zh-CN/agent-sdk/modifying-system-prompts#activate-an-output-style)

<h3 id="recap-only-runs-when-you-ask-for-it-yourself">
  /recap 仅在您亲自请求时运行
</h3>

该 [`/recap`](/docs/zh-CN/interactive-mode#session-recap) 请求并非来自您自己的输入。它出现在从 Slack、Teams 或[项目](/docs/zh-CN/claude-projects)线程转发到会话中的消息里，或出现在 [Routine](/docs/zh-CN/routines) 或其他程序发送的提示词中。

即使转发的消息是您本人撰写的，也会收到此通知。Claude Code 无法判断转发或自动化的消息是否来自运行该会话的账户所有者，因此会以此通知代替摘要进行回复：

```text theme={null}
/recap only runs when you ask for it yourself in this session: from the terminal, the Claude app or claude.ai/code, or over Remote Control. A message relayed from Slack, Teams or a project thread, or sent by a routine or another program, can't request it.
```

传给 `claude -p` 的 `/recap`，或您自己的 [Agent SDK](/docs/zh-CN/agent-sdk/overview) 应用程序向其启动的会话发送的 `/recap`，都算作您自己的输入。

**解决方法：**

* 亲自打开该会话并在其中运行 `/recap`：在其终端中、在 [Desktop 应用](/docs/zh-CN/desktop)或[移动应用](/docs/zh-CN/mobile)中、在 [claude.ai/code](https://claude.ai/code) 上，或通过 [Remote Control](/docs/zh-CN/remote-control)
* 如果是 Routine 或其他程序发送的，请从该提示词中删除 `/recap`

<h2 id="plugin-errors">
  插件错误
</h2>

这些错误来自[插件](/docs/zh-CN/plugins/overview)和[marketplace](/docs/zh-CN/plugins/overview)配置。对于不会产生此页面上的消息之一的插件问题，例如无法加载的 marketplace URL 或已安装但未显示的插件，请参阅[插件故障排除](/docs/zh-CN/plugins/troubleshooting)。

<h3 id="plugin-eval-is-currently-in-early-access">
  plugin eval 目前处于早期访问阶段
</h3>

您运行了[`claude plugin eval`](/docs/zh-CN/plugin-evals)或`claude plugin eval init`，它在执行任何操作之前以退出代码 1 和以下消息之一退出：

```text theme={null}
`plugin eval` is currently in early access
```

```text theme={null}
`plugin eval` is currently unavailable
```

第一条消息表示您的构建版本早于 v2.1.269，这是该命令正式发布的第一个版本。第二条消息表示 Anthropic 已在服务器端关闭了该命令；您的机器上没有任何东西可以将其重新打开。

**要做什么：**

* 运行`claude --version`，然后运行`claude update`，并在新会话中再次运行该命令。请参阅[插件 evals 的要求](/docs/zh-CN/plugin-evals#requirements)
* 如果您在当前构建上看到第二条消息，请在另一次`claude update`后稍后重试

<h3 id="marketplace-is-registered-from-an-untrusted-source">
  Marketplace 从不受信任的来源注册
</h3>

marketplace 注册在一个名称下，该名称是[为官方 Anthropic marketplaces 保留的](/docs/zh-CN/plugins/marketplace-reference#marketplace-file)，但其注册来源不是`anthropics` GitHub 存储库。Claude Code 每次加载或刷新 marketplace 时都会重新检查保留的名称，因此 marketplace 及从中安装的插件停止加载。在 v2.1.205 之前，在其名称被保留之前注册的条目继续加载。

```text theme={null}
Marketplace "claude-community" is registered from an untrusted source: The name 'claude-community' is reserved for official Anthropic marketplaces. Only repositories from 'github.com/anthropics/' can use this name. To fix it, remove the marketplace and re-add it from the official source.
```

对于来源不是 GitHub 存储库或 Git URL 的 marketplace，例如本地目录，中间句子改为`can only be used with GitHub sources from the 'anthropics' organization`。`claude plugin marketplace add`运行相同的检查，并拒绝保留的名称，返回`Failed to add marketplace:`后跟相同的保留名称句子。

**要做什么：**

* 如果 marketplace 已注册，运行`claude plugin marketplace remove <name>`，然后从官方`github.com/anthropics`存储库重新添加它
* 如果您发布了在名称被保留之前使用该名称的第三方 marketplace，请重命名它并要求用户从您的来源重新添加它
* 请参阅[Marketplace schema](/docs/zh-CN/plugins/marketplace-reference#marketplace-file)下的保留名称列表

<h3 id="marketplace-name-is-another-spelling-of-a-reserved-name">
  Marketplace 名称是保留名称的另一种拼写
</h3>

marketplace 的名称本身不是保留名称，但 Claude Code 将其视为保留名称的另一种拼写。[保留名称](/docs/zh-CN/plugins/marketplace-reference#reserved-name-spellings)列出了哪些拼写算作保留名称。当您添加 marketplace 时，Claude Code 拒绝这样的名称：

```text theme={null}
Failed to add marketplace: "claude.code.plugins" is another spelling of "claude-code-plugins", a reserved marketplace name.
```

当 marketplace 已在这样的名称下注册时，其条目停止加载，`/plugin`、`claude plugin install`和`claude plugin update`警告：

```text wrap theme={null}
known_marketplaces.json has an entry named "claude.code.plugins", another spelling of the reserved marketplace name "claude-code-plugins", so it is ignored. Remove it with: claude plugin marketplace remove claude.code.plugins
```

当名称需要 shell 引用时，添加时的拒绝读作`This marketplace's name is another spelling of "<reserved>", a reserved marketplace name. It is not exactly the reserved name it appears to be.`

**要做什么：**

* 将 marketplace 重命名为不拼写保留名称的名称，然后重新添加它
* 对于忽略的条目警告，运行它给出的`claude plugin marketplace remove`命令，或从`~/.claude/plugins/known_marketplaces.json`中删除该条目

<h3 id="claude-code-refuses-the-marketplace-name">
  Claude Code 拒绝 marketplace 名称
</h3>

已注册的 marketplace 的名称[冒充官方 Anthropic marketplace](/docs/zh-CN/plugins/marketplace-reference#reserved-names)，违反了该部分列出的规则。

如果 marketplace 在这样的名称下注册时检查阻止了它，marketplace 及从中安装的插件停止加载，因为 Claude Code 每次读取 marketplace 的目录时都会检查名称。当名称模仿官方名称时，`claude plugin list`和`/plugin`**Errors**选项卡报告每个受影响的插件，消息开头为：

```text theme={null}
Claude Code refuses the marketplace name "anthropic-plugins-v2"
```

对于模仿名称，marketplace 自己的错误读作`Claude Code refuses this marketplace's name: it looks like one of Anthropic's own`。`claude plugin marketplace add`拒绝任何冒充名称，返回`Marketplace name impersonates an official Anthropic/Claude marketplace`。

在 v2.1.282 之前，`claude plugin list`和`/plugin`报告模仿名称的插件加载失败，但没有将 marketplace 的名称命名为原因。

**要做什么：**

* 运行`claude plugin marketplace remove <name>`。这也会卸载从 marketplace 安装的插件并删除其保存的数据
* 要保留 marketplace，请等待其维护者重命名它，然后运行`claude plugin marketplace update <name>`
* 如果您发布 marketplace，在您的`marketplace.json`中重命名它；用户随后更新 marketplace 而不是删除它

<h3 id="marketplace-is-already-added-from-a-different-source">
  Marketplace 已从不同的来源添加
</h3>

您在会话中或从 shell 中，通过[安装命令上的`--marketplace <source>`](/docs/zh-CN/plugins/install#add-a-marketplace-and-install-in-one-command)指定了一个新的市场来源。Claude Code 从该来源获取的目录与您已从不同来源添加的市场同名。Claude Code 保留现有的市场而不是替换它，插件未安装。

```text theme={null}
Marketplace "acme-tools" is already added from a different source (github:acme/plugins). To use this source instead, remove that marketplace first with /plugin marketplace remove acme-tools.
```

**要做什么：**

* 如果您已添加的 marketplace 是您想要的，按名称从中安装：`/plugin install <plugin>@<name>`
* 要切换到新来源，运行`/plugin marketplace remove <name>`，然后重试安装

<h3 id="plugin-command-references-user-config">
  插件命令在 shell 命令中引用 user\_config
</h3>

插件 hook、[monitor](/docs/zh-CN/plugins/components#monitors)或 MCP [`headersHelper`](/docs/zh-CN/mcp#use-dynamic-headers-for-custom-authentication)命令引用`${user_config.KEY}` [插件选项](/docs/zh-CN/plugins/manifest-reference#user-configuration)，替换后的字符串将被传递到 shell。配置的值包含`$(...)` 、反引号或`;`会在那里作为代码运行，因此 Claude Code 拒绝启动该组件而不是替换该值。检查在命令模板上运行，因此即使尚未配置任何值，错误也会出现。在 v2.1.207 之前，该值被替换到 shell 命令中。

措辞取决于哪个界面引用了该选项。shell 形式的 hook 报告：

```text theme={null}
Hook from plugin formatter@acme-tools references ${user_config.*} in a shell-form command. The substituted value would be re-parsed by the shell. Use exec form instead — {"command": "<executable>", "args": ["${user_config.KEY}", ...]} — or read $CLAUDE_PLUGIN_OPTION_<KEY> from the hook's environment. Command: ./scripts/notify.sh ${user_config.webhook_url}
```

monitor 报告：

```text theme={null}
Monitor "deploy-status" from plugin deploy-tools references ${user_config.*} in its command. The substituted value would be passed to a shell. Monitor commands cannot safely reference ${user_config.*}; have the monitor script read the value from a config file or prompt instead.
```

MCP `headersHelper`报告：

```text theme={null}
headersHelper for MCP server 'internal-api' references ${user_config.*}. The substituted value would be passed to a shell; read the value inside the helper script instead (e.g. from an env var set in the server's "env" block).
```

**要做什么：**

* 对于 hook，添加`args`数组使其以[exec 形式](/docs/zh-CN/hooks#exec-form-and-shell-form)运行，其中每个`${user_config.KEY}`成为一个参数，中间没有 shell。或删除引用并读取脚本内的`$CLAUDE_PLUGIN_OPTION_<KEY>`环境变量
* 对于 monitor，删除引用并让 monitor 脚本从配置文件读取该值
* 对于`headersHelper`，将`${user_config.KEY}`移到服务器的`headers`字段中，该字段不被 shell 解析，或在 helper 脚本内读取该值

<h3 id="plugin-archive-integrity-check-failed">
  插件存档完整性检查失败
</h3>

插件的 marketplace 条目使用带有`sha256`引脚的[`archive`源](/docs/zh-CN/plugins/marketplace-reference#archive-plugin-source)，下载文件的摘要与引脚不匹配。Claude Code 拒绝安装，因此插件缓存中没有任何更改。不匹配有三个可能的原因：

* 作者计算引脚后 URL 处的文件已更改
* 作者在 marketplace 条目中输入了错误的摘要
* URL 提供的文件与作者引脚的文件不同

```text theme={null}
Plugin archive integrity check failed for https://artifacts.example.com/claude-plugins/my-plugin.zip: expected sha256 6bfa50e3d2e00c052b46abe51fff89346ac803e45771f76dcf6df1ab74cca5e1, got ac52220c0914ef8ca6a602e4a7362f88d30fb021110f72a6d15b68c3fe7df2b7. The archive was not installed. Verify the sha256 in the marketplace entry, or that the URL serves the intended file.
```

**要做什么：**

* 如果您发布插件，重新计算 URL 提供的确切文件的摘要，例如使用`shasum -a 256 my-plugin.zip`或在 PowerShell 中使用`Get-FileHash -Algorithm SHA256 my-plugin.zip`，并更新 marketplace 条目中的`sha256`
* 如果您安装插件，运行`/plugin marketplace update <name>`以刷新目录以防条目已更正，然后重试安装
* 如果刷新后摘要仍然不一致，请在安装前询问 marketplace 所有者他们引脚的是哪个文件

<h3 id="path-escapes-plugin-directory">
  路径逃逸插件目录
</h3>

插件组件路径在插件的`plugin.json`或其[marketplace 条目](/docs/zh-CN/plugins/marketplace-reference#plugin-entries)中声明，解析到插件自己目录之外。Claude Code 删除该路径并加载插件的其余部分。消息中的组件名称（例如`commands`或`hooks`）命名声明路径的字段。

```text theme={null}
commands path escapes plugin directory: ./../shared.md
```

在`claude plugin`命令输出中，相同的错误读作`Path escapes plugin directory: ./../shared.md (commands)`。

Claude Code 拒绝指向插件外部的路径（如`../shared-utils`）和导致插件外部的符号链接，[marketplace 符号链接规则](/docs/zh-CN/plugins/host-marketplace#share-files-within-a-marketplace-with-symlinks)不允许的符号链接。对于符号链接，消息还说明路径解析的位置：

```text theme={null}
commands path escapes plugin directory: ./commands/deploy.md — it resolves to /home/user/shared/deploy.md, outside the plugin directory
```

在 macOS 和 Linux 上，Claude Code 也拒绝包含反斜杠的组件路径，即使路径保留在插件内。使用 Windows 风格分隔符的组件路径的插件在 Windows 上加载并在其他平台上触发此拒绝：

```text theme={null}
commands path escapes plugin directory: ./commands\deploy.md — its path contains a backslash, which is not resolved reliably on this platform
```

在 v2.1.251 之前，Claude Code 加载在 marketplace 条目中声明的`commands`路径，即使它指向插件目录之外。

在 v2.1.257 之前，检查仅查看路径的拼写，而不是符号链接导向的位置。

**要做什么：**

* 将引用的文件移到插件目录内，并使用`./`相对路径指向它
* 如果路径是指向插件外部文件的符号链接，用文件副本替换符号链接
* 如果消息说路径包含反斜杠，用正斜杠写路径，例如`./commands/deploy.md`
* 要与同一 marketplace 中的其他插件共享文件，使用插件目录内的符号链接链接它们，遵循[符号链接规则](/docs/zh-CN/plugins/host-marketplace#share-files-within-a-marketplace-with-symlinks)

<h3 id="path-could-not-be-checked">
  路径无法检查
</h3>

Claude Code 询问操作系统插件路径是否存在，并收到"未找到"以外的错误，因此它不加载路径命名的内容。插件加载多少取决于哪个路径失败：

* 插件的[默认组件位置](/docs/zh-CN/plugins/manifest-reference#standard-layout)之一，例如`skills/`文件夹、`monitors/monitors.json`文件或[插件根目录的`SKILL.md`](/docs/zh-CN/plugins/components#skills)：插件的其他组件仍然加载
* 插件自己的目录：该插件中没有任何内容加载

对于根本不存在的路径，您看不到此错误。在`/plugin`中，错误出现在插件下方，并命名路径和操作系统返回的代码：

```text theme={null}
skills path could not be checked: /home/user/my-plugin/skills (ELOOP)
```

在`claude plugin list`中，相同的错误读作`Path not found: /home/user/my-plugin/skills (skills, ELOOP)`。

产生此错误的原因包括：

* `ELOOP`：路径中的符号链接指向自己或形成循环
* `EIO`或`ESTALE`：路径在损坏或陈旧的网络挂载上
* `EACCES`：路径上方的目录之一拒绝您遍历它的权限

**要做什么：**

* 用真实文件夹替换指向自己的符号链接，或删除它
* 如果路径在网络挂载上，重新挂载共享
* 如果代码是`EACCES`，恢复您对路径上方目录的执行权限
* 修复路径后运行`/reload-plugins`，或重启 Claude Code，以加载插件或组件

在 v2.1.265 之前，Claude Code 将无法检查的默认组件文件夹视为不存在，并加载没有该组件的插件，没有错误。

<h3 id="marketplace-entry-path-does-not-stay-inside-the-marketplace-directory">
  Marketplace 条目路径不保留在 marketplace 目录内
</h3>

插件的[marketplace 条目](/docs/zh-CN/plugins/marketplace-reference#plugin-entries)声明了一个源路径，Claude Code 无法将其解析到 marketplace 自己目录内的位置，因此插件不安装或加载。拒绝涵盖：

* 绝对的条目路径、使用`..`爬出 marketplace 的路径或拼写为网络路径的路径
* 在 macOS 和 Linux 上，在前导`./`之后任何地方包含反斜杠的条目路径
* 从远程来源（例如 git 或 URL）获取的 marketplace 中的条目，通过解析到 marketplace 目录外的符号链接到达其目标
* 从直接 URL 添加到其`marketplace.json`的 marketplace 中的相对条目：Claude Code 仅下载该文件，因此不存在本地插件文件供路径命名。请参阅[相对路径的插件在基于 URL 的 marketplace 中失败](/docs/zh-CN/plugins/troubleshooting#plugins-with-relative-paths-fail-in-url-based-marketplaces)

`claude plugin install`报告拒绝如下：

```text theme={null}
Cannot install my-plugin@my-marketplace: its marketplace entry path does not stay inside the marketplace directory (an absolute, climbing, network-shaped, backslash-containing or link-traversing entry, an entry of a fetched marketplace that resolves or opens outside its tree — or a relative entry in a url-catalog marketplace, which has no local directory)
```

当已安装的插件的条目失败相同的检查时，`claude plugin list`显示插件为`failed to load`，带有：

```text theme={null}
Plugin source path refused: ./my-plugin does not stay inside its marketplace directory. Check that the marketplace entry has a plain relative path.
```

**要做什么：**

* 如果您维护 marketplace，将条目的`source`写为带正斜杠的纯相对路径，例如`./plugins/my-plugin`，并保持它跨越的任何符号链接指向 marketplace 目录内
* 如果您从直接 URL 添加了 marketplace，相对条目无法解析。要求 marketplace 作者使用[另一个插件源](/docs/zh-CN/plugins/marketplace-reference#plugin-sources)，或从其 git 存储库添加 marketplace

<h3 id="failed-to-load-marketplace-configuration">
  无法加载 marketplace 配置
</h3>

Claude Code 将您添加的插件 marketplace 保存在`~/.claude/plugins/known_marketplaces.json`的注册表文件中。当 Claude Code 无法使用该文件时，需要注册表的插件命令（例如`claude plugin install`）失败，返回两条消息之一：

* `Failed to load marketplace configuration`：文件存在但不是有效的 JSON 或无法读取。空文件也会以这种方式失败。
* `Marketplace configuration file is corrupted`：文件是有效的 JSON，但其内容与注册表架构不匹配。

对于空文件，`claude plugin install`报告：

```text theme={null}
✘ Failed to install plugin "my-plugin": Failed to load marketplace configuration: JSON Parse error: Unexpected EOF
```

在 v2.1.246 之前，`claude plugin install`没有报告此失败。

**要做什么：**

* 打开`~/.claude/plugins/known_marketplaces.json`并修复 JSON，或修复消息命名为与注册表架构不匹配的条目
* 如果您无法修复它，删除文件或用`{}`替换其内容，然后使用`claude plugin marketplace add <source>`重新添加每个 marketplace。Claude Code 在您下次在您信任的文件夹中启动它时重新注册您的用户或托管设置在[`extraKnownMarketplaces`](/docs/zh-CN/settings-reference#extraknownmarketplaces)中声明的 marketplace。

<h3 id="plugin-is-required-by-your-organization">
  插件由您的组织要求
</h3>

您运行了`claude plugin disable`，或使用`/plugin`**Installed**选项卡关闭了从 claude.ai 同步的[插件](/docs/zh-CN/plugins/loading#synced-plugins)，您的组织将其标记为必需：

```text theme={null}
Plugin "<name>@synced" is required by your organization and can't be disabled here. Contact your admin to change it.
```

Claude Code 不保存任何内容，插件保持启用。

当您尝试禁用必需插件依赖的插件时，Claude Code 以相同的方式拒绝，消息命名需要它的必需插件。

**要做什么：**

* 要求您的 claude.ai 组织的管理员在 claude.ai 上更改插件的必需状态

<h3 id="plugin-was-not-uninstalled">
  插件未卸载
</h3>

您运行了[`claude plugin uninstall`](/docs/zh-CN/plugins/cli-reference#plugin-uninstall)，或在`/plugin`**Installed**选项卡中选择了**Uninstall**，卸载停止，消息开头为`"<plugin>" was not uninstalled:`。如果该冒号后的文本以`installed_plugins.json`开头而不是命名设置文件，原因是`installed_plugins.json`中的内容，此版本的 Claude Code 无法读取。对于该形式，请参阅[`installed_plugins.json`保存此版本无法读取的记录](/docs/zh-CN/plugins/troubleshooting#installed-plugins-json-holds-a-record-this-version-cannot-read)。

当 Claude Code 从`enabledPlugins`中删除插件的条目并读回该范围的设置文件时，要么插件仍在那里打开，要么可以打开它的文件无法读取或检查。删除插件保存的选项、机密和数据，同时设置条目可以将其打开，会丢失它们，因此卸载停止：插件保持安装，它保存的任何内容都不会被删除。

```text theme={null}
✘ Failed to uninstall plugin "formatter": "formatter" was not uninstalled: it is still switched on in /home/user/project/.claude/settings.local.json, although the settings change reported no error. It is still installed. Take it out of "enabledPlugins" in that file yourself, then uninstall it again.
```

消息的中间部分命名文件和原因：

* `it is still switched on in <file>, although the settings change reported no error`：设置写报告成功，但读回文件时条目仍在那里
* `it is still switched on in <file>, and the settings change failed (<error>)`：文件无法保存，原因在括号中
* `<file> is there and could not be read`：文件存在但无法作为设置读取，例如因为它不是有效的 JSON，所以它可能仍然启用插件
* `<file> (not read: it is on a network path or is a link to one, or could not be checked)`：Claude Code 没有读取项目或本地设置文件，因为文件或保存它的`.claude`文件夹是指向网络位置的链接，或因为它无法检查该路径

`claude plugin uninstall`退出 1，使用`--json`时结果带有`failureCode: "settings_still_on"`。`/plugin`显示相同的消息。

**要做什么：**

* 遵循消息的最后一句：修复或替换它命名的设置文件，或自己从该文件中的`enabledPlugins`中删除插件的条目，然后再次运行卸载

<h2 id="tool-errors">
  工具错误
</h2>

这些错误来自 Claude 的工具调用。Claude 通常会自动纠正大多数工具错误。当需要您进行更改时，该错误的**应该做什么**列表会说明需要更改的内容。

<h3 id="no-such-tool-available">
  没有此类工具可用
</h3>

Claude 按名称调用了一个不在会话工具列表中的工具。Claude Code 将该错误作为工具调用的结果返回给 Claude，轮次继续。当 Claude Code 能够判断工具缺失的原因时，它会在工具名称后添加一句话，说明原因或指出应改为调用的工具，如第二行所示：

```text theme={null}
Error: No such tool available: <tool name>
Error: No such tool available: read. Tool names are case-sensitive: call Read instead.
```

在您恢复会话后不久，当 Claude 调用某个 MCP 服务器的工具时，该服务器可能仍在进行首次连接尝试。此时 Claude Code 会[等待该服务器](/docs/zh-CN/mcp#tool-availability)，如果等待结束时该工具仍不可用，则返回此错误。在 v2.1.284 之前，此类调用会立即失败，而不会等待。

工具名称被 Claude Code [截断为 200 个字符](#tool-use-name-over-200-characters)的调用也会以此错误失败。

**应该做什么：**

* 如果只出现一次，无需执行任何操作。Claude 会读取该错误，轮次继续。
* 如果对某个 MCP 服务器工具的调用持续以此错误失败，请在会话中运行 `/mcp` 或在 shell 中运行 `claude mcp list` 来检查该服务器的[状态](/docs/zh-CN/mcp#server-status)，并从 `/mcp` 重新连接失败的服务器。在 Agent SDK 中，请参阅[错误处理](/docs/zh-CN/agent-sdk/mcp#error-handling)。

<h3 id="agent-would-be-spawned-with-zero-tools">
  Agent 将以零个工具生成
</h3>

子代理的 [`tools` 列表](/docs/zh-CN/sub-agents#supported-frontmatter-fields)中的每个条目都无法匹配可用工具，因此 Claude Code 拒绝启动子代理：没有工具，它无法行动。该消息按出错原因对您的条目进行分组：

* **无法识别**：该条目与任何工具名称都不匹配，通常是拼写错误，例如 `Grpe` 代替 `Grep`。
* **子代理不可用**：该条目命名了一个真实工具，但[子代理无法使用](/docs/zh-CN/sub-agents#available-tools)。后台子代理保持较小的内置工具集，因此当子代理在后台运行时（这是默认设置），只有前台子代理才能使用的条目会出现在这里。如果您列出 `Agent`，该消息会改为在下一组中报告它。
* **在此会话中未匹配任何工具**：该条目有效，但当前会话中没有工具与其匹配，例如没有连接 GitHub MCP 服务器的 `mcp__github__*`，或子代理处于[深度限制](/docs/zh-CN/sub-agents#let-subagents-spawn-their-own-subagents)的 `Agent`。

省略 `tools` 字段永远不会触发此拒绝。如果您将 `tools` 列表留空，或 `disallowedTools` 删除其中的每个条目，Claude Code 也会跳过拒绝并启动没有工具的子代理。

在 v2.1.208 之前，子代理以零个工具启动，可能返回空结果或令人困惑的结果。

```text theme={null}
Agent 'code-reviewer' would be spawned with zero tools — refusing. Its tools list resolved to nothing: unrecognized [Grpe]. Fix the agent's tools frontmatter or pass a different subagent_type.
```

**应该做什么：**

* 根据[子代理可用的工具](/docs/zh-CN/sub-agents#available-tools)纠正错误命名的每个条目
* 删除会话没有的工具条目，例如来自未连接的服务器的 MCP 工具
* 对于[后台子代理删除](/docs/zh-CN/sub-agents#available-tools)的工具（例如 `CronCreate`），删除该条目。要保留该工具，[关闭 fork 模式](/docs/zh-CN/sub-agents#turn-fork-mode-on-or-off)并要求 Claude 在前台运行子代理
* 删除 `tools` 字段而不是列出工具，以给子代理每个[子代理可用的工具](/docs/zh-CN/sub-agents#available-tools)
* 对于仅包含 `Agent` 的 `tools` 列表，提高[深度限制](/docs/zh-CN/sub-agents#let-subagents-spawn-their-own-subagents)或给该 Agent 至少一个其他工具：Claude Code 在该限制处保留 `Agent`，因此列表中没有其他内容会解析为零个工具

<h3 id="file-is-covered-by-a-read-deny-rule">
  文件被 Read 拒绝规则覆盖
</h3>

Edit 或 Write 工具在与 [`Read` 拒绝规则](/docs/zh-CN/permissions#read-and-edit)匹配的路径上被调用，包括在该路径创建新文件。两个工具都会更改 Claude 必须能够读回的内容，因此 Claude Code 在任何文件访问之前拒绝该调用。NotebookEdit 不受 `Read` 拒绝规则覆盖。在 v2.1.228 之前，该规则仅阻止 Edit 工具，在 v2.1.208 之前，仅 `Edit` 拒绝规则阻止编辑。

```text theme={null}
File is covered by a Read deny rule in your permission settings and cannot be edited.
```

当 Claude Code 拒绝 Write 工具时，消息以 `and cannot be written` 结尾。

**应该做什么：**

* 如果 Claude 应该能够更改文件，请在 `/permissions` 或[设置](/docs/zh-CN/settings-reference#permission-settings)中删除或缩小 `Read` 拒绝规则
* 如果文件必须保持不变，请保留该规则并为相同路径添加 `Edit` 拒绝规则以同时阻止 NotebookEdit 工具

<h3 id="path-cannot-contain-null-bytes">
  路径不能包含空字节
</h3>

文件工具调用的路径或模式参数包含空字节，文件系统和搜索工具无法接受。Read、Write、Edit、NotebookEdit、Glob 和 Grep 检查此项，消息命名工具和参数：

```text theme={null}
Read file_path cannot contain null bytes (\0). Remove the null byte and try again.
```

工具调用失败，Claude 看到错误，轮次继续。

**应该做什么：**

* 您这边不需要做任何事：错误作为工具的结果返回给 Claude，消息本身告诉 Claude 删除空字节并重试

在 v2.1.281 之前，Read、Write、Edit 或 NotebookEdit 路径中的空字节会以命名 `Path contains null bytes` 的错误结束整个轮次，工具从不运行。

<h3 id="subagent-type-is-required">
  subagent\_type 是必需的
</h3>

```text theme={null}
subagent_type is required: the general-purpose agent is not available in this session. Available agents: ...
```

Claude 调用了 [Agent 工具](/docs/zh-CN/tools-reference#agent-tool-behavior)而没有 `subagent_type`，此会话没有[通用子代理](/docs/zh-CN/sub-agents#built-in-subagents)可回退。这种情况出现在两种设置中：

* [`CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS=1`](/docs/zh-CN/env-vars)在非交互模式下设置，这会删除每个内置子代理
* 会话的主线程 Agent 有一个 [`tools: Agent(...)` 允许列表](/docs/zh-CN/sub-agents#restrict-which-subagents-can-be-spawned)，其中不包括 `general-purpose`

**应该做什么：**

* 通常不需要做任何事：该消息列出了会话确实拥有的子代理，因此 Claude 可以使用其中一个重试
* 如果 Claude 继续失败，请将 `general-purpose` 添加到 `tools: Agent(...)` 允许列表，或取消设置 `CLAUDE_AGENT_SDK_DISABLE_BUILTIN_AGENTS`

在 v2.1.235 之前，相同的调用失败并显示 `Agent type 'general-purpose' not found`。

<h3 id="memory-index-is-over-its-read-limit">
  记忆索引超过其读取限制
</h3>

Claude 写入了[自动记忆](/docs/zh-CN/memory#auto-memory)索引 `MEMORY.md`，并使其超过了读取限制之一：200 行或 25KB。写入成功，但会话开始时仅加载前 200 行或 25KB（以先到者为准），因此每次读取索引时，超过限制的所有内容都会被丢弃。在 v2.1.210 之前，超限索引在下次加载时被静默截断，没有写入时信号。

```text theme={null}
Error: this write left the memory index at MEMORY.md at 214 lines, over its 200-line read limit. The write succeeded, but everything past the limit is silently dropped each time the index is loaded — entries at the end are already invisible to readers. Rewrite it to under 140 lines now: keep one line per entry, move detail into topic files, and merge or drop stale entries.
```

仅加载的内容计入限制。YAML frontmatter 和块级 HTML 注释在加载索引前被删除，因此它们被排除在测量之外。在 v2.1.211 之前，Claude Code 测量原始文件，frontmatter 或注释即使在加载的内容符合时也可能触发此错误。

Claude Code 在写入后将错误传递给 Claude，而不是在您的终端中打印为横幅，因此您可能仅在会话记录中注意到它。

当 Claude 的写入使文件接近限制但未超过时，Claude Code 返回更温和的提醒以压缩索引，而不是此错误。

**应该做什么：**

* 让 Claude 重写 `MEMORY.md`，或要求它：每个条目保留一行，将详细信息移到主题文件中，并合并或删除过时条目
* 要自己修剪索引，请参阅[审计和编辑您的记忆](/docs/zh-CN/memory#audit-and-edit-your-memory)

<h3 id="pkill-pattern-matches-the-claude-code-process">
  pkill 模式匹配 Claude Code 进程
</h3>

Bash 工具调用中的 `pkill` 命令使用了一个模式（通常带有 `-f`），该模式与 Claude Code 进程本身匹配，因此 Claude Code 拒绝该命令而不是让它结束会话。Claude Code 在运行 `pkill` 之前使用 `pgrep` 测试该模式，并在其自己的进程 ID 在结果中时拒绝。该检查仅在 Linux 上运行；在 macOS 上，`pkill` 不经修改地运行。在 v2.1.214 之前，该命令运行，匹配的模式在轮次中途杀死了 Claude Code 会话。

```text theme={null}
pkill: refusing to run — this pattern matches the Claude CLI process (PID 12345). Narrow the pattern, or target your own children with `pkill -P $$ ...`.
```

拒绝出现在 Bash 工具结果中，而不是作为您终端中的横幅，Claude 通常会自动调整该命令。

**应该做什么：**

* 缩小模式，使其仅匹配预期的进程，例如目标二进制文件的完整路径而不是短子字符串
* 要停止由当前 shell 启动的进程，请使用 `pkill -P $$` 和该模式，这将匹配限制为 shell 自己的子进程

<h3 id="failed-to-write-to-a-teammate-inbox">
  无法写入队友的收件箱
</h3>

Claude Code 无法将消息写入 `~/.claude/teams/{team-name}/inboxes/` 下的队友邮箱文件，因此收件人没有收到任何内容。当 Claude Code 无法创建或更新文件时写入失败，例如因为磁盘已满、目录不可写或另一个 Agent 长时间持有收件箱锁。在 v2.1.224 之前，Claude Code 即使在写入失败时也报告消息已发送。

该错误出现在发送方 Agent 的工具结果中，而不是作为您终端中的横幅，其文本告诉 Claude 重试：

```text theme={null}
Failed to write to researcher's inbox — nothing was sent. Try again, or message the lead.
```

结构化 [agent team](/docs/zh-CN/agent-teams) 协议消息以相同方式失败，错误命名未送达的消息：当 Claude Code 无法写入计划批准、计划拒绝、关闭请求或关闭拒绝时，错误读取 `Failed to write the <message> to <name>'s inbox — nothing was sent`。该列表中的 `plan approval` 是领导批准队友计划的决定；队友的计划提交是单独的 `plan approval request` 消息。该消息和另外两个协议消息携带自己的消息文本和后果：

* `Failed to write the plan approval request to the lead's inbox — plan not submitted; try again`：队友的计划从未到达领导，队友保持计划模式直到重新提交成功
* `The permission request could not be delivered to the team lead (mailbox write failed)`：队友的权限请求从未到达领导，因此没有人批准工具调用
* `The confirmation could not be written to team-lead's inbox.`：关闭批准本身生效，队友退出；仅缺少对领导的确认

当您自己给队友发消息时，在领导会话中输入 `@name` 后跟消息，相同的失败显示为通知 `Couldn't write to @name's inbox — message not sent. Try again.`，Claude Code 将您的文本保留在输入框中，以便您可以再次发送。

**应该做什么：**

* 要求发送者重新发送消息；收件箱锁的争用是暂时的，重试时会清除
* 检查可用磁盘空间，并检查 `~/.claude/teams` 及其下的文件是否可由您的用户写入

<h3 id="teammate-agent-definition-not-restored">
  队友的 Agent 定义未被恢复
</h3>

Claude 给已停止的 [agent team](/docs/zh-CN/agent-teams) 队友发消息，Claude Code 将其恢复，但没有重新应用它生成时所依据的[子代理定义](/docs/zh-CN/agent-teams#use-subagent-definitions-for-teammates)。该通知跟随发送方 Agent 的工具结果中的恢复报告，并说明原因。当定义文件来自没有保存信任的文件夹时，内容如下：

```text wrap theme={null}
Its agent definition was not restored: the folder its definition file came from is not trusted (source: projectSettings), so the teammate is running with the team-essential tools and no custom instructions. To restore it, the user needs to run Claude Code in that folder once and accept the trust dialog (the --debug log names the folder); do not change trust settings on the user's behalf.
```

该检查适用于项目的 `.claude/agents/` 目录或 `--add-dir` 目录中的定义，接受父文件夹的信任对话框并不能满足它。

**应该做什么：**

* 在[调试日志](/docs/zh-CN/debug-your-config)命名的文件夹中运行 `claude` 并接受信任对话框。下次 Claude Code 恢复队友时重新应用定义；您不需要重启领导会话
* 或在 `~/.claude.json` 中将 `hasTrustDialogAccepted` 条目设置为 `true`，使用调试日志打印的确切 `projects["<path>"]` 键

<h3 id="message-too-large-for-cross-session-delivery">
  跨会话传递消息过大
</h3>

Claude 发往此机器上您的另一个会话的[跨会话消息](/docs/zh-CN/cross-session-messaging)太长而无法发送。Claude Code 拒绝了它，接收会话什么都没有收到。拒绝出现在发送会话的工具结果中，而不是作为您终端中的横幅。它命名两个大小以及如何使消息符合：

```text wrap theme={null}
Failed to send to api-worker: Message too large for cross-session delivery: the serialized message is 1,203,844 characters and the limit is 1,048,576. Shorten the message text — put bulk content in a file the recipient can read rather than in the message — or split it into smaller messages.
```

重新发送相同的文本以相同方式失败。

**应该做什么：**

* 要求 Claude 总结消息，或将大量内容放入文件并发送该文件的路径
* 要求 Claude 将内容分成几条较短的消息

在 v2.1.235 之前，Claude Code 报告超大消息已发送。接收会话未读地丢弃了它。

<h3 id="too-many-messages-to-this-session-just-now">
  此会话刚刚收到太多消息
</h3>

Claude 向此机器上您的一个会话快速连续发送了大量[跨会话消息](/docs/zh-CN/cross-session-messaging)，达到了该会话收件箱所能接受的上限。Claude Code 拒绝了下一次发送，接收会话什么都没有收到。拒绝出现在发送会话的工具结果中，而不是作为您终端中的横幅：

```text wrap theme={null}
Failed to send to api-worker: Too many messages to this session just now: 30 were sent recently and more would be dropped by its rate limit, so this one was not sent. Batch what remains into one message, or wait a little before sending more.
```

**应该做什么：**

* 通常不需要做任何事：Claude 将剩余内容批处理为一条消息，或在发送更多内容前等待
* 如果是您自己的提示词引发了这次突发，请要求 Claude 将剩余内容合并为单条消息

在 v2.1.236 之前，Claude Code 报告这些消息已发送。接收会话未读地丢弃了它们。

<h3 id="cross-session-message-dropped-at-the-inbox">
  跨会话消息在收件人会话的收件箱处被丢弃
</h3>

Claude 发送了[跨会话消息](/docs/zh-CN/cross-session-messaging)到此机器上您的另一个会话，该会话的收件箱在该会话中的 Claude 读取之前丢弃了它。该行命名收件人的地址，当收件人给出原因时，在破折号后添加原因：

```text wrap theme={null}
Cross-session message was dropped at the recipient session's inbox (recipient: uds:/tmp/cc-socks/13605.sock) and not delivered — its queue of undelivered peer messages was full. Claude was told not to resend right away.
```

一行可以覆盖多条丢弃的消息。然后它以复数形式开始，例如 `Cross-session messages (12) were dropped`。要找到地址属于哪个会话，请将其与 `/status` 在每个会话中显示的 [`Peer address` 行](/docs/zh-CN/cross-session-messaging#the-sessions-inbox-socket)进行比较。

在破折号后，该行给出以下一个或多个原因：

* `its queue of undelivered peer messages was full`：收件人持有的来自其他会话的未送达消息已达到其队列允许的上限
* `you sent faster than that session accepts`：发送会话的消息到达速度比收件人从一个发送者接受的速度快
* `it repeated your previous message`：该消息与发送会话不久前发送给该收件人的消息相同
* `a relay loop between sessions was cut`：该消息延续了会话之间相互发送消息的链，且该链经过收件人的次数过多或增长过长

**应该做什么：**

* 假设收件人从未看到丢弃的消息。Claude Code 也会这样告诉 Claude，并告诉它在稍后的一条消息中包含仍然重要的任何内容，而不是立即重新发送
* 如果您的会话相互发送频繁更新，请要求 Claude 发送更少、更大的消息，例如在会话完成其工作时发送一份报告
* 对于 `a relay loop between sessions was cut`，请在其中一个会话中自己输入下一条指令。Claude 为响应您自己的提示词而发送的消息会开始一条新链

在 v2.1.238 之前，当收件人的收件箱丢弃消息时，发送会话没有收到报告。

<h3 id="refusing-to-send-a-cross-session-message">
  拒绝发送跨会话消息
</h3>

在 Claude Code 将[跨会话消息](/docs/zh-CN/cross-session-messaging)写入此机器上您的另一个会话之前，它检查目标会话的收件箱套接字是否为消息寻址到的端点。当检查失败时，Claude Code 在发送会话中拒绝发送，目标会话什么都没有收到。对于 Claude 发送的消息，拒绝出现在发送会话的工具结果中：

```text theme={null}
Failed to send to api-worker: Refusing to send: reply target is a symlink
```

`Refusing to send:` 后的文本命名失败的检查：

* `reply target is a symlink`：符号链接位于目标会话的套接字路径。Claude Code 不通过它传递，因为那里的链接可能会将消息重定向到目标会话未创建的端点。
* `cannot vet reply target`：Claude Code 根本无法检查目标路径，例如因为读取失败并出现权限错误。

**应该做什么：**

* 通常不需要做任何事：这些检查防止消息到达其寻址会话之外的端点，且没有发送任何内容
* 如果 `reply target is a symlink` 对某个会话重复出现，请检查是什么在该会话的套接字路径处创建了链接，该路径显示在其 `/status` 的 `Peer address` 下

<h3 id="refusing-after-a-symlink-changed">
  拒绝读取、写入或搜索路径
</h3>

Claude Code 检查文件路径的[权限规则](/docs/zh-CN/permissions#read-and-edit)，然后在工具打开文件或启动搜索时再次确认该解析。当它无法确认路径仍然导向检查批准的位置时，Claude Code 拒绝操作而不是跟随它。拒绝出现在工具结果中：

```text wrap theme={null}
Refusing to read /path/to/file: its symlink resolution changed after permission was checked (a link on the way now leads somewhere the check did not see). If a link in the working directory is being rewritten concurrently, stop that and retry.
```

每个拒绝命名其原因：

* `its symlink resolution changed after permission was checked`：路径上的符号链接或 Grep 或 Glob 搜索根在权限检查和操作之间被替换。在读取拒绝中，括号中的短语命名哪个比较失败。
* `its parent-directory symlink resolution changed after permission was checked`：写入路径经过的目录不再解析到批准的位置
* `where it leads on disk could not be determined (a link on the way could not be examined, or the links do not resolve)`：Claude Code 无法跟随路径到磁盘上的最终位置，例如因为其上的符号链接形成循环
* `it is a symbolic link. Write to the link's target path instead`：符号链接位于请求的写入位置本身，例如 `CLAUDE.md` 是 `AGENTS.md` 的符号链接；消息指导 Claude 转向链接的目标
* `Refusing to write through symlink: <path>. Resolve the symlink and pass the real target path explicitly.`：当另一个写入器打开文件时捕获的相同条件，例如写入符号链接的 `.mcp.json`
* `Refusing to write into symlinked directory: <path>`：持有文件的目录本身是符号链接，例如项目的 `.claude/` 目录链接到另一个位置
* `a path one of its Read deny rules is written through changed while the search was being prepared. Retry.`：搜索的 `Read` 拒绝规则命名了经过符号链接的路径，该链接在 Claude Code 准备搜索时发生更改
* `it could not be opened (EACCES) — it is unreadable, or is being replaced concurrently.`：搜索根存在但无法打开；括号中的代码是操作系统错误
* `its permission check expired before it ran (too many concurrent file operations). Retry.`：在大量同时进行的文件操作下，Claude Code 在工具使用批准记录之前将其逐出；重试会运行新的权限检查
* `ripgrep was found only by name on PATH, and a search outside the working directory cannot apply your Read deny rules in that configuration`：Claude Code 无法将 `rg` 二进制文件解析为绝对路径，因此它拒绝工作目录外的搜索，而不是运行您的拒绝规则无法覆盖的搜索

**应该做什么：**

* 通常不需要做任何事：拒绝作为工具结果到达 Claude，被拒绝的操作不会运行
* 如果符号链接拒绝在某个路径上重复出现，请找出是什么在不断重写那里的链接，例如构建工具或文件监视程序，或要求 Claude 使用文件的解析路径而不是链接路径
* 如果 Claude Code 在 Windows 上的 AppContainer 或受限令牌沙箱内运行时，每个文件都出现此拒绝，请升级到 v2.1.265 或更高版本
* 如果在 macOS 上，对没有任何东西在重写的文件（例如拖入提示词的屏幕截图）出现读取拒绝，请升级到 v2.1.273 或更高版本
* 对于 ripgrep 拒绝，使用您的包管理器安装 ripgrep，以便 `rg` 在 `PATH` 上解析为绝对路径，或将搜索保持在工作目录下

在 v2.1.251 之前，Claude Code 仅对文件写入重新检查路径的解析，因此在权限检查后替换的链接可能会将读取或搜索重定向到不同的位置而没有消息。其中，仅父目录、通过符号链接和符号链接目录写入拒绝会出现在早期版本上。

在 v2.1.280 之前，`where it leads on disk could not be determined` 拒绝没有出现。

<h3 id="task-output-swap-refused">
  任务输出交换被拒绝
</h3>

Claude Code 将每个 Bash 命令的输出保存到其临时目录下的文件。每次打开其中一个文件时，它检查路径仍然导向它创建的文件，没有符号链接、额外硬链接或移动目录重定向它。此消息意味着该检查失败，因此 Claude Code 拒绝操作而不是通过该路径写入或读取输出。消息出现在 Bash 工具结果中：

```text wrap theme={null}
task output swap refused (tasks dir moved or linked): /private/tmp/claude-501/-Users-you-my-project/1f0e62dc-4b0a-4f5e-9c2d-8a7b6c5d4e3f/tasks/b7k2f9m3q.output. To recover: restart Claude Code with CLAUDE_CODE_TMPDIR set to a fresh directory; or, if /private/tmp/claude-501/-Users-you-my-project is a stray directory or a symbolic link that should not be there, remove that entry itself (not what it points to) and restart.
```

括号中的文本命名失败的检查。诸如 `output symlink was re-pointed`、`output file identity changed` 和 `not a regular file` 之类的原因都报告相同的条件：输出路径上或沿途的某些东西不再是 Claude Code 创建的文件。仅某些原因携带 `To recover:` 句子。

如果在命令仍在运行时检查失败，Claude Code 停止该命令，其结果报告：

```text theme={null}
Command killed: its output file was replaced or could no longer be verified
```

**应该做什么：**

* 升级到 v2.1.260 或更高版本。早期版本有时在没有链接或移动目录存在时显示此消息
* 使用设置为新目录的 [`CLAUDE_CODE_TMPDIR`](/docs/zh-CN/env-vars)重启 Claude Code
* 或检查您的项目在 Claude Code 临时目录下的目录，示例消息中的 `/private/tmp/claude-501/-Users-you-my-project`。如果该路径是符号链接或不应该存在的目录，删除链接或目录本身而不是链接的目标，然后重启 Claude Code
* 如果拒绝重复出现，说明有进程在会话运行时替换、链接或删除 Claude Code 临时目录下的条目。将 [`CLAUDE_CODE_TMPDIR`](/docs/zh-CN/env-vars) 设置为没有其他东西管理的目录并重启

<h3 id="disk-quota-or-temp-filesystem-is-full">
  磁盘配额或临时文件系统已满
</h3>

Claude Code 将每个 Bash 和 PowerShell 命令的输出保存到其临时目录下的文件。当命令以非零代码退出且完全没有输出时，Claude Code 检查持有该文件的文件系统是否空间不足或 inode 不足，或您在其上的磁盘配额是否已用完。如果是这样，诊断出现在命令的结果中，代替空输出：

```text wrap theme={null}
Your disk quota is full on the filesystem with Claude Code's temp directory /private/tmp/claude-501/-Users-you-my-project/1f0e62dc-4b0a-4f5e-9c2d-8a7b6c5d4e3f/tasks (EDQUOT), so any output this command printed was lost, and it may have failed because it could not write. Delete files you no longer need there, or restart Claude Code with CLAUDE_CODE_TMPDIR set to a directory on another filesystem.
```

该消息命名什么用完了：

* `Your disk quota is full ... (EDQUOT)`：您在该文件系统上的配额已用完。配额可以在文件系统仍显示可用空间时已满
* `The filesystem with Claude Code's temp directory ..., or your disk quota on it, is full (ENOSPC)`：文件系统或您在其上的配额没有剩余空间
* `Command output was lost: the temp filesystem at ... is full` 或 `... is out of inodes`：文件系统几乎没有剩余空间，或 inode 即将用完

**应该做什么：**

* 删除您在持有 Claude Code 临时目录的文件系统上不再需要的文件。对于 `EDQUOT`，删除计入您自己配额的文件。对于 `out of inodes`，删除许多文件而不是几个大文件，因为每个文件占用一个 inode，无论其大小如何
* 或使用设置为具有空间的文件系统上的目录的 [`CLAUDE_CODE_TMPDIR`](/docs/zh-CN/env-vars)重启 Claude Code
* 然后让 Claude 再次运行该命令。它打印的输出已丢失，未被截断

<h3 id="the-source-file-is-not-valid-utf-8-text">
  源文件不是有效的 UTF-8 文本
</h3>

Claude 尝试从一个字节无法解码为文本、或其文本已包含替换字符 `U+FFFD` 的文件发布 [Artifact](/docs/zh-CN/artifacts)，因此 Claude Code 在上传任何内容之前拒绝了发布。消息出现在 Artifact 工具结果中并命名第一个要修复的位置：

```text wrap theme={null}
file_path: the source file is not valid UTF-8 text (first invalid byte at line 12, column 40). It may be saved in another encoding or contain binary data. Rewrite it as UTF-8, then publish again. Nothing was published.

file_path: the source file has the replacement character U+FFFD at line 12, column 40, usually left where an earlier edit or paste lost a character. Replace it with the intended text (in HTML, write an intended U+FFFD as &#xFFFD;), then publish again. Nothing was published.
```

Claude Code 将文件解码为 UTF-8，或当它以小端 UTF-16 字节顺序标记开始时解码为 UTF-16。当这样的 UTF-16 文件无法解码时，第一条消息命名 `UTF-16` 并仍然告诉您将文件重写为 UTF-8。当命名的位置之后还有更多位置时，消息在位置后添加计数，例如 `(+2 more)`。

**应该做什么：**

* 通常不需要做任何事：Claude 重写文件并再次发布
* 如果文件是您编写或导出的，请再次将其保存为 UTF-8，并将每个 `U+FFFD` 替换为早期编辑、粘贴或转换丢失的字符
* 要在页面上显示有意的 `U+FFFD`，在 HTML 中将其写为 `&#xFFFD;` 而不是字面字符

在 v2.1.267 之前，Claude Code 不加检查地上传这样的文件，而由服务器拒绝发布。

<h3 id="not-published-that-file-is-on-a-network-share">
  未发布：该文件位于网络共享上
</h3>

Claude 尝试从一个路径指向网络主机的文件发布 [Artifact](/docs/zh-CN/artifacts)：

* 在 Windows 上，不在您启动时通过 [`--add-dir`](/docs/zh-CN/cli-reference#cli-flags) 传入的映射网络驱动器下的 `\\server\share` 路径
* 在 macOS 或 Linux 上，自动挂载路径，例如 `/net/<host>/page.html`

查找此类路径会联系其指向的主机，而在 Windows 上，这种联系可能会将您的凭据发送给该主机。Claude Code 拒绝发布该文件，也不会读取它。拒绝出现在 Artifact 工具结果中：

```text theme={null}
Not published: that file is on a network share. Publish a file from this session's folders instead.
```

**应该做什么：**

* 如果您不需要该特定文件，则无需执行任何操作：消息会告诉 Claude 改为从会话自己的文件夹发布文件
* 要发布该特定文件，请将其复制到本地磁盘上的文件夹中，然后再次请求
* 在 Windows 上，要让 Claude 直接从共享发布，请将其映射到驱动器号，并在启动 Claude Code 时传入该驱动器。例如，在 PowerShell 中运行 `net use Z: \\server\share`，然后运行 `claude --add-dir Z:\`。之后 Claude 就可以从该驱动器发布文件。在会话中途使用 `/add-dir` 添加驱动器是不够的。
* 在 macOS 或 Linux 上，将共享挂载到某个目录（例如 `/mnt` 或 `/Volumes` 下的目录），并从该路径而不是自动挂载路径发布

<h3 id="reading-a-local-file-from-outside-the-connected-folders">
  在 Cowork 会话中从连接的文件夹外读取本地文件
</h3>

在 Claude Desktop 应用中于您的机器上运行的 [Cowork](https://claude.com/docs/cowork/overview) 会话中，Claude 为 [Artifact](/docs/zh-CN/artifacts) 指定了一个本地文件。Claude Code 无法确认该文件是会话连接的文件夹内的普通文件：路径位于这些文件夹之外、经过符号链接，或者其写法可能指向与表面不同的文件。读取这样的文件需要您的批准，而在无法向您显示批准卡片的会话中（例如设置为跳过所有批准的会话），Claude Code 会拒绝读取。

拒绝出现在 Artifact 工具结果中；当文件根本无法检查时，它改为命名该失败：

```text wrap theme={null}
Reading a local file from outside this session's connected folders, or through a link, needs the approval card, and no one can answer it in this Cowork session. Use a plain file inside the connected folders; do not retry this file in this session.

cannot read file_path (ENOENT) — the file could not be examined, and no one can answer the approval card in this Cowork session. Check that the file exists as a plain file inside the connected folders, then retry with that path.
```

**应该做什么：**

* 通常不需要做任何事：消息告诉 Claude 改为使用连接的文件夹内的普通文件
* 要将该特定文件放入 Artifact，请将其作为常规文件（而非符号链接）复制到会话的某个连接文件夹中，然后再次请求

<h3 id="webfetch-cannot-fetch-localhost">
  WebFetch 无法获取 localhost
</h3>

Claude 调用了 [WebFetch](/docs/zh-CN/tools-reference#webfetch-tool-behavior)，其 URL 的主机名中没有点，例如 `http://localhost:3000` 或类似 `http://wiki/` 的纯内网名称。WebFetch 在发出任何请求之前拒绝这些 URL：

```text wrap theme={null}
WebFetch cannot fetch localhost or other hostnames without a dot. To reach a local server, use Bash with curl instead.
```

**应该做什么：**

* 通常不需要做任何事：消息引导 Claude 通过 Bash 工具使用 `curl`，它可以访问本地和内网服务器

在 v2.1.268 之前，WebFetch 用通用的 `Invalid URL` 错误报告这些 URL。

<h3 id="webfetch-domain-safety-check-failed">
  WebFetch 域名安全检查失败
</h3>

在获取 URL 之前，WebFetch 将 URL 的主机名发送到 `api.anthropic.com`，以根据 Anthropic 的[域名安全阻止列表](/docs/zh-CN/data-usage#webfetch-domain-safety-check)检查它。如果检查无法完成，WebFetch 无法确认域名是安全的，因此它不获取页面，工具结果改为携带以下消息之一：

```text wrap theme={null}
The safety check for domain example.com is rate-limited (too many domain checks from this network; the limit is shared and can stay exhausted for minutes). Do not retry WebFetch in a loop or sleep to wait it out; continue without this page and report that its safety check was rate-limited. A single later attempt is fine; if that is rate-limited too, stop.

Unable to verify if domain example.com is safe to fetch. This may be due to network restrictions or enterprise security policies blocking claude.ai.
```

* `rate-limited`：检查端点以 HTTP `429` 响应。消息告诉 Claude 在没有该页面的情况下继续，并且稍后最多再尝试一次。Claude Code 不缓存失败的检查，因此稍后获取该域名时会再次运行检查。如果您网络上的会话经常遇到这种情况，您可以在设置中使用 [`skipWebFetchPreflight: true`](/docs/zh-CN/settings-reference#skipwebfetchpreflight) 跳过检查。
* `Unable to verify`：检查请求失败、超时或收到其他错误状态。如果您的网络阻止 `api.anthropic.com`，请将该域名加入允许列表，或在设置中使用 [`skipWebFetchPreflight: true`](/docs/zh-CN/settings-reference#skipwebfetchpreflight) 跳过检查。

在 v2.1.286 之前，速率限制消息为 `The safety check for domain example.com is temporarily rate-limited (too many domain checks from this network). Retry after about a minute; retrying sooner will fail the same way.`。
在 v2.1.285 之前，被限流的检查改为用 `Unable to verify` 消息报告。

<h2 id="background-session-errors">
  后台会话错误
</h2>

[后台会话](/docs/zh-CN/agent-view)在没有自己的交互式终端的情况下运行，因此需要终端的命令在那里的行为会有所不同。这些消息出现在后台会话的会话记录中、附加到后台会话的终端中、您分派的会话或 shell 中，或者对于下面的[worktree-guard 条目](#write-or-command-blocked-because-the-path-cannot-be-safely-resolved)，出现在任何在 worktree 中隔离的会话或运行 worktree 隔离子代理中；当消息特定于一个使用入口时，其条目会说明这一点。

<h3 id="commands-refused-in-a-background-session">
  后台会话中拒绝的命令
</h3>

打开交互式对话框的命令在没有终端附加到后台会话时无法执行。`/install-github-app`、`/mcp` 设置列表和 MCP 服务器菜单中的身份验证操作会响应一条消息。对于 `/install-github-app` 和 `/mcp` 设置列表，该会话也在 [Agent 视图](/docs/zh-CN/agent-view)中的**需要输入**下显示，以便您可以找到它、附加并再次运行该命令。附加终端时，这些命令正常工作。

在 v2.1.216 之前，会话在拒绝 `/install-github-app` 或 `/mcp` 设置列表后不会在**需要输入**下显示。在 v2.1.213 到 v2.1.215 中，附加终端时命令仍然有效，拒绝消息告诉您附加并再次运行该命令。从 v2.1.208 到 v2.1.212，Claude Code 即使附加了终端也拒绝了它们，消息如 `Can't open MCP settings in a background session`；在这些版本上，从常规 `claude` 会话运行该命令，或升级。在 v2.1.208 之前，它们在后台会话内打开了对话框。在仅 v2.1.208 中，Claude Code 也拒绝了后台会话中的 `/model` 选择器，`/upgrade` 打印了升级 URL 而不是打开浏览器。

措辞命名该命令。`/mcp` 设置列表报告：

```text theme={null}
Can't open MCP settings while no terminal is attached to this background session. This session now shows "needs input" in agent view — open it and run /mcp to manage servers, or use `/mcp enable|disable|reconnect <server>` to steer without the panel.
```

**要做什么：**

* 从 Agent 视图附加到会话并再次运行该命令
* 或使用消息命名的形式，例如 `/mcp reconnect <server>`、`/mcp enable` 或 `/mcp disable`，这些不需要附加即可工作

<h3 id="write-or-command-blocked-because-the-path-cannot-be-safely-resolved">
  写入或命令被阻止，因为路径无法安全解析
</h3>

Claude 通过 [worktree 隔离保护](/docs/zh-CN/agent-view#how-file-edits-are-isolated)无法解析为一个可验证位置的拼写来寻址文件或工作目录。保护检查[任何在 worktree 中隔离的会话](/docs/zh-CN/worktrees#how-claude-code-enforces-isolation)中的写入和命令工作目录，交互式或后台，以及[worktree 隔离的子代理](/docs/zh-CN/worktrees#isolate-subagents-with-worktrees)中的写入和命令工作目录。它在检查操作不会到达共享检出之前解析符号链接，当解析失败时，它会阻止操作而不是让它落在那里。消息命名它拒绝的路径形式以及如何重试：

```text theme={null}
This write was blocked because the path is spelled in a form that cannot be safely resolved (for example through a symlink storing a raw dot segment, a network-share or device-namespace shape, or an unreadable ancestor directory). If the file is inside the worktree /path/to/worktree, address it by its direct symlink-free path instead.
```

被阻止的命令为其工作目录报告相同的原因，并以 `re-run the command from its direct symlink-free path` 结尾。在 v2.1.217 之前，保护在不解析符号链接的情况下比较路径拼写，因此这些拼写未被阻止，通过符号链接路由的写入可能会落在共享检出中。

**要做什么：**

* 通常什么都不做：完整消息作为工具错误发送给 Claude，Claude 使用它命名的直接路径重试。对于被阻止的文件编辑，对话视图仅显示简短的 `Error editing file` 行；完整消息出现在您使用 `Ctrl+O` 打开的会话记录视图中。被阻止的命令在其命令输出中打印它。
* 如果同一文件上的阻止重复出现，路径可能通过包含 `..` 的已提交符号链接运行，例如 `docs/current -> ../README.md`；要求 Claude 通过其真实路径而不是通过链接编辑目标文件

<h3 id="write-or-command-blocked-because-the-path-names-a-network-location">
  写入或命令被阻止，因为路径命名网络位置
</h3>

Claude 通过命名不在您机器上的驱动器、UNC 共享（如 `\\server\share\file`）或 `/net` 自动挂载路径的路径来寻址文件或工作目录，而会话的检出在本地磁盘上。相同的 [worktree 隔离保护](#write-or-command-blocked-because-the-path-cannot-be-safely-resolved)无法验证这样的路径保持在共享检出之外，因此它会阻止操作。在 worktree 中隔离会话不会解除阻止。消息命名要使用的路径形式：

```text theme={null}
This write was blocked because the path is network-shaped (a UNC share or /net automount spelling) while this session's checkout is local. Isolating cannot unblock it. If the file is genuinely inside the worktree /path/to/worktree, address it by its local, plainly-spelled path instead.
```

被阻止的命令为其工作目录报告相同的原因，并以 `re-run the command from its local, plainly-spelled path` 结尾。在 v2.1.217 之前，保护仅比较路径文本，因此通过 UNC 或 `/net` 路径寻址检出内的文件未被阻止。

**要做什么：**

* 通常什么都不做：Claude 使用消息要求的本地拼写重试

<h3 id="command-blocked-by-the-worktree-isolation-checks">
  命令被 worktree 隔离检查阻止
</h3>

Claude 在[在 worktree 中隔离的会话](/docs/zh-CN/worktrees#how-claude-code-enforces-isolation)中运行了 Bash 或 Monitor 命令，Claude Code 因以下两个原因之一拒绝了它：

* 该命令将 git 指向主检出。
* Claude Code 无法从命令文本验证该命令运行的任何 git 都保留在 worktree 内。从不命名 git 的命令仍然可能因此原因被拒绝，因为展开变量间接寻址（如 `${!name}`）或运行 Bash 函数替换（如 `${ command; }`）会产生在运行时本身可能是命令的值。

消息的中间命名无法验证的内容：

```text wrap theme={null}
This session is isolated in the worktree /path/to/worktree, but this command evaluates ${!x@P} arithmetically inside a construct too complex to verify, which can run a command hidden in a variable's value. Refusing to run it — a worktree-isolated session's git operations must target its own worktree. Split it into plain, separate commands and run them from /path/to/worktree.
```

**要做什么：**

* 通常什么都不做：Claude 读取消息并按照其最后一句要求的方式重写命令
* 如果您要求的命令继续被拒绝，按字面拼写标记的值：用其值替换间接寻址或替换，并从 worktree 内作为其自己的纯命令运行 git
* 要有意对主检出采取行动，在会话外的终端中自己运行该命令

<h3 id="this-session-has-no-saved-transcript">
  此会话没有保存的会话记录
</h3>

您附加到一个停止的[后台会话](/docs/zh-CN/agent-view)，该会话从另一个对话中用 `←` 或 `/background` 后台化，并在其第一个回复完成之前停止。在该第一个回复完成之前，对话仍然仅存在于后台化它的会话中，因此 `claude attach` 拒绝启动停止的会话，而不是在相同的会话 ID 下开始空白对话。消息以此会话的 `claude respawn` 命令结尾：

```text theme={null}
This session has no saved transcript — it was stopped before its first response finished. If it was backgrounded from another conversation, that one is still intact; `claude respawn <id>` starts this one fresh.
```

在 [Agent 视图](/docs/zh-CN/agent-view)中打开相同会话的行则会在列表下方显示 `Press enter again to restart this session fresh`，在该行上第二次按 `Enter` 会使用空对话重启会话。

**要做什么：**

* 您后台化的对话是完整的：使用 [`claude --resume`](/docs/zh-CN/sessions) 恢复它或继续在其中工作
* 要无论如何启动停止的会话，请使用消息中的 ID 运行 `claude respawn <id>`，或在 Agent 视图中的其行上按 `Enter` 两次
* 如果会话确实完成了回复，您仍然在 v2.1.214 之前的版本上看到此拒绝，`~/.claude/projects` 中的不可读文件夹可能会使会话记录扫描错过保存的对话；更新到 v2.1.214 或更高版本，它在扫描期间容忍不可读的文件夹

<h3 id="this-session-is-running-in-another-terminal">
  此会话在另一个终端中运行
</h3>

您在 [Agent 视图](/docs/zh-CN/agent-view)中打开了停止的会话的行，其保存的对话已在此机器上的另一个实时 Claude Code 进程中打开，因此 Claude Code 拒绝启动将写入相同会话记录的第二个进程。您看到的消息取决于[什么持有对话](/docs/zh-CN/agent-view#opening-a-session-says-the-conversation-is-already-open)：

```text theme={null}
Can't open — this session is running in another terminal
This conversation is already open in another running Claude session — use that one, or close it and try again
```

* **`running in another terminal`**：终端持有对话，例如您使用 `claude --resume` 或 `/resume` 恢复它的终端。该行也显示 `Open in a terminal`。
* **`already open in another running Claude session`**：另一个非交互式 Claude Code 进程持有它，例如相同对话的[后台会话](/docs/zh-CN/agent-view#the-supervisor-process)进程尚未退出。

**要做什么：**

* 在持有它的进程中继续对话，或退出该进程并再次打开该行

在 v2.1.248 之前，仅存在 `already open in another running Claude session` 拒绝：在终端中恢复的对话不计为打开，打开该行启动了第二个 Claude Code 进程写入相同的对话。

<h3 id="this-sessions-saved-conversation-is-no-longer-on-disk">
  此会话的保存对话不再在磁盘上
</h3>

您打开了一个[后台会话](/docs/zh-CN/agent-view)，该会话在后台服务关闭时结束，[会话记录清理](/docs/zh-CN/settings-reference#cleanupperioddays)随后删除了其保存的对话，例如在机器关闭数周后。通常打开这样的行会[恢复其保存的对话](/docs/zh-CN/agent-view#sessions-show-as-failed-after-shutdown)。没有什么可恢复的，Claude Code 拒绝而不是在不询问的情况下重新运行会话的原始提示词：

```text theme={null}
This session's saved conversation is no longer on disk (it ended while the background service was off, and old transcripts are cleaned up), so there is nothing to resume. `claude rm 7c5dcf5d` deletes the row; `claude respawn 7c5dcf5d` runs its original prompt again instead.
```

`claude attach <id>` 打印此文本。在 Agent 视图中，页脚更短，以 `ctrl+x deletes the row` 结尾。

**要做什么：**

* 运行 `claude rm <id>` 删除该行。当[保留的情况](/docs/zh-CN/agent-view#what-deleting-a-session-removes)之一适用时，`claude rm` 保留该行和 worktree，并命名原因
* 要再次运行会话的原始提示词作为新对话，请运行 `claude respawn <id>`

在 v2.1.248 之前，打开这样的行会重新运行会话的原始提示词，而不是拒绝，将数周前的任务拉回前台。

<h3 id="worktree-has-commits-that-are-not-pushed-anywhere">
  Worktree 有未推送到任何地方的提交
</h3>

您尝试删除一个[后台会话](/docs/zh-CN/agent-view#what-deleting-a-session-removes)，其 worktree 持有 Claude Code 无法确认保存在其他地方的提交。Claude Code 保留 worktree 和会话行，而不是在未查看的情况下销毁提交。`claude rm` 命名分支和未推送的提交，并说明如何继续：

```text theme={null}
kept 7c5dcf5d — its worktree is still at “/home/you/project/.claude/worktrees/fix-login”
  2 unpushed commits on “claude/fix-login”: a1b2c3d “Fix login flow” and 1 more. They exist on no remote, so deleting the worktree would lose them.
  push them and run 'claude rm 7c5dcf5d' again, or discard the worktree and its commits: claude rm 7c5dcf5d --discard-unpushed a1b2c3d000000000000000000000000000000000@0123456789abcdef0123456789abcdef
```

当 Claude Code 无法总结提交时，详细行读取 `The worktree has unpushed commits`。在 [Agent 视图](/docs/zh-CN/agent-view)中，会话的行显示 `not deleted` 和相同的原因。

远程上的提交不会阻止删除。本地副本中您的 `origin` 远程的默认分支上的提交也不会，只要该分支在您的主检出中检出，即仓库目录本身而不是 worktree。

**要做什么：**

* 要保留提交，推送 worktree 的分支，或将其合并到在主检出中检出的默认分支，然后再次删除会话
* 要丢弃提交，运行消息打印的 `claude rm <id> --discard-unpushed` 命令，或在 Agent 视图中的会话行上再次按 `Ctrl+X` 两次。这会删除会话和 worktree 以及其分支、未推送的提交和任何未提交的更改。如果 worktree 自拒绝以来获得了提交，Claude Code 再次保留它并显示更新的状态
* 当消息说 worktree 也由另一个完成的会话记录时，再次删除不会丢弃它：推送提交，然后再次删除会话

在 v2.1.268 之前，`claude rm` 将提交摘要放在 `kept` 行本身上。当 `claude rm` 无法总结提交时，`kept` 行读取 `worktree has commits that are not pushed anywhere` 代替摘要。

在 v2.1.260 之前，消息没有命名分支或提交，再次删除被拒绝的方式相同：删除会话而不推送意味着使用 `git worktree remove --force <path>` 自己删除 worktree，然后再次运行 `claude rm <id>`。

在 v2.1.248 之前，在主检出中检出的默认分支不计数：您已经合并到那里的分支仍然触发此拒绝，直到其提交到达远程。

<h3 id="terminal-host-process-died">
  终端主机进程已死亡
</h3>

每个[后台会话的](/docs/zh-CN/agent-view)终端在后台服务下的主机进程中运行，该进程在服务仍然持有其连接时死亡，因此无法到达会话。

在 Linux 和 WSL 上，后台服务每隔几秒检查每个主机进程，当进程已退出但其与服务的连接从未关闭时标记会话失败，并在 [Agent 视图](/docs/zh-CN/agent-view#read-session-state)中的其行上显示原因：

```text theme={null}
terminal host process died — press Enter to restart
```

从 shell，`claude attach <id>` 重启已标记为死主机失败的会话，否则打印原因并退出：

```text theme={null}
Couldn't attach to <id> — This session's terminal host process died (the conversation is saved) — run `claude attach <id>` again to restart it on a fresh host.
```

对话无论如何都被保存。

运行 [shell 命令](/docs/zh-CN/agent-view#run-a-shell-command)的行显示 `terminal host process died — its output is gone; the command was not run again`，`claude attach` 打印 `This command's terminal host process died — its output is gone and the command was not run again`。Claude Code 从不为您重新运行该命令。

**要做什么：**

* 在 Agent 视图中，在失败的行上按 `Enter`；会话在新的主机进程上重启，对话恢复
* 从 shell，再次运行 `claude attach <id>`。Claude Code 打印 `Session <id>'s terminal host died — restarting it on a fresh one…` 并重新打开会话
* 您无法以这种方式重启 shell 命令行；再次分派命令以重新运行它

在 v2.1.247 之前，死主机进程可能通过后台服务运行的每个活跃性检查，因此打开会话无限期地显示 `opening… · esc to cancel`，`claude attach <id>` 等待而不报告错误。

<h3 id="session-isnt-responding">
  会话没有响应
</h3>

您打开了一个[后台会话](/docs/zh-CN/agent-view)，后台服务接受了打开，但大约十秒钟内没有输出到达，因此 Claude Code 得出结论，中继会话终端的进程无法传递输出，并结束尝试而不是等待。

在 Agent 视图中，Claude Code 在页脚中提供重启：

```text theme={null}
Press enter again to restart this session — it isn't responding (its conversation is saved and resumes).
```

从 shell，`claude attach <id>` 打印原因并退出：

```text theme={null}
Couldn't attach to <id> — Session isn't responding — `claude stop <id>`, then `claude attach <id>` restarts it (the conversation is saved).
```

Claude Code 从不为您重启运行 [shell 命令](/docs/zh-CN/agent-view#run-a-shell-command)的行，因为重启会再次运行该命令。

**要做什么：**

* 在 Agent 视图中，在同一行上再次按 `Enter`。Claude Code 停止无响应的进程并重启会话，对话恢复。没有第二次按下就不会停止任何东西
* 从 shell，运行 `claude stop <id>`，然后 `claude attach <id>`
* 对于 shell 命令行，在 Agent 视图中按 `Ctrl+X` 或运行 `claude stop <id>` 停止它；再次分派命令以重新运行它

<h3 id="session-was-stopped-while-the-respawn-was-in-flight">
  会话在 respawn 进行中时被停止
</h3>

您打开了一个[后台会话](/docs/zh-CN/agent-view)，其进程未运行，当 Claude Code 重启它时，另一个 Claude Code 进程停止了它，例如在另一个终端中 `claude stop`。Claude Code 保持会话停止：

```text theme={null}
Session <id> was stopped while the respawn was in flight
```

打开您刚刚分派的会话，当其进程仍在启动时，会改为等待进程。在 v2.1.246 之前，在那一刻打开它可能会停止它并显示此消息。

**要做什么：**

* 如果您没有停止会话，在 Agent 视图中再次打开其行或运行 `claude respawn <id>` 重启它
* 如果您自己停止了它，没有什么剩下要做的：会话保持停止

<h3 id="session-agent-no-longer-available">
  会话 Agent 不再可用
</h3>

您恢复了一个正在运行[自定义 Agent](/docs/zh-CN/sub-agents#invoke-subagents-explicitly) 的会话，该会话使用 `--agent` 或 `agent` 设置启动，Claude Code 没有找到具有该名称的 Agent。它首先搜索会话的原始目录（当您已[信任该工作区](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust)时），然后搜索您恢复的目录。会话仍然恢复，但使用默认工具，因此 Agent 的工具限制不再适用：

```text theme={null}
This session was running agent 'code-reviewer', which is no longer available (no agent by that name in /home/you/project). Continuing with the default tools and system prompt — the agent's tool restrictions no longer apply. To restore it, re-create the agent, or resume with an explicit --agent <name>.
```

警告仅命名 Claude Code 搜索的目录，它出现在恢复的对话中，无论您唤醒[后台会话](/docs/zh-CN/agent-view)、运行 `/resume` 或 `claude --resume`，还是在[非交互模式](/docs/zh-CN/headless)中恢复，在非交互模式中它也会发送到 stderr。使用 `--input-format stream-json` 的会话不显示它，因为 Agent SDK 在启动后提供 Agent。

Claude Code 不会将回退保存到会话，因此警告在每次恢复时重复，直到您采取行动。内置 `claude` Agent 不触发警告，因为回退到默认工具集对它没有改变。在 v2.1.216 之前，Claude Code 无声地继续作为默认 Agent，查找仅覆盖您恢复的目录，因此项目范围的 Agent 在从另一个目录恢复时丢失。

**要做什么：**

* 在会话的项目中的 `.claude/agents/<name>.md` 或个人 Agent 的 `~/.claude/agents/<name>.md` 重新创建 Agent 文件，然后再次恢复
* 或使用 `--agent <name>` 恢复，命名确实存在的 Agent，以改为作为该 Agent 运行会话
* 如果 Agent 是项目范围的，您还没有信任会话的原始目录，在那里运行一次 Claude Code，接受信任对话框，然后再次恢复

<h3 id="claude_code_process_wrapper-launcher-errors">
  CLAUDE\_CODE\_PROCESS\_WRAPPER 启动器错误
</h3>

[`CLAUDE_CODE_PROCESS_WRAPPER`](/docs/zh-CN/corporate-launcher) 已设置，其值无法使用，因此 Claude Code 拒绝启动受影响的进程，而不是在没有启动器的情况下运行它。配置问题报告为以变量名开头并说明原因的消息，例如：

```text theme={null}
CLAUDE_CODE_PROCESS_WRAPPER: launcher `/opt/corp/launcher` is not an executable regular file
```

启动但在用 Claude Code 替换自己之前退出的启动器会使其启动的会话失败，会话在 Agent 视图中的行报告启动器 `must exec, not daemonize`，后跟启动器打印的任何内容。因启动器而无法启动或到达后台服务的会话会将启动器问题作为 `Couldn't reach the background service (...)` 内的原因报告。

**要做什么：**

* 将变量设置为以调用 `exec "$@"` 结尾的可执行文件的绝对路径。有关完整合同，请参阅[启动器合同](/docs/zh-CN/corporate-launcher#the-launcher-contract)
* 检查 `/status`，它在其 Self-exec 条目中显示解析的启动命令，并在运行的后台服务不匹配时警告，或从 shell 运行 `claude daemon status`
* 在[设置](/docs/zh-CN/corporate-launcher#set-up-the-launcher)的 `env` 块中修复值后，使用 `claude daemon stop --any` 重启后台服务，以便下一次分派启动一个包装的后台服务

<h3 id="eunknown-when-starting-a-background-session">
  启动后台会话时 EUNKNOWN
</h3>

Windows 拒绝使用没有标准名称的错误代码启动程序，因此失败显示为 `EUNKNOWN`。通常的触发器是软件限制策略，例如组策略或 AppLocker，阻止启动的程序。当您使用 `/background` 或 `claude --bg` 启动[后台会话](/docs/zh-CN/agent-view)时，错误出现：

```text theme={null}
Couldn't reach the background service (spawn background service: EUNKNOWN: unknown error, uv_spawn) — run 'claude daemon status'
```

在某些帐户上，消息说 `daemon` 代替 `background service`。

在 npm 安装上，在 `npm install -g @anthropic-ai/claude-code` 替换二进制文件时出现的 `EUNKNOWN` 与[重新安装期间的 `EACCES`](#eacces-when-starting-a-background-session) 有相同的原因，并在您在安装完成后重试时清除。

Claude Code 通过 PowerShell 启动后台服务，以便服务在关闭终端后存活，在安装时使用 PowerShell 7，否则使用 Windows PowerShell 5.1。当两个 PowerShell 都无法运行时，Claude Code 直接启动服务，因此仅阻止 PowerShell 的策略不会导致此错误。

在 v2.1.212 之前，Claude Code 仅使用 Windows PowerShell 5.1 启动服务，因此任何组策略阻止 PowerShell 5.1 的机器失败，出现 `Couldn't start the session — EUNKNOWN: unknown error, uv_spawn`，即使安装了 PowerShell 7。

**要做什么：**

* 如果消息读取 `Couldn't start the session`，升级到 v2.1.212 或更高版本。在早期版本上，您也可以在单独的终端中首先运行 `claude daemon run`，然后再次启动后台会话。该命令在终端的前台运行后台服务，因此服务仅在该终端保持打开时持续。
* 如果 npm 安装正在替换二进制文件，等待它完成，然后再次启动后台会话
* 如果错误在 v2.1.212 或更高版本上出现，而没有 npm 安装运行，请向您的 Windows 管理员确认是否有限制策略阻止了 Claude Code 可执行文件
* 如果关闭终端时后台服务停止，Claude Code 在没有 PowerShell 的情况下启动了它。安装 PowerShell 7，或要求您的管理员解除对 PowerShell 的阻止，以便服务可以超越终端。

<h3 id="eacces-when-starting-a-background-session">
  启动后台会话时 EACCES
</h3>

Claude Code 无法运行其自己的二进制文件来启动[后台服务](/docs/zh-CN/agent-view#the-supervisor-process)，该服务托管后台会话。在 npm 安装上，这通常意味着 `npm install -g @anthropic-ai/claude-code` 在那一刻替换二进制文件，无论您运行它还是[自动更新程序](/docs/zh-CN/setup#auto-updates)运行。当您从 [Agent 视图](/docs/zh-CN/agent-view)打开会话时，错误出现：

```text theme={null}
Couldn't start the background service — spawn background service: EACCES: permission denied, posix_spawn '/usr/local/lib/node_modules/@anthropic-ai/claude-code/bin/claude'
```

当您使用 `/background` 或 `claude --bg` 启动会话时，相同的原因出现在 `Couldn't reach the background service (...)` 内。在相同的重新安装窗口期间，错误可能命名另一个代码，例如 `ENOENT` 或 `ENOEXEC`，或在 Windows 上 `EUNKNOWN` 或 `EPERM`；跨重试持续的 `EUNKNOWN` 有[不同的原因](#eunknown-when-starting-a-background-session)。

在 npm 安装上，Claude Code 等待重新安装完成并自动重试：最多十秒，以及在 npm 安装 Claude Code 在机器上仍然可见运行时最多两分钟，这涵盖了另一个 Claude Code 进程下载更新。当安装超过该等待时，失败命名更新而不是裸错误代码：

```text theme={null}
Claude Code is being updated by npm on this machine (still not runnable after 2 min, EACCES) — try again when the update finishes
```

在 v2.1.257 之前，等待在每种情况下都在十秒处停止，因此此错误在另一个 Claude Code 进程仍在下载更新时出现。在 v2.1.246 之前，Claude Code 立即失败，没有等待。

**要做什么：**

* 等待几秒钟，然后打开会话或再次分派。当消息说 Claude Code 正在更新时，在更新完成后重试。
* 如果错误在没有 npm 安装运行时持续，您的用户无法运行已安装的二进制文件。检查其权限及其目录的权限，或重新安装 Claude Code。

<h3 id="background-service-exited-before-it-became-reachable">
  后台服务在变得可达之前退出
</h3>

Claude Code 作为[后台服务](/docs/zh-CN/agent-view#the-supervisor-process)启动的进程在接受连接之前退出，因此 Claude Code 无法打开您的会话。当服务在退出前打印错误时，括号中的原因给出退出码或信号以及服务打印的第一行，它命名停止它的内容：

```text theme={null}
Couldn't reach the background service (background service exited before it became reachable (exit code N): <the service's first error line>) — run 'claude daemon status'
```

当您从 [Agent 视图](/docs/zh-CN/agent-view)打开会话时，相同的原因跟随 `Couldn't start the background service —`。当服务在退出前没有打印任何内容时，消息说 `nothing on stderr`。

Claude Code 使用服务的错误行报告失败。在 v2.1.246 之前，失败仅在 45 秒等待后显示，作为 `background service did not become reachable within 45s`，没有服务的错误行。

两个引用的原因有已知的成因：

* `Error: claude native binary not installed.`：npm 安装在那一刻替换 Claude Code 二进制文件，因此服务运行了 npm 的占位符。在安装完成后重试；如果在没有安装运行时该行持续出现，[完成 npm 安装](/docs/zh-CN/troubleshoot-install#native-binary-not-found-after-npm-install)。在 v2.1.257 之前，macOS npm 自更新在安装窗口期间的每次启动时产生此失败。
* 在 Windows 上，`nothing on stderr` 和退出码 1，每次启动：`daemon.lock` 命名一个 Claude Code 既无法发信号也无法证明已消失的进程，因此每个新服务得出结论另一个持有锁并退出。Claude Code 可以证明其编写者已消失的锁会自动替换，不会产生此失败。当失败在每次启动时重复时，删除 `~/.claude/daemon.lock`，然后打开会话或再次分派。在 v2.1.257 之前，这样的锁阻止了每次启动，直到您删除了文件。

**要做什么：**

* 如果消息引用一行，修复它命名的内容，然后打开会话或再次分派。下一次尝试再次启动服务
* 运行 `claude daemon status` 检查现在是否有服务运行

<h3 id="working-directory-no-longer-exists-when-starting-a-background-session">
  启动后台会话时工作目录不再存在
</h3>

您启动[后台会话](/docs/zh-CN/agent-view)所在的目录在会话启动期间被删除。Claude Code 不启动会话，消息命名缺失的目录：

```text theme={null}
Couldn't start a background session (working directory no longer exists or is not accessible: /tmp/demo)
```

在 v2.1.257 之前，会话似乎启动，然后在 Agent 视图中显示为具有相同原因的失败行。

在 v2.1.281 之前，当您启动会话之前目录已经消失时，此消息也出现。该情况报告 [`could not be resolved on disk`](#workspace-not-trusted-when-dispatching-a-background-session)。

**要做什么：**

* 重新创建消息命名的目录，或从存在的目录分派，然后重试

<h3 id="workspace-not-trusted-when-dispatching-a-background-session">
  分派后台会话时工作区不受信任
</h3>

您在未[信任](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust)的目录中启动或重启[后台会话](/docs/zh-CN/agent-view)，工作区信任对话框无法出现以询问您。Claude Code 不启动会话：

```text theme={null}
Workspace not trusted. Run `claude` in /path/to/project once and accept the trust prompt, then retry.
```

从会话自己的目录中的终端，相同的命令会改为显示信任对话框，并在您接受后启动会话。此消息出现在无法显示对话框的地方，例如在脚本中，或当您从不同于其自己的目录重启会话时。

两个变体命名不同的原因：

* **`The home directory is trusted one session at a time`**：会话的目录是您的主目录。Claude Code 从不保存主目录的信任，因此在早期会话中在那里接受对话框不计数。
* **`<path> could not be resolved on disk`**：Claude Code 无法在磁盘上找到会话的目录。

在 v2.1.286 之前，在 Windows 上，如果某个您已信任的目录的信任记录是以不同字母大小写的路径保存的，此消息也可能在该目录中出现。请更新到 v2.1.286 或更高版本。

**要做什么：**

* 在消息命名的目录中运行 `claude` 并接受信任对话框，然后再次运行该命令
* 对于主目录消息，从您的主目录中的终端运行该命令，以便对话框可以出现，或改为从项目目录启动会话
* 对于 `could not be resolved on disk` 消息，重新创建目录，或从存在的目录启动新会话

<h2 id="wrapper-and-ide-errors">
  包装器和 IDE 错误
</h2>

这些错误来自启动 Claude Code 的程序，例如 IDE 扩展或 [Agent SDK](/docs/zh-CN/agent-sdk/overview) 应用程序，而不是来自 Claude Code 本身。

<h3 id="claude-code-process-exited-with-code-n">
  Claude Code 进程以代码 N 退出
</h3>

底层 `claude` 进程以非零代码退出。仅凭退出代码无法说明失败的原因：真正的错误在于进程自身的输出，包装器会在捕获时附加该输出，否则将其保留在日志中。

```text theme={null}
Error: Claude Code process exited with code 1
```

在 Windows 上，本机构建可能在回合完成后立即以代码 `4294967295` 退出。当该退出发生在回合边界处，没有等待的消息且没有后台任务运行时，[VS Code 扩展](/docs/zh-CN/vs-code)会静默关闭会话而不显示此错误。您的下一条消息将恢复对话。

在 v2.1.273 之前，扩展在每个回合边界处显示该退出的错误，即使没有任何内容丢失。

**应该怎么做：**

* 在 VS Code 中，点击错误显示的**查看输出日志**链接以查看底层故障
* 在 Agent SDK 应用程序中，在消息循环周围捕获错误。[CLI 进程退出](/docs/zh-CN/agent-sdk/troubleshooting#cli-process-exit)下的条目涵盖了您的代码在每种 SDK 语言中接收的内容。
* 在终端中的同一项目中运行 `claude`。故障通常会在那里重现，并显示其真实错误消息，您可以在此页面上查找。
* 在终端中运行 `claude doctor` 以检查安装和配置

<h3 id="could-not-locate-the-claude-cli-on-path">
  无法在 PATH 上找到 Claude CLI
</h3>

当您在集成终端中打开 Claude Code、终端的 shell 是 PowerShell 且扩展无法在 PATH 上找到已安装的 `claude` 可执行文件时，[VS Code 扩展](/docs/zh-CN/vs-code)在 Windows 上显示此错误。扩展拒绝启动 Claude Code，直到它在 PATH 上找到已安装的 `claude`。

```text theme={null}
Failed to run Claude Code: Error: Could not locate the Claude CLI on PATH. Launching by name in a PowerShell terminal would run a 'claude' from the open folder instead of the installed CLI, so the launch was blocked. Make sure the Claude CLI's install directory is on your system PATH (not only your PowerShell profile), then restart VS Code and try again. VS Code reads PATH when it starts, so PATH changes take effect only after a restart.
```

**应该怎么做：**

* 在 VS Code 外打开新的 PowerShell 窗口并运行 `where.exe claude`。如果它没有打印路径，则 CLI 不在您的 PATH 上：按照[验证您的 PATH](/docs/zh-CN/troubleshoot-install#verify-your-path)添加其安装目录。如果它打印了路径，该条目来自您的 PowerShell 配置文件或 VS Code 尚未获取的 PATH 更改；接下来的两个步骤涵盖这些情况。
* 将 PATH 条目设置为用户或系统环境变量，而不是在您的 PowerShell 配置文件中。扩展不运行您的配置文件，因此仅存在于那里的 PATH 编辑永远无法到达它。
* 更改 PATH 后重启 VS Code。扩展检查 VS Code 在启动时捕获的 PATH，因此 PATH 更改仅在重启后生效。

<h3 id="the-connection-to-claude-code-ended-before-this-message-completed">
  Claude Code 的连接在此消息完成前结束
</h3>

[VS Code 扩展](/docs/zh-CN/vs-code)将您的消息发送到 `claude` 进程，连接在进程确认或完成之前无错误地结束。扩展无法判断消息是否已处理，因此它要求您再次发送：

```text theme={null}
The connection to Claude Code ended before this message completed — it may not have been processed, so please send it again.
```

**应该怎么做：**

* 再次发送消息。下一条消息启动一个新的 `claude` 进程，该进程恢复对话。
* 如果重复发生，在同一项目的终端中运行 `claude`。持续结束进程的故障通常会在那里重现，并显示其真实错误消息。

<h2 id="rewind-warnings-and-errors">
  Rewind 警告和错误
</h2>

这些消息来自 [`/rewind`](/docs/zh-CN/checkpointing) 代码恢复。`Restored the code, but skipped N files` 是一个警告，表示 Claude Code 跳过了某些路径。`No files were restored` 是一个错误，表示它没有恢复任何内容。

<h3 id="restored-the-code-but-skipped-files">
  Restored the code, but skipped files
</h3>

一个 `/rewind` 代码恢复跳过了一个或多个跟踪的路径，而不是通过它们进行写入或删除。Claude Code 在以下情况下会跳过一个路径：

* 它是或变成了符号链接、硬链接或其他非常规文件
* 自检查点以来其目录已更改
* 其备份无法安全读取

跳过的路径保持其当前内容。在 v2.1.216 之前，`/rewind` 通过跟踪路径上的链接进行写入和删除，并且不报告部分恢复。

```text theme={null}
Restored the code, but skipped 2 files: the tracked path is (or became) a link or other non-regular file, its directory changed since the checkpoint, or its backup could not be safely read. Skipped files were left untouched — run with --debug for the paths.
```

**应该怎么做：**

* 确定哪些文件被跳过，以便您可以使用下面的步骤处理每个文件。该消息仅给出计数；`~/.claude/debug/<session-id>.txt` 中的调试日志在恢复运行时命名每个跳过的路径，因此在下次恢复之前使用 `/debug` 打开调试日志。在 macOS 或 Linux 上，您可以直接找到链接：`find . -type l` 用于符号链接，`find . -type f -links +1` 用于硬链接文件。
* 如果跳过的文件是您有意创建的链接，例如由点文件管理器管理的配置文件或由 pnpm 等工具硬链接的文件，rewind 保持其内容不变。要撤销会话对其所做的更改，请要求 Claude 反转编辑或自己编辑文件
* 如果您没有创建该链接，请在信任其内容之前检查该路径

<h3 id="no-files-were-restored">
  No files were restored
</h3>

当您使用 [`/rewind`](/docs/zh-CN/checkpointing) 恢复代码且无法恢复该检查点中的任何文件时，Claude Code 会显示此消息。对于每个文件，要么 Claude Code 在编辑前保存的备份丢失，要么 Claude Code 无法写入或删除该文件。

```text theme={null}
Failed to restore the code:
No files were restored: 1 file failed (backup missing, or the file could not be updated)
```

Claude Code 在 [retention sweep](/docs/zh-CN/claude-directory#cleaned-up-automatically) 中删除会话的备份，默认情况下在会话最后一次保存后约 30 天。如果您在之后恢复会话，`/rewind` 仍会列出其检查点，但恢复到其中一个可能会因此错误而失败。如果消息还说 `N paths were skipped for link safety`，请参阅 [Restored the code, but skipped files](#restored-the-code-but-skipped-files) 了解这些路径。

当您分叉会话时，例如使用 [`--fork-session`](/docs/zh-CN/cli-reference#cli-flags) 或 [`/branch`](/docs/zh-CN/sessions#branch-a-session)，Claude Code 会将原始会话的备份复制到分叉中。当 Claude Code 无法复制备份时，例如因为磁盘已满，该备份在分叉中丢失。恢复到需要它的检查点可能会因此错误而失败。

**应该怎么做：**

* 以另一种方式撤销更改：要求 Claude 反转其编辑，或从版本控制恢复文件。当备份消失时，再次运行 `/rewind` 会以相同方式失败。
* 如果 Claude Code 无法写入或删除文件，请修复阻止写入的内容，例如文件权限，然后再次运行 `/rewind`。
* 要在将来的会话中保留更长时间的备份，请提高 [`cleanupPeriodDays`](/docs/zh-CN/settings-reference#cleanupperioddays)。

在 v2.1.260 之前，Claude Code 无声地跳过备份丢失的文件，恢复似乎成功了。

<h2 id="session-saving-warnings">
  会话保存警告
</h2>

当 Claude Code 未保存您的会话记录时，它会在输入框下方的持久行上显示这些警告。无论哪种方式，会话都会继续工作；这些警告告诉您该会话稍后可能在 [`--resume`](/docs/zh-CN/sessions) 中丢失。

<h3 id="transcript-writes-are-failing">
  记录写入失败
</h3>

Claude Code 在您工作时将记录保存到磁盘，其对[记录文件](/docs/zh-CN/sessions#where-transcripts-are-stored)的写入失败。该消息会说明原因并显示底层错误代码，例如磁盘已满：

```text theme={null}
Transcript writes are failing (disk full — ENOSPC) · recent messages may not be saved for resume
```

警告在不同的时间点出现，具体取决于错误：

* 对于不会自行清除的条件，在首次失败时出现：磁盘已满、超过磁盘配额、文件系统为只读、路径超过文件系统长度限制，或在 macOS 和 Linux 上出现权限错误
* 对于所有其他情况，在至少跨越一分钟的重复失败后出现，包括 Windows 上的权限错误，其中防病毒扫描可能会导致单次写入失败，然后在重试时成功

在 v2.1.217 之前，Claude Code 会在没有警告的情况下丢弃失败的写入，稍后 `--resume` 缺少最近的消息是第一个迹象。

**应该怎么做：**

* 修复错误代码指出的条件：对于 `ENOSPC` 释放磁盘空间；对于 `EDQUOT` 提高或清除配额；对于 `EACCES`、`EPERM` 或 `EROFS` 恢复对记录位置的写入访问
* 警告会在下一次成功写入时自动清除；无需重启
* 在警告显示期间发送的消息稍后恢复会话时可能仍然丢失

<h3 id="transcript-saving-is-off-skip-prompt-history">
  因为设置了 CLAUDE\_CODE\_SKIP\_PROMPT\_HISTORY 所以记录保存已关闭
</h3>

此会话启动时设置了 [`CLAUDE_CODE_SKIP_PROMPT_HISTORY`](/docs/zh-CN/env-vars)，因此 Claude Code 不会为其写入任何记录或提示历史记录：

```text theme={null}
Transcript saving is off — CLAUDE_CODE_SKIP_PROMPT_HISTORY is set · --resume will not find this session; if unintended, unset it and restart
```

该变量是针对临时脚本会话的有意选择退出，但它也可以通过 shell 配置文件、包装脚本或导出它的父进程到达会话。

**应该怎么做：**

* 如果您有意设置了该变量，无需采取任何操作；该通知确认该会话不会出现在 `--resume`、`--continue` 或向上箭头历史记录中
* 如果您没有，请从启动 `claude` 的 shell 或脚本中删除该变量，然后启动新会话。当前会话中的消息不会被追溯保存。

<h3 id="transcript-saving-is-off-child-session-marker">
  因为继承了 CLAUDE\_CODE\_CHILD\_SESSION 标记所以记录保存已关闭
</h3>

Claude Code 在它生成的子进程中设置 [`CLAUDE_CODE_CHILD_SESSION`](/docs/zh-CN/env-vars)，并将继承它的交互式会话视为嵌套的：Claude Code 不会为其保存任何记录，因此 Claude 本身启动的会话不会填充您的 `--resume` 列表。此通知意味着您的当前会话继承了该标记：

```text theme={null}
Transcript saving is off — inherited CLAUDE_CODE_CHILD_SESSION marker · restart with CLAUDE_CODE_FORCE_SESSION_PERSISTENCE=1 to keep future transcripts
```

当您从另一个 Claude Code 会话内部运行 `claude` 时，该通知是预期的；当标记通过长期存在的中介（例如终端、`screen` 会话或 Claude Code 会话最初启动的启动器）泄露时，它会发出误分类信号。

在 tmux 内，Claude Code 检测到通过 tmux 服务器全局环境到达的标记，并继续保存，因此在这种情况下不会出现此通知。

**应该怎么做：**

* 如果您有意从另一个 Claude Code 会话内部启动了此会话，无需采取任何操作
* 如果这是顶级会话，请退出并使用设置的 [`CLAUDE_CODE_FORCE_SESSION_PERSISTENCE=1`](/docs/zh-CN/env-vars) 重新启动。保存从重新启动时开始应用，因此在此之前发送的消息不会被保存。
* 要修复从同一终端或启动器的未来启动，请从其环境中删除 `CLAUDE_CODE_CHILD_SESSION`

<h2 id="configuration-warnings">
  配置警告
</h2>

Claude Code 将大多数这些消息写入 stderr，而不是写入对话中，并在启动时写入大多数消息。当消息出现在其他地方（例如在调试日志中或作为对话视图中的启动通知）或在其他时间（例如[请求时的无法识别的模型诊断行](#unrecognized-model-id-on-a-request)）时，条目会说明这一点。

<h3 id="exited-after-an-unrecoverable-interface-error">
  Claude Code 因无法恢复的界面错误而退出
</h3>

当 Claude Code 退出时，它会打印此消息，因为其终端界面在任一渲染器中遇到了无法恢复的错误。第二句仅在[全屏](/docs/zh-CN/fullscreen)渲染器启动时发生错误时出现：

```text theme={null}
Claude Code exited after an unrecoverable interface error (<error>). It happened while the fullscreen renderer was starting, so the next launch will use the classic renderer (CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1 forces that any time).
```

**要做什么：**

* 再次启动 Claude Code。要继续该对话，请在同一目录中运行 `claude --resume`。
* 如果消息命名全屏渲染器，[全屏渲染](/docs/zh-CN/fullscreen#fullscreen-renderer-didnt-finish-starting)说明下一次启动的操作，这取决于您如何打开全屏，以及如何再次尝试全屏或保持经典渲染器。

在 v2.1.236 之前，Claude Code 在此类错误后退出而不打印消息。

<h3 id="agent-descriptions-are-over-the-15000-token-limit">
  Agent 描述超过 15.0k token 限制
</h3>

Claude Code 将此警告显示为对话视图中的启动通知，而不是在 stderr 上。您的[子代理](/docs/zh-CN/sub-agents)（内置子代理除外）的组合描述超过 Claude Code 估计的 15,000 个 token。每个 Agent 计算其名称加上其 `description` frontmatter。Claude Code 加载每个 Agent，无论总数是否超过限制，因此警告不会改变加载的内容。

```text theme={null}
Agent descriptions are over the 15.0k-token limit (~16.2k tokens) · ask Claude to trim agent descriptions in .claude/agents/
```

**要做什么：**

* 缩短您的 Agent 文件的 `description` frontmatter，或要求 Claude 为您修剪它们。
* 删除您不再使用的 Agent 文件。

<h3 id="a-skill-command-or-workflow-wasnt-loaded-because-its-name-is-reserved">
  skill、命令或工作流未被加载，因为其名称是保留的
</h3>

skill 文件夹、frontmatter `name`、`.claude/commands/` 中的文件或子文件夹，或[保存的工作流](/docs/zh-CN/workflows#save-the-workflow-for-reuse)使用名称 `anthropic-skills` 或以 `anthropic-skills:` 开头的名称。Claude Code [为从 claude.ai 同步的 skill 保留该名称](/docs/zh-CN/skills#names-reserved-for-synced-skills)，不加载该项。

Claude Code 将此警告显示为对话视图中的启动通知，而不是在 stderr 上：

```text theme={null}
Not loaded: rename .claude/skills/anthropic-skills, then restart — its name uses "anthropic-skills", a name reserved for the skills synced from your claude.ai account
```

通知命名它拒绝的第一项需要更改的内容：要重命名的文件夹或文件、要编辑的 `name:` 行，或要重命名的工作流。当拒绝多个项时，通知以计数结尾，例如 `· 2 more`，[调试日志](/docs/zh-CN/debug-your-config)命名每一个。

**要做什么：**

* 重命名通知命名的项，或编辑它指向的 `name:` 行，然后重启会话。

在 v2.1.282 之前，Claude Code 加载具有这些名称的 skill 和命令。

<h3 id="workspace-has-not-been-trusted">
  工作区尚未被信任
</h3>

Claude Code 在项目的 `.claude/settings.json` 或 `.claude/settings.local.json` 中找到了 `permissions.allow` 规则或 `permissions.additionalDirectories` 条目，但未应用它们，因为[来自项目设置的允许规则需要工作区信任](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust)。计数、设置名称和消息中命名的文件因您的配置而异。`deny` 和 `ask` 规则不受影响。

```text theme={null}
Ignoring 2 permissions.allow entries from .claude/settings.local.json: this workspace has not been trusted. Run Claude Code interactively here once and accept the trust dialog, or set projects["/Users/you/project"].hasTrustDialogAccepted: true in /Users/you/.claude.json.
```

**要做什么：**

* 在目录中运行 `claude` 并接受信任对话框。[项目允许规则和工作区信任](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust)说明该接受涵盖的文件夹。
* 在[非交互模式](/docs/zh-CN/headless)中使用 `-p` 不显示对话框。使用消息打印的确切 `projects` 键在 `~/.claude.json` 中设置 `hasTrustDialogAccepted` 条目。
* 如果消息命名 `.claude/settings.local.json` 并且您在 git 仓库外或主目录中启动了 Claude Code，请更新到 v2.1.200 或更高版本。版本 2.1.196 至 2.1.199 在这些工作区中将您自己的 `.claude/settings.local.json` 视为仓库提供的。在 v2.1.207 及更高版本上，如果您尚未信任该文件夹，在 git 仓库外仅更新是不够的：确定文件夹不在仓库内会运行 git，Claude Code 仅在您接受信任对话框后才运行该检查，因此请使用第一步。您的主目录和任何其他[配置主目录](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust)是豁免的，不等待对话框。请参阅[项目允许规则和工作区信任](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust)。

<h3 id="working-directory-is-a-network-path">
  工作目录是网络路径
</h3>

Claude Code 不将网络路径添加为工作目录。查找网络路径可能会联系它命名的主机，在 Windows 上该联系可能会向主机发送您的凭据，因此 Claude Code 拒绝该路径而不查找它。当您使用此类路径运行 `/add-dir` 时，或作为启动时的警告，您会看到此消息。当它在启动时出现时，Claude Code 启动时不包含该目录。

```text theme={null}
\\server\share is a network path, which cannot be added as a working directory. On Windows, map the share to a drive letter and pass it at launch with --add-dir (a drive letter added mid-session does not yet carry remote-read trust).
```

Claude Code 以这种方式拒绝的路径包括：

* UNC 共享，例如 `\\server\share`
* 自动挂载路径，例如 `/net/<host>`，除非您从该主机的自动挂载下的目录启动了 Claude Code
* 通过符号链接或连接点到达网络位置的本地路径

映射的驱动器号和 `\\wsl$` 路径不计为网络路径。

**要做什么：**

* 在 Windows 上，将共享映射到驱动器号，例如使用 `net use Z: \\server\share`，并在启动时使用 `claude --add-dir Z:\` 传递驱动器。
* 在 macOS 或 Linux 上，将共享挂载到本地路径并改为添加该路径。
* 如果路径在 `permissions.additionalDirectories` 中，请从列出它的设置文件中删除它。

在 v2.1.257 之前，Claude Code 接受可达的网络路径作为工作目录。

<h3 id="remote-managed-settings-failed-to-load">
  远程托管设置加载失败
</h3>

您的会话符合[服务器托管设置](/docs/zh-CN/server-managed-settings)的条件，但 Claude Code 无法获取它们或无法应用服务器返回的内容，因此在交互式会话中显示此警告。

括号中的原因命名失败的内容，例如 `network error`、`request timed out` 或 `authentication rejected (401)`。原因 `no setting in the server response could be applied as written` 意味着服务器已应答，但它返回的设置都没有通过[验证](/docs/zh-CN/server-managed-settings#invalid-entries-in-delivered-settings)。在 v2.1.282 之前，此原因显示为 `server returned invalid settings`。

该行的其余部分说明会话运行的策略：

* **从较早的成功获取缓存的设置**：Claude Code 在该缓存策略上运行会话，但[扣留的环境变量](/docs/zh-CN/server-managed-settings#fetch-and-caching-behavior)除外，该行显示 `using cached policy`。
* **无缓存**：Claude Code 在没有服务器托管设置的情况下运行会话，该行显示 `no remote policy applied`。

**要做什么：**

* 对消息命名的原因采取行动：对于网络原因，检查此计算机是否可以到达 `api.anthropic.com`；对于身份验证原因，使用 `/status` 检查您的登录
* 对于 `no setting in the server response could be applied as written`，要求您的管理员更正服务器上的设置
* 运行 `/status` 或 `claude doctor` 以获取完整诊断

在 v2.1.248 之前，Claude Code 仅在调试日志中报告失败的设置获取。

<h3 id="managed-settings-were-not-approved">
  托管设置未被批准
</h3>

您的组织的[服务器托管设置](/docs/zh-CN/server-managed-settings)包括需要您批准的设置，您拒绝了[安全批准对话框](/docs/zh-CN/server-managed-settings#security-approval-dialogs)，因此 Claude Code 退出而不应用它们：

```text theme={null}
Managed settings were not approved; exiting without applying them.
```

**要做什么：**

* 再次启动 Claude Code 并批准对话框以在您的组织设置下继续。拒绝的对话框不会被记住，因此在下一次启动时会再次出现。
* 如果您对对话框列出的设置不确定，请在批准前询问维护您的组织托管设置的人

<h3 id="managed-settings-block-the-default-model">
  托管设置阻止默认模型
</h3>

您的组织的[托管设置](/docs/zh-CN/managed-settings)阻止默认选项解析到的模型以及它可以降级到的每个模型。将在默认选项上启动的会话在启动时退出，而不是运行被阻止的模型。您看到的消息取决于阻止它的设置。当 [`deniedModels`](/docs/zh-CN/model-config#block-specific-models-or-versions) 列表阻止它时，消息显示为：

```text theme={null}
Claude Code can't start: your organization's managed settings block the default model (claude-opus-5-5) in "deniedModels", and none of the models they allow can be used as the default instead. Ask your administrator to update "deniedModels" or "availableModels".
```

当 [`availableModelsMatch`](/docs/zh-CN/settings-reference#availablemodelsmatch) 设置为 `"exact"` 的 `availableModels` 列表省略它时，消息显示为：

```text theme={null}
Claude Code can't start: your organization allows only the models listed in "availableModels", and none of them can be used as the default model (claude-opus-5-5 isn't listed). Ask your administrator to update "availableModels".
```

**要做什么：**

* 如果您管理设置，请将您的用户可以运行的模型添加到 `availableModels`，或缩小阻止每个备用模型的 `deniedModels` 条目。[阻止特定模型或版本](/docs/zh-CN/model-config#block-specific-models-or-versions)描述默认选项如何降级
* 如果您不管理它们，请将消息发送给您的管理员。您自己的设置文件无法扩大托管的 `availableModels` 或 `deniedModels` 列表

<h3 id="managed-settings-dont-allow-this-api-provider">
  托管设置不允许此 API 提供商
</h3>

您的组织的[托管设置](/docs/zh-CN/managed-settings)设置了 [`allowedProviders`](/docs/zh-CN/settings-reference#allowedproviders) 列表，会话的 API 提供商不在其上，或会话使用的端点不是按该条目要求的方式固定的。Claude Code 在启动时、登录前或会话下次联系 API 时拒绝。消息以允许的提供商开头：

```text theme={null}
Your organization's managed settings allow Claude Code to use: Anthropic API, Amazon Bedrock.
```

当列表为空时，消息改为显示：

```text theme={null}
Your organization's managed settings allow Claude Code to use no API provider at all (allowedProviders is an empty list), so it cannot start on this machine.
```

当每个条目都无法识别时，括号内容改为 `(allowedProviders lists only unrecognized entries)`。

**要做什么：**

* 按照消息的 `To continue:` 步骤进行
* 如果您管理设置，消息中以 `Admins:` 开头的行命名要添加的条目或要固定的值，[`allowedProviders`](/docs/zh-CN/settings-reference#allowedproviders) 条目说明哪个源的 `env` 块可以固定它

<h3 id="mcp-server-is-blocked-by-enterprise-managed-policy">
  MCP 服务器被企业托管策略阻止
</h3>

您在 `/mcp` 中的服务器上选择了**重新连接**，或在那里重新打开了禁用的服务器，而[限制 MCP 服务器](/docs/zh-CN/managed-mcp)的设置阻止了该服务器。Claude Code 拒绝连接它并显示：

```text theme={null}
MCP server <name> is blocked by enterprise managed policy
```

这些设置中的任何一个都可以产生该消息：

* 与服务器匹配的 [`deniedMcpServers`](/docs/zh-CN/managed-mcp#policy-based-control-with-allowlists-and-denylists) 条目，包括您自己的 `~/.claude/settings.json` 或项目的 `.claude/settings.json` 中的条目
* 服务器不匹配的 [`allowedMcpServers`](/docs/zh-CN/managed-mcp#policy-based-control-with-allowlists-and-denylists) 列表
* 锁定了 `mcp` 的 [`strictPluginOnlyCustomization`](/docs/zh-CN/settings-reference#strictpluginonlycustomization)，这会阻止在 `~/.claude.json` 和 `.mcp.json` 中配置的服务器
* [`disableClaudeAiConnectors`](/docs/zh-CN/mcp#disable-claude-ai-connectors)，当服务器是 claude.ai 连接器时

**要做什么：**

* 检查您自己的用户和项目设置文件中是否有这些设置之一，并更改或删除它
* 如果您自己的设置都不能解释该阻止，请询问您的管理员哪个托管设置阻止了服务器

在 v2.1.257 之前，`/mcp` 中的**重新连接**和重新启用可以连接被会话中途策略更新阻止的服务器。

<h3 id="managed-settings-document-could-not-be-parsed">
  托管设置文档无法解析
</h3>

您的组织部署了[托管设置](/docs/zh-CN/managed-settings)，其中一个部署的文档存在但无法解析为 JSON 对象，因此 Claude Code 在启动时以退出码 1 退出，而不是在没有该文档所携带策略的情况下运行。该行在消息前命名失败的源：

```text theme={null}
/Library/Application Support/ClaudeCode/managed-settings.json: Managed settings document could not be parsed as a JSON object; none of its settings are in effect. Fix or remove it.
```

源是以下之一：

* `managed-settings.json` 文件的路径或 `managed-settings.d` 下的放入文件
* macOS 托管首选项配置文件，`per-user managed preferences` 或 `device-level managed preferences`
* Windows 注册表值，`Registry: HKLM\SOFTWARE\Policies\ClaudeCode\Settings`

[查找 Claude Code 删除的条目](/docs/zh-CN/managed-settings#find-entries-claude-code-dropped)列出了使每个源无法解析的原因。

即使另一个管理员源提供了有效策略，Claude Code 也会拒绝启动。您在交互式会话、`claude -p`、Agent SDK 会话、[后台会话](/docs/zh-CN/agent-view)和大多数子命令（包括 `claude doctor`）中都会看到此错误。该拒绝有意采用失败关闭：Claude Code 无法解析的文档中的设置无法被强制执行，强行启动会在没有组织控制的情况下运行会话。

可解析文档中的 schema 问题不会产生此错误。[查找 Claude Code 删除的条目](/docs/zh-CN/managed-settings#find-entries-claude-code-dropped)涵盖 Claude Code 对此类问题的处理方式。

当 `managed-settings.d/` 目录存在但无法列出时，Claude Code 改为报告 `Managed settings drop-in directory could not be read:`，后跟底层错误。[查找 Claude Code 删除的条目](/docs/zh-CN/managed-settings#find-entries-claude-code-dropped)涵盖读取失败何时会在启动时退出。

**要做什么：**

* 如果您管理计算机，请修复命名的文档使其解析为 JSON 对象，或删除文件、配置文件或注册表值。空的 `managed-settings.json` 计为 `{}`，不会阻止启动。
* 如果您不管理，请要求您的管理员修复部署的文档。您自己的设置文件中的任何内容都不会导致或清除此错误。

<h3 id="unable-to-read-managed-policy-settings">
  无法读取托管策略设置
</h3>

您的组织部署了[托管设置](/docs/zh-CN/managed-settings)，其中一个部署的源存在但无法读取，原因例如 I/O 错误，而不是操作系统拒绝读取。在没有其他管理员源提供策略的情况下，Claude Code 在启动时退出，而不是在没有该源可能携带的策略的情况下运行：

```text theme={null}
Unable to read managed policy settings.
This machine may require organization login enforcement, but the policy file failed to load.
Contact your administrator.

Detail: <source>: <reason>
```

在相同的状态下，登录流程、来自已运行会话的 API 请求和 [`claude gateway`](/docs/zh-CN/claude-apps-gateway) 服务器会被拒绝，并显示第一行的一个变体，其中命名 [`allowedProviders`](/docs/zh-CN/settings-reference#allowedproviders)。

操作系统拒绝的读取（例如对仅限 root 的文件）不会导致此退出：[会话启动时不使用该源的策略](/docs/zh-CN/managed-settings#find-entries-claude-code-dropped)。对于无法解析的源，Claude Code 以[命名该源的不同消息](#managed-settings-document-could-not-be-parsed)退出。

**要做什么：**

* 如果您管理计算机，请修复 `Detail:` 行命名的问题，以便部署的源可以被读取，或删除该源
* 如果您不管理，请将消息发送给您的管理员。您自己的设置文件中的任何内容都不会导致或清除此错误

在 v2.1.285 之前，仅使用 claude.ai 或 Claude Console 凭据登录的会话以此消息退出，并且操作系统拒绝的读取也会产生它。

<h3 id="otelheadershelper-failed">
  otelHeadersHelper 失败
</h3>

当 [`otelHeadersHelper`](/docs/zh-CN/settings-reference#otelheadershelper) 脚本失败或打印不符合[脚本要求](/docs/zh-CN/monitoring-usage#script-requirements)的输出时，Claude Code 将此警告显示为终端界面中的通知，每个交互式会话一次。

当脚本持续失败时，导出失败，您的遥测后端从会话中接收不到任何内容。

`See /status:` 后的文本说明失败的内容，例如脚本的退出码后跟其错误输出：

```text theme={null}
otelHeadersHelper failed; telemetry is not being exported. See /status: exited 1: token service unreachable
```

**要做什么：**

* 运行 `/status` 以读取失败详情。
* 修复脚本使其在 30 秒内以 0 退出，并在 stdout 上打印由字符串标头值组成的 JSON 对象。请参阅[脚本要求](/docs/zh-CN/monitoring-usage#script-requirements)。
* 如果您的组织通过[托管设置](/docs/zh-CN/managed-settings)部署脚本，请要求维护它们的人修复它。

在[非交互模式](/docs/zh-CN/headless)中使用 `-p` 时，相同的失败改为在 stderr 上显示为 `otelHeadersHelper failed (OpenTelemetry export headers unavailable): <error>`。

<h3 id="headershelper-not-run">
  headersHelper 未运行
</h3>

Claude Code 仅使用 MCP 服务器的静态 `headers` 连接了它，并跳过了服务器的 [`headersHelper`](/docs/zh-CN/mcp#use-dynamic-headers-for-custom-authentication)，因为该助手是 shell 命令，而该文件夹没有保存的信任。当您手动在 `~/.claude.json` 中设置其条目时，或在主目录外，当您在交互式会话中为其接受信任对话框时，文件夹获得保存的信任。请参阅[在 headersHelper 运行前信任文件夹](/docs/zh-CN/mcp#trust-a-folder-before-its-headershelper-runs)了解此检查适用于哪些服务器。

Claude Code 仅在[非交互模式](/docs/zh-CN/headless)中写入此行，每个服务器一次。在交互式会话中，它改为将相同的拒绝写入调试日志。

```text theme={null}
MCP server 'internal-api': headersHelper not run — this workspace has no persisted trust; accept the trust dialog here once interactively, or set projects["/Users/you/project"].hasTrustDialogAccepted in /Users/you/.claude.json.
```

消息打印的 `projects` 键就是[项目允许规则和工作区信任](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust)中说明的 Claude Code 用来记录信任的文件夹。为父文件夹接受信任对话框不满足该检查，`-p` 或 SDK 会话也不满足。

**要做什么：**

* 在消息命名的文件夹中运行 `claude`，接受信任对话框，然后再次运行您的 `-p` 或 SDK 命令
* 在 `~/.claude.json` 中自己设置 `hasTrustDialogAccepted` 条目，使用消息打印的确切 `projects` 键
* 如果您在主目录中启动了会话，请从您已信任的项目目录工作。当您在主目录中接受信任对话框时，Claude Code 仅为当前会话保持该信任。

<h3 id="malformed-tool-content-rule">
  格式错误的 Tool(content) 规则
</h3>

您的某个设置文件中的[权限规则](/docs/zh-CN/permissions#permission-rule-syntax)不具有 `Tool` 或 `Tool(content)` 的形式，例如因为右括号后跟有文本或缺少其中一个括号。Claude Code 跳过该规则，并在交互式会话启动时的无效设置对话框中以及 [`claude doctor`](/docs/zh-CN/debug-your-config#check-resolved-settings) 输出中列出它：

```text theme={null}
Invalid permission rule "Bash(ls) x" was skipped: Malformed Tool(content) rule. Rules take the form Tool or Tool(content) and must end at the closing ")"; parentheses inside the content are literal
```

**要做什么：**

* 在消息列出的设置文件中，重写规则使其在其右括号处结束，例如用 `Bash(ls *)` 代替 `Bash(ls) x`
* 将内容内的括号保留原样。它们是字面量，因此诸如 `Edit(./Finance (2024)/**)` 的规则无需转义即有效

在 v2.1.260 之前，Claude Code 将具有不匹配括号的规则报告为 `Mismatched parentheses`。

<h3 id="is-not-matched-by-file-permission-checks">
  不匹配文件权限检查
</h3>

Claude Code 在您的某个[设置文件](/docs/zh-CN/settings#where-settings-live)、[托管设置](/docs/zh-CN/managed-settings)或 `--allowedTools`、`--disallowedTools` 或 `--settings` 标志值中找到了带有路径的 `Write`、`NotebookEdit`、`MultiEdit` 或 `Glob` [权限规则](/docs/zh-CN/permissions#read-and-edit)。它仅针对 `Edit` 和 `Read` 规则检查文件权限，因此从不查询命名其他文件工具之一的路径规则。它保留该规则且不改变其他任何内容；警告命名该规则、括号中的来源以及要写入的替换内容：

```text theme={null}
Permission deny rule (.claude/settings.json): Write(docs/**) is not matched by file permission checks — only Edit(path) rules are. Use Edit(docs/**) instead (Edit rules cover all file-editing tools).
```

**要做什么：**

* 将 `Write(path)`、`NotebookEdit(path)` 和旧版 `MultiEdit(path)` 规则替换为 `Edit(path)`。`Edit` 规则涵盖所有文件编辑工具。
* 除了在 `--allowedTools` 中（Claude Code 接受 `Glob` 规则而不警告），将 `Glob(path)` 规则替换为 `Read(path)`。
* 在警告括号中命名的来源处修复规则：设置文件路径，或对于 `--allowed-tools` 和 `--disallowed-tools` 则是标志本身。磁盘上不存在的 `claude-settings-<hash>.json` 路径代表内联 `--settings` 值。请修复您传递给该标志的 JSON。
* 将诸如 `Write` 或 `Glob` 的裸工具名称规则保留原样。Claude Code 在[工具级别](/docs/zh-CN/permissions#match-all-uses-of-a-tool)匹配它们，不对它们发出警告。
* 如果来源显示为 `managed policy settings`，请将警告转发给维护您的托管设置的人，因为您无法自己清除它。

在[后台会话](/docs/zh-CN/agent-view)中或使用 `--output-format json` 或 `stream-json` 时，Claude Code 将警告写入调试日志而不是 stderr，以保持机器读取的输出干净。使用 `--debug` 运行以在 `~/.claude/debug/<session-id>.txt` 处捕获它。在 v2.1.210 之前，Claude Code 接受这些规则而不警告。

<h3 id="has-a-wildcard-before-the-rest-of-the-command">
  在命令的其余部分之前有通配符
</h3>

Claude Code 在您的某个[设置文件](/docs/zh-CN/settings#where-settings-live)、[托管设置](/docs/zh-CN/managed-settings)或 `--allowedTools` 或 `--settings` 标志值中找到了一个 `Bash` 允许规则，其 `*` 出现在决定命令类型的后续单词之前，例如 `Bash(git * main)` 或 `Bash(git -C * status *)`。`*` 匹配任何文本，包括在该位置插入的选项：`Bash(git * main)` 也会批准 `git -c core.fsmonitor=<script> diff main`，其中 `-c` 会使 git 运行命令所命名的程序。[通配符模式](/docs/zh-CN/permissions#wildcard-patterns)显示匹配规则。

此警告的目的是让您缩小通配符范围超出预期的规则。Claude Code 保留该规则且不改变其匹配方式；警告命名该规则及括号中的来源：

```text theme={null}
Permission allow rule (.claude/settings.json): Bash(git -C * status *) has a wildcard before the rest of the command, so it also matches any options inserted at that position and approves them without a prompt. For git, options such as -c and --exec-path can run arbitrary commands. Replace that * with the exact value you mean, or only use * after the subcommand (for example Bash(git status *)).
```

**要做什么：**

* 将子命令前的 `*` 替换为您想要的确切值：用 `Bash(git checkout main)` 代替 `Bash(git * main)`。
* 将每个 `*` 移到子命令后：用 `Bash(git status *)` 代替 `Bash(git -C * status *)`。为您想允许的每个子命令写一条规则。
* 在警告括号中命名的来源处修复规则：设置文件路径，或 `--allowed-tools` 标志本身。磁盘上不存在的 `claude-settings-<hash>.json` 路径代表内联 `--settings` 值。请修复您传递给该标志的 JSON。
* 如果来源显示为 `managed policy settings`，请将警告转发给维护您的托管设置的人，因为您无法自己清除它。

在[后台会话](/docs/zh-CN/agent-view)中或使用 `--output-format json` 或 `stream-json` 时，Claude Code 将警告写入调试日志而不是 stderr，以保持机器读取的输出干净。使用 `--debug` 运行以在 `~/.claude/debug/<session-id>.txt` 处捕获它。在 v2.1.246 之前，Claude Code 接受这些规则而不警告。

<h3 id="denying-bash-also-turns-off-the-powershell-tool">
  拒绝 Bash 也会关闭 PowerShell 工具
</h3>

您移除了整个 Bash 工具，例如使用 `--disallowedTools Bash`，或在您的某个设置文件中使用裸 `Bash` 或 `Bash(*)` [拒绝规则](/docs/zh-CN/permissions#match-all-uses-of-a-tool)。在安装了 Git Bash 的 Windows 上，[拒绝 Bash 也会关闭 PowerShell 工具](/docs/zh-CN/tools-reference#bash-deny-rules-also-turn-off-the-powershell-tool)，因此会话启动时没有任何 shell 工具。Claude Code 在启动时打印此警告：

```text theme={null}
Denying Bash also turns off the PowerShell tool, so Claude has neither. To use PowerShell, set CLAUDE_CODE_USE_POWERSHELL_TOOL=1.
```

**要做什么：**

* 要让 Claude 使用 PowerShell，请在您的环境中或设置文件的 `env` 块中将 [`CLAUDE_CODE_USE_POWERSHELL_TOOL`](/docs/zh-CN/env-vars) 设置为 `1`，如[启用 PowerShell 工具](/docs/zh-CN/tools-reference#enable-the-powershell-tool)所示。之后 PowerShell 工具会与您的 Bash 拒绝规则并存并保持启用。
* 要阻止特定命令而不是整个工具，请在同一设置文件或标志中将裸 `Bash` 条目替换为限定范围的规则，例如 `Bash(git push *)`。Claude 会保留 Bash 工具，而 PowerShell 工具会保持关闭，直到您同时设置该变量或添加限定范围的 [`PowerShell` 权限规则](/docs/zh-CN/permissions#powershell)。

在[后台会话](/docs/zh-CN/agent-view)中或使用 `--output-format json` 或 `stream-json` 时，Claude Code 将警告写入调试日志而不是 stderr。使用 `--debug` 运行以在 `~/.claude/debug/<session-id>.txt` 处捕获它。在 v2.1.287 之前，Claude Code 以同样的方式关闭 PowerShell 工具，但不打印警告。

<h3 id="crosssessioninbound-must-be-one-of-accept-hold-refuse">
  crossSessionInbound 必须是 accept、hold 或 refuse 之一
</h3>

某个设置文件将 [`crossSessionInbound`](/docs/zh-CN/settings-reference#crosssessioninbound) 设置为 Claude Code 无法识别的值，例如拼写错误 `"reject"`。警告的第二句取决于哪个文件包含该值；在用户、项目、本地或 `--settings` 文件中，它显示为：

```text theme={null}
"crossSessionInbound" must be one of "accept", "hold", "refuse"; received "reject". This value was ignored; while it is present, cross-session messages are held for your approval instead of being delivered. Set it to one of the values above.
```

在[托管设置](/docs/zh-CN/managed-settings)中，Claude Code 将无法识别的值视为 `refuse`（最严格的值），警告说明跨会话消息将被拒绝，直到管理员修复它。有关保留行为如何与您的其他设置文件中的值结合，请参阅 [`crossSessionInbound`](/docs/zh-CN/settings-reference#crosssessioninbound)。

**要做什么：**

* 将该键设置为 `"accept"`、`"hold"` 或 `"refuse"`，或删除它
* 当警告命名托管设置时，要求管理员修复该值

在 v2.1.248 之前，Claude Code 忽略无法识别的值而不警告。

<h3 id="anthropic-foundry-resource-must-be-a-foundry-resource-name">
  ANTHROPIC\_FOUNDRY\_RESOURCE 必须是 Foundry 资源名称
</h3>

您将 [`ANTHROPIC_FOUNDRY_RESOURCE`](/docs/zh-CN/env-vars) 设置为了裸 [Microsoft Foundry](/docs/zh-CN/microsoft-foundry) 资源名称以外的内容，例如端点 URL 或其主机名。Claude Code 在发送请求前拒绝了该值。该消息出现在 Claude 回复的位置，而不是作为启动警告：

```text theme={null}
API Error: ANTHROPIC_FOUNDRY_RESOURCE must be a Foundry resource name (2-64 letters, digits and hyphens, not starting or ending with a hyphen, such as my-resource), not a URL or host name. To use a full URL, set ANTHROPIC_FOUNDRY_BASE_URL instead.
```

**要做什么：**

* 将 `ANTHROPIC_FOUNDRY_RESOURCE` 仅设置为资源名称，然后重启 Claude Code。对于端点 `https://my-resource.services.ai.azure.com/anthropic`，名称为 `my-resource`。
* 若要改为提供完整的端点 URL，请将 [`ANTHROPIC_FOUNDRY_BASE_URL`](/docs/zh-CN/env-vars) 设置为该 URL 并删除 `ANTHROPIC_FOUNDRY_RESOURCE`，然后重启 Claude Code。Claude Code 只接受这两个变量之一。

<h3 id="the-200k-limit-isnt-enforced">
  200K 限制未被强制执行
</h3>

您设置了 [`CLAUDE_CODE_DISABLE_1M_CONTEXT=1`](/docs/zh-CN/env-vars)，这通常使[自动压缩](/docs/zh-CN/model-config#default-auto-compact-thresholds)将 1M 上下文模型上的会话保持在 200K 窗口内，但没有压缩阈值将此会话限制在 200K 或以下，因此对话可以超过它。

```text theme={null}
CLAUDE_CODE_DISABLE_1M_CONTEXT is set, but the 200K limit isn't enforced for <model>, so this session can grow past it. To enforce it, set CLAUDE_CODE_AUTO_COMPACT_WINDOW=200000 (or the autoCompactWindow setting).
```

Claude Code 会为它识别为具有原生 1M 窗口的每个模型自行强制执行 200K 限制，对于它无法识别的模型 ID，它会在其假设的窗口处压缩。当其他配置使该强制执行失效时，会出现此警告：

* 模型 ID 不是 Claude Code 能识别的，例如 [LLM 网关](/docs/zh-CN/llm-gateway)别名，并且您设置了 [`CLAUDE_CODE_DISABLE_UNKNOWN_MODEL_WINDOW_ENFORCEMENT=1`](/docs/zh-CN/env-vars) 或使用 [`CLAUDE_CODE_MAX_CONTEXT_TOKENS`](/docs/zh-CN/env-vars) 将假设的窗口提高到 200K 以上。在这种情况下，消息还会提供 `or update to a Claude Code version that recognizes <model>` 作为补救措施。
* 通过 [`ANTHROPIC_BETAS`](/docs/zh-CN/env-vars) 或 [`--betas`](/docs/zh-CN/cli-reference#cli-flags) 标志请求的 `context-1m` 测试版仍然会在接受该测试版的模型上向 API 请求 1M 窗口，而没有任何机制在 200K 处压缩会话

**要做什么：**

* 设置 [`CLAUDE_CODE_AUTO_COMPACT_WINDOW=200000`](/docs/zh-CN/env-vars)，或将 [`autoCompactWindow`](/docs/zh-CN/settings-reference#autocompactwindow) 设置为 `200000`，以便自动压缩在 200K 边界处压缩
* 如果消息命名了此版本无法识别的模型 ID，请运行 `claude update`。能够将该 ID 识别为 1M 上下文模型的版本会强制执行该限制，无需进一步配置。
* 如果您希望会话改为使用模型的完整窗口，请取消设置 `CLAUDE_CODE_DISABLE_1M_CONTEXT`；该警告仅报告 200K 限制未被强制执行

在[后台会话](/docs/zh-CN/agent-view)中或使用 `--output-format json` 或 `stream-json` 时，Claude Code 将警告写入调试日志而不是 stderr。

<h3 id="unrecognized-model-id-on-a-request">
  请求上无法识别的模型 ID
</h3>

Claude Code 为您的 Claude Code 版本无法识别的模型 ID 发送了请求，并且找不到将该 ID 映射到它能识别的模型的 [`modelOverrides`](/docs/zh-CN/model-config#override-model-ids-per-version) 条目。Claude Code 仍然使用您配置的 ID 发送请求，不会退出或切换模型。

```text theme={null}
[claude-code:unrecognized_model] {"model":"my-proxy-model","query_source":"sdk"}
```

在读取 stderr 的脚本或测试工具中，请匹配 `[claude-code:unrecognized_model]` 前缀。在前缀和一个空格之后，Claude Code 写入单行 JSON 对象。Claude Code 可能在更高版本中向其添加字段，因此请忽略任何您未预期的字段。它至少写入以下两个字段：

* `model`：您配置的模型字符串
* `query_source`：使用该模型的请求路径。对于 `-p` 运行，Claude Code 报告 `sdk`；对于子代理，报告以 `agent:` 开头的值。

Claude Code 根据您的运行方式将该行写入以下两个位置之一：

* 在[非交互模式](/docs/zh-CN/headless)中使用 `-p` 时，Claude Code 在每种 `--output-format` 下都将其写入 stderr，因此您可以解析 stdout 而无需过滤掉该行
* 在交互式会话或[后台会话](/docs/zh-CN/agent-view)中，Claude Code 改为将其写入调试日志；使用 `--debug` 运行以在 `~/.claude/debug/<session-id>.txt` 处捕获它

Claude Code 每个进程为每个模型字符串写入该行一次。对于每个其他无法识别的 ID，例如[子代理](/docs/zh-CN/sub-agents#choose-a-model)或[后台功能](/docs/zh-CN/costs#background-token-usage)使用的 ID，它会写入单独的一行。

对于它能解析为可识别模型的提供商 ID，Claude Code 不写入该行，例如 Amazon Bedrock `us.anthropic.claude-...` ID、带有 `@` 版本后缀的 Google Cloud Agent Platform ID，以及包含 Claude 模型 ID 的 Microsoft Foundry 部署名称。Claude Code 检查 Amazon Bedrock [应用推理配置文件 ARN](/docs/zh-CN/amazon-bedrock#map-each-model-version-to-an-inference-profile) 背后的模型，而不是 ARN 本身。对于无法解析的 ARN（例如拼写错误的 ARN），它不写入任何行。

**要做什么：**

* 如果您是有意设置该 ID 的，例如 [LLM 网关](/docs/zh-CN/llm-gateway)别名，请在您的[设置文件](/docs/zh-CN/settings#where-settings-live)中添加一个以该 ID 为值的 [`modelOverrides`](/docs/zh-CN/model-config#override-model-ids-per-version) 条目。使用 Anthropic 模型 ID 作为键，而不是诸如 `opus` 的系列别名。对于示例行中的 `my-proxy-model`，添加此条目：

  ```json theme={null}
  {
    "modelOverrides": {
      "claude-opus-4-6": "my-proxy-model"
    }
  }
  ```

  然后 Claude Code 会将 `my-proxy-model` 视为 `claude-opus-4-6` 并停止写入该行。

* 如果该 ID 命名的模型比您的 Claude Code 版本更新，请运行 `claude update`

* 如果该 ID 是拼写错误，请在包含它的[可设置模型的位置](/docs/zh-CN/model-config#setting-your-model)或[别名变量](/docs/zh-CN/model-config#environment-variables)中修复它。如果 `query_source` 以 `agent:` 开头，请改为在您设置[子代理模型](/docs/zh-CN/sub-agents#choose-a-model)的地方修复它。

在 v2.1.233 之前，Claude Code 在为无法识别的模型 ID 发送请求时不写入任何行。

<h3 id="stale-sandbox-mask-files-left-by-a-killed-session">
  被终止的会话留下的陈旧沙箱掩码文件
</h3>

`claude doctor` 在其诊断中打印此警告，`/status` 也列出相同的行。当启用了[沙箱隔离](/docs/zh-CN/sandboxing)并打开文件系统隔离时，它会在 Linux 和 WSL2 上出现。

当沙箱中的命令运行时，沙箱通过在尚不存在的文件位置创建 0 字节只读占位符来保持对该文件的写入拒绝，并在之后删除它。在该清理运行前被终止的会话（例如通过 SIGKILL）会留下这些占位符。之后的会话在每次启动时都会再次以只读方式绑定它们，因此在占位符所在位置的设置写入（例如保存"是，不要再问"）会失败。

```text theme={null}
- Stale sandbox mask files left by a killed session: /home/you/project/.claude/settings.local.json
  Fix: Remove each with `rm <path>` while no other Claude Code session is running in that project — a 0-byte read-only file where a settings file belongs makes "Yes, and don't ask again" fail to save, and the sandbox binds it read-only again on every start
```

**要做什么：**

* 退出在该项目中运行的任何其他 Claude Code 会话，然后使用 `rm` 删除每个列出的文件。警告最多列出三个文件并对其余文件计数，因此删除后请重新运行 `claude doctor`，直到警告不再出现。另一个会话的沙箱仍在使用的占位符是该会话写入保护的有效组成部分
* 如果您使用"是，不要再问"保存的权限选择没有生效，请在删除占位符后再次保存

在 v2.1.257 之前，`claude doctor` 不会标记这些文件；较早的版本在会话被终止时会留下相同的占位符。

<h2 id="responses-seem-lower-quality-than-usual">
  回复质量似乎低于预期
</h2>

如果 Claude 的回答似乎不如你预期的那样有能力，但没有显示错误，原因通常是对话状态而不是模型本身。Claude Code 不会无声地更改模型版本。它只能在这些情况下切换到备用模型：

* 配置的 [`--fallback-model`](/docs/zh-CN/cli-reference#cli-flags) 在可用性错误后接管该轮，并在记录中显示通知
* Amazon Bedrock 或 Google Cloud 的 Agent Platform 启动检查发现你的默认模型不可用，或你的账户[在会话中途失去对它的访问权限](/docs/zh-CN/amazon-bedrock#when-a-model-is-disabled-mid-session)
* [自动模型备用](/docs/zh-CN/model-config#automatic-model-fallback) 在 Fable 5.1、Fable 5、Opus 5.5、Sonnet 5.5 和 Opus 5 上，当该类别有备用模型时，将会话移动到标记类别的备用模型，并在记录中显示通知

下面的模型选择检查捕获第二和第三种情况；第一种情况显示为记录通知而不是 `/model` 更改。[模型配置](/docs/zh-CN/model-config) 解释了每个备用何时适用。

首先检查这些：

* **模型选择**：运行 `/model` 以确认你在预期的模型上。之前的 `/model` 选择或 `ANTHROPIC_MODEL` 环境变量可能使你在比预期更小的模型上。
* **努力级别**：运行 `/effort` 以检查当前推理级别，并为困难的调试或设计工作提高它。默认值因模型而异，所以在假设你低于最大值之前请检查。有关每个模型的默认值和 `ultrathink` 快捷方式，请参阅[调整努力级别](/docs/zh-CN/model-config#adjust-effort-level)。
* **上下文压力**：运行 `/context` 以查看窗口有多满。如果接近容量，在自然断点处运行 `/compact` 或运行 `/clear` 以重新开始。有关 auto-compact 如何影响早期轮次的信息，请参阅[探索上下文窗口](/docs/zh-CN/context-window)。
* **过时的指令**：大型或过时的 `CLAUDE.md` 文件和 MCP 工具定义会消耗上下文并可能引导回复。`/doctor` 检查会标记超大内存文件和未使用的扩展，`/context` 显示 MCP 工具令牌使用情况。在 v2.1.205 之前，`/doctor` 打开一个诊断屏幕，标记超大内存文件和子代理定义。

当回复出错时，回退通常比用更正回复效果更好。按 Esc 两次或运行 `/rewind` 以回到坏轮之前，然后用更多细节重新表述提示。在线程中更正会将错误的尝试保留在上下文中，这可能会将后来的答案锚定到它。请参阅[检查点](/docs/zh-CN/checkpointing)。

如果在检查上述内容后质量仍然似乎有问题，运行 `/feedback` 并描述你期望的内容与你得到的内容。以这种方式提交的反馈包括对话记录，这是 Anthropic 诊断真实回归的最快方式。如果 `/feedback` 在你的环境中不可用，请参阅[报告错误](#report-an-error)。

如果 Claude 警告可疑的提示注入，或因可疑注入而拒绝请求，并且警告命名的文本是 Claude Code 自动添加到对话中的上下文而不是文件或网络内容，运行 `claude update` 并重试。如果更新后警告重复出现，[报告它](#report-an-error)而不是将标记的内容粘贴回提示中。在 v2.1.201 之前，Sonnet 5 以相同的方式拒绝了一些请求。

<h2 id="report-an-error">
  报告错误
</h2>

对于此页面未涵盖的组件错误，请参阅相关指南：

* MCP 服务器连接或身份验证失败：[MCP](/docs/zh-CN/mcp)
* Hook 脚本失败或阻止了工具：[调试 hooks](/docs/zh-CN/hooks#debug-hooks)
* 安装期间权限被拒绝或文件系统错误：[排查安装和登录问题](/docs/zh-CN/troubleshoot-install)

如果此处未列出错误或建议的修复方法无法帮助：

* 在 Claude Code 中运行 `/feedback` 将记录和描述发送给 Anthropic。该命令还提供打开预填充的 GitHub issue 的选项。发送到 Anthropic 需要[身份验证](/docs/zh-CN/authentication)。在 Amazon Bedrock、Google Cloud 的 Agent Platform、Microsoft Foundry 和其他第三方提供商上，或者当未配置 Anthropic 凭证时，`/feedback` 会保存一个本地存档，您可以将其发送给您的 Anthropic 账户代表。
* 从您的 shell 中运行 `claude doctor` 以获取安装的只读诊断，或在 Claude Code 中运行 `/doctor` 检查以查找和修复设置问题
* 检查 [status.claude.com](https://status.claude.com) 以了解活跃的事件
* 在 GitHub 上搜索[现有问题](https://github.com/anthropics/claude-code/issues)
