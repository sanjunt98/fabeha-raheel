#!/usr/bin/env python3

import time
import sys
import rospy
from llm import LLMInterface, SwarmCommand
from SwarmLeader_API import *


# === UAV swarm wrapper ===
class SwarmController:
    def __init__(self, n_followers=2):
        self.takeoff_spacing = 3
        self.formation_offset = 3
        self.helical_offset = 5

        rospy.loginfo("Initializing Leader UAV...")
        self.leader = SwarmLeader(name='drone1', n_followers=n_followers)

        self.setup_leader()
        self.setup_followers()

    def setup_leader(self):
        rospy.loginfo("Waiting for Leader to switch to Guided Mode")
        self.leader.wait_for_guided()
        self.leader.set_stream_rate()
        rospy.loginfo("Leader's Mode is now GUIDED.")

        rospy.loginfo("Registering Followers")
        self.leader.initialize_followers()
        self.leader.wait_for_GPS_Fix()

    def setup_followers(self):
        rospy.loginfo("Setting Followers Mode to GUIDED")
        for follower in self.leader.followers:
            follower_response = follower.set_mode(mode='GUIDED')
            if follower_response.mode_sent:
                rospy.loginfo(f"{follower.data.header.name} switched to GUIDED.")
            else:
                rospy.logwarn(f"{follower.data.header.name} cannot switch to GUIDED. Removing...")
                self.leader.followers.remove(follower)
                self.leader.n_followers -= 1

    def takeoff(self):
        rospy.loginfo("Arming Leader")
        leader_response = self.leader.arm()
        if not leader_response.success:
            rospy.logerr("Leader not armable. Aborting.")
            return False

        rospy.loginfo("Leader taking off...")
        leader_min_altitude = (self.takeoff_spacing * self.leader.n_followers) + self.takeoff_spacing
        leader_response = self.leader.takeoff(altitude=leader_min_altitude)
        if not leader_response.success:
            rospy.logerr("Leader takeoff failed.")
            return False

        rospy.loginfo("Arming Followers")
        for follower in self.leader.followers:
            follower.arm()
            follower_index = self.leader.followers.index(follower)
            follower.takeoff(
                altitude=(self.takeoff_spacing * (self.leader.n_followers - (follower_index + 1)))
                + self.takeoff_spacing
            )
        return True

    def land_all(self):
        rospy.loginfo("Landing all UAVs...")
        for follower in self.leader.followers:
            follower.set_mode(mode="LAND")
        self.leader.set_mode(mode="LAND")

    def rtl_all(self):
        rospy.loginfo("Returning all UAVs to home...")
        for follower in self.leader.followers:
            follower.set_mode(mode="RTL")
        self.leader.set_mode(mode="RTL")

    def move_line(self):
        rospy.loginfo("Switching to Line formation...")
        follower_coordinates = self.leader.calculate_line_formation_coordinates(offset=self.formation_offset)
        self._move_followers(follower_coordinates)

    def move_flock(self):
        rospy.loginfo("Switching to Flock formation...")
        follower_coordinates = self.leader.calculate_flock_formation_coordinates(offset=self.formation_offset)
        self._move_followers(follower_coordinates)

    def move_helical(self):
        rospy.loginfo("Switching to Helical formation...")
        follower_coordinates = self.leader.calculate_helical_formation_coordinates(offset=self.helical_offset)
        self._move_followers(follower_coordinates)

    def _move_followers(self, follower_coordinates):
        heading = self.leader.data.euler_orientation.yaw
        for follower in self.leader.followers:
            idx = self.leader.followers.index(follower)
            follower.goto_location(
                latitude=follower_coordinates[idx][0],
                longitude=follower_coordinates[idx][1],
                altitude=self.leader.data.global_position.altitude
                - (self.takeoff_spacing * (idx + 1)),
            )


# === Main interactive loop ===
if __name__ == "__main__":
    # rospy.init_node("swarm_llm_controller", anonymous=True)

    llm = LLMInterface()
    swarm = SwarmController()

    rospy.loginfo("Ready to receive natural language commands.")

    try:
        while not rospy.is_shutdown():
            user_input = input("\n>>> Enter Command: ")
            cmd: SwarmCommand = llm.parse_command(user_input)

            if cmd.action == "unknown":
                print(f"❌ Could not interpret command. Reason: {cmd.reason}")
                continue

            if cmd.action == "takeoff":
                swarm.takeoff()
            elif cmd.action == "land":
                swarm.land_all()
            elif cmd.action == "rtl":
                swarm.rtl_all()
            elif cmd.action == "move_line":
                swarm.move_line()
            elif cmd.action == "move_flock":
                swarm.move_flock()
            elif cmd.action == "move_helical":
                swarm.move_helical()
            else:
                print(f"⚠️ Command not implemented: {cmd.action}")

    except KeyboardInterrupt:
        rospy.logwarn("KeyboardInterrupt received! Landing all UAVs...")
        swarm.land_all()
        rospy.signal_shutdown("User interrupted with Ctrl+C")
        sys.exit(0)
