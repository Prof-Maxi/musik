# ZDF – Zukunftsbündnis Digitaler Fortschritt · „The Wealth Campaign 2026“
Satirischer Wahlwerbespot einer **fiktiven Schulpartei** für den Sozialkundeunterricht.
Slogan: *Digital denken. Zukunft lenken.* Kein Bezug zum Zweiten Deutschen Fernsehen.

## Stand (28.11.2026)
Die Planung ist abgeschlossen, die Produktion wartet auf Zugänge und Dateien.
- `00_planung/Drehbuch.md`: Drehbuch v1 mit Timeline (ca. 2:14), Pointen-Timing und Reserve-Gags
- `00_planung/shotlist.json`: 30 Higgsfield-Einstellungen mit Prompts, Modellwahl, Figurenbeschreibungen und Credit-Schätzung
- `00_planung/Produktionsplan.md`: Higgsfield-Anbindung, Modellwahl, Kosten, Stimme, Musikrechte, Mischung

## Übergabe an die nächste Sitzung
Die nächste Sitzung braucht den Higgsfield-Connector (`https://mcp.higgsfield.ai/mcp`, als eigener Connector in claude.ai hinzugefügt).
Danach:
1. Higgsfield-Live-Modellliste und -Preise lesen und die Shotliste anpassen. Der Nutzerin bzw. dem Nutzer die exakte Credit-Summe zur Freigabe vorlegen.
2. Plakate aus `01_corporate-design/plakate/` analysieren und `brand`-Tokens festlegen.
3. Sprecher und Musik erzeugen (Entscheidung in `Produktionsplan.md` Abschnitt 5/6), Timeline auf die echten Längen festzurren.
4. Motion Design bauen. Werkzeuge wie in `../werbespot-schoene-stiftung/_werkzeuge/` (HTML/Canvas → Playwright → FFmpeg).
5. Generieren, schneiden, mischen und rendern nach `05_final/`.

## Ordner (geplant)
`00_planung` · `01_corporate-design` · `02_higgsfield` (Clips, nicht im Repository) · `03_voiceover` · `04_musik` · `05_final` · `_werkzeuge`
