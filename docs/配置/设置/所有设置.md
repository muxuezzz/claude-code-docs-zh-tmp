> ## Documentation Index
> Fetch the complete documentation index at: https://code.claude.com/docs/llms.txt
> Use this file to discover all available pages before exploring further.

# 所有设置

> Claude Code settings.json 的完整参考：每个键的位置、类型和默认值，以及可直接粘贴的示例，包含每个键的索引。

export const BackToIndex = ({href = '#all-settings', label = 'Back to index'}) => {
  const [show, setShow] = useState(false);
  useEffect(() => {
    const onScroll = () => setShow(window.scrollY > window.innerHeight);
    onScroll();
    window.addEventListener('scroll', onScroll, {
      passive: true
    });
    return () => window.removeEventListener('scroll', onScroll);
  }, []);
  return <div className="not-prose">
      <style>{`
        .bti-btn {
          position: fixed; right: 20px; bottom: 20px; z-index: 40;
          display: inline-flex; align-items: center; gap: 6px;
          padding: 8px 12px; border-radius: 999px;
          font-size: 13px; font-weight: 500; line-height: 1; text-decoration: none;
          color: #1f1f1f; background: #ffffff; border: 1px solid #d9d9d9;
          box-shadow: 0 2px 8px rgba(0,0,0,0.12);
          opacity: 0; pointer-events: none; transform: translateY(6px);
          transition: opacity 160ms ease, transform 160ms ease;
        }
        .bti-btn.bti-show { opacity: 1; pointer-events: auto; transform: translateY(0); }
        .bti-btn:hover { border-color: #b3b3b3; }
        .dark .bti-btn { color: #ececec; background: #1e1e1e; border-color: #3a3a3a; box-shadow: 0 2px 8px rgba(0,0,0,0.5); }
        .dark .bti-btn:hover { border-color: #5a5a5a; }
        @media (max-width: 1279px) { .bti-btn { bottom: 112px; } }
        @media print { .bti-btn { display: none; } }
      `}</style>
      <a className={'bti-btn' + (show ? ' bti-show' : '')} href={href} aria-hidden={!show} tabIndex={show ? 0 : -1}>
        <svg width="12" height="12" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true"><path d="M8 13V3M3.5 7.5 8 3l4.5 4.5" /></svg>
        {label}
      </a>
    </div>;
};

export const ReferenceFilter = ({placeholder, noun, facets, facetOrder, columnHelp, children}) => {
  const useLive = init => {
    const [v, setV] = useState(init);
    const ref = useRef(init);
    return [v, ref, x => {
      ref.current = x;
      setV(x);
    }];
  };
  const cap = s => s.charAt(0).toUpperCase() + s.slice(1);
  const plural = s => s.endsWith('y') ? s.slice(0, -1) + 'ies' : s + 's';
  const facetNames = facets || ['category', 'topic', 'scope', 'where'];
  const orderOf = {};
  Object.keys(facetOrder || ({})).forEach(k => {
    orderOf[k] = facetOrder[k].map(x => String(x).toLowerCase());
  });
  const rankIn = (col, v) => {
    const list = orderOf[col];
    if (!list) return -1;
    const i = list.indexOf(String(v).toLowerCase());
    return i < 0 ? list.length : i;
  };
  const cmpValues = col => (a, b) => {
    const ra = rankIn(col, a);
    const rb = rankIn(col, b);
    if (ra !== rb) return ra - rb;
    return a < b ? -1 : a > b ? 1 : 0;
  };
  const help = columnHelp || ({});
  const FIRST_COL_HELP = 'Click an entry to open it.';
  const optionLabel = (f, c) => c === 'All' ? 'All ' + plural(f.label.toLowerCase()) : c;
  const nounText = noun || 'entries';
  const placeholderText = placeholder || 'Filter this reference';
  const rootRef = useRef(null);
  const tablesRef = useRef(null);
  const searchRef = useRef(null);
  const menuRef = useRef({});
  const [q, qRef, setQ] = useLive('');
  const [sel, selRef, setSel] = useLive({});
  const [sortBy, sortRef, setSortBy] = useLive(null);
  const [menuOpen, menuOpenRef, setMenu] = useLive(null);
  const [facetList, setFacetList] = useState([]);
  const [firstHead, setFirstHead] = useState('');
  const [counts, setCounts] = useState({
    shown: 0,
    total: 0
  });
  const [disabled, setDisabled] = useState(false);
  const menuBtn = name => menuRef.current[name] ? menuRef.current[name].querySelector(':scope > button') : null;
  const menuList = name => menuRef.current[name] ? menuRef.current[name].querySelector('[role="listbox"]') : null;
  const closeMenu = name => {
    setMenu(null);
    const btn = menuBtn(name);
    if (btn) btn.focus();
  };
  const focusSelected = name => {
    const list = menuList(name);
    if (!list) return;
    const btn = list.querySelector('button[aria-selected="true"]') || list.querySelector('button');
    if (btn) btn.focus();
  };
  const setFacet = (name, value) => {
    setSel(Object.assign({}, selRef.current, {
      [name]: value
    }));
    apply(qRef.current);
    closeMenu(name);
  };
  const sortTables = by => {
    (tablesRef.current || []).forEach(tab => {
      const t = tab.el;
      const idx = tab.heads.indexOf(by);
      const body = t.querySelector('tbody');
      if (idx < 0 || !body) return;
      const rows = [...body.querySelectorAll('tr')];
      const keyOf = r => r.children[idx] ? r.children[idx].textContent.trim().toLowerCase() : '';
      const cmp = cmpValues(by);
      rows.map((r, i) => ({
        r,
        i: Number(r.dataset.sfIndex !== undefined ? r.dataset.sfIndex : i),
        k: keyOf(r)
      })).sort((a, b) => cmp(a.k, b.k) || a.i - b.i).forEach(x => body.appendChild(x.r));
      [...t.querySelectorAll('thead th')].forEach((h, i) => {
        const sortable = tab.heads[i] === tab.heads[0] || facetNames.indexOf(tab.heads[i]) > -1;
        if (sortable) h.setAttribute('aria-sort', i === idx ? 'ascending' : 'none'); else h.removeAttribute('aria-sort');
      });
    });
  };
  const scan = () => {
    const tables = [];
    let el = rootRef.current ? rootRef.current.nextElementSibling : null;
    while (el) {
      if (el.tagName === 'H2' || el.querySelector(':scope > h2')) break;
      const found = el.tagName === 'TABLE' ? [el] : [...el.querySelectorAll('table')];
      found.forEach(t => {
        const headCells = [...t.querySelectorAll('thead th, thead td')];
        const heads = headCells.map(h => h.textContent.trim().toLowerCase());
        if (heads.length === 0) return;
        const facetIdx = {};
        heads.forEach((h, i) => {
          if (facetNames.indexOf(h) > -1) facetIdx[h] = i;
        });
        if (!t.dataset.sfDecorated) {
          t.dataset.sfDecorated = '1';
          headCells.forEach((h, i) => {
            const text = i === 0 ? help[heads[0]] || FIRST_COL_HELP : help[heads[i]];
            if (text) h.title = text;
          });
        }
        const rows = [...t.querySelectorAll('tbody tr')].map((r, i) => {
          if (r.dataset.sfIndex === undefined) r.dataset.sfIndex = String(i);
          const cells = r.querySelectorAll('td');
          const fv = {};
          Object.keys(facetIdx).forEach(h => {
            fv[h] = cells[facetIdx[h]] ? cells[facetIdx[h]].textContent.trim() : '';
          });
          return {
            el: r,
            text: [...cells].map(c => c.textContent).join(' ').toLowerCase(),
            facets: fv,
            anchors: [...r.querySelectorAll('a[href^="#"]')].map(a => a.getAttribute('href').slice(1)),
            ids: [...r.querySelectorAll('[id]')].map(n => n.id)
          };
        });
        tables.push({
          el: t,
          box: t.closest('[data-table-wrapper]') || t,
          rows,
          heads
        });
      });
      el = el.nextElementSibling;
    }
    tablesRef.current = tables;
    if (sortRef.current) sortTables(sortRef.current);
    return tables;
  };
  const apply = query => {
    let tables = tablesRef.current || scan();
    if (tables.some(t => !t.el.isConnected)) tables = scan();
    const needle = query.trim().toLowerCase();
    const sel = selRef.current;
    const activeFacets = Object.keys(sel).filter(h => sel[h] && sel[h] !== 'All');
    const show = (el, on) => {
      const want = on ? '' : 'none';
      if (el.style.display !== want) el.style.display = want;
    };
    let total = 0;
    let shown = 0;
    const visibleTargets = new Set();
    tables.forEach(t => {
      let tableVisible = 0;
      t.rows.forEach(row => {
        total += 1;
        const catOk = activeFacets.every(h => {
          const v = row.facets[h];
          return v === sel[h] || v === '' || v === undefined;
        });
        const match = catOk && (needle === '' || row.text.includes(needle));
        show(row.el, match);
        if (match) {
          tableVisible += 1;
          row.anchors.forEach(a => visibleTargets.add(a));
        }
      });
      show(t.box, !(t.rows.length > 0 && tableVisible === 0));
      shown += tableVisible;
    });
    if (shown < total && visibleTargets.size > 0) {
      tables.forEach(t => {
        t.rows.forEach(row => {
          if (row.el.style.display === 'none' && row.ids.some(id => visibleTargets.has(id))) {
            show(row.el, true);
            show(t.box, true);
            shown += 1;
          }
        });
      });
    }
    setCounts({
      shown,
      total
    });
    return total;
  };
  const deriveFacets = tables => {
    const seen = {};
    tables.forEach(t => t.rows.forEach(r => {
      Object.keys(r.facets).forEach(h => {
        if (!seen[h]) seen[h] = [];
        if (r.facets[h] && seen[h].indexOf(r.facets[h]) === -1) seen[h].push(r.facets[h]);
      });
    }));
    const list = facetNames.filter(h => seen[h] && seen[h].length > 0).map(h => ({
      name: h,
      label: cap(h),
      values: seen[h].sort(cmpValues(h))
    }));
    setFacetList(list);
    const first = tables[0] ? tables[0].heads[0] : '';
    setFirstHead(first);
    if (!sortRef.current && first) {
      setSortBy(first);
      sortTables(first);
    }
    const init = {};
    list.forEach(f => {
      init[f.name] = selRef.current[f.name] || 'All';
    });
    setSel(init);
  };
  const onChange = value => {
    setQ(value);
    apply(value);
  };
  const clearAll = () => {
    const next = {};
    Object.keys(selRef.current).forEach(k => {
      next[k] = 'All';
    });
    setSel(next);
    setQ('');
    apply('');
    if (searchRef.current) searchRef.current.focus();
  };
  useEffect(() => {
    const tables = scan();
    deriveFacets(tables);
    const total = apply('');
    let retryTimer;
    if (total === 0) {
      retryTimer = setTimeout(() => {
        tablesRef.current = null;
        if (apply(qRef.current) > 0) deriveFacets(tablesRef.current); else setDisabled(true);
      }, 500);
    }
    const onKey = e => {
      if (e.key === 'Escape' && menuOpenRef.current !== null) closeMenu(menuOpenRef.current);
      if (!searchRef.current) return;
      if (e.metaKey || e.ctrlKey || e.altKey) return;
      const active = document.activeElement;
      const tag = active && active.tagName;
      const editable = active && active.isContentEditable;
      const interactive = tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'SELECT' || tag === 'BUTTON' || tag === 'A' || editable || active && active.getAttribute && active.getAttribute('role');
      if (e.key === '/' && !interactive) {
        const r = rootRef.current ? rootRef.current.getBoundingClientRect() : null;
        if (r && r.bottom > 0 && r.top < (window.innerHeight || 0)) {
          e.preventDefault();
          setMenu(null);
          searchRef.current.focus();
        }
      }
      if (e.key === 'Escape' && menuOpenRef.current === null && active === searchRef.current) {
        onChange('');
        searchRef.current.blur();
      }
    };
    const onDocClick = e => {
      const open = menuOpenRef.current;
      if (open !== null && menuRef.current[open] && !menuRef.current[open].contains(e.target)) setMenu(null);
    };
    window.addEventListener('keydown', onKey);
    document.addEventListener('mousedown', onDocClick);
    return () => {
      if (retryTimer) clearTimeout(retryTimer);
      window.removeEventListener('keydown', onKey);
      document.removeEventListener('mousedown', onDocClick);
      (tablesRef.current || []).forEach(t => {
        t.box.style.display = '';
        t.rows.forEach(row => {
          row.el.style.display = '';
        });
      });
    };
  }, []);
  useEffect(() => {
    if (menuOpen !== null) focusSelected(menuOpen);
  }, [menuOpen]);
  if (disabled) return null;
  const facetActive = Object.keys(sel).some(h => sel[h] && sel[h] !== 'All');
  const sortOptions = [firstHead].concat(facetList.map(f => f.name)).filter((h, i, a) => h && a.indexOf(h) === i);
  return <>
      <style>{`
        .sf-root {
          --sf-accent: #D97757;
          --sf-bg: #fff;
          --sf-border: #E8E6DC;
          --sf-text: #141413;
          --sf-text-3: #73726C;
          --sf-text-4: #9C9A92;
        }
        .dark .sf-root {
          --sf-bg: #1a1918;
          --sf-border: #3a3936;
          --sf-text: #e8e6dc;
          --sf-text-3: #9c9a92;
          --sf-text-4: #73726c;
        }
        .sf-root .sf-end {
          position: absolute;
          right: 10px;
          top: 50%;
          transform: translateY(-50%);
        }
        .sf-root .sf-x {
          background: none;
          border: none;
          cursor: pointer;
          color: var(--sf-text-3);
          font-size: 14px;
          padding: 2px 4px;
          line-height: 1;
        }
      `}</style>
      <div ref={rootRef} className="sf-root" style={{
    margin: '16px 0 8px'
  }}>
        <div style={{
    display: 'flex',
    gap: '8px',
    flexWrap: 'wrap',
    alignItems: 'center'
  }}>
        <div style={{
    position: 'relative',
    flex: '1 1 260px',
    maxWidth: '480px'
  }}>
          <input ref={searchRef} value={q} onChange={e => onChange(e.target.value)} placeholder={placeholderText} aria-label={placeholderText} style={{
    width: '100%',
    padding: '8px 56px 8px 12px',
    borderRadius: '8px',
    border: '1px solid var(--sf-border)',
    background: 'var(--sf-bg)',
    color: 'var(--sf-text)',
    fontSize: '14px',
    outline: 'none',
    boxSizing: 'border-box'
  }} />
          {q ? <button type="button" onClick={() => {
    onChange('');
    if (searchRef.current) searchRef.current.focus();
  }} aria-label="Clear text" className="sf-end sf-x">
              ×
            </button> : <span className="sf-end" style={{
    fontFamily: 'var(--font-mono, ui-monospace, monospace)',
    fontSize: '11px',
    color: 'var(--sf-text-4)',
    border: '1px solid var(--sf-border)',
    borderRadius: '3px',
    padding: '0 5px',
    pointerEvents: 'none'
  }}>
              /
            </span>}
        </div>
        {facetList.map(f => {
    const cur = sel[f.name] || 'All';
    const isOpen = menuOpen === f.name;
    return <div key={f.name} ref={el => {
      menuRef.current[f.name] = el;
    }} style={{
      position: 'relative'
    }}>
            <button type="button" onClick={() => setMenu(isOpen ? null : f.name)} onKeyDown={e => {
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        if (!isOpen) setMenu(f.name); else focusSelected(f.name);
      }
    }} aria-haspopup="listbox" aria-expanded={isOpen} style={{
      display: 'flex',
      alignItems: 'center',
      gap: '8px',
      padding: cur !== 'All' ? '8px 30px 8px 12px' : '8px 12px',
      borderRadius: '8px',
      border: '1px solid ' + (cur !== 'All' ? 'var(--sf-accent)' : 'var(--sf-border)'),
      background: 'var(--sf-bg)',
      color: cur === 'All' ? 'var(--sf-text-3)' : 'var(--sf-text)',
      fontSize: '13.5px',
      cursor: 'pointer',
      whiteSpace: 'nowrap',
      maxWidth: '260px'
    }}>
              <span style={{
      overflow: 'hidden',
      textOverflow: 'ellipsis'
    }}>
                {f.label + ': ' + optionLabel(f, cur)}
              </span>
              <span aria-hidden="true" style={{
      fontSize: '9px',
      color: 'var(--sf-text-4)',
      transform: isOpen ? 'rotate(180deg)' : 'none',
      transition: 'transform 120ms'
    }}>
                ▼
              </span>
            </button>
            {cur !== 'All' && <button type="button" onClick={() => setFacet(f.name, 'All')} aria-label={'Clear ' + f.label + ' filter'} title={'Clear ' + f.label + ' filter'} className="sf-end sf-x">
                ×
              </button>}
            {isOpen && <div role="listbox" aria-label={f.label} onKeyDown={e => {
      const items = [...e.currentTarget.querySelectorAll('button')];
      const idx = items.indexOf(document.activeElement);
      if (e.key === 'ArrowDown') {
        e.preventDefault();
        (items[idx + 1] || items[0]).focus();
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        (items[idx - 1] || items[items.length - 1]).focus();
      } else if (e.key === 'Home') {
        e.preventDefault();
        if (items[0]) items[0].focus();
      } else if (e.key === 'End') {
        e.preventDefault();
        if (items[items.length - 1]) items[items.length - 1].focus();
      } else if (e.key === 'Tab') {
        closeMenu(f.name);
      }
    }} style={{
      position: 'absolute',
      top: 'calc(100% + 6px)',
      left: 0,
      zIndex: 1000,
      minWidth: '260px',
      maxHeight: '340px',
      overflowY: 'auto',
      background: 'var(--sf-bg)',
      border: '1px solid var(--sf-border)',
      borderRadius: '10px',
      boxShadow: '0 8px 24px rgba(0,0,0,0.12)',
      padding: '5px'
    }}>
                {['All'].concat(f.values).map(c => {
      const selected = cur === c;
      return <button key={c} role="option" aria-selected={selected} tabIndex={-1} onClick={() => setFacet(f.name, c)} style={{
        display: 'flex',
        alignItems: 'center',
        gap: '8px',
        width: '100%',
        textAlign: 'left',
        padding: '7px 10px',
        borderRadius: '6px',
        border: 'none',
        background: 'transparent',
        color: selected ? 'var(--sf-accent)' : 'var(--sf-text)',
        fontWeight: selected ? 600 : 400,
        fontSize: '13.5px',
        cursor: 'pointer'
      }}>
                      <span aria-hidden="true" style={{
        width: '14px',
        color: 'var(--sf-accent)',
        flexShrink: 0
      }}>
                        {selected ? '✓' : ''}
                      </span>
                      {optionLabel(f, c)}
                    </button>;
    })}
              </div>}
          </div>;
  })}
        {sortOptions.length > 1 && <div role="group" aria-label="Sort by" style={{
    display: 'flex',
    alignItems: 'center',
    gap: '4px',
    fontSize: '13px',
    color: 'var(--sf-text-3)',
    whiteSpace: 'nowrap'
  }}>
            <span style={{
    marginRight: '4px'
  }}>Sort by</span>
            {sortOptions.map(o => {
    const on = sortBy === o;
    return <button key={o} type="button" aria-pressed={on} onClick={() => {
      setSortBy(o);
      sortTables(o);
    }} style={{
      padding: '6px 10px',
      borderRadius: '8px',
      border: '1px solid ' + (on ? 'var(--sf-accent)' : 'var(--sf-border)'),
      background: 'var(--sf-bg)',
      color: on ? 'var(--sf-text)' : 'var(--sf-text-3)',
      fontSize: '13px',
      cursor: 'pointer'
    }}>
                  {o.charAt(0).toUpperCase() + o.slice(1)}
                </button>;
  })}
          </div>}
        </div>
        <div aria-live="polite" style={{
    margin: '8px 0 0',
    fontSize: '13px',
    color: 'var(--sf-text-3)',
    minHeight: '1px'
  }}>
          {q.trim() === '' && !facetActive ? <>{counts.total} {nounText}</> : counts.shown === 0 ? <>
                {q.trim() === '' ? 'No ' + nounText + ' match the selected filters.' : facetActive ? 'No ' + nounText + ' match \u201c' + q + '\u201d with the selected filters.' : 'No ' + nounText + ' match \u201c' + q + '\u201d.'}{' '}
                <button type="button" onClick={clearAll} style={{
    background: 'none',
    border: 'none',
    padding: 0,
    color: 'var(--sf-accent)',
    cursor: 'pointer',
    font: 'inherit',
    textDecoration: 'underline'
  }}>
                  Clear filters
                </button>
                {children ? <> {children}</> : null}
              </> : <>
                Showing {counts.shown} of {counts.total} {nounText}
              </>}
        </div>
      </div>
    </>;
};

<BackToIndex href="#all-settings" label="返回索引" />

本参考页面列出了 Claude Code 从设置文件读取的每个键，以及它保存在 `~/.claude.json` 中的[短键组](#global-config-settings)。要选择文件或检查优先级，请从[设置文件和优先级](/docs/zh-CN/settings)开始。

<span id="available-settings" />

<span id="scopes" />

<span id="all-settings" />

<h2 id="settings-index">
  设置索引
</h2>

下面的每个键都链接到其条目。范围列出了[文件](/docs/zh-CN/settings#settings-files-and-who-they-affect)，其中可以使用该键：`User` 是 `~/.claude/settings.json`，`Project` 是 `.claude/settings.json`，`Local` 是 `.claude/settings.local.json`，`Managed` 是[您的组织部署的内容](/docs/zh-CN/managed-settings)。`Any file` 表示所有四个文件，`Global config` 表示 [`~/.claude.json`](#global-config-settings)。

<ReferenceFilter
  noun="settings"
  placeholder="按键或用途筛选设置"
  facetOrder={{ scope: ["Any file", "User, local, or managed", "User or managed", "Managed", "Global config"] }}
  columnHelp={{
topic: "本页面中包含该条目的部分。使用排序方式按主题对表格进行分组。",
scope: "哪些设置文件可以设置该键：用户 (~/.claude/settings.json)、项目 (.claude/settings.json)、本地 (.claude/settings.local.json) 或托管（由您的组织部署）。全局配置键位于 ~/.claude.json 中。",
}}
/>

| 键 | 描述 | 主题 | 范围 |
| :- | :- | :- | :- |
| [`advisorModel`](#advisormodel) | 选择当 Claude 使用[顾问工具](/docs/zh-CN/advisor)时哪个模型来回答 | 模型和响应 | Any file |
| [`agent`](#agent) | 将每个会话作为具有其提示、工具和模型的命名[子代理](/docs/zh-CN/sub-agents)启动 | 代理、会话和工作树 | Any file |
| [`agentPushNotifEnabled`](#agentpushnotifenabled) | 让 Claude 在决定时向您的手机发送[推送通知](/docs/zh-CN/remote-control#mobile-push-notifications) | 远程、桌面和通知 | Any file |
| [`allowAllClaudeAiMcps`](#allowallclaudeaimcps) | 加载[claude.ai 连接器](/docs/zh-CN/mcp)，Claude Code 与部署的 [`managed-mcp.json`](/docs/zh-CN/managed-mcp#exclusive-control-with-managed-mcp-json) 一起自行获取 | MCP | Managed |
| [`allowClaudeInChromeWithManagedMcp`](#allowclaudeinchromewithmanagedmcp) | 让内置的[Chrome 中的 Claude](/docs/zh-CN/chrome)服务器与部署的 [`managed-mcp.json`](/docs/zh-CN/managed-mcp#exclusive-control-with-managed-mcp-json) 一起运行 | MCP | Managed |
| [`allowedChannelPlugins`](#allowedchannelplugins) | 替换可以推送消息的[频道插件](/docs/zh-CN/channels#restrict-which-channel-plugins-can-run)的默认允许列表 | 插件和技能 | Managed |
| [`allowedHttpHookUrls`](#allowedhttphookurls) | 限制[HTTP hooks](/docs/zh-CN/hooks)可以针对的 URL | Hooks 和自动化 | Any file |
| [`allowedMcpServers`](#allowedmcpservers) | 允许列表用户可以添加的[MCP 服务器](/docs/zh-CN/mcp) | MCP | Any file |
| [`allowedProviders`](#allowedproviders) | 限制[API 提供商](/docs/zh-CN/third-party-integrations)机器可以使用的 | 身份验证和提供商 | Managed |
| [`allowManagedHooksOnly`](#allowmanagedhooksonly) | 仅运行您的组织部署的[hooks](/docs/zh-CN/hooks) | Hooks 和自动化 | Managed |
| [`allowManagedMcpServersOnly`](#allowmanagedmcpserversonly) | 使托管的 [MCP](/docs/zh-CN/mcp) 允许列表成为唯一适用的列表 | MCP | Managed |
| [`allowManagedPermissionRulesOnly`](#allowmanagedpermissionrulesonly) | 使[托管设置](/docs/zh-CN/managed-settings)成为[权限规则](/docs/zh-CN/permissions#managed-settings)的唯一设置来源 | 权限设置 | Managed |
| [`alwaysThinkingEnabled`](#alwaysthinkingenabled) | 为每个会话关闭[扩展思考](/docs/zh-CN/model-config#extended-thinking) | 模型和响应 | Any file |
| [`apiKeyHelper`](#apikeyhelper) | 使用您自己的命令生成 [API 凭证](/docs/zh-CN/authentication#credential-management) | 身份验证和提供商 | Any file |
| [`askUserQuestionTimeout`](#askuserquestiontimeout) | 让未回答的问题在空闲时间后[自动继续](/docs/zh-CN/tools-reference#question-auto-continue-timeout) | 界面和终端 | User or managed |
| [`appendPlugins`](#appendplugins) | 在用户安装的每个 mod 之后运行您的组织的 [mod](/docs/zh-CN/plugins/mods/admin) | 插件和 skill | User or managed |
| [`attribution`](#attribution) | 自定义 Claude Code 添加到提交和拉取请求的属性 | Git 和属性 | Any file |
| [`attribution.commit`](#attribution-commit) | 更改或隐藏 Claude Code 添加到提交的预告片 | Git 和属性 | Any file |
| [`attribution.pr`](#attribution-pr) | 更改或隐藏拉取请求描述中的属性行 | Git 和属性 | Any file |
| [`attribution.sessionUrl`](#attribution-sessionurl) | 从[云](/docs/zh-CN/claude-code-on-the-web)和[远程控制](/docs/zh-CN/remote-control)提交中省略 claude.ai 会话链接 | Git 和属性 | Any file |
| [`autoCompactEnabled`](#autocompactenabled) | 打开或关闭[自动压缩](/docs/zh-CN/context-window) | 内存和上下文 | Any file |
| [`autoCompactWindow`](#autocompactwindow) | 设置上下文在 Claude Code [压缩](/docs/zh-CN/context-window)之前有多满 | 内存和上下文 | Any file |
| [`autoConnectIde`](#autoconnectide) | 从外部终端自动连接到运行的 [VS Code](/docs/zh-CN/vs-code) 或 [JetBrains](/docs/zh-CN/jetbrains#from-external-terminals) IDE | 全局配置设置 | Global config |
| [`autoContinueAtUsageLimit`](#autocontinueatusagelimit) | 在打开的会话中等待，并在 claude.ai 使用限制重置后[自动继续任务](/docs/zh-CN/interactive-mode#wait-for-a-usage-limit-to-reset) | 界面和终端 | User or managed |
| [`autoInstallIdeExtension`](#autoinstallideextension) | 关闭从 VS Code 终端自动安装 [IDE 扩展](/docs/zh-CN/vs-code#install-the-extension) | 全局配置设置 | Global config |
| [`autoMemoryDirectory`](#automemorydirectory) | 在您选择的目录中存储[自动内存](/docs/zh-CN/memory#auto-memory) | 内存和上下文 | Any file |
| [`autoMemoryEnabled`](#automemoryenabled) | 打开或关闭[自动内存](/docs/zh-CN/memory#auto-memory) | 内存和上下文 | Any file |
| [`autoMode`](#automode) | 向[自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)分类器添加您自己的允许和拒绝规则 | 权限设置 | User or managed |
| [`autoMode.classifyAllShell`](#automode-classifyallshell) | 通过[自动模式分类器](/docs/zh-CN/permission-modes#what-the-classifier-blocks-by-default)发送每个 shell 命令，即使是狭窄允许规则匹配的命令 | 权限设置 | User or managed |
| [`autoScrollEnabled`](#autoscrollenabled) | 在全屏渲染中[跟随新输出](/docs/zh-CN/fullscreen#auto-follow)到底部 | 界面和终端 | Any file |
| [`autoUpdatesChannel`](#autoupdateschannel) | 遵循稳定[发布频道](/docs/zh-CN/setup#configure-release-channel)而不是最新版本 | 更新和版本控制 | Any file |
| [`availableModels`](#availablemodels) | [限制人们可以选择的模型](/docs/zh-CN/model-config#restrict-model-selection) | 模型和响应 | Any file |
| [`availableModelsMatch`](#availablemodelsmatch) | 使每个 `availableModels` 模型 ID 条目[仅允许它命名的版本](/docs/zh-CN/model-config#block-specific-models-or-versions) | 模型和响应 | Managed |
| [`awaySummaryEnabled`](#awaysummaryenabled) | 关闭当您回到终端时显示的[会话回顾](/docs/zh-CN/interactive-mode#session-recap) | 远程、桌面和通知 | Any file |
| [`awsAuthRefresh`](#awsauthrefresh) | 使用您自己的命令刷新 `.aws` 中过期的 [Bedrock 凭证](/docs/zh-CN/amazon-bedrock#advanced-credential-configuration) | 身份验证和提供商 | Any file |
| [`awsCredentialExport`](#awscredentialexport) | 从您自己的命令以 JSON 形式提供 [Bedrock 凭证](/docs/zh-CN/amazon-bedrock#advanced-credential-configuration) | 身份验证和提供商 | Any file |
| [`axScreenReader`](#axscreenreader) | 渲染[屏幕阅读器友好的输出](/docs/zh-CN/accessibility) | 界面和终端 | Any file |
| [`bashEditDiffEnabled`](#basheditdiffenabled) | 在每个权限模式中记录 [Bash 命令运行期间发生更改的文件](/docs/zh-CN/hooks#bash) | 界面和终端 | User or managed |
| [`bashOutputMaxChars`](#bashoutputmaxchars) | 设置成功命令的[输出](/docs/zh-CN/tools-reference#output-limits)有多少 Claude 内联接收 | 内存和上下文 | Any file |
| [`blockedMarketplaces`](#blockedmarketplaces) | 为您的组织阻止[插件市场](/docs/zh-CN/plugins/overview)来源 | 插件和技能 | Managed |
| [`browserExternalPageTools`](#browserexternalpagetools) | 在[桌面](/docs/zh-CN/desktop)浏览器窗格中的外部页面上关闭 Claude 的工具 | 工具 | Managed |
| [`channelsEnabled`](#channelsenabled) | 为您的组织允许[频道](/docs/zh-CN/channels#enable-channels-for-your-organization) | 插件和技能 | Managed |
| [`claudeInChromeDefaultEnabled`](#claudeinchromedefaultenabled) | 在会话启动时打开 [Chrome 集成](/docs/zh-CN/chrome)，适用于交互式 CLI 和 VS Code 扩展 | 全局配置设置 | Global config |
| [`claudeMd`](#claudemd) | 从托管设置注入组织范围的 [CLAUDE.md](/docs/zh-CN/memory#deploy-organization-wide-claude-md) 指令 | 内存和上下文 | Managed |
| [`claudeMdExcludes`](#claudemdexcludes) | 在内存加载时跳过特定的 [CLAUDE.md](/docs/zh-CN/memory#exclude-specific-claude-md-files) 文件 | 内存和上下文 | Any file |
| [`cleanupPeriodDays`](#cleanupperioddays) | 选择 Claude Code 在删除[记录](/docs/zh-CN/data-usage#data-retention)之前保留多少天 | 隐私和遥测 | Any file |
| [`companyAnnouncements`](#companyannouncements) | 在启动时显示您的组织的公告 | 界面和终端 | Any file |
| [`copyFullResponse`](#copyfullresponse) | 使 [`/copy`](/docs/zh-CN/commands) 复制完整响应而不显示代码块选择器 | 全局配置设置 | Global config |
| [`copyOnSelect`](#copyonselect) | 关闭在[全屏渲染](/docs/zh-CN/fullscreen#use-the-mouse)和代理视图中用鼠标选择的文本的自动复制 | 全局配置设置 | Global config |
| [`crossSessionInbound`](#crosssessioninbound) | 选择 Claude Code 是否传递[来自您其他会话的消息](/docs/zh-CN/cross-session-messaging#control-inbound-messages)、显示通知而不传递它们，或拒绝它们 | 代理、会话和工作树 | Any file |
| [`defaultShell`](#defaultshell) | 选择 Bash 或 PowerShell 是否运行您使用 [`!` 前缀](/docs/zh-CN/interactive-mode#shell-mode-with-prefix)键入的 shell 命令 | 界面和终端 | Any file |
| [`defaultToAgentsView`](#defaulttoagentsview) | 当您运行不带参数的 `claude` 时打开[代理视图](/docs/zh-CN/agent-view)而不是新对话 | 全局配置设置 | Global config |
| [`deniedMcpServers`](#deniedmcpservers) | 按 URL、命令或名称阻止特定的 [MCP 服务器](/docs/zh-CN/mcp) | MCP | Any file |
| [`deniedModels`](#deniedmodels) | [阻止特定模型](/docs/zh-CN/model-config#block-specific-models-or-versions)，即使是 `availableModels` 允许的模型 | 模型和响应 | Managed |
| [`desktopSessionCleanupPeriodDays`](#desktopsessioncleanupperioddays) | 为[Claude Desktop 和 Cowork 记录](/docs/zh-CN/claude-directory#cleaned-up-automatically)设置年龄限制（天数） | 隐私和遥测 | User or managed |
| [`dialogExpiry`](#dialogexpiry) | 设置 Claude Code 在取消对话之前等待[远程控制](/docs/zh-CN/remote-control)或 SDK 主机回答转发对话的时间 | 界面和终端 | User or managed |
| [`diffTool`](#difftool) | 选择 Claude 提议的文件更改是在 [VS Code](/docs/zh-CN/vs-code) 或 [JetBrains](/docs/zh-CN/jetbrains#features) diff 查看器中打开还是保留在终端中 | 全局配置设置 | Global config |
| [`disableAgentView`](#disableagentview) | 关闭后台代理和[代理视图](/docs/zh-CN/agent-view) | 代理、会话和工作树 | Any file |
| [`disableAllHooks`](#disableallhooks) | 一次关闭 [hooks](/docs/zh-CN/hooks)、自定义[状态行](/docs/zh-CN/statusline)和自定义 [`@` 文件建议](/docs/zh-CN/interactive-mode#quick-commands)命令 | Hooks 和自动化 | Any file |
| [`disableArtifact`](#disableartifact) | 已弃用；使用 `enableArtifact` 关闭[工件工具](/docs/zh-CN/artifacts) | 远程、桌面和通知 | Any file |
| [`disableAutoMode`](#disableautomode) | 从权限模式循环中删除[自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode) | 权限设置 | Any file |
| [`disableBrowserExternalNavigation`](#disablebrowserexternalnavigation) | 将[桌面](/docs/zh-CN/desktop)浏览器窗格限制为 localhost，供人员和 Claude 使用 | 工具 | Managed |
| [`disableBundledSkills`](#disablebundledskills) | 关闭 Claude Code 附带的[技能](/docs/zh-CN/skills#bundled-skills)和[工作流](/docs/zh-CN/workflows) | 插件和技能 | Any file |
| [`disableClaudeAiConnectors`](#disableclaudeaiconnectors) | 关闭 [claude.ai 连接器](/docs/zh-CN/mcp#disable-claude-ai-connectors)，以便 Claude Code 不会获取它们 | MCP | Any file |
| [`disableCommandPluginSources`](#disablecommandpluginsources) | 阻止通过运行市场声明的命令安装的[插件](/docs/zh-CN/plugins/overview) | 插件和技能 | Managed |
| [`disableDeepLinkRegistration`](#disabledeeplinkregistration) | 停止 Claude Code 注册 [`claude-cli://` 处理程序](/docs/zh-CN/deep-links) | 远程、桌面和通知 | Any file |
| [`disableDesktopLocalSessions`](#disabledesktoplocalsessions) | 关闭在设备上运行的[桌面代码会话](/docs/zh-CN/desktop#local-sessions-on-managed-devices)，仅保留 SSH 到其他主机和云 | 远程、桌面和通知 | Managed |
| [`disabledMcpjsonServers`](#disabledmcpjsonservers) | 拒绝项目的 [`.mcp.json`](/docs/zh-CN/mcp#project-scope) 中的特定服务器 | MCP | Any file |
| [`disableMobileSimulatorTools`](#disablemobilesimulatortools) | 在[桌面](/docs/zh-CN/desktop) iOS 模拟器窗格中阻止 Claude 的工具 | 工具 | Managed |
| [`disableRemoteControl`](#disableremotecontrol) | 在可以启动的任何地方关闭[远程控制](/docs/zh-CN/remote-control) | 远程、桌面和通知 | Any file |
| [`disableSideloadFlags`](#disablesideloadflags) | 拒绝侧加载[插件](/docs/zh-CN/plugins/overview)、[子代理](/docs/zh-CN/sub-agents)和 [MCP 服务器](/docs/zh-CN/mcp)的 CLI 标志 | 企业和托管设置 | Managed |
| [`disableSkillShellExecution`](#disableskillshellexecution) | 停止[技能](/docs/zh-CN/skills)和自定义命令运行内联 shell | 插件和技能 | Any file |
| [`disableWorkflows`](#disableworkflows) | 为所有人关闭[动态工作流](/docs/zh-CN/workflows)；为自己使用 `enableWorkflows` | Hooks 和自动化 | Any file |
| [`editorMode`](#editormode) | 在输入提示中使用 [vim 快捷键](/docs/zh-CN/interactive-mode#vim-editor-mode) | 界面和终端 | Any file |
| [`effortLevel`](#effortlevel) | 为没有保存级别的模型设置默认[努力级别](/docs/zh-CN/model-config#adjust-effort-level) | 模型和响应 | Any file |
| [`emojiCompletionEnabled`](#emojicompletionenabled) | 关闭提示输入中的 [`:shortcode:` 表情符号建议和替换](/docs/zh-CN/interactive-mode#emoji-shortcodes) | 界面和终端 | Any file |
| [`enableAllProjectMcpServers`](#enableallprojectmcpservers) | 批准项目 [`.mcp.json`](/docs/zh-CN/mcp#project-server-approvals-and-workspace-trust) 文件中的每个服务器，无需提示 | MCP | Any file |
| [`enableArtifact`](#enableartifact) | 使用任何文件中的 `false` 关闭[工件工具](/docs/zh-CN/artifacts)；没有文件可以将其打开 | 远程、桌面和通知 | Any file |
| [`enabledMcpjsonServers`](#enabledmcpjsonservers) | 批准项目的 [`.mcp.json`](/docs/zh-CN/mcp#project-server-approvals-and-workspace-trust) 中的特定服务器 | MCP | Any file |
| [`enabledPlugins`](#enabledplugins) | 按范围打开或关闭单个[插件](/docs/zh-CN/plugins/overview) | 插件和技能 | Any file |
| [`enableWorkflows`](#enableworkflows) | 根据您的计划默认值打开或关闭[动态工作流](/docs/zh-CN/workflows) | Hooks 和自动化 | Any file |
| [`enforceAvailableModels`](#enforceavailablemodels) | 保持 [`/model` 默认选择](/docs/zh-CN/model-config#enforce-the-allowlist-for-the-default-model)在您的 `availableModels` 允许列表内 | 模型和响应 | Any file |
| [`env`](#env) | 为每个会话及其子进程设置[环境变量](/docs/zh-CN/env-vars#in-settings-files) | 内存和上下文 | Any file |
| [`externalEditorContext`](#externaleditorcontext) | 当您按 [Ctrl+G](/docs/zh-CN/interactive-mode#general-controls) 编辑时，将 Claude 的最后响应显示为注释 | 全局配置设置 | Global config |
| [`extraKnownMarketplaces`](#extraknownmarketplaces) | 为存储库或组织注册[市场](/docs/zh-CN/plugins/overview) | 插件和技能 | Any file |
| [`fallbackModel`](#fallbackmodel) | 为主模型过载时命名[备份模型](/docs/zh-CN/model-config#fallback-model-chains) | 模型和响应 | Any file |
| [`fastMode`](#fastmode) | 为可用的会话打开[快速模式](/docs/zh-CN/fast-mode) | 模型和响应 | Any file |
| [`fastModePerSessionOptIn`](#fastmodepersessionoptin) | 要求人们在每个会话中打开[快速模式](/docs/zh-CN/fast-mode) | 模型和响应 | Any file |
| [`feedbackDrafts`](#feedbackdrafts) | 控制 Claude 是否为您排队[反馈草稿](/docs/zh-CN/tools-reference#sendfeedback-tool-behavior)以供审查 | 隐私和遥测 | User or managed |
| [`feedbackSurveyRate`](#feedbacksurveyrate) | 更改[会话质量调查](/docs/zh-CN/data-usage#session-quality-surveys)出现的频率 | 隐私和遥测 | Any file |
| [`fileCheckpointingEnabled`](#filecheckpointingenabled) | 打开或关闭 [`/rewind`](/docs/zh-CN/checkpointing) 恢复的文件快照 | 内存和上下文 | Any file |
| [`fileSuggestion`](#filesuggestion) | 从您自己的命令提供 [`@` 文件自动完成](/docs/zh-CN/interactive-mode#quick-commands) | 界面和终端 | Any file |
| [`footerLinksRegexes`](#footerlinksregexes) | 将输出中的问题或审查 ID 变成输入框下方的[可点击链接](/docs/zh-CN/statusline#clickable-links) | 界面和终端 | User or managed |
| [`forceLoginGatewayUrl`](#forcelogingatewayurl) | 设置登录屏幕连接到的[网关 URL](/docs/zh-CN/claude-apps-gateway#set-the-gateway-url) | 身份验证和提供商 | Managed |
| [`forceLoginMethod`](#forceloginmethod) | [限制登录](/docs/zh-CN/authentication#restrict-login-to-your-organization)到 claude.ai、Claude Console 或[云网关](/docs/zh-CN/claude-apps-gateway) | 身份验证和提供商 | Any file |
| [`forceLoginOrgUUID`](#forceloginorguuid) | [将 claude.ai 登录固定到您的组织](/docs/zh-CN/authentication#restrict-login-to-your-organization)；仅托管源强制执行 | 身份验证和提供商 | Any file |
| [`forceRemoteSettingsRefresh`](#forceremotesettingsrefresh) | 阻止启动，直到[服务器托管设置](/docs/zh-CN/server-managed-settings)被新鲜获取 | 企业和托管设置 | Managed |
| [`gatewayInternalNetworks`](#gatewayinternalnetworks) | 让 `/login` 到达您的组织在内部使用的公共 IPv4 空间上的[云网关](/docs/zh-CN/claude-apps-gateway#allow-a-gateway-on-public-address-space-you-own) | 身份验证和提供商 | Managed |
| [`gcpAuthRefresh`](#gcpauthrefresh) | 使用您自己的命令刷新 [Google Cloud 凭证](/docs/zh-CN/google-vertex-ai#advanced-credential-configuration) | 身份验证和提供商 | Any file |
| [`hooks`](#hooks) | 在 Claude Code 生命周期中的点运行您自己的命令作为 [hooks](/docs/zh-CN/hooks) | Hooks 和自动化 | Any file |
| [`httpHookAllowedEnvVars`](#httphookallowedenvvars) | 限制[HTTP hooks](/docs/zh-CN/hooks)可以在标头中放入的环境变量 | Hooks 和自动化 | Any file |
| [`includeCoAuthoredBy`](#includecoauthoredby) | 已弃用；使用 `attribution` 隐藏或更改提交和 PR 属性 | Git 和属性 | Any file |
| [`includeGitInstructions`](#includegitinstructions) | 从 Claude 的上下文中删除内置的提交和 PR 指令 | Git 和属性 | Any file |
| [`inputNeededNotifEnabled`](#inputneedednotifenabled) | 当 Claude 在等待您时获得[推送通知](/docs/zh-CN/remote-control#mobile-push-notifications) | 远程、桌面和通知 | Any file |
| [`isolatePeerMachines`](#isolatepeermachines) | 在 Claude [向您在另一台机器上的会话发送消息](/docs/zh-CN/cross-session-messaging#require-approval-for-cross-machine-messages)之前询问您 | 代理、会话和工作树 | Any file |
| [`keybindingFlavor`](#keybindingflavor) | 已弃用且无效；单词编辑快捷键始终[遵循 readline 约定](/docs/zh-CN/interactive-mode#make-ctrl-w-delete-back-to-whitespace) | 界面和终端 | Any file |
| [`language`](#language) | 让 Claude 用英语以外的语言回应 | 模型和响应 | Any file |
| [`leftArrowOpensAgents`](#leftarrowopensagents) | 关闭 `←` 快捷键，该快捷键[后台会话并打开代理视图](/docs/zh-CN/agent-view#switch-sessions-without-leaving-the-terminal) | 全局配置设置 | Global config |
| [`managedMcpServers`](#managedmcpservers) | 为每个用户提供远程 [MCP 服务器](/docs/zh-CN/managed-mcp#provide-servers-through-managed-settings)以及他们添加的服务器 | MCP | Managed |
| [`managedSourcesBehavior`](#managedsourcesbehavior) | 组合您部署的每个[托管源](/docs/zh-CN/managed-settings#how-claude-code-combines-managed-sources)，而不是仅使用优先级最高的源 | 企业和托管设置 | Managed |
| [`maxEffortLevel`](#maxeffortlevel) | 在每个模型或每个提供商上限制每个模型的[努力级别](/docs/zh-CN/model-config#adjust-effort-level) | 模型和响应 | Any file |
| [`maxProseWidth`](#maxprosewidth) | 限制 Claude 响应中的散文在宽终端中运行的宽度 | 界面和终端 | Any file |
| [`minimumVersion`](#minimumversion) | 保持[自动更新](/docs/zh-CN/setup#pin-a-minimum-version)不安装低于版本的任何内容 | 更新和版本控制 | Any file |
| [`model`](#model) | 更改 Claude Code 启动时使用的[模型](/docs/zh-CN/model-config#set-a-default-model-for-new-sessions) | 模型和响应 | Any file |
| [`modelOverrides`](#modeloverrides) | [将模型 ID 映射](/docs/zh-CN/model-config#override-model-ids-per-version)到您的提供商的 ID，例如 Bedrock ARN | 模型和响应 | Any file |
| [`modelPicker`](#modelpicker) | 选择 [`/model` 选择器](/docs/zh-CN/model-config#available-models)列出的模型，按您自己的顺序和您自己的标签 | 模型和响应 | User or managed |
| [`modelPricing`](#modelpricing) | 按您的组织合同费率而不是列表价格报告支出 | 模型和响应 | Managed |
| [`modelSettings`](#modelsettings) | 为每个模型保留已保存的 [effort 级别](/docs/zh-CN/model-config#adjust-effort-level)或[自动压缩窗口](/docs/zh-CN/model-config#set-the-auto-compact-window)，或限制某个模型的 effort | 模型和响应 | Any file |
| [`otelHeadersHelper`](#otelheadershelper) | 使用您自己的命令生成旋转的 [OpenTelemetry](/docs/zh-CN/monitoring-usage#dynamic-headers) 标头 | 身份验证和提供商 | Any file |
| [`outputStyle`](#outputstyle) | 使用[输出样式](/docs/zh-CN/output-styles)更改 Claude 的角色、语气和输出格式 | 模型和响应 | Any file |
| [`parentSettingsBehavior`](#parentsettingsbehavior) | 应用或删除[SDK 或 IDE 主机](/docs/zh-CN/managed-settings#let-an-embedding-host-add-policy)在您部署[托管设置](/docs/zh-CN/managed-settings)时传递的限制 | 企业和托管设置 | Managed |
| [`permissionExplainerEnabled`](#permissionexplainerenabled) | 在 v2.1.257 中删除，以及 shell 权限提示上的 `Ctrl+E` 命令说明 | 全局配置设置 | Global config |
| [`permissions`](#permissions) | 设置允许、询问和拒绝规则以及启动[权限模式](/docs/zh-CN/permission-modes) | 权限设置 | Any file |
| [`permissions.additionalDirectories`](#permissions-additionaldirectories) | 给予 Claude 文件访问权限到[当前目录外的目录](/docs/zh-CN/permissions#working-directories) | 权限设置 | Any file |
| [`permissions.allow`](#permissions-allow) | 批准列出的[工具使用](/docs/zh-CN/permissions#permission-rule-syntax)而无需提示 | 权限设置 | Any file |
| [`permissions.ask`](#permissions-ask) | 始终在列出的[工具使用](/docs/zh-CN/permissions#permission-rule-syntax)之前提示 | 权限设置 | Any file |
| [`permissions.blockReadsOutsideWorkingDirectories`](#permissions-blockreadsoutsideworkingdirectories) | 使文件工具在每个权限模式下拒绝在[工作目录](/docs/zh-CN/permissions#working-directories)外的读取 | 权限设置 | Any file |
| [`permissions.defaultMode`](#permissions-defaultmode) | 设置新会话启动的[权限模式](/docs/zh-CN/permission-modes#which-mode-a-session-starts-in) | 权限设置 | Any file |
| [`permissions.deny`](#permissions-deny) | 阻止列出的[工具使用](/docs/zh-CN/permissions#permission-rule-syntax)，包括保存秘密的文件的读取 | 权限设置 | Any file |
| [`permissions.disableBypassPermissionsMode`](#permissions-disablebypasspermissionsmode) | 防止任何人进入 [bypassPermissions 模式](/docs/zh-CN/permission-modes#skip-all-checks-with-bypasspermissions-mode) | 权限设置 | Any file |
| [`plansDirectory`](#plansdirectory) | 选择[计划模式](/docs/zh-CN/permission-modes#analyze-before-you-edit-with-plan-mode)写入计划文件的位置 | 内存和上下文 | Any file |
| [`pluginConfigs`](#pluginconfigs) | 存储您给[插件](/docs/zh-CN/plugins/overview)的配置对话框的答案 | 插件和技能 | User or managed |
| [`pluginSuggestionMarketplaces`](#pluginsuggestionmarketplaces) | 选择哪些[市场](/docs/zh-CN/plugins/overview)可以在 `/plugin` 中显示插件安装建议 | 插件和技能 | Managed |
| [`pluginTrustMessage`](#plugintrustmessage) | 向[插件](/docs/zh-CN/plugins/overview)信任警告添加您自己的文本 | 插件和技能 | Managed |
| [`policyHelper`](#policyhelper) | 运行在启动时计算[托管设置](/docs/zh-CN/managed-settings#compute-the-policy-with-a-helper-program)的可执行文件 | 企业和托管设置 | Managed |
| [`policyHelper.path`](#policyhelper-path) | 命名 Claude Code 运行的[辅助可执行文件](/docs/zh-CN/managed-settings#compute-the-policy-with-a-helper-program) | 企业和托管设置 | Managed |
| [`policyHelper.refreshIntervalMs`](#policyhelper-refreshintervalms) | 在后台按间隔重新运行[辅助程序](/docs/zh-CN/managed-settings#compute-the-policy-with-a-helper-program) | 企业和托管设置 | Managed |
| [`policyHelper.timeoutMs`](#policyhelper-timeoutms) | 设置 Claude Code 等待[辅助程序](/docs/zh-CN/managed-settings#compute-the-policy-with-a-helper-program)的时间 | 企业和托管设置 | Managed |
| [`preferredNotifChannel`](#preferrednotifchannel) | 为任务完成选择[终端铃声或桌面通知](/docs/zh-CN/terminal-config#get-a-terminal-bell-or-notification) | 远程、桌面和通知 | Any file |
| [`prefersReducedMotion`](#prefersreducedmotion) | [减少或关闭](/docs/zh-CN/accessibility#accessibility-settings)旋转、闪烁和闪光动画 | 界面和终端 | Any file |
| [`prependPlugins`](#prependplugins) | 在用户安装的每个 mod 之前运行您的组织的 [mod](/docs/zh-CN/plugins/mods/admin) | 插件和 skill | User or managed |
| [`processWrapper`](#processwrapper) | 在 macOS 和 Linux 上通过[企业启动器](/docs/zh-CN/corporate-launcher)运行 Claude Code 的后台进程 | 代理、会话和工作树 | User or managed |
| [`promptCacheTtl`](#promptcachettl) | 为主对话选择[提示缓存生命周期](/docs/zh-CN/prompt-caching#cache-lifetime) | 模型和响应 | Any file |
| [`promptSuggestionEnabled`](#promptsuggestionenabled) | 隐藏输入框中灰显的[提示建议](/docs/zh-CN/interactive-mode#prompt-suggestions) | 界面和终端 | Any file |
| [`prStatusFooterEnabled`](#prstatusfooterenabled) | 关闭提示页脚的 [PR 审查状态](/docs/zh-CN/interactive-mode#pr-review-status)徽章和其后面的拉取请求检查 | 全局配置设置 | Global config |
| [`prUrlTemplate`](#prurltemplate) | 将 PR 链接指向内部代码审查工具而不是 github.com | Git 和属性 | Any file |
| [`remote.defaultEnvironmentId`](#remote-defaultenvironmentid) | 为 `claude --cloud` 选择默认的[云环境](/docs/zh-CN/cloud-environments)；自托管 `ccpool_` ID 仅从用户和托管设置以及 `--settings` 读取 | 远程、桌面和通知 | Any file |
| [`remoteControlAtStartup`](#remotecontrolatstartup) | 当会话启动时自动连接[远程控制](/docs/zh-CN/remote-control#enable-remote-control-for-all-sessions) | 远程、桌面和通知 | Any file |
| [`requiredMaximumVersion`](#requiredmaximumversion) | [拒绝在](/docs/zh-CN/setup#pin-a-minimum-version)您的组织允许的版本更新的版本上启动 | 更新和版本控制 | Managed |
| [`requiredMinimumVersion`](#requiredminimumversion) | [拒绝在](/docs/zh-CN/setup#pin-a-minimum-version)您的组织要求的版本更旧的版本上启动 | 更新和版本控制 | Managed |
| [`respectGitignore`](#respectgitignore) | 将 gitignored 文件保留在 [`@` 文件选择器](/docs/zh-CN/interactive-mode#quick-commands)之外 | 界面和终端 | Any file |
| [`respondToBashCommands`](#respondtobashcommands) | 停止 Claude 在 [`!` shell 命令](/docs/zh-CN/interactive-mode#shell-mode-with-prefix)运行后响应 | 界面和终端 | Any file |
| [`sandbox`](#sandbox) | 在 macOS、Linux 和 WSL2 上[隔离 Bash 命令](/docs/zh-CN/sandboxing)与您的文件系统和网络 | 沙箱设置 | Any file |
| [`sandbox.allowAppleEvents`](#sandbox-allowappleevents) | 让[沙箱化](/docs/zh-CN/sandboxing)命令在 macOS 上发送 Apple Events | 沙箱设置 | User or managed |
| [`sandbox.allowUnsandboxedCommands`](#sandbox-allowunsandboxedcommands) | 让 Claude 在[沙箱](/docs/zh-CN/sandboxing#the-unsandboxed-retry-escape-hatch)外重试被阻止的命令，或禁止它 | 沙箱设置 | Any file |
| [`sandbox.autoAllowBashIfSandboxed`](#sandbox-autoallowbashifsandboxed) | 运行[沙箱化](/docs/zh-CN/sandboxing#auto-allow-mode)命令而无需权限提示 | 沙箱设置 | Any file |
| [`sandbox.bwrapPath`](#sandbox-bwrappath) | 将[沙箱](/docs/zh-CN/sandboxing)指向 `PATH` 外的 bubblewrap 二进制文件 | 沙箱设置 | Managed |
| [`sandbox.credentials`](#sandbox-credentials) | 在[沙箱](/docs/zh-CN/sandboxing#protect-credentials)内隐藏或掩盖凭证文件和变量 | 沙箱设置 | Any file |
| [`sandbox.credentials.allowPlaintextInject`](#sandbox-credentials-allowplaintextinject) | 让[掩盖的凭证](/docs/zh-CN/sandboxing#mask-credentials)到达受信任的测试网络上的纯 HTTP 服务 | 沙箱设置 | User or managed |
| [`sandbox.credentials.awsPairs`](#sandbox-credentials-awspairs) | 将自定义命名的 AWS 密钥变量链接到一个凭证以进行[重新签名](/docs/zh-CN/sandboxing#re-sign-aws-requests) | 沙箱设置 | User or managed |
| [`sandbox.credentials.envVars`](#sandbox-credentials-envvars) | 在[沙箱](/docs/zh-CN/sandboxing#mask-environment-variables)内取消设置或掩盖环境变量 | 沙箱设置 | Any file |
| [`sandbox.credentials.files`](#sandbox-credentials-files) | 在[沙箱](/docs/zh-CN/sandboxing#mask-credential-files)内阻止或掩盖凭证文件的读取 | 沙箱设置 | Any file |
| [`sandbox.credentials.sigv4`](#sandbox-credentials-sigv4) | 选择流式传输、预签名或 [SigV4A AWS 请求](/docs/zh-CN/sandboxing#re-sign-aws-requests)是否失败或通过 | 沙箱设置 | User or managed |
| [`sandbox.enabled`](#sandbox-enabled) | 在 macOS、Linux 和 WSL2 上打开 [Bash 沙箱](/docs/zh-CN/sandboxing#get-started) | 沙箱设置 | Any file |
| [`sandbox.enableWeakerNestedSandbox`](#sandbox-enableweakernestedsandbox) | 在无特权容器内运行 Linux [沙箱](/docs/zh-CN/sandboxing) | 沙箱设置 | Any file |
| [`sandbox.enableWeakerNetworkIsolation`](#sandbox-enableweakernetworkisolation) | 在 macOS 上让 `gh`、`gcloud` 和 `terraform` 在[沙箱](/docs/zh-CN/sandboxing#go-based-clis-fail-tls-verification-on-macos)内的 MITM 代理后面验证 TLS | 沙箱设置 | Any file |
| [`sandbox.excludedCommands`](#sandbox-excludedcommands) | 命名始终在[沙箱](/docs/zh-CN/sandboxing)外运行的命令 | 沙箱设置 | Any file |
| [`sandbox.failIfUnavailable`](#sandbox-failifunavailable) | 当[沙箱](/docs/zh-CN/sandboxing)无法启动时拒绝启动，而不是运行未沙箱化的 | 沙箱设置 | Any file |
| [`sandbox.filesystem`](#sandbox-filesystem) | 控制[沙箱化](/docs/zh-CN/sandboxing#filesystem-isolation)命令可以读写的路径 | 沙箱设置 | Any file |
| [`sandbox.filesystem.allowManagedReadPathsOnly`](#sandbox-filesystem-allowmanagedreadpathsonly) | 停止开发人员重新打开您的组织阻止的[读取路径](/docs/zh-CN/sandboxing#keep-developers-from-widening-the-policy) | 沙箱设置 | Managed |
| [`sandbox.filesystem.allowRead`](#sandbox-filesystem-allowread) | 重新打开在 [`denyRead`](#sandbox-filesystem-denyread) 阻止的区域内的读取 | 沙箱设置 | Any file |
| [`sandbox.filesystem.allowWrite`](#sandbox-filesystem-allowwrite) | 添加[沙箱化](/docs/zh-CN/sandboxing)命令可以写入的路径 | 沙箱设置 | Any file |
| [`sandbox.filesystem.denyRead`](#sandbox-filesystem-denyread) | 阻止[沙箱化](/docs/zh-CN/sandboxing)命令读取特定路径 | 沙箱设置 | Any file |
| [`sandbox.filesystem.denyWrite`](#sandbox-filesystem-denywrite) | 阻止[沙箱化](/docs/zh-CN/sandboxing)命令写入特定路径 | 沙箱设置 | Any file |
| [`sandbox.filesystem.disabled`](#sandbox-filesystem-disabled) | [关闭文件系统隔离](/docs/zh-CN/sandboxing#disable-filesystem-isolation)同时保持网络隔离 | 沙箱设置 | User or managed |
| [`sandbox.ignoreViolations`](#sandbox-ignoreviolations) | 沉默命令预期探测的路径的违规报告 | 沙箱设置 | Any file |
| [`sandbox.network`](#sandbox-network) | 控制[沙箱化](/docs/zh-CN/sandboxing#network-isolation)命令可以到达的主机、端口和套接字 | 沙箱设置 | Any file |
| [`sandbox.network.allowAllUnixSockets`](#sandbox-network-allowallunixsockets) | 让[沙箱化](/docs/zh-CN/sandboxing)命令连接到每个 Unix 套接字 | 沙箱设置 | Any file |
| [`sandbox.network.allowedDomains`](#sandbox-network-alloweddomains) | 预先允许域，以便[沙箱化](/docs/zh-CN/sandboxing)命令不会提示它们 | 沙箱设置 | Any file |
| [`sandbox.network.allowLocalBinding`](#sandbox-network-allowlocalbinding) | 让[沙箱化](/docs/zh-CN/sandboxing)命令在 macOS 上监听网络端口并连接到 localhost | 沙箱设置 | Any file |
| [`sandbox.network.allowMachLookup`](#sandbox-network-allowmachlookup) | 让 macOS [沙箱化](/docs/zh-CN/sandboxing)工具（如 iOS 模拟器或 Playwright）到达其 XPC 服务 | 沙箱设置 | Any file |
| [`sandbox.network.allowManagedDomainsOnly`](#sandbox-network-allowmanageddomainsonly) | 将网络允许列表锁定到[托管设置](/docs/zh-CN/sandboxing#keep-developers-from-widening-the-policy) | 沙箱设置 | Managed |
| [`sandbox.network.allowUnixSockets`](#sandbox-network-allowunixsockets) | 列出[沙箱化](/docs/zh-CN/sandboxing)命令可以在 macOS 上使用的 Unix 套接字路径 | 沙箱设置 | Any file |
| [`sandbox.network.deniedDomains`](#sandbox-network-denieddomains) | 为[沙箱化](/docs/zh-CN/sandboxing)命令阻止域，即使在允许的通配符内 | 沙箱设置 | Any file |
| [`sandbox.network.httpProxyPort`](#sandbox-network-httpproxyport) | 通过您自己的代理路由[沙箱](/docs/zh-CN/sandboxing#custom-proxy-configuration) HTTP 流量 | 沙箱设置 | Any file |
| [`sandbox.network.socksProxyPort`](#sandbox-network-socksproxyport) | 通过您自己的代理路由[沙箱](/docs/zh-CN/sandboxing#custom-proxy-configuration) SOCKS 流量 | 沙箱设置 | Any file |
| [`sandbox.network.strictAllowlist`](#sandbox-network-strictallowlist) | 拒绝[允许列表](/docs/zh-CN/sandboxing#network-isolation)外的主机，而不是提示 | 沙箱设置 | User or managed |
| [`sandbox.network.tlsTerminate`](#sandbox-network-tlsterminate) | 让[沙箱](/docs/zh-CN/sandboxing#network-isolation)代理终止 TLS，以便它可以读取 HTTPS 请求 | 沙箱设置 | User or managed |
| [`sandbox.ripgrep`](#sandbox-ripgrep) | 在[沙箱](/docs/zh-CN/sandboxing)内使用您自己的 ripgrep 二进制文件 | 沙箱设置 | User or managed |
| [`sandbox.socatPath`](#sandbox-socatpath) | 将[沙箱](/docs/zh-CN/sandboxing)代理指向 `PATH` 外的 `socat` 二进制文件 | 沙箱设置 | Managed |
| [`showClearContextOnPlanAccept`](#showclearcontextonplanaccept) | 在[计划接受屏幕](/docs/zh-CN/permission-modes#review-and-approve-a-plan)上显示"清除上下文"选项 | 界面和终端 | Any file |
| [`showThinkingSummaries`](#showthinkingsummaries) | 查看 Claude 的[思考](/docs/zh-CN/model-config#extended-thinking)摘要而不是折叠的存根 | 模型和响应 | Any file |
| [`showTurnDuration`](#showturnduration) | 隐藏每个响应后的"烹饪"持续时间 | 界面和终端 | Any file |
| [`skillListingBudgetFraction`](#skilllistingbudgetfraction) | 为[技能列表](/docs/zh-CN/skills#skill-descriptions-are-cut-short)保留更多或更少的上下文 | 内存和上下文 | Any file |
| [`skillListingMaxDescChars`](#skilllistingmaxdescchars) | 在[技能列表](/docs/zh-CN/skills#skill-descriptions-are-cut-short)中限制每个技能的描述长度 | 内存和上下文 | Any file |
| [`skillOverrides`](#skilloverrides) | [隐藏或折叠技能](/docs/zh-CN/skills#override-skill-visibility-from-settings)而无需编辑其 SKILL.md | 插件和技能 | Any file |
| [`skipAutoPermissionPrompt`](#skipautopermissionprompt) | 跳过 Claude Code 在您自己进入[自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)而不是通过内置默认值时显示的一次性通知 | 权限设置 | User or managed |
| [`skipDangerousModePermissionPrompt`](#skipdangerousmodepermissionprompt) | 在[bypassPermissions 模式](/docs/zh-CN/permission-modes#skip-all-checks-with-bypasspermissions-mode)之前跳过确认对话 | 权限设置 | User, local, or managed |
| [`skipWebFetchPreflight`](#skipwebfetchpreflight) | 当 Anthropic 无法到达时跳过 [WebFetch 主机名检查](/docs/zh-CN/tools-reference#webfetch-tool-behavior) | 隐私和遥测 | Any file |
| [`spellcheck`](#spellcheck) | 在提示输入中用您安装的[拼写检查器](/docs/zh-CN/interactive-mode#check-spelling-as-you-type)为拼写错误的单词加下划线 | 界面和终端 | User or managed |
| [`spinnerTipsEnabled`](#spinnertipsenabled) | 在 Claude 工作时隐藏旋转器中的提示 | 界面和终端 | Any file |
| [`spinnerTipsOverride`](#spinnertipsoverride) | 向旋转器轮换添加您自己的提示，或替换内置提示 | 界面和终端 | Any file |
| [`spinnerVerbs`](#spinnerverbs) | 添加或替换在转弯运行时显示的动词 | 界面和终端 | Any file |
| [`sshConfigs`](#sshconfigs) | 将 [SSH 连接](/docs/zh-CN/desktop#pre-configure-ssh-connections-for-your-team)添加到桌面环境下拉列表 | 远程、桌面和通知 | User or managed |
| [`sshHostAllowlist`](#sshhostallowlist) | 限制[桌面 SSH 会话](/docs/zh-CN/desktop#restrict-which-ssh-hosts-users-can-connect-to)可以到达的主机 | 远程、桌面和通知 | Managed |
| [`statusLine`](#statusline) | 运行您自己的命令来呈现提示下方的[状态行](/docs/zh-CN/statusline) | 界面和终端 | Any file |
| [`strictKnownMarketplaces`](#strictknownmarketplaces) | 允许列表用户可以添加和安装的[市场](/docs/zh-CN/plugins/overview)来源 | 插件和技能 | Managed |
| [`strictPluginOnlyCustomization`](#strictpluginonlycustomization) | 阻止[技能](/docs/zh-CN/skills)、[代理](/docs/zh-CN/sub-agents)、[hooks](/docs/zh-CN/hooks) 和 [MCP 服务器](/docs/zh-CN/mcp)来自用户和项目来源 | 插件和技能 | Managed |
| [`strictPluginOnlyCustomization.agents`](#strictpluginonlycustomization-agents) | 将[代理](/docs/zh-CN/sub-agents)锁定到插件和托管来源 | 插件和技能 | Managed |
| [`strictPluginOnlyCustomization.hooks`](#strictpluginonlycustomization-hooks) | 将[hooks](/docs/zh-CN/hooks)锁定到插件和托管来源 | 插件和技能 | Managed |
| [`strictPluginOnlyCustomization.mcp`](#strictpluginonlycustomization-mcp) | 将 [MCP 服务器](/docs/zh-CN/mcp)锁定到插件和托管来源 | 插件和技能 | Managed |
| [`strictPluginOnlyCustomization.skills`](#strictpluginonlycustomization-skills) | 将[技能](/docs/zh-CN/skills)锁定到插件和托管来源 | 插件和技能 | Managed |
| [`subagentPromptCacheTtl`](#subagentpromptcachettl) | 为子代理和主对话外的其他请求选择[提示缓存生命周期](/docs/zh-CN/prompt-caching#cache-lifetime) | 模型和响应 | Any file |
| [`subagentStatusLine`](#subagentstatusline) | 使用您自己的命令重写[子代理](/docs/zh-CN/sub-agents)任务显示中的行 | 界面和终端 | Any file |
| [`switchModelsOnFlag`](#switchmodelsonflag) | 当[安全分类器](/docs/zh-CN/model-config#ask-before-switching)标记请求时自动切换模型或暂停 | 模型和响应 | Any file |
| [`syncClaudeAiPlugins`](#syncclaudeaiplugins) | 停止加载[在您的 claude.ai 帐户上启用的插件](/docs/zh-CN/plugins/loading#synced-plugins)并停止下载新的 | 插件和技能 | User, local, or managed |
| [`syncClaudeAiSkills`](#syncclaudeaiskills) | 停止加载[在您的 claude.ai 帐户上启用的技能](/docs/zh-CN/skills#how-synced-skills-behave)并停止下载新的 | 插件和技能 | User, local, or managed |
| [`syntaxHighlightingDisabled`](#syntaxhighlightingdisabled) | 关闭 diffs 和代码块中的语法突出显示 | 界面和终端 | Any file |
| [`taskOutputMaxChars`](#taskoutputmaxchars) | 在 v2.1.277 中删除，以及它调整大小的 `TaskOutput` 工具 | 内存和上下文 | Any file |
| [`teammateDefaultModel`](#teammatedefaultmodel) | 在 v2.1.234 中删除；请参阅[指定队友和模型](/docs/zh-CN/agent-teams#specify-teammates-and-models)了解 Claude Code 如何选择队友的模型 | 全局配置设置 | Global config |
| [`teammateMode`](#teammatemode) | 选择[代理团队队友显示](/docs/zh-CN/agent-teams#choose-a-display-mode)的方式 | 代理、会话和工作树 | Any file |
| [`terminalProgressBarEnabled`](#terminalprogressbarenabled) | 在支持它的终端中隐藏终端进度条 | 界面和终端 | Any file |
| [`terminalTitleFromRename`](#terminaltitlefromrename) | 停止 [`/rename`](/docs/zh-CN/sessions#name-your-sessions) 和 `--name` 更改终端选项卡标题 | 界面和终端 | Any file |
| [`theme`](#theme) | 选择界面[颜色主题](/docs/zh-CN/terminal-config#match-the-color-theme)，内置或自定义 | 界面和终端 | Any file |
| [`timeFormat`](#timeformat) | 在 12 小时或 24 小时制、UTC 或 strftime 模式下显示界面中的时间 | 界面和终端 | Any file |
| [`timeZone`](#timezone) | 在时区而不是系统时区显示界面中的时间 | 界面和终端 | Any file |
| [`tui`](#tui) | 选择[全屏](/docs/zh-CN/fullscreen)或经典终端渲染器 | 界面和终端 | Any file |
| [`ultracode`](#ultracode) | 让 Claude 为每个实质性任务规划[工作流](/docs/zh-CN/workflows#let-claude-decide-with-ultracode)而无需被要求 | 模型和响应 | Any file |
| [`useAutoModeDuringPlan`](#useautomodeduringplan) | 让[自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)分类器在[计划模式](/docs/zh-CN/permission-modes#analyze-before-you-edit-with-plan-mode)中审查 shell 命令；设置 `false` 以获取提示 | 权限设置 | User, local, or managed |
| [`verbose`](#verbose) | 显示[完整工具输出](/docs/zh-CN/cli-reference#cli-flags)而不是截断的摘要；当两者都设置时 `viewMode` 优先 | 界面和终端 | Any file |
| [`viewMode`](#viewmode) | 在[默认、详细或焦点视图](/docs/zh-CN/cli-reference#cli-flags)中启动每个会话 | 界面和终端 | Any file |
| [`vimInsertModeRemaps`](#viminsertmoderemaps) | 将两键 [INSERT 模式序列](/docs/zh-CN/interactive-mode#remap-insert-mode-key-sequences)（如 `jj`）映射到 Escape | 界面和终端 | User or managed |
| [`voice`](#voice) | 打开[语音听写](/docs/zh-CN/voice-dictation)并选择按住或点击模式 | 界面和终端 | Any file |
| [`voiceEnabled`](#voiceenabled) | 使用较旧的单键形式打开[语音听写](/docs/zh-CN/voice-dictation) | 界面和终端 | Any file |
| [`wheelScrollAccelerationEnabled`](#wheelscrollaccelerationenabled) | 在全屏渲染中关闭[鼠标滚轮加速](/docs/zh-CN/fullscreen#mouse-wheel-scrolling) | 界面和终端 | Any file |
| [`workflowKeywordTriggerEnabled`](#workflowkeywordtriggerenabled) | 让提示中的单词 `ultracode` 启动[工作流](/docs/zh-CN/workflows)；设置 `false` 以在不启动的情况下键入它 | Hooks 和自动化 | Any file |
| [`workflowSizeGuideline`](#workflowsizeguideline) | 设置 Claude 在[动态工作流](/docs/zh-CN/workflows)中的目标代理数 | Hooks 和自动化 | Any file |
| [`worktree`](#worktree) | 配置 Claude Code 如何创建 git [worktrees](/docs/zh-CN/worktrees) | 代理、会话和工作树 | Any file |
| [`worktree.baseRef`](#worktree-baseref) | 从远程默认分支或本地 HEAD 分支新[worktrees](/docs/zh-CN/worktrees) | 代理、会话和工作树 | Any file |
| [`worktree.bgIsolation`](#worktree-bgisolation) | 让后台会话编辑工作副本而无需[worktree](/docs/zh-CN/worktrees) | 代理、会话和工作树 | Any file |
| [`worktree.sparsePaths`](#worktree-sparsepaths) | 在每个[worktree](/docs/zh-CN/worktrees)中仅检出您需要的目录 | 代理、会话和工作树 | Any file |
| [`worktree.symlinkDirectories`](#worktree-symlinkdirectories) | 将大型目录符号链接到每个[worktree](/docs/zh-CN/worktrees)中，而不是复制它们 | 代理、会话和工作树 | Any file |
| [`wslInheritsWindowsSettings`](#wslinheritswindowssettings) | 让 WSL 从 Windows 策略链读取[托管设置](/docs/zh-CN/managed-settings) | 企业和托管设置 | Managed |

<h2 id="model-and-responses">
  模型和响应
</h2>

选择 Claude Code 使用的模型以及它如何响应。关于这些设置如何与 `/model` 命令和环境变量交互，请参阅[模型配置](/docs/zh-CN/model-config)。

<h3 id="advisormodel">
  `advisorModel`
</h3>

选择当 Claude 调用服务器端[顾问工具](/docs/zh-CN/advisor)时哪个模型来回答。取消设置它以关闭顾问。顾问的能力必须至少与您的主模型一样强。请参阅[选择顾问模型](/docs/zh-CN/advisor#choose-an-advisor-model)了解接受的配对以及选择未被接受的配对时会发生什么。

您通常不会手动编辑此键。运行 `/advisor` 打开一个选择器，显示当前选择、可以提供建议的模型和**无顾问**。Claude Code 将您的选择保存到 `~/.claude/settings.json` 中的此键。如果您从[远程控制](/docs/zh-CN/remote-control)客户端或在附加到远程工作者的会话中选择，该选择仅适用于该会话，不会更改此键。

如果您的账户需要[使用额度同意](/docs/zh-CN/advisor#fable-advisor-and-usage-credits)，请先通过运行 `/model fable` 来接受它。在您这样做之前，在 `/advisor` 中选择 Fable 不会保存任何内容，Claude Code 会告诉您先运行 `/model fable`。

* **Scope**: [`Any file`](#scopes)
* **Type**: string，其中一个别名 `"fable"`、`"opus"` 或 `"sonnet"`，它们解析为 Claude Code 当前默认版本的该模型系列，或完整模型 ID，如 `"claude-opus-5-5"`
* **Default**: 未设置，因此顾问已关闭
* **Per-session overrides**: `--advisor` 对此键优先一个会话。[`CLAUDE_CODE_DISABLE_ADVISOR_TOOL`](/docs/zh-CN/env-vars)关闭顾问，此键无法将其重新打开

```json settings.json theme={null}
{
  "advisorModel": "opus"
}
```

该键对顾问[不可用](/docs/zh-CN/advisor#requirements)的提供商（如 Amazon Bedrock 和 AWS 上的 Claude Platform）没有影响。`"fable"` 需要[Fable 访问权限](/docs/zh-CN/advisor#choose-an-advisor-model)。

<h3 id="alwaysthinkingenabled">
  `alwaysThinkingEnabled`
</h3>

通过将其设置为 `false` 来为每个会话关闭[扩展思考](/docs/zh-CN/model-config#extended-thinking)。默认情况下思考是打开的，所以 `true` 不会改变任何内容。大多数人通过 `/config` 而不是编辑文件来设置这个。

在总是思考的模型上，如 Opus 5.5、Sonnet 5.5、Haiku 5.5 和 Fable 模型，`false` 没有效果。在[第三方提供商](/docs/zh-CN/third-party-integrations)上，Claude Code 省略 `thinking` 参数而不是关闭思考，因此自适应推理模型可能仍然会思考。在 Anthropic API 上关闭思考时，对于 Claude Code 已知[不接受该组合](/docs/zh-CN/errors#effort-isnt-available-with-thinking-turned-off)的模型（如 Opus 5），Claude Code 会发送 effort `high` 而不是更高级别。

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`: 无效果；思考已经打开
  * `false`: Claude Code 为每个会话关闭扩展思考
* **Default**: 未设置，因此对于支持它的模型，思考是打开的
* **Per-session overrides**: [`MAX_THINKING_TOKENS`](/docs/zh-CN/env-vars)对此键优先一个会话：`0` 关闭思考，在与 `false` 相同的模型和提供商限制下，正值打开思考，即使此键是 `false`。在自适应推理模型上，数字本身被忽略

```json settings.json theme={null}
{
  "alwaysThinkingEnabled": false
}
```

<h3 id="availablemodels">
  `availableModels`
</h3>

限制人们可以为主会话、[subagents](/docs/zh-CN/sub-agents)、[skills](/docs/zh-CN/skills) 和[顾问](/docs/zh-CN/advisor)选择的模型。托管列表限制 `/model`、`--model` 和开发人员自己文件中的 `model` 键；列表外的模型无法选择。使用默认前缀匹配，这不会单独触及默认选项；将其与[`enforceAvailableModels`](#enforceavailablemodels)配对以实现这一点。

* **Scope**: [`Any file`](#scopes)。在托管设置中部署它以为组织强制执行。
* **Type**: 模型别名或 ID 的数组
* **Default**: 未设置，因此每个模型都可用

此示例仅允许人们选择 Sonnet 和 Haiku 模型：

```json settings.json theme={null}
{
  "availableModels": ["sonnet", "haiku"]
}
```

模型 ID 条目（如 `"claude-opus-5"`）也允许扩展它的更高版本，如 Opus 5.5。要阻止其中一个版本，请使用[`deniedModels`](#deniedmodels)。要使每个模型 ID 条目仅允许它命名的版本，请使用[`availableModelsMatch`](#availablemodelsmatch)。请参阅[限制模型选择](/docs/zh-CN/model-config#restrict-model-selection)。

<h3 id="availablemodelsmatch">
  `availableModelsMatch`
</h3>

选择[`availableModels`](#availablemodels)条目如何匹配模型 ID。默认情况下，模型 ID 条目也允许扩展它的更高版本，因此 `"claude-opus-5"` 允许 Opus 5.5。使用 `"exact"`，每个模型 ID 条目仅允许它命名的版本，因此该模型的更高版本保持阻止状态，直到您列出它。需要 Claude Code v2.1.283 或更高版本。

* **Scope**: [`Managed`](#scopes)。Claude Code 在用户、项目和本地设置以及 `--settings` 中忽略该键，并显示警告
* **Type**: string，其中一个：
  * `"prefix"`: 模型 ID 条目允许其版本和任何用另一个段扩展它的模型 ID
  * `"exact"`: 模型 ID 条目仅允许它命名的版本，包括该版本的日期 ID，因此 `"claude-opus-5"` 允许 Opus 5 但不允许 `claude-opus-5-5`。系列别名如 `"opus"` 仍然允许整个系列，`best`、`opusplan` 和 `default` 条目被忽略
* **Default**: `"prefix"`

此示例允许 Opus 5 和 Sonnet 5，不允许任何更高版本：

```json managed-settings.json theme={null}
{
  "availableModels": ["claude-opus-5", "claude-sonnet-5"],
  "availableModelsMatch": "exact"
}
```

使用 `"exact"`，当列表至少命名一个模型或系列时，默认选项也限制为列出的模型。请参阅[阻止特定模型或版本](/docs/zh-CN/model-config#block-specific-models-or-versions)。

<h3 id="deniedmodels">
  `deniedModels`
</h3>

阻止特定模型，无论是否有[`availableModels`](#availablemodels)允许列表，即使该列表允许它们。Claude Code 从 `/model` 选择器中隐藏被阻止的模型，该模型无法在强制执行 `availableModels` 的任何地方选择。默认选项上的会话也不会运行被阻止的模型，如[阻止特定模型或版本](/docs/zh-CN/model-config#block-specific-models-or-versions)所述。需要 Claude Code v2.1.283 或更高版本。

* **Scope**: [`Managed`](#scopes)。Claude Code 在用户、项目和本地设置以及 `--settings` 中忽略该键，并显示警告
* **Type**: 模型别名或 ID 的数组
  * 系列别名如 `"opus"` 阻止该系列中的每个模型
  * 模型 ID 如 `"claude-opus-5-5"` 在每种拼写中阻止该版本，包括日期和提供商特定 ID
  * 没有次要版本的模型 ID，如 `"claude-opus-5"`，也阻止更高的次要版本，如 Opus 5.5。写 `"claude-opus-5-0"` 仅阻止 Opus 5
  * `best`、`opusplan` 和 `default` 条目被忽略
* **Default**: 未设置，因此没有模型被阻止

此示例允许 Opus 和 Sonnet 模型并阻止 Opus 5.5：

```json managed-settings.json theme={null}
{
  "availableModels": ["opus", "sonnet"],
  "deniedModels": ["claude-opus-5-5"]
}
```

请参阅[阻止特定模型或版本](/docs/zh-CN/model-config#block-specific-models-or-versions)。

<h3 id="effortlevel">
  `effortLevel`
</h3>

为您尚未保存级别的模型设置默认[努力级别](/docs/zh-CN/model-config#adjust-effort-level)。较低的级别在直接任务上更快且更便宜，较高的级别在复杂问题上推理更深入。

当您在您的机器上的交互式会话中运行 `/effort low`、`medium`、`high` 或 `xhigh` 时，Claude Code 将该级别保存在[`modelSettings`](#modelsettings)下的活动模型下，而不是写入此键。在 v2.1.251 之前，`/effort` 写入此键。

在同一设置文件中，Claude Code 使用模型的保存级别而不是此键。[`modelSettings`](#modelsettings)说明跨文件优先级。

在附加到远程工作者的会话中、在 `-p` 运行中以及在 Agent SDK 中，`/effort` 仅适用于该会话。[调整努力级别](/docs/zh-CN/model-config#adjust-effort-level)列出也仅适用于该会话的交互式选择。`/effort` 打印的消息说明发生了什么。

* **Scope**: [`Any file`](#scopes)
* **Type**: string，其中一个：
  * `"low"`: 最少推理，用于短的、范围内的、延迟敏感的、不是智能敏感的任务
  * `"medium"`: 减少成本敏感工作的令牌使用，可以权衡一些智能
  * `"high"`: 平衡令牌使用和智能
  * `"xhigh"`: 更深入的推理，更高的令牌支出
* **Default**: 未设置
* **Per-session overrides**: `--effort` 对此键优先一个会话，[`CLAUDE_CODE_EFFORT_LEVEL`](/docs/zh-CN/env-vars)对两者都优先

```json settings.json theme={null}
{
  "effortLevel": "xhigh"
}
```

在您的用户设置文件 `~/.claude/settings.json` 中，此键是 `/effort` 在保存每个模型的级别之前写入的较旧形式，它继续在之前应用的地方应用，在 Opus 5、Fable 5.1 和更早的模型上。Opus 5.5 和之后发布的模型忽略它，并从它们自己的默认值开始，直到您为它们保存一个级别，`/effort` 在[`modelSettings`](#modelsettings)下写入。在项目、本地和托管设置中，以及使用 `--settings` 时，此键适用于每个模型。

<h3 id="enforceavailablemodels">
  `enforceAvailableModels`
</h3>

`/model` 选择器有一个**默认**选项，[`default` 模型设置](/docs/zh-CN/model-config#default-model-setting)描述它解析为的模型。[`availableModels`](#availablemodels)允许列表限制您可以命名的模型，但使用默认[前缀匹配](#availablemodelsmatch)它不会单独重新映射您的账户类型的默认值，因此**默认**仍然可以解析为列表外的模型。此键关闭该间隙。需要 Claude Code v2.1.175 或更高版本。

当您的组织部署任何托管设置时，Claude Code 仅从托管源读取此键，并在您的其他文件中忽略它。

关于此键如何应用于启动时的模型检查，请参阅 [Amazon Bedrock](/docs/zh-CN/amazon-bedrock#when-your-organization-enforces-a-model-allowlist) 和 [Google Cloud 的 Agent Platform](/docs/zh-CN/google-vertex-ai#when-your-organization-enforces-a-model-allowlist)。

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`: 当**默认**会解析为 `availableModels` 外的模型时，Claude Code 将其解析为列表中第一个可用的模型
  * `false`: 此键不改变**默认**的解析方式
* **Default**: `false`

此示例将命名选择限制为 Sonnet 和 Haiku 模型，并使**默认**解析为其中第一个可用的：

```json settings.json theme={null}
{
  "availableModels": ["sonnet", "haiku"],
  "enforceAvailableModels": true
}
```

当 `availableModels` 未设置或为空时，此键没有效果。请参阅[为默认模型强制执行允许列表](/docs/zh-CN/model-config#enforce-the-allowlist-for-the-default-model)。需要 Claude Code v2.1.175 或更高版本。

<h3 id="fallbackmodel">
  `fallbackModel`
</h3>

命名备用模型供 Claude Code 在您的主模型过载或不可用时按顺序尝试。Claude Code 为该轮的其余部分切换到链中下一个可用的模型，并显示通知。没有链的情况下，Claude Code 重试同一模型，然后显示服务器的错误，您重试或自己切换模型。

切换意味着在备用模型上进行一轮冷[提示缓存](/docs/zh-CN/prompt-caching#switching-models)；您的下一条消息首先再次尝试主模型。

* **Scope**: [`Any file`](#scopes)
* **Type**: 模型别名或 ID 的数组；`"default"` 扩展为默认模型
* **Default**: 未设置，因此失败的请求不会在另一个模型上重试
* **Per-session overrides**: `--fallback-model` 对此键优先一个会话

此示例在您的主模型失败时首先尝试 Sonnet 5，然后尝试 Haiku 4.5：

```json settings.json theme={null}
{
  "fallbackModel": ["claude-sonnet-5", "claude-haiku-4-5"]
}
```

与大多数数组设置不同，此键不跨设置文件合并：最高优先级文件定义它提供整个链。如果您的项目文件设置 `["claude-sonnet-5"]` 而您的用户文件设置 `["claude-haiku-4-5"]`，链是 `["claude-sonnet-5"]` 仅。Claude Code 从列表中最多保留三个不同的允许模型，忽略其余的。请参阅[备用模型链](/docs/zh-CN/model-config#fallback-model-chains)。

<h3 id="fastmode">
  `fastMode`
</h3>

为可用的会话打开[快速模式](/docs/zh-CN/fast-mode)，用于交互式工作，如快速迭代或实时调试，您希望以更高的每令牌成本获得速度。您通常不会手动编辑此键：运行 `/fast` 将 `fastMode: true` 写入 `~/.claude/settings.json`，再次运行它以关闭快速模式会删除该键。快速模式仅在 Opus 5.5、Opus 5 和 Opus 4.8 上运行：从另一个模型打开它会切换您到 Opus，切换到不支持的模型会关闭它。请参阅[在快速模式打开时切换模型](/docs/zh-CN/fast-mode#switch-models-while-fast-mode-is-on)。

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`: Claude Code 为可用的会话打开快速模式
  * `false`: 快速模式保持关闭
* **Default**: 未设置，因此快速模式已关闭
* **Per-session overrides**: [`CLAUDE_CODE_DISABLE_FAST_MODE`](/docs/zh-CN/env-vars)为一个会话关闭快速模式，此键无法将其重新打开

```json settings.json theme={null}
{
  "fastMode": true
}
```

<h3 id="fastmodepersessionoptin">
  `fastModePerSessionOptIn`
</h3>

通常，运行 `/fast` 将[`fastMode`](#fastmode)保存到一个人的用户设置，因此快速模式在之后每个会话的开始时打开。将此键设置为 `true` 以停止这种情况：保存的 `fastMode: true` 不再在会话开始时打开快速模式，每个人必须在他们想要它的每个会话中运行 `/fast`。Claude Code 在他们的文件中保留 `fastMode` 键，因此关闭此键会恢复旧行为。

Team 或 Enterprise 计划的所有者可以通过[服务器托管设置](/docs/zh-CN/server-managed-settings)在组织范围内部署它。当托管设置设置该键时，`/fast on` 在交互式终端会话外被拒绝，并报告您的组织已禁用快速模式。这涵盖[非交互式模式](/docs/zh-CN/headless)、[VS Code 扩展](/docs/zh-CN/vs-code)和[云会话](/docs/zh-CN/claude-code-on-the-web)。

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`: 保存的 `fastMode: true` 不再在会话开始时打开快速模式，因此每个人在他们想要它的每个会话中运行 `/fast`；使用 `--settings` 传递的 `fastMode: true` 仍然对该会话计数，除非托管设置设置此键
  * `false`: 保存的 `fastMode: true` 在之后每个会话的开始时打开快速模式
* **Default**: `false`

```json settings.json theme={null}
{
  "fastModePerSessionOptIn": true
}
```

请参阅[需要每个会话的选择加入](/docs/zh-CN/fast-mode#require-per-session-opt-in)。

<h3 id="language">
  `language`
</h3>

默认情况下让 Claude 用英语以外的语言响应。响应没有固定列表：Claude Code 将值逐字传递给 Claude 作为始终用该语言响应的指令，因此任何 Claude 可以读取的语言名称都有效。Claude Code 不检查该值，因此拼写错误的名称按原样到达 Claude，而不是产生错误。相同的值为[语音听写](/docs/zh-CN/voice-dictation#change-the-dictation-language)设置语言，它有一个固定的[支持的听写语言](/docs/zh-CN/voice-dictation#change-the-dictation-language)列表，以及自动生成的会话标题。

* **Scope**: [`Any file`](#scopes)
* **Type**: string，任何语言名称，如 `"japanese"`、`"spanish"` 或 `"french"`；Claude Code 不验证它
* **Default**: 未设置；会话标题然后匹配您的对话语言

```json settings.json theme={null}
{
  "language": "japanese"
}
```

<h3 id="maxeffortlevel">
  `maxEffortLevel`
</h3>

限制会话可以使用的[努力级别](/docs/zh-CN/model-config#adjust-effort-level)，保留较低的级别可用。任何更高的级别都在上限处运行，包括来自 `/effort`、`/model` 选择器、`--effort`、[`CLAUDE_CODE_EFFORT_LEVEL`](/docs/zh-CN/env-vars)、skill 或 subagent 的 `effort` frontmatter 或模型自己的默认值。Claude Code 在每个请求之前自己应用上限，因此它在每个提供商上保持，包括 Amazon Bedrock、Google Cloud 的 Agent Platform 和 Microsoft Foundry。需要 Claude Code v2.1.267 或更高版本。

* **Scope**: [`Any file`](#scopes)。在托管设置中部署它以为组织强制执行。当多个范围设置上限时，最低的适用，因此在一个范围中设置的上限无法从另一个范围提高
* **Type**: string，其中一个 `"low"`、`"medium"`、`"high"`、`"xhigh"` 或 `"max"`。`"max"` 值设置无上限
* **Default**: 未设置，因此无上限适用
* **Per-model caps**: 将 `maxEffortLevel` 添加到模型的[`modelSettings`](#modelsettings)条目。该条目在设置两者的设置源（如您的用户设置或一个[托管源](/docs/zh-CN/managed-settings#how-claude-code-combines-managed-sources)）中仅替换该模型的此键。在那里设置 `"max"` 以豁免该模型免受该源的上限；Claude Code 仍然应用来自其他源的上限

此示例将每个模型限制在 `medium`，并豁免 Sonnet 4.6：

```json settings.json theme={null}
{
  "maxEffortLevel": "medium",
  "modelSettings": {
    "claude-sonnet-4-6": {
      "maxEffortLevel": "max"
    }
  }
}
```

当您的组织也为模型设置[努力限制](/docs/zh-CN/model-config#organization-effort-limits)时，两个上限中较低的适用。

<h3 id="model">
  `model`
</h3>

设置每个新会话使用的模型，因此您不必每次都用 `/model` 选择一个。在此处设置它不会阻止您在会话中期切换。如果您的管理员设置了[组织默认模型](/docs/zh-CN/model-config#organization-default-model)以覆盖用户选择，即使您在用户、项目或本地设置中设置此键，您也会获得该模型。

* **Scope**: [`Any file`](#scopes)
* **Type**: string，模型别名或完整模型 ID
* **Default**: 未设置，因此 Claude Code 使用您账户的默认模型
* **Per-session overrides**: `--model` 优先于[`ANTHROPIC_MODEL`](/docs/zh-CN/env-vars)，两者都优先于此键一个会话，包括优先于托管 `model`；[`availableModels`](#availablemodels)列表仍然适用于选择

```json settings.json theme={null}
{
  "model": "claude-sonnet-5"
}
```

此处的值优先于[`ANTHROPIC_DEFAULT_MODEL`](/docs/zh-CN/model-config#set-a-default-model-for-new-sessions)，Claude Code 仅在没有其他内容选择模型时使用。

<h3 id="modeloverrides">
  `modelOverrides`
</h3>

将 Anthropic 模型 ID 映射到提供商特定的模型 ID，如 Amazon Bedrock 推理配置文件 ARN。每个模型选择器条目然后在调用提供商 API 时使用其映射值。管理员在[Amazon Bedrock、Google Cloud 的 Agent Platform 和 Microsoft Foundry](/docs/zh-CN/model-config#override-model-ids-per-version)上使用这个来将每个模型版本路由到特定的推理配置文件、版本名称或部署，以实现治理、成本分配或区域路由。

* **Scope**: [`Any file`](#scopes)
* **Type**: 将模型 ID 映射到提供商模型 ID 的对象
* **Default**: 未设置

此示例将 Opus 4.6 的每个调用路由到命名的 Bedrock 推理配置文件：

```json settings.json theme={null}
{
  "modelOverrides": {
    "claude-opus-4-6": "arn:aws:bedrock:us-east-1:123456789012:inference-profile/example"
  }
}
```

请参阅[按版本覆盖模型 ID](/docs/zh-CN/model-config#override-model-ids-per-version)。

<h3 id="modelpicker">
  `modelPicker`
</h3>

列出 `/model` 选择器提供的模型，按您写入它们的顺序和您选择的标签下，因此选择器列出您的组织运行的模型，在内置阵容之后或代替它。每行的 `model` 逐字获取，因此它接受 `--model` 接受的任何内容：别名如 `opus`、Anthropic 模型 ID 或 Amazon Bedrock、Google Cloud 的 Agent Platform、Microsoft Foundry 或 LLM 网关的提供商格式 ID。需要 Claude Code v2.1.242 或更高版本。

* **Scope**: [`User or managed`](#scopes)。Claude Code 从托管设置、`--settings` 和用户设置读取该键，并在项目和本地设置中忽略它，因此您克隆的存储库无法重新标记选择器。这三个中最高的设置该键提供整个阵容，Claude Code 从不合并来自两个源的阵容。
* **Type**: 带有 `options` 数组的对象和可选的 `replaceBuiltInOptions` Boolean
* **Default**: 未设置，因此选择器显示内置阵容

此示例在内置阵容之后添加两个 Bedrock 部署，在您的团队识别的名称下：

```json managed-settings.json theme={null}
{
  "modelPicker": {
    "options": [
      { "model": "us.anthropic.claude-opus-4-8", "label": "Opus (production)" },
      {
        "model": "us.anthropic.claude-sonnet-4-6",
        "label": "Sonnet (production)",
        "description": "Day-to-day work"
      }
    ]
  }
}
```

<span id="modelpicker-options" />

<span id="modelpicker-replacebuiltinoptions" />

<h4 id="fields-for-modelpicker">
  `modelPicker` 的字段
</h4>

该键有两个字段，一个用于行本身，一个用于它们是替换内置阵容还是添加到它。

| Field | Type | What it does |
| :- | :- | :- |
| `options` | 行的数组，每个都有必需的 `model` 和可选的 `label`、`description` 和 `behavesAs` | 选择器显示的行，按此顺序，除了灰显的行移到底部。没有 `label`，Claude Code 用它知道的模型的内置名称标记行，或模型 ID 否则，没有 `description` 它写一个通用的第二行 |
| `replaceBuiltInOptions` | Boolean，默认 `false` | 将其设置为 `true` 以仅显示这些行、**默认**和会话已在使用的模型的行。保留未设置以在内置阵容之后添加这些行 |

`options` 中的条目也可以在其 `model` 旁边携带可选的 `behavesAs` 字符串，需要 v2.1.257 或更高版本。将其设置为您的 Claude Code 版本已知的模型的 ID，如 `claude-opus-4-8`，在其 `model` 比您的版本更新的条目上。Claude Code 然后将该已知模型的能力和努力默认值应用于条目，而不是将其模型视为未知。条目的标签和 Claude Code 在请求中发送的模型 ID 不改变。

使用 `replaceBuiltInOptions` 打开时，Claude Code 隐藏每个其他行：内置阵容、它为[`availableModels`](#availablemodels)条目添加的行、[网关发现](/docs/zh-CN/llm-gateway-protocol#model-discovery)找到的模型和[`ANTHROPIC_CUSTOM_MODEL_OPTION`](/docs/zh-CN/model-config#add-a-custom-model-option)。关闭时，Claude Code 跳过内置阵容已覆盖的列出的模型。标签改变选择器显示的内容，而不是 Claude Code 运行的模型。

[`availableModels`](#availablemodels)允许列表仍然适用于这些行。在将列出的模型添加到允许列表之前，请阅读[合并行为](/docs/zh-CN/model-config#merge-behavior)：特定模型 ID 缩小其系列的通配符条目。Claude Code 也在显示选择器之前检查每行与会话：

* **Dropped**: Claude Code 无法提供的行，如已退休的模型或您的组织无权访问的模型
* **Grayed out**: 您还无法选择的行，显示原因
* **No row survives**: Claude Code 保留内置阵容，按允许列表过滤如常

Claude Code 删除它无法解析的行，保留其余的。请参阅[修复损坏的设置文件](/docs/zh-CN/settings#fix-a-broken-settings-file)。

<h3 id="modelpricing">
  `modelPricing`
</h3>

按您的组织支付的费率而不是列表价格报告支出。当您的组织有合同费率时设置它，因此开发人员看到的美元数字与您的账单匹配。Claude Code 在 `/usage`、[状态行](/docs/zh-CN/statusline)、Agent SDK 的 `total_cost_usd`、[`--max-budget-usd`](/docs/zh-CN/cli-reference)限制和[OpenTelemetry](/docs/zh-CN/monitoring-usage)成本指标和事件中应用费率。您提供费率：Claude Code 不从您的合同或 Claude Console 读取它们。需要 Claude Code v2.1.242 或更高版本。

* **Scope**: [`Managed`](#scopes)。通过服务器托管设置、MDM 策略、`managed-settings.json` 文件或[策略助手](/docs/zh-CN/managed-settings#compute-the-policy-with-a-helper-program)部署该键。Claude Code 在用户、项目和本地设置、`--settings` 中忽略它，在 Windows 中的用户可写[HKCU 注册表](/docs/zh-CN/managed-settings#where-each-mechanism-stores-the-policy)中忽略它。使用服务器托管设置，每个会话以列表价格报告成本，直到该会话的[设置获取](/docs/zh-CN/server-managed-settings#fetch-and-caching-behavior)已确认该设置。嵌入 Claude Code 并设置[`CLAUDE_CODE_PROVIDER_MANAGED_BY_HOST`](/docs/zh-CN/env-vars)的主机应用可以通过 SDK [`managedSettings`](/docs/zh-CN/agent-sdk/typescript#options)选项提供自己的表，Claude Code 仅在没有托管源设置该键时使用，仅在 Claude Code v2.1.246 或更高版本中。
* **Type**: 带有可选 `multiplier` 和可选 `overrides` 映射的对象
* **Default**: 未设置，因此 Claude Code 报告列表价格，除非主机应用提供表

单独设置 `multiplier` 以获得统一折扣或加价，单独设置 `overrides` 以获得每个模型费率，或两者都设置。

此示例为 Sonnet 4.6 设置合同费率，然后将每个数字（包括 Sonnet 行）减少 15%：

```json managed-settings.json theme={null}
{
  "modelPricing": {
    "multiplier": 0.85,
    "overrides": {
      "claude-sonnet-4-6": {
        "input": 2.4,
        "output": 12,
        "cacheRead": 0.24,
        "cacheWrite": 3
      }
    }
  }
}
```

将 `multiplier` 设置为 1 以上，最多 10，以标记每个数字。加价需要 Claude Code v2.1.271 或更高版本。更早的版本忽略 `multiplier` 高于 1 的警告，保留设置的其余部分。

有关步骤，包括如何确认费率有效，请参阅[按您的合同费率报告支出](/docs/zh-CN/costs#report-spend-at-your-contracted-rates)。

<span id="modelpricing-multiplier" />

<span id="modelpricing-overrides" />

<h4 id="fields-for-modelpricing">
  `modelPricing` 的字段
</h4>

| Field | Type | What it does |
| :- | :- | :- |
| `multiplier` | 大于 0 且最多 10 的数字 | 缩放 Claude Code 计算的每个成本，无论 `overrides` 行是否覆盖它。低于 1 是折扣，高于 1 是加价 |
| `overrides` | 模型 ID 到具有 `input`、`output`、`cacheRead` 和 `cacheWrite` 的费率对象的映射，每个 0 到 10000 | 该模型的美元每百万令牌费率，全部四个必需。`cacheWrite` 涵盖五分钟和一小时缓存写入。请参阅[`modelPricing` 行适用于哪些模型](#which-models-a-modelpricing-row-applies-to) |

Claude Code 完全按照您写入的方式使用行的费率，不添加快速模式附加费或[仅限美国推理费率](https://platform.claude.com/docs/en/about-claude/pricing)。如果您也设置 `multiplier`，Claude Code 在行的费率之上应用它。Claude Code 删除具有它无法解析的费率或 `multiplier` 的行，保留其余的；请参阅[修复损坏的设置文件](/docs/zh-CN/settings#fix-a-broken-settings-file)。

<h4 id="which-models-a-modelpricing-row-applies-to">
  `modelPricing` 行适用于哪些模型
</h4>

Claude Code 从行的键决定行适用于哪些模型：

* **内置模型的 ID**: Claude Code 本身为内置模型使用的键，无论该键是模型自己的 ID，如 `claude-sonnet-4-6`，还是其 Bedrock、Agent Platform 或 Foundry ID。Claude Code 将行应用于该模型的每个日期快照 ID 和提供商特定 ID。
* **任何其他键**: 不是内置模型 ID 的键，如网关模型别名。Claude Code 仅将行应用于该一个 ID。当模型 ID 完全匹配您的一个键，也落在由内置模型 ID 键的行下时，Claude Code 使用精确匹配。
* **Bedrock 应用推理配置文件**: 一旦 Claude Code 通过您的[`modelOverrides`](#modeloverrides)映射或[`bedrock:GetInferenceProfile` 查找](/docs/zh-CN/amazon-bedrock#iam-configuration)将配置文件解析为它路由到的模型，Claude Code 将该模型的行应用于配置文件。

<h3 id="modelsettings">
  `modelSettings`
</h3>

为您使用的每个模型保存[努力级别](/docs/zh-CN/model-config#adjust-effort-level)。需要 Claude Code v2.1.251 或更高版本。

在您机器上的交互式会话中，当您使用 `/effort` 或 `/model` 选择器的努力滑块将 `low`、`medium`、`high` 或 `xhigh` 保存为您的默认值时，Claude Code 在您使用的模型下在此处写入该级别，因此您很少自己编辑此键。当您在[VS Code 扩展的模型选择器](/docs/zh-CN/vs-code#use-the-prompt-box)中选择其中一个级别时，Claude Code 以相同的方式在此处保存它。[`effortLevel`](#effortlevel)条目列出 `/effort` 仅适用于该会话的会话。

手动编辑该键以更改或删除您保存的级别。

此处模型的 `effortLevel` 优先于同一设置文件中的顶级[`effortLevel`](#effortlevel)。跨文件，Claude Code 分别解析每个模型：最高优先级[设置文件](/docs/zh-CN/settings#settings-precedence)设置该模型的 `effortLevel` 或[适用于该模型](#effortlevel)的顶级 `effortLevel` 决定，因此托管设置中的 `effortLevel` 优先于您在用户设置中保存的级别。[调整努力级别](/docs/zh-CN/model-config#adjust-effort-level)列出还可以覆盖保存级别的内容，如启动时的 `--effort`。

要限制一个模型的努力而不是设置其级别，将[`maxEffortLevel`](#maxeffortlevel)字段添加到该模型的条目。该字段需要 Claude Code v2.1.267 或更高版本。

* **Scope**: [`Any file`](#scopes)
* **Type**: 将模型名称映射到对象的对象，该对象可包含以下任意字段：
  * `effortLevel`: 其中一个 `"low"`、`"medium"`、`"high"` 或 `"xhigh"`
  * [`maxEffortLevel`](#maxeffortlevel): 该模型可以运行的最高 effort 级别
  * `autoCompactWindow`: 从 `100000` 到 `1000000` 的 token 数，或 `"auto"` 表示为该模型调优的窗口。[`/autocompact`](/docs/zh-CN/model-config#set-the-auto-compact-window) 保存到此处。对于该模型，该值优先于同一设置文件中的顶级 [`autoCompactWindow`](#autocompactwindow)。需要 Claude Code v2.1.288 或更高版本
* **Default**: 未设置

Claude Code 在模型的规范名称下写入每个条目，如 `claude-opus-5-5`，并将该模型的别名、日期后缀、`[1m]` 和识别的提供商特定 ID 匹配到同一条目。

此示例将 Opus 5.5 保持在 `high`，而其他模型使用它们自己的保存或默认级别：

```json settings.json theme={null}
{
  "modelSettings": {
    "claude-opus-5-5": {
      "effortLevel": "high"
    }
  }
}
```

运行 `/effort auto` 以清除您为正在使用的模型保存的级别。Claude Code 保留其他条目和任何顶级 `effortLevel`。

<h3 id="outputstyle">
  `outputStyle`
</h3>

按名称选择[输出样式](/docs/zh-CN/output-styles)。输出样式是一组保存的指令，改变 Claude 的角色、语气和输出格式，如内置的 Explanatory 和 Learning 样式或您自己写的。

如果您在会话期间更改此键，Claude 从您的下一条消息开始使用新样式。关于该消息在提示缓存中的成本，请参阅[更改输出样式](/docs/zh-CN/prompt-caching#changing-output-style)。在 v2.1.251 之前，编辑仅在您运行 `/clear` 或启动新会话后应用。

* **Scope**: [`Any file`](#scopes)
* **Type**: string，[内置](/docs/zh-CN/output-styles#built-in-output-styles)或[自定义](/docs/zh-CN/output-styles#create-a-custom-output-style)输出样式的名称
* **Default**: 未设置，因此 Claude Code 使用默认样式

此示例选择内置的 Explanatory 样式，它在任务之间添加教育见解：

```json settings.json theme={null}
{
  "outputStyle": "Explanatory"
}
```

<h3 id="promptcachettl">
  `promptCacheTtl`
</h3>

选择[提示缓存](/docs/zh-CN/prompt-caching)保持主对话的时间长度。此键适用于您的交互式、`-p` 和 Agent SDK 轮，以及 Claude Code 与它们内联运行的助手。一小时的生命周期在较长的中断中保持缓存温暖，API [在五分钟生命周期的更高费率下计费每个缓存写入](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#pricing)。需要 Claude Code v2.1.242 或更高版本。

* **Scope**: [`Any file`](#scopes)
* **Type**: string，其中一个：
  * `"5m"`: 缓存保持五分钟
  * `"1h"`: 缓存保持一小时
* **Default**: 未设置，因此每个主对话请求获得[其默认生命周期](/docs/zh-CN/prompt-caching#which-ttl-each-request-gets)
* **Per-session overrides**: [`FORCE_PROMPT_CACHING_5M`](/docs/zh-CN/env-vars)优先于所有其他，然后[`CLAUDE_CODE_PROMPT_CACHE_TTL`](/docs/zh-CN/env-vars)，然后此键，最后[`ENABLE_PROMPT_CACHING_1H`](/docs/zh-CN/env-vars)

此示例将主对话保持在一小时生命周期，并将 subagents 保留在五分钟：

```json settings.json theme={null}
{
  "promptCacheTtl": "1h",
  "subagentPromptCacheTtl": "5m"
}
```

关于每个生命周期的成本，请参阅[缓存生命周期](/docs/zh-CN/prompt-caching#cache-lifetime)。

<h3 id="showthinkingsummaries">
  `showThinkingSummaries`
</h3>

在交互式会话中查看 Claude 的[扩展思考](/docs/zh-CN/model-config#extended-thinking)摘要。如果您想在使用 `Ctrl+O` 展开思考时看到完整摘要，请设置它。未设置或 `false` 时，Anthropic API 编辑思考块，Claude Code 显示折叠的存根；第三方提供商不编辑。

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`: 当您使用 `Ctrl+O` 展开思考时，您看到完整的思考摘要
  * `false`: Anthropic API 编辑思考块，Claude Code 显示折叠的存根
* **Default**: `false`

```json settings.json theme={null}
{
  "showThinkingSummaries": true
}
```

编辑仅改变您看到的内容，而不是模型生成的内容。要减少思考支出，[降低预算或禁用思考](/docs/zh-CN/model-config#extended-thinking)。

<h3 id="subagentpromptcachettl">
  `subagentPromptCacheTtl`
</h3>

选择[提示缓存](/docs/zh-CN/prompt-caching)保持 Claude Code 在主对话外进行的请求的时间长度。此键适用于[subagents](/docs/zh-CN/sub-agents)、[workflows](/docs/zh-CN/workflows) 和 Claude Code 自己的后台和助手请求，如压缩和会话标题。一小时的生命周期在较长的中断中保持缓存温暖，API [在五分钟生命周期的更高费率下计费每个缓存写入](https://platform.claude.com/docs/en/build-with-claude/prompt-caching#pricing)。需要 Claude Code v2.1.242 或更高版本。

* **Scope**: [`Any file`](#scopes)
* **Type**: string，其中一个：
  * `"5m"`: 缓存保持五分钟
  * `"1h"`: 缓存保持一小时
* **Default**: 未设置，因此这些请求中的每一个获得[其默认生命周期](/docs/zh-CN/prompt-caching#which-ttl-each-request-gets)
* **Per-session overrides**: [`FORCE_PROMPT_CACHING_5M`](/docs/zh-CN/env-vars)优先于所有其他，然后[`CLAUDE_CODE_SUBAGENT_PROMPT_CACHE_TTL`](/docs/zh-CN/env-vars)，然后此键，然后[`ENABLE_PROMPT_CACHING_1H`](/docs/zh-CN/env-vars)，它要求每个请求的一小时生命周期。关于 subagent 自己的 frontmatter 值的排名，请参阅[自己选择 TTL](/docs/zh-CN/prompt-caching#choose-the-ttl-yourself)

此示例为 subagents 和主对话外的其他请求提供一小时生命周期：

```json settings.json theme={null}
{
  "subagentPromptCacheTtl": "1h"
}
```

此键涵盖[`promptCacheTtl`](#promptcachettl)不涵盖的请求，因此设置两者以为 Claude Code 进行的每个请求选择生命周期。关于 subagent 的缓存与主对话的缓存的不同之处，请参阅[Subagents 和缓存](/docs/zh-CN/prompt-caching#subagents-and-the-cache)。

<h3 id="switchmodelsonflag">
  `switchModelsOnFlag`
</h3>

选择当[安全分类器标记请求](/docs/zh-CN/model-config#automatic-model-fallback)时会发生什么：切换到备用模型并继续，或暂停以便您可以在切换和编辑提示之间选择。

* **Scope**: [`Any file`](#scopes)。在 `/config` 中显示为 **Switch models when a message is flagged**，选项为 **Switch automatically** 和 **Ask each time**。
* **Type**: Boolean
  * `true`: Claude Code 切换到备用模型并继续
  * `false`: 在交互式会话中，Claude Code 暂停以便您可以在切换和编辑提示之间选择；在无法显示对话框的地方，如 `-p` 运行，标记的请求以错误结束
* **Default**: 未设置。Claude Code 会自动切换，但在交互式会话中可能会[先询问](/docs/zh-CN/model-config#ask-before-switching)

```json settings.json theme={null}
{
  "switchModelsOnFlag": false
}
```

请参阅[在切换前询问](/docs/zh-CN/model-config#ask-before-switching)。

<h3 id="ultracode">
  `ultracode`
</h3>

使用[ultracode](/docs/zh-CN/workflows#let-claude-decide-with-ultracode)启动会话。打开时，Claude 为每个实质性任务规划工作流，而不是等待您要求。Claude 仅在为您启用[动态工作流](/docs/zh-CN/workflows)且您的模型支持 `xhigh` 努力时规划工作流。该键不改变会话的努力级别：ultracode 在会话使用的任何级别处运行。Claude Code 读取此键但从不写入它：`/effort ultracode` 仅为当前会话打开 ultracode。

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`: 当为您启用动态工作流且您的模型支持 `xhigh` 时，会话以 ultracode 打开启动
  * `false`: 会话以 ultracode 关闭启动
* **Default**: 未设置，因此 ultracode 已关闭
* **Per-session overrides**: `/effort ultracode` 在没有此键的情况下为一个会话打开 ultracode，而当此键为 `true` 时，`/effort ultracode off` 为一个会话关闭它。`--effort ultracode` 标志也为一个会话打开它，在 `xhigh` 努力处，需要 Claude Code v2.1.203 或更高版本

```json settings.json theme={null}
{
  "ultracode": true
}
```

会话的努力级别来自[`effortLevel`](#effortlevel)、[`modelSettings`](#modelsettings) 和其他[努力源](/docs/zh-CN/model-config#adjust-effort-level)，[努力上限](/docs/zh-CN/model-config#organization-effort-limits)如[`maxEffortLevel`](#maxeffortlevel)降低该级别而不关闭 ultracode。这和 `/effort ultracode off` 形式需要 Claude Code v2.1.284 或更高版本。在 v2.1.284 之前，`ultracode: true` 在 `xhigh` 努力处运行会话，低于 `xhigh` 的努力上限使 ultracode 在上限适用的模型上不可用。Agent SDK `apply_flag_settings` 控制请求也接受该键。

<h2 id="permission-settings">
  权限设置
</h2>

决定 Claude 在不询问的情况下可以做什么、会话以哪种权限模式启动，以及自动模式的分类器允许什么。有关规则语法和权限模型，请参阅[配置权限](/docs/zh-CN/permissions)。

<h3 id="allowmanagedpermissionrulesonly">
  `allowManagedPermissionRulesOnly`
</h3>

使托管设置成为权限规则的唯一设置来源。Claude Code 随后会忽略用户、项目、本地和 `--settings` 文件中的 `allow`、`ask` 和 `deny` 规则，忽略 `--allowedTools`，隐藏权限提示中的始终允许选项，并停止保存新规则。

当[来自嵌入主机的父设置](/docs/zh-CN/managed-settings#let-an-embedding-host-add-policy)适用时，Claude Code 将其视为托管层的一部分。它删除其 `allow` 规则和 `additionalDirectories`，并保留其 `deny` 和 `ask` 规则，除了模式以 `!` 开头的 `Read` 和 `Edit` 规则。无论您是否设置此键，主机都无法使用 `!` 规则从托管规则中排除路径。

`--disallowedTools` 规则以及当前会话的 `deny` 和 `ask` 规则仍然适用，包括在 Claude Code 在会话中途重新加载设置后。它们仅限制，因此无法扩展托管规则授予的权限。在 v2.1.257 之前，Claude Code 在第一次设置重新加载时删除了这些命令行和会话规则。

有关 `--disallowedTools` 或会话规则中的 `!` 模式可以排除什么，请参阅 [Read 和 Edit 规则](/docs/zh-CN/permissions#read-and-edit)。

设置此键后，Claude Code v2.1.282 或更高版本还会忽略来自以下来源的 skill 和 `.claude/commands/` 文件中的 [`allowed-tools`](/docs/zh-CN/skills#pre-approve-tools-for-a-skill) frontmatter：

* 仓库的 `.claude/` 目录
* 您的 `~/.claude/skills/` 和 `~/.claude/commands/` 目录，包括[从 claude.ai 同步的 skill](/docs/zh-CN/skills#where-synced-skills-load)
* `--add-dir` 目录
* `~/.claude/skills/` 或项目的 `.claude/skills/` 中[使用 `.claude-plugin` 清单声明的插件](/docs/zh-CN/plugins/loading#plugins-shared-through-a-repository)

来自托管设置的 skill 和随附 skill 保留其 `allowed-tools`。skill 的 `disallowed-tools` 仍然适用。有关 Claude Code 忽略该字段时开发人员会看到什么，请参阅[仅应用托管权限规则时](/docs/zh-CN/skills#when-only-managed-permission-rules-apply)。

* **作用域**: [`Managed`](#scopes)
* **类型**: 布尔值
  * `true`: 托管设置成为权限规则的唯一设置来源
  * `false`: Claude Code 除了应用托管规则外，还应用来自用户、项目、本地和 `--settings` 文件的权限规则
* **默认值**: 未设置，因此 Claude Code 应用来自用户、项目和本地设置以及 `--settings` 的权限规则，以及托管规则

```json managed-settings.json theme={null}
{
  "allowManagedPermissionRulesOnly": true
}
```

此键不会锁定 MCP 服务器允许列表；为此，请设置 [`allowManagedMcpServersOnly`](#allowmanagedmcpserversonly)。请参阅[仅托管设置](/docs/zh-CN/managed-settings#managed-only-settings)。

<h3 id="automode">
  `autoMode`
</h3>

添加您自己的规则到[自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)分类器阻止和允许的内容。使用它告诉分类器您的组织信任哪些仓库、存储桶和域，以便它停止阻止常规内部操作。分类器附带[内置允许和拒绝规则](/docs/zh-CN/auto-mode-config#inspect-the-defaults-and-your-effective-config)。在数组中包含字面字符串 `"$defaults"` 以在该位置保留这些内置规则并在其周围添加您的规则；省略它以用您的规则替换它们。

* **作用域**: [`User or managed`](#scopes)
* **类型**: 包含 `environment`、`allow`、`soft_deny` 和 `hard_deny` 散文规则数组的对象，加上 [`classifyAllShell`](#automode-classifyallshell) 布尔值
* **默认值**: 未设置，因此分类器仅使用其[内置规则](/docs/zh-CN/auto-mode-config#inspect-the-defaults-and-your-effective-config)

此示例保留内置的 `soft_deny` 规则（通过 `"$defaults"`），并添加一个阻止 `terraform apply` 的规则：

```json settings.json theme={null}
{
  "autoMode": {
    "soft_deny": ["$defaults", "Never run terraform apply"]
  }
}
```

当多个文件设置相同的数组时，Claude Code 会连接这些条目。有关规则格式以及如何应用每个数组，请参阅[配置自动模式](/docs/zh-CN/auto-mode-config)。

<h3 id="automode-classifyallshell">
  `autoMode.classifyAllShell`
</h3>

在自动模式处于活动状态时，将每个 Bash 和 PowerShell 命令通过自动模式分类器。默认情况下，自动模式仅暂停可以运行任意代码的允许规则：工具范围和通配符规则（如 `Bash(*)`）以及解释器或 shell 包装器前缀（如 `Bash(python *)`）。任何其他允许规则匹配的命令（如 `Bash(npm test)`）会跳过分类器，除非它携带[每个命令允许的域](/docs/zh-CN/sandboxing#per-command-allowed-domains-in-auto-mode)。当它跳过时，规则前缀未预期的破坏性参数可能会通过而不被看到。设置此键会为会话暂停每个 shell 允许规则，以便分类器看到每个命令。需要 Claude Code v2.1.193 或更高版本。

* **作用域**: [`User or managed`](#scopes)。在读取 [`autoMode`](#automode) 的任何地方读取。
* **类型**: 布尔值
  * `true`: 当自动模式处于活动状态时，Claude Code 将每个 Bash 和 PowerShell 命令通过分类器发送，并暂停您的 shell 允许规则；在自动模式之外，规则仍然适用
  * `false`: 自动模式仅暂停可以运行任意代码的允许规则，如 `Bash(*)` 和 `Bash(python *)`；任何其他允许规则匹配的命令会跳过分类器，除非它携带[每个命令允许的域](/docs/zh-CN/sandboxing#per-command-allowed-domains-in-auto-mode)，每个其他 shell 命令都会通过它
* **默认值**: `false`

```json settings.json theme={null}
{
  "autoMode": {
    "classifyAllShell": true
  }
}
```

请参阅[将所有 shell 命令路由通过分类器](/docs/zh-CN/auto-mode-config#route-all-shell-commands-through-the-classifier)。

<h3 id="disableautomode">
  `disableAutoMode`
</h3>

从 `Shift+Tab` 循环中删除[自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)。任何本应[以自动模式启动](/docs/zh-CN/permission-modes#which-mode-a-session-starts-in)的会话，无论是来自 `--permission-mode auto`、设置文件还是内置默认值，都改为以 `default` 启动。管理员在托管设置中设置它以防止其组织中的开发人员使用自动模式。

* **作用域**: [`Any file`](#scopes)。在[托管设置](/docs/zh-CN/managed-settings)中最有用，用户无法覆盖它。也接受在 `permissions` 下作为 `permissions.disableAutoMode`。
* **类型**: 字符串 `"disable"`
* **默认值**: 未设置

```json settings.json theme={null}
{
  "disableAutoMode": "disable"
}
```

<h3 id="permissions">
  `permissions`
</h3>

控制 Claude 在不询问的情况下可以使用哪些工具、哪些工具始终提示，以及哪些工具被阻止，并设置会话启动的[权限模式](/docs/zh-CN/permission-modes)。下面的每个 `permissions.*` 键都嵌套在此对象下。

* **作用域**: [`Any file`](#scopes)
* **类型**: 包含 `allow`、`ask`、`deny`、`additionalDirectories`、`blockReadsOutsideWorkingDirectories`、`defaultMode`、`disableBypassPermissionsMode` 和 `disableAutoMode` 的对象
* **默认值**: 未设置

此示例批准 `npm run` 命令而不询问，在 `git push` 前提示，阻止读取 `.env`，并以 `acceptEdits` 启动会话：

```json settings.json theme={null}
{
  "permissions": {
    "allow": ["Bash(npm run *)"],
    "ask": ["Bash(git push *)"],
    "deny": ["Read(./.env)"],
    "defaultMode": "acceptEdits"
  }
}
```

三个规则数组共享一个语法；请参阅 `permissions.allow` 下的[权限规则语法](#permission-rule-syntax)。有关来自不同文件的权限规则如何组合，请参阅[权限规则如何跨作用域合并](/docs/zh-CN/permissions#settings-precedence)；有关设置键如何组合，请参阅设置指南上的[设置优先级](/docs/zh-CN/settings#settings-precedence)。

<h3 id="useautomodeduringplan">
  `useAutoModeDuringPlan`
</h3>

选择 Claude Code 是否使用自动模式分类器在计划模式下审查 shell 命令。使用默认值 `true`，当自动模式可用且您看不到提示时，分类器在规划期间审查每个命令，除了[关键路径删除](/docs/zh-CN/permission-modes#critical-paths)。设置 `false` 以获得对内置只读集之外的每个命令的权限提示。在 `/config` 中显示为**在计划期间使用自动模式**。

* **作用域**: [`User, local, or managed`](#scopes)。存储库无法为您关闭它。
* **类型**: 布尔值
  * `true`: 与未设置相同；当自动模式可用时，分类器在规划期间审查每个 shell 命令而不是提示您，除了[关键路径删除](/docs/zh-CN/permission-modes#critical-paths)。这些文件中的任何 `false` 仍然会关闭它
  * `false`: 您会获得对内置只读集之外的每个命令的权限提示
* **默认值**: `true`

```json settings.json theme={null}
{
  "useAutoModeDuringPlan": false
}
```

<h3 id="permissions-allow">
  `permissions.allow`
</h3>

列出 Claude Code 在不询问您的情况下批准的工具使用。在 MCP 规则中，`*` 只能出现在 `mcp__<server>__` 前缀之后的工具名称中，如 `mcp__github__get_*`；它不能出现在服务器名称中。

* **作用域**: [`Any file`](#scopes)
* **类型**: 权限规则字符串数组
* **默认值**: 未设置
* **每个会话覆盖**: `--allowedTools` 为一个会话添加允许规则，来自任何设置文件的拒绝规则仍然会阻止它命名的工具

此示例批准 `git diff` 并让 Claude Code 读取您的 `.zshrc` 而不询问：

```json settings.json theme={null}
{
  "permissions": {
    "allow": ["Bash(git diff *)", "Read(~/.zshrc)"]
  }
}
```

Claude Code 仅在您接受该文件夹的[工作区信任对话框](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust)后，才应用项目的 `.claude/settings.json` 中的 `allow` 规则。

<h4 id="permission-rule-syntax">
  权限规则语法
</h4>

权限规则遵循格式 `Tool` 或 `Tool(specifier)`。Claude Code 首先评估 `deny` 规则，然后是 `ask`，然后是 `allow`，第一个匹配决定，无论每个规则的具体程度如何；请参阅[权限规则评估顺序](/docs/zh-CN/permissions#manage-permissions)。

每行显示一个规则形状及其匹配的内容。

| 规则 | 匹配的内容 |
| :- | :- |
| `Bash` | 每个 Bash 命令 |
| `Bash(npm run *)` | 以 `npm run` 开头的命令 |
| `Read(./.env)` | 读取 `.env` 文件 |
| `WebFetch(domain:example.com)` | 对 example.com 的获取请求 |

有关完整的规则语法，包括通配符行为、Read、Edit、WebFetch、MCP 和 Agent 规则的工具特定模式，以及 Bash 模式的安全限制，请参阅[权限规则语法](/docs/zh-CN/permissions#permission-rule-syntax)。

<h3 id="permissions-ask">
  `permissions.ask`
</h3>

列出提示您确认的工具使用，即使在本应批准它们的权限模式中，如 `acceptEdits` 或 `bypassPermissions`。在 `dontAsk` 模式中，Claude Code 拒绝匹配的工具使用而不是提示。

* **作用域**: [`Any file`](#scopes)
* **类型**: 权限规则字符串数组
* **默认值**: 未设置

```json settings.json theme={null}
{
  "permissions": {
    "ask": ["Bash(git push *)"]
  }
}
```

<span id="exclude-sensitive-files" />

<h3 id="permissions-deny">
  `permissions.deny`
</h3>

列出 Claude Code 阻止的工具使用。将其用于保存 API 密钥、机密或环境值的文件：Claude Code 从文件发现和搜索结果中排除匹配的文件，拒绝读取它们，并在匹配的路径上阻止 [Edit 和 Write 工具](/docs/zh-CN/permissions#read-and-edit)。

Read 和 Edit 拒绝规则适用于 Claude 的内置文件工具、Claude Code 在 Bash 中识别的文件命令（如 `cat`、`head`、`tail`、`sed` 和 `tee`）以及 Bash [重定向](/docs/zh-CN/permissions#redirections)的目标（如 `> file` 和 `< file`）；它们不适用于读取文件而不命名它们的命令（如 `grep -r pattern .`）或任意子进程，因此对于操作系统级别的强制执行，请[启用沙箱](/docs/zh-CN/sandboxing)。

* **作用域**: [`Any file`](#scopes)
* **类型**: 权限规则字符串数组
* **默认值**: 未设置
* **每个会话覆盖**: `--disallowedTools` 为一个会话添加拒绝规则，与此键一起

此示例拒绝读取 `.env` 文件、`secrets` 目录和凭证文件，并阻止 `curl` 命令：

```json settings.json theme={null}
{
  "permissions": {
    "deny": [
      "Read(./.env)",
      "Read(./.env.*)",
      "Read(./secrets/**)",
      "Read(./config/credentials.json)",
      "Bash(curl *)"
    ]
  }
}
```

工具名称接受 glob 模式，因此 `"*"` 拒绝每个工具，`"mcp__*"` 拒绝每个 MCP 工具。只要任何其他工具仍然可用于 Claude，Claude Code 就会忽略 [`EndConversation`](/docs/zh-CN/tools-reference#endconversation-tool-behavior) 工具的拒绝规则。`Bash` 拒绝规则与 Claude 编写的命令匹配，因此 `Bash(curl *)` 不会停止 `/usr/bin/curl` 或 `sh -c 'curl …'`；请参阅 [Bash 规则不匹配的内容](/docs/zh-CN/permissions#bash-rule-limits)。此键替换已弃用的 `ignorePatterns` 配置。

<h3 id="permissions-additionaldirectories">
  `permissions.additionalDirectories`
</h3>

给予 Claude 对您启动的目录之外的目录的文件访问权限，作为额外的[工作目录](/docs/zh-CN/permissions#working-directories)。大多数 `.claude/` 配置[不会从这些目录中发现](/docs/zh-CN/permissions#additional-directories-grant-file-access-not-configuration)。

* **作用域**: [`Any file`](#scopes)，项目和本地条目提供的[沙箱写入访问权限受到限制](/docs/zh-CN/sandboxing#repository-settings-under-an-admin-required-sandbox)
* **类型**: 目录路径数组
* **默认值**: 未设置
* **每个会话覆盖**: `--add-dir` 和 `/add-dir` 为一个会话添加目录，与此键一起

```json settings.json theme={null}
{
  "permissions": {
    "additionalDirectories": ["../docs/"]
  }
}
```

与 `allow` 规则一样，项目的 `.claude/settings.json` 中的条目仅在您接受该文件夹的[工作区信任对话框](/docs/zh-CN/permissions#project-allow-rules-and-workspace-trust)后才生效。

<h3 id="permissions-blockreadsoutsideworkingdirectories">
  `permissions.blockReadsOutsideWorkingDirectories`
</h3>

使 Claude 的文件工具在每种权限模式下拒绝在[工作目录](/docs/zh-CN/permissions#working-directories)之外的读取，包括 `bypassPermissions`。Claude Code 拒绝这些路径上的 `Read`、`Grep`、`Glob` 和 `LSP` 调用，并告诉 Claude 要求您使用 `/add-dir` 添加目录。Claude Code 本身需要的文件保持可读，如您的技能、插件、规则、代理、命令以及 `~/.claude/` 下的 `CLAUDE.md` 内存文件。需要 Claude Code v2.1.257 或更高版本。

Claude Code 不以相同方式拒绝 shell 命令：

* [没有模式自动批准的操作](/docs/zh-CN/permission-modes#actions-no-mode-auto-approves)涵盖读取此类路径的 shell 命令何时提示您
* [块下的沙箱命令](#sandboxed-commands-under-the-block)涵盖沙箱命令可以读取的内容

shell 解析器无法追踪的 Bash 命令（如更改目录多次或运行子 shell 的命令）即使在自动模式和 `bypassPermissions` 模式下也会提示您。即使命令未命名工作目录之外的任何路径，提示也会出现。当命令在[沙箱](/docs/zh-CN/sandboxing)中运行且沙箱强制执行块时，此提示不适用。

Claude Code 还在您选择在[自动模式的提示中阻止此类读取（在第一次在工作目录之外读取之前）](/docs/zh-CN/permission-modes#first-read-outside-the-working-directories)时在此处写入 `true`。

* **作用域**: [`Any file`](#scopes)。任何文件中的 `true` 都适用，因此存储库可以为自己打开块，但无法解除您的块。
* **类型**: 布尔值
  * `true`: Claude 的文件工具拒绝在工作目录之外的读取
  * `false`: 与未设置相同；如果另一个文件设置 `true`，块仍然适用
* **默认值**: 未设置，因此在工作目录之外的读取遵循您的[权限模式](/docs/zh-CN/permission-modes)

```json settings.json theme={null}
{
  "permissions": {
    "blockReadsOutsideWorkingDirectories": true
  }
}
```

您使用 `--add-dir`、`/add-dir` 或用户或托管设置中的 `additionalDirectories` 添加的目录计为块的工作目录。仅在存储库设置中添加的目录不计：`.claude/settings.json` 中的目录，以及 `.claude/settings.local.json` 中的目录，除非 git 报告该文件为未跟踪。在不是 git 存储库的目录中，或当 git 跟踪该文件时，Claude Code 将 `.claude/settings.local.json` 视为存储库设置，因此将您想要保持可读的目录放在用户设置中。

当 [`autoMemoryDirectory`](#automemorydirectory) 来自项目的 `.claude/settings.json` 或来自[视为存储库提供的](/docs/zh-CN/permissions#when-your-local-settings-file-needs-trust) `.claude/settings.local.json` 时，Claude Code 不会从该目录加载任何[自动内存](/docs/zh-CN/memory#storage-location)，也不会将任何保存到它。

要解除块，从设置它的每个设置文件中删除该键，然后启动新会话。

<h4 id="sandboxed-commands-under-the-block">
  块下的沙箱命令
</h4>

当[沙箱](/docs/zh-CN/sandboxing)打开时，块也涵盖沙箱命令。Claude Code 拒绝它们对您的主目录和保存用户文件的其他根的读取访问：`/Users`、`/home`、`/root`、`/Volumes`、`/mnt`、`/media`、`/run/media` 和 `/srv`。然后它重新打开工作目录、[Claude Code 在会话中创建的 worktrees](/docs/zh-CN/worktrees)、会话临时目录以及命令需要的 `~/.claude` 部分，如技能和插件。当块生效时，来自存储库设置的 `allowRead` 和 `allowWrite` 条目不计。

当会话的工作目录是链接的 [git worktree](/docs/zh-CN/worktrees)（包括 Claude Code 在会话中途进入的）时，存储库的公共 `.git` 目录对沙箱命令保持可读和可写，因此 git 在那里保持工作。

在这些情况下，块不会到达沙箱命令，而 Claude 的文件工具继续强制执行它：

* 文件系统隔离通过 [`sandbox.filesystem.disabled`](#sandbox-filesystem-disabled) 关闭
* [`allowManagedReadPathsOnly`](#sandbox-filesystem-allowmanagedreadpathsonly) 已设置
* 您启动 Claude Code 的目录的路径包含 glob 字符，如 `*`、`?` 或 `[`

在块下，Claude Code 重新打开您的全局 git 配置文件到沙箱命令，以便 `git` 保持您的身份和设置：

* `~/.gitconfig`
* `$XDG_CONFIG_HOME/git` 下的 `config`、`ignore` 和 `attributes` 文件，默认为 `~/.config/git`
* 您的全局 git 配置通过 `[include]`、`[includeIf]`、`core.excludesFile` 或 `core.attributesFile` 命名的文件

Claude Code 单独判断每个文件。当文件位于沙箱命令可以直接或通过符号链接写入的位置时，Claude Code 不会重新打开它命名的文件。

在 Linux 和 WSL2 上，作为符号链接的配置文件可以在其自己的路径处保持不可读，然后 `git` 在没有它的情况下运行。`~/.git-credentials` 和 `$XDG_CONFIG_HOME/git/credentials` 保持被阻止。

如果重新打开的文件保存机密，如 `http.extraHeader` 令牌，请将其路径添加到 [`sandbox.filesystem.denyRead`](#sandbox-filesystem-denyread)。覆盖此重新打开的 `denyRead` 条目始终优先。

<h3 id="permissions-defaultmode">
  `permissions.defaultMode`
</h3>

设置新会话启动的[权限模式](/docs/zh-CN/permission-modes)。当您将其留空时，会话以您的表面的[内置默认值](/docs/zh-CN/permission-modes#which-mode-a-session-starts-in)启动。

* **作用域**: [`Any file`](#scopes)。`auto` 和 `bypassPermissions` 不会从项目或本地设置生效，因此改为在 `~/.claude/settings.json` 中设置它们。在 v2.1.257 之前，`bypassPermissions` 从任何文件生效。对于 VS Code 扩展启动的对话，Claude Code 仅读取用户、托管和 `--settings` 值。
* **类型**: 字符串，以下之一：
  * `"default"`: Claude Code 仅运行读取而不询问
  * `"acceptEdits"`: Claude Code 还运行文件编辑和常见文件系统命令（如 `mkdir` 和 `mv`）而不询问
  * `"plan"`: Claude Code 读取和规划但阻止编辑直到您批准计划
  * `"auto"`: Claude Code 运行而不进行常规提示；在 shell 命令和网络请求等操作运行之前，后台分类器检查它们是否与您的请求一致
  * `"dontAsk"`: Claude Code 自动拒绝每个本应提示的调用；读取、不需要批准的其他操作以及预批准的工具仍然运行
  * `"bypassPermissions"`: Claude Code 运行所有内容而不询问
  * `"manual"`: `"default"` 的别名
* **默认值**: 未设置
* **每个会话覆盖**: `--permission-mode` 及其 `bypassPermissions` 的等效 `--dangerously-skip-permissions` 对一个会话优先于此键

```json settings.json theme={null}
{
  "permissions": {
    "defaultMode": "acceptEdits"
  }
}
```

权限规则分层在每种模式之上：`deny` 规则在每种模式中阻止，包括 `bypassPermissions`。请参阅[权限模式](/docs/zh-CN/permission-modes)。在云端会话中，Claude Code 仅从此键中遵守 `acceptEdits`、`plan`、`default` 和 `auto`。对于 VS Code 扩展启动的对话，请参阅[扩展为启动权限模式读取的设置](/docs/zh-CN/permission-modes#switch-permission-modes)。

<h3 id="permissions-disablebypasspermissionsmode">
  `permissions.disableBypassPermissionsMode`
</h3>

防止任何人进入 `bypassPermissions` 模式。Claude Code 随后拒绝 `--dangerously-skip-permissions` 标志，并忽略[代理定义的](/docs/zh-CN/sub-agents#permission-modes) `permissionMode: bypassPermissions`，因此子代理以父会话的权限模式运行。

* **作用域**: [`Any file`](#scopes)。通常在[托管设置](/docs/zh-CN/managed-settings)中设置以强制执行组织政策。
* **类型**: 字符串 `"disable"`
* **默认值**: 未设置
* **每个会话覆盖**: 此键优先于 `--dangerously-skip-permissions`，在设置此键时 Claude Code 拒绝

```json settings.json theme={null}
{
  "permissions": {
    "disableBypassPermissionsMode": "disable"
  }
}
```

在 v2.1.223 之前，Claude Code 即使禁用绕过也应用了 frontmatter 权限模式。

<h3 id="skipautopermissionprompt">
  `skipAutoPermissionPrompt`
</h3>

跳过 Claude Code 在您自己首次进入自动模式时显示的一次性通知，描述[自动模式](/docs/zh-CN/permission-modes#eliminate-prompts-with-auto-mode)，例如通过您自己的设置或模式选择器，而不是当内置默认值在其中启动会话时。Claude Code 显示该通知一次，然后记录它已显示，因此此键仅在通知尚未出现的地方重要。

* **作用域**: [`User or managed`](#scopes)。存储库无法为您设置它。
* **类型**: 布尔值
  * `true`: Claude Code 跳过通知
  * `false`: 与未设置相同；通知出现一次，除非这些文件中的另一个设置 `true`
* **默认值**: 未设置，因此通知出现一次

```json settings.json theme={null}
{
  "skipAutoPermissionPrompt": true
}
```

<h3 id="skipdangerousmodepermissionprompt">
  `skipDangerousModePermissionPrompt`
</h3>

跳过 Claude Code 在会话进入 `bypassPermissions` 模式之前显示的确认对话框，无论是来自 `--dangerously-skip-permissions` 还是来自 `defaultMode: "bypassPermissions"`。当您接受该对话框一次时，Claude Code 在您的用户设置中写入 `true`。

* **作用域**: [`User, local, or managed`](#scopes)。不受信任的存储库无法为您跳过对话框。
* **类型**: 布尔值
  * `true`: Claude Code 跳过会话进入 `bypassPermissions` 模式之前的确认对话框
  * `false`: 与未设置相同；对话框出现，除非这些文件中的另一个设置 `true`
* **默认值**: 未设置，因此对话框出现

```json settings.json theme={null}
{
  "skipDangerousModePermissionPrompt": true
}
```

<h2 id="sandbox-settings">
  Sandbox 设置
</h2>

将 Claude 运行的命令与您的文件系统、网络和凭证隔离。有关沙箱工作原理和平台要求，请参阅 [Sandboxing](/docs/zh-CN/sandboxing)。

<h3 id="sandbox">
  `sandbox`
</h3>

使用 [sandboxing](/docs/zh-CN/sandboxing) 将 Claude 运行的 Bash 命令与您的文件系统和网络隔离。使用 `enabled` 打开沙箱，然后使用 `filesystem`、`network` 和 `credentials` 子对象缩小或扩大沙箱命令可以接触的内容。沙箱在 macOS、Linux 和 WSL2 上运行。

* **Scope**: [`Any file`](#scopes)
* **Type**: 对象，包含 `enabled`、`failIfUnavailable`、`autoAllowBashIfSandboxed`、`excludedCommands`、`allowUnsandboxedCommands`、`enableWeakerNestedSandbox`、`enableWeakerNetworkIsolation`、`allowAppleEvents`、`bwrapPath`、`socatPath`、`ignoreViolations` 和 `ripgrep`，以及 `filesystem`、`network` 和 `credentials` 对象
* **Default**: 未设置，因此 Claude Code 运行命令时不使用沙箱

这会打开沙箱，跳过沙箱命令的权限提示，在沙箱外运行 `docker`，打开两个额外的写入路径，隐藏您的 AWS 凭证文件，并预先允许 GitHub 和 npm：

```json settings.json theme={null}
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": true,
    "excludedCommands": ["docker *"],
    "filesystem": {
      "allowWrite": ["/tmp/build", "~/.kube"],
      "denyRead": ["~/.aws/credentials"]
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org"]
    }
  }
}
```

当托管设置设置了 `enabled` 或 `failIfUnavailable` 等布尔键时，该值会覆盖开发人员设置的任何内容。Claude Code 在会话加载的各个设置作用域中合并数组键，因此开发人员可以追加条目；请参阅 [Keep developers from widening the policy](/docs/zh-CN/sandboxing#keep-developers-from-widening-the-policy) 了解仅限托管的锁。要为组织强制执行沙箱，请参阅 [Enforce sandboxing with managed settings](/docs/zh-CN/sandboxing#enforce-sandboxing-with-managed-settings)。

<h3 id="sandbox-enabled">
  `sandbox.enabled`
</h3>

为 Bash 命令打开 [sandboxing](/docs/zh-CN/sandboxing)。当您在 `/sandbox` 面板中选择一个模式时，Claude Code 会将此键写入当前项目的 `.claude/settings.local.json`；在 `~/.claude/settings.json` 中设置它以对每个项目进行沙箱处理。

* **Scope**: [`Any file`](#scopes)，[项目和本地设置受到限制](/docs/zh-CN/sandboxing#repository-settings-under-an-admin-required-sandbox)
* **Type**: 布尔值
  * `true`: Claude Code 对 Bash 命令进行沙箱处理
  * `false`: Bash 命令在没有沙箱的情况下运行
* **Default**: `false`

```json settings.json theme={null}
{
  "sandbox": {
    "enabled": true
  }
}
```

在 Linux 和 WSL2 上，沙箱需要 `bubblewrap` 和 `socat`；请参阅 [Set up Linux and WSL2](/docs/zh-CN/sandboxing#set-up-linux-and-wsl2)。当沙箱无法启动时，除非您同时设置了 [`failIfUnavailable`](#sandbox-failifunavailable)，否则 Claude Code 会在没有沙箱的情况下运行命令。

<h3 id="sandbox-failifunavailable">
  `sandbox.failIfUnavailable`
</h3>

当 `sandbox.enabled` 为 `true` 但沙箱无法启动时（因为缺少依赖项或不支持该平台），使 Claude Code 在启动时以错误退出。没有此键时，Claude Code 会在没有沙箱的情况下运行命令。将沙箱作为安全关卡强制要求的托管部署可以使用此设置。

在沙箱不支持的平台上，启用此键时 Claude Code 不会启动。请参阅 [Enforce sandboxing with managed settings](/docs/zh-CN/sandboxing#enforce-sandboxing-with-managed-settings)。

* **Scope**: [`Any file`](#scopes)，[项目和本地设置受到限制](/docs/zh-CN/sandboxing#repository-settings-under-an-admin-required-sandbox)
* **Type**: 布尔值
  * `true`: 当 `sandbox.enabled` 为 `true` 但沙箱无法启动时，Claude Code 在启动时以错误退出
  * `false`: 当沙箱无法启动时，Claude Code 在没有沙箱的情况下运行命令
* **Default**: `false`

这使每台托管机器对命令进行沙箱处理或拒绝启动：

```json managed-settings.json theme={null}
{
  "sandbox": {
    "enabled": true,
    "failIfUnavailable": true
  }
}
```

请参阅 [Enforce sandboxing with managed settings](/docs/zh-CN/sandboxing#enforce-sandboxing-with-managed-settings)。

<h3 id="sandbox-autoallowbashifsandboxed">
  `sandbox.autoAllowBashIfSandboxed`
</h3>

让 Claude Code 运行沙箱化的 Bash 命令而无需权限提示。无法在沙箱中运行的命令仍会通过常规权限流程，`deny` 规则和内容范围的 `ask` 规则（如 `Bash(git push *)` ）仍然适用；对于沙箱化命令，裸 `Bash` ask 规则被跳过。将其设置为 `false` 以也通过常规权限流程发送沙箱化命令，`/sandbox` **Mode** 选项卡称之为常规权限模式。

* **Scope**: [`Any file`](#scopes)
* **Type**: 布尔值
  * `true`: Claude Code 运行沙箱化的 Bash 命令而无需权限提示，受 `deny` 规则和内容范围的 `ask` 规则约束；`CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` 关闭自动允许
  * `false`: 沙箱化命令通过常规权限流程，因此您的允许规则和权限模式决定。`/sandbox` **Mode** 选项卡称之为常规权限模式
* **Default**: `true`

这保持沙箱打开并通过常规权限流程发送沙箱化命令：

```json settings.json theme={null}
{
  "sandbox": {
    "enabled": true,
    "autoAllowBashIfSandboxed": false
  }
}
```

请参阅 [Sandbox modes](/docs/zh-CN/sandboxing#sandbox-modes) 了解自动允许模式仍会提示什么以及它在计划模式中的行为。

<h3 id="sandbox-excludedcommands">
  `sandbox.excludedCommands`
</h3>

指定 Claude Code 在沙箱外运行的命令，例如在沙箱下无法工作的工具。每个条目使用与 `Bash(...)` [permission rule](/docs/zh-CN/permissions#permission-rule-syntax) 内容相同的语法：精确命令、前缀（如 `docker *` ）或通配符模式。不含通配符的模式是精确匹配，因此 `docker` 仅匹配不带参数的 `docker`。

您的条目仅当它们覆盖复合命令中的每个命令时才将 Bash 调用从沙箱中取出，某些调用形式即使这样也保持沙箱化。单独的 `docker *` 条目不会将 `npm ci && docker build .` 从沙箱中取出。

* **Scope**: [`Any file`](#scopes)，[项目和本地设置受到限制](/docs/zh-CN/sandboxing#repository-settings-under-an-admin-required-sandbox)
* **Type**: 命令模式数组
* **Default**: 未设置，因此没有命令被排除

```json settings.json theme={null}
{
  "sandbox": {
    "excludedCommands": ["docker *"]
  }
}
```

Claude Code 在具有以下形式之一时保持 Bash 调用沙箱化，以及其他形式：

* 以 `sudo`、`eval` 或 `xargs` 开头的命令
* `cd`、`pushd` 或 `popd`，无论它在调用中的任何位置出现
* 命令替换、子 shell 或控制流块，例如 `if` 或 `for`
* 重定向，例如 `docker build . > build.log`，除了仅复制文件描述符的重定向，如 `2>&1` 所做的
* 来自变量的命令名称
* 带有绝对路径参数、以 `~` 开头的路径参数或包含 `..` 段的路径参数的 `git clone`、`git init`、`git worktree add`、`git worktree move` 或 `git bundle create`

例如，`cd build && docker compose up` 在 `docker *` 条目下保持沙箱化，添加 `cd` 条目不会改变这一点。在 `git *` 条目下，`git clone <url> vendor/lib` 在沙箱外运行，但 `git clone <url> ~/tools` 保持沙箱化。克隆操作会在其目标路径指向的任何位置写入整个文件树，其中可能包括可执行文件。

排除的命令仍会通过常规权限流程。排除是一种便利，而不是安全边界：当工具只需要在特定位置写入时，[`filesystem.allowWrite`](#sandbox-filesystem-allowwrite) 可以使其保持沙箱化。

除非沙箱是[管理员强制要求的](/docs/zh-CN/sandboxing#repository-settings-under-an-admin-required-sandbox)，否则来自会话加载的各个设置作用域的条目会合并为一个列表。在管理员强制要求沙箱期间，Claude Code 会忽略 `.claude/settings.json` 和 `.claude/settings.local.json` 中的条目，因此克隆的仓库无法将命令移出沙箱。托管设置、`--settings` 和您的 `~/.claude/settings.json` 中的条目仍然适用，并且此列表没有仅限托管的锁。

<h3 id="sandbox-allowunsandboxedcommands">
  `sandbox.allowUnsandboxedCommands`
</h3>

让 Claude 在沙箱阻止命令后，使用 `dangerouslyDisableSandbox` 参数在沙箱外重试该命令。当其为 `false` 时，Claude Code 会忽略该参数。此时在沙箱运行期间，Claude 运行的命令都会进行沙箱处理，除非它们匹配 [`excludedCommands`](#sandbox-excludedcommands) 条目。`/sandbox` **Overrides** 选项卡将该状态显示为 **Strict sandbox mode**。托管设置中的 `false` 会为其覆盖的开发人员打开严格沙箱模式。

* **Scope**: [`Any file`](#scopes)，[项目和本地设置受到一项限制](/docs/zh-CN/sandboxing#turn-off-the-retry-with-strict-sandbox-mode)
* **Type**: 布尔值
  * `true`: Claude 可以在沙箱阻止后使用 `dangerouslyDisableSandbox` 参数在沙箱外重试命令
  * `false`: Claude Code 忽略该参数，因此在沙箱运行期间，Claude 运行的命令都会进行沙箱处理，除非它们匹配 `excludedCommands` 条目
* **Default**: `true`

这为托管设置覆盖的每个人强制执行严格沙箱模式：

```json managed-settings.json theme={null}
{
  "sandbox": {
    "enabled": true,
    "allowUnsandboxedCommands": false
  }
}
```

来自托管设置或 `--settings` 的 `false` 还会使沙箱成为[管理员强制要求的](/docs/zh-CN/sandboxing#repository-settings-under-an-admin-required-sandbox)。用户设置中的 `false` 会优先于项目的 `true`，但不会使沙箱成为管理员强制要求的。优先于项目值需要 Claude Code v2.1.285 或更高版本。

由谁批准未沙箱化的重试取决于您的权限模式和允许规则。请参阅 [The unsandboxed retry escape hatch](/docs/zh-CN/sandboxing#the-unsandboxed-retry-escape-hatch)。

要查看您在 [`!` shell-mode prompt](/docs/zh-CN/interactive-mode#shell-mode-with-prefix) 处自己输入的命令何时以沙箱化方式运行，请参阅 [strict sandbox mode](/docs/zh-CN/sandboxing#turn-off-the-retry-with-strict-sandbox-mode)。

<h3 id="sandbox-filesystem">
  `sandbox.filesystem`
</h3>

控制沙箱化命令可以读取和写入的路径。默认情况下，它们可以写入工作目录、会话临时目录以及使用 `--add-dir`、`/add-dir` 或 `permissions.additionalDirectories` 添加的目录，并可以读取文件系统的其余部分，包括凭证文件。使用四个路径列表扩大或缩小范围，或使用 `disabled` 关闭文件系统层。请参阅 [Filesystem isolation](/docs/zh-CN/sandboxing#filesystem-isolation) 了解默认边界。

* **Scope**: [`Any file`](#scopes)
* **Type**: 对象，包含 `allowWrite`、`denyWrite`、`denyRead` 和 `allowRead` 数组，以及 `allowManagedReadPathsOnly` 和 `disabled` 布尔值
* **Default**: 未设置，因此应用默认读写边界

这让沙箱化命令写入构建目录和您的 kubeconfig，并隐藏您的 AWS 凭证文件：

```json settings.json theme={null}
{
  "sandbox": {
    "filesystem": {
      "allowWrite": ["/tmp/build", "~/.kube"],
      "denyRead": ["~/.aws/credentials"]
    }
  }
}
```

Claude Code 在操作系统沙箱边界强制执行这些列表，因此它们适用于沙箱化命令启动的每个子进程，例如 `kubectl`、`terraform` 或 `npm`。Claude Code 将您的 [permission rules](/docs/zh-CN/sandboxing#permission-rules) 添加到相同的列表：`Edit` 允许和拒绝规则到 `allowWrite` 和 `denyWrite`，`Read` 拒绝规则到 `denyRead`，以及 `WebFetch(domain:...)` 允许和拒绝规则到 [`network`](#sandbox-network) 域列表。

除非有锁适用，否则 Claude Code 在会话加载的设置文件中合并这些列表。[`allowManagedReadPathsOnly`](#sandbox-filesystem-allowmanagedreadpathsonly) 将 `allowRead` 限制为托管设置中的条目，[`allowManagedDomainsOnly`](#sandbox-network-allowmanageddomainsonly) 对允许的域执行相同操作。[仓库锁](/docs/zh-CN/sandboxing#repository-settings-under-an-admin-required-sandbox)会排除来自仓库设置文件的条目。

[Configure sandboxing](/docs/zh-CN/sandboxing#configure-sandboxing) 涵盖您使用 `--setting-sources` 排除的源。当您在会话期间编辑列表时，Claude Code [applies the change to the running session](/docs/zh-CN/settings#when-edits-take-effect)。

<h4 id="sandbox-path-prefixes">
  Sandbox 路径前缀
</h4>

`allowWrite`、`denyWrite`、`denyRead`、`allowRead` 和 [`credentials.files`](#sandbox-credentials-files) 中的路径按其前缀解析：

| 前缀 | 含义 | 示例 |
| :- | :- | :- |
| `/` | 从文件系统根目录的绝对路径 | `/tmp/build` 保持 `/tmp/build` |
| `~/` | 相对于主目录 | `~/.kube` 变为 `$HOME/.kube` |
| `./` 或无前缀 | 相对于项目根目录（用于项目设置）或 `~/.claude`（用于用户设置） | `.claude/settings.json` 中的 `./output` 解析为 `<project-root>/output` |

绝对路径的 `//path` 前缀也有效。如果您使用单斜杠 `/path` 期望项目相对解析，请切换到 `./path`。此语法与 [Read and Edit permission rules](/docs/zh-CN/permissions#read-and-edit) 不同，后者使用 `//path` 表示绝对路径，`/path` 表示项目相对路径：沙箱文件系统路径使用标准约定，因此 `/tmp/build` 是绝对路径。

Claude Code 从目录路径中删除尾部斜杠，因此 `~/.aws` 和 `~/.aws/` 匹配同一目录。在 v2.1.224 之前，Claude Code 将尾部斜杠传递给沙箱，Claude 仍然可以读取或写入使用一个尾部斜杠编写的 `denyRead` 或 `denyWrite` 条目下的路径。

Claude Code 也删除尾部 `/**`，因此 `~/build/**` 和 `~/build` 覆盖同一目录。通配符（如 `*` ）是否有效取决于条目所在的列表和平台：

* **`allowWrite` 和 `denyWrite`**: 在 macOS 上，通配符有效。在 Linux 和 WSL2 上，沙箱挂载具体路径，因此 Claude Code 在删除尾部 `/**` 后跳过包含 `*`、`?` 或 `[` 的条目，该条目无效。Claude Code 将您的 `Edit` 权限规则中的路径添加到这些列表中，因此相同的限制适用于它们，`/sandbox` 的 **Config** 选项卡警告包含通配符的 `Edit` 和 `Read` 权限规则。
* **`denyRead` 和 `allowRead`**: 通配符在每个平台上都有效。在 Linux 和 WSL2 上，Claude Code 将读取条目扩展到它匹配的具体路径，对写入列表不执行此操作。

<h3 id="sandbox-filesystem-allowwrite">
  `sandbox.filesystem.allowWrite`
</h3>

添加沙箱化命令可以写入的路径，超出工作目录、会话临时目录以及使用 `--add-dir`、`/add-dir` 或 `permissions.additionalDirectories` 添加的目录。当子进程（如 `kubectl` 或构建工具）需要在项目外写入时使用它。

* **Scope**: [`Any file`](#scopes)，[项目和本地设置受到限制](/docs/zh-CN/sandboxing#repository-settings-under-an-admin-required-sandbox)
* **Type**: 路径字符串数组，使用 [sandbox path prefixes](#sandbox-path-prefixes)
* **Default**: 未设置，因此沙箱化命令可以写入工作目录、会话临时目录、使用 `--add-dir` 或 `/add-dir` 添加的目录以及 [`permissions.additionalDirectories`](#permissions-additionaldirectories) 中的目录

这让构建在 `/tmp/build` 下写入并让 `kubectl` 更新您的 kubeconfig：

```json settings.json theme={null}
{
  "sandbox": {
    "filesystem": {
      "allowWrite": ["/tmp/build", "~/.kube"]
    }
  }
}
```

Claude Code 在会话加载的各个设置作用域中合并 `allowWrite` 条目和您的 `Edit(...)` 允许权限规则中的路径，在 [`permissions.blockReadsOutsideWorkingDirectories`](#sandboxed-commands-under-the-block) 打开时排除来自仓库设置的条目。[仓库锁](/docs/zh-CN/sandboxing#repository-settings-under-an-admin-required-sandbox)也可能排除仓库的条目。`allowWrite` 条目不能解除 [protected path](/docs/zh-CN/sandboxing#protected-paths)。

<h3 id="sandbox-filesystem-denywrite">
  `sandbox.filesystem.denyWrite`
</h3>

阻止沙箱化命令写入特定路径，包括在其他可写目录内的路径。

* **Scope**: [`Any file`](#scopes)
* **Type**: 路径字符串数组，使用 [sandbox path prefixes](#sandbox-path-prefixes)
* **Default**: 未设置

这防止沙箱化命令更改系统配置或安装二进制文件：

```json settings.json theme={null}
{
  "sandbox": {
    "filesystem": {
      "denyWrite": ["/etc", "/usr/local/bin"]
    }
  }
}
```

Claude Code 在会话加载的每个设置范围中合并条目，并添加您的 `Edit(...)` 拒绝权限规则中的路径。

<h3 id="sandbox-filesystem-denyread">
  `sandbox.filesystem.denyRead`
</h3>

阻止沙箱化命令读取特定路径，例如默认读取策略会公开的凭证文件。要保护凭证文件并使其可通过沙箱代理使用，请改为参阅 [`sandbox.credentials`](#sandbox-credentials)。

* **Scope**: [`Any file`](#scopes)
* **Type**: 路径字符串数组，使用 [sandbox path prefixes](#sandbox-path-prefixes)
* **Default**: 未设置，因此沙箱化命令保持 [default read access](/docs/zh-CN/sandboxing#filesystem-isolation)，包括凭证文件，如 `~/.aws/credentials`

```json settings.json theme={null}
{
  "sandbox": {
    "filesystem": {
      "denyRead": ["~/.aws/credentials"]
    }
  }
}
```

Claude Code 在会话加载的每个设置范围中合并条目，并添加您的 `Read(...)` 拒绝权限规则中的路径。当 [`filesystem.disabled`](#sandbox-filesystem-disabled) 为 `true` 时，Claude Code 不强制执行这些条目。

<h3 id="sandbox-filesystem-allowread">
  `sandbox.filesystem.allowRead`
</h3>

重新打开 [`denyRead`](#sandbox-filesystem-denyread) 阻止的区域内特定路径的读取，以构建仅工作区读取访问。精确或通配符 `denyRead` 条目在更广泛的 `allowRead` 内保持阻止，如 [overlap table](/docs/zh-CN/sandboxing#configure-sandboxing) 所示。当通配符 `denyRead` 条目（如 `~/**/.env` ）匹配目录时，Claude Code 也会阻止其内容的读取。在 v2.1.236 之前的 macOS 上，Claude Code 在更广泛的 `allowRead` 条目覆盖它们的任何地方重新打开通配符 `denyRead` 条目匹配的路径，并保持匹配目录的内容可读。

* **Scope**: [`Any file`](#scopes)，[项目和本地设置受到限制](/docs/zh-CN/sandboxing#repository-settings-under-an-admin-required-sandbox)
* **Type**: 路径字符串数组，使用 [sandbox path prefixes](#sandbox-path-prefixes)
* **Default**: 未设置

这阻止读取您的主目录，除了项目本身：

```json settings.json theme={null}
{
  "sandbox": {
    "filesystem": {
      "denyRead": ["~/"],
      "allowRead": ["."]
    }
  }
}
```

Claude Code 在项目设置中将 `.` 条目解析为项目根目录，在用户设置中解析为 `~/.claude`。Claude Code 在会话加载的设置文件中合并条目，除非设置了 [`allowManagedReadPathsOnly`](#sandbox-filesystem-allowmanagedreadpathsonly)，并在 [`permissions.blockReadsOutsideWorkingDirectories`](#sandboxed-commands-under-the-block) 打开时排除来自仓库设置的条目。[仓库锁](/docs/zh-CN/sandboxing#repository-settings-under-an-admin-required-sandbox)也可能排除仓库的条目。

<h3 id="sandbox-filesystem-allowmanagedreadpathsonly">
  `sandbox.filesystem.allowManagedReadPathsOnly`
</h3>

仅遵守来自托管设置的 [`allowRead`](#sandbox-filesystem-allowread) 条目，以便开发人员无法重新打开对您的组织阻止的路径的读取访问。Claude Code 仍然从会话加载的每个设置范围合并 `denyRead` 条目。

* **Scope**: [`Managed`](#scopes)
* **Type**: 布尔值
  * `true`: Claude Code 仅遵守来自托管设置的 `allowRead` 条目
  * `false`: 来自其他设置文件的 `allowRead` 条目可以合并进来
* **Default**: `false`

这阻止读取主目录，重新打开 `~/work`，并阻止开发人员重新打开任何其他内容：

```json managed-settings.json theme={null}
{
  "sandbox": {
    "filesystem": {
      "denyRead": ["~/"],
      "allowRead": ["~/work"],
      "allowManagedReadPathsOnly": true
    }
  }
}
```

请参阅 [Keep developers from widening the policy](/docs/zh-CN/sandboxing#keep-developers-from-widening-the-policy)。

<h3 id="sandbox-filesystem-disabled">
  `sandbox.filesystem.disabled`
</h3>

跳过文件系统隔离，同时保持网络隔离。沙箱化命令获得对主机文件系统的无限制读写访问，其网络出口仍限制在 [`network.allowedDomains`](#sandbox-network-alloweddomains)。当您沙箱化以控制命令连接的位置而不是它们写入的内容时使用它。需要 Claude Code v2.1.216 或更高版本。

* **Scope**: [`User or managed`](#scopes)。当托管设置配置 `sandbox.filesystem` 时，或列出带有 `"mode": "deny"` 的 `sandbox.credentials.files` 条目时，只有托管设置可以设置它。
* **Type**: 布尔值
  * `true`: Claude Code 跳过文件系统隔离并保持网络隔离
  * `false`: 文件系统隔离保持打开
* **Default**: `false`，因此文件系统隔离保持打开

这使文件系统打开并将网络出口限制在 GitHub 和 npm：

```json settings.json theme={null}
{
  "sandbox": {
    "enabled": true,
    "filesystem": {
      "disabled": true
    },
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org"]
    }
  }
}
```

关闭该层后，Claude Code 不强制执行 `denyRead` 或 `credentials.files` `deny` 条目，而 `credentials.envVars` 条目和应用的 `mask` 条目保持工作。[`autoAllowBashIfSandboxed`](#sandbox-autoallowbashifsandboxed) 仍默认为 `true`，因此将其设置为 `false` 以保持提示。请参阅 [Disable filesystem isolation](/docs/zh-CN/sandboxing#disable-filesystem-isolation) 了解可以设置它的完整源列表以及隔离关闭时的变化。需要 Claude Code v2.1.216 或更高版本。

<h3 id="sandbox-ignoreviolations">
  `sandbox.ignoreViolations`
</h3>

沉默沙箱违规报告，针对您期望命令探测并被拒绝的路径，例如在启动时检查 `/etc/hosts` 的工具，因此这些拒绝不会显示为违规或在 Claude 看到的内容中。沙箱仍然阻止访问；只有报告被抑制。键是与命令匹配的子字符串，`*` 匹配每个命令，值是该命令要忽略的违规子字符串，例如文件系统路径。

* **Scope**: [`Any file`](#scopes)，[项目和本地设置受到限制](/docs/zh-CN/sandboxing#repository-settings-under-an-admin-required-sandbox)
* **Type**: 对象，将命令子字符串映射到违规子字符串数组，通常是路径
* **Default**: 未设置，因此报告每个违规

```json settings.json theme={null}
{
  "sandbox": {
    "ignoreViolations": {
      "*": ["/etc/hosts"]
    }
  }
}
```

<h3 id="sandbox-enableweakernestedsandbox">
  `sandbox.enableWeakerNestedSandbox`
</h3>

在无特权 Docker 容器内运行 Linux 沙箱，其中 bubblewrap 无法挂载新的 `/proc`。相反，内部沙箱绑定挂载容器的现有 `/proc`，这暴露了新挂载会隐藏的进程信息。这降低了安全性；仅当外部容器已提供您需要的隔离时才使用它。

* **Scope**: [`Any file`](#scopes)，[项目和本地设置受到限制](/docs/zh-CN/sandboxing#repository-settings-under-an-admin-required-sandbox)
* **Type**: 布尔值
  * `true`: 内部沙箱绑定挂载容器的现有 `/proc` 而不是挂载新的
  * `false`: 沙箱挂载新的 `/proc`，在无特权 Docker 容器中不工作
* **Default**: `false`

```json settings.json theme={null}
{
  "sandbox": {
    "enabled": true,
    "enableWeakerNestedSandbox": true
  }
}
```

仅限 Linux 和 WSL2。请参阅 [Bubblewrap fails to start inside a container](/docs/zh-CN/sandboxing#bubblewrap-fails-to-start-inside-a-container)。

<h3 id="sandbox-enableweakernetworkisolation">
  `sandbox.enableWeakerNetworkIsolation`
</h3>

让 macOS 上的沙箱化命令到达系统 TLS 信任服务 `com.apple.trustd.agent`。基于 Go 的工具（如 `gh`、`gcloud` 和 `terraform` ）在您使用 [`network.httpProxyPort`](#sandbox-network-httpproxyport) 与 MITM 代理和自定义 CA 时需要它来验证 TLS 证书。这通过打开通过信任服务的潜在数据泄露路径来降低安全性。

* **Scope**: [`Any file`](#scopes)，[项目和本地设置受到限制](/docs/zh-CN/sandboxing#repository-settings-under-an-admin-required-sandbox)
* **Type**: 布尔值
  * `true`: macOS 上的沙箱化命令可以到达 `com.apple.trustd.agent`
  * `false`: macOS 上的沙箱化命令无法到达系统 TLS 信任服务
* **Default**: `false`

```json settings.json theme={null}
{
  "sandbox": {
    "enabled": true,
    "enableWeakerNetworkIsolation": true
  }
}
```

如果您不使用 MITM 代理，请改为在 [`excludedCommands`](#sandbox-excludedcommands) 中列出失败的工具；请参阅 [Go-based CLIs fail TLS verification on macOS](/docs/zh-CN/sandboxing#go-based-clis-fail-tls-verification-on-macos)。

<h3 id="sandbox-allowappleevents">
  `sandbox.allowAppleEvents`
</h3>

让 macOS 上的沙箱化命令发送 Apple Events，`open`、`osascript` 和在浏览器中打开 URL 的工具需要它；没有它们会失败，错误为 `-600`。这删除了代码执行隔离：沙箱化命令可以在没有用户提示的情况下启动其他应用程序，并可以向运行的应用程序（如 Terminal）发送 AppleScript 命令，受每个应用程序的 macOS 自动化同意提示 (TCC) 约束。

* **Scope**: [`User or managed`](#scopes)
* **Type**: 布尔值
  * `true`: macOS 上的沙箱化命令可以发送 Apple Events
  * `false`: macOS 上的沙箱化命令无法发送 Apple Events，因此 `open` 和 `osascript` 失败，错误为 `-600`
* **Default**: `false`

```json settings.json theme={null}
{
  "sandbox": {
    "enabled": true,
    "allowAppleEvents": true
  }
}
```

要保持隔离并仍然运行一个这样的工具，请改为将其添加到 [`excludedCommands`](#sandbox-excludedcommands)。请参阅 [Apple Events on macOS](/docs/zh-CN/sandboxing#security-limitations)。

<h3 id="sandbox-ripgrep">
  `sandbox.ripgrep`
</h3>

将沙箱指向您自己的 ripgrep 二进制文件，而不是 Claude Code 使用的，例如当您的平台需要不同构建的 `rg` 时。

* **Scope**: [`User or managed`](#scopes)
* **Type**: 对象，包含 `command`（ripgrep 二进制文件的路径）和可选的 `args`（要前置的参数数组）
* **Default**: 未设置，因此沙箱使用与 Claude Code 相同的 ripgrep 二进制文件。这是捆绑的二进制文件，除非您将 [`USE_BUILTIN_RIPGREP`](/docs/zh-CN/env-vars) 设置为 `0`

```json settings.json theme={null}
{
  "sandbox": {
    "ripgrep": {
      "command": "/usr/local/bin/rg"
    }
  }
}
```

<h3 id="sandbox-bwrappath">
  `sandbox.bwrapPath`
</h3>

将沙箱指向安装在 `PATH` 外的 bubblewrap 二进制文件，例如在气隙主机上的供应商副本。Claude Code 在启动依赖项检查和包装每个沙箱化命令时都使用该路径。

* **Scope**: [`Managed`](#scopes)。Claude Code 仅从托管设置读取它，以便用户、项目或本地文件无法将沙箱指向不同的二进制文件。
* **Type**: 字符串，绝对路径；Claude Code 删除相对路径并回退到 `PATH` 查找
* **Default**: 未设置，因此 Claude Code 在 `PATH` 上找到 `bwrap`

```json managed-settings.json theme={null}
{
  "sandbox": {
    "enabled": true,
    "bwrapPath": "/opt/admin/bwrap"
  }
}
```

仅限 Linux 和 WSL2。

<h3 id="sandbox-socatpath">
  `sandbox.socatPath`
</h3>

将沙箱网络代理指向安装在 `PATH` 外的 `socat` 二进制文件。

* **Scope**: [`Managed`](#scopes)
* **Type**: 字符串，绝对路径；Claude Code 删除相对路径并回退到 `PATH` 查找
* **Default**: 未设置，因此 Claude Code 在 `PATH` 上找到 `socat`

```json managed-settings.json theme={null}
{
  "sandbox": {
    "enabled": true,
    "socatPath": "/opt/admin/socat"
  }
}
```

仅限 Linux 和 WSL2。

<h3 id="sandbox-credentials">
  `sandbox.credentials`
</h3>

声明凭证文件和环境变量以 [protect from sandboxed commands](/docs/zh-CN/sandboxing#protect-credentials)。每个条目命名文件 `path` 或变量 `name` 和 `mode`：`deny` 在沙箱内隐藏凭证，`mask` 向沙箱化命令显示占位符，同时 [sandbox proxy](/docs/zh-CN/sandboxing#mask-credentials) 在出站请求上替换真实值。Claude Code 仅保护您列出的条目；没有内置凭证拒绝列表。

* **Scope**: [`Any file`](#scopes)。Claude Code 仅从用户设置、托管设置和 `--settings` 标志遵守 `mask` 条目、`allowPlaintextInject`、`awsPairs` 和 `sigv4`。
* **Type**: 对象，包含 `files`、`envVars`、`allowPlaintextInject`、`awsPairs` 和 `sigv4`
* **Default**: 未设置，因此没有凭证被保护

这隐藏您的 AWS 凭证文件并从沙箱化命令中删除 `GITHUB_TOKEN`：

```json settings.json theme={null}
{
  "sandbox": {
    "credentials": {
      "files": [{ "path": "~/.aws/credentials", "mode": "deny" }],
      "envVars": [{ "name": "GITHUB_TOKEN", "mode": "deny" }]
    }
  }
}
```

`deny` 文件保护是文件系统层的一部分，因此当您 [disable filesystem isolation](/docs/zh-CN/sandboxing#disable-filesystem-isolation) 时不适用；环境变量保护仍然适用。

<h4 id="invalid-credential-entries-in-managed-settings">
  托管设置中的无效凭证条目
</h4>

当托管 `sandbox.credentials` 条目验证失败时，Claude Code 在可能的地方保持保护凭证：

* `files` 或 `envVars` 中仍有有效 `path` 或 `name` 和 `mask` 或 `deny` 的 `mode` 的条目，例如其 `extract` 模式没有捕获组的条目，降级为 `mode: "deny"` 并带有警告，因此凭证保持阻止，而不是掩盖，直到您修复条目。降级的 `files` 条目像显式 `deny` 条目一样固定 [`filesystem.disabled`](/docs/zh-CN/sandboxing#disable-filesystem-isolation)，警告注意如果托管设置关闭文件系统隔离，其读取块不被强制执行。
* 具有未知 `mode` 或无效 `path` 或 `name` 的条目被删除。
* 每种情况都会警告；无论条目是降级还是删除，其余有效条目仍然被强制执行，完全无效的 `credentials` 值被删除，同时 `sandbox` 的其余部分仍然适用。

适用于 v2.1.191 及更高版本；在 v2.1.221 之前，每个无效条目都被删除。对于其他具有每字段处理的托管键，请参阅 [Invalid entries in managed settings](/docs/zh-CN/managed-settings#invalid-entries-in-managed-settings)。

<h3 id="sandbox-credentials-files">
  `sandbox.credentials.files`
</h3>

保护凭证文件或目录免受沙箱化命令。使用 `"mode": "deny"`，Claude Code 阻止在沙箱内读取路径，与 [`sandbox.filesystem.denyRead`](#sandbox-filesystem-denyread) 相同的读取块。使用 `"mode": "mask"`，Linux 和 WSL2 上的沙箱化命令读取文件的哨兵副本，沙箱代理在对该条目的 `injectHosts` 的出站请求上替换真实值；在 macOS 上，文件在沙箱内不可读。`"mode": "mask"` 需要 Claude Code v2.1.221 或更高版本。

* **Scope**: [`Any file`](#scopes)。Claude Code 从项目 `.claude/settings.json` 和本地 `.claude/settings.local.json` 删除 `mask` 条目。
* **Type**: 对象数组，每个包含 `path` 和 `"deny"` 或 `"mask"` 的 `mode`，加上可选的 [mask fields for files](#mask-fields-for-files)
* **Default**: 未设置，因此没有凭证文件被保护

这隐藏您的 AWS 凭证文件并掩盖 `gh` 主机文件，仅在对 `api.github.com` 的请求上替换真实值：

```json settings.json theme={null}
{
  "sandbox": {
    "credentials": {
      "files": [
        { "path": "~/.aws/credentials", "mode": "deny" },
        { "path": "~/.config/gh/hosts.yml", "mode": "mask", "injectHosts": ["api.github.com"] }
      ]
    }
  }
}
```

路径使用与 `sandbox.filesystem.*` 设置相同的 [prefixes](#sandbox-path-prefixes)，Claude Code 在会话加载的每个设置范围中合并数组。[Protect credentials](/docs/zh-CN/sandboxing#protect-credentials) 涵盖您使用 `--setting-sources` 排除的源仍然适用的内容。`mask` 条目需要 Claude Code v2.1.221 或更高版本。

`mask` 替换仅通过沙箱代理运行，因此请设置 [`sandbox.network.tlsTerminate`](#sandbox-network-tlsterminate)，或针对纯 HTTP 测试网络设置 [`allowPlaintextInject`](#sandbox-credentials-allowplaintextinject)。`mask` 适用于单个文件，因此请单独列出每个凭据文件。Claude Code 接受但忽略 `deny` 条目上的 `mask` 字段。[Mask credentials](/docs/zh-CN/sandboxing#mask-credentials) 涵盖遵守哪些设置源，[Mask credential files](/docs/zh-CN/sandboxing#mask-credential-files) 涵盖条目何时回退到 `deny`。

<span id="sandbox-credentials-files-extract" />

<span id="sandbox-credentials-files-onextractnomatch" />

<span id="sandbox-credentials-files-decode" />

<span id="sandbox-credentials-files-maskclaims" />

<span id="sandbox-credentials-files-maskduplicates" />

<span id="sandbox-credentials-files-injecthosts" />

<h4 id="mask-fields-for-files">
  文件的掩盖字段
</h4>

`mask` 条目接受这些可选字段。没有 `extract` 或 `decode`，Claude Code 用一个哨兵替换整个文件内容。在启用文件系统隔离的 macOS 上，Claude Code 在 `extract` 或 `decode` 运行之前将 `mask` 条目应用为 `deny`；请参阅 [Mask credential files](/docs/zh-CN/sandboxing#mask-credential-files)。

| 字段 | 类型 | 它做什么 |
| :- | :- | :- |
| `extract` | 字符串，至少有一个捕获组的正则表达式 | 仅掩盖每个匹配的第 1 组捕获的文本，因此文件的其余部分保持可解析。设置 `decode` 后，Claude Code 检查每个捕获作为可能的 JWT，而不是直接替换它。需要 v2.1.221 或更高版本 |
| `onExtractNoMatch` | `"warn"`、`"deny"` 或 `"error"`；默认 `"warn"` | 当 `extract` 或 `decode` 找不到要掩盖的内容时会发生什么。`warn` 在沙箱内保持文件可读，`deny` 使其不可读，`error` 停止沙箱设置直到您修复配置。当读取块不被强制执行时，Claude Code 将 `deny` 视为 `error`，因为您 [disable filesystem isolation](/docs/zh-CN/sandboxing#disable-filesystem-isolation) 或 [`sandbox.filesystem.allowRead`](#sandbox-filesystem-allowread) 条目重新打开路径。需要 v2.1.221 或更高版本；`decode` 情况需要 v2.1.224 或更高版本 |
| `decode` | 字符串 `"jwt"` | 在文件中查找 JSON Web Tokens (JWTs)，使用内置模式或设置 `extract` 时，验证每个候选，并用结构有效的假令牌替换它，因此沙箱内解码令牌的代码保持工作。当没有候选验证时，`onExtractNoMatch` 管理结果。需要 v2.1.224 或更高版本 |
| `maskClaims` | 字符串数组，至少一个声明名称；需要 `decode` | 仅掩盖每个验证的 JWT 内的命名顶级有效负载声明并围绕修改的有效负载重建令牌，因此其他声明保持可读。当没有命名声明匹配时，`onExtractNoMatch` 管理结果。需要 v2.1.224 或更高版本 |
| `maskDuplicates` | 布尔值，默认 `false` | 也替换文件中其他地方每个掩盖值的逐字副本，例如粘贴到注释中的秘密。Claude Code 匹配原始子字符串，因此为长的、高熵的秘密保留它。仅在设置 `extract` 或 `decode` 时咨询。需要 v2.1.221 或更高版本 |
| `injectHosts` | 字符串数组，每个是 [`sandbox.network.allowedDomains`](#sandbox-network-alloweddomains) 也允许的主机 | 缩小沙箱代理替换真实值的主机。未设置时，代理在对 `sandbox.network.allowedDomains` 中每个主机的请求上替换它。需要 v2.1.221 或更高版本 |

这仅掩盖 `gh` 主机文件中的 `oauth_token` 值，替换文件中它的每个其他副本，如果模式匹配不到任何内容则使文件不可读，并仅在对 `api.github.com` 的请求上替换真实令牌：

```json settings.json theme={null}
{
  "sandbox": {
    "credentials": {
      "files": [
        {
          "path": "~/.config/gh/hosts.yml",
          "mode": "mask",
          "extract": "oauth_token:\\s*(\\S+)",
          "maskDuplicates": true,
          "onExtractNoMatch": "deny",
          "injectHosts": ["api.github.com"]
        }
      ]
    }
  }
}
```

<h3 id="sandbox-credentials-envvars">
  `sandbox.credentials.envVars`
</h3>

保护环境变量免受沙箱化命令。使用 `"mode": "deny"`，Claude Code 从沙箱化命令的环境中删除变量。使用 `"mode": "mask"`，沙箱化命令看到每个会话的哨兵值，沙箱代理在对该条目的 `injectHosts` 的出站请求上替换真实值，因此 `gh` 和 `npm` 等工具保持身份验证而无需持有真实凭据。

* **Scope**: [`Any file`](#scopes)。Claude Code 从项目 `.claude/settings.json` 和本地 `.claude/settings.local.json` 删除 `mask` 条目。
* **Type**: 对象数组，每个包含 `name` 和 `"deny"` 或 `"mask"` 的 `mode`，加上可选的 [mask fields for environment variables](#mask-fields-for-environment-variables)
* **Default**: 未设置，因此没有环境变量被保护

这从沙箱化命令中删除 `NPM_TOKEN` 并掩盖 `GITHUB_TOKEN`，仅在对 `api.github.com` 的请求上替换真实值：

```json settings.json theme={null}
{
  "sandbox": {
    "credentials": {
      "envVars": [
        { "name": "NPM_TOKEN", "mode": "deny" },
        { "name": "GITHUB_TOKEN", "mode": "mask", "injectHosts": ["api.github.com"] }
      ]
    }
  }
}
```

`name` 必须以字母或下划线开头，仅包含字母、数字和下划线。Claude Code 在会话加载的每个设置作用域中合并数组，当同一变量同时出现两种模式时应用 `deny`。[Protect credentials](/docs/zh-CN/sandboxing#protect-credentials) 涵盖您使用 `--setting-sources` 排除的源仍然适用的内容。

`mask` 替换仅通过沙箱代理运行，因此请设置 [`sandbox.network.tlsTerminate`](#sandbox-network-tlsterminate)，或针对纯 HTTP 测试网络设置 [`allowPlaintextInject`](#sandbox-credentials-allowplaintextinject)；请参阅 [Mask credentials](/docs/zh-CN/sandboxing#mask-credentials)。Claude Code 接受但忽略 `deny` 条目上的 `mask` 字段。

<span id="sandbox-credentials-envvars-extract" />

<span id="sandbox-credentials-envvars-onextractnomatch" />

<span id="sandbox-credentials-envvars-decode" />

<span id="sandbox-credentials-envvars-maskclaims" />

<span id="sandbox-credentials-envvars-injecthosts" />

<h4 id="mask-fields-for-environment-variables">
  环境变量的掩盖字段
</h4>

`mask` 条目接受这些可选字段。没有 `extract` 或 `decode`，Claude Code 用一个哨兵替换整个值。`extract` 和 `decode` 不能在同一条目上组合。

| 字段 | 类型 | 它做什么 |
| :- | :- | :- |
| `extract` | 字符串，至少有一个捕获组的正则表达式 | 仅掩盖每个匹配的第 1 组捕获的文本，例如 `DATABASE_URL` 连接字符串内的密码，因此值的其余部分保持可解析。需要 v2.1.224 或更高版本 |
| `onExtractNoMatch` | `"warn"`、`"deny"` 或 `"error"`；默认 `"warn"`。在带有 `decode` 的条目上，仅接受 `"warn"` | 当 `extract` 匹配不到任何内容时会发生什么。`warn` 未掩盖地传递变量，`deny` 在沙箱内取消设置它，`error` 停止沙箱设置直到您修复配置。需要 v2.1.224 或更高版本 |
| `decode` | 字符串 `"jwt"` | 验证整个值是 JWT 并用结构有效的假令牌替换它，因此沙箱内解码令牌的代码保持工作；代理在出口上替换整个真实令牌。不验证的值未掩盖地传递并带有警告。需要 v2.1.224 或更高版本 |
| `maskClaims` | 字符串数组，至少一个声明名称；需要 `decode` | 仅掩盖解码的 JWT 内的命名顶级有效负载声明并围绕修改的有效负载重建令牌，因此其他声明保持可读。当没有命名声明匹配时，变量未掩盖地传递并带有警告。需要 v2.1.224 或更高版本 |
| `injectHosts` | 字符串数组，每个是 [`sandbox.network.allowedDomains`](#sandbox-network-alloweddomains) 也允许的主机 | 缩小沙箱代理替换真实值的主机。未设置时，代理在对 `sandbox.network.allowedDomains` 中每个主机的请求上替换它。将 IPv6 目标写为裸压缩地址，例如 `"::1"`，而不是括号形式；请参阅 [IPv6 destinations in `injectHosts`](/docs/zh-CN/sandboxing#ipv6-destinations-in-injecthosts) |

这仅掩盖 `DATABASE_URL` 内的密码，如果模式匹配不到任何内容则取消设置变量，并掩盖 `SERVICE_JWT` 中的 JWT，同时保持除 `api_key` 外的每个声明可读：

```json settings.json theme={null}
{
  "sandbox": {
    "credentials": {
      "envVars": [
        {
          "name": "DATABASE_URL",
          "mode": "mask",
          "extract": "://[^:]+:([^@]+)@",
          "onExtractNoMatch": "deny"
        },
        {
          "name": "SERVICE_JWT",
          "mode": "mask",
          "decode": "jwt",
          "maskClaims": ["api_key"]
        }
      ]
    }
  }
}
```

<h3 id="sandbox-credentials-allowplaintextinject">
  `sandbox.credentials.allowPlaintextInject`
</h3>

允许 `mask` 替换在纯 HTTP 请求以及 TLS 终止的 HTTPS 上。在纯 HTTP 上，上游身份未验证，凭据以明文形式传输，因此在受信任的测试网络外保持关闭。

* **Scope**: [`User or managed`](#scopes)
* **Type**: 布尔值
  * `true`: Claude Code 允许 `mask` 替换在纯 HTTP 请求以及 TLS 终止的 HTTPS 上
  * `false`: Claude Code 仅允许 `mask` 替换在 TLS 终止的 HTTPS 上
* **Default**: `false`

```json settings.json theme={null}
{
  "sandbox": {
    "credentials": {
      "allowPlaintextInject": true
    }
  }
}
```

<h3 id="sandbox-credentials-awspairs">
  `sandbox.credentials.awsPairs`
</h3>

分组掩盖的环境变量，形成一个 AWS 凭证用于 [SigV4 re-signing](/docs/zh-CN/sandboxing#re-sign-aws-requests)，当您的凭证存在于具有非标准名称的变量中时。Claude Code 在您掩盖其整个值时自动链接常规 `AWS_ACCESS_KEY_ID`、`AWS_SECRET_ACCESS_KEY` 和 `AWS_SESSION_TOKEN` 三元组，因此您仅在其他名称时需要此键。需要 Claude Code v2.1.224 或更高版本。

* **Scope**: [`User or managed`](#scopes)
* **Type**: 对象数组，每个包含 `accessKeyIdVar`、`secretAccessKeyVar` 和可选的 `sessionTokenVar`，命名 `sandbox.credentials.envVars` 条目
* **Default**: 未设置，因此仅配对常规三元组

这将三个自定义命名的变量链接到一个 AWS 凭证以进行重新签名：

```json settings.json theme={null}
{
  "sandbox": {
    "credentials": {
      "awsPairs": [
        {
          "accessKeyIdVar": "MY_KEY_ID",
          "secretAccessKeyVar": "MY_SECRET_KEY",
          "sessionTokenVar": "MY_SESSION_TOKEN"
        }
      ]
    }
  }
}
```

每个指定的变量必须是 [`sandbox.credentials.envVars`](#sandbox-credentials-envvars) 中的整值 `mask` 条目，不带 `extract` 或 `decode`，并且在所有配对中只能填充一个槽位。以下规则也适用：

* 代理在访问密钥 ID 条目的 `injectHosts` 中列出的主机上重新签名请求
* 设置 `sessionTokenVar` 时，代理在重新签名的请求上将真实令牌作为 `x-amz-security-token` 发送
* 在配对中指定任何常规变量都会替换自动配对

<h3 id="sandbox-credentials-sigv4">
  `sandbox.credentials.sigv4`
</h3>

选择沙箱代理对 AWS 请求形式的处理，它 [can't re-sign](/docs/zh-CN/sandboxing#re-sign-aws-requests)：`streaming` 用于 aws-chunked 流上传，`presigned` 用于预签名 URL，`sigv4a` 用于 SigV4A 非对称签名。这仅适用于使用掩盖对的占位符访问密钥 ID 签名的请求。需要 Claude Code v2.1.224 或更高版本。

* **Scope**: [`User or managed`](#scopes)
* **Type**: 对象，包含 `streaming`、`presigned` 和 `sigv4a`，每个为以下之一：
  * `"deny"`: 代理失败请求
  * `"passthrough"`: 代理转发使用掩盖占位符签名的请求，因此工具接收 AWS 自己的拒绝
* **Default**: 未设置，因此每种形式都是 `"deny"`

这转发流上传而不是在代理处失败它们：

```json settings.json theme={null}
{
  "sandbox": {
    "credentials": {
      "sigv4": {
        "streaming": "passthrough"
      }
    }
  }
}
```

使用 `deny`，代理失败请求。使用 `passthrough`，代理转发使用掩盖占位符计算的签名的请求，因此 AWS 拒绝它，调用工具接收 AWS 自己的响应而不是代理错误。

<h3 id="sandbox-network">
  `sandbox.network`
</h3>

控制沙箱化命令可以到达的主机、端口和套接字。沙箱通过强制执行这些列表的代理路由出站流量；请参阅 [Network isolation](/docs/zh-CN/sandboxing#network-isolation) 了解代理如何决定以及何时提示。

* **Scope**: [`Any file`](#scopes)。`strictAllowlist`、`allowManagedDomainsOnly` 和 `tlsTerminate` 从较少的源读取，如其条目所述。
* **Type**: 对象，包含以下子键
* **Default**: 未设置，因此没有域被预先允许，由您的权限模式决定[每个新主机的处理方式](/docs/zh-CN/sandboxing#hosts-outside-your-allowed-domains)

这预先允许 GitHub 和 npm，阻止 `uploads.github.com`，并让命令绑定到 localhost：

```json settings.json theme={null}
{
  "sandbox": {
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org"],
      "deniedDomains": ["uploads.github.com"],
      "allowLocalBinding": true
    }
  }
}
```

Claude Code 在各个设置作用域中合并数组子键，因此项目可以向您的用户列表添加域，除非有[仓库锁](/docs/zh-CN/sandboxing#repository-settings-under-an-admin-required-sandbox)适用。`WebFetch(domain:...)` 允许和拒绝 [permission rules](/docs/zh-CN/sandboxing#permission-rules) 会填充相同的允许和拒绝列表。

<h3 id="sandbox-network-allowunixsockets">
  `sandbox.network.allowUnixSockets`
</h3>

列出 macOS 上沙箱化命令可以连接到的 Unix 套接字路径。Claude Code 在 Linux 和 WSL2 上忽略此列表，其中 seccomp 过滤器无法检查套接字路径；改为在那里使用 [`allowAllUnixSockets`](#sandbox-network-allowallunixsockets)。

* **Scope**: [`Any file`](#scopes)，[项目和本地设置受到限制](/docs/zh-CN/sandboxing#repository-settings-under-an-admin-required-sandbox)
* **Type**: 字符串数组，每个是套接字路径
* **Default**: 未设置，因此 macOS 沙箱阻止每个 Unix 套接字

```json settings.json theme={null}
{
  "sandbox": {
    "network": {
      "allowUnixSockets": ["~/.ssh/agent-socket"]
    }
  }
}
```

套接字路径可以授予广泛的访问权限：例如，允许 `/var/run/docker.sock` 让沙箱化命令控制 Docker 守护程序。请参阅 [Security limitations](/docs/zh-CN/sandboxing#security-limitations)。

<h3 id="sandbox-network-allowallunixsockets">
  `sandbox.network.allowAllUnixSockets`
</h3>

让沙箱化命令连接到每个 Unix 套接字。在 Linux 和 WSL2 上，沙箱的 [seccomp filter](/docs/zh-CN/sandboxing#set-up-linux-and-wsl2) 阻止 `socket(AF_UNIX, ...)` 调用，因此这是在那里允许 Unix 套接字的唯一方式。当过滤器缺失时，`/sandbox` 在其 Dependencies 选项卡上报告，沙箱不阻止 Unix 套接字调用。请参阅 [Set up Linux and WSL2](/docs/zh-CN/sandboxing#set-up-linux-and-wsl2) 了解过滤器来自何处。

* **Scope**: [`Any file`](#scopes)，[项目和本地设置受到限制](/docs/zh-CN/sandboxing#repository-settings-under-an-admin-required-sandbox)
* **Type**: 布尔值
  * `true`: 沙箱化命令可以连接到每个 Unix 套接字
  * `false`: 沙箱阻止 Unix 套接字连接：在 macOS 上除了 `allowUnixSockets` 中的路径，在 Linux 和 WSL2 上通过 seccomp 过滤器（当存在时）
* **Default**: `false`

```json settings.json theme={null}
{
  "sandbox": {
    "network": {
      "allowAllUnixSockets": true
    }
  }
}
```

在 WSL2 上，`true` 也重新打开启动 Windows 二进制文件（如 `cmd.exe` 和 `powershell.exe` ）的互操作套接字。

<h3 id="sandbox-network-allowlocalbinding">
  `sandbox.network.allowLocalBinding`
</h3>

让 macOS 上的沙箱化命令监听网络端口（例如启动开发服务器），并连接到 localhost 上的任何端口。监听非回环地址的命令会接受来自其他机器的连接。该键在 Linux 和 WSL2 上无效，因为那里每个沙箱化命令都有自己的回环接口。要从 Linux 或 WSL2 访问主机上的服务器，请参阅 [A command fails to reach a server on localhost](/docs/zh-CN/sandboxing#a-command-fails-to-reach-a-server-on-localhost)。

* **Scope**: [`Any file`](#scopes)，[项目和本地设置受到限制](/docs/zh-CN/sandboxing#repository-settings-under-an-admin-required-sandbox)
* **Type**: 布尔值
  * `true`: macOS 上的沙箱化命令可以监听任何本地地址并连接到 localhost 上的任何端口
  * `false`: macOS 上的沙箱化命令无法监听端口，也无法直接连接到 localhost 上的服务器
* **Default**: `false`

```json settings.json theme={null}
{
  "sandbox": {
    "network": {
      "allowLocalBinding": true
    }
  }
}
```

<h3 id="sandbox-network-allowmachlookup">
  `sandbox.network.allowMachLookup`
</h3>

列出 macOS 沙箱可能查找的其他 XPC 和 Mach 服务名称。通过 XPC 通信的工具，例如 iOS Simulator 或 Playwright，需要在此处列出其服务。

* **Scope**: [`Any file`](#scopes)，[项目和本地设置受到限制](/docs/zh-CN/sandboxing#repository-settings-under-an-admin-required-sandbox)
* **Type**: 字符串数组，每个是服务名称；单个尾部 `*` 匹配前缀，`"*"` 单独匹配每个服务
* **Default**: 未设置

这允许 `com.apple.coresimulator.` 前缀下的每个服务：

```json settings.json theme={null}
{
  "sandbox": {
    "network": {
      "allowMachLookup": ["com.apple.coresimulator.*"]
    }
  }
}
```

<h3 id="sandbox-network-alloweddomains">
  `sandbox.network.allowedDomains`
</h3>

预先允许来自沙箱化命令的出站流量的域，因此沙箱不会为它们提示。通配符（如 `*.example.com` ）匹配子域，可选的 `:port` 后缀将条目限制为一个端口；没有端口的条目匹配每个端口。

* **Scope**: [`Any file`](#scopes)，[项目和本地设置受到限制](/docs/zh-CN/sandboxing#repository-settings-under-an-admin-required-sandbox)。当设置了 [`allowManagedDomainsOnly`](#sandbox-network-allowmanageddomainsonly) 时，仅限托管设置。
* **Type**: 字符串数组，每个是域、通配符模式或 IP 文字，带有可选的 `:port` 后缀
* **Default**: 未设置，因此由您的权限模式决定[每个新主机的处理方式](/docs/zh-CN/sandboxing#hosts-outside-your-allowed-domains)

这预先允许 GitHub 在每个端口、每个 npm 子域和一个 API 主机仅在端口 443 上：

```json settings.json theme={null}
{
  "sandbox": {
    "network": {
      "allowedDomains": ["github.com", "*.npmjs.org", "api.example.com:443"]
    }
  }
}
```

将 IPv6 文字写成括号形式，带有可选端口：`"[::1]"` 允许每个端口，`"[::1]:443"` 一个端口。括号形式需要 Claude Code v2.1.229 或更高版本。请参阅 [IPv6 addresses in domain lists](/docs/zh-CN/sandboxing#ipv6-addresses-in-domain-lists)。

<h3 id="sandbox-network-denieddomains">
  `sandbox.network.deniedDomains`
</h3>

阻止来自沙箱化命令的出站流量的域，使用与 [`allowedDomains`](#sandbox-network-alloweddomains) 相同的通配符、端口和 IPv6 语法。被拒绝的域即使 `allowedDomains` 条目也匹配它也保持阻止。

* **Scope**: [`Any file`](#scopes)
* **Type**: 字符串数组，每个是域、通配符模式或 IP 文字，带有可选的 `:port` 后缀
* **Default**: 未设置

```json settings.json theme={null}
{
  "sandbox": {
    "network": {
      "deniedDomains": ["sensitive.cloud.example.com"]
    }
  }
}
```

Claude Code 从会话加载的每个设置源合并此列表，即使设置了 `allowManagedDomainsOnly`，因此开发人员总是可以收紧拒绝列表。对于 IPv6 文字，请参阅 [IPv6 addresses in domain lists](/docs/zh-CN/sandboxing#ipv6-addresses-in-domain-lists)。

使用标记完全限定域名的尾部点编写的条目，例如 `example.com.`，阻止与 `example.com` 相同的连接。

<h3 id="sandbox-network-strictallowlist">
  `sandbox.network.strictAllowlist`
</h3>

拒绝沙箱化命令访问允许列表外的主机，而不是提示批准。允许列表是 [`allowedDomains`](#sandbox-network-alloweddomains) 加上来自 `WebFetch(domain:...)` 允许规则的域，或者当设置了 [`allowManagedDomainsOnly`](#sandbox-network-allowmanageddomainsonly) 时仅为托管设置条目。[Locks that apply without an admin-required sandbox](/docs/zh-CN/sandboxing#locks-that-apply-without-an-admin-required-sandbox) 涵盖仓库的条目。需要 Claude Code v2.1.219 或更高版本。

* **Scope**: [`User or managed`](#scopes)。存储库无法打开或关闭它。
* **Type**: 布尔值
  * `true`: Claude Code 拒绝沙箱化命令访问允许列表外的主机
  * `false`: 除非另一个受信任的设置文件设置 `true`，Claude Code 根据权限模式而不是直接拒绝来决定允许列表外的主机：它在自动模式下检查主机对命令的 [per-command allowed domains](/docs/zh-CN/sandboxing#per-command-allowed-domains-in-auto-mode)，在 `dontAsk` 模式下拒绝，在 `bypassPermissions` 模式下允许，在交互式终端计划模式会话中当绕过可用时允许，否则询问您
* **Default**: `false`

```json settings.json theme={null}
{
  "sandbox": {
    "network": {
      "strictAllowlist": true
    }
  }
}
```

Claude Code 仅对沙箱化命令强制执行此；进程内工具（如 `WebFetch` ）仍然遵循其 [permission rules](/docs/zh-CN/sandboxing#permission-rules)。当任何遵守的源将其设置为 `true` 时，它保持打开。请参阅 [Network isolation](/docs/zh-CN/sandboxing#network-isolation)。需要 Claude Code v2.1.219 或更高版本。

<h3 id="sandbox-network-allowmanageddomainsonly">
  `sandbox.network.allowManagedDomainsOnly`
</h3>

将网络允许列表锁定到托管设置定义的内容。Claude Code 然后仅遵守来自托管设置的 `allowedDomains` 和 `WebFetch(domain:...)` 允许规则，忽略来自用户、项目、本地和 `--settings` 设置的域，并自动阻止非允许的域而不是提示。

* **Scope**: [`Managed`](#scopes)
* **Type**: 布尔值
  * `true`: Claude Code 仅遵守来自托管设置的 `allowedDomains` 和 `WebFetch(domain:...)` 允许规则，并阻止非允许的域而不是提示
  * `false`: 来自其他设置文件的域可以合并到允许列表中
* **Default**: `false`

这将允许列表锁定到 GitHub 和 npm，并忽略开发人员添加的任何域：

```json managed-settings.json theme={null}
{
  "sandbox": {
    "network": {
      "allowManagedDomainsOnly": true,
      "allowedDomains": ["github.com", "*.npmjs.org"]
    }
  }
}
```

当该键为 `true` 时，沙箱是[管理员强制要求的](/docs/zh-CN/sandboxing#repository-settings-under-an-admin-required-sandbox)，并且只有托管设置可以设置[代理端口](#sandbox-network-httpproxyport)。

被拒绝的域仍然从会话加载的每个源合并。请参阅 [Keep developers from widening the policy](/docs/zh-CN/sandboxing#keep-developers-from-widening-the-policy)。

<h3 id="sandbox-network-httpproxyport">
  `sandbox.network.httpProxyPort`
</h3>

将沙箱指向您自己的 HTTP 代理，而不是 Claude Code 运行的代理。组织这样做是为了检查 HTTPS 流量、应用自己的过滤规则或记录请求日志。您的代理将接管过滤，Claude Code 不再对发送到那里的流量应用其域列表和网络提示。未设置时，Claude Code 为 HTTP 流量启动自己的代理。

* **Scope**: [`Any file`](#scopes)，除非[其他沙箱设置限制了哪些文件可以设置端口](/docs/zh-CN/sandboxing#custom-proxy-configuration)
* **Type**: 数字，本地 TCP 端口
* **Default**: 未设置，因此 Claude Code 运行自己的代理

```json settings.json theme={null}
{
  "sandbox": {
    "network": {
      "httpProxyPort": 8080
    }
  }
}
```

如果您的代理也应该携带 SOCKS 流量，也设置 [`socksProxyPort`](#sandbox-network-socksproxyport)；仅设置其中一个，Claude Code 仍然为另一个协议运行自己的代理。请参阅 [Custom proxy configuration](/docs/zh-CN/sandboxing#custom-proxy-configuration)。

<h3 id="sandbox-network-socksproxyport">
  `sandbox.network.socksProxyPort`
</h3>

将沙箱指向您自己的 SOCKS5 代理，而不是 Claude Code 运行的代理。您的代理将接管过滤，Claude Code 不再对发送到那里的流量应用其域列表和网络提示。未设置时，Claude Code 为 SOCKS 流量启动自己的代理。

* **Scope**: [`Any file`](#scopes)，除非[其他沙箱设置限制了哪些文件可以设置端口](/docs/zh-CN/sandboxing#custom-proxy-configuration)
* **Type**: 数字，本地 TCP 端口
* **Default**: 未设置，因此 Claude Code 运行自己的代理

```json settings.json theme={null}
{
  "sandbox": {
    "network": {
      "socksProxyPort": 8081
    }
  }
}
```

请参阅 [Custom proxy configuration](/docs/zh-CN/sandboxing#custom-proxy-configuration)。

<h3 id="sandbox-network-tlsterminate">
  `sandbox.network.tlsTerminate`
</h3>

使沙箱代理终止 TLS，以便它可以读取 HTTPS 请求的内容。这是实验性的，`mask` [credential substitution](/docs/zh-CN/sandboxing#mask-credentials) 需要它。设置 `{}` 为会话生成临时证书颁发机构，或设置 `caCertPath` 和 `caKeyPath` 以使用您自己的。

* **Scope**: [`User or managed`](#scopes)。存储库无法打开它或提供证书颁发机构。
* **Type**: 对象，包含可选的 `caCertPath` 和 `caKeyPath` 字符串，每个是文件路径
* **Default**: 未设置，因此代理不终止或检查 TLS

```json settings.json theme={null}
{
  "sandbox": {
    "network": {
      "tlsTerminate": {}
    }
  }
}
```

当多个遵守的源设置它时，Claude Code 使用来自最高优先级源的值：托管设置，然后是 `--settings` 标志，然后是用户设置。

<span id="context-and-memory" />

<h2 id="memory-and-context">
  内存和上下文
</h2>

控制 Claude Code 加载到上下文中的内容、如何压缩以及在何处保存内存和计划。请参阅[管理上下文](/docs/zh-CN/context-window)和[内存](/docs/zh-CN/memory)。

<h3 id="autocompactenabled">
  `autoCompactEnabled`
</h3>

当上下文接近限制时，让 Claude Code [自动压缩对话](/docs/zh-CN/context-window#when-your-context-fills-up)。在 `/config` 中显示为**自动压缩**，在那里切换它会将此键写入您的用户设置。

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`: 当上下文接近限制时，Claude Code 自动压缩对话
  * `false`: Claude Code 不自动压缩
* **Default**: `true`
* **Per-session overrides**: [`DISABLE_AUTO_COMPACT`](/docs/zh-CN/env-vars) 为一个会话关闭自动压缩；两者中任何一个关闭它，另一个就无法将其打开

```json settings.json theme={null}
{
  "autoCompactEnabled": false
}
```

手动 `/compact` 命令在自动压缩关闭时继续工作。

<h3 id="autocompactwindow">
  `autoCompactWindow`
</h3>

设置在 Claude Code [自动压缩](/docs/zh-CN/context-window#when-your-context-fills-up)之前上下文窗口的填充程度。

* **Scope**: [`Any file`](#scopes)
* **Type**: 令牌数，从 `100000` 到 `1000000`。Claude Code 将值限制在您的模型的上下文窗口；[模型概览](https://platform.claude.com/docs/en/about-claude/models/overview)列出了每个模型的窗口
* **Default**: 未设置，因此 Claude Code 选择为您的模型调整的窗口
* **Per-session overrides**: [`--autocompact`](/docs/zh-CN/cli-reference#cli-flags) 对一个会话优先于此键，[`CLAUDE_CODE_AUTO_COMPACT_WINDOW`](/docs/zh-CN/env-vars) 优先于两者

```json settings.json theme={null}
{
  "autoCompactWindow": 500000
}
```

[`/autocompact`](/docs/zh-CN/commands#all-commands) 命令会在 [`modelSettings`](#modelsettings) 下为当前模型保存一个窗口，对于该模型，它优先于同一文件中的此键。[设置自动压缩窗口](/docs/zh-CN/model-config#set-the-auto-compact-window)涵盖了命令、标志、变量和设置如何相互作用。

<h3 id="automemorydirectory">
  `autoMemoryDirectory`
</h3>

将[自动内存](/docs/zh-CN/memory#storage-location)存储在您选择的目录中，而不是每个项目的默认值。

* **Scope**: [`Any file`](#scopes)
* **Type**: 字符串，绝对路径或 `~/` 前缀的目录路径
* **Default**: 未设置，因此 Claude Code 使用 `~/.claude/projects/<project>/memory/`

```json settings.json theme={null}
{
  "autoMemoryDirectory": "~/my-memory-dir"
}
```

从项目或本地设置中，Claude Code 在与 [hooks 相同的工作区信任规则](/docs/zh-CN/permissions#what-runs-before-you-trust-a-folder)下遵守此键，因为克隆的存储库可以提供这些文件。

<h3 id="automemoryenabled">
  `autoMemoryEnabled`
</h3>

打开或关闭[自动内存](/docs/zh-CN/memory#enable-or-disable-auto-memory)。当为 `false` 时，Claude 不会从自动内存目录读取或写入。您也可以在会话期间使用 `/memory` 切换它，这会将此键写入您的用户设置。

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`: 与未设置相同；自动内存保持打开，除非优先于此键的内容为会话关闭它，例如 `--bare`、安全模式或 `CLAUDE_CODE_DISABLE_AUTO_MEMORY`
  * `false`: Claude 不会从自动内存目录读取或写入
* **Default**: `true`
* **Per-session overrides**: [`CLAUDE_CODE_DISABLE_AUTO_MEMORY`](/docs/zh-CN/env-vars) 对一个会话优先于此键，无论哪个方向

```json settings.json theme={null}
{
  "autoMemoryEnabled": false
}
```

<h3 id="bashoutputmaxchars">
  `bashOutputMaxChars`
</h3>

设置成功的 Bash 或 PowerShell 命令的[输出 Claude 内联接收](/docs/zh-CN/tools-reference#output-limits)的字符数。当输出超过限制时，Claude Code 将其保存到文件，Claude 接收简短预览加文件路径。当命令输出（例如详细构建或完整测试套件日志）经常超过默认值且您希望 Claude 在不打开文件的情况下读取它时，提高限制。需要 Claude Code v2.1.261 或更高版本。

* **Scope**: [`Any file`](#scopes)
* **Type**: 字符数，正整数。Claude Code 将值限制在 `4000` 到 `128000` 范围内
* **Default**: 未设置，因此 Claude 内联接收最多 30,000 个字符

```json settings.json theme={null}
{
  "bashOutputMaxChars": 100000
}
```

设置此键时，Claude Code 忽略 [`BASH_MAX_OUTPUT_LENGTH`](/docs/zh-CN/env-vars) 环境变量。

<h3 id="claudemd">
  `claudeMd`
</h3>

注入 CLAUDE.md 风格的说明作为组织管理的内存，无需部署单独的文件。Claude Code 将文本作为托管内存条目加载，位于用户和项目 CLAUDE.md 文件之前。

* **Scope**: [`Managed`](#scopes)
* **Type**: 字符串，CLAUDE.md 文件的文本；按照您编写文件的方式编写，包括 Markdown，行中断为 `\n`
* **Default**: 未设置

此示例将两个规则部署为简短的 Markdown 列表：

```json managed-settings.json theme={null}
{
  "claudeMd": "# Engineering rules\n\n- Always run make lint before committing.\n- Never push directly to main."
}
```

请参阅[部署组织范围的 CLAUDE.md](/docs/zh-CN/memory#deploy-organization-wide-claude-md)。

<h3 id="claudemdexcludes">
  `claudeMdExcludes`
</h3>

当 Claude Code 加载[内存](/docs/zh-CN/memory#exclude-specific-claude-md-files)时跳过特定的 `CLAUDE.md` 文件。在大型单体仓库中，使用它跳过来自与您的工作无关的其他团队的 CLAUDE.md 文件；大型代码库指南中的[排除无关的 CLAUDE.md 文件](/docs/zh-CN/large-codebases#exclude-irrelevant-claude-md-files)演示了该情况。模式与绝对文件路径匹配。

* **Scope**: [`Any file`](#scopes)
* **Type**: 字符串数组，每个都是 glob 模式或绝对路径
* **Default**: 未设置，因此 Claude Code 加载它找到的每个 CLAUDE.md

```json settings.json theme={null}
{
  "claudeMdExcludes": ["**/vendor/**/CLAUDE.md"]
}
```

排除仅适用于用户、项目和本地内存文件；托管策略 CLAUDE.md 文件无法被排除。

<span id="environment-variables" />

<h3 id="env">
  `env`
</h3>

为每个会话和 Claude Code 从中启动的子进程设置环境变量。[环境变量参考](/docs/zh-CN/env-vars)中的大多数变量都可以放在这里，这是如何将其应用于每个会话或向您的团队推出的方式。项目和本地设置无法设置[其中一些](#variables-claude-code-ignores-in-env)。

* **Scope**: [`Any file`](#scopes)
* **Type**: 将变量名映射到字符串值的对象
* **Default**: 未设置

此示例关闭自动压缩并通过代理路由 API 请求：

```json settings.json theme={null}
{
  "env": {
    "DISABLE_AUTO_COMPACT": "1",
    "ANTHROPIC_BASE_URL": "https://proxy.example.com"
  }
}
```

<h4 id="how-env-values-interact-with-your-shell">
  `env` 值如何与您的 shell 交互
</h4>

* 此处的值覆盖在您的 shell 中导出的相同变量，当多个设置文件设置一个变量时，[最高优先级](/docs/zh-CN/settings#settings-precedence)的值适用。[Claude Code 在 `env` 中忽略的变量](#variables-claude-code-ignores-in-env)列出了项目和本地设置的例外。
* 当 Claude Desktop 应用或[自托管环境](/docs/zh-CN/self-hosted-environments)运行器启动会话时，它构建的启动环境优先：Claude Code 忽略任何设置文件中的 `env` 值，用于启动环境已经设置的变量。[调试日志](/docs/zh-CN/debug-your-config)命名每个被忽略的变量。
* 要取消 shell 导出，将变量设置为 `""`。Claude Code 将空值视为提供程序选择的未设置，子进程继承空值。
* `NO_COLOR` 和 `FORCE_COLOR` 在此处设置仅到达子进程。要更改 Claude Code 自己的界面颜色，请在启动 `claude` 之前在您的 shell 中设置它们。
* 此处的值是设置文件中的纯文本，到达 Claude Code 启动的每个子进程。对于轮换的 OTLP 承载令牌，使用 [`otelHeadersHelper`](#otelheadershelper)；对于 API 凭证，使用 [`apiKeyHelper`](#apikeyhelper)。

<h4 id="when-claude-code-applies-env-values">
  Claude Code 何时应用 `env` 值
</h4>

* 从用户设置、`--settings` 和托管设置：在启动时，以及在运行会话中当保存的更改改变合并的 `env` 时。
* 从项目和本地设置：在您信任工作区后，或在 `-p` 模式下启动时（从不显示信任对话），以及当保存的更改改变合并的 `env` 时。
* Claude Code 分类为安全的变量，例如模型选择、超时和限制、功能切换：在启动时从每个设置文件，除了[项目和本地设置无法设置的变量](#variables-claude-code-ignores-in-env)。
* 在 v2.1.246 或更高版本上使用 `/cd` [移动会话](/docs/zh-CN/permissions#move-the-session-to-another-directory)后：新目录的项目和本地 `env` 值，在前一个目录的基础上。

<h4 id="variables-claude-code-ignores-in-env">
  Claude Code 在 `env` 中忽略的变量
</h4>

* 项目和本地设置无法设置已检出的仓库不应控制的变量；改为在您的 shell、用户设置或托管设置中设置这些变量。除少数关闭遥测的值外，Claude Code 删除每个变量并记录您可以使用 `claude --debug` 看到的警告。它们包括：

  * 选择 Claude Code 存储或写入其自己文件的位置的变量：`CLAUDE_CONFIG_DIR`、`CLAUDE_CODE_TMPDIR` 和操作系统目录变量，例如 `HOME`、`TMPDIR`、`TMP`、`TEMP` 和 `XDG_*` 系列。
  * 为 Claude Code 启动的进程选择程序和机器范围配置的 Windows 变量，例如 `SystemRoot`、`ComSpec`、`ProgramData`、`LOCALAPPDATA`、`PATHEXT`、`PSModulePath` 和 `ProgramFiles` 系列。
  * 导出会话内容的变量：[`OTEL_LOG_RAW_API_BODIES`](/docs/zh-CN/env-vars#variables) 和详细的 beta 跟踪对 `ENABLE_BETA_TRACING_DETAILED` 和 `BETA_TRACING_ENDPOINT`。
  * [OpenTelemetry 导出器](/docs/zh-CN/monitoring-usage)变量，打开遥测、选择它的去向或选择它捕获的内容：

    * `CLAUDE_CODE_ENABLE_TELEMETRY`，加上增强的遥测 beta 对 `CLAUDE_CODE_ENHANCED_TELEMETRY_BETA` 和 `ENABLE_ENHANCED_TELEMETRY_BETA`
    * 导出器选择器 `OTEL_LOGS_EXPORTER`、`OTEL_METRICS_EXPORTER` 和 `OTEL_TRACES_EXPORTER`
    * 内容变量 `OTEL_LOG_USER_PROMPTS`、`OTEL_LOG_ASSISTANT_RESPONSES`、`OTEL_LOG_TOOL_CONTENT` 和 `OTEL_LOG_TOOL_DETAILS`
    * `OTEL_EXPORTER_OTLP_*` 变量，其名称以 `_ENDPOINT`、`_HEADERS`、`_PROTOCOL`、`_CERTIFICATE`、`_CLIENT_KEY` 或 `_INSECURE` 结尾，采用通用和按信号形式，例如 `OTEL_EXPORTER_OTLP_ENDPOINT` 和 `OTEL_EXPORTER_OTLP_METRICS_HEADERS`
    * `OTEL_EXPORTER_PROMETHEUS_HOST` 和 `OTEL_EXPORTER_PROMETHEUS_PORT`

    只有这些值仍然适用于项目和本地设置，因为它们关闭某些内容：三个导出器选择器的 `none`，以及 `OTEL_LOG_USER_PROMPTS`、`OTEL_LOG_TOOL_CONTENT` 和 `OTEL_LOG_TOOL_DETAILS` 的关闭值，例如 `0`。这样的值覆盖您的用户设置中的相同变量，但不覆盖您启动 Claude Code 的环境、`--settings` 文件或托管设置设置的变量。

    当项目或本地设置文件设置此组中的变量时，本地交互式会话在启动时显示通知。运行 `/status` 或 `claude doctor` 以查看 Claude Code 忽略了哪些变量以及哪些关闭了遥测；两者都列出名称，从不列出值。非交互式运行（使用 `-p` 或 Agent SDK 会话）不显示通知，因此在升级后检查您的收集器是否仍然接收数据。如果没有，请在您的用户设置、托管设置、作业的环境或您使用 `--settings` 传递的文件中设置变量。

    在项目和本地设置中忽略此组需要 Claude Code v2.1.282 或更高版本。
  * 改变 Claude Code 如何启动或同步的变量，例如 `CLAUDE_CODE_PROCESS_WRAPPER`、`CLAUDE_CODE_SYNC_SKILLS`、`CLAUDE_CODE_SYNC_PLUGINS`、`CLAUDE_CODE_PLUGIN_CACHE_DIR` 和 `CLAUDE_CODE_PLUGIN_SEED_DIR`。
  * 设置未应答对话框计时器的变量：[`CLAUDE_CODE_USER_DIALOG_TIMEOUT_MS`、`CLAUDE_AFK_TIMEOUT_MS` 和 `CLAUDE_AFK_COUNTDOWN_MS`](/docs/zh-CN/env-vars#variables)。
  * [`CLAUDE_CODE_DISABLE_ATTACHMENTS`](/docs/zh-CN/env-vars#variables)，它会关闭附件处理。

  在 v2.1.251 之前，项目和本地设置也可以设置此列表中选择 Claude Code 写入其文件位置或导出会话内容的变量，除了 `HOME` 和 `XDG_CONFIG_HOME`。在 v2.1.290 之前，它们还可以设置对话框计时器变量和 `CLAUDE_CODE_DISABLE_ATTACHMENTS`。
* Claude Code 的托管环境拥有的身份变量，例如 `CLAUDE_CODE_REMOTE` 和 `CLAUDE_CODE_ACCOUNT_UUID`，从每个文件中被忽略。
* [`CLAUDE_CODE_MESSAGING_SOCKET` 和 `CLAUDE_CODE_MESSAGING_TOKEN`](/docs/zh-CN/env-vars#variables)，Claude Code 自己导出的，从每个文件中被忽略。忽略套接字变量需要 Claude Code v2.1.224 或更高版本，忽略令牌需要 v2.1.228 或更高版本。
* [`CLAUDE_CODE_PROJECT_DIR_NAME`](/docs/zh-CN/sessions#name-the-project-directory-yourself)，Claude Code 仅从启动环境读取，从每个文件中被忽略；需要 v2.1.234 或更高版本。
* [`CLAUDE_CODE_RESTRICTED`](/docs/zh-CN/env-vars#variables)，Claude Code 仅从启动环境读取，从每个文件中被忽略。
* [`CLAUDE_CODE_DISABLE_POWERSHELL_CMD_RM_DENY`](/docs/zh-CN/env-vars#variables)，Claude Code 仅从启动环境读取，从每个文件中被忽略。该变量需要 Claude Code v2.1.283 或更高版本。
* [`CLAUDE_CODE_DISABLE_DANGEROUS_RM_TIMEOUT`、`CLAUDE_CODE_DISABLE_SUBSTITUTION_RM_PROMPT` 和 `CLAUDE_CODE_DISABLE_INLINE_SHELL_RM_PROMPT`](/docs/zh-CN/env-vars#variables)，Claude Code 仅从启动环境读取，从每个文件中被忽略。

<h3 id="filecheckpointingenabled">
  `fileCheckpointingEnabled`
</h3>

让 Claude Code 在每次编辑前快照文件，以便 [`/rewind`](/docs/zh-CN/checkpointing) 可以恢复它们。在 `/config` 中显示为**回退代码（检查点）**，在那里切换它会将此键写入您的用户设置。

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`: Claude Code 在每次编辑前快照文件，以便 `/rewind` 可以恢复它们
  * `false`: Claude Code 不快照文件，因此 `/rewind` 无法恢复它们
* **Default**: `true`
* **Per-session overrides**: [`CLAUDE_CODE_DISABLE_FILE_CHECKPOINTING`](/docs/zh-CN/env-vars) 为一个会话关闭检查点；两者中任何一个关闭它，另一个就无法将其打开

```json settings.json theme={null}
{
  "fileCheckpointingEnabled": false
}
```

在 `-p` 运行或 Agent SDK 会话中，Claude Code 忽略此键。SDK 使用其 `enableFileCheckpointing` 选项打开检查点，裸 `-p` 运行需要 `CLAUDE_CODE_ENABLE_SDK_FILE_CHECKPOINTING=true`。请参阅 [Agent SDK 中的文件检查点](/docs/zh-CN/agent-sdk/file-checkpointing)。

<h3 id="plansdirectory">
  `plansDirectory`
</h3>

选择 Claude Code 在[计划模式](/docs/zh-CN/permission-modes#analyze-before-you-edit-with-plan-mode)中写入的计划文件的存储位置。Claude Code 相对于项目根目录解析路径。

* **Scope**: [`Any file`](#scopes)
* **Type**: 字符串，相对于项目根目录的路径
* **Default**: 未设置，因此 Claude Code 使用 `~/.claude/plans`

```json settings.json theme={null}
{
  "plansDirectory": "./plans"
}
```

在以下情况下，Claude Code 会将计划存储在 `~/.claude/plans` 中，而不是您设置的目录中：

* **位于项目根目录之外**：路径解析到项目根目录之外，例如 `"../plans"`。
* **在 macOS、Linux 和 WSL 上包含反斜杠**：解析后的路径包含反斜杠，例如 Windows 风格的 `"docs\\plans"`。请写成 `"docs/plans"`，它在 Windows 上同样适用。

<h3 id="skilllistingbudgetfraction">
  `skillListingBudgetFraction`
</h3>

每个回合，Claude 看到[您的技能列表](/docs/zh-CN/skills#skill-descriptions-are-cut-short)及其描述，Claude Code 将该列表限制在上下文窗口的一部分。当列表超过上限时，Claude Code 保留每个技能的名称，但删除使用最少的技能的描述，因此 Claude 仍然可以调用这些技能，但不太可能自己选择一个。提高此键以保持更多描述可见，代价是每个回合更多上下文。

* **Scope**: [`Any file`](#scopes)
* **Type**: 数字，大于 `0` 且最多 `1` 的分数
* **Default**: `0.01`，保留 1% 的上下文窗口

```json settings.json theme={null}
{
  "skillListingBudgetFraction": 0.02
}
```

要查看列表使用多少上下文以及哪些技能贡献最多，请运行 `/doctor`。

<h3 id="skilllistingmaxdescchars">
  `skillListingMaxDescChars`
</h3>

每个回合，Claude 看到[您的技能列表](/docs/zh-CN/skills#skill-descriptions-are-cut-short)，显示每个技能的 `description` 和 `when_to_use` 文本。此键限制 Claude Code 每个技能显示多少字符的该文本；较长的文本在上限处被切割。

* **Scope**: [`Any file`](#scopes)
* **Type**: 字符数，正整数
* **Default**: `1536`

```json settings.json theme={null}
{
  "skillListingMaxDescChars": 2048
}
```

提高它以保持长描述完整，代价是每个回合更多上下文；降低它以在 [`skillListingBudgetFraction`](#skilllistingbudgetfraction) 下适应更多技能。

<h3 id="taskoutputmaxchars">
  `taskOutputMaxChars`
</h3>

<Warning>
  在 v2.1.277 中删除，连同它调整大小的 `TaskOutput` 工具一起。设置它对当前版本没有影响。Claude 使用 `Read` 读取后台任务的[输出文件](/docs/zh-CN/tools-reference#background-commands)。
</Warning>

通过 v2.1.276，您将此键设置为[后台任务](/docs/zh-CN/tools-reference#background-commands)的输出字符数，当 Claude 使用 `TaskOutput` 工具读取任务时 Claude 内联接收。

<h2 id="interface-and-terminal">
  界面和终端
</h2>

改变 Claude Code 在终端中的外观和行为：主题、编辑器模式、状态行、加载动画、会话内通知和无障碍功能。请参阅[终端配置](/docs/zh-CN/terminal-config)。

<h3 id="askuserquestiontimeout">
  `askUserQuestionTimeout`
</h3>

让未回答的 [`AskUserQuestion`](/docs/zh-CN/tools-reference) 对话框在空闲一段时间后自动继续，提交您已选择的任何选项。当您离开时设置此项，让 Claude 在没有您的情况下继续。使用默认设置时，问题会等待您回答。关于计时器何时暂停或从不启动，请参阅[问题自动继续超时](/docs/zh-CN/tools-reference#question-auto-continue-timeout)。

* **Scope**: [`User or managed`](#scopes)
* **Type**: string，值为 `"60s"`、`"5m"`、`"10m"` 或 `"never"` 之一
* **Default**: `"never"`
* **Per-session overrides**: [`CLAUDE_AFK_TIMEOUT_MS`](/docs/zh-CN/env-vars) 在单个会话中优先于此键

```json settings.json theme={null}
{
  "askUserQuestionTimeout": "5m"
}
```

在 `/config` 中显示为**问题自动继续超时**，它将此键写入用户设置；当托管设置或 `--settings` 标志设置此键时，Claude Code 会隐藏该行。

<h3 id="autocontinueatusagelimit">
  `autoContinueAtUsageLimit`
</h3>

在 claude.ai 使用限制停止您的会话后，在打开的会话中等待，并在重置后自动继续任务。请参阅[关闭自动继续](/docs/zh-CN/interactive-mode#turn-automatic-continue-off)。需要 Claude Code v2.1.234 或更高版本。

* **Scope**: [`User or managed`](#scopes)。仅从用户设置、`--settings` 和托管设置中读取。当这些都没有设置此键时，设置此键的项目或本地设置文件会关闭该功能，而不是被忽略。
* **Type**: Boolean
  * `true`：在 claude.ai 使用限制停止您的会话后，Claude Code 在打开的会话中等待，并在重置后自动继续任务
  * `false`：Claude Code 不会自动启动等待。您仍然可以从使用限制选项菜单[自己启动等待](/docs/zh-CN/interactive-mode#start-a-wait-yourself)
* **Default**: `true`

```json settings.json theme={null}
{
  "autoContinueAtUsageLimit": false
}
```

在 `/config` 中显示为**在使用限制时自动继续**，它将此键写入用户设置；当托管设置或 `--settings` 标志设置此键时，Claude Code 会隐藏该行。

<h3 id="autoscrollenabled">
  `autoScrollEnabled`
</h3>

在[全屏渲染](/docs/zh-CN/fullscreen)中跟随新输出到对话底部。关闭它以在 Claude 继续工作时保持您滚动的位置；权限提示仍会滚动到视图中。

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`：对话跟随新输出到底部
  * `false`：当 Claude 继续工作时，您保持在滚动的位置；权限提示仍会显示在记录下方
* **Default**: `true`

```json settings.json theme={null}
{
  "autoScrollEnabled": false
}
```

在全屏渲染打开时，在 `/config` 中显示为**自动滚动**，它将此键写入用户设置。

<h3 id="axscreenreader">
  `axScreenReader`
</h3>

渲染屏幕阅读器友好的输出：没有装饰性边框或动画的平面文本。屏幕阅读器模式使用经典渲染器，因此在它处于活动状态时 `tui` 设置无效；附加的[后台会话](/docs/zh-CN/agent-view)仍会全屏渲染。

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`：Claude Code 使用经典渲染器渲染没有装饰性边框或动画的平面文本
  * `false`：Claude Code 正常渲染
* **Default**: unset，所以屏幕阅读器模式关闭
* **Per-session overrides**: [`--ax-screen-reader`](/docs/zh-CN/cli-reference#cli-flags) 优先于 [`CLAUDE_AX_SCREEN_READER`](/docs/zh-CN/env-vars)，两者都优先于单个会话的此键

```json settings.json theme={null}
{
  "axScreenReader": true
}
```

<h3 id="basheditdiffenabled">
  `bashEditDiffEnabled`
</h3>

选择 Claude Code 是否记录 Bash 命令运行期间 Git 存储库中发生更改的文件。当它记录它们时，您会在命令后在终端中看到它们的差异，您的 [PostToolUse Bash hooks](/docs/zh-CN/hooks#bash) 会接收更改的文件列表。

列出的文件并不总是命令更改的文件。命令运行时另一个程序或另一个 Bash 调用所做的更改也可能出现在那里。

将键设置为 `true` 以在每个权限模式中记录它们。需要 Claude Code v2.1.269 或更高版本。

* **Scope**: [`User or managed`](#scopes)。`true` 仅从您的用户设置、使用 `--settings` 传递的 JSON 或[托管设置](/docs/zh-CN/managed-settings)计数，因此存储库的 `.claude/settings.json` 或 `.claude/settings.local.json` 中的 `true` 无法打开记录。存储库文件中的 `false` 仍会关闭它，除非[更高优先级](/docs/zh-CN/settings#settings-precedence)的文件设置 `true`。
* **Type**: Boolean
* **Default**: unset，所以当 Claude Code 指导 Claude 通过 Bash 编辑文件时，Claude Code 在自动模式和 `bypassPermissions` 模式中记录更改
* **Per-session overrides**: [`CLAUDE_CODE_BASH_EDIT_DIFF`](/docs/zh-CN/env-vars) 在单个会话中优先于此键

```json settings.json theme={null}
{
  "bashEditDiffEnabled": true
}
```

<h3 id="companyannouncements">
  `companyAnnouncements`
</h3>

在启动时向用户显示您组织的公告。当您列出多个公告时，Claude Code 为每个会话随机选择一个；在某人的首次启动时，它显示第一个条目。

* **Scope**: [`Any file`](#scopes)
* **Type**: array of strings
* **Default**: unset，所以不显示公告

```json settings.json theme={null}
{
  "companyAnnouncements": [
    "欢迎来到 Acme Corp！请在 docs.example.com 查看我们的代码指南"
  ]
}
```

<h3 id="defaultshell">
  `defaultShell`
</h3>

选择 Bash 或 PowerShell 是否运行您在输入框中使用 [`!` 前缀](/docs/zh-CN/interactive-mode#shell-mode-with-prefix)键入的 shell 命令，以及 Claude Code 直接运行并添加到会话的命令。

`"powershell"` 仅在 [PowerShell tool](/docs/zh-CN/tools-reference#powershell-tool) 打开时有效。该工具在没有 Git Bash 的 Windows 上默认打开，在带有 Git Bash 的 Windows 上对于 claude.ai 和 Console 账户默认打开。在 Amazon Bedrock、Google Cloud 的 Agent Platform 和 Microsoft Foundry 会话中，以及在 macOS、Linux 和 WSL 上，设置 `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` 以打开该工具。将该变量设置为 `0` 以关闭该工具。

* **Scope**: [`Any file`](#scopes)
* **Type**: string，值为以下之一：
  * `"bash"`：Claude Code 在 Bash 中运行您的 `!` 命令
  * `"powershell"`：Claude Code 在 PowerShell 中运行您的 `!` 命令
* **Default**: `"bash"`，或在 Bash 不可用时在 Windows 上为 `"powershell"`

```json settings.json theme={null}
{
  "defaultShell": "powershell"
}
```

如果您指定的 shell 不可用，Claude Code 会使用另一个：当 PowerShell 工具关闭时 `"powershell"` 回退到 Bash，当 Bash 未安装时 `"bash"` 回退到 PowerShell。

<h3 id="dialogexpiry">
  `dialogExpiry`
</h3>

为 Claude Code [转发给远程客户端](/docs/zh-CN/remote-control#limitations)的对话框（例如远程控制或 SDK 主机）以及[保留的跨会话消息](/docs/zh-CN/cross-session-messaging#control-inbound-messages)的批准对话框设置截止时间。在 Claude Code v2.1.236 或更高版本上，相同的截止时间限制了会话中可能没有人在终端的中期 [Fable 使用额度同意提示](/docs/zh-CN/model-config#fable-and-usage-credits)。当在截止时间前没有答案到达时，Claude Code 取消对话框并继续使用其无操作默认值。需要 Claude Code v2.1.224 或更高版本。

* **Scope**: [`User or managed`](#scopes)
* **Type**: string，值为 `"60s"`、`"5m"`、`"10m"` 或 `"never"` 之一，后者禁用截止时间
* **Default**: `"5m"`
* **Per-session overrides**: [`CLAUDE_CODE_USER_DIALOG_TIMEOUT_MS`](/docs/zh-CN/env-vars) 在单个会话中优先于此键

```json settings.json theme={null}
{
  "dialogExpiry": "10m"
}
```

权限提示和 [`AskUserQuestion`](/docs/zh-CN/tools-reference#askuserquestion-tool-behavior) 问题使用它们自己的流程，不受此截止时间管制。在 `/config` 中显示为**对话框过期**，它将此键写入用户设置；该行需要 Claude Code v2.1.232 或更高版本，当托管设置或 `--settings` 标志设置此键时，Claude Code 会隐藏它。

<h3 id="editormode">
  `editorMode`
</h3>

为输入提示选择快捷键绑定模式。

* **Scope**: [`Any file`](#scopes)
* **Type**: string，值为以下之一：
  * `"normal"`：提示输入中的标准快捷键
  * `"vim"`：vim 风格编辑，具有 NORMAL、INSERT 和 VISUAL 模式
* **Default**: `"normal"`

```json settings.json theme={null}
{
  "editorMode": "vim"
}
```

在 `/config` 中显示为**编辑器模式**，它将此键写入用户设置。

<h3 id="emojicompletionenabled">
  `emojiCompletionEnabled`
</h3>

当您在提示输入中键入 `:` 加上速记代码时显示表情符号建议，并将完成的速记代码（如 `:heart:`）替换为其表情符号。将其设置为 `false` 以关闭两者。

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`：Claude Code 在 `:` 后显示表情符号建议，并将完成的速记代码替换为其表情符号
  * `false`：Claude Code 既不建议表情符号也不替换速记代码
* **Default**: `true`

```json settings.json theme={null}
{
  "emojiCompletionEnabled": false
}
```

请参阅[表情符号速记代码](/docs/zh-CN/interactive-mode#emoji-shortcodes)。需要 Claude Code v2.1.217 或更高版本。

<span id="file-suggestion-settings" />

<h3 id="filesuggestion">
  `fileSuggestion`
</h3>

运行您自己的命令来提供 `@` 文件路径自动完成，而不是使用内置文件建议。内置建议使用快速文件系统遍历；大型单体仓库可能会通过项目特定的索引（如预构建的文件索引）做得更好。

* **Scope**: [`Any file`](#scopes)。在[状态行和文件建议门](#status-line-and-file-suggestion-gates)下，Claude Code 关闭命令或仅运行托管值，并跳过您的而不发出警告。
* **Type**: 对象，包含 `type`（始终为 `"command"`）和 `command`（要运行的 shell 命令）
* **Default**: unset，所以 Claude Code 使用内置文件建议

```json settings.json theme={null}
{
  "fileSuggestion": {
    "type": "command",
    "command": "~/.claude/file-suggestion.sh"
  }
}
```

保存后，在提示中键入 `@` 后跟部分路径：建议来自您命令的输出。

<h4 id="command-input-and-output">
  命令输入和输出
</h4>

Claude Code 使用与 [hooks](/docs/zh-CN/hooks) 相同的环境变量运行命令，包括 `CLAUDE_PROJECT_DIR`，并在五秒后停止等待。该命令在 stdin 上接收 JSON，其中 `query` 字段包含您到目前为止键入的内容：

```json theme={null}
{"query": "src/comp"}
```

将换行符分隔的文件路径打印到 stdout。Claude Code 最多显示 15 个：

```text theme={null}
src/components/Button.tsx
src/components/Modal.tsx
src/components/Form.tsx
```

以下脚本读取查询并将其传递给存储库文件索引：

```bash theme={null}
#!/bin/bash
query=$(cat | jq -r '.query')
# 用您自己的文件搜索命令替换 your-repo-file-index
your-repo-file-index --query "$query" | head -20
```

<span id="footer-link-badges" />

<h3 id="footerlinksregexes">
  `footerLinksRegexes`
</h3>

当正则表达式匹配转向输出时在输入框下方的页脚中渲染额外的可点击徽章：工具结果，包括文件内容和获取的页面，以及 Claude 自己的响应。使用它将项目 CLI 打印的 ID（如审查工具和问题跟踪器）转换为会话链接。

* **Scope**: [`User or managed`](#scopes)
* **Type**: 对象数组，每个对象的 `type` 设置为 `"regex"`、`pattern` 正则表达式、`url` 模板和可选的 `label`；`url` 和 `label` 中的 `{name}` 占位符从 `pattern` 中的命名捕获组填充
* **Default**: unset，所以不渲染徽章

此示例匹配问题键（如 `PROJ-1234`）并从捕获的键构建每个链接：

```json settings.json theme={null}
{
  "footerLinksRegexes": [
    {
      "type": "regex",
      "pattern": "\\b(?<key>PROJ-\\d+)\\b",
      "url": "https://issues.example.com/browse/{key}",
      "label": "{key}"
    }
  ]
}
```

配置此项后，当 `PROJ-1234` 出现在工具结果或 Claude 的回复中时，页脚中会出现一个 `PROJ-1234` 徽章，链接到 `https://issues.example.com/browse/PROJ-1234`。

<h4 id="badge-constraints">
  徽章约束
</h4>

每个条目的 URL、标签和徽章计数受以下限制：

| 约束 | 行为 |
| :- | :- |
| URL 源 | 捕获的值是 URL 编码的，构造的 URL 必须共享模板的字面源。捕获可以填充路径段或查询值，但不能改变链接指向的位置 |
| URL 长度 | 长于 2048 个字符的构造 URL 被丢弃 |
| URL 方案 | 必须是 `https`、`http` 或公认的编辑器或工作区深层链接方案：`vscode`、`vscode-insiders`、`cursor`、`windsurf`、`zed`、`jetbrains`、`idea`、`slack`、`linear`、`notion`、`figma` |
| 标签 | 默认为匹配的文本，截断为 28 个显示列 |
| 徽章计数 | 最多渲染 5 个徽章。最旧的被较新的匹配替换，`/clear` 删除它们 |

当转向完成时，Claude Code 在主线程上将每个条目的 `pattern` 正则表达式与转向输出匹配，因此缓慢的正则表达式会阻止 UI 直到完成。嵌套量词（如 `(a+)+$`）对某些输入可能需要指数级长的时间并冻结会话，因此保持每个 `pattern` 线性并避免嵌套 `+` 或 `*`。

页脚徽章与[自定义状态行](/docs/zh-CN/statusline)一起渲染（当配置了一个时）；两者都不替换另一个。使用状态行来获得从会话数据计算自己内容的脚本驱动行，使用页脚徽章将对话中的 ID 转换为链接而无需脚本。

<h3 id="keybindingflavor">
  `keybindingFlavor`
</h3>

<Warning>
  自 v2.1.261 起已弃用，无效。提示的单词编辑键始终[遵循 readline 约定](/docs/zh-CN/interactive-mode#make-ctrl-w-delete-back-to-whitespace)，如在 Bash 中一样。Claude Code 仍然接受 `keybindingFlavor`，因此设置它的设置文件保持有效。
</Warning>

在 v2.1.238 到 v2.1.260 中，将其设置为 `"readline"` 使 `Ctrl+W` 删除回到前一个空格而不仅仅是前一个单词。

* **Scope**: [`Any file`](#scopes)
* **Type**: string，`"classic"` 或 `"readline"`
* **Default**: unset

<h3 id="maxprosewidth">
  `maxProseWidth`
</h3>

限制 Claude 响应中散文的宽度，使行在宽终端中保持可读性。段落、标题、列表和块引用在此列数内换行，而表格和代码块保持完整的终端宽度。需要 Claude Code v2.1.282 或更高版本。

* **Scope**: [`Any file`](#scopes)
* **Type**: 终端列数，整数，最小 `40`。Claude Code 忽略任何其他值
* **Default**: unset，所以散文在终端边缘换行

```json settings.json theme={null}
{
  "maxProseWidth": 80
}
```

<h3 id="prefersreducedmotion">
  `prefersReducedMotion`
</h3>

减少或关闭界面动画，如加载动画、闪烁和闪光效果。在 `/config` 中显示为**减少动画**。

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`：Claude Code 减少或关闭界面动画，如加载动画、闪烁和闪光效果
  * `false`：与 unset 相同；Claude Code 显示其动画
* **Default**: `false`

```json settings.json theme={null}
{
  "prefersReducedMotion": true
}
```

<h3 id="promptsuggestionenabled">
  `promptSuggestionEnabled`
</h3>

显示或隐藏[提示建议](/docs/zh-CN/interactive-mode#prompt-suggestions)，即在您的提示输入中出现的灰显预测。将其设置为 `false`，或在 `/config` 中关闭**提示建议**，以隐藏它们。

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`：您在提示输入中看到提示建议
  * `false`：Claude Code 隐藏提示建议
* **Default**: `true`
* **Per-session overrides**: [`CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION`](/docs/zh-CN/env-vars) 在单个会话中优先于此键

```json settings.json theme={null}
{
  "promptSuggestionEnabled": false
}
```

提示建议需要启用了遥测的 claude.ai 或 Console 账户。在 Amazon Bedrock、Google Cloud 的 Agent Platform 和 Microsoft Foundry 上，或关闭遥测时（如通过 [`DISABLE_TELEMETRY`](/docs/zh-CN/env-vars)），此键无效，仅 `CLAUDE_CODE_ENABLE_PROMPT_SUGGESTION=1` 打开它们。

<h3 id="respectgitignore">
  `respectGitignore`
</h3>

控制 `@` 文件选择器是否排除与 `.gitignore` 模式匹配的文件。在 `/config` 中显示为**在文件选择器中尊重 .gitignore**。

* **Scope**: [`Any file`](#scopes)。当没有设置文件设置它时，Claude Code 回退到 `~/.claude.json` 中的 `respectGitignore`，这是 `/config` 切换写入的。
* **Type**: Boolean
  * `true`：`@` 文件选择器排除与 `.gitignore` 模式匹配的文件
  * `false`：`@` 文件选择器包括与 `.gitignore` 模式匹配的文件
* **Default**: `true`

```json settings.json theme={null}
{
  "respectGitignore": false
}
```

<h3 id="respondtobashcommands">
  `respondToBashCommands`
</h3>

选择在您使用输入框中的 [`!` 前缀](/docs/zh-CN/interactive-mode#shell-mode-with-prefix)运行 shell 命令后 Claude 是否响应。默认情况下，Claude Code 将命令的输出添加到对话中，Claude 对其进行回复。将此键设置为 `false` 以将输出添加到上下文而不进行回复，以便您可以运行多个命令并一起询问它们。

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`：Claude Code 将命令的输出添加到对话中，Claude 对其进行回复
  * `false`：Claude Code 将输出添加到上下文而不进行回复
* **Default**: `true`

```json settings.json theme={null}
{
  "respondToBashCommands": false
}
```

请参阅[使用 `!` 前缀的 Shell 模式](/docs/zh-CN/interactive-mode#shell-mode-with-prefix)。

<h3 id="showclearcontextonplanaccept">
  `showClearContextOnPlanAccept`
</h3>

当 Claude 在[计划模式](/docs/zh-CN/permission-modes#review-and-approve-a-plan)中完成计划时，它显示一个批准菜单。规划可能会使用大量上下文，因此此键向该菜单添加第一个选项**是的，清除上下文并…**，它批准计划、清除对话上下文并仅从计划开始实施。标签的其余部分命名会话继续的权限模式，并显示规划使用了多少上下文。

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`：计划批准菜单获得第一个选项**是的，清除上下文并…**，它批准计划并清除对话上下文
  * `false`：计划批准菜单不显示清除上下文选项
* **Default**: `false`

```json settings.json theme={null}
{
  "showClearContextOnPlanAccept": true
}
```

<h3 id="showturnduration">
  `showTurnDuration`
</h3>

显示或隐藏每个响应后的转向持续时间消息，如"Cooked for 1m 6s · done 6:05 PM"。"done"后的时钟显示转向何时完成；[`timeFormat`](#timeformat) 和 [`timeZone`](#timezone) 控制其格式和区域。在 `/config` 中显示为**显示转向持续时间**。

* **Scope**: [`Any file`](#scopes)。当没有设置文件设置它时，来自较旧版本的 `~/.claude.json` 中的值适用。
* **Type**: Boolean
  * `true`：您在每个响应后看到转向持续时间消息
  * `false`：Claude Code 隐藏转向持续时间消息
* **Default**: `true`

```json settings.json theme={null}
{
  "showTurnDuration": false
}
```

<h3 id="spellcheck">
  `spellcheck`
</h3>

在您键入时在提示输入中为拼写错误的单词加下划线，使用您安装的拼写检查器。Claude Code 仅检查输入框中的文本。[在您键入时检查拼写](/docs/zh-CN/interactive-mode#check-spelling-as-you-type)涵盖安装 aspell、hunspell 或 ispell 以及检查器涵盖的内容。需要 Claude Code v2.1.235 或更高版本。

* **Scope**: [`User or managed`](#scopes)。设置它的最高层的块整体应用。
* **Type**: 对象，包含 `enabled`（Boolean）、`checker`（`"aspell"`、`"hunspell"`、`"ispell"` 或 `"auto"`）、`language`（字符串，传递给检查器作为其字典名称）和 `color`（字符串，终端颜色名称、`#rrggbb`、`rgb(r,g,b)`、`ansi256(n)` 或 `ansi:<name>`）
* **Default**: unset，所以拼写检查关闭；`checker` 默认为 `"auto"`，`PATH` 上找到的前三个之一；`language` 默认为检查器自己的字典；`color` 默认为主题的错误颜色

```json settings.json theme={null}
{
  "spellcheck": { "enabled": true, "language": "en_GB" }
}
```

<h3 id="spinnertipsenabled">
  `spinnerTipsEnabled`
</h3>

当 Claude 工作时，加载动画行轮换显示关于 Claude Code 功能的短提示，如"使用计划模式为复杂请求做准备，然后再进行更改。按 Shift+Tab 两次以启用。"将此键设置为 `false` 以隐藏它们。在 `/config` 中显示为**显示提示**。

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`：当 Claude 工作时，您在加载动画中看到提示
  * `false`：Claude Code 隐藏加载动画提示
* **Default**: `true`

```json settings.json theme={null}
{
  "spinnerTipsEnabled": false
}
```

<h3 id="spinnertipsoverride">
  `spinnerTipsOverride`
</h3>

将您自己的提示添加到 Claude Code 在 Claude 工作时显示的[加载动画提示](#spinnertipsenabled)，或用您的提示替换内置提示。Claude Code 将您的提示放在与内置提示相同的轮换中。

如果您将 [`spinnerTipsEnabled`](#spinnertipsenabled) 设置为 `false`，Claude Code 会隐藏所有提示，包括您的。

* **Scope**: [`Any file`](#scopes)。Claude Code 从用户设置、`--settings` 标志和托管设置中尊重提示对象、`tipsFile`、`label` 和 `excludeDefault`；从项目和本地设置中，它仅读取纯字符串提示。
* **Type**: 对象，包含 `tips`、`tipsFile`、`label` 和 `excludeDefault` 字段，每个都是可选的
* **Default**: unset，所以 Claude Code 仅显示内置提示

提示对象、`tipsFile`、`label` 和 Scope 行的规则（项目和本地设置仅贡献纯字符串）需要 Claude Code v2.1.247 或更高版本。

每个 `tips` 条目是纯字符串或具有这些字段的对象：

| 字段 | 必需 | 描述 |
| :- | :- | :- |
| `id` | 是 | 最多 64 个字母、数字、`.`、`_` 或 `-`。Claude Code 在其上键入提示的显示历史，因此提示的冷却期在重新排序列表后仍然存在。在两个具有相同 id 的条目中，Claude Code 使用第一个 |
| `text` | 是 | 提示，最多 500 个字符的一行。Claude Code 剥离 ANSI 转义和控制字符，并折叠空格 |
| `cooldownSessions` | 否 | Claude Code 在再次显示提示之前等待的会话数，`0` 到 `1000`，默认 `0` |
| `priority` | 否 | 在未显示时间相同的提示中的顺序，较高的优先，`-10` 到 `10`，默认 `0` |

Claude Code 将纯字符串读取为具有这些默认值和基于位置的 id 的提示，因此当您重新排序列表时其显示历史重置。给提示一个 `id` 以在编辑中保持其历史。

Claude Code 在 `tips` 和 `tipsFile` 中最多读取 200 个提示，并用调试警告丢弃无效条目，而不是拒绝设置文件。

使用其余字段来命名提示文件、设置前缀和隐藏内置提示：

* `tipsFile`：指向本地 JSON 文件的绝对或 `~/` 路径，该文件包含相同条目的数组，或包含 `tips` 数组的对象，最多 256 KB。Claude Code 每个进程读取一次文件，因此在下次启动时加载您的编辑。您不能通过[服务器管理的设置](/docs/zh-CN/server-managed-settings)设置它；在那里部署内联 `tips`，或在磁盘上的 `managed-settings.json` 中部署路径。
* `label`：Claude Code 在来自用户、`--settings` 和托管设置的提示之前显示的前缀，最多 40 个字符。默认值是 `Tip`，与内置提示相同的前缀，来自项目和本地设置的提示始终使用它。
* `excludeDefault`：将其设置为 `true` 以隐藏内置提示并仅显示您的。当 Claude Code 无法加载您的任何提示时，例如因为 `tipsFile` 不存在或每个条目都无效，它保持内置轮换而不是空加载动画。

当多个设置文件设置此键时，Claude Code 显示来自所有这些文件的提示，并从托管设置、`--settings` 标志和用户设置中最高优先级的设置每个的 `tipsFile`、`label` 和 `excludeDefault`。

此示例在您的用户设置中添加纯字符串提示和对象提示到 `Acme tip` 前缀下的轮换：

```json settings.json theme={null}
{
  "spinnerTipsOverride": {
    "label": "Acme tip",
    "tips": [
      "在打开 PR 之前运行 /review",
      {
        "id": "gateway-errors",
        "text": "看到 5xx 错误？首先检查网关状态页面",
        "cooldownSessions": 5,
        "priority": 2
      }
    ]
  }
}
```

示例中的每个字段改变 Claude Code 显示提示的一个方面：

* `label`：Claude Code 将两个提示显示为 `Acme tip: ...` 而不是 `Tip: ...`。
* 纯字符串：Claude Code 给它默认值，所以它可以在下一个会话中再次出现。
* `id`：Claude Code 在 `gateway-errors` 上键入第二个提示的显示历史，因此其冷却期在添加或重新排序提示后仍然适用。
* `cooldownSessions`：在 Claude Code 显示 `gateway-errors` 提示后，它在五个会话后才再次显示该提示。
* `priority`：当 `gateway-errors` 提示和另一个提示未显示相同数量的会话时，例如当两者都尚未显示时，Claude Code 首先显示 `gateway-errors`。纯字符串具有默认优先级 `0`。

当 Claude 工作时，Claude Code 在加载动画中显示您的提示，带有您的前缀，如 `Acme tip: 在打开 PR 之前运行 /review`。

<h3 id="spinnerverbs">
  `spinnerVerbs`
</h3>

当转向进行中时，加载动画显示轮换的动词，如"Accomplishing"、"Architecting"或"Baking"。使用此键将您自己的动词添加到该轮换或用您的替换内置列表。

* **Scope**: [`Any file`](#scopes)
* **Type**: 对象，包含 `verbs` 字符串数组和 `mode`，值为以下之一：
  * `"append"`：Claude Code 将您的动词添加到内置集合
  * `"replace"`：Claude Code 仅显示您的动词
* **Default**: unset，所以 Claude Code 使用内置动词

此示例将两个动词添加到内置集合：

```json settings.json theme={null}
{
  "spinnerVerbs": {
    "mode": "append",
    "verbs": ["Pondering", "Crafting"]
  }
}
```

在 `"replace"` 模式下使用空 `verbs` 数组，Claude Code 保持内置动词。

<h3 id="statusline">
  `statusLine`
</h3>

运行您自己的命令来渲染提示下方的[状态行](/docs/zh-CN/statusline)，包含模型、成本或 git 分支等上下文。可选字段调整间距、添加定期重新运行，并在您的脚本自己渲染 `vim.mode` 时隐藏内置 vim 模式指示器。

* **Scope**: [`Any file`](#scopes)。当 [`allowManagedHooksOnly`](#allowmanagedhooksonly) 打开时，或 [`disableAllHooks`](#disableallhooks) 在托管设置外设置时，仅托管设置值运行。
* **Type**: 对象，`type` 设置为 `"command"` 和 `command` 字符串，加上可选的 `padding` 作为字符数、`refreshInterval` 作为秒数（最少 `1`）和 `hideVimModeIndicator` 作为 Boolean
* **Default**: unset，所以没有状态行

此示例打印模型名称和上下文使用情况，并添加两个字符的水平间距：

```json settings.json theme={null}
{
  "statusLine": {
    "type": "command",
    "command": "jq -r '\"[\\(.model.display_name)] \\(.context_window.used_percentage // 0)% context\"'",
    "padding": 2
  }
}
```

示例需要安装 [`jq`](https://jqlang.org/) 并在 shell 中运行。对于 PowerShell 和 Git Bash 等效项，请参阅[Windows 配置](/docs/zh-CN/statusline#windows-configuration)；对于完整设置，请参阅[手动配置状态行](/docs/zh-CN/statusline#manually-configure-a-status-line)。

<h3 id="subagentstatusline">
  `subagentStatusLine`
</h3>

当 Claude 运行[子代理](/docs/zh-CN/sub-agents)时，Claude Code 在提示下方的任务显示中列出它们，每个子代理一行显示 `name · description · token count`。此键让您运行自己的命令来重写这些行，例如显示每个子代理的上下文使用情况百分比。在每次刷新时，Claude Code 将可见行作为一个 JSON 对象发送到 stdin，其中 `tasks` 数组包含每个子代理的 `id`、`name`、`status`、`model`、`tokenCount` 等，并将您写回的每个 `id` 的行替换为 `{"id", "content"}` 行。您不写回的行保持默认渲染。

* **Scope**: [`Any file`](#scopes)。当 [`allowManagedHooksOnly`](#allowmanagedhooksonly) 打开时，或 [`disableAllHooks`](#disableallhooks) 在托管设置外设置时，仅托管设置值运行。
* **Type**: 对象，`type` 设置为 `"command"` 和 `command` 字符串
* **Default**: unset，所以 Claude Code 渲染默认行

```json settings.json theme={null}
{
  "subagentStatusLine": {
    "type": "command",
    "command": "jq -c '.tasks[] | {id, content: \"\\(.name): \\(.tokenCount) tokens\"}'"
  }
}
```

请参阅[子代理状态行](/docs/zh-CN/statusline#subagent-status-lines)。

<h3 id="syntaxhighlightingdisabled">
  `syntaxHighlightingDisabled`
</h3>

Claude Code 使用其内置高亮器按语言为它在终端中显示的差异、代码块和文件预览着色；不涉及插件或语言服务器。将此键设置为 `true` 以改为将它们显示为纯文本，例如如果颜色与您的终端主题冲突或减慢屏幕阅读器。

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`：Claude Code 在差异、代码块和文件预览中关闭语法高亮
  * `false`：Claude Code 高亮语法
* **Default**: `false`

```json settings.json theme={null}
{
  "syntaxHighlightingDisabled": true
}
```

<h3 id="terminalprogressbarenabled">
  `terminalProgressBarEnabled`
</h3>

某些终端可以在选项卡或任务栏中为在其中运行的程序显示进度指示器。当 Claude 工作时，Claude Code 向终端报告进行中状态，因此您可以从另一个选项卡或窗口看到会话是否仍然繁忙。指示器在转向结束后保持可见，同时[后台子代理](/docs/zh-CN/sub-agents#run-subagents-in-foreground-or-background)或[动态工作流](/docs/zh-CN/workflows)仍在运行，并在会话空闲后清除。

Claude Code 仅在支持指示器的终端中报告它：ConEmu、Ghostty 1.2.0 或更高版本以及 iTerm2 3.6.6 或更高版本。将此键设置为 `false` 以停止 Claude Code 报告它。在 `/config` 中显示为**终端进度条**。

* **Scope**: [`Any file`](#scopes)。当没有设置文件设置它时，来自较旧版本的 `~/.claude.json` 中的值适用。
* **Type**: Boolean
  * `true`：您在支持它的终端中看到终端进度条
  * `false`：Claude Code 隐藏终端进度条
* **Default**: `true`

```json settings.json theme={null}
{
  "terminalProgressBarEnabled": false
}
```

<h3 id="terminaltitlefromrename">
  `terminalTitleFromRename`
</h3>

Claude Code 设置您的终端选项卡的标题。默认情况下，它使用从对话生成的标题，一旦您使用 `/rename` 或 `--name` 给会话[命名](/docs/zh-CN/sessions#name-your-sessions)，选项卡会改为显示该名称。将此键设置为 `false` 以在您命名会话后保持生成的标题在选项卡上。名称本身仍然适用，因此 `/resume <name>` 和会话选择器找到它。

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`：终端选项卡标题显示您设置的会话名称
  * `false`：选项卡保持 Claude Code 从您的对话生成的标题
* **Default**: `true`

```json settings.json theme={null}
{
  "terminalTitleFromRename": false
}
```

要停止 Claude Code 完全更新终端标题，请改为将 [`CLAUDE_CODE_DISABLE_TERMINAL_TITLE`](/docs/zh-CN/env-vars) 设置为 `1`。

<h3 id="theme">
  `theme`
</h3>

为界面选择颜色主题。在 `/config` 中显示为**主题**。

* **Scope**: [`Any file`](#scopes)。当没有设置文件设置它时，来自较旧版本的 `~/.claude.json` 中的值适用。
* **Type**: string，值为以下之一：
  * `"auto"`：匹配您的终端的浅色或深色背景
  * `"dark"`：深色主题
  * `"light"`：浅色主题
  * `"dark-daltonized"`：具有色盲友好颜色的深色主题
  * `"light-daltonized"`：具有色盲友好颜色的浅色主题
  * `"dark-ansi"`：仅使用您的终端 ANSI 调色板的深色主题
  * `"light-ansi"`：仅使用您的终端 ANSI 调色板的浅色主题
  * `"custom:<slug>"` 或 `"custom:<plugin-name>:<slug>"`：来自 `~/.claude/themes/` 或插件的自定义主题
* **Default**: `"dark"`

```json settings.json theme={null}
{
  "theme": "light-daltonized"
}
```

请参阅[创建自定义主题](/docs/zh-CN/terminal-config#create-a-custom-theme)。

<h3 id="timeformat">
  `timeFormat`
</h3>

选择 Claude Code 如何写入它在界面中显示的时间，如每个转向持续时间消息末尾的 `done 6:05 PM` 和[记录查看器](/docs/zh-CN/interactive-mode#transcript-viewer)中的时间戳。要选择预设，运行 `/config` 并设置**时间格式**。需要 Claude Code v2.1.257 或更高版本。

* **Scope**: [`Any file`](#scopes)
* **Type**: string，值为以下之一：
  * `"auto"`：与 unset 相同；每个时间保持其内置格式，在转向持续时间消息上遵循您的区域设置
  * `"12-hour"`：12 小时制
  * `"24-hour"`：24 小时制
  * `"24-hour-utc"`：UTC 中的 24 小时制，分钟后带 `Z`，如 `18:05Z`；Claude Code 对此预设忽略 [`timeZone`](#timezone)
  * strftime 模式，如 `"%H:%M"`：Claude Code 使用模式写入每个时间。任何包含 `%` 的值都是模式，任何在预设外的其他值计为 `"auto"`
* **Default**: `"auto"`

```json settings.json theme={null}
{
  "timeFormat": "24-hour"
}
```

`/config` 仅提供预设，因此要使用 strftime 模式，请将键添加到设置文件。此示例将每个时间显示为两位数 24 小时制：

```json settings.json theme={null}
{
  "timeFormat": "%H:%M"
}
```

转向持续时间消息和记录查看器然后显示时间，如 `18:05`。在记录查看器中，模式是整个时间戳，因此在需要日期时添加日期指令。此示例将日期放在时钟前面：

```json settings.json theme={null}
{
  "timeFormat": "%Y-%m-%d %H:%M"
}
```

相同的表面然后显示时间，如 `2026-09-01 18:05`。

<h3 id="timezone">
  `timeZone`
</h3>

在不同于您系统的时区中显示界面中的时间。将其设置为 [IANA 时区名称](https://www.iana.org/time-zones)，如 `"UTC"` 或 `"Europe/Dublin"`。[`timeFormat`](#timeformat) 控制的时间然后在此区域中显示。如果 `timeFormat` 是 `"24-hour-utc"`，时间保持在 UTC 中，Claude Code 忽略此键。`/config` 对此键没有行，因此在设置文件中设置它。需要 Claude Code v2.1.257 或更高版本。

* **Scope**: [`Any file`](#scopes)
* **Type**: string，IANA 时区名称。当 Claude Code 不识别名称时，它使用您的系统时区
* **Default**: unset，所以时间显示在您的系统时区

```json settings.json theme={null}
{
  "timeZone": "Europe/Dublin"
}
```

<h3 id="tui">
  `tui`
</h3>

选择终端 UI 渲染器。使用 `"fullscreen"` 获得无闪烁的[替代屏幕渲染器](/docs/zh-CN/fullscreen)，具有虚拟化滚动条，或使用 `"default"` 获得经典主屏幕渲染器。运行 `/tui fullscreen` 或 `/tui default` 为您写入此键。

* **Scope**: [`Any file`](#scopes)
* **Type**: string，值为以下之一：
  * `"default"`：经典主屏幕渲染器
  * `"fullscreen"`：无闪烁的替代屏幕渲染器，具有虚拟化滚动条
* **Default**: unset，所以 Claude Code [为您选择渲染器](/docs/zh-CN/fullscreen#fullscreen-by-default)
* **Per-session overrides**: [`CLAUDE_CODE_NO_FLICKER`](/docs/zh-CN/env-vars) 和 [`CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN`](/docs/zh-CN/env-vars) 在单个会话中优先于此键：`CLAUDE_CODE_NO_FLICKER=1` 打开全屏，`CLAUDE_CODE_NO_FLICKER=0` 或 `CLAUDE_CODE_DISABLE_ALTERNATE_SCREEN=1` 关闭它；当两者都设置时，Claude Code 关闭它

```json settings.json theme={null}
{
  "tui": "fullscreen"
}
```

在 tmux `-CC` 下或通过 SSH 到 Windows，Claude Code 保持经典渲染器，除非您设置 `CLAUDE_CODE_NO_FLICKER=1`。从[代理视图](/docs/zh-CN/agent-view)打开的后台会话始终使用全屏渲染器，无论此设置如何。

<h3 id="verbose">
  `verbose`
</h3>

默认情况下，记录将每个工具调用折叠为简短摘要，如 Claude 运行的命令和其输出的行数，您按 `Ctrl+O` 在需要详细信息时将整个记录切换到展开视图。将此键设置为 `true` 以在发生时内联显示每个工具调用的完整输入和输出，这在您调试 hook、MCP 服务器或长 shell 命令时很有用。在 `/config` 中显示为**详细输出**。

* **Scope**: [`Any file`](#scopes)。当没有设置文件设置它时，来自较旧版本的 `~/.claude.json` 中的值适用。
* **Type**: Boolean
  * `true`：您看到完整工具输出
  * `false`：您看到工具输出的截断摘要
* **Default**: `false`
* **Per-session overrides**: [`--verbose`](/docs/zh-CN/cli-reference#cli-flags) 在单个会话中优先于此键

```json settings.json theme={null}
{
  "verbose": true
}
```

[`viewMode`](#viewmode) 值或粘性 `/focus` 选择在每个会话中覆盖此键。

<h3 id="viewmode">
  `viewMode`
</h3>

设置 Claude Code 启动的记录视图：`"default"`、`"verbose"` 或 `"focus"`。设置时，它覆盖粘性 `/focus` 选择和 [`verbose`](#verbose) 设置。

* **Scope**: [`Any file`](#scopes)
* **Type**: string，值为以下之一：
  * `"default"`：具有截断工具输出的正常记录
  * `"verbose"`：具有完整工具输出的记录
  * `"focus"`：仅您的最后提示、工具调用的单行摘要，带编辑差异统计，和最终响应。焦点视图需要[全屏渲染器](#tui)
* **Default**: unset，所以 `verbose` 设置和您最后的 `/focus` 选择适用
* **Per-session overrides**: [`--verbose`](/docs/zh-CN/cli-reference#cli-flags) 在单个会话中优先于此键

```json settings.json theme={null}
{
  "viewMode": "focus"
}
```

<h3 id="viminsertmoderemaps">
  `vimInsertModeRemaps`
</h3>

在 [vim 编辑器模式](/docs/zh-CN/interactive-mode#vim-editor-mode)中将两键 INSERT 模式序列映射到 Escape。每个键恰好是按顺序键入的两个可打印字符，`"<Esc>"` 是唯一支持的目标；Claude Code 忽略其他条目。需要 Claude Code v2.1.208 或更高版本。

* **Scope**: [`User or managed`](#scopes)。存储库不能重新映射您的按键。
* **Type**: 对象，将两字符序列映射到 `"<Esc>"`
* **Default**: unset

```json settings.json theme={null}
{
  "vimInsertModeRemaps": {
    "jj": "<Esc>"
  }
}
```

除非 `editorMode` 是 `"vim"`，否则无效。请参阅[重新映射 INSERT 模式快捷键序列](/docs/zh-CN/interactive-mode#remap-insert-mode-key-sequences)。需要 Claude Code v2.1.208 或更高版本。

<h3 id="voice">
  `voice`
</h3>

打开[语音听写](/docs/zh-CN/voice-dictation)并选择听写键的行为方式。当您运行 `/voice` 时，Claude Code 为您写入此对象。

* **Scope**: [`Any file`](#scopes)
* **Type**: 对象，`enabled` 作为 Boolean，`autoSubmit` 作为仅在保持模式中适用的 Boolean，和 `mode`，值为以下之一：
  * `"hold"`：您在说话时按住听写键，释放它以停止
  * `"tap"`：您点击键一次以开始录制，再次以发送
* **Default**: unset，所以听写关闭；当 `enabled` 是 `true` 且 `mode` 未设置时，Claude Code 使用 `"hold"`

此示例打开听写并使键点击一次以开始录制，再次以发送：

```json settings.json theme={null}
{
  "voice": {
    "enabled": true,
    "mode": "tap"
  }
}
```

`autoSubmit` 在保持模式中释放键时发送提示。语音听写需要 claude.ai 账户。

<h3 id="voiceenabled">
  `voiceEnabled`
</h3>

<Warning>
  自 v2.1.92 起已弃用，当 [`voice`](#voice) 对象替换它时。Claude Code 仍然读取它，因此较旧的设置文件保持工作，但新配置应设置 `voice.enabled`。
</Warning>

使用在 `voice` 对象之前的单个 Boolean 形式打开语音听写。当两者都设置时，`voice.enabled` 适用。

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`：当您使用 claude.ai 账户登录且您的组织政策允许语音时，语音听写打开，除非 `voice.enabled` 设置
  * `false`：语音听写关闭，除非 `voice.enabled` 设置
* **Default**: unset

```json settings.json theme={null}
{
  "voiceEnabled": true
}
```

<h3 id="wheelscrollaccelerationenabled">
  `wheelScrollAccelerationEnabled`
</h3>

在[全屏渲染](/docs/zh-CN/fullscreen#mouse-wheel-scrolling)中快速滚动期间加速鼠标滚轮滚动速度。将其设置为 `false` 以获得每个滚轮凹口的恒定滚动速率。

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`：Claude Code 在快速滚动期间加速鼠标滚轮滚动速度
  * `false`：Claude Code 以每个滚轮凹口的恒定速率滚动
* **Default**: `true`

```json settings.json theme={null}
{
  "wheelScrollAccelerationEnabled": false
}
```

<h2 id="git-and-attribution">
  Git 和归属
</h2>

控制 Claude Code 添加到提交和拉取请求的归属，以及它如何与 git 配合使用。

<span id="attribution-settings" />

<h3 id="attribution">
  `attribution`
</h3>

自定义 Claude Code 添加到 git 提交和拉取请求的归属。提交默认获得 [git trailer](https://git-scm.com/docs/git-interpret-trailers)，例如 `Co-Authored-By`；拉取请求描述获得纯文本。使用下面的子键分别设置每个部分。

* **Scope**: [`Any file`](#scopes)
* **Type**: 包含 `commit` 和 `pr` 字符串以及 `sessionUrl` 布尔值的对象，或 `false` 以隐藏所有归属。`false` 值需要 Claude Code v2.1.281 或更高版本；更早的版本会拒绝它并[跳过整个用户、项目或本地设置文件](/docs/zh-CN/settings#fix-a-broken-settings-file)
* **Default**: 未设置，因此 Claude Code 使用每个子键下显示的标准归属

要隐藏所有归属，请将 `attribution` 设置为 `false`。在早期版本也读取的设置文件中，将 [`commit`](#attribution-commit) 和 [`pr`](#attribution-pr) 设置为空字符串，并将 [`sessionUrl`](#attribution-sessionurl) 设置为 `false`。

此示例替换提交归属，删除拉取请求归属，并删除会话链接：

```json settings.json theme={null}
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>",
    "pr": "",
    "sessionUrl": false
  }
}
```

一旦设置 `commit` 或 `pr`，Claude Code 将忽略已弃用的 `includeCoAuthoredBy` 设置，并对未设置的两个中的任何一个使用其默认文本。

Claude Code 告诉 Claude，您自己关于归属的说明（例如 CLAUDE.md 或 [memory](/docs/zh-CN/memory) 规则）优先于这些提交和 PR 行，除非该行在 [managed settings](/docs/zh-CN/managed-settings) 中设置。

<h3 id="includecoauthoredby">
  `includeCoAuthoredBy`
</h3>

<Warning>
  自 v2.0.62 起已弃用，当 [`attribution`](#attribution) 替换它时。Claude Code 仍然读取它，但新配置应设置 `attribution`。
</Warning>

改用 [`attribution`](#attribution)，它替换此键，让您可以分别更改或隐藏提交 trailer、拉取请求文本和会话链接。Claude Code 仍然遵守来自早于 `attribution` 的设置文件中的 `includeCoAuthoredBy: false`，但一旦设置 `attribution.commit` 或 `attribution.pr`，就会忽略它。

* **Scope**: [`Any file`](#scopes)
* **Type**: 布尔值
  * `true`: 与未设置相同；Claude Code 添加提交 trailer 和拉取请求归属文本
  * `false`: Claude Code 省略提交 trailer 和拉取请求归属文本，除非 `attribution` 设置 `commit` 或 `pr`，在这种情况下 [`attribution`](#attribution) 规则适用
* **Default**: `true`

```json settings.json theme={null}
{
  "includeCoAuthoredBy": false
}
```

要隐藏所有归属，请参阅 [`attribution`](#attribution)。

<h3 id="includegitinstructions">
  `includeGitInstructions`
</h3>

Claude Code 向 Claude 提供两个与 git 相关的上下文片段：其内置的关于如何编写提交和拉取请求的说明（在 Bash 工具的描述中），以及您的存储库的 git 状态快照。快照包含当前分支、主分支、`git status` 输出和最近的提交。Claude Code 在会话开始时读取它。

将此键设置为 `false` 以将两者都排除，例如当您使用自己的 git 工作流技能时。

* **Scope**: [`Any file`](#scopes)
* **Type**: 布尔值
  * `true`: Claude Code 包含其内置的提交和拉取请求工作流说明以及 git 状态快照。云会话永远不包括快照
  * `false`: Claude Code 将两者都排除
* **Default**: `true`
* **Per-session overrides**: [`CLAUDE_CODE_DISABLE_GIT_INSTRUCTIONS`](/docs/zh-CN/env-vars) 对此键优先一个会话

```json settings.json theme={null}
{
  "includeGitInstructions": false
}
```

<h3 id="prurltemplate">
  `prUrlTemplate`
</h3>

将 Claude Code 呈现的 PR 链接（在页脚徽章和工具结果摘要中）指向内部代码审查工具而不是 `github.com`。Claude Code 从 PR URL 替换 `{host}`、`{owner}`、`{repo}`、`{number}` 和 `{url}`。[GitLab 合并请求](/docs/zh-CN/interactive-mode#gitlab-merge-requests) 两个表面上的链接保持其 GitLab URL。

* **Scope**: [`Any file`](#scopes)
* **Type**: 字符串，使用五个占位符中任何一个的 URL 模板
* **Default**: 未设置

```json settings.json theme={null}
{
  "prUrlTemplate": "https://reviews.example.com/{owner}/{repo}/pull/{number}"
}
```

Claude Code 仅将模板应用于它自己呈现的链接；Claude 在消息中编写的 PR 号（例如 `#123`）保持 Claude 编写的样子。没有 `/pull/<number>` 形状的 URL 保持不变。

<h3 id="attribution-commit">
  `attribution.commit`
</h3>

设置 Claude Code 添加到 git 提交的归属文本，包括任何 trailer。将其设置为空字符串以隐藏提交归属。

* **Scope**: [`Any file`](#scopes)
* **Type**: 字符串
* **Default**: 未设置，因此 Claude Code 添加 `Co-Authored-By: <name> <noreply@anthropic.com>`。名称是进行提交时使用的模型，例如 `Claude Sonnet 5`。当 [subagent](/docs/zh-CN/sub-agents) 进行提交时，trailer 命名 subagent 的模型。
  * 当 Claude Code 识别模型为 Claude 模型但无法确认其确切版本时，它单独写入 `Claude`。
  * 当它无法将模型 ID 匹配到任何 Claude 模型（例如通过自定义 [`ANTHROPIC_BASE_URL`](/docs/zh-CN/env-vars) 提供的第三方模型）时，它写入 `Claude Code`。

此示例用自定义行和自定义 `Co-Authored-By` trailer 替换默认 trailer：

```json settings.json theme={null}
{
  "attribution": {
    "commit": "Generated with AI\n\nCo-Authored-By: AI <ai@example.com>"
  }
}
```

<h3 id="attribution-pr">
  `attribution.pr`
</h3>

设置 Claude Code 添加到拉取请求描述的归属文本。将其设置为空字符串以隐藏拉取请求归属。

* **Scope**: [`Any file`](#scopes)
* **Type**: 字符串
* **Default**: 未设置，因此 Claude Code 添加 `🤖 Generated with [Claude Code](https://claude.com/claude-code)`

```json settings.json theme={null}
{
  "attribution": {
    "pr": ""
  }
}
```

<h3 id="attribution-sessionurl">
  `attribution.sessionUrl`
</h3>

选择 Claude Code 在从 [cloud](/docs/zh-CN/claude-code-on-the-web) 或 [Remote Control](/docs/zh-CN/remote-control) 会话提交或打开拉取请求时是否附加 claude.ai 会话链接。Claude Code 在提交上添加链接作为 `Claude-Session` trailer，在拉取请求描述中添加链接。将其设置为 `false` 以省略链接。

* **Scope**: [`Any file`](#scopes)
* **Type**: 布尔值
  * `true`: Claude Code 在从云或 Remote Control 会话提交或打开拉取请求时附加 claude.ai 会话链接
  * `false`: Claude Code 省略链接
* **Default**: `true`

```json settings.json theme={null}
{
  "attribution": {
    "sessionUrl": false
  }
}
```

<span id="hook-configuration" />

<span id="hook-and-skill-settings" />

<h2 id="hooks-and-automation">
  Hooks 和自动化
</h2>

注册 hooks，限制哪些 hooks 运行，以及控制工作流。有关 hook 事件和有效负载，请参阅 [hooks 参考](/docs/zh-CN/hooks)。

<h3 id="allowedhttphookurls">
  `allowedHttpHookUrls`
</h3>

限制 [HTTP hooks](/docs/zh-CN/hooks#http-hook-fields) 可以针对的 URL。定义此键时，Claude Code 仅在 HTTP hook 的 URL 与某个模式匹配时才运行该 hook，并阻止其余的而不运行它们；空数组会阻止每个 HTTP hook。

* **作用域**: [`任何文件`](#scopes)。数组在设置文件中合并。
* **类型**: URL 模式数组，`*` 作为通配符
* **默认值**: 未设置，因此允许任何 URL

此示例允许 `https://hooks.example.com/` 下的任何 URL 和任何 `http://localhost` URL：

```json settings.json theme={null}
{
  "allowedHttpHookUrls": ["https://hooks.example.com/*", "http://localhost:*"]
}
```

主机名匹配不区分大小写，并将 `hooks.example.com.`（带有标记完全限定域名的尾部点）视为与 `hooks.example.com` 相同，这是 DNS 的处理方式。允许列表适用于来自每个源的 hooks，包括托管设置。

<h3 id="allowmanagedhooksonly">
  `allowManagedHooksOnly`
</h3>

限制 hook 执行仅限于您的组织部署的 hooks。

* **作用域**: [`托管`](#scopes)
* **类型**: 布尔值
  * `true`: 仅运行托管 hooks，加上 Agent SDK hooks 和您的托管设置强制启用的插件中的 hooks。请参阅 [在 `allowManagedHooksOnly` 下运行什么](#what-runs-under-allowmanagedhooksonly)
  * `false`: 来自每个设置作用域和插件的 hooks 都运行
* **默认值**: 未设置，因此来自每个设置作用域和插件的 hooks 都运行

```json managed-settings.json theme={null}
{
  "allowManagedHooksOnly": true
}
```

<h4 id="what-runs-under-allowmanagedhooksonly">
  在 `allowManagedHooksOnly` 下运行什么
</h4>

将其设置为 `true` 时，Claude Code 会更改加载的 hooks 和类似 hook 的命令：

* **托管和 SDK hooks 运行**: 来自托管设置的 hooks 和 [Agent SDK](/docs/zh-CN/agent-sdk/overview) 在进程中注册的 hooks
* **强制启用的插件 hooks 运行**: 来自您的托管设置通过 [`enabledPlugins`](#enabledplugins) 强制启用的插件的 hooks。Claude Code 与完整的 `plugin@marketplace` ID 匹配，因此来自不同市场的同名插件保持被阻止。这使您可以通过组织市场分发经过审查的 hooks，同时阻止其他所有内容。此类插件中的 [mod](/docs/zh-CN/plugins/mods/overview) 仅在[被视为您组织的 mod](/docs/zh-CN/plugins/mods/admin#install-your-organizations-mods) 时才会加载
* **其他所有内容都被阻止**: 用户、项目和本地 hooks，来自其他已安装插件的 hooks 和 mods，以及在 Agent frontmatter 中声明的 hooks。[Claude Code 内置的 mods](/docs/zh-CN/plugins/mods/overview#mods-built-into-claude-code) 会继续运行。若只想阻止用户的 mods，请改为设置 [`allowManagedModsOnly`](/docs/zh-CN/plugins/mods/admin#set-options-on-the-built-in-guard)。
* **禁用命令源插件**: Claude Code 还禁用具有 [`command` 源](/docs/zh-CN/plugins/marketplace-reference#command-plugin-source) 的插件，包括在托管 `enabledPlugins` 中强制启用的插件，除非您明确将 [`disableCommandPluginSources`](#disablecommandpluginsources) 设置为 `false`
* **市场 `headersHelper` 命令被阻止**: Claude Code 还会阻止市场 [`headersHelper` 命令](/docs/zh-CN/plugins/host-marketplace#authenticate-archive-downloads)，除非 [`disableCommandPluginSources`](#disablecommandpluginsources) 明确设置为 `false`，托管设置本身声明的市场除外。需要 Claude Code v2.1.238 或更高版本
* **状态行和文件建议缩小到托管设置**: Claude Code 仅从托管设置读取 [`statusLine`](/docs/zh-CN/statusline)、[`fileSuggestion`](#filesuggestion) 和 [`subagentStatusLine`](/docs/zh-CN/statusline#subagent-status-lines)，遵循 [状态行和文件建议门](#status-line-and-file-suggestion-gates)

设置此键时，[`/goal`](/docs/zh-CN/goal) 命令无法运行，因为它依赖于 hooks。

<h3 id="disableallhooks">
  `disableAllHooks`
</h3>

关闭 [hooks](/docs/zh-CN/hooks#disable-or-remove-hooks)、任何自定义 [状态行](/docs/zh-CN/statusline) 和任何自定义 [文件建议](#filesuggestion) 命令。使用它可以临时关闭所有这些，而无需从设置中删除它们。

* **作用域**: [`任何文件`](#scopes)。仅托管设置可以禁用托管 hooks。
* **类型**: 布尔值
  * `true`: Claude Code 关闭 hooks、任何自定义状态行和任何自定义文件建议命令
  * `false`: hooks、状态行和文件建议命令运行
* **默认值**: 未设置，因此 hooks 运行

```json settings.json theme={null}
{
  "disableAllHooks": true
}
```

范围取决于哪个文件包含该键：

* **在托管设置中**: Claude Code 禁用每个配置的 hook，包括托管的，并继续运行 [Agent SDK](/docs/zh-CN/agent-sdk/overview) 在进程中注册的 hooks
* **在任何其他设置文件中**: Claude Code 禁用用户、项目、本地和插件 hooks；托管 hooks、Agent SDK hooks 和来自在托管 [`enabledPlugins`](#enabledplugins) 中强制启用的插件的 hooks 继续运行

该键还会停止 [mods](/docs/zh-CN/plugins/mods/overview)，即其代码会注册 hook 的插件：

* **在托管设置中**: 每个已安装插件中的 mods 都会停止，包括您组织的 mods
* **在任何其他设置文件中**: 您安装的 mods 会停止，而[您组织的 mods](/docs/zh-CN/plugins/mods/admin#install-your-organizations-mods) 继续运行

Claude Code 内置的 mods 在这两种情况下都会继续运行。每个内置 mod 都有[各自的开关](/docs/zh-CN/plugins/mods/overview#mods-built-into-claude-code)。

当托管设置设置此键时保持 Agent SDK hooks 运行需要 Claude Code v2.1.242 或更高版本。

当 hooks 被禁用时，[`/goal`](/docs/zh-CN/goal) 命令无法运行，`/hooks` 菜单显示通知而不是您的 hooks。

<h4 id="status-line-and-file-suggestion-gates">
  状态行和文件建议门
</h4>

Claude Code 为 `statusLine`、`fileSuggestion` 和 `subagentStatusLine` 按此顺序做出两个决定：

* **完全关闭**: 当托管设置设置 `disableAllHooks` 时，或当文件夹在与 [设置文件中的 hooks 相同的工作区信任规则](/docs/zh-CN/permissions#what-runs-before-you-trust-a-folder) 下不受信任时
* **缩小到托管设置**: 当设置 [`allowManagedHooksOnly`](#allowmanagedhooksonly) 时，当在应用 [设置优先级](/docs/zh-CN/hooks#disable-or-remove-hooks) 后 `disableAllHooks` 在托管设置外为 `true` 时，或当您使用 `--safe-mode` 启动 Claude Code 时

在缩小范围下，如果部署了托管值，Claude Code 会运行它。否则它会跳过您的值而不发出警告：状态行被禁用，`@` 自动完成回退到内置文件建议。

<h3 id="disableworkflows">
  `disableWorkflows`
</h3>

关闭 [动态工作流](/docs/zh-CN/workflows#turn-workflows-off) 和您的设置所涉及的每个人的捆绑工作流命令，例如通过托管设置的组织。要仅为自己打开或关闭工作流，请改用 [`enableWorkflows`](#enableworkflows)，这是 `/config` 中的 **动态工作流** 切换写入您的用户设置的内容。

* **作用域**: [`任何文件`](#scopes)
* **类型**: 布尔值
  * `true`: Claude Code 关闭动态工作流和您的设置所涉及的每个人的捆绑工作流命令
  * `false`: 与未设置相同；工作流是否打开然后遵循 [`enableWorkflows`](#enableworkflows) 和您的计划默认值
* **默认值**: `false`
* **每会话覆盖**: [`CLAUDE_CODE_DISABLE_WORKFLOWS`](/docs/zh-CN/env-vars) 关闭一个会话的工作流；无论两者中哪一个关闭它们，另一个都无法将其打开

```json settings.json theme={null}
{
  "disableWorkflows": true
}
```

<h3 id="enableworkflows">
  `enableWorkflows`
</h3>

当您的计划默认值不是您想要的时，为自己打开或关闭 [动态工作流](/docs/zh-CN/workflows)。在 `/config` 中显示为 **动态工作流**，它将此键写入您的用户设置，并在您切换回计划默认值时再次删除它。要从托管设置为每个人关闭工作流，请改用 [`disableWorkflows`](#disableworkflows)。

* **作用域**: [`任何文件`](#scopes)
* **类型**: 布尔值
  * `true`: Claude Code 为您打开动态工作流
  * `false`: Claude Code 为您关闭动态工作流
* **默认值**: 未设置，因此工作流打开，除非您在 Pro 计划上，其中工作流关闭
* **每会话覆盖**: [`CLAUDE_CODE_DISABLE_WORKFLOWS`](/docs/zh-CN/env-vars) 关闭一个会话的工作流，而 `true` 在此处无法在设置时将其打开

```json settings.json theme={null}
{
  "enableWorkflows": true
}
```

[`disableWorkflows`](#disableworkflows) 和您的组织的工作流策略也优先：`enableWorkflows: true` 在任何源关闭工作流时无法将其打开。当除您的用户设置之外的源设置 `enableWorkflows` 或将 `disableWorkflows` 设置为 `true` 时，Claude Code 隐藏 `/config` 行。

<h3 id="hooks">
  `hooks`
</h3>

在 Claude Code 的生命周期中的某些点（例如在工具调用之前或会话启动时）运行您自己的命令、提示、代理、HTTP 请求或 MCP 工具作为 [hooks](/docs/zh-CN/hooks)；[hooks 参考](/docs/zh-CN/hooks#hook-events) 列出每个事件、其有效负载和其退出代码。每个事件映射到匹配器组列表，每个组列出在匹配器应用时运行的处理程序。

* **作用域**: [`任何文件`](#scopes)。Hooks 在文件中合并而不是相互替换，来自托管设置的 hooks 无法从其他文件中删除。
* **类型**: 以 [hook 事件](/docs/zh-CN/hooks#hook-events) 为键的对象；每个值是 `{ "matcher", "hooks" }` 组的数组，其 `hooks` 条目的 `type` 为 `"command"`、`"prompt"`、`"agent"`、`"http"` 或 `"mcp_tool"`
* **默认值**: 未设置，因此没有 hooks 运行

此示例在每个 Bash 工具调用之前运行脚本：

```json settings.json theme={null}
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          { "type": "command", "command": "~/.claude/hooks/check-bash.sh" }
        ]
      }
    ]
  }
}
```

对于每个事件、匹配器模式和处理程序字段，请参阅 [hooks 参考](/docs/zh-CN/hooks#configuration)。要关闭 hooks，请参阅 [`disableAllHooks`](#disableallhooks)；要将 hooks 限制为您的组织部署的 hooks，请参阅 [`allowManagedHooksOnly`](#allowmanagedhooksonly)。

<h3 id="httphookallowedenvvars">
  `httpHookAllowedEnvVars`
</h3>

[HTTP hook](/docs/zh-CN/hooks#http-hook-fields) 可以将环境变量的值放入请求标头中，例如 `Authorization: Bearer $HOOK_TOKEN` 标头，但仅限于 hook 在其自己的 `allowedEnvVars` 中列出的变量。此键为每个 HTTP hook 的该列表设置外部限制：hook 只能使用变量（如果其自己的 `allowedEnvVars` 和此键都命名它）。使用它可以防止 hook 读取它不应该读取的秘密，即使 hook 的定义要求它。

* **作用域**: [`任何文件`](#scopes)。数组在设置文件中合并。
* **类型**: 环境变量名称数组
* **默认值**: 未设置，因此应用每个 hook 自己的 `allowedEnvVars` 列表

此示例将标头插值限制为 `MY_TOKEN` 和 `HOOK_SECRET`：

```json settings.json theme={null}
{
  "httpHookAllowedEnvVars": ["MY_TOKEN", "HOOK_SECRET"]
}
```

允许列表适用于来自每个源的 hooks，包括托管设置。

<h3 id="workflowkeywordtriggerenabled">
  `workflowKeywordTriggerEnabled`
</h3>

选择在提示中键入关键字 `ultracode` 是否触发 [动态工作流](/docs/zh-CN/workflows#ask-for-a-workflow-in-your-prompt)。将其设置为 `false` 以在不触发工作流的情况下键入该词。

* **作用域**: [`任何文件`](#scopes)。在 `/config` 中显示为 **Ultracode 关键字触发**。
* **类型**: 布尔值
  * `true`: 在提示中键入 `ultracode` 触发动态工作流
  * `false`: 您可以在不触发工作流的情况下键入该词
* **默认值**: `true`

```json settings.json theme={null}
{
  "workflowKeywordTriggerEnabled": false
}
```

`ultracode` 工作量设置、`/workflows` 和保存的工作流命令不受影响。

<h3 id="workflowsizeguideline">
  `workflowSizeGuideline`
</h3>

设置 [Claude 在其编写的动态工作流中针对的代理计数](/docs/zh-CN/workflows#set-a-size-guideline)。Claude Code 将值作为建议而不是强制上限发送给 Claude：`"small"` 要求少于 5 个代理，`"medium"` 少于 10 个，`"large"` 少于 50 个。当您想限制工作流花费的内容时，选择 `"small"`。需要 Claude Code v2.1.219 或更高版本。

* **作用域**: [`任何文件`](#scopes)。那里的值优先于 `/config` 中的 **动态工作流大小** 选择，Claude Code 将其存储在 `~/.claude.json` 中，当设置文件设置键时，Claude Code 隐藏该行。
* **类型**: 字符串，以下之一：
  * `"unrestricted"`: 无指导，因此 Claude 根据任务调整工作流大小
  * `"small"`: Claude 针对少于 5 个代理
  * `"medium"`: Claude 针对少于 10 个代理
  * `"large"`: Claude 针对少于 50 个代理
* **默认值**: `"medium"`，或 当您在 Pro 计划上使用 Claude Code v2.1.271 或更高版本登录时为 `"small"`

```json settings.json theme={null}
{
  "workflowSizeGuideline": "small"
}
```

需要 Claude Code v2.1.219 或更高版本；在 v2.1.202 到 v2.1.218 上，改为在 `/config` 中设置指导。

<span id="plugin-configuration" />

<span id="manage-plugins" />

<span id="plugin-settings" />

<h2 id="plugins-and-skills">
  Plugins 和 skills
</h2>

启用 plugins，注册 marketplaces，限制组织允许的 plugin 源，并控制哪些 skills 加载。有关安装和构建 plugins，请参阅 [Plugins](/docs/zh-CN/plugins/overview)。

<h3 id="disablebundledskills">
  `disableBundledSkills`
</h3>

关闭 Claude Code 附带的 [skills](/docs/zh-CN/skills) 和工作流。Claude Code 完全删除捆绑的 skills 和工作流，而内置命令（如 `/init`）仍可输入但对模型隐藏。

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`: Claude Code 删除捆绑的 skills 和工作流，并对模型隐藏内置命令（如 `/init`）
  * `false`: 捆绑的 skills 加载
* **Default**: 未设置，因此捆绑的 skills 加载
* **Per-session overrides**: [`CLAUDE_CODE_DISABLE_BUNDLED_SKILLS`](/docs/zh-CN/env-vars) 设置为 `1` 会在一个会话中关闭捆绑的 skills；两者中任何一个关闭它们，另一个就无法将其打开

```json settings.json theme={null}
{
  "disableBundledSkills": true
}
```

来自 plugins、`.claude/skills/` 和 `.claude/commands/` 的 skills 不受影响。`/doctor` 与内置命令一样仍可输入；要隐藏它，请改为设置 [`DISABLE_DOCTOR_COMMAND`](/docs/zh-CN/env-vars)。

<h3 id="disableskillshellexecution">
  `disableSkillShellExecution`
</h3>

关闭 [skills](/docs/zh-CN/skills) 和来自用户、项目、plugin 或附加目录源的自定义命令中 `` !`...` `` 和 ` ```! ` 块的内联 shell 执行。Claude Code 用 `[shell command execution disabled by policy]` 替换每个命令，而不是运行它。

* **Scope**: [`Any file`](#scopes)。托管设置中的 `true` 无法被其他地方的 `false` 覆盖。
* **Type**: Boolean
  * `true`: Claude Code 用 `[shell command execution disabled by policy]` 替换每个内联 shell 命令，而不是运行它
  * `false`: 内联 shell 运行
* **Default**: 未设置，因此内联 shell 运行

```json settings.json theme={null}
{
  "disableSkillShellExecution": true
}
```

捆绑的 skills 和通过托管设置部署的 skills 不受影响。

<h3 id="skilloverrides">
  `skillOverrides`
</h3>

隐藏或折叠 [skill](/docs/zh-CN/skills#override-skill-visibility-from-settings)，无需编辑其 `SKILL.md`。Claude Code 将每个 skill 名称下的值应用于 Claude 看到的 skill 列表和您的 `/` 自动完成。

* **Scope**: [`Any file`](#scopes)。`/skills` 菜单写入 `.claude/settings.local.json`。
* **Type**: 对象，将 skill 名称映射到以下之一：
  * `"on"`: Claude 看到该 skill，您可以输入 `/name`
  * `"name-only"`: Claude 按名称看到该 skill，但不显示其描述
  * `"user-invocable-only"`: Claude 看不到该 skill，但您仍可输入 `/name`
  * `"off"`: Claude 看不到该 skill，`/name` 从自动完成中隐藏
* **Default**: 未设置，因此每个 skill 都是 `"on"`

此示例仅按名称向 Claude 列出 `legacy-context`，并从 Claude 和 `/` 自动完成中隐藏 `deploy`：

```json settings.json theme={null}
{
  "skillOverrides": {
    "legacy-context": "name-only",
    "deploy": "off"
  }
}
```

覆盖不适用于 plugin skills，您可以通过 `/plugin` 管理这些。

在托管设置和使用 `--settings` 传递的文件中，捆绑 skill 的别名上的键（如 `/doctor` 的 `checkup`）也适用于该 skill；请参阅 [别名键如何与 skill 自身名称上的键结合](/docs/zh-CN/skills#override-skill-visibility-from-settings)。

<h3 id="syncclaudeaiskills">
  `syncClaudeAiSkills`
</h3>

关闭 [为您的 claude.ai 账户启用的 skills](/docs/zh-CN/skills#how-synced-skills-behave) 的下载。Claude Code 在 [您使用 claude.ai 账户登录的终端会话](/docs/zh-CN/skills#where-synced-skills-load)（交互式或非交互式）以及 Cowork 和云会话中将它们下载到 `~/.claude/skills/synced/`。设置 `false` 以停止该下载并停止加载已同步的 skills。Claude Code 仅接受 `false`：`true` 与未设置相同，不会在其他情况下关闭的地方打开同步。

* **Scope**: [`User, local, or managed`](#scopes)，以及使用 `--settings` 传递的文件。存储库无法为您关闭它。
* **Type**: Boolean
  * `false`: Claude Code 停止下载同步的 skills，停止加载 `~/.claude/skills/synced/` 中已有的 skills。在用户或托管设置中，它还将它们移动到 `~/.claude/skills/.trash/`
  * `true`: 与未设置相同
* **Default**: 未设置，因此使用 claude.ai 账户登录的会话同步您的 skills

此示例防止机器在任何会话中下载账户的 skills：

```json settings.json theme={null}
{
  "syncClaudeAiSkills": false
}
```

<h3 id="syncclaudeaiplugins">
  `syncClaudeAiPlugins`
</h3>

关闭 [为您的 claude.ai 账户启用的 plugins](/docs/zh-CN/plugins/loading#synced-plugins) 的下载。Claude Code 在您使用 claude.ai 账户登录的终端会话开始时和 Cowork 会话中将它们下载到 `~/.claude/plugins/synced/`，并将每个加载为 `<name>@synced`。设置 `false` 以停止该下载并停止加载已同步的 plugins。Claude Code 仅接受 `false`：`true` 与未设置相同，不会在其他情况下关闭的地方打开同步。需要 Claude Code v2.1.273 或更高版本。

* **Scope**: [`User, local, or managed`](#scopes)，以及使用 `--settings` 传递的文件。存储库无法为您关闭它。
* **Type**: Boolean
  * `false`: Claude Code 停止下载同步的 plugins，停止加载 `~/.claude/plugins/synced/` 中已有的 plugins。在用户或托管设置中，它还将它们移动到 `~/.claude/plugins/.trash/`
  * `true`: 与未设置相同
* **Default**: 未设置，因此使用 claude.ai 账户登录的会话同步您的 plugins

要关闭一个同步的 plugin 而不是全部，请在 [`enabledPlugins`](#enabledplugins) 中设置 `"<name>@synced": false`。

此示例防止机器在任何会话中下载账户的 plugins：

```json settings.json theme={null}
{
  "syncClaudeAiPlugins": false
}
```

<h3 id="allowedchannelplugins">
  `allowedChannelPlugins`
</h3>

选择哪些 [channel](/docs/zh-CN/channels) plugins 可以将消息推送到您组织中的会话。设置后，Claude Code 使用您的列表代替默认的 Anthropic 允许列表；每个条目命名一个 plugin 和它来自的 marketplace。

* **Scope**: [`Managed`](#scopes)
* **Type**: 对象数组，每个都有 `marketplace` 和 `plugin` 字符串。条目也可以是 `"plugin@marketplace"` 字符串，如 `"telegram@claude-plugins-official"`，Claude Code 将其视为等效对象。字符串形式需要 Claude Code v2.1.267 或更高版本；更早的版本在 `allowedChannelPlugins` 包含一个时拒绝整个值
* **Default**: 未设置，因此 Claude Code 使用默认的 Anthropic 允许列表

此示例打开 channels 并仅允许来自官方 Anthropic marketplace 的 Telegram plugin：

```json managed-settings.json theme={null}
{
  "channelsEnabled": true,
  "allowedChannelPlugins": [
    { "marketplace": "claude-plugins-official", "plugin": "telegram" }
  ]
}
```

空数组阻止每个 channel plugin。

此键在 channels 通过账户的 [`channelsEnabled`](#channelsenabled) 门控后生效：在 Team 和 Enterprise 计划上，以及在具有托管设置的 Console 账户上，这意味着 `channelsEnabled: true`。请参阅 [限制哪些 channel plugins 可以运行](/docs/zh-CN/channels#restrict-which-channel-plugins-can-run)。

<h3 id="blockedmarketplaces">
  `blockedMarketplaces`
</h3>

阻止您组织的 plugin marketplace 源。Claude Code 在 marketplace 添加以及 plugin 安装、更新、刷新和自动更新时检查阻止列表，因此在您设置策略之前添加的 marketplace 也无法用于获取 plugins。阻止的源在下载前被检查，因此它们永远不会接触文件系统。

如果您在 [claude.ai 管理控制台](/docs/zh-CN/server-managed-settings) 中设置此键，claude.ai 也会在您组织中的任何人从 claude.ai 上的 git 存储库添加 marketplace 时应用它，如 [限制如何工作](/docs/zh-CN/plugins/org#restrict-what-users-can-install) 所述。

* **Scope**: [`Managed`](#scopes)
* **Type**: marketplace 源对象数组，形式与 [`strictKnownMarketplaces`](#allowed-source-types) 相同
* **Default**: 未设置，因此没有 marketplace 被阻止

此示例阻止一个 GitHub 存储库作为 marketplace 源：

```json managed-settings.json theme={null}
{
  "blockedMarketplaces": [
    { "source": "github", "repo": "untrusted/plugins" }
  ]
}
```

一个 `github` 条目可能使用 [owner-wildcard 形式](#owner-wildcards) `"owner/*"` 来阻止该 GitHub owner 下的每个存储库，这需要 Claude Code v2.1.223 或更高版本。添加 `{ "source": "skills-dir" }` 以停止 Claude Code 从 `~/.claude/skills/` 加载 [`@skills-dir` plugins](/docs/zh-CN/plugins/loading#plugins-shared-through-a-repository)，而不限制任何 marketplace。请参阅 [托管 marketplace 限制](/docs/zh-CN/plugins/org#restrict-what-users-can-install)。

<h3 id="channelsenabled">
  `channelsEnabled`
</h3>

为您的组织允许 [channels](/docs/zh-CN/channels)。在 claude.ai Team 和 Enterprise 计划上，Claude Code 阻止 channels 直到您将其设置为 `true`。对于使用 API 密钥进行身份验证的 [Anthropic Console](/docs/zh-CN/authentication#claude-console-authentication) 账户，channels 默认被允许。如果您的组织部署托管设置，Claude Code 也会在这些账户上阻止 channels，直到您将此键设置为 `true`。

* **Scope**: [`Managed`](#scopes)
* **Type**: Boolean
  * `true`: Claude Code 为您的组织允许 channels
  * `false`: 与未设置相同；channels 是否被阻止取决于您的计划，如默认值所述
* **Default**: 未设置；channels 在 Team 和 Enterprise 计划上以及在具有托管设置的 Console 账户上被阻止，在 Pro 和 Max 计划上以及在没有托管设置的 Console 账户上被允许

```json managed-settings.json theme={null}
{
  "channelsEnabled": true
}
```

要限制哪些 plugins 可以在启用后注册为 channels，请设置 [`allowedChannelPlugins`](#allowedchannelplugins)。请参阅 [企业控制](/docs/zh-CN/channels#enterprise-controls)。

<h3 id="disablecommandpluginsources">
  `disableCommandPluginSources`
</h3>

阻止 [`command` plugin 源](/docs/zh-CN/plugins/marketplace-reference#command-plugin-source)，它通过在用户的机器上运行 marketplace 声明的命令来安装 plugin。当您将其设置为 `true` 时，Claude Code 永远不会运行该命令，不会安装或更新命令源的 plugins，并停止加载已安装的 plugins。设置为 `false` 以明确允许它们。每当它阻止命令源时，无论您将其设置为 `true` 还是在 [`allowManagedHooksOnly`](#allowmanagedhooksonly) 下保持未设置，它也会阻止 marketplace [`headersHelper` 命令](/docs/zh-CN/plugins/host-marketplace#authenticate-archive-downloads)，除了托管设置本身声明的 marketplace。需要 Claude Code v2.1.229 或更高版本，`headersHelper` 阻止需要 v2.1.238 或更高版本。

* **Scope**: [`Managed`](#scopes)
* **Type**: Boolean
  * `true`: Claude Code 永远不会运行 marketplace 声明的命令，不会安装或更新命令源的 plugins，并停止加载已安装的 plugins
  * `false`: Claude Code 明确允许命令源的 plugins
* **Default**: 未设置，因此 Claude Code 遵循 [`allowManagedHooksOnly`](#allowmanagedhooksonly)：限制 hook 执行到托管设置的组织也会禁用命令源

```json managed-settings.json theme={null}
{
  "disableCommandPluginSources": true
}
```

需要 Claude Code v2.1.229 或更高版本。

<h3 id="pluginsuggestionmarketplaces">
  `pluginSuggestionMarketplaces`
</h3>

命名其 plugins 可以作为上下文安装建议出现的 marketplaces，在 spinner 提示和 `/plugin` **Discover** 标签顶部固定。内置的第一方前端设计提示不受影响。建议来自每个 plugin 在其 marketplace 条目中的 `relevance` 声明。

* **Scope**: [`Managed`](#scopes)
* **Type**: marketplace 名称数组
* **Default**: 未设置，因此没有 marketplace 声明的建议出现

```json managed-settings.json theme={null}
{
  "pluginSuggestionMarketplaces": ["acme-corp-plugins"]
}
```

一个名称仅在 marketplace 在机器上注册且其注册源也在同一托管设置中声明时生效，要么作为该名称的 [`extraKnownMarketplaces`](#extraknownmarketplaces) 条目，要么作为 [`strictKnownMarketplaces`](#strictknownmarketplaces) 的条目。Claude Code 忽略从不同源注册的 marketplace，即使在允许列表名称下。官方 marketplace 豁免源要求：仅允许列表其名称就足够了，因为该名称只能从官方 Anthropic 源注册。请参阅 [按上下文建议 plugins](/docs/zh-CN/plugins/relevance)。

<h3 id="plugintrustmessage">
  `pluginTrustMessage`
</h3>

在安装前向 Claude Code 显示的 plugin 信任警告中添加您组织自己的文本，例如确认来自您内部 marketplace 的 plugins 已被审查。

* **Scope**: [`Managed`](#scopes)
* **Type**: 字符串
* **Default**: 未设置，因此 Claude Code 仅显示标准警告

```json managed-settings.json theme={null}
{
  "pluginTrustMessage": "All plugins from our marketplace are approved by IT"
}
```

<h3 id="strictknownmarketplaces">
  `strictKnownMarketplaces`
</h3>

限制您组织中的人员可以添加和安装 plugins 的 plugin marketplace 源。Claude Code 在 marketplace 添加以及 plugin 安装、更新、刷新和自动更新时强制执行允许列表，在任何网络或文件系统操作之前，因此在您设置策略之前添加的 marketplace 一旦其源不再匹配就无法用于获取 plugins。被阻止的用户会看到一个错误，命名托管策略。

如果您在 [claude.ai 管理控制台](/docs/zh-CN/server-managed-settings) 中设置此键，claude.ai 也会在您组织中的任何人从 claude.ai 上的 git 存储库添加 marketplace 时应用它，如 [限制如何工作](/docs/zh-CN/plugins/org#restrict-what-users-can-install) 所述。

* **Scope**: [`Managed`](#scopes)
* **Type**: marketplace 源对象数组；请参阅 [允许的源类型](#allowed-source-types)
* **Default**: 未设置，因此用户可以添加任何 marketplace。空数组是完全锁定，阻止每个 marketplace 源，包括官方 Anthropic marketplace

此示例允许两个 GitHub 存储库，一个固定到 `v2.0` ref，一个托管的 `marketplace.json` URL：

```json managed-settings.json theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/approved-plugins" },
    { "source": "github", "repo": "acme-corp/security-tools", "ref": "v2.0" },
    { "source": "url", "url": "https://plugins.example.com/marketplace.json" }
  ]
}
```

您也可以将此键写为 `allowedMarketplaces`；[Marketplace 键别名](#marketplace-key-aliases) 描述 Claude Code 如何处理别名以及哪个版本接受它。此键是一个策略门控：它控制用户可能添加什么，但不注册任何内容。要在一个文件中限制和预注册，请参阅 [与 `extraKnownMarketplaces` 结合](#combine-with-extraknownmarketplaces)。对于用户面向的视图，请参阅 [托管 marketplace 限制](/docs/zh-CN/plugins/org#restrict-what-users-can-install)。

<h4 id="allowed-source-types">
  允许的源类型
</h4>

下面每个条目显示每个源类型的一个允许列表条目及其接受的字段。大多数类型精确匹配；`hostPattern` 和 `pathPattern` 按正则表达式匹配，`github` 条目可以使用 [owner 通配符](#owner-wildcards)。

| Source | Example entry | Fields |
| :- | :- | :- |
| `github` | `{ "source": "github", "repo": "acme-corp/plugins", "ref": "main", "path": "marketplace" }` | `repo` 必需；`ref` 是分支或标签；`path` 是子目录 |
| `git` | `{ "source": "git", "url": "https://gitlab.example.com/tools/plugins.git", "ref": "production" }` | `url` 必需；`ref` 和 `path` 与 `github` 相同 |
| `url` | `{ "source": "url", "url": "https://plugins.example.com/marketplace.json", "headers": { "Authorization": "Bearer ${TOKEN}" } }` | `url` 必需；`headers` 为经过身份验证的访问添加 HTTP 标头 |
| `file` | `{ "source": "file", "path": "/opt/acme-corp/plugins/marketplace.json" }` | `path` 必需，`marketplace.json` 文件的绝对路径 |
| `directory` | `{ "source": "directory", "path": "/opt/acme-corp/approved-marketplaces" }` | `path` 必需，包含 `.claude-plugin/marketplace.json` 的目录的绝对路径 |
| `hostPattern` | `{ "source": "hostPattern", "hostPattern": "^github\\.example\\.com$" }` | `hostPattern` 必需，在 marketplace 主机中任何地方匹配的正则表达式；用 `^` 和 `$` 锚定它以匹配整个主机 |
| `pathPattern` | `{ "source": "pathPattern", "pathPattern": "^/opt/approved/" }` | `pathPattern` 必需，在 `file` 和 `directory` 源的 `path` 中任何地方匹配的正则表达式；用 `^` 开始它以固定前缀 |
| `skills-dir` | `{ "source": "skills-dir" }` | 无字段。选择 `~/.claude/skills/` plugin 扫描回入 |

三个源类型有超出表格的规则：

* **`url`**: URL marketplace 仅下载 `marketplace.json` 文件，Claude Code 不从该服务器按相对路径获取 plugin 文件，因此其 plugins 必须使用 [plugin 源](/docs/zh-CN/plugins/marketplace-reference#plugin-sources)，而不是相对路径，如存档 URL，可以在同一主机上。对于具有相对路径的 plugins，请改用基于 Git 的 marketplace。请参阅 [URL 基础 marketplaces 中的相对路径 plugins 失败](/docs/zh-CN/plugins/troubleshooting#plugins-with-relative-paths-fail-in-url-based-marketplaces)。
* **`hostPattern`**: 使用它来允许内部 GitHub Enterprise 或 GitLab 服务器上的每个 marketplace，而无需列出每个存储库。Claude Code 针对 `github.com` 匹配 `github` 源，从 `url` 源获取主机名，从 `git` 源获取它，取决于 [git URL](https://git-scm.com/docs/git-clone#_git_urls) 的形式：

  * 具有方案的 URL，如 `https://` 或 `ssh://`：URL 中的主机名。
  * 没有方案的 SSH 地址，采用 git 的 `user@host:path` 形式，如 `git@git.example.com:tools/plugins.git`：`@` 和 `:` 之间的主机，这是 git 连接到的主机。
  * 任何其他没有方案的形式：没有主机，因此没有 `strictKnownMarketplaces` `hostPattern` 条目匹配它。对于 `blockedMarketplaces` `hostPattern`，Claude Code 从更广泛的形式集合中获取主机，因此阻止列表条目仍可以匹配这样的形式。在 v2.1.234 之前，`strictKnownMarketplaces` `hostPattern` 也匹配 git 不视为 SSH 地址的某些形式。

  `file` 和 `directory` 源没有主机，永远不会匹配 `hostPattern` 条目。
* **`pathPattern`**: 使用它来允许文件系统 marketplaces 与网络源的 `hostPattern` 条目一起。`".*"` 允许每个本地路径；更窄的模式如 `"^/opt/approved/"` 限制到一个目录。

任何允许列表，即使是空的，也会停止 Claude Code 从 `~/.claude/skills/` 加载 [`@skills-dir` plugins](/docs/zh-CN/plugins/loading#plugins-shared-through-a-repository)。添加 `{ "source": "skills-dir" }` 条目以继续加载它们；该条目在此键和 `blockedMarketplaces` 之外没有意义。

<h4 id="owner-wildcards">
  Owner 通配符
</h4>

一个 `github` 条目，其 `repo` 值为 `"<owner>/*"`，匹配该 GitHub owner 下的每个存储库。Owner 通配符需要 Claude Code v2.1.223 或更高版本，仅在 `strictKnownMarketplaces` 和 `blockedMarketplaces` 中工作。在 `github` 源出现的其他地方，如 `extraKnownMarketplaces` 或 `/plugin marketplace add`，`repo` 值必须命名单个存储库。在 v2.1.223 之前，Claude Code 按字面比较条目，因此允许列表条目不匹配任何存储库，阻止列表条目不阻止任何内容；单存储库条目在每个版本上强制执行。

此条目允许 `acme-corp` 组织下的任何 marketplace 存储库：

```json managed-settings.json theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/*" }
  ]
}
```

只有整个存储库名称位置可以是通配符。Claude Code 忽略条目如 `*`、`*/plugins` 或 `acme-corp/tools-*` 作为无效，因此它们不匹配任何存储库。

两个设置之间的匹配规则不同：

| Rule | `strictKnownMarketplaces` | `blockedMarketplaces` |
| - | - | - |
| 匹配源拼写 | 仅 `owner/repo` 形式。克隆同一存储库的 git URL 不匹配 | 任何拼写，包括解析为同一 github.com 存储库的 git URL |
| Owner 大小写 | 区分大小写 | 不区分大小写 |
| `ref` | 遵循精确条目规则：带 `ref` 的条目仅匹配具有该精确 ref 的源，没有的条目仅匹配不指定 ref 的源 | 没有 `ref` 的条目阻止它匹配的存储库的所有 refs |
| `path` | 比精确条目规则更宽松：带 `path` 的条目需要该精确值，而没有的条目匹配存储库内的任何路径 | 没有 `path` 的条目阻止它匹配的存储库的所有路径 |

<h4 id="exact-matching">
  精确匹配
</h4>

对于除 owner-wildcard `github` 条目和正则表达式匹配的 `hostPattern` 和 `pathPattern` 条目之外的每个源类型，Claude Code 仅在 marketplace 源与条目精确匹配时允许用户的添加。对于基于 git 的源 `github` 和 `git`，精确匹配包括可选字段：

* `repo` 或 `url` 必须精确匹配
* `ref` 字段必须精确匹配，或两者都未定义
* `path` 字段必须精确匹配，或两者都未定义

例如，Claude Code 将下面的每对视为两个不同的源：

* `{ "source": "github", "repo": "acme-corp/plugins" }` 和 `{ "source": "github", "repo": "acme-corp/plugins", "ref": "main" }`
* `{ "source": "github", "repo": "acme-corp/plugins", "path": "marketplace" }` 和 `{ "source": "github", "repo": "acme-corp/plugins" }`

<h4 id="allow-only-the-official-marketplace">
  仅允许官方 marketplace
</h4>

要仅允许官方 Anthropic marketplace，列出其存储库：

```json managed-settings.json theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "anthropics/claude-plugins-official" }
  ]
}
```

使用此条目，Claude Code 保持已注册的官方 marketplace 可用，在新机器上，在您第一次启动交互式终端会话时自动注册 marketplace。自动注册最常遗漏：

* 在机器的第一个交互式终端会话之前运行的非交互式环境。
* Claude Code 仅通过 VS Code 扩展运行过的机器。
* Claude Code 已在阻止 marketplace 的策略下运行过交互式终端会话的机器，如空数组锁定。Claude Code 记录被阻止的尝试，在策略更改后不重试。

在这些机器上，将 marketplace 添加到同一 `managed-settings.json` 中的 [`extraKnownMarketplaces`](#extraknownmarketplaces)，以便 Claude Code 自动注册它，或运行 `claude plugin marketplace add anthropics/claude-plugins-official`。

<h4 id="combine-with-extraknownmarketplaces">
  与 `extraKnownMarketplaces` 结合
</h4>

两个键做不同的工作。此表比较它们：

| Aspect | `strictKnownMarketplaces` | `extraKnownMarketplaces` |
| - | - | - |
| Purpose | 组织策略执行 | 团队便利 |
| Settings file | 仅托管设置 | 任何设置文件 |
| Behavior | 阻止非允许列表的添加 | 注册缺失的 marketplaces |
| When enforced | 在网络和文件系统操作之前 | 立即从用户或托管设置；在存储库文件的工作区信任对话框之后 |
| Can be overridden | 否，最高优先级 | 是，由更高优先级的设置 |
| Source format | 直接源对象 | 具有嵌套 `source` 对象的命名 marketplace |

要为所有用户限制和预注册 marketplace，请在 `managed-settings.json` 中同时设置两者：

```json managed-settings.json theme={null}
{
  "strictKnownMarketplaces": [
    { "source": "github", "repo": "acme-corp/plugins" }
  ],
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "github", "repo": "acme-corp/plugins" }
    }
  }
}
```

仅设置 `strictKnownMarketplaces` 时，用户仍可以使用 `/plugin marketplace add` 自己添加允许的 marketplace。官方 Anthropic marketplace 是唯一 Claude Code 自动注册的，仅当允许列表允许时。[仅允许官方 marketplace](#allow-only-the-official-marketplace) 列出它遗漏的机器。

<h3 id="strictpluginonlycustomization">
  `strictPluginOnlyCustomization`
</h3>

阻止 skills、agents、hooks 和 MCP 服务器来自用户和项目源，因此它们只能来自 plugins 或托管设置。将其与 [`strictKnownMarketplaces`](#strictknownmarketplaces) 结合以控制完整的自定义供应链：marketplace 允许列表控制用户可以安装哪些 plugins。

* **Scope**: [`Managed`](#scopes)
* **Type**: `true` 以锁定所有四种自定义，或一个数组命名要锁定的种类，来自 `"skills"`、`"agents"`、`"hooks"` 和 `"mcp"`
* **Default**: 未设置，因此没有被锁定

此示例锁定 skills 和 hooks，保留 agents 和 MCP 服务器解锁：

```json managed-settings.json theme={null}
{
  "strictPluginOnlyCustomization": ["skills", "hooks"]
}
```

下面的四个子键条目列出每个表面阻止什么以及什么仍然加载。Claude Code 忽略它不识别的表面名称，而不是使设置文件失败，因此您可以在每个客户端更新之前添加新的表面名称。

<h3 id="strictpluginonlycustomization-skills">
  `strictPluginOnlyCustomization.skills`
</h3>

锁定 `skills` 表面。Claude Code 停止从 `~/.claude/skills/` 和 `.claude/skills/` 加载 skills，从 `~/.claude/commands/` 和 `.claude/commands/` 加载自定义命令，从 `--add-dir` 目录加载 skills 和命令，从您的 claude.ai 账户同步的 skills。它继续加载 plugin skills、捆绑的 skills 和托管策略目录中的 skills。

* **Scope**: [`Managed`](#scopes)
* **Type**: [`strictPluginOnlyCustomization`](#strictpluginonlycustomization) 数组中的字符串 `"skills"`
* **Default**: 未锁定

```json managed-settings.json theme={null}
{
  "strictPluginOnlyCustomization": ["skills"]
}
```

<h3 id="strictpluginonlycustomization-agents">
  `strictPluginOnlyCustomization.agents`
</h3>

锁定 `agents` 表面。Claude Code 停止从 `~/.claude/agents/`、`.claude/agents/` 和 `--add-dir` 目录加载 agents。它继续加载 plugin agents、内置 agents 和托管策略目录中的 agents。

* **Scope**: [`Managed`](#scopes)
* **Type**: [`strictPluginOnlyCustomization`](#strictpluginonlycustomization) 数组中的字符串 `"agents"`
* **Default**: 未锁定

```json managed-settings.json theme={null}
{
  "strictPluginOnlyCustomization": ["agents"]
}
```

<h3 id="strictpluginonlycustomization-hooks">
  `strictPluginOnlyCustomization.hooks`
</h3>

锁定 `hooks` 表面。Claude Code 停止运行来自用户、项目和本地 `settings.json` 的 hooks，并继续运行 plugin hooks 和托管设置中的 hooks。

* **Scope**: [`Managed`](#scopes)
* **Type**: [`strictPluginOnlyCustomization`](#strictpluginonlycustomization) 数组中的字符串 `"hooks"`
* **Default**: 未锁定

```json managed-settings.json theme={null}
{
  "strictPluginOnlyCustomization": ["hooks"]
}
```

<h3 id="strictpluginonlycustomization-mcp">
  `strictPluginOnlyCustomization.mcp`
</h3>

锁定 `mcp` 表面。Claude Code 停止从 `~/.claude.json` 和 `.mcp.json` 加载 MCP 服务器，并继续加载 plugin MCP 服务器、[`managed-mcp.json`](/docs/zh-CN/managed-mcp) 服务器和来自 [`managedMcpServers`](#managedmcpservers) 的服务器。

* **Scope**: [`Managed`](#scopes)
* **Type**: [`strictPluginOnlyCustomization`](#strictpluginonlycustomization) 数组中的字符串 `"mcp"`
* **Default**: 未锁定

```json managed-settings.json theme={null}
{
  "strictPluginOnlyCustomization": ["mcp"]
}
```

<h3 id="enabledplugins">
  `enabledPlugins`
</h3>

打开或关闭单个 [plugins](/docs/zh-CN/plugins/overview)，由 `plugin-name@marketplace-name` 键控。在任何范围内没有条目的 plugin 回退到其 [`defaultEnabled`](/docs/zh-CN/plugins/manifest-reference#fields) 值。当您使用 `/plugin` 或 `claude plugin enable` 启用或禁用 plugin 时，Claude Code 为您写入此键。

* **Scope**: [`Any file`](#scopes)
* **Type**: 对象，将 `plugin-name@marketplace-name` 映射到 Boolean
* **Default**: 未设置，因此每个 plugin 遵循其 `defaultEnabled` 值

此示例启用来自 `team-tools` marketplace 的两个 plugins，禁用来自 `personal` 的一个：

```json settings.json theme={null}
{
  "enabledPlugins": {
    "code-formatter@team-tools": true,
    "deployment-tools@team-tools": true,
    "experimental-features@personal": false
  }
}
```

每个范围服务不同的目的：

* **User settings**: 您的个人 plugin 偏好
* **Project settings**: 与存储库中的每个人共享的 plugins
* **Local settings**: 每台机器的覆盖，当 Claude Code 在那里保存设置时被 gitignored
* **Managed settings**: 组织范围的策略。设置为 `false` 的 plugin 在每个范围都被阻止安装，并从 marketplace 隐藏

项目设置优先于用户设置，因此在 `~/.claude/settings.json` 中将 plugin 设置为 `false` 不会禁用项目的 `.claude/settings.json` 启用的 plugin。要在您的机器上选择退出项目启用的 plugin，请改为在 `.claude/settings.local.json` 中将其设置为 `false`。由托管设置强制启用的 Plugins 无法以这种方式禁用，因为托管设置覆盖本地设置。

在项目的 `.claude/settings.json` 中启用来自外部源（如 GitHub 存储库或 npm 包）的 plugin 不会为其他人安装它。在加载 plugins 的每条路径上，Claude Code 报告 plugin 未安装，直到每个用户 [自己安装它](/docs/zh-CN/plugins/org#require-plugins-per-repository)。

<h3 id="extraknownmarketplaces">
  `extraKnownMarketplaces`
</h3>

按名称注册其他 plugin marketplaces，以便打开存储库的人或您的托管设置到达的每个人都获得 marketplace，而无需自己添加它。Claude Code 注册它还不知道的每个 marketplace。[`enabledPlugins`](#enabledplugins) 从它命名的 plugin 是否安装取决于 plugin 的源和哪个文件启用它；该条目有规则。

* **Scope**: [`Any file`](#scopes)。Claude Code 仅在您接受该文件夹的工作区信任对话框后才接受存储库的 `.claude/settings.json` 或 `.claude/settings.local.json` 中的条目；在您未信任的文件夹中，包括 `-p` 运行，它在没有消息的情况下忽略它们。
* **Type**: 对象，将 marketplace 名称映射到具有 `source` 对象和可选 `autoUpdate` Boolean 的对象
* **Default**: 未设置

此示例注册一个 GitHub marketplace 和来自自托管 git URL 的 marketplace：

```json settings.json theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": {
        "source": "github",
        "repo": "acme-corp/claude-plugins"
      }
    },
    "security-plugins": {
      "source": {
        "source": "git",
        "url": "https://git.example.com/security/plugins.git"
      }
    }
  }
}
```

[在您信任文件夹之前运行什么](/docs/zh-CN/permissions#what-runs-before-you-trust-a-folder) 将信任门与存储库可以提供的其他内容进行比较。您也可以将此键写为 `additionalMarketplaces`；请参阅 [Marketplace 键别名](#marketplace-key-aliases)。

设置 `"autoUpdate": true` 与 `source` 一起，使 Claude Code 在启动后在后台刷新该 marketplace 并更新其已安装的 plugins。省略时，`claude-plugins-official` 和大多数其他官方 Anthropic marketplaces 默认为 `true`，第三方 marketplaces 默认为 `false`。请参阅 [配置自动更新](/docs/zh-CN/plugins/install#keep-plugins-updated)。

当多个设置文件在同一名称下定义 marketplace 条目时，Claude Code 使用来自 [最高优先级文件](/docs/zh-CN/settings#settings-precedence) 的条目。该条目替换较低优先级的条目，不继承其任何字段，因此重新定义无法将一个文件的 `source.headers` 凭证与另一个文件控制的 URL 结合。在 v2.1.228 之前，Claude Code 逐字段合并同名条目，因此较高优先级文件中的条目可以继承它未设置的字段，包括另一个文件的 `headers`。

<h4 id="marketplace-source-types">
  Marketplace 源类型
</h4>

`source` 对象采用以下形式之一：

* **`github`**: GitHub 存储库，带 `repo`
* **`git`**: 任何 git URL，带 `url`
* **`url`**: 直接 URL 到 `marketplace.json` 文件，带 `url` 和可选 `headers` 和 `headersHelper` 用于经过身份验证的访问。`headersHelper` 命名一个打印标头的命令，其值太短暂而无法在 `headers` 中列出，需要 Claude Code v2.1.238 或更高版本
* **`file`**: 到 `marketplace.json` 文件的本地路径，带 `path`
* **`directory`**: 本地文件系统路径，使用 `path`。可用于开发，或用于您的组织[部署到每台机器](/docs/zh-CN/plugins/mods/admin#install-your-organizations-mods)的市场。
* **`settings`**: 直接在设置文件中声明的内联 marketplace，不带托管存储库，带 `name` 和 `plugins`

`git` 源类型适用于任何 git 托管服务，包括自托管 GitLab 和 Bitbucket。Claude Code 使用 `git clone` 在该机器上使用的相同身份验证克隆存储库：配置的凭证助手或 SSH 密钥。提供者令牌如 `GITHUB_TOKEN` 通过读取它的凭证助手生效。请参阅 [私有存储库](/docs/zh-CN/plugins/host-marketplace#grant-access-to-a-private-marketplace) 了解设置详情。

对于 `github` 和 `git` 源，Claude Code 在克隆 marketplace 存储库以添加或更新它时永远不会下载 [Git LFS](https://git-lfs.com) 内容。LFS 跟踪的文件被检出为指针文件，添加或更新输出报告有多少。

`source` 对象内的 `skipLfs` 字段被接受且没有效果。在 v2.1.274 之前，Claude Code 下载 LFS 内容，除非您设置 `"skipLfs": true`。

对于 `url` 源，当 `headers` 中的凭证过期且命令必须生成新凭证时，在 `source` 对象内设置 `headersHelper`。需要 Claude Code v2.1.238 或更高版本。对于命令必须打印的内容以及 Claude Code 运行它的位置，请参阅 [编写 headersHelper 命令](/docs/zh-CN/plugins/host-marketplace#write-the-headershelper-command)，对于 Claude Code 不运行它的情况，请参阅 [当 Claude Code 跳过 headersHelper 命令或丢弃其输出时](/docs/zh-CN/plugins/host-marketplace#when-claude-code-skips-a-headershelper-command-or-drops-its-output)。一旦您在 `https://` marketplace URL 上设置 `headersHelper`，Claude Code 在两个点运行命令，重用一次运行的输出长达 60 秒：

* 在该 marketplace 的 `marketplace.json` 的每次获取之前，包括稍后的刷新。Claude Code 使用该获取发送打印的标头。
* 在 marketplace URL 的源上的每个 plugin 存档下载之前，意味着相同的方案、主机和端口。Claude Code 使用该下载发送输出，没有其他下载获得标头。

Claude Code 忽略在您使用 [`--add-dir`](/docs/zh-CN/permissions#what-runs-before-you-trust-a-folder) 添加的目录的 `.claude/settings.json` 或 `.claude/settings.local.json` 中设置的任何 `headersHelper`，在 `url` 源和内联 plugin 条目上，仅发送在该文件中设置的固定 `headers`。[用户如何接受 headersHelper 命令](/docs/zh-CN/plugins/host-marketplace#how-users-accept-a-headershelper-command) 涵盖其他设置文件。

在 `settings` 源中列出的 Plugins 必须引用外部源如 GitHub 或 npm，`name` 必须与 marketplace 键匹配。您仍然在 `enabledPlugins` 中单独启用每个 plugin。此示例声明一个 plugin 内联：

```json settings.json theme={null}
{
  "extraKnownMarketplaces": {
    "team-tools": {
      "source": {
        "source": "settings",
        "name": "team-tools",
        "plugins": [
          {
            "name": "code-formatter",
            "source": {
              "source": "github",
              "repo": "acme-corp/code-formatter"
            }
          }
        ]
      }
    }
  }
}
```

在 `source: 'settings'` 下的 plugin 条目，其自身 `source` 是 [`archive`](/docs/zh-CN/plugins/marketplace-reference#archive-plugin-source) 的，可以为存档下载设置 `headers`。如果您想放在 `headers` 中的值是短暂的，如您的注册表按请求铸造的令牌，请改为设置 `headersHelper` 命令。条目可以同时设置两者。两个字段都需要 Claude Code v2.1.238 或更高版本。

Claude Code 发送条目的 `headers` 和命令打印的任何内容，与该 plugin 的存档下载一起，没有其他下载。Claude Code 仅在用户 [自己安装或更新该一个 plugin](/docs/zh-CN/plugins/host-marketplace#how-users-accept-a-headershelper-command) 时运行命令。三个进一步的规则取决于哪个文件持有条目：

* **`strict`**: 与 marketplace 的 `marketplace.json` 中的条目不同，设置文件中的条目不需要 `"strict": false`，因为设置文件不携带要内联的清单字段。请参阅 [严格模式](/docs/zh-CN/plugins/marketplace-reference#strict-mode)。
* **Folder trust**: 对于项目的 `.claude/settings.json` 或 `.claude/settings.local.json` 中的条目，Claude Code 仅在用户也 [信任该文件夹](/docs/zh-CN/permissions#what-runs-before-you-trust-a-folder) 后运行命令。
* **Header filter**: Claude Code 从项目的 `.claude/settings.json` 或 `.claude/settings.local.json` 中的条目删除 [请求路由和客户端身份标头名称](/docs/zh-CN/plugins/host-marketplace#when-claude-code-skips-a-headershelper-command-or-drops-its-output)，因为存储库可以提供这些文件。Claude Code 对目录条目和 `--add-dir` 目录的设置中的条目应用相同的过滤器，对您的用户设置、`--settings` 文件或托管设置中的条目不应用过滤器。

<h4 id="marketplace-key-aliases">
  Marketplace 键别名
</h4>

在 Claude Code v2.1.232 或更高版本上，您可以将 `extraKnownMarketplaces` 写为 `additionalMarketplaces`，将 `strictKnownMarketplaces` 写为 `allowedMarketplaces`。Claude Code 按如下方式处理每个别名：

* 更早的版本忽略别名，因此在较旧版本也读取的文件中保持规范拼写，如具有混合 Claude Code 版本的队伍的托管设置文件。
* 在接受规范键的任何设置文件中，Claude Code 完全按照读取规范键的方式读取别名。
* Claude Code 可能在更新文件时将 `additionalMarketplaces` 重写为 `extraKnownMarketplaces`。
* 如果您在一个文件中同时设置两个拼写，Claude Code 使用规范值并忽略别名。

<h3 id="pluginconfigs">
  `pluginConfigs`
</h3>

存储您给 plugin 的 [`userConfig`](/docs/zh-CN/plugins/manifest-reference#user-configuration) 配置对话框的非敏感答案，由 plugin ID 键控。当您填写对话框时，Claude Code 将此键写入您的用户设置，因此您无需手动编辑它。Claude Code 将敏感选项存储在 macOS Keychain 中，当 Keychain 拒绝写入时回退到 `~/.claude/.credentials.json`；在没有支持的 keychain 的平台上，它将它们存储在 `~/.claude/.credentials.json` 中。

* **Scope**: [`User or managed`](#scopes)
* **Type**: 对象，将 plugin ID 映射到具有 `options` 字段的对象，将每个选项名称映射到字符串、数字、Boolean 或字符串数组，以及可选的 `mcpServers` 字段，以相同形状保存每个服务器的用户配置值
* **Default**: 未设置

此示例为来自 `acme-tools` 的 `deployer` plugin 存储 `api_endpoint` 选项：

```json settings.json theme={null}
{
  "pluginConfigs": {
    "deployer@acme-tools": {
      "options": {
        "api_endpoint": "https://api.example.com"
      }
    }
  }
}
```

内置插件在同一键下存储其选项，带 `@builtin` 后缀。例如，控制 Claude Code 是否读取 `AGENTS.md` 文件的 [**Project instructions**](/docs/zh-CN/memory#choose-which-instruction-files-load) 设置是 `pluginConfigs["cc-plugin-agents-md@builtin"].options.instructionFiles`。在 v2.1.285 之前，该插件的 ID 为 `agents-md@builtin`。更高版本会读取任一 ID 下的条目。

Claude Code 忽略项目和本地条目，因为它将这些值替换到 plugin hook、MCP 和 LSP 配置中，克隆的存储库不得能够提供它们。在 v2.1.207 之前，项目和本地设置也被读取。

<h3 id="prependplugins">
  `prependPlugins`
</h3>

列出托管插件，其 [mod](/docs/zh-CN/plugins/mods/overview) 会按列出的顺序在用户安装的所有 mod 之前运行。当您在托管设置中设置此键时，请在列表中包含 `sec-default@builtin` 以保留内置防护。在托管设置中，如果某个 ID 对应的插件不被视为您组织的插件，Claude Code 会跳过它。有关这些条件以及两个排序键如何协同工作，请参阅[安装您组织的 mod 并设置顺序](/docs/zh-CN/plugins/mods/admin#install-your-organizations-mods)。

* **Scope**: [`User or managed`](#scopes)。Claude Code 从托管设置中读取此键。仅在没有托管设置的机器上，且用户未使用 Team 或 Enterprise 计划登录时，它才会从用户设置中读取此键。它会忽略项目设置、本地设置以及 `--settings` 文件中的此键。
* **Type**: `plugin-name@marketplace-name` 字符串数组
* **Default**: 未设置

```json managed-settings.json theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "directory", "path": "/opt/acme/claude-plugins" }
    }
  },
  "enabledPlugins": { "acme-guard@acme-tools": true },
  "prependPlugins": ["acme-guard@acme-tools", "sec-default@builtin"]
}
```

<h3 id="appendplugins">
  `appendPlugins`
</h3>

列出托管插件，其 [mod](/docs/zh-CN/plugins/mods/overview) 会按列出的顺序在用户安装的所有 mod 之后运行。同时列在 `prependPlugins` 和 `appendPlugins` 中的 ID 会被前置。在托管设置中，如果某个 ID 对应的插件不[被视为您组织的插件](/docs/zh-CN/plugins/mods/admin#install-your-organizations-mods)，Claude Code 会跳过它。

* **Scope**: [`User or managed`](#scopes)。Claude Code 从托管设置中读取此键。仅在没有托管设置的机器上，且用户未使用 Team 或 Enterprise 计划登录时，它才会从用户设置中读取此键。它会忽略项目设置、本地设置以及 `--settings` 文件中的此键。
* **Type**: `plugin-name@marketplace-name` 字符串数组
* **Default**: 未设置

```json managed-settings.json theme={null}
{
  "extraKnownMarketplaces": {
    "acme-tools": {
      "source": { "source": "directory", "path": "/opt/acme/claude-plugins" }
    }
  },
  "enabledPlugins": { "acme-audit@acme-tools": true },
  "appendPlugins": ["acme-audit@acme-tools"]
}
```

<h2 id="mcp">
  MCP
</h2>

控制 Claude Code 连接到哪些 MCP 服务器以及组织允许哪些服务器。请参阅[使用 MCP 连接到外部工具](/docs/zh-CN/mcp)和[托管 MCP 配置](/docs/zh-CN/managed-mcp)。

<h3 id="allowallclaudeaimcps">
  `allowAllClaudeAiMcps`
</h3>

加载 [claude.ai 连接器](/docs/zh-CN/mcp#use-mcp-servers-from-claude-ai)，Claude Code 会在部署的 `managed-mcp.json` 旁边自行获取这些连接器。如果没有此密钥，`managed-mcp.json` 将对 MCP 服务器拥有独占控制权并禁止这些连接器。

* **作用域**: [`Managed`](#scopes)。用户无法重新启用独占控制禁止的连接器。
* **类型**: 布尔值
  * `true`: Claude Code 在部署的 `managed-mcp.json` 旁边加载 claude.ai 连接器
  * `false`: 部署的 `managed-mcp.json` 对 MCP 服务器拥有独占控制权并禁止 claude.ai 连接器 [Claude Code 自行获取](/docs/zh-CN/mcp#how-connectors-reach-claude-code)
* **默认值**: `false`，因此部署的 `managed-mcp.json` 会禁止 Claude Code 自行获取的 claude.ai 连接器

```json managed-settings.json theme={null}
{
  "allowAllClaudeAiMcps": true
}
```

[`allowedMcpServers`](#allowedmcpservers) 和 [`deniedMcpServers`](#deniedmcpservers) 仍然适用于此密钥加载的连接器。传递到[云会话](/docs/zh-CN/claude-code-on-the-web)的连接器，其主机携带 `managed-mcp.json`（例如自托管运行器），仍然会被禁止。请参阅[在托管集合旁边允许 claude.ai 连接器](/docs/zh-CN/managed-mcp#allow-claude-ai-connectors-alongside-the-managed-set)。

<h3 id="allowclaudeinchromewithmanagedmcp">
  `allowClaudeInChromeWithManagedMcp`
</h3>

让内置的 [Chrome 中的 Claude](/docs/zh-CN/chrome) 服务器在部署的 `managed-mcp.json` 旁边运行。如果没有此密钥，部署的 `managed-mcp.json` 会在终端会话中阻止 Chrome 中的 Claude。需要 Claude Code v2.1.282 或更高版本。

* **作用域**: [`Managed`](#scopes)，仅来自设备自己的托管设置：MDM 部署的 plist 或 HKLM 注册表密钥，或系统 `managed-settings.json` 文件。Claude Code 在服务器托管的设置、用户可写的 HKCU 注册表以及用户或项目设置中忽略它。
* **类型**: 布尔值
  * `true`: 内置的 Chrome 中的 Claude 服务器可以在部署的 `managed-mcp.json` 旁边运行
  * `false`: 部署的 `managed-mcp.json` 会在终端会话中阻止 Chrome 中的 Claude
* **默认值**: `false`，因此部署的 `managed-mcp.json` 会在终端会话中阻止 Chrome 中的 Claude

```json managed-settings.json theme={null}
{
  "allowClaudeInChromeWithManagedMcp": true
}
```

[`deniedMcpServers`](#deniedmcpservers) 中的 `claude-in-chrome` 条目仍然会在此密钥打开时阻止服务器。请参阅[在托管集合旁边允许 Chrome 中的 Claude](/docs/zh-CN/managed-mcp#allow-claude-in-chrome-alongside-the-managed-set)。

<h3 id="allowedmcpservers">
  `allowedMcpServers`
</h3>

允许列表化人们可以添加的 MCP 服务器。Claude Code 会阻止任何不匹配条目的服务器，无论在何处定义，包括插件服务器、使用 `--mcp-config` 传递的服务器以及来自 claude.ai 的服务器。

内置服务器（例如 Chrome 中的 Claude、Claude Code 在运行的 [VS Code](/docs/zh-CN/vs-code#the-built-in-ide-mcp-server) 或 [JetBrains](/docs/zh-CN/jetbrains#the-built-in-ide-mcp-server) IDE 中连接的 `ide` 服务器，以及 CLI 本身配置的服务器）不受允许列表的限制，拒绝列表仍然适用于它们。在 Claude Code v2.1.268 或更高版本上，[Claude Tag](/docs/zh-CN/claude-tag) 会话的 Slack 工具也不受允许列表的限制，拒绝列表仍然适用于它们。进程内 `type: "sdk"` 服务器不受两个列表的限制；[启动会话的应用](/docs/zh-CN/mcp#how-connectors-reach-claude-code)会注册它们。

您的组织提供的服务器也不受允许列表的限制，拒绝列表仍然适用于它们。豁免涵盖每个 [`managedMcpServers`](#managedmcpservers) 条目，以及任何 [`managed-mcp.json`](/docs/zh-CN/managed-mcp#exclusive-control-with-managed-mcp-json) 条目，其值不使用 `${VAR}` 扩展。有关完整的检查顺序，请参阅[如何评估服务器](/docs/zh-CN/managed-mcp#how-a-server-is-evaluated)。在 v2.1.259 之前，来自 `managed-mcp.json` 的服务器也必须匹配。

* **作用域**: [`Any file`](#scopes)。来自每个文件的条目合并为一个允许列表，除非设置了 [`allowManagedMcpServersOnly`](#allowmanagedmcpserversonly)。在托管设置中部署它以强制执行。
* **类型**: 对象数组，每个对象恰好有一个密钥：`serverName`，一个限制为字母、数字、连字符和下划线的字符串；`serverCommand`，一个与命令及其参数完全匹配的数组；或 `serverUrl`，一个带有 `*` 通配符的 URL 模式
* **默认值**: 未设置，因此允许每个服务器；空数组会阻止用户添加的每个服务器

此示例仅允许列出的 `npx` 命令启动的 stdio 服务器：

```json settings.json theme={null}
{
  "allowedMcpServers": [
    { "serverCommand": ["npx", "-y", "@modelcontextprotocol/server-filesystem"] }
  ]
}
```

[`deniedMcpServers`](#deniedmcpservers) 条目优先，因此同时在两个列表中的服务器会被阻止。一旦列表包含任何 `serverCommand` 条目，stdio 服务器必须匹配 `serverCommand` 条目，一旦它包含任何 `serverUrl` 条目，远程服务器必须匹配 `serverUrl` 条目：`serverName` 匹配不再允许该类型的服务器。请参阅[使用允许列表和拒绝列表进行基于策略的控制](/docs/zh-CN/managed-mcp#policy-based-control-with-allowlists-and-denylists)。

<h3 id="allowmanagedmcpserversonly">
  `allowManagedMcpServersOnly`
</h3>

使托管允许列表成为唯一适用的列表。Claude Code 随后仅从托管设置中读取 [`allowedMcpServers`](#allowedmcpservers)，并忽略用户、项目和本地设置中的允许列表；[`deniedMcpServers`](#deniedmcpservers) 仍然从每个设置作用域合并，因此用户仍然可以为自己阻止服务器。管理员设置它，以便用户自己的设置无法扩展托管允许列表允许的内容。

* **作用域**: [`Managed`](#scopes)
* **类型**: 布尔值
  * `true`: Claude Code 仅从托管设置中读取 `allowedMcpServers`，并忽略用户、项目和本地设置中的允许列表
  * `false`: 来自每个设置作用域的允许列表合并
* **默认值**: `false`，因此来自每个设置作用域的允许列表合并

此示例将允许列表锁定到托管设置，并仅允许名为 `github` 的服务器：

```json managed-settings.json theme={null}
{
  "allowManagedMcpServersOnly": true,
  "allowedMcpServers": [
    { "serverName": "github" }
  ]
}
```

用户仍然可以添加自己的 MCP 服务器；只有与托管允许列表匹配的服务器才会加载。请参阅[将允许列表限制为仅托管设置](/docs/zh-CN/managed-mcp#restrict-the-allowlist-to-managed-settings-only)。

<h3 id="deniedmcpservers">
  `deniedMcpServers`
</h3>

阻止特定的 MCP 服务器。Claude Code 拒绝加载匹配的服务器，无论在何处定义，包括插件服务器、使用 `--mcp-config` 传递的服务器、来自 `managed-mcp.json` 的服务器、来自 [`managedMcpServers`](#managedmcpservers) 的服务器，以及 [它自行获取](/docs/zh-CN/mcp#how-connectors-reach-claude-code)的 claude.ai 连接器。进程内 `type: "sdk"` 服务器不受限制；启动会话的应用会注册它们。

* **作用域**: [`Any file`](#scopes)。来自每个文件的条目合并为一个拒绝列表，[`allowManagedMcpServersOnly`](#allowmanagedmcpserversonly) 不会改变这一点。在托管设置中部署它以强制执行。
* **类型**: 对象数组，每个对象恰好有一个密钥：`serverName`，一个字符串，因此 claude.ai 连接器的显示名称（例如 `"claude.ai Slack"`）有效；`serverCommand`，一个与命令及其参数完全匹配的数组；或 `serverUrl`，一个带有 `*` 通配符的 URL 模式
* **默认值**: 未设置，因此不阻止任何服务器；空数组也不阻止任何内容

```json settings.json theme={null}
{
  "deniedMcpServers": [
    { "serverName": "filesystem" }
  ]
}
```

拒绝列表优先于 [`allowedMcpServers`](#allowedmcpservers)，因此同时在两个列表中的服务器会被阻止。请参阅[使用允许列表和拒绝列表进行基于策略的控制](/docs/zh-CN/managed-mcp#policy-based-control-with-allowlists-and-denylists)。

<h3 id="disableclaudeaiconnectors">
  `disableClaudeAiConnectors`
</h3>

关闭 [claude.ai MCP 连接器](/docs/zh-CN/mcp#use-mcp-servers-from-claude-ai) [Claude Code 自行获取](/docs/zh-CN/mcp#how-connectors-reach-claude-code)，因此它既不获取也不连接它们。任何设置文件中的 `true` 都适用：签入的项目 `.claude/settings.json` 可以选择退出存储库中的这些连接器，但项目级别的 `false` 无法覆盖用户级别或托管级别的 `true`。

* **作用域**: [`Any file`](#scopes)
* **类型**: 布尔值
  * `true`: Claude Code 既不获取也不连接这些连接器
  * `false`: 与未设置相同；Claude Code 获取您的连接器，除非另一个设置文件或 `ENABLE_CLAUDEAI_MCP_SERVERS` 关闭它们
* **默认值**: `false`，因此 Claude Code 获取您的连接器
* **每会话覆盖**: [`ENABLE_CLAUDEAI_MCP_SERVERS`](/docs/zh-CN/env-vars) 设置为 `false` 会为一个会话关闭连接器；无论两者中哪一个关闭它们，另一个都无法将其打开

```json settings.json theme={null}
{
  "disableClaudeAiConnectors": true
}
```

您使用 `--mcp-config` 显式传递的服务器不受影响。要阻止单个连接器而不是全部，请使用 [`deniedMcpServers`](#deniedmcpservers)。请参阅[禁用 claude.ai 连接器](/docs/zh-CN/mcp#disable-claude-ai-connectors)。

<h3 id="disabledmcpjsonservers">
  `disabledMcpjsonServers`
</h3>

拒绝项目 `.mcp.json` 文件中定义的特定服务器，以便 Claude Code 永远不会连接它们或要求您批准它们。任何设置文件中的拒绝都适用，包括签入存储库的项目 `.claude/settings.json`。

* **作用域**: [`Any file`](#scopes)
* **类型**: 字符串数组，服务器名称如 `.mcp.json` 中所示
* **默认值**: 未设置

```json settings.json theme={null}
{
  "disabledMcpjsonServers": ["filesystem"]
}
```

当您在批准对话框中拒绝服务器时，Claude Code 会将此密钥写入 `.claude/settings.local.json`。`claude mcp get <name>` 将被拒绝的服务器显示为 `✘ Rejected (see disabledMcpjsonServers in settings)`。拒绝优先于 [`enabledMcpjsonServers`](#enabledmcpjsonservers) 和 [`enableAllProjectMcpServers`](#enableallprojectmcpservers)。

<h3 id="enableallprojectmcpservers">
  `enableAllProjectMcpServers`
</h3>

批准项目 `.mcp.json` 文件中定义的每个 MCP 服务器，无需提示。当您在批准对话框中选择批准所有服务器时，Claude Code 会将此密钥写入 `.claude/settings.local.json`。

* **作用域**: [`Any file`](#scopes)。在您尚未接受信任对话框的文件夹中，Claude Code 从用户设置、托管设置和 `--settings` 中遵守它，并在共享项目文件中忽略它，包括在会话中以及 `claude mcp list` 和 `claude mcp get`；[项目服务器批准和工作区信任](/docs/zh-CN/mcp#project-server-approvals-and-workspace-trust)说明何时未跟踪的 `.claude/settings.local.json` 也计数。
* **类型**: 布尔值
  * `true`: Claude Code 批准项目 `.mcp.json` 文件中定义的每个 MCP 服务器，无需提示
  * `false`: Claude Code 要求您批准每个服务器。在受信任的文件夹中，较高优先级文件中的 `false` 会覆盖较低优先级文件中的 `true`；在您尚未信任的文件夹中，任何受尊重文件中的 `true` 就足够了
* **默认值**: 未设置，因此 Claude Code 要求您批准每个服务器

```json settings.json theme={null}
{
  "enableAllProjectMcpServers": true
}
```

[`disabledMcpjsonServers`](#disabledmcpjsonservers) 条目仍然会拒绝服务器。

<h3 id="enabledmcpjsonservers">
  `enabledMcpjsonServers`
</h3>

批准项目 `.mcp.json` 文件中定义的特定服务器，以便 Claude Code 连接它们而无需询问。当您在批准对话框中批准服务器时，Claude Code 会将此密钥写入 `.claude/settings.local.json`。

* **作用域**: [`Any file`](#scopes)。在您尚未接受信任对话框的文件夹中，Claude Code 从用户设置、托管设置和 `--settings` 中遵守它，并在共享项目文件中忽略它，包括在会话中以及 `claude mcp list` 和 `claude mcp get`；[项目服务器批准和工作区信任](/docs/zh-CN/mcp#project-server-approvals-and-workspace-trust)说明何时未跟踪的 `.claude/settings.local.json` 也计数。
* **类型**: 字符串数组，服务器名称如 `.mcp.json` 中所示
* **默认值**: 未设置

此示例批准项目 `.mcp.json` 中的 `memory` 和 `github` 服务器：

```json settings.json theme={null}
{
  "enabledMcpjsonServers": ["memory", "github"]
}
```

[`disabledMcpjsonServers`](#disabledmcpjsonservers) 条目仍然会拒绝服务器。

<h3 id="managedmcpservers">
  `managedMcpServers`
</h3>

从托管设置向每个用户提供远程 MCP 服务器。用户保留他们自己添加的服务器，无法编辑或删除您提供的服务器。需要 Claude Code v2.1.259 或更高版本。

* **作用域**: [`Managed`](#scopes)。Claude Code 在用户、项目和本地设置中使用警告删除该密钥，并且不在 Claude Desktop 应用的代码选项卡中读取它（在第三方部署上）或在应用的 Cowork 会话中读取它，其中 Claude Desktop 提供并锁定这些会话的 MCP 服务器。
* **类型**: 以服务器名称为键的对象。每个条目都具有 `http` 或 `sse` 服务器的 `.mcp.json` 形状：必需的 `https://` `url`，以及可选的 `headers`、`oauth` 和其他 HTTP 和 SSE 选项。Claude Code 删除验证失败的条目，[条目可以包含的内容](/docs/zh-CN/managed-mcp#what-an-entry-can-contain)列出了条件
* **默认值**: 未设置，因此托管设置不提供任何服务器

此示例提供一个名为 `search` 的 HTTP 服务器：

```json managed-settings.json theme={null}
{
  "managedMcpServers": {
    "search": {
      "type": "http",
      "url": "https://search.example.com/mcp"
    }
  }
}
```

有关优先级、提供的服务器如何与 `managed-mcp.json` 以及允许和拒绝列表结合、用户看到的内容，请参阅[通过托管设置提供服务器](/docs/zh-CN/managed-mcp#provide-servers-through-managed-settings)。

<h2 id="agents-sessions-and-worktrees">
  代理、会话和工作树
</h2>

设置默认代理、控制团队成员和跨会话消息传递，以及配置工作树。请参阅 [Subagents](/docs/zh-CN/sub-agents) 和 [Worktrees](/docs/zh-CN/worktrees)。

<h3 id="agent">
  `agent`
</h3>

将主线程作为命名的 [subagent](/docs/zh-CN/sub-agents#invoke-subagents-explicitly) 运行，以便 Claude Code 将该 subagent 的系统提示、工具限制和模型应用于您的会话。同一密钥为从 `claude agents` 分派的会话设置默认代理。

* **Scope**: [`Any file`](#scopes)
* **Type**: string，内置或自定义代理的名称
* **Default**: 未设置，因此主线程作为 Claude Code 的默认代理运行
* **Per-session overrides**: `--agent` 对一个会话的优先级高于此密钥

```json settings.json theme={null}
{
  "agent": "code-reviewer"
}
```

插件自己的 `settings.json` 也可以提供此密钥；请参阅 [Ship default settings with your plugin](/docs/zh-CN/plugins/components#default-settings)。

<h3 id="crosssessioninbound">
  `crossSessionInbound`
</h3>

选择此会话如何处理 [来自您其他 Claude Code 会话的消息](/docs/zh-CN/cross-session-messaging#control-inbound-messages)。当没有值适用时，Claude Code 根据两个会话的权限模式类从每条消息中决定。需要 Claude Code v2.1.224 或更高版本。

* **Scope**: [`Any file`](#scopes)。项目或本地值仅在严格于托管设置、`--settings` 标志或用户设置提供的值时才适用。
* **Type**: string，以下之一：
  * `"accept"`: Claude Code 将消息传递给 Claude
  * `"hold"`: Claude Code 显示消息通知而不传递它
  * `"refuse"`: Claude Code 丢弃消息
* **Default**: 未设置，因此 Claude Code 从每条消息中决定

```json settings.json theme={null}
{
  "crossSessionInbound": "hold"
}
```

Claude Code 首先读取托管设置，然后是 `--settings` 标志，然后是用户设置，并应用找到的第一个值。`refuse` 比 `hold` 更严格，`hold` 比 `accept` 更严格。当没有受信任的源设置值时，项目或本地 `hold` 或 `refuse` 仍然适用，替换每条消息的默认值。在具有跨会话消息传递的会话中，此密钥在 `/config` 中显示为 **Messages from your other sessions**，它将其写入用户设置；该行需要 Claude Code v2.1.232 或更高版本，当 `--settings` 标志或托管设置设置密钥时，Claude Code 会隐藏它。

Claude Code [warns](/docs/zh-CN/errors#crosssessioninbound-must-be-one-of-accept-hold-refuse) 当您设置它无法识别的值时。当该值存在于用户、项目、本地或 `--settings` 文件中时，Claude Code 会保留入站消息，即使优先级更高的源设置 `accept`。另一个源设置的 `refuse` 仍然适用。修复或删除该值以清除保留。

当无法识别的值在 [managed settings](/docs/zh-CN/managed-settings) 中时，Claude Code 改为将其视为 `refuse`，直到管理员修复它。在 v2.1.248 之前，Claude Code 忽略无法识别的值而不发出警告。

<h3 id="disableagentview">
  `disableAgentView`
</h3>

关闭 [background agents and agent view](/docs/zh-CN/agent-view)：`claude agents`、`--bg`、`/background` 和按需主管。在 [managed settings](/docs/zh-CN/managed-settings) 中设置它以为组织强制执行。

* **Scope**: [`Any file`](#scopes)
* **Type**: Boolean
  * `true`: Claude Code 关闭 `claude agents`、`--bg`、`/background` 和按需主管
  * `false`: agent view 可用
* **Default**: 未设置，因此 agent view 可用
* **Per-session overrides**: [`CLAUDE_CODE_DISABLE_AGENT_VIEW`](/docs/zh-CN/env-vars) 为一个会话关闭 agent view；无论两者中哪一个关闭它，另一个都无法将其打开

```json settings.json theme={null}
{
  "disableAgentView": true
}
```

<h3 id="isolatepeermachines">
  `isolatePeerMachines`
</h3>

在 Claude 的 `SendMessage` 到达此机器之外的您的会话之前，需要您的明确批准；请参阅 [Require approval for cross-machine messages](/docs/zh-CN/cross-session-messaging#require-approval-for-cross-machine-messages)。即使在 [`bypassPermissions` mode](/docs/zh-CN/permission-modes#skip-all-checks-with-bypasspermissions-mode) 中，批准提示也会出现。

* **Scope**: [`Any file`](#scopes)。来自任何范围的 `true` 都适用，因此签入的项目文件可以打开要求但不能关闭。
* **Type**: Boolean
  * `true`: Claude Code 在 Claude 的 `SendMessage` 到达此机器之外的您的会话之前要求您的批准
  * `false`: 跨机器消息不提示
* **Default**: 未设置，因此跨机器消息不提示

```json settings.json theme={null}
{
  "isolatePeerMachines": true
}
```

跨机器 `SendMessage` 批准需要 Claude Code v2.1.224 或更高版本。

<h3 id="processwrapper">
  `processWrapper`
</h3>

在 macOS 和 Linux 上，在 [Claude Code 启动的后台进程](/docs/zh-CN/corporate-launcher#what-the-launcher-covers) 前面放置公司启动器命令。Claude Code 使用其自己的命令行附加运行启动器，因此启动器必须执行到 Claude Code；请参阅 [Run Claude Code behind a corporate launcher](/docs/zh-CN/corporate-launcher) 了解启动器合约。需要 Claude Code v2.1.210 或更高版本。

* **Scope**: [`User or managed`](#scopes)
* **Type**: string，启动器命令作为 argv 前缀，例如带有可选参数的绝对路径
* **Default**: 未设置，因此后台进程启动时不包装
* **Per-session overrides**: [`CLAUDE_CODE_PROCESS_WRAPPER`](/docs/zh-CN/env-vars) 对此密钥的一个会话优先级更高

```json settings.json theme={null}
{
  "processWrapper": "/opt/corp/launcher --profile claude"
}
```

Claude Code 在 Windows 上忽略启动器并启动每个进程不包装。需要 Claude Code v2.1.210 或更高版本。

<h3 id="teammatemode">
  `teammateMode`
</h3>

选择 Claude Code 显示 [agent team](/docs/zh-CN/agent-teams) 队友的位置：在您的主终端窗格内，或在您的终端支持时在分割窗格中。请参阅 [Choose a display mode](/docs/zh-CN/agent-teams#choose-a-display-mode)。

* **Scope**: [`Any file`](#scopes)。Claude Code 也读取由较旧版本留在 `~/.claude.json` 中的值。
* **Type**: string，以下之一：
  * `"in-process"`: 队友在您的主终端窗格内运行
  * `"auto"`: 当您在 tmux 内运行时分割窗格，或在 iTerm2 内运行且 `it2` 在您的 `PATH` 上或安装了 tmux；否则为进程内
  * `"tmux"`: 使用 tmux 或 iTerm2 分割窗格，从您的终端检测
  * `"iterm2"`: iTerm2 本机分割窗格通过 `it2` CLI
* **Default**: `"in-process"`
* **Per-session overrides**: `--teammate-mode` 对此密钥的一个会话优先级更高

```json settings.json theme={null}
{
  "teammateMode": "auto"
}
```

<span id="worktree-settings" />

<h3 id="worktree">
  `worktree`
</h3>

配置 Claude Code 如何为 `--worktree`、`EnterWorktree` 工具以及隔离的 subagents 和后台会话创建和管理 [git worktrees](/docs/zh-CN/worktrees)。

* **Scope**: [`Any file`](#scopes)
* **Type**: object with `baseRef`, `symlinkDirectories`, `sparsePaths`, and `bgIsolation`
* **Default**: 未设置

此示例从您当前的 `HEAD` 分支新工作树，并将 `node_modules` 符号链接到每个工作树中：

```json settings.json theme={null}
{
  "worktree": {
    "baseRef": "head",
    "symlinkDirectories": ["node_modules"]
  }
}
```

要将 gitignored 文件（如 `.env`）复制到新工作树中，请改为在项目根目录中添加 [`.worktreeinclude` file](/docs/zh-CN/worktrees#copy-gitignored-files-into-worktrees)，而不是设置。

<h3 id="worktree-baseref">
  `worktree.baseRef`
</h3>

选择新工作树从哪个 ref 分支。`"fresh"` 从 `origin/<default-branch>` 分支以获得与远程匹配的干净树；`"head"` 从您当前的本地 `HEAD` 分支，因此未推送的提交和功能分支状态存在于工作树中。

* **Scope**: [`Any file`](#scopes)
* **Type**: string，以下之一：
  * `"fresh"`: 新工作树从 `origin/<default-branch>` 分支
  * `"head"`: 新工作树从您当前的本地 `HEAD` 分支，包括未推送的提交
* **Default**: `"fresh"`

```json settings.json theme={null}
{
  "worktree": {
    "baseRef": "head"
  }
}
```

在链接的工作树内，`"head"` 解析为该工作树的 `HEAD`，而不是主检出的。

<h3 id="worktree-symlinkdirectories">
  `worktree.symlinkDirectories`
</h3>

将目录从主存储库符号链接到每个工作树中，以便您不会在磁盘上复制大型目录。

* **Scope**: [`Any file`](#scopes)
* **Type**: array of strings，相对于存储库根目录的目录路径
* **Default**: 未设置，因此 Claude Code 不符号链接任何目录

此示例将 `node_modules` 和 `.cache` 从主存储库符号链接到每个新工作树中：

```json settings.json theme={null}
{
  "worktree": {
    "symlinkDirectories": ["node_modules", ".cache"]
  }
}
```

<h3 id="worktree-sparsepaths">
  `worktree.sparsePaths`
</h3>

通过 git sparse-checkout 在每个工作树中仅检出列出的目录。Claude Code 仅将这些目录加上根级文件写入磁盘，这在大型 monorepos 中更快；请参阅 [Check out only the directories you need](/docs/zh-CN/large-codebases#check-out-only-the-directories-you-need)。

* **Scope**: [`Any file`](#scopes)
* **Type**: array of strings，相对于存储库根目录的目录路径
* **Default**: 未设置，因此每个工作树检出整个树

此示例在每个工作树中仅检出 `packages/my-app` 和 `shared/utils`，加上根级文件：

```json settings.json theme={null}
{
  "worktree": {
    "sparsePaths": ["packages/my-app", "shared/utils"]
  }
}
```

当稀疏工作树存在时，git 在存储库的共享 `.git/config` 中启用 `extensions.worktreeConfig`。

<h3 id="worktree-bgisolation">
  `worktree.bgIsolation`
</h3>

选择[后台会话](/docs/zh-CN/agent-view#how-file-edits-are-isolated)如何隔离其文件编辑。如果您是通过 `←` 或 `/background` 将会话移至后台的，则无论此键如何设置，该会话都会就地编辑文件。使用 `"worktree"` 时，Claude Code 会在会话调用 `EnterWorktree` 之前阻止在主检出中使用 `Edit` 和 `Write`；使用 `"none"` 时，后台作业直接编辑工作副本。对于不适合使用 git worktree 的仓库，请设置 `"none"`。

* **Scope**: [`Any file`](#scopes)
* **Type**: string，以下之一：
  * `"worktree"`: Claude Code 在会话调用 `EnterWorktree` 之前阻止主检出中的 `Edit` 和 `Write`
  * `"none"`: 后台作业直接编辑工作副本
* **Default**: `"worktree"`

```json settings.json theme={null}
{
  "worktree": {
    "bgIsolation": "none"
  }
}
```

在 git 存储库之外，失败的 [`WorktreeCreate` hook](/docs/zh-CN/worktrees#non-git-version-control) 释放块，以便会话可以就地编辑工作目录；该释放需要 Claude Code v2.1.203 或更高版本。

<h2 id="remote-desktop-and-notifications">
  远程、桌面和通知
</h2>

配置远程控制、云环境、桌面应用和 Claude Code 在需要你时发送的通知。请参阅[远程控制](/docs/zh-CN/remote-control)。

<h3 id="agentpushnotifenabled">
  `agentPushNotifEnabled`
</h3>

允许 Claude 在认为值得发送时向你的手机发送推送通知，例如当长任务完成时。Claude Code 将此选择同步到你的账户，推送在[远程控制](/docs/zh-CN/remote-control)连接时到达。在 `/config` 中显示为**Claude 决定时推送**。

* **作用域**: [`任何文件`](#scopes)。Claude Code 也会读取由旧版本留在 `~/.claude.json` 中的值。
* **类型**: 布尔值
  * `true`: Claude 可以在认为值得时向你的手机发送推送通知
  * `false`: Claude 不发送这些通知
* **默认值**: `false`

```json settings.json theme={null}
{
  "agentPushNotifEnabled": true
}
```

请参阅[移动推送通知](/docs/zh-CN/remote-control#mobile-push-notifications)。

<h3 id="awaysummaryenabled">
  `awaySummaryEnabled`
</h3>

当你离开终端几分钟后返回时，显示一行会话摘要。将其设置为 `false`，或在 `/config` 中关闭**会话摘要**，以停止摘要。

* **作用域**: [`任何文件`](#scopes)
* **类型**: 布尔值
  * `true`: 你离开几分钟后返回时会看到一行会话摘要
  * `false`: Claude Code 不显示摘要
* **默认值**: 未设置，因此摘要处于开启状态
* **每个会话的覆盖**: [`CLAUDE_CODE_ENABLE_AWAY_SUMMARY`](/docs/zh-CN/env-vars) 在任一方向上优先于此键一个会话

```json settings.json theme={null}
{
  "awaySummaryEnabled": false
}
```

Claude Code 在非交互模式下永远不会显示摘要。

<h3 id="disableartifact">
  `disableArtifact`
</h3>

<Warning>
  已弃用，已被 [`enableArtifact`](#enableartifact) 替代。Claude Code 仍然将 `disableArtifact: true` 视为等同于 `enableArtifact: false`，并忽略 `disableArtifact: false`。
</Warning>

改用 [`enableArtifact`](#enableartifact) 来关闭 [Artifact](/docs/zh-CN/artifacts) 工具，该工具将会话输出发布为 claude.ai 上的私有网页。当你在 `/config` 中关闭**Artifacts** 行时，Claude Code 会将 `enableArtifact` 写入你的用户设置并清除此键。

* **作用域**: [`任何文件`](#scopes)
* **类型**: 布尔值
  * `true`: Claude Code 为该文件适用的每个会话关闭 Artifact 工具，且没有其他文件将其打开
  * `false`: 被忽略；要保持工具打开，请删除该键
* **默认值**: 未设置，因此工具遵循你账户的[可用性](/docs/zh-CN/artifacts#availability)
* **每个会话的覆盖**: [`CLAUDE_CODE_DISABLE_ARTIFACT`](/docs/zh-CN/env-vars) 设置为 `1` 会为一个会话关闭工具

```json settings.json theme={null}
{
  "disableArtifact": true
}
```

[禁用 artifacts](/docs/zh-CN/artifacts#disable-artifacts) 列出了关闭工具的每种方式。

<h3 id="disabledeeplinkregistration">
  `disableDeepLinkRegistration`
</h3>

阻止 Claude Code 向操作系统注册 `claude-cli://` 协议处理程序，否则在你发送交互式会话的第一个提示后会进行注册。[深链接](/docs/zh-CN/deep-links)允许外部工具使用预填充的提示打开 Claude Code 会话。在协议处理程序注册受限或单独管理的环境中设置此项。

* **作用域**: [`任何文件`](#scopes)
* **类型**: 字符串 `"disable"`
* **默认值**: 未设置，因此 Claude Code 注册处理程序

```json settings.json theme={null}
{
  "disableDeepLinkRegistration": "disable"
}
```

<h3 id="disabledesktoplocalsessions">
  `disableDesktopLocalSessions`
</h3>

在[桌面应用](/docs/zh-CN/desktop#local-sessions-on-managed-devices)中关闭在设备上运行的 Code 会话，用于开发人员应该通过 SSH 在远程机器上工作的部署。在 Code 选项卡中，**本地**环境保留在环境下拉列表中，但呈灰显状态且无法选择，工具提示显示你的组织已关闭它；在 Windows 上，WSL 条目以相同方式呈灰显，尽管 WSL 会话是否在托管设备上运行[由单独管理](/docs/zh-CN/admin-setup#wsl-sessions-in-claude-code-desktop)。新会话默认为第一个[SSH 连接](/docs/zh-CN/desktop#ssh-sessions)（如果已配置），应用拒绝在设备上启动或恢复会话，包括返回同一机器的 SSH 连接。到其他主机的 SSH 会话和云会话不受影响。桌面应用读取此键；终端 CLI 忽略它。需要 Claude Desktop v1.37937.0 或更高版本。

* **作用域**: [`托管`](#scopes)。默认情况下，桌面应用从[一个托管源](/docs/zh-CN/managed-settings#how-claude-code-combines-managed-sources)读取此键。
* **类型**: 布尔值；仅 JSON 布尔值 `true` 生效
  * `true`: 桌面应用不提供设备上的 Code 会话；现有本地会话保留在列表中但无法继续
  * `false`: 本地会话保持可用
* **默认值**: 未设置，因此本地会话可用

```json managed-settings.json theme={null}
{
  "disableDesktopLocalSessions": true
}
```

桌面应用忽略任何其他值，非布尔值（如字符串 `"true"` 或 `1`）也会记录警告。将其与 [`sshConfigs`](#sshconfigs) 配对，以便用户登陆到工作连接，并与 [`sshHostAllowlist`](#sshhostallowlist) 配对以限制他们可以访问的主机。请参阅[托管设备上的本地会话](/docs/zh-CN/desktop#local-sessions-on-managed-devices)。

Claude Desktop 为 Code 会话提供从你的桌面配置派生的策略，例如出口允许列表、文件系统沙箱和第三方部署中的 MCP 限制。每当存在[管理员源](/docs/zh-CN/managed-settings#how-claude-code-combines-managed-sources)时，Claude Code 忽略这些父设置：服务器管理的设置、MDM 或操作系统级别的策略或托管设置文件。通过其中一个在之前没有的设备上部署此键（如在第三方部署中），因此会停止桌面派生的策略应用。[让嵌入主机添加策略](/docs/zh-CN/managed-settings#let-an-embedding-host-add-policy)涵盖了父设置何时仍可合并；这适用于你以这种方式部署的任何键，不仅仅是这个。

<h3 id="disableremotecontrol">
  `disableRemoteControl`
</h3>

关闭[远程控制](/docs/zh-CN/remote-control)：Claude Code 随后拒绝 `claude remote-control`、`--remote-control` 标志、自动启动和会话内切换，并报告你的组织的策略已禁用它。将其放在[托管设置](/docs/zh-CN/managed-settings)中以进行每个设备的 MDM 强制执行。

* **作用域**: [`任何文件`](#scopes)
* **类型**: 布尔值
  * `true`: Claude Code 拒绝 `claude remote-control`、`--remote-control` 标志、自动启动和会话内切换
  * `false`: 远程控制保持可用
* **默认值**: `false`

```json settings.json theme={null}
{
  "disableRemoteControl": true
}
```

<h3 id="enableartifact">
  `enableArtifact`
</h3>

关闭 [Artifact](/docs/zh-CN/artifacts) 工具，该工具将会话输出发布为 claude.ai 上的私有网页。当你在 `/config` 中关闭**Artifacts** 行时，Claude Code 会将此键写入你的用户设置，因此你通常不需要手动编辑它。需要 Claude Code v2.1.196 或更高版本。

* **作用域**: [`任何文件`](#scopes)。每个文件都可以关闭工具，但没有文件可以将其打开。
* **类型**: 布尔值
  * `false`: Claude Code 为该文件适用的每个会话关闭 Artifact 工具
  * `true`: 与保留键未设置相同，因为它永远不会覆盖来自另一个文件、[`CLAUDE_CODE_DISABLE_ARTIFACT`](/docs/zh-CN/env-vars) 或你的组织[管理员设置](/docs/zh-CN/artifacts#manage-artifacts-for-your-organization)的 `false`
* **默认值**: 未设置，因此工具遵循你账户的[可用性](/docs/zh-CN/artifacts#availability)

```json settings.json theme={null}
{
  "enableArtifact": false
}
```

当除你自己的用户设置之外的源保持工具关闭时，Claude Code 在 `/config` 中隐藏**Artifacts** 行，因为在那里打开它不会改变任何东西。[禁用 artifacts](/docs/zh-CN/artifacts#disable-artifacts) 列出了关闭工具的每种方式。

<h3 id="inputneedednotifenabled">
  `inputNeededNotifEnabled`
</h3>

当权限提示或问题等待你的输入时，在你的手机上获得推送通知。Claude Code 仅在[远程控制](/docs/zh-CN/remote-control)连接时发送这些通知。在 `/config` 中显示为**需要操作时推送**。

* **作用域**: [`任何文件`](#scopes)。Claude Code 也会读取由旧版本留在 `~/.claude.json` 中的值。
* **类型**: 布尔值
  * `true`: 当权限提示或问题等待时，你会在手机上获得推送通知，同时远程控制已连接
  * `false`: Claude Code 不发送此类通知
* **默认值**: `false`

```json settings.json theme={null}
{
  "inputNeededNotifEnabled": true
}
```

请参阅[移动推送通知](/docs/zh-CN/remote-control#mobile-push-notifications)。

<h3 id="preferrednotifchannel">
  `preferredNotifChannel`
</h3>

选择 Claude Code 在任务完成或权限提示等待时如何通知你。在 `/config` 中显示为**本地通知**。

* **作用域**: [`任何文件`](#scopes)。Claude Code 也会读取由旧版本留在 `~/.claude.json` 中的值。
* **类型**: 字符串，以下之一：
  * `"auto"`: Claude Code 在 iTerm2、Ghostty 和 Kitty 中发送桌面通知，在 Terminal.app 中仅当其可听铃声关闭时才响铃，在其他地方不执行任何操作
  * `"terminal_bell"`: Claude Code 在任何终端中响铃字符
  * `"iterm2"`: Claude Code 发送 iTerm2 桌面通知
  * `"iterm2_with_bell"`: Claude Code 发送 iTerm2 桌面通知并响铃
  * `"kitty"`: Claude Code 发送 Kitty 桌面通知
  * `"ghostty"`: Claude Code 发送 Ghostty 桌面通知
  * `"notifications_disabled"`: Claude Code 不发送通知
* **默认值**: `"auto"`

```json settings.json theme={null}
{
  "preferredNotifChannel": "terminal_bell"
}
```

使用 `"auto"` 时，Claude Code 在 iTerm2、Ghostty 和 Kitty 中发送桌面通知。在 Terminal.app 中，仅当你关闭了 Terminal 的可听铃声时才响铃字符，在其他终端中不执行任何操作。设置 `"terminal_bell"` 以在任何终端中响铃字符。请参阅[获取终端铃声或通知](/docs/zh-CN/terminal-config#get-a-terminal-bell-or-notification)。

<h3 id="remote-defaultenvironmentid">
  `remote.defaultEnvironmentId`
</h3>

为你从 CLI 创建的云会话（例如使用 `claude --cloud`）选择默认[云环境](/docs/zh-CN/cloud-environments)。当你使用 [`/remote-env`](/docs/zh-CN/cloud-environments#select-an-environment-from-the-cli) 选择环境时，Claude Code 会将此键写入你的用户设置。

* **作用域**: [`任何文件`](#scopes)。对于自托管环境 ID，仅用户或托管设置或 `--settings` 标志。
* **类型**: 字符串，环境 ID，如 `env_...` 或 `ccpool_...`
* **默认值**: 未设置，因此当你的列表有 Anthropic 托管环境时 Claude Code 使用它，否则使用列表中不是[远程控制桥接环境](/docs/zh-CN/cloud-environments#the-default-environment)的第一个环境，或当每个都是桥接环境时使用第一个环境
* **每个会话的覆盖**: `--environment` 优先于此键用于它创建的一个云会话

```json settings.json theme={null}
{
  "remote": {
    "defaultEnvironmentId": "env_0123abcd"
  }
}
```

Anthropic 托管的环境 ID（以 `env_` 开头）遵循标准设置优先级，因此存储库的项目设置中的值会覆盖你的用户级别选择。[自托管环境](/docs/zh-CN/self-hosted-environments) ID（以 `ccpool_` 开头）仅从用户设置、托管设置和 `--settings` 标志中获得尊重；Claude Code 忽略存储库的项目或本地设置中的一个，`/remote-env` 显示它忽略了哪个值，因此签入的文件无法将会话引导到你未选择的自托管环境。

<h3 id="remotecontrolatstartup">
  `remoteControlAtStartup`
</h3>

当每个交互式会话启动时自动连接[远程控制](/docs/zh-CN/remote-control)，而不是等待 `/remote-control`。将其设置为 `true` 以打开自动连接，`false` 以关闭。在 `/config` 中显示为**为所有会话启用远程控制**。

* **作用域**: [`任何文件`](#scopes)。Claude Code 也会读取由旧版本留在 `~/.claude.json` 中的值。
* **类型**: 布尔值
  * `true`: Claude Code 在每个交互式会话启动时自动连接远程控制
  * `false`: Claude Code 等待 `/remote-control`
* **默认值**: 未设置，因此[自动连接默认值](/docs/zh-CN/remote-control#enable-remote-control-for-all-sessions)适用
* **每个会话的覆盖**: `--remote-control` 即使此键为 `false` 也会为一个会话打开远程控制，没有标志会为一个会话关闭它

```json settings.json theme={null}
{
  "remoteControlAtStartup": true
}
```

Claude Code 忽略项目或本地设置中的 `true`，因此存储库可以为其检出关闭自动连接，但无法打开。有关完整的每个作用域行为，请参阅[为所有会话启用远程控制](/docs/zh-CN/remote-control#enable-remote-control-for-all-sessions)和[应用更严格值的安全键](/docs/zh-CN/settings#security-keys-where-the-stricter-value-applies)。

<h3 id="sshconfigs">
  `sshConfigs`
</h3>

将 SSH 连接添加到[桌面](/docs/zh-CN/desktop#pre-configure-ssh-connections-for-your-team)环境下拉列表。管理员使用它向团队分发共享连接。你在托管设置中定义的连接显示为托管，因此用户可以选择它们，但无法在应用中编辑或删除它们。

* **作用域**: [`用户或托管`](#scopes)。桌面应用读取此键。默认情况下，它从[一个托管源](/docs/zh-CN/managed-settings#how-claude-code-combines-managed-sources)读取托管连接。
* **类型**: 对象数组，每个都有必需的 `id`、`name` 和 `sshHost` 以及可选的 `sshPort` 和 `sshIdentityFile`
* **默认值**: 未设置

此示例添加一个名为 `Dev VM` 的连接，连接到 `user@dev.example.com`：

```json settings.json theme={null}
{
  "sshConfigs": [
    {
      "id": "dev-vm",
      "name": "Dev VM",
      "sshHost": "user@dev.example.com"
    }
  ]
}
```

<h3 id="sshhostallowlist">
  `sshHostAllowlist`
</h3>

限制[桌面 SSH 会话](/docs/zh-CN/desktop#restrict-which-ssh-hosts-users-can-connect-to)可以连接到的主机。仅桌面应用读取此键；CLI 不读取。模式不区分大小写：`*` 匹配任何主机，`*.example.com` 匹配 `example.com` 和每个子域，其他任何内容都是针对 `~/.ssh/config` 解析后的主机名的精确匹配。空数组关闭 SSH 会话。

* **作用域**: [`托管`](#scopes)。默认情况下，桌面应用从[一个托管源](/docs/zh-CN/managed-settings#how-claude-code-combines-managed-sources)读取此键。
* **类型**: 主机名模式数组
* **默认值**: 未设置，因此允许任何主机

此示例允许 `devboxes.example.com` 及其子域，加上精确主机 `bastion.example.com`：

```json managed-settings.json theme={null}
{
  "sshHostAllowlist": ["*.devboxes.example.com", "bastion.example.com"]
}
```

桌面应用无法读取为主机列表的值（例如 `true` 或对象）在您更正之前会被视为空数组，但 `null` 除外，它被视为未设置。需要 Claude Desktop v2.26454.0 或更高版本。

如果您在优先级最高的源中将 [`managedSourcesBehavior`](#managedsourcesbehavior) 设置为 `"merge"`，桌面应用会合并来自每个[管理员源](/docs/zh-CN/managed-settings#how-claude-code-combines-managed-sources)的列表，并允许与其中任意一个列表匹配的主机。如果您在某个源中设置了空数组，对于另一个源列出的主机，SSH 会话仍保持开启。

<span id="authentication-and-login" />

<h2 id="authentication-and-providers">
  身份验证和提供商
</h2>

通过辅助脚本提供凭据，对于组织，强制使用登录方法或组织。请参阅[身份验证](/docs/zh-CN/authentication)。

<h3 id="allowedproviders">
  `allowedProviders`
</h3>

列出机器可以通过其访问 Claude 的服务，例如 Anthropic API、Amazon Bedrock 或 LLM 网关。使用未列出的提供商的会话会在启动时、登录时以及下次联系 API 时被拒绝，因此在会话中途切换到未列出的提供商也会被拒绝。[拒绝消息](/docs/zh-CN/errors#managed-settings-dont-allow-this-api-provider)会指明是什么选择了该提供商以及继续操作的步骤。需要 Claude Code v2.1.285 或更高版本。

* **Scope**: [`Managed`](#scopes)。由机器自身的管理员源（MDM 策略和托管设置文件）设置的列表，在服务器托管设置也提供一个列表时仍继续生效：此时会话只能使用同时出现在两个列表上的提供商，因此服务器托管列表可以缩小机器允许的范围，但永远不能扩大它。哪个机器源的 `allowedProviders` 生效遵循[Claude Code 如何组合托管源](/docs/zh-CN/managed-settings#how-claude-code-combines-managed-sources)。仅通过服务器托管设置提供的列表只会作用于[获取服务器托管设置](/docs/zh-CN/server-managed-settings#platform-availability)的会话。
* **Type**: 字符串数组，每个都是以下之一：
  * `"anthropic"`：Anthropic 自有主机上的 Anthropic API，通过 claude.ai 或 Console 登录或 API 密钥访问。将其与 [`forceLoginMethod`](#forceloginmethod) 或 [`forceLoginOrgUUID`](#forceloginorguuid) 配合使用，以同时限制登录
  * `"bedrock"`：[Amazon Bedrock](/docs/zh-CN/amazon-bedrock)
  * `"vertex"`：[Google Cloud 的 Agent Platform](/docs/zh-CN/google-vertex-ai)，以前称为 Vertex AI
  * `"foundry"`：[Microsoft Foundry](/docs/zh-CN/microsoft-foundry)
  * `"anthropicAws"`：[AWS 上的 Claude Platform](/docs/zh-CN/claude-platform-on-aws)
  * `"mantle"`：Amazon Bedrock [Mantle 端点](/docs/zh-CN/amazon-bedrock#use-the-mantle-endpoint)。[在 Invoke API 旁边运行 Mantle](/docs/zh-CN/amazon-bedrock#run-mantle-alongside-the-invoke-api) 的会话使用两个提供商，因此需为其将 `"bedrock"` 和 `"mantle"` 一起列出
  * `"customEndpoint"`：发送到其他主机的 Anthropic API 或云提供商的 API，例如由 `ANTHROPIC_BASE_URL` 或由提供商的端点变量（例如 `ANTHROPIC_BEDROCK_BASE_URL`）指定的 [LLM 网关](/docs/zh-CN/llm-gateway)。Claude Code 仅允许托管 [`env`](#env) 块所固定的确切值
  * `"gateway"`：[Cloud 网关](/docs/zh-CN/claude-apps-gateway)登录
* **Default**: 未设置，因此可以使用任何提供商

```json managed-settings.json theme={null}
{
  "allowedProviders": ["anthropic", "bedrock"]
}
```

每个云提供商的条目指该提供商自己的服务，包括其区域、FIPS 和私有端点。

Claude Code 无法识别为提供商名称的条目会被删除并报告，列表的其余部分仍保持强制执行。如果列表为空，或其每个条目都无法识别，Claude Code 会拒绝所有提供商，并且不会在该机器上启动。

<h4 id="endpoints-that-need-a-pin-in-managed-env">
  需要在托管 `env` 中固定的端点
</h4>

固定值是在托管 [`env`](#env) 块中设置的端点变量的值。当会话将提供商的流量发送到该提供商自己的服务以外的地方时，Claude Code 仅在会话的值与固定值相同时才允许它。以下端点需要固定值：

* **`"customEndpoint"` 会话**：指定主机的变量，例如 `ANTHROPIC_BASE_URL`
* **Amazon Bedrock**：当 AWS SDK 的 `AWS_ENDPOINT_URL`、`AWS_ENDPOINT_URL_BEDROCK` 和 `AWS_ENDPOINT_URL_BEDROCK_RUNTIME` 变量指向 Bedrock 自己的服务之外时。会话仍归于 `"bedrock"` 而不是 `"customEndpoint"`
* **网关登录的 URL**：会话仍归于 `"gateway"`，[`forceLoginGatewayUrl`](#forcelogingatewayurl) 也计为固定值

哪些 `env` 块计为固定值取决于列表设置的位置：

* **机器上的管理员源设置了列表**：仅机器自身管理员源的 `env` 块计为固定值
* **仅服务器托管设置设置了列表**：这些服务器托管设置中的 `env` 值也计为固定值

该列表不评判云提供商的凭据和租户变量或网络路径，例如 `HTTPS_PROXY` 和证书设置。请在托管 `env` 块中为所有机器设置这些内容。

<h3 id="apikeyhelper">
  `apiKeyHelper`
</h3>

运行您自己的命令来生成 Claude Code 随模型请求发送的凭据。Claude Code 通过系统 shell 运行该命令，在 macOS 和 Linux 上为 `/bin/sh`，在 Windows 上为 `cmd`，并将其输出同时作为 `X-Api-Key` 和 `Authorization: Bearer` 标头发送。将其用于动态或轮换的凭据，例如从保管库获取的短期令牌。

* **Scope**: [`Any file`](#scopes)
* **Type**: string，shell 命令行
* **Default**: 未设置，因此 Claude Code 不运行辅助程序

```json settings.json theme={null}
{
  "apiKeyHelper": "/bin/generate_temp_api_key.sh"
}
```

Claude Code 缓存该值并在以下情况下重新运行该命令：

* 在缓存生命周期之后，默认为五分钟或您使用 [`CLAUDE_CODE_API_KEY_HELPER_TTL_MS`](/docs/zh-CN/env-vars) 设置的间隔。
* 当对 Anthropic API 的请求（直接或通过 [LLM 网关](/docs/zh-CN/llm-gateway)）失败并返回 `401` 或 `403` 时。
* 在向 Anthropic API 发送请求之前（直接或通过 LLM 网关），当缓存的输出是在辅助程序生成后已过期的 JWT 时。需要 Claude Code v2.1.246 或更高版本。

最后两种情况仅在辅助程序的输出是 Claude Code 发送的凭据且未设置 `ANTHROPIC_AUTH_TOKEN` 时适用。

在交互式会话中，当命令来自项目或本地设置时，Claude Code 在您接受工作区信任提示之前不会运行它。请参阅[凭据管理](/docs/zh-CN/authentication#credential-management)。

<h3 id="awsauthrefresh">
  `awsAuthRefresh`
</h3>

运行您自己的命令（例如 `aws sso login`），以在 Claude Code 用于 [Amazon Bedrock](/docs/zh-CN/amazon-bedrock) 的凭据失效时刷新 `.aws` 目录中的凭据。Claude Code 首先通过 STS 检查当前凭据，仅在该检查失败时运行该命令，然后读取刷新后的 `.aws` 目录。

当多个使用相同命令和凭据的 Claude Code 进程（例如不同的终端或 IDE 窗口）同时检查失败时，由一个进程运行该命令，其余进程等待该次运行，而不是各自启动运行。在有待处理请求的情况下已等待 60 秒的进程会自行运行该命令。要关闭此行为，请将 [`CLAUDE_CODE_DISABLE_AUTH_REFRESH_LOCK`](/docs/zh-CN/env-vars) 设置为 `1`。

* **Scope**: [`Any file`](#scopes)
* **Type**: string，shell 命令行
* **Default**: 未设置，因此 Claude Code 不会为您刷新 AWS 凭据

```json settings.json theme={null}
{
  "awsAuthRefresh": "aws sso login --profile myprofile"
}
```

当您的刷新流程写入 `.aws` 时使用此设置项；当它打印凭据时改用 [`awsCredentialExport`](#awscredentialexport)。请参阅[高级凭据配置](/docs/zh-CN/amazon-bedrock#advanced-credential-configuration)。

<h3 id="awscredentialexport">
  `awsCredentialExport`
</h3>

运行您自己的命令，该命令将 AWS 凭据打印为 JSON，以便 Claude Code 可以使用不存放在 `.aws` 目录中的凭据调用 [Amazon Bedrock](/docs/zh-CN/amazon-bedrock)。Claude Code 接受 `aws sts` 输出格式和扁平的 `aws configure export-credentials` 格式，并将凭据限定于其自己的 Bedrock 客户端，因此 Claude 运行的 shell 命令仍然看到您的环境凭据。

* **Scope**: [`Any file`](#scopes)
* **Type**: string，shell 命令行
* **Default**: 未设置，因此 Claude Code 使用环境中的 AWS 凭据链

```json settings.json theme={null}
{
  "awsCredentialExport": "/bin/generate_aws_grant.sh"
}
```

与 [`awsAuthRefresh`](#awsauthrefresh) 不同，只要设置了此命令，Claude Code 就始终运行它，而不会先检查环境凭据。请参阅[高级凭据配置](/docs/zh-CN/amazon-bedrock#advanced-credential-configuration)。

<h3 id="forceloginmethod">
  `forceLoginMethod`
</h3>

限制人们可以使用哪种帐户登录。设置 `"claudeai"` 以仅允许 claude.ai 帐户，设置 `"console"` 以仅允许 Claude Console 帐户，或设置 `"gateway"` 以将人们引导至 [cloud gateway](/docs/zh-CN/claude-apps-gateway) 而不是第一方登录。管理员在托管设置中设置它，并将其与 [`forceLoginOrgUUID`](#forceloginorguuid) 配合使用，以将开发人员的 claude.ai 登录限制在一个组织内。如果您在任何设置文件中将其设置为 `"claudeai"` 或 `"console"`，Claude Code 也会在该文件适用的会话中停止提供[无密钥 Console 登录](/docs/zh-CN/authentication#sign-in-without-an-api-key)。

* **Scope**: [`Any file`](#scopes)。Claude Code 仅接受来自机器上托管源（`managed-settings.json`、macOS plist 或 Windows HKLM 注册表或策略辅助程序）的 `"gateway"`。它在用户、项目、本地、HKCU 和服务器托管设置中将 `"gateway"` 视为未设置，与 [`forceLoginGatewayUrl`](#forcelogingatewayurl) 的规则相同。
* **Type**: string，以下之一：
  * `"claudeai"`：仅 claude.ai 帐户可以登录
  * `"console"`：仅 Claude Console 帐户可以登录
  * `"gateway"`：Claude Code 将人们引导至 cloud gateway 而不是第一方登录
* **Default**: 未设置，因此人们自行选择登录方法

```json settings.json theme={null}
{
  "forceLoginMethod": "claudeai"
}
```

每个第一方登录路径都会应用该限制，包括 [VS Code 扩展](/docs/zh-CN/vs-code)、Agent SDK、`claude setup-token` 和 `/install-github-app`，但终端的交互式登录屏幕（通过 `/login` 或首次运行引导进入）除外，它会预先选择该方法但不强制执行。在 v2.1.212 之前，仅终端登录应用该限制。请参阅[限制登录到您的组织](/docs/zh-CN/authentication#restrict-login-to-your-organization)，了解如何处理每个登录路径、环境凭据和第三方提供商。

当机器上的托管源设置 `"gateway"` 时，Claude Code 不会使用遗留的登录、API 密钥或 `apiKeyHelper` 凭据。请参阅[管理员策略需要 Cloud gateway 登录](/docs/zh-CN/errors#administrator-policy-requires-a-cloud-gateway-sign-in)，了解每种情况生成的消息。如果您通过 `CLAUDE_CODE_USE_BEDROCK` 或类似的环境变量选择云提供商，该会话不需要网关登录。在 v2.1.261 之前，Claude Code 在这些机器上会使用遗留的登录。

<h3 id="forcelogingatewayurl">
  `forceLoginGatewayUrl`
</h3>

设置 `/login` Cloud gateway 屏幕连接到的网关 URL，以便人们无需输入地址即可访问您的 [cloud gateway](/docs/zh-CN/claude-apps-gateway)。该屏幕没有 URL 字段：设置此设置项后，它会显示您的网关 URL，并在用户按 Enter 时连接；未设置时，它会告诉用户联系其 IT 管理员。

此设置项或 `forceLoginMethod: "gateway"` 都会使机器仅限网关，但使用 `CLAUDE_CODE_USE_*` 选择云提供商的会话除外。此时 `/login` 会直接打开 Cloud gateway 屏幕，没有登录方法选择器。请参阅[管理员策略需要 Cloud gateway 登录](/docs/zh-CN/errors#administrator-policy-requires-a-cloud-gateway-sign-in)，了解遗留的第一方登录或 API 密钥会发生什么。请同时设置这两个设置项，以便屏幕能够连接而不是显示错误。

* **Scope**: [`Managed`](#scopes)。仅从机器上的源读取：`managed-settings.json`、macOS plist 或 Windows HKLM 注册表或策略辅助程序。Claude Code 在 HKCU 和服务器托管设置中忽略它。
* **Type**: string，包含协议方案的完整 URL
* **Default**: 未设置，因此 Cloud gateway 屏幕显示错误，告诉人们联系其 IT 管理员

```json managed-settings.json theme={null}
{
  "forceLoginGatewayUrl": "https://claude-gateway.example.com"
}
```

如果该值不是有效的 URL，登录屏幕会报告该问题，托管设置文件的其余部分仍然适用。请参阅[设置网关 URL](/docs/zh-CN/claude-apps-gateway#set-the-gateway-url)。

<h3 id="forceloginorguuid">
  `forceLoginOrgUUID`
</h3>

在托管源中，要求 claude.ai 帐户登录属于某一个 Anthropic 组织（以单个 UUID 给出），或属于多个组织中的任意一个（以数组给出）。在任何设置文件中，Claude Code 还会使用单个 UUID 在 claude.ai 或 Claude Console 登录期间预先选择该组织，而对于数组则不预选任何组织。如果您在任何设置文件中设置此设置项，Claude Code 也会在该文件适用的会话中停止提供[无密钥 Console 登录](/docs/zh-CN/authentication#sign-in-without-an-api-key)，并改为创建 API 密钥。

* **Scope**: [`Any file`](#scopes)。仅托管源会强制执行限制；任何其他设置文件中的单个 UUID 只会在登录期间预先选择组织，而不会限制它。
* **Type**: string，一个 UUID，或字符串数组，多个 UUID
* **Default**: 未设置，因此任何组织都可以登录

此示例接受来自两个组织中任意一个的登录，而不预先选择其中之一：

```json managed-settings.json theme={null}
{
  "forceLoginOrgUUID": ["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "yyyyyyyy-yyyy-yyyy-yyyy-yyyyyyyyyyyy"]
}
```

如果托管源设置了空数组或 Claude Code 无法解析的值，Claude Code 会以配置错误消息阻止所有登录。

请参阅[限制登录到您的组织](/docs/zh-CN/authentication#restrict-login-to-your-organization)，了解 Claude Code 如何处理 Claude Console 登录、其他登录路径和环境凭据。

<h3 id="gatewayinternalnetworks">
  `gatewayInternalNetworks`
</h3>

声明您的组织用于为其内部网络编址的公共 IPv4 地址块，以便 `/login` 接受位于其中的 [cloud gateway](/docs/zh-CN/claude-apps-gateway)。需要 Claude Code v2.1.268 或更高版本。

未设置此设置项时，`/login` 只会连接到私有地址上的网关。设置后，`/login` 还会接受位于所列地址块内的网关，但仅限直接连接。该机器在该连接上的自身地址也必须位于同一地址块内。

* **Scope**: [`Managed`](#scopes)。仅从机器上的源读取：`managed-settings.json`、macOS plist 或 Windows HKLM 注册表或策略辅助程序。Claude Code 在 HKCU 和服务器托管设置中忽略它。
* **Type**: 字符串数组，最多四个 IPv4 CIDR 块，每个为 `/8` 到 `/32`，彼此不重叠，且都不与私有地址空间重叠。
* **Default**: 未设置，因此 `/login` 仅接受私有地址上的网关

```json managed-settings.json theme={null}
{
  "gatewayInternalNetworks": ["203.0.113.0/24"]
}
```

请将示例中的文档专用地址范围替换为您自己的地址块。Claude Code 会拒绝文档专用地址范围、VPN 和 NAT64 客户端在本地使用的地址范围，以及不用于任何网络编址的保留地址空间，例如多播。

如果某个条目无效，或该值不是字符串列表，`/login` 会指明问题，并拒绝该机器上的所有新网关登录，直到您修复该值。现有登录继续有效。请参阅[允许网关在您拥有的公共地址空间上](/docs/zh-CN/claude-apps-gateway#allow-a-gateway-on-public-address-space-you-own)，了解完整规则以及开发人员看到的内容。

<h3 id="gcpauthrefresh">
  `gcpAuthRefresh`
</h3>

运行您自己的命令，以在 Claude Code 发现 Google Cloud Application Default Credentials 已过期或无法加载时刷新它们，以便 [Google Cloud 的 Agent Platform](/docs/zh-CN/google-vertex-ai) 请求继续正常工作，而无需您手动重新进行身份验证。

当多个使用相同命令和凭据的 Claude Code 进程（例如不同的终端或 IDE 窗口）同时发现凭据已过期时，由一个进程运行该命令，其余进程等待该次运行，而不是各自启动运行。在有待处理请求的情况下已等待 60 秒的进程会自行运行该命令。要关闭此行为，请将 [`CLAUDE_CODE_DISABLE_AUTH_REFRESH_LOCK`](/docs/zh-CN/env-vars) 设置为 `1`。

* **Scope**: [`Any file`](#scopes)
* **Type**: string，shell 命令行
* **Default**: 未设置，因此 Claude Code 的凭据错误会提示您自行运行 `gcloud auth application-default login`

```json settings.json theme={null}
{
  "gcpAuthRefresh": "gcloud auth application-default login"
}
```

请参阅[高级凭据配置](/docs/zh-CN/google-vertex-ai#advanced-credential-configuration)。

<h3 id="otelheadershelper">
  `otelHeadersHelper`
</h3>

运行您自己的命令以生成 Claude Code 随 OpenTelemetry 导出发送的标头，适用于令牌会轮换的后端。Claude Code 在启动时运行它，之后定期运行，并期望在 stdout 上获得由字符串标头值组成的 JSON 对象。

* **Scope**: [`Any file`](#scopes)
* **Type**: string，可执行文件路径或 shell 命令行
* **Default**: 未设置，因此 Claude Code 不添加辅助程序生成的标头

```json settings.json theme={null}
{
  "otelHeadersHelper": "/bin/generate_otel_headers.sh"
}
```

使用 [`CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS`](/docs/zh-CN/env-vars) 设置刷新间隔。请参阅[动态标头](/docs/zh-CN/monitoring-usage#dynamic-headers)，了解脚本要求以及辅助程序失败时会发生什么。

<h2 id="updates-and-versioning">
  更新和版本控制
</h2>

选择更新渠道，对于组织，可以固定人们可以运行的版本。请参阅[更新 Claude Code](/docs/zh-CN/setup#update-claude-code)。

<h3 id="autoupdateschannel">
  `autoUpdatesChannel`
</h3>

选择[发布渠道](/docs/zh-CN/setup#configure-release-channel)，背景自动更新和 `claude update` 遵循该渠道。设置 `"stable"` 以获得通常约一周前的版本，并跳过有重大回归的发布，或设置 `"latest"` 以获得最新发布。

* **Scope**: [`Any file`](#scopes)。在托管设置中设置以在整个组织中强制执行一个渠道。
* **Type**: string，以下之一：
  * `"latest"`：更新遵循最新发布
  * `"stable"`：更新遵循通常约一周前的版本，并跳过有重大回归的发布
* **Default**: 未设置，所以 Claude Code 遵循 `"latest"`

```json settings.json theme={null}
{
  "autoUpdatesChannel": "stable"
}
```

当您在 `/config` 中的**自动更新渠道**下选择它时，Claude Code 会将 `"stable"` 写入您的用户设置，当您在那里切换回最新版本时会删除该键。`claude install stable` 和 `claude install latest` 也会保存您命名的渠道。在 `/config` 中从 `"latest"` 切换到 `"stable"` 会询问是否允许降级或保持当前版本；保持设置 [`minimumVersion`](#minimumversion)。Homebrew 安装会忽略此键：`claude-code` cask 跟踪稳定版，`claude-code@latest` 跟踪最新版，`claude update` 遵循 `brew upgrade`。要完全关闭自动更新，请在 `env` 中设置 [`DISABLE_AUTOUPDATER`](/docs/zh-CN/setup#disable-auto-updates)。

<h3 id="minimumversion">
  `minimumVersion`
</h3>

防止背景自动更新和 `claude update` 安装低于此版本的任何版本，因此移动到 `"stable"` 渠道不会从较新的 `"latest"` 构建中降级您。当您在 `/config` 中选择在切换渠道时保持当前版本时，Claude Code 会为您写入此键，当您切换回 `"latest"` 时会清除它。

* **Scope**: [`Any file`](#scopes)。在托管设置中设置以固定组织范围的最小值，用户和项目设置无法降低。
* **Type**: string，版本号，例如 `"2.1.100"`；不是有效版本的值会被忽略
* **Default**: 未设置，所以更新可以安装渠道提供的任何版本

此示例遵循稳定渠道，并拒绝安装低于 2.1.100 的任何版本：

```json settings.json theme={null}
{
  "autoUpdatesChannel": "stable",
  "minimumVersion": "2.1.100"
}
```

此键仅约束更新。要使 Claude Code 拒绝在版本以下启动，请改用 [`requiredMinimumVersion`](#requiredminimumversion)。请参阅[固定最小版本](/docs/zh-CN/setup#pin-a-minimum-version)。

<h3 id="requiredmaximumversion">
  `requiredMaximumVersion`
</h3>

设置您的组织允许启动的最新 Claude Code 版本。当运行版本较新时，Claude Code 在启动时退出，并告诉用户通过您组织的批准方法安装批准的版本；`claude install <version>` 也可能有效。需要 Claude Code v2.1.163 或更高版本。

* **Scope**: [`Managed`](#scopes)。Claude Code 在其他地方忽略该键时不会发出警告。
* **Type**: string，版本号，例如 `"2.1.150"`；不是有效版本的值会被忽略
* **Default**: 未设置，所以不适用上限

```json managed-settings.json theme={null}
{
  "requiredMaximumVersion": "2.1.150"
}
```

背景自动更新和 `claude update` 跳过上限以上的版本，因此范围内的安装保持在范围内。`claude update`、`claude install` 和 `claude doctor` 在上限以上继续工作，以便用户可以恢复。将其与 [`requiredMinimumVersion`](#requiredminimumversion) 配对以强制执行范围。

<h3 id="requiredminimumversion">
  `requiredMinimumVersion`
</h3>

设置您的组织允许启动的最旧 Claude Code 版本。当运行版本较旧时，Claude Code 在启动时退出，并告诉用户通过您组织的批准方法进行更新。检查仅在启动时运行，因此已在运行的会话会继续。需要 Claude Code v2.1.163 或更高版本。

* **Scope**: [`Managed`](#scopes)。Claude Code 在其他地方忽略该键时不会发出警告。
* **Type**: string，版本号，例如 `"2.1.150"`；不是有效版本的值会被忽略
* **Default**: 未设置，所以不适用下限

```json managed-settings.json theme={null}
{
  "requiredMinimumVersion": "2.1.150"
}
```

`claude update`、`claude install` 和 `claude doctor` 在下限以下继续工作，以便用户可以恢复。与仅防止降级的 [`minimumVersion`](#minimumversion) 不同，此键会阻止启动。将其与 [`requiredMaximumVersion`](#requiredmaximumversion) 配对以强制执行范围。

<h2 id="tools">
  Tools
</h2>

在 [Claude Code 桌面应用](/docs/zh-CN/desktop) 中关闭特定工具。终端 CLI 会忽略这些密钥。有关工具本身，请参阅 [Claude 可用的工具](/docs/zh-CN/tools-reference)。

<h3 id="browserexternalpagetools">
  `browserExternalPageTools`
</h3>

阻止 Claude 在桌面应用的 [浏览器窗格](/docs/zh-CN/desktop#browse-external-sites) 中使用其工具读取或作用于外部页面。您组织中的人员仍然可以自己打开外部网站，本地开发服务器预览继续与 Claude 的工具一起工作。桌面应用读取此密钥；终端 CLI 会忽略它。

* **Scope**: [`Managed`](#scopes)
* **Type**: string，`"disabled"`；桌面应用也接受 `"disable"`，在任何一种情况下
* **Default**: 未设置，因此 Claude 的工具可在外部页面上工作

```json managed-settings.json theme={null}
{
  "browserExternalPageTools": "disabled"
}
```

任何其他值都会使 Claude 的工具保持打开状态，非空字符串如果不是两个接受的值之一，则会记录警告。要同时阻止人员和 Claude 访问外部网站，请改为设置 [`disableBrowserExternalNavigation`](#disablebrowserexternalnavigation)。请参阅 [为您的组织限制外部浏览](/docs/zh-CN/desktop#restrict-external-browsing-for-your-organization)。

<h3 id="disablebrowserexternalnavigation">
  `disableBrowserExternalNavigation`
</h3>

在桌面应用的 [浏览器窗格](/docs/zh-CN/desktop#browse-external-sites) 中为人员和 Claude 关闭外部浏览。Localhost 开发服务器预览继续工作。桌面应用读取此密钥；终端 CLI 会忽略它。

* **Scope**: [`Managed`](#scopes)
* **Type**: Boolean；仅 JSON Boolean `true` 生效
  * `true`：桌面应用在浏览器窗格中为人员和 Claude 关闭外部浏览；localhost 预览继续工作
  * `false`：外部浏览保持打开
* **Default**: 未设置，因此外部浏览是打开的

```json managed-settings.json theme={null}
{
  "disableBrowserExternalNavigation": true
}
```

桌面应用会忽略任何其他值，非 Boolean 的值（例如字符串 `"true"` 或 `1`）也会记录警告。要保持外部浏览打开但在外部页面上关闭 Claude 的工具，请改为设置 [`browserExternalPageTools`](#browserexternalpagetools)。请参阅 [为您的组织限制外部浏览](/docs/zh-CN/desktop#restrict-external-browsing-for-your-organization)。

<h3 id="disablemobilesimulatortools">
  `disableMobileSimulatorTools`
</h3>

阻止 Claude 的工具用于桌面应用的 [iOS 模拟器窗格](/docs/zh-CN/desktop-ios-simulator#turn-off-simulator-access)。人员保持对窗格的手动使用；仅移除 Claude 的访问权限，任何人都无法从应用内部将其重新打开。桌面应用读取此密钥；终端 CLI 会忽略它。

* **Scope**: [`Managed`](#scopes)
* **Type**: Boolean；仅 JSON Boolean `true` 生效
  * `true`：桌面应用阻止 Claude 的工具用于 iOS 模拟器窗格
  * `false`：Claude 的模拟器工具遵循桌面应用中每个人的设置切换
* **Default**: 未设置，因此 Claude 的模拟器工具遵循桌面应用中每个人的设置切换

```json managed-settings.json theme={null}
{
  "disableMobileSimulatorTools": true
}
```

桌面应用会忽略任何其他值，非 Boolean 的值（例如字符串 `"true"` 或 `1`）也会记录警告。

<span id="data-and-privacy" />

<h2 id="privacy-and-telemetry">
  隐私和遥测
</h2>

控制 Claude Code 保留会话数据的时间以及它发送的内容。关闭使用指标和错误报告的开关是环境变量，而不是设置键：在 [`env`](#env) 键中或在 shell 中设置 `DISABLE_TELEMETRY`、`DISABLE_ERROR_REPORTING` 或 `CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC`。[遥测服务](/docs/zh-CN/data-usage#telemetry-services)说明了每个变量的作用。两个例外可以从设置文件中关闭：下面的 [`feedbackDrafts`](#feedbackdrafts) 用于 Claude 起草的反馈，下面的 [`feedbackSurveyRate`](#feedbacksurveyrate) 用于会话调查。

<h3 id="cleanupperioddays">
  `cleanupPeriodDays`
</h3>

设置 Claude Code 在删除之前保留[会话记录和其他应用程序数据](/docs/zh-CN/claude-directory#cleaned-up-automatically)的天数。Claude Code 在会话开始后作为后台扫描运行删除，只要它能够安全地确定保留期。扫描删除记录时不显示消息，因此您未使用超过保留期的会话不再出现在 [`/resume`](/docs/zh-CN/sessions#resume-a-session) 选择器中。

* **范围**: [`任何文件`](#scopes)
* **类型**: 天数，整数，最小值 `1`
* **默认值**: `30`

```json settings.json theme={null}
{
  "cleanupPeriodDays": 20
}
```

设置 `0` 会导致验证失败，因此请选择一个较大的值，例如 `3650` 以实现长期保留。要停止 Claude Code 完全写入记录，请参阅[纯文本存储](/docs/zh-CN/claude-directory#plaintext-storage)。

<h3 id="desktopsessioncleanupperioddays">
  `desktopSessionCleanupPeriodDays`
</h3>

为您在 Claude Desktop 或 Cowork 中启动或最近继续的会话的会话记录设置天数年龄限制。没有此键，Claude Code [会无限期地保留这些会话记录](/docs/zh-CN/claude-directory#cleaned-up-automatically)。Claude Code 在每个会话记录的年龄超过此限制和 [`cleanupPeriodDays`](#cleanupperioddays) 时删除它，因此当 `cleanupPeriodDays` 处于其默认值 30 时，值 `7` 仍会保留它们 30 天。[自动清理](/docs/zh-CN/claude-directory#cleaned-up-automatically)列出了改为适用 `cleanupPeriodDays` 且 Claude Code 忽略此键的情况。需要 Claude Code v2.1.248 或更高版本。

* **范围**: [`用户或托管`](#scopes)。Claude Code 也从您使用 `--settings` 传递的文件中读取该键，并在项目和本地设置中忽略它。
* **类型**: 天数，整数，最小值 `0`
* **默认值**: `0`，不设置年龄限制

```json settings.json theme={null}
{
  "desktopSessionCleanupPeriodDays": 90
}
```

<h3 id="feedbackdrafts">
  `feedbackDrafts`
</h3>

控制 [Claude 起草的反馈](/docs/zh-CN/tools-reference#sendfeedback-tool-behavior)：Claude 是否可以为您排队反馈草稿以供审查，以及 Claude Code 在 Claude 排队时是否显示卡片。

* **范围**: [`用户或托管`](#scopes)
* **类型**: 字符串，`"notify"`、`"quiet"` 或 `"off"` 之一
  * `"notify"`：当 Claude 排队草稿时，Claude Code 在提示上方显示卡片，默认情况下[一个会话中最多三张卡片](/docs/zh-CN/tools-reference#what-you-see-when-claude-drafts)
  * `"quiet"`：Claude 在没有卡片的情况下起草。您在提示页脚中看到排队草稿的计数，并在 `/feedback` 中审查它们
  * `"off"`：Claude Code 删除 SendFeedback 工具，因此 Claude 无法排队草稿
* **默认值**: `"notify"`
* **每个会话的覆盖**: [`CLAUDE_CODE_SEND_FEEDBACK`](/docs/zh-CN/env-vars) 设置为 `0` 会关闭一个会话的此功能

```json settings.json theme={null}
{
  "feedbackDrafts": "quiet"
}
```

在 `/config` 中显示为**Claude 起草的反馈**，它将此键写入您的用户设置。您只在 Claude 可以起草反馈的[会话中](/docs/zh-CN/tools-reference#sessions-without-claude-drafted-feedback)看到 `/config` 行；设置 `"off"` 不会隐藏它，因此您可以从同一行重新打开此功能。托管设置中的值优先于您的用户设置，因此当管理员设置此键时，该行显示托管值，更改它无效。Claude Code 在项目和本地设置中忽略此键。

<h3 id="feedbacksurveyrate">
  `feedbackSurveyRate`
</h3>

设置[会话质量调查](/docs/zh-CN/data-usage#session-quality-surveys)在会话符合条件时出现的概率。设置 `0` 以防止调查出现。

* **范围**: [`任何文件`](#scopes)
* **类型**: `0` 到 `1` 之间的数字
* **默认值**: 未设置，因此 Claude Code 使用 Anthropic 远程设置的速率，或在 Amazon Bedrock、Google Cloud 的 Agent Platform 和 Microsoft Foundry 上的内置速率 `0.005`，这些不接收远程配置
* **每个会话的覆盖**: [`CLAUDE_CODE_DISABLE_FEEDBACK_SURVEY`](/docs/zh-CN/env-vars) 设置为 `1` 会关闭一个会话的调查，无论此键设置的速率如何

```json settings.json theme={null}
{
  "feedbackSurveyRate": 0.05
}
```

相同的速率适用于 VS Code 扩展中的调查。

<h3 id="skipwebfetchpreflight">
  `skipWebFetchPreflight`
</h3>

跳过 [WebFetch 域安全检查](/docs/zh-CN/data-usage#webfetch-domain-safety-check)，该检查在获取之前将每个请求的主机名发送到 `api.anthropic.com`。在阻止到 Anthropic 的流量的环境中设置 `true`，例如 Amazon Bedrock、Google Cloud 的 Agent Platform 或具有限制性出站的 Microsoft Foundry 部署。

* **范围**: [`任何文件`](#scopes)
* **类型**: 布尔值
  * `true`：Claude Code 跳过 WebFetch 域安全检查
  * `false`：检查在会话中首次获取每个主机名之前运行，以及对于其早期检查被阻止或失败的主机名再次运行
* **默认值**: 未设置，因此检查在会话中首次获取每个主机名之前运行

```json settings.json theme={null}
{
  "skipWebFetchPreflight": true
}
```

跳过检查后，WebFetch 尝试任何 URL 而不查询阻止列表，因此如果您需要限制 Claude 可以访问的域，请将其与 [`WebFetch` 权限规则](/docs/zh-CN/permissions#webfetch)配对。

<span id="managed-policy" />

<h2 id="enterprise-and-managed-settings">
  企业和托管设置
</h2>

组织用来计算、刷新和合并托管设置的密钥。请参阅[设置托管设置](/docs/zh-CN/admin-setup)。

<h3 id="disablesideloadflags">
  `disableSideloadFlags`
</h3>

在启动时拒绝 `--plugin-dir`、`--plugin-url`、`--agents` 和 `--mcp-config` CLI 标志，用户可能会传递这些标志来绕过 [`strictKnownMarketplaces`](#strictknownmarketplaces) 进行单次运行。Claude Code 会以错误退出并命名被拒绝的标志。在[云会话](/docs/zh-CN/claude-code-on-the-web)中，Claude Code 会启动会话并删除服务器通过 `--mcp-config` 传递的每个条目，除了进程内 `type: "sdk"` 条目和 [Claude Tag](/docs/zh-CN/claude-tag) 会话的 Slack 工具。需要 Claude Code v2.1.193 或更高版本。

* **Scope**: [`Managed`](#scopes)
* **Type**: Boolean
  * `true`: Claude Code 在启动时拒绝 `--plugin-dir`、`--plugin-url`、`--agents` 和 `--mcp-config`，并以错误退出并命名它们。在云会话中，它会启动会话并删除服务器通过 `--mcp-config` 传递的每个条目，除了进程内 `type: "sdk"` 条目和 Claude Tag 会话的 Slack 工具
  * `false`: Claude Code 接受这些标志
* **Default**: `false`

```json managed-settings.json theme={null}
{
  "disableSideloadFlags": true
}
```

Claude Code 仍然接受其服务器都是进程内 `type: "sdk"` 条目的 `--mcp-config`，因此 Agent SDK 和 VS Code 扩展继续工作。用户仍然可以使用 `claude mcp add` 或 `.mcp.json` 文件添加服务器；对于按服务器控制，也设置 [`allowedMcpServers`](/docs/zh-CN/managed-mcp)。需要 Claude Code v2.1.193 或更高版本。

相同的检查涵盖在 [`CLAUDE_CODE_PLUGIN_DIRS`](/docs/zh-CN/env-vars#variables) 环境变量中命名的插件文件夹，这需要 Claude Code v2.1.280 或更高版本。当变量命名一个文件夹时，Claude Code 以相同的错误退出，错误说要取消设置该变量。

在云会话中，Claude Code 也忽略服务器传递的中途 MCP 更新，云会话配置和 SDK `setMcpServers()` 调用背后的路径到达这些会话。进程内 `type: "sdk"` 条目和 Claude Tag 会话的 Slack 工具在那里也保持豁免。在 v2.1.268 之前，这个删除和启动删除也删除了 Claude Tag 会话的 Slack 工具。在 v2.1.239 之前，服务器传递的 `--mcp-config` 阻止云会话启动。

桌面应用自己管理一些插件，包括从 claude.ai 同步的插件和您的组织通过应用部署的插件。如果您通过 MDM、OS 级别策略或托管设置文件将此密钥部署到设备，桌面应用不会将这些插件传递给该设备上的以下会话：

* **[用户机器上的代码会话](/docs/zh-CN/desktop#environment-configuration)**: 它们也启动时不启用用户 claude.ai 账户的技能。Claude Code 从您的托管设置中的市场安装的插件仍然加载。在 [Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/overview) 中，您部署到设备 `org-plugins` 目录的插件中的 MCP 服务器仍然可用，因为桌面应用自己连接到它们。在 Claude Desktop v1.37937.0 之前，这些会话在启动时失败。
* **[用户机器上的协作会话](/docs/zh-CN/managed-settings#where-and-when-a-policy-applies)**: 这些插件内的技能和为用户 claude.ai 账户启用的技能保持可用。在 [Claude Desktop on 3P](https://claude.com/docs/third-party/claude-desktop/overview) 中，您部署到设备 `org-plugins` 目录的插件中的 MCP 服务器仍然可用，因为桌面应用自己连接到它们。在 Claude Desktop v1.44121.0 之前，这些会话在启动时失败。

<h3 id="forceremotesettingsrefresh">
  `forceRemoteSettingsRefresh`
</h3>

阻止 CLI 启动，直到 Claude Code 已经新鲜获取[服务器管理的设置](/docs/zh-CN/server-managed-settings)。如果获取失败，Claude Code 会退出而不是继续使用缓存或无设置。当您的环境无法接受即使是短暂的窗口（在该窗口中会话运行而没有其托管策略）时，设置它。

当密钥未设置时，Claude Code 不会在获取时阻止启动，尽管当开发人员在启动时登录时，它会等待最多五秒钟以进行获取。Cloud 网关会话总是等待，如果无法到达网关则退出。

* **Scope**: [`Managed`](#scopes)。Claude Code 从任何管理员控制的托管源（即使不是最高优先级源）中接受 `true`。
* **Type**: Boolean
  * `true`: Claude Code 阻止启动，直到它已经新鲜获取服务器管理的设置，如果获取失败则退出
  * `false`: Claude Code 不会在获取时阻止启动，尽管在登录启动时它会等待最多五秒钟以进行获取
* **Default**: `false`

```json managed-settings.json theme={null}
{
  "forceRemoteSettingsRefresh": true
}
```

在 MDM 配置文件或托管设置文件中设置它以在第一个服务器有效负载到达之前强制执行故障关闭启动。Claude Code 仅在获取服务器管理的设置的会话中应用检查，因此[不获取它们](/docs/zh-CN/server-managed-settings#platform-availability)的会话启动时不会等待。`claude auth` 子命令是豁免的，因此用户可以在过期凭证是获取失败原因时重新身份验证。请参阅[强制执行故障关闭启动](/docs/zh-CN/server-managed-settings#enforce-fail-closed-startup)。

<h3 id="managedsourcesbehavior">
  `managedSourcesBehavior`
</h3>

选择 Claude Code 是仅应用您的组织提供的最高优先级[托管源](/docs/zh-CN/managed-settings#how-claude-code-combines-managed-sources)，还是合并它提供的每个管理员源。默认情况下，Claude Code 采用携带[策略密钥](/docs/zh-CN/managed-settings#how-claude-code-combines-managed-sources)的最高优先级源并忽略其余的。策略密钥是除了这个和 `wslInheritsWindowsSettings` 之外的任何设置密钥。在该默认值下，一旦服务器管理的设置或 MDM 策略传递策略密钥，`managed-settings.json` 文件仅贡献 [Claude Code 从每个管理员源读取的密钥](/docs/zh-CN/managed-settings#keys-read-from-every-admin-source)。使用 `"merge"`，您提供的每个管理员源都将其密钥贡献给一个合并的策略。需要 Claude Code v2.1.242 或更高版本。

仅在您[排名](/docs/zh-CN/managed-settings#how-claude-code-combines-managed-sources)低于最高优先级的每个源都在管理员的控制下时设置 `"merge"`，因为 Claude Code 然后从较低源（例如 `permissions.allow` 规则）添加条目到策略。

* **Scope**: [`Managed`](#scopes)。Claude Code 从携带此密钥或策略密钥的最高优先级源读取此密钥，并忽略排名较低的每个源中的此密钥，因此较低源无法选择自己合并到上面的源。Windows HKCU 注册表和[来自嵌入主机的父设置](/docs/zh-CN/managed-settings#let-an-embedding-host-add-policy)都不参与合并。
* **Type**: string, one of:
  * `"first-wins"`: 携带策略密钥的最高优先级源提供策略，较低源仅贡献 [Claude Code 从每个管理员源读取的密钥](/docs/zh-CN/managed-settings#keys-read-from-every-admin-source)
  * `"merge"`: 您提供的每个管理员源都贡献其密钥，按以下规则合并
* **Default**: `"first-wins"`

在您部署的最高优先级源中传递密钥。从不接收服务器管理的设置的机器也需要在其 MDM 配置文件中使用该密钥，因为 Claude Code 从携带它或策略密钥的最高优先级源读取该密钥。`managed-settings.json` 文件是最低排名的管理员源，因此在那里设置的 `"merge"` 没有下面的源来合并。在服务器管理的设置中，密钥看起来像这样：

```json theme={null}
{
  "managedSourcesBehavior": "merge"
}
```

在 `"merge"` 下，Claude Code 按其类型合并每个密钥。此表给出每种类型的规则。限制允许列表、整体取值和仅最高源行命名它们覆盖的每个密钥，其他行给出示例：

| 密钥类型 | Claude Code 如何合并它 | 密钥 |
| :- | :- | :- |
| Lists | 合并来自每个源的条目 | [`permissions.allow`](#permissions-allow)、[`sandbox.network.allowedDomains`](#sandbox-network-alloweddomains) 和其他列表密钥 |
| Locks | 应用任何源设置的最严格值。当没有源设置严格值时，仅从最高源应用较宽松的值 | [`allowManagedPermissionRulesOnly`](#allowmanagedpermissionrulesonly)、[`permissions.disableBypassPermissionsMode`](#permissions-disablebypasspermissionsmode) 和其他布尔值或枚举锁 |
| Restriction allowlists | 从设置它的最高源整体取值，不从较低源添加条目。当最高源未设置时，从下一个较低源整体取值 | [`availableModels`](#availablemodels)、[`allowedMcpServers`](#allowedmcpservers)、[`allowedProviders`](#allowedproviders)、[`strictKnownMarketplaces`](#strictknownmarketplaces)、[`allowedChannelPlugins`](#allowedchannelplugins) 和 [`fallbackModel`](#fallbackmodel) 链 |
| Values taken whole | 从设置它的最高源整体取值，不合并来自较低源的条目或字段。当最高源未设置时，从下一个较低源整体取值 | [`sandbox.credentials.awsPairs`](#sandbox-credentials-awspairs)、[`sandbox.ripgrep`](#sandbox-ripgrep) |
| Provided MCP servers | 合并来自每个源的服务器名称。当两个源设置相同名称时，应用较高源的整个条目 | [`managedMcpServers`](#managedmcpservers) |
| Read from the highest-priority source only | 仅从携带策略密钥的最高优先级源读取密钥，因此即使最高源未设置任何值，较低源的值也会被忽略 | [`apiKeyHelper`](#apikeyhelper)、[`awsAuthRefresh`](#awsauthrefresh)、[`awsCredentialExport`](#awscredentialexport)、[`gcpAuthRefresh`](#gcpauthrefresh)、[`otelHeadersHelper`](#otelheadershelper)、`proxyAuthHelper`、[`forceLoginOrgUUID`](#forceloginorguuid)、[`forceLoginMethod`](#forceloginmethod) 的 `"claudeai"` 和 `"console"` 值、[`parentSettingsBehavior`](#parentsettingsbehavior)、[`modelPicker`](#modelpicker)、[`policyHelper`](#policyhelper)、[`permissions.defaultMode`](#permissions-defaultmode) |
| `env` | [在管理员源之间按变量合并](/docs/zh-CN/managed-settings#keys-read-from-every-admin-source)，在 `"first-wins"` 和 `"merge"` 下都是 | [`env`](#env) |
| Every other key | 从设置它的最高源取值 | [`cleanupPeriodDays`](#cleanupperioddays)、[`model`](#model) |

整体取值 `sandbox.credentials.awsPairs` 和 `sandbox.ripgrep` 需要 Claude Code v2.1.257 或更高版本。

一些密钥添加了表格不显示的条件：

* **[`policyHelper`](#policyhelper)**: Claude Code 仅在携带策略密钥的最高源是 MDM 策略或托管设置文件时才接受它，因此在服务器管理的设置下它不适用。
* **[`modelOverrides`](#modeloverrides)**: 与 `availableModels` 配对。Claude Code 从设置它的最高源取值 `modelOverrides`，除非较高源设置 `availableModels` 而不设置 `modelOverrides`。在这种情况下，它忽略来自每个源的 `modelOverrides`。
* **[`forceLoginGatewayUrl`](#forcelogingatewayurl)、[`gatewayInternalNetworks`](#gatewayinternalnetworks) 和 [`forceLoginMethod`](#forceloginmethod) 的 `"gateway"` 值**: Claude Code 从不从服务器管理的设置读取它们中的任何一个，因此那里的值既不适用也不隐藏在 MDM 策略或托管设置文件中设置的值。在机器上的管理员源中，仅携带策略密钥的最高排名源提供它们，无论是否也存在服务器管理的设置。
* **[`allowedProviders`](#allowedproviders)**: 在表格的规则之后，机器自己的列表仍然限制结果，如其条目的 Scope 注释所述。

要确认机器上合并了哪些源，请运行 `/status` 并[读取 `Setting sources` 行](/docs/zh-CN/managed-settings#read-the-source-in-/status)。

<h3 id="parentsettingsbehavior">
  `parentSettingsBehavior`
</h3>

选择 Claude Code 是否应用由嵌入主机进程（例如 Agent SDK 或 IDE 扩展）提供的托管设置，当管理员部署的托管层也存在时。使用 `"first-wins"`，Claude Code 删除主机提供的设置；使用 `"merge"`，它通过限制性过滤器在管理员层下应用它们。当主机需要将其自己的限制传递给它启动的会话时，设置 `"merge"`，例如 Claude Desktop 传递网关的出口允许列表。

* **Scope**: [`Managed`](#scopes)。Claude Code 从最高优先级管理员控制的托管源读取它。
* **Type**: string, one of:
  * `"first-wins"`: 当管理员部署的托管层存在时，Claude Code 删除主机提供的设置
  * `"merge"`: Claude Code 通过限制性过滤器在管理员层下应用主机提供的设置
* **Default**: `"first-wins"`

```json managed-settings.json theme={null}
{
  "parentSettingsBehavior": "merge"
}
```

当不存在管理员部署的托管层时，此密钥无效：主机的设置然后应用为唯一的托管层，仍然被过滤为限制性值。对于过滤器的限制以及托管源如何交互，请参阅[来自嵌入主机的父设置](/docs/zh-CN/managed-settings#parent-settings-from-embedding-hosts)和[限制父设置](/docs/zh-CN/claude-apps-gateway#restrict-parent-settings)。

<span id="compute-managed-settings-with-a-policy-helper" />

<h3 id="policyhelper">
  `policyHelper`
</h3>

运行您部署的可执行文件，在启动时计算托管设置，以便您可以从设备状态、身份或远程服务而不是静态文件派生策略。Claude Code 在接受第一个提示之前运行帮助程序，并将其发出的设置视为会话的托管设置。

* **Scope**: [`Managed`](#scopes)。从 macOS plist、Windows HKLM 注册表或托管设置文件读取。Claude Code 从携带[策略密钥](/docs/zh-CN/managed-settings#how-claude-code-combines-managed-sources)的最高优先级托管源读取密钥，仅当该源是这三个之一时才运行帮助程序；它忽略服务器管理的设置、HKCU 注册表和主机提供的父设置中的密钥。
* **Type**: object with `path`, `timeoutMs`, and `refreshIntervalMs`
* **Default**: unset, so no helper runs

当服务器管理的设置在启动时传递策略时，它们优先于帮助程序的源，帮助程序不运行。

如果稍后的设置获取报告服务器管理的设置已删除，Claude Code 在该点运行帮助程序，而不是等待下一次启动。其输出管理会话的其余部分，失败的运行以与[失败的启动运行](#helper-failures)相同的消息结束会话。

此示例以 5 秒超时运行帮助程序，并每五分钟重新运行一次：

```json managed-settings.json theme={null}
{
  "policyHelper": {
    "path": "/usr/local/bin/claude-policy",
    "timeoutMs": 5000,
    "refreshIntervalMs": 300000
  }
}
```

<h4 id="write-the-helper-output">
  Write the helper output
</h4>

Claude Code 不带参数运行帮助程序，在其环境中设置 `CLAUDE_CODE_VERSION`，并从 stdout 读取 JSON 信封，上限为 1 MiB。

将设置放在 `managedSettings` 密钥下。没有 `managedSettings` 密钥的裸设置对象解析为 `managedSettings` 未定义且不应用任何内容，Claude Code 也不报告错误：

```json theme={null}
{
  "managedSettings": {
    "permissions": { "deny": ["Read(//etc/secrets/**)"] }
  }
}
```

当帮助程序发出 `managedSettings` 时，该对象成为运行的唯一托管设置源：Claude Code 忽略 MDM、文件和 HKCU 源，仅从帮助程序的输出读取[跨源密钥](/docs/zh-CN/managed-settings#keys-read-from-every-admin-source)，并从不合并[父设置](/docs/zh-CN/managed-settings#parent-settings-from-embedding-hosts)。

启动 `forceRemoteSettingsRefresh` 检查在帮助程序之前运行并读取任何管理员源。以 0 退出且信封省略 `managedSettings` 的帮助程序不贡献托管设置，其他源照常应用。

<h4 id="helper-failures">
  Helper failures
</h4>

帮助程序运行失败时：

* `path` 违反 [`policyHelper.path`](#policyhelper-path) 中的规则。
* `path` 处没有常规文件。Claude Code 在启动帮助程序之前检查文件，在相同的 `timeoutMs` 预算内，因此无响应的网络挂载可能导致运行失败。
* 帮助程序以非零退出、在 `timeoutMs` 经过时仍在运行，或根本不启动，例如因为它不可执行。
* 帮助程序向 stdout 或 stderr 写入超过 1 MiB。
* stdout 不是单个 JSON 对象，或其 `managedSettings` 有 [Claude Code 无法修复的架构违规](/docs/zh-CN/managed-settings#find-entries-claude-code-dropped)。

当启动运行失败时，Claude Code 打印原因并拒绝启动。非零退出后，原因包括帮助程序的 stderr，或当 stderr 为空时的 stdout。超时后，原因命名 `timeoutMs` 限制，不包括帮助程序的任何输出。拒绝涵盖交互式会话、`claude -p`、Agent SDK 会话、[后台会话](/docs/zh-CN/agent-view) 和大多数子命令。

拒绝是故意的，因此需要中断恢复能力的帮助程序应该从其自己的缓存提供并以 0 退出。

当后台刷新失败时，Claude Code 保持最后成功的策略有效，`/status` 显示失败的刷新及其原因，直到刷新成功。每次刷新在与启动运行相同的 `timeoutMs` 和失败规则下运行。

使用 `--debug`，Claude Code 将每次运行的帮助程序的 stderr 写入[调试日志](/docs/zh-CN/debug-your-config)。

Claude Code 将无效的 `policyHelper` 值报告为[删除的条目](/docs/zh-CN/managed-settings#find-entries-claude-code-dropped)，并在剩余的托管设置上启动会话而不运行帮助程序。无效值包括裸路径字符串和低于[其最小值](#policyhelper-timeoutms)的 `timeoutMs`。

要关闭帮助程序，请从设置它的源中删除密钥。

<h3 id="policyhelper-path">
  `policyHelper.path`
</h3>

命名 Claude Code 运行的帮助程序可执行文件。有关路径违反以下规则时发生的情况，请参阅[帮助程序失败](#helper-failures)。

* **Scope**: [`Managed`](#scopes)。从 macOS plist、Windows HKLM 注册表或托管设置文件读取，无论 [`policyHelper`](#policyhelper) 在哪里读取。
* **Type**: string, an absolute path in normalized form, without `.` or `..` segments; on Windows, a drive-letter or UNC path that ends in `.exe`
* **Default**: none; required when `policyHelper` is set

```json managed-settings.json theme={null}
{
  "policyHelper": {
    "path": "/usr/local/bin/claude-policy"
  }
}
```

<h3 id="policyhelper-timeoutms">
  `policyHelper.timeoutMs`
</h3>

设置 Claude Code 在将运行视为失败之前等待帮助程序的时间。超时的运行失败方式与非零退出相同，因此在启动时 Claude Code 拒绝启动。

* **Scope**: [`Managed`](#scopes)。从 macOS plist、Windows HKLM 注册表或托管设置文件读取，无论 [`policyHelper`](#policyhelper) 在哪里读取。
* **Type**: integer, milliseconds, minimum `1000`
* **Default**: `10000`

```json managed-settings.json theme={null}
{
  "policyHelper": {
    "path": "/usr/local/bin/claude-policy",
    "timeoutMs": 5000
  }
}
```

<h3 id="policyhelper-refreshintervalms">
  `policyHelper.refreshIntervalMs`
</h3>

让 Claude Code 在后台按间隔重新运行帮助程序，以便策略更改到达运行中的会话。当刷新成功时，其输出替换之前的托管设置而不重启；当刷新失败时，Claude Code 保持它已有的策略。

* **Scope**: [`Managed`](#scopes)。从 macOS plist、Windows HKLM 注册表或托管设置文件读取，无论 [`policyHelper`](#policyhelper) 在哪里读取。
* **Type**: integer, milliseconds: `0` to disable refresh, otherwise at least `60000`
* **Default**: unset, so Claude Code runs the helper once at startup

此示例每五分钟重新运行帮助程序：

```json managed-settings.json theme={null}
{
  "policyHelper": {
    "path": "/usr/local/bin/claude-policy",
    "refreshIntervalMs": 300000
  }
}
```

<h3 id="wslinheritswindowssettings">
  `wslInheritsWindowsSettings`
</h3>

让 WSL 上的 Claude Code 从 Windows 策略链读取托管设置，HKLM 和 Windows 托管设置文件优先于下面的 `/etc/claude-code` 和 HKCU。当链打开时，Claude Code 仅在 [HKLM 注册表值或 `C:\Program Files\ClaudeCode\` 文件夹中不存在 Windows 管理员文档](/docs/zh-CN/managed-settings#present-admin-documents)时才读取 `/etc/claude-code`。设置它以将您已在 Windows 上部署的策略扩展到同一机器上的 WSL 会话，以便它们遵循与主机会话相同的规则。Claude Code 仅在 HKLM 注册表密钥或托管设置文件或 `C:\Program Files\ClaudeCode\` 下的放入中设置时才接受它，两者都需要 Windows 管理员才能写入。

* **Scope**: [`Managed`](#scopes)。在管理员控制的 Windows 源中。
* **Type**: Boolean
  * `true`: WSL 上的 Claude Code 从 Windows 策略链读取托管设置，仅在不存在 Windows 管理员文档时读取 `/etc/claude-code`
  * `false`: WSL 仅读取 `/etc/claude-code`
* **Default**: `false`, so WSL reads only `/etc/claude-code`

```json managed-settings.json theme={null}
{
  "wslInheritsWindowsSettings": true
}
```

一旦管理员源打开链，HKCU 策略仅在 HKCU 也将密钥设置为 `true` 时才加入 WSL 上的链。该副本不会自行打开链。仅包含此密钥的 Windows 源（设置为 `true` 或 `false`）不计为策略源，因此较低优先级源仍然提供策略。此密钥对本机 Windows 无效。

Claude Code 读取带或不带引号的 `true` 和 `false`，并将 `null` 读取为删除密钥。包含任何其他值的管理员控制的 Windows 源计为[存在的管理员文档](/docs/zh-CN/managed-settings#present-admin-documents)，链打开：既不应用 `/etc/claude-code` 也不应用 HKCU，启动警告命名密钥。无法读取的 HKLM 值或 Windows 文件夹文件也会阻止 `/etc/claude-code` 应用，无论链是否打开。需要 Claude Code v2.1.282 或更高版本。

<h2 id="global-config-settings">
  全局配置设置
</h2>

将这些键保存在 `~/.claude.json` 中，而不是在设置文件中。Claude Code 在其他任何地方都会忽略它们。Claude Code 和 `/config` 会为你写入大部分设置，你也可以手动编辑它们。

<h3 id="autoconnectide">
  `autoConnectIde`
</h3>

当你从外部终端启动 Claude Code 时，自动连接到正在运行的 IDE。当你在 VS Code 或 JetBrains 终端外运行 Claude Code 时，在 `/config` 中显示为**自动连接到 IDE（外部终端）**。

* **作用域**: [`全局配置`](#scopes)
* **类型**: 布尔值
  * `true`: 当你从外部终端启动 Claude Code 时，它会自动连接到正在运行的 IDE
  * `false`: Claude Code 不会从外部终端自动连接；在 VS Code 或 JetBrains 终端内，或使用 `--ide`，它仍然会连接
* **默认值**: `false`
* **每个会话的覆盖**: [`CLAUDE_CODE_AUTO_CONNECT_IDE`](/docs/zh-CN/env-vars) 在任一方向上优先于此键，持续一个会话

```json ~/.claude.json theme={null}
{
  "autoConnectIde": true
}
```

Claude Code 在 `settings.json` 中忽略此键。

<h3 id="autoinstallideextension">
  `autoInstallIdeExtension`
</h3>

当你从 VS Code 终端运行 Claude Code 时，自动安装 Claude Code IDE 扩展。当你在 VS Code 或 JetBrains 终端内运行 Claude Code 时，在 `/config` 中显示为**自动安装 IDE 扩展**。

* **作用域**: [`全局配置`](#scopes)
* **类型**: 布尔值
  * `true`: 当你从 VS Code 终端运行 Claude Code 时，它会自动安装 IDE 扩展
  * `false`: Claude Code 不会自动安装扩展
* **默认值**: `true`
* **每个会话的覆盖**: [`CLAUDE_CODE_IDE_SKIP_AUTO_INSTALL`](/docs/zh-CN/env-vars) 设置为 `1` 会跳过安装一个会话，即使此键为 `true`

```json ~/.claude.json theme={null}
{
  "autoInstallIdeExtension": false
}
```

Claude Code 在 `settings.json` 中忽略此键。

<h3 id="claudeinchromedefaultenabled">
  `claudeInChromeDefaultEnabled`
</h3>

启动每个交互式 CLI 会话时默认打开 [Chrome 集成](/docs/zh-CN/chrome)，无需每次都传递 `--chrome`。如果您运行 [`claude remote-control`](/docs/zh-CN/remote-control)，它为您的某个[项目](/docs/zh-CN/claude-projects)线程启动的会话也遵循此键，但 `bypassPermissions` 模式除外。在 Claude Code v2.1.287 或更高版本中，此键也适用于 [VS Code 扩展](/docs/zh-CN/vs-code#automate-browser-tasks-with-chrome)中的会话：请参阅[默认启用 Chrome](/docs/zh-CN/chrome#enable-chrome-by-default)。

运行 `/chrome` 并选择**默认启用**会为您设置此键。在 `/config` 中显示为**默认启用 Chrome 中的 Claude**。

* **作用域**: [`全局配置`](#scopes)
* **类型**: 布尔值
  * `true`: 当交互式 CLI 会话启动时，Claude Code 打开 Chrome 集成，就像传递 `--chrome` 时一样。在 VS Code 扩展中，会话在启动时连接到浏览器
  * `false`: 交互式 CLI 会话启动时 Chrome 集成关闭，Claude Code 不再[提议进行设置](/docs/zh-CN/chrome#install-the-extension-when-claude-asks)。传递 `--chrome` 可为单个交互式会话打开它。在 VS Code 扩展中，会话在您输入 `@browser` 时连接，与未设置此键时相同
* **默认值**: 未设置，因此 Chrome 集成关闭，Claude Code 仍然可以提供设置它
* **每个会话的覆盖**: `--chrome` 和 [`--no-chrome`](/docs/zh-CN/cli-reference) 在一个交互式会话中优先于此键

```json ~/.claude.json theme={null}
{
  "claudeInChromeDefaultEnabled": true
}
```

Claude Code 在 `settings.json` 中忽略此键。

<h3 id="copyfullresponse">
  `copyFullResponse`
</h3>

使 [`/copy`](/docs/zh-CN/commands) 每次都复制完整响应，而不显示当响应包含代码块时通常显示的选择器。在该选择器中选择**始终复制完整响应**会将此键设置为 `true`。在 `/config` 中显示为**跳过 /copy 选择器**。

* **作用域**: [`全局配置`](#scopes)
* **类型**: 布尔值
  * `true`: `/copy` 复制完整响应而不显示选择器
  * `false`: 当响应包含代码块时，`/copy` 显示一个选择器，你可以在其中选择一个代码块或完整响应
* **默认值**: `false`

```json ~/.claude.json theme={null}
{
  "copyFullResponse": true
}
```

Claude Code 在 `settings.json` 中忽略此键。

<h3 id="copyonselect">
  `copyOnSelect`
</h3>

当你在[全屏渲染](/docs/zh-CN/fullscreen#use-the-mouse)或[代理视图](/docs/zh-CN/agent-view)中用鼠标完成文本选择时，自动将文本复制到剪贴板。在全屏渲染打开时，在 `/config` 中显示为**选择时复制**。

* **作用域**: [`全局配置`](#scopes)
* **类型**: 布尔值
  * `true`: 当你完成文本选择时，Claude Code 会将文本复制到剪贴板
  * `false`: 选择文本不会改变你的剪贴板，你[用键盘快捷键复制选择](/docs/zh-CN/fullscreen#use-the-mouse)
* **默认值**: `true`

```json ~/.claude.json theme={null}
{
  "copyOnSelect": false
}
```

Claude Code 在 `settings.json` 中忽略此键。

<h3 id="defaulttoagentsview">
  `defaultToAgentsView`
</h3>

当你运行不带参数的 `claude` 时，打开[代理视图](/docs/zh-CN/agent-view)而不是新对话。在 `/config` 中显示为**默认打开代理视图**，除非代理视图被[关闭](#disableagentview)。

* **作用域**: [`全局配置`](#scopes)
* **类型**: 布尔值
  * `true`: 不带参数的 `claude` 打开代理视图，除非代理视图被[关闭](#disableagentview)
  * `false`: 不带参数的 `claude` 启动新对话
* **默认值**: `false`

```json ~/.claude.json theme={null}
{
  "defaultToAgentsView": true
}
```

Claude Code 在 `settings.json` 中忽略此键。

<h3 id="difftool">
  `diffTool`
</h3>

选择 Claude Code 在连接[VS Code](/docs/zh-CN/vs-code)或[JetBrains](/docs/zh-CN/jetbrains#features) IDE 时显示其提议的 `Edit` 或 `Write` 更改的 diff 的位置：`"auto"` 在 IDE 的 diff 查看器中打开它，`"terminal"` 将其保留在终端中。仅当 Claude Code 连接到 VS Code 或 JetBrains IDE 时，在 `/config` 中显示为**Diff 工具**。

* **作用域**: [`全局配置`](#scopes)
* **类型**: 字符串，以下之一：
  * `"auto"`: 当连接到 VS Code 或 JetBrains IDE 时，Claude Code 在 IDE 的 diff 查看器中打开 diff
  * `"terminal"`: Claude Code 将 diff 保留在终端中
* **默认值**: `"auto"`

```json ~/.claude.json theme={null}
{
  "diffTool": "terminal"
}
```

Claude Code 在 `settings.json` 中忽略此键。

<h3 id="externaleditorcontext">
  `externalEditorContext`
</h3>

当你按 `Ctrl+G` 时，Claude Code 在你的[外部编辑器](/docs/zh-CN/interactive-mode#general-controls)中打开你正在输入的提示。启用此键后，编辑器缓冲区以 Claude 的上一个响应作为 `#` 注释行开始，因此你可以在写入时读取它，Claude Code 在你保存时删除这些行。在 `/config` 中显示为**在外部编辑器中显示最后响应**。

* **作用域**: [`全局配置`](#scopes)
* **类型**: 布尔值
  * `true`: 编辑器缓冲区以 Claude 的上一个响应作为 `#` 注释行开始，Claude Code 在保存时删除这些行
  * `false`: 编辑器缓冲区仅以你的提示打开
* **默认值**: `false`

```json ~/.claude.json theme={null}
{
  "externalEditorContext": true
}
```

启用后，Claude Code 打开的缓冲区如下所示，只有标记行下方的文本才会作为你的提示发送：

```text theme={null}
# ─── Claude's last response (for reference; removed on save) ───
# I added the retry loop to fetchUser in src/api.ts and a test
# for the timeout case. Want me to wire the same retry into
# fetchOrders?
# ─── Write your reply below this line ──────────────────────────

Yes, and cap it at three attempts.
```

Claude Code 保留响应的最后 50 行，并用 `# … (earlier output truncated)` 标记截断。

Claude Code 在 `settings.json` 中忽略此键。

<h3 id="leftarrowopensagents">
  `leftArrowOpensAgents`
</h3>

在空提示上按 `←` 以[后台会话并打开代理视图](/docs/zh-CN/agent-view#switch-sessions-without-leaving-the-terminal)。将此键设置为 `false` 以关闭快捷键。当代理视图可用时，在 `/config` 中显示为\*\*← 打开代理\*\*。

* **作用域**: [`全局配置`](#scopes)
* **类型**: 布尔值
  * `true`: 在你在终端中启动的会话中的空提示上按 `←` 会后台该会话并打开代理视图
  * `false`: Claude Code 关闭快捷键；在你[从代理视图附加到的会话](/docs/zh-CN/agent-view#attach-to-a-session)中，空提示上的 `←` 仍然会分离
* **默认值**: `true`

```json ~/.claude.json theme={null}
{
  "leftArrowOpensAgents": false
}
```

Claude Code 在 `settings.json` 中忽略此键。

<h3 id="permissionexplainerenabled">
  `permissionExplainerEnabled`
</h3>

<Warning>
  在 v2.1.257 中删除，以及 Bash 和 PowerShell 权限提示上的 `Ctrl+E` 命令说明。在当前版本中设置它没有效果。
</Warning>

在 v2.1.256 及更早版本中，你可以在 Bash 或 PowerShell 权限提示上按 `Ctrl+E` 查看模型生成的命令说明，并将此键设置为 `false` 以关闭该快捷键。

* **作用域**: [`全局配置`](#scopes)。在 v2.1.256 及更早版本上。
* **类型**: 布尔值
* **默认值**: `true`

<h3 id="prstatusfooterenabled">
  `prStatusFooterEnabled`
</h3>

在提示页脚中显示当前分支的开放拉取请求或合并请求的徽章，带有显示其[状态](/docs/zh-CN/interactive-mode#pr-review-status)的彩色下划线。在 `/config` 中显示为**显示 PR 状态页脚**。

* **作用域**: [`全局配置`](#scopes)
* **类型**: 布尔值
  * `true`: 页脚在[PR 审查状态](/docs/zh-CN/interactive-mode#pr-review-status)中的条件下显示徽章
  * `false`: Claude Code 跳过页脚的拉取请求和合并请求检查，不显示该徽章。你[从代理视图附加到的会话](/docs/zh-CN/agent-view#attach-to-a-session)仍然可以显示指向[链接到它的](/docs/zh-CN/agent-view#pull-request-status)拉取请求的纯链接
* **默认值**: `true`

```json ~/.claude.json theme={null}
{
  "prStatusFooterEnabled": false
}
```

Claude Code 在 `settings.json` 中忽略此键。

<h3 id="teammatedefaultmodel">
  `teammateDefaultModel`
</h3>

<Warning>
  在 v2.1.234 中删除，以及其 `/config` 行**默认队友模型**。在当前版本中设置它没有效果。
</Warning>

在 v2.1.233 及更早版本中，你将此键设置为[代理团队](/docs/zh-CN/agent-teams#specify-teammates-and-models)队友的模型，你的提示没有为其命名模型：一个别名如 `"sonnet"`，或 `null` 以遵循主导的模型。有关 Claude Code 现在为此类队友选择的模型，请参阅[指定队友和模型](/docs/zh-CN/agent-teams#specify-teammates-and-models)。

* **作用域**: [`全局配置`](#scopes)。在 v2.1.233 及更早版本上。
* **类型**: 字符串，模型别名或完整模型 ID，或 `null`
* **默认值**: 未设置

<h2 id="see-also">
  另请参阅
</h2>

* [配置权限](/docs/zh-CN/permissions)：规则语法、权限模式和工作区信任
* [环境变量](/docs/zh-CN/env-vars)：Claude Code 读取的每个 `CLAUDE_*`、`ANTHROPIC_*` 和提供商变量
* [Claude 可用的工具](/docs/zh-CN/tools-reference)：内置工具以及哪些需要批准
* [示例设置文件](/docs/zh-CN/settings-example)：个人文件、团队文件和组织的托管文件
* [设置托管设置](/docs/zh-CN/admin-setup)：组织如何决定要强制执行的内容
* [部署托管设置](/docs/zh-CN/managed-settings)：交付机制、托管层内的优先级和托管设置中的无效条目
* [调试您的配置](/docs/zh-CN/debug-your-config)：`claude doctor` 和设置错误对话框
