# -*- coding: utf-8 -*-
# Copyright (c) 2015-2016 Jeff Stevens
# SR700-Artisan-PDServer, released under GPLv3

import time
import sys
import freshroastsr700
import logging
import Pyro4


@Pyro4.expose
class Roaster(object):
    def __init__(self):
        """Creates a freshroastsr700 object passing in methods included in this
        class."""
        self.roaster = freshroastsr700.freshroastsr700(
            self.update_data, self.next_state, thermostat=True)

    def update_data(self):
        """This is a method that will be called every time a packet is opened
        from the roaster."""
        cur_state = self.roaster.get_roaster_state()
        print("Current Temperature:", self.roaster.current_temp, cur_state)

    def next_state(self):
        """This is a method that will be called when the time remaining ends.
        The current state can be: roasting, cooling, idle, sleeping, connecting,
        or unkown."""
        if(self.roaster.get_roaster_state() == 'roasting'):
            self.roaster.time_remaining = 20
            self.roaster.cool()
        elif(self.roaster.get_roaster_state() == 'cooling'):
            self.roaster.idle()

    def run_roast(self):
        if(self.roaster.get_roaster_state() == 'idle'):
            self.roaster.roast()

    def set_fan_speed(self, speed):
        new_speed = int(speed)
        self.roaster.fan_speed = new_speed

    def set_temperature(self, temperature):
        new_temperature = int(temperature)
        if new_temperature < 150:
            self.roaster.cool()
        else:
            self.roaster.target_temp = new_temperature

    def set_time(self, time):
        new_time = int(time)
        self.roaster.time_remaining = new_time

    def output_current_state(self):
        cur_state = self.roaster.get_roaster_state()
        cur_temp = str(self.roaster.current_temp)
        ret_state = cur_temp + cur_state
        return ret_state


# Create a roaster object.
r = Roaster()

# Set logging
#logging.basicConfig(filename="RoastControl_debug_log.log",level=logging.DEBUG)

# Conenct to the roaster.
r.roaster.auto_connect()

# Wait for the roaster to be connected.
while(r.roaster.connected is False):
    print("Please connect your roaster...")
    time.sleep(1)

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()
uri = daemon.register(r)

print("Ready. Object uri =", uri)      # print the uri so we can use it in the client later
ns.register("roaster.sr700", uri)
daemon.requestLoop()                   # start the event loop of the server to wait for calls
