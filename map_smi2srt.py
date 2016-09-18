#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 00:03:20 2016

@author: nad2000
"""
import codecs
import sys
import logging
#%%

def msis(file_name):
    """
    Iterates over lines ins SMI file
    """
    ts = None
    with codecs.open(file_name, "r", "UTF-8") as s:
        for l in s:
            if l.startswith("<SYNC Start="):
                ts = int(l[12:l.index(">")])
            elif l.startswith("<"):
                continue
            else:
                if ts is not None:
                    yield (ts, l)
                    ts = None


def extract(file_name):
    output_name, _ = os.path.splitext(file_name)
    output_name += ".list.txt"
    with codecs.open(output_name, "w", 'UTF-8') as out:
        for line in subtitle(file_name):
            out.write("%d\t%s\n" % line)
 
#%%           
def ms(ts_str):
    try:
        ts1, ms = ts_str.split(",")
        ms = int(ms)
        hh, mm, ss = ts1.split(":")
        return ms + 1000 * (int(ss) + 60 * (int(mm) + 60 * int(hh)))
    except:
        return None
    
#%%
          
def srts(file_name):
    """
    Iterates over lines ins SRT file
    """
    ts = None
    num = None
    ts_start, ts_end = None, None
    with codecs.open(file_name, "r", "UTF-8") as s:
        for l in s.xreadlines():
            l = l.strip()
            if l.isdigit():
                num = int(l)
                line = ""
            elif l == "":
                yield (num, ms(ts_start), ms(ts_end), line)
                line = ""
            elif " --> " in l:
                ts_start, ts_end = l.split(" --> ")
            else:
                if line == "":
                    line = l
                else:
                    line += " / " + l

if __name__ == "__main__":
    
    sys.stdout = codecs.getwriter('utf8')(sys.stdout)
    
    st = dict(msis(sys.argv[1] if len(sys.argv) > 1 else "Aachi.And.Ssipak.KOREAN.DVDRiP.KOR.smi"))
    ss = list(srts(sys.argv[2] if len(sys.argv) > 2 else "Aachi.And.Ssipak.KOREAN.DVDRiP.SubEng.srt"))
    keys = sorted(st.keys())                  
    for l in ss:
        idx = filter(lambda i: i >= l[1] and i <= l[2], keys)
        if idx:
            line = ' / '.join(st[i].strip() for i in idx).replace("<br>", "")
        
            try:
                print u"%s\t%s" % (line, l[3])
            except Exception as ex:
                logging.error("Error in line %d (ts: %d): %s", l[0], l[1], ex)

