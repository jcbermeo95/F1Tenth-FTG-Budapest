import rclpy
from rclpy.node import Node
from ackermann_msgs.msg import AckermannDriveStamped
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
import math
import time
import numpy as np

class RaceFTG(Node):
  def __init__(self):
    super().__init__('race_ftg')
    
    self.start_time = None
    self.final_time = None
    self.state = 'after'  
    self.lap = 1
    self.total_time = 0
    self.safety_bubble = 1.8 #original value = 1.0, 2,0, 1.8
    
    self.laser = self.create_subscription(LaserScan, '/scan', self.lidar_callback, 1) 
    self.odom = self.create_subscription(Odometry, '/ego_racecar/odom', self.odom_callback, 1)
    self.drive = self.create_publisher(AckermannDriveStamped, '/drive', 1)
    
  def odom_callback(self, msg):
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
      
    if self.start_time is None:
      self.start_time = time.time()
        
    if -0.5 < x < 0.5 and -2 < y < 2:
      if self.state == 'after' and x < 0:
        self.state = 'before'
      elif x > 0 and self.state == 'before':
        self.final_time = time.time()
        timelap = self.final_time - self.start_time
        self.total_time += timelap
        print(f"Tiempo de vuelta {self.lap} : {timelap:.6f}. Tiempo total: {self.total_time:.6f}")
        self.start_time = self.final_time
        self.state = 'after'
        self.lap += 1

  def lidar_callback(self, msg):
    ranges = np.array(msg.ranges)
    ranges[np.isinf(ranges)] = 1000.0
          
    safe_mask = (ranges > (np.min(ranges) + self.safety_bubble))
    valid_indices = np.where(safe_mask)[0]
    gaps = np.where(np.diff(valid_indices) > 1)[0] + 1
    subranges_idx = np.split(valid_indices, gaps)
    subranges = [ranges[idx] for idx in subranges_idx]
        
    wide_array, wide_array_idx = self.get_wide_arrays(subranges, subranges_idx)
    
    center_index = 0
    selected_chain = None 
    if wide_array.size != 0:
      longest_chain, longest_chain_idx = self.find_longest_chain(wide_array, wide_array_idx)
      center_index = np.mean(longest_chain_idx)
      selected_chain = longest_chain 
    else:  
      max_distance_chain, max_distance_chain_idx = self.max_distance_chain(subranges, subranges_idx)
      center_index = np.mean(max_distance_chain_idx)
      selected_chain = max_distance_chain 

    steering_angle = (center_index - 540) * (270.0 / 1080.0) * (math.pi / 180.0)
       
    drive_msg = AckermannDriveStamped()
    steering_angle = np.clip(steering_angle, -0.5, 0.5) 
    if np.max(selected_chain) < 20:
      drive_msg.drive.speed = 9.0 
    elif np.max(selected_chain) < 30:
      drive_msg.drive.speed = 9.5 
    else:
      drive_msg.drive.speed = 10.0 
      steering_angle = np.clip(steering_angle, -0.8, 0.8)
    drive_msg.drive.steering_angle = float(steering_angle)
    self.drive.publish(drive_msg)
    
  def max_distance_chain(self, subranges, subranges_idx):
    max_dist = -1
    best_idx = 0
    
    for i, chain in enumerate(subranges):
      local_max = np.max(chain)
      if local_max > max_dist:
        max_dist = local_max
        best_idx = i
    
    max_distance_chain = np.array(subranges[best_idx])
    max_distance_chain_idx = np.array(subranges_idx[best_idx])
    
    return max_distance_chain, max_distance_chain_idx
          
  def find_longest_chain(self, subranges, subranges_idx):
    longest_chain = np.array([])
    longest_idx = np.array([])
    max_length = 0
      
    for i in range(len(subranges)):
      current_chain = np.array(subranges[i])
      current_idx = np.array(subranges_idx[i])
    
      if len(current_chain) > max_length:
        max_length = len(current_chain)
        longest_chain = current_chain
        longest_idx = current_idx
        
    return longest_chain, longest_idx  
      
  def get_wide_arrays(self, subranges, subranges_idx, threshold_deg=30.0, total_fov_deg=270.0, num_total_points=1080):
      
    angle_per_point = total_fov_deg / num_total_points
    min_points = int(threshold_deg / angle_per_point)  
    wide_subranges = []
    wide_subranges_idx = []
      
    for i in range(len(subranges)):
      if len(subranges[i]) >= min_points:
        wide_subranges.append(subranges[i])
        wide_subranges_idx.append(subranges_idx[i])
        
    return np.array(wide_subranges, dtype=object), np.array(wide_subranges_idx, dtype=object)
      
def main(args=None):
  rclpy.init(args=args)
  node = RaceFTG()
  rclpy.spin(node)
  node.destroy_node()
  rclpy.shutdown()

if __name__ == '__main__':
    main()
