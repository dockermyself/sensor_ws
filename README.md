# Sensor Workspace (sensor_ws)

A comprehensive ROS workspace for sensor data collection, processing, and management. This workspace provides a complete framework for working with various sensors including temperature and humidity sensors.

## Features

- **Temperature Sensor Node**: Simulates and publishes temperature data with configurable parameters
- **Humidity Sensor Node**: Simulates and publishes humidity data with realistic variations
- **Sensor Manager**: Aggregates sensor data, monitors sensor health, and calculates derived metrics
- **Configurable Parameters**: Easy configuration through YAML files and launch parameters
- **Health Monitoring**: Real-time sensor status and timeout detection
- **Data Aggregation**: Combined sensor data with comfort index and dew point calculations

## Package Structure

```
sensor_ws/
├── src/
│   └── sensor_package/
│       ├── scripts/                 # Python sensor nodes
│       │   ├── temperature_sensor.py
│       │   ├── humidity_sensor.py
│       │   └── sensor_manager.py
│       ├── launch/                  # Launch files
│       │   ├── sensors.launch
│       │   ├── temperature_only.launch
│       │   └── humidity_only.launch
│       ├── config/                  # Configuration files
│       │   ├── sensor_config.yaml
│       │   └── environment_presets.yaml
│       ├── package.xml
│       └── CMakeLists.txt
└── README.md
```

## Topics

### Published Topics

- `/sensors/temperature` (sensor_msgs/Temperature): Temperature readings with variance
- `/sensors/humidity` (sensor_msgs/RelativeHumidity): Humidity readings with variance
- `/sensors/status` (std_msgs/String): JSON status of all sensors
- `/sensors/aggregated` (std_msgs/String): Combined sensor data with derived metrics

### Message Format Examples

**Temperature Message:**
```
header:
  stamp: 1234567890.123
  frame_id: "temperature_sensor"
temperature: 23.45
variance: 0.25
```

**Aggregated Data:**
```json
{
  "timestamp": 1234567890.123,
  "temperature": {
    "value": 23.45,
    "unit": "celsius",
    "variance": 0.25,
    "frame_id": "temperature_sensor"
  },
  "humidity": {
    "value": 55.2,
    "unit": "percent",
    "variance": 4.0,
    "frame_id": "humidity_sensor"
  },
  "comfort_index": 85.3,
  "dew_point": 14.2
}
```

## Quick Start

### Prerequisites

- ROS Noetic (or compatible version)
- Python 3
- Required ROS packages: `rospy`, `std_msgs`, `sensor_msgs`, `geometry_msgs`

### Build the Workspace

```bash
cd sensor_ws
catkin_make
source devel/setup.bash
```

### Launch All Sensors

```bash
roslaunch sensor_package sensors.launch
```

### Launch Individual Sensors

```bash
# Temperature sensor only
roslaunch sensor_package temperature_only.launch

# Humidity sensor only
roslaunch sensor_package humidity_only.launch
```

### Monitor Sensor Data

```bash
# View temperature data
rostopic echo /sensors/temperature

# View humidity data
rostopic echo /sensors/humidity

# View aggregated data
rostopic echo /sensors/aggregated

# View sensor status
rostopic echo /sensors/status
```

## Configuration

### Launch Parameters

Each sensor node supports the following parameters:

**Temperature Sensor:**
- `publish_rate`: Publishing frequency (default: 1.0 Hz)
- `sensor_frame`: TF frame ID (default: "temperature_sensor")
- `min_temp`: Minimum temperature (default: 15.0°C)
- `max_temp`: Maximum temperature (default: 35.0°C)
- `noise_level`: Temperature noise level (default: 0.5°C)

**Humidity Sensor:**
- `publish_rate`: Publishing frequency (default: 1.0 Hz)
- `sensor_frame`: TF frame ID (default: "humidity_sensor")
- `min_humidity`: Minimum humidity (default: 30.0%)
- `max_humidity`: Maximum humidity (default: 80.0%)
- `noise_level`: Humidity noise level (default: 2.0%)

**Sensor Manager:**
- `publish_rate`: Status publishing frequency (default: 0.5 Hz)
- `sensor_timeout`: Sensor timeout threshold (default: 5.0 seconds)

### Configuration Files

Use the YAML configuration files in the `config/` directory to set up different environments:

- `sensor_config.yaml`: Main sensor configuration
- `environment_presets.yaml`: Predefined environment settings

## Advanced Usage

### Custom Launch File

Create your own launch file with custom parameters:

```xml
<?xml version="1.0"?>
<launch>
  <node name="custom_temp_sensor" pkg="sensor_package" type="temperature_sensor.py" output="screen">
    <param name="publish_rate" value="5.0"/>
    <param name="min_temp" value="10.0"/>
    <param name="max_temp" value="40.0"/>
  </node>
</launch>
```

### Integration with Other Nodes

The sensor data can be easily integrated with other ROS nodes:

```python
import rospy
from sensor_msgs.msg import Temperature

def temperature_callback(msg):
    print(f"Temperature: {msg.temperature}°C")

rospy.init_node('sensor_listener')
rospy.Subscriber('/sensors/temperature', Temperature, temperature_callback)
rospy.spin()
```

## Troubleshooting

1. **No sensor data**: Check if nodes are running with `rosnode list`
2. **Sensor timeout**: Verify publish rates and network connectivity
3. **Build errors**: Ensure all dependencies are installed
4. **Permission errors**: Make sure scripts are executable (`chmod +x scripts/*.py`)

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License - see the package.xml file for details.