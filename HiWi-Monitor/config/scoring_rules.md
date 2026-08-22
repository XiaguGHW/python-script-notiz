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
