
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
from matplotlib.ticker import MaxNLocator

import itertools as itt

def setfigdefaults():
  mpl.rcParams['axes.linewidth'] = 1
  mpl.rcParams['font.size'] = 14
  #mpl.rcParams['font.family'] = 'sans-serif'
  mpl.rcParams['font.sans-serif'] = ['Arial']
  mpl.rcParams['svg.fonttype'] = 'none'
  mpl.rcParams['pdf.fonttype'] = 42
  mpl.rcParams['lines.linewidth'] = 1
  mpl.rcParams['patch.linewidth'] = 1
  mpl.rcParams['xtick.direction'] = 'out'
  mpl.rcParams['ytick.direction'] = 'out'
  mpl.rcParams['xtick.major.width'] = 1
  mpl.rcParams['ytick.major.width'] = 1

def dressfig(fig, clip=False, **kwargs):
  for ax in fig.get_axes():
    prettify(ax, **kwargs)
    if not clip:
      noclip(ax)
  #fig.tight_layout()

def prettify(ax, xbins=None, ybins=None):
  ch = ax.get_children()

  ax.spines['right'].set_color('none')
  ax.spines['top'].set_color('none')
  ax.xaxis.set_ticks_position('bottom')
  ax.yaxis.set_ticks_position('left')

  if xbins is not None:
    ax.xaxis.set_major_locator(MaxNLocator(xbins))
  if ybins is not None:
    ax.yaxis.set_major_locator(MaxNLocator(ybins))

  xlabel = ax.get_xlabel()
  ylabel = ax.get_ylabel()
  #xtkls  = map(lambda x: x.get_text(), ax.get_xticklabels())
  #ytkls  = map(lambda x: x.get_text(), ax.get_yticklabels())
  xtks   = ax.get_xticks()
  ytks   = ax.get_yticks()
  for spine in ax.spines.values():
    spine.set_position(('outward', 10))
    #spine.set_smart_bounds(True)
  ax.set_xticks(xtks)
  ax.set_yticks(ytks)
  ax.set_xlabel(xlabel)
  ax.set_ylabel(ylabel)
  #ax.set_xticklabels(xtkls)
  #ax.set_yticklabels(ytkls)


def noclip(ax):
  "Turn off all clipping in axes ax; call immediately before drawing"
  ax.set_clip_on(False)
  artists = []
  artists.extend(ax.collections)
  artists.extend(ax.patches)
  artists.extend(ax.lines)
  artists.extend(ax.texts)
  artists.extend(ax.artists)
  for a in artists:
    a.set_clip_on(False) 


def barerrbar(ax, x, y, yerr, width=0.2, color='r'):
  numbars = len(y)
  ax.bar(np.array(x) - width/2.0, y, width, yerr=yerr, color=color, ecolor='k')


def _plotarea(ax,   xa, above, xb, below, color):
  if isinstance(xa, np.ndarray):     xa    = xa.tolist()
  if isinstance(above, np.ndarray):  above = above.tolist()
  if isinstance(xb, np.ndarray):     xb    = xb.tolist()
  if isinstance(below, np.ndarray):  below = below.tolist()
  xs = xa + [x for x in reversed(xb)]
  ys = above + [x for x in reversed(below)]
  ax.fill_between(xs, ys, color=color)


def spreadplot(ax,   x, center, layers, \
    colors=mpl.rcParams['axes.color_cycle'] ):
  layers = np.atleast_2d(layers)
  center = np.array(center)
  for l, c in zip(layers, colors):
    _plotarea(ax, x, center + l, x, center - l, c)


def rasterplot(ax, spiketimes, **kwargs):
  """ Draw a raster plot from the spike-times.

  Parameters
  ==========

  ax : Axis object to draw to.
  spiketimes : list of lists, one list for each trial, containing spike times.
  """
  xdata = ((t, t) for t in itt.chain(*spiketimes))
  ydata = ((t, t+1) for t in itt.chain( \
      *[itt.repeat(i, len(spiketimes[i])) for i in range(len(spiketimes))] ))
  for (x, y) in itt.izip(xdata, ydata):
    ax.add_line(plt.Line2D(x,y, **kwargs))

def gaussapprox(\
    ax, vecs, \
    stds=1., color=['b','g','r','c','m','y'], alpha=.5):
  """ Display ellipses marking out the concentration of a gaussian distribution
  modeled on the input vectors.

  Parameters
  ==========

  vecs : collection of ndarrays; size=(Dists, Dims, Points)
    Collection of distributions to visualize.
  stds : float
    Number of standard deviations over which to shade.
  colors : list
    Order in which to color the different distributions.
  alpha : float
    Alpha with which to display the distributions.
  """
  ells = []
  for dist in vecs:
    """ Assume 2 dimensions for now """
    xy = np.mean(dist, 1)
    eigval, eigvec = np.linalg.eig(np.cov(dist))
    angle = np.arctan2(eigvec[1,0], eigvec[0,0])
    height = np.sqrt(eigval[1])*2.*stds # Go out in both directions
    width = np.sqrt(eigval[0])*2.*stds
    ells.append(\
        Ellipse(xy=xy, angle=np.degrees(angle), height=height, width=width))

  for ell, col in zip(ells, color):
    ax.add_artist(ell)
    ell.set_clip_box(ax.bbox)
    ell.set_alpha(alpha)
    ell.set_facecolor(col)
    ell.set_zorder(2.6)

  return ells


def sizelabelfonts(ax, size):
  for l in ax.xaxis.get_ticklabels():
    l.set_fontsize(size)
  for l in ax.yaxis.get_ticklabels():
    l.set_fontsize(size)
    
def sizefonts( ax, size ):
  sizelabelfonts(ax, size)
  ax.xaxis.label.set_fontsize(size)
  ax.yaxis.label.set_fontsize(size)
  ax.title.set_fontsize(size)

