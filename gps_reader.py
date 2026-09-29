import serial
import pynmea2
import threading
import time


# ============================================================
# GPS CONFIGURATION
# ============================================================

GPS_PORT = "/dev/serial0"
GPS_BAUDRATE = 9600


# ============================================================
# GPS DATA
# ============================================================

gps_data = {
    "latitude": None,
    "longitude": None,
    "altitude": None,
    "satellites": 0,
    "fix": False
}


gps = None
gps_thread = None
gps_running = False


# ============================================================
# GPS READER
# ============================================================

def _gps_loop():

    global gps_data
    global gps_running

    while gps_running:

        try:

            line = gps.readline().decode(
                "ascii",
                errors="replace"
            ).strip()

            if not line:
                continue

            try:

                message = pynmea2.parse(line)

                # --------------------------------------------
                # GGA
                # --------------------------------------------

                if isinstance(
                    message,
                    pynmea2.types.talker.GGA
                ):

                    if message.latitude:
                        gps_data["latitude"] = message.latitude

                    if message.longitude:
                        gps_data["longitude"] = message.longitude

                    try:
                        gps_data["altitude"] = float(
                            message.altitude
                        )
                    except:
                        pass

                    try:
                        gps_data["satellites"] = int(
                            message.num_sats
                        )
                    except:
                        pass

                    try:
                        gps_data["fix"] = (
                            int(message.gps_qual) > 0
                        )
                    except:
                        pass

                # --------------------------------------------
                # RMC
                # --------------------------------------------

                elif isinstance(
                    message,
                    pynmea2.types.talker.RMC
                ):

                    if message.latitude:
                        gps_data["latitude"] = message.latitude

                    if message.longitude:
                        gps_data["longitude"] = message.longitude

                    gps_data["fix"] = (
                        message.status == "A"
                    )

            except pynmea2.ParseError:

                pass

        except Exception as e:

            print("GPS error:", e)

            time.sleep(1)


# ============================================================
# START GPS
# ============================================================

def start_gps():

    global gps
    global gps_thread
    global gps_running

    if gps_running:
        return

    try:

        gps = serial.Serial(
            GPS_PORT,
            GPS_BAUDRATE,
            timeout=1
        )

        time.sleep(2)

        gps_running = True

        gps_thread = threading.Thread(
            target=_gps_loop,
            daemon=True
        )

        gps_thread.start()

        print("GPS started successfully.")

    except Exception as e:

        print("GPS ERROR:", e)


# ============================================================
# GET GPS DATA
# ============================================================

def get_gps_data():

    return gps_data.copy()


# ============================================================
# STOP GPS
# ============================================================

def stop_gps():

    global gps_running
    global gps

    gps_running = False

    if gps is not None:

        gps.close()

        gps = None


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    print("======================================")
    print("        NEO-M8N GPS TEST")
    print("======================================")

    start_gps()

    try:

        while True:

            data = get_gps_data()

            print()
            print("Latitude :", data["latitude"])
            print("Longitude:", data["longitude"])
            print("Altitude :", data["altitude"])
            print("Satellites:", data["satellites"])
            print("GPS Fix  :", data["fix"])

            print("--------------------------------------")

            time.sleep(2)

    except KeyboardInterrupt:

        print("\nGPS test stopped.")

    finally:

        stop_gps()
