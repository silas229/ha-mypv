#!/usr/bin/env python3
"""
MyPV Heizstab Proxy Server for Home Assistant Addon
Provides CORS proxy functionality for MyPV Heizstab devices
"""

import os
import json
import logging
import requests
from flask import Flask, request, Response, jsonify, send_from_directory
from flask_cors import CORS

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Check if running under Home Assistant Ingress
INGRESS_ENTRY = os.environ.get('INGRESS_ENTRY', '')
INGRESS_TOKEN = os.environ.get('INGRESS_TOKEN', '')

def get_base_path():
    """Get the base path for URLs when running under Ingress"""
    if INGRESS_ENTRY:
        return INGRESS_ENTRY.rstrip('/')
    return ''

def is_ingress():
    """Check if running under Home Assistant Ingress"""
    return bool(INGRESS_ENTRY)

# Read configuration from Home Assistant addon options
def get_config():
    """Read configuration from addon options"""
    try:
        with open('/data/options.json', 'r') as f:
            options = json.load(f)
    except FileNotFoundError:
        # Default configuration for development
        options = {
            'device_ip': '192.168.1.100',
            'device_port': 80,
            'log_level': 'info'
        }
    
    # Set log level
    log_level = options.get('log_level', 'info').upper()
    logging.getLogger().setLevel(getattr(logging, log_level, logging.INFO))
    
    return options

config = get_config()
DEVICE_IP = config['device_ip']
DEVICE_PORT = config['device_port']
DEVICE_BASE_URL = f"http://{DEVICE_IP}:{DEVICE_PORT}"

logger.info(f"Starting MyPV Heizstab Proxy - Device: {DEVICE_BASE_URL}")
if is_ingress():
    logger.info(f"Running under Home Assistant Ingress: {INGRESS_ENTRY}")

@app.route('/')
def index():
    """Serve the main HTML interface"""
    return send_from_directory('static', 'index.html')

@app.route('/static/<path:filename>')
def static_files(filename):
    """Serve static files"""
    return send_from_directory('static', filename)

# Add Ingress support for static files
if is_ingress():
    @app.route(f'{get_base_path()}/static/<path:filename>')
    def ingress_static_files(filename):
        """Serve static files under Ingress"""
        return send_from_directory('static', filename)

# MyPV specific API endpoints
@app.route('/mypv_dev.jsn')
def get_mypv_dev():
    """Get device information"""
    return proxy_request('/mypv_dev.jsn')

@app.route('/data.jsn')
def get_data():
    """Get current data"""
    return proxy_request('/data.jsn')

@app.route('/chart.jsn')
def get_chart():
    """Get chart data"""
    return proxy_request('/chart.jsn')

@app.route('/setup.jsn')
def get_setup():
    """Get setup data"""
    return proxy_request('/setup.jsn')

@app.route('/api/wifidata.jsn')
def get_wifidata():
    """Get wifi data"""
    return proxy_request('/api/wifidata.jsn')

# Generic proxy route for any other requests
@app.route('/api/proxy')
def proxy_generic():
    """Generic proxy for any other requests"""
    target_path = request.args.get('path', '/')
    return proxy_request(target_path)

def proxy_request(path):
    """
    Internal function to proxy requests to MyPV device
    Handles CORS issues by acting as a proxy
    """
    try:
        target_url = f"{DEVICE_BASE_URL}{path}"
        logger.debug(f"Proxying request to: {target_url}")
        
        # Forward query parameters
        params = {k: v for k, v in request.args.items() if k != 'path'}
        
        # Make request to device
        response = requests.get(
            target_url,
            params=params,
            timeout=10
        )
        
        # Create response with CORS headers
        flask_response = Response(
            response.content,
            status=response.status_code,
            content_type=response.headers.get('content-type', 'application/json')
        )
        
        # Add CORS headers
        flask_response.headers['Access-Control-Allow-Origin'] = '*'
        flask_response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        flask_response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        
        return flask_response
        
    except requests.exceptions.ConnectionError:
        logger.error(f"Could not connect to device at {DEVICE_BASE_URL}")
        return jsonify({
            "error": "Could not connect to MyPV Heizstab device",
            "device_url": DEVICE_BASE_URL,
            "path": path
        }), 503
    except requests.exceptions.Timeout:
        logger.error(f"Timeout connecting to device at {DEVICE_BASE_URL}")
        return jsonify({
            "error": "Timeout connecting to MyPV Heizstab device",
            "path": path
        }), 504
    except Exception as e:
        logger.error(f"Proxy error: {str(e)}")
        return jsonify({
            "error": f"Proxy error: {str(e)}",
            "path": path
        }), 500

@app.route('/api/config')
def get_config_info():
    """Return current configuration info"""
    return jsonify({
        "device_ip": DEVICE_IP,
        "device_port": DEVICE_PORT,
        "device_url": DEVICE_BASE_URL,
        "status": "running"
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Try to ping the device
        response = requests.get(f"{DEVICE_BASE_URL}/", timeout=5)
        device_status = "reachable" if response.status_code < 500 else "error"
    except:
        device_status = "unreachable"
    
    return jsonify({
        "status": "healthy",
        "device_status": device_status,
        "device_url": DEVICE_BASE_URL
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
