> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 配置云环境

> 为 Claude Code 云端会话配置云环境：网络访问级别、环境变量、设置脚本和环境缓存。

<Note>
  云环境适用于[云端会话](/docs/zh-CN/claude-code-on-the-web)，这些会话在 Pro、Max 和 Team 计划上可用，以及具有[高级席位或 Chat + Claude Code 席位](https://support.claude.com/en/articles/11845131-use-claude-code-with-your-team-or-enterprise-plan)的 Enterprise 用户。
</Note>

每个[云端会话](/docs/zh-CN/claude-code-on-the-web)都在云环境中运行。您可以配置环境以允许或拒绝[网络访问](#access-levels)、为会话[设置环境变量](#set-environment-variables)、在 Pro 和 Max 计划上存储会话使用但无法看到的[网络密钥](#add-network-secrets)，以及在 Claude 开始工作前运行[设置脚本](#setup-scripts)。

相同的环境适用于您启动云端会话的任何地方：[Desktop 应用](/docs/zh-CN/desktop)、[Claude 移动应用](/docs/zh-CN/mobile)、浏览器中的 [claude.ai/code](https://claude.ai/code)、终端中搭配 [`claude --cloud`](/docs/zh-CN/claude-code-on-the-web#from-terminal-to-cloud)、[Routine](/docs/zh-CN/routines) 和 [Claude Tag](https://claude.com/docs/claude-tag/overview)。这些使用入口中的每一个也可以路由到[自托管环境](/docs/zh-CN/self-hosted-environments)。[可用性和限制](/docs/zh-CN/self-hosted-environments#availability-and-limitations)涵盖了当 Claude Tag 会话在其中运行时 Claude 还不能使用的内容。

<Info>
  [Remote Control](/docs/zh-CN/remote-control) 会话将网页和移动界面连接到您自己机器上的会话，该会话使用您机器的网络和文件，而不是云环境。Claude Tag 频道会话仅使用组织级别的环境，即[共享环境](#organization-shared-environments)或[自托管环境](/docs/zh-CN/self-hosted-environments)。
</Info>

<h2 id="the-default-environment">
  Default 环境
</h2>

如果您还没有环境，引导设置会为您设置 **Default** 环境。具体方式取决于您在哪里进行引导：

* **CLI 流程（例如 `/web-setup`）**：为您创建 **Default**
* **Pro 和 Max 上的网页引导**：为您创建 **Default**
* **Team 和 Enterprise 上的网页引导**：显示 **Create your first cloud environment** 表单，除非所有者已启用[快速设置](/docs/zh-CN/claude-code-on-the-web#quick-setup-for-team-and-enterprise)；保持表单的默认值并点击 **Create & finish** 以获得相同的 **Default** 环境

**Default** 本身不带有任何配置：

* [**Trusted** 网络访问](#access-levels)：会话可以访问包注册表和其他[允许列表中的域](#default-allowed-domains)，但无法通过会话的网络访问其他任何内容。
* 无其他配置：**Default** 不定义任何环境变量或设置脚本，因此会话只以[预安装的工具](#installed-tools)开始。

只有 **Default** 可用时，每个会话都在其中运行。当您有多个环境时，会话会按界面选择一个：

* 在网页、Desktop 应用和移动应用上，会话使用[选择器](#configure-your-environment)中显示的环境。当您尚未选择时，所有者设置的[组织默认值](#organization-shared-environments)会填入选择。线程在[项目](/docs/zh-CN/claude-projects#project-settings-reference)中使用项目设置中设置的环境。
* 从 CLI，Claude Code 使用您的 [`/remote-env` 选择](#select-an-environment-from-the-cli)，或在您的列表中有一个 Anthropic 托管环境时回退到该环境，否则回退到您列表中第一个不是桥接环境的环境，即 [Remote Control](/docs/zh-CN/remote-control) 注册的条目，用于代表您自己的机器而不是云环境。对于[自托管环境](/docs/zh-CN/self-hosted-environments)，在[分派会话](/docs/zh-CN/self-hosted-environments-testing#run-the-test-loop)时使用其 `ccpool_` ID 传递 `--environment <environment-id>` 会覆盖该调用的 `/remote-env` 选择和回退。Claude Code 拒绝传递给该标志的 Anthropic 托管 `env_` ID，因此请使用 `/remote-env` 来定位这些。该标志需要 Claude Code v2.1.224 或更高版本。

当默认环境不够用时，请配置环境：当 Claude 需要访问[默认允许列表](#default-allowed-domains)之外的域、需要为其会话设置环境变量，或需要在开始工作前安装依赖项时。

<h2 id="configure-your-environment">
  配置您的环境
</h2>

在环境选择器中创建、编辑和归档环境。完成[网页快速入门](/docs/zh-CN/web-quickstart)后，您可以在 [claude.ai/code](https://claude.ai/code) 访问该选择器，也可以从[桌面应用](/docs/zh-CN/desktop#cloud-sessions)的输入框中访问。您创建的环境是您账户的个人环境；由所有者创建的[共享环境](#organization-shared-environments)会出现在同一个选择器中。查看[已安装的工具](#installed-tools)，了解无需任何配置即可使用的工具。

<Steps>
  <Step title="打开环境选择器">
    在 [claude.ai/code](https://claude.ai/code) 上，选择显示当前环境名称的云图标，它位于消息框上方的行中。选择器没有设置页面或直接 URL。

    <Frame>
      <img src="https://mintcdn.com/claude-code/ZFId6l95856c5LSw/images/cloud-environment-selector.png?fit=max&auto=format&n=ZFId6l95856c5LSw&q=85&s=cc2813a5664519eaf5a89d793ce5af26" alt="环境选择器在 claude.ai/code 的消息框上方打开。显示环境名称 Default 的云按钮位于消息框上方的行中。打开的菜单列出了一个带有 Download 和 Desktop only 标签的 Local 行、一个 Cloud 部分（其中 Default 环境被选中并显示复选标记，悬停时显示设置齿轮图标）、一个 Add cloud environment 选项，以及一个带有设置说明的 Remote Control 部分。" width="1672" height="682" data-path="images/cloud-environment-selector.png" />
    </Frame>
  </Step>

  <Step title="添加或编辑环境">
    选择 **Cloud** 来列出您的环境。然后选择 **Add cloud environment**，或悬停在现有环境上并选择右侧出现的设置图标。

    对话框包括名称、网络访问级别、环境变量和设置脚本。当您在 Pro 或 Max 计划上编辑现有的云环境时，对话框还包括[网络机密](#add-network-secrets)。

    <Frame>
      <img src="https://mintcdn.com/claude-code/ZFId6l95856c5LSw/images/cloud-environment-dialog.png?fit=max&auto=format&n=ZFId6l95856c5LSw&q=85&s=30d4478b31d1f879f7ee287ddab32505" alt="New cloud environment 对话框。一个占位符为 Default 的 Name 字段；一个设置为 Trusted 的 Network access 选择器，带有网络策略和访问级别的链接；一个 Environment variables 框，显示 .env 格式的占位符文本，并注明值对使用该环境的任何人都可见；一个 Setup script 框，描述为在新会话启动时、Claude Code 启动之前运行的 Bash 脚本；以及 Cancel 和 Create environment 按钮。" width="874" height="1372" data-path="images/cloud-environment-dialog.png" />
    </Frame>
  </Step>
</Steps>

<h3 id="set-environment-variables">
  设置环境变量
</h3>

环境变量使用 `.env` 格式，每行一个 `KEY=value` 对。普通值不需要引号，如果您用匹配的一对引号引用一个值，引号不会成为该值的一部分。跨越多行或包含 `#` 的值需要加引号：在未加引号的值中，`#` 会开始注释，该行的其余部分会被丢弃。

以下示例定义了三个变量。

```text theme={null}
NODE_ENV=development
LOG_LEVEL=debug
DATABASE_URL=postgres://localhost:5432/myapp
```

会话会将环境的值读入普通环境变量中，Claude 运行的任何命令都可以读取这些变量，`OTEL_*` 变量除外。Claude Code 使用这些变量进行自己的[遥测导出](/docs/zh-CN/monitoring-usage#telemetry-from-cloud-sessions-and-claude-tag)，不会将它们传递给它运行的命令。

在 Anthropic 托管的环境中，会话在创建时读取环境的值，之后每次 Claude Code 在会话的 VM 中启动时也会再次读取，这发生在两种情况下：

* **VM 在空闲后被恢复**：在几分钟没有活动后，会话的 VM 会暂停，其文件会被保存。您的下一条消息会恢复同一个 VM 并再次启动 Claude Code。
* **VM 被回收并被重建**：如果暂停的 VM 已经被[回收](/docs/zh-CN/claude-code-on-the-web#environment-expired)，重新打开会话会配置一个新的 VM。

编辑、添加或删除变量后，Anthropic 托管环境中的现有会话会保持它最后读取的值，直到其 VM 下次被恢复或重建，此后才使用您的更改。会话空闲后其 VM 会自动暂停，您无法手动暂停它。要立即使用新值，请要求 Claude 在它运行的命令上设置该值，例如 `LOG_LEVEL=trace npm test`，或启动一个新会话。

云端会话在启动时也会自行设置一些变量。对于 [`CLAUDE_AUTOCOMPACT_PCT_OVERRIDE`](/docs/zh-CN/claude-code-on-the-web#manage-context)，会话设置的值会覆盖您在这里添加的值，因此在这里添加该键没有效果。

使用该环境的任何人都可以读取这些值。在 Pro 和 Max 计划上，对于 Agent 代理可以附加到请求中的密钥，请改用[网络机密](#add-network-secrets)。[永远不会获得机密的请求](#requests-that-never-get-the-credential)在该处列出。

<span id="add-api-credentials" />

<h3 id="add-network-secrets">
  添加网络机密
</h3>

网络机密是您存储在云环境中的 API 密钥或令牌，使 Claude 可以从该环境中的任何会话调用该 API，而无需看到密钥。每个请求离开会话的 VM 后，Anthropic 的 Agent 代理会将密钥添加到发往您所列主机的请求中，因此密钥本身始终位于 VM 之外。

网络机密适用于 Pro 和 Max 计划。它们目前尚不适用于 Team 或 Enterprise 计划，因此在这些计划上，环境对话框中不会出现 **Network secrets** 部分。

<h4 id="requirements">
  要求
</h4>

以下要求决定您是否可以添加机密，以及添加后 Agent 代理是否可以使用它：

* **Role**：您的 claude.ai 组织中的组织管理员角色
  * 在 Team 和 Enterprise 上，所有者持有该角色，管理员（Admin）不持有
  * 在 Pro 和 Max 上，您在自己的组织中持有该角色
* **Environment type**：一个已存在的 Anthropic 托管云环境。[自托管环境](/docs/zh-CN/self-hosted-environments)没有网络机密
* **API reachability**：API 接受来自互联网的连接，因为请求从 Anthropic 的网络发出
* **Encryption keys**：如果您的组织使用客户管理的加密密钥，则无法保存网络机密

<h4 id="add-a-credential">
  添加机密
</h4>

机密需要逐个添加，添加后无法编辑。要更改机密的主机或值，请将其删除后重新添加。

<Steps>
  <Step title="打开环境的网络机密">
    在 [claude.ai/code](https://claude.ai/code) [打开环境进行编辑](#configure-your-environment)。在 **Edit environment** 对话框中，找到 **Network secrets** 部分。您会看到环境中已有的机密，每个机密都附有其适用的主机。
  </Step>

  <Step title="添加机密">
    选择 **Add secret** 并填写表单。对于在请求头中传输的 API 密钥，保留默认的 **Credential type**，即 **Bearer**，并填写以下字段：

    * **Name**：机密的标签，例如 `Internal billing API`
    * **Allowed websites**：API 的主机，例如 `api.example.com`。前导 `*.` 匹配所有子域
    * **Custom headers**：用于携带密钥的请求头占一行。该行默认以 `Authorization` 作为请求头的 **Name**，以 `Bearer` 作为其 **Prefix**；将密钥本身粘贴为 **Value**。对于接受裸值的请求头（如 `X-Api-Key`），请更改名称并清除前缀

    对于以其他方式进行身份验证的 API，请选择不同的 **Credential type**。该列表与 [Claude Tag](https://claude.com/docs/claude-tag/overview)（适用于 Team 和 Enterprise 计划的 Slack 集成）为 [connections](https://claude.com/docs/claude-tag/admins/add-connections) 提供的列表相同。
  </Step>

  <Step title="保存机密">
    选择 **Connect**。机密会连同其主机一起出现在列表中，无需点击对话框的 **Save changes** 按钮即已保存。保存后您无法再次查看该值。
  </Step>
</Steps>

要确认机密是否有效，请在该环境中启动会话并让 Claude 调用 API，例如使用 `curl`。API 的响应就如同请求中带有密钥一样，而密钥不会出现在会话的环境变量或任何文件中。如果列表将某个机密标记为 **Not sent**，其下方的说明会解释原因和处理方法。两个主机重叠但不完全匹配的机密不会显示标记，而 Agent 代理只会发送其中一个。

<h4 id="which-requests-get-the-credential">
  哪些请求会获得机密
</h4>

当请求的主机与您在某个机密上列出的主机匹配时，Agent 代理会将该机密附加到请求中。即使环境的[网络访问级别](#access-levels)原本不允许访问这些主机，会话也可以访问它们，但[永远不会获得机密的主机](#requests-that-never-get-the-credential)除外。机密适用于在该环境中运行的每个会话，无论由谁启动，直到您将其删除。

<h4 id="requests-that-never-get-the-credential">
  永远不会获得机密的请求
</h4>

Agent 代理永远不会将您添加的机密附加到以下请求：

* **GitHub**：[GitHub 代理](#github-proxy)会代为对发往 GitHub 的请求进行身份验证，因此您无需为其设置网络机密
* **Anthropic API 和公共包注册表**：`api.anthropic.com`、`registry.npmjs.org`、`jsr.io`、`npm.jsr.io`、`pypi.org`、`files.pythonhosted.org`、`index.crates.io` 和 `proxy.golang.org`
* **设置脚本请求**：Claude Code 在启动时才连接到 Agent 代理，此时[设置脚本](#setup-scripts)已经运行完毕
* **Claude Code 的遥测导出**：Claude Code 自行发送其[遥测导出](/docs/zh-CN/monitoring-usage#telemetry-from-cloud-sessions-and-claude-tag)，而不是通过它运行的命令发送，该请求不会经过 Agent 代理

<h3 id="select-an-environment-from-the-cli">
  从 CLI 选择环境
</h3>

在终端中运行 `/remote-env`，为您从 CLI 创建的云端会话（例如 [`claude --cloud`](/docs/zh-CN/claude-code-on-the-web#from-terminal-to-cloud)）选择默认环境。该命令会打开现有环境的选择器，并将您的选择保存到[用户设置](/docs/zh-CN/settings#where-settings-live)中的 `remote.defaultEnvironmentId` 键，因此它适用于您机器上的每个项目，直到您更改它为止，除非在更高优先级的[设置层级](/docs/zh-CN/settings#settings-precedence)（例如仓库的项目设置）中设置了相同的键。

[自托管环境](/docs/zh-CN/self-hosted-environments) ID 的形式为 `ccpool_...`，遵循更严格的来源规则。查看 [`remote.defaultEnvironmentId`](/docs/zh-CN/settings-reference#remote-defaultenvironmentid)，了解 Claude Code 会从哪些设置层级采用该值。

`/remote-env` 仅设置默认值：它不会启动会话，也不能添加或编辑环境。请从[环境选择器](#configure-your-environment)管理环境。

<h3 id="archive-an-environment">
  归档环境
</h3>

要归档您自己的某个环境，请打开它进行编辑并选择 **Archive**。所有者从管理设置中的 **Cloud environments** 页面归档[共享环境](#organization-shared-environments)。您无法删除环境，只能归档它。

归档影响新会话，不影响运行中的会话：

* 已经在环境中运行的会话会继续工作。
* 环境会从选择器和 `/remote-env` 中消失，因此您无法为新会话选择它。
* 环境中的网络机密在其正在运行的会话中仍保持附加状态。请在归档前删除不再需要的机密。
* 在任何使用入口上都无法在已归档的环境中启动新会话。如果该环境是您保存的 [CLI 默认值](#select-an-environment-from-the-cli)，当您的列表中有 Anthropic 托管的环境时，Claude Code 会在该环境中启动 CLI 云端会话，否则会在列表中第一个不是 [Remote Control bridge 环境](#the-default-environment)的环境中启动。任何显式配置了该环境的内容，例如 [Routine](/docs/zh-CN/routines#environments-and-network-access)，都无法在其中启动新会话。请将其指向另一个环境。

<h3 id="organization-shared-environments">
  组织共享环境
</h3>

在 Team 和 Enterprise 计划上，所有者可以创建与组织每个成员共享的云环境。同一角色管理 **Cloud environments** 管理页面上的其他所有内容，包括[自托管环境](/docs/zh-CN/self-hosted-environments)；管理员（Admin）角色无法打开该页面。可以打开该页面的完整角色列表与[管理服务器托管设置](/docs/zh-CN/server-managed-settings#access-control)的角色列表相同。

共享环境出现在每个成员的[环境选择器](#configure-your-environment)中的 **Organization** 标题下，位于成员自己在 **Personal** 下的环境之后，因此团队可以统一使用一套配置，而无需每个成员各自重新创建。在那里选择共享环境的设置图标，会为每个成员（包括所有者）打开其配置的只读摘要。

所有者可以通过以下两种方式之一使环境对组织可用：

* **创建共享环境**：使用[管理设置](https://claude.ai/admin-settings)中的 **Cloud environments** 页面，所有者也在该页面编辑和归档共享环境。每个共享环境都有一个名称、一个[网络访问级别](#access-levels)、`.env` 格式的[环境变量](#set-environment-variables)和一个[设置脚本](#setup-scripts)。
* **共享个人环境**：在环境选择器中打开您自己的某个环境进行编辑，然后从 **Who can use it** 行共享它。环境会保留其 ID，因此已经使用它的会话和 Routine 不受影响，每个成员随后都可以看到它并在其中启动会话。

所有者在 [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) 单独选择组织的[默认环境](#the-default-environment)。

每个成员在共享环境中的会话都会读取其变量，因此请勿在其中包含机密信息。[网络机密](#add-network-secrets)可以为会话提供其无法读取的密钥，但目前尚不适用于 Team 或 Enterprise 计划。

<h3 id="set-the-environment-a-claude-tag-channel-uses">
  设置 Claude Tag 频道使用的环境
</h3>

在 [Claude Tag](https://claude.com/docs/claude-tag/overview) 频道中，Claude 以您组织的共享身份工作，而不是以任何成员的身份工作，因此频道会话仅使用组织级别的环境，即共享环境或[自托管环境](/docs/zh-CN/self-hosted-environments)。要为频道提供未[预安装](#installed-tools)的工具链（例如 .NET），所有者可以从 **Cloud environments** 管理页面创建一个[共享环境](#organization-shared-environments)，并使用[设置脚本](#setup-scripts)安装该工具链。通过以下两种方式之一将频道指向某个环境：

* 在 [claude.ai/admin-settings/claude-code](https://claude.ai/admin-settings/claude-code) 将共享环境或自托管环境设置为组织的[默认环境](#the-default-environment)。
* 在 Claude Tag 管理设置中[将某个环境固定到频道](https://claude.com/docs/claude-tag/admins/troubleshooting#channel-sessions-use-the-wrong-environment-or-can%E2%80%99t-find-one)。

<h2 id="network-access">
  网络访问
</h2>

每个环境都设置一个网络访问级别，控制其会话可以进行的出站连接。默认级别 **Trusted** 允许包注册表和其他[允许列表中的域](#default-allowed-domains)；**Custom** 采用您自己的域列表。

要更改环境的网络访问，[打开它进行编辑](#configure-your-environment)并在对话框中使用 **Network access** 选择器。[共享环境](#organization-shared-environments)在那里以只读方式打开，因此 Owner 改为从[管理设置](https://claude.ai/admin-settings)中的 **Cloud environments** 页面更改其网络访问。打开选择器的云图标出现在[Default 环境](#the-default-environment)下列出的应用使用入口上，以及 [Routine 编辑器](/docs/zh-CN/routines#environments-and-network-access)中；个人环境在您的 claude.ai 账户设置中没有单独的页面。

当您更改 Anthropic 托管环境的网络访问时，其现有会话在约一分钟内遵循新设置，用于通过会话的[网络允许列表](#access-levels)的请求。您无需启动新会话。

<Note>
  您在会话或 Routine 上启用的 MCP 连接器无需将其主机添加到 **Allowed domains**，因为连接器流量通过 Anthropic 的服务器而不是会话的网络传输。这依赖于[安全性和隔离](/docs/zh-CN/claude-code-on-the-web#security-and-isolation)下提到的同一条通往 Anthropic 的通道。关闭任何您不需要的连接器，以限制 Claude 可以访问的工具。
</Note>

<h3 id="access-levels">
  访问级别
</h3>

**Network access** 字段在[环境对话框](#configure-your-environment)中采用以下四个级别之一：

| 级别 | 出站连接 |
| :- | :- |
| **None** | 通过会话的网络没有出站网络访问 |
| **Trusted** | 仅限[允许列表中的域](#default-allowed-domains)：包注册表、GitHub、云 SDK |
| **Full** | 任何域 |
| **Custom** | 您自己的允许列表，可选择包含默认值 |

无论您选择哪个级别，会话仍然可以访问这些，因为每一个都采用不经过会话的网络允许列表的路径：

* GitHub，通过其[单独的代理](#github-proxy)
* 您启用的 [MCP 连接器](#network-access)，其流量通过 Anthropic 的服务器传输
* 您在环境的[网络密钥](#add-network-secrets)上列出的主机，除了[永远不会获得该密钥的主机](#requests-that-never-get-the-credential)
* Anthropic API，用于 Claude Code 自己的请求，即使在 **None** 下也是如此，如[安全性和隔离](/docs/zh-CN/claude-code-on-the-web#security-and-isolation)下所述

<h3 id="allow-specific-domains">
  允许特定域
</h3>

要允许不在 Trusted 列表中的域，请在环境的网络访问设置中选择 **Custom**，然后在 **Allowed domains** 字段中每行列出一个域。此示例允许内部项目可能需要的三个主机。

```text theme={null}
api.example.com
*.internal.example.com
registry.example.com
```

此环境中的会话现在可以访问 `api.example.com`、`internal.example.com` 的任何子域和 `registry.example.com`，但无法通过会话的网络访问其他域。[GitHub 流量](#github-proxy)、[MCP 连接器流量](#network-access)和对环境[网络密钥](#add-network-secrets)的主机的请求（除了[永远不会获得该密钥的主机](#requests-that-never-get-the-credential)）不经过此允许列表。前导 `*.` 匹配每个子域。要同时保留 [Trusted 域](#default-allowed-domains)，请勾选 **Also include default list of common package managers**；不勾选则只允许您列出的内容。

如果您的组织使用 [Artifact](/docs/zh-CN/artifacts#availability)，会话读取 Artifact 时不需要在列表中包含 `*.frame.claudeusercontent.com`。当列表中没有该主机时，Claude Code 通过会话与 Anthropic 的连接读取 Artifact 内容。在两种情况下保留允许列表中的主机：

* **此环境中的会话打开另一个组织的公开 Artifact**：Claude Code 直接从主机获取这些 Artifact，因此将其添加到此列表。
* **您正在配置本地 CLI 或自托管运行器**：在该允许列表中保留主机。请参阅[网络访问要求](/docs/zh-CN/network-config#network-access-requirements)和自托管[网络要求](/docs/zh-CN/self-hosted-environments-deploy#network-requirements)。

每个环境都有自己的允许域列表；没有组织级别的允许列表可供管理员推送到每个成员的环境。[服务器管理的设置](/docs/zh-CN/server-managed-settings)也不会将域添加到环境的网络允许列表。要为团队提供一个标准列表，Owner 可以创建一个具有 **Custom** 网络访问和该列表的[组织共享环境](#organization-shared-environments)。

<h3 id="github-proxy">
  GitHub 代理
</h3>

在 Anthropic 托管的环境中，所有 GitHub 操作都经过专用代理，使您的真实 GitHub 凭据保留在会话的 VM 之外，独立于环境的[访问级别](#access-levels)。自托管环境中的会话使用您的部署提供的凭据进行 git 操作身份验证；[配置 git](/docs/zh-CN/self-hosted-environments-deploy#configure-git)涵盖了选项，包括按会话生成的凭据和选择加入此同一代理。代理提供：

* **Git 凭据**：VM 内的 git 客户端使用范围受限的凭据，代理验证并将其交换为您的实际 GitHub 令牌。
* **API 请求**：来自内置 GitHub 工具的请求，以及来自 [`proxy-injected` 占位符](#work-with-github-issues-and-pull-requests)下的 `gh` 的请求，会在替换为您的真实凭据后发出。
* **推送限制**：代理会拒绝分支删除，以及推送分支以外的任何内容（例如标签）。它不限制推送可以更新哪些分支。如需限制，请在 GitHub 上使用分支保护规则或规则集。
* **仓库范围**：代理为附加到会话的仓库处理 GitHub API 请求。针对其他仓库的 API 请求会收到 403，其消息以 `GitHub access to` 开头并包含 `is not enabled for this session`。
* **GraphQL 限制**：代理会拒绝发往 GitHub GraphQL 端点的请求，返回 403，其消息以 `GitHub GraphQL is not available from Claude Code sessions` 开头，并指明 REST 回退方式 `gh api repos/{owner}/{repo}/...`。使用 GraphQL 的 `gh` 子命令（例如 `gh pr` 和 `gh issue`）也会收到相同的 403。无论您提供的凭据如何，限制都适用于通过代理的每个请求，因此您设置的 `GH_TOKEN` 会收到相同的 403。Claude 无法通过代理访问仅存在于 GraphQL 中的 GitHub API，例如 Projects v2。

来自公开仓库的已提交文件通过 `raw.githubusercontent.com` 到达，改由[安全代理](#security-proxy)处理。该域在默认 [Trusted 列表](#default-allowed-domains)中，因此除非环境的[访问级别](#access-levels)排除它，否则这些文件保持可访问。

<h3 id="security-proxy">
  安全代理
</h3>

Anthropic 托管环境中的云端会话在 HTTP/HTTPS 网络代理后面运行，用于安全和滥用防范目的；在[自托管环境](/docs/zh-CN/self-hosted-environments-deploy#default-deny-egress)中，出站流量通过您自己的网络边界离开。来自 Anthropic 托管会话的所有出站互联网流量都经过此代理，它提供：

* 防范恶意请求
* 速率限制和滥用防范

<h2 id="what’s-available-in-cloud-sessions">
  云端会话中可用的内容
</h2>

在 Anthropic 托管的环境中，每个会话都会获得一台运行 Ubuntu 24.04 的全新虚拟机 (VM)（x86\_64 架构），无论您自己的操作系统和 CPU 架构是什么，您的仓库已克隆，常见的工具链已预安装。当依赖提供预编译的二进制文件（例如具有本机扩展的 Ruby gem 或预构建的 Python wheel）时，请使用其 x86\_64 Linux 构建版本以匹配 VM。本节涵盖 Anthropic 托管的默认值、内置 GitHub 工具、如何[运行测试和服务](#run-tests-start-services-and-add-packages)、每台 VM 获得的[资源限制](#resource-limits)，以及长时间运行的工作的[时间限制](#time-limits)。

<Note>
  您的组织路由到[自托管环境](/docs/zh-CN/self-hosted-environments)的会话在您自己的运行器上运行，使用您的运行器镜像提供的工具。
</Note>

<h3 id="what-carries-over-from-your-setup">
  您的设置中会保留的内容
</h3>

云端会话从您仓库的全新克隆开始。您提交到仓库的任何内容都可用。您只在自己机器上安装或配置的任何内容在会话中都不可用。您组织的策略通过[服务器托管设置](/docs/zh-CN/server-managed-settings)单独到达。

| | 在云端会话中可用 | 原因 |
| :- | :- | :- |
| 您的仓库的 `CLAUDE.md` | 是 | 克隆的一部分 |
| 您的仓库的 `.claude/settings.json` hook 和权限规则 | 是，在具有一个仓库的会话中 | 克隆的一部分。对于具有多个仓库的会话，请参阅[它读取哪些设置](/docs/zh-CN/settings#settings-in-cloud-sessions) |
| 您的仓库的 `.mcp.json` MCP 服务器 | 是，在具有一个仓库的会话中 | 克隆的一部分，从会话的工作目录中找到。对于自托管环境，请参阅[哪个仓库的设置适用](/docs/zh-CN/self-hosted-environments-configuration#repository-settings-in-sessions-with-several-repositories) |
| 您的仓库的 `.claude/rules/` | 是 | 克隆的一部分 |
| 您的仓库的 `.claude/skills/`、`.claude/agents/`、`.claude/commands/` | 是 | 克隆的一部分 |
| 在您的仓库的 `.claude/settings.json` 中声明的插件和市场 | 否 | 云端会话不会安装仓库在 [`enabledPlugins`](/docs/zh-CN/settings-reference#enabledplugins) 下启用的插件，包括来自它在 [`extraKnownMarketplaces`](/docs/zh-CN/settings-reference#extraknownmarketplaces) 下列出的市场的插件 |
| 您组织的[服务器托管设置](/docs/zh-CN/server-managed-settings) | 是，除了在 [Claude Tag](https://claude.com/docs/claude-tag/overview) 会话中 | 在会话启动时从 Anthropic 的服务器获取。请参阅[使用入口覆盖范围](/docs/zh-CN/model-config#surface-coverage)了解 `availableModels` 在云端会话中如何强制执行。通过 MDM 或托管设置文件部署到您设备的设置不适用，因为会话在 Anthropic 管理的 VM 上运行；在[自托管环境](/docs/zh-CN/self-hosted-environments)中，会话也会读取运行器镜像中的托管设置文件，根据 [Claude Code 如何组合托管来源](/docs/zh-CN/managed-settings#how-claude-code-combines-managed-sources) |
| 您的用户 `~/.claude/CLAUDE.md` | 否 | 位于您的机器上，不在仓库中。请参阅[添加个人偏好而无需提交到仓库](#add-personal-preferences-without-committing-to-the-repo) |
| 您的用户 `~/.claude/skills/`、`~/.claude/agents/`、`~/.claude/commands/` | 否 | 位于您的机器上，不在仓库中。请改为将它们提交到仓库的 `.claude/` 目录。云端会话会自动加载您在 claude.ai 上启用的 skill |
| 仅在您的用户设置中启用的插件 | 否 | 用户作用域的 `enabledPlugins` 位于您机器上的 `~/.claude/settings.json` |
| 您使用 `claude mcp add` 在默认本地作用域或用户作用域添加的 MCP 服务器 | 否 | 这些写入您机器上的 `~/.claude.json`，而不是仓库。请使用 `claude mcp add --scope project` 添加服务器，它会写入仓库的 [`.mcp.json`](/docs/zh-CN/mcp#project-scope)，并提交该文件。具有一个仓库的会话会加载它 |
| 您的仓库的 `.claude/settings.json` `env` 块中的传输变量，例如 `NODE_EXTRA_CA_CERTS` 和 [mTLS 客户端证书变量](/docs/zh-CN/network-config#mtls-authentication) | 否 | 托管环境管理会话的 API 连接，因此 Claude Code 忽略这些键，并在会话的调试日志中记录每个被忽略的键 |
| Claude 调用的服务的 API 密钥和令牌 | 在 Pro 和 Max 计划中，作为[网络密钥](#add-network-secrets) | 您在环境中添加一次密钥，Agent 代理会将其附加到发往您列出的主机的请求。Agent 代理[无法附加](#requests-that-never-get-the-credential)的密钥，或 Team 或 Enterprise 计划中的任何密钥，保留在环境变量中 |
| 交互式身份验证，例如 AWS SSO | 否 | 不支持。SSO 需要基于浏览器的登录，无法在云端会话中执行 |

要在云端会话中提供您自己的配置，请将其提交到仓库。

任何使用环境的人都可以读取其环境变量和设置脚本。对话框在**环境变量**下的注释说明了这一点，并警告不要在那里放置密钥。在 Pro 和 Max 计划中，请改为将 Agent 代理可以附加的密钥存储为[网络密钥](#add-network-secrets)。

<h4 id="add-personal-preferences-without-committing-to-the-repo">
  添加个人偏好而无需提交到仓库
</h4>

在 Anthropic 托管的环境中，对于您不希望放入共享仓库的偏好，请添加一个写入 `~/.claude/CLAUDE.md` 的[设置脚本](#setup-scripts)。Claude Code 会在会话中将该文件作为[用户指令](/docs/zh-CN/memory#choose-where-to-put-claude-md-files)加载。以下示例设置了一项提交信息偏好：

```bash theme={null}
#!/bin/bash
mkdir -p ~/.claude
cat > ~/.claude/CLAUDE.md <<'EOF'
Use conventional commit messages.
EOF
```

请将该脚本放在您自己的某个环境上，而不是[共享环境](#organization-shared-environments)上。

在下一个云端会话中运行 `/context`，并确认 `/root/.claude/CLAUDE.md` 出现在 **Memory files** 下。

<h3 id="installed-tools">
  已安装的工具
</h3>

云端会话预安装了常见的语言运行时、构建工具和数据库。下表按类别总结了包含的内容。

| 类别 | 包含 |
| :- | :- |
| **Python** | Python 3.x，搭配 pip、poetry、uv、black、mypy、pytest、ruff |
| **Node.js** | 20、21 和 22，搭配 npm、yarn、pnpm、bun¹、eslint、prettier、chromedriver |
| **Ruby** | 3.1、3.2、3.3，搭配 gem、bundler、rbenv |
| **PHP** | 8.3，搭配 Composer |
| **Java** | OpenJDK 21，搭配 Maven 和 Gradle |
| **Go** | Go，搭配模块支持 |
| **Rust** | rustc 和 cargo |
| **C/C++** | GCC、Clang、cmake、ninja、conan |
| **Docker** | docker、dockerd、docker compose |
| **Databases** | PostgreSQL 16、Redis 7.0 |
| **Utilities** | git、gh、jq、yq、ripgrep、tmux、vim、nano |

¹ Bun 已安装，但在包获取时存在已知的[代理兼容性问题](#install-dependencies-with-a-sessionstart-hook)。

要获取此表中大多数工具的版本，请让 Claude 在云端会话中运行 `check-tools`。它是安装在会话 VM 上的 shell 命令，不是您以 `/` 输入的命令；您让 Claude 运行是因为 [Claude 为您运行所有 VM 命令](#run-tests-start-services-and-add-packages)。对于它不报告的工具，例如 Ruby、PHP、bun、PostgreSQL 或 Redis，请让 Claude 运行该工具自己的版本命令，例如 `psql --version`。

Node.js 版本安装在 `/opt/node20`、`/opt/node21` 和 `/opt/node22`，默认情况下 22 在 `PATH` 上。要使用不同的版本，请让 Claude 将该版本的 `bin` 目录（例如 `/opt/node20/bin`）前置到 `PATH`。

此列表之外的工具链，例如 .NET SDK，即使其包注册表在[默认允许列表](#default-allowed-domains)上也不会预安装。请使用[设置脚本](#setup-scripts)安装它们。

<h3 id="work-with-github-issues-and-pull-requests">
  使用 GitHub 问题和 Pull Request
</h3>

云端会话包括内置 GitHub 工具，让 Claude 无需任何设置即可读取问题、列出 Pull Request、获取 diff 和发布评论。这些工具通过 [GitHub 代理](#github-proxy)，使用您在 [GitHub 身份验证选项](/docs/zh-CN/claude-code-on-the-web#github-authentication-options)下配置的任何方法进行身份验证，因此您的令牌永远不会进入容器。

您可以在[环境设置](#set-environment-variables)中自己设置 `GH_TOKEN` 或 `GITHUB_TOKEN`，或者两者都不设置，让 [GitHub 代理](#github-proxy)为您进行身份验证：

* 如果您设置了令牌，它会原封不动地传递到容器中，因此您的脚本和 GitHub 的 [`gh` CLI](https://cli.github.com) 会直接使用它。
* 如果您都不设置，且由 [GitHub 代理](#github-proxy)为您的会话处理身份验证，这两个变量在 Claude 运行的命令中读取为占位符字符串 `proxy-injected`，代理在出站 GitHub 请求上替换为您的真实凭据。针对已附加仓库的 `gh api` 调用无需您自己的令牌即可工作，但直接读取 `GITHUB_TOKEN` 的脚本会得到占位符，而不是可用的令牌。

您设置的令牌是普通环境变量，因此使用环境的任何人都可以读取它；代理路径将凭据保留在环境配置和会话 VM 之外。

要检查哪种情况适用于您的会话，请让 Claude 运行 `echo $GH_TOKEN`。

GitHub 的 [`gh` CLI](https://cli.github.com) 已预安装。如果您需要内置工具未涵盖的 GitHub 操作，请让 Claude 使用 `gh api` 调用 REST API。使用 REST API 的 `gh` 子命令（例如 `gh workflow list`）也可以工作。代理会[拒绝使用 GraphQL 的子命令](#github-proxy)，例如 `gh pr` 和 `gh issue`。`gh` 会自动读取 `GH_TOKEN`，因此您不需要运行 `gh auth login`。

<h3 id="link-output-back-to-the-session">
  将输出链接回会话
</h3>

每个云端会话在 claude.ai 上都有一个会话记录 URL，会话可以从 `CLAUDE_CODE_REMOTE_SESSION_ID` 环境变量读取自己的 ID。使用它在 PR 正文、提交信息、Slack 帖子或生成的报告中放置可追溯的链接，以便审阅者可以打开生成它们的运行。

Claude 在云端会话中创建的提交包括 `Claude-Session: <url>` git 尾注，PR 正文在单独一行包括会话 URL。要省略尾注和 PR 正文链接，请将 [`attribution.sessionUrl`](/docs/zh-CN/settings-reference#attribution-sessionurl) 设置为 `false`。

要在提交或 PR 以外的内容中包含会话链接，例如 Claude 发布的 Slack 消息或它编写的报告文件，请让 Claude 运行以下命令并使用其输出。该命令将环境变量值中的 `cse_` 前缀转换为会话记录 URL 预期的 `session_` 前缀：

```bash theme={null}
echo "https://claude.ai/code/${CLAUDE_CODE_REMOTE_SESSION_ID/#cse_/session_}"
```

<h3 id="run-tests-start-services-and-add-packages">
  运行测试、启动服务和添加包
</h3>

您无法进入会话 VM 的 shell。Claude 为您运行每个命令，因此请将本节中的任务表述为您提示词中的请求。

<h4 id="run-tests">
  运行测试
</h4>

Claude 在处理任务的过程中运行测试。在您的提示词中提出要求，例如"修复 `tests/` 中的失败测试"或"在每次更改后运行 pytest"。随[预安装的工具链](#installed-tools)提供的测试运行器（例如 pytest 和 cargo test）无需额外设置即可工作。您的项目声明为依赖的运行器（例如 jest）会随您的依赖一起安装。

<h4 id="start-services">
  启动服务
</h4>

PostgreSQL 和 Redis 已预安装但默认不运行。让 Claude 启动您需要的任何一个；它运行的命令是：

```bash theme={null}
service postgresql start
```

```bash theme={null}
service redis-server start
```

Docker 可用于运行容器化服务。让 Claude 运行 `docker compose up` 以启动您项目的服务。拉取镜像的网络访问遵循您环境的[访问级别](#access-levels)，[Trusted 默认值](#default-allowed-domains)包括 Docker Hub 和其他常见注册表。

如果您的镜像很大或拉取速度很慢，请将 `docker compose pull` 或 `docker compose build` 添加到您的[设置脚本](#setup-scripts)。[环境缓存](#environment-caching)保留拉取的镜像，因此每个新会话的磁盘上都有它们。缓存仅保存文件，不保存运行中的进程，因此 Claude 仍然在每个会话中启动容器。

<h4 id="add-packages">
  添加包
</h4>

要添加未预安装的包，请使用[设置脚本](#setup-scripts)。[环境缓存](#environment-caching)保留脚本安装的内容，因此您在那里安装的包在每个会话开始时都可用，无需每次重新安装。您也可以让 Claude 在会话中途安装包，但这些安装不会带到其他会话。

<h3 id="resource-limits">
  资源限制
</h3>

Anthropic 托管环境中的云端会话运行时具有可能随时间变化的近似资源上限：

* 4 vCPU
* 16 GB RAM
* 30 GB 磁盘

VM 可能会停止需要明显更多内存的任务，例如大型构建作业或内存密集型测试。对于超出这些限制的工作负载，请使用 [Remote Control](/docs/zh-CN/remote-control) 在您自己的硬件上运行 Claude Code，或在[自托管环境](/docs/zh-CN/self-hosted-environments)中运行云端会话，该环境在您的组织运营的计算资源上。

<h3 id="time-limits">
  时间限制
</h3>

在 Anthropic 托管的环境中，这些时间限制适用于云端会话中的长时间运行的工作，例如构建、安装或测试运行。每个条目链接到定义该限制的部分。

* **Claude 运行的命令**：云环境不设置自己的命令超时时间，因此 Bash 工具的默认值适用。Claude 默认为前台命令等待 2 分钟，最多可以要求 10 分钟。

  当命令达到其[超时](/docs/zh-CN/tools-reference#timeout-and-output-limits)时，Claude Code [将其移到后台](/docs/zh-CN/tools-reference#foreground-commands-that-move-to-the-background)，而不是停止它，除非命令以 `sleep` 开头。以这种方式移动的命令可以继续运行最多 30 分钟，然后 Claude Code 在其[后台时间限制](/docs/zh-CN/tools-reference#time-limit-for-background-commands)处停止它。将 `BASH_DEFAULT_TIMEOUT_MS` 设置为 `1800000` 毫秒以上会延长该限制以及前台默认值。
* **SessionStart hook**：Claude Code 在 600 秒后取消 `command` hook，除非您在 hook 条目上设置 [`timeout`](/docs/zh-CN/hooks#common-fields)（以秒为单位）。Claude Code 不会对您使用 [`async: true`](/docs/zh-CN/hooks#run-hooks-in-the-background) 运行的 hook 强制执行超时。
* **设置脚本**：花费超过大约五分钟的脚本不会被缓存。[脚本要求](#script-requirements)涵盖如何保持在该时间以下。
* **空闲会话**：在几分钟没有活动后，会话的 VM 会暂停并保存其文件，暂停的 VM 之后可能会被回收。[设置环境变量](#set-environment-variables)描述会话在每种情况下会获取什么，[环境已过期](/docs/zh-CN/claude-code-on-the-web#environment-expired)涵盖如何重新打开 VM 被回收的会话。

要为环境的会话提高命令超时时间，请将 [`BASH_DEFAULT_TIMEOUT_MS` 和 `BASH_MAX_TIMEOUT_MS`](/docs/zh-CN/env-vars#variables) 添加到其[环境变量](#set-environment-variables)。两者都采用毫秒。例如，`BASH_DEFAULT_TIMEOUT_MS=600000` 使 10 分钟成为默认值。

<h2 id="setup-scripts">
  设置脚本
</h2>

设置脚本是一个 Bash 脚本，在新的云会话启动时运行，在 Claude Code 启动之前运行。使用设置脚本来安装依赖项、配置工具，或获取会话需要但未预安装的任何内容。

脚本以 root 身份在 Ubuntu 24.04 上运行，因此 `apt install` 和大多数语言包管理器都能工作。

要添加设置脚本，请打开环境设置对话框，并在 **Setup script** 字段中输入您的脚本。

此示例安装 [ShellCheck](https://www.shellcheck.net/)，它不是预安装的。

```bash theme={null}
#!/bin/bash
apt update && apt install -y shellcheck
```

<h3 id="script-requirements">
  脚本要求
</h3>

设置脚本有三个需要考虑的约束：

* **以零退出**：如果脚本以非零状态结束，会话将无法启动。在非关键命令后附加 `|| true`，以便间歇性安装失败不会阻止会话。
* **在五分钟内完成**：将脚本的总运行时间保持在大约五分钟以内，以便[环境缓存](#environment-caching)可以建立。当设置耗时超过五分钟时，环境不会被缓存。使用 `&` 和 `wait` 并行运行独立的安装，并将任何无法容纳的单个下载移至 [SessionStart hook](#setup-scripts-vs-sessionstart-hooks)，在后台启动它。如果新会话在设置期间停滞或失败，请参阅[新会话在设置期间挂起或超时](/docs/zh-CN/web-quickstart#new-sessions-hang-or-time-out-during-setup)。
* **安装需要网络访问**：包安装需要连接到注册表。默认的 **Trusted** 级别涵盖[常见包注册表](#default-allowed-domains)，包括 npm、PyPI、RubyGems 和 crates.io；使用 **None** 网络访问时，安装会失败。

<h3 id="environment-caching">
  环境缓存
</h3>

设置脚本在您第一次在环境中启动会话时运行。当设置在[大约五分钟](#script-requirements)内完成时，Anthropic 会对文件系统进行快照，并将该快照重用作后续会话的起点。新会话以您的依赖项、工具和 Docker 镜像已在磁盘上的状态开始，并跳过设置脚本步骤。即使脚本安装大型工具链或拉取容器镜像，这也能保持启动速度快。如果设置耗时超过大约五分钟，环境不会被缓存。

缓存是文件系统快照，因此它会保留设置脚本写入磁盘的内容，并丢失任何仅在运行中的内容。您安装的包、您拉取的 Docker 镜像和您写入的文件都会保留。脚本启动的数据库、`docker compose up` 堆栈或任何其他后台进程不会保留；请通过询问 Claude 或使用 [SessionStart hook](#setup-scripts-vs-sessionstart-hooks) 在每个会话中启动这些。

当您更改环境的设置脚本或允许的网络主机时，以及当缓存在大约七天后到期时，设置脚本会再次运行以重建缓存。在 Anthropic 托管环境中，当会话的 VM 在[空闲后恢复](#set-environment-variables)时，设置脚本不会运行，因此对脚本的更改仅在其 VM 被[回收](/docs/zh-CN/claude-code-on-the-web#environment-expired)并重建时才会到达现有会话。要立即应用更改，请在会话中运行命令或启动新会话。

您不需要自己启用缓存或管理快照。

<h3 id="setup-scripts-vs-sessionstart-hooks">
  设置脚本与 SessionStart hooks
</h3>

使用设置脚本来配备 VM 本身：未[预安装](#installed-tools)的工具链和 CLI 工具。使用 [SessionStart hook](/docs/zh-CN/hooks#sessionstart) 进行应在各处运行的项目设置，包括云端和本地，例如 `npm install`。

设置脚本和 SessionStart hooks 在云会话启动时按固定顺序运行。下表比较了您在哪里配置它们、何时运行以及在哪里运行。

| | 设置脚本 | SessionStart hooks |
| - | - | - |
| **您在哪里配置它们** | [claude.ai/code](https://claude.ai/code) 的环境对话框，以及[共享环境](#organization-shared-environments)的 **Cloud environments** 管理页面 | [设置文件](/docs/zh-CN/settings#where-settings-live)，例如您的存储库的 `.claude/settings.json`；请参阅[您的设置中会保留的内容](#what-carries-over-from-your-setup)，了解哪些文件会到达云会话 |
| **它们何时运行** | 在 Claude Code 启动之前，当存在[缓存环境](#environment-caching)时跳过 | 在 Claude Code 启动后，在每个会话（包括已恢复的会话）上 |
| **它们在哪里运行** | 仅限云会话 | 本地和云会话 |

如果您在用户级 `~/.claude/settings.json` 中有 SessionStart hooks，不要期望它们在云端生效。用户级设置保留在您的机器上。其他 hooks 运行的位置取决于会话运行的位置：

* **Anthropic 托管环境**：Claude Code 运行来自存储库和您组织的[服务器管理的设置](/docs/zh-CN/server-managed-settings)的 hooks。[Claude Tag](https://claude.com/docs/claude-tag/overview) 会话不会接收服务器管理的设置，因此来自服务器管理的设置的 hooks 不会在那里运行。
* **[自托管环境](/docs/zh-CN/self-hosted-environments-configuration#permissions-and-tool-approval)**：Claude Code 还运行运行程序主机的 `~/.claude/` 中的运行程序操作员播种的 hooks，以及运行程序镜像的托管设置文件中的 hooks，当该文件是 [Claude Code 应用的托管源](/docs/zh-CN/managed-settings#how-claude-code-combines-managed-sources)之一时。

<h3 id="install-dependencies-with-a-sessionstart-hook">
  使用 SessionStart hook 安装依赖项
</h3>

要仅在云会话中安装依赖项，请将 SessionStart hook 与检查其运行位置的脚本配对。

首先，将 SessionStart hook 添加到您的存储库的 `.claude/settings.json`。此配置告诉 Claude Code 在会话启动或恢复时运行存储库中的 `scripts/install_pkgs.sh`：

```json theme={null}
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume",
        "hooks": [
          {
            "type": "command",
            "command": "bash \"$CLAUDE_PROJECT_DIR\"/scripts/install_pkgs.sh"
          }
        ]
      }
    ]
  }
}
```

`matcher` 将 hook 限制为 `startup` 和 `resume` 事件，`$CLAUDE_PROJECT_DIR` 解析为存储库根目录，因此无论会话的工作目录是什么，hook 都能找到脚本。

接下来，在 `scripts/install_pkgs.sh` 创建脚本。它在云端之外立即退出，否则安装您的依赖项：

```bash theme={null}
#!/bin/bash

if [ "$CLAUDE_CODE_REMOTE" != "true" ]; then
  exit 0
fi

npm install
pip install -r requirements.txt
exit 0
```

`CLAUDE_CODE_REMOTE` 检查是将安装限制在云会话的关键：会话 VM 的环境将该变量设置为 `true`，在本地永远不会是 `true`，因此在您的笔记本电脑上，脚本会在安装任何内容之前退出。

这两个文件一起使每个云会话在启动时获得全新的 `npm install` 和 `pip install`，同时保持本地会话不受影响。

<h4 id="limitations-in-cloud-sessions">
  云会话中的限制
</h4>

SessionStart hooks 在云端的行为与本地相同，但有以下注意事项：

* **每个会话一个仓库**：在 Anthropic 托管环境中，具有多个仓库的会话不会从任何仓库的 `.claude/settings.json` 加载 hook，因此您在那里定义的 SessionStart hook 不会运行。请改为使用[设置脚本](#setup-scripts)为这些会话安装依赖项。对于自托管环境，请参阅[适用哪个仓库的设置](/docs/zh-CN/self-hosted-environments-configuration#repository-settings-in-sessions-with-several-repositories)。
* **没有仅云端的范围**：hooks 在本地和云会话中都运行。要跳过本地运行，请在 `CLAUDE_CODE_REMOTE` 环境变量不为 `true` 时提前退出，就像[依赖项安装脚本](#install-dependencies-with-a-sessionstart-hook)所做的那样。
* **需要网络访问**：安装命令需要连接到包注册表。如果您的环境使用 **None** 网络访问，这些 hooks 会失败。**Trusted** 下的[默认允许列表](#default-allowed-domains)涵盖 npm、PyPI、RubyGems 和 crates.io。
* **代理兼容性**：在 Anthropic 托管环境中，所有出站流量都经过[安全代理](#security-proxy)，某些包管理器无法与此代理正确配合工作；Bun 是一个已知的例子。在[自托管环境](/docs/zh-CN/self-hosted-environments-deploy#default-deny-egress)中，出站流量改为经过您自己的网络边界。
* **增加启动延迟**：hooks 在每次会话启动或恢复时运行，不同于受益于[环境缓存](#environment-caching)的设置脚本。请通过在重新安装之前检查依赖项是否已存在来保持安装脚本快速。

要自定义基础镜像，请使用设置脚本在[提供的镜像](#installed-tools)上安装您需要的内容，或使用 `docker compose` 将您自己的镜像作为 Claude 旁边的容器运行。目前不支持完全替换基础镜像。

<h2 id="default-allowed-domains">
  默认允许的域
</h2>

使用 **Trusted** 网络访问，会话默认可以访问以下域。标记为 `*` 的域表示通配符子域匹配，因此 `*.gcr.io` 允许 `gcr.io` 的任何子域。

<AccordionGroup>
  <Accordion title="Anthropic 服务">
    * api.anthropic.com
    * docs.claude.com
    * platform.claude.com
    * code.claude.com
    * claude.ai
    * claude.com
    * support.claude.com
    * anthropic.com
    * [www.anthropic.com](http://www.anthropic.com)
  </Accordion>

  <Accordion title="版本控制">
    * github.com
    * [www.github.com](http://www.github.com)
    * api.github.com
    * npm.pkg.github.com
    * raw\.githubusercontent.com
    * pkg-npm.githubusercontent.com
    * objects.githubusercontent.com
    * release-assets.githubusercontent.com
    * codeload.github.com
    * avatars.githubusercontent.com
    * camo.githubusercontent.com
    * gist.github.com
    * gitlab.com
    * [www.gitlab.com](http://www.gitlab.com)
    * registry.gitlab.com
    * bitbucket.org
    * [www.bitbucket.org](http://www.bitbucket.org)
    * api.bitbucket.org
  </Accordion>

  <Accordion title="容器注册表">
    * registry-1.docker.io
    * auth.docker.io
    * index.docker.io
    * hub.docker.com
    * [www.docker.com](http://www.docker.com)
    * production.cloudflare.docker.com
    * production.cloudfront.docker.com
    * download.docker.com
    * gcr.io
    * \*.gcr.io
    * ghcr.io
    * mcr.microsoft.com
    * \*.data.mcr.microsoft.com
    * public.ecr.aws
  </Accordion>

  <Accordion title="云平台">
    * cloud.google.com
    * accounts.google.com
    * gcloud.google.com
    * \*.googleapis.com
    * storage.googleapis.com
    * compute.googleapis.com
    * container.googleapis.com
    * azure.com
    * portal.azure.com
    * microsoft.com
    * [www.microsoft.com](http://www.microsoft.com)
    * \*.microsoftonline.com
    * packages.microsoft.com
    * dotnet.microsoft.com
    * dot.net
    * visualstudio.com
    * dev.azure.com
    * \*.amazonaws.com
    * \*.api.aws
    * oracle.com
    * [www.oracle.com](http://www.oracle.com)
    * java.com
    * [www.java.com](http://www.java.com)
    * java.net
    * [www.java.net](http://www.java.net)
    * download.oracle.com
    * yum.oracle.com
    * \*.r2.cloudflarestorage.com
  </Accordion>

  <Accordion title="JavaScript 和 Node 包管理器">
    * registry.npmjs.org
    * [www.npmjs.com](http://www.npmjs.com)
    * [www.npmjs.org](http://www.npmjs.org)
    * npmjs.com
    * npmjs.org
    * yarnpkg.com
    * registry.yarnpkg.com
    * jsr.io
    * npm.jsr.io
  </Accordion>

  <Accordion title="Python 包管理器">
    * pypi.org
    * [www.pypi.org](http://www.pypi.org)
    * files.pythonhosted.org
    * pythonhosted.org
    * test.pypi.org
    * pypi.python.org
    * pypa.io
    * [www.pypa.io](http://www.pypa.io)
  </Accordion>

  <Accordion title="Ruby 包管理器">
    * rubygems.org
    * [www.rubygems.org](http://www.rubygems.org)
    * api.rubygems.org
    * index.rubygems.org
    * ruby-lang.org
    * [www.ruby-lang.org](http://www.ruby-lang.org)
    * rubyforge.org
    * [www.rubyforge.org](http://www.rubyforge.org)
    * rubyonrails.org
    * [www.rubyonrails.org](http://www.rubyonrails.org)
    * rvm.io
    * get.rvm.io
  </Accordion>

  <Accordion title="Rust 包管理器">
    * crates.io
    * [www.crates.io](http://www.crates.io)
    * index.crates.io
    * static.crates.io
    * rustup.rs
    * static.rust-lang.org
    * [www.rust-lang.org](http://www.rust-lang.org)
  </Accordion>

  <Accordion title="Go 包管理器">
    * proxy.golang.org
    * sum.golang.org
    * index.golang.org
    * golang.org
    * [www.golang.org](http://www.golang.org)
    * goproxy.io
    * pkg.go.dev
  </Accordion>

  <Accordion title="JVM 包管理器">
    * maven.org
    * repo.maven.org
    * central.maven.org
    * repo1.maven.org
    * repo.maven.apache.org
    * maven.google.com
    * jcenter.bintray.com
    * gradle.org
    * [www.gradle.org](http://www.gradle.org)
    * services.gradle.org
    * plugins.gradle.org
    * plugins-artifacts.gradle.org
    * kotlinlang.org
    * [www.kotlinlang.org](http://www.kotlinlang.org)
    * spring.io
    * repo.spring.io
  </Accordion>

  <Accordion title="其他包管理器">
    * packagist.org (PHP Composer)
    * [www.packagist.org](http://www.packagist.org)
    * repo.packagist.org
    * nuget.org (.NET NuGet)
    * [www.nuget.org](http://www.nuget.org)
    * api.nuget.org
    * pub.dev (Dart/Flutter)
    * api.pub.dev
    * hex.pm (Elixir/Erlang)
    * [www.hex.pm](http://www.hex.pm)
    * cpan.org (Perl CPAN)
    * [www.cpan.org](http://www.cpan.org)
    * metacpan.org
    * [www.metacpan.org](http://www.metacpan.org)
    * api.metacpan.org
    * cocoapods.org (iOS/macOS)
    * [www.cocoapods.org](http://www.cocoapods.org)
    * cdn.cocoapods.org
    * haskell.org
    * [www.haskell.org](http://www.haskell.org)
    * hackage.haskell.org
    * swift.org
    * [www.swift.org](http://www.swift.org)
  </Accordion>

  <Accordion title="Linux 发行版">
    * archive.ubuntu.com
    * security.ubuntu.com
    * ubuntu.com
    * [www.ubuntu.com](http://www.ubuntu.com)
    * \*.ubuntu.com
    * ppa.launchpad.net
    * launchpad.net
    * [www.launchpad.net](http://www.launchpad.net)
    * \*.nixos.org
  </Accordion>

  <Accordion title="开发工具和平台">
    * dl.k8s.io (Kubernetes)
    * pkgs.k8s.io
    * k8s.io
    * [www.k8s.io](http://www.k8s.io)
    * releases.hashicorp.com (HashiCorp)
    * apt.releases.hashicorp.com
    * rpm.releases.hashicorp.com
    * archive.releases.hashicorp.com
    * hashicorp.com
    * [www.hashicorp.com](http://www.hashicorp.com)
    * repo.anaconda.com (Anaconda/Conda)
    * conda.anaconda.org
    * anaconda.org
    * [www.anaconda.com](http://www.anaconda.com)
    * anaconda.com
    * continuum.io
    * apache.org (Apache)
    * [www.apache.org](http://www.apache.org)
    * archive.apache.org
    * downloads.apache.org
    * eclipse.org (Eclipse)
    * [www.eclipse.org](http://www.eclipse.org)
    * download.eclipse.org
    * nodejs.org (Node.js)
    * [www.nodejs.org](http://www.nodejs.org)
    * developer.apple.com
    * developer.android.com
    * pkg.stainless.com
    * binaries.prisma.sh
  </Accordion>

  <Accordion title="云服务和监控">
    * http-intake.logs.datadoghq.com
    * \*.datadoghq.com
    * \*.datadoghq.eu
    * api.honeycomb.io
  </Accordion>

  <Accordion title="内容分发和镜像">
    * sourceforge.net
    * \*.sourceforge.net
    * packagecloud.io
    * \*.packagecloud.io
    * fonts.googleapis.com
    * fonts.gstatic.com
  </Accordion>

  <Accordion title="架构和配置">
    * json-schema.org
    * [www.json-schema.org](http://www.json-schema.org)
    * json.schemastore.org
    * [www.schemastore.org](http://www.schemastore.org)
  </Accordion>

  <Accordion title="Model Context Protocol">
    * \*.modelcontextprotocol.io
  </Accordion>
</AccordionGroup>

<h2 id="related-resources">
  相关资源
</h2>

* [Cloud sessions reference](/docs/zh-CN/claude-code-on-the-web)：启动、管理和共享云会话
* [Cloud sessions quickstart](/docs/zh-CN/web-quickstart)：连接 GitHub 并启动您的第一个云会话
* [Claude Tag](https://claude.com/docs/claude-tag/overview)：Claude 从 Slack 启动的会话在相同的环境中运行
* [Routines](/docs/zh-CN/routines)：计划运行使用相同的环境和网络访问级别
* [Remote Control](/docs/zh-CN/remote-control)：改为在您自己的机器的网络和文件上运行会话
* [Self-hosted environments](/docs/zh-CN/self-hosted-environments)：在您的组织自己的基础设施上运行云会话
* [SessionStart hooks](/docs/zh-CN/hooks#sessionstart)：存储库提交的设置，在本地和云会话中运行
* [Server-managed settings](/docs/zh-CN/server-managed-settings)：从管理控制台交付的组织策略
