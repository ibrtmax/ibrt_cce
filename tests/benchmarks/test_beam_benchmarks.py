"""Mechanics truth suite: benchmarks B-001...B-005 (docs/VALIDATION.md).

Every case checks the Pynite adapter against a closed-form analytic
solution from classical beam/truss theory (cf. standard structural
engineering references, e.g. Schneider Bautabellen). For frame models
without shear deformation these solutions are exact, so tolerances are
tight by design and must never be loosened silently.

Units: SI (m, N, Pa). Sign conventions: see adapters/pynite_adapter.py.
"""

from __future__ import annotations

import math

import pytest

from ibrt_cce.adapters.pynite_adapter import PyniteAdapter
from ibrt_cce.core.model import StructuralModel

# Relative tolerances per docs/VALIDATION.md.
RTOL_BEAM = 1e-3  # 0.1 % ceiling for beam benchmarks
RTOL_EXACT = 1e-9  # machine-level agreement expected

# Steel-like reference material, SI.
E = 210e9
G = 80.77e9
NU = 0.3
RHO = 7850.0

# IPE300-like section, SI (values only need to be consistent, not normative).
A = 53.8e-4
IY = 604e-8
IZ = 8356e-8
J = 20.1e-8


def _material_and_section(model: StructuralModel) -> None:
    model.add_material("steel", E, G, NU, RHO)
    model.add_section("sec", A, IY, IZ, J)


def _relative_error(value: float, reference: float) -> float:
    return abs(value - reference) / abs(reference)


def test_b001_simply_supported_beam_udl() -> None:
    """B-001: simply supported beam, span L, UDL q (load in -Y).

    Analytic: w(L/2) = -5*q*L^4 / (384*E*Iz)
              Mz(L/2) = -q*L^2 / 8   (sagging negative, adapter convention)
              Fy(0)   = +q*L / 2     (left support shear)
    """
    L, q = 6.0, 10e3
    model = StructuralModel()
    model.add_node("N1", 0, 0, 0)
    model.add_node("N2", L, 0, 0)
    _material_and_section(model)
    model.add_member("M1", "N1", "N2", "steel", "sec")
    model.add_support("N1", dx=True, dy=True, dz=True, rx=True)
    model.add_support("N2", dy=True, dz=True, rx=True)
    model.add_member_udl("M1", "FY", -q)

    res = PyniteAdapter().analyze(model)

    w_ref = -5 * q * L**4 / (384 * E * IZ)
    m_ref = -q * L**2 / 8
    v_ref = +q * L / 2
    assert _relative_error(res.deflection("M1", "dy", L / 2), w_ref) < RTOL_BEAM
    assert _relative_error(res.moment("M1", "Mz", L / 2), m_ref) < RTOL_BEAM
    assert _relative_error(res.shear("M1", "Fy", 0.0), v_ref) < RTOL_BEAM


def test_b002_cantilever_tip_load() -> None:
    """B-002: cantilever, fixed at N1, point load F in -Y at the free tip.

    Analytic: w(L) = -F*L^3 / (3*E*Iz)
              |Mz(0)| = F*L  (fixed-end moment magnitude)
    """
    L, F = 3.0, 25e3
    model = StructuralModel()
    model.add_node("N1", 0, 0, 0)
    model.add_node("N2", L, 0, 0)
    _material_and_section(model)
    model.add_member("M1", "N1", "N2", "steel", "sec")
    model.add_support("N1", dx=True, dy=True, dz=True, rx=True, ry=True, rz=True)
    model.add_node_load("N2", "FY", -F)

    res = PyniteAdapter().analyze(model)

    w_ref = -F * L**3 / (3 * E * IZ)
    assert _relative_error(res.deflection("M1", "dy", L), w_ref) < RTOL_BEAM
    assert _relative_error(abs(res.moment("M1", "Mz", 0.0)), F * L) < RTOL_BEAM


def test_b003_simply_supported_beam_central_point_load() -> None:
    """B-003: simply supported beam, central point load F in -Y.

    Analytic: w(L/2) = -F*L^3 / (48*E*Iz)
              Mz(L/2) = -F*L / 4   (sagging negative, adapter convention)
    """
    L, F = 6.0, 40e3
    model = StructuralModel()
    model.add_node("N1", 0, 0, 0)
    model.add_node("N2", L, 0, 0)
    _material_and_section(model)
    model.add_member("M1", "N1", "N2", "steel", "sec")
    model.add_support("N1", dx=True, dy=True, dz=True, rx=True)
    model.add_support("N2", dy=True, dz=True, rx=True)
    model.add_member_point_load("M1", "FY", -F, L / 2)

    res = PyniteAdapter().analyze(model)

    w_ref = -F * L**3 / (48 * E * IZ)
    m_ref = -F * L / 4
    assert _relative_error(res.deflection("M1", "dy", L / 2), w_ref) < RTOL_BEAM
    assert _relative_error(res.moment("M1", "Mz", L / 2), m_ref) < RTOL_BEAM


def test_b004_two_bar_planar_truss() -> None:
    """B-004: symmetric two-bar truss, apex load P in -Y.

    Geometry: supports at (0,0) and (2a,0), apex at (a,h).
    Analytic member force from joint equilibrium:
        N = P / (2*sin(theta)),  theta = atan2(h, a)   [compression]
    Adapter reports compression positive.
    """
    a, h, P = 2.0, 3.0, 100e3
    theta = math.atan2(h, a)
    model = StructuralModel()
    model.add_node("A", 0, 0, 0)
    model.add_node("B", 2 * a, 0, 0)
    model.add_node("C", a, h, 0)
    _material_and_section(model)
    model.add_member("M1", "A", "C", "steel", "sec", truss=True)
    model.add_member("M2", "B", "C", "steel", "sec", truss=True)
    model.add_support("A", dx=True, dy=True, dz=True, rx=True, ry=True, rz=True)
    model.add_support("B", dx=True, dy=True, dz=True, rx=True, ry=True, rz=True)
    # Planar problem: restrain out-of-plane translation and the free
    # rotations of the pin-ended joint (no mechanical influence).
    model.add_support("C", dz=True, rx=True, ry=True, rz=True)
    model.add_node_load("C", "FY", -P)

    res = PyniteAdapter().analyze(model)

    n_ref = P / (2 * math.sin(theta))  # compression, positive per convention
    bar_length = math.hypot(a, h)
    for member in ("M1", "M2"):
        assert _relative_error(res.axial(member, bar_length / 2), n_ref) < RTOL_BEAM


def test_b005_axial_rod_elongation() -> None:
    """B-005: rod fixed at N1, axial tension N in +X at free end N2.

    Analytic: u(N2) = N*L / (E*A). Purely nodal quantity of a single
    truss-type element -> machine-precision agreement expected.
    """
    L, N = 4.0, 500e3
    model = StructuralModel()
    model.add_node("N1", 0, 0, 0)
    model.add_node("N2", L, 0, 0)
    _material_and_section(model)
    model.add_member("M1", "N1", "N2", "steel", "sec")
    model.add_support("N1", dx=True, dy=True, dz=True, rx=True, ry=True, rz=True)
    model.add_support("N2", dy=True, dz=True, rx=True, ry=True, rz=True)
    model.add_node_load("N2", "FX", N)

    res = PyniteAdapter().analyze(model)

    u_ref = N * L / (E * A)
    assert res.node_displacement("N2", "DX") == pytest.approx(u_ref, rel=RTOL_EXACT)
