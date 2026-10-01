> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 在 Chrome 中使用 Claude Code

> 将 Claude Code 连接到 Chrome 浏览器，以测试网络应用、使用控制台日志进行调试、自动填充表单以及从网页中提取数据。

Claude Code 与 [Claude in Chrome 浏览器扩展程序](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) 集成，为您提供从 CLI 或 [VS Code 扩展程序](/docs/zh-CN/vs-code#automate-browser-tasks-with-chrome) 进行浏览器自动化的功能。构建您的代码，然后在浏览器中测试和调试，无需切换上下文。

Claude 为浏览器任务打开新标签页，并共享您浏览器的登录状态，因此它可以访问您已登录的任何网站。浏览器操作在实时可见的 Chrome 窗口中运行。当 Claude 遇到登录页面或 CAPTCHA 时，它会暂停并要求您手动处理。

扩展程序将 Claude 打开的标签页收集到与您的会话相关联的 Chrome 标签页组中。在本地会话中，Claude Code 是否在会话结束时关闭该组取决于会话如何结束：

* 当您输入 `/clear` 时，Claude Code 会关闭该组（包括打开的页面），除非仍在运行的工作在清除后仍然存在
* 当您使用 `/resume` 等命令切换会话、退出 Claude Code 或在仍在运行的工作中运行 `/clear` 时，Claude Code 仅在该组仅包含空的新标签页时才关闭该组，因此您可能仍在阅读的页面保持打开状态

<Note>
  Chrome 集成适用于 Google Chrome 和 Microsoft Edge。Claude Code 还会检测扩展程序并在其他基于 Chromium 的浏览器中设置连接，包括 Brave、Arc、Vivaldi 和 Opera。Windows 子系统 for Linux (WSL) 不支持 Chrome 集成。
</Note>

<h2 id="capabilities">
  功能
</h2>

连接 Chrome 后，您可以在单个工作流中链接浏览器操作和编码任务：

* **实时调试**：直接读取控制台错误和 DOM 状态，然后修复导致这些错误的代码
* **设计验证**：从 Figma 模型构建 UI，然后在浏览器中打开它以验证它是否匹配
* **网络应用测试**：测试表单验证、检查视觉回归或验证用户流程
* **已认证的网络应用**：与 Google Docs、Gmail、Notion 或您已登录的任何应用交互，无需 API 连接器
* **数据提取**：从网页中提取结构化信息并将其保存到本地
* **任务自动化**：自动化重复的浏览器任务，如数据输入、表单填充或多站点工作流
* **文件上传**：将您计算机中的文件附加到网页上的上传字段
* **会话录制**：将浏览器交互录制为 GIF，以记录或分享发生的情况

<h2 id="prerequisites">
  前置条件
</h2>

在使用 Claude Code 与 Chrome 之前，您需要：

* [Google Chrome](https://www.google.com/chrome/)、[Microsoft Edge](https://www.microsoft.com/edge) 或其他基于 Chromium 的浏览器，如 Brave、Arc、Vivaldi 或 Opera
* [Claude in Chrome 扩展程序](https://chromewebstore.google.com/detail/claude/fcoeoabgfenejglbffodgkkbkcdhcgfn) 版本 1.0.36 或更高版本，可在 Chrome Web Store 中获得
* [Claude Code](/docs/zh-CN/quickstart#step-1-install-claude-code)
* 直接 Anthropic 计划（Pro、Max、Team 或 Enterprise）

Chrome 集成还需要使用 `/login` 登录。如果您使用 API 密钥或来自 [`claude setup-token`](/docs/zh-CN/authentication#generate-a-long-lived-token) 的长期令牌进行身份验证，Claude Code 会关闭 Chrome 集成，即使您传递 `--chrome`，因为浏览器扩展程序无法使用这些凭据进行身份验证。在 v2.1.216 之前，这些会话可以启用 Chrome 集成，但每次尝试连接到浏览器扩展程序都会失败，并显示 403 错误。

<Note>
  Chrome 集成不可通过 Amazon Bedrock、Google Cloud 的 Agent Platform 或 Microsoft Foundry 等第三方提供商获得。如果您仅通过第三方提供商访问 Claude，则需要单独的 claude.ai 账户来使用此功能。
</Note>

<h2 id="get-started-in-the-cli">
  在 CLI 中开始
</h2>

<Steps>
  <Step title="使用 Chrome 启动 Claude Code">
    使用 `--chrome` 标志启动 Claude Code：

    ```bash theme={null}
    claude --chrome
    ```

    首次使用 Chrome 启动时，Claude Code 会显示一个一次性对话框，介绍该集成并解释网站权限的工作原理。按 Enter 继续。

    要在未来的会话中启用 Chrome 而无需该标志，请参阅[默认启用 Chrome](#enable-chrome-by-default)。
  </Step>

  <Step title="要求 Claude 使用浏览器">
    此示例导航到页面、与其交互并报告其发现，全部来自您的终端或编辑器：

    ```text wrap theme={null}
    Go to code.claude.com/docs, click on the search box,
    type "hooks", and tell me what results appear
    ```

    如果 Claude Code 在浏览器操作前要求权限，请批准它。对话框以 `Claude in Chrome wants to` 开头，并提供在该会话中允许该网站上所有操作的选项。Claude 打开一个新标签页并开始任务。
  </Step>
</Steps>

随时运行 `/chrome` 以检查连接状态、管理权限、重新连接扩展程序或选择要使用的已连接浏览器。当状态面板显示"Status: 已启用"和"Extension: 已安装"时，集成正在工作。

如果连接了多个浏览器，您可以选择 Claude 使用哪一个。当浏览器操作在您选择之前开始时，Claude 会提示您选择一个。要稍后切换浏览器，运行 `/chrome` 并选择**选择浏览器…**。即使另一个浏览器连接，Claude 也会继续使用您的选择。

对于 VS Code，请参阅[在 VS Code 中使用 Chrome 自动化浏览器任务](/docs/zh-CN/vs-code#automate-browser-tasks-with-chrome)。

<h3 id="install-the-extension-when-claude-asks">
  当 Claude 要求时安装扩展程序
</h3>

当 Claude 在交互式会话中需要您的浏览器，而 Claude Code 未检测到扩展程序时，Claude Code 会显示标题为"Claude wants to use your browser"的安装提示。Claude Code 每个会话最多询问一次。

该提示提供三个选择：

* **安装扩展程序**：在您的浏览器中打开扩展程序安装页面并启动引导式设置。Claude Code 等待安装、连接扩展程序，并在同一会话中启用浏览器工具。当连接准备好时，选择"Continue with browser tools"，Claude 在您的浏览器中恢复任务。您可以通过选择"Continue without browser tools"离开设置，稍后使用 `/chrome` 完成。
* **暂不**：继续执行任务而不使用浏览器工具。Claude Code 可以在稍后的会话中再次询问。
* **不再询问**：在未来的会话中停止该提示。您仍然可以随时使用 `/chrome` 设置集成。

两个托管 MCP 策略会关闭该提示：

* 如果您的组织使用 [`deniedMcpServers` 托管设置](/docs/zh-CN/managed-mcp#policy-based-control-with-allowlists-and-denylists)阻止 `claude-in-chrome` MCP 服务器，Claude Code 不会显示安装提示。
* 如果您的组织部署了 [`managed-mcp.json`](/docs/zh-CN/managed-mcp#exclusive-control-with-managed-mcp-json) 文件，但未[在托管集合中允许 Claude in Chrome](/docs/zh-CN/managed-mcp#allow-claude-in-chrome-alongside-the-managed-set)，Claude Code 不会显示安装提示。

<h3 id="enable-chrome-by-default">
  默认启用 Chrome
</h3>

为了避免每个会话都传递 `--chrome`，运行 `/chrome` 并选择"默认启用"。

当 Chrome 未运行时，Claude Code 正常启动。在 v2.1.211 之前，当启用了 Chrome 集成但 Chrome 未运行时，启动可能会挂起。

在 [VS Code 扩展程序](/docs/zh-CN/vs-code#automate-browser-tasks-with-chrome)中，只要安装了 Chrome 扩展程序，Chrome 就可用。无需额外标志。

<Note>
  在 CLI 中默认启用 Chrome 会增加上下文使用，因为浏览器工具始终被加载。如果您注意到上下文消耗增加，请禁用此设置，仅在需要时使用 `--chrome`。
</Note>

<h3 id="manage-site-permissions">
  管理网站权限
</h3>

网站级权限从 Chrome 扩展程序继承。在 Chrome 扩展程序设置中管理权限，以控制 Claude 可以浏览、点击和输入的网站。在[自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)中，当自动模式分类器本身批准对网站的浏览器调用时，扩展程序会跳过该调用的自己的按网站检查，除非您的权限规则拒绝任何网站对 Claude in Chrome 的访问。

<h3 id="browser-tools-in-plan-mode">
  Plan Mode 中的浏览器工具
</h3>

在 [plan mode](/docs/zh-CN/permission-modes#analyze-before-you-edit-with-plan-mode)中，在 Claude 记录 GIF、打开新标签页或运行快捷方式之前会出现权限提示。如果您的会话中[可用绕过权限模式](/docs/zh-CN/permission-modes#skip-all-checks-with-bypasspermissions-mode)且[功能标志获取](/docs/zh-CN/env-vars#features-that-need-feature-flag-fetching)已关闭，这些调用将在没有提示的情况下运行。

当 `tabs_context_mcp` 调用设置 `createIfEmpty` 时也会提示，包含任何这些操作的 `browser_batch` 调用也是如此。

<h2 id="example-workflows">
  示例工作流
</h2>

这些示例展示了将浏览器操作与编码任务结合的常见方式。运行 `/mcp`，选择 `claude-in-chrome`，然后选择**查看工具**以查看可用浏览器工具的完整列表。

<h3 id="test-a-local-web-application">
  测试本地网络应用
</h3>

在开发网络应用时，要求 Claude 验证您的更改是否正常工作：

```text wrap theme={null}
I just updated the login form validation. Can you open localhost:3000,
try submitting the form with invalid data, and check if the error
messages appear correctly?
```

Claude 导航到您的本地服务器、与表单交互并报告其观察到的内容。

<h3 id="debug-with-console-logs">
  使用控制台日志进行调试
</h3>

Claude 可以读取控制台输出以帮助诊断问题。告诉 Claude 要查找的模式，而不是要求所有控制台输出，因为日志可能很冗长：

```text wrap theme={null}
Open the dashboard page and check the console for any errors when
the page loads.
```

Claude 读取控制台消息，可以过滤特定模式或错误类型。

<h3 id="automate-form-filling">
  自动填充表单
</h3>

加快重复数据输入任务的速度：

```text wrap theme={null}
I have a spreadsheet of customer contacts in contacts.csv. For each row,
go to the CRM at crm.example.com, click "Add Contact", and fill in the
name, email, and phone fields.
```

Claude 读取您的本地文件、导航网络界面并为每条记录输入数据。

<h3 id="upload-files-to-web-pages">
  将文件上传到网页
</h3>

Claude 可以将您计算机中的文件附加到页面上的上传字段。Claude Code 读取文件并将其内容发送到浏览器，因此上传在本地和远程会话中都有效。需要 Claude Code v2.1.211 或更高版本。

此示例将日志文件附加到表单：

```text wrap theme={null}
Open the bug tracker at bugs.example.com, create a new issue,
and attach logs/session.log to it
```

上传有三个限制：

* **权限**：Claude 只能在会话被允许读取文件时上传文件，因此[权限规则](/docs/zh-CN/settings-reference#permission-settings)拒绝对文件的 `Read` 访问也会阻止上传。
* **大小**：单次上传最多可包含 10 MB 的文件。
* **硬链接**：Claude 拒绝具有多个硬链接的文件，这在 `node_modules` 等包管理器存储中很常见。复制文件并上传副本。

<h3 id="draft-content-in-google-docs">
  在 Google Docs 中起草内容
</h3>

使用 Claude 直接在您的文档中写入，无需 API 设置：

```text wrap theme={null}
Draft a project update based on the recent commits and add it to my
Google Doc at docs.google.com/document/d/abc123
```

Claude 打开文档、点击编辑器并输入内容。这适用于您已登录的任何网络应用：Gmail、Notion、Sheets 等。

<h3 id="extract-data-from-web-pages">
  从网页中提取数据
</h3>

从网站中提取结构化信息：

```text wrap theme={null}
Go to the product listings page and extract the name, price, and
availability for each item. Save the results as a CSV file.
```

Claude 导航到页面、读取内容并将数据编译成结构化格式。

<h3 id="run-multi-site-workflows">
  运行多站点工作流
</h3>

协调多个网站之间的任务：

```text wrap theme={null}
Check my calendar for meetings tomorrow, then for each meeting with
an external attendee, look up their company website and add a note
about what they do.
```

Claude 跨标签页工作以收集信息并完成工作流。

<h3 id="record-a-demo-gif">
  录制演示 GIF
</h3>

创建浏览器交互的可共享录制：

```text wrap theme={null}
Record a GIF showing how to complete the checkout flow, from adding
an item to the cart through to the confirmation page.
```

Claude 录制交互序列并将其保存为 GIF 文件。录制捕获浏览器中可见的所有内容，包括已登录页面上的帐户详细信息，因此在与团队外部共享之前请查看。

<h3 id="save-screenshots-to-disk">
  将屏幕截图保存到磁盘
</h3>

要求 Claude 将屏幕截图保存为文件：

```text wrap theme={null}
Take a screenshot of the checkout page and save it to disk
```

Claude 将图像保存到磁盘并报告文件路径。在 v2.1.211 之前，屏幕截图工具的 `save_to_disk` 选项没有写入文件。

<h2 id="troubleshooting">
  故障排除
</h2>

<h3 id="extension-not-detected">
  未检测到扩展程序
</h3>

如果 Claude Code 无法检测到 Chrome 扩展程序：

1. 验证 Chrome 扩展程序已安装并在 `chrome://extensions` 中启用
2. 通过运行 `claude --version` 验证 Claude Code 是最新的
3. 检查 Chrome 是否正在运行
4. 运行 `/chrome` 并选择"重新连接扩展程序"以重新建立连接
5. 如果问题仍然存在，请重新启动 Claude Code 和 Chrome

第一次启用 Chrome 集成时，Claude Code 会安装本机消息传递主机配置文件。Chrome 在启动时读取此文件，因此如果扩展程序在您的第一次尝试中未被检测到，请重新启动 Chrome 以获取新配置。

Claude Code 在首次安装时会打开一个浏览器标签页，提示您连接扩展程序。稍后重写配置文件的会话（例如在切换构建或配置目录后）不会重新打开它。

如果连接仍然失败，请验证主机配置文件是否存在于：

对于 Chrome：

* **macOS**：`~/Library/Application Support/Google/Chrome/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`
* **Linux**：`~/.config/google-chrome/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`
* **Windows**：检查 Windows 注册表中的 `HKCU\Software\Google\Chrome\NativeMessagingHosts\`

对于 Edge：

* **macOS**：`~/Library/Application Support/Microsoft Edge/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`
* **Linux**：`~/.config/microsoft-edge/NativeMessagingHosts/com.anthropic.claude_code_browser_extension.json`
* **Windows**：检查 Windows 注册表中的 `HKCU\Software\Microsoft\Edge\NativeMessagingHosts\`

其他基于 Chromium 的浏览器从其自己的配置目录读取相同的文件，该目录以浏览器命名。例如，macOS 上的 Brave 使用 `~/Library/Application Support/BraveSoftware/Brave-Browser/NativeMessagingHosts/`，在 Windows 上每个浏览器都有自己的注册表项，例如 `HKCU\Software\BraveSoftware\Brave-Browser\NativeMessagingHosts\`。

<h3 id="browser-not-responding">
  浏览器无响应
</h3>

如果 Claude 的浏览器命令停止工作：

1. 检查是否有模态对话框（alert、confirm、prompt）阻止页面。JavaScript 对话框阻止浏览器事件并防止 Claude 接收命令。手动关闭对话框，然后告诉 Claude 继续。
2. 要求 Claude 创建新标签页并重试
3. 通过在 `chrome://extensions` 中禁用并重新启用来重新启动 Chrome 扩展程序

<h3 id="connection-drops-during-long-sessions">
  长会话期间连接断开
</h3>

Chrome 扩展程序的 service worker 在扩展会话期间可能会进入空闲状态，这会破坏连接。如果浏览器工具在一段时间不活动后停止工作，请运行 `/chrome` 并选择"重新连接扩展程序"。

<h3 id="windows-specific-issues">
  Windows 特定问题
</h3>

在 Windows 上，您可能会遇到：

* **命名管道冲突 (EADDRINUSE)**：如果另一个进程正在使用相同的命名管道，请重新启动 Claude Code。关闭任何可能使用 Chrome 的其他 Claude Code 会话。
* **本机消息传递主机错误**：如果本机消息传递主机在启动时崩溃，请尝试重新安装 Claude Code 以重新生成主机配置。
* **设置页面无法打开**：更新 Claude Code。在 v2.1.211 之前，提示您连接扩展程序的浏览器标签页在 Windows 上可能无法打开。

<h3 id="common-error-messages">
  常见错误消息
</h3>

这些是最常见的错误及其解决方法：

| 错误 | 原因 | 修复 |
| - | - | - |
| "浏览器扩展程序未连接" | 本机消息传递主机无法到达扩展程序，或您的组织的 IP 允许列表拒绝了到 `bridge.claudeusercontent.com` 的连接 | 重新启动 Chrome 和 Claude Code，然后运行 `/chrome` 以重新连接。如果您的组织使用 IP 允许列表且错误仍然存在，请参阅[组织 IP 允许列表和代理出口](/docs/zh-CN/network-config#organization-ip-allowlists-and-proxy-egress) |
| 扩展程序在 `/chrome` 中显示"未检测到" | Chrome 扩展程序未安装或已禁用 | 在 `chrome://extensions` 中安装或启用扩展程序 |
| "没有可用的标签页" | Claude 在标签页准备好之前尝试操作 | 要求 Claude 创建新标签页并重试 |
| "接收端不存在" | 扩展程序 service worker 进入空闲状态 | 运行 `/chrome` 并选择"重新连接扩展程序" |

<h2 id="see-also">
  另请参阅
</h2>

* [计算机使用](/docs/zh-CN/computer-use)：当任务无法在浏览器中完成时控制本机 macOS 应用
* [在 VS Code 中使用 Claude Code](/docs/zh-CN/vs-code#automate-browser-tasks-with-chrome)：VS Code 扩展程序中的浏览器自动化
* [CLI 参考](/docs/zh-CN/cli-reference)：命令行标志，包括 `--chrome`
* [常见工作流](/docs/zh-CN/common-workflows)：更多使用 Claude Code 的方式
* [数据和隐私](/docs/zh-CN/data-usage)：Claude Code 如何处理您的数据
* [Claude in Chrome 入门](https://support.claude.com/en/articles/12012173-getting-started-with-claude-in-chrome)：Chrome 扩展程序的完整文档，包括快捷键、计划和权限
