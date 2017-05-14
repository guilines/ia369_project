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
    ''' Classs responsible to receive GET and POST calls. It is expected to 
    receive messages in JSON format, and will return in this format.'''
    def GET(self):
        ''' Implemented, but not used'''
        reqs = req()
        return render.index(reqs, "Your text goes here.")
        
    def POST(self):
        ''' POST message, will look for a operation field to execute some
        action.'''
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
    '''Deprecated'''
    return True

def _start(reqs):
    '''Deprecated'''
    return True

def _getForbidedSheets():
    '''Set manually sheets that will not work with this plotter'''
    fS =['A.6',
         'C.2', 'C.4', 'C.8', 'C.9',
         'D.5', 'D.31', 'D.29', 'D.30', 'D.23',
         'E.18', 'E.8', 'E.9.1', 'E.20', 'E.21', 'E.14',
         'G.3', 'G.7']
    return fS

def _getTabsNames(reqs):
    '''Get all sheet names from data files, and return them
    in a list'''
    
    #Get sheet names
    sheetNames = getData.getSheetNames()

    #Eliminate not working sheets
    fS = _getForbidedSheets()
    for i,dummy in enumerate(sheetNames):
        for name in dummy:
            for nUse in fS:
                if nUse+':' in name:
                    sheetNames[i].remove(name)
    
    #Return the list
    reqs['names'] = sheetNames
    return reqs

def _apply(reqs):
    '''Get selected sheet names to return a vector list to be plot'''

    data={}
    values=[]
    years=[]
    names=[]
    # For ervery sheet name selected in the page
    if 'plots' in reqs:
        plots=reqs['plots']
        for key in plots:
            if plots[key]:
                #Get the series, years and names of sheets
                #Appending them into a common vector
                value,year,name = getData.getTabs(plots[key])
                values+=value
                years+=year
                names+=[name]
    
    # To normalize the vector, avoiding bad formations
    if len(names) > 1:
        tmp_names=list(itertools.chain.from_iterable(names))
        names=[]
        [names.append(item) for item in tmp_names if item not in names]
        names=[names]

    # Calls the function responsible to set the series and years into a 
    # common format to be plot
    graph = getData.setGraph(values,years)

    #Return the vector with all information, adding the sheet names on the beginning of it
    reqs['graph']=names+graph
    return reqs

if __name__ == '__main__':
    print 'Server running on: 127.0.0.1:8080.'
    #The next line opens a page in the default browser 
#    webbrowser.open("http://127.0.0.1:8080/", new=2)
    app.run()

