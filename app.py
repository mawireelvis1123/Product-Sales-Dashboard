import pandas as pd
import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State, dash_table
import dash_auth
import plotly.express as px
import io
import base64
from dash.exceptions import PreventUpdate

USERNAME_PASSWORD_PAIRS = [['admin', 'admin123']]

app = dash.Dash(__name__, external_stylesheets=[
    dbc.themes.BOOTSTRAP,
    'https://fonts.googleapis.com/css2?family=Poppins:wght@700&family=Roboto:wght@400;600&display=swap'
], suppress_callback_exceptions=True)
auth = dash_auth.BasicAuth(app, USERNAME_PASSWORD_PAIRS)
server = app.server

# Placeholder dataframe
df = pd.DataFrame()

# Custom CSS for global styles
app.css.append_css({
    'external_url': 'data:text/css;charset=utf-8,' + base64.b64encode('''
        .dash-tabs .tabs {
            background-color: #2F4F4F !important;
            padding: 10px !important;
            border-radius: 12px !important;
        }
        .dash-tabs .tab {
            color: #E0FFFF !important;
            background-color: #87CEEB !important; /* Sky blue background */
            border: 1px solid #00B7EB !important;
            border-radius: 12px !important;
            font-family: 'Roboto', sans-serif !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
            padding: 12px 24px !important;
            margin: 0 5px !important;
            box-shadow: 0 2px 5px rgba(0,0,0,0.2) !important;
            transition: all 0.3s ease !important;
        }
        .dash-tabs .tab:hover {
            color: #FFFFFF !important;
            background-color: #00CED1 !important; /* Slightly darker sky blue on hover */
            box-shadow: 0 0 10px #00B7EB !important;
        }
        .dash-tabs .tab--selected {
            color: #FFFFFF !important;
            background-color: #87CEEB !important; /* Sky blue for selected tab */
            border: 1px solid #00B7EB !important;
            border-radius: 12px !important;
            box-shadow: 0 0 15px #00B7EB, 0 0 25px #00B7EB !important; /* Glowing effect */
            font-family: 'Roboto', sans-serif !important;
            font-weight: 600 !important;
            font-size: 1.1rem !important;
            padding: 12px 24px !important;
        }
        .Select-control, .Select-menu-outer {
            background-color: #F5F5F5 !important;
            color: #333333 !important;
            border: 1px solid #00B7EB !important;
            font-family: 'Roboto', sans-serif !important;
        }
        .Select-option:hover {
            background-color: #C71585 !important;
            color: #FFFFFF !important;
        }
        .DateInput_input {
            background-color: #F5F5F5 !important;
            color: #333333 !important;
            border: 1px solid #00B7EB !important;
            font-family: 'Roboto', sans-serif !important;
        }
        .dash-table-container {
            background-color: #F5F5F5 !important;
            color: #333333 !important;
            border: 1px solid #00B7EB !important;
        }
        .filter-label {
            color: #0000FF !important; /* Blue color for filter labels */
            font-family: 'Roboto', sans-serif !important;
            margin-bottom: 10px !important;
        }
    '''.encode('utf-8')).decode('utf-8')
})

