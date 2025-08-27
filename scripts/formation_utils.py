from config import FORMATION_OFFSETS

def get_formation_positions(leader_position, formation_type):
    """
    leader_position: dict {"x":..., "y":..., "z":...}
    formation_type: str ('flock', 'line', 'helical')
    Returns list of positions [{"x":..., "y":..., "z":...}, ...]
    """
    positions = []
    offsets = FORMATION_OFFSETS.get(formation_type, FORMATION_OFFSETS["flock"])
    for offset in offsets:
        x = leader_position["x"] + offset[0]
        y = leader_position["y"] + offset[1]
        z = leader_position["z"] + offset[2]
        positions.append({"x": x, "y": y, "z": z})
    return positions
