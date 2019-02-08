import matplotlib
from matplotlib.figure import Figure
from matplotlib.animation import TimedAnimation
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

import numpy as np

class CustomFigCanvas(FigureCanvas, TimedAnimation):

    def __init__(self):

        self.data1 = []
        self.data2 = []
        self.data3 = []
        self.data4 = []
        print(matplotlib.__version__)

        # The data
        self.xlim = 200
        self.n = np.linspace(0, self.xlim - 1, self.xlim)
        self.y1 = (self.n * 0.0)
        self.y2 = (self.n * 0.0)
        self.y3 = (self.n * 0.0)
        self.y4 = (self.n * 0.0)

        # The window
        self.fig = Figure(figsize=(5,5), dpi=100)
        self.ax1 = self.fig.add_subplot(111)

        # self.ax1 settings
        self.ax1.set_xlabel('time')
        self.ax1.set_ylabel('raw data')
        self.line1 = Line2D([], [], color='blue')
        self.line2 = Line2D([], [], color='green')
        self.line3 = Line2D([], [], color='red')
        self.line4 = Line2D([], [], color='black', linewidth=2)
        self.ax1.add_line(self.line1)
        self.ax1.add_line(self.line2)
        self.ax1.add_line(self.line3)
        self.ax1.add_line(self.line4)
        self.ax1.set_xlim(0, self.xlim - 1)
        self.ax1.set_ylim(-5, 5)
        self.ax1.legend(("Position","Velocity","Acceleration","Force"))

        FigureCanvas.__init__(self, self.fig)
        TimedAnimation.__init__(self, self.fig, interval = 50, blit = True)

    def new_frame_seq(self):
        return iter(range(self.n.size))

    def _init_draw(self):
        lines = [self.line1, self.line2, self.line3, self.line4]
        for l in lines:
            l.set_data([], [])

    def add_data(self, v1,v2,v3,v4):
        self.data1.append(v1)
        self.data2.append(v2)
        self.data3.append(v3)
        self.data4.append(v4)

    def _step(self, *args):
        # Extends the _step() method for the TimedAnimation class.
        try:
            TimedAnimation._step(self, *args)
        except Exception as e:
            self.abc += 1
            print(str(self.abc))
            TimedAnimation._stop(self)
            pass

    def _draw_frame(self, framedata):
        margin = 2
        
        while(len(self.data1) > 0 and len(self.data2) > 0 and len(self.data3) > 0 and len(self.data4) > 0):
            
            self.y1 = np.roll(self.y1, -1)
            self.y1[-1] = self.data1[0]

            self.y2 = np.roll(self.y2, -1)
            self.y2[-1] = self.data2[0]

            self.y3 = np.roll(self.y3, -1)
            self.y3[-1] = self.data3[0]
            
            self.y4 = np.roll(self.y4, -1)
            self.y4[-1] = self.data4[0]
            
            del(self.data1[0])
            del(self.data2[0])
            del(self.data3[0])
            del(self.data4[0])


        self.line1.set_data(self.n[ 0 : self.n.size - margin ], self.y1[ 0 : self.n.size - margin ])
        self.line2.set_data(self.n[ 0 : self.n.size - margin ], self.y2[ 0 : self.n.size - margin ])
        self.line3.set_data(self.n[ 0 : self.n.size - margin ], self.y3[ 0 : self.n.size - margin ])
        self.line4.set_data(self.n[ 0 : self.n.size - margin ], self.y4[ 0 : self.n.size - margin ])
        self._drawn_artists = [self.line1, self.line2, self.line3, self.line4]

