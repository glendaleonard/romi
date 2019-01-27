import sys
import Adafruit_GPIO.I2C as I2C

I2C_ADDRESS = 0x6b

# configuration registers for accelerometer
CTRL1_XL = 0x10

# data registers for accelerometer
OUTX_L_XL = 0x28  # auto incr will also read 0x29
OUTY_L_XL = 0x2A  # auto incr will also read 0x2B
OUTZ_L_XL = 0x2C  # auto incr will also read 0x2D

# configuration registers for gyro
CTRL2_G = 0X11

# data registers for gyro
OUTX_L_G = 0x22  # auto incr will also read 0x23
OUTY_L_G = 0x24  # auto incr will also read 0x25
OUTZ_L_G = 0x26  # auto incr will also read 0x27


class LSM6DS33:
    i2c = None
    tempvar = 0
    global accel_center_x
    accel_center_x = 0
    global accel_center_y
    accel_center_y = 0
    global accel_center_z
    accel_center_z = 0

    def __init__(self, debug=0, pause=0.8):
        self.i2c = I2C.get_i2c_device(I2C_ADDRESS)

        # initialize acc

        # To set output data rate (ODR) = 1.66KHz and scale to +- 2g (00) use 0x80
        # To set output data rate (ODR) = 1.66KHz and scale to +- 4g (10) use 0x88
        # To set output data rate (ODR) = 1.66KHz and scale to +- 8g (11) use 0x8C
        # To set output data rate (ODR) = 1.66KHz and scale to +- 16g (01) use 0x84
        data_to_write = 0
        data_to_write |= 0x80
        self.i2c.write8(CTRL1_XL, data_to_write)

        # initial gyro

        # To set output data rate (ODR) = 1.66KHz and scale to +- 245 dps (00) use 0x80
        # To set output data rate (ODR) = 1.66KHz and scale to +- 500 dps (01) use 0x84
        # To set output data rate (ODR) = 1.66KHz and scale to +- 1000 dps (10) use 0x88
        # To set output data rate (ODR) = 1.66KHz and scale to +- 2000 dps (11) use 0x8C
        data_to_write = 0
        data_to_write |= 0x80
        self.i2c.write8(CTRL2_G, data_to_write)

        accel_center_x = self.i2c.readS16(0X28)
        accel_center_y = self.i2c.readS16(0x2A)
        accel_center_z = self.i2c.readS16(0x2C)

    def read_raw_accel_x(self):
        output = self.i2c.readS16(OUTX_L_XL)
        return output

    def read_raw_accel_y(self):
        output = self.i2c.readS16(OUTY_L_XL)
        return output

    def read_raw_accel_z(self):
        output = self.i2c.readS16(OUTZ_L_XL)
        return output

    def read_raw_gyro_x(self):
        output = self.i2c.readS16(OUTX_L_G)
        return output

    def read_raw_gyro_y(self):
        output = self.i2c.readS16(OUTY_L_G)
        return output

    def read_raw_gyro_z(self):
        output = self.i2c.readS16(OUTZ_L_G)
        return output

    '''def read_float_gyro_x(self):
        output = self.calc_gyro(self.read_raw_gyro_x())
        return output

    def calc_gyro_x_angle(self):
        temp = 0
        temp += self.read_float_gyro_x()
        if temp > 3 or temp < 0:
            self.tempvar += temp
        return self.tempvar

    def calc_gyro(self, raw_input):
        gyro_range_divisor = 245 / 125  # 500 is the gyro range (DPS)
        output = raw_input * 4.375 * gyro_range_divisor / 1000
        return output
'''


def main(argv):
    lsmd = LSM6DS33()

    raw_acc_x = lsmd.read_raw_accel_x()
    raw_acc_y = lsmd.read_raw_accel_y()
    raw_acc_z = lsmd.read_raw_accel_z()
    # dividing by 16393 (0x4009) which is what 1g measures as.
    print("raw acc X: {} raw acc Y: {} raw acc Z: {}".format(raw_acc_x, raw_acc_y, raw_acc_z))
    print("acc X: {} acc Y: {} acc Z: {}".format(raw_acc_x/16393, raw_acc_y/16393, raw_acc_z/16393))
    print("------------------------------")
    raw_gyro_x = lsmd.read_raw_gyro_x()
    raw_gyro_y = lsmd.read_raw_gyro_y()
    raw_gyro_z = lsmd.read_raw_gyro_z()
    print("raw gyro X: {} raw gyro Y: {} raw gyro Z: {}".format(raw_gyro_x, raw_gyro_y, raw_gyro_z))


if __name__ == '__main__':
    main(sys.argv[1:])