# -*- coding: utf-8 -*-
import re
import sys
import os
import subprocess

def res_cmd(cmd):
  return subprocess.Popen(
    cmd, stdout=subprocess.PIPE,
    shell=True).communicate()[0]


if __name__ == '__main__':
  while(True):
    # ファイル名をargv[1]の引数に
    filename = sys.argv[1]
    # 確認のためos.systemで表示
    os.system("sugar " + filename)
    cmd = ("sugar " + filename)
    r = str(res_cmd(cmd))

    # 満たすかどうかの判断
    cm_list = re.split('[ ]',r)
    if(cm_list[1] == "SATISFIABLE\\na"):
      print("OK")
    elif(cm_list[1] == "UNSATISFIABLE\\n'"):
      print("No")
      break
    else:
      print("Error?")
      break

    # 各製品の真偽の否定をとって制約に追記
    cm_list2 = []
    con_cm_list = []
    cur_cm = []
    for cm in cm_list:
      cm_list2.append(cm.rstrip("a").rstrip(r"\n").rstrip(r"\\na\\n'"))
    test_count = 0
    for cm in cm_list2:
      cur_cm = cm.split("\\t")
      # print(cur_cm)
      if(test_count > 1):
        t = "(eq " + cur_cm[0] + " " + cur_cm[1] + ") "
        con_cm_list.append(t)
      test_count += 1
    con_cm = "(not (and "
    for l in con_cm_list:
      con_cm += l
    con_cm += "))\n"
    f = open(filename, "a")
    f.write(con_cm)
    f.close()