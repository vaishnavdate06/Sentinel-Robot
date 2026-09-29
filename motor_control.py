from gpiozero import DigitalOutputDevice, PWMOutputDevice
from time import sleep

# ============================================================
# TB6612FNG #1 — FRONT MOTORS
# ============================================================

# Front Left Motor
FL_AIN1 = DigitalOutputDevice(5)
FL_AIN2 = DigitalOutputDevice(6)
FL_PWM  = PWMOutputDevice(12, frequency=1000)

# Front Right Motor
FR_BIN1 = DigitalOutputDevice(13)
FR_BIN2 = DigitalOutputDevice(19)
FR_PWM  = PWMOutputDevice(18, frequency=1000)

# Standby for Driver #1
STBY1 = DigitalOutputDevice(25)


# ============================================================
# TB6612FNG #2 — REAR MOTORS
# ============================================================

# Rear Left Motor
RL_AIN1 = DigitalOutputDevice(20)
RL_AIN2 = DigitalOutputDevice(21)
RL_PWM  = PWMOutputDevice(26, frequency=1000)

# Rear Right Motor
RR_BIN1 = DigitalOutputDevice(16)
RR_BIN2 = DigitalOutputDevice(23)
RR_PWM  = PWMOutputDevice(24, frequency=1000)

# Standby for Driver #2
STBY2 = DigitalOutputDevice(22)


# ============================================================
# ENABLE BOTH MOTOR DRIVERS
# ============================================================

STBY1.on()
STBY2.on()


# ============================================================
# MOTOR FUNCTIONS
# ============================================================

def front_left_forward(speed):
    FL_AIN1.on()
    FL_AIN2.off()
    FL_PWM.value = speed


def front_left_backward(speed):
    FL_AIN1.off()
    FL_AIN2.on()
    FL_PWM.value = speed


def front_left_stop():
    FL_AIN1.off()
    FL_AIN2.off()
    FL_PWM.value = 0


def front_right_forward(speed):
    FR_BIN1.on()
    FR_BIN2.off()
    FR_PWM.value = speed


def front_right_backward(speed):
    FR_BIN1.off()
    FR_BIN2.on()
    FR_PWM.value = speed


def front_right_stop():
    FR_BIN1.off()
    FR_BIN2.off()
    FR_PWM.value = 0


def rear_left_forward(speed):
    RL_AIN1.on()
    RL_AIN2.off()
    RL_PWM.value = speed


def rear_left_backward(speed):
    RL_AIN1.off()
    RL_AIN2.on()
    RL_PWM.value = speed


def rear_left_stop():
    RL_AIN1.off()
    RL_AIN2.off()
    RL_PWM.value = 0


def rear_right_forward(speed):
    RR_BIN1.on()
    RR_BIN2.off()
    RR_PWM.value = speed


def rear_right_backward(speed):
    RR_BIN1.off()
    RR_BIN2.on()
    RR_PWM.value = speed


def rear_right_stop():
    RR_BIN1.off()
    RR_BIN2.off()
    RR_PWM.value = 0


# ============================================================
# COMPLETE ROBOT MOVEMENT FUNCTIONS
# ============================================================

def forward(speed=0.6):

    front_left_forward(speed)
    front_right_forward(speed)
    rear_left_forward(speed)
    rear_right_forward(speed)


def backward(speed=0.6):

    front_left_backward(speed)
    front_right_backward(speed)
    rear_left_backward(speed)
    rear_right_backward(speed)


def stop():

    front_left_stop()
    front_right_stop()
    rear_left_stop()
    rear_right_stop()


def turn_left(speed=0.6):

    # Left side backward
    front_left_backward(speed)
    rear_left_backward(speed)

    # Right side forward
    front_right_forward(speed)
    rear_right_forward(speed)


def turn_right(speed=0.6):

    # Left side forward
    front_left_forward(speed)
    rear_left_forward(speed)

    # Right side backward
    front_right_backward(speed)
    rear_right_backward(speed)


def rotate_left(speed=0.5):

    front_left_backward(speed)
    rear_left_backward(speed)

    front_right_forward(speed)
    rear_right_forward(speed)


def rotate_right(speed=0.5):

    front_left_forward(speed)
    rear_left_forward(speed)

    front_right_backward(speed)
    rear_right_backward(speed)


# ============================================================
# SPEED CONTROL
# ============================================================

def set_speed(speed):

    speed = max(0.0, min(1.0, speed))

    FL_PWM.value = speed
    FR_PWM.value = speed
    RL_PWM.value = speed
    RR_PWM.value = speed


# ============================================================
# SHUTDOWN
# ============================================================

def cleanup():

    stop()

    STBY1.off()
    STBY2.off()

    FL_AIN1.close()
    FL_AIN2.close()
    FL_PWM.close()

    FR_BIN1.close()
    FR_BIN2.close()
    FR_PWM.close()

    RL_AIN1.close()
    RL_AIN2.close()
    RL_PWM.close()

    RR_BIN1.close()
    RR_BIN2.close()
    RR_PWM.close()

    STBY1.close()
    STBY2.close()


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    print("===================================")
    print("  Raspberry Pi 4 Motor Test")
    print("  2 x TB6612FNG / 4 Motors")
    print("===================================")

    try:

        print("Moving FORWARD...")
        forward(0.5)
        sleep(2)

        print("STOP")
        stop()
        sleep(1)

        print("Moving BACKWARD...")
        backward(0.5)
        sleep(2)

        print("STOP")
        stop()
        sleep(1)

        print("Turning LEFT...")
        turn_left(0.5)
        sleep(2)

        print("STOP")
        stop()
        sleep(1)

        print("Turning RIGHT...")
        turn_right(0.5)
        sleep(2)

        print("STOP")
        stop()
        sleep(1)

        print("Motor test completed.")

    except KeyboardInterrupt:

        print("\nTest interrupted by user.")

    finally:

        cleanup()
        print("Motor GPIO cleaned up.")
