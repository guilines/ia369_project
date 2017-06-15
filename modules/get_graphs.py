import numpy as np
import datasets
import random
import matplotlib.pyplot as plt
import cStringIO

class Graphs:
    def __init__(self):
        # self.nGraphs=number_of_graphs
        self.cmaps=['Greys', 'GnBu', 'YlOrRd']
        self.ss=[100,300,750]
        self.markers=['o','v','^']
        self.rdn_choices=['cmaps','sizes','markers']
        self.graphs_names = ['','']
        self.dataset=['linearIncrease','linearDecrease','constant']


    def encodeGraph(self,figure):
        sio = cStringIO.StringIO()
        figure.savefig(sio, format="PNG")
        encoded_img = sio.getvalue().encode('Base64')
        return ('data:image/png;base64,{}'.format(encoded_img))


    def getGraphs(self):
        item=random.choice(self.rdn_choices)
        cmaps=None
        markers=None
        ss=None

        if item == 'cmaps':
            cmap1=random.choice(self.cmaps)
            cmap2=cmap1
            while cmap1==cmap2:
                cmap2 = random.choice(self.cmaps)
            cmaps=[cmap1,cmap2]

        elif item == 'sizes':
            size1=random.choice(self.ss)
            size2=size1
            while size1==size2:
                size2 = random.choice(self.ss)
            ss=[size1,size2]

        elif item == 'markers':
            marker1=random.choice(self.markers)
            marker2=marker1
            while marker1==marker2:
                marker2 = random.choice(self.markers)
            markers=[marker1,marker2]

        return self.buildGraphs(cmaps=cmaps,ss=ss,markers=markers)


    def buildGraphs(self,cmaps=None,ss=None,markers=None):
        if cmaps is None:
            c = random.choice(self.cmaps)
            cmaps=[c,c]
        if ss is None:
            s = random.choice(self.ss)
            ss = [s,s]
        if markers is None:
            m = random.choice(self.markers)
            markers = [m,m]

        dataset_name=random.choice(self.dataset)
        data = datasets.getDataset(dataset_name)
        graphs=[]

        for i in range(2):
            plt.figure()
            plt.scatter(data[0],data[1],c=range(data[1].size),
                        cmap=cmaps[i],marker=markers[i],s=ss[i])

            if dataset_name == 'constant':
                plt.ylim(0,10)
            sio = cStringIO.StringIO()
            plt.savefig(sio, format="PNG")
            plt.close()
            encoded_img = sio.getvalue().encode('Base64')
            graphs.append('data:image/png;base64,{}'.format(encoded_img))
            graph_name='{},{},{},{}'.format(dataset_name,cmaps[i],markers[i],ss[i])
            self.graphs_names[i] = graph_name

        return graphs

    def getGraphNames(self):
        return self.graphs_names