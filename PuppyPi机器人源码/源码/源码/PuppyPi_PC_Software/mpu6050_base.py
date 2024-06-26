"""This program handles the communication over I2C
between a Raspberry Pi and a MPU-6050 Gyroscope / Accelerometer combo.
Made by: MrTijn/Tijndagamer
Released under the MIT License
Copyright (c) 2015, 2016, 2017 MrTijn/Tijndagamer
"""

import smbus, struct#, math

class MPU6050Base:

    # Global Variables
    GRAVITIY_MS2 = 9.80665
    address = None
    bus = None

    # Scale Modifiers
    ACCEL_SCALE_MODIFIER_2G = 16384.0
    ACCEL_SCALE_MODIFIER_4G = 8192.0
    ACCEL_SCALE_MODIFIER_8G = 4096.0
    ACCEL_SCALE_MODIFIER_16G = 2048.0

    GYRO_SCALE_MODIFIER_250DEG = 131.0
    GYRO_SCALE_MODIFIER_500DEG = 65.5
    GYRO_SCALE_MODIFIER_1000DEG = 32.8
    GYRO_SCALE_MODIFIER_2000DEG = 16.4

    # Pre-defined ranges
    ACCEL_RANGE_2G = 0x00
    ACCEL_RANGE_4G = 0x08
    ACCEL_RANGE_8G = 0x10
    ACCEL_RANGE_16G = 0x18

    GYRO_RANGE_250DEG = 0x00
    GYRO_RANGE_500DEG = 0x08
    GYRO_RANGE_1000DEG = 0x10
    GYRO_RANGE_2000DEG = 0x18

    # MPU-6050 Registers
    PWR_MGMT_1 = 0x6B
    PWR_MGMT_2 = 0x6C

    ACCEL_XOUT0 = 0x3B
    ACCEL_YOUT0 = 0x3D
    ACCEL_ZOUT0 = 0x3F

    TEMP_OUT0 = 0x41

    GYRO_XOUT0 = 0x43
    GYRO_YOUT0 = 0x45
    GYRO_ZOUT0 = 0x47

    ACCEL_CONFIG = 0x1C
    GYRO_CONFIG = 0x1B

    def __init__(self, address=0x68, bus=1):
        self.address = address
        self.bus = smbus.SMBus(bus)
        # Wake up the MPU-6050 since it starts in sleep mode
        for i in range(10):
            try:
                self.bus.write_byte_data(self.address, self.PWR_MGMT_1, 0x00)
                self.set_accel_range(self.ACCEL_RANGE_2G)
                self.set_gyro_range(self.GYRO_RANGE_2000DEG)
            except:
                pass


        # self.SecondOrderFilterX = self._SecondOrderFilter()
        # self.SecondOrderFilterY = self._SecondOrderFilter()
        
    # I2C communication methods

    def read_i2c_word(self, register):
        """Read two i2c registers and combine them.

        register -- the first register to read from.
        Returns the combined read results.
        """
        # Read the data from the registers
        high = self.bus.read_byte_data(self.address, register)
        low = self.bus.read_byte_data(self.address, register + 1)

        value = (high << 8) + low

        if (value >= 0x8000):
            return -((65535 - value) + 1)
        else:
            return value

    # MPU-6050 Methods

    def get_temp(self):
        """Reads the temperature from the onboard temperature sensor of the MPU-6050.

        Returns the temperature in degrees Celcius.
        """
        raw_temp = self.read_i2c_word(self.TEMP_OUT0)

        # Get the actual temperature using the formule given in the
        # MPU-6050 Register Map and Descriptions revision 4.2, page 30
        actual_temp = (raw_temp / 340.0) + 36.53

        return actual_temp

    def set_accel_range(self, accel_range):
        """Sets the range of the accelerometer to range.

        accel_range -- the range to set the accelerometer to. Using a
        pre-defined range is advised.
        """
        # First change it to 0x00 to make sure we write the correct value later
        self.bus.write_byte_data(self.address, self.ACCEL_CONFIG, 0x00)

        # Write the new range to the ACCEL_CONFIG register
        self.bus.write_byte_data(self.address, self.ACCEL_CONFIG, accel_range)

    def read_accel_range(self, raw = False):
        """Reads the range the accelerometer is set to.

        If raw is True, it will return the raw value from the ACCEL_CONFIG
        register
        If raw is False, it will return an integer: -1, 2, 4, 8 or 16. When it
        returns -1 something went wrong.
        """
        raw_data = self.bus.read_byte_data(self.address, self.ACCEL_CONFIG)

        if raw is True:
            return raw_data
        elif raw is False:
            if raw_data == self.ACCEL_RANGE_2G:
                return 2
            elif raw_data == self.ACCEL_RANGE_4G:
                return 4
            elif raw_data == self.ACCEL_RANGE_8G:
                return 8
            elif raw_data == self.ACCEL_RANGE_16G:
                return 16
            else:
                return -1

    def get_accel_data(self, g = False):
        """Gets and returns the X, Y and Z values from the accelerometer.

        If g is True, it will return the data in g
        If g is False, it will return the data in m/s^2
        Returns a dictionary with the measurement results.
        """
        x = self.read_i2c_word(self.ACCEL_XOUT0)
        y = self.read_i2c_word(self.ACCEL_YOUT0)
        z = self.read_i2c_word(self.ACCEL_ZOUT0)

        accel_scale_modifier = None
        accel_range = self.read_accel_range(True)

        if accel_range == self.ACCEL_RANGE_2G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G
        elif accel_range == self.ACCEL_RANGE_4G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_4G
        elif accel_range == self.ACCEL_RANGE_8G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_8G
        elif accel_range == self.ACCEL_RANGE_16G:
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_16G
        else:
            print("Unkown range - accel_scale_modifier set to self.ACCEL_SCALE_MODIFIER_2G")
            accel_scale_modifier = self.ACCEL_SCALE_MODIFIER_2G

        

        x = x / accel_scale_modifier
        y = y / accel_scale_modifier
        z = z / accel_scale_modifier

        if g is True:
            return {'x': x, 'y': y, 'z': z}
        elif g is False:
            x = x * self.GRAVITIY_MS2
            y = y * self.GRAVITIY_MS2
            z = z * self.GRAVITIY_MS2
            return {'x': x, 'y': y, 'z': z}


    def set_gyro_range(self, gyro_range):
        """Sets the range of the gyroscope to range.

        gyro_range -- the range to set the gyroscope to. Using a pre-defined
        range is advised.
        """
        # First change it to 0x00 to make sure we write the correct value later
        self.bus.write_byte_data(self.address, self.GYRO_CONFIG, 0x00)

        # Write the new range to the ACCEL_CONFIG register
        self.bus.write_byte_data(self.address, self.GYRO_CONFIG, gyro_range)

    def read_gyro_range(self, raw = False):
        """Reads the range the gyroscope is set to.

        If raw is True, it will return the raw value from the GYRO_CONFIG
        register.
        If raw is False, it will return 250, 500, 1000, 2000 or -1. If the
        returned value is equal to -1 something went wrong.
        """
        raw_data = self.bus.read_byte_data(self.address, self.GYRO_CONFIG)

        if raw is True:
            return raw_data
        elif raw is False:
            if raw_data == self.GYRO_RANGE_250DEG:
                return 250
            elif raw_data == self.GYRO_RANGE_500DEG:
                return 500
            elif raw_data == self.GYRO_RANGE_1000DEG:
                return 1000
            elif raw_data == self.GYRO_RANGE_2000DEG:
                return 2000
            else:
                return -1

    def get_gyro_data(self):
        """Gets and returns the X, Y and Z values from the gyroscope.

        Returns the read values in a dictionary.
        """
        x = self.read_i2c_word(self.GYRO_XOUT0)
        y = self.read_i2c_word(self.GYRO_YOUT0)
        z = self.read_i2c_word(self.GYRO_ZOUT0)

        gyro_scale_modifier = None
        gyro_range = self.read_gyro_range(True)

        if gyro_range == self.GYRO_RANGE_250DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG
        elif gyro_range == self.GYRO_RANGE_500DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_500DEG
        elif gyro_range == self.GYRO_RANGE_1000DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_1000DEG
        elif gyro_range == self.GYRO_RANGE_2000DEG:
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_2000DEG
        else:
            print("Unkown range - gyro_scale_modifier set to self.GYRO_SCALE_MODIFIER_250DEG")
            gyro_scale_modifier = self.GYRO_SCALE_MODIFIER_250DEG

        x = x / gyro_scale_modifier
        y = y / gyro_scale_modifier
        z = z / gyro_scale_modifier

        return {'x': x, 'y': y, 'z': z}

    def get_all_data(self):
        """Reads and returns all the available data."""
        data = self.bus.read_i2c_block_data(self.address,self.ACCEL_XOUT0,14)
        data = struct.unpack('>hhhhhhh',bytes(data))

        temp = (data[3] / 340.0) + 36.53

        accel = data[:3]
        accel = [a/self.ACCEL_SCALE_MODIFIER_2G*self.GRAVITIY_MS2 for a in accel]
        gyro = data[-3:]
        gyro = [g/self.GYRO_SCALE_MODIFIER_2000DEG for g in gyro]
        # temp = self.get_temp()
        # accel = self.get_accel_data()
        # gyro = self.get_gyro_data()

        return {"accel":accel, "gyro":gyro, "temp":temp}

    # def _SecondOrderFilter(self):
    #     x1=0
    #     x2=0
    #     y1=0
    #     angle = 0
    #     K2 =0.02
    #     def fun( angle_m, gyro_m, dt = 0.01):
    #         nonlocal x1
    #         nonlocal x2
    #         nonlocal y1
    #         nonlocal angle
    #         nonlocal K2
    #         x1=(angle_m-angle)*(1-K2)*(1-K2)
    #         y1=y1+x1*dt
    #         x2=y1+2*(1-K2)*(angle_m-angle)+gyro_m
    #         angle=angle+ x2*dt
    #         return angle

    #     return fun

    # def get_euler_angle(self, dt = 0.01):
    #     data = self.get_all_data()
    #     accel_Y = math.atan2(data['accel'][0],data['accel'][2])*180/math.pi
    #     gyro_Y = data['gyro'][1]
    #     angleY = self.SecondOrderFilterY(-accel_Y,gyro_Y,dt)

    #     accel_X = math.atan2(data['accel'][1],data['accel'][2])*180/math.pi
    #     gyro_X = data['gyro'][0]
    #     angleX = self.SecondOrderFilterX(accel_X,gyro_X,dt)

    #     # return {'pitch':0, 'roll':0, 'yaw':0}
    #     return {'pitch':-math.radians(angleX), 'roll':-math.radians(angleY), 'yaw':0}



 


