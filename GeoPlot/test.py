def multi_plot(plot_row, plot_column, df, proj):
    """
    绘制多个地图在同个图片中
    :param proj: 投影
    :param plot_row: 绘制子图的行数
    :param plot_column: 绘制子图的列数
    :param df: 需要绘制的数据
    :return:
    """
    fig, axs = plt.subplots(plot_row, plot_column, subplot_kw={'projection': proj})  # 准备画图
    for index_row in range(0, plot_row):  # 循环画图
        for index_column in range(0, plot_column):
            ax = axs[index_row, index_column]
            ax.set_extent([-5000000, 6000000, -5000000, 6000000], crs=proj)
            df.plot(ax=ax, color='grey', linewidth=df['Id'])  # 绘制格子
            ax.set_title(f'Axis [gnus{index_row}, {index_column}]', {'style': 'italic'})
            ax.gridlines(
                xlocs=np.arange(-180, 180 + 1, 10), ylocs=np.arange(-90, 90 + 1, 10),
                draw_labels=True, x_inline=False, y_inline=False,
                linewidth=0.5, linestyle='--', color='gray'
            )
            ax.set_axis_off()
    plt.show()  # 显示图片
