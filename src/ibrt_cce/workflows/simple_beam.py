"""Simple-beam workflow: the Phase-0 vertical slice.

Builds the parameter model for a simply supported beam under UDL, runs the
Pynite adapter and returns plot-ready arrays plus - living the project's
plausibility duty - the closed-form analytic reference values alongside the
FEM results, so every UI can display "FEM vs. analytic" transparently.

UI-free by design (architecture rule: UI never touches solver internals).
Units: strictly SI in, strictly SI out.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from ibrt_cce.adapters.pynite_adapter import PyniteAdapter
from ibrt_cce.core.model import StructuralModel


@dataclass(frozen=True)
class SimpleBeamInput:
    """Simply supported beam, span L [m], UDL q [N/m] acting in -Y.

    E [Pa], Iz [m^4] govern the bending results; A [m^2], Iy [m^4], J [m^4]
    complete the section definition required by the 3D kernel.
    """

    L: float
    q: float
    E: float
    Iz: float
    A: float = 53.8e-4
    Iy: float = 604e-8
    J: float = 20.1e-8
    G: float = 80.77e9
    nu: float = 0.3
    rho: float = 7850.0


@dataclass(frozen=True)
class SimpleBeamResult:
    """FEM results with analytic companions (all SI).

    Sign conventions follow the adapter docstring: downward deflection and
    sagging moment are negative.
    """

    x: np.ndarray  # sample stations along the beam [m]
    deflection: np.ndarray  # w(x) [m]
    moment: np.ndarray  # Mz(x) [N*m]
    w_mid: float
    m_mid: float
    r_left: float
    w_mid_analytic: float  # -5qL^4/(384 E Iz)
    m_mid_analytic: float  # -qL^2/8
    r_left_analytic: float  # +qL/2
    stiffness_matrix: np.ndarray  # global K (glasbox), shape (n_dof, n_dof)

    @property
    def w_rel_error(self) -> float:
        return abs(self.w_mid - self.w_mid_analytic) / abs(self.w_mid_analytic)

    @property
    def m_rel_error(self) -> float:
        return abs(self.m_mid - self.m_mid_analytic) / abs(self.m_mid_analytic)


def analyze_simple_beam(inp: SimpleBeamInput, n_samples: int = 101) -> SimpleBeamResult:
    """Run the FEM analysis and evaluate deflection/moment at n_samples stations."""
    model = StructuralModel()
    model.add_node("N1", 0.0, 0.0, 0.0)
    model.add_node("N2", inp.L, 0.0, 0.0)
    model.add_material("mat", inp.E, inp.G, inp.nu, inp.rho)
    model.add_section("sec", inp.A, inp.Iy, inp.Iz, inp.J)
    model.add_member("M1", "N1", "N2", "mat", "sec")
    model.add_support("N1", dx=True, dy=True, dz=True, rx=True)
    model.add_support("N2", dy=True, dz=True, rx=True)
    model.add_member_udl("M1", "FY", -inp.q)

    adapter = PyniteAdapter()
    res = adapter.analyze(model)

    x = np.linspace(0.0, inp.L, n_samples)
    deflection = np.array([res.deflection("M1", "dy", xi) for xi in x])
    moment = np.array([res.moment("M1", "Mz", xi) for xi in x])

    # Glasbox: global stiffness matrix straight from the kernel.
    stiffness = np.asarray(
        res.kernel_model.Ke(check_stability=False, sparse=False)
    )

    return SimpleBeamResult(
        x=x,
        deflection=deflection,
        moment=moment,
        w_mid=res.deflection("M1", "dy", inp.L / 2),
        m_mid=res.moment("M1", "Mz", inp.L / 2),
        r_left=res.shear("M1", "Fy", 0.0),
        w_mid_analytic=-5 * inp.q * inp.L**4 / (384 * inp.E * inp.Iz),
        m_mid_analytic=-inp.q * inp.L**2 / 8,
        r_left_analytic=+inp.q * inp.L / 2,
        stiffness_matrix=stiffness,
    )
