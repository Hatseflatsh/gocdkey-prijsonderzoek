#!/usr/bin/env python3
"""Neem de vaste groep van twaalf edities opnieuw op via de openbare GoCDKey-API."""
import argparse
import csv
import json
import re
import time
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path
from urllib.request import Request, urlopen

SITE = 'https://gocdkey.nl'
SPELEN = [
    'battlefield-6', 'battlefield-6-xbox',
    'cyberpunk-2077', 'cyberpunk-2077-xbox',
    'farming-simulator-25', 'farming-simulator-25-xbox',
    'hogwarts-legacy', 'hogwarts-legacy-xbox',
    'kerbal-space-program', 'assetto-corsa',
    'assetto-corsa-competizione-xbox', 'forza-horizon-6-xbox',
]
VELDEN = ['slug', 'titel', 'platform', 'bronpagina', 'bron_api', 'opgehaald_utc',
          'bron_gegenereerd_utc', 'winkel', 'winkeltype', 'prijs_eur', 'activatie',
          'regio', 'editie', 'voorraad_bevestigd', 'winkel_gecontroleerd_utc']


def utc(timestamp):
    # Python 3.9 vereist precies zes cijfers bij sommige fracties van een seconde.
    iso = re.sub(r'\.(\d+)', lambda m: '.' + m[1][:6].ljust(6, '0'), timestamp.replace('Z', '+00:00'))
    datum = datetime.fromisoformat(iso)
    if datum.tzinfo is None:
        raise ValueError('Tijdzone ontbreekt in brondatum')
    return datum.astimezone(timezone.utc).isoformat(timespec='seconds').replace('+00:00', 'Z')


def neem_op(slug):
    api = f'{SITE}/api/v1/games/{slug}.json'
    request = Request(api, headers={'Accept': 'application/json', 'User-Agent': 'GoCDKey-open-data/1.0'})
    with urlopen(request, timeout=30) as antwoord:
        bron = json.load(antwoord, parse_float=Decimal)
    opgehaald = utc(datetime.now(timezone.utc).isoformat())
    pagina = f'{SITE}/game/{slug}'
    if bron['slug'] != slug or bron['url'] != pagina or bron['is_free']:
        raise ValueError(f'Onverwacht catalogusrecord voor {slug}')
    rijen = []
    for aanbod in bron['offers']:
        prijs = Decimal(aanbod['price_eur'])
        if not prijs.is_finite() or prijs < 0:
            raise ValueError(f'Ongeldig tarief voor {slug}')
        rijen.append(dict(slug=slug, titel=bron['title'], platform=bron['platform'],
            bronpagina=pagina, bron_api=api, opgehaald_utc=opgehaald,
            bron_gegenereerd_utc=utc(bron['generated_at']), winkel=aanbod['store'],
            winkeltype=aanbod['type'], prijs_eur=f'{prijs:.2f}',
            activatie=aanbod.get('activation') or '', regio=aanbod.get('region') or '',
            editie=aanbod.get('edition') or '', voorraad_bevestigd={True: 'ja', False: 'nee'}[aanbod['stock_confirmed']],
            winkel_gecontroleerd_utc=utc(aanbod['checked_at']) if aanbod.get('checked_at') else ''))
    return rijen


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('bestand', type=Path, help='Nieuw CSV-bestand, bijvoorbeeld aanbiedingen-nieuw.csv')
    doel = parser.parse_args().bestand
    if doel.exists():
        parser.error(f'Kies een nieuw bestand. {doel} bestaat al.')
    alles = []
    for n, slug in enumerate(SPELEN):
        if n:
            time.sleep(1.25)
        alles.extend(neem_op(slug))
    with doel.open('x', encoding='utf-8', newline='') as out:
        writer = csv.DictWriter(out, fieldnames=VELDEN)
        writer.writeheader()
        writer.writerows(alles)
    print(f'{len(SPELEN)} edities opgenomen, {len(alles)} winkelrijen in {doel}.')


if __name__ == '__main__':
    main()
