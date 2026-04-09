from __future__ import annotations

import os
import sys
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, quote_plus, unquote, urlparse

import arxiv
import requests
from bs4 import BeautifulSoup

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.insert(0, parent_dir)

from utils.JsonTools import save_json


USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
)
REQUEST_TIMEOUT = 15


def _clean_str(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _ensure_metadata_fields(content_plan: dict[str, Any]) -> dict[str, Any]:
    metadata = content_plan.setdefault("metadata", {})
    if not isinstance(metadata, dict):
        metadata = {}
        content_plan["metadata"] = metadata
    metadata.setdefault("github", "")
    metadata.setdefault("arxiv_id", "")
    return metadata


def _normalize_arxiv_url(value: str) -> str:
    value = _clean_str(value)
    if not value:
        return ""
    if value.startswith("http://") or value.startswith("https://"):
        return value
    return f"https://arxiv.org/abs/{value}"


def _normalize_github_url(value: str) -> str:
    value = _clean_str(value)
    if not value:
        return ""
    if value.startswith("http://") or value.startswith("https://"):
        parsed = urlparse(value)
        parts = [part for part in parsed.path.split("/") if part]
        if len(parts) >= 2:
            return f"https://github.com/{parts[0]}/{parts[1]}"
        return value
    return value


def _search_arxiv_url(title: str, log=None) -> str:
    title = _clean_str(title)
    if not title:
        return ""

    try:
        client = arxiv.Client()
        search = arxiv.Search(query=f'ti:"{title}"', max_results=5)
        results = list(client.results(search))
    except Exception as exc:
        if log:
            log.warning(f"arXiv lookup failed: {exc}")
        return ""

    title_lower = title.lower()
    for paper in results:
        if _clean_str(getattr(paper, "title", "")).lower() == title_lower:
            return _normalize_arxiv_url(getattr(paper, "entry_id", ""))

    if results:
        return _normalize_arxiv_url(getattr(results[0], "entry_id", ""))
    return ""


def _extract_search_links(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")
    links: list[str] = []
    for anchor in soup.select("a[href]"):
        href = anchor.get("href", "").strip()
        if not href:
            continue

        if "duckduckgo.com/l/?" in href:
            query = parse_qs(urlparse(href).query)
            target = query.get("uddg", [""])[0]
            href = unquote(target) if target else href

        if href.startswith("//"):
            href = "https:" + href

        if href.startswith("http://") or href.startswith("https://"):
            links.append(href)
    return links


def _search_duckduckgo(query: str, log=None) -> list[str]:
    url = f"https://duckduckgo.com/html/?q={quote_plus(query)}"
    headers = {"User-Agent": USER_AGENT}
    try:
        response = requests.get(url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except Exception as exc:
        if log:
            log.warning(f"DuckDuckGo lookup failed for query '{query}': {exc}")
        return []
    return _extract_search_links(response.text)


def _is_probably_paper_repo(url: str) -> bool:
    parsed = urlparse(url)
    if parsed.netloc.lower() not in {"github.com", "www.github.com"}:
        return False

    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        return False

    blocked_first = {"topics", "search", "orgs", "collections", "marketplace", "features"}
    if parts[0].lower() in blocked_first:
        return False
    return True


def _normalize_repo_root(url: str) -> str:
    parsed = urlparse(url)
    parts = [part for part in parsed.path.split("/") if part]
    if len(parts) < 2:
        return url
    return f"https://github.com/{parts[0]}/{parts[1]}"


def _validate_github_repo(repo_url: str, title: str, authors: list[str], log=None) -> bool:
    headers = {"User-Agent": USER_AGENT}
    try:
        response = requests.get(repo_url, headers=headers, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
    except Exception as exc:
        if log:
            log.warning(f"GitHub repo validation failed for '{repo_url}': {exc}")
        return False

    page_text = BeautifulSoup(response.text, "html.parser").get_text(" ", strip=True).lower()
    title_tokens = [token.lower() for token in title.split() if len(token) > 3]
    matched_title_tokens = sum(1 for token in title_tokens[:8] if token in page_text)
    author_match = any(_clean_str(author).lower() in page_text for author in authors[:3])

    return matched_title_tokens >= 2 or author_match


def _search_github_url(title: str, authors: list[str], log=None) -> str:
    title = _clean_str(title)
    queries = [
        f'"{title}" github',
        f"{title} official github",
    ]
    if authors:
        queries.append(f'"{title}" github "{authors[0]}"')

    seen: set[str] = set()
    candidates: list[str] = []

    for query in queries:
        for link in _search_duckduckgo(query, log=log):
            if not _is_probably_paper_repo(link):
                continue
            repo_url = _normalize_repo_root(link)
            if repo_url in seen:
                continue
            seen.add(repo_url)
            candidates.append(repo_url)

    for repo_url in candidates:
        if _validate_github_repo(repo_url, title, authors, log=log):
            return repo_url
    return ""


def enrich_content_plan_metadata(
    content_plan: dict[str, Any],
    output_path: str | Path,
    file_name: str,
    log=None,
    github_url: str = "",
    arxiv_url: str = "",
) -> dict[str, Any]:
    metadata = _ensure_metadata_fields(content_plan)

    manual_github = _normalize_github_url(github_url)
    manual_arxiv = _normalize_arxiv_url(arxiv_url)

    if manual_github:
        metadata["github"] = manual_github
        if log:
            log.info("Metadata enrich: use manual GitHub URL.")
    elif not _clean_str(metadata.get("github")):
        github_candidate = _search_github_url(
            metadata.get("title", ""),
            metadata.get("authors", []) if isinstance(metadata.get("authors"), list) else [],
            log=log,
        )
        metadata["github"] = github_candidate
        if log:
            if github_candidate:
                log.info(f"Metadata enrich: found GitHub URL {github_candidate}")
            else:
                log.info("Metadata enrich: GitHub URL not found.")

    if manual_arxiv:
        metadata["arxiv_id"] = manual_arxiv
        if log:
            log.info("Metadata enrich: use manual arXiv URL.")
    elif not _clean_str(metadata.get("arxiv_id")):
        arxiv_candidate = _search_arxiv_url(metadata.get("title", ""), log=log)
        metadata["arxiv_id"] = arxiv_candidate
        if log:
            if arxiv_candidate:
                log.info(f"Metadata enrich: found arXiv URL {arxiv_candidate}")
            else:
                log.info("Metadata enrich: arXiv URL not found.")

    save_json(
        content_plan,
        Path(output_path) / file_name / "contentPlan" / "final_content_plan.json",
    )
    return content_plan
