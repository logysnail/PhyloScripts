import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.colors as mcolors
import matplotlib.cm as cm


def show_cmap(cmap, norm=None, extend=None):
    """展示一个colormap."""
    if norm is None:
        norm = mcolors.Normalize(vmin=0, vmax=cmap.N)
    im = cm.ScalarMappable(norm=norm, cmap=cmap)

    fig, ax = plt.subplots(figsize=(6, 1))
    fig.subplots_adjust(bottom=0.5)
    fig.colorbar(im, cax=ax, orientation='horizontal', extend=extend)
    plt.show()


def two_factor_legend_continue(ax, range1, range2, cmap1, cmap2):
    # Extracting colors from a continuous colormap
    """
    创造渐变的二因素图例，通过划分100个格子达到渐变效果。
    :param ax:
    :param fig: 图片对象
    :param range1: x轴区间 （x最大值）
    :param range2: y轴区间 （y最大值）
    :param cmap1: x轴色带
    :param cmap2: y轴色带
    :return:
    """
    # x轴变量
    x_tick = [1]
    x_tick_labels = [int(range1)]
    for step in range(0, 100):
        x_min = (step * (range1 / 100))/range1  # 把数值映射到0-1的区间内
        x_max = ((step + 1) * (range1 / 100))/range1
        color = cmap1(step * 1/100)
        if step == 0:
            continue  # 第一格白色不绘制
        else:
            ax.axvspan(xmin=x_min, xmax=x_max, ymin=0, ymax=1, alpha=0.8, color=color, linewidth=0)
    plt.xticks(x_tick, x_tick_labels, fontsize=5)
    # y轴变量
    y_tick = [0, 1]
    y_tick_labels = [0, int(range2)]
    for step in range(0, 100):
        y_min = (step * (range2 / 100))/range2  # 每次往上画一格
        y_max = ((step + 1) * (range2 / 100))/range2
        color = cmap2(step * 1/100)  # 色带是从白色开始加深所以第一个取ymin值
        if step == 0:
            continue  # 第一格白色不绘制
        else:
            ax.axvspan(xmin=0, xmax=1, ymin=y_min, ymax=y_max, alpha=0.5, color=color, linewidth=0)
    plt.yticks(y_tick, y_tick_labels, fontsize=5)
    ax.tick_params(axis='both', which='both', length=0)  # remove ticks from the big box
    # ax2.axis('off')  # turn off its axis
    ax.spines['right'].set_color('None')  # 将图片的框隐藏
    ax.spines['top'].set_color('None')
    ax.spines['left'].set_color('None')
    ax.spines['bottom'].set_color('None')
    ax.patch.set_alpha(0.0)
    plt.xlabel('All species', fontsize=6)  # annotate x axis
    plt.ylabel('Shared species', fontsize=6)  # annotate y axis


def two_factor_legend_discrete(fig, range1, range2, cdict1, cdict2, level):
    """
    绘制二因素的legend
    :param cdict1: 配置连续色带1
    :param cdict2: 配置连续色带2
    :param fig: 图片对象
    :param range1: 横轴变量范围
    :param range2: 纵轴变量范围
    :param level: 横纵分隔块数量
    :return:
    """

    # Extracting colors from a continuous colormap
    cdict1 = {'red': [(0.0, 1.0, 1.0),
                      (1.0, 1.0, 1.0)],

              'green': [(0.0, 0.0, 0.0),
                        (1.0, 0.0, 0.0)],

              'blue': [(0.0, 0.0, 0.0),
                       (0.5, 0.0, 0.0),
                       (1.0, 0.0, 0.0)]}
    cmap1 = (mpl.colors.LinearSegmentedColormap('cc', cdict1))
    cmap2 = (mpl.colors.LinearSegmentedColormap('cc', cdict2))
    ax2 = fig.add_axes([0.15, 0.25, 0.1,
                        0.1])  # add new axes to place the legend there and specify its location

    # x轴变量
    x_tick = [0]
    x_tick_labels = [0]
    color_x = []
    color_y = []
    for step in level:
        x_tick.append((step + 1) * (range1 / level))
        x_min = (step + 1) * (1 / level)
        x_max = (step + 2) * (1 / level)
        color = cmap1(x_min)
        color_x.append(color)
        ax2.axvspan(xmin=x_min, xmax=x_max, ymin=0, ymax=1, alpha=0.5, color=color, linewidth=0)
    # y轴变量
    cmap_x = mcolors.ListedColormap(color_x)  # 设置间隔的色带
    for step in level:
        y_min = (step + 1) * (1 / level)  # 每次往上画一格，第一格白色不绘制
        y_max = (step + 2) * (1 / level)
        color = cmap2(y_min)  # 色带是从白色开始加深所以第一个取ymin值
        color_y.append(color)
        ax2.axvspan(xmin=0, xmax=1, ymin=y_min, ymax=y_max, alpha=0.5, color=color, linewidth=0)
    cmap_y = mcolors.ListedColormap(color_y)

    ax2.tick_params(axis='both', which='both', length=0)  # remove ticks from the big box
    # ax2.axis('off')  # turn off its axis
    ax2.set_yticks([])
    ax2.text(s='Species richness', x=0.1, y=-0.25, fontsize=6)  # annotate x axis
    ax2.text(s='Shared species richness', x=-0.25, y=0.2, rotation=90, fontsize=6)  # annotate y axis
    plt.show()
