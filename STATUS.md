# STATUS – Lebendes Übergabedokument

> **Regel:** Diese Datei ist das Erste, was jede neue Session (Claude Code,
> Cowork, Mensch) liest – und das Letzte, was jede Session aktualisiert.
> Sie beantwortet immer: Wo stehen wir? Was ist offen? Was kommt als Nächstes?

**Letzte Aktualisierung:** 2026-08-13 (Session 2) · **Aktuelle Phase:** 0 – Fundament (in Arbeit)
**Repo:** `IBRT_CCE` – Startpaket fertig, Push auf GitHub ausstehend

---

## ✅ Erledigt

- Zieldokument fertig: Vision, Grundsatzentscheidungen, Tech-Stack,
  8-Phasen-Roadmap, BIM/IFC-Strategie (`docs/Projektziele_FEM_Software.md`)
- **Phase-0-Startpaket gebaut und lokal verifiziert** (Python 3.12,
  Pynite 3.0.0): `pyproject.toml`, Paket `ibrt_cce` (core-Datenmodell +
  Pynite-Adapter), CI-Workflow, `.gitignore`, englisches README
- **Benchmarks B-001…B-005 implementiert und GRÜN** (7/7 Tests bestanden,
  ruff sauber). Relative Fehler ≤ 2e-16 (Maschinengenauigkeit), weit unter
  der 0,1-%-Toleranz aus `docs/VALIDATION.md`
- Vorzeichenkonventionen empirisch verifiziert und im Adapter dokumentiert:
  Feldmoment (Durchhang) bei Last in −Y ist in Pynite **negativ**;
  Normalkraft: **Druck positiv**
- Arbeitsregeln für Claude-Sessions definiert (`CLAUDE.md`)
- Git-/GitHub-Workflow definiert (`docs/GIT_WORKFLOW.md`)
- Validierungsstrategie + Start-Benchmarks B-001…B-005 definiert
  (`docs/VALIDATION.md`)

## 🔄 In Arbeit

- Phase 0, Restpunkte: Repo-Push, CI-Verifikation, PySide6-Grundfenster

## ⏭ Nächste Schritte (Phase 0 – Fundament)

1. ZIP entpacken, `git init`, GitHub-Repo `IBRT_CCE` anlegen und pushen;
   prüfen, dass die CI (Actions) grün durchläuft
2. Projektwissen in Claude auf GitHub-Sync umstellen
3. Minimales PySide6-Fenster: Einfeldträger-Parameter (L, q, E, I) →
   Durchbiegung + Momentenlinie als Plot (letzter Phase-0-Meilenstein)
4. Glasbox v0: Systemsteifigkeitsmatrix aus dem Kernel auslesbar machen
   (Adapter hat dafür bereits `kernel_model`-Zugriff)

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
