from gpiozero import DigitalOutputDevice, DigitalInputDevice
from time import monotonic, sleep


# ============================================================
# GPIO CONFIGURATION
# ============================================================

# FRONT
FRONT_TRIG_PIN = 17
FRONT_ECHO_PIN = 27

# LEFT
LEFT_TRIG_PIN = 4
LEFT_ECHO_PIN = 8

# RIGHT
RIGHT_TRIG_PIN = 10
RIGHT_ECHO_PIN = 9


# ============================================================
# GPIO DEVICES
# ============================================================

front_trig = DigitalOutputDevice(
    FRONT_TRIG_PIN,
    initial_value=False
)

front_echo = DigitalInputDevice(FRONT_ECHO_PIN)


left_trig = DigitalOutputDevice(
    LEFT_TRIG_PIN,
    initial_value=False
)

left_echo = DigitalInputDevice(LEFT_ECHO_PIN)


right_trig = DigitalOutputDevice(
    RIGHT_TRIG_PIN,
    initial_value=False
)

right_echo = DigitalInputDevice(RIGHT_ECHO_PIN)


# ============================================================
# MEASURE DISTANCE
# ============================================================

def measure_distance(trig, echo):

    trig.off()

    sleep(0.000002)

    trig.on()
    sleep(0.00001)
    trig.off()

    # Wait for echo HIGH
    start_wait = monotonic()

    while not echo.is_active:

        if monotonic() - start_wait > 0.03:
            return None

    pulse_start = monotonic()

    # Wait for echo LOW
    while echo.is_active:

        if monotonic() - pulse_start > 0.03:
            return None

    pulse_end = monotonic()

    pulse_time = pulse_end - pulse_start

    distance_cm = (pulse_time * 34300) / 2

    if distance_cm < 2 or distance_cm > 400:
        return None

    return round(distance_cm, 1)


# ============================================================
# INDIVIDUAL SENSOR FUNCTIONS
# ============================================================

def get_front_distance():

    return measure_distance(
        front_trig,
        front_echo
    )


def get_left_distance():

    return measure_distance(
        left_trig,
        left_echo
    )


def get_right_distance():

    return measure_distance(
        right_trig,
        right_echo
    )


# ============================================================
# ALL THREE SENSORS
# ============================================================

def get_all_distances():

    front = get_front_distance()

    sleep(0.05)

    left = get_left_distance()

    sleep(0.05)

    right = get_right_distance()

    return {
        "front": front,
        "left": left,
        "right": right
    }


# ============================================================
# OBSTACLE DETECTION
# ============================================================

def obstacle_detected(distance, limit=30):

    if distance is None:
        return False

    return distance < limit


def get_obstacle_status():

    distances = get_all_distances()

    return {
        "front": obstacle_detected(distances["front"]),
        "left": obstacle_detected(distances["left"]),
        "right": obstacle_detected(distances["right"])
    }


# ============================================================
# CLEANUP
# ============================================================

def cleanup():

    front_trig.close()
    front_echo.close()

    left_trig.close()
    left_echo.close()

    right_trig.close()
    right_echo.close()


# ============================================================
# STANDALONE TEST
# ============================================================

if __name__ == "__main__":

    print("======================================")
    print("   3-SENSOR ULTRASONIC TEST")
    print("======================================")

    print("Front : TRIG GPIO17 / ECHO GPIO27")
    print("Left  : TRIG GPIO4  / ECHO GPIO8")
    print("Right : TRIG GPIO10 / ECHO GPIO9")
    print("--------------------------------------")

    try:

        while True:

            distances = get_all_distances()

            front = distances["front"]
            left = distances["left"]
            right = distances["right"]

            if front is None:
                print("Front: No reading", end=" | ")
            else:
                print(
                    f"Front: {front:.1f} cm",
                    end=" | "
                )

            if left is None:
                print("Left: No reading", end=" | ")
            else:
                print(
                    f"Left: {left:.1f} cm",
                    end=" | "
                )

            if right is None:
                print("Right: No reading")
            else:
                print(
                    f"Right: {right:.1f} cm"
                )

            if obstacle_detected(front):
                print("⚠ FRONT OBSTACLE!")

            if obstacle_detected(left):
                print("⚠ LEFT OBSTACLE!")

            if obstacle_detected(right):
                print("⚠ RIGHT OBSTACLE!")

            print("--------------------------------------")

            sleep(0.2)

    except KeyboardInterrupt:

        print("\nUltrasonic test stopped.")

    finally:

        cleanup()

        print("GPIO cleaned up.")
