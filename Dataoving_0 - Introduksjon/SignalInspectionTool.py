from numpy import sin, cos, pi, exp
import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, fixed, FloatSlider, IntSlider, HBox, VBox, interactive_output, Layout

def sliderPanelSetup(set_details, n_of_sets=1, slider_type='float'):
    panel_col = []
    sliders = {}
    for i in range(n_of_sets):
        panel_row = []
        for item in set_details:
            mathtext = item['description']
            mathtext = mathtext.strip('$')
            if n_of_sets > 1:
                if mathtext.find(" ") == -1:
                    mathtext = '$' + mathtext + '_' + str(i+1) + '$' 
                else:
                    mathtext = '$' + mathtext.replace(" ", '_'+str(i+1)+'\ ', 1) + '$'
            else:
                mathtext = '$' + mathtext + '$'
            #mathtext = r'{}'.format(mathtext)

            panel_row.append(FloatSlider(value=item['value'], 
                                         min=item['min'],
                                         max = item['max'], 
                                         step = item['step'], 
                                         description=mathtext, 
                                         layout=Layout(width='95%')))
            
            sliders[item['keyword']+str(i+1)] = panel_row[-1]
        panel_col.append(HBox(panel_row, layout = Layout(width='100%')))
    layout = VBox(panel_col, layout = Layout(width='90%'))
    return sliders, layout

class y_of_x_plot:
    def __init__(self, ax, t, A_max, N=1, t_unit='s'):
        res  = len(t)
        self.N = N
        t_nd = np.outer(t, np.ones(self.N))
        x_t = np.zeros((res, self.N))          

        self.ax = ax
        self.lines = self.ax.plot(t_nd, x_t)
        
        # avgrensning av akser, rutenett, merkede punkt på aksene, tittel, aksenavn
        self.ax.axis([t[0], t[-1], -A_max, A_max])
        self.ax.grid(True)
        self.ax.set_xticks(np.linspace(t[0],t[-1],11))
        self.ax.set_xlabel("Tid (" + t_unit + ")")
        
    def update(self, new_lines_x, new_lines_y):
        assert self.N == len(new_lines_x) == len(new_lines_y), "Error: Parameter lenght different from number of sines."
        for i in range(self.N):
            self.lines[i].set_ydata(new_lines_y[i])
            self.lines[i].set_xdata(new_lines_x[i])
            
    def setLabels(self, names):
        self.ax.legend(self.lines, names, loc='upper right')
        
    def setStyles(self, styles):
        for i in range(min(len(styles), len(self.lines))):
            try:
                self.lines[i].set_color(styles[i]['color'])
            except:
                pass
            
            try:
                self.lines[i].set_linestyle(styles[i]['linestyle'])
            except:
                pass
# Demo 4:
# Sum av sinusbølger med vektoraddisjon        
class demo4:
    def __init__(self, x_n, f_s, fig_num=1):
        self.x_n = x_n
        self.f_s = f_s
        self.t = np.arange(0, len(self.x_n))/self.f_s
        
        
        # Set up canvas
        plt.close(fig_num)
        self.fig = plt.figure(fig_num, figsize=(8, 8))
        
        
        # Set up subplot with sine waves
        ax1 = plt.subplot(5, 1, 1)
        ax1.set_title(r"Full Signal Plot")
        ax1.plot(self.x_n, self.t)
        
        self.SineWaves = timeSeriesPlot(ax1, self.t, A_max = 2,  N = 3)
        
        self.SineWaves.setStyles([{'color': 'tab:green', 'linestyle': '-.'},
                                  {'color': 'tab:orange', 'linestyle': '-.'},
                                  {'color': 'tab:blue'}])
        
        self.SineWaves.setLabels([r'$x_1(t) = A_1\cdot \cos(2\pi t + \phi_1)$',
                                  r'$x_2(t) = A_2\cdot \cos(2\pi t + \phi_2)$', 
                                  r'$y(t)=x_1(t)+x_2(t)$'])

        
        # Set up vector subplot
        ax2 = plt.subplot(1, 5, (4,5))
        ax2.set_title("Kompleks amplitude $a_k = A_ke^{j\phi_k}$")
        
        self.VectorSumPlot = vectorPlot(ax2, A_max = 2, N = 3)
        
        self.VectorSumPlot.setStyles([{'color': 'tab:green', 'linestyle': '-.'},
                                      {'color': 'tab:orange', 'linestyle': '-.'},
                                      {'color': 'tab:blue'}])
        
        # Adjust figure layout
        self.fig.tight_layout(pad=0.1, w_pad=1.0, h_pad=1.0)

        # Set up slider panel
        self.sliders, self.layout = sliderPanelSetup(
            [{'keyword': 'A', 'value': 1, 'min': 0, 'max': 1, 'step': 0.1, 'description': r'A'},
             {'keyword': 'phi', 'value': 0.5, 'min': -1, 'max': 1, 'step': 1/12, 'description': r'\phi (\times \pi)'}],
            n_of_sets = 2)
        
        # Run demo
        out = interactive_output(self.update, self.sliders)
        display(self.layout, out)
        
    def update(self, **kwargs):
        x1 = kwargs['A1']*cos(2*pi*self.t + kwargs['phi1']*pi)
        x2 = kwargs['A2']*cos(2*pi*self.t + kwargs['phi2']*pi)
        y = x1 + x2
        
        self.SineWaves.update([x1, x2, y])
        
        v1_x = np.array([0, kwargs['A1']*cos(kwargs['phi1']*pi)])
        v1_y = np.array([0, kwargs['A1']*sin(kwargs['phi1']*pi)])
        
        v2_x = np.array([0, kwargs['A2']*cos(kwargs['phi2']*pi)])+v1_x[-1]
        v2_y = np.array([0, kwargs['A2']*sin(kwargs['phi2']*pi)])+v1_y[-1]
        
        v3_x = np.array([0, v2_x[-1]])
        v3_y = np.array([0, v2_y[-1]])
        
        self.VectorSumPlot.update([v1_x, v2_x, v3_x], [v1_y, v2_y, v3_y])
              