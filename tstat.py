#!/usr/bin/python
# -*- coding:utf-8 -*-

import sys
import os
import fcntl
import time
import commands
import argparse
import logging
from logging.handlers import RotatingFileHandler

try:
    import simplejson as json
except:
    import json

from functools import wraps

# logging
rHandler = RotatingFileHandler("tstat.log", maxBytes = 100*1024*1024, backupCount = 5)
rHandler.setLevel(logging.INFO)
rHandler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger = logging.getLogger(__name__)
logger.addHandler(rHandler)

def Command(cmd, msg = ""):
    #print cmd
    s, o = commands.getstatusoutput(cmd)
    if s != 0:
        raise Exception("\nCmd: %s, \nMsg: %s, \nError:%s"%(cmd, msg, str(o)))
    return o

def GetCurTime(cur):
    return time.strftime("%Y-%m-%dT%H:%M:%S",time.localtime(cur))

class TCPState(object):
    def __init__(self, cur, input, recv_q, send_q):
        self.input = input
        self.cur = cur
        self.v = {
            "Time": cur,
            "Recv-Q": recv_q,
            "Send-Q": send_q,
            "TIME_WAIT":0,
            "ESTABLISHED":0,
            "CLOSE_WAIT":0,
            "SYN_RECV":0,
            "SYN_SENT":0,
            "FIN_WAIT1":0,
            "FIN_WAIT_1":0,
            "FIN_WAIT2":0,
            "FIN_WAIT_2":0,
            "CLOSING":0,
            "LAST_ACK":0,
            "CLOSED":0,
            "LISTEN":0,
        }

        self._do()

    def get_tuple(self, item):
        out = []
        for i in item:
            out.append(self.v[i])

        return tuple(out)


    def _do(self):
        item = self.input.split("\n")
        for i in item:
            i = i.strip().split(" ")
            self.v[i[0]] += int(i[1])

        self.v["FIN_WAIT1"] = self.v["FIN_WAIT1"] + self.v["FIN_WAIT_1"]
        self.v["FIN_WAIT2"] = self.v["FIN_WAIT2"] + self.v["FIN_WAIT_2"]
            
def tcp_proc():
    pass


def handle_netstat(args):
    cmd = "netstat -nat | awk '/^tcp/{++S[$NF]}END{for (a in S) print a,S[a]}'"
    cmd_recv_q = '''netstat -ant | grep -v Recv-Q | grep -v "servers and established" | awk '{print $2}' | awk '{sum+=$1}END{print sum}' '''
    cmd_send_q = '''netstat -ant | grep -v Recv-Q | grep -v "servers and established" | awk '{print $3}' | awk '{sum+=$1}END{print sum}' '''
    title = ["Time", "Recv-Q", "Send-Q", "ESTABLISHED", "TIME_WAIT", "CLOSE_WAIT", "SYN_RECV", "SYN_SENT", "FIN_WAIT1", "FIN_WAIT2", "CLOSING", "LAST_ACK", "CLOSED", "LISTEN",] 
    format = "%19s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s %10s"
    print format % (tuple(title))

    i = int(args.interval)
    if i <= 0:
        raise Exception("Invalid interval.")

    remain = int(time.time()) % i

    time.sleep(remain)

    while True:
        cur = int(time.time())
        remain = cur % i

        if remain > 0:
            time.sleep(0.5)
            continue

        cur = GetCurTime(cur)
        out = Command(cmd)
        recv_q = Command(cmd_recv_q)
        send_q = Command(cmd_send_q)
        x = TCPState(cur, out, recv_q, send_q)

        msg = format % (x.get_tuple(title))
        print msg
        logger.info(msg)
        time.sleep(i)
    
def gen_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', '--interval', dest='interval', default=5, help='print interval.')

    subs = parser.add_subparsers(title="Sub Commands")
    sub = subs.add_parser('netstat', help="netstat")
    sub.set_defaults(func=handle_netstat)

    return parser

def main():
    parser = gen_parser()
    result = parser.parse_args(sys.argv[1:])
    result.func(result)

if __name__ == '__main__':
    main()

