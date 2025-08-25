#!/usr/bin/env python3
"""
Humidity Sensor Node
Publishes humidity readings to /humidity topic
"""

import rospy
import random
import math
import time
from sensor_msgs.msg import RelativeHumidity
from std_msgs.msg import Header


class HumiditySensor:
    def __init__(self):
        rospy.init_node('humidity_sensor', anonymous=True)
        
        # Publisher for humidity data
        self.humidity_pub = rospy.Publisher('/sensors/humidity', RelativeHumidity, queue_size=10)
        
        # Parameters
        self.publish_rate = rospy.get_param('~publish_rate', 1.0)  # Hz
        self.sensor_frame = rospy.get_param('~sensor_frame', 'humidity_sensor')
        self.min_humidity = rospy.get_param('~min_humidity', 30.0)  # Percentage
        self.max_humidity = rospy.get_param('~max_humidity', 80.0)  # Percentage
        self.noise_level = rospy.get_param('~noise_level', 2.0)  # Humidity noise
        
        # Rate control
        self.rate = rospy.Rate(self.publish_rate)
        
        rospy.loginfo(f"Humidity sensor initialized. Publishing at {self.publish_rate} Hz")
        
    def simulate_humidity(self):
        """Simulate humidity readings with some noise"""
        base_humidity = (self.min_humidity + self.max_humidity) / 2
        # Add sinusoidal variation and random noise
        variation = 15 * math.sin(time.time() / 80)  # Humidity variation
        noise = random.uniform(-self.noise_level, self.noise_level)
        humidity = base_humidity + variation + noise
        
        # Clamp between 0 and 100
        return max(0.0, min(100.0, humidity))
    
    def publish_humidity(self):
        """Create and publish humidity message"""
        humidity_msg = RelativeHumidity()
        
        # Header
        humidity_msg.header = Header()
        humidity_msg.header.stamp = rospy.Time.now()
        humidity_msg.header.frame_id = self.sensor_frame
        
        # Humidity data
        humidity_msg.relative_humidity = self.simulate_humidity() / 100.0  # Convert to 0-1 range
        humidity_msg.variance = (self.noise_level / 100.0) ** 2  # Variance in 0-1 range
        
        # Publish
        self.humidity_pub.publish(humidity_msg)
        rospy.logdebug(f"Published humidity: {humidity_msg.relative_humidity * 100:.2f}%")
    
    def run(self):
        """Main loop"""
        while not rospy.is_shutdown():
            self.publish_humidity()
            self.rate.sleep()


if __name__ == '__main__':
    try:
        sensor = HumiditySensor()
        sensor.run()
    except rospy.ROSInterruptException:
        rospy.loginfo("Humidity sensor node terminated.")
    except Exception as e:
        rospy.logerr(f"Humidity sensor error: {e}")