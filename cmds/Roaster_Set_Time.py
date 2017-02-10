#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# TerminalRoastDB, released under GPLv3
# Roaster Set Time
import Pyro4
import sys

new_roaster_time = sys.argv[1]

roast_control = Pyro4.Proxy("PYRONAME:roaster.sr700")
if int(new_roaster_time) > 0 and int(new_roaster_time) <1200:
    roast_control.set_time(new_roaster_time)
