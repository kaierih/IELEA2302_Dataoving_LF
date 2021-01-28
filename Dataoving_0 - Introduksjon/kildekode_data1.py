from numpy import sin, cos, pi, exp
from scipy.signal import welch
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, fixed, FloatSlider, IntSlider, HBox, VBox, interactive_output, Layout
import ipywidgets as widget

# UI tool to inspect segments of a larger signal in time and frequency domain   
class signalAnalyzer:
    def __init__(self, x_n, f_s, fig_num=1):
        self.x_n = x_n
        self.f_s = f_s
        self.t = np.linspace(0, len(self.x_n)/self.f_s, len(self.x_n), endpoint=False)
        
        
        # Set up canvas
        plt.close(fig_num)
        self.fig = plt.figure(fig_num, figsize=(9, 6))
        
        
        # Set up plot showing signal selection
        self.ax1 = plt.subplot(4, 1, 1)
        self.ax1.set_title(r"Full Signal Plot")
        self.ax1.plot(self.t, self.x_n,  color='tab:blue')
        self.ax1.grid(True)
        self.ax1.set_xlabel('Time t (seconds)')
        self.highlight, = self.ax1.plot(self.t, self.x_n, color='tab:orange')
        self.ax1.axis(xmin=self.t[0], xmax=self.t[-1])
        
        
        
        # Set up signal segment inspection plot
        self.ax2 = plt.subplot(4, 1, (2,4))
        
        self.selectionCurve, = self.ax2.plot(self.t, self.x_n, color='tab:blue')
        self.ax2.grid(True)
        
        
        # Adjust figure layout
        self.fig.tight_layout(pad=0.1, w_pad=1.0, h_pad=2.0)
        
        # Set up UI panel
        domainSelection = widget.RadioButtons(
            options=['Time Trace', 'Frequency Spectrum'],
            value='Time Trace',
            description='Display: ',
            disabled=False,
            continuous_update=False
        )
        win_start = widget.BoundedIntText(    
            value=4000,
            min=0,
            max=len(self.x_n)-1,
            step=1,
            description='Signal segment start (sample number):',
            disabled=False,
            style = {'description_width': 'initial'},
            layout=Layout(width='95%'),
            continuous_update=False
        )
        win_stop = widget.BoundedIntText(    
            value=8000,
            min=4001,
            max=len(self.x_n),
            step=1,
            description='Signal segment stop (sample number):',
            disabled=False,
            style = {'description_width': 'initial'},
            layout=Layout(width='95%'),
            continuous_update=False
        )
        self.layout = HBox(
            [VBox([win_start, win_stop]), 
             domainSelection]
        )
        self.userInput = {
            'n_start': win_start,
            'n_stop': win_stop,
            'domain': domainSelection
        }
        out = interactive_output(self.update, self.userInput)
        display(self.layout, out)
        # Run demo
        #out = interactive_output(self.update, self.sliders)
        #display(self.layout, out)
        
    def update(self, n_start, n_stop, domain):
        self.userInput['n_stop'].min=n_start+1
        if n_stop <= n_start:
            n_stop = n_start+1
        self.highlight.set_ydata(self.x_n[n_start:n_stop])
        self.highlight.set_xdata(self.t[n_start:n_stop])
        if domain=='Time Trace':
            self.ax2.set_xlabel('Time t (seconds)')
            self.ax2.set_ylabel('Value x(t)')
            self.selectionCurve.set_ydata(self.x_n[n_start:n_stop])
            self.selectionCurve.set_xdata(self.t[n_start:n_stop])
            self.ax2.set_xlabel("Time t (seconds)")
            self.ax2.set_ylabel("Value x(t)")
            self.ax2.set_title("Time plot of selected signal segment")
            self.ax2.relim()
            self.ax2.autoscale_view()
            self.ax2.axis(xmin=self.t[n_start], xmax=self.t[n_stop])
            
        elif domain=='Frequency Spectrum':
            M = n_stop-n_start
            f, Sxx_sub = welch(self.x_n[n_start:n_stop], self.f_s, 'hamming', int(M/4), int(M/8), int(M/2))
            
            self.ax2.set_xlabel("Frequency f (Hz)")
            self.ax2.set_ylabel("Power Pxx(f) (dB)")
            self.ax2.set_title("Frequency content of selected signal segment")
            self.selectionCurve.set_ydata(10*np.log10(Sxx_sub))
            self.selectionCurve.set_xdata(f)
            self.ax2.relim()
            self.ax2.autoscale_view()
            self.ax2.axis(xmin=0, xmax=self.f_s/2)
            
        else:
            pass
        self.fig.tight_layout(pad=0.1, w_pad=1.0, h_pad=2.0)