import json
import os
import asyncio
import numpy as np

import threading

import boto3

ddb = boto3.client('dynamodb')

f = open('puuids.json')
puuids = np.array(json.load(f)['data'])
x = np.array_split(puuids, 100)

table_name = 'LeagueMLStack-Puuids82D0B762-17KCZA7BLHG1M'

# class AtomicInteger():
#     def __init__(self, value=0):
#         self._value = int(value)
#         self._lock = threading.Lock()
        
#     def inc(self, d=1):
#         with self._lock:
#             self._value += int(d)
#             return self._value

#     def dec(self, d=1):
#         return self.inc(-d)    

#     @property
#     def value(self):
#         with self._lock:
#             return self._value

#     @value.setter
#     def value(self, v):
#         with self._lock:
#             self._value = int(v)
#             return self._value

# count = AtomicInteger()

# def update(p, count):
#     for item in p:
#         n = count.inc()
#         if n % 100 == 0:
#             print(n)
#         k = "puuid/" + item
#         ddb.put_item(TableName = table_name, Item={'key':{'S':k}})

# threads = []
# for i in range(100):   
#     t = threading.Thread(target = update, args = (x[i], count))
#     t.start()
#     threads.append(t)

# for i in range(100):
#     threads[i].join()


