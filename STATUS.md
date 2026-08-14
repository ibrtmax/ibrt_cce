# STATUS – Lebendes Übergabedokument

> **Regel:** Diese Datei ist das Erste, was jede neue Session (Claude Code,
> Cowork, Mensch) liest – und das Letzte, was jede Session aktualisiert.
> Sie beantwortet immer: Wo stehen wir? Was ist offen? Was kommt als Nächstes?

**Letzte Aktualisierung:** 2026-08-14 (Session 3) · **Aktuelle Phase:** 0 – Fundament (Abschluss-PR offen)
**Repo:** `github.com/ibrtmax/ibrt_cce` – main gepusht, CI grün (Run #1, 31 s)

---

## ✅ Erledigt

- Zieldokument fertig: Vision, Grundsatzentscheidungen, Tech-Stack,
  8-Phasen-Roadmap, BIM/IFC-Strategie (`docs/Projektziele_FEM_Software.md`)
- **Phase-0-Startpaket gebaut und lokal verifiziert** (Python 3.12,
  Pynite 3.0.0): `pyproject.toml`, Paket `ibrt_cce` (core-Datenmodell +
  Pynite-Adapter), CI-Workflow, `.gitignore`, englisches README
- **Benchmarks B-001…B-005 implementiert und GRÜN** (jetzt 8/8 Tests,
  ruff sauber). Relative Fehler ≤ 2e-16 (Maschinengenauigkeit), weit unter
  der 0,1-%-Toleranz aus `docs/VALIDATION.md`; von GitHub-CI unabhängig
  bestätigt (Python 3.11 + 3.12)
- **Erstes UI fertig (v0.1.0):** PySide6-Fenster `ibrt-beam` – Eingaben in
  Ingenieureinheiten (Umrechnung nur am UI-Rand), Biegelinie +
  Momentenlinie (Zugseite unten), FEM-vs.-Analytik-Anzeige mit
  Abweichung, **Glasbox v0** (globale K-Matrix mit Handformel-Check
  K[1,1] = 12·E·Iz/L³); offscreen getestet inkl. Screenshot
- Workflows-Schicht eingeführt (`ibrt_cce.workflows`, UI-frei, testbar)
- CI-Actions auf checkout@v5/setup-python@v6 gehoben (Node-20-Warnung
  behoben); `.gitattributes` erzwingt LF im Repo (CRLF-Warnungen erledigt)
- Vorzeichenkonventionen empirisch verifiziert und im Adapter dokumentiert:
  Feldmoment (Durchhang) bei Last in −Y ist in Pynite **negativ**;
  Normalkraft: **Druck positiv**
- Arbeitsregeln für Claude-Sessions definiert (`CLAUDE.md`)
- Git-/GitHub-Workflow definiert (`docs/GIT_WORKFLOW.md`)
- Validierungsstrategie + Start-Benchmarks B-001…B-005 definiert
  (`docs/VALIDATION.md`)

## 🔄 In Arbeit

- Abschluss-PR Phase 0: `feat/phase0-beam-ui` (UI + Workflows + Fixes,
  Paket liegt als ZIP vor, Merge durch Maintainer ausstehend)

## ⏭ Nächste Schritte (Phase 0 – Fundament)

1. PR `feat/phase0-beam-ui` erstellen, CI abwarten, mergen
2. GitHub-Release **v0.1.0** taggen → Phase 0 offiziell abgeschlossen
3. Projektwissen in Claude auf GitHub-Sync umstellen
4. Phase 1 starten: Node-Editor-Basis evaluieren (NodeGraphQt vs. Ryven)
   und Grund-Nodes definieren (Punkt, Stab, Querschnitt, Material, Last,
   Lager, Solve, Plot)

## ⚠ Offene Fragen & Blocker

- Lizenz MIT vs. GPLv3 (vor erstem Release; beeinflusst CalculiX/Gmsh-Einbindung)
- Projektweite Vorzeichenkonvention für Schnittgrößen als ADR festlegen
  (aktuell: dokumentierte Pynite-Konvention im Adapter)
- Generische Member-End-Releases im Core-Modell (aktuell nur `truss`-Flag)
- Node-Editor-Basis: NodeGraphQt vs. Ryven (Entscheidung erst Phase 1 nötig)

## 📌 Entscheidungs-Log

| Datum | Entscheidung | Begründung |
|---|---|---|
| 2026-08 | Fertige Rechenkerne statt Solver-Eigenbau | Schneller nutzbar; Lernziel über Glasbox-Prinzip |
| 2026-08 | Desktop-App, Python + PySide6 | s. Zieldokument |
| 2026-08 | Open Source, Entwicklung öffentlich ab Tag 1 | Community-Ziel |
| 2026-08 | IFC 4.3 als BIM-Basis, Datenmodell IFC5/IFCX-ready | Zukunftssicherheit |
| 2026-08 | Kommunikation Deutsch, Code/Commits/Doku Englisch | Community-Anschluss |
| 2026-08 | Zwei Render-Modi: Analyse + Szene („Game-Look") | Wow-Faktor & Lehre, ohne Präzision zu opfern; Überhöhungsfaktor immer sichtbar |
| 2026-08 | Leitbild „Computational Engineering" (Vorbild LEAP 71) | Wissen als Code; Aerospace-V&V-Qualität (NAFEMS, Konvergenzpflicht); Topologieoptimierung als Ausbaustufe |
| 2026-08-13 | Projektname: **IBRT_CCE** (Ibert Computational Civil Engineering) | PyPI (`ibrt-cce`) und GitHub geprüft und frei; keine Namenskollision im Software-/Baubereich; Python-Paket `ibrt_cce` |
| 2026-08-13 | Pynite auf `>=3.0,<4` gepinnt | Adapter gegen 3.0.0 verifiziert; API änderte sich zwischen Major-Versionen |
| 2026-08-13 | Ergebnis-Konvention Phase 0 = dokumentierte Pynite-Konvention | Empirisch verifiziert (B-001…B-005); eigene IBRT-Konvention als ADR offen |
| 2026-08-14 | UI spricht nur mit `workflows`, nie mit Adaptern direkt | Architektur-Regel 1 durchgesetzt; Workflows bleiben ohne Qt testbar |
| 2026-08-14 | „FEM vs. analytisch" wird im UI immer mit angezeigt | Plausibilisierungspflicht als sichtbares Produktmerkmal (Lehre!) |

---

## Vorlage für Session-Abschluss (kopieren & ausfüllen)

```
**Letzte Aktualisierung:** JJJJ-MM-TT · **Phase:** X · **Branch:** ...
✅ Erledigt: ...
🔄 In Arbeit (inkl. halbfertiger Stellen im Code!): ...
⏭ Nächste Schritte: ...
⚠ Neue offene Fragen/Blocker: ...
📌 Neue Entscheidungen (mit Begründung): ...
```
