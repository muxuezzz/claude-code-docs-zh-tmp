> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 第 34 周 · 2026 年 8 月 17–21 日

> 使用 /design skill 草拟可编辑的 UI 画板，设置 Concise 输出样式，并从手机在您的机器上启动 Claude Code 会话。

<div className="digest-meta">
  <span>发布版本 <a href="/docs/en/changelog#2-1-234">v2.1.234 → v2.1.239</a></span>
  <span>3 项功能 · 8 月 17–21</span>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">/design</span>
    <span className="digest-feature-pill">research preview</span>
  </div>

  <p className="digest-feature-lede"><code>/design</code> skill 将 Claude Design 的画板工作流程引入 CLI 和 Claude Code Desktop，基于 artifacts 构建。使用简要说明运行它，Claude 会发布一个可编辑画板的画布供您的 UI 使用。选择一个，调整它，然后让 Claude 实现它。适用于 Pro、Max、Team 和 Enterprise。需要 v2.1.234 或更高版本。</p>

  <Frame>
    <video autoPlay muted loop playsInline className="w-full" src="https://mintcdn.com/claude-code/2SnAdpL4dJ18nKb3/images/whats-new/design-skill.mp4?fit=max&auto=format&n=2SnAdpL4dJ18nKb3&q=85&s=0b376a94227c14a4204af89c4c9fd7ac" data-path="images/whats-new/design-skill.mp4" />
  </Frame>

  <p className="digest-feature-try">描述您想要设计的内容，让 Claude 草拟选项：</p>

  ```text Claude Code theme={null}
  > /design redesign the composer based on what people actually use it for
  ```

  <p className="digest-feature-try">Claude 打印已发布画布的链接。打开它，选择一个画板，并告诉 Claude 要实现哪个选项。</p>

  <a className="digest-feature-link" href="/docs/zh-CN/artifacts#availability">artifacts 可用的位置</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">Concise 输出样式</span>
    <span className="digest-feature-pill">v2.1.237</span>
  </div>

  <p className="digest-feature-lede">Concise 是一种新的内置输出样式。Claude 以结果开头，跳过前言和叙述，同时以与默认样式相同的彻底程度完成工作。当您要求解释或更多详细信息时，Claude 会完整回答。错误报告、安全警告和破坏性操作的确认保持其完整内容。</p>

  <Frame>
    <video autoPlay muted loop playsInline className="w-full" src="https://mintcdn.com/claude-code/2SnAdpL4dJ18nKb3/images/whats-new/concise-output-style.mp4?fit=max&auto=format&n=2SnAdpL4dJ18nKb3&q=85&s=dfb40ec8921ed1bc82eb629042a8ec17" data-path="images/whats-new/concise-output-style.mp4" />
  </Frame>

  <p className="digest-feature-try">在 <code>/config</code> 中的 <strong>Output style</strong> 下打开它，或在您的设置文件中设置它：</p>

  ```json ~/.claude/settings.json {2} theme={null}
  {
    "outputStyle": "Concise"
  }
  ```

  <p className="digest-feature-try">运行 <code>/clear</code> 或启动新会话，Claude 的回复以结果开头。</p>

  <a className="digest-feature-link" href="/docs/zh-CN/output-styles#built-in-output-styles">内置输出样式</a>
</div>

<div className="digest-feature">
  <div className="digest-feature-header">
    <span className="digest-feature-title">从手机在您的机器上启动会话</span>
    <span className="digest-feature-pill">mobile</span>
  </div>

  <p className="digest-feature-lede">任何运行 <code>claude remote-control</code> 的机器现在都会在 Claude 应用的 Code 标签页顶部显示为设备卡片。Remote Control 也已退出研究预览。</p>

  <Frame>
    <img className="w-full" src="https://mintcdn.com/claude-code/2SnAdpL4dJ18nKb3/images/whats-new/remote-control-phone-start.jpg?fit=max&auto=format&n=2SnAdpL4dJ18nKb3&q=85&s=9f0ebedab23aa0e1732cc37782573907" alt="Claude 移动应用中的 Code 标签页，其中 Devices 部分显示连接的 MacBook 作为设备卡片，位于会话列表上方" width="1206" height="895" data-path="images/whats-new/remote-control-phone-start.jpg" />
  </Frame>

  <p className="digest-feature-try">在您想要访问的机器上启动 Remote Control，然后在手机上打开 Code 标签页：</p>

  ```bash terminal theme={null}
  claude remote-control
  ```

  <p className="digest-feature-try">您的机器显示为 Code 标签页顶部的设备卡片。点击它以选择目录并在那里启动会话。</p>

  <a className="digest-feature-link" href="/docs/zh-CN/remote-control#start-a-remote-control-session">启动 Remote Control 会话</a>
