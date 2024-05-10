import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px

# Cargar el dataset
df = pd.read_csv('online_shoppers_intention.csv')

# Lista de opciones para el primer dropdown (columnas)
dropdown_columns = [{'label': column, 'value': column} for column in df.columns]

# Lista de opciones para el segundo dropdown (tipo de gráfico)
dropdown_chart_types = [
    {'label': 'Histograma', 'value': 'histogram'},
    {'label': 'Gráfico de dispersión', 'value': 'scatter'},
    {'label': 'Gráfico de barras', 'value': 'bar'}
]

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Layout del dashboard
app.layout = html.Div([
    dcc.Dropdown(
        id='dropdown_column',
        options=dropdown_columns,
        value='PageValues',  # Valor predeterminado del dropdown
        placeholder='Selecciona una columna'
    ),
    dcc.Dropdown(
        id='dropdown_chart_type',
        options=dropdown_chart_types,
        value='histogram',  # Valor predeterminado del dropdown
        placeholder='Selecciona un tipo de gráfico'
    ),
    dcc.Graph(id='graph'),
])

# Callback para actualizar el gráfico según la interacción del usuario
@app.callback(
    Output('graph', 'figure'),
    [Input('dropdown_column', 'value'),
     Input('dropdown_chart_type', 'value')]
)
def update_figure(selected_column, selected_chart_type):
    # Crea y actualiza el gráfico según la interacción del usuario
    if selected_chart_type == 'histogram':
        fig = px.histogram(df, x=selected_column)
    elif selected_chart_type == 'scatter':
        fig = px.scatter(df, x=selected_column, y='PageValues')  # Usando 'PageValues' como ejemplo de eje Y
    elif selected_chart_type == 'bar':
        fig = px.bar(df, x=selected_column, y='PageValues')  # Usando 'PageValues' como ejemplo de eje Y
    else:
        fig = px.histogram(df, x=selected_column)  # Por defecto, mostrar un histograma
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
