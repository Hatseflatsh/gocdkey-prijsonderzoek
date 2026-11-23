# Nederlandse pc-gameprijzen vergelijken met dezelfde activatie

Hoeveel verschilt een Steam-aankoop bij een officiële winkel van een Steam-sleutel bij een keyshop? Met dit Python-script kun je de prijsvergelijking uit ons onderzoek opnieuw uitvoeren. Het script gebruikt alleen de standaardbibliotheek van Python 3.9 of hoger. De uitkomst is een CSV-bestand met tijdstip, laagste aanbiedingsprijs per winkelsoort, alle winkels die die prijs delen en de bronpagina.

    python3 vergelijk_steam.py > peiling.csv
    python3 vergelijk_steam.py dispatch battlefield-6

## Peiling van 20 november 2026

| Basisspel voor pc | Officiële winkel met Steam-activatie | Keyshop met Steam-activatie | Verschil |
| --- | --- | --- | --- |
| [Battlefield 6](https://gocdkey.nl/game/battlefield-6) | € 23,09 bij Steam | € 17,58 bij CJS CD Keys | € 5,51 |
| [Dispatch](https://gocdkey.nl/game/dispatch) | € 28,99 bij Steam | € 21,22 bij CJS CD Keys | € 7,77 |
| [WARDOGS](https://gocdkey.nl/game/wardogs) | € 32,66 bij Zapagames | € 23,20 bij CJS CD Keys | € 9,46 |

Peiltijd 02.45 uur Nederlandse tijd. De drie spellen zijn gekozen als voorbeelden. Er is geen gemiddelde voor de Nederlandse markt afgeleid. De winkel kan de prijs daarna wijzigen of bij het afrekenen een toeslag rekenen. [Redactionele uitleg en voorgaande peiling](https://gocdkey.nl/blog/steam-activatie-pc-prijzen-november-2026)

## Welke aanbiedingen tellen mee?

Per spel lezen we de lijst voor het basisspel. Uitbreidingen en apart gerangschikte edities vallen buiten de selectie. De vermelding moet Steam expliciet als activatieplatform noemen, de voorraad bevestigen en een positieve europrijs dragen die binnen 24 uur vóór het genereren van de gegevens is gecontroleerd. Bij een gedeelde minimumprijs blijven alle winkelnamen zichtbaar. Als geen aanbieding aan de criteria voldoet, verschijnt er voor die winkelsoort geen rij. Extra kortingscodes passen we in dit script niet toe.

De gegevens komen van Gocdkey.nl en zijn afkomstig uit winkelprijzen, IsThereAnyDeal en productfeeds van keyshops. Gebruik bij herpublicatie de bronpagina van de betreffende game en het peilmoment. [Openbare API, velden en bronvermelding](https://gocdkey.nl/data)

## Pc en Xbox op 23 november 2026

De nieuwe meting bevat vier spellen op beide platforms plus vier afzonderlijke edities. De twaalf prijskaarten laten per winkel de basisprijs, activatie, regio en controletijd zien. [Lees de bevindingen en bekijk alle winkelrijen](metingen/2026-11-23/README.md).
