#!/usr/bin/env python3
"""Collect hourly AI intelligence from public feeds and APIs.

Dependency-free collector. Public engagement metrics are signals, not proof
of product quality, adoption, or commercial success.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import datetime as dt
import html
import json
import os
import re
import sys
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from typing import Any, Iterable


USER_AGENT = "ray-ai-hourly-intelligence/1.1 (+https://github.com/rayest/xiaobai-xue-ai-7-days)"
TIMEOUT = 20
BEIJING = dt.timezone(dt.timedelta(hours=8))


@dataclass
class Item:
    title: str
    url: str
    source: str
    published: str = ""
    summary: str = ""
    signal: str = ""
    score: float = 0.0


def format_datetime(value: str) -> str:
    value = (value or "").strip()
    if not value:
        return ""
    try:
        if value.isdigit():
            parsed = dt.datetime.fromtimestamp(int(value), dt.timezone.utc)
        else:
            normalized = value.replace("Z", "+00:00")
            try:
                parsed = dt.datetime.fromisoformat(normalized)
            except ValueError:
                parsed = dt.datetime.strptime(value.replace(" GMT", " +0000"), "%a, %d %b %Y %H:%M:%S %z")
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=dt.timezone.utc)
        return parsed.astimezone(BEIJING).strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        return value


def request(url: str, *, method: str = "GET", data: bytes | None = None,
            headers: dict[str, str] | None = None) -> bytes:
    request_headers = {"User-Agent": USER_AGENT, "Accept": "*/*"}
    if headers:
        request_headers.update(headers)
    req = urllib.request.Request(url, data=data, headers=request_headers, method=method)
    with urllib.request.urlopen(req, timeout=TIMEOUT) as response:
        return response.read()


def json_request(url: str, **kwargs: Any) -> Any:
    return json.loads(request(url, **kwargs).decode("utf-8", errors="replace"))


def clean_text(value: str) -> str:
    value = html.unescape(re.sub(r"<[^>]+>", " ", value or ""))
    return re.sub(r"\s+", " ", value).strip()


def parse_feed(payload: bytes, source: str) -> list[Item]:
    root = ET.fromstring(payload)
    items: list[Item] = []
    nodes = list(root.findall(".//item")) + list(root.findall(".//{http://www.w3.org/2005/Atom}entry"))
    for node in nodes:
        def text(path: str) -> str:
            child = node.find(path)
            return clean_text(child.text if child is not None and child.text else "")

        title = text("title") or text("{http://www.w3.org/2005/Atom}title")
        link = text("link")
        if not link:
            atom_link = node.find("{http://www.w3.org/2005/Atom}link")
            link = atom_link.attrib.get("href", "") if atom_link is not None else ""
        published = format_datetime(text("pubDate") or text("published") or text("{http://www.w3.org/2005/Atom}published"))
        summary = text("description") or text("summary") or text("{http://www.w3.org/2005/Atom}summary")
        if title and link:
            items.append(Item(title, link, source, published, summary))
    return items


def collect_rss(name: str, url: str) -> list[Item]:
    try:
        return parse_feed(request(url), name)
    except Exception as exc:
        print(f"warning: {name}: {exc}", file=sys.stderr)
        return []


def collect_hacker_news() -> list[Item]:
    try:
        ids = json_request("https://hacker-news.firebaseio.com/v0/newstories.json")[:60]
        result: list[Item] = []
        for story_id in ids:
            story = json_request(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json")
            title = story.get("title", "")
            text = clean_text(story.get("text", ""))
            if title and any(word in (title + " " + text).lower() for word in ("ai", "llm", "model", "agent", "gpu", "claude", "anthropic")):
                result.append(Item(title, story.get("url", f"https://news.ycombinator.com/item?id={story_id}"),
                                   "Hacker News", format_datetime(str(story.get("time", ""))), text,
                                   f"score={story.get('score', 0)}, comments={story.get('descendants', 0)}",
                                   float(story.get("score", 0))))
        return result
    except Exception as exc:
        print(f"warning: Hacker News: {exc}", file=sys.stderr)
        return []


def collect_github() -> list[Item]:
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()
    query = urllib.parse.quote(f"topic:artificial-intelligence created:>={today}")
    url = f"https://api.github.com/search/repositories?q={query}&sort=stars&order=desc&per_page=30"
    try:
        data = json_request(url, headers={"Accept": "application/vnd.github+json"})
        return [Item(repo["full_name"], repo["html_url"], "GitHub", format_datetime(repo.get("created_at", "")),
                     clean_text(repo.get("description", "")),
                     f"stars={repo.get('stargazers_count', 0)}, forks={repo.get('forks_count', 0)}",
                     float(repo.get("stargazers_count", 0))) for repo in data.get("items", [])]
    except Exception as exc:
        print(f"warning: GitHub: {exc}", file=sys.stderr)
        return []


def collect_github_releases() -> list[Item]:
    """Track official Claude Code release notes without requiring GitHub auth."""
    return collect_rss("Claude Code GitHub Releases", "https://github.com/anthropics/claude-code/releases.atom")


def collect_hugging_face() -> list[Item]:
    result: list[Item] = []
    endpoints = [("models", "https://huggingface.co/api/models?sort=likes&direction=-1&limit=30"),
                 ("spaces", "https://huggingface.co/api/spaces?sort=likes&direction=-1&limit=30"),
                 ("datasets", "https://huggingface.co/api/datasets?sort=likes&direction=-1&limit=30")]
    try:
        for kind, url in endpoints:
            for entry in json_request(url):
                ident = entry.get("id", "")
                if not ident:
                    continue
                page_url = f"https://huggingface.co/{ident}" if kind == "models" else f"https://huggingface.co/{kind}/{ident}"
                result.append(Item(ident, page_url, f"Hugging Face {kind}", format_datetime(entry.get("lastModified", "")),
                                   entry.get("pipeline_tag", ""),
                                   f"likes={entry.get('likes', 0)}, downloads={entry.get('downloads', 0)}",
                                   float(entry.get("likes", 0))))
        return result
    except Exception as exc:
        print(f"warning: Hugging Face: {exc}", file=sys.stderr)
        return result


def collect_product_hunt() -> list[Item]:
    token = os.getenv("PRODUCT_HUNT_TOKEN")
    if not token:
        print("info: Product Hunt skipped; set PRODUCT_HUNT_TOKEN to enable its API.", file=sys.stderr)
        return []
    since = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(hours=24)).isoformat()
    query = f'''query {{ posts(first: 30, order: VOTES, postedAfter: "{since}") {{ edges {{ node {{ name tagline url votesCount commentsCount createdAt }} }} }} }}'''
    try:
        data = json_request("https://api.producthunt.com/v2/api/graphql", method="POST",
                            data=json.dumps({"query": query}).encode(),
                            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"})
        posts = data.get("data", {}).get("posts", {}).get("edges", [])
        return [Item(post["node"]["name"], post["node"]["url"], "Product Hunt",
                     format_datetime(post["node"].get("createdAt", "")), post["node"].get("tagline", ""),
                     f"votes={post['node'].get('votesCount', 0)}, comments={post['node'].get('commentsCount', 0)}",
                     float(post["node"].get("votesCount", 0))) for post in posts]
    except Exception as exc:
        print(f"warning: Product Hunt: {exc}", file=sys.stderr)
        return []


def dedupe(items: Iterable[Item]) -> list[Item]:
    seen: set[str] = set()
    result: list[Item] = []
    for item in items:
        key = item.url.split("#", 1)[0].rstrip("/")
        if key not in seen:
            seen.add(key)
            result.append(item)
    return sorted(result, key=lambda item: item.score, reverse=True)


def markdown(items: list[Item], generated_at: dt.datetime, hours: int) -> str:
    lines = ["# AI 与大模型情报", "", f"生成时间：{generated_at.astimezone(BEIJING).strftime('%Y-%m-%d %H:%M:%S')}",
             f"抓取窗口：最近 {hours} 小时；来源条目：{len(items)}", "",
             "> 官方发布、平台热度、社区观点和分析判断分开记录。点赞、投票、评论、Star、下载量只是公开信号，不等于真实用户规模、产品质量或商业成功。", ""]
    groups: dict[str, list[Item]] = {}
    for item in items:
        groups.setdefault(item.source, []).append(item)
    for source, group in groups.items():
        lines += [f"## {source}", ""]
        for item in group[:20]:
            meta = " · ".join(value for value in (item.published, item.signal) if value)
            lines.append(f"- [{item.title}]({item.url})" + (f" — {meta}" if meta else ""))
            if item.summary:
                lines.append(f"  - 摘要：{item.summary[:280].rstrip()}")
        lines.append("")
    lines += ["## 人工分析提示", "", "- 核对发布时间和原始来源，再判断是否为当天新增。",
              "- Anthropic/Claude Code 官方内容属于公司自述；应与社区反馈、采用数据和后续结果交叉验证。",
              "- 继续追踪真实用户采用、生产部署、收入/成本变化、版本迭代和反例。", ""]
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect hourly AI intelligence from public sources.")
    parser.add_argument("--output", default="ai-intelligence.md")
    parser.add_argument("--hours", type=int, default=24)
    args = parser.parse_args()
    feeds = {
        "OpenAI": "https://openai.com/news/rss.xml",
        "Anthropic Newsroom": "https://www.anthropic.com/rss.xml",
        "Anthropic API Release Notes": "https://docs.anthropic.com/en/release-notes/api",
        "Claude Code Docs": "https://docs.anthropic.com/en/docs/claude-code/changelog",
        "Google AI": "https://blog.google/technology/ai/rss/",
        "Microsoft AI": "https://blogs.microsoft.com/ai/feed/",
        "Hugging Face Blog": "https://huggingface.co/blog/feed.xml",
        "arXiv AI": "https://export.arxiv.org/rss/cs.AI",
        "Reddit r/artificial": "https://www.reddit.com/r/artificial/hot/.rss",
    }
    collectors = [lambda name=name, url=url: collect_rss(name, url) for name, url in feeds.items()]
    collectors += [collect_hacker_news, collect_github, collect_github_releases, collect_hugging_face, collect_product_hunt]
    all_items: list[Item] = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(collectors)) as pool:
        for future in concurrent.futures.as_completed([pool.submit(fn) for fn in collectors]):
            try:
                all_items.extend(future.result())
            except Exception as exc:
                print(f"warning: collector failed: {exc}", file=sys.stderr)
    content = markdown(dedupe(all_items), dt.datetime.now(dt.timezone.utc), args.hours)
    output = os.path.abspath(args.output)
    with open(output, "w", encoding="utf-8") as file:
        file.write(content)
    print(f"Wrote {len(all_items)} collected items to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
