import os
import json
import yaml
import markdown
from pathlib import Path
from typing import List, Dict, Any

def load_markdown_file(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        raw_text = f.read()
    html = markdown.markdown(raw_text)
    return {
        "text": raw_text,
        "html": html,
        "metadata": {"source": str(path)}
    }

def load_yaml_file(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return {
        "text": json.dumps(data),
        "metadata": {"source": str(path)}
    }

def load_json_file(path: Path) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {
        "text": json.dumps(data),
        "metadata": {"source": str(path)}
    }

def ingest_data(data_dir: str) -> List[Dict[str, Any]]:
    records = []
    for root, _, files in os.walk(data_dir):
        for filename in files:
            path = Path(root) / filename
            if filename.endswith(".md"):
                records.append(load_markdown_file(path))
            elif filename.endswith(".yaml") or filename.endswith(".yml"):
                records.append(load_yaml_file(path))
            elif filename.endswith(".json"):
                records.append(load_json_file(path))
    return records

if __name__ == "__main__":
    # Example usage
    data = ingest_data("data")
    print(f"Ingested {len(data)} records.")
