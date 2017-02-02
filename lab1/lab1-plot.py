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

    def linePlot(self):
		raw_data = {
		'Utilization': [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 98, 10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 98],
		'Queueing Delay': [0.0007,0.0007,0.0007,0.0007,0.0007,0.0007,0.0007,0.0007,0.0007,0.0007,0.0007,0.000246186799194, 0.000744426315041, 0.00180887562312, 0.00207776042834, 0.00370991960505, 0.00617988242069, 0.0083786921238, 0.0148861562441,0.0422212596784, 0.0289565539489, 0.0457814929168],
		'type': ['Theory','Theory','Theory','Theory','Theory','Theory','Theory','Theory','Theory','Theory','Theory','Average','Average','Average','Average','Average','Average','Average','Average','Average','Average','Average']
		}
		df = pd.DataFrame(raw_data, columns = ['Utilization', 'Queueing Delay', 'type'])
		fig, ax = plt.subplots()
		labels = []
		for key, grp in df.groupby(['type']):
			myColor = 'blue'
			if key == 'Theory' :
				myColor = 'green'
			ax = grp.plot(ax=ax, kind='line', x='Utilization', y='Queueing Delay', c=myColor)
			labels.append(key)
		lines, _ = ax.get_legend_handles_labels()
		ax.legend(lines, labels, loc='best')
		plt.show()

if __name__ == '__main__':
    p = Plotter()
    p.linePlot()
