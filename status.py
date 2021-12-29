#!/usr/local/bin/python3

import sys;
import time;
import asyncio;
from kasa import Discover, SmartPlug, SmartDimmer;

MY_DEVICES = dict();

def getType(device):
   deviceType = 'Unknown';

   if device.is_bulb:
      deviceType = 'Bulb';
   elif device.is_dimmer:
      deviceType = 'Dimmer';
   elif device.is_strip:
      deviceType = 'Strip';
   elif device.is_light_strip:
      deviceType = 'Light Strip';
   elif device.is_plug:
      deviceType = 'Plug';

   return deviceType;

async def main():
   global MY_DEVICES;
   MY_DEVICES = await Discover.discover();
   tasks = [];
   for dev in MY_DEVICES:
      task = asyncio.create_task(check_plug(dev));
      tasks.append(task);

   await asyncio.gather(*tasks);

async def check_plug(ip_addr):
   deviceType = getType(MY_DEVICES[ip_addr]);

   if deviceType == 'Dimmer':
      device = SmartDimmer(ip_addr);
   elif deviceType == 'Plug':
      device = SmartPlug(ip_addr);
   else:
      return False;

   await device.update();

   #print(f'{time.strftime("%X")}');
   alias = list(device.alias.upper());
   alias = '='.join(alias);
   bottom = '=' * len(alias);

   print(f'''
   ============ { alias } ============

          Device Id : { device.device_id }
              Model : { device.model }
         IP Address : { ip_addr }
         LED Status : { 'On' if device.led else 'Off' }
        Device Type : { deviceType }
        Is Dimmable : { 'Yes' if device.is_dimmable else 'No' }
   Currently On/Off ? { 'On' if device.is_on else 'Off' }

   ============ { bottom } ============ ''');

   await asyncio.sleep(0);

if __name__ == '__main__':
   asyncio.run(main());
   #print(f'{time.strftime("%X")}');
