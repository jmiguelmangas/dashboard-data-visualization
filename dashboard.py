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
    {'label': 'Gráfico de barras', 'value': 'bar'},
    {'label': 'Gráfico circular', 'value': 'pie'},
    {'label': 'Gráfico de líneas', 'value': 'line'}
]

# Función para calcular métricas estadísticas
def calculate_statistics(column):
    statistics = {
        'Mínimo': df[column].min(),
        'Máximo': df[column].max(),
        'Media': df[column].mean(),
        'Mediana': df[column].median(),
        'Desviación Estándar': df[column].std()
    }
    return statistics

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
    html.Div(id='statistics-table')
])

# Callback para actualizar el gráfico y la tabla de estadísticas según la interacción del usuario
@app.callback(
    [Output('graph', 'figure'),
     Output('statistics-table', 'children')],
    [Input('dropdown_column', 'value'),
     Input('dropdown_chart_type', 'value')]
)
def update_figure(selected_column, selected_chart_type):
    # Crea el gráfico según la interacción del usuario
    if selected_chart_type == 'histogram':
        fig = px.histogram(df, x=selected_column)
    elif selected_chart_type == 'scatter':
        fig = px.scatter(df, x=selected_column, y='PageValues')  # Usando 'PageValues' como ejemplo de eje Y
    elif selected_chart_type == 'bar':
        fig = px.bar(df, x=selected_column, y='PageValues')  # Usando 'PageValues' como ejemplo de eje Y
    elif selected_chart_type == 'pie':
        fig = px.pie(df, names=selected_column)
    elif selected_chart_type == 'line':
        fig = px.line(df, x=selected_column, y='PageValues')  # Usando 'PageValues' como ejemplo de eje Y
    else:
        fig = px.histogram(df, x=selected_column)  # Por defecto, mostrar un histograma
    
    # Calcula las estadísticas
    statistics = calculate_statistics(selected_column)
    
    # Crea la tabla de estadísticas
    statistics_table = html.Table(
        [html.Tr([html.Td(key), html.Td("{:.2f}".format(value))]) for key, value in statistics.items()],
        style={'margin-top': '20px'}
    )
    
    return fig, statistics_table

if __name__ == '__main__':
    app.run_server(debug=True)
