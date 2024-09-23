import pandas as pd
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from dash import dash_table
from get_latest_file import find_latest_report
from data_transform_functions import extract_material, agg_so

# Configuration
download_folder_path = "C:/Users/hank.aungkyaw/Downloads"
SO_prefix = "SalesOrder1yearSalesOnlyHKResults677"

# Load the latest sales order report
so_filename = find_latest_report(download_folder_path, SO_prefix)
if so_filename is None:
    raise FileNotFoundError(f"No file found with prefix {SO_prefix} in {download_folder_path}")

# Construct the full file path and load the data
so_filepath = f"{download_folder_path}/{so_filename}"
so = pd.read_csv(so_filepath)

# Data preprocessing
agg_so_df = agg_so(so)

# Extract category, family, and material from item descriptions
agg_so_df['Category'] = agg_so_df['Item'].str.split('-').str[0]
agg_so_df['Family'] = agg_so_df['Item'].str.split('-').str[1]
agg_so_df['Material'] = agg_so_df['Item'].apply(extract_material)

# Filter out rows with 'Unknown' materials
merged_df = agg_so_df[agg_so_df['Material'] != 'Unknown']

merged_df = merged_df[
    ['Item', 'Category', 'Family', 'Material', 'Sales Date', 'Sales Quantity', 'Sales Amount']]

# Parse 'Sales Date' into datetime format, handle errors with 'coerce'
merged_df['Sales Date'] = pd.to_datetime(merged_df['Sales Date'], errors='coerce')

# Initialize the Dash app with Bootstrap styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Dropdown options for filtering
category_options = [{'label': name, 'value': name} for name in merged_df['Category'].unique()]
family_options = [{'label': name, 'value': name} for name in merged_df['Family'].unique()]
material_options = [{'label': name, 'value': name} for name in merged_df['Material'].unique()]
item_options = [{'label': name, 'value': name} for name in merged_df['Item'].unique()]

# Layout of the dashboard
app.layout = dbc.Container([
    # Title
    html.H1("Sales Analysis Dashboard", style={'marginBottom': '40px'}),

    # Filter controls: date picker, dropdowns, and sort order radio buttons
    dbc.Row([
        dbc.Col([
            html.H3("Sales Analysis", style={'marginTop': '40px'}),
            dbc.Row([
                dbc.Col(dcc.DatePickerRange(
                    id='date-picker-range',
                    start_date=merged_df['Sales Date'].min(),
                    end_date=merged_df['Sales Date'].max(),
                    display_format='MM/DD/YYYY',
                    style={'margin-top': '10px'}
                ))
            ], style={'marginBottom': '10px'}),
            # Filter dropdowns for Item, Category, Family, and Material
            dbc.Row([
                dbc.Col(
                    dcc.Dropdown(id='item-dropdown', options=item_options, multi=True, placeholder='Filter by Item'),
                    width=6),
                dbc.Col(dcc.Dropdown(id='category-dropdown', options=category_options, multi=True,
                                     placeholder='Filter by Category'), width=6)
            ], style={'margin-bottom': '5px'}),
            dbc.Row([
                dbc.Col(dcc.Dropdown(id='family-dropdown', options=family_options, multi=True,
                                     placeholder='Filter by Family'), width=6),
                dbc.Col(dcc.Dropdown(id='material-dropdown', options=material_options, multi=True,
                                     placeholder='Filter by Material'), width=6)
            ]),
            # Sort order radio buttons
            dbc.Row([
                dbc.Col(html.Div([
                    html.Label('Sort Order'),
                    dcc.RadioItems(id='sort-order-radio', options=[
                        {'label': 'Ascending', 'value': 'asc'},
                        {'label': 'Descending', 'value': 'desc'}
                    ], value='desc', labelStyle={'display': 'inline-block', 'marginRight': '10px'})
                ], style={'paddingTop': '20px'}))
            ])
        ])
    ]),

    # Plots and data table
    dbc.Row([dcc.Graph(id='time-series-plot')]),
    dbc.Row([
        dbc.Col([dcc.Graph(id='item-bar-plot')], width=8),
        dbc.Col([dcc.Graph(id='category-bar-plot')], width=4)
    ]),
    dbc.Row([
        dbc.Col([dcc.Graph(id='family-bar-plot')], width=8),
        dbc.Col([dcc.Graph(id='material-bar-plot')], width=4)
    ]),
    dash_table.DataTable(
        id='datatable',
        columns=[{'name': col, 'id': col} for col in merged_df.columns],
        data=merged_df.to_dict('records'),
        fixed_rows={'headers': True},
        style_table={'height': '500px', 'paddingTop': '5px'},
        style_cell={'textAlign': 'left', 'minWidth': '30px', 'maxWidth': '150px', 'whiteSpace': 'normal'},
        style_header={'backgroundColor': '#D3D3D3', 'fontWeight': 'bold', 'border': '1px solid black'},
        style_data={'border': '1px solid black'}
    )
], fluid=True)


