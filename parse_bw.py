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

def filter_stats_by_rwmixread(stats, f):
    seen = set()
    stats = [stat for stat in filter(f, stats) if not (stat.rwmixread in seen or seen.add(stat.rwmixread))]
    stats.sort(key=lambda stat: stat.rwmixread, reverse=True)
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


    with Output(output, "read-bandwidth") as f:
        f.write_head("label,1,2,4,8,16,32")   


        for stats in lats:
            stats = filter_stats(stats, 
                lambda stat: stat.bs == "4k" and stat.rwmixread == 100 and stat.iodepth in iodepts)
            if len(stats) == 0:
                continue

            f.write_stats(stats[0].disk_name, stats, lambda stat: "%.1f" % (stat.read.lat_mean))


    with Output(output, "read70-bandwidth") as f:
        f.write_head("label,1,2,4,8,16,32")

        for stats in lats:
            stats = filter_stats(stats, lambda stat: stat.bs == "4k" and stat.rwmixread == 70 and stat.iodepth in iodepts)
            if len(stats) == 0:
                continue

            f.write_stats(stats[0].disk_name, stats, lambda stat: "%.1f" % (stat.read.lat_p99))
   

if __name__ == "__main__":
    main()