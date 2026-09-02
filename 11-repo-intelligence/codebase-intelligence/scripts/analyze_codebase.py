#!/usr/bin/env python3
"""Deep codebase analyzer that writes durable project intelligence artifacts."""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Sequence, Set, Tuple


IGNORE_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".idea",
    ".vscode",
    ".next",
    ".nuxt",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".turbo",
    ".yarn",
    "__pycache__",
    "bin",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "obj",
    "out",
    "site-packages",
    "target",
    "tmp",
    "vendor",
    "venv",
    ".venv",
}

LANGUAGE_BY_EXTENSION = {
    ".py": "Python",
    ".pyi": "Python",
    ".js": "JavaScript",
    ".jsx": "JavaScript",
    ".mjs": "JavaScript",
    ".cjs": "JavaScript",
    ".ts": "TypeScript",
    ".tsx": "TypeScript",
    ".java": "Java",
    ".kt": "Kotlin",
    ".kts": "Kotlin",
    ".go": "Go",
    ".rs": "Rust",
    ".cs": "C#",
    ".fs": "F#",
    ".php": "PHP",
    ".rb": "Ruby",
    ".swift": "Swift",
    ".scala": "Scala",
    ".sql": "SQL",
    ".sh": "Shell",
    ".ps1": "PowerShell",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".json": "JSON",
    ".toml": "TOML",
    ".ini": "Config",
    ".cfg": "Config",
    ".xml": "XML",
    ".html": "HTML",
    ".css": "CSS",
    ".scss": "SCSS",
    ".sass": "SASS",
    ".less": "LESS",
    ".vue": "Vue",
    ".svelte": "Svelte",
    ".md": "Markdown",
    ".dockerfile": "Docker",
}

TEXT_EXTENSIONS = set(LANGUAGE_BY_EXTENSION) | {
    ".env",
    ".gitignore",
    ".editorconfig",
    ".properties",
    ".gradle",
}

MANIFEST_PRIORITY = {
    "package.json": "Node package",
    "pnpm-workspace.yaml": "PNPM workspace",
    "turbo.json": "Turbo repo",
    "nx.json": "Nx repo",
    "pyproject.toml": "Python project",
    "requirements.txt": "Python dependencies",
    "requirements-dev.txt": "Python dev dependencies",
    "Pipfile": "Python Pipenv",
    "poetry.lock": "Poetry lockfile",
    "Cargo.toml": "Rust project",
    "go.mod": "Go module",
    "pom.xml": "Maven project",
    "build.gradle": "Gradle build",
    "build.gradle.kts": "Gradle build",
    "settings.gradle": "Gradle settings",
    "settings.gradle.kts": "Gradle settings",
    "composer.json": "PHP Composer",
    "Gemfile": "Ruby Gemfile",
    "Dockerfile": "Docker build",
    "docker-compose.yml": "Docker Compose",
    "docker-compose.yaml": "Docker Compose",
    "Makefile": "Make build",
    "Procfile": "Procfile",
}

ENTRYPOINT_NAMES = {
    "main.py",
    "app.py",
    "manage.py",
    "server.py",
    "__main__.py",
    "main.ts",
    "main.tsx",
    "main.js",
    "main.jsx",
    "index.ts",
    "index.tsx",
    "index.js",
    "index.jsx",
    "server.ts",
    "server.js",
    "Program.cs",
    "Main.java",
    "main.go",
    "main.rs",
}

JS_EXTENSIONS = (".ts", ".tsx", ".js", ".jsx", ".mjs", ".cjs", ".json")


@dataclass
class ImportRecord:
    kind: str
    spec: str


