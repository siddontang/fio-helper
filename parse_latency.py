import sys
import getopt
import operator

from parse_stat import *

def usage():
    print("Usage %s [-i|-o|-h] [--help|--input|--output|]" % sys.argv[0])

def filter_stats(stats, f):
    seen = set()
    stats = [stat for stat in filter(f, stats) if not (stat.iodepth in seen or seen.add(stat.iodepth))]
    stats.sort(key=lambda stat: stat.iodepth)
    return stats

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hi:o", ["help", "input=", "output"])
    except getopt.GetoptError as err:
        print(str(err))
        usage()
        sys.exit(2)

    inputs = []
    output = "./output"
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit(1)
        elif opt in ("-i", "--input"):
            inputs.append(arg)
        elif opt in ("-o", "--output"):
            output = arg
    
    iodepts = [1, 2, 4, 8, 16, 32]

    lats = []
    for log_dir in inputs:
        stats = parse_dir(log_dir, lambda stat: True)

        lats.append(stats)


    for rwmixread in [100, 70]:
        def filter_stat(stat):
            return stat.bs == "4k" and stat.rwmixread == rwmixread and stat.iodepth in iodepts

        with Output(output, "read%d-lat-mean" % rwmixread) as f:
            f.write_head("label,1,2,4,8,16,32")   

            for stats in lats:
                stats = filter_stats(stats, filter_stat)

                if len(stats) == 0:
                    continue

                f.write_stats(stats[0].disk_name, stats, lambda stat: "%.1f" % (stat.read.lat_mean))

        with Output(output, "read%d-lat-p99" % rwmixread) as f:
            f.write_head("label,1,2,4,8,16,32")   

            for stats in lats:
                stats = filter_stats(stats, filter_stat)

                if len(stats) == 0:
                    continue

                f.write_stats(stats[0].disk_name, stats, lambda stat: "%.1f" % (stat.read.lat_p99))

    for rwmixwrite in [100, 30]:
        def filter_stat(stat):
            return stat.bs == "4k" and stat.rwmixread == 100 - rwmixwrite and stat.iodepth in iodepts

        with Output(output, "write%d-lat-mean" % rwmixwrite) as f:
            f.write_head("label,1,2,4,8,16,32")   

            for stats in lats:
                stats = filter_stats(stats, filter_stat)

                if len(stats) == 0:
                    continue

                f.write_stats(stats[0].disk_name, stats, lambda stat: "%.1f" % (stat.write.lat_mean))

        with Output(output, "write%d-lat-p99" % rwmixwrite) as f:
            f.write_head("label,1,2,4,8,16,32")   

            for stats in lats:
                stats = filter_stats(stats, filter_stat)

                if len(stats) == 0:
                    continue

                f.write_stats(stats[0].disk_name, stats, lambda stat: "%.1f" % (stat.write.lat_p99))
  

if __name__ == "__main__":
    main()