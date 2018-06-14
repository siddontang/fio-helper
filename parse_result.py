import sys
import os 
import json

def parse_job(job, data):
    bw_avg = "{:.1f}M/s".format(job["bw"] / 1024.0)
    bw_min = "{:.1f}M/s".format(job["bw_min"] / 1024.0) 
    bw_max = "{:.1f}M/s".format(job["bw_max"] / 1024.0) 

    iops_avg = "{:.1f}".format(job["iops"])
    iops_min = "{:.1f}".format(job["iops_min"])
    iops_max = "{:.1f}".format(job["iops_max"])
    
    lat_min = "{:.1f}us".format(job["lat_ns"]["min"] / 1000.0)
    lat_max = "{:.1f}us".format(job["lat_ns"]["max"] / 1000.0)
    lat_mean = "{:.1f}us".format(job["lat_ns"]["mean"] / 1000.0)
    
    data.extend([bw_avg, bw_min, bw_max, iops_avg, iops_min, iops_max, lat_min, lat_max, lat_mean])
    return data


def parse_file(res, name):
    with open(name) as f:
        data = json.load(f)

    g_opts = data["global options"]
    ioengine = g_opts["ioengine"]
    bs = g_opts["bs"]
    iodepth = g_opts.get("iodepth", 0)
    fdatasync = g_opts.get("fdatasync", 0)
    direct = g_opts.get("direct", 0)

 
    for index, job in enumerate(data["jobs"]):
        jobname = str(job["jobname"])

        row = [ioengine, bs, str(len(data["jobs"]))]

        if iodepth > 0:
            row.append("iodepth" + str(iodepth))
        elif fdatasync > 0:
            row.append("sync")
        elif direct > 0:
            row.append("direct")
        else:
            row.append("cache")

        row.extend(["job" + str(index), "{:.2f}%".format(data["disk_util"][0]["util"])])            

        if jobname.find("read") > -1 or jobname.find("rw") > -1:
            row = parse_job(job["read"], row)
    
        if jobname.find("write") > -1 or jobname.find("rw") > -1:
            row = parse_job(job["write"], row)

        rows = res.get(jobname, [])
        rows.append(row)
        res[jobname] = rows


def main():
    log_dir = "./log"
    if len(sys.argv) == 2:
        log_dir = sys.argv[1]

    files = os.listdir(log_dir)
    files.sort()

    res = dict()

    for file in files:
        parse_file(res, os.path.join(log_dir, file))

    jobnames = ["read", "randread", "write", "randwrite", "readwrite", "randrw"]
    for jobname in jobnames:
        if jobname not in res:
            continue

        rows = res[jobname]

        print "##", jobname, "\n"

        if jobname.find("readwrite") > -1 or jobname.find("rw") > - 1:
            print "|" + jobname + "|bs|jobs|ext|job|util|r bw avg|r bw min|r bw max|r iops avg|r iops min|r iops max|r lat min|r lat max|r lat mean|w bw avg|w bw min|w bw max|w iops avg|w iops min|w iops max|w lat min|w lat max|w lat mean|"
            print "| --- " * 24 + "|"
        else:
            print "|" + jobname + "|bs|jobs|ext|job|util|bw avg|bw min|bw max|iops avg|iops min|iops max|lat min|lat max|lat mean|"
            print "| --- " * 15 + "|"

        for row in rows:
            print "| " + " | ".join(row) + " |"

        print "\n"

            

if __name__ == "__main__":
    main()