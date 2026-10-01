> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 第 32 周 · 2026 年 8 月 3–7 日

> Claude Code 会话可以相互发送消息，自托管环境在您的基础设施上运行云会话，自动模式成为默认权限模式。

<div className="digest-meta">
  <span>发布版本 <a href="/docs/en/changelog#2-1-220">v2.1.220 → v2.1.224</a></span>
  <span>3 项功能 · 8 月 3–7 日</span>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">跨会话消息传递</span>
    <span className="digest-feature-pill">v2.1.224</span>
  </div>

  <p className="digest-feature-lede">您的 Claude Code 会话现在可以相互发送消息。Claude 使用 <code>ListAgents</code> 工具发现您的其他会话，并使用 <code>SendMessage</code> 发送消息，可以在您要求时发送，也可以自动发送，例如在一个会话中的更改影响另一个会话的工作后。消息是 Claude 为另一个会话编写的文本，永远不会是您的对话历史或文件。在 macOS 和 Linux 上可用。需要 v2.1.224 或更高版本。</p>

  <Frame>
    <video autoPlay muted loop playsInline className="w-full" src="https://mintcdn.com/claude-code/N3yEaTYPXMXFrF6k/images/whats-new/cross-session-messaging.mp4?fit=max&auto=format&n=N3yEaTYPXMXFrF6k&q=85&s=8f33c3390f78660a4a26dc980f46159f" data-path="images/whats-new/cross-session-messaging.mp4" />
  </Frame>

  <p className="digest-feature-try">在同一台机器上打开两个会话，要求其中一个会话传递一些内容：</p>

  ```text title="Claude Code" wrap theme={null}
  告诉处理支付 API 的会话 users.name 现在是 users.display_name
  ```

  <p className="digest-feature-try">一旦 Claude 读取了消息，另一个会话会显示一个 <code>Message from</code> 行；按 <code>Ctrl+O</code> 展开它。要查看 Claude 可以访问哪些会话，请运行 <code>/list-agents</code>。</p>

  <a className="digest-feature-link" href="/docs/zh-CN/cross-session-messaging#message-another-session">向另一个会话发送消息</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">自托管环境</span>
    <span className="digest-feature-pill">v2.1.224</span>
  </div>

  <p className="digest-feature-lede">自托管环境在您组织自己的基础设施上运行 Claude Code 云会话，在 Team 和 Enterprise 计划上处于公开测试阶段。在您的机器或容器上运行 <code>claude self-hosted-runner</code> 将它们转变为运行器。当有人在从 claude.ai、移动或桌面应用程序或 `claude --cloud` 启动会话时选择您的环境时，该会话在您的网络内运行，可以访问您的内部服务。所有者首先在 <a href="https://claude.ai/admin-settings/cloud-environments">管理设置</a> 中打开 <strong>允许自托管环境</strong>。</p>

  <Frame>
    <img className="w-full" src="https://mintcdn.com/claude-code/N3yEaTYPXMXFrF6k/images/whats-new/self-hosted-environments.jpg?fit=max&auto=format&n=N3yEaTYPXMXFrF6k&q=85&s=ae9152cb1670c8af517d1aee57689b14" alt="自托管环境管理页面，列出了 linux-dev 和 macos-prod 等环境及其状态和活跃会话计数" width="2048" height="1152" data-path="images/whats-new/self-hosted-environments.jpg" />
  </Frame>

  <p className="digest-feature-try">以所有者身份登录，运行引导式设置，它将引导您创建环境并启动运行器：</p>

  ```bash terminal theme={null}
  claude self-hosted-runner setup
  ```

  <p className="digest-feature-try">运行器注册后，该环境在管理设置中显示 <strong>健康</strong>。</p>

  <a className="digest-feature-link" href="/docs/zh-CN/self-hosted-environments-quickstart#set-up-an-environment-and-runner">自托管环境快速入门</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">自动模式成为默认值</span>
    <span className="digest-feature-pill">CLI</span>
  </div>

  <p className="digest-feature-lede">从 8 月 14 日开始，自动模式是 Pro、Max 和 Team 计划上新会话的默认权限模式。如果您自己设置了默认模式，它将保持不变，除非您接受一次性切换提示，而您的组织管理的默认值不会改变。您仍然可以随时切换模式。已在这些计划上生效：自动模式进行的分类器调用不再计入您的使用限制。</p>

  <p className="digest-feature-try">在切换前以自动模式启动每个会话，请在您的用户设置中将其设置为默认值：</p>

  ```json ~/.claude/settings.json {3} theme={null}
  {
    "permissions": {
      "defaultMode": "auto"
    }
  }
  ```

  <p className="digest-feature-try">新会话随后在状态栏中显示 <code>auto mode on</code>。</p>

  <a className="digest-feature-link" href="/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode">自动模式要求和控制</a>
