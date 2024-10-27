import pandas as pd
import dash
from dash.dependencies import Input, Output
from dash import dcc
from dash import html
import plotly.express as px

app = dash.Dash(__name__)

df = px.data.iris()

app.layout = html.Div([

    
    dcc.Graph(id="heatmap"),
    dcc.Graph(id="heatmap2")
])


@app.callback(
    [
     Output(component_id="heatmap", component_property="figure"),
     Output(component_id="heatmap2", component_property="figure"),
    ],
    Input(component_id="heatmap", component_property="hoverData")
)
def update(hover):  # inputs

    fig2 = px.scatter(df, x="sepal_width", y="sepal_length", color="sepal_length")
    
    fig.update_traces(marker_color="white")

    return fig, fig2


if __name__ == '__main__':
    app.run_server(debug=True, port=8080)
