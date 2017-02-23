from __future__ import print_function

import sys

sys.path.append('..')

from src.sim import Sim
from src.packet import Packet

from networks.network import Network

import random

	
myLoadPercent = 98
class Generator(object):
    def __init__(self, node, destination, load, duration):
        self.node = node
        self.load = load
        self.destination = destination
        self.duration = duration
        self.start = 0
        self.ident = 1

    def handle(self, event):
        # quit if done
        now = Sim.scheduler.current_time()
        if (now - self.start) > self.duration:
            return

        # generate a packet
        self.ident += 1
        p = Packet(destination_address=self.destination, ident=self.ident, protocol='delay', length=1000)
        Sim.scheduler.add(delay=0, event=p, handler=self.node.send_packet)
        # schedule the next time we should generate a packet
        Sim.scheduler.add(delay=random.expovariate(self.load), event='generate', handler=self.handle)


class DelayHandler(object):
    @staticmethod
    def receive_packet(packet):
        f1=open('./experiment'+ str(myLoadPercent)+'.txt', 'a+')
        f1.write(str(packet.queueing_delay) +"\n")

def main():
    # parameters
    Sim.scheduler.reset()

    # setup network
    net = Network('Lab1-queueingdelay.txt')

    # setup routes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n1.add_forwarding_entry(address=n2.get_address('n1'), link=n1.links[0])
    n2.add_forwarding_entry(address=n1.get_address('n2'), link=n2.links[0])

    # setup app
    d = DelayHandler()
    net.nodes['n2'].add_protocol(protocol="delay", handler=d)


    f1=open('./experiment'+ str(myLoadPercent)+'.txt', 'w+')
    f1.write("")
	
    # setup packet generator
    destination = n2.get_address('n1')
    max_rate = 1000000 // (1000 * 8)
		
    load = myLoadPercent/100.0 * max_rate
    g = Generator(node=n1, destination=destination, load=load, duration=10)
    Sim.scheduler.add(delay=0, event='generate', handler=g.handle)

    # run the simulation
    Sim.scheduler.run()

if __name__ == '__main__':
    main()