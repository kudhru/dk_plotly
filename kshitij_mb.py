from utils import utils

from utils.utils import plot_summary

x = [1,2,5,10,20,50,100,200,500,1000]
n_5 = [0.028071,0.028035,0.028284,0.028154,0.028274,0.028227,0.027940,0.027898,0.028323,0.026951]
n_10 = [0.008184,0.008223,0.008255,0.008195,0.008262,0.008282,0.008239,0.008244,0.008254,0.008276]
n_15 = [0.003864,0.003875,0.003879,0.003867,0.003884,0.003906,0.003901,0.003897,0.003919,0.003898]

trace_data = []

trace_data.append(utils.scatter_trace(
    x,
    n_5,
    'A',
    marker_size=9,
    symbol='circle',
))

trace_data.append(utils.scatter_trace(
    x,
    n_10,
    'B',
    marker_size=9,
    symbol='square',
))

trace_data.append(utils.scatter_trace(
    x,
    n_15,
    'A',
    symbol='triangle-up',
    marker_size=9,
))

utils.plot(
    trace_data,
    '',
    'Kshitij',
    x_title='Mini Batch Size',
    y_title='Test Error',
    x_scale='log',
    x_tickvals=[1, 10, 100, 1000],
    x_ticktext=['$10^0$', '$10^1$', '$10^2$', '$10^3$'],
    # y_tickvals=[0, 0.01, 0.02, 0.03, 0.4],
    # y_ticktext=y_ticktexts,
    # x_range=x_range,
    # y_range=[0, 0.04],
    # legend_x=legend_x,
    # legend_xanchor=legend_xanchor,
    legend_y=0.8,
    # legend_orientation='h',
)