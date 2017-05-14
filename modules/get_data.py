import itertools
import pandas as pd
import numpy as np
from modules.get_constrains import *


def readTab(filename='data/Serie_Grupo_A.xlsx',sheetname='A.2',header=3,index_col=0,skip_footer=6):
    return pd.read_excel(open(filename,'rb'),sheetname=sheetname,
            header=header,index_col=index_col,skip_footer=skip_footer)

def setGraph(series,years):
    VERBOSE=True
    seriesSize=len(series)
    series=np.asarray(series)
    years=np.asarray(years)

    _years=years
    while any(isinstance(el, list) for el in _years):
        _years=list(itertools.chain.from_iterable(years))
    yearsArray=np.sort(np.unique(_years))

    graph=np.zeros(shape=(np.size(yearsArray),seriesSize+1))
    if VERBOSE: print "yearsArray{0}".format(yearsArray)
    graph[:,0]=yearsArray


    for i in range(1,seriesSize+1):
        graph[:,i]=np.nan

    if VERBOSE:
        print '\n--'
        print 'Graph'
        print graph
        print 'Series'
        print series
        print 'Years'
        print years
        print '--\n' 

    if not seriesSize == 1:
        for i in range(seriesSize):
            seriesTab=series[i]
            yearsTab=years[i]
            if isinstance(yearsTab, np.ndarray):
                yearsTab=yearsTab.tolist()
            for s,y in zip(seriesTab,yearsTab):
                k = (yearsTab.index(y)) #index to insert the value
                graph[k,i+1]=s


    else:
        graph[:,1]=series

    if VERBOSE:
        print '\n--'
        print 'Graph'
        print graph
        print '--\n'


    graph=graph.tolist()
 

    for i in range(len(graph)):
        graph[i][0] = str(int(graph[i][0]))

    return graph


def getA(tabs=[1],regiao='Brasil'):
    #Atencao, no javascript, tabs comeca no 0, e nos arquivos, em 1
    getTabs(tabs, regiao)
    
def getTabs(tabs=[1],region='Brasil'):
    VERBOSE=False
    if VERBOSE: print "tabs{}".format(tabs)
    series = list()
    years = list()
    names = ['Ano']
    for tab in tabs:
        sp = tab.split(':')
        _tab = sp[0]
        group = _tab.split('.')[0]
        sheetName, header, indexCol, footer, label = getConstrains(tab=_tab)
        if VERBOSE: print sheetName, header, indexCol, footer, label

        dados = readTab('data/Serie_Grupo_{0}.xlsx'.format((group)), sheetname=_tab, header=(header),
                      index_col=indexCol, skip_footer=footer, )

        x = dados.keys()
        dados = dados.transpose()
        y = dados[region]
        value = []
        year = []
        names.append(label)
        for i, v in zip(x, y):
            value.append(v)
            year.append(str(i))
        series.append(value)
        years.append(year)
    return series, years, names

def getSheetNames():
    grupos=['A','B','C','D','E','F','G']
    sources=[]
    for let in grupos:
        dados=pd.read_excel(open('data/Serie_Grupo_{}.xlsx'.format(let),'rb'),sheetname='Lista',
            header=None,usecols=[0,1])
        tmp=[]
        for v in dados.as_matrix():
            try:
                tmp.append(str(v[0]) + ': ' + v[1])
            except:
                continue
        sources.append(tmp)
    return sources

