# Projektziele: Parametrische Open-Source-FEM-Software für Bauingenieure

**Stand:** August 2026 · **Status:** Zieldefinition abgeschlossen, Phase 0 startbereit
**Projektname:** **IBRT_CCE** – *Ibert Computational Civil Engineering*
(GitHub-Repo: `IBRT_CCE` · Python-Paket: `ibrt_cce` · PyPI: `ibrt-cce`)

---

## 1. Vision

Eine Open-Source-Desktop-Software, die parametrische Tragwerksmodellierung im
Dynamo-/Grasshopper-Stil (visuelle Node-Programmierung) mit echten FEM-Berechnungen
verbindet – ergänzt um eine KI-Schicht, die natürliche Sprache in parametrische
Modelle übersetzt und auf Basis realer Berechnungen Optimierungsvorschläge macht
(z. B. Querschnittswahl bei geänderter Spannweite).

**Leitbeispiel:** Nutzer öffnet ein Brückenmodell, verlängert die Spannweite um 3 m
→ Software rechnet automatisch neu, vergleicht Querschnittsvarianten
(Kasten, Plattenbalken, Spann-T) unter der maßgebenden Einwirkung und schlägt
die mechanisch/wirtschaftlich sinnvollste Variante vor.

**Leitbild „Computational Engineering" (Vorbild: LEAP 71):** Ingenieurwissen
wird als ausführbarer Code kodiert – Designs werden von Algorithmen erzeugt
und von Physik geprüft, statt manuell gezeichnet. Unser Parametergraph ist
genau das im Kleinen: ein wachsendes Computational Engineering Model für den
konstruktiven Ingenieurbau, mit Rückkopplung von Berechnungs-, Optimierungs-
und Validierungsergebnissen ins Modellwissen.

---

## 2. Getroffene Grundsatzentscheidungen

| Frage | Entscheidung |
|---|---|
| Priorität | Schnell nutzbare Software – **fertige Open-Source-Rechenkerne einbinden** statt Solver-Eigenbau |
| Plattform | **Desktop-App**, Python + Qt |
| Nutzerkreis | **Open Source für die Community** (öffentliche Entwicklung von Anfang an) |

**Kompromiss zum Lernziel ("Glasbox-Prinzip"):** Auch wenn fertige Kerne rechnen,
macht die Software Zwischengrößen sichtbar – Elementsteifigkeitsmatrizen,
assemblierte Systemmatrix, Randbedingungseinbau, Gleichungssystem. So bleibt das
ursprüngliche Ziel „FEM-Theorie endlich verstehen" Teil des Produkts und wird
zugleich ein Alleinstellungsmerkmal für Studierende.

---

## 3. Ziele (priorisiert)

1. **Parametrik als Kernprinzip:** Ein Modell ist ein Parametergraph. Jede
   Parameteränderung löst automatische Neuberechnung aus.
2. **Visuelle Node-Programmierung:** Kästchen + Verbindungen (Dynamo-Style) als
   primäre Modellierungsoberfläche; jedes Element (Geometrie, Material, Last,
   Lager, Solver, Auswertung) ist ein Node.
3. **Echte FEM-Ergebnisse:** Erst Materialebene / reine Mechanik (Stabwerke,
   später Kontinuum), keine Normlogik in v1.
4. **Modernes UI mit zwei Render-Modi:** **Analyse-Modus** (präzise:
   Farbskalen, Netz, Zahlenwerte) und **Szenen-Modus** („Videospiel-Look":
   texturierte Bauteile z. B. in rustikaler Betonoptik, grüne Wiese, Himmel,
   Umgebungselemente wie Bach/Gelände) – damit sichtbar wird, dass da eine
   echte Brücke in einer Landschaft steht. Verformungen werden in beiden Modi
   animiert und überhöht dargestellt.
5. **Optimierung & generatives Design auf Basis echter Berechnungen:**
   Parameterstudien und Querschnittsoptimierung unter definierten Lastfällen;
   als Aerospace-Import später Topologieoptimierung (Material folgt dem
   Kraftfluss) – im Bau hochaktuell durch 3D-Betondruck, Materialeinsparung
   und CO₂-Reduktion.
