import optparse
import sys

import pandas as pd
import matplotlib.pyplot as plt

# Class that parses a file and plots several graphs
class Plotter:
    def __init__(self):
        plt.style.use('ggplot')
        pd.set_option('display.width', 1000)
        pass

    def linePlotThroughput(self):
        """ Create a line graph. """
        data = pd.read_csv("data1.csv")
        plt.figure()
        ax = data.plot(x='Window Size',y='Throughput')
        ax.set_xlabel("Window Size (bytes)")
        ax.set_ylabel("Throughput (bps)")
        fig = ax.get_figure()
        fig.savefig('line.png',bbox_inches='tight')

    def linePlotQueueingDelay(self):
        """ Create a line graph. """
        data = pd.read_csv("data2.csv")
        plt.figure()
        ax = data.plot(x='Window Size',y='Queueing Delay')
        ax.set_xlabel("Window Size (bytes)")
        ax.set_ylabel("Average Queueing Delay")
        fig = ax.get_figure()
        fig.savefig('line2.png',bbox_inches='tight')

if __name__ == '__main__':
    p = Plotter()
    p.linePlotThroughput()
    p.linePlotQueueingDelay()