#!/usr/bin/env python3
import rospy
from drone_interface import DroneInterface
from groq_agent import get_drone_commands
import time

class DroneBridge:
    def __init__(self, drone_names):
        rospy.init_node("drone_bridge", anonymous=True)
        self.drones = {name: DroneInterface(name) for name in drone_names}
        rospy.sleep(1)  # allow subscribers to initialize

    def get_swarm_state(self):
        """
        Returns a list of dicts with telemetry for each drone.
        """
        state = []
        for name, drone in self.drones.items():
            pose = getattr(drone.pose, "position", None)
            pos = {
                "x": getattr(pose, "x", None) if pose else None,
                "y": getattr(pose, "y", None) if pose else None,
                "z": getattr(pose, "z", None) if pose else None,
            }
            state.append({
                "drone": name,
                "position": pos,
                "armed": getattr(drone.state, "armed", False),
                "battery": None,
            })
        return state

    def telemetry_loop(self):
        while not rospy.is_shutdown():
            swarm_state = self.get_swarm_state()
            print(swarm_state)
            user_input = input("Enter swarm command: ")

            # Extract drone names as strings
            drone_names = [d["drone"] for d in swarm_state]

            try:
                response = get_drone_commands(user_input, drone_names)
            except Exception as e:
                rospy.logwarn(f"LLM call failed: {e}")
                continue

            if not response:
                rospy.logwarn("LLM returned empty response")
                continue

            for drone_name, target in response.items():
                drone = self.drones.get(drone_name)
                if not drone:
                    rospy.logwarn(f"Unknown drone in LLM response: {drone_name}")
                    continue

                # Arm if not armed
                if not getattr(drone.state, "armed", False):
                    drone.arm()
                    rospy.sleep(1)

                # Takeoff if below target altitude
                current_z = getattr(getattr(drone.pose, "position", None), "z", 0)
                if current_z is None:
                    current_z = 0
                if target["z"] > 1 and current_z < 1:
                    drone.takeoff(altitude=target["z"])
                    rospy.sleep(2)

                # Move to target coordinates
                try:
                    drone.go_to(target["x"], target["y"], target["z"])
                except Exception as e:
                    rospy.logerr(f"[{drone_name}] Move failed: {e}")

if __name__ == "__main__":
    drone_names = ["drone1", "drone2", "drone3"]
    bridge = DroneBridge(drone_names)
    bridge.telemetry_loop()
