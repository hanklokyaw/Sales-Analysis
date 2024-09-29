import pandas as pd
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from dash import dash_table
from get_latest_file import find_latest_report
from data_transform_functions import extract_material, agg_so

# -------------------------------
# Configuration
# -------------------------------

DOWNLOAD_FOLDER_PATH = "C:/Users/hank.aungkyaw/Downloads"
SO_PREFIX = "SalesOrder1yearSalesOnlyHKResults906"

# -------------------------------
# Data Loading and Preprocessing
# -------------------------------

# Load the latest sales order report
so_filename = find_latest_report(DOWNLOAD_FOLDER_PATH, SO_PREFIX)
if so_filename is None:
    raise FileNotFoundError(f"No file found with prefix '{SO_PREFIX}' in '{DOWNLOAD_FOLDER_PATH}'")

# Construct the full file path and load the data with low_memory=False to suppress DtypeWarnings
so_filepath = f"{DOWNLOAD_FOLDER_PATH}/{so_filename}"
so = pd.read_csv(so_filepath, low_memory=False)
so = so[so["Date"] >= "4/1/2024"]

# Print out the first few rows to verify data loading
print("Loaded Sales Order Data:")
print(so.head())

# Aggregate sales order data using the provided agg_so function
agg_so_df = agg_so(so)

# Extract 'Category', 'Family', and 'Material' from the 'Item' column
agg_so_df['Category'] = agg_so_df['Item'].str.split('-').str[0]
agg_so_df['Family'] = agg_so_df['Item'].str.split('-').str[1]
agg_so_df['Material'] = agg_so_df['Item'].apply(extract_material)

# Print unique values to verify extraction
print("Unique Categories:", agg_so_df['Category'].unique())
print("Unique Families:", agg_so_df['Family'].unique())
print("Unique Materials:", agg_so_df['Material'].unique())

# Filter out rows with 'Unknown' materials
merged_df = agg_so_df[agg_so_df['Material'] != 'Unknown']

# Select relevant columns
# Removed 'Note' as it doesn't exist in the dataset
merged_df = merged_df[['Item', 'Category', 'Family', 'Material', 'Sales Date', 'Sales Quantity', 'Sales Amount']]

# Parse 'Sales Date' into datetime format, handle errors with 'coerce'
merged_df['Sales Date'] = pd.to_datetime(merged_df['Sales Date'], errors='coerce')

# Check for any NaT values after parsing
if merged_df['Sales Date'].isna().any():
    print("Warning: Some 'Sales Date' entries could not be parsed and are set as NaT.")

# -------------------------------
# Initialize Dash App
# -------------------------------

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Sales Analysis Dashboard"

# -------------------------------
# Define Dropdown Options
# -------------------------------

category_options = [{'label': name, 'value': name} for name in sorted(merged_df['Category'].unique())]
family_options = [{'label': name, 'value': name} for name in sorted(merged_df['Family'].unique())]
material_options = [{'label': name, 'value': name} for name in sorted(merged_df['Material'].unique())]
item_options = [{'label': name, 'value': name} for name in sorted(merged_df['Item'].unique())]

# -------------------------------
# Define App Layout
# -------------------------------

