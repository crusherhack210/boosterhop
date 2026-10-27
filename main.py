import board, busio
import time
from adafruit_bno08x import BNO_REPORT_ACCELEROMETER
from adafruit_bno08x.i2c import BNO08X_I2C

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
bno = BNO08X_I2C(i2c)
bno.enable_feature(BNO_REPORT_ACCELEROMETER)
while True:
  print(bno.linear_acceleration)
  time.sleep(0.1)
