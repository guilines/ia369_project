import pandas as pd
import numpy as np
from modules.get_constrains import *


def readTab(filename='data/Serie_Grupo_A.xlsx',sheetname='A.2',header=3,index_col=0,skip_footer=6):
    return pd.read_excel(open(filename,'rb'),sheetname=sheetname,
            header=header,index_col=index_col,skip_footer=skip_footer)

def setGraph(series,years):
    series=np.asarray(series)
    years=np.asarray(years)

    yearsArray=np.sort(np.unique(np.concatenate(years)))
    graph=np.zeros(shape=(np.size(yearsArray[0]),series.size+1))
    print "yearsArray{0}".format(yearsArray)
    graph[:,0]=yearsArray[0]
    for i in range(1,series.size+1):
        graph[:,i]=np.nan
#TODO: Gotta fix it for only one plot
    for i in range(series[0].size):
        seriesTab=series[0][i]
        yearsTab=years[0][i]
        for s,y in zip(seriesTab,yearsTab):
            k = (yearsTab.index(y)) #index to insert the value
            graph[k,i+1]=s
    graph=graph.tolist()
    for i in range(len(graph)):
        graph[i][0] = str(int(graph[i][0]))
    return graph


    #nTabs=len(series)
    #graphVec=np.empty(shape=(years.size,nTabs))
    #graphVec[:,0]=years

    ##Series = [[[year,value],[year,value],[year,value]],[],[]]
    #for i in years.size:
    #    if graph[i][0] not in series[0,0,:]
    #

    ## Let all vectors with same dates:
    #for tabs in enumerate(np.asarray(series)):
    #    for x,y in tabs:

    #        if x not in years:
    #            

    #    
    #            
    #            
    #graphVec.append(['year','A.1','A.2','B.1'])


def getA(tabs=[1],regiao='Brasil'):
    #Atencao, no javascript, tabs comeca no 0, e nos arquivos, em 1
    getTabs(tabs, regiao)
    # print "tabs{}".format(tabs)
    # series=list()
    # years=list()
    # names=['year']
    # for tab in tabs:
    #     sp = tab.split(':')
    #     _tab = sp[0]
    #     names.append(sp[1][1:])
    #     dados=readTab(filename='data/Serie_Grupo_A.xlsx',
    #             sheetname=_tab)
    #
    #     x=dados.keys()
    #     dados=dados.transpose()
    #     y=dados[regiao]
    #     value=[]
    #     year=[]
    #     for i,v in zip(x,y):
    #         value.append(v)
    #         year.append(str(i))
    #     series.append(value)
    #     years.append(year)
    # return series,years,names
    #
    #
    # #res.append(['Ano','Razao de sexo'])
    # for i,v in zip(x,y):
    #     res.append([str(i),v])
    # series.append(res)
    #
    #
    # dados=readTab(sheetname='A.4')
    # x=dados.keys()
    # dados=dados.transpose()
    # y=dados.Brasil
    # res=[]
    # res.append(['Ano','Grau de Urbanizacao'])
    # for i,v in zip(x,y):
    #     res.append([str(i),v])
    # series.append(res)
    #
    # return series
    # #return dados.Brasil.values.tolist()
    #series.append(dados.Brasil.values.tolist())
    #return series

def getTabs(tabs=[1],region='Brasil'):

    print "tabs{}".format(tabs)
    series = list()
    years = list()
    names = ['year']
    for tab in tabs:
        sp = tab.split(':')
        _tab = sp[0]
        names.append(sp[1][1:])
        group = _tab.split('.')[0]
        sheetName, header, indexCol, footer, label = getConstrains(tab=_tab)
        print sheetName, header, indexCol, footer, label

        dados = readTab('data/Serie_Grupo_{0}.xlsx'.format((group)), sheetname=_tab, header=(header),
                      index_col=indexCol, skip_footer=footer, )

        x = dados.keys()
        dados = dados.transpose()
        y = dados[region]
        value = []
        year = []
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

