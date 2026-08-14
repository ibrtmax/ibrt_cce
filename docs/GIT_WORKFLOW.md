# Git- & GitHub-Workflow

Ziel: Jede Änderung ist nachvollziehbar, geprüft und reproduzierbar.
Gilt für menschliche Contributor und für Claude-Code-Sessions gleichermaßen.

## Repository-Struktur

```
repo-root/
├── CLAUDE.md              # Arbeitsregeln für Claude Code (Repo-Root!)
├── STATUS.md              # Lebendes Übergabedokument
├── README.md              # Englisch, für die Community
├── docs/
│   ├── Projektziele_FEM_Software.md
│   ├── GIT_WORKFLOW.md
│   └── VALIDATION.md
├── src/ibrt_cce/
│   ├── core/              # Parametergraph, Datenmodell (IFC-mappbar)
│   ├── adapters/          # Solver-Adapter (Pynite, später CalculiX/sfepy)
│   ├── nodes/             # Node-Definitionen
│   └── ui/                # PySide6, Viewport
└── tests/
    ├── unit/
    └── benchmarks/        # Mechanik-Validierung (siehe VALIDATION.md)
```

## Branching

- `main` ist geschützt: kein Direkt-Push, nur via Pull Request mit grüner CI.
- Branch-Namen: `feat/<thema>`, `fix/<thema>`, `docs/<thema>`,
  `test/<thema>`, `refactor/<thema>` – kurz, englisch, kebab-case.
- Ein Branch = ein abgeschlossenes Thema. Langlebige Branches vermeiden.

## Commits (Conventional Commits, Englisch)

Format: `<typ>(<bereich>): <beschreibung>`

- Typen: `feat`, `fix`, `docs`, `test`, `refactor`, `chore`, `ci`
- Beispiele:
  - `feat(adapters): add Pynite adapter for 3D frame analysis`
  - `test(benchmarks): add simply supported beam UDL benchmark`
  - `fix(core): correct sign convention for moment results`
- Klein und atomar committen; jede Commit-Message erklärt das *Warum*,
  wenn es nicht offensichtlich ist.

## Pull Requests – Checkliste

Ein PR wird nur gemerged, wenn:

- [ ] CI grün (Lint + Unit-Tests + Benchmark-Suite)
- [ ] Neue Mechanik-Funktionen haben Benchmark-Tests (VALIDATION.md)
- [ ] Keine Verschlechterung bestehender Benchmark-Toleranzen
- [ ] `STATUS.md` aktualisiert
- [ ] Neue Abhängigkeiten: Begründung + Lizenz im PR-Text
- [ ] Docstrings vorhanden (Einheiten dokumentiert!)

## CI (GitHub Actions)

Bei jedem Push/PR laufen automatisch:

1. `ruff` (Lint + Format-Check)
2. `pytest tests/unit`
3. `pytest tests/benchmarks` – die Mechanik-Wahrheitsprüfung
4. (später) Build-Check der Desktop-App

## Releases & Versionierung

- Semantic Versioning: `MAJOR.MINOR.PATCH`
- `v0.1.0` = Abschluss Phase 0 (validierter Einfeldträger)
- Jedes Release: Git-Tag + GitHub-Release mit Changelog
- Changelog wird aus Conventional Commits generiert

## Issues & Milestones

- Pro Roadmap-Phase ein GitHub-Milestone (Phase 0 … Phase 8)
- Aufgaben als Issues mit Labels: `mechanics`, `ui`, `nodes`, `bim`,
  `validation`, `good first issue` (für spätere Community)
- Größere Architektur-Entscheidungen als kurze ADRs
  (Architecture Decision Records) in `docs/adr/` festhalten
