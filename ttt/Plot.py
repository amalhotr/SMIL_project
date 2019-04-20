import plotly.offline as opy
import plotly.graph_objs as go

class Plot():
    '''
    Plot class provides static methods for generating HTML blocks
    containing various plots. Intended for encapsulating the plotting functionality
    and for ease of writing views
    '''

    @staticmethod
    def getLinePlot(x, y, title):
        '''
        return an HTML div with a plot
        :param x: Horizontal axis data (array-like)
        :param y: Vertical axis data (array-like)
        :param title: Title for the plot
        :return: an html div with a plot
        '''
        trace1 = go.Scatter(x=x,y=y, marker={'color':'red', 'symbol':'circle', 'size':10},mode='lines', name=title)

        layout=go.Layout(title=title,xaxis={'title':'Date'}, yaxis={'title':'Value'})
        figure=go.Figure([trace1], layout=layout)
        div=opy.plot(figure, auto_open=False, output_type='div')
        return div

    @staticmethod
    def getTwoPlots(x1, y1,x2, y2, title):
        '''
        return an HTML div with a plot
        :param x1: Horizontal axis data (array-like)
        :param y1: Vertical axis data (array-like)
        :param x2: Horizontal axis data (array-like)
        :param y2: Vertical axis data (array-like)
        :param title: Title for the plot
        :return: an html div with two plots
        '''
        trace1 = go.Scatter(x=x1,y=y1, marker={'color':'red', 'symbol':'circle', 'size':10},mode='lines', name=title)

        trace2 = go.Scatter(x=x2,y=y2, marker={'color':'blue', 'symbol':'circle', 'size':10},mode='lines', name='Holt Winters Forecast')
        layout=go.Layout(title=title,xaxis={'title':'Date'}, yaxis={'title':'Value'})
        figure=go.Figure([trace1, trace2], layout=layout)
        div=opy.plot(figure, auto_open=False, output_type='div')
        return div

    @staticmethod
    def getPieChart(labels, values, title):
        '''
        return an HTML div with a pie chart
        :param labels: data labels
        :param values: Values mapped to the given labels
        :param title: Title for the chart
        :return: an html div with a pie chart
        '''
        trace = go.Pie(labels=labels, values=values)
        layout=go.Layout(title=title)
        figure=go.Figure([trace], layout=layout)
        div=opy.plot(figure, auto_open=False, output_type='div')
        return div
