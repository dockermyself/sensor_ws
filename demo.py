#!/usr/bin/env python3
"""
Demo script to show sensor functionality without ROS dependencies
This demonstrates the core sensor logic and data structures
"""

import json
import time
import math
import random
from datetime import datetime


class SensorDemo:
    def __init__(self):
        self.min_temp = 20.0
        self.max_temp = 28.0
        self.temp_noise = 0.3
        
        self.min_humidity = 40.0
        self.max_humidity = 70.0
        self.humidity_noise = 1.5
        
        print("Sensor Workspace Demo")
        print("====================")
        print("Simulating temperature and humidity sensors...")
        print()
    
    def simulate_temperature(self):
        """Simulate temperature readings"""
        base_temp = (self.min_temp + self.max_temp) / 2
        variation = 3 * math.sin(time.time() / 50)  # Slow variation
        noise = random.uniform(-self.temp_noise, self.temp_noise)
        return base_temp + variation + noise
    
    def simulate_humidity(self):
        """Simulate humidity readings"""
        base_humidity = (self.min_humidity + self.max_humidity) / 2
        variation = 10 * math.sin(time.time() / 60)  # Humidity variation
        noise = random.uniform(-self.humidity_noise, self.humidity_noise)
        humidity = base_humidity + variation + noise
        return max(0.0, min(100.0, humidity))
    
    def calculate_comfort_index(self, temp, humidity):
        """Calculate comfort index"""
        optimal_temp = 22.0
        optimal_humidity = 50.0
        
        temp_score = max(0, 100 - abs(temp - optimal_temp) * 5)
        humidity_score = max(0, 100 - abs(humidity - optimal_humidity) * 2)
        
        return (temp_score + humidity_score) / 2
    
    def calculate_dew_point(self, temp, humidity):
        """Calculate dew point temperature"""
        a = 17.27
        b = 237.7
        
        alpha = ((a * temp) / (b + temp)) + math.log(humidity / 100.0)
        dew_point = (b * alpha) / (a - alpha)
        
        return round(dew_point, 2)
    
    def run_demo(self, duration=30):
        """Run sensor demo for specified duration"""
        start_time = time.time()
        
        while time.time() - start_time < duration:
            # Simulate sensor readings
            temp = self.simulate_temperature()
            humidity = self.simulate_humidity()
            
            # Calculate derived metrics
            comfort = self.calculate_comfort_index(temp, humidity)
            dew_point = self.calculate_dew_point(temp, humidity)
            
            # Create sensor data structure
            sensor_data = {
                "timestamp": datetime.now().isoformat(),
                "temperature": {
                    "value": round(temp, 2),
                    "unit": "celsius",
                    "frame_id": "temperature_sensor"
                },
                "humidity": {
                    "value": round(humidity, 1),
                    "unit": "percent",
                    "frame_id": "humidity_sensor"
                },
                "comfort_index": round(comfort, 1),
                "dew_point": dew_point,
                "status": "healthy"
            }
            
            # Display data
            print(f"🌡️  Temperature: {temp:.1f}°C")
            print(f"💧 Humidity:    {humidity:.1f}%")
            print(f"😊 Comfort:     {comfort:.1f}/100")
            print(f"💨 Dew Point:   {dew_point}°C")
            print(f"⏰ Time:        {datetime.now().strftime('%H:%M:%S')}")
            print("-" * 40)
            
            time.sleep(2)
        
        print("\\nDemo completed! 🎉")
        print("\\nIn a real ROS environment, this data would be published to:")
        print("  • /sensors/temperature")
        print("  • /sensors/humidity") 
        print("  • /sensors/aggregated")
        print("  • /sensors/status")


if __name__ == "__main__":
    demo = SensorDemo()
    demo.run_demo(10)  # Run for 10 seconds