<p align="center">
  <img src="./assets/terminal.svg" alt="Terminal: whoami, what I'm building, open-source" width="760"/>
</p>

<p align="center">
  <a href="https://udbhav-shrinet.github.io/me/">portfolio</a> &nbsp;·&nbsp;
  <a href="https://www.linkedin.com/in/udbhav-shrinet">linkedin</a> &nbsp;·&nbsp;
  <a href="mailto:udbhav.singh.shrinet@gmail.com">email</a>
</p>

I'm Udbhav. I work with data for a living, and my side projects are mostly me trying to see how far I can push an idea. When I hit a bug in a library I use, I usually end up sending the fix upstream.

---

## Merged pull requests

Fixes that landed in projects I don't own, mostly agent tooling and data libraries: Model Context Protocol, DSPy, DeepEval, Hugging Face.

<!-- OSS:START -->
### Merged

| Project | Stars | Pull request | Merged |
|---|---|---|---|
| [confident-ai/deepeval](https://github.com/confident-ai/deepeval) | 19.5k | [fix(litellm): omit default temperature to prevent failures on reasoning models](https://github.com/confident-ai/deepeval/pull/3431) (#3431) | 2026-11-02 |
| [davidgasquez/awesome-duckdb](https://github.com/davidgasquez/awesome-duckdb) | 2.5k | [Add ds-agent-playbook to Libraries Powered by DuckDB](https://github.com/davidgasquez/awesome-duckdb/pull/372) (#372) | 2026-10-12 |
| [ddotta/awesome-polars](https://github.com/ddotta/awesome-polars) | 1.1k | [Add ds-agent-playbook to Tools Built with Polars](https://github.com/ddotta/awesome-polars/pull/643) (#643) | 2026-10-12 |

### Upstream Architecture & Attributed Solutions

**[Model Context Protocol Servers](https://github.com/modelcontextprotocol/servers)** · 91.6k stars · [Issue #5107](https://github.com/modelcontextprotocol/servers/issues/5107) · [Merged PR #5145](https://github.com/modelcontextprotocol/servers/pull/5145)
> "The fix is the one @udbhav-shrinet proposed on the issue." — Cliff Hall, core maintainer

`git_show` was printing diff headers without the `a/` and `b/` prefixes, so `git apply` didn't work on its output. I found it and proposed the fix, and the maintainers merged it.

**[REA Core](https://github.com/morluto/rea)** · [PR #2787](https://github.com/morluto/rea/pull/2787) · [Merged in `e572c38dc`](https://github.com/morluto/rea/commit/e572c38dcf6ae72176319baef000784ff7d15e2f)
> "Continues #2787, originally contributed by @udbhav-shrinet (Udbhav Shrinet). Original contributor history remains in this branch."

Fixed the guide links across the main docs and the 18 translated builds. A maintainer picked the PR up and merged it with my history kept.

**[Stanford NLP DSPy](https://github.com/stanfordnlp/dspy)** · 22k+ stars · [PR #10606](https://github.com/stanfordnlp/dspy/pull/10606) · fix went in via [Merged PR #10604](https://github.com/stanfordnlp/dspy/pull/10604)

`BootstrapFewShot` treated `metric_threshold=0.0` as if it wasn't set, because 0.0 is falsy in Python. I traced it down and the same fix got merged.

**[Hugging Face Smolagents](https://github.com/huggingface/smolagents)** · 30.1k stars · [Issue #2961](https://github.com/huggingface/smolagents/issues/2961) · [PR #2972](https://github.com/huggingface/smolagents/pull/2972)

The safe serializer was rejecting NumPy scalars and extended-precision values.

<details>
<summary><b>Participated & Mentioned</b> (12 threads)</summary>

<br/>

| Project | Stars | Thread | Activity | Status | Date |
|---|---|---|---|---|---|
| [huggingface/smolagents](https://github.com/huggingface/smolagents) | 30.3k | [BUG: open_deep_research YouTubeConverter silently drops transcripts (get_transcript removed in youtube-transcript-api 1.0)](https://github.com/huggingface/smolagents/issues/3010) (#3010) | Commented | Open | 2026-10-17 |
| [huggingface/smolagents](https://github.com/huggingface/smolagents) | 30.3k | [ENH: Add a first-class NvidiaModel for NVIDIA NIM](https://github.com/huggingface/smolagents/issues/2995) (#2995) | Commented | Open | 2026-10-15 |
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | 92k | [fix(git): prefix git_show diff headers with a/ and b/](https://github.com/modelcontextprotocol/servers/pull/5145) (#5145) | Mentioned | Resolved | 2026-10-13 |
| [BerriAI/litellm](https://github.com/BerriAI/litellm) | 63.2k | [fix(redis): keep the data node host, port and db off Redis Sentinel connections](https://github.com/BerriAI/litellm/pull/46041) (#46041) | Commented | Open | 2026-10-12 |
| [BerriAI/litellm](https://github.com/BerriAI/litellm) | 63.2k | [test(router): stop test_default_model_fallbacks leaking litellm.default_fallbacks](https://github.com/BerriAI/litellm/pull/46014) (#46014) | Commented | Resolved | 2026-10-12 |
| [huggingface/smolagents](https://github.com/huggingface/smolagents) | 30.3k | [BUG: SafeSerializer rejects NumPy string and complex scalar values](https://github.com/huggingface/smolagents/issues/2961) (#2961) | Mentioned & Commented | Resolved | 2026-10-12 |
| [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) | 24.8k | [Add a filesystem backed provider for the Skills extension](https://github.com/modelcontextprotocol/python-sdk/issues/3683) (#3683) | Commented | Open | 2026-10-11 |
| [BerriAI/litellm](https://github.com/BerriAI/litellm) | 63.2k | [fix(databricks): route GPT-5.4+ function-tool calls through the Responses API](https://github.com/BerriAI/litellm/pull/45952) (#45952) | Mentioned & Commented | Open | 2026-10-11 |
| [modelcontextprotocol/python-sdk](https://github.com/modelcontextprotocol/python-sdk) | 24.8k | [[v1.x] Server revalidates every tools/call with one-shot jsonschema.validate(), re-checking the schema each time](https://github.com/modelcontextprotocol/python-sdk/issues/3676) (#3676) | Commented | Open | 2026-10-11 |
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | 92k | [git: git_show diff headers lack git's a/ and b/ path prefixes](https://github.com/modelcontextprotocol/servers/issues/5107) (#5107) | Commented | Resolved | 2026-10-10 |
| [huggingface/smolagents](https://github.com/huggingface/smolagents) | 30.3k | [BUG: Tool.to_dict rejects valid tuple aliases in with statements as undefined names](https://github.com/huggingface/smolagents/issues/2942) (#2942) | Commented | Open | 2026-10-10 |
| [huggingface/smolagents](https://github.com/huggingface/smolagents) | 30.3k | [BUG: LocalPythonExecutor loses print output when print is passed as a callback](https://github.com/huggingface/smolagents/issues/2941) (#2941) | Commented | Open | 2026-10-10 |

</details>

<sub>Auto-generated from public GitHub activity · updated 2026-11-12 UTC</sub>

<!-- OSS:END -->

<p align="center">
  <img src="https://github-readme-stats.vercel.app/api?username=udbhav-shrinet&show_icons=true&hide=commits,stars&show=prs_merged,prs_merged_percentage,reviews,discussions_started,discussions_answered&count_private=false&bg_color=0d1117&border_color=30363d&border_radius=8&title_color=3fb950&icon_color=8b949e&text_color=8b949e&ring_color=3fb950" width="49%" alt="Open source activity"/>
  <img src="https://github-readme-stats.vercel.app/api/top-langs/?username=udbhav-shrinet&layout=compact&langs_count=6&bg_color=0d1117&border_color=30363d&border_radius=8&title_color=3fb950&text_color=8b949e" width="49%" alt="Top languages"/>
</p>

---

## Things I've built

<table width="100%">
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/udbhav-shrinet/Pac-Fly"><img src="https://github-readme-stats.vercel.app/api/pin/?username=udbhav-shrinet&repo=Pac-Fly&bg_color=0d1117&border_color=30363d&border_radius=8&title_color=3fb950&icon_color=8b949e&text_color=8b949e" width="100%" alt="Pac-Fly"/></a>
      <p>A fruit fly brain simulation. 130k+ neurons running in the browser with WebGL, and sound through WebAudio.<br/><a href="https://udbhav-shrinet.github.io/Pac-Fly/">demo</a> · <a href="https://github.com/udbhav-shrinet/Pac-Fly">source</a></p>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/udbhav-shrinet/Multi-Agent-Trading-Bot"><img src="https://github-readme-stats.vercel.app/api/pin/?username=udbhav-shrinet&repo=Multi-Agent-Trading-Bot&bg_color=0d1117&border_color=30363d&border_radius=8&title_color=3fb950&icon_color=8b949e&text_color=8b949e" width="100%" alt="Multi-Agent Trading Bot"/></a>
      <p>A multi-agent trading engine. It scores the macro regime from FRED data, trades through the Alpaca API, and runs on its own.<br/><a href="https://udbhav-shrinet.github.io/Multi-Agent-Trading-Bot/">demo</a> · <a href="https://github.com/udbhav-shrinet/Multi-Agent-Trading-Bot">source</a></p>
    </td>
  </tr>
  <tr>
    <td width="50%" valign="top">
      <a href="https://github.com/udbhav-shrinet/trends"><img src="https://github-readme-stats.vercel.app/api/pin/?username=udbhav-shrinet&repo=trends&bg_color=0d1117&border_color=30363d&border_radius=8&title_color=3fb950&icon_color=8b949e&text_color=8b949e" width="100%" alt="Trends"/></a>
      <p>Search trend analytics across regions. Python pipelines and the charts on top of them.<br/><a href="https://udbhav-shrinet.github.io/trends/">demo</a> · <a href="https://github.com/udbhav-shrinet/trends">source</a></p>
    </td>
    <td width="50%" valign="top">
      <a href="https://github.com/udbhav-shrinet/ds-agent-playbook"><img src="https://github-readme-stats.vercel.app/api/pin/?username=udbhav-shrinet&repo=ds-agent-playbook&bg_color=0d1117&border_color=30363d&border_radius=8&title_color=3fb950&icon_color=8b949e&text_color=8b949e" width="100%" alt="ds-agent-playbook"/></a>
      <p>A playbook for doing data science with agents. Polars and DuckDB, automated feature synthesis, and pipelines that run out-of-core.<br/><a href="https://github.com/udbhav-shrinet/ds-agent-playbook">source</a></p>
    </td>
  </tr>
</table>

---

## Stack

| | |
|---|---|
| **Languages** | `Python` `TypeScript` `JavaScript` `SQL` `R` `Bash` |
| **Data & ML** | `PyTorch` `TensorFlow` `scikit-learn` `pandas` `Polars` `DuckDB` `NumPy` |
| **Agentic AI** | `Claude Code` `OpenAI Codex` `Model Context Protocol` `agentic workflows` |
| **Infra & databases** | `Google Cloud` `AWS` `PostgreSQL` `MySQL` `Git` `Vercel` `Netlify` |

---

<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/udbhav-shrinet/udbhav-shrinet/output/github-contribution-grid-snake-dark.svg" />
    <img src="https://raw.githubusercontent.com/udbhav-shrinet/udbhav-shrinet/output/github-contribution-grid-snake.svg" alt="Contribution snake" />
  </picture>
</p>
