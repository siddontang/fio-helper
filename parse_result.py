import sys
import os 
import json

def parse_job(job, data):
    bw = "{:.1f}M/s".format(job["bw_mean"] / 1024.0)
    
    iops = "{:.1f}".format(job["iops_mean"])
    
    lat = "{:.1f}us".format(job["lat_ns"]["mean"] / 1000.0)
    
    data.extend([bw, iops, lat])
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
            print "|" + jobname + "|bs|jobs|ext|job|util|r bw|r iops|r lat|r bw|w iops|w lat|"
            print "| --- " * 12 + "|"
        else:
            print "|" + jobname + "|bs|jobs|ext|job|util|bw|iops|lat|"
            print "| --- " * 9 + "|"

        for row in rows:
            print "| " + " | ".join(row) + " |"

        print "\n"

            

if __name__ == "__main__":
    main()