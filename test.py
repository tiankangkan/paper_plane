# -*- coding:utf8 -*-
import os
import re
import json
import csv
import requests
import threading

global thread_num
global error_count

from multiprocessing.dummy import Pool


def map_func_async(func, args_list, worker_num=8):
    job = lambda args: func(args)
    p = Pool(worker_num)
    p.map(job, args_list)

def request_url(url):
    r = requests.post(url)
    print r
    try:
        print r.text
        # res = eval(r.text)
        # print res
    except:
        pass
        # error_count += 1
        # print error_count


def analysis_csv():
    thread_num = 0
    threads = []
    url = ur'http://10.188.3.152:80/translate_daily?fileinfo={"dumpFileStoreDir": "group3/M00/3E/E8/CrkSIFcsUjCANhJDAAACJXFxNgY6742300", "uploadTime": 1462520754000, "p_id": "2", "dumpFileName": "0330d87f6436ac348249b7dabf7ea79f", "uin": 1318798393, "uuidBinary": "", "pluginName": "newblue", "deviceId": "iPhone 5S", "versionName": "6.3.5.118", "uuidRDM": "83a4c159-8712-4ea4-a22c-f6a9bfad39b9", "id": 7692002}'
    map_func_async(request_url, [url for i in range(1000)], 20)
    # while True:
    #     th = threading.Thread(target=request_url, args=(url,))
    #     threads.append(th)
    #     try:
    #         th.start()
    #         thread_num += 1
    #     except:
    #         import traceback
    #         traceback.print_exc()
    #     if thread_num == 1:
    #         for th in threads:
    #             th.join()
    #         thread_num = 0
    #         threads = []


if __name__ == '__main__':
    analysis_csv()
