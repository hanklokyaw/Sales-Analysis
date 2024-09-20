import pandas as pd
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from dash import dash_table
from get_latest_file import find_latest_report
from data_transform_functions import extract_material, agg_so

download_folder_path = "C:/Users/hank.aungkyaw/Downloads"
SO_prefix = "SalesOrder1yearHKResults"

so_filename = find_latest_report(download_folder_path, SO_prefix)

# Ensure filenames are found
if so_filename is None:
    raise FileNotFoundError(f"No file found with prefix {SO_prefix} in {download_folder_path}")

so_filepath = f"{download_folder_path}/{so_filename}"

# Read sales order on gems
so = pd.read_csv(so_filepath)

# Print out df to check if they are loading properly
print(so)

agg_so = agg_so(so)

agg_so['Category'] = agg_so['Item'].str.split('-').str[0]
print(agg_so['Category'].unique())

agg_so['Family'] = agg_so['Item'].str.split('-').str[1]
print(agg_so['Family'].unique())

agg_so['Material'] = agg_so['Item'].apply(extract_material)
print(agg_so['Material'].unique())

merged_df = agg_so[agg_so['Material'] != 'Unknown']

# default_df = merged_df.copy()
# default_df = default_df[
#     ['Unique_ID', 'Item', 'Category', 'Family', 'Material', 'Sales Date', 'Sales Quantity', 'Invoice Date',
#      'Invoice Quantity', 'Date Difference']]
# default_df['Unique_ID'] = default_df['Unique_ID'].str.split('+').str[0]
# default_df.rename(columns={'Unique_ID': 'Document Number', 'Date Difference': 'Lead Time'}, inplace=True)
#
# merged_df = merged_df[
#     ['Item', 'Category', 'Family', 'Material', 'Sales Date', 'Sales Quantity', 'Invoice Date', 'Invoice Quantity',
#      'Date Difference']]
#
# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define dropdown options for filtering
category_option = [{'label': name, 'value': name} for name in merged_df['Category'].unique()]
family_option = [{'label': name, 'value': name} for name in merged_df['Family'].unique()]
material_option = [{'label': name, 'value': name} for name in merged_df['Material'].unique()]
item_option = [{'label': name, 'value': name} for name in merged_df['Item'].unique()]

app.layout = dbc.Container([
    html.H1("Lead Time Dashboard", style={'marginBottom': '40px'}),
    dcc.Input(id='dummy-input', style={'display': 'none'}),

    # Dropdowns and radio buttons
    dbc.Row([
        dbc.Col([
            html.H3("Sales Analysis", style={'marginTop': '40px'}),
            html.Div([
                # First row of dropdowns
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(
                            id='item-dropdown',
                            options=item_option,
                            multi=True,
                            placeholder='Filter by Item',
                        ), width=6
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id='category-dropdown',
                            options=category_option,
                            multi=True,
                            placeholder='Filter by Category',
                        ), width=6
                    )
                ], style={'margin-bottom': '5px'}),
                # Second row of dropdowns
                dbc.Row([
                    dbc.Col(
                        dcc.Dropdown(
                            id='family-dropdown',
                            options=family_option,
                            multi=True,
                            placeholder='Filter by Product Family',
                        ), width=6
                    ),
                    dbc.Col(
                        dcc.Dropdown(
                            id='material-dropdown',
                            options=material_option,
                            multi=True,
                            placeholder='Filter by Material',
                        ), width=6
                    )
                ]),
                # Radio buttons in the same line
                dbc.Row([
                    dbc.Col(
                        html.Div([
                            html.Label('Sort Order'),
                            dcc.RadioItems(
                                id='sort-order-radio',
                                options=[
                                    {'label': 'Ascending', 'value': 'asc'},
                                    {'label': 'Descending', 'value': 'desc'}
                                ],
                                value='desc',
                                labelStyle={'display': 'inline-block', 'marginRight': '10px'}
                            )
                        ], style={'paddingTop': '20px'}),
                        width=12
                    )
                ])
            ], style={'paddingTop': '5px'})
        ])
    ]),
    # Time series plot
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='time-series-plot')
        ], width=12)
    ]),
    dbc.Row([
        dbc.Col([dcc.Graph(id='item-bar-plot')], width=8),
        dbc.Col([dcc.Graph(id='category-bar-plot')], width=4),
    ]),
    dbc.Row([
        dbc.Col([dcc.Graph(id='family-bar-plot')], width=8),
        dbc.Col([dcc.Graph(id='material-bar-plot')], width=4),
    ]),
    dash_table.DataTable(
        id='datatable',
        columns=[{'name': col, 'id': col} for col in merged_df.columns],
        data=merged_df.to_dict('records'),
        fixed_rows={'headers': True},
        style_table={'height': '500px', 'paddingTop': '5px'},
        style_cell={'textAlign': 'left', 'minWidth': '30px', 'maxWidth': '150px', 'whiteSpace': 'normal'},
        style_header={
            'backgroundColor': '#D3D3D3',  # Set a slightly darker grey color for the header background
            'fontWeight': 'bold',
            'border': '1px solid black'  # Define border properties for the header
        },
        style_data={
            'border': '1px solid black'  # Define border properties for the data cells
        }
    )
], fluid=True)


