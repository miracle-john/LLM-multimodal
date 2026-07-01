import json
import os
import re
import subprocess
from pathlib import Path

root = Path(r"c:\Users\USER\Documents\LLM-multimodal")
patterns = [
    (re.compile(r"AIza[0-9A-Za-z\-_]{20,}"), "REDACTED_GEMINI_API_KEY"),
    (re.compile(r"sk-[A-Za-z0-9]{16,}"), "REDACTED_OPENAI_API_KEY"),
    (re.compile(r"AQ\.[A-Za-z0-9._-]{10,}"), "REDACTED_OPENAI_API_KEY"),
    (re.compile(r"ghp_[A-Za-z0-9]{20,}"), "REDACTED_GITHUB_TOKEN"),
    (re.compile(r"github_pat_[A-Za-z0-9_]{20,}"), "REDACTED_GITHUB_PAT"),
]

tracked = subprocess.check_output(["git", "-C", str(root), "ls-files", "-z"], text=True).split("\0")
for rel in tracked:
    if not rel:
        continue
    path = root / rel
    if not path.exists() or path.is_dir() or ".git" in path.parts:
        continue
    try:
        if path.suffix.lower() == ".ipynb":
            try:
                data = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
            except Exception:
                continue
            data = {
                "cells": [],
                "metadata": data.get("metadata", {}),
                "nbformat": 4,
                "nbformat_minor": 5,
            }
            path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        else:
            text = path.read_text(encoding="utf-8", errors="ignore")
            new_text = text
            for pattern, repl in patterns:
                new_text = pattern.sub(repl, new_text)
            if new_text != text:
                path.write_text(new_text, encoding="utf-8")
    except Exception:
        continue