app.layout = dbc.Container([
    # Title
    html.H1("Sales Analysis Dashboard", style={'marginBottom': '40px', 'textAlign': 'center'}),

    # -------------------------------
    # Total Sales Amount and Additional Cards
    # -------------------------------
    # Added section to display the total sales amount and five additional sales metrics
    dbc.Row([
        # Total Sales Amount Card
        dbc.Col([
            html.Div(
                style={
                    'backgroundColor': '#1f77b4',
                    'padding': '20px',
                    'borderRadius': '10px',
                    'textAlign': 'center',
                    'color': '#ffffff',
                    'marginBottom': '20px'
                },
                children=[
                    html.H2(
                        children='Total Sales',
                        style={'marginBottom': '10px'}
                    ),
                    html.H1(
                        id='total-sales-amount',
                        children='$0.00',
                        style={'margin': '0'}
                    )
                ]
            )
        ], width=2),  # Adjusted width for the main card

        # SS Sales Amount Card
        dbc.Col([
            html.Div(
                style={
                    'backgroundColor': '#ff7f0e',
                    'padding': '15px',
                    'borderRadius': '10px',
                    'textAlign': 'center',
                    'color': '#ffffff',
                    'marginBottom': '20px'
                },
                children=[
                    html.H4(
                        children='Steel Sales',
                        style={'marginBottom': '5px'}
                    ),
                    html.H5(
                        id='ss-sales-amount',
                        children='$0.00',
                        style={'margin': '0'}
                    )
                ]
            )
        ], width=1),

        # TI Sales Amount Card
        dbc.Col([
            html.Div(
                style={
                    'backgroundColor': '#2ca02c',
                    'padding': '15px',
                    'borderRadius': '10px',
                    'textAlign': 'center',
                    'color': '#ffffff',
                    'marginBottom': '20px'
                },
                children=[
                    html.H4(
                        children='Titanium Sales',
                        style={'marginBottom': '5px'}
                    ),
                    html.H5(
                        id='ti-sales-amount',
                        children='$0.00',
                        style={'margin': '0'}
                    )
                ]
            )
        ], width=1),

        # NB Sales Amount Card
        dbc.Col([
            html.Div(
                style={
                    'backgroundColor': '#d62728',
                    'padding': '15px',
                    'borderRadius': '10px',
                    'textAlign': 'center',
                    'color': '#ffffff',
                    'marginBottom': '20px'
                },
                children=[
                    html.H4(
                        children='Niobium Sales',
                        style={'marginBottom': '5px'}
                    ),
                    html.H5(
                        id='nb-sales-amount',
                        children='$0.00',
                        style={'margin': '0'}
                    )
                ]
            )
        ], width=1),

        # Gold Sales Amount Card
        dbc.Col([
            html.Div(
                style={
                    'backgroundColor': '#9467bd',
                    'padding': '15px',
                    'borderRadius': '10px',
                    'textAlign': 'center',
                    'color': '#ffffff',
                    'marginBottom': '20px'
                },
                children=[
                    html.H4(
                        children='Gold Sales',
                        style={'marginBottom': '5px'}
                    ),
                    html.H5(
                        id='gold-sales-amount',
                        children='$0.00',
                        style={'margin': '0'}
                    )
                ]
            )
        ], width=1),

        # Others Sales Amount Card
        dbc.Col([
            html.Div(
                style={
                    'backgroundColor': '#8c564b',
                    'padding': '15px',
                    'borderRadius': '10px',
                    'textAlign': 'center',
                    'color': '#ffffff',
                    'marginBottom': '20px'
                },
                children=[
                    html.H4(
                        children='Others Sales',
                        style={'marginBottom': '5px'}
                    ),
                    html.H5(
                        id='others-sales-amount',
                        children='$0.00',
                        style={'margin': '0'}
                    )
                ]
            )
        ], width=1)
    ], justify='center'),  # Centers the row

    # Filter Controls
    dbc.Row([
        dbc.Col(
            html.Div([html.Link(rel='stylesheet', href='/assets/styles.css')], id='gem-wait-plots',
                     style={'paddingBottom': '100px'}),
            md=6  # Set the column width to 6 for half of the screen
        ),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(
                    html.H3("Filters", className='blue-table-header'),
                    className='blue-table'  # Apply the same custom styles
                ),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            # Date Range Picker
                            dbc.Row([
                                dbc.Col([
                                    dcc.DatePickerRange(
                                        id='date-picker-range',
                                        start_date=merged_df['Sales Date'].min(),
                                        end_date=merged_df['Sales Date'].max(),
                                        display_format='MM/DD/YYYY',
                                        style={'margin-top': '10px'}
                                    )
                                ]),
                                dbc.Col([
                                    html.Label('Time Format'),
                                    dcc.RadioItems(
                                        id='type-filter',  # Changed ID to 'type-filter' as per user request
                                        options=[
                                            {'label': 'Daily', 'value': 'D'},
                                            {'label': 'Weekly', 'value': 'W'},
                                            {'label': 'Monthly', 'value': 'M'},
                                            {'label': 'Yearly', 'value': 'Y'}
                                        ],
                                        value='M',  # Default value
                                        labelStyle={'display': 'inline-block', 'margin-right': '15px'}
                                    )
                                ]),
                                dbc.Col([
                                    html.Label('Sort'),
                                    dcc.RadioItems(
                                        id='sort-order-radio',
                                        options=[
                                            {'label': 'Ascending', 'value': 'asc'},
                                            {'label': 'Descending', 'value': 'desc'}
                                        ],
                                        value='desc',
                                        labelStyle={'display': 'inline-block', 'margin-right': '15px'}
                                    )
                                ])
                            ], style={'marginBottom': '20px'}),

                            # Dropdowns for Item, Category, Family, Material
                            dbc.Row([
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='item-dropdown',
                                        options=item_options,
                                        multi=True,
                                        placeholder='Filter by Item',
                                    ),
                                    width=6
                                ),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='category-dropdown',
                                        options=category_options,
                                        multi=True,
                                        placeholder='Filter by Category',
                                    ),
                                    width=6
                                )
                            ], style={'marginBottom': '10px'}),

                            dbc.Row([
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='family-dropdown',
                                        options=family_options,
                                        multi=True,
                                        placeholder='Filter by Family',
                                    ),
                                    width=6
                                ),
                                dbc.Col(
                                    dcc.Dropdown(
                                        id='material-dropdown',
                                        options=material_options,
                                        multi=True,
                                        placeholder='Filter by Material',
                                    ),
                                    width=6
                                )
                            ], style={'marginBottom': '10px'}),

                        ], style={'padding': '10px', 'backgroundColor': '#E4E5E5'})
                    ]),
                ])
            ], className='light-blue-table')  # Apply custom card style
        ], width=12)
    ], style={'paddingBottom': '30px'}),


    # Plots
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='time-series-plot')
        ], width=12)
    ], style={'marginTop': '40px'}),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='item-bar-plot')
        ], width=8),
        dbc.Col([
            dcc.Graph(id='category-bar-plot')
        ], width=4)
    ], style={'marginTop': '40px'}),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='family-bar-plot')
        ], width=8),
        dbc.Col([
            dcc.Graph(id='material-bar-plot')
        ], width=4)
    ], style={'marginTop': '40px'}),

    # Data Table
    dbc.Row([
        dbc.Col([
            dash_table.DataTable(
                id='datatable',
                columns=[{'name': col, 'id': col} for col in merged_df.columns],
                data=merged_df.to_dict('records'),
                fixed_rows={'headers': True},
                style_table={'height': '500px', 'overflowY': 'auto'},
                style_cell={
                    'textAlign': 'left',
                    'minWidth': '100px',
                    'maxWidth': '200px',
                    'whiteSpace': 'normal'
                },
                style_header={
                    'backgroundColor': '#D3D3D3',
                    'fontWeight': 'bold',
                    'border': '1px solid black'
                },
                style_data={
                    'border': '1px solid black'
                },
                page_size=20  # Adjust based on preference
            )
        ], width=12)
    ], style={'marginTop': '40px', 'paddingBottom': '40px'})
], fluid=True)