# App layout
app.layout = dbc.Container([
    html.H1(
        "\U0001F4CA Product Sales Dashboard",
        className="text-center my-4",
        style={
            'fontFamily': "'Poppins', sans-serif",
            'fontWeight': '700',
            'fontSize': '3rem',
            'color': '#FFFFFF',
            'textShadow': '0 0 10px #C71585, 0 0 20px #C71585',
            'letterSpacing': '2px'
        }
    ),

    dcc.Upload(
        id='upload-data',
        children=html.Div(['Drag and Drop or ', html.A('Select CSV File', style={'color': '#C71585'})]),
        style={
            'width': '50%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '2px',
            'borderStyle': 'dashed',
            'borderColor': '#00B7EB',
            'borderRadius': '10px',
            'textAlign': 'center',
            'margin': '0 auto 30px auto',
            'backgroundColor': '#FFFF33',
            'display': 'flex',
            'justifyContent': 'center',
            'alignItems': 'center',
            'color': '#333333',
            'fontFamily': "'Roboto', sans-serif",
            'transition': 'all 0.3s ease',
            'boxShadow': '0 0 5px #00B7EB'
        },
        multiple=False
    ),

    html.Div(id='filters-container', children=[], style={'marginBottom': '30px'}),
    dcc.Store(id='filter-store'),

    dcc.Tabs(id='main-tabs', children=[
        dcc.Tab(label="By Geographical Location", children=[
            dbc.Row([
                dbc.Col([
                    html.Label("Select Visualization:", className="filter-label"),
                    dcc.Dropdown(
                        id='visual-selector',
                        options=[
                            {'label': 'Map', 'value': 'map'},
                            {'label': 'Bar Graph', 'value': 'bar'},
                            {'label': 'Pie Chart', 'value': 'pie'}
                        ],
                        value='map',
                        style={
                            'width': '50%',
                            'margin': '0 auto 20px auto',
                            'backgroundColor': '#F5F5F5',
                            'color': '#333333',
                            'border': '1px solid #00B7EB'
                        }
                    )
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='geo-graph'), width=12)
            ])
        ], style={'padding': '20px'}),
        dcc.Tab(label="By Time Period", children=[
            dcc.Tabs(id='time-tabs', children=[
                dcc.Tab(label="By Day of the Week", children=[
                    dcc.Graph(id='metrics-by-day')
                ]),
                dcc.Tab(label="By Week", children=[
                    dcc.Graph(id='metrics-by-week')
                ]),
                dcc.Tab(label="By Month", children=[
                    dcc.Graph(id='metrics-by-month')
                ]),
                dcc.Tab(label="By Year", children=[
                    dcc.Graph(id='metrics-by-year')
                ])
            ])
        ], style={'padding': '20px'}),
        dcc.Tab(label="By Gender", children=[
            dcc.Graph(id='gender-graph')
        ], style={'padding': '20px'}),
        dcc.Tab(label="Basic Statistics", children=[
            html.Div(id='stats-output')
        ], style={'padding': '20px'}),
        dcc.Tab(label="JOB TYPES", children=[
            dcc.Graph(id='job-types-graph'),
            html.Div(id='job-drilldown-container')
        ], style={'padding': '20px'})
    ], style={'marginTop': '20px'})
], fluid=True, style={
    'background': 'linear-gradient(135deg, #2F4F4F 0%, #4682B4 100%)',
    'min-height': '100vh',
    'padding': '30px'
})

def parse_contents(contents):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    return pd.read_csv(io.StringIO(decoded.decode('utf-8')))

@app.callback(
    [Output('filters-container', 'children'),
     Output('filter-store', 'data')],
    Input('upload-data', 'contents')
)
def initialize_filters(contents):
    if contents is None:
        raise PreventUpdate

    global df
    df = parse_contents(contents)
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df.rename(columns={'event_type': 'performance_metric'}, inplace=True)
    df = df[df['gender'].isin(['Male', 'Female']) & df['performance_metric'].notna()]

    # Add time-based columns
    df['day_of_week'] = df['timestamp'].dt.day_name()
    df['week'] = df['timestamp'].dt.strftime('%Y-W%U')
    df['month'] = df['timestamp'].dt.strftime('%Y-%m')
    df['year'] = df['timestamp'].dt.year

    # Add job_type and job_subtype columns (placeholder mapping)
    job_type_map = {
        'click': 'AI Assistant',
        'view': 'Demo Schedule',
    }
    job_subtype_map = {
        'AI Assistant': ['Chat Support', 'Data Analysis'],
        'Demo Schedule': ['Product Demo', 'Trial Setup'],
    }
    df['job_type'] = df['performance_metric'].map(job_type_map).fillna('Other')
    df['job_subtype'] = df['job_type'].map(lambda x: job_subtype_map.get(x, ['Unknown'])[0])

    filters = [
        dbc.Row([
            dbc.Col([
                html.Label("Filter by Gender:", className="filter-label"),
                dcc.Dropdown(
                    id='gender-filter',
                    options=[{'label': g, 'value': g} for g in sorted(df['gender'].dropna().unique())],
                    value=[],
                    multi=True,
                    style={'backgroundColor': '#F5F5F5', 'color': '#333333', 'border': '1px solid #00B7EB'}
                )
            ], width=4),
            dbc.Col([
                html.Label("Filter by Metric:", className="filter-label"),
                dcc.Dropdown(
                    id='metric-filter',
                    options=[{'label': m, 'value': m} for m in sorted(df['performance_metric'].dropna().unique())],
                    value=[],
                    multi=True,
                    style={'backgroundColor': '#F5F5F5', 'color': '#333333', 'border': '1px solid #00B7EB'}
                )
            ], width=4),
            dbc.Col([
                html.Label("Filter by Date Range:", className="filter-label"),
                dcc.DatePickerRange(
                    id='date-filter',
                    min_date_allowed=df['timestamp'].min(),
                    max_date_allowed=df['timestamp'].max(),
                    start_date=df['timestamp'].min(),
                    end_date=df['timestamp'].max(),
                    style={'border': '1px solid #00B7EB'}
                )
            ], width=4)
        ], style={'backgroundColor': '#F5F5F5', 'padding': '20px', 'borderRadius': '10px', 'boxShadow': '0 0 10px #00B7EB'})
    ]

    filter_data = {
        'gender': [],
        'metric': [],
        'start_date': str(df['timestamp'].min()),
        'end_date': str(df['timestamp'].max()),
        'job_type_map': job_type_map,
        'job_subtype_map': job_subtype_map
    }

    return filters, filter_data

