import time, math
import board, busio
from adafruit_bno08x import BNO_REPORT_LINEAR_ACCELERATION, BNO_REPORT_ROTATION_VECTOR
from adafruit_bno08x.i2c import BNO08X_I2C

i2c = busio.I2C(board.SCL, board.SDA)
bno = BNO08X_I2C(i2c)
bno.enable_feature(BNO_REPORT_LINEAR_ACCELERATION, 10000)  # 100 Hz
bno.enable_feature(BNO_REPORT_ROTATION_VECTOR, 10000)

def cross(a, b):
    return (a[1]*b[2]-a[2]*b[1], a[2]*b[0]-a[0]*b[2], a[0]*b[1]-a[1]*b[0])

def rotate(q, v):
    """Rotate sensor-frame vector v into world frame using quaternion q = (i, j, k, real)."""
    qv = q[:3]
    qw = q[3]
    t = cross(qv, v)
    t = (2*t[0], 2*t[1], 2*t[2])
    c = cross(qv, t)
    return (v[0] + qw*t[0] + c[0],
            v[1] + qw*t[1] + c[1],
            v[2] + qw*t[2] + c[2])

vel = [0.0, 0.0, 0.0]
pos = [0.0, 0.0, 0.0]
still_count = 0
last = time.monotonic()

while True:
    try:
        a = bno.linear_acceleration
        q = bno.quaternion
    except (KeyError, RuntimeError, OSError):
        time.sleep(0.01)
        continue

    now = time.monotonic()
    dt = now - last
    last = now

    aw = rotate(q, a)  # acceleration in world frame

    if math.sqrt(aw[0]**2 + aw[1]**2 + aw[2]**2) < 0.15:
        aw = (0.0, 0.0, 0.0)
        still_count += 1
    else:
        still_count = 0

    for i in range(3):
        vel[i] += aw[i] * dt
        pos[i] += vel[i] * dt

    if still_count > 10:
        vel = [0.0, 0.0, 0.0]

    print(f"pos = ({pos[0]:6.2f}, {pos[1]:6.2f}, {pos[2]:6.2f}) m")
    time.sleep(0.01)