class CodebaseAnalyzer:
    def __init__(self, root: Path, output_dir: Path, max_files: int = 6000) -> None:
        self.root = root.resolve()
        self.output_dir = output_dir.resolve()
        self.max_files = max_files
        self.output_dir_name = self.output_dir.name if self.output_dir.parent == self.root else None
        self.files: Dict[str, Dict[str, object]] = {}
        self.module_to_path: Dict[str, str] = {}
        self.package_json_data: Dict[str, object] = {}

    def should_skip_dir(self, name: str) -> bool:
        if name in IGNORE_DIRS:
            return True
        if self.output_dir_name and name == self.output_dir_name:
            return True
        return False

    def allow_walk_dir(self, parent: str, name: str) -> bool:
        if self.should_skip_dir(name):
            return False
        candidate = Path(parent) / name
        try:
            candidate.resolve().relative_to(self.root)
        except ValueError:
            return False
        return True

    def analyze(self) -> Dict[str, object]:
        files_truncated = self.collect_files()
        manifests = self.find_manifests()
        frameworks = self.detect_frameworks(manifests)
        entrypoints = self.detect_entrypoints()
        graph = self.build_relationship_graph()
        risks = self.detect_risks(graph, files_truncated)
        summary = self.build_summary(manifests, frameworks, entrypoints, graph, risks, files_truncated)
        report = {
            "artifact_type": "codebase-intelligence",
            "generated_at": utc_now(),
            "project_root": str(self.root),
            "output_dir": str(self.output_dir),
            "summary": summary,
            "languages": self.language_stats(),
            "manifests": manifests,
            "frameworks": frameworks,
            "entrypoints": entrypoints,
            "directories": self.directory_stats(),
            "files": self.top_file_records(),
            "relationships": graph,
            "risks": risks,
        }
        return report

    def collect_files(self) -> bool:
        count = 0
        truncated = False
        for current_root, dirs, files in os.walk(self.root):
            dirs[:] = sorted(d for d in dirs if self.allow_walk_dir(current_root, d))
            for file_name in sorted(files):
                if count >= self.max_files:
                    truncated = True
                    break
                path = Path(current_root) / file_name
                rel_path = path.resolve().relative_to(self.root)
                record = self.build_file_record(rel_path, path)
                self.files[str(rel_path).replace("\\", "/")] = record
                module_name = self.python_module_name(rel_path)
                if module_name:
                    self.module_to_path[module_name] = record["path"]  # type: ignore[index]
                count += 1
            if truncated:
                break
        return truncated

    def build_file_record(self, rel_path: Path, path: Path) -> Dict[str, object]:
        ext = path.suffix.lower()
        name = path.name
        if name == "Dockerfile":
            ext = ".dockerfile"
        language = LANGUAGE_BY_EXTENSION.get(ext, "Other")
        size_bytes = path.stat().st_size
        top_level = rel_path.parts[0] if rel_path.parts else "."
        category = classify_category(rel_path)
        line_count = None
        if is_text_file(path, ext, size_bytes):
            line_count = count_lines(path)
        return {
            "path": str(rel_path).replace("\\", "/"),
            "name": name,
            "extension": ext,
            "language": language,
            "size_bytes": size_bytes,
            "line_count": line_count,
            "top_level": top_level,
            "category": category,
        }

    def find_manifests(self) -> List[Dict[str, object]]:
        manifests: List[Dict[str, object]] = []
        for path_str, record in self.files.items():
            rel_path = Path(path_str)
            name = rel_path.name
            if name in MANIFEST_PRIORITY or rel_path.suffix.lower() in {".csproj", ".sln"}:
                manifest_type = MANIFEST_PRIORITY.get(name)
                if not manifest_type and rel_path.suffix.lower() == ".csproj":
                    manifest_type = "C# project"
                if not manifest_type and rel_path.suffix.lower() == ".sln":
                    manifest_type = "C# solution"
                text = read_text(self.root / rel_path)
                info = {
                    "path": path_str,
                    "type": manifest_type,
                    "top_level": record["top_level"],
                    "signals": manifest_signals(name, text),
                }
                manifests.append(info)
                if name == "package.json":
                    self.package_json_data = parse_package_json(text)
        manifests.sort(key=lambda item: item["path"])  # type: ignore[index]
        return manifests

    def detect_frameworks(self, manifests: Sequence[Dict[str, object]]) -> List[Dict[str, object]]:
        scores: Counter = Counter()
        reasons: Dict[str, List[str]] = defaultdict(list)

        package_deps = set(self.package_json_data.get("dependencies", []))
        package_deps.update(self.package_json_data.get("devDependencies", []))
        if package_deps:
            add_framework_score(scores, reasons, package_deps, "react", {"react", "react-dom"})
            add_framework_score(scores, reasons, package_deps, "nextjs", {"next"})
            add_framework_score(scores, reasons, package_deps, "vue", {"vue"})
            add_framework_score(scores, reasons, package_deps, "angular", {"@angular/core"})
            add_framework_score(scores, reasons, package_deps, "nestjs", {"@nestjs/core"})
            add_framework_score(scores, reasons, package_deps, "express", {"express"})
            add_framework_score(scores, reasons, package_deps, "vite", {"vite"})
            add_framework_score(scores, reasons, package_deps, "svelte", {"svelte"})

        manifest_text = {item["path"]: read_text(self.root / item["path"]) for item in manifests}  # type: ignore[index]
        combined = "\n".join(text.lower() for text in manifest_text.values())
        for framework, needles in {
            "fastapi": ["fastapi"],
            "django": ["django"],
            "flask": ["flask"],
            "pytest": ["pytest"],
            "spring-boot": ["spring-boot", "org.springframework"],
            "dotnet": ["microsoft.aspnetcore", "usewpf", "usewindowsforms"],
            "rust-axum": ["axum"],
            "rust-actix": ["actix-web"],
            "go-gin": ["github.com/gin-gonic/gin"],
            "go-fiber": ["github.com/gofiber/fiber"],
            "docker": ["dockerfile", "docker-compose"],
        }.items():
            hits = [needle for needle in needles if needle in combined]
            if hits:
                scores[framework] += len(hits)
                reasons[framework].append(", ".join(hits))

        for path_str in self.files:
            if path_str.endswith(".vue"):
                scores["vue"] += 1
                reasons["vue"].append(".vue files")
            elif path_str.endswith(".svelte"):
                scores["svelte"] += 1
                reasons["svelte"].append(".svelte files")
            elif path_str.endswith(".tsx"):
                scores["react"] += 1
                reasons["react"].append(".tsx files")

        frameworks = [
            {"name": name, "score": score, "reasons": sorted(set(reasons[name]))}
            for name, score in scores.most_common()
        ]
        return frameworks[:10]

    def detect_entrypoints(self) -> List[Dict[str, object]]:
        entrypoints: List[Dict[str, object]] = []
        if self.package_json_data:
            scripts = self.package_json_data.get("scripts", {})
            if isinstance(scripts, dict):
                entrypoints.append(
                    {
                        "path": "package.json",
                        "kind": "package-scripts",
                        "details": scripts,
                    }
                )

        for path_str, record in self.files.items():
            name = record["name"]
            if name in ENTRYPOINT_NAMES:
                entrypoints.append(
                    {
                        "path": path_str,
                        "kind": "common-entrypoint",
                        "details": {"language": record["language"]},
                    }
                )
            elif path_str.startswith(".github/workflows/"):
                entrypoints.append(
                    {
                        "path": path_str,
                        "kind": "ci-workflow",
                        "details": {},
                    }
                )
            elif name == "Dockerfile":
                entrypoints.append(
                    {
                        "path": path_str,
                        "kind": "docker-build",
                        "details": {},
                    }
                )
        return sorted(entrypoints, key=lambda item: item["path"])

    def build_relationship_graph(self) -> Dict[str, object]:
        resolved_edges: List[Dict[str, str]] = []
        unresolved_internal: Counter = Counter()
        external_imports: Counter = Counter()
        import_totals: Counter = Counter()

        for path_str, record in self.files.items():
            imports = self.extract_imports(Path(path_str), record)
            import_totals[path_str] = len(imports)
            for item in imports:
                target = self.resolve_import(Path(path_str), item)
                if target:
                    resolved_edges.append({"from": path_str, "to": target, "kind": item.kind})
                    continue
                if item.kind in {"python", "js"}:
                    if looks_like_external(item.spec):
                        external_imports[normalize_external_name(item.spec)] += 1
                    else:
                        unresolved_internal[item.spec] += 1
                else:
                    external_imports[normalize_external_name(item.spec)] += 1

        inbound = Counter(edge["to"] for edge in resolved_edges)
        outbound = Counter(edge["from"] for edge in resolved_edges)
        cross_directory = Counter()
        for edge in resolved_edges:
            source_top = edge["from"].split("/", 1)[0]
            target_top = edge["to"].split("/", 1)[0]
            if source_top != target_top:
                cross_directory[f"{source_top} -> {target_top}"] += 1

        cycles = self.detect_cycles(resolved_edges)
        return {
            "resolved_edge_count": len(resolved_edges),
            "resolved_edges_sample": resolved_edges[:200],
            "most_referenced_files": counter_records(inbound),
            "most_connected_files": counter_records(outbound, with_key_name="path"),
            "cross_directory_edges": counter_records(cross_directory, with_key_name="boundary"),
            "external_dependencies": counter_records(external_imports, with_key_name="name"),
            "unresolved_internal_imports": counter_records(unresolved_internal, with_key_name="spec"),
            "cycle_groups": cycles,
            "files_with_most_imports": counter_records(import_totals, with_key_name="path"),
        }

    def extract_imports(self, rel_path: Path, record: Dict[str, object]) -> List[ImportRecord]:
        ext = record["extension"]
        full_path = self.root / rel_path
        text = read_text(full_path)
        if not text:
            return []

        if ext in {".py", ".pyi"}:
            return self.extract_python_imports(rel_path, text)
        if ext in {".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".vue", ".svelte"}:
            return extract_js_imports(text)
        if ext in {".java", ".kt", ".kts", ".scala"}:
            return extract_regex_imports(text, r"^\s*import\s+([A-Za-z0-9_.*]+)", "jvm")
        if ext == ".cs":
            return extract_regex_imports(text, r"^\s*using\s+([A-Za-z0-9_.]+)", "dotnet")
        if ext == ".go":
            return extract_go_imports(text)
        if ext == ".php":
            return extract_regex_imports(text, r"(?:require|include)(?:_once)?\s*\(?\s*['\"]([^'\"]+)['\"]", "php")
        if ext == ".rb":
            return extract_regex_imports(text, r"^\s*require(?:_relative)?\s+['\"]([^'\"]+)['\"]", "ruby")
        return []

    def extract_python_imports(self, rel_path: Path, text: str) -> List[ImportRecord]:
        try:
            tree = ast.parse(text)
        except SyntaxError:
            return extract_regex_imports(text, r"^\s*(?:from|import)\s+([A-Za-z0-9_., ]+)", "python")

        imports: List[ImportRecord] = []
        module_name = self.python_module_name(rel_path)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(ImportRecord("python", alias.name))
            elif isinstance(node, ast.ImportFrom):
                resolved = resolve_python_spec(module_name, rel_path.name == "__init__.py", node.module, node.level)
                if resolved:
                    imports.append(ImportRecord("python", resolved))
                elif node.module:
                    imports.append(ImportRecord("python", node.module))
        return imports

    def resolve_import(self, source: Path, item: ImportRecord) -> Optional[str]:
        if item.kind == "python":
            if item.spec in self.module_to_path:
                return self.module_to_path[item.spec]
            if "." in item.spec:
                parts = item.spec.split(".")
                for size in range(len(parts) - 1, 0, -1):
                    candidate = ".".join(parts[:size])
                    if candidate in self.module_to_path:
                        return self.module_to_path[candidate]
            return None
        if item.kind == "js":
            return resolve_js_spec(self.root, source, item.spec)
        return None

    def python_module_name(self, rel_path: Path) -> Optional[str]:
        if rel_path.suffix.lower() not in {".py", ".pyi"}:
            return None
        parts = list(rel_path.with_suffix("").parts)
        if not parts:
            return None
        if parts[-1] == "__init__":
            parts = parts[:-1]
        return ".".join(parts) if parts else None

    def language_stats(self) -> List[Dict[str, object]]:
        counter = Counter()
        for record in self.files.values():
            language = record["language"]
            if language != "Other":
                counter[language] += 1
        return counter_records(counter, with_key_name="language")

    def directory_stats(self) -> List[Dict[str, object]]:
        counter = Counter(record["top_level"] for record in self.files.values())
        return counter_records(counter, with_key_name="directory")

    def top_file_records(self) -> Dict[str, object]:
        by_size = sorted(
            self.files.values(),
            key=lambda item: int(item["size_bytes"]),  # type: ignore[arg-type]
            reverse=True,
        )[:15]
        by_lines = sorted(
            (item for item in self.files.values() if item["line_count"] is not None),
            key=lambda item: int(item["line_count"]),  # type: ignore[arg-type]
            reverse=True,
        )[:15]
        return {"largest_files": by_size, "longest_files": by_lines}

    def detect_cycles(self, edges: Sequence[Dict[str, str]]) -> List[List[str]]:
        graph: Dict[str, Set[str]] = defaultdict(set)
        for edge in edges:
            graph[edge["from"]].add(edge["to"])
        index = 0
        indices: Dict[str, int] = {}
        lowlink: Dict[str, int] = {}
        stack: List[str] = []
        on_stack: Set[str] = set()
        components: List[List[str]] = []

        def strongconnect(node: str) -> None:
            nonlocal index
            indices[node] = index
            lowlink[node] = index
            index += 1
            stack.append(node)
            on_stack.add(node)

            for neighbor in graph.get(node, ()):
                if neighbor not in indices:
                    strongconnect(neighbor)
                    lowlink[node] = min(lowlink[node], lowlink[neighbor])
                elif neighbor in on_stack:
                    lowlink[node] = min(lowlink[node], indices[neighbor])

            if lowlink[node] == indices[node]:
                component = []
                while stack:
                    member = stack.pop()
                    on_stack.remove(member)
                    component.append(member)
                    if member == node:
                        break
                if len(component) > 1:
                    components.append(sorted(component))

        for node in list(graph):
            if node not in indices:
                strongconnect(node)
        components.sort(key=len, reverse=True)
        return components[:10]

    def detect_risks(self, graph: Dict[str, object], files_truncated: bool) -> List[Dict[str, str]]:
        risks: List[Dict[str, str]] = []
        tests = [record for record in self.files.values() if record["category"] == "test"]
        if not tests:
            risks.append({"severity": "medium", "message": "No obvious automated test files were detected."})

        longest = graph["files_with_most_imports"][0] if graph["files_with_most_imports"] else None  # type: ignore[index]
        if longest and longest["count"] > 30:
            risks.append(
                {
                    "severity": "medium",
                    "message": f"{longest['path']} has unusually high import fan-out ({longest['count']}).",
                }
            )

        if graph["cycle_groups"]:  # type: ignore[index]
            risks.append({"severity": "high", "message": "The dependency graph contains local cycle groups."})

        oversized = [
            record["path"]
            for record in self.files.values()
            if record["line_count"] and int(record["line_count"]) > 1200
        ]
        if oversized:
            risks.append(
                {
                    "severity": "medium",
                    "message": f"Oversized files detected: {', '.join(oversized[:5])}.",
                }
            )

        if files_truncated:
            risks.append(
                {
                    "severity": "medium",
                    "message": f"Analysis hit the file cap ({self.max_files}) and may be incomplete.",
                }
            )
        return risks

    def build_summary(
        self,
        manifests: Sequence[Dict[str, object]],
        frameworks: Sequence[Dict[str, object]],
        entrypoints: Sequence[Dict[str, object]],
        graph: Dict[str, object],
        risks: Sequence[Dict[str, str]],
        files_truncated: bool,
    ) -> Dict[str, object]:
        return {
            "file_count": len(self.files),
            "manifest_count": len(manifests),
            "entrypoint_count": len(entrypoints),
            "frameworks_detected": [item["name"] for item in frameworks[:5]],
            "primary_languages": [item["language"] for item in self.language_stats()[:5]],
            "cross_directory_edge_count": sum(item["count"] for item in graph["cross_directory_edges"][:20]),  # type: ignore[index]
            "cycle_group_count": len(graph["cycle_groups"]),  # type: ignore[arg-type]
            "risk_count": len(risks),
            "files_truncated": files_truncated,
        }


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def is_text_file(path: Path, ext: str, size_bytes: int) -> bool:
    if ext in TEXT_EXTENSIONS:
        return True
    if path.name in {"Dockerfile", "Makefile", "Procfile"}:
        return True
    return size_bytes <= 1024 * 1024 and ext == ""


def count_lines(path: Path) -> int:
    text = read_text(path)
    return text.count("\n") + (1 if text else 0)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        try:
            return path.read_text(encoding="utf-8-sig")
        except UnicodeDecodeError:
            try:
                return path.read_text(encoding="cp1252")
            except UnicodeDecodeError:
                return path.read_text(errors="ignore")


def classify_category(rel_path: Path) -> str:
    parts = {part.lower() for part in rel_path.parts}
    name = rel_path.name.lower()
    if "test" in parts or "tests" in parts or name.startswith("test_") or name.endswith(".spec.ts") or name.endswith(".test.ts"):
        return "test"
    if "docs" in parts or rel_path.suffix.lower() == ".md":
        return "documentation"
    if name in MANIFEST_PRIORITY or rel_path.suffix.lower() in {".csproj", ".sln"}:
        return "manifest"
    if any(part in {"deploy", "deployment", ".github", "terraform", "k8s", "helm"} for part in parts):
        return "infrastructure"
    if any(part in {"config", "configs", "settings"} for part in parts):
        return "config"
    return "source"


def parse_package_json(text: str) -> Dict[str, object]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return {}
    return {
        "name": payload.get("name"),
        "dependencies": sorted((payload.get("dependencies") or {}).keys()),
        "devDependencies": sorted((payload.get("devDependencies") or {}).keys()),
        "scripts": payload.get("scripts") or {},
    }


def manifest_signals(name: str, text: str) -> List[str]:
    lowered = text.lower()
    signals = []
    if name == "package.json":
        payload = parse_package_json(text)
        deps = payload.get("dependencies", [])
        signals.extend(deps[:8] if isinstance(deps, list) else [])
    elif name in {"requirements.txt", "requirements-dev.txt"}:
        signals.extend([line.strip() for line in text.splitlines() if line.strip() and not line.startswith("#")][:8])
    else:
        for needle in ("react", "next", "vue", "fastapi", "django", "flask", "spring", "aspnetcore", "docker"):
            if needle in lowered:
                signals.append(needle)
    return sorted(set(signals))[:10]


def add_framework_score(
    scores: Counter,
    reasons: Dict[str, List[str]],
    dependencies: Set[str],
    framework: str,
    needles: Set[str],
) -> None:
    hits = sorted(needles & dependencies)
    if hits:
        scores[framework] += len(hits)
        reasons[framework].append(", ".join(hits))


def extract_regex_imports(text: str, pattern: str, kind: str) -> List[ImportRecord]:
    matches = re.findall(pattern, text, flags=re.MULTILINE)
    return [ImportRecord(kind, value.strip()) for value in matches if value.strip()]


def extract_js_imports(text: str) -> List[ImportRecord]:
    patterns = [
        r"import\s+[^;\n]*?\s+from\s+['\"]([^'\"]+)['\"]",
        r"export\s+[^;\n]*?\s+from\s+['\"]([^'\"]+)['\"]",
        r"require\(\s*['\"]([^'\"]+)['\"]\s*\)",
        r"import\(\s*['\"]([^'\"]+)['\"]\s*\)",
    ]
    specs: List[ImportRecord] = []
    for pattern in patterns:
        for value in re.findall(pattern, text):
            specs.append(ImportRecord("js", value.strip()))
    return specs


def extract_go_imports(text: str) -> List[ImportRecord]:
    results = []
    block_match = re.findall(r"import\s*\((.*?)\)", text, flags=re.DOTALL)
    for block in block_match:
        for value in re.findall(r"['\"]([^'\"]+)['\"]", block):
            results.append(ImportRecord("go", value.strip()))
    for value in re.findall(r"import\s+['\"]([^'\"]+)['\"]", text):
        results.append(ImportRecord("go", value.strip()))
    return results


def resolve_python_spec(
    module_name: Optional[str],
    is_package_init: bool,
    module: Optional[str],
    level: int,
) -> Optional[str]:
    if not module_name:
        return module
    if level == 0:
        return module
    current_package = module_name if is_package_init else module_name.rsplit(".", 1)[0] if "." in module_name else ""
    parts = current_package.split(".") if current_package else []
    if level > 1:
        parts = parts[: max(0, len(parts) - (level - 1))]
    if module:
        parts.extend(module.split("."))
    return ".".join(part for part in parts if part)


def resolve_js_spec(root: Path, source: Path, spec: str) -> Optional[str]:
    if not spec.startswith("."):
        return None
    source_dir = (root / source).parent
    base = (source_dir / spec).resolve()
    candidates = [base]
    if base.suffix:
        candidates.append(base.with_suffix(base.suffix))
    else:
        for ext in JS_EXTENSIONS:
            candidates.append(base.with_suffix(ext))
        for ext in JS_EXTENSIONS:
            candidates.append(base / f"index{ext}")
    for candidate in candidates:
        if candidate.exists() and candidate.is_file():
            return str(candidate.relative_to(root)).replace("\\", "/")
    return None


def looks_like_external(spec: str) -> bool:
    return not spec.startswith(".")


def normalize_external_name(spec: str) -> str:
    if spec.startswith("@"):
        parts = spec.split("/")
        return "/".join(parts[:2]) if len(parts) >= 2 else spec
    return spec.split("/")[0]


def counter_records(counter: Counter, with_key_name: str = "path") -> List[Dict[str, object]]:
    rows = []
    for key, count in counter.most_common(15):
        rows.append({with_key_name: key, "count": count})
    return rows


def render_markdown(report: Dict[str, object]) -> str:
    summary = report["summary"]
    frameworks = report["frameworks"]
    languages = report["languages"]
    entrypoints = report["entrypoints"]
    directories = report["directories"]
    relationships = report["relationships"]
    risks = report["risks"]

    lines = [
        "# Project Intelligence",
        "",
        f"- Project root: `{report['project_root']}`",
        f"- Generated at: `{report['generated_at']}`",
        "",
        "## Executive Summary",
        "",
        f"- Files analyzed: `{summary['file_count']}`",
        f"- Manifests detected: `{summary['manifest_count']}`",
        f"- Entrypoints detected: `{summary['entrypoint_count']}`",
        f"- Cycle groups: `{summary['cycle_group_count']}`",
        f"- Risk count: `{summary['risk_count']}`",
        "",
        "## Technology Signals",
        "",
    ]
    lines.extend(format_ranked_items(frameworks, "name"))
    lines.append("")
    lines.append("## Primary Languages")
    lines.append("")
    lines.extend(format_ranked_items(languages, "language"))
    lines.append("")
    lines.append("## Entrypoints")
    lines.append("")
    if entrypoints:
        for item in entrypoints[:20]:
            lines.append(f"- `{item['path']}` ({item['kind']})")
    else:
        lines.append("- No obvious entrypoints were detected.")
    lines.append("")
    lines.append("## Top Directories")
    lines.append("")
    lines.extend(format_ranked_items(directories, "directory"))
    lines.append("")
    lines.append("## Most Referenced Files")
    lines.append("")
    lines.extend(format_ranked_items(relationships["most_referenced_files"], "path"))
    lines.append("")
    lines.append("## Cross-Directory Edges")
    lines.append("")
    lines.extend(format_ranked_items(relationships["cross_directory_edges"], "boundary"))
    lines.append("")
    lines.append("## External Dependencies")
    lines.append("")
    lines.extend(format_ranked_items(relationships["external_dependencies"], "name"))
    lines.append("")
    lines.append("## Cycles")
    lines.append("")
    cycles = relationships["cycle_groups"]
    if cycles:
        for group in cycles:
            lines.append(f"- `{', '.join(group)}`")
    else:
        lines.append("- No local dependency cycles were detected in resolved imports.")
    lines.append("")
    lines.append("## Risks")
    lines.append("")
    if risks:
        for risk in risks:
            lines.append(f"- `{risk['severity']}`: {risk['message']}")
    else:
        lines.append("- No major structural risks were flagged by the baseline scan.")
    return "\n".join(lines) + "\n"


def render_memory(report: Dict[str, object]) -> str:
    summary = report["summary"]
    frameworks = [item["name"] for item in report["frameworks"][:5]]
    languages = [item["language"] for item in report["languages"][:5]]
    referenced = report["relationships"]["most_referenced_files"][:8]
    risks = report["risks"][:8]

    lines = [
        "# Project Memory",
        "",
        "Read this file first in future Codex sessions before opening the full report.",
        "",
        f"- Project root: `{report['project_root']}`",
        f"- Last refresh: `{report['generated_at']}`",
        f"- Files analyzed: `{summary['file_count']}`",
        f"- Framework signals: `{', '.join(frameworks) if frameworks else 'none'}`",
        f"- Primary languages: `{', '.join(languages) if languages else 'unknown'}`",
        "",
        "## Important Files",
        "",
    ]
    if referenced:
        for item in referenced:
            lines.append(f"- `{item['path']}` referenced `{item['count']}` times")
    else:
        lines.append("- No strongly referenced files were detected.")
    lines.append("")
    lines.append("## Risks And Follow-Up")
    lines.append("")
    if risks:
        for risk in risks:
            lines.append(f"- `{risk['severity']}`: {risk['message']}")
    else:
        lines.append("- No major risks were flagged by the baseline scan.")
    lines.append("")
    lines.append("## Refresh Rule")
    lines.append("")
    lines.append("- Refresh this bundle after dependency changes, directory moves, or major feature merges.")
    return "\n".join(lines) + "\n"


def format_ranked_items(items: Sequence[Dict[str, object]], key_name: str) -> List[str]:
    if not items:
        return ["- None detected."]
    return [f"- `{item[key_name]}`: `{item['count']}`" for item in items[:15]]


def write_outputs(output_dir: Path, report: Dict[str, object]) -> Tuple[Path, Path, Path]:
    output_dir.mkdir(parents=True, exist_ok=True)
    json_path = output_dir / "project_intelligence.json"
    md_path = output_dir / "project_intelligence.md"
    memory_path = output_dir / "project_memory.md"
    json_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    md_path.write_text(render_markdown(report), encoding="utf-8")
    memory_path.write_text(render_memory(report), encoding="utf-8")
    return json_path, md_path, memory_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Analyze a repository and write durable project intelligence artifacts.")
    parser.add_argument("root", nargs="?", default=".", help="Project root to analyze")
    parser.add_argument(
        "--output-dir",
        default=".codex-project-intel",
        help="Output directory, absolute or relative to the analyzed root",
    )
    parser.add_argument("--max-files", type=int, default=6000, help="Maximum files to analyze before truncation")
    args = parser.parse_args()

    root = Path(args.root).resolve()
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Project root does not exist or is not a directory: {root}")

    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = root / output_dir

    analyzer = CodebaseAnalyzer(root=root, output_dir=output_dir, max_files=args.max_files)
    report = analyzer.analyze()
    json_path, md_path, memory_path = write_outputs(output_dir, report)
    print(json.dumps({"json": str(json_path), "markdown": str(md_path), "memory": str(memory_path)}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
