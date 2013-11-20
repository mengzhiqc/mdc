#!/usr/bin/python

# import zmq
# import msgpack

# context = zmq.Context()

# receiver = context.socket(zmq.PULL)
# receiver.connect("tcp://10.10.3.76:5434")

# # subscriber = context.socket(zmq.SUB)
# # subscriber.connect("tcp://10.10.3.76:5434")
# # subscriber.setsockopt(zmq.SUBSCRIBE, "10001")

# poller = zmq.Poller()
# poller.register(receiver, zmq.POLLIN)
# #poller.register(subscriber, zmq.POLLIN)

# while True:
# 	socks = dict(poller.poll())

# 	if receiver in socks and socks[receiver] == zmq.POLLIN:
# 		message = receiver.recv()
# 		print msgpack.unpackb(message)
from AccessLogParser import Parser
parser = Parser("10.10.3.76",5434)
parser.parse()