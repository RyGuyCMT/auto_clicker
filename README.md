# Auto Clicker

A threaded, class-based auto clicker utility for Windows automation tasks. This package provides keyboard and mouse automation capabilities with smooth mouse movement, configurable key bindings, and real-time status monitoring.

## Features

- **Threaded Architecture**: Run multiple input automation tasks concurrently
- **Smooth Mouse Movement**: Natural, stepwise mouse movement between coordinates
- **Keyboard Automation**: Automate key presses with configurable hold durations and delays
- **Mouse Clicking**: Programmatic mouse clicks at specified coordinates
- **Real-time Control**: F2-F7 function keys for live control during automation
- **Configuration Module**: Easy customization of actions, delays, and coordinates
- **Shape Generation**: Built-in utilities for generating movement patterns (spirals, rectangles, etc.)

## Installation

Install the package directly from PyPI:

```bash
pip install auto-clicker
```

Or install from source:

```bash
git clone https://github.com/yourusername/auto-clicker.git
cd auto-clicker
pip install -e .
```

## Quick Start

```python
from auto_clicker import Clicker_Main

# Initialize and run the clicker
clicker = Clicker_Main()
clicker.run()
```

## Control Keys

While the clicker is running, use the following function keys:

- **F2**: Display current mouse coordinates
- **F3**: Toggle WASD keyboard movement automation
- **F4**: Toggle mouse movement automation  
- **F5**: Toggle mouse clicking automation
- **F6**: Reload the configuration module
- **F7**: Exit the clicker

## Configuration

Configure automation behavior in `_configurations.py`:

```python
# Set mouse movement coordinates and delays
mouse_moves_xys = [(100, 200, 0.5), (150, 250, 0.5)]

# Set keyboard movement sequences
kb_moves_khw = [("w", 2.0, 0.5), ("d", 2.0, 0.5)]

# Other options
click_delay_s = 0.15
debug = False
```

## Dependencies

- `keyboard>=0.13.5` - Global keyboard input detection
- `pynput>=1.7.6` - Keyboard listener for global hotkeys
- `ait>=1.0.0` - Mouse control utilities

## Requirements

- Windows OS (uses keyboard and mouse automation)
- Python 3.8 or higher

## License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## Author

Ryan

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This tool is provided for educational and legitimate automation purposes. Users are responsible for ensuring their use of this software complies with all applicable laws and the terms of service of any applications they automate.
