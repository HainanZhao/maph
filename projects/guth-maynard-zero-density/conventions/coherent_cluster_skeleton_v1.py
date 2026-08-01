"""Exact coherent-cluster skeleton exponent conventions, Cycle 18."""
from fractions import Fraction


Q = Fraction


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def local_rows() -> dict[str, Fraction]:
    threshold = Q(7, 10)
    radius = Q(3, 5)
    first = 2 - 2 * threshold
    mean_branch = 1 - 2 * threshold
    high_branch = 4 - 6 * threshold
    selected_branch = min(mean_branch, high_branch)
    local_second = radius + selected_branch
    local = max(first, local_second)
    require(first == Q(3, 5), "first local exponent mismatch")
    require((mean_branch, high_branch, selected_branch) == (Q(-2, 5), Q(-1, 5), Q(-2, 5)), "classical branch mismatch")
    require(local_second == Q(1, 5), "local interval term mismatch")
    require(local == radius == Q(3, 5), "cluster exponent mismatch")
    return {"threshold": threshold, "radius": radius, "first_term": first, "mean_branch": mean_branch, "high_branch": high_branch, "selected_branch": selected_branch, "local_interval_term": local_second, "cluster_exponent": local}


def skeleton_rows() -> dict[str, Fraction]:
    generic = Q(8, 5)
    target = Q(36, 25)
    cluster = Q(3, 5)
    generic_skeleton = generic - cluster
    target_skeleton = target - cluster
    saving = generic_skeleton - target_skeleton
    require(generic_skeleton == 1, "generic skeleton exponent mismatch")
    require(target_skeleton == Q(21, 25), "target skeleton exponent mismatch")
    require(saving == Q(4, 25), "skeleton saving mismatch")
    return {"generic_count": generic, "target_count": target, "cluster": cluster, "generic_skeleton": generic_skeleton, "target_skeleton": target_skeleton, "required_saving": saving}


def verify_all() -> dict[str, object]:
    return {"local_large_values": local_rows(), "skeleton_translation": skeleton_rows(), "covering_statement": "A maximal D-separated subset has D-neighborhoods covering W; each 2D interval contains X^(3/5+o(1)) rows."}
