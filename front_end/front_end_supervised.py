# -*- coding: utf-8 -*-
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
import plotly.graph_objs as go


app = dash.Dash("Mi segunda aplicacion en Dash")
app.config['suppress_callback_exceptions'] = True

# Read Data
df = pd.read_csv('../data/mag_ym.csv')
X_original = pd.DataFrame(pd.to_datetime(df['YM']))
y_original = df['mag']

# Split data into train and test
X, X_test, y, y_test = train_test_split(X_original, y_original, test_size=0.10)
# Create model and predict
regk = KNeighborsRegressor(n_neighbors=2)
regk.fit(X,y)
regk.predict(X_test)

from sklearn.model_selection import train_test_split
X, X_test, y, y_test = train_test_split(X_original, y_original, test_size=0.10)

app.layout = html.Div(
    [
        # header
        html.Div([
            html.Span("Supervised Learning", className='app-title', style={'textAlign': 'center'})
        ],
            className="row header"),

        # tabs
        html.Div([

            dcc.Tabs(
                id="tabs",
                style={"height": "20", "verticalAlign": "middle"},
                children=[
                    dcc.Tab(label="Regression", value="regression_tab"),
                    dcc.Tab(label="Classification", value="classification_tab")
                ],
                value="model_tabs",
            )

        ],
            className="row tabs_div"
        ),

        # Tab content
        html.Div(id="tab_content", className="row", style={"margin": "5%"}),


        # Style Sheets
        html.Link(
            href="https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css",
            rel="stylesheet"),
        html.Link(
            href="https://cdn.rawgit.com/amadoukane96/8a8cfdac5d2cecad866952c52a70a50e/raw/cd5a9bf0b30856f4fc7e3812162c74bfc0ebe011/dash_crm.css",
            rel="stylesheet")
    ],
    className="row",
    style={"margin": "0%"},
)

# Selecting a tab makes visible checkbox models related to the tab
@app.callback(Output("tab_content", "children"), [Input("tabs", "value")])
def render_content(tab):
    if tab == "classification_tab":
        return html.Div(id='parameters_content',
                        children =
                            [
                                html.Label('n_neighbors'),
                                dcc.Slider(min=0, max=9,
                                           marks={i: '{}'.format(i) if i == 1 else str(i) for i in range(1, 6)},
                                           value=5,
                                           className="row"),
                                html.Hr(),
                                dcc.Graph(id='ytd1',
                                          figure={'data': [
                                              go.Scatter(
                                                  x=X_original['YM'],
                                                  y=y_original,
                                                  name='SP500 YTD',
                                              ),
                                              go.Scatter(
                                                  x=X_original['YM'],
                                                  y=y_original,
                                                  name='SP500 YTD',
                                              )
                                          ],
                                              'layout': go.Layout(title='Menudo lio',
                                                                  xaxis={'title': 'Years'},
                                                                  yaxis={'title': 'Magnitude'}
                                                                  )}, style={'width': '100%', 'display': 'inline-block'}
                                          )
                            ],
                        className="row",style={"margin": "2% 3%"}),

    elif tab == "regression_tab":
        return html.Div(id='website', children=[html.Iframe(src='./ModelosNoSupervisados.html')],
                        className= "row")


if __name__ == "__main__":
    app.run_server(debug=True)