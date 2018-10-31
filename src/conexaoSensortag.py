# -*- coding: utf-8 -*-

import bluepy
import threading
import time
import re
import argparse
import sys

# this name is the BTLE characteristic which gives the device type
BTNAME = 'Complete Local Name'

# I have never had this many sensortags, there may be a lower limit in the bluetooth stack/hardware
MAX_DEVICES = 16

# the interval in seconds for sending of services request
READING_INTERVAL = 1.0

SENSORTYPES = [
    'accelerometer', 'barometer'  # ,'battery'
    , 'gyroscope', 'humidity', 'IRtemperature'  # ,'keypress'
    , 'lightmeter', 'magnetometer'  # ,'customService'
]

DEBUG = True

# from http://stackoverflow.com/questions/354038/how-do-i-check-if-a-string-is-a-number-float-in-python


def is_float(text):
    try:
        float(text)
        # check for nan/infinity etc.
        if str(text).isalpha():
            return False
        return True
    except ValueError:
        return False
    except TypeError:
        return False


class _paireddevice():
    def __init__(self, dev, devdata):
        if DEBUG:
            print "devdata=", devdata
        self.devdata = devdata
        self.name = self.devdata[BTNAME]
        self.friendlyname = devicenames[dev.addr]
        self.addr = dev.addr
        self.addrType = dev.addrType
        self.rssi = dev.rssi
        self.report("status", "found")
        if DEBUG:
            print "created _paireddevice"

    def unpair(self):
        if DEBUG:
            print "unpairing", self
        self.running = False
        for thread in self.threads:
            thread.join()
        pass

    def _sensorlookup(self, sensorname):
        if not hasattr(self.tag, sensorname):
            if DEBUG:
                print "not found", sensorname
            return None
        return getattr(self.tag, sensorname)

    # do whatever it takes to kick off threads to read the sensors in f,m,s
    # at read rates FAST, MEDIUM, SLOW
    def start(self):
        """
        f,m,s are list of sensor names to run at FAST, MEDIUM and SLOW read rates
        """
        if DEBUG:
            print "starting", f, m, s
        self.running = True
        self.threads = []
        for sensors in sensorList:
            if sensors:
                self.threads.append(threading.Thread(
                    target=self.runner, args=(sensors, READING_INTERVAL)))
#                print "setting daemon"
                self.threads[-1].daemon = True
                self.threads[-1].start()

    def runinit(self, sensors):
        if DEBUG:
            print "initializing for run", sensors
        return False

    def runread(self, sensors):
        if DEBUG:
            print('Doing something important in the background', self, sensors)
        return False

    def runner(self, sensors, interval):
        """ Method that runs forever """
        if not self.runinit(sensors):
            return
        while self.running:
            # Do something
            if not self.runread(sensors):
                break
#            print "pausing for",self.interval
            time.sleep(interval)
        if DEBUG:
            print "Aborting"

    def report(self, tag, value=None):
        #        print "report",self.addr, self.friendlyname, tag, value
        if is_float(value):
            print '{"deviceuid":"'+self.addr+'","devicename":"'+self.friendlyname+'","'+tag+'":'+str(value)+'}'
        else:
            if not isinstance(value, basestring):
                # a lit of numbers
                #                print "["+",".join([str(x) for x in value])+"]"
                print '{"deviceuid":"'+self.addr+'","devicename":"'+self.friendlyname+'","'+tag+'":'+"["+",".join([str(x) for x in value])+"]"+'}'
            else:
                # a simple string
                print '{"deviceuid":"'+self.addr+'","devicename":"'+self.friendlyname+'","'+tag+'":"'+str(value)+'"}'
        sys.stdout.flush()

# this is a generic sensortag


class _SensorTag(_paireddevice):
    def __init__(self, dev, devdata):
        if DEBUG:
            print "creating _SensorTag"
        self.tag = bluepy.sensortag.SensorTag(dev.addr)
        _paireddevice.__init__(self, dev, devdata)
        self.devicetype = "SensorTag generic"
        if DEBUG:
            print "created _SensorTag"
        return True

    def runinit(self, sensors):
        if DEBUG:
            print "_Sensortag runinit", sensors
        self.report("status", "enabled "+repr(sensors))
        for sensor in sensors:
            if DEBUG:
                print "enabling", sensor
            tagfn = self._sensorlookup(sensor)
            if tagfn:
                tagfn.enable()
