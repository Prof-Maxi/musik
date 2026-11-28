# Produktionsplan ZDF-Wahlwerbespot · Technik, Modelle, Kosten, Rechte
Stand: 28.11.2026

## 1. Technischer Status
| Komponente | Status |
|---|---|
| FFmpeg 6.1, Node 22, Python 3, Chromium mit Playwright | vorhanden (bewährte Pipeline aus dem Stiftungsspot: HTML/Canvas → Playwright-Frames → FFmpeg) |
| Netzwerkfreigabe für higgsfield.ai, docs, api, platform, mcp, cloud | in der Umgebung „Werbespot-Produktion (Musik)“ eingetragen |
| Higgsfield-Connector (MCP) | **fehlt.** Muss in claude.ai hinzugefügt werden, siehe Abschnitt 2 |
| Sprecherstimme | Entscheidung offen, siehe Abschnitt 5 |
| Musik | Entscheidung offen, siehe Abschnitt 6 |
| Wahlplakate (Corporate Design) | **fehlen.** Die drei Plakate wurden nicht mitgeliefert |

## 2. Higgsfield-Anbindung (offizieller Weg)
Higgsfield betreibt einen gehosteten MCP-Server unter `https://mcp.higgsfield.ai/mcp`.
Für Claude im Web und in der Desktop-App ist der offizielle Weg ein **eigener Connector**.
Für eine lokale Claude-Code-Installation empfiehlt Higgsfield die CLI (`@higgsfield/cli`). In dieser Cloud-Sitzung ist der Connector der richtige Weg, denn eine lokale CLI-Anmeldung über den Browser ist hier nicht möglich.

Schritte für die Nutzerin bzw. den Nutzer:
1. Ein Higgsfield-Konto mit **bezahltem Plan** anlegen. Generierungen über MCP verbrauchen die Credits des Kontos.
2. Auf https://claude.ai/customize/connectors die Option **„Benutzerdefinierten Connector hinzufügen“** wählen.
   Name: `Higgsfield`, URL: `https://mcp.higgsfield.ai/mcp`
3. Im Anmeldefenster bei Higgsfield einloggen und den Zugriff erlauben.
4. **Eine neue Claude-Code-Sitzung** mit der Umgebung „Werbespot-Produktion (Musik)“ und dem Repository `Prof-Maxi/musik` starten, denn Connectoren werden beim Sitzungsstart geladen.
   Dort genügt: *„Setze die ZDF-Produktion fort, siehe zdf-wahlwerbespot-2026/README.md.“*

## 3. Modellwahl (vorläufig, wird gegen die Live-Liste des Connectors geprüft)
| Einsatz | Modell | Begründung |
|---|---|---|
| Dialogszenen mit Lippenbewegung (S2-01, S3-02, S5-05) | **Google Veo 3.1** (Bild-zu-Video mit nativem Ton) | erzeugt Bild und Sprache gemeinsam lippensynchron, sehr realistische Menschen. Die O-Ton-Stimme kann bei Bedarf durch die Sprecherstimme ersetzt werden |
| Hero-Fahrzeuge, Drohnen- und Tracking-Shots, Architektur (S1-06, S2-02, S3-01, S7-01, S7-04) | **Seedance 2.0** | sehr präzise Kamerafahrten, Reflexionen, filmischer Look |
| B-Roll und Montage-Shots (22 Einstellungen) | **Kling 3.0** | gute Physik und Bewegung, sehr günstig pro Clip, ideal für Schnitte von 1–2 s |
| Referenzbilder für Figurenkonstanz | **Nano Banana Pro** bzw. **Higgsfield Soul** | derselbe Kandidat in allen Szenen; Clips entstehen als Bild-zu-Video aus diesen Referenzen |
| Texte, Logos, Zahlen, Diagramme | **kein Videomodell**: eigenes Motion Design (HTML/Canvas/SVG → Playwright → FFmpeg) | gestochen scharf und exakt im CD |

## 4. Kostenschätzung Higgsfield
Die Credit-Preise stammen aus Drittquellen vom Herbst 2026 und schwanken je nach Quelle.
**Vor jeder Generierung lese ich die Live-Preise über den Connector aus und lege dir die genaue Summe zur Freigabe vor.**

| Posten | Anzahl | Credits je Stück (geschätzt) | Summe |
|---|---|---|---|
| Referenzbilder | 3 | ~4 | ~12 |
| Kling 3.0, 5 s, 1080p | 22 | ~8–15 | ~264 |
| Seedance 2.0, 5 s, 1080p | 5 | ~45–60 | ~250 |
| Veo 3.1, 8 s mit Ton (je 2 Varianten der 3 Dialogszenen) | 6 | ~60–80 | ~420 |
| **Summe** | 36 | | **~950** |
| Puffer für Nachgenerierungen (+25 %) | | | **~1.200** |