# Helper function to filter the data based on user inputs
def filter_data(start_date, end_date, category_filter, family_filter, material_filter, item_filter):
    # Make a copy of the merged data
    filtered_df = merged_df.copy()

    # Convert the 'Sales Date' column to datetime if it isn't already
    filtered_df['Sales Date'] = pd.to_datetime(filtered_df['Sales Date'], errors='coerce')

    # Filter by date range
    if start_date and end_date:
        filtered_df = filtered_df[
            (filtered_df['Sales Date'] >= pd.to_datetime(start_date)) &
            (filtered_df['Sales Date'] <= pd.to_datetime(end_date))
            ]

    # Apply category filter if specified
    if category_filter:
        filtered_df = filtered_df[filtered_df['Category'].isin(category_filter)]

    # Apply family filter if specified
    if family_filter:
        filtered_df = filtered_df[filtered_df['Family'].isin(family_filter)]

    # Apply material filter if specified
    if material_filter:
        filtered_df = filtered_df[filtered_df['Material'].isin(material_filter)]

    # Apply item filter if specified
    if item_filter:
        filtered_df = filtered_df[filtered_df['Item'].isin(item_filter)]

    # Group the filtered data by necessary columns and sum the sales
    filtered_df = filtered_df.groupby(['Sales Date', 'Item', 'Category', 'Material', 'Family']).agg({
        'Sales Quantity': 'sum',
        'Sales Amount': 'sum'
    }).reset_index()

    # Sort the dataframe by Sales Date in descending order
    filtered_df.sort_values(['Sales Date'], ascending=False, inplace=True)

    # Round the Sales Amount to 2 decimal places
    filtered_df['Sales Amount'] = filtered_df['Sales Amount'].round(2)

    # Format the 'Sales Date' to a readable string (e.g., mm/dd/yyyy)
    filtered_df['Sales Date'] = filtered_df['Sales Date'].dt.strftime("%m/%d/%Y")


    return filtered_df


@app.callback(
    [Output('item-bar-plot', 'figure'),
     Output('category-bar-plot', 'figure'),
     Output('family-bar-plot', 'figure'),
     Output('material-bar-plot', 'figure')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('category-dropdown', 'value'),
     Input('family-dropdown', 'value'),
     Input('material-dropdown', 'value'),
     Input('item-dropdown', 'value'),
     Input('sort-order-radio', 'value')]
)
def update_bar_plots(start_date, end_date, category_filter, family_filter, material_filter, item_filter, sort_order):
    # Filter the data
    filtered_data = filter_data(start_date, end_date, category_filter, family_filter, material_filter, item_filter)

    # Function to create a bar plot with custom hover template
    def create_bar_plot(group_col, title):
        # Grouping by the specified column and calculating total quantity and amount
        grouped_data = filtered_data.groupby(group_col)[['Sales Quantity', 'Sales Amount']].sum().reset_index()
        # Sorting based on Sales Quantity and limiting to top 50 if applicable
        sorted_data = grouped_data.sort_values('Sales Quantity', ascending=(sort_order == 'asc')).head(50)

        # Create the bar plot with hovertemplate for both quantity and amount
        fig = go.Figure(data=[
            go.Bar(
                x=sorted_data[group_col],
                y=sorted_data['Sales Quantity'],
                hovertemplate=(
                        '<b>%{x}</b><br>' +
                        'Total Sales Quantity: %{y}<br>' +
                        'Total Sales Amount: %{customdata[0]:,.2f}<extra></extra>'
                ),
                customdata=sorted_data[['Sales Amount']].values  # Add custom data for hover (Sales Amount)
            )
        ])

        # Update layout of the plot
        fig.update_layout(
            title=title,
            xaxis_title=group_col,
            yaxis_title='Total Sales Quantity',
            template='plotly_white'
        )
        return fig

    # Return the updated figures for all bar plots
    return (
        create_bar_plot('Item', 'Top 50 Sales Quantity by Item'),
        create_bar_plot('Category', 'Total Sales Quantity by Category'),
        create_bar_plot('Family', 'Top 50 Sales Quantity by Family'),
        create_bar_plot('Material', 'Total Sales Quantity by Material')
    )


# Callback to update the time-series plot
@app.callback(
    Output('time-series-plot', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('category-dropdown', 'value'),
     Input('family-dropdown', 'value'),
     Input('material-dropdown', 'value'),
     Input('item-dropdown', 'value')]
)
def update_time_series_plot(start_date, end_date, category_filter, family_filter, material_filter, item_filter):
    filtered_data = filter_data(start_date, end_date, category_filter, family_filter, material_filter, item_filter)

    time_series_data = filtered_data.groupby('Sales Date')[['Sales Quantity', 'Sales Amount']].sum().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=time_series_data['Sales Date'], y=time_series_data['Sales Quantity'], mode='lines',
                             name='Sales Quantity', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=time_series_data['Sales Date'], y=time_series_data['Sales Amount'], mode='lines',
                             name='Sales Amount', line=dict(color='green', dash='dot'), yaxis='y2'))

    fig.update_layout(
        title='Total Sales Quantity and Sales Amount Over Time',
        xaxis_title='Sales Date',
        yaxis_title='Total Sales Quantity',
        yaxis2=dict(title='Total Sales Amount', overlaying='y', side='right'),
        template='plotly_white'
    )
    return fig


# Callback to update the data table
@app.callback(
    Output('datatable', 'data'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('category-dropdown', 'value'),
     Input('family-dropdown', 'value'),
     Input('material-dropdown', 'value'),
     Input('item-dropdown', 'value')]
)
def update_table(start_date, end_date, category_filter, family_filter, material_filter, item_filter):
    filtered_data = filter_data(start_date, end_date, category_filter, family_filter, material_filter, item_filter)
    return filtered_data.to_dict('records')


# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
