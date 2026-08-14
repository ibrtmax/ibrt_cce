"""Core structural data model of IBRT_CCE.

This module defines the solver-agnostic entities of the parameter graph.
It deliberately knows nothing about any FEM kernel (architecture rule 1/2)
and is structured so every entity maps cleanly onto IFC structural analysis
classes later (architecture rule 7, IfcStructuralAnalysisModel).

Units
-----
Strictly SI everywhere in this package:
    length  [m], force [N], moment [N*m], stress/modulus [Pa],
    distributed load [N/m], density [kg/m^3].
Unit conversion happens only at UI boundaries, never inside core/adapters.

Coordinate system
-----------------
Right-handed global XYZ. Gravity loads act in -Y by project convention
for the Phase-0 beam benchmarks.
"""

from __future__ import annotations

from dataclasses import dataclass, field

# Global load/displacement direction labels (subset used in Phase 0).
GLOBAL_DIRECTIONS = ("FX", "FY", "FZ")


@dataclass(frozen=True)
class Material:
    """Linear-elastic isotropic material.

    E: Young's modulus [Pa], G: shear modulus [Pa],
    nu: Poisson's ratio [-], rho: density [kg/m^3].
    """

    name: str
    E: float
    G: float
    nu: float
    rho: float


@dataclass(frozen=True)
class Section:
    """Prismatic cross-section.

    A: area [m^2]; Iy, Iz: second moments of area about local y/z [m^4];
    J: torsion constant [m^4].
    """

    name: str
    A: float
    Iy: float
    Iz: float
    J: float


@dataclass(frozen=True)
class NodePoint:
    """Geometric node in global coordinates [m]."""

    name: str
    x: float
    y: float
    z: float


@dataclass(frozen=True)
class Support:
    """Nodal support conditions (True = restrained)."""

    node: str
    dx: bool = False
    dy: bool = False
    dz: bool = False
    rx: bool = False
    ry: bool = False
    rz: bool = False


@dataclass(frozen=True)
class Member:
    """Prismatic frame member between two nodes.

    truss=True releases bending (Ry, Rz) at both ends, i.e. the member
    carries axial force only. Generic end releases are a later feature
    (tracked in STATUS.md).
    """

    name: str
    i_node: str
    j_node: str
    material: str
    section: str
    truss: bool = False


@dataclass(frozen=True)
class MemberUDL:
    """Uniformly distributed member load.

    direction: global 'FX' | 'FY' | 'FZ'; w: load intensity [N/m]
    (negative FY = gravity direction by project convention).
    """

    member: str
    direction: str
    w: float


@dataclass(frozen=True)
class MemberPointLoad:
    """Concentrated load on a member at distance x [m] from the i-node.

    direction: global 'FX' | 'FY' | 'FZ'; P: load [N].
    """

    member: str
    direction: str
    P: float
    x: float


@dataclass(frozen=True)
class NodeLoad:
    """Concentrated nodal load. direction: 'FX' | 'FY' | 'FZ'; P: [N]."""

    node: str
    direction: str
    P: float


@dataclass
class StructuralModel:
    """Container for one analysis model (the Phase-0 parameter graph).

    The add_* helpers validate referential integrity so that adapters can
    rely on a consistent model.
    """

    nodes: dict[str, NodePoint] = field(default_factory=dict)
    materials: dict[str, Material] = field(default_factory=dict)
    sections: dict[str, Section] = field(default_factory=dict)
    members: dict[str, Member] = field(default_factory=dict)
    supports: list[Support] = field(default_factory=list)
    member_udls: list[MemberUDL] = field(default_factory=list)
    member_point_loads: list[MemberPointLoad] = field(default_factory=list)
    node_loads: list[NodeLoad] = field(default_factory=list)

    # -- builders ---------------------------------------------------------

    def add_node(self, name: str, x: float, y: float, z: float = 0.0) -> NodePoint:
        node = NodePoint(name, x, y, z)
        self.nodes[name] = node
        return node

    def add_material(self, name: str, E: float, G: float, nu: float, rho: float) -> Material:
        mat = Material(name, E, G, nu, rho)
        self.materials[name] = mat
        return mat

    def add_section(self, name: str, A: float, Iy: float, Iz: float, J: float) -> Section:
        sec = Section(name, A, Iy, Iz, J)
        self.sections[name] = sec
        return sec

    def add_member(
        self,
        name: str,
        i_node: str,
        j_node: str,
        material: str,
        section: str,
        truss: bool = False,
    ) -> Member:
        self._require_node(i_node)
        self._require_node(j_node)
        if material not in self.materials:
            raise KeyError(f"Unknown material '{material}'")
        if section not in self.sections:
            raise KeyError(f"Unknown section '{section}'")
        member = Member(name, i_node, j_node, material, section, truss)
        self.members[name] = member
        return member

    def add_support(self, node: str, **restraints: bool) -> Support:
        self._require_node(node)
        support = Support(node=node, **restraints)
        self.supports.append(support)
        return support

    def add_member_udl(self, member: str, direction: str, w: float) -> MemberUDL:
        self._require_member(member)
        self._require_direction(direction)
        load = MemberUDL(member, direction, w)
        self.member_udls.append(load)
        return load

    def add_member_point_load(
        self, member: str, direction: str, P: float, x: float
    ) -> MemberPointLoad:
        self._require_member(member)
        self._require_direction(direction)
        load = MemberPointLoad(member, direction, P, x)
        self.member_point_loads.append(load)
        return load

    def add_node_load(self, node: str, direction: str, P: float) -> NodeLoad:
        self._require_node(node)
        self._require_direction(direction)
        load = NodeLoad(node, direction, P)
        self.node_loads.append(load)
        return load

    # -- validation helpers ----------------------------------------------

    def _require_node(self, name: str) -> None:
        if name not in self.nodes:
            raise KeyError(f"Unknown node '{name}'")

    def _require_member(self, name: str) -> None:
        if name not in self.members:
            raise KeyError(f"Unknown member '{name}'")

    @staticmethod
    def _require_direction(direction: str) -> None:
        if direction not in GLOBAL_DIRECTIONS:
            raise ValueError(
                f"Direction must be one of {GLOBAL_DIRECTIONS}, got '{direction}'"
            )
