import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import copy

def strList2list(strList, start, end):
    new_str = strList[start:end]
    time_list = new_str.split(',')
    new_list = []
    for str_time in time_list:
        new_list.append(float(str_time))
    return new_list

def strMatrix2matrix(strMatrix):
    new_matrix = []
    for strList in strMatrix:
        new_matrix.append(strList2list(strList, 1, -2))
    return new_matrix

def heatmap(data, row_labels, col_labels, ax=None,
            cbar_kw=None, cbarlabel="", **kwargs):
    """
    Create a heatmap from a numpy array and two lists of labels.

    Parameters
    ----------
    data
        A 2D numpy array of shape (M, N).
    row_labels
        A list or array of length M with the labels for the rows.
    col_labels
        A list or array of length N with the labels for the columns.
    ax
        A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
        not provided, use current axes or create a new one.  Optional.
    cbar_kw
        A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
    cbarlabel
        The label for the colorbar.  Optional.
    **kwargs
        All other arguments are forwarded to `imshow`.
    """

    if ax is None:
        ax = plt.gca()

    if cbar_kw is None:
        cbar_kw = {}

    # Plot the heatmap
    im = ax.imshow(data, **kwargs)

    # Create colorbar
    cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
    cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom", fontsize="15")

    # Show all ticks and label them with the respective list entries.
    ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
    ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)

    # Let the horizontal axes labeling appear on top.
    ax.tick_params(top=True, bottom=False,
                   labeltop=True, labelbottom=False)

    # Rotate the tick labels and set their alignment.
    plt.setp(ax.get_xticklabels(), rotation=0, ha="right",
             rotation_mode="anchor")

    # Turn spines off and create white grid.
    ax.spines[:].set_visible(False)

    ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
    ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
    plt.xticks(fontsize="15")
    plt.yticks(fontsize="15")
    ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
    ax.tick_params(which="minor", bottom=False, left=False)

    return im, cbar


def annotate_heatmap(im, data=None, valfmt="{x:.2f}",
                     textcolors=("black", "white"),
                     threshold=None, **textkw):
    """
    A function to annotate a heatmap.

    Parameters
    ----------
    im
        The AxesImage to be labeled.
    data
        Data used to annotate.  If None, the image's data is used.  Optional.
    valfmt
        The format of the annotations inside the heatmap.  This should either
        use the string format method, e.g. "$ {x:.2f}", or be a
        `matplotlib.ticker.Formatter`.  Optional.
    textcolors
        A pair of colors.  The first is used for values below a threshold,
        the second for those above.  Optional.
    threshold
        Value in data units according to which the colors from textcolors are
        applied.  If None (the default) uses the middle of the colormap as
        separation.  Optional.
    **kwargs
        All other arguments are forwarded to each call to `text` used to create
        the text labels.
    """

    if not isinstance(data, (list, np.ndarray)):
        data = im.get_array()

    # Normalize the threshold to the images color range.
    if threshold is not None:
        threshold = im.norm(threshold)
    else:
        threshold = im.norm(data.max())/2.

    # Set default alignment to center, but allow it to be
    # overwritten by textkw.
    kw = dict(horizontalalignment="center",
              verticalalignment="center", fontsize="14")
    kw.update(textkw)

    # Get the formatter in case a string is supplied
    if isinstance(valfmt, str):
        valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

    # Loop over the data and create a `Text` for each "pixel".
    # Change the text's color depending on the data.
    texts = []
    for i in range(data.shape[0]):
        for j in range(data.shape[1]):
            kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
            text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
            texts.append(text)

    return texts

# 比较不同算法的计算时间差异
def exp1():
    f = open("exp1.time_depths.txt", "r")
    x = np.array(strList2list(f.readline(), 1, -2))
    y_mm = np.array(strList2list(f.readline(), 1, -2))
    y_ab = np.array(strList2list(f.readline(), 1, -2))
    # for i in range(len(y_mm)):
    #     y_mm[i] = np.log(y_mm[i])
    #     y_ab[i] = np.log(y_ab[i])
    l1 = plt.plot(x, y_mm, 'r-', label='Minimax')
    l2 = plt.plot(x, y_ab, 'b-', label='Alpha-Beta')

    plt.title("Comparison between different algorithms with different depths", fontsize="13")
    plt.xlabel('Depths', fontsize="15")
    plt.ylabel('Average Time/Step', fontsize="15")
    x_ticks = np.arange(1, len(x)+1, 1)
    plt.xticks(x_ticks)
    plt.xticks(fontsize="15")
    plt.yticks(fontsize="15")
    plt.legend(fontsize="15")
    plt.grid(axis='both')
    plt.show()
    print(x)
    print(y_mm)
    print(y_ab)

# 比较不同depth的性能差异
def exp2():
    depths = ["1", "2", "3", "4"]
    f = open("win_rate.txt", "r")
    data = f.readlines()
    win_rates = np.array(strMatrix2matrix(data))
    fig, ax = plt.subplots()

    im, cbar = heatmap(win_rates, depths, depths, ax=ax,
                       cmap="YlGn", cbarlabel="Winning Rate [%]")
    texts = annotate_heatmap(im, valfmt="{x:.1f} %")
    fig.tight_layout()
    plt.show()

# 比较不同evaluate函数的性能差异
def exp3():
    depths = ["1", "2", "3", "4", "5"]
    f = open("exp3.win_rate_eval_new.txt", "r")
    data = f.readlines()
    win_rates = np.array(strMatrix2matrix(data))
    fig, ax = plt.subplots()

    im, cbar = heatmap(win_rates, depths, depths, ax=ax,
                       cmap="YlGn", cbarlabel="Winning Rate [%]")
    texts = annotate_heatmap(im, valfmt="{x:.1f} %")
    fig.tight_layout()
    plt.show()

# exp1()
# exp2()
exp3()
