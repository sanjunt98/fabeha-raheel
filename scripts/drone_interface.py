#!/usr/bin/env python3

import rospy
from mavros_msgs.msg import State, PositionTarget
from mavros_msgs.srv import CommandBool, SetMode, CommandTOL
from nav_msgs.msg import Odometry
from geometry_msgs.msg import PoseStamped
from pymavlink import mavutil

class DroneInterface:
    def __init__(self, drone_name):
        self.drone_name = drone_name
        self.state = None
        self.pose = None

        # Subscribers
        rospy.Subscriber(f"/{drone_name}/mavros/state", State, self._state_cb)
        rospy.Subscriber(f"/{drone_name}/mavros/local_position/odom", Odometry, self._pose_cb)

        # Publishers for setpoints
        self.setpoint_pub = rospy.Publisher(f"/{drone_name}/mavros/setpoint_position/local", PoseStamped, queue_size=10)

        # Service proxies
        rospy.wait_for_service(f"/{drone_name}/mavros/cmd/arming")
        rospy.wait_for_service(f"/{drone_name}/mavros/set_mode")
        rospy.wait_for_service(f"/{drone_name}/mavros/cmd/takeoff")

        self.arming_srv = rospy.ServiceProxy(f"/{drone_name}/mavros/cmd/arming", CommandBool)
        self.set_mode_srv = rospy.ServiceProxy(f"/{drone_name}/mavros/set_mode", SetMode)
        self.takeoff_srv = rospy.ServiceProxy(f"/{drone_name}/mavros/cmd/takeoff", CommandTOL)

        # Wait a bit for publishers to register
        rospy.sleep(1.0)

    def _state_cb(self, msg):
        self.state = msg

    def _pose_cb(self, msg):
        self.pose = msg.pose.pose

    def arm(self):
        if not self.state or self.state.armed:
            return
        try:
            res = self.arming_srv(True)
            if res.success:
                rospy.loginfo(f"[{self.drone_name}] Armed successfully")
            else:
                rospy.logwarn(f"[{self.drone_name}] Arming failed")
        except Exception as e:
            rospy.logerr(f"[{self.drone_name}] Arming exception: {e}")

    def takeoff(self, altitude=5.0):
        try:
            mode_res = self.set_mode_srv(custom_mode="GUIDED")
            if not mode_res.mode_sent:
                rospy.logwarn(f"[{self.drone_name}] Failed to set mode GUIDED")
                return

            res = self.takeoff_srv(
                min_pitch=0,
                yaw=0,
                latitude=0,
                longitude=0,
                altitude=altitude
            )
            if res.success:
                rospy.loginfo(f"[{self.drone_name}] Taking off to {altitude} m")
            else:
                rospy.logwarn(f"[{self.drone_name}] Takeoff failed")
        except Exception as e:
            rospy.logerr(f"[{self.drone_name}] Takeoff exception: {e}")

    def go_to(self, x, y, z):
        """
        Send a single position setpoint to the drone
        """
        if not self.state or not self.state.armed:
            rospy.logwarn(f"[{self.drone_name}] Cannot move, drone not armed")
            return

        pose = PoseStamped()
        pose.header.stamp = rospy.Time.now()
        pose.header.frame_id = "map"
        pose.pose.position.x = x
        pose.pose.position.y = y
        pose.pose.position.z = z

        # Maintain current orientation (yaw) if available
        if self.pose:
            pose.pose.orientation = self.pose.orientation
        else:
            pose.pose.orientation.w = 1.0

        # Publish multiple times to ensure MAVROS receives it
        for _ in range(10):
            self.setpoint_pub.publish(pose)
            rospy.sleep(0.1)

        rospy.loginfo(f"[{self.drone_name}] Moving to x:{x}, y:{y}, z:{z}")
