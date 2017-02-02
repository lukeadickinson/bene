import optparse
import sys

import pandas as pd
import matplotlib.pyplot as plt
import plotly.plotly as py
import plotly.graph_objs as go
# Class that parses a file and plots several graphs
class Plotter:
    def __init__(self):
        plt.style.use('ggplot')
        pd.set_option('display.width', 1000)
        pass

    def linePlot(self):
        """ Create a line graph. """
        data = pd.read_csv("data1.csv")
		data.head()
		
		trace1 = go.Scatter(
                    x=df['Utilization'], y=df['Theory'], # Data
                    mode='lines', name='Theory' # Additional options
                   )
trace2 = go.Scatter(x=df['x'], y=df['sinx'], mode='lines', name='sinx' )
trace3 = go.Scatter(x=df['x'], y=df['cosx'], mode='lines', name='cosx')

layout = go.Layout(title='Simple Plot from csv data',
                   plot_bgcolor='rgb(230, 230,230)')

fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)

# Plot data in the notebook
py.iplot(fig, filename='simple-plot-from-csv')
		
		plt.plot(x, np.sin(x - 0), color='blue')
		plt.plot(x, np.sin(x - 0), color='blue')
        plt.figure()
        ax = data.plot(x='Utilization',y='Theory')
        bx = data.plot(x='Utilization',y='Average')
        ax.set_xlabel("Utilization")
        ax.set_ylabel("Queueing Delay")
        fig = ax.get_figure()
        fig.savefig('line.png')

if __name__ == '__main__':
    p = Plotter()
    p.linePlot()