</div>

<div className="digest-wins">
  <p className="digest-wins-title">其他改进</p>

  <div className="digest-wins-grid">
    <div>VS Code 扩展获得 <a href="/docs/zh-CN/vs-code#extension-settings">焦点视图</a>，它在每个轮次后面隐藏一个可展开行中的工具活动；从命令菜单或使用 <code>Ctrl+Alt+F</code>（Mac 上为 <code>Ctrl+Option+F</code>）切换它</div>
    <div>沙箱凭证文件在 Linux 和 WSL2 上接受 <a href="/docs/zh-CN/sandboxing#mask-credential-files"><code>mode: "mask"</code></a>，因此沙箱命令读取哨兵副本，而沙箱代理在出口时替换真实值；凭证掩蔽还获得 <code>extract</code>、JWT 感知的 <code>decode</code> 和 AWS SigV4 重新签名选项</div>
    <div>市场可以使用新的 <code>archive</code> 源将插件分发为 <a href="/docs/zh-CN/plugins/marketplace-reference#archive-plugin-source">zip 存档</a>，通过 HTTPS 下载，带有可选的 SHA-256 引脚，因此安装无需 git 或 npm</div>
    <div><code>/review</code> 现在是 <a href="/docs/zh-CN/code-review#review-a-diff-locally"><code>/code-review</code></a> 的别名，<code>/code-review</code> 不带努力级别会重用您上次输入的级别</div>
    <div>您使用 <a href="/docs/zh-CN/agent-view#copy-the-session-with-%2Ffork"><code>/fork</code></a> 复制的会话现在在其自己的 worktree 中进行代码更改，而不是原始会话的检出</div>
    <div>您从 <a href="/docs/zh-CN/plugins/install#install-a-plugin"><code>/plugin</code></a> 安装的插件在当前会话中激活，当这样做是安全的时；安装摘要报告 <code>Plugin is now active.</code> 或告诉您运行 <code>/reload-plugins</code></div>
    <div><a href="/docs/zh-CN/agent-view#how-file-edits-are-isolated">后台会话</a> 在 worktree 中更改代码现在在完成前提交和推送，仅当任务需要时才打开草稿拉取请求，并遵循您的 <code>CLAUDE.md</code> 中的 git 指令</div>
    <div>每个会话 200 个子代理的上限被移除，因此长时间运行的会话不再拒绝新的子代理；<a href="/docs/zh-CN/sub-agents#concurrent-subagent-limit">并发</a> 和深度限制仍然适用</div>
    <div>存储库的签入设置不再能打开 <a href="/docs/zh-CN/remote-control#enable-remote-control-for-all-sessions">远程控制自动连接</a>；改为在您的用户或托管设置中设置 <code>remoteControlAtStartup</code>，项目和本地设置只能将其关闭</div>
    <div><a href="/docs/zh-CN/worktrees#how-claude-code-enforces-isolation">Worktree 隔离</a> 现在不仅阻止文件编辑，还阻止 Bash 命令和 git 重定向到达主检出，在每种会话类型和会话的子代理中</div>
    <div>Bash 命令不再能从权限检查中隐藏其自身的一部分，制表符或不可见的 Unicode 填充不再从批准对话框中隐藏命令的一部分</div>
    <div>PreToolUse 自动允许钩子不再绕过 Claude Code 内部侧任务（如摘要和压缩）中的工具限制</div>
    <div><a href="/docs/zh-CN/ultraplan">Ultraplan</a> 研究预览被移除，包括 <code>/ultraplan</code> 命令和 <code>ultraplan</code> 关键字；改为使用计划模式或网络上的 Claude Code</div>
  </div>
</div>

[v2.1.220–v2.1.224 的完整更新日志 →](/docs/en/changelog#2-1-220)
