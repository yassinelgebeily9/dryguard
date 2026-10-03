"""Restore both pinned data subsets, verifying each unique file's Git blob hash."""
import concurrent.futures
import hashlib
import json
import ssl
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen

import certifi

ROOT = Path(__file__).resolve().parents[1]


def git_blob_sha(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def main():
    # The matched subset reuses four original files; download each local path once.
    items = {}
    for manifest_path in ["data/manifest.json", "data/matched/manifest.json"]:
        manifest = json.loads((ROOT / manifest_path).read_text())
        repo = manifest["repository"].removeprefix("https://github.com/")
        for item in manifest["files"]:
            entry = {**item, "repository": repo, "commit": manifest["commit"]}
            previous = items.get(item["local_path"])
            if previous is not None:
                for field in ["source_path", "blob_sha", "size_bytes", "repository", "commit"]:
                    if previous[field] != entry[field]:
                        raise ValueError(f"Conflicting manifests: {item['local_path']}")
            items[item["local_path"]] = entry

    # Use a maintained CA bundle, including on Python installations without OS certificates.
    context = ssl.create_default_context(cafile=certifi.where())

    def download(item):
        target = ROOT / item["local_path"]
        if target.exists():
            cached = target.read_bytes()
            if len(cached) == item["size_bytes"] and git_blob_sha(cached) == item["blob_sha"]:
                return "cached"
        url = f"https://raw.githubusercontent.com/{item['repository']}/{item['commit']}/{quote(item['source_path'])}"
        request = Request(url, headers={"User-Agent": "dryguard-learning-project"})
        with urlopen(request, context=context, timeout=60) as response:
            data = response.read()
        if len(data) != item["size_bytes"] or git_blob_sha(data) != item["blob_sha"]:
            raise ValueError(f"Source verification failed: {item['source_path']}")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
        return "downloaded"

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(download, items.values()))
    print(f"Verified {len(results)} unique source files ({results.count('downloaded')} downloaded).")


if __name__ == "__main__":
    main()