if __name__ == "__main__":
    import time
    # import matplotlib.pyplot as plt
    # # plt.ion() #开启interactive mode 成功的关键函数
    # plt.figure(1)
    # # plt.xlim([0.05, 0.15])
    # # plt.ylim([-0.16, -0.1])
    # plt.grid(linestyle='-', linewidth='0.5', color='gray')
    # pltX = [[],[],[],[]]
    # pltY = [[],[],[],[]]
    # x = 0

    mpu = MPU6050()
    timeLast = time.time()
    timeLast2 = time.time()
    while True:
        
        # timeLast = time.time()
        if time.time() - timeLast < 0.01:
            time.sleep(0.00001)
            continue
        timeLast = time.time()

        data = mpu.get_angle()
        # print('temperature',mpu.get_temp())
        # accel_data = mpu.get_accel_data()
        # print(accel_data)
        # print(accel_data['x'])
        # print(accel_data['y'])
        # print(accel_data['z'])
        # gyro_data = mpu.get_gyro_data()
        # print(gyro_data)
        # print(gyro_data['x'])
        # print(gyro_data['y'])
        # print(gyro_data['z'])
        # print('get_accel_data',time.time()-timeLast)

        # timeLast = time.time()

        # angle_Y = math.atan2(data['accel'][0],data['accel'][2])*180/math.pi
        # Gyro_Y = data['gyro'][1]

        # angleY = mpu.SecondOrderFilterX(angle_Y,-Gyro_Y)
        

        # if x > 3:
        # pltX[0].append(x)
        # pltY[0].append(angleY)
        # pltX[1].append(x)
        # pltY[1].append(angleYY)
        # x += 1

        # oula = IMUupdate(data['accel'][0],data['accel'][1],data['accel'][2],
        # data['gyro'][0], data['gyro'][1], data['gyro'][2])
        
        # print('oula=',oula)
        # print(time.time()-timeLast)
        if time.time() - timeLast2 >= 0.1:
            timeLast2 = time.time()
        #     # print('accel_data',accel_data)
            print(data)
            # plt.plot(pltX[0], pltY[0],'r--o',pltX[1], pltY[1],'g--v')
            # plt.pause(0.001)

            # print('oula=',oula)
        # time.sleep(0.0015)

        # print(time.time()-timeLast)