@app.callback(
    Output('filter-store', 'data', allow_duplicate=True),
    [Input('gender-filter', 'value'),
     Input('metric-filter', 'value'),
     Input('date-filter', 'start_date'),
     Input('date-filter', 'end_date')],
    State('filter-store', 'data'),
    prevent_initial_call=True
)
def update_filter_store(gender, metric, start_date, end_date, current_data):
    if df.empty or not current_data:
        raise PreventUpdate

    filter_data = {
        'gender': gender or [],
        'metric': metric or [],
        'start_date': str(start_date) if start_date else str(df['timestamp'].min()),
        'end_date': str(end_date) if end_date else str(df['timestamp'].max()),
        'job_type_map': current_data.get('job_type_map', {}),
        'job_subtype_map': current_data.get('job_subtype_map', {})
    }

    return filter_data

def apply_filters(data, gender, metric, start_date, end_date, for_job_types=False):
    dff = data.copy()
    if gender and isinstance(gender, list) and len(gender) > 0:
        dff = dff[dff['gender'].isin(gender)]
    if metric and isinstance(metric, list) and len(metric) > 0 and not for_job_types:
        dff = dff[dff['performance_metric'].isin(metric)]
    if start_date and end_date:
        try:
            dff = dff[(dff['timestamp'] >= pd.to_datetime(start_date)) & (dff['timestamp'] <= pd.to_datetime(end_date))]
        except (ValueError, TypeError):
            pass
    dff = dff.dropna(subset=['gender', 'job_type', 'job_subtype'] + (['performance_metric', 'country'] if not for_job_types else []))
    return dff

