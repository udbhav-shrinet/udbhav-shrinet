#!/usr/bin/env python3
"""Rebuild the open-source section of the profile README.

Only PUBLIC repos you don't own are considered:
  * merged pull requests   (with link + repo stars)
  * open / in-review PRs
  * issues you reported    (open + resolved)
  * thanks left by others on your PRs / issues
"""
import os, re, sys, json, time, urllib.request, urllib.parse
from pathlib import Path

USER = os.environ.get("GH_USER", "udbhav-shrinet")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
README = Path(os.environ.get("README_PATH", "README.md"))
START, END = "<!-- OSS:START -->", "<!-- OSS:END -->"
LIMIT = int(os.environ.get("OSS_LIMIT", "10"))
THANKS = re.compile(r"\b(thanks?|thank you|thx|ty|much appreciated|appreciate(d)?|great (catch|work|fix|job)|nice (catch|work|fix))\b|🙏|❤️|🎉|🙌", re.I)

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
    time.sleep(2)  # stay well under the search rate limit
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


def thanks_for(item):
    """Comments from other humans on this PR/issue that read as thanks."""
    if not item.get("comments"):
        return []
    comments = api(item["comments_url"], {"per_page": 100}) or []
    out = []
    for c in comments:
        who = c["user"]["login"]
        if who.lower() == USER.lower() or c["user"]["type"] == "Bot" or who.endswith("[bot]"):
            continue
        body = c.get("body") or ""
        if THANKS.search(body):
            snippet = re.sub(r"\s+", " ", re.sub(r"```.*?```", "", body, flags=re.S)).strip()
            out.append({
                "who": who, "url": c["html_url"], "repo": repo_of(item),
                "title": item["title"], "number": item["number"],
                "kind": "PR" if "pull_request" in item else "issue",
                "snippet": snippet[:140] + ("…" if len(snippet) > 140 else ""),
            })
    return out


def table(rows, head):
    if not rows:
        return "_Nothing here yet._\n"
    lines = ["| " + " | ".join(head) + " |", "|" + "|".join(["---"] * len(head)) + "|"]
    lines += ["| " + " | ".join(r) + " |" for r in rows]
    return "\n".join(lines) + "\n"


def build():
    base = f"author:{USER} -user:{USER} is:public archived:false"
    merged = search(f"{base} type:pr is:merged")[:LIMIT]
    open_prs = search(f"{base} type:pr is:open")[:LIMIT]
    issues = search(f"{base} type:issue")[:LIMIT]

    thanks = []
    for it in merged + issues:
        thanks += thanks_for(it)

    def pr_row(it, merged_flag):
        repo = repo_of(it)
        link = f"[{esc(it['title'])}]({it['html_url']})"
        when = date((it.get("pull_request") or {}).get("merged_at") or it["closed_at"]) if merged_flag else date(it["created_at"])
        return [f"[{repo}](https://github.com/{repo})", f"⭐ {fmt_stars(stars(repo))}",
                f"{link} (#{it['number']})", when]

    out = []
    out.append("#### Merged pull requests\n")
    out.append(table([pr_row(i, True) for i in merged], ["Project", "Stars", "Pull request", "Merged"]))
    out.append("#### In progress\n")
    out.append(table([pr_row(i, False) for i in open_prs], ["Project", "Stars", "Pull request", "Opened"]))

    rows = []
    for it in issues:
        repo = repo_of(it)
        if it["state"] == "closed":
            status = "Resolved" if it.get("state_reason") != "not_planned" else "Closed"
        else:
            status = "Open"
        rows.append([f"[{repo}](https://github.com/{repo})",
                     f"[{esc(it['title'])}]({it['html_url']}) (#{it['number']})", status, date(it["created_at"])])
    out.append("#### Issues reported\n")
    out.append(table(rows, ["Project", "Issue", "Status", "Opened"]))

    out.append("#### Kind words from maintainers\n")
    if thanks:
        for t in thanks[:8]:
            out.append(f"- **[@{t['who']}]({t['url']})** on {t['kind']} [{t['repo']}#{t['number']}]({t['url']}): “{esc(t['snippet'])}”")
        out.append("")
    else:
        out.append("_Nothing here yet._\n")

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
