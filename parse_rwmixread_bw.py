import sys
import getopt
import operator

from parse_stat import *

def usage():
    print("Usage %s [-i|-o|-h] [--help|--input|--output|]" % sys.argv[0])


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


    # Define customized filter here
    rwmixreads = [100, 90, 80, 70, 60, 50]
    def f(stat):
        return stat.bs == "4k" and stat.rwmixread in rwmixreads and stat.iodepth == 32

    with Output(output, "mix-read-bandwidth") as f:
        f.write_head("label,100%,90%,80%,70%,60%,50%")   


        for stats in lats:
            stats = filter_stats_by_rwmixread(stats, 
                lambda stat: stat.bs == "4k" and stat.rwmixread in rwmixreads and stat.iodepth == 32)
            if len(stats) == 0:
                continue

            f.write_stats("Reads", stats, lambda stat: "%.1f" % (stat.read.bw))
            f.write_stats("Writes", stats, lambda stat: "%.1f" % (stat.write.bw))
            f.write_stats("Combines", stats, lambda stat: "%.1f" % (stat.read.bw + stat.write.bw))

    with Output(output, "mix-read-var-write-bandwidth") as f:
        f.write_head("label,100%,90%,80%,70%,60%,50%")   


        for stats in lats:
            stats = filter_stats_by_rwmixread(stats, 
                lambda stat: stat.bs == "4k" and stat.rwmixread in rwmixreads and stat.iodepth == 32)
            if len(stats) == 0:
                continue

            f.write_stats("4KB Write", stats, lambda stat: "%.1f" % (stat.read.bw + stat.write.bw))
            
        for stats in lats:
            stats = filter_stats_by_rwmixread(stats, 
                lambda stat: stat.bs == "4k,128k" and stat.rwmixread in rwmixreads and stat.iodepth == 32)
            if len(stats) == 0:
                continue

            f.write_stats("128KB Write", stats, lambda stat: "%.1f" % (stat.read.bw + stat.write.bw))
    
   

if __name__ == "__main__":
    main()