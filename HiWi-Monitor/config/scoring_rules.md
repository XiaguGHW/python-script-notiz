# Scoring Rules

## Remote Score (0–5)

- **5** – ausdrücklich Remote/Homeoffice möglich oder nahezu vollständig software-/datenbasiert
- **4** – stark computerbasiert; Hybrid sehr realistisch
- **3** – gemischt: relevante Computerarbeit plus regelmäßige Präsenzanteile
- **2** – überwiegend vor Ort, aber mit einzelnen Auswertungs-/Dokumentationsanteilen
- **1** – Labor, Hardware, Lehre oder Versuch fast vollständig vor Ort
- **0** – ausdrücklich nur vor Ort

## Match Score (0–5)

Bewertet wird die fachliche Nähe zum hinterlegten Profil in `profile/matching_profile.md`.

Besonders positiv:

- Python
- Machine Learning / LLM
- Datenaufbereitung / Klassifikation
- Modellvergleich / Evaluation
- AI / Data Analysis
- ROS2 / Robotik / autonome Navigation
- Simulation / Numerical Methods
- Engineering Data / technische Dokumentation
- Fahrzeugtechnik / Produktion / Automatisierung

## Combined Score

Standardgewichtung:

- Match: 60 %
- Remote: 40 %

`combined = 0.6 * match_score + 0.4 * remote_score`

Bei gleicher Punktzahl wird die neuere und aktuell eindeutig offene Stelle höher gerankt.

## Automatische personalisierte Bewerbungs-E-Mail

Eine auf die konkrete Stelle zugeschnittene deutsche Bewerbungs-/Anfrage-E-Mail wird erzeugt, wenn beide Bedingungen erfüllt sind:

- `Match Score >= 3`
- `Remote Score >= 3`

Der Match Score und der Remote Score bleiben getrennte Kriterien; ein hoher Wert darf einen Wert unter 3 beim anderen Kriterium nicht ausgleichen.

Der Ansprechpartner muss anhand der aktuellen offiziellen Stellenausschreibung oder eines offiziellen Instituts-/Arbeitsgruppenprofils zuverlässig verifiziert werden. Name, Geschlecht, Titel oder E-Mail-Adresse dürfen nicht geraten werden. Wenn keine konkrete Person zuverlässig bestätigt werden kann, wird `Sehr geehrte Damen und Herren` verwendet und die Unsicherheit im Bericht ausdrücklich angegeben. Quelle und offizielle Kontaktangaben werden neben dem E-Mail-Entwurf dokumentiert.

Eine Frage zu Remote/Homeoffice wird als vollständig eigenständiger optionaler Absatz formuliert. Der Absatz darf keine für den restlichen Text notwendigen Übergänge, Pronomen oder Verweise enthalten. Wird er vollständig gelöscht, muss die E-Mail weiterhin sprachlich und inhaltlich geschlossen sowie direkt versandfertig sein.
