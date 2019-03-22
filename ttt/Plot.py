import plotly.offline as opy
import plotly.graph_objs as go


class Plot():

    @staticmethod
    def getLinePlot(x, y, title):
        trace1 = go.Scatter(x=x,y=y, marker={'color':'red', 'symbol':'circle', 'size':10},mode='lines', name='1st trace')

        data=go.Data([trace1])
        layout=go.Layout(title=title,xaxis={'title':'Date'}, yaxis={'title':'Value'})
        figure=go.Figure(data=data, layout=layout)
        div=opy.plot(figure, auto_open=False, output_type='div')
        return div

