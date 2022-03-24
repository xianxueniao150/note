# -*- coding:utf8 -*-
import os
import sys
import json

def findAllFile(base):
    for root, ds, fs in os.walk(base):
        for f in fs:
            fullname = os.path.join(root, f)
            yield fullname

def parse(access_log,): 
    out_dict = {}
    for line in open(access_log):
        try:
            log_line = json.loads(line)
            path = log_line["properties"]["path"]
            if path.endswith("invitation/genCode"):
                status = log_line["properties"]["http_status"]
                if status==200:
                    # print(path)
                    print(line)
            if path.endswith("invitation/getName"):
                status = log_line["properties"]["http_status"]
                if status==200:
                    print(line)
        except:
            pass

    return out_dict

def main():
    base = '/data/logs/lpserver-api'
    for i in findAllFile(base):
        if i.endswith("access.log"):
            # print(i)
            out = parse(i)
            # for k, v in out.items():
            #     print(k + "\t" + str(v["pv"]) + "\t" + str(len(v["uids"])) + "\t" + str(len(v["tokens"])) + "\t" + str(len(v["devices"])) + "\t" + str(len(v["ips"])))

if __name__ == '__main__':
    main()
