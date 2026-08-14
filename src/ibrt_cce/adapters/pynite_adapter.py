"""Adapter mapping the IBRT_CCE core model onto the Pynite FEM kernel.

Verified against Pynite 3.0.0 (see tests/benchmarks). The adapter follows
the project architecture: ``build -> solve -> results`` behind a kernel-
agnostic interface, so kernels stay interchangeable.

Sign conventions of returned results (Pynite-native, verified empirically
against the analytic benchmarks B-001...B-005; a project-wide convention
ADR is tracked in STATUS.md):

* ``deflection('dy', x)``: global displacement [m]; loads in -Y produce
  negative (downward) deflections.
* ``moment('Mz', x)``: local bending moment [N*m]; for an X-aligned beam
  loaded in -Y, the sagging midspan moment is reported NEGATIVE
  (e.g. B-001: Mz(L/2) = -q*L^2/8).
* ``shear('Fy', x)``: local shear [N]; left support of B-001 gives +q*L/2.
* ``axial(x)``: axial force [N]; COMPRESSION is reported POSITIVE
  (verified in B-004).

Units: strictly SI (see core.model docstring).
"""

from __future__ import annotations

from Pynite import FEModel3D

from ibrt_cce.core.model import StructuralModel

#: Single load case/combination used in Phase 0. Load combinations become a
#: first-class concept in Phase 4 (see roadmap).
DEFAULT_COMBO = "Combo 1"


class PyniteResults:
    """Thin, read-only view on a solved Pynite model."""

    def __init__(self, fe_model: FEModel3D) -> None:
        self._m = fe_model

    # -- member results ---------------------------------------------------

    def deflection(self, member: str, direction: str, x: float) -> float:
        """Member deflection [m] at local position x [m]. direction: 'dx'|'dy'|'dz'."""
        return self._m.members[member].deflection(direction, x, DEFAULT_COMBO)

    def moment(self, member: str, axis: str, x: float) -> float:
        """Internal bending moment [N*m] at x. axis: 'My'|'Mz' (local)."""
        return self._m.members[member].moment(axis, x, DEFAULT_COMBO)

    def shear(self, member: str, axis: str, x: float) -> float:
        """Internal shear force [N] at x. axis: 'Fy'|'Fz' (local)."""
        return self._m.members[member].shear(axis, x, DEFAULT_COMBO)

    def axial(self, member: str, x: float) -> float:
        """Axial force [N] at x. Compression positive (Pynite convention)."""
        return self._m.members[member].axial(x, DEFAULT_COMBO)

    # -- nodal results ----------------------------------------------------

    def node_displacement(self, node: str, dof: str) -> float:
        """Global nodal displacement [m] or rotation [rad].

        dof: one of 'DX','DY','DZ','RX','RY','RZ'.
        """
        return getattr(self._m.nodes[node], dof)[DEFAULT_COMBO]

    # -- glasbox access ---------------------------------------------------

    @property
    def kernel_model(self) -> FEModel3D:
        """Direct access to the solved kernel model (glasbox principle)."""
        return self._m


class PyniteAdapter:
    """Builds and solves a Pynite model from the core StructuralModel."""

    def analyze(self, model: StructuralModel) -> PyniteResults:
        fe = self.build(model)
        fe.analyze(check_stability=True, check_statics=False)
        return PyniteResults(fe)

    def build(self, model: StructuralModel) -> FEModel3D:
        """Map core entities 1:1 onto the kernel (no solving yet)."""
        fe = FEModel3D()

        for node in model.nodes.values():
            fe.add_node(node.name, node.x, node.y, node.z)

        for mat in model.materials.values():
            fe.add_material(mat.name, mat.E, mat.G, mat.nu, mat.rho)

        for sec in model.sections.values():
            fe.add_section(sec.name, sec.A, sec.Iy, sec.Iz, sec.J)

        for mem in model.members.values():
            fe.add_member(mem.name, mem.i_node, mem.j_node, mem.material, mem.section)
            if mem.truss:
                # Axial-only member: release bending about both local axes
                # at both ends. Torsion stays coupled for numerical stability.
                fe.def_releases(
                    mem.name, Ryi=True, Rzi=True, Ryj=True, Rzj=True
                )

        for sup in model.supports:
            fe.def_support(sup.node, sup.dx, sup.dy, sup.dz, sup.rx, sup.ry, sup.rz)

        for udl in model.member_udls:
            fe.add_member_dist_load(udl.member, udl.direction, udl.w, udl.w)

        for pl in model.member_point_loads:
            fe.add_member_pt_load(pl.member, pl.direction, pl.P, pl.x)

        for nl in model.node_loads:
            fe.add_node_load(nl.node, nl.direction, nl.P)

        return fe