# Callbacks to update the bar plots based on filters
@app.callback(
    [
        Output('item-bar-plot', 'figure'),
        Output('category-bar-plot', 'figure'),
        Output('family-bar-plot', 'figure'),
        Output('material-bar-plot', 'figure')
    ],
    [
        Input('category-dropdown', 'value'),
        Input('family-dropdown', 'value'),
        Input('material-dropdown', 'value'),
        Input('item-dropdown', 'value'),
        Input('sort-order-radio', 'value')
    ]
)
def update_bar_plots(category_filter, family_filter, material_filter, item_filter, sort_order):
    filtered_data = merged_df.copy()

    if category_filter:
        filtered_data = filtered_data[filtered_data['Category'].isin(category_filter)]
    if family_filter:
        filtered_data = filtered_data[filtered_data['Family'].isin(family_filter)]
    if material_filter:
        filtered_data = filtered_data[filtered_data['Material'].isin(material_filter)]
    if item_filter:
        filtered_data = filtered_data[filtered_data['Item'].isin(item_filter)]

    # Item bar plot
    item_data = filtered_data.groupby('Item')['Sales Quantity'].sum().reset_index()
    item_data.columns = ['Item', 'Total Sales Quantity']
    item_data = item_data.sort_values(by='Total Sales Quantity', ascending=(sort_order == 'asc')).head(50)

    item_fig = go.Figure(data=[
        go.Bar(x=item_data['Item'], y=item_data['Total Sales Quantity'])
    ])
    item_fig.update_layout(title='Total Sales Quantity by Item', xaxis_title='Item', yaxis_title='Total Sales Quantity')

    # Category bar plot
    category_data = filtered_data.groupby('Category')['Sales Quantity'].mean().reset_index()
    category_data.columns = ['Category', 'Total Sales Quantity']
    category_data = category_data.sort_values(by='Total Sales Quantity', ascending=(sort_order == 'asc'))

    category_fig = go.Figure(data=[
        go.Bar(x=category_data['Category'], y=category_data['Total Sales Quantity'])
    ])
    category_fig.update_layout(title='Total Sales Quantity by Category', xaxis_title='Category',
                               yaxis_title='Total Sales Quantity')

    # Family bar plot
    family_data = filtered_data.groupby('Family')['Sales Quantity'].mean().reset_index()
    family_data.columns = ['Family', 'Total Sales Quantity']
    family_data = family_data.sort_values(by='Sales Quantity', ascending=(sort_order == 'asc')).head(50)

    family_fig = go.Figure(data=[
        go.Bar(x=family_data['Family'], y=family_data['Total Sales Quantity'])
    ])
    family_fig.update_layout(title='Total Sales Quantity by Family', xaxis_title='Family', yaxis_title='Total Sales Quantity')

    # Material bar plot
    material_data = filtered_data.groupby('Material')['Sales Quantity'].mean().reset_index()
    material_data.columns = ['Material', 'Total Sales Quantity']
    material_data = material_data.sort_values(by='Total Sales Quantity', ascending=(sort_order == 'asc'))

    material_fig = go.Figure(data=[
        go.Bar(x=material_data['Material'], y=material_data['Total Sales Quantity'])
    ])
    material_fig.update_layout(title='Total Sales Quantity by Material', xaxis_title='Material',
                               yaxis_title='Total Sales Quantity')

    return item_fig, category_fig, family_fig, material_fig


# Callbacks to update DataTable based on filters
@app.callback(
    Output('datatable', 'data'),
    [
        Input('category-dropdown', 'value'),
        Input('family-dropdown', 'value'),
        Input('material-dropdown', 'value'),
        Input('item-dropdown', 'value')
    ]
)
# def update_datatable(selected_names, min_available, min_to_order):
def update_datatable(category_filter, family_filter, material_filter, item_filter):
    filtered_data = merged_df.copy()
    filtered_data['Sales Date'] = filtered_data['Sales Date'].dt.strftime('%m/%d/%Y')

    if category_filter:
        filtered_data = filtered_data[filtered_data['Category'].isin(category_filter)]
    if family_filter:
        filtered_data = filtered_data[filtered_data['Family'].isin(family_filter)]
    if material_filter:
        filtered_data = filtered_data[filtered_data['Material'].isin(material_filter)]
    if item_filter:
        filtered_data = filtered_data[filtered_data['Item'].isin(item_filter)]

    filtered_data = filtered_data.sort_values(by='Sales Date', ascending=True)

    return filtered_data.to_dict('records')


# Callback to update the time series plot based on filters
@app.callback(
    Output('time-series-plot', 'figure'),
    [
        Input('category-dropdown', 'value'),
        Input('family-dropdown', 'value'),
        Input('material-dropdown', 'value'),
        Input('item-dropdown', 'value')
    ]
)
def update_time_series_plot(category_filter, family_filter, material_filter, item_filter):
    filtered_data = merged_df.copy()

    if category_filter:
        filtered_data = filtered_data[filtered_data['Category'].isin(category_filter)]
    if family_filter:
        filtered_data = filtered_data[filtered_data['Family'].isin(family_filter)]
    if material_filter:
        filtered_data = filtered_data[filtered_data['Material'].isin(material_filter)]
    if item_filter:
        filtered_data = filtered_data[filtered_data['Item'].isin(item_filter)]

    # Group by Invoice Date and calculate the average Date Difference
    time_series_data = filtered_data.groupby('Sales Date')['Sales Quantity'].mean().reset_index()

    time_series_fig = go.Figure(data=[
        go.Scatter(x=time_series_data['Sales Date'], y=time_series_data['Sales Quantity'], mode='lines+markers')
    ])
    time_series_fig.update_layout(title='Total Sales Quantity Over Time', xaxis_title='Sales Date',
                                  yaxis_title='Total Sales Quantity')

    return time_series_fig


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)