6. **KI-Schicht:** LLM-API übersetzt natürliche Sprache („dreifeldrige
   Spannbetonbrücke, 2 × 10 m, kostengünstig") in einen Parametergraphen und
   stößt Optimierungsläufe an. Die KI erfindet keine Ergebnisse – sie steuert
   nur Parameter; gerechnet wird immer im FEM-Kern.
7. **BIM-Interoperabilität (openBIM):** Maximale Anschlussfähigkeit an andere
   Programme über den IFC-Standard. Implementierungsbasis ist IFC 4.3
   (ISO 16739-1:2024, aktuellste offizielle Version); die Entwicklung von IFC5
   wird aktiv verfolgt, damit die Software zu den ersten gehört, die den
   Nachfolger unterstützen.
8. **Glasbox-Lernmodus:** Zwischenmatrizen und Rechenschritte einsehbar.

## 4. Nicht-Ziele (vorerst)

- Keine Normbemessung (Eurocode etc.) vor Phase 7
- Keine Konkurrenz zu Abaqus/SOFiSTiK/RFEM in Funktionstiefe – Nische ist
  Parametrik + UX + KI + Lehre
- Keine Web-Version, kein Mobile
- Kein Architektur-CAD: Die BIM-Rolle der Software ist das **Fachmodell
  Tragwerk** (Referenzmodelle importieren, Analysemodell exportieren) – keine
  Gebäudemodellierung
- Keine Haftungsübernahme: deutlicher Hinweis, dass Ergebnisse nicht
  prüffähig/normkonform sind (wichtig bei Open-Source-Statiksoftware!)

---

## 5. Tech-Stack

| Baustein | Wahl | Anmerkung |
|---|---|---|
| Sprache | Python ≥ 3.12 | NumPy/SciPy-Ökosystem |
| UI-Framework | PySide6 (Qt for Python) | LGPL, Open-Source-kompatibel |
| Node-Editor | NodeGraphQt (MIT) als Basis, alternativ Ryven | zu evaluieren in Phase 1 |
| 3D-Viewport | PyVista + pyvistaqt (VTK) | Analyse-Modus; Szenen-Modus v1 über VTK-PBR (Texturen, Skybox/HDR-Licht, Bodenfläche) |
| Stabwerks-Kern | **Pynite** (MIT, reines Python, 3D-Rahmen) | gut lesbarer Code → ideal fürs Glasbox-Prinzip |
| Kontinuums-Kern | CalculiX **oder** sfepy/FEniCSx | Phase 3; Lizenzfrage beachten (s. u.) |
| Netzgenerierung | Gmsh (Python-API) | Phase 3 |
| Optimierung | SciPy `optimize`, später pymoo (evolutionär, mehrkriteriell) | Phase 4 |
| KI-Anbindung | LLM-API mit strukturierter JSON-Ausgabe / Function Calling | Phase 5; Provider austauschbar halten |
| Projektformat | eigenes JSON/YAML-Schema (= vollständiger Parametergraph) | reproduzierbare Modelle; bewusst nah an der JSON-Richtung von IFC5/IFCX |
| BIM/IFC | **IfcOpenShell** (LGPL, Python-API) | Basis: IFC 4.3 ADD2 (ISO 16739-1:2024); IFC5 in Beobachtung |
| Versionierung | GitHub-Repo ab Phase 0, CI mit Benchmark-Tests | Open Source von Tag 1 |

**⚠ Lizenz-Entscheidung nötig:** CalculiX und Gmsh sind GPL, Pynite/NodeGraphQt
sind MIT, Qt/PySide6 ist LGPL. Die Wahl der eigenen Lizenz (MIT vs. GPLv3) muss
**vor** dem ersten Release fallen und beeinflusst, wie GPL-Kerne eingebunden
werden (z. B. als externe Prozesse statt als gelinkte Bibliothek).

---

## 6. Architektur-Grundsätze

1. **Strikte Dreiteilung:** Parametergraph (Modell) ↔ Solver-Adapter ↔ UI.
   Kein UI-Code kennt Solver-Interna.
2. **Solver-Adapter-Pattern:** Jeder Rechenkern liegt hinter derselben
   Schnittstelle (`build_model → solve → results`). Kerne sind austauschbar.
3. **Alles ist ein Node.** Auch Solver und Plots.
4. **Reproduzierbarkeit:** Parametersatz + Softwareversion = vollständige,
   erneut ausführbare Modellbeschreibung.
5. **Validierung ist Pflicht:** Jede neue Funktion wird gegen analytische
   Lösungen (Schneider Bautabellen, klassische Benchmarks) oder etablierte
   Software geprüft. Benchmark-Suite läuft in der CI.
6. **KI schlägt vor, Mechanik entscheidet:** LLM-Ausgaben werden ausschließlich
   als Parameter interpretiert und validiert, nie als Rechenergebnis.
7. **IFC-natives Datenmodell:** Kernentitäten (Stab, Querschnitt, Material,
   Last, Lager, Lastfall) werden von Tag 1 so strukturiert, dass sie sich 1:1
   auf IFC-Klassen abbilden lassen – v. a. auf das `IfcStructuralAnalysisModel`
   (das Tragwerks-Analysemodell in IFC). BIM wird nicht nachgerüstet, sondern
   ist Teil des Schemas. Da IFC5 in Richtung eines modularen, JSON-basierten
   Formats (IFCX) entwickelt wird, ist das eigene JSON-Parameterschema
   konzeptionell darauf ausgerichtet.
8. **Ehrliche Schönheit:** Der Szenen-Modus darf die Physik nie verfälschen.
   Verformungen sind real winzig (mm bei m-Spannweiten) und werden deshalb
   überhöht dargestellt – der Überhöhungsfaktor ist dabei **immer sichtbar
   eingeblendet**. Farbskalen bleiben quantitativ, und jede „schöne" Ansicht
   ist per Klick in den Analyse-Modus überführbar.

---

## 7. Roadmap

| Phase | Inhalt | Ergebnis / Meilenstein |
|---|---|---|
| **0 – Fundament** | Repo + CI, PySide6-Grundfenster, Pynite-Adapter, IFC-mappbares Datenschema, parametrischer Einfeldträger per Formular | Durchbiegung & Momentenlinie stimmen mit Handrechnung überein |
| **1 – Node-Editor** | NodeGraphQt-Integration; Nodes: Punkt, Stab, Querschnitt, Material, Last, Lager, Solve, Plot | Fachwerk/Rahmen komplett visuell modellierbar |
| **2 – 3D-Viewport** | PyVista-Einbettung; Analyse-Modus (Verformungen, Schnittgrößen, Farbskalen); Szenen-Modus v1 (Skybox, Boden-/Materialtexturen, PBR-Beleuchtung); animierte, überhöhte Verformung mit sichtbarem Faktor | „Wow-Faktor": Brücke steht sichtbar „in der Landschaft", Ergebnisse live in 3D |
| **3 – Kontinuum** | Gmsh-Meshing, Kontinuums-Adapter (CalculiX/sfepy), Scheiben, Spannungsplots | Materialverhalten auf Elementebene sichtbar |
| **4 – Optimierung** | Parameterstudien, Querschnittsoptimierung, Lastfall-Management; Ausblick: Topologieoptimierung (SIMP) auf Scheibenmodellen | Leitbeispiel „Spannweite +3 m" funktioniert |
| **5 – KI-Schicht** | LLM → Parametergraph, Vorschlagssystem auf Optimierungsbasis | Spracheingabe erzeugt lauffähiges Modell |
| **6 – BIM/IFC** | IfcOpenShell-Anbindung: Geometrie-/Achs-Import aus Architekturmodellen (IFC 4.3), Export des Tragwerksmodells als `IfcStructuralAnalysisModel`, BCF für Issue-Austausch | Roundtrip mit mind. einem externen BIM-Viewer/CAD nachgewiesen |
| **7 – Normen** | Lastkombinationen, erste Eurocode-Nachweise (Stahl, Beton) | bemessungsnahe Aussagen |
| **8 – Community** | Doku, Beispielbibliothek, Plugin-System, buildingSMART-Zertifizierung anstreben, Release ≥ v1.0 | externe Contributor |

---

## 8. Erfolgskriterien

- **v0.1:** Einfeldträger parametrisch, Ergebnisse < 0,1 % Abweichung zur
  analytischen Lösung.
- Jede Phase endet mit einem validierten, dokumentierten Meilenstein.
- Glasbox-Modus zeigt spätestens ab Phase 1 die Systemsteifigkeitsmatrix an.
- Ab Phase 2 ist jedes Modell als Screenshot/Animation „vorzeigbar" (Portfolio).

## 9. Offene Entscheidungen

- [ ] Lizenz (MIT vs. GPLv3) – vor erstem Release
- [ ] Node-Editor: NodeGraphQt vs. Ryven vs. Eigenbau
- [ ] Kontinuums-Kern: CalculiX vs. sfepy vs. FEniCSx
- [ ] KI-Provider & Umgang mit Offline-Betrieb
- [ ] Zeitpunkt des IFC5-Umstiegs (sobald der Standard final ist und
  Toolsupport z. B. in IfcOpenShell existiert)
- [ ] Szenen-Renderer langfristig: reicht VTK-PBR, oder braucht der volle
  „Game-Look" (animiertes Wasser, Vegetation) später einen
  Game-Engine-Viewer (z. B. Godot-/three.js-Export)? Evaluierung in Phase 2
- [ ] Voxel-/Level-Set-Geometrie für generative Formen: PicoGK von LEAP 71
  (Apache 2.0, C#/OpenVDB) als Studienobjekt oder Anbindung evaluieren
  (frühestens Phase 4)
