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
DELAY = 0.6;
RANDOM_DELAY = .4;
START, STOP, STEP = 40, 100, 5;

async def danceMyStyle(device, style = None):
   if style == 'asc':
      for num in range(START, STOP + 1, STEP):
         await device.set_brightness(num);
         await asyncio.sleep(DELAY);

   elif style == 'dsc':
      for num in range(STOP, START + 1, -STEP):
         await device.set_brightness(num);
         await asyncio.sleep(DELAY);

   elif style == 'blink':
      for num in range(5):
         await device.set_brightness(STOP);
         await asyncio.sleep(DELAY);
         await device.set_brightness(START);
         await asyncio.sleep(DELAY);

   elif style == 'wink':
      for num in range(1):
         await device.set_brightness(STOP);
         await asyncio.sleep(DELAY);
         await device.set_brightness(START);
         await asyncio.sleep(DELAY);

   elif style == 'random':
      for num in range(6):
         num = random.randrange(START, STOP + 1, STEP);
         await device.set_brightness(num);
         await asyncio.sleep(RANDOM_DELAY);

   elif style == 'mixed':
      for num in range(10):
         await danceMyStyle(device, 'dsc');
         await danceMyStyle(device, 'asc');
      else:
         await danceMyStyle(device, 'wink');

   else:
      await danceMyStyle(device, 'dsc');
      await danceMyStyle(device, 'asc');

async def main(style = None):
   ip_addr = '<x.x.x.x>';

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

   while True:
      await danceMyStyle(device, style);

if __name__ == '__main__':
   eLoop = asyncio.new_event_loop();
   asyncio.set_event_loop(eLoop);

   try:
      if len(sys.argv) == 2:
         style = sys.argv[1];
         eLoop.run_until_complete(main(style));
      elif len(sys.argv) == 1:
         eLoop.run_until_complete(main());
      else:
         print(f'\nUsage: {sys.argv[0]} [ asc | dsc | blink | wink | random | on | off ]\n');
         exit(0);

   except KeyboardInterrupt:
      sys.stdout.flush();
      eLoop.stop();
      sys.exit();

