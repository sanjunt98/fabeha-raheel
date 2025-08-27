# config.py

# List of drone IDs
DRONE_IDS = ["drone1", "drone2", "drone3"]

# Default takeoff altitude in meters
TAKEOFF_ALTITUDE = 5.0

# Relative offsets for formations (leader is drone1)
FORMATION_OFFSETS = {
    "flock": [(0, 0, 0), (1, 1, 0), (-1, 1, 0)],
    "line": [(0, 0, 0), (0, 2, 0), (0, 4, 0)],
    "helical": [(0, 0, 0), (1, 1, 1), (-1, 1, 2)],
}
