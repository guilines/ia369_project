import web
import sys
import simplejson as json
import numpy as np
import pandas
import webbrowser
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
    data={}
    values=[]
    years=[]
    names=[]
    if 'plots' in reqs:
        plots=reqs['plots']
        for key in plots:
            print '{}:{}'.format(key,plots[key])
            if plots[key]:
                value,year,name = getData.getTabs(plots[key])
                values.append(value)
                years.append(year)
                names.append(name)
    #TODO: fix this appending, it gets one dimension bigger than it should, requiring additional index on setGraph
    print "values at _apply{0} \n years at _apply{1}".format(values, years)
    graph = getData.setGraph(values,years)
    reqs['graph']=[names]+graph
    
    print reqs['graph']
    #reqs['values'] = getData.plot_A()
    return reqs

if __name__ == '__main__':
    print 'Server running on: 127.0.0.1:8080.'
    #The next line opens a page in the default browser 
#    webbrowser.open("http://127.0.0.1:8080/", new=2)
    app.run()

