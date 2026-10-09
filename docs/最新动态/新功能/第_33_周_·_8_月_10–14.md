> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 第 33 周 · 2026 年 8 月 10–14 日

> Claude Code Desktop 在使用限制重置后自动继续，fork 模式默认启用，GitLab 合并请求和市场加入 GitHub。

<div className="digest-meta">
  <span>发布版本 <a href="/docs/en/changelog#2-1-225">v2.1.225 → v2.1.233</a></span>
  <span>3 项功能 · 8 月 10–14</span>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Desktop 上限制重置后自动继续</span>
    <span className="digest-feature-pill">Desktop</span>
  </div>

  <p className="digest-feature-lede">当您在 Claude Code Desktop 的 Code 选项卡中达到会话限制时，限制卡现在提供一个<strong>限制重置时自动继续</strong>复选框。勾选它，Desktop 应用将在重置后重试中断的轮次。该卡显示重试时间。每周限制卡不提供此选项。</p>

  <Frame>
    <video autoPlay muted loop playsInline className="w-full" src="https://mintcdn.com/claude-code/2SnAdpL4dJ18nKb3/images/whats-new/desktop-auto-continue.mp4?fit=max&auto=format&n=2SnAdpL4dJ18nKb3&q=85&s=1937f489695feaea715e48ecfd7e62cd" data-path="images/whats-new/desktop-auto-continue.mp4" />
  </Frame>

  <p className="digest-feature-try">下次出现会话限制卡时，勾选<strong>限制重置时自动继续</strong>并保持会话打开。该卡显示 <code>Auto-resuming at</code> 后跟重置时间，一旦限制重置，轮次将自动继续。</p>

  <a className="digest-feature-link" href="/docs/zh-CN/errors#youve-hit-your-session-limit">达到使用限制时该怎么办</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Fork 模式默认启用</span>
    <span className="digest-feature-pill">v2.1.232</span>
  </div>

  <p className="digest-feature-lede">Fork 模式现在在交互式会话中默认启用。Claude 可以请求 <code>fork</code> 子代理类型，它继承完整的对话和提示缓存，而不是从头开始，因此您不必为辅助任务重新解释上下文。子代理 Claude 在交互式会话中生成的，除了代理团队队友生成的，也默认在后台运行。</p>

  <p className="digest-feature-try">使用需要您迄今为止讨论的所有内容的任务自己启动 fork：</p>

  ```text Claude Code theme={null}
  > /subtask draft unit tests for the parser changes so far
  ```

  <p className="digest-feature-try">fork 出现在您的提示下方的面板中，其结果在完成时到达您的对话。要关闭 fork 模式，请设置 <code>CLAUDE\_CODE\_FORK\_SUBAGENT=0</code>。</p>

  <a className="digest-feature-link" href="/docs/zh-CN/sub-agents#turn-fork-mode-on-or-off">启用或关闭 fork 模式</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">GitLab 合并请求和市场</span>
    <span className="digest-feature-pill">v2.1.232</span>
  </div>

  <p className="digest-feature-lede">插件市场克隆裸 <code>gitlab.com</code> URL，包括嵌套子组。在 v2.1.233 或更高版本上，将 GitLab 合并请求 URL 传递给 <code>--worktree</code> 以从其分支，<code>claude agents</code> 视图将链接到合并请求的会话标记为 <code>!N</code>。Claude Code 还会编辑 GitLab 令牌族，如 <code>glpat-</code> 和 <code>glrt-</code>，并以与保护 <code>gh</code> 相同的方式保护 <code>glab</code> CLI 的配置存储。</p>

  <p className="digest-feature-try">在从合并请求分支的 worktree 中启动会话：</p>

  ```bash terminal theme={null}
  claude --worktree https://gitlab.com/group/project/-/merge_requests/42
  ```

  <p className="digest-feature-try">当 <code>origin</code> 在 gitlab.com 上时，Claude Code 获取 <code>merge-requests/42/head</code> 并在其自己的 worktree 中的该分支上打开会话。</p>

  <a className="digest-feature-link" href="/docs/zh-CN/worktrees#branch-from-a-pull-request">从拉取或合并请求分支 worktree</a>
</div>

<div className="digest-wins">
  <p className="digest-wins-title">其他改进</p>

  <div className="digest-wins-grid">
    <div>在提示中键入 <code>@</code> 以<a href="/docs/zh-CN/cross-session-messaging#message-another-session">提及另一个 Claude 会话</a>的名称，Claude 使用 <code>SendMessage</code> 直接向其发送消息；与恰好一个活跃会话完全匹配的裸名称现在无需确认步骤即可传递</div>
    <div>一台机器上的交互式会话保持<a href="/docs/zh-CN/cross-session-messaging#see-which-sessions-claude-can-reach">唯一名称</a>：如果您启动或重命名会话时使用另一个活跃会话已在使用的名称，Claude Code 会为您的会话提供 <code>name-word-word</code> 变体并告知您</div>
    <div>插件市场接受<a href="/docs/zh-CN/plugins/marketplace-reference#command-plugin-source"><code>command</code> 源</a>：本地命令打印插件目录，Claude Code 在每个会话中重新解析并应用，无需重启</div>
    <div>在 Linux 和 WSL 上，设置<a href="/docs/zh-CN/tools-reference#memory-limit-on-linux-and-wsl"><code>CLAUDE\_CODE\_TOOL\_MEMORY\_LIMIT</code></a> 为大小（如 <code>4G</code>）以限制 Bash 和 PowerShell 工具命令可以使用的内存</div>
    <div>任务跟踪工具，如 <code>TaskCreate</code>、<code>TaskUpdate</code> 和 <code>TodoWrite</code>，<a href="/docs/zh-CN/tools-reference#task-tool-availability">在 Opus 4.8、Sonnet 5、Fable 5、Mythos 5 及这些系列中的更高版本上不再可用</a>；设置 <code>CLAUDE\_CODE\_ENABLE\_TODO\_TOOLS=1</code> 以重新启用它们</div>
    <div><a href="/docs/zh-CN/code-review#review-a-diff-locally"><code>/code-review</code></a> 在高、超高和最大努力级别现在像其他级别一样在后台代理中运行</div>
    <div><a href="/docs/zh-CN/plugins/install#install-a-plugin"><code>/plugin install plugin\@marketplace</code></a> 首先刷新市场，因此新发布的插件无需手动市场更新即可安装</div>
    <div>设置接受<a href="/docs/zh-CN/settings-reference#marketplace-key-aliases"><code>additionalMarketplaces</code> 和 <code>allowedMarketplaces</code></a> 作为 <code>extraKnownMarketplaces</code> 和 <code>strictKnownMarketplaces</code> 的别名</div>
    <div>在较新的模型上，Claude 可以<a href="/docs/zh-CN/tools-reference#write-tool-behavior">使用 Write 工具覆盖现有文件</a>而无需在此会话中首先读取它，与 Edit 工具的规则匹配；较旧的模型需要读取</div>
    <div>VS Code 扩展可以<a href="/docs/zh-CN/vs-code#organize-sessions-into-groups">将会话列表组织成组</a>：右键单击以创建、重命名或删除组，使用 Cmd/Ctrl- 或 Shift-单击一次移动多个会话</div>
    <div>如果您的组织通过<a href="/docs/zh-CN/claude-apps-gateway-spend-limits">具有支出限制的 Claude 应用网关</a>路由 Claude Code，Claude Code 会在您达到限制时显示限制期间、其重置时间和运营商的消息</div>
  </div>
</div>

[v2.1.225–v2.1.233 的完整更新日志 →](/docs/en/changelog#2-1-225)
