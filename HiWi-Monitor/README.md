# HiWi Monitor

Dieses Projekt dient als dauerhafter, zustandsbehafteter Monitor für HiWi-Stellen an der Universität Stuttgart.

## Ziel

Bei jedem manuellen Update werden die Fakultäten F01, F02, F03, F04, F05, F06, F07, F08 und F10 erneut geprüft. Gesucht werden neue oder veränderte HiWi-/SHK-/WHK-/studentische Hilfskraft-Stellen, die seit dem letzten Scan noch nicht erfasst wurden.

## Ausführungsbefehl

**HiWi Update**

Dieser Befehl bedeutet:

1. vorhandene Datenbank unter `data/known_jobs.json` lesen;
2. offizielle Fakultäts- und Institutsseiten prüfen;
3. Stellenangebote-/Karriere-/HiWi-Seiten direkt prüfen;
4. zusätzlich gezielte Websuche als Fallback verwenden;
5. PDF-Ausschreibungen vollständig prüfen;
6. neue, geänderte und verschwundene Stellen mit dem bisherigen Stand vergleichen;
7. Remote-/Homeoffice-Eignung und Profil-Match bewerten;
8. einen aktuellen Bericht für alle 9 Fakultäten erzeugen;
9. neue Stellen in `data/known_jobs.json` eintragen;
10. Scan-Verlauf aktualisieren.

## Ordner

- `config/` – Fakultäten, Scanregeln und Bewertungsregeln
- `data/` – bekannte Stellen und Scanstatus
- `profile/` – Profil zur Match-Bewertung
- `reports/` – Ausgaben einzelner Scans
- `../HiWi/` – bestehende ausführliche Markdown-Dateien zu bereits geprüften Stellen

## Grundprinzip

Nicht nur Suchmaschinen verwenden. Primär werden offizielle Uni-/Institutsseiten geprüft; Suchmaschinen dienen nur als Ergänzung. Ein fehlender Suchtreffer bedeutet nicht automatisch, dass keine Stelle existiert.