# -------------------------------
# Helper Function
# -------------------------------

def filter_data(start_date, end_date, type_filter, category_filter, family_filter, material_filter, item_filter):
    """
    Filters the merged_df based on the provided criteria.

    Parameters:
        start_date (str): Start date in 'YYYY-MM-DD' format.
        end_date (str): End date in 'YYYY-MM-DD' format.
        type_filter (str): Aggregation level ('D', 'W', 'M', 'Y').
        category_filter (list): List of categories to filter by.
        family_filter (list): List of families to filter by.
        material_filter (list): List of materials to filter by.
        item_filter (list): List of items to filter by.

    Returns:
        pd.DataFrame: Filtered and aggregated dataframe.
    """
    # Make a copy of the merged data
    filtered_df = merged_df.copy()

    # Ensure 'Sales Date' is in datetime format
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

    # Aggregate data based on the type_filter (time aggregation)
    if type_filter == 'D':
        # Daily aggregation
        filtered_df['Sales Period'] = filtered_df['Sales Date'].dt.to_period('D').dt.to_timestamp()
    elif type_filter == 'W':
        # Weekly aggregation
        filtered_df['Sales Period'] = filtered_df['Sales Date'].dt.to_period('W').dt.to_timestamp()
    elif type_filter == 'M':
        # Monthly aggregation
        filtered_df['Sales Period'] = filtered_df['Sales Date'].dt.to_period('M').dt.to_timestamp()
    elif type_filter == 'Y':
        # Yearly aggregation
        filtered_df['Sales Period'] = filtered_df['Sales Date'].dt.to_period('Y').dt.to_timestamp()
    else:
        # Default to daily if no valid type_filter is provided
        filtered_df['Sales Period'] = filtered_df['Sales Date']

    # Group the filtered data by 'Sales Period' and other relevant columns, then sum the sales
    aggregated_df = filtered_df.groupby(['Sales Period', 'Item', 'Category', 'Material', 'Family']).agg({
        'Sales Quantity': 'sum',
        'Sales Amount': 'sum'
    }).reset_index()

    # Sort the dataframe by 'Sales Period' in ascending order
    aggregated_df.sort_values(['Sales Period'], ascending=True, inplace=True)

    # Round the Sales Amount to 2 decimal places
    aggregated_df['Sales Amount'] = aggregated_df['Sales Amount'].round(2)

    return aggregated_df

