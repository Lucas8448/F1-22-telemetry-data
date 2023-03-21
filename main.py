import socket
import threading
from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Set up UDP server
UDP_IP = "0.0.0.0"
UDP_PORT = 20777
BUFFER_SIZE = 2048

received_data = None


def udp_server():
    global received_data
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))

    while True:
        data, addr = sock.recvfrom(BUFFER_SIZE)
        received_data = data


def parse_data(data):
    return {'data': data}


@app.route('/')
def get_telemetry_data():
    global received_data
    if received_data:
        print(received_data)
        return jsonify(parse_data(received_data))
    else:
        print("None")
        return jsonify({'error': 'No data received'})


if __name__ == '__main__':
    udp_thread = threading.Thread(target=udp_server)
    udp_thread.daemon = True
    udp_thread.start()

    app.run(host='0.0.0.0', port=5000, debug=True)
