



REDIS_HOST = "ec2-108-128-200-47.eu-west-1.compute.amazonaws.com"
REDIS_PORT = 28530
REDIS_PASS = "p398b8babb0102d6b97c810e43e88705ce876770add3656275a4eef35318bf002"


from urllib.parse import urlparse
REDIS_URL = "redis://:p398b8babb0102d6b97c810e43e88705ce876770add3656275a4eef35318bf002@ec2-108-128-200-47.eu-west-1.compute.amazonaws.com:28530"
# REDIS_URL = "rediss://:p398b8babb0102d6b97c810e43e88705ce876770add3656275a4eef35318bf002@ec2-108-128-200-47.eu-west-1.compute.amazonaws.com:28530"

x = urlparse(REDIS_URL)

import os
import redis

client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, username="", password=REDIS_PASS, ssl=True, ssl_cert_reqs=None)


"""

import redis
client = redis.Redis(host="localhost")#, port=6379, password="mypassword")
client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASS,
)#, port=6379, password="mypassword")
import json

value = {"Hello": ["A", "B", 1, 3]}
# r.set("test", json.dumps(value))
"""


for k in client.keys():
    print(k)

"""
value = client.get("flask_cache_report/6YGnLdrtyKMWwcmx")
print(value)
"""
