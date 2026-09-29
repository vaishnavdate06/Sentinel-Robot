from flask import Flask, render_template, jsonify, request
from datetime import datetime
import time

import ultrasonic
import gps_reader
import esp32_serial


# ============================================================
# FLASK
# ============================================================

app = Flask(__name__)


# ============================================================
# MOTOR SIMULATION
# ============================================================

# Keep TRUE until your replacement motor driver arrives.
SIMULATION_MODE = True

current_motor_command = "STOP"


def motor_command(command):

    global current_motor_command

    command = command.upper()

    valid_commands = [
        "FORWARD",
        "BACKWARD",
        "LEFT",
        "RIGHT",
        "STOP"
    ]

    if command not in valid_commands:

        return False

    current_motor_command = command

    if SIMULATION_MODE:

        print(
            "[SIMULATION] Motor command:",
            command
        )

    else:

        # Real motor functions will be connected later.
        print(
            "[MOTOR]",
            command
        )

    return True


# ============================================================
# SENSOR DATA
# ============================================================

def get_all_sensor_data():

    # --------------------------------------------------------
    # ULTRASONIC
    # --------------------------------------------------------

    distances = ultrasonic.get_all_distances()


    # --------------------------------------------------------
    # GPS
    # --------------------------------------------------------

    gps = gps_reader.get_gps_data()


    # --------------------------------------------------------
    # ESP32
    # --------------------------------------------------------

    esp = esp32_serial.get_sensor_data()


    # --------------------------------------------------------
    # COMBINE EVERYTHING
    # --------------------------------------------------------

    return {

        # Ultrasonic
        "front": distances["front"],
        "left": distances["left"],
        "right": distances["right"],

        # ESP32
        "temperature": esp["temperature"],
        "humidity": esp["humidity"],
        "gas": esp["gas"],
        "ir": esp["ir"],
        "metal": esp["metal"],

        # GPS
        "latitude": gps["latitude"],
        "longitude": gps["longitude"],
        "altitude": gps["altitude"],
        "satellites": gps["satellites"],
        "gps_fix": gps["fix"],

        # Motor
        "motor": current_motor_command,

        # Time
        "time": datetime.now().strftime(
            "%H:%M:%S"
        )
    }


# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
def index():

    return render_template(
        "index.html",
        simulation=SIMULATION_MODE
    )


# ============================================================
# SENSOR API
# ============================================================

@app.route("/api/sensors")
def sensors():

    try:

        data = get_all_sensor_data()

        return jsonify(data)

    except Exception as e:

        print("Sensor API error:", e)

        return jsonify({
            "error": str(e)
        }), 500


# ============================================================
# MOTOR API
# ============================================================

@app.route("/api/motor", methods=["POST"])
def motor():

    data = request.get_json()

    if not data:

        return jsonify({
            "success": False,
            "message": "No data received"
        }), 400


    command = data.get("command")


    if command is None:

        return jsonify({
            "success": False,
            "message": "No command received"
        }), 400


    success = motor_command(command)


    return jsonify({

        "success": success,

        "command": current_motor_command,

        "simulation": SIMULATION_MODE

    })


# ============================================================
# START HARDWARE
# ============================================================

def start_hardware():

    print()
    print("======================================")
    print("Starting robot hardware...")
    print("======================================")


    # GPS

    try:

        gps_reader.start_gps()

    except Exception as e:

        print("GPS startup failed:", e)


    # ESP32

    try:

        esp32_serial.start_esp32()

    except Exception as e:

        print("ESP32 startup failed:", e)


    print()
    print("Hardware startup complete.")
    print()


# ============================================================
# STOP HARDWARE
# ============================================================

def stop_hardware():

    print("Stopping hardware...")


    try:

        gps_reader.stop_gps()

    except Exception:
        pass


    try:

        esp32_serial.stop_esp32()

    except Exception:
        pass


    try:

        ultrasonic.cleanup()

    except Exception:
        pass


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print()
    print("==========================================")
    print(" ROBOT SURVEILLANCE DASHBOARD")
    print("==========================================")

    if SIMULATION_MODE:

        print(
            "Motor mode: SIMULATION"
        )

    else:

        print(
            "Motor mode: REAL"
        )


    # Start GPS + ESP32

    start_hardware()


    print(
        "Starting Flask server..."
    )

    print(
        "Open:"
    )

    print(
        "http://<RASPBERRY-PI-IP>:5000"
    )

    print()


    try:

        app.run(
            host="0.0.0.0",
            port=5000,
            debug=False,
            threaded=True
        )

    except KeyboardInterrupt:

        print("\nServer stopped.")

    finally:

        stop_hardware()
