#!/usr/bin/env python3
"""
Temperature Sensor Node
Publishes temperature readings to /temperature topic
"""

import rospy
import random
import time
from sensor_msgs.msg import Temperature
from std_msgs.msg import Header


class TemperatureSensor:
    def __init__(self):
        rospy.init_node('temperature_sensor', anonymous=True)
        
        # Publisher for temperature data
        self.temp_pub = rospy.Publisher('/sensors/temperature', Temperature, queue_size=10)
        
        # Parameters
        self.publish_rate = rospy.get_param('~publish_rate', 1.0)  # Hz
        self.sensor_frame = rospy.get_param('~sensor_frame', 'temperature_sensor')
        self.min_temp = rospy.get_param('~min_temp', 15.0)  # Celsius
        self.max_temp = rospy.get_param('~max_temp', 35.0)  # Celsius
        self.noise_level = rospy.get_param('~noise_level', 0.5)  # Temperature noise
        
        # Rate control
        self.rate = rospy.Rate(self.publish_rate)
        
        rospy.loginfo(f"Temperature sensor initialized. Publishing at {self.publish_rate} Hz")
        
    def simulate_temperature(self):
        """Simulate temperature readings with some noise"""
        base_temp = (self.min_temp + self.max_temp) / 2
        # Add sinusoidal variation and random noise
        variation = 5 * math.sin(time.time() / 100)  # Slow temperature variation
        noise = random.uniform(-self.noise_level, self.noise_level)
        return base_temp + variation + noise
    
    def publish_temperature(self):
        """Create and publish temperature message"""
        temp_msg = Temperature()
        
        # Header
        temp_msg.header = Header()
        temp_msg.header.stamp = rospy.Time.now()
        temp_msg.header.frame_id = self.sensor_frame
        
        # Temperature data
        temp_msg.temperature = self.simulate_temperature()
        temp_msg.variance = self.noise_level ** 2  # Variance based on noise level
        
        # Publish
        self.temp_pub.publish(temp_msg)
        rospy.logdebug(f"Published temperature: {temp_msg.temperature:.2f}°C")
    
    def run(self):
        """Main loop"""
        while not rospy.is_shutdown():
            self.publish_temperature()
            self.rate.sleep()


if __name__ == '__main__':
    try:
        import math
        sensor = TemperatureSensor()
        sensor.run()
    except rospy.ROSInterruptException:
        rospy.loginfo("Temperature sensor node terminated.")
    except Exception as e:
        rospy.logerr(f"Temperature sensor error: {e}")