@app.callback(
    Output('geo-graph', 'figure'),
    [Input('visual-selector', 'value'),
     Input('filter-store', 'data')]
)
def update_geo_visual(visual_type, filter_data):
    if df.empty or not filter_data or not all(key in filter_data for key in ['gender', 'metric', 'start_date', 'end_date']):
        return {
            'data': [],
            'layout': {
                'title': {'text': 'Geographical Metrics', 'font': {'color': '#333333'}},
                'annotations': [{
                    'text': 'Upload data to view visualizations.',
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 16, 'color': '#333333'}
                }],
                'plot_bgcolor': '#F5F5F5',
                'paper_bgcolor': '#F5F5F5'
            }
        }

    filtered = apply_filters(df, filter_data['gender'], filter_data['metric'], filter_data['start_date'], filter_data['end_date'])
    if filtered.empty:
        return {
            'data': [],
            'layout': {
                'title': {'text': 'Geographical Metrics', 'font': {'color': '#333333'}},
                'annotations': [{
                    'text': 'No data available for the selected filters.',
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 16, 'color': '#333333'}
                }],
                'plot_bgcolor': '#F5F5F5',
                'paper_bgcolor': '#F5F5F5'
            }
        }

    by_country = filtered.groupby(['country', 'performance_metric']).size().reset_index(name='count')

    if visual_type == 'map':
        metric_value = filter_data['metric'][0] if filter_data['metric'] and isinstance(filter_data['metric'], list) and len(filter_data['metric']) > 0 else filtered['performance_metric'].iloc[0] if not filtered['performance_metric'].empty else 'Unknown'
        data = filtered[filtered['performance_metric'] == metric_value]
        if data.empty:
            return {
                'data': [],
                'layout': {
                    'title': {'text': f"Heatmap of {metric_value} by Country", 'font': {'color': '#333333'}},
                    'annotations': [{
                        'text': 'No data for selected metric.',
                        'xref': 'paper',
                        'yref': 'paper',
                        'showarrow': False,
                        'font': {'size': 16, 'color': '#333333'}
                    }],
                    'plot_bgcolor': '#F5F5F5',
                    'paper_bgcolor': '#F5F5F5'
                }
            }
        by_country_heatmap = data['country'].value_counts().reset_index()
        by_country_heatmap.columns = ['country', 'count']
        fig = px.choropleth(by_country_heatmap, locations='country', locationmode='country names', color='count',
                            title=f"Heatmap of {metric_value} by Country", color_continuous_scale=['#FFFF33', '#00B7EB', '#C71585'],
                            template='plotly')
        fig.update_layout(plot_bgcolor='#F5F5F5', paper_bgcolor='#F5F5F5', font_color='#333333')
        return fig

    elif visual_type == 'bar':
        fig = px.bar(by_country, x='country', y='count', color='performance_metric', barmode='group',
                     title='Performance Metrics by Country', template='plotly',
                     color_discrete_sequence=['#00B7EB', '#C71585', '#FFFF33'])
        fig.update_layout(plot_bgcolor='#F5F5F5', paper_bgcolor='#F5F5F5', font_color='#333333')
        return fig

    elif visual_type == 'pie':
        pie_data = by_country.groupby('country')['count'].sum().reset_index()
        fig = px.pie(pie_data, names='country', values='count',
                     title='Proportion of Metrics by Country', template='plotly',
                     color_discrete_sequence=['#00B7EB', '#C71585', '#FFFF33'])
        fig.update_layout(plot_bgcolor='#F5F5F5', paper_bgcolor='#F5F5F5', font_color='#333333')
        return fig

    return {}

@app.callback(
    Output('metrics-by-day', 'figure'),
    Input('filter-store', 'data')
)
def update_day(filter_data):
    if df.empty or not filter_data or not all(key in filter_data for key in ['gender', 'metric', 'start_date', 'end_date']):
        return {
            'data': [],
            'layout': {
                'title': {'text': 'Distribution by Day of the Week', 'font': {'color': '#333333'}},
                'annotations': [{
                    'text': 'Upload data to view visualizations.',
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 16, 'color': '#333333'}
                }],
                'plot_bgcolor': '#F5F5F5',
                'paper_bgcolor': '#F5F5F5'
            }
        }

    filtered = apply_filters(df, filter_data['gender'], filter_data['metric'], filter_data['start_date'], filter_data['end_date'])
    if filtered.empty:
        return {
            'data': [],
            'layout': {
                'title': {'text': 'Distribution by Day of the Week', 'font': {'color': '#333333'}},
                'annotations': [{
                    'text': 'No data available for the selected filters.',
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 16, 'color': '#333333'}
                }],
                'plot_bgcolor': '#F5F5F5',
                'paper_bgcolor': '#F5F5F5'
            }
        }

    by_day = filtered.groupby(['day_of_week', 'performance_metric']).size().reset_index(name='count')
    fig = px.bar(by_day, x='day_of_week', y='count', color='performance_metric', barmode='stack',
                 title='Distribution by Day of the Week', template='plotly',
                 color_discrete_sequence=['#00B7EB', '#C71585', '#FFFF33'])
    fig.update_layout(plot_bgcolor='#F5F5F5', paper_bgcolor='#F5F5F5', font_color='#333333')
    return fig

