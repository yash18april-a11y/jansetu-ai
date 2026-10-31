
import csv
import json
import urllib.request
import urllib.error
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SCHEMES_FILE = BASE_DIR / "schemes.json"
REPORT_FILE = BASE_DIR.parent / "scheme_link_report.csv"

def check_url(url):
    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0"}
        )
        with urllib.request.urlopen(request, timeout=10) as response:
            return str(response.status), response.geturl()

    except urllib.error.HTTPError as error:
        return f"HTTP {error.code}", url

    except Exception as error:
        return "CHECK_FAILED", str(error)[:150]


def main():
    schemes = json.loads(SCHEMES_FILE.read_text(encoding="utf-8"))
    results = []
    checked_urls = {}

    for index, scheme in enumerate(schemes, start=1):
        name = scheme["name"]
        url = scheme["official_url"]

        print(f"[{index}/{len(schemes)}] Checking: {name}", flush=True)

        if url not in checked_urls:
            checked_urls[url] = check_url(url)

        status, destination = checked_urls[url]

        results.append({
            "Scheme": name,
            "URL": url,
            "HTTP Status": status,
            "Destination or Error": destination
        })

        print(f"  Result: {status}", flush=True)

    with REPORT_FILE.open("w", newline="", encoding="utf-8-sig") as file:
        writer = csv.DictWriter(file, fieldnames=[
            "Scheme", "URL", "HTTP Status", "Destination or Error"
        ])
        writer.writeheader()
        writer.writerows(results)

    print()
    print("Finished checking", len(results), "scheme entries.")
    print("Report saved to:", REPORT_FILE)


if __name__ == "__main__":
    main()
