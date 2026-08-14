# Validierung & Benchmarks – die Mechanik-Wahrheitsprüfung

Grundsatz: **Dieser Software darf man nur glauben, was sie bewiesen hat.**
Jede Berechnungsfunktion existiert erst dann offiziell, wenn ein
automatisierter Test sie gegen eine unabhängige Referenz prüft.

## Warum so streng?

KI-generierter Code kann plausibel aussehen und trotzdem mechanisch falsch
sein (Vorzeichen, Einheiten, Randbedingungen, Elementformulierung). Die
Benchmark-Suite ist die Instanz, die das aufdeckt – nicht das Bauchgefühl
und nicht die KI selbst. Sie läuft bei jedem Push in der CI.

## Referenz-Hierarchie (in dieser Reihenfolge bevorzugen)

1. **Analytische Lösungen** (Baustatik-Formelwerk, z. B. Schneider
   Bautabellen): exakt, unabhängig, zitierfähig.
2. **Konvergenzstudien**: Netzverfeinerung muss gegen die analytische
   Lösung konvergieren (für Kontinuumselemente ab Phase 3).
3. **Patch-Tests**: Elementformulierungen müssen konstante
   Spannungszustände exakt abbilden.
4. **NAFEMS-Benchmarks**: international standardisierte
   FEM-Verifikationsfälle (u. a. die LE-Serie) – das Qualitätsmaß, an dem
   sich auch Aerospace-Software misst; ab Phase 3 Pflichtteil der Suite.
5. **Fremdsoftware-Vergleich**: dokumentierter Vergleichswert aus
   etablierter Software (Version + Modell im Test vermerken).

## Start-Benchmarks (Phase 0, Stabwerke – analytisch exakt)

| ID | System | Referenzlösung | Toleranz |
|---|---|---|---|
| B-001 | Einfeldträger, Gleichlast q | w_max = 5·q·L⁴ / (384·E·I); M_max = q·L²/8 | ≤ 0,1 % |
| B-002 | Kragarm, Einzellast F am Ende | w = F·L³ / (3·E·I); M_Einsp. = −F·L | ≤ 0,1 % |
| B-003 | Einfeldträger, mittige Einzellast | w = F·L³ / (48·E·I); M = F·L/4 | ≤ 0,1 % |
| B-004 | Ebenes 2-Stab-Fachwerk | Stabkräfte aus Knotengleichgewicht (Hand) | ≤ 0,1 % |
| B-005 | Dehnstab unter Normalkraft | Δl = N·L / (E·A) | ≤ 1e-6 (exakt) |

Für Stabwerksmodelle ohne Schubverformung sind FEM-Ergebnisse an den
Knoten theoretisch exakt – Abweichungen deuten immer auf Fehler hin.

## Test-Regeln

- **Test-first bei Mechanik:** Referenz + Test schreiben, dann
  implementieren, bis der Test grün ist.
- **Netzkonvergenz-Pflicht (ab Kontinuum):** Kein Kontinuums-Ergebnis ohne
  dokumentierte Konvergenzstudie. Die App zeigt Netz-Sensitivität offen an,
  statt sie zu verstecken – ein Ergebnis ohne Konvergenznachweis wird als
  „unbestätigt" markiert.
- Jeder Benchmark dokumentiert im Docstring: System, Formel, Quelle,
  Einheiten, Toleranz und *warum* diese Toleranz.
- **Vorzeichenkonvention** einmal zentral definieren (docs/adr/) und in
  jedem Ergebnis-Test mitprüfen.
- **Einheiten-Tests:** mindestens ein Test pro Adapter, der absichtlich
  gemischte Größenordnungen nutzt (mm-Eingabe-Fehler entdecken).
- **Jeder Mechanik-Bug → Regressionstest.** Kein Fix ohne Test, der den
  Bug vorher reproduziert hat.
- Toleranzen dürfen nie stillschweigend aufgeweicht werden; jede Änderung
  einer Toleranz braucht Begründung im PR.

## Plausibilisierungs-Pflicht (für jede Claude-Session)

Zu jedem präsentierten Rechenergebnis gehört eine kurze Gegenrechnung:

1. Größenordnung per Handformel (stimmt die Zehnerpotenz?)
2. Einheiten-Kette explizit (N, m → Ergebnis in m? Pa?)
3. Grenzfall-Check (L → klein, E → groß: verhält sich das Modell richtig?)
4. Symmetrie-Check, wo anwendbar

## Grenzen (ehrlich dokumentiert)

Die Suite beweist Korrektheit **für die getesteten Fälle**, nicht
allgemein. Ergebnisse der Software sind nicht prüffähig im Sinne der
Bauordnung und ersetzen keine Verantwortung eines Tragwerksplaners.
Dieser Hinweis steht auch im README und in der App.
