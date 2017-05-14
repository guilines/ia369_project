import web
import sys
import simplejson as json
import numpy as np
import pandas
import webbrowser
import itertools
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix

import modules.get_data as getData
urls = ('/', 'messages')
render = web.template.render('templates/')

app = web.application(urls, globals())

req = web.form.Form(web.form.Textbox('', class_='textfield', id='textfield'),)

class messages:
    def GET(self):
        reqs = req()
        return render.index(reqs, "Your text goes here.")
        
    def POST(self):
        data=web.data()
        reqs=json.loads(data)
        if not reqs['operation']:
            print 'Failed to get operation'
            return False
        else:
            print 'Requested operation: {}'.format(reqs['operation'])
            if reqs['operation'] == 'reset':
                reqs =  _reset(reqs)
            elif reqs['operation'] == 'start':
                reqs =  _start(reqs)
            elif reqs['operation'] == 'apply':
                reqs =  _apply(reqs)
            elif reqs['operation'] == 'getTabsNames':
                reqs =  _getTabsNames(reqs)
        #s = reqs.value['textfield']
        return json.dumps(reqs,ignore_nan=True)

def _reset(reqs):
    return True

def _start(reqs):
    return True

def _getForbidedSheets():
    fS=['A.3','A.16','A.7','A.6','A.18','A.8','A.9','A.10',
        'A.11','A.12','B.1','B.2.1','B.2.2','B.8','B.5.1',
        'B.5.2','B.10','C.1','C.1.4','C.1.3','C.2','C.16',
        'C.18','C.4','C.5','C.8','C.9','C.10','C.12','C.14',
        'C.17']

    return fS

def _getTabsNames(reqs):
    sheetNames = getData.getSheetNames()
    fS = _getForbidedSheets()
    for i,dummy in enumerate(sheetNames):
        for name in dummy:
            for nUse in fS:
                if nUse+':' in name:
                    print name
                    sheetNames[i].remove(name)
        
    reqs['names'] = sheetNames
    return reqs

def _apply(reqs):
    VERBOSE=False
    data={}
    values=[]
    years=[]
    names=[]
    if 'plots' in reqs:
        plots=reqs['plots']
        for key in plots:
            if VERBOSE: print '{}:{}'.format(key,plots[key])
            if plots[key]:
                value,year,name = getData.getTabs(plots[key])
                values+=value
                years+=year
                names+=[name]
    
    if len(names) > 1:
        tmp_names=list(itertools.chain.from_iterable(names))
        names=[]
        [names.append(item) for item in tmp_names if item not in names]
        names=[names]

    if VERBOSE:
        print '\n------'
        print "values at _apply{0} \n years at _apply{1}".format(values, years)
    graph = getData.setGraph(values,years)

    if VERBOSE:
        print '--'
        print 'Names:'
        print names 
        print 'graph:'
        print graph


    reqs['graph']=names+graph
    if VERBOSE:
        print '\n\n--------' 
        print reqs['graph']
    #reqs['values'] = getData.plot_A()
    return reqs

if __name__ == '__main__':
    print 'Server running on: 127.0.0.1:8080.'
    #The next line opens a page in the default browser 
#    webbrowser.open("http://127.0.0.1:8080/", new=2)
    app.run()

