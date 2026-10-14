#!/usr/bin/env python3
"""Generate README.md / index.html / data.json from https://51cgw9.cc/wp-json/nav/v1/export"""
import json, sys, html, urllib.request, datetime, collections
MODE = sys.argv[1] if len(sys.argv) > 1 else 'main'
SRC = 'https://51cgw9.cc/wp-json/nav/v1/export'
def U(u, c): return u + ('&' if '?' in u else '?') + 'utm_source=github&utm_campaign=' + c
d = json.load(urllib.request.urlopen(urllib.request.Request(SRC, headers={'User-Agent': '51nav-github-sync'}), timeout=60))
S, T = d['sites'], d['topics']
today = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d')
ACC = {'cn': '🇨🇳 直连', 'vpn': '🌐 需代理'}; PRI = {'free': '🆓 免费', 'freemium': '💡 免费+付费', 'paid': '💰 付费'}
def tags(s): return ' '.join(x for x in [ACC.get(s['access'], ''), PRI.get(s['price'], ''), '📱 需海外手机号' if s.get('phone') == 'yes' else ''] if x)
def names(s): return [c['name'] for c in s['cats']]
def row(s, c): return f"| [{s['title']}]({U(s['page'], c)}) | {s['desc'][:70].replace('|', '/')}{'…' if len(s['desc'])>70 else ''} | {tags(s) or '—'} |"
def table(lst, c): return '\n'.join(['| 工具 | 简介 | 标签 |', '|---|---|---|'] + [row(s, c) for s in lst])
NAV = ("🔥 [今日热榜](https://51cgw9.cc/hot/?utm_source=github) · 🔁 [AI 替代品](https://51cgw9.cc/alternatives/?utm_source=github) · "
       "🚫 [Claude 替代品](https://51cgw9.cc/alternatives/claude/?utm_source=github) · ➕ [提交网站](https://51cgw9.cc/submit/?utm_source=github)")
FOOT = f"\n---\n\n数据由 [51发现导航](https://51cgw9.cc/?utm_source=github) 提供，最近同步：{today}。发现失效或想推荐工具？欢迎提 [Issue](../../issues) 或在 [51cgw9.cc/submit](https://51cgw9.cc/submit/?utm_source=github) 提交。\n\n许可：[CC0 1.0](LICENSE)\n"
def topics(keys): return [t for t in T if any(k in t['url'] for k in keys)]
def tlist(ts, c): return '\n'.join(f"- [{t['title']}]({U(t['url'], c)})" for t in ts)
CFG = {
 'claude-alternatives-cn': dict(title='Claude 替代品 · Claude 封号后怎么办', c='claude-alt',
   intro='Claude 账号被封、地区受限或额度用完时可以换用的 AI 对话 / 编程助手，以及封号原因与申诉要点。',
   f=lambda s: any(n in ('AI对话', '国产AI助手', 'AI编程') or 'AI对话' in n or '编程' in n for n in names(s)),
   tk=['claude'], extra='''## 封号申诉要点（摘要）

1. 先确认是 **账号封禁** 还是 **地区/网络限制**，后者换网络即可，不需要申诉。
2. 申诉走 Anthropic 官方支持表单，用注册邮箱提交，写清使用场景，不要反复提交。
3. 避免共享账号、频繁切换 IP、使用来路不明的虚拟卡与接码号码。
4. 团队 / API 用户应查看用量政策（Usage Policy），企业场景建议走官方商务渠道。
5. 等待期间先用下方替代品顶上，重要数据定期导出。

详细版见：[Claude 封号申诉指南](https://51cgw9.cc/topics/claude-banned-appeal-guide/?utm_source=github) · [封号原因](https://51cgw9.cc/topics/claude-account-ban-reasons/?utm_source=github)
'''),
 'ai-tools-china-direct': dict(title='国内直连 AI 工具清单', c='cn-direct', intro='国内网络无需代理即可访问的 AI 工具，51发现导航每日自动检测可用性。',
   f=lambda s: s['access'] == 'cn' or any('国产' in n for n in names(s)), tk=['alternatives-china', 'deepseek', 'ai-assistant']),
 'free-ai-tools-cn': dict(title='免费 AI 工具清单', c='free', intro='可以免费使用（或有免费额度）的 AI 工具与常用网站，标注国内是否直连。',
   f=lambda s: s['price'] in ('free', 'freemium'), tk=['ai-assistant-guide', 'ai-image', 'ai-office']),
 'awesome-ai-coding-cn': dict(title='Awesome AI Coding CN · AI 编程工具中文清单', c='coding', intro='AI 编程助手、代码审查、模型 API 与开发者常用工具，中文点评 + 国内可用性。',
   f=lambda s: any(('编程' in n or '代码' in n or 'API' in n or n == '开发工具') for n in names(s)), tk=['coding', 'code-review', 'model-api', 'developer', 'agent']),
}
def badges(n, repo):
    return (f"[![站点](https://img.shields.io/badge/官网-51cgw9.cc-7c3aed)](https://51cgw9.cc/?utm_source=github) "
            f"![工具数](https://img.shields.io/badge/收录-{n}-blue) ![更新](https://img.shields.io/badge/更新-{today.replace('-','--')}-green) "
            f"[![Awesome](https://awesome.re/badge.svg)](https://github.com/sindresorhus/awesome) ![License](https://img.shields.io/badge/license-CC0-lightgrey)")
