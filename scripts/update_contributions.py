#!/usr/bin/env python3
"""Rebuild the open-source section of the profile README.

Only PUBLIC repos you don't own are considered:
  * merged pull requests   (with link + repo stars)
  * discussions / participations / mentions in public issues and PRs
"""
import os, re, sys, json, time, urllib.request, urllib.parse
from pathlib import Path

USER = os.environ.get("GH_USER", "udbhav-shrinet")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
README = Path(os.environ.get("README_PATH", "README.md"))
START, END = "<!-- OSS:START -->", "<!-- OSS:END -->"
LIMIT = int(os.environ.get("OSS_LIMIT", "12"))
EXCLUDE_REPOS = {"vardhancodes/Multithreading", "Danyw24/mcp-radar", "morluto/rea"}

_stars = {}


def api(url, params=None):
    if params:
        url += "?" + urllib.parse.urlencode(params)
    req = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "profile-readme-updater",
        **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
    })
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except Exception as e:  # noqa: BLE001
            if attempt == 2:
                print(f"warn: {url} failed: {e}", file=sys.stderr)
                return None
            time.sleep(2 * (attempt + 1))


def search(q):
    data = api("https://api.github.com/search/issues",
               {"q": q, "sort": "updated", "order": "desc", "per_page": 50})
    time.sleep(1.5)  # stay well under search rate limit
    return (data or {}).get("items", [])


def repo_of(item):
    return item["repository_url"].replace("https://api.github.com/repos/", "")


def stars(repo):
    if repo not in _stars:
        d = api(f"https://api.github.com/repos/{repo}")
        _stars[repo] = d.get("stargazers_count") if d else None
    return _stars[repo]


def fmt_stars(n):
    if n is None:
        return "–"
    return f"{n/1000:.1f}k".replace(".0k", "k") if n >= 1000 else str(n)


def esc(s):
    return s.replace("|", "\\|").replace("\n", " ").strip()


def date(s):
    return (s or "")[:10]


def table(rows, head):
    if not rows:
        return "_Nothing here yet._\n"
    lines = ["| " + " | ".join(head) + " |", "|" + "|".join(["---"] * len(head)) + "|"]
    lines += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(lines) + "\n"


