#!/usr/local/bin/python3

import os;
import sys;
import time;
import asyncio;
import argparse;

'''
  Usage: operate.py <delay> default SLEEP_TIME
'''

DEFAULT_SLEEP_TIME = 0.4;

parser = argparse.ArgumentParser(description='A Python tool to make lights dance!\n');
parser.add_argument('-d', '--delay', help='delay in seconds, default: 0.4s', type=float, default=DEFAULT_SLEEP_TIME);
parser.add_argument('-n', '--number', help='number of times to dance, default: unlimited', type=int, default=None);

args = parser.parse_args();

if __name__ == '__main__':

   import operate;

   eLoop = asyncio.new_event_loop();
   asyncio.set_event_loop(eLoop);

   delay = args.delay;

   cmds = [ 'off', 'on' ];
   eLoop = asyncio.get_event_loop();

   count = 0;
   while True:
      for cmd in cmds:
         eLoop.run_until_complete(operate.main(cmd));
         #print(cmd);
         time.sleep(delay);

      if args.number:
         count += 1;
         if count == args.number:
            break;

