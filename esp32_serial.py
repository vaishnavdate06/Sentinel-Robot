import serial
import threading
import time
import json
import os

ESP32_PORT = "/dev/ttyUSB0"
BAUD_RATE = 115200

sensor_data = {
    "temperature": None,
    "humidity": None,
    "gas": None,
    "ir": None,
    "metal": None
}

esp32 = None
esp32_thread = None
esp32_running = False


def parse_sensor_data(line):
    global sensor_data

    line = line.strip()

    # Ignore debug messages
    if not line.startswith("{") or not line.endswith("}"):
        return

    try:
        data = json.loads(line)

        if "temperature" in data:
            sensor_data["temperature"] = float(data["temperature"])

        if "humidity" in data:
            sensor_data["humidity"] = float(data["humidity"])

        if "mq2" in data:
            sensor_data["gas"] = int(data["mq2"])

        if "ir" in data:
            sensor_data["ir"] = (
                "DETECTED" if int(data["ir"]) == 1 else "CLEAR"
            )

        if "metal" in data:
            sensor_data["metal"] = (
                "DETECTED"
                if int(data["metal"]) == 1
                else "NOT DETECTED"
            )

        print("[ESP32 DATA]", sensor_data, flush=True)

    except json.JSONDecodeError:
        pass

    except Exception as e:
        print("[ESP32] Parsing error:", e, flush=True)


def _esp32_loop():
    global esp32_running
    global esp32

    while esp32_running:

        try:

            # Wait until USB serial device exists
            while esp32_running and not os.path.exists(ESP32_PORT):
                print("[ESP32] Waiting for /dev/ttyUSB0...", flush=True)
                time.sleep(2)

            if not esp32_running:
                break

            print("[ESP32] Connecting to serial port...", flush=True)

            esp32 = serial.Serial(
                port=ESP32_PORT,
                baudrate=BAUD_RATE,
                timeout=2
            )

            print("[ESP32] Serial connected.", flush=True)

            # ESP32 may reset when serial port opens
            time.sleep(3)

            esp32.reset_input_buffer()

            print("[ESP32] Reading sensor data...", flush=True)

            while esp32_running:

                line = esp32.readline()

                if not line:
                    continue

                try:
                    decoded = line.decode(
                        "utf-8",
                        errors="ignore"
                    ).strip()

                    if decoded:
                        parse_sensor_data(decoded)

                except Exception as e:
                    print(
                        "[ESP32] Decode error:",
                        e,
                        flush=True
                    )

        except serial.SerialException as e:

            print(
                "[ESP32] Serial connection lost:",
                e,
                flush=True
            )

        except Exception as e:

            print(
                "[ESP32] Unexpected error:",
                e,
                flush=True
            )

        finally:

            if esp32 is not None:

                try:
                    if esp32.is_open:
                        esp32.close()
                except Exception:
                    pass

                esp32 = None

            if esp32_running:

                print(
                    "[ESP32] Retrying connection in 3 seconds...",
                    flush=True
                )

                time.sleep(3)


def start_esp32():
    global esp32_thread
    global esp32_running

    if esp32_running:
        return

    esp32_running = True

    esp32_thread = threading.Thread(
        target=_esp32_loop,
        daemon=True
    )

    esp32_thread.start()

    print("ESP32 reader started.", flush=True)


def get_sensor_data():
    return sensor_data.copy()


def stop_esp32():
    global esp32_running
    global esp32

    esp32_running = False

    if esp32 is not None:

        try:
            if esp32.is_open:
                esp32.close()
        except Exception:
            pass

        esp32 = None

    if esp32_thread is not None:
        esp32_thread.join(timeout=2)

    print("ESP32 stopped.", flush=True)


if __name__ == "__main__":

    print("======================================")
    print("        ESP32 SENSOR TEST")
    print("======================================")

    start_esp32()

    try:

        while True:

            data = get_sensor_data()

            print()
            print("Temperature:", data["temperature"])
            print("Humidity   :", data["humidity"])
            print("MQ-2       :", data["gas"])
            print("IR         :", data["ir"])
            print("Metal      :", data["metal"])
            print("--------------------------------------")

            time.sleep(1)

    except KeyboardInterrupt:

        print("\nESP32 test stopped.")

    finally:

        stop_esp32()
