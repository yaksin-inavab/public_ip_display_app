from flask import Flask, jsonify, request
import requests
import socket
import platform
import logging
import signal
import sys
import os

app = Flask(__name__)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Graceful shutdown function
def graceful_shutdown(signum, frame):
    print("Shutting down gracefully...")
    sys.exit(0)

signal.signal(signal.SIGINT, graceful_shutdown)
signal.signal(signal.SIGTERM, graceful_shutdown)

# Log requests
@app.before_request
def log_request_info():
    logging.info(f"Request from {request.remote_addr} to {request.path}")

# Route to display system information
@app.route('/')
def get_system_info():
    public_ip = requests.get('https://api.ipify.org').text
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    os_info = platform.system() + " " + platform.release()
    return jsonify({
        'public_ip': public_ip,
        'hostname': hostname,
        'local_ip': local_ip,
        'os_info': os_info
    })

# Echo message route
@app.route('/echo', methods=['GET'])
def echo_message():
    message = request.args.get('message', 'No message provided')
    return jsonify({'message': message})

# Health check route
@app.route('/status', methods=['GET'])
def status():
    return jsonify({'status': 'ok', 'message': 'Application is running'}), 200

if __name__ == '__main__':
    # Environment-specific configuration
    port = int(os.getenv('PORT', 5000))
    debug = bool(os.getenv('DEBUG', False))
    app.run(host='0.0.0.0', port=port, debug=debug)
    print("MISSION ACCOMPLISHED")