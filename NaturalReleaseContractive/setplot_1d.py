
"""
Set up the plot figures, axes, and items to be done for each frame.

This module is imported by the plotting routines and then the
function setplot is called to set the plot parameters.

"""
import setrun
import numpy as np
import matplotlib as mp
import matplotlib.pyplot as pplt
import clawtools.digplot as digplot
from pyclaw.plotters import geoplot
import clawtools.gaugedata as cg
import pytools.scalebars as scalebars
import pylab
import pdb

setrundata = setrun.setrun()

#pdb.set_trace()
(allgaugedata,xgauges,ygauges,gauge_nums) = cg.getgaugedata('_output/fort.gauge','_output/setgauges.data')
theta = 31.0*np.pi/180.
m0 = 0.5
g = 9.81
gp=g*np.cos(theta)

axisfontsize = 20
timefontsize = 22
instrumentmarkersize = 18

#--------------------------
def setplot(plotdata):
#--------------------------

    """
    Specify what is to be plotted at each frame.
    Input:  plotdata, an instance of pyclaw.plotters.data.ClawPlotData.
    Output: a modified version of plotdata.

    """
    import setrun

    setrundata = setrun.setrun()

    plotdata.clearfigures()  # clear any old figures,axes,items data


    def q_1d_fill(current_data):
        X = current_data.x
        Y = current_data.y
        a2dvar = current_data.var
        a2dvar2 = current_data.var2
        dy = current_data.dy

        #yind = np.where(np.abs(Y[0,:]-1.0)<=dy/2.0)[0]
        #xind = np.where(X[:,0]> -1.e10)[0]

        if (current_data.grid.level==3):
            yind = np.where(np.abs(Y[0,:]-1.0)<=dy)[0]
            xind = np.where(X[:,0]> -1.e10)[0]
        else:
            yind = np.where(Y[0,:]>1.e10)[0]
            xind = np.where(X[:,0]>1.e10)[0]

        x = X[np.ix_(xind,yind)]
        a1dvar = a2dvar[np.ix_(xind,yind)]#-x*np.sin(31.*np.pi/180.0)
        a1dvar2 = a2dvar2[np.ix_(xind,yind)]#-x*np.sin(31.*np.pi/180.0)
        #pdb.set_trace() #<-----------------------------

        return x,a1dvar,a1dvar2

    def q_1d(current_data):
        X = current_data.x
        Y = current_data.y
        dy = current_data.dy
        a2dvar = current_data.var

        if (current_data.grid.level==3):
            yind = np.where(np.abs(Y[0,:]-1.0)<=dy)[0]
            xind = np.where(X[:,0]> -1.e10)[0]
        else:
            yind = np.where(Y[0,:]>1.e10)[0]
            xind = np.where(X[:,0]>1.e10)[0]

        x = X[np.ix_(xind,yind)]
        a1dvar = a2dvar[np.ix_(xind,yind)]#-x*np.sin(31.*np.pi/180.0)

        return x,a1dvar

    def fixup(current_data):
        import pylab

        t=current_data.t
        pylab.title('')
        pylab.xticks([-5.9,-3,0,2.9],('-6.0','-3.0','0.0','3.0'),fontsize=axisfontsize)
        pylab.yticks([0,1.0,1.9],('0.0','1.0','2.0'),fontsize=axisfontsize)
        pylab.text(-5.5,1.9,'t = %6.2f s'% (t-4.0),fontsize=timefontsize, style = 'italic', \
            horizontalalignment='left',verticalalignment='top', \
            rotation = 31.0)
        #pdb.set_trace()
        #axx = pylab.gca()
        #scalebars.add_scalebar(axx)
        xbase = np.linspace(-6.0,0.0,5000)
        ybase = 0.0*xbase
        ybase[-1] = 0.65
        pylab.plot(xbase,ybase,'k-')
        #in front of ramp
        xbase = np.linspace(0.0,3.0,5000)
        ybase = 0.0*xbase
        pylab.plot(xbase,ybase,'k-')
        pylab.gcf().subplots_adjust(bottom=0.15)
        #pylab.tight_layout()
        return current_data

    def plot_lagrangian(current_data):

        #lagrangian dots

        if current_data.grid.level < 3:
            return current_data

        t=current_data.t
        #(allgaugedata,xgauges,ygauges,gauge_nums) = cg.getgaugedata('../_output/fort.gauge','../_output/setgauges.data')
        #pdb.set_trace()
        x0Lagrangian=[0.0975 -2.9,-2.3 + 0.65*np.tan(theta),-1.3+0.0512]
        xColor = ['c*','rp','m*']
        vplacement=[1.0,0.15,1.0,0.15]
        T = np.linspace(0.0,t,500)
        X = current_data.x
        Y = current_data.y
        dy = current_data.dy
        dx = current_data.dx
        h2d = current_data.q[:,:,0]
        topo2d = digplot.topo(current_data)

        for x0ind in xrange(len(x0Lagrangian)):
            x0 = x0Lagrangian[x0ind]

            Xoft = cg.Lagrangian_Xoft(allgaugedata,xgauges,gauge_nums,x0,T)
            xnow = Xoft[-1]

            if ((current_data.xupper+0.5*dx> xnow)&(current_data.xlower-0.5*dx<=xnow)):
                yind = np.where(np.abs(Y[0,:]-1.0)<=dy)[0]
                xind = np.where(X[:,0]> xnow)[0]
            else:
                yind = np.where(Y[0,:]>1.e10)[0]
                xind = np.where(X[:,0]>1.e10)[0]

            x = X[np.ix_(xind,yind)]
            #pdb.set_trace()
            if (xind.any()&yind.any()):
                h1d = h2d[np.ix_(xind,yind)]#-x*np.sin(31.*np.pi/180.0)
                topo1d = topo2d[np.ix_(xind,yind)]
                h1d = h1d.flatten()
                topo1d = topo1d.flatten()
                zcoord = topo1d[0] + vplacement[x0ind]*h1d[0]
                if x0ind==1:
                    zcoord = topo1d[0] + 0.1
                #pdb.set_trace()
                pylab.plot(xnow,zcoord,xColor[x0ind],markersize=instrumentmarkersize)

        return current_data



    # Figure for surface elevation
    plotfigure = plotdata.new_plotfigure(name='Surface', figno=1)
    plotfigure.kwargs = {'figsize':(9,2.2),'frameon':False}
    plotfigure.tight_layout = True
