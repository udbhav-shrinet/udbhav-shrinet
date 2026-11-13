#!/usr/bin/env python3
"""Builds assets/stats-card.svg matching the Sila purple theme with robust static rendering."""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

USER = os.environ.get("GH_USER", "udbhav-shrinet")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
OUT = os.environ.get("OUT", "assets/stats-card.svg")
SLEEP = 0.5 if TOKEN else 2.0


def api(path):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "stats-card"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    req = urllib.request.Request("https://api.github.com" + path, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.load(r)


def count(kind, q):
    data = api(f"/search/{kind}?q={urllib.parse.quote(q)}&per_page=1")
    time.sleep(SLEEP)
    return data["total_count"]


def rank(commits, prs, issues, reviews, stars, followers):
    exp_cdf = lambda x: 1 - 2 ** -x
    log_cdf = lambda x: x / (1 + x)
    weights = dict(commits=2, prs=3, issues=1, reviews=1, stars=4, followers=1)
    score = (
        weights["commits"] * exp_cdf(commits / 1000)
        + weights["prs"] * exp_cdf(prs / 50)
        + weights["issues"] * exp_cdf(issues / 25)
        + weights["reviews"] * exp_cdf(reviews / 2)
        + weights["stars"] * log_cdf(stars / 50)
        + weights["followers"] * log_cdf(followers / 10)
    )
    pct = (1 - score / sum(weights.values())) * 100
    levels = ["S", "A+", "A", "A-", "B+", "B", "B-", "C+", "C"]
    thresholds = [1, 12.5, 25, 37.5, 50, 62.5, 75, 87.5, 100]
    level = next(l for l, t in zip(levels, thresholds) if pct <= t)
    return level, pct


def collect():
    user = api(f"/users/{USER}")
    repos = api(f"/users/{USER}/repos?per_page=100&type=owner")
    stars = sum(r["stargazers_count"] for r in repos if not r["fork"])
    prs_all = count("issues", f"author:{USER} type:pr")
    prs_up = count("issues", f"author:{USER} type:pr -user:{USER}")
    merged_up = count("issues", f"author:{USER} type:pr is:merged -user:{USER}")
    issues = count("issues", f"author:{USER} type:issue")
    reviews = count("issues", f"reviewed-by:{USER} type:pr -author:{USER}")
    commits = count("commits", f"author:{USER}")
    level, pct = rank(commits, prs_all, issues, reviews, stars, user["followers"])
    rate = round(100 * merged_up / prs_up) if prs_up else 0
    return dict(merged=merged_up, rate=rate, reviews=reviews, issues=issues, commits=commits, level=level, pct=pct)


def svg(d):
    rate_str = f"{d['rate']}%"
    rows = [
        ("Merged PRs (upstream)", d["merged"]),
        ("Merge rate", rate_str),
        ("Code reviews", d["reviews"]),
        ("Issues opened", d["issues"]),
        ("Total commits", d["commits"])
    ]
    body = ""
    for i, (label, val) in enumerate(rows):
        y = 78 + i * 26
        body += (
            f'<g class="r">'
            f'<circle cx="30" cy="{y-5}" r="3" fill="#c084fc"/>'
            f'<text x="44" y="{y}" class="l">{label}</text>'
            f'<text x="300" y="{y}" class="v" text-anchor="end">{val}</text></g>'
        )
    circ = 2 * 3.14159265 * 38
    fill = max(0.04, min(1.0, (100 - d["pct"]) / 100))
    off = circ * (1 - fill)
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="495" height="210" viewBox="0 0 495 210" role="img" aria-label="GitHub stats for {USER}">
<style>
text{{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Helvetica,Arial,sans-serif}}
.h{{font-size:16px;font-weight:600;fill:#c084fc;letter-spacing:0.5px}}
.l{{font-size:13px;fill:#aab2e0}} .v{{font-size:13px;font-weight:700;fill:#f1f3ff}}
.k{{font-size:32px;font-weight:700;fill:#f1f3ff}} .s{{font-size:11px;fill:#a78bfa;font-weight:500}}
.r{{opacity:1}}
</style>
<rect x="0.5" y="0.5" width="494" height="209" rx="12" fill="#0d0a1a" stroke="#2c2250"/>
<text x="25" y="38" class="h">{USER} · open source</text>
{body}
<g transform="translate(395,100)">
<circle r="38" fill="none" stroke="#251b47" stroke-width="6"/>
<circle r="38" fill="none" stroke="#c084fc" stroke-width="6" stroke-linecap="round" stroke-dasharray="{circ:.1f}" stroke-dashoffset="{off:.1f}" transform="rotate(-90)"/>
<text y="11" text-anchor="middle" class="k">{d["level"]}</text>
<text y="64" text-anchor="middle" class="s">open source</text>
</g>
</svg>"""


if __name__ == "__main__":
    data = collect()
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(svg(data))
    print(json.dumps(data))
