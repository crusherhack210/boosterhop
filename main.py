import time, math
import board, busio
from adafruit_bno08x import BNO_REPORT_LINEAR_ACCELERATION
from adafruit_bno08x.i2c import BNO08X_I2C

i2c = busio.I2C(board.SCL, board.SDA)
bno = BNO08X_I2C(i2c)
bno.enable_feature(BNO_REPORT_LINEAR_ACCELERATION)

vx = vy = vz = 0.0
still_count = 0
last = time.monotonic()
posx = 0
posy = 0
posz = 0
while True:
    ax, ay, az = bno.linear_acceleration
    now = time.monotonic()
    dt = now - last
    last = now

    mag = math.sqrt(ax*ax + ay*ay + az*az)

    if mag < 0.15:                 # deadband: treat tiny readings as noise
        ax = ay = az = 0.0
        still_count += 1
    else:
        still_count = 0

    vx += ax * dt
    vy += ay * dt
    vz += az * dt

    if still_count > 10:           # stationary for a while: reset velocity
        vx = vy = vz = 0.0
    posx += vx *dt
    posy += vy *dt
    posz += vz *dt
    print(str(posx) + " " + str(posy) + " " + str(posz))
    time.sleep(0.02)
