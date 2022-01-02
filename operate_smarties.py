#!/usr/local/bin/python3

import sys;
import time;
import asyncio;
import os;
import pickle;

sys.path.append('/usr/local/lib/python3.9/site-packages');

from kasa import Discover, SmartPlug;

CACHE_PATH = '/tmp/automation';
CACHE_FILE = CACHE_PATH + '/smart_plug_devices';

#DEVICES_NOT = [ 'Pluggy' ];
#DEVICES_NOT = [ 'Smuggy' ];
DEVICES_NOT = [];

DEVICE_CACHE = [];
PLUG_CACHE = {};

async def load_into_cache():
   global DEVICE_CACHE;
   if not os.path.exists(CACHE_PATH):
      os.mkdir(CACHE_PATH);

   with open(CACHE_FILE, 'w+') as f:
      devices = await Discover.discover();
      for ip_addr in devices:
         DEVICE_CACHE.append(ip_addr);
         f.write(f'{ip_addr}\n');

   return None;

async def load_from_cache():
   global DEVICE_CACHE;
   with open(CACHE_FILE, 'r') as f:
      DEVICE_CACHE = f.read().splitlines();
 
   return None;

async def main(cmd):
   if not DEVICE_CACHE:
      if os.path.exists(CACHE_FILE):
         await load_from_cache()
      else:
         await load_into_cache();

   #sys.exit();
   cmd = cmd.upper();

   if cmd not in ['ON', 'OFF']:
      print('Error: Unknown command!');
      return False;

   tasks = [];
   for ip_addr in DEVICE_CACHE:
      # create concurrent tasks
      task = asyncio.create_task(operate(ip_addr, cmd));
      tasks.append(task);

   # run all the tasks concurrently now
   for task in tasks:
      await task;

async def operate(ip_addr, cmd):
   #print(f'{time.strftime("%X")}');

   if ip_addr not in PLUG_CACHE:
      plug = SmartPlug(ip_addr);
      await plug.update();
      PLUG_CACHE[ip_addr] = plug;

   plug = PLUG_CACHE[ip_addr];

   alias = plug.alias;
   if alias in DEVICES_NOT:
      #print(f'skipping {alias} ...');
      return None;

   sys_cmd = None;

   if cmd == 'ON':
      sys_cmd = plug.turn_on;
   elif cmd == 'OFF':
      sys_cmd = plug.turn_off;

   #print(f'{alias} going { cmd } ...', end='');
   await sys_cmd();
   #print('done');
   #await asyncio.sleep(5);

if __name__ == '__main__':
   command = None;
   if len(sys.argv) == 2:
      cmd = sys.argv[1];
      asyncio.run(main(cmd));
   else:
      print(f'\nUsage: {sys.argv[0]} <on|off>\n');

   exit(0);
