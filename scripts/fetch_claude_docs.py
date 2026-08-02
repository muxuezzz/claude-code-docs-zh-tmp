#!/usr/bin/env python3
"""
Improved Claude Code documentation fetcher with hierarchical 3-level directory structure.
"""

import requests
import time
from pathlib import Path
from typing import List, Tuple, Set, Optional, Dict
import logging
from datetime import datetime
import sys
import xml.etree.ElementTree as ET
from urllib.parse import urlparse, urljoin
import json
import hashlib
import os
import re
import random
from bs4 import BeautifulSoup

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

# Sitemap URLs to try (in order of preference)
SITEMAP_URLS = [
    "https://code.claude.com/docs/sitemap.xml",
    "https://docs.anthropic.com/sitemap.xml",
    "https://docs.anthropic.com/sitemap_index.xml",
    "https://anthropic.com/sitemap.xml"
]
MANIFEST_FILE = "docs_manifest.json"

HEADERS = {
    'User-Agent': 'Claude-Code-Docs-Fetcher/4.0',
    'Cache-Control': 'no-cache, no-store, must-revalidate',
    'Pragma': 'no-cache',
    'Expires': '0'
}

MAX_RETRIES = 3
RETRY_DELAY = 2
MAX_RETRY_DELAY = 30
RATE_LIMIT_DELAY = 0.5

# Entry point for discovering top-level nav tabs
OVERVIEW_URL = "https://code.claude.com/docs/zh-CN/overview"
BASE_SITE = "https://code.claude.com"


def sanitize_dirname(name: str) -> str:
    """Sanitize a directory/file name: keep Chinese, alphanumeric, replace others with _."""
    name = name.strip()
    # Replace path-unsafe characters
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '_', name)
    name = re.sub(r'\s+', '_', name)
    name = name.strip('._')
    return name or "untitled"


def load_manifest(docs_dir: Path) -> dict:
    """Load the manifest of previously fetched files."""
    manifest_path = docs_dir / MANIFEST_FILE
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text())
            if "files" not in manifest:
                manifest["files"] = {}
            return manifest
        except Exception as e:
            logger.warning(f"Failed to load manifest: {e}")
    return {"files": {}, "last_updated": None}


def save_manifest(docs_dir: Path, manifest: dict) -> None:
    """Save the manifest of fetched files."""
    manifest_path = docs_dir / MANIFEST_FILE
    manifest["last_updated"] = datetime.now().isoformat()

    github_repo = os.environ.get('GITHUB_REPOSITORY', 'ericbuess/claude-code-docs')
    github_ref = os.environ.get('GITHUB_REF_NAME', 'main')

    if not re.match(r'^[\w.-]+/[\w.-]+$', github_repo):
        logger.warning(f"Invalid repository format: {github_repo}, using default")
        github_repo = 'ericbuess/claude-code-docs'

    if not re.match(r'^[\w.-]+$', github_ref):
        logger.warning(f"Invalid ref format: {github_ref}, using default")
        github_ref = 'main'

    manifest["base_url"] = f"https://raw.githubusercontent.com/{github_repo}/{github_ref}/docs/"
    manifest["github_repository"] = github_repo
    manifest["github_ref"] = github_ref
    manifest["description"] = "Claude Code documentation manifest. Keys are relative paths, append to base_url for full URL."
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))