Sparvariante: zunächst nur eine Variante pro Dialogszene und eine zweite nur bei Bedarf. Das ergibt ca. **740 Credits**, mit Puffer ca. **900 Credits**.
Plan-Richtwerte (Drittquellen): Starter ca. 19 USD für 270 Credits (zu klein, ohne Seedance 2.0), **Plus ca. 59 USD für 1.200 Credits (passt)**.
Ein Monat Plus genügt also voraussichtlich. Credits verfallen am Monatsende.

## 5. Sprecherstimme (Off-Sprecher, männlich, tief, trocken, leicht arrogant)
| Option | Qualität | Kosten | Rechte |
|---|---|---|---|
| **A · ElevenLabs** (Empfehlung) | Spitzenklasse auf Deutsch, Regie über Pausen und Betonung | Starter ca. 5–6 USD pro Monat, reicht für Sprecher und Musik | ab Starter kommerzielle Lizenz |
| B · Higgsfield Audio (TTS) | gut, falls über den Connector verfügbar | Higgsfield-Credits | laut Higgsfield-AGB |
| C · Open Source (Piper „Thorsten“, wie beim Stiftungsspot) | deutlich synthetischer, für Luxuswerbung grenzwertig | kostenlos | frei |

Für ElevenLabs braucht diese Umgebung einen API-Schlüssel für `api.elevenlabs.io`. Ich frage ihn über das sichere Formular ab, er erscheint nie im Chat.

## 6. Musik und Nutzungsrechte
Die Wunschtitel (AC/DC, ATB, Pink Floyd, Tiësto, ABBA, Frank Ocean, Moloko) sind urheberrechtlich geschützt.
Für eine Nutzung im Spot wären Synchronisations- und Masterrechte nötig. § 60a UrhG deckt nur die Vorführung im Unterricht, keine Veröffentlichung (Schulhomepage, Social Media, Schulversammlung mit Publikum).
Ich lade außerdem keine geschützten Aufnahmen aus dem Netz herunter.

**Empfehlung: ein eigener Originaltrack mit vollen Rechten** in drei Teilen auf 124 BPM:
1. **A (0:00–0:13):** ernste Wahlkampfmusik mit Klavier und Streichern
2. **Drop (0:16,5):** Motorstart, dann luxuriöser Deep-/Electro-House mit Bläser-Stabs (Gefühl von „The Business“ bzw. „9 PM“, ohne zu kopieren). Bei Szene 5 kommt eine Warteschleifen-Parodie, danach der Re-Drop
3. **C (ab 1:42):** episch-hybrides Finale mit Logo-Hit und Nachhall

Umsetzung: **ElevenLabs Music** (ca. 900 Credits pro Minute, im Starter-Kontingent enthalten) in mehreren Stems bzw. Abschnitten, die ich selbst schneide, auf den Takt lege und mit Sidechain-Ducking unter die Stimme mische.
Alternative ohne Zusatzkosten: eine eigene Synthese wie beim Stiftungsspot, klanglich aber schwächer.
Falls Originalsongs gewünscht sind: Ich baue eine separate **Unterrichtsfassung**, in die du eine rechtmäßig erworbene Audiodatei einspielst. Sie ist nur zur Vorführung im Klassenraum bestimmt.

## 7. Mischung und Ausgabe
- Stimme −16 LUFS integriert, Musik in Sprachpassagen −10 bis −14 dB unter der Stimme (Sidechain), True Peak ≤ −1 dBTP
- Ausgabe 1920 × 1080, 30 fps, H.264 High, AAC 320 kbit/s, 48 kHz. Optional 4K-Upscale der Higgsfield-Clips
- Einheitliches Farbgrading aller Clips mit FFmpeg (Navy-Schatten, Gold-Lichter), dazu leichtes Korn über alles als „Kinokamera-Kitt“

## 8. Arbeitsablauf
1. ✅ Werkzeuge prüfen, Netzwerk freigeben, Higgsfield-Weg recherchieren
2. ✅ Drehbuch v1, Timeline, Shotliste mit Prompts, Kostenschätzung
3. ⏳ Plakate analysieren → CD-Tokens (Farben, Schrift, Wortmarke), Wortmarke als Vektor nachbauen
4. ⏳ Sprecher und Musik erzeugen → Timeline auf echte Satzlängen und Takte festzurren
5. ⏳ Motion Design: Szene 4 (Grafiken), Szene 6 (Programm), Szene 8 (Finale), Bauchbinden, Fußnoten
6. ⏳ **Nach Kostenfreigabe:** Referenzbilder → Dialogszenen → Hero-Shots → B-Roll
7. ⏳ Schnitt, Grading, Sounddesign, Mischung, Qualitätskontrolle, finales MP4
