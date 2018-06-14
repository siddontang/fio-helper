import sys
import os 
import json

def parse_job(job, data):
    bw_avg = str(job["bw"])
    bw_min = str(job["bw_min"])
    bw_max = str(job["bw_max"])
    # bw_agg = str(job["bw_agg"])
    # bw_mean = str(job["bw_mean"])
    # bw_dev = str(job["bw_dev"])
    iops_avg = str(job["iops"])
    iops_min = str(job["iops_min"])
    iops_max = str(job["iops_max"])
    # iops_mean = str(job["iops_mean"])
    # iops_stddev = str(job["iops_stddev"])
    # slat_min = str(job["slat_ns"]["min"])
    # slat_max = str(job["slat_ns"]["max"])
    # slat_mean = str(job["slat_ns"]["mean"])
    # slat_stddev = str(job["slat_ns"]["stddev"])
    # clat_min = str(job["clat_ns"]["min"])
    # clat_max = str(job["clat_ns"]["max"])
    # clat_mean = str(job["clat_ns"]["mean"])
    # clat_stddev = str(job["clat_ns"]["stddev"])
    lat_min = str(job["lat_ns"]["min"])
    lat_max = str(job["lat_ns"]["max"])
    lat_mean = str(job["lat_ns"]["mean"])
    # lat_stddev = str(job["lat_ns"]["stddev"])

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

        row.extend(["job" + str(index), str(data["disk_util"][0]["util"])])            

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

    for jobname, rows in res.iteritems():
        if jobname.find("readwrite") > -1 or jobname.find("rw") > - 1:
            print "|" + jobname + "|bs|jobs|ext|job|util|r bw avg|r bw min|r bw max|r iops avg|r iops min|r iops max|r lat min|r lat max|r lat mean|w bw avg|w bw min|w bw max|w iops avg|w iops min|w iops max|w lat min|w lat max|w lat mean|"
            print "| --- " * 24 + "|"
        else:
            print "|" + jobname + "|bs|jobs|ext|job|util|bw avg|bw min|bw max|iops avg|iops min|iops max|lat min|lat max|lat mean|"
            print "| --- " * 15 + "|"

        for row in rows:
            print "| " + " | ".join(row) + " |"

            

if __name__ == "__main__":
    main()