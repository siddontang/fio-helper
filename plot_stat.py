import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
  

class Row:
    label = ""
    cols = []

    def __init__(self, label, cols):
        self.label = label
        self.cols = cols

def draw_lat_with_iodepth(y_label, iodepths, rows):
    for row in rows:
        plt.plot(iodepths, row.cols, label = row.label)
    
    ax = plt.axes()
    plt.xscale('log', basex=2)
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.xaxis.set_minor_formatter(ticker.NullFormatter())
    ax.xaxis.set_minor_locator(ticker.NullLocator())

    plt.yscale('log')
    ax.yaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.yaxis.set_minor_formatter(ticker.NullFormatter())
    ax.yaxis.set_minor_locator(ticker.NullLocator())
    ax.yaxis.grid(True)

    plt.xlabel('Queue Depth')
    plt.ylabel(y_label)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=2, fancybox=False, shadow=True)
            

def draw_bw_with_iodepth(y_label, iodepths, rows):
    for row in rows:
        plt.plot(iodepths, row.cols, label = row.label)
    
    ax = plt.axes()
    plt.xscale('log', basex=2)
    ax.xaxis.set_major_formatter(ticker.ScalarFormatter())
    ax.xaxis.set_minor_formatter(ticker.NullFormatter())
    ax.xaxis.set_minor_locator(ticker.NullLocator())

    # Use proper formatter and locator for Y axis later.
    ax.yaxis.grid(True)

    plt.xlabel('Queue Depth')
    plt.ylabel(y_label)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=2, fancybox=False, shadow=True)

def draw_bw_with_read_ratio(y_label, read_ratios, rows):
    for row in rows:
        plt.plot(read_ratios, row.cols, label = row.label)
    
    ax = plt.axes()
    ax.set_xlim(100, 50)
    ax.xaxis.set_major_formatter(ticker.FormatStrFormatter('%d%%'))
    
    # Use proper formatter and locator for Y axis later.
    ax.yaxis.grid(True)

    plt.xlabel('Read percentage')
    plt.ylabel(y_label)
    plt.legend(loc='upper center', bbox_to_anchor=(0.5, -0.05), ncol=2, fancybox=False, shadow=True)


if __name__ == "__main__":
    # rows = []
    
    # rows.append(Row("a", [1, 30, 40, 50, 110, 800]))
    # rows.append(Row("b", [100, 300, 400, 500, 600, 900]))

    # # draw_lat_with_iodepth("Mean Read Latency (us)\n(Read Only)", [1, 2, 4, 8, 16, 32], rows)

    # draw_bw_with_iodepth("Bandwidth (MB/s)\n(Read Only)", [1, 2, 4, 8, 16, 32], rows)

    rows = []
    rows.append(Row("a", [1000, 900, 800, 700, 600, 200]))
    rows.append(Row("b", [100, 300, 400, 500, 600, 900]))
    
    draw_bw_with_read_ratio("Bandwidth (MB/s)", [100, 90, 80, 70, 60, 50], rows)

    plt.show()