@app.callback(
    Output('metrics-by-week', 'figure'),
    Input('filter-store', 'data')
)
def update_week(filter_data):
    if df.empty or not filter_data or not all(key in filter_data for key in ['gender', 'metric', 'start_date', 'end_date']):
        return {
            'data': [],
            'layout': {
                'title': {'text': 'Distribution by Week', 'font': {'color': '#333333'}},
                'annotations': [{
                    'text': 'Upload data to view visualizations.',
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 16, 'color': '#333333'}
                }],
                'plot_bgcolor': '#F5F5F5',
                'paper_bgcolor': '#F5F5F5'
            }
        }

    filtered = apply_filters(df, filter_data['gender'], filter_data['metric'], filter_data['start_date'], filter_data['end_date'])
    if filtered.empty:
        return {
            'data': [],
            'layout': {
                'title': {'text': 'Distribution by Week', 'font': {'color': '#333333'}},
                'annotations': [{
                    'text': 'No data available for the selected filters.',
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 16, 'color': '#333333'}
                }],
                'plot_bgcolor': '#F5F5F5',
                'paper_bgcolor': '#F5F5F5'
            }
        }

    by_week = filtered.groupby(['week', 'performance_metric']).size().reset_index(name='count')
    fig = px.bar(by_week, x='week', y='count', color='performance_metric', barmode='stack',
                 title='Distribution by Week', template='plotly',
                 color_discrete_sequence=['#00B7EB', '#C71585', '#FFFF33'])
    fig.update_layout(plot_bgcolor='#F5F5F5', paper_bgcolor='#F5F5F5', font_color='#333333')
    return fig

@app.callback(
    Output('metrics-by-month', 'figure'),
    Input('filter-store', 'data')
)
def update_month(filter_data):
    if df.empty or not filter_data or not all(key in filter_data for key in ['gender', 'metric', 'start_date', 'end_date']):
        return {
            'data': [],
            'layout': {
                'title': {'text': 'Distribution by Month', 'font': {'color': '#333333'}},
                'annotations': [{
                    'text': 'Upload data to view visualizations.',
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 16, 'color': '#333333'}
                }],
                'plot_bgcolor': '#F5F5F5',
                'paper_bgcolor': '#F5F5F5'
            }
        }

    filtered = apply_filters(df, filter_data['gender'], filter_data['metric'], filter_data['start_date'], filter_data['end_date'])
    if filtered.empty:
        return {
            'data': [],
            'layout': {
                'title': {'text': 'Distribution by Month', 'font': {'color': '#333333'}},
                'annotations': [{
                    'text': 'No data available for the selected filters.',
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 16, 'color': '#333333'}
                }],
                'plot_bgcolor': '#F5F5F5',
                'paper_bgcolor': '#F5F5F5'
            }
        }

    by_month = filtered.groupby(['month', 'performance_metric']).size().reset_index(name='count')
    fig = px.bar(by_month, x='month', y='count', color='performance_metric', barmode='stack',
                 title='Distribution by Month', template='plotly',
                 color_discrete_sequence=['#00B7EB', '#C71585', '#FFFF33'])
    fig.update_layout(plot_bgcolor='#F5F5F5', paper_bgcolor='#F5F5F5', font_color='#333333')
    return fig

@app.callback(
    Output('metrics-by-year', 'figure'),
    Input('filter-store', 'data')
)
def update_year(filter_data):
    if df.empty or not filter_data or not all(key in filter_data for key in ['gender', 'metric', 'start_date', 'end_date']):
        return {
            'data': [],
            'layout': {
                'title': {'text': 'Distribution by Year', 'font': {'color': '#333333'}},
                'annotations': [{
                    'text': 'Upload data to view visualizations.',
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 16, 'color': '#333333'}
                }],
                'plot_bgcolor': '#F5F5F5',
                'paper_bgcolor': '#F5F5F5'
            }
        }

    filtered = apply_filters(df, filter_data['gender'], filter_data['metric'], filter_data['start_date'], filter_data['end_date'])
    if filtered.empty:
        return {
            'data': [],
            'layout': {
                'title': {'text': 'Distribution by Year', 'font': {'color': '#333333'}},
                'annotations': [{
                    'text': 'No data available for the selected filters.',
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 16, 'color': '#333333'}
                }],
                'plot_bgcolor': '#F5F5F5',
                'paper_bgcolor': '#F5F5F5'
            }
        }

    by_year = filtered.groupby(['year', 'performance_metric']).size().reset_index(name='count')
    fig = px.bar(by_year, x='year', y='count', color='performance_metric', barmode='stack',
                 title='Distribution by Year', template='plotly',
                 color_discrete_sequence=['#00B7EB', '#C71585', '#FFFF33'])
    fig.update_layout(plot_bgcolor='#F5F5F5', paper_bgcolor='#F5F5F5', font_color='#333333')
    return fig

