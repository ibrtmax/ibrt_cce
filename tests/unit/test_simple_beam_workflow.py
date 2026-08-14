"""Unit tests for the simple-beam workflow (UI-free vertical slice)."""

from ibrt_cce.workflows.simple_beam import SimpleBeamInput, analyze_simple_beam

RTOL = 1e-3  # docs/VALIDATION.md beam tolerance


def test_simple_beam_workflow_matches_analytic() -> None:
    inp = SimpleBeamInput(L=6.0, q=10e3, E=210e9, Iz=8356e-8)
    res = analyze_simple_beam(inp)

    assert res.w_rel_error < RTOL
    assert res.m_rel_error < RTOL
    assert abs(res.r_left - res.r_left_analytic) / res.r_left_analytic < RTOL
    # Deflection curve is sampled along the span and points downward.
    assert len(res.x) == len(res.deflection) == len(res.moment) == 101
    assert res.deflection.min() < 0

    # Glasbox hand check: K[DY1, DY1] == 12*E*Iz/L^3 for a single member.
    expected = 12 * inp.E * inp.Iz / inp.L**3
    assert abs(res.stiffness_matrix[1, 1] - expected) / expected < 1e-9
