# -*- coding: utf-8 -*-
"""
Created on Wed Apr 12 21:33:33 2023

@author: pizzacoin
"""

import datetime
#import os
import re
import subprocess

# %%

class TraceRoute:
    def __init__(self, host):
        self.host = host
        self.route_list = []
        self.run(host)
        
    def add_hop(self, route) -> bool:
        try:
            self.route_list.append(route)
            return True
        except:
            return False
        
    def run(self, host):
        output = subprocess.check_output(["tracert", host]).decode()
        for line in output.splitlines():
            if evaluate_tracert_line(line):
                self.add_hop(parse_tracert_line(line))
        
    def __repr__(self):
        return f"<Trace Route: {self.host if self.host else 'Empty'}>"


# %%

class Route:
    def __init__(self, matches=None):
        self.number = None
        self.tests = None
        self.route = None
        self.average = None
        self.datetime = None
        if matches:
            self.load_matches(matches) 
            
    def load_matches(self, matches):
        self.number = matches[1]
        self.tests = [matches[2], matches[3], matches[4]]
        self.route = matches[5]
        self.average = self._get_average()
        self.datetime = datetime.datetime.now()
        
    def _get_average(self):
        count = 0
        total = 0
        for test in self.tests:
            if test != "*":
                total += int(test.replace(" ms", ""))
                count += 1
        if count > 0:
            return int(total / count)
        return None
        
    def __repr__(self):
        return f"""<Route {self.number:0>2}: {
            (self.average if self.average else '*'): >2}{
                (' ms' if self.average else '   ')} {self.route}>"""
    
# %%

def evaluate_tracert_line(line):
    if line[:3].strip().isnumeric():
        return True
    return False

# %%

def parse_tracert_line(line):
    pattern = "(\d{1,3})[ ]*(\d{1,3} ms|[*])[ ]*(\d{1,3} ms|[*])[ ]*(\d{1,3}"\
        " ms|[*])[ ]*(.*$)"
    matches = re.match(pattern, line.strip())    
    return Route(matches)
    
# %%

if __name__ == "__main__":
    host = "google.com"
    trace_route = TraceRoute(host)
    print(trace_route)


# %%

#if line[:3].strip().isnumeric():
#    print(line)
#    matches = re.match(pattern, line.strip())
#    if matches:
#        print(str(Trace(matches).average) + " ms")
    
# %%

import unittest

class TraceTestCase(unittest.TestCase):
    
    def setUp(self):
        pass
    
    def tearDown(self):
        pass



# %%















