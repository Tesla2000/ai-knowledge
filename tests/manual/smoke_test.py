"""
Manual smoke test: deploys must be live before running this.
Usage: python tests/manual/smoke_test.py [--api-url https://...]
"""

import argparse
import json
import logging
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")
_logger = logging.getLogger(__name__)

TF_DIR = Path(__file__).parent.parent.parent / "terraform"

SAMPLE_PAYLOAD = {
    "race": "Human",
    "class_": "Fighter",
    "level": 1,
}


def get_api_url() -> str:
    result = subprocess.run(
        ["terraform", f"-chdir={TF_DIR}", "output", "-raw", "api_url"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def run_smoke_test(api_url: str) -> None:
    url = f"{api_url.rstrip('/')}/create_character"
    body = json.dumps(SAMPLE_PAYLOAD).encode()
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    _logger.info("POST %s", url)
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            status = resp.status
            raw = resp.read()
    except urllib.error.HTTPError as exc:
        status = exc.code
        raw = exc.read()

    _logger.info("Status: %s", status)

    if status != 200:
        _logger.error("FAIL — expected 200, got %s", status)
        _logger.error("%s", raw.decode(errors="replace"))
        sys.exit(1)

    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        _logger.error("FAIL — response is not valid JSON")
        _logger.error("%s", raw.decode(errors="replace"))
        sys.exit(1)

    if not data:
        _logger.error("FAIL — response JSON is empty")
        sys.exit(1)

    _logger.info("PASS")
    _logger.info("%s", json.dumps(data, indent=2)[:500])


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--api-url", default=None, help="Override API Gateway URL")
    args = parser.parse_args()

    api_url = args.api_url or get_api_url()
    run_smoke_test(api_url)


if __name__ == "__main__":
    main()