def discover_docs_hierarchy(session: requests.Session) -> List[Dict]:
    """
    三级目录发现（一个函数完成）：

    1. 从 overview 页解析 class 含 nav-tabs 的区域 → 一级目录名 + 对应入口 URL
    2. 对每个一级入口页，解析 class 含 sidebar-group-header 的元素 → 二级目录名
    3. 在对应 ul.sidebar-group 中收集所有子链接 → 最终 markdown 路径信息

    Returns:
        List of dicts:
        {
            "level1": "快速开始",
            "level2": "核心概念",
            "title": "概述",
            "path": "/docs/zh-CN/overview",   # URL path (no .md)
            "url": "https://code.claude.com/docs/zh-CN/overview",
            "md_url": "https://code.claude.com/docs/zh-CN/overview.md",
            "rel_path": "快速开始/核心概念/概述.md"  # local relative path under docs/
        }
    """
    logger.info("Discovering documentation hierarchy (3-level) from nav-tabs + sidebar...")

    results: List[Dict] = []
    seen_paths: Set[str] = set()  # dedupe by URL path

    # ---------- Level 1: nav-tabs ----------
    try:
        resp = session.get(OVERVIEW_URL, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        logger.error(f"Failed to fetch overview page: {e}")
        return results

    nav = soup.find(class_=re.compile(r"\bnav-tabs\b"))
    if not nav:
        logger.error("Could not find nav-tabs on overview page")
        return results

    level1_tabs: List[Tuple[str, str]] = []
    for a in nav.find_all("a", class_=re.compile(r"nav-tabs-item")):
        href = a.get("href", "").strip()
        text = a.get_text(strip=True)
        if not href or not text:
            continue
        full_url = urljoin(BASE_SITE, href)
        level1_tabs.append((text, full_url))
        logger.info(f"  Level1 tab: {text} -> {full_url}")

    if not level1_tabs:
        logger.error("No nav-tabs items found")
        return results

    # ---------- Level 2 + 3: each level1 page's sidebar ----------
    for level1_name, level1_url in level1_tabs:
        logger.info(f"Fetching sidebar for Level1 [{level1_name}]: {level1_url}")
        try:
            r = session.get(level1_url, headers=HEADERS, timeout=30)
            r.raise_for_status()
            page_soup = BeautifulSoup(r.text, "html.parser")
            time.sleep(RATE_LIMIT_DELAY)
        except Exception as e:
            logger.warning(f"  Failed to fetch {level1_url}: {e}")
            continue

        headers_el = page_soup.find_all(class_=re.compile(r"\bsidebar-group-header\b"))
        if not headers_el:
            logger.warning(f"  No sidebar-group-header found on {level1_url}")
            continue

        for header in headers_el:
            level2_name = header.get_text(strip=True)
            if not level2_name:
                continue

            # Find the associated ul.sidebar-group
            ul = header.find_next_sibling("ul", class_=re.compile(r"\bsidebar-group\b"))
            if not ul:
                parent = header.parent
                if parent:
                    ul = parent.find("ul", class_=re.compile(r"\bsidebar-group\b"))
            if not ul:
                logger.debug(f"  No sidebar-group ul after header '{level2_name}'")
                continue

            for li in ul.find_all("li", recursive=False):
                a = li.find("a", href=True)
                if not a:
                    continue
                href = a.get("href", "").strip()
                title = a.get_text(strip=True) or li.get("data-title", "").strip()
                if not href or not title:
                    continue

                # Skip external links (e.g. GitHub CHANGELOG) for hierarchical docs;
                # they can still be handled separately if needed.
                if href.startswith("http") and "code.claude.com" not in href:
                    logger.info(f"  Skip external link: {title} -> {href}")
                    continue

                full_url = urljoin(BASE_SITE, href)
                parsed = urlparse(full_url)
                path = parsed.path
                # Normalize path: strip trailing slash / .html
                if path.endswith(".html"):
                    path = path[:-5]
                if path.endswith("/"):
                    path = path[:-1]

                if path in seen_paths:
                    continue
                seen_paths.add(path)

                # Build relative local path: level1 / level2 / title.md
                safe_l1 = sanitize_dirname(level1_name)
                safe_l2 = sanitize_dirname(level2_name)
                safe_title = sanitize_dirname(title)
                rel_path = f"{safe_l1}/{safe_l2}/{safe_title}.md"

                entry = {
                    "level1": level1_name,
                    "level2": level2_name,
                    "title": title,
                    "path": path,
                    "url": full_url,
                    "md_url": f"{BASE_SITE}{path}.md",
                    "rel_path": rel_path,
                }
                results.append(entry)
                logger.info(f"    [{level1_name}/{level2_name}] {title} -> {rel_path}")

    logger.info(f"Discovered {len(results)} documentation pages in hierarchy")
    return results


def validate_markdown_content(content: str, filename: str) -> None:
    """Validate that content is proper markdown."""
    if not content or content.startswith("<!DOCTYPE") or "<html" in content[:100]:
        raise ValueError("Received HTML instead of markdown")

    if len(content.strip()) < 50:
        raise ValueError(f"Content too short ({len(content)} bytes)")

    lines = content.split("\n")
    markdown_indicators = [
        "# ", "## ", "### ", "```", "- ", "* ", "1. ",
        "[", "**", "_", "> ",
    ]
    indicator_count = 0
    for line in lines[:50]:
        for indicator in markdown_indicators:
            if line.strip().startswith(indicator) or indicator in line:
                indicator_count += 1
                break

    if indicator_count < 3:
        raise ValueError(
            f"Content doesn't appear to be markdown "
            f"(only {indicator_count} markdown indicators found)"
        )


def fetch_markdown_content(entry: Dict, session: requests.Session) -> Tuple[str, str]:
    """
    Fetch markdown content for a hierarchy entry.
    Returns (rel_path, content).
    """
    md_url = entry["md_url"]
    rel_path = entry["rel_path"]

    logger.info(f"Fetching: {md_url} -> {rel_path}")

    for attempt in range(MAX_RETRIES):
        try:
            response = session.get(md_url, headers=HEADERS, timeout=30, allow_redirects=True)

            if response.status_code == 429:
                wait_time = int(response.headers.get("Retry-After", 60))
                logger.warning(f"Rate limited. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue

            response.raise_for_status()
            content = response.text
            validate_markdown_content(content, rel_path)

            logger.info(f"Successfully fetched and validated {rel_path} ({len(content)} bytes)")
            return rel_path, content

        except requests.exceptions.RequestException as e:
            logger.warning(f"Attempt {attempt + 1}/{MAX_RETRIES} failed for {rel_path}: {e}")
            if attempt < MAX_RETRIES - 1:
                delay = min(RETRY_DELAY * (2 ** attempt), MAX_RETRY_DELAY)
                jittered_delay = delay * random.uniform(0.5, 1.0)
                logger.info(f"Retrying in {jittered_delay:.1f} seconds...")
                time.sleep(jittered_delay)
            else:
                raise Exception(f"Failed to fetch {rel_path} after {MAX_RETRIES} attempts: {e}")

        except ValueError as e:
            logger.error(f"Content validation failed for {rel_path}: {e}")
            raise


def content_has_changed(content: str, old_hash: str) -> bool:
    """Check if content has changed based on hash."""
    new_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
    return new_hash != old_hash


def fetch_changelog(session: requests.Session) -> Tuple[str, str]:
    """Fetch Claude Code changelog from GitHub repository."""
    changelog_url = "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md"
    # Put changelog under a top-level virtual category
    rel_path = "快速开始/快速开始/更新日志.md"

    logger.info(f"Fetching Claude Code changelog: {changelog_url}")

    for attempt in range(MAX_RETRIES):
        try:
            response = session.get(changelog_url, headers=HEADERS, timeout=30, allow_redirects=True)

            if response.status_code == 429:
                wait_time = int(response.headers.get("Retry-After", 60))
                logger.warning(f"Rate limited. Waiting {wait_time} seconds...")
                time.sleep(wait_time)
                continue

            response.raise_for_status()
            content = response.text

            header = """# Claude Code Changelog

> **Source**: https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md
>
> This is the official Claude Code release changelog, automatically fetched from the Claude Code repository.

---

"""
            content = header + content

            if len(content.strip()) < 100:
                raise ValueError(f"Changelog content too short ({len(content)} bytes)")

            logger.info(f"Successfully fetched changelog ({len(content)} bytes)")
            return rel_path, content

        except requests.exceptions.RequestException as e:
            logger.warning(f"Attempt {attempt + 1}/{MAX_RETRIES} failed for changelog: {e}")
            if attempt < MAX_RETRIES - 1:
                delay = min(RETRY_DELAY * (2 ** attempt), MAX_RETRY_DELAY)
                jittered_delay = delay * random.uniform(0.5, 1.0)
                logger.info(f"Retrying in {jittered_delay:.1f} seconds...")
                time.sleep(jittered_delay)
            else:
                raise Exception(f"Failed to fetch changelog after {MAX_RETRIES} attempts: {e}")

        except ValueError as e:
            logger.error(f"Changelog validation failed: {e}")
            raise


def save_markdown_file(docs_dir: Path, rel_path: str, content: str) -> str:
    """
    Save markdown content into hierarchical path and return its hash.

    Creates intermediate directories as needed:
      docs/
        快速开始/
          核心概念/
            概述.md
        使用_Claude_Code_构建/
          MCP/
            参考.md
        ...
    """
    file_path = docs_dir / rel_path
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_text(content, encoding="utf-8")
        content_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        logger.info(f"Saved: {rel_path}")
        return content_hash
    except Exception as e:
        logger.error(f"Failed to save {rel_path}: {e}")
        raise


def cleanup_old_files(docs_dir: Path, current_files: Set[str], manifest: dict) -> None:
    """
    Remove only files that were previously fetched but no longer exist.
    Preserves manually added files. Also removes empty directories left behind.
    """
    previous_files = set(manifest.get("files", {}).keys())
    files_to_remove = previous_files - current_files

    for filename in files_to_remove:
        if filename == MANIFEST_FILE:
            continue
        file_path = docs_dir / filename
        if file_path.exists() and file_path.is_file():
            logger.info(f"Removing obsolete file: {filename}")
            file_path.unlink()
            # Clean up empty parent dirs (up to docs_dir)
            parent = file_path.parent
            while parent != docs_dir and parent.exists():
                try:
                    parent.rmdir()  # only succeeds if empty
                    parent = parent.parent
                except OSError:
                    break


def main():
    """Main function with hierarchical 3-level docs layout."""
    start_time = datetime.now()
    logger.info("Starting Claude Code documentation fetch (hierarchical v4.0)")

    github_repo = os.environ.get("GITHUB_REPOSITORY", "ericbuess/claude-code-docs")
    logger.info(f"GitHub repository: {github_repo}")

    docs_dir = Path(__file__).parent.parent / "docs"
    docs_dir.mkdir(exist_ok=True)
    logger.info(f"Output directory: {docs_dir}")

    manifest = load_manifest(docs_dir)

    successful = 0
    failed = 0
    failed_pages = []
    fetched_files: Set[str] = set()
    new_manifest = {"files": {}}

    with requests.Session() as session:
        # ---- Discover 3-level hierarchy in one function ----
        documentation_entries = discover_docs_hierarchy(session)

        if not documentation_entries:
            logger.error("No documentation pages discovered from hierarchy!")
            sys.exit(1)

        # ---- Fetch each page and save under hierarchical path ----
        for i, entry in enumerate(documentation_entries, 1):
            logger.info(
                f"Processing {i}/{len(documentation_entries)}: "
                f"{entry['level1']}/{entry['level2']}/{entry['title']}"
            )

            try:
                rel_path, content = fetch_markdown_content(entry, session)

                old_entry = manifest.get("files", {}).get(rel_path, {})
                old_hash = old_entry.get("hash", "")

                if content_has_changed(content, old_hash):
                    content_hash = save_markdown_file(docs_dir, rel_path, content)
                    logger.info(f"Updated: {rel_path}")
                    last_updated = datetime.now().isoformat()
                else:
                    content_hash = old_hash
                    logger.info(f"Unchanged: {rel_path}")
                    last_updated = old_entry.get("last_updated", datetime.now().isoformat())

                new_manifest["files"][rel_path] = {
                    "level1": entry["level1"],
                    "level2": entry["level2"],
                    "title": entry["title"],
                    "original_url": entry["url"],
                    "original_md_url": entry["md_url"],
                    "hash": content_hash,
                    "last_updated": last_updated,
                }

                fetched_files.add(rel_path)
                successful += 1

                if i < len(documentation_entries):
                    time.sleep(RATE_LIMIT_DELAY)

            except Exception as e:
                logger.error(f"Failed to process {entry.get('path', entry)}: {e}")
                failed += 1
                failed_pages.append(entry.get("path", str(entry)))

        # ---- Changelog (optional, placed under 快速开始) ----
        logger.info("Fetching Claude Code changelog...")
        try:
            rel_path, content = fetch_changelog(session)

            old_entry = manifest.get("files", {}).get(rel_path, {})
            old_hash = old_entry.get("hash", "")

            if content_has_changed(content, old_hash):
                content_hash = save_markdown_file(docs_dir, rel_path, content)
                logger.info(f"Updated: {rel_path}")
                last_updated = datetime.now().isoformat()
            else:
                content_hash = old_hash
                logger.info(f"Unchanged: {rel_path}")
                last_updated = old_entry.get("last_updated", datetime.now().isoformat())

            new_manifest["files"][rel_path] = {
                "level1": "快速开始",
                "level2": "快速开始",
                "title": "更新日志",
                "original_url": "https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md",
                "original_raw_url": "https://raw.githubusercontent.com/anthropics/claude-code/main/CHANGELOG.md",
                "hash": content_hash,
                "last_updated": last_updated,
                "source": "claude-code-repository",
            }

            fetched_files.add(rel_path)
            successful += 1

        except Exception as e:
            logger.error(f"Failed to fetch changelog: {e}")
            failed += 1
            failed_pages.append("changelog")

    # Clean up obsolete files
    cleanup_old_files(docs_dir, fetched_files, manifest)

    # Metadata
    new_manifest["fetch_metadata"] = {
        "last_fetch_completed": datetime.now().isoformat(),
        "fetch_duration_seconds": (datetime.now() - start_time).total_seconds(),
        "total_pages_discovered": len(documentation_entries),
        "pages_fetched_successfully": successful,
        "pages_failed": failed,
        "failed_pages": failed_pages,
        "base_url": BASE_SITE,
        "total_files": len(fetched_files),
        "fetch_tool_version": "4.0-hierarchical",
        "structure": "level1(nav-tabs) / level2(sidebar-group-header) / page.md",
    }

    save_manifest(docs_dir, new_manifest)

    duration = datetime.now() - start_time
    logger.info("\n" + "=" * 50)
    logger.info(f"Fetch completed in {duration}")
    logger.info(f"Discovered pages: {len(documentation_entries)}")
    logger.info(f"Successful: {successful}")
    logger.info(f"Failed: {failed}")

    if failed_pages:
        logger.warning("\nFailed pages (will retry next run):")
        for page in failed_pages:
            logger.warning(f"  - {page}")
        if successful == 0:
            logger.error("No pages were fetched successfully!")
            sys.exit(1)
    else:
        logger.info("\nAll pages fetched successfully!")


if __name__ == "__main__":
    main()
