from src.buffer import SendBuffer, ReceiveBuffer
from src.connection import Connection
from src.sim import Sim
from src.tcppacket import TCPPacket
from sys import getsizeof

class TCP(Connection):
    """ A TCP connection between two hosts."""

    def __init__(self, transport, source_address, source_port,
                 destination_address, destination_port, app=None, window=1000,drop=[]):
        Connection.__init__(self, transport, source_address, source_port,
                            destination_address, destination_port, app)

        # -- Sender functionality

        # send window; represents the total number of bytes that may
        # be outstanding at one time
        self.window = window
        # send buffer
        self.send_buffer = SendBuffer()
        # maximum segment size, in bytes
        self.mss = 1000
        # largest sequence number that has been ACKed so far; represents
        # the next sequence number the client expects to receive
        self.sequence = 0
        # plot sequence numbers
        self.plot_sequence_header()
        # packets to drop
        self.drop = drop
        self.dropped = []
        # retransmission timer
        self.timer = None
        # timeout duration in seconds
        self.timeout = 1

        self.fastRetransmit = fastRetransmit
        self.lastAckReceived = None
        self.duplicateAckCount = 0

        self.totalQueueingDelay = 0
        self.packetsSent = 0
        # -- Receiver functionality

        # receive buffer
        self.receive_buffer = ReceiveBuffer()
        # ack number to send; represents the largest in-order sequence
        # number not yet received
        self.ack = 0

    def trace(self, message):
        """ Print debugging messages. """
        Sim.trace("TCP", message)

    def plot_sequence_header(self):
        if self.node.hostname =='n1':
            Sim.plot('sequence.csv','Time,Sequence Number,Event\n')

    def plot_sequence(self,sequence,event):
        if self.node.hostname =='n1':
            Sim.plot('sequence.csv','%s,%s,%s\n' % (Sim.scheduler.current_time(),sequence,event))

    def receive_packet(self, packet):
        """ Receive a packet from the network layer. """
        if packet.ack_number > 0:
            # handle ACK
            self.handle_ack(packet)
        if packet.length > 0:
            # handle data
            self.handle_data(packet)

    ''' Sender '''

    def send(self, data):
        self.send_buffer.put(data)
        if(self.send_buffer.available() > 0 and self.send_buffer.outstanding() < self.window):
            pulledData, sequence = self.send_buffer.get(self.mss)
            self.send_packet(pulledData, sequence)

    def send_packet(self, data, sequence):
        packet = TCPPacket(source_address=self.source_address,
                           source_port=self.source_port,
                           destination_address=self.destination_address,
                           destination_port=self.destination_port,
                           body=data,
                           sequence=sequence, ack_number=self.ack)

        if sequence in self.drop and not sequence in self.dropped:
            self.dropped.append(sequence)
            self.plot_sequence(sequence,'drop')
            self.trace("%s (%d) dropping TCP segment to %d for %d" % (
                self.node.hostname, self.source_address, self.destination_address, packet.sequence))
            return

        # send the packet        
        self.plot_sequence(sequence,'send')
        self.trace("%s (%d) sending TCP segment to %d for %d" % (
            self.node.hostname, self.source_address, self.destination_address, packet.sequence))
        self.transport.send_packet(packet)

        # set a timer
        if not self.timer:
            self.timer = Sim.scheduler.add(delay=self.timeout, event='retransmit', handler=self.retransmit)

    def handle_ack(self, packet):
        """ Handle an incoming ACK. """
        self.plot_sequence(packet.ack_number - 1000,'ack')
        self.trace("%s (%d) received ACK from %d for %d" % (
            self.node.hostname, packet.destination_address, packet.source_address, packet.ack_number))
        
        if self.fastRetransmit:
            if self.lastAckReceived != packet.ack_number:
               self.lastAckReceived = packet.ack_number
               self.duplicateAckCount = 0
            else :
                self.duplicateAckCount += 1
                if self.duplicateAckCount == 3:
                    #do fastRetransmit
                    print("fast retransmit for:")
                    print("packet.ack_number")
                    pulledData, sequence = self.send_buffer.resend(self.mss)
                    self.send_packet(pulledData, sequence)
    
        self.totalQueueingDelay += packet.queueing_delay
        self.packetsSent += 1.0
        if self.sequence < packet.ack_number :
            self.sequence = packet.ack_number
            self.send_buffer.slide(self.sequence)
            while(self.send_buffer.available() > 0 and self.send_buffer.outstanding() < self.window):
                self.cancel_timer()
                pulledData, sequence = self.send_buffer.get(self.mss)
                self.send_packet(pulledData, sequence) 
        if(self.send_buffer.outstanding() == 0):
            self.cancel_timer()
        

    def retransmit(self, event):
        """ Retransmit data. """
        pulledData, sequence = self.send_buffer.resend(self.mss)
        self.send_packet(pulledData, sequence)
        self.timer = Sim.scheduler.add(delay=self.timeout, event='retransmit', handler=self.retransmit)
        self.trace("%s (%d) retransmission timer fired" % (self.node.hostname, self.source_address))

    def cancel_timer(self):
        """ Cancel the timer. """
        if not self.timer:
            return
        Sim.scheduler.cancel(self.timer)
        self.timer = None

    ''' Receiver '''

    def handle_data(self, packet):
        """ Handle incoming data. This code currently gives all data to
            the application, regardless of whether it is in order, and sends
            an ACK."""
        self.trace("%s (%d) received TCP segment from %d for %d" % (
            self.node.hostname, packet.destination_address, packet.source_address, packet.sequence))
 
        self.totalQueueingDelay += packet.queueing_delay
        self.packetsSent += 1.0
        #print("true Queueing Delay------------------------------")
        #print(self.totalQueueingDelay/self.packetsSent)
        self.receive_buffer.put(packet.body,packet.sequence)
        data, start = self.receive_buffer.get()
        self.ack = start + len(data)
        self.app.receive_data(data)
        self.send_ack()

    def send_ack(self):
        """ Send an ack. """
        packet = TCPPacket(source_address=self.source_address,
                           source_port=self.source_port,
                           destination_address=self.destination_address,
                           destination_port=self.destination_port,
                           sequence=self.sequence, ack_number=self.ack)
        # send the packet
        self.trace("%s (%d) sending TCP ACK to %d for %d" % (
            self.node.hostname, self.source_address, self.destination_address, packet.ack_number))
        self.transport.send_packet(packet)
