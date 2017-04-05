from __future__ import print_function

import sys

sys.path.append('..')

from src.sim import Sim
from src.packet import Packet

from networks.network import Network

broadcastRate = 5 #seconds
broadcastTimeout = broadcastRate * 3

def broadcastPacket(sourceAddress, identification, delayToSend, handlerMethod):
    #actually send the data
    p = Packet(
        source_address=sourceAddress,
        destination_address=0,
        ident=identification, ttl=1, protocol='dvrouting', length=100)
    Sim.scheduler.add(delay=delayToSend, event=p, handler=handlerMethod)

class BroadcastApp(object):
    def __init__(self, node):
        self.node = node

    def receive_packet(self, packet):
        print(Sim.scheduler.current_time(), self.node.hostname, packet.ident)
        #todo
        #read the data
        #apply changes to stored dataobjects
    def storeData(self, data)
        
class Generator(object):
    def __init__(self, node, sourceAddress, rate):
        self.node = node
        self.sourceAddress = sourceAddress
        self.rate = rate
        self.ident = 0

    def handle(self, event):
        now = Sim.scheduler.current_time()
        # generate a packet
        self.ident += 1
        
        #todo
        #check for neighbors that have not respond
            #if not responded
                #remove path information about node that is gone

        broadcastPacket(self.sourceAddress, self.ident, now,  self.node.send_packet)
        # schedule the next time we should generate a packet
        Sim.scheduler.add(delay=(now + self.rate), event='generate', handler=self.handle)


def main():
    # parameters
    Sim.scheduler.reset()
    Sim.set_debug(True)

    # setup network
    net = Network('../networks/five-nodes-line.txt')

    # get nodes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n3 = net.get_node('n3')
    n4 = net.get_node('n4')
    n5 = net.get_node('n5')

    # setup broadcast application
    b1 = BroadcastApp(n1)
    n1.add_protocol(protocol="dvrouting", handler=b1)
    b2 = BroadcastApp(n2)
    n2.add_protocol(protocol="dvrouting", handler=b2)
    b3 = BroadcastApp(n3)
    n3.add_protocol(protocol="dvrouting", handler=b3)
    b4 = BroadcastApp(n4)
    n4.add_protocol(protocol="dvrouting", handler=b4)
    b5 = BroadcastApp(n5)
    n5.add_protocol(protocol="dvrouting", handler=b5)

    #send a broadcast every 30 seconds from all nodes
    g1 = Generator(node=n1, sourceAddress=n1.get_address('n2') ,rate=broadcastRate)
    Sim.scheduler.add(delay=0, event='generate', handler=g1.handle)
    g2 = Generator(node=n2, sourceAddress=n2.get_address('n1') ,rate=broadcastRate)
    Sim.scheduler.add(delay=0, event='generate', handler=g1.handle)
    g3 = Generator(node=n3, sourceAddress=n3.get_address('n2') ,rate=broadcastRate)
    Sim.scheduler.add(delay=0, event='generate', handler=g1.handle)
    g4 = Generator(node=n4, sourceAddress=n4.get_address('n3') ,rate=broadcastRate)
    Sim.scheduler.add(delay=0, event='generate', handler=g1.handle)
    g5 = Generator(node=n5, sourceAddress=n5.get_address('n4') ,rate=broadcastRate)
    Sim.scheduler.add(delay=0, event='generate', handler=g1.handle)

    # run the simulation
    Sim.scheduler.run()



if __name__ == '__main__':
    main()