def build():
    base = f"author:{USER} -user:{USER} is:public archived:false"
    raw_merged = search(f"{base} type:pr is:merged")

    merged = [p for p in raw_merged if repo_of(p) not in EXCLUDE_REPOS]
    merged.sort(key=lambda x: (x.get("pull_request") or {}).get("merged_at") or x.get("closed_at") or "", reverse=True)
    merged = merged[:LIMIT]

    # Gather participated & mentioned threads
    ic = search(f"commenter:{USER} -author:{USER} is:public archived:false type:issue")
    pc = search(f"commenter:{USER} -author:{USER} is:public archived:false type:pr")
    im = search(f"mentions:{USER} -author:{USER} is:public archived:false type:issue")
    pm = search(f"mentions:{USER} -author:{USER} is:public archived:false type:pr")

    threads = {}
    for it in ic:
        r = repo_of(it)
        if r in EXCLUDE_REPOS:
            continue
        threads[it["html_url"]] = {"item": it, "role": "Commented"}

    for it in pc:
        r = repo_of(it)
        if r in EXCLUDE_REPOS:
            continue
        threads[it["html_url"]] = {"item": it, "role": "Commented"}

    for it in im:
        r = repo_of(it)
        if r in EXCLUDE_REPOS:
            continue
        if it["html_url"] in threads:
            threads[it["html_url"]]["role"] = "Mentioned & Commented"
        else:
            threads[it["html_url"]] = {"item": it, "role": "Mentioned"}

    for it in pm:
        r = repo_of(it)
        if r in EXCLUDE_REPOS:
            continue
        if it["html_url"] in threads:
            threads[it["html_url"]]["role"] = "Mentioned & Commented"
        else:
            threads[it["html_url"]] = {"item": it, "role": "Mentioned"}

    participated_items = list(threads.values())
    participated_items.sort(key=lambda x: x["item"]["created_at"], reverse=True)

    def pr_row(it, merged_flag):
        repo = repo_of(it)
        link = f"[{esc(it['title'])}]({it['html_url']})"
        when = date((it.get("pull_request") or {}).get("merged_at") or it["closed_at"]) if merged_flag else date(it["created_at"])
        return [f"[{repo}](https://github.com/{repo})", f"⭐ {fmt_stars(stars(repo))}",
                f"{link} (#{it['number']})", when]

    out = []
    out.append("#### 💡 Upstream Architecture & Attributed Solutions\n")
    out.append("- **[Model Context Protocol Servers](https://github.com/modelcontextprotocol/servers)** (⭐ 91.6k) — [Issue #5107](https://github.com/modelcontextprotocol/servers/issues/5107) / [Merged PR #5145](https://github.com/modelcontextprotocol/servers/pull/5145)")
    out.append("  > *\"The fix is the one @udbhav-shrinet proposed on the issue.\"* — Core maintainer Cliff Hall  ")
    out.append("  Diagnosed `git_show` diff headers lacking `a/` and `b/` prefixes, unblocking `git apply` functionality across all MCP tools.\n")
    out.append("- **[REA Core](https://github.com/morluto/rea)** — [PR #2787](https://github.com/morluto/rea/pull/2787) / [Merged in `e572c38dc`](https://github.com/morluto/rea/commit/e572c38dcf6ae72176319baef000784ff7d15e2f)")
    out.append("  > *\"Continues #2787, originally contributed by @udbhav-shrinet (Udbhav Shrinet). Original contributor history remains in this branch.\"*  ")
    out.append("  Aligned guide link routing across core documentation and 18 translation localized builds.\n")
    out.append("- **[Stanford NLP DSPy](https://github.com/stanfordnlp/dspy)** (⭐ 22k+) — [PR #10606](https://github.com/stanfordnlp/dspy/pull/10606)")
    out.append("  Isolated `BootstrapFewShot` optimizer's zero-threshold falsy evaluation flaw (`metric_threshold=0.0`), establishing the fix adopted in [Merged PR #10604](https://github.com/stanfordnlp/dspy/pull/10604).\n")
    out.append("- **[Hugging Face Smolagents](https://github.com/huggingface/smolagents)** (⭐ 30.1k) — [Issue #2961](https://github.com/huggingface/smolagents/issues/2961)")
    out.append("  Architected the `numpy.generic` inspection fix for safe execution serialization.\n")

    out.append("#### Merged pull requests\n")
    out.append(table([pr_row(i, True) for i in merged], ["Project", "Stars", "Pull request", "Merged"]))

    p_rows = []
    for entry in participated_items[:LIMIT]:
        it = entry["item"]
        repo = repo_of(it)
        link = f"[{esc(it['title'])}]({it['html_url']}) (#{it['number']})"
        state = "Resolved" if it["state"] == "closed" and it.get("state_reason") != "not_planned" else ("Closed" if it["state"] == "closed" else "Open")
        p_rows.append([
            f"[{repo}](https://github.com/{repo})",
            f"⭐ {fmt_stars(stars(repo))}",
            link,
            entry["role"],
            state,
            date(it["created_at"])
        ])
    out.append("#### Participated & Mentioned\n")
    out.append(table(p_rows, ["Project", "Stars", "Thread", "Activity", "Status", "Date"]))

    out.append(f"<sub>Auto-generated from public GitHub activity · updated {time.strftime('%Y-%m-%d', time.gmtime())} UTC</sub>\n")
    return "\n".join(out)


def main():
    text = README.read_text(encoding="utf-8")
    if START not in text or END not in text:
        sys.exit(f"markers {START} / {END} not found in {README}")
    block = f"{START}\n{build()}\n{END}"
    new = re.sub(re.escape(START) + r".*?" + re.escape(END), lambda _: block, text, flags=re.S)
    if new != text:
        README.write_text(new, encoding="utf-8")
        print("README updated")
    else:
        print("no changes")


if __name__ == "__main__":
    main()
