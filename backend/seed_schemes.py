
"""Import reviewed government schemes into JanSetu AI.

New records remain unpublished until explicitly verified.
Run inside the backend Docker container.
"""

import json
from pathlib import Path

from app import create_app
from app.extensions import db
from app.models import Scheme
from app.engine import SUPPORTED

DATA_FILE = Path(__file__).with_name("schemes.json")


def main():
    if not DATA_FILE.exists():
        print("schemes.json not found.")
        return

    records = json.loads(DATA_FILE.read_text(encoding="utf-8"))

    if not isinstance(records, list):
        raise ValueError("schemes.json must contain a JSON array")

    app = create_app()

    added = 0
    skipped = 0

    with app.app_context():
        for item in records:
            name = str(item.get("name", "")).strip()
            description = str(item.get("description", "")).strip()
            category = str(item.get("category", "")).strip()
            official_url = str(item.get("official_url", "")).strip()
            rules = item.get("rules", {})

            if not all([name, description, category, official_url]):
                raise ValueError("Scheme has missing required fields")

            if not official_url.startswith("https://"):
                raise ValueError(f"Official HTTPS URL required: {name}")

            if not isinstance(rules, dict):
                raise ValueError(f"Rules must be an object: {name}")

            unsupported = set(rules) - SUPPORTED

            if unsupported:
                raise ValueError(
                    f"{name}: unsupported eligibility rules {unsupported}"
                )

            existing = Scheme.query.filter_by(name=name).first()

            if existing:
                print(f"Skipped existing scheme: {name}")
                skipped += 1
                continue

            scheme = Scheme(
                name=name,
                description=description,
                category=category,
                official_url=official_url,
                rules=rules,
                active=False,
                source_verified_at=None,
            )

            db.session.add(scheme)
            added += 1

            print(f"Added draft scheme: {name}")

        db.session.commit()

    print()
    print("Import completed successfully.")
    print(f"New schemes added: {added}")
    print(f"Existing schemes skipped: {skipped}")
    print("New schemes remain unpublished until reviewed.")


if __name__ == "__main__":
    main()