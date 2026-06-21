#!/usr/bin/env python3
"""Upload a local file to the fal.ai CDN and print its URL.

The gpt-image-2 edit endpoint takes image URLs, not local files, so each source
screenshot must be uploaded first.

Auth: set FAL_KEY in the environment (format "key_id:key_secret"). For files <1 MB you
can instead skip this script and use the `mcp__fal-ai__upload_file` tool with base64.

Usage:  FAL_KEY=... python fal_upload.py "<path-to-screenshot>"
"""
import json, os, sys, mimetypes, urllib.request


def upload(path, token):
    name = os.path.basename(path)
    ctype = mimetypes.guess_type(path)[0] or "application/octet-stream"
    init_req = urllib.request.Request(
        "https://rest.alpha.fal.ai/storage/upload/initiate?storage_type=fal-cdn-v3",
        data=json.dumps({"file_name": name, "content_type": ctype}).encode(),
        headers={"Authorization": f"Key {token}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(init_req) as r:
        init = json.load(r)
    with open(path, "rb") as f:
        body = f.read()
    put_req = urllib.request.Request(
        init["upload_url"], data=body, headers={"Content-Type": ctype}, method="PUT"
    )
    with urllib.request.urlopen(put_req):
        pass
    return init.get("file_url") or init.get("public_url")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("usage: FAL_KEY=... python fal_upload.py <path>")
    tok = os.environ.get("FAL_KEY")
    if not tok:
        sys.exit("Set FAL_KEY in the environment (format key_id:key_secret).")
    print(upload(sys.argv[1], tok))
