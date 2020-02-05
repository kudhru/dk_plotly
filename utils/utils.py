import datetime
import os
import plotly.plotly as py
import plotly.graph_objs as go
import plotly.offline as offline
import numpy as np
from scipy import stats
import math
from PIL import Image

def plotly_signin():
    py.sign_in('kudhru', '9h58aP1ztlebPjPlccwb') # Replace the username, and API key with your credentials.


def scatter_trace(x, y, name, symbol='circle', marker_size=18, color=None, showlegend=True, mode='lines+markers', dash='solid'):
    return go.Scatter(
        x=x,
        y=y,
        name=name,
        mode=mode,
        marker=dict(
            color=color,
            symbol=symbol,
            size=marker_size,
            line=dict(
                color=color,
                width=2,
            )
        ),
        line=dict(
            dash=dash,
        ),
        showlegend=showlegend,
        # showlegend=False,
    )


def histogram_trace(x, name, nbinsx=None):
    return go.Histogram(
        x=x,
        histnorm='probability',
        name=name,
        nbinsx=nbinsx
    )


def cumulative_histogram_trace(x, name):
    return go.Histogram(x=x, histnorm='probability', cumulative=dict(enabled=True), name=name)


def scatter_plot(x, y, title, filename):
    trace = scatter_trace(x, y, title)
    data = [trace]
    plot(data, title, filename)


def plot(trace_data, title, filename, x_title=None, y_title=None, x_scale='-', y_scale='-', x_dtick=None, y_dtick=None, x_tickvals=None, x_ticktext=None, y_tickvals=None, y_ticktext=None, x_range=None, y_range=None, legend_x=1.0, legend_xanchor='right', legend_y=1.0, legend_orientation='v'):
    layout = go.Layout(
        title=title,
        width=800,
        height=640,
        xaxis=plotly_construct_axis_dict(x_range, x_scale, x_ticktext, x_tickvals, x_title),
        yaxis=plotly_construct_axis_dict(y_range, y_scale, y_ticktext, y_tickvals, y_title),
        legend=plotly_construct_legend_dict(legend_x, legend_xanchor, legend_y, legend_orientation)
    )
    fig = go.Figure(data=trace_data, layout=layout)
    offline.plot(fig, filename=filename, image='png', image_filename=filename.split('/')[-1])
    plotly_signin()
    plot_url = py.plot(fig, filename='latex')


def plotly_construct_legend_dict(legend_x=1.0, legend_xanchor='right', legend_y=1.0, orientation='v', font_size=24):
    return dict(
        orientation=orientation,
        xanchor=legend_xanchor,
        x=legend_x,
        y=legend_y,
        bordercolor='#000000',
        borderwidth=2,
        font=dict(
            family='Helvetica, monospace',
            size=font_size,
            color='#000000'
        ),
    )


def plotly_construct_axis_dict(range=None, scale='-', ticktext=None, tickvals=None, title=None):
    return dict(
        title=title,
        type=scale,
        automargin=True,
        showline=True,
        zeroline=False,
        titlefont=dict(
            family='Helvetica, monospace',
            size=30,
            color='#000000'
        ),
        exponentformat='power',
        tickangle=0,
        tickvals=tickvals,
        ticktext=ticktext,
        range=range,
        mirror=True,
        tickfont=dict(
            family='Helvetica, monospace',
            size=24,
            color='#000000'
        ),
    )


def format_float(value):
    return '%.8f' % value


def convert_png_to_eps(image_filename, suffix='.png'):
    img = Image.open(image_filename)
    # new_img = img.resize((256, 256))
    new_file_name = '{0}.eps'.format(os.path.join(os.path.dirname(image_filename), 'eps_format', image_filename.split('/')[-1].split(suffix)[0]))
    if img.mode not in ("L", "RGB", "CMYK"):
        img = img.convert("RGB")
    if not os.path.exists(new_file_name):
        img.save(new_file_name)


