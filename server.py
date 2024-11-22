from flask import Flask, request

app = Flask(__name__)

@app.route('/rfid', methods=['POST'])
def receive_rfid():
    data = request.json
    print(f"Received RFID Data: {data}")
    return "Data received!", 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
