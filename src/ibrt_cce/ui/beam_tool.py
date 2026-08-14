"""IBRT_CCE beam tool - the first window (Phase 0 milestone).

A deliberately small PySide6 app: enter L, q, E, Iz (engineering units),
get deflection and moment diagrams plus a transparent "FEM vs. analytic"
readout, and open the glasbox to inspect the global stiffness matrix.

Unit conversion to SI happens ONLY here, at the UI boundary
(engineering units in the form: m, kN/m, GPa, cm^2, cm^4).
"""

from __future__ import annotations

import sys

import numpy as np
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDoubleSpinBox,
    QFormLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from ibrt_cce import __version__
from ibrt_cce.workflows.simple_beam import SimpleBeamInput, analyze_simple_beam

# UI -> SI conversion factors.
KNM_TO_NM = 1e3  # kN/m -> N/m
GPA_TO_PA = 1e9
CM2_TO_M2 = 1e-4
CM4_TO_M4 = 1e-8


class StiffnessDialog(QDialog):
    """Glasbox: shows the global stiffness matrix with a hand-check line."""

    def __init__(self, K: np.ndarray, hand_check: str, parent: QWidget | None = None):
        super().__init__(parent)
        self.setWindowTitle("Glasbox - global stiffness matrix K")
        layout = QVBoxLayout(self)
        layout.addWidget(
            QLabel(
                f"K is {K.shape[0]}x{K.shape[1]} (2 nodes x 6 DOF: "
                "DX, DY, DZ, RX, RY, RZ per node), units N, m, rad.\n"
                f"Hand check: {hand_check}"
            )
        )
        text = QPlainTextEdit(self)
        text.setReadOnly(True)
        text.setFont(QFont("Courier New", 9))
        text.setPlainText(
            np.array2string(K, precision=3, max_line_width=200, suppress_small=True)
        )
        text.setMinimumSize(720, 380)
        layout.addWidget(text)


class BeamToolWindow(QMainWindow):
    """Main window of the Phase-0 simple-beam tool."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"IBRT_CCE {__version__} - Simple Beam (Phase 0)")
        self._result = None

        # -- input form (engineering units) -------------------------------
        self.in_L = self._spin(0.5, 100.0, 6.0, " m", 2)
        self.in_q = self._spin(0.1, 1000.0, 10.0, " kN/m", 2)
        self.in_E = self._spin(1.0, 500.0, 210.0, " GPa", 1)
        self.in_Iz = self._spin(1.0, 1e7, 8356.0, " cm4", 0)
        self.in_A = self._spin(0.1, 1e5, 53.8, " cm2", 1)

        form_box = QGroupBox("Simply supported beam - UDL (no self-weight)")
        form = QFormLayout(form_box)
        form.addRow("Span L", self.in_L)
        form.addRow("Load q", self.in_q)
        form.addRow("Modulus E", self.in_E)
        form.addRow("Inertia Iz", self.in_Iz)
        form.addRow("Area A", self.in_A)

        self.btn_run = QPushButton("Analyze")
        self.btn_run.clicked.connect(self.run_analysis)
        self.btn_glasbox = QPushButton("Glasbox: show K matrix")
        self.btn_glasbox.clicked.connect(self.show_glasbox)
        self.btn_glasbox.setEnabled(False)

        self.lbl_results = QLabel("Enter parameters and press Analyze.")
        self.lbl_results.setTextInteractionFlags(Qt.TextSelectableByMouse)

        left = QVBoxLayout()
        left.addWidget(form_box)
        left.addWidget(self.btn_run)
        left.addWidget(self.lbl_results)
        left.addWidget(self.btn_glasbox)
        left.addStretch(1)
        left_w = QWidget()
        left_w.setLayout(left)
        left_w.setMaximumWidth(340)

        # -- plots --------------------------------------------------------
        self.figure = Figure(figsize=(6.5, 5.5), layout="constrained")
        self.canvas = FigureCanvasQTAgg(self.figure)
        self.ax_w = self.figure.add_subplot(211)
        self.ax_m = self.figure.add_subplot(212, sharex=self.ax_w)

        root = QHBoxLayout()
        root.addWidget(left_w)
        root.addWidget(self.canvas, stretch=1)
        container = QWidget()
        container.setLayout(root)
        self.setCentralWidget(container)
        self.resize(1080, 620)

    @staticmethod
    def _spin(lo: float, hi: float, value: float, suffix: str, decimals: int) -> QDoubleSpinBox:
        box = QDoubleSpinBox()
        box.setRange(lo, hi)
        box.setValue(value)
        box.setSuffix(suffix)
        box.setDecimals(decimals)
        return box

    # -- actions ----------------------------------------------------------

    def run_analysis(self) -> None:
        inp = SimpleBeamInput(
            L=self.in_L.value(),
            q=self.in_q.value() * KNM_TO_NM,
            E=self.in_E.value() * GPA_TO_PA,
            Iz=self.in_Iz.value() * CM4_TO_M4,
            A=self.in_A.value() * CM2_TO_M2,
        )
        res = analyze_simple_beam(inp)
        self._result = res

        self.lbl_results.setText(
            "Midspan deflection w:\n"
            f"  FEM      {res.w_mid * 1e3:10.4f} mm\n"
            f"  analytic {res.w_mid_analytic * 1e3:10.4f} mm"
            f"   (dev {res.w_rel_error:.2e})\n"
            "Midspan moment M (sagging neg.):\n"
            f"  FEM      {res.m_mid / 1e3:10.3f} kNm\n"
            f"  analytic {res.m_mid_analytic / 1e3:10.3f} kNm"
            f"   (dev {res.m_rel_error:.2e})\n"
            f"Support reaction R = {res.r_left / 1e3:.2f} kN"
        )
        self.btn_glasbox.setEnabled(True)
        self._draw(res)

    def _draw(self, res) -> None:
        self.ax_w.clear()
        self.ax_m.clear()

        self.ax_w.plot(res.x, res.deflection * 1e3, color="#1f77b4", lw=2)
        self.ax_w.axhline(0, color="black", lw=0.8)
        self.ax_w.set_ylabel("w [mm]")
        self.ax_w.set_title("Deflection")
        self.ax_w.grid(True, alpha=0.3)

        # Structural convention: plot moments on the tension side (down).
        self.ax_m.plot(res.x, res.moment / 1e3, color="#d62728", lw=2)
        self.ax_m.fill_between(res.x, res.moment / 1e3, 0, color="#d62728", alpha=0.15)
        self.ax_m.axhline(0, color="black", lw=0.8)
        self.ax_m.set_ylabel("Mz [kNm]  (tension side down)")
        self.ax_m.set_xlabel("x [m]")
        self.ax_m.set_title("Bending moment")
        self.ax_m.grid(True, alpha=0.3)

        self.canvas.draw_idle()

    def show_glasbox(self) -> None:
        if self._result is None:
            return
        K = self._result.stiffness_matrix
        # Hand check straight from theory: K[DY1, DY1] = 12 E Iz / L^3.
        e_si = self.in_E.value() * GPA_TO_PA
        iz_si = self.in_Iz.value() * CM4_TO_M4
        l_si = self.in_L.value()
        expected = 12 * e_si * iz_si / l_si**3
        hand = (
            f"K[1,1] (DY at node 1) = {K[1, 1]:.4e} N/m vs. "
            f"12*E*Iz/L^3 = {expected:.4e} N/m"
        )
        StiffnessDialog(K, hand, self).exec()


def main() -> int:
    app = QApplication(sys.argv)
    window = BeamToolWindow()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
