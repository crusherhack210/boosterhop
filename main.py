import time
import board, busio
from adafruit_bno08x import BNO_REPORT_LINEAR_ACCELERATION
from adafruit_bno08x.i2c import BNO08X_I2C

i2c = busio.I2C(board.SCL, board.SDA)
bno = BNO08X_I2C(i2c)
bno.enable_feature(BNO_REPORT_LINEAR_ACCELERATION)

while True:
    x, y, z = bno.linear_acceleration
    print(f"{x:6.2f} {y:6.2f} {z:6.2f}")
    time.sleep(0.05)