#        time.sleep( 1.0 )
        return True

    def runread(self, sensors):
        try:
            for sensor in sensors:
                tagfn = self._sensorlookup(sensor)
                if tagfn:
                    self.report(sensor, tagfn.read())
        except bluepy.btle.BTLEException:
            self.report("status", "lost")
            return False
        return True

# this is a CC2650 sensortag


class _ST2650(_SensorTag):
    def __init__(self, dev, devdata):
        if DEBUG:
            print "creating _ST2650"
        _SensorTag.__init__(self, dev, devdata)
        self.devicetype = "Sensortag CC2650"
        self.report("status", "started")
        if DEBUG:
            print "created _ST2650"

# this is a CC1350 sensortag


class _ST1350(_SensorTag):
    def __init__(self, dev, devdata):
        if DEBUG:
            print "creating _ST1350"
        _SensorTag.__init__(self, dev, devdata)
        self.devicetype = "Sensortag CC1350"
        self.report("status", "started")
        if DEBUG:
            print "created _ST1350"

# this is a CC2540


class _ST(_SensorTag):
    def __init__(self, dev, devdata):
        if DEBUG:
            print "creating _ST"
        _SensorTag.__init__(self, dev, devdata)
        self.devicetype = "Sensortag CC2540"
        self.report("status", "started")
        if DEBUG:
            print "created _ST"
# depending on the bluetooth device type, this
# creates an instance of the appropriate class


def paireddevicefactory(dev):
    # get the device name to decide which type of device to create
    devdata = {}
    for (adtype, desc, value) in dev.getScanData():
        devdata[desc] = value
    if BTNAME not in devdata.keys():
        devdata[BTNAME] = 'Unknown!'
    if DEBUG:
        print "Found", devdata[BTNAME]
    if devdata[BTNAME] == 'SensorTag':
        return _ST(dev, devdata)
    elif devdata[BTNAME] == 'CC2650 SensorTag':
        return _ST2650(dev, devdata)
    elif devdata[BTNAME] == 'CC1350 SensorTag':
        return _ST1350(dev, devdata)
    return None

# this scandelegate handles discovery of new devices


class ScanDelegate(bluepy.btle.DefaultDelegate):
    def __init__(self):
        bluepy.btle.DefaultDelegate.__init__(self)
        self.activedevlist = []
#        self.gw = gateway

    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            if DEBUG:
                print "found", dev.addr
            if len(self.activedevlist) < MAXDEVICES:
                thisdev = paireddevicefactory(dev)
                if DEBUG:
                    print "thisdev=", thisdev
                if thisdev:
                    self.activedevlist.append(thisdev)
                    thisdev.start()
                if DEBUG:
                    print "activedevlist=", self.activedevlist
            else:
                if DEBUG:
                    print "TOO MANY DEVICES - IGNORED", dev.addr
            # launch a thread which pairs with this device and reads temperatures
        elif isNewData:
            if DEBUG:
                print "Received new data from", dev.addr
            pass

    def shutdown(self):
        if DEBUG:
            print "My activedevlist=", self.activedevlist
        # unpair the paired devices
        for dev in self.activedevlist:
            if DEBUG:
                print "dev=", dev
            dev.unpair()


sensorList = ['accelerometer', 'lightmeter']

scandelegate = ScanDelegate()
scanner = bluepy.btle.Scanner().withDelegate(scandelegate)

# while keepScanning:
# scan for a while - until ^C is pressed
try:
    while True:
        try:
            devices = scanner.scan(timeout=30.0)
        except bluepy.btle.BTLEException:
            if DEBUG:
                print "Aargh BTLE execption. Not panicing. Carrying on."
except KeyboardInterrupt:
    pass

if DEBUG:
    print "finishing"

scandelegate.shutdown()

if DEBUG:
    print "finished"
