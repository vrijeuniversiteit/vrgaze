import matplotlib
from matplotlib import pyplot as plt, cycler

plt.rcParams.update(
	{
		'axes.prop_cycle': cycler(color=["0.00", "0.40", "0.60", "0.70"]),
		'axes.edgecolor': 'black',
		'axes.facecolor': 'white',
		'axes.labelcolor': 'black',
		'axes.grid': True,
		'axes.titlesize': 12,
		'axes.labelsize': 12,
		'figure.edgecolor': 'white',
		'figure.facecolor': 'white',
		'figure.autolayout': True,
		'figure.dpi': 100,
		'font.serif': 'Computer Modern',
		'grid.color': 'black',
		'grid.linestyle': '--',
		'image.cmap': 'gray',
		'lines.color': 'black',
		'lines.linewidth': 2.0,
		'mathtext.fontset': 'cm',
		'patch.edgecolor': 'black',
		'patch.facecolor': 'gray',
		'savefig.edgecolor': 'white',
		'savefig.facecolor': 'white',
		'text.color': 'black',
		'xtick.labelsize': 12,
		'ytick.labelsize': 12,
		'xtick.color': 'black',
		'ytick.color': 'black'
	}
)