def generate_tickvals(x, scale):
    if scale == 'log':
        x = np.sort(x)
        index = 0
        while x[index] == 0:
            index += 1
        min = x[index]
        max = np.max(x)

        max_log = np.int(np.ceil(np.log10(max)))
        min_log = np.int(np.floor(np.log10(min)))

        major_tickvals = np.array(range(min_log, max_log+1))
        major_ticktexts = ['1e{0}'.format(tick) for tick in major_tickvals]

        final_tickvals = []
        final_ticktexts = []

        for i in range(7, 10):
            minor_tickval = i * np.float_power(10, major_tickvals[0] - 1)
            minor_ticktext = ''
            final_tickvals.append(minor_tickval)
            final_ticktexts.append(minor_ticktext)

        for index in range(len(major_tickvals) - 1):
            major_tickval = major_tickvals[index]
            major_ticktext = major_ticktexts[index]
            final_tickvals.append(np.float_power(10, major_tickval))
            final_ticktexts.append(major_ticktext)
            for i in range(1, 10):
                minor_tickval = i * np.float_power(10, major_tickval)
                minor_ticktext = ''
                final_tickvals.append(minor_tickval)
                final_ticktexts.append(minor_ticktext)
        final_tickvals.append(np.float_power(10, major_tickvals[index+1]))
        final_ticktexts.append(major_ticktexts[index+1])
        return final_tickvals, final_ticktexts, [major_tickvals[0], major_tickvals[-1]]
    else:
        min = np.min(x)
        max = np.max(x)
        min = min - (max-min) / 10
        max = max + (max - min) / 10
        return None, None, [min, max]
        # min = -0.05
        # max = 1.05
        # return [-0.05, 0, 0.2, 0.4, 0.6, 0.8, 1, 1.05], ['', '0', '0.2', '0.4', '0.6', '0.8', '1', ''], [min, max]


def plot_summary(filename, dfs, labels, marker_symbols, title='', x_col='traffic', y_col='delay', x_title='Traffic', y_title='Delay', x_scale='-', y_scale='-', x_dtick=None, y_dtick=None, legend_x=1.0, legend_xanchor='right', legend_y=1.0, legend_orientation='v'):
    trace_data = list()
    x_lists = np.empty(0)
    y_lists = np.empty(0)
    for label, df, marker_symbol in zip(labels, dfs, marker_symbols):
        trace_data.append(scatter_trace(
            df[x_col],
            df[y_col],
            label,
            symbol=marker_symbol
        ))
        x_lists = np.append(x_lists, np.array(df[x_col]))
        y_lists = np.append(y_lists, np.array(df[y_col]))

    x_tickvals, x_ticktexts, x_range = generate_tickvals(x_lists, x_scale)
    y_tickvals, y_ticktexts, y_range = generate_tickvals(y_lists, y_scale)

    plot(
        trace_data,
        title,
        filename,
        x_title=x_title,
        y_title=y_title,
        x_scale=x_scale,
        y_scale=y_scale,
        x_dtick=x_dtick,
        y_dtick=y_dtick,
        x_tickvals=x_tickvals,
        x_ticktext=x_ticktexts,
        y_tickvals=y_tickvals,
        y_ticktext=y_ticktexts,
        x_range=x_range,
        y_range=y_range,
        legend_x=legend_x,
        legend_xanchor=legend_xanchor,
        legend_y=legend_y,
        legend_orientation=legend_orientation,
    )


def construct_plot_compatible_data(triplets, dfs, prefixes, x_col, y_col):
    result_labels = []
    result_dfs = []
    result_marker_symbols = []
    marker_symbols = get_marker_symbol_list()
    index = 0
    for prefix, df in zip(prefixes, dfs):
        for triplet in triplets:
            result_labels.append(triplet[0])
            # result_labels.append('{0} {1}'.format(prefix, triplet[0]))
            result_dfs.append(df[[triplet[1], triplet[2]]].rename(columns={triplet[1]: x_col, triplet[2]: y_col}))
            result_marker_symbols.append(marker_symbols[index])
            index = (index + 1) % len(marker_symbols)

    return result_labels, result_dfs, result_marker_symbols


def convert_png_files_in_dir_to_eps(path):
    onlyfiles = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    for file in onlyfiles:
        if file.endswith('.png'):
            convert_png_to_eps(os.path.join(path, file))


def get_marker_symbol_list():
    return [
        'circle',
        'square',
        'triangle-up',
        'star',
        'diamond',
        'circle-cross',
        'star-triangle-up',
        'triangle-down',
        'triangle-left',
        'triangle-right',
    ]