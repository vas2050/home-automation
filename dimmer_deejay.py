#!/usr/local/bin/python3

import asyncio;
import functools;
import os;
import random;
import signal;
import sys;
import time;

sys.path.append('/usr/local/lib/python3.9/site-packages');

from kasa import Discover, SmartDimmer;

DEVICES_NOT = [];
DEVICE_CACHE = {};
DELAY = 0.6;
RANDOM_DELAY = .4;
LO, HI, STEP = 40, 100, 5;

DANCE = {
   'once': [ 'high', 'h', 'low', 'l', 'stop', 's', 'cancel', 'ca', 'on', 'off' ],
   'multi': [ 'asc', 'a', 'dsc', 'd', 'blink', 'b', 'wink', 'w', 'random', 'r', 'cycle', 'c', 'mixed', 'm' ]
};

def dance_forever(func):
   functools.wraps(func);
   async def wrapped_dance_forever(*args, **kwargs):
      print(args);
      if kwargs.style in DANCE.once:
         return await func(*args, **kwargs);
      elif kwargs.style in DANCE.multi:
         while True:
            return await func(*args, **kwargs);
      else:
         print('unkown command');
         pass;

   return wrapped_dance_forever;

@dance_forever
async def dance_my_style(device, style = None):
   if style == 'asc' or style == 'a':
      for num in range(LO, HI + 1, STEP):
         await device.set_brightness(num);
         await asyncio.sleep(DELAY);

   elif style == 'dsc' or style == 'd':
      for num in range(HI, LO + 1, -STEP):
         await device.set_brightness(num);
         await asyncio.sleep(DELAY);

   elif style == 'blink' or style == 'b':
      for num in range(5):
         await device.set_brightness(HI);
         await asyncio.sleep(DELAY);
         await device.set_brightness(LO);
         await asyncio.sleep(DELAY);

   elif style == 'wink' or style == 'w':
      for num in range(1):
         await device.set_brightness(HI);
         await asyncio.sleep(DELAY);
         await device.set_brightness(LO);
         await asyncio.sleep(DELAY);

   elif style == 'random' or style == 'r':
      for num in range(6):
         num = random.randrange(LO, HI + 1, STEP);
         await device.set_brightness(num);
         await asyncio.sleep(RANDOM_DELAY);

   elif style == 'mixed' or style == 'm':
      for num in range(8):
         await danceMyStyle(device, 'dsc');
         await danceMyStyle(device, 'asc');
      else:
         await danceMyStyle(device, 'wink');

   elif style == 'cycle' or style == 'c':
      await danceMyStyle(device, 'dsc');
      await danceMyStyle(device, 'asc');

   elif style == 'high' or style == 'h':
      await device.set_brightness(HI);

   elif style == 'low' or style == 'l':
      await device.set_brightness(LO);

   elif style == 'cancel' or style == 'ca':
      await danceMyStyle(device, 'high');

   elif style == 'stop' or style == 's':
      pass;

   elif style == 'on':
      await device.turn_on();
      await device.set_brightness(100);

   elif style == 'off':
      await device.turn_off();

async def main():
   eLoop = asyncio.get_event_loop();

   ip_addr = '<x.x.x.x>';

   if ip_addr not in DEVICE_CACHE:
      device = SmartDimmer(ip_addr);
      await device.update();
      DEVICE_CACHE[ip_addr] = device;

   device = DEVICE_CACHE[ip_addr];

   alias = device.alias;
   if alias in DEVICES_NOT:
      return None;

   task = '';
   while True:
      cmd = input('>>> ').strip();

      if cmd == 'help':
         print('''  Commands:
   a[sc]
   b[link]
   ca[ncel]
   c[ycle]
   d[sc]
   h[igh]
   l[ow]
   m[ixed]
   r[andom]
   s[top]
   w[ink]
   on
   off
   exit ''');
         continue;

      if cmd == 'exit':
         signal.raise_signal(signal.SIGINT);

      if cmd:
         if task:
            task.cancel();

         task = eLoop.create_task(dance_my_style(device, style=cmd));

if __name__ == '__main__':
   eLoop = asyncio.new_event_loop();
   asyncio.set_event_loop(eLoop);

   try:
      eLoop.run_until_complete(main());
   except KeyboardInterrupt:
      sys.stdout.flush();
      print('\nGood Bye!');
      eLoop.stop();
      sys.exit();