#    plotfigure.clf_each_frame = False

    # Set up for axes in this figure:
    plotaxes = plotfigure.new_plotaxes()
    plotaxes.xlimits = [-6.0,3.0]
    plotaxes.ylimits = [-0.2,2.0]#'auto' #[-.1,2.0]
    plotaxes.kwargs = {'frameon':'False','axis':'off'}
    plotaxes.afteraxes = fixup



    # Set up for item on these axes: (plot tan depth)
    plotitem = plotaxes.new_plotitem(plot_type='1d_fill_between_from_2d_data')
    plotitem.plot_var = digplot.topo
    plotitem.plot_var2 = digplot.eta
    plotitem.map_2d_to_1d = q_1d_fill
    #plotitem.amr_gridlines_show = [1,1,1]


    plotitem.color = 'tan'

    # Set up for item on these axes: (plot blue fill for pressure)
    plotitem = plotaxes.new_plotitem(plot_type='1d_fill_between_from_2d_data')
    plotitem.plot_var = digplot.topo
    plotitem.plot_var2 = digplot.pressure_lithohead_eta
    plotitem.map_2d_to_1d = q_1d_fill
    #plotitem.amr_gridlines_show = [1,1,1]
    plotitem.color = 'blue'

    # Set up for item on these axes: (dark line for topography)
    plotitem = plotaxes.new_plotitem(plot_type='1d_from_2d_data')
    plotitem.plot_var = digplot.topo
    plotitem.map_2d_to_1d = q_1d
    plotitem.linestyle = '-'
    plotitem.color = 'black'
    plotitem.linewidth = 2.0
    plotitem.show = True

    # Set up for lagrangian points
    plotitem = plotaxes.new_plotitem(plot_type = '2d_empty')
    plotitem.aftergrid = plot_lagrangian

    plotitem.show = True


    # figure of surface
    plotfigure = plotdata.new_plotfigure(name='Surface_2', figno=2)
    plotaxes = plotfigure.new_plotaxes()
    plotitem = plotaxes.new_plotitem(plot_type='2d_pcolor')
    plotaxes.xlimits = [-6.0,20.0]
    plotaxes.ylimits = [-2.0,4.0]
    plotitem.plot_var = 0#digplot.pressure_head
    plotitem.pcolor_cmin = 0.0
    plotitem.pcolor_cmax = 1.2
    plotitem.amr_gridlines_show = [1,1,0]
    #plotitem.amr_gridedges_show = [1 1 1]

    plotitem.show = False


    # Parameters used only when creating html and/or latex hardcopy
    # e.g., via pyclaw.plotters.frametools.printframes:

    plotdata.printfigs = True                # print figures
    plotdata.print_format = 'png'            # file format
    plotdata.print_framenos = 'all'    # list of frames to print
    plotdata.print_fignos = 'all'            # list of figures to print
    plotdata.html = True                     # create html files of plots?
    plotdata.html_homelink = '../README.html'
    plotdata.latex = True                    # create latex file of plots?
    plotdata.latex_figsperline = 2           # layout of plots
    plotdata.latex_framesperline = 1         # layout of plots
    plotdata.latex_makepdf = False           # also run pdflatex?
    plotdata.print_gaugenos = []

    return plotdata