if MODE == 'main':
    groups = collections.OrderedDict()
    for s in S:
        top = next((c['name'] for c in s['cats'] if not c['parent']), '其他'); groups.setdefault(top, []).append(s)
    out = [f"<div align=\"center\">\n\n# Awesome AI Tools CN\n\n**中文 AI 工具与常用网站导航清单 · 每日自动同步**\n\n{badges(len(S),'main')}\n\n</div>\n",
           f"> 精选 **{len(S)}** 个 AI 工具与常用网站，标注 **国内能否直连 / 是否免费 / 是否需要海外手机号**。在线版（可搜索、可收藏、实时可用性）：👉 **[51发现导航 51cgw9.cc](https://51cgw9.cc/?utm_source=github)**\n",
           NAV, '\n## 目录\n', '- [专题清单](#专题清单)'] + [f"- [{g}](#{g.replace(' ', '-').lower()})（{len(v)}）" for g, v in groups.items()] + ['- [最新专题文章](#最新专题文章)', '- [参与贡献](#参与贡献)']
    out += ['\n## 专题清单\n'] + [f"- [{v['title']}](https://github.com/51fxdaohang/{k})" for k, v in CFG.items()] + ['- [币圈 Web3 工具导航 · Awesome Web3 Tools CN](https://github.com/51fxdaohang/awesome-web3-tools-cn)', '- [常用网址导航（hao123 式）· Useful Websites CN](https://github.com/51fxdaohang/useful-websites-cn)']
    for g, v in groups.items(): out += [f"\n## {g}\n", table(v, 'main')]
    out += ['\n## 最新专题文章\n', tlist(T[:15], 'main'), '\n## 参与贡献\n', '欢迎推荐好用的工具或报告失效链接，请先阅读 [CONTRIBUTING.md](CONTRIBUTING.md)。本 README 由 [GitHub Actions](.github/workflows/sync.yml) 每日从站点数据自动生成，请勿直接编辑表格。', FOOT]
    open('README.md', 'w').write('\n'.join(out))
    json.dump(d, open('data.json', 'w'), ensure_ascii=False)
else:
    c = CFG[MODE]; lst = [s for s in S if c['f'](s)]
    lst.sort(key=lambda s: (s['access'] != 'cn', s['price'] not in ('free', 'freemium')))
    out = [f"# {c['title']}\n", badges(len(lst), MODE) + '\n', f"> {c['intro']} 完整导航（{len(S)}+ 工具、实时可用性）：👉 **[51发现导航](https://51cgw9.cc/?utm_source=github&utm_campaign={c['c']})**\n", NAV,
           '\n图例：🇨🇳 直连 = 国内网络可直接访问；🌐 需代理；🆓 免费；💡 免费+付费；💰 付费\n', c.get('extra', ''), f"\n## 工具列表（{len(lst)}）\n", table(lst, c['c'])]
    ts = topics(c['tk'])
    if ts: out += ['\n## 相关指南\n', tlist(ts, c['c'])]
    out += ['\n## 更多清单\n', '- [Awesome AI Tools CN 总清单](https://github.com/51fxdaohang/awesome-ai-tools-cn)'] + [f"- [{v['title']}](https://github.com/51fxdaohang/{k})" for k, v in CFG.items() if k != MODE] + [FOOT]
    open('README.md', 'w').write('\n'.join(out))
print(MODE, 'ok')
