#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import os
import re

def readTxt(filename):
    with open(filename, "r") as f:
        return f.readlines()

def convert(lines):
    convertedLines = []
    i = 0
    for line in lines:
        if re.match("\s+", line):
            continue
        words = line.split()
        newLine = []
        for j in range(len(words)):
            newLine.extend(str(i+1) + "-" + str(j+1) + "\t" + words[j] + "\n")
        convertedLines.append(newLine)
        i+=1
    return convertedLines

def writeTsv(lines, filename):
    with open(filename, "w") as f:
        for line in lines:
            f.write("".join(line) + "\n")

def convertFile(filenameIn, filenameOut):
    writeTsv(convert(readTxt(filenameIn)), filenameOut)

def convertFiles(pathIn, pathOut):
    for filename in os.listdir(path):
        convertFile(os.path.join(path, filename), os.path.join(pathOut, filename.replace(".txt", ".tsv")))

if __name__=="__main__":
    path = sys.argv[1]
    pathOut = sys.argv[2]
    convertFiles(path, pathOut)
