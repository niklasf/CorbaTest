import CORBA

import CorbaTest
import CorbaTest__POA

import sys
import os
import uuid
import time
import threading

class CarImpl(CorbaTest__POA.Car):
    def __init__(self):
        self.lock = threading.Lock()

        self.uuid = uuid.uuid4()

        self.wheels = False
        self.windows = False
        self.doors = False
        self.engine = False
        self.brakes = False
        self.lights = False
        self.steering_wheel = False
        self.color = False

    def has_wheels(self):
        return self.wheels

    def has_windows(self):
        return self.windows

    def has_doors(self):
        return self.doors

    def has_engine(self):
        return self.engine

    def has_brakes(self):
        return self.brakes

    def has_lights(self):
        return self.lights

    def has_steering_wheel(self):
        return self.steering_wheel

    def has_color(self):
        return self.color

    def add_wheels(self):
        if not self.lock.acquire(False):
            return False
        time.sleep(5)
        self.wheels = True
        self.lock.release()
        return True

    def add_windows(self):
        if not self.lock.acquire(False):
            return False
        time.sleep(5)
        self.windows = True
        self.lock.release()
        return True

    def add_doors(self):
        if not self.lock.acquire(False):
            return False
        time.sleep(5)
        self.doors = True
        self.lock.release()
        return True

    def add_engine(self):
        if not self.lock.acquire(False):
            return False
        time.sleep(10)
        self.engine = True
        self.lock.release()
        return True

    def add_brakes(self):
        if not self.lock.acquire(False):
            return False
        time.sleep(8)
        self.brakes = True
        self.lock.release()
        return True

    def add_lights(self):
        if not self.lock.acquire(False):
            return False
        time.sleep(3)
        self.lights = True
        self.lock.release()
        return True

    def add_steering_wheel(self):
        if not self.lock.acquire(False):
            return False
        time.sleep(5)
        self.steering_wheel = True
        self.lock.release()
        return True

    def add_color(self):
        if not self.lock.acquire(False):
             return False
        time.sleep(1)
        self.color = True
        self.lock.release()
        return True

    def get_uuid():
        return self.uuid

class CarFactoryImpl(CorbaTest__POA.CarFactory):
    def __init__(self):
        self.cars = []

    def add_car(self, index):
        car = CarImpl()
        self.cars.append(car)
        return car._this()

    def get_car(self, index):
        return self.cars[index]._this()

    def get_car_count(self):
        return len(self.cars)

if __name__ == "__main__":
    orb = CORBA.ORB_init(sys.argv)
    poa = orb.resolve_initial_references("RootPOA")

    servant = CarFactoryImpl()
    poa.activate_object(servant)

    print orb.object_to_string(servant._this())

    poa._get_the_POAManager().activate()
    orb.run()