@app.callback(
    Output('gender-graph', 'figure'),
    Input('filter-store', 'data')
)
def update_gender(filter_data):
    if df.empty or not filter_data or not all(key in filter_data for key in ['gender', 'metric', 'start_date', 'end_date']):
        return {
            'data': [],
            'layout': {
                'title': {'text': 'Metrics by Gender', 'font': {'color': '#333333'}},
                'annotations': [{
                    'text': 'Upload data to view visualizations.',
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 16, 'color': '#333333'}
                }],
                'plot_bgcolor': '#F5F5F5',
                'paper_bgcolor': '#F5F5F5'
            }
        }

    filtered = apply_filters(df, filter_data['gender'], filter_data['metric'], filter_data['start_date'], filter_data['end_date'])
    if filtered.empty or filtered['gender'].isna().all() or filtered['performance_metric'].isna().all():
        return {
            'data': [],
            'layout': {
                'title': {'text': 'Metrics by Gender', 'font': {'color': '#333333'}},
                'annotations': [{
                    'text': 'No data available for the selected filters.',
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 16, 'color': '#333333'}
                }],
                'plot_bgcolor': '#F5F5F5',
                'paper_bgcolor': '#F5F5F5'
            }
        }

    filtered['gender'] = filtered['gender'].astype(str)
    filtered['performance_metric'] = filtered['performance_metric'].astype(str)
    fig = px.histogram(filtered, x='gender', color='performance_metric', barmode='group',
                       title='Metrics by Gender', template='plotly',
                       color_discrete_sequence=['#00B7EB', '#C71585', '#FFFF33'])
    fig.update_layout(plot_bgcolor='#F5F5F5', paper_bgcolor='#F5F5F5', font_color='#333333')
    return fig

@app.callback(
    Output('stats-output', 'children'),
    Input('filter-store', 'data')
)
def update_stats(filter_data):
    if df.empty or not filter_data or not all(key in filter_data for key in ['gender', 'metric', 'start_date', 'end_date']):
        return html.Div("Upload data to view statistics.", style={'color': '#333333', 'fontFamily': "'Roboto', sans-serif"})

    filtered = apply_filters(df, filter_data['gender'], filter_data['metric'], filter_data['start_date'], filter_data['end_date'])
    if filtered.empty:
        return html.Div("No data available for the selected filters.", style={'color': '#333333', 'fontFamily': "'Roboto', sans-serif"})

    # Calculate counts per performance metric
    counts = filtered['performance_metric'].value_counts().reset_index()
    counts.columns = ['Performance Metric', 'Count']

    # Calculate statistical measures on the counts
    count_series = filtered['performance_metric'].value_counts()
    stats_data = {
        'Statistic': ['Mean', 'Median', 'Mode', 'Variance', 'Standard Deviation'],
        'Value': [
            round(count_series.mean(), 2) if not count_series.empty else 'N/A',
            round(count_series.median(), 2) if not count_series.empty else 'N/A',
            count_series.idxmax() if not count_series.empty else 'N/A',
            round(count_series.var(), 2) if not count_series.empty else 'N/A',
            round(count_series.std(), 2) if not count_series.empty else 'N/A'
        ]
    }
    stats_df = pd.DataFrame(stats_data)

    # Create tables
    count_table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in counts.columns],
        data=counts.to_dict('records'),
        style_table={'overflowX': 'auto', 'marginBottom': '20px'},
        style_cell={'textAlign': 'left', 'color': '#333333', 'backgroundColor': '#F5F5F5', 'fontFamily': "'Roboto', sans-serif"},
        style_header={'backgroundColor': '#C71585', 'color': '#FFFFFF', 'fontWeight': 'bold'}
    )

    stats_table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in stats_df.columns],
        data=stats_df.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'color': '#333333', 'backgroundColor': '#F5F5F5', 'fontFamily': "'Roboto', sans-serif"},
        style_header={'backgroundColor': '#C71585', 'color': '#FFFFFF', 'fontWeight': 'bold'}
    )

    return html.Div([
        html.H5("Performance Metric Counts", style={'color': '#333333', 'fontFamily': "'Roboto', sans-serif"}),
        count_table,
        html.H5("Statistical Measures", style={'color': '#333333', 'fontFamily': "'Roboto', sans-serif", 'marginTop': '20px'}),
        stats_table
    ])

