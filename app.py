import simplejson as json
import web
import modules.get_graphs as graphs
from time import gmtime, strftime

g_Graphs = graphs.Graphs()
g_historygraph='modules/data/results.csv'

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
            elif reqs['operation'] == 'next_graph':
                reqs = _next_graph(reqs)
        #s = reqs.value['textfield']
        return json.dumps(reqs,ignore_nan=True)

def _reset(reqs):
    '''Deprecated'''
    return True

def _start(reqs):
    global g_Graphs
    g_Graphs = graphs.Graphs()
    g = g_Graphs.getGraphs()
    reqs['graph1'] = g[0]
    reqs['graph2'] = g[1]
    reqs['names'] = g_Graphs.getGraphNames()
    return reqs

def _next_graph(reqs):
    global g_Graphs,g_historygraph

    names = reqs['graph_names']
    ip = reqs['ip']

    if reqs['selected'] == 'graph1':
        results=[1,-1]
    else:
        results=[-1,1]

    time=strftime("%Y%m%d,%H:%M:%S", gmtime())
    fh=open(g_historygraph,'a+')
    fh.write('{},{},{},{}\n'.format(time,ip,names[0],results[0]))
    fh.write('{},{},{},{}\n'.format(time,ip,names[1],results[1]))
    fh.close()

    if reqs['nLeft'] < 1:
        reqs['stop'] = True
        return reqs

    g = g_Graphs.getGraphs()
    reqs['graph1'] = g[0]
    reqs['graph2'] = g[1]
    reqs['names'] = g_Graphs.getGraphNames()
    return reqs


if __name__ == '__main__':
    print 'Server running on: 127.0.0.1:8080.'

    #The next line opens a page in the default browser 
#    webbrowser.open("http://127.0.0.1:8080/", new=2)
    app.run()

