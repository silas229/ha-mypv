<!-- Use this file to provide workspace-specific custom instructions to Copilot. For more details, visit https://code.visualstudio.com/docs/copilot/copilot-customization#_use-a-githubcopilotinstructionsmd-file -->

# MyPV Heizstab Home Assistant Addon

This is a Home Assistant Addon project that provides a web interface for MyPV Heizstab devices with CORS proxy functionality.

## Project Structure

- `proxy_server.py` - Python Flask server that acts as a proxy to bypass CORS restrictions
- `static/heizstab.html` - Main web interface (modified from original MyPV interface)
- `static/proxy-adapter.js` - JavaScript adapter that intercepts API calls and routes them through the proxy
- `config.yaml` - Home Assistant addon configuration
- `Dockerfile` - Container configuration
- `run.sh` - Startup script

## Key Features

- Proxies MyPV device API calls (*.jsn endpoints)
- Handles CORS headers properly
- Configurable device IP address
- Web interface accessible through Home Assistant
- Real-time data display and device control

## API Endpoints

The addon proxies these MyPV device endpoints:
- `/mypv_dev.jsn` - Device information
- `/data.jsn` - Current sensor data
- `/chart.jsn` - Chart/historical data
- `/setup.jsn` - Setup configuration
- `/api/wifidata.jsn` - WiFi status data

## Development Notes

- The original HTML file uses JavaScript to make direct API calls to MyPV devices
- Our proxy-adapter.js intercepts these calls and routes them through the Flask proxy
- CORS headers are added by the Python proxy server
- The addon can be configured with the target device IP address through Home Assistant