@app.callback(
    Output('job-types-graph', 'figure'),
    Input('filter-store', 'data')
)
def update_job_types(filter_data):
    if df.empty or not filter_data or not all(key in filter_data for key in ['gender', 'start_date', 'end_date']):
        return {
            'data': [],
            'layout': {
                'title': {'text': 'Job Types Distribution', 'font': {'color': '#333333'}},
                'annotations': [{
                    'text': 'Upload data to view job types.',
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 16, 'color': '#333333'}
                }],
                'plot_bgcolor': '#F5F5F5',
                'paper_bgcolor': '#F5F5F5'
            }
        }

    filtered = apply_filters(df, filter_data['gender'], None, filter_data['start_date'], filter_data['end_date'], for_job_types=True)
    if filtered.empty:
        return {
            'data': [],
            'layout': {
                'title': {'text': 'Job Types Distribution', 'font': {'color': '#333333'}},
                'annotations': [{
                    'text': 'No data available for the selected filters.',
                    'xref': 'paper',
                    'yref': 'paper',
                    'showarrow': False,
                    'font': {'size': 16, 'color': '#333333'}
                }],
                'plot_bgcolor': '#F5F5F5',
                'paper_bgcolor': '#F5F5F5'
            }
        }

    by_job_type = filtered.groupby('job_type').size().reset_index(name='count')
    fig = px.bar(by_job_type, x='job_type', y='count', title='Job Types Distribution',
                 template='plotly', color='job_type',
                 color_discrete_sequence=['#00B7EB', '#C71585', '#FFFF33'])
    fig.update_layout(plot_bgcolor='#F5F5F5', paper_bgcolor='#F5F5F5', font_color='#333333')
    return fig

@app.callback(
    Output('job-drilldown-container', 'children'),
    Input('job-types-graph', 'clickData'),
    State('filter-store', 'data')
)
def update_job_drilldown(click_data, filter_data):
    if not click_data or not filter_data or df.empty or not all(key in filter_data for key in ['gender', 'start_date', 'end_date', 'job_subtype_map']):
        return html.Div("Click a job type to view details.", style={
            'textAlign': 'center', 'marginTop': '20px', 'color': '#333333', 'fontFamily': "'Roboto', sans-serif"
        })

    selected_job_type = click_data['points'][0]['x']
    filtered = apply_filters(df, filter_data['gender'], None, filter_data['start_date'], filter_data['end_date'], for_job_types=True)
    filtered = filtered[filtered['job_type'] == selected_job_type]

    if filtered.empty:
        return html.Div(f"No jobs available for {selected_job_type}.", style={
            'textAlign': 'center', 'marginTop': '20px', 'color': '#333333', 'fontFamily': "'Roboto', sans-serif"
        })

    by_job_subtype = filtered.groupby('job_subtype').size().reset_index(name='count')
    fig = px.bar(by_job_subtype, x='job_subtype', y='count', title=f'Jobs under {selected_job_type}',
                 template='plotly', color='job_subtype',
                 color_discrete_sequence=['#00B7EB', '#C71585', '#FFFF33'])
    fig.update_layout(plot_bgcolor='#F5F5F5', paper_bgcolor='#F5F5F5', font_color='#333333')
    return dcc.Graph(figure=fig)

if __name__ == '__main__':
    app.run(debug=True)