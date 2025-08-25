#!/usr/bin/env python3
"""
Sensor Manager Node
Aggregates and manages multiple sensor data streams
Provides unified sensor status and health monitoring
"""

import rospy
from sensor_msgs.msg import Temperature, RelativeHumidity
from std_msgs.msg import String, Header
from geometry_msgs.msg import Twist
import json
import time


class SensorManager:
    def __init__(self):
        rospy.init_node('sensor_manager', anonymous=True)
        
        # Sensor data storage
        self.temperature_data = None
        self.humidity_data = None
        self.last_temp_time = None
        self.last_humidity_time = None
        
        # Publishers
        self.status_pub = rospy.Publisher('/sensors/status', String, queue_size=10)
        self.aggregated_pub = rospy.Publisher('/sensors/aggregated', String, queue_size=10)
        
        # Subscribers
        self.temp_sub = rospy.Subscriber('/sensors/temperature', Temperature, self.temperature_callback)
        self.humidity_sub = rospy.Subscriber('/sensors/humidity', RelativeHumidity, self.humidity_callback)
        
        # Parameters
        self.publish_rate = rospy.get_param('~publish_rate', 0.5)  # Hz
        self.sensor_timeout = rospy.get_param('~sensor_timeout', 5.0)  # seconds
        
        # Rate control
        self.rate = rospy.Rate(self.publish_rate)
        
        rospy.loginfo("Sensor manager initialized")
        
    def temperature_callback(self, msg):
        """Handle temperature sensor data"""
        self.temperature_data = msg
        self.last_temp_time = rospy.Time.now()
        rospy.logdebug(f"Received temperature: {msg.temperature:.2f}°C")
        
    def humidity_callback(self, msg):
        """Handle humidity sensor data"""
        self.humidity_data = msg
        self.last_humidity_time = rospy.Time.now()
        rospy.logdebug(f"Received humidity: {msg.relative_humidity * 100:.2f}%")
        
    def check_sensor_health(self):
        """Check if sensors are providing fresh data"""
        current_time = rospy.Time.now()
        
        temp_healthy = (self.last_temp_time is not None and 
                       (current_time - self.last_temp_time).to_sec() < self.sensor_timeout)
        
        humidity_healthy = (self.last_humidity_time is not None and 
                           (current_time - self.last_humidity_time).to_sec() < self.sensor_timeout)
        
        return {
            'temperature_sensor': 'healthy' if temp_healthy else 'timeout',
            'humidity_sensor': 'healthy' if humidity_healthy else 'timeout',
            'overall_status': 'healthy' if (temp_healthy and humidity_healthy) else 'degraded'
        }
        
    def publish_status(self):
        """Publish sensor health status"""
        status = self.check_sensor_health()
        status_msg = String()
        status_msg.data = json.dumps(status, indent=2)
        self.status_pub.publish(status_msg)
        
    def publish_aggregated_data(self):
        """Publish aggregated sensor data"""
        if self.temperature_data is None or self.humidity_data is None:
            return
            
        # Create aggregated data structure
        aggregated = {
            'timestamp': rospy.Time.now().to_sec(),
            'temperature': {
                'value': self.temperature_data.temperature,
                'unit': 'celsius',
                'variance': self.temperature_data.variance,
                'frame_id': self.temperature_data.header.frame_id
            },
            'humidity': {
                'value': self.humidity_data.relative_humidity * 100,  # Convert to percentage
                'unit': 'percent',
                'variance': self.humidity_data.variance * 10000,  # Convert to percentage variance
                'frame_id': self.humidity_data.header.frame_id
            },
            'comfort_index': self.calculate_comfort_index(),
            'dew_point': self.calculate_dew_point()
        }
        
        aggregated_msg = String()
        aggregated_msg.data = json.dumps(aggregated, indent=2)
        self.aggregated_pub.publish(aggregated_msg)
        
    def calculate_comfort_index(self):
        """Calculate a simple comfort index based on temperature and humidity"""
        if self.temperature_data is None or self.humidity_data is None:
            return None
            
        temp = self.temperature_data.temperature
        humidity = self.humidity_data.relative_humidity * 100
        
        # Simple comfort calculation (0-100, higher is more comfortable)
        optimal_temp = 22.0  # 22°C
        optimal_humidity = 50.0  # 50%
        
        temp_score = max(0, 100 - abs(temp - optimal_temp) * 5)
        humidity_score = max(0, 100 - abs(humidity - optimal_humidity) * 2)
        
        return (temp_score + humidity_score) / 2
        
    def calculate_dew_point(self):
        """Calculate dew point temperature"""
        if self.temperature_data is None or self.humidity_data is None:
            return None
            
        import math
        
        temp = self.temperature_data.temperature
        humidity = self.humidity_data.relative_humidity * 100
        
        # Magnus formula approximation
        a = 17.27
        b = 237.7
        
        alpha = ((a * temp) / (b + temp)) + math.log(humidity / 100.0)
        dew_point = (b * alpha) / (a - alpha)
        
        return round(dew_point, 2)
        
    def run(self):
        """Main loop"""
        while not rospy.is_shutdown():
            self.publish_status()
            self.publish_aggregated_data()
            self.rate.sleep()


if __name__ == '__main__':
    try:
        manager = SensorManager()
        manager.run()
    except rospy.ROSInterruptException:
        rospy.loginfo("Sensor manager node terminated.")
    except Exception as e:
        rospy.logerr(f"Sensor manager error: {e}")