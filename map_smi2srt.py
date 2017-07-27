#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 00:03:20 2016, 2107

@author: nad2000
"""
import codecs
import logging
import sys

import click

#%%


def msis(input_file):
    """
    Iterates over lines ins SMI file
    """

    def lines(s):
        ts = None
        for l in s:
            if l.startswith("<SYNC Start="):
                ts = int(l[12:l.index(">")])
            elif l.startswith("<"):
                continue
            else:
                if ts is not None:
                    l = l.replace('\t', ' ').replace("<br>", " / ").strip()
                    yield (ts, l)
                    ts = None

    if isinstance(input_file, str):
        with codecs.open(input_file, "r", "UTF-8") as s:
            yield from lines(s)
    else:
        yield from lines(input_file)


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


def srts(input_file):
    """
    Iterates over lines ins SRT file
    """

    def lines(s):
        ts = None
        num = None
        ts_start, ts_end = None, None
        for l in s.readlines():
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

    if isinstance(input_file, str):
        with codecs.open(input_file, "r", "UTF-8") as s:
            yield from lines(s)
    else:
        yield from lines(input_file)


@click.command()
@click.argument(
    "smi_input",
    type=click.File("r"),
    required=False,
    default="Aachi.And.Ssipak.KOREAN.DVDRiP.KOR.smi")
@click.argument(
    "srt_input",
    type=click.File("r"),
    required=False,
    default="Aachi.And.Ssipak.KOREAN.DVDRiP.SubEng.srt")
def cli(smi_input, srt_input):
    st = dict(msis(smi_input))
    ss = list(srts(srt_input))
    for ts in sorted(st.keys()):
        lines = list(filter(lambda l: l[1] <= ts and ts <= l[2], ss))
        if lines:
            ss_line = ' / '.join(l[3].strip() for l in lines).replace(
                "<br>", " / ").replace('\t', ' ')

            try:
                click.echo(f"{st[ts]}\t{ss_line}")
            except Exception as ex:
                logging.error("Error in line %r: %s", lines, ex)


if __name__ == "__main__":
    cli()
