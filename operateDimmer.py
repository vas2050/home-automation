#!/usr/local/bin/python3

import sys;
import time;
import asyncio;
import os;
import pickle;
import random;

sys.path.append('/usr/local/lib/python3.9/site-packages');

from kasa import Discover, SmartDimmer;

DEVICES_NOT = [];
DEVICE_CACHE = {};
DELAY = 0.2;
BLINK_DELAY = .2;
STEP = 10;

async def danceMyStyle(device, style = None):
   if style == 'asc':
      start, stop, step = 5, 100, STEP; 
      for num in range(start, stop, step):
         await device.set_brightness(num);
         await asyncio.sleep(DELAY);

   elif style == 'dsc':
      start, stop, step = 100, 5, -STEP; 
      for num in range(start, stop, step):
         await device.set_brightness(num);
         await asyncio.sleep(DELAY);

   elif style == 'blink':
      for num in range(0, 6):
         await device.set_brightness(100);
         await asyncio.sleep(BLINK_DELAY);
         await device.set_brightness(5);
         await asyncio.sleep(BLINK_DELAY);

   elif style == 'random':
      for num in range(0, 6):
         num = random.randrange(5, 100, 5);
         await device.set_brightness(num);
         await asyncio.sleep(DELAY);

   else:
      await danceMyStyle(device, 'dsc');
      await danceMyStyle(device, 'asc');

async def main(style = None):
   ip_addr = '<ip_addr_of_dimmer>';

   if ip_addr not in DEVICE_CACHE:
      device = SmartDimmer(ip_addr);
      await device.update();
      DEVICE_CACHE[ip_addr] = device;

   device = DEVICE_CACHE[ip_addr];

   alias = device.alias;
   if alias in DEVICES_NOT:
      return None;

   if style == 'off':
      await device.turn_off();
      exit(0);

   elif style == 'on':
      await device.turn_on();
      await device.set_brightness(100);
      exit(0);

   await device.turn_on();
   while True:
      await danceMyStyle(device, style);

if __name__ == '__main__':
   if len(sys.argv) == 2:
      style = sys.argv[1];
      asyncio.run(main(style));
   elif len(sys.argv) == 1:
      asyncio.run(main());
   else:
      print(f'\nUsage: {sys.argv[0]} [ asc | dsc | blink | random | on | off ]\n');
      exit(0);

