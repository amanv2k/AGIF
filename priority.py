import pandas as pd
import numpy as np
from utils import miulab
import pickle

def priority():
    with open('intents', 'rb') as fp:
        lines = pickle.load(fp)
    with open("priority.txt","r") as fw:
        rank = [x.strip().split(" ") for x in fw]

    def printing(lst):
        intent=""
        fp = open("prioritized_intents.txt", 'a')
        for i in range(len(lst)):
            for x in rank:
                if lst[i]==x[1]:
                    if i != len(lst)-1:
                        intent = x[0][5:]
                        print(intent,end=',')
                        fp.write(intent + ',')
                        break
                    else:
                        intent = x[0][5:]
                        print(intent)
                        fp.write(intent + '\n')
                        break





    for lst in lines:
        temp = []
        for i in range(len(lst)):
            for lst1 in rank:
                if lst[i]==(lst1[0]):
                    temp.append(lst1[1])
                    break
            temp.sort()
        printing(temp)