</div>

<div className="digest-wins">
  <p className="digest-wins-title">其他改进</p>

  <div className="digest-wins-grid">
    <div>Claude Code 现在在 claude.ai 使用限制重置时自动继续您的会话；从 <code>/config</code> 中的 <strong>Continue automatically at usage limit</strong> 行关闭它</div>
    <div>可选的 <a href="/docs/zh-CN/interactive-mode#check-spelling-as-you-type"><code>spellcheck</code> 设置</a>在您键入时在提示输入中为拼写错误的单词加下划线，使用您安装的 <code>aspell</code>、<code>hunspell</code> 或 <code>ispell</code></div>
    <div>在具有开放 GitLab 合并请求的分支上，使用通过 <code>glab auth login</code> 进行身份验证的 <code>glab</code> CLI，页脚显示一个 <a href="/docs/zh-CN/interactive-mode#gitlab-merge-requests"><code>MR !N</code> 徽章</a>，其颜色取决于合并请求是草稿、开放还是可合并</div>
    <div>从手机或 claude.ai/code 更改工作量级别，它 <a href="/docs/zh-CN/remote-control#what-connected-devices-see">应用于您机器上的会话</a>；由 Desktop 或 VS Code 托管的 Remote Control 会话也向连接的设备显示会话的当前权限模式</div>
    <div>您可以在 Claude 工作时打开 <a href="/docs/zh-CN/permissions#manage-permissions"><code>/permissions</code></a> 或运行 <code>/add-dir \<path></code>；权限规则更改适用于当前轮次的其余部分</div>
    <div>当后台任务使 <a href="/docs/zh-CN/goal#background-work-defers-evaluation"><code>/goal</code></a> 等待时，Claude 在 30 分钟后检查它们，而不是无限期等待，并继续检查，在会话空闲时以更长的间隔检查；设置 <code>CLAUDE\_CODE\_GOAL\_CHECKIN\_MINUTES=0</code> 以选择退出</div>
    <div>您自己的提示现在在成绩单中呈现 markdown，具有突出显示的代码块、内联代码和列表，与回复的方式相同</div>
    <div>新的 <a href="/docs/zh-CN/model-config#set-a-default-model-for-new-sessions"><code>ANTHROPIC\_DEFAULT\_MODEL</code></a> 环境变量设置新会话启动的模型；<code>/model</code> 选择仍会覆盖它并在重启后保持</div>
    <div>使用 <code>SendMessage</code> 上的 <code>notify\_when\_idle</code> 输入，Claude 可以要求同一机器上的另一个 Claude Code 会话 <a href="/docs/zh-CN/cross-session-messaging#get-a-notice-when-another-session-goes-idle">在它下次空闲时发送一个通知</a></div>
    <div>将 <a href="/docs/zh-CN/interactive-mode#make-ctrl-w-delete-back-to-whitespace"><code>keybindingFlavor</code></a> 设置为 <code>"readline"</code>，使提示中的 <code>Ctrl+W</code> 删除回到前一个空格，如 Bash 所做的那样，而不是在标点符号（如 <code>/</code>）处停止</div>
    <div>在本机 Windows 上，您的 Claude Code 会话现在可以 <a href="/docs/zh-CN/cross-session-messaging#availability">相互消息</a>，使用 <code>SendMessage</code> 并使用 <code>ListAgents</code> 找到彼此，如在 macOS 和 Linux 上一样</div>
    <div>自托管运行器接受 `--defer-shutdown-max-min`，它 <a href="/docs/zh-CN/self-hosted-environments-deploy#defer-the-drain-past-the-first-signal">在 SIGTERM 后的设定分钟数内继续为附加会话提供服务</a></div>
    <div>自托管运行器接受 `--proxy-authorization-command` 或 `--proxy-authorization-file` 为 <a href="/docs/zh-CN/self-hosted-environments-deploy#authenticate-to-an-egress-proxy">需要一个的出口代理提供新的 `Proxy-Authorization` 标头</a></div>
  </div>
</div>

[v2.1.234–v2.1.239 的完整更新日志 →](/docs/en/changelog#2-1-234)