# -------------------------------
# Callbacks
# -------------------------------

# Callback to update bar plots
@app.callback(
    [Output('item-bar-plot', 'figure'),
     Output('category-bar-plot', 'figure'),
     Output('family-bar-plot', 'figure'),
     Output('material-bar-plot', 'figure')],
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('type-filter', 'value'),
     Input('category-dropdown', 'value'),
     Input('family-dropdown', 'value'),
     Input('material-dropdown', 'value'),
     Input('item-dropdown', 'value'),
     Input('sort-order-radio', 'value')]
)
def update_bar_plots(start_date, end_date, type_filter, category_filter, family_filter, material_filter, item_filter, sort_order):
    """
    Updates the bar plots based on the selected filters.
    """
    # Filter the data
    filtered_data = filter_data(start_date, end_date, type_filter, category_filter, family_filter, material_filter, item_filter)

    # Function to create a bar plot with custom hover template
    def create_bar_plot(group_col, title):
        """
        Creates a bar plot for the specified grouping column.

        Parameters:
            group_col (str): The column to group by (e.g., 'Item', 'Category').
            title (str): The title of the plot.

        Returns:
            plotly.graph_objs.Figure: The bar plot figure.
        """
        # Grouping by the specified column and calculating total quantity and amount
        grouped_data = filtered_data.groupby(group_col)[['Sales Quantity', 'Sales Amount']].sum().reset_index()

        # Sorting based on Sales Quantity and limiting to top 50 if applicable
        if group_col in ['Item', 'Family']:
            sorted_data = grouped_data.sort_values('Sales Quantity', ascending=(sort_order == 'asc')).head(50)
        else:
            sorted_data = grouped_data.sort_values('Sales Quantity', ascending=(sort_order == 'asc'))

        # Create the bar plot with hovertemplate for both quantity and amount
        fig = go.Figure(data=[
            go.Bar(
                x=sorted_data[group_col],
                y=sorted_data['Sales Quantity'],
                hovertemplate=(
                    '<b>%{x}</b><br>' +
                    'Total Sales Quantity: %{y}<br>' +
                    'Total Sales Amount: $%{customdata[0]:,.2f}<extra></extra>'
                ),
                customdata=sorted_data[['Sales Amount']].values,  # Add custom data for hover (Sales Amount)
                marker=dict(color='rgba(55, 128, 191, 0.7)')  # Optional: Customize bar color
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

    # Create figures for each bar plot
    item_fig = create_bar_plot('Item', 'Top 50 Sales Quantity by Item')
    category_fig = create_bar_plot('Category', 'Total Sales Quantity by Category')
    family_fig = create_bar_plot('Family', 'Top 50 Sales Quantity by Family')
    material_fig = create_bar_plot('Material', 'Total Sales Quantity by Material')

    return item_fig, category_fig, family_fig, material_fig

# Callback to update the time-series plot
@app.callback(
    Output('time-series-plot', 'figure'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('type-filter', 'value'),
     Input('category-dropdown', 'value'),
     Input('family-dropdown', 'value'),
     Input('material-dropdown', 'value'),
     Input('item-dropdown', 'value')]
)
def update_time_series_plot(start_date, end_date, type_filter, category_filter, family_filter, material_filter, item_filter):
    """
    Updates the time-series plot based on the selected filters and time aggregation.
    """
    # Filter the data
    filtered_data = filter_data(start_date, end_date, type_filter, category_filter, family_filter, material_filter, item_filter)

    # Group by 'Sales Period' and calculate the sums
    time_series_data = filtered_data.groupby('Sales Period')[['Sales Quantity', 'Sales Amount']].sum().reset_index()

    # Create figure with two traces for quantity and amount
    fig = go.Figure()

    # Add Sales Quantity line
    fig.add_trace(go.Scatter(
        x=time_series_data['Sales Period'],
        y=time_series_data['Sales Quantity'],
        mode='lines',
        name='Sales Quantity',
        line=dict(color='blue'),
        hovertemplate=(
            'Sales Period: %{x}<br>' +
            'Total Sales Quantity: %{y}<br>' +
            '<extra></extra>'
        )
    ))

    # Add Sales Amount line with dotted style on the secondary y-axis
    fig.add_trace(go.Scatter(
        x=time_series_data['Sales Period'],
        y=time_series_data['Sales Amount'],
        mode='lines',
        name='Sales Amount',
        line=dict(color='green', dash='dot'),
        yaxis='y2',
        hovertemplate=(
            'Sales Period: %{x}<br>' +
            'Total Sales Amount: $%{y:,.2f}<br>' +
            '<extra></extra>'
        )
    ))

    # Update layout for dual axes
    fig.update_layout(
        title='Total Sales Quantity and Sales Amount Over Time',
        xaxis_title='Sales Period',
        yaxis_title='Total Sales Quantity',
        yaxis=dict(
            title='Total Sales Quantity',
            showgrid=True,
            zeroline=True
        ),
        yaxis2=dict(
            title='Total Sales Amount',
            overlaying='y',
            side='right',
            showgrid=False,
            zeroline=False
        ),
        legend=dict(x=0.01, y=0.99, bgcolor='rgba(255,255,255,0)'),
        template='plotly_white'
    )

    return fig

# Callback to update the data table
@app.callback(
    Output('datatable', 'data'),
    [Input('date-picker-range', 'start_date'),
     Input('date-picker-range', 'end_date'),
     Input('type-filter', 'value'),
     Input('category-dropdown', 'value'),
     Input('family-dropdown', 'value'),
     Input('material-dropdown', 'value'),
     Input('item-dropdown', 'value')]
)
def update_table(start_date, end_date, type_filter, category_filter, family_filter, material_filter, item_filter):
    """
    Updates the data table based on the selected filters.
    """
    # Filter the data
    filtered_data = filter_data(start_date, end_date, type_filter, category_filter, family_filter, material_filter, item_filter)

    # Format 'Sales Period' as string in 'MM/DD/YYYY' format if it's a Timestamp
    if pd.api.types.is_datetime64_any_dtype(filtered_data['Sales Period']):
        filtered_data['Sales Period'] = filtered_data['Sales Period'].dt.strftime("%m/%d/%Y")

    return filtered_data.to_dict('records')

# Callback to update Total Sales Amount and Additional Sales Amount Cards
@app.callback(
    [
        Output('total-sales-amount', 'children'),
        Output('ss-sales-amount', 'children'),
        Output('ti-sales-amount', 'children'),
        Output('nb-sales-amount', 'children'),
        Output('gold-sales-amount', 'children'),
        Output('others-sales-amount', 'children')
    ],
    [
        Input('date-picker-range', 'start_date'),
        Input('date-picker-range', 'end_date'),
        Input('type-filter', 'value'),
        Input('category-dropdown', 'value'),
        Input('family-dropdown', 'value'),
        Input('material-dropdown', 'value'),
        Input('item-dropdown', 'value')
    ]
)
def update_sales_cards(start_date, end_date, type_filter, category_filter, family_filter, material_filter, item_filter):
    """
    Updates the Total Sales Amount and five additional sales amount cards based on the selected filters.
    """
    # Filter the data
    filtered_data = filter_data(start_date, end_date, type_filter, category_filter, family_filter, material_filter, item_filter)

    # Calculate Total Sales Amount
    total_sales_amount = filtered_data['Sales Amount'].sum()

    # Calculate SS Sales Amount
    ss_sales_amount = filtered_data[filtered_data['Material'] == 'SS']['Sales Amount'].sum()

    # Calculate TI Sales Amount
    ti_sales_amount = filtered_data[filtered_data['Material'] == 'TI']['Sales Amount'].sum()

    # Calculate NB Sales Amount
    nb_sales_amount = filtered_data[filtered_data['Material'] == 'NB']['Sales Amount'].sum()

    # Calculate Gold Sales Amount (materials "RG", "WG", "YG")
    gold_materials = ['RG', 'WG', 'YG']
    gold_sales_amount = filtered_data[filtered_data['Material'].isin(gold_materials)]['Sales Amount'].sum()

    # Calculate Others Sales Amount (all other materials)
    others_sales_amount = filtered_data[~filtered_data['Material'].isin(['SS', 'TI', 'NB'] + gold_materials)]['Sales Amount'].sum()

    # Format the amounts as currency
    formatted_total = f"${total_sales_amount:,.0f}"
    formatted_ss = f"${ss_sales_amount:,.0f}"
    formatted_ti = f"${ti_sales_amount:,.0f}"
    formatted_nb = f"${nb_sales_amount:,.0f}"
    formatted_gold = f"${gold_sales_amount:,.0f}"
    formatted_others = f"${others_sales_amount:,.0f}"

    return formatted_total, formatted_ss, formatted_ti, formatted_nb, formatted_gold, formatted_others

# -------------------------------
# Run the App
# -------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
