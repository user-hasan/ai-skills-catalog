#!/usr/bin/env python3
"""Collect approved-source update intelligence for a target skill."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen

LIB = Path(__file__).resolve().parents[2] / "_skill-governance" / "python_lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from skill_governance import (  # noqa: E402
    UPDATE_REQUESTS_DIR,
    classify_update_signal,
    default_urls_for_category,
    infer_category_from_skill,
    is_url_allowed,
    load_json,
    load_source_policies,
    log_operation,
    normalize_skill_category,
    utc_now,
    write_json,
    write_registry_entry,
)


def load_request(args) -> dict:
    payload = {}
    if args.input:
        data = load_json(Path(args.input), {})
        if isinstance(data, dict):
            payload.update(data)
    if args.skill:
        payload["skill"] = args.skill
    if args.category:
        payload["category"] = args.category
    if args.topic:
        payload["topic"] = args.topic
    if args.source_url:
        payload["source_urls"] = list(args.source_url)
    return payload


def normalize_text(value: str) -> str:
    text = html.unescape(value)
    text = re.sub(r"<script.*?</script>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<style.*?</style>", " ", text, flags=re.DOTALL | re.IGNORECASE)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def fetch_url(url: str) -> dict:
    request = Request(url, headers={"User-Agent": "CodexSkillUpdater/1.0"})
    with urlopen(request, timeout=20) as response:
        body = response.read().decode("utf-8", errors="ignore")
    title_match = re.search(r"<title>(.*?)</title>", body, re.IGNORECASE | re.DOTALL)
    title = normalize_text(title_match.group(1)) if title_match else url
    text = normalize_text(body)
    excerpt = text[:700]
    return {"url": url, "title": title, "text": excerpt}


def classify_sources(sources: list[dict], category: str) -> list[dict]:
    evidence = []
    for item in sources:
        text = item.get("text", "")
        signal = classify_update_signal(item["url"], text, category)
        evidence.append(
            {
                "url": item["url"],
                "title": item.get("title", item["url"]),
                "signal": signal,
                "excerpt": text[:400],
            }
        )
    return evidence


def runtime_update_notes(evidence: list[dict], category: str) -> dict:
    combined = " ".join(f"{item.get('url', '')} {item.get('title', '')} {item.get('excerpt', '')}" for item in evidence).lower()
    is_openai = category == "openai-codex"
    approval_required = is_openai and any(term in combined for term in ("mcp", "approval", "connector"))
    polling_required = is_openai and any(term in combined for term in ("background", "poll", "asynchronous", "async"))
    schema_required = is_openai and any(term in combined for term in ("structured output", "schema", "json schema"))
    tool_surface = is_openai and any(term in combined for term in ("tool", "computer use", "shell", "remote mcp", "hosted"))
    return {
        "approval_required": approval_required,
        "polling_required": polling_required,
        "schema_adherence_required": schema_required,
        "official_source_required": is_openai,
        "detected_runtime_topics": [
            topic
            for topic, enabled in (
                ("tool-surface", tool_surface),
                ("mcp-approval", approval_required),
                ("background-mode", polling_required),
                ("structured-output", schema_required),
                ("source-discipline", is_openai),
            )
            if enabled
        ],
    }


def render_markdown(skill_name: str, category: str, evidence: list[dict], topic: str) -> str:
    lines = [
        f"# Update Intelligence: {skill_name}",
        "",
        f"- Generated at: `{utc_now()}`",
        f"- Category: `{category}`",
        f"- Topic: `{topic}`",
        "",
        "## Sources",
        "",
    ]
    for item in evidence:
        lines.append(f"- `{item['signal']}` | [{item['title']}]({item['url']})")
    lines.extend(["", "## Notes", ""])
    for item in evidence:
        lines.append(f"- `{item['signal']}`: {item['excerpt'][:220]}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect approved-source update intelligence for a skill.")
    parser.add_argument("--input", help="Optional JSON request")
    parser.add_argument("--skill", help="Skill name override")
    parser.add_argument("--category", help="Category override")
    parser.add_argument("--topic", help="Topic override")
    parser.add_argument("--source-url", action="append", help="Approved source URL override")
    parser.add_argument("--output", default="skill_update_request.json", help="Primary JSON output path")
    args = parser.parse_args()

    request = load_request(args)
    skill_name = str(request.get("skill", "")).strip()
    if not skill_name:
        raise SystemExit("A skill name is required.")
    category = normalize_skill_category(str(request.get("category") or infer_category_from_skill(skill_name)))
    topic = str(request.get("topic", "refresh skill knowledge from approved sources")).strip()
    policies = load_source_policies()
    requested_urls = list(request.get("source_urls", [])) or default_urls_for_category(category, policies)
    if not requested_urls:
        raise SystemExit(f"No approved default URLs configured for category: {category}")

    offline_sources = list(request.get("offline_sources", []))
    source_rows = []
    if offline_sources:
        for item in offline_sources:
            url = item["url"]
            if not is_url_allowed(url, category, policies):
                raise SystemExit(f"URL rejected by allowlist: {url}")
            source_rows.append({"url": url, "title": item.get("title", url), "text": str(item.get("text", ""))})
    else:
        for url in requested_urls:
            if not is_url_allowed(url, category, policies):
                raise SystemExit(f"URL rejected by allowlist: {url}")
            source_rows.append(fetch_url(url))

    evidence = classify_sources(source_rows, category)
    request_id = f"{skill_name}-{utc_now().replace(':', '').replace('-', '')}"
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    source_evidence_path = output_path.parent / "source_evidence.json"
    update_md_path = output_path.parent / "update_intelligence.md"

    source_evidence = {
        "artifact_type": "source-evidence",
        "generated_at": utc_now(),
        "skill": skill_name,
        "category": category,
        "sources": evidence,
    }
    update_request = {
        "artifact_type": "skill-update-request",
        "generated_at": utc_now(),
        "request_id": request_id,
        "target_skill": skill_name,
        "category": category,
        "origin": "skill-knowledge-updater",
        "topic": topic,
        "signal_summary": [item["signal"] for item in evidence],
        "source_policy_status": "approved",
        "source_urls": [item["url"] for item in evidence],
        "proposed_scope": {
            "files": [
                f"C:\\Users\\HASAN\\.agents\\skills\\{skill_name}\\SKILL.md",
                f"C:\\Users\\HASAN\\.agents\\skills\\{skill_name}\\agents\\openai.yaml",
                f"C:\\Users\\HASAN\\.agents\\skills\\{skill_name}\\references",
                f"C:\\Users\\HASAN\\.agents\\skills\\{skill_name}\\scripts"
            ],
            "shared_dependency_declared": False
        },
        "recommended_action": "Review source evidence, refresh target skill guidance, and keep changes scoped to the skill directory.",
        "runtime_update_notes": runtime_update_notes(evidence, category),
    }

    write_json(source_evidence_path, source_evidence)
    update_md_path.write_text(render_markdown(skill_name, category, evidence, topic), encoding="utf-8")
    write_json(output_path, update_request)
    if request.get("side_effects_enabled", True):
        write_json(UPDATE_REQUESTS_DIR / f"{request_id}.json", update_request)
        write_registry_entry(
            skill_name,
            {
                "last_update_intelligence": update_request["generated_at"],
                "last_update_category": category,
                "last_update_request_id": request_id,
            },
        )
        log_operation("skill-knowledge-updater", "collect-update-intelligence", skill_name, "completed", {"output": str(output_path)})
    print(output_path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
