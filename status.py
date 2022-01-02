#!/usr/local/bin/python3

import sys;
import time;
import asyncio;
from kasa import Discover, SmartPlug;

async def main():
   my_devices = await Discover.discover();
   tasks = [];
   for ip_addr in my_devices:
      task = asyncio.create_task(check_plug(ip_addr));
      tasks.append(task);

   await asyncio.gather(*tasks);

async def check_plug(ip_addr = None):
   plug = SmartPlug(ip_addr);
   await plug.update();

   #print(f'{time.strftime("%X")}');
   alias = list(plug.alias.upper());
   alias = '='.join(alias);
   bottom = '=' * len(alias);

   print(f'''
   ============ { alias } ============

          Device Id : { plug.device_id }
              Model : { plug.model }
         IP Address : { ip_addr }
         LED Status : { 'On' if plug.led else 'Off' }
        Is Dimmable : { 'Yes' if plug.is_dimmable else 'No' }
        Device Type : { 'Plug' if plug.is_plug else 'Non-Plug' }
   Currently On/Off ? { 'On' if plug.is_on else 'Off' }

   ============ { bottom } ============ ''');

   await asyncio.sleep(0);

if __name__ == '__main__':
   asyncio.run(main());
   #print(f'{time.strftime("%X")}');
