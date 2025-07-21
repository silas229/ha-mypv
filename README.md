# MyPV Home Assistant Addon

An addon that integrates the MyPV app into Home Assistant.

## Supported Devices

- MyPV ELWA 2
- Feel free to contribute the HTML page for other models

## Features

- Web interface for MyPV devices
- Configurable device IP address
- Home Assistant Ingress integration
- Sidebar panel integration
- Easy installation and configuration

## Installation

[![Open your Home Assistant instance and show the add add-on repository dialog with a specific repository URL pre-filled.](https://my.home-assistant.io/badges/supervisor_add_addon_repository.svg)](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fsilas229%2Fha-mypv)

1. Add this [repository](https://my.home-assistant.io/redirect/supervisor_add_addon_repository/?repository_url=https%3A%2F%2Fgithub.com%2Fsilas229%2Fha-mypv) to your Home Assistant addon repositories (or click the button above)
2. Install the "MyPV" addon
3. Configure the IP address of your device
4. Start the addon

## Configuration

- `device_ip`: IP address of the MyPV device (default: 192.168.1.100)
- `device_port`: Port of the MyPV device (default: 80)
- `log_level`: Log level for the addon (info, debug, etc.)

## Usage

After installation and configuration, the interface automatically appears in the Home Assistant sidebar. The addon uses Home Assistant Ingress for secure and seamless integration.

### Access via Ingress

The interface is available through Home Assistant Ingress and appears as a panel in the sidebar with the name "MyPV Heizstab".

### API Endpoints

The addon provides these MyPV-specific endpoints:

- `/mypv_dev.jsn` - Device information
- `/data.jsn` - Current sensor data
- `/chart.jsn` - Chart/historical data
- `/setup.jsn` - Setup configuration
- `/api/wifidata.jsn` - WiFi status data

## Development

The addon uses Python Flask as a proxy server and serves the original HTML file as a static asset. The proxy adapter intercepts all API calls and routes them through the Flask server.
