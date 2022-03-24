# -*- coding:utf8 -*-
import json
import time

def main():
    out_dict = {}
    out_dict2 = {}
    for line in open("a.out"):
        if line!="\n":
            log_line = json.loads(line) 
            path = log_line["properties"]["path"]
            device = ("deviceId" in log_line.keys() and log_line["deviceId"] or "")
            ts = log_line["timestamp"]
            #转换成localtime
            time_local = time.localtime(ts)
            #转换成新的时间格式(2016-05-05 20:28:54)
            dt = time.strftime("%Y-%m-%d",time_local)
            path = log_line["properties"]["path"]
           
            if path.endswith("invitation/genCode"):
                out_dict.setdefault(dt, {
                    "devices": set(),
                    "pv": 0
                })
                out_dict[dt]["devices"].add(device)
                out_dict[dt]["pv"] += 1
            if path.endswith("invitation/getName"):
                out_dict2.setdefault(dt, {
                    "devices": set(),
                    "pv": 0
                })
                out_dict2[dt]["devices"].add(device)
                out_dict2[dt]["pv"] += 1
    print("日期" + "\t  " + "邀请页pv" + "  " +  "邀请页uv" + "  " + "注册页pv" + "  " +  "注册页uv" )
    for k, v in out_dict.items():
        if k in out_dict2.keys():
            v2=out_dict2[k]
            print(k + "\t" + str(v["pv"]) + "\t" +  str(len(v["devices"])) + "\t" + str(v2["pv"]) + "\t" +  str(len(v2["devices"])) )
        else:
            print(k + "\t" + str(v["pv"]) + "\t" +  str(len(v["devices"])) + "\t0\t0")
if __name__ == '__main__':
    main()