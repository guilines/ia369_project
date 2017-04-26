import pandas as pd
import numpy as np


def readTab(filename='data/Serie_Grupo_A.xlsx',sheetname='A.2',header=3,index_col=0,skip_footer=6):
    return pd.read_excel(open(filename,'rb'),sheetname=sheetname,
            header=header,index_col=index_col,skip_footer=skip_footer)


def plot_A():
    series=[]
    dados=readTab(sheetname='A.2')
    
    x=dados.keys()
    dados=dados.transpose()
    y=dados.Brasil
    
    res=[]
    res.append(['Ano','Razao de sexo'])
    for i,v in zip(x,y):
        res.append([str(i),v])
    series.append(res)
    
    
    dados=readTab(sheetname='A.4')
    x=dados.keys()
    dados=dados.transpose()
    y=dados.Brasil
    res=[]
    res.append(['Ano','Grau de Urbanizacao'])
    for i,v in zip(x,y):
        res.append([str(i),v])
    series.append(res)

    return series
    #return dados.Brasil.values.tolist()
    #series.append(dados.Brasil.values.tolist())
    #return series


