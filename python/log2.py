# -*- coding:utf8 -*-
import json
import time

def main():
    out_dict = {}
    out_dict2 = {}
    for line in open("a.out"):
        if line!="\n":
            keys=line.split("\t") 
            path = keys[1]
            device = keys[2]
            dt = keys[0]
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