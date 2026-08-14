# CLAUDE.md – Arbeitsregeln für IBRT_CCE

**IBRT_CCE** (*Ibert Computational Civil Engineering*): parametrische
Open-Source-FEM-Software für Bauingenieure (Python/PySide6,
Node-Editor, Pynite-Kern, später Kontinuum + KI-Schicht + BIM/IFC).
Vollständige Ziele & Roadmap: @docs/Projektziele_FEM_Software.md

## Session-Ablauf (immer in dieser Reihenfolge)

1. **`STATUS.md` lesen** – dort steht, wo das Projekt steht und was als
   Nächstes ansteht. Nie ohne diesen Kontext loslegen.
2. Aufgabe bestätigen, Annahmen explizit auflisten.
3. Feature-Branch anlegen (siehe @docs/GIT_WORKFLOW.md).
4. Implementieren – bei Mechanik gilt Test-first (siehe unten).
5. Tests + Benchmarks laufen lassen.
6. **`STATUS.md` aktualisieren** (Erledigt / Offen / Nächste Schritte /
   Entscheidungen) – Pflicht am Ende jeder Session.
7. Committen/PR nach @docs/GIT_WORKFLOW.md.

## Eiserne Regeln – Mechanik

- **Keine Mechanik ohne Referenz.** Jede neue Berechnungsfunktion braucht
  VOR der Implementierung eine dokumentierte Referenzlösung (analytische
  Formel, Bautabellen-Wert oder verifizierter Fremdsoftware-Wert) und einen
  Test dagegen. Details: @docs/VALIDATION.md
- **Hinterfragen ist Pflicht.** Jedes Ergebnis aktiv plausibilisieren:
  Größenordnung per Handformel gegenrechnen, Einheiten prüfen,
  Vorzeichenkonvention prüfen, Symmetrien nutzen. Das Ergebnis der
  Plausibilisierung gehört in die Antwort, nicht nur der Code.
- **Zahlen nie behaupten.** Numerische Aussagen ("Durchbiegung = 12,3 mm")
  nur aus tatsächlich ausgeführtem Code, nie aus dem Kopf.
- **Einheiten:** intern strikt SI (N, m, Pa, kg). Umrechnung nur an den
  UI-Rändern. Jede Funktion dokumentiert ihre Einheiten im Docstring.
- **Unsicherheit aussprechen.** Wenn eine mechanische Annahme unsicher ist
  (Lagerungsart, Theorie II. Ordnung nötig?, Schubverformung?):
  Optionen nennen, nicht stillschweigend wählen.

## Eiserne Regeln – Code & Projekt

- Sprache: Kommunikation mit dem Maintainer auf **Deutsch**; Code,
  Kommentare, Docstrings, Commits, Issues auf **Englisch** (Open Source).
- Architektur einhalten: Parametergraph ↔ Solver-Adapter ↔ UI strikt
  getrennt. Kein UI-Code importiert Solver-Interna.
- Datenmodell IFC-mappbar halten (siehe Zieldokument, Grundsatz 7).
- Keine neuen Abhängigkeiten ohne Begründung + Lizenzcheck (GPL-Frage!).
- Kleine, nachvollziehbare Schritte. Lieber 3 kleine PRs als 1 großer.

## Definition of Done

Eine Aufgabe ist erst fertig, wenn: Code + Tests grün + Benchmarks grün +
Docstrings + `STATUS.md` aktualisiert + Commit nach Konvention.

## Verweise

- Ziele & Roadmap: @docs/Projektziele_FEM_Software.md
- Git & PR-Regeln: @docs/GIT_WORKFLOW.md
- Validierung & Benchmarks: @docs/VALIDATION.md
- Aktueller Stand & Übergabe: @STATUS.md
