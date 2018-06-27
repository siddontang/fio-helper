import sys
import os, errno
import json

class SubJobStat:
    bw = 0.0
    iops = 0.0
    lat_mean = 0.0
    lat_p99 = 0.0

    def parse(self, job):
        self.bw += job["bw"] / 1024.0
        self.iops += job["iops"]
        self.lat_mean += job["clat_ns"]["mean"] / 1000.0
        self.lat_p99 += job["clat_ns"]["percentile"]["99.000000"] / 1000.0

    def adjust(self, job_count):
        self.bw /= job_count
        self.iops /= job_count
        self.lat_mean /= job_count
        self.lat_p99 /= job_count

    def __str__(self):
        return "bw: %0.1fM/s, iops: %0.1f, lat mean: %0.1fus, lat p99: %0.1fus" % (self.bw, self.iops, self.lat_mean, self.lat_p99)

class JobStat:
    disk_name = ""
    bs = "4k"
    ioengine = "libaio"
    iodepth = 1
    rwmixread = 100
    read = None
    write = None

    def has_read(self):
        return self.rwmixread > 0

    def has_write(self):
        return self.rwmixread != 100

    def __init__(self, name):
        with open(name) as f:
            data = json.load(f)

        g_opts = data["global options"]

        self.read = SubJobStat()
        self.write = SubJobStat()
        self.ioengine = g_opts["ioengine"]
        
        bs = g_opts.get("bs", None)
        iodepth = g_opts.get("iodepth", None)
        rwmixread = g_opts.get("rwmixread", None)

        self.disk_name = data["disk_util"][0]["name"]
        
        job_count = len(data["jobs"])

        for job in data["jobs"]:
            job_opts = job["job options"]
            if bs == None:
                bs = job_opts["bs"]

            if iodepth == None:
                iodepth = job_opts["iodepth"]

            if rwmixread == None:
                rwmixread = job_opts.get("rwmixread", None)


            self.read.parse(job["read"])
            self.write.parse(job["write"])


        if rwmixread != None:
            self.rwmixread = int(rwmixread)
        elif not self.write.lat_p99 > 0:
            # No write
            self.rwmixread = 100
        else:
            # No read
            self.rwmixread = 0

        self.read.adjust(job_count)
        self.write.adjust(job_count)

        self.bs = bs 
        self.iodepth = int(iodepth)


    def __str__(self):
        return "disk: %s, ioengine: %s, iodepth: %d, bs: %s, rwmixread: %d\nread: %s\nwrite: %s\n" % (self.disk_name, self.ioengine, self.iodepth, self.bs, self.rwmixread, self.read, self.write)


def parse_dir(name, f):
    files = os.listdir(name)
    files.sort()

    stats = [JobStat(os.path.join(name, file)) for file in files]
    
    return list(filter(f, stats))


class Output:
    fd = None
    def __init__(self, output, name):
        try:
            os.makedirs(output)
        except OSError as e:
            if e.errno != errno.EEXIST:
                raise

        self.fd = open(os.path.join(output, "%s.csv" % name), "w")

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.fd.close()

    def write_head(self, head):
        self.fd.write(head)
        self.fd.write("\n")


    def write_stats(self, label, stats, f):
        self.fd.write("%s,%s" % (label, ",".join(map(f, stats))))
        self.fd.write("\n")


def main():
    log_dir = "./log/com"
    if len(sys.argv) == 2:
        log_dir = sys.argv[1]


    stats = parse_dir(log_dir, lambda stat: True)
    for stat in stats:
        print(stat)
            

if __name__ == "__main__":
    main()