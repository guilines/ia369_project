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

def _getTabsNames(reqs):
    reqs['names'] = getData.getSheetNames()
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
                #TODO: This is a little messed up
                # the format is varying a lot
                #This should return always one type: [[A.1],[A.2],[B.1],[D.3]]
                values+=value
                years+=year
                names+=[name]
    
    if len(names) > 1:
        tmp_names=list(itertools.chain.from_iterable(names))
        names=[]
        [names.append(item) for item in tmp_names if item not in names]
        names=[names]

    #TODO: fix this appending, it gets one dimension bigger than it should, requiring additional index on setGraph
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

