# -*- coding:utf8 -*-
import os
import time
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
            device = ("deviceId" in log_line.keys() and log_line["deviceId"] or "")
            ts = log_line["timestamp"]
            #转换成localtime
            time_local = time.localtime(ts)
            dt = time.strftime("%Y-%m-%d",time_local)
            if path.endswith("invitation/genCode"):
                status = log_line["properties"]["http_status"]
                if status==200:
                    print(dt,path,device,sep='\t')
            if path.endswith("invitation/getName"):
                status = log_line["properties"]["http_status"]
                if status==200:
                    print(dt,path,device,sep='\t')
        except:
            pass

    return out_dict

def main():
    base = '/data/logs/lpserver-api'
    for i in findAllFile(base):
        if i.endswith("access.log"):
            date=i.split("/")[4]
            if int(date)>20220323:
                out = parse(i)

if __name__ == '__main__':
    main()
