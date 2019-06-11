import dash
import dash_core_components as dcc # interactive elements (checkbox, dropdown, ...)
import dash_html_components as html # html labels
from dash.dependencies import Input, Output
import dash_table
import pandas as pd

app = dash.Dash("Mi segunda aplicacion en Dash")

# app.layout = shiny UI

app.layout = html.Div(children=[
    html.H1(children='Interaction With Regression Models ', style={'textAlign': 'center'}),

    html.Label('Check List'),
    dcc.Checklist(
        options=[
            {'label': 'Linear Regression      ', 'value': 'LR'},
            {'label': 'K nearest neighbors    ', 'value': 'KN'},
            {'label': 'Decision Tree          ', 'value': 'DT'},
            {'label': 'Random Forest          ', 'value': 'RF'}
        ],
        values=['MTL', 'SF']
    ),

    dcc.Graph(
        id='k_nearest__id',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {'title': 'K nearest neighbor'}
        }
    ),

    dcc.Graph(
        id='linear_regression_id',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {'title': 'Linear Regression'}
        }
    ),

    dcc.Graph(
        id='decision_tree_id',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {'title': 'Decision Tree'}
        }
    ),

    dcc.Graph(
        id='random_forest_id',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'SF'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': u'Montréal'},
            ],
            'layout': {'title': 'Randon Forest'}
        }
    )
])
# < link rel = "stylesheet" href = "css/estilo.css" >
# < header >
# < img src = "Media/ejemplo-logotipo.gif" width = "189" height = "57" alt = "logo" / >
# < h1 > EJEMPLO MAQUETACIÓN</h1>
# < / header >
#
# < !-- Contenido -->
# < section >
#
# < figure >
# < img
# src = "Media/Koala.jpg"
# width = "200"
# height = "200"
# alt = "foto" / >
# < figcaption > Figura: descipción
# foto < / figcaption >
# < / figure >
#
# < p > Lorem
# ipsum
# d
# lacus. < / p >
#
# < / section >
#
# < !-- Contenido
# relacionado -->
# < aside >
# < p > Contenido
# Relacionado < / p >
# < / aside >
#
# < !-- Pie
# de
# pagina -->
# < footer >
# < a
# href = "http://www.ejemplocodigo.com" > www.ejemplocodigo.com < / a >
# < / footer >
#
# < / body >
# < / html >
#
#
#
#
#
#
#
# app.layout = html.Div([
#     html.H1("Mi segunda aplicacion Dash"), # https://dash.plot.ly/dash-html-components
#
#     dash_table.DataTable(id="mitabla",
#                          data=df.to_dict("rows"),
#                          columns=[{"name": "geo", "id": "geo", "deletable": True, "editable": True}, # este editable puede cambiar el nombre de la columna
#                                   {"name": "time", "id": "time"},
#                                   {"name": "total_gdp_ppp_inflation_adjusted", "id": "total_gdp_ppp_inflation_adjusted"}],
#                          editable=True
#                          ),
#
#     #html.Img("miimagen", src="../images/Conclusion2.png"),
#     #dcc.Input("miinput", value="Hola", type="text"), # all Dash components https://dash.plot.ly/dash-core-components
#     html.Div(id="resultado")
# ])
#
# #esto es el server de shiny
# # @app.callback(
# #     Output("resultado", "children"), # children es el value de un div
# #     [Input("miinput", "value")] # es una lista porque puede haber varios inputs pero solo un output
# # )
# # def calcular_longitud(texto):
# #     return len(texto)

if __name__ == "__main__":
    # Server Launch
    app.run_server(debug=True) # set to False to release in production
