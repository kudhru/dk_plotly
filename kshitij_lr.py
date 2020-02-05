from utils import utils

# x = [1,2,5,10,20,50,100,200,500,1000]
n_5 = [0.027004, 0.026967, 0.027286, 0.028454, 0.027769, 0.028079, 0.028064, 0.028167, 0.028202, 0.028317, 0.027675]
n_10 = [0.007913, 0.007936, 0.008106, 0.008205, 0.008220, 0.008291, 0.008309, 0.008315, 0.008250, 0.008293, 0.008160]
n_15 = [0.003784, 0.003776, 0.003825, 0.003861, 0.003882, 0.003897, 0.003895, 0.003890, 0.003903, 0.003900, 0.003869]

x = [0.1, 0.05, 0.01, 0.005, .001, .0005, 0.0001, 0.00005, 0.00001, 0.000005, 0.000001]

x_tickvals = [1, 0.1, 0.01, 0.001, 0.0001, 0.00001, 0.000001, 0.0000001]
x_ticktext = ['$10^{-0}$', '$10^{-1}$', '$10^{-2}$', '$10^{-3}$', '$10^{-4}$', '$10^{-5}$', '$10^{-6}$']
x_title = 'Learning Rate'

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
    x_title=x_title,
    y_title='Test Error',
    x_scale='log',
    x_tickvals=x_tickvals,
    x_ticktext=x_ticktext,
    # y_tickvals=[0, 0.01, 0.02, 0.03, 0.4],
    # y_ticktext=y_ticktexts,
    # x_range=x_range,
    # y_range=[0, 0.04],
    # legend_x=legend_x,
    # legend_xanchor=legend_xanchor,
    legend_y=0.8,
    # legend_orientation='h',
)