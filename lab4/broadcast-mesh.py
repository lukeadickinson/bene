from __future__ import print_function

import sys
from sets import Set
sys.path.append('..')

from src.sim import Sim
from src.packet import Packet

from networks.network import Network

broadcastRate = 5 #seconds
broadcastTimeout = broadcastRate * 3


def broadcastPacket(sourceAddress, identification, delayToSend, packetData, handlerMethod):
    #actually send the data
    p = Packet(
        source_address=sourceAddress,
        destination_address=0,
        ident=identification, ttl=1, protocol='dvrouting', body=packetData)
    Sim.scheduler.add(delay=0, event=p, handler=handlerMethod)

def getMyAddressesSet(node):
    myAddresses = Set()
    for link in node.links:
        myAddresses.add(link.address)
    return myAddresses

def generateOwnPath(node):
    hostname = node.hostname
    #myAddressesSet = getMyAddressesSet(node)
    setOfKnownAddresses = Set(node.datastore.keys())
    setOfKnownAddresses.add(hostname)

    for neighborsDataKey in node.datastore:
        neighborsData = node.datastore[neighborsDataKey]
        neighborPath = neighborsData["path"]
        setOfKnownAddresses = setOfKnownAddresses | Set(neighborPath.keys())

    myPath = {}
    myValues = {}
    for knownAddress in setOfKnownAddresses:
        if knownAddress == hostname:
            myPath[knownAddress] = knownAddress
            myValues[knownAddress] = 0
        else:
            bestValue = float("inf")
            bestFirstHop = None
            for neighborsDataKey in node.datastore:
                neighborsData = node.datastore[neighborsDataKey]
                neighborPath = neighborsData["path"]
                neighborValues = neighborsData["values"]
                if knownAddress in neighborPath:
                    if neighborPath[knownAddress] != hostname:
                        if bestValue > neighborValues[knownAddress] + 1:
                            bestValue = neighborValues[knownAddress] + 1
                            bestFirstHop = neighborPath[neighborsDataKey]

            myPath[knownAddress] = bestFirstHop
            myValues[knownAddress] = bestValue

    
    changeForwardingTables(hostname, node, myPath)
    myData = {"hostname": hostname, "path": myPath, "values": myValues}
    return myData

def changeForwardingTables(hostname, node, myPath):
    node.forwarding_table.clear()
    for destAddress in myPath:
        if destAddress != hostname:
            if myPath[destAddress] != None:
                #todo: fix, this doesnt work
                node.add_forwarding_entry(address=destAddress, link=node.get_link(myPath[destAddress]))

class BroadcastApp(object):
    def __init__(self, node):
        self.node = node
        self.node.datastore = {}
        self.node.datastoreTimestamp = {}

    def receive_packet(self, packet):
        print(Sim.scheduler.current_time(), self.node.hostname, packet.ident, self.node.forwarding_table)
        self.storeData(packet.body)
        
    def storeData(self, data):
        myHostname = data["hostname"]
        self.node.datastore[myHostname] = data
        now = Sim.scheduler.current_time()
        self.node.datastoreTimestamp[myHostname] = now
        print(self.node.datastore, "total datastore")
        generateOwnPath(self.node)

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
        
        removeTheseNodes = []
        for neighborAddress in self.node.datastore:
            if self.isNodeInactive(neighborAddress) :
                removeTheseNodes.append(neighborAddress)
        
        for removeMe in removeTheseNodes:
            self.removeNodeData(removeMe)

        myData = generateOwnPath(self.node)
        broadcastPacket(self.sourceAddress, self.ident, now, myData, self.node.send_packet)
        
        # schedule the next time we should generate a packet
        Sim.scheduler.add(delay=self.rate, event='generate', handler=self.handle)

    def isNodeInactive(self, myHostname):
        now = Sim.scheduler.current_time()
        timeLastUpdated = self.node.datastoreTimestamp[myHostname]
        if now - timeLastUpdated >= broadcastTimeout:
            return True
        
        return False
        
    def removeNodeData(self, myHostname):
        del self.node.datastore[myHostname]
        del self.node.datastoreTimestamp[myHostname]

def main():
    # parameters
    Sim.scheduler.reset()
    Sim.set_debug(True)

    # setup network
    net = Network('../networks/fifteen-nodes.txt')

    # get nodes
    n1 = net.get_node('n1')
    n2 = net.get_node('n2')
    n3 = net.get_node('n3')
    n4 = net.get_node('n4')
    n5 = net.get_node('n5')
    n6 = net.get_node('n6')
    n7 = net.get_node('n7')
    n8 = net.get_node('n8')
    n9 = net.get_node('n9')
    n10 = net.get_node('n10')
    n11 = net.get_node('n11')
    n12 = net.get_node('n12')
    n13 = net.get_node('n13')
    n14 = net.get_node('n14')
    n15 = net.get_node('n15')
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
    b6 = BroadcastApp(n6)
    n6.add_protocol(protocol="dvrouting", handler=b6)
    b7 = BroadcastApp(n7)
    n7.add_protocol(protocol="dvrouting", handler=b7)
    b8 = BroadcastApp(n8)
    n8.add_protocol(protocol="dvrouting", handler=b8)
    b9 = BroadcastApp(n9)
    n9.add_protocol(protocol="dvrouting", handler=b9)
    b10 = BroadcastApp(n10)
    n10.add_protocol(protocol="dvrouting", handler=b10)
    b11 = BroadcastApp(n11)
    n11.add_protocol(protocol="dvrouting", handler=b11)
    b12 = BroadcastApp(n12)
    n12.add_protocol(protocol="dvrouting", handler=b12)
    b13 = BroadcastApp(n13)
    n13.add_protocol(protocol="dvrouting", handler=b13)
    b14 = BroadcastApp(n14)
    n14.add_protocol(protocol="dvrouting", handler=b14)
    b15 = BroadcastApp(n15)
    n15.add_protocol(protocol="dvrouting", handler=b15)
    #send a broadcast every 30 seconds from all nodes
    g1 = Generator(node=n1, sourceAddress=n1.get_address('n2'), rate=broadcastRate)
    Sim.scheduler.add(delay=0, event='generate', handler=g1.handle)
    g2 = Generator(node=n2, sourceAddress=n2.get_address('n1'),rate=broadcastRate)
    Sim.scheduler.add(delay=0, event='generate', handler=g2.handle)
    g3 = Generator(node=n3 ,sourceAddress=n3.get_address('n2'),rate=broadcastRate)
    Sim.scheduler.add(delay=0, event='generate', handler=g3.handle)
    g4 = Generator(node=n4 ,sourceAddress=n4.get_address('n5'),rate=broadcastRate)
    Sim.scheduler.add(delay=0, event='generate', handler=g4.handle)
    g5 = Generator(node=n5 ,sourceAddress=n5.get_address('n3'),rate=broadcastRate)
    Sim.scheduler.add(delay=0, event='generate', handler=g5.handle)
    g6 = Generator(node=n6, sourceAddress=n6.get_address('n1'), rate=broadcastRate)
    Sim.scheduler.add(delay=0, event='generate', handler=g6.handle)
    g7 = Generator(node=n7, sourceAddress=n7.get_address('n6'),rate=broadcastRate)
    Sim.scheduler.add(delay=0, event='generate', handler=g7.handle)
    g8 = Generator(node=n8 ,sourceAddress=n8.get_address('n7'),rate=broadcastRate)
    Sim.scheduler.add(delay=0, event='generate', handler=g8.handle)
    g9 = Generator(node=n9 ,sourceAddress=n9.get_address('n7'),rate=broadcastRate)
    Sim.scheduler.add(delay=0, event='generate', handler=g9.handle)
    g10 = Generator(node=n10 ,sourceAddress=n10.get_address('n1'),rate=broadcastRate)
    Sim.scheduler.add(delay=0, event='generate', handler=g10.handle)
    g11 = Generator(node=n11, sourceAddress=n11.get_address('n4'), rate=broadcastRate)
    Sim.scheduler.add(delay=0, event='generate', handler=g11.handle)
    g12 = Generator(node=n12, sourceAddress=n12.get_address('n5'),rate=broadcastRate)
    Sim.scheduler.add(delay=0, event='generate', handler=g12.handle)
    g13 = Generator(node=n13 ,sourceAddress=n13.get_address('n5'),rate=broadcastRate)
    Sim.scheduler.add(delay=0, event='generate', handler=g13.handle)
    g14 = Generator(node=n14 ,sourceAddress=n14.get_address('n2'),rate=broadcastRate)
    Sim.scheduler.add(delay=0, event='generate', handler=g14.handle)
    g15 = Generator(node=n15 ,sourceAddress=n15.get_address('n14'),rate=broadcastRate)
    Sim.scheduler.add(delay=0, event='generate', handler=g15.handle)

    Sim.scheduler.add(delay=30, event=None, handler=n3.get_link('n2').down)
    Sim.scheduler.add(delay=30, event=None, handler=n2.get_link('n3').down)

    # bring the link up
    Sim.scheduler.add(delay=300, event=None, handler=n3.get_link('n2').up)
    Sim.scheduler.add(delay=300, event=None, handler=n2.get_link('n3').up)

    #print(n1.get_address('n2'), n2.get_address('n1'), n2.get_address('n3'), n3.get_address('n2'), n3.get_address('n4'),n4.get_address('n3'), n4.get_address('n5'), n5.get_address('n4'))
    # run the simulation
    Sim.scheduler.run()



if __name__ == '__main__':
    main()
