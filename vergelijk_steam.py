"""Vergelijk in Nederland verkrijgbare pc-basisspellen met Steam-activatie."""
import argparse
import csv
from datetime import datetime, timedelta, timezone
from decimal import Decimal
import json
import re
import sys
from urllib.request import Request, urlopen

BASE = "https://gocdkey.nl"
DEFAULT_SLUGS = ("battlefield-6", "dispatch", "wardogs")


def steam_prijzen(data):
    peiltijd = datetime.fromisoformat(data["generated_at"].replace("Z", "+00:00"))
    goedkoopste = {}
    for aanbod in data["offers"]:
        soort = aanbod.get("type")
        if soort not in ("officieel", "keyshop") or not aanbod.get("stock_confirmed"):
            continue
        if (aanbod.get("activation") or "").strip().lower() != "steam":
            continue
        if not aanbod.get("checked_at") or aanbod.get("price_eur") is None:
            continue
        tijd = datetime.fromisoformat(aanbod["checked_at"].replace("Z", "+00:00"))
        if not peiltijd - timedelta(hours=24) <= tijd <= peiltijd:
            continue
        bedrag = Decimal(str(aanbod["price_eur"]))
        if bedrag <= 0:
            continue
        eerder = goedkoopste.get(soort)
        winkel = aanbod["store"]
        if eerder is None or bedrag < eerder[0]:
            goedkoopste[soort] = (bedrag, {winkel})
        elif bedrag == eerder[0]:
            eerder[1].add(winkel)
    return goedkoopste


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("slug", nargs="*", help="Slug van een pc-game, bijvoorbeeld dispatch")
    args = parser.parse_args()
    out = csv.writer(sys.stdout)
    out.writerow(["slug", "peiltijd_utc", "type", "prijs_eur", "winkels", "bron"])
    for slug in dict.fromkeys(args.slug or DEFAULT_SLUGS):
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", slug):
            parser.error("Ongeldige slug: " + slug)
        req = Request(f"{BASE}/api/v1/games/{slug}.json", headers={"User-Agent": "Gocdkey-prijsonderzoek/1.0"})
        try:
            with urlopen(req, timeout=15) as response:
                data = json.load(response)
        except (OSError, ValueError) as exc:
            print(f"{slug}: ophalen mislukt ({exc})", file=sys.stderr)
            return 1
        if data.get("platform") != "PC":
            print(f"{slug}: geen bevestigde pc-versie", file=sys.stderr)
            continue
        for soort, (bedrag, winkels) in sorted(steam_prijzen(data).items()):
            out.writerow([slug, data["generated_at"], soort, format(bedrag, ".2f"), " / ".join(sorted(winkels)), data["url"]])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
