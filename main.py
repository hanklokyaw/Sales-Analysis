import pandas as pd
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.graph_objs as go
from dash import dash_table
from get_latest_file import find_latest_report

download_folder_path = "C:/Users/hank.aungkyaw/Downloads"
SO_prefix = "SalesOrder1yearHKResults"
INVOICE_prefix = "InvoiceDetailoneyearHKResults"

so_filename = find_latest_report(download_folder_path, SO_prefix)
invoice_filename = find_latest_report(download_folder_path, INVOICE_prefix)

# Ensure filenames are found
if so_filename is None:
    raise FileNotFoundError(f"No file found with prefix {SO_prefix} in {download_folder_path}")
if invoice_filename is None:
    raise FileNotFoundError(f"No file found with prefix {INVOICE_prefix} in {download_folder_path}")

so_filepath = f"{download_folder_path}/{so_filename}"
invoice_filepath = f"{download_folder_path}/{invoice_filename}"

# Read sales order on gems
so = pd.read_csv(so_filepath)
invoice = pd.read_csv(invoice_filepath)

# Print out df to check if they are loading properly
print(so)
print(invoice)

#
# # Function to extract material
# def extract_material(item):
#     if '-yg-' in item.lower():
#         return 'YG'
#     elif '-rg-' in item.lower():
#         return 'RG'
#     elif '-wg-' in item.lower():
#         return 'WG'
#     elif '-ss-' in item.lower():
#         return 'SS'
#     elif '-ti-' in item.lower():
#         return 'TI'
#     elif '-nb-' in item.lower():
#         return 'NB'
#     elif '-sv-' in item.lower():
#         return 'SV'
#     elif '-br-' in item.lower():
#         return 'BR'
#     elif '-cop-' in item.lower():
#         return 'CP'
#     elif '-rb-' in item.lower():
#         return 'RB'
#     elif '-display-' in item.lower():
#         return 'acrylic'
#     elif '-nb/hm-' in item.lower():
#         return 'NB/HM'
#     elif '-nb/ti-' in item.lower():
#         return 'NB/TI'
#     elif '-nblti-' in item.lower():
#         return 'NB/TI'
#     elif '-nblhm-' in item.lower():
#         return 'NB/HM'
#     elif '-ti/rg-' in item.lower():
#         return 'TI/RG'
#     elif '-sgy-' in item.lower():
#         return 'SGY'
#     elif '-ssv-' in item.lower():
#         return 'SSV'
#     elif '-ggw-' in item.lower():
#         return 'GGW'
#     elif '-ggy-' in item.lower():
#         return 'GGY'
#     elif '-ggr-' in item.lower():
#         return 'GGR'
#     elif '-gysv-' in item.lower():
#         return 'GYSV'
#     elif '-oring-' in item.lower():
#         return 'SLC'
#     elif '-tle-' in item.lower():
#         return 'TLE'
#     elif '-tlepost-' in item.lower():
#         return 'TLE'
#     elif '-sv' in item.lower():
#         return 'SV'
#     elif '-ti' in item.lower():
#         return 'TI'
#     else:
#         return 'Unknown'
#
#
# # Ensure all necessary columns are of type string
# so['Document Number'] = so['Document Number'].astype(str)
# so['Item'] = so['Item'].astype(str)
# so['Product Set ID'] = so['Product Set ID'].astype(str)
# so['Unique_ID'] = so['Document Number'] + '+' + so['Item'] + so['Product Set ID']
# # Filter for items starting with 'ED-', 'RN-', or 'BB-' or 'SN-' or 'PL-' or 'JU-' or 'NC-' or 'OT-'
# so = so[(so["Item"].str.startswith('BB-')) |
#         (so["Item"].str.startswith('ED-')) |
#         (so["Item"].str.startswith('JU-')) |
#         (so["Item"].str.startswith('PL-')) |
#         (so["Item"].str.startswith('NC-')) |
#         (so["Item"].str.startswith('OT-')) |
#         (so["Item"].str.startswith('RN-')) |
#         (so["Item"].str.startswith('SN-'))]
# so = so[['Unique_ID', 'Item', 'Date', 'Quantity']]
# agg_so = so.groupby(['Unique_ID', 'Item']).agg({'Date': 'max', 'Quantity': 'sum'}).reset_index()
# agg_so.rename(columns={'Date': 'Sales Date', 'Quantity': 'Sales Quantity'}, inplace=True)
# # agg_so.to_csv("so_test.csv")
#
# # Filter out rows with NaN values in 'Created From' column
# invoice = invoice.dropna(subset=['Created From'])
#
# # Filter for rows where 'Created From' starts with 'Sales Order #'
# invoice = invoice[invoice['Created From'].str.startswith('Sales Order #')]
#
# # Remove the 'Sales Order #' prefix from 'Created From' column
# invoice['Created From'] = invoice['Created From'].str.replace('Sales Order #', '')
#
# # Ensure all necessary columns are of type string
# invoice['Created From'] = invoice['Created From'].astype(str)
# invoice['Item'] = invoice['Item'].astype(str)
# invoice['Product Set ID'] = invoice['Product Set ID'].astype(str)
#
# # Create 'Unique_ID' column
# invoice['Unique_ID'] = invoice['Created From'] + '+' + invoice['Item'] + invoice['Product Set ID']
#
# # Filter for items starting with specific prefixes
# invoice = invoice[(invoice["Item"].str.startswith('BB-')) |
#                   (invoice["Item"].str.startswith('ED-')) |
#                   (invoice["Item"].str.startswith('JU-')) |
#                   (invoice["Item"].str.startswith('PL-')) |
#                   (invoice["Item"].str.startswith('NC-')) |
#                   (invoice["Item"].str.startswith('OT-')) |
#                   (invoice["Item"].str.startswith('RN-')) |
#                   (invoice["Item"].str.startswith('SN-'))]
#
# # Select relevant columns
# invoice = invoice[['Unique_ID', 'Date', 'Quantity']]
# agg_invoice = invoice.groupby(['Unique_ID']).agg({'Date': 'max', 'Quantity': 'sum'}).reset_index()
# agg_invoice.rename(columns={'Date': 'Invoice Date', 'Quantity': 'Invoice Quantity'}, inplace=True)
# # agg_invoice.to_csv("invoice_test.csv")
#
# print(so)
# print(invoice)
#
# merged_df = pd.merge(agg_so, agg_invoice, on='Unique_ID', how='left').reset_index()
# # merged_df.to_csv("merged_test.csv")
#
# # # Debug print after merge
# # print("Merged DataFrame:")
# # print(merged_df.head())
# # print("Merged DataFrame Columns:", merged_df.columns)
# #
# # # Check for the existence of 'Invoice Date' and 'Sales Date' columns
# # if 'Invoice Date' not in merged_df.columns:
# #     raise KeyError("'Invoice Date' column not found in merged DataFrame")
# # if 'Sales Date' not in merged_df.columns:
# #     raise KeyError("'Sales Date' column not found in merged DataFrame")
# #
# # # Check for null values in date columns
# # print("Null values in 'Sales Date':", merged_df['Sales Date'].isnull().sum())
# # # print("Null values in 'Invoice Date':", merged_df['Invoice Date'].isnull().sum())
# #
# # # Check the data types of the date columns before conversion
# # print("Data types before conversion:")
# # print(merged_df[['Sales Date', 'Invoice Date']].dtypes)
#
# # Convert date columns to datetime
# merged_df['Sales Date'] = pd.to_datetime(merged_df['Sales Date'], errors='coerce')
# merged_df['Invoice Date'] = pd.to_datetime(merged_df['Invoice Date'], errors='coerce')
# #
# # # Check the data types of the date columns after conversion
# # print("Data types after conversion:")
# # print(merged_df[['Sales Date', 'Invoice Date']].dtypes)
# #
# # # Check for null values in date columns after conversion
# # print("Null values in 'Sales Date' after conversion:", merged_df['Sales Date'].isnull().sum())
# # print("Null values in 'Invoice Date' after conversion:", merged_df['Invoice Date'].isnull().sum())
#
# # Calculate the date difference in days
# merged_df['Date Difference'] = (merged_df['Invoice Date'] - merged_df['Sales Date']).dt.days
#
# # print("Merged DataFrame with Date Difference:")
# # print(merged_df.head())
# print(merged_df.shape)
# merged_df = merged_df[~merged_df['Invoice Date'].isna()]
# print(merged_df.shape)
#
# merged_df['Category'] = merged_df['Item'].str.split('-').str[0]
# print(merged_df['Category'].unique())
#
# merged_df['Family'] = merged_df['Item'].str.split('-').str[1]
# print(merged_df['Family'].unique())
#
# merged_df['Material'] = merged_df['Item'].apply(extract_material)
# print(merged_df['Material'].unique())
#
# merged_df = merged_df[merged_df['Material'] != 'Unknown']
#
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
# # Initialize Dash app
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
#
# # Define dropdown options for filtering
# category_option = [{'label': name, 'value': name} for name in merged_df['Category'].unique()]
# family_option = [{'label': name, 'value': name} for name in merged_df['Family'].unique()]
# material_option = [{'label': name, 'value': name} for name in merged_df['Material'].unique()]
# item_option = [{'label': name, 'value': name} for name in merged_df['Item'].unique()]
#
# app.layout = dbc.Container([
#     html.H1("Lead Time Dashboard", style={'marginBottom': '40px'}),
#     dcc.Input(id='dummy-input', style={'display': 'none'}),
#
#     # Dropdowns and radio buttons
#     dbc.Row([
#         dbc.Col([
#             html.H3("Lead Time Analysis", style={'marginTop': '40px'}),
#             html.Div([
#                 # First row of dropdowns
#                 dbc.Row([
#                     dbc.Col(
#                         dcc.Dropdown(
#                             id='item-dropdown',
#                             options=item_option,
#                             multi=True,
#                             placeholder='Filter by Item',
#                         ), width=6
#                     ),
#                     dbc.Col(
#                         dcc.Dropdown(
#                             id='category-dropdown',
#                             options=category_option,
#                             multi=True,
#                             placeholder='Filter by Category',
#                         ), width=6
#                     )
#                 ], style={'margin-bottom': '5px'}),
#                 # Second row of dropdowns
#                 dbc.Row([
#                     dbc.Col(
#                         dcc.Dropdown(
#                             id='family-dropdown',
#                             options=family_option,
#                             multi=True,
#                             placeholder='Filter by Product Family',
#                         ), width=6
#                     ),
#                     dbc.Col(
#                         dcc.Dropdown(
#                             id='material-dropdown',
#                             options=material_option,
#                             multi=True,
#                             placeholder='Filter by Material',
#                         ), width=6
#                     )
#                 ]),
#                 # Radio buttons in the same line
#                 dbc.Row([
#                     dbc.Col(
#                         html.Div([
#                             html.Label('Sort Order'),
#                             dcc.RadioItems(
#                                 id='sort-order-radio',
#                                 options=[
#                                     {'label': 'Ascending', 'value': 'asc'},
#                                     {'label': 'Descending', 'value': 'desc'}
#                                 ],
#                                 value='desc',
#                                 labelStyle={'display': 'inline-block', 'marginRight': '10px'}
#                             )
#                         ], style={'paddingTop': '20px'}),
#                         width=12
#                     )
#                 ])
#             ], style={'paddingTop': '5px'})
#         ])
#     ]),
#     # Time series plot
#     dbc.Row([
#         dbc.Col([
#             dcc.Graph(id='time-series-plot')
#         ], width=12)
#     ]),
#     dbc.Row([
#         dbc.Col([dcc.Graph(id='item-bar-plot')], width=8),
#         dbc.Col([dcc.Graph(id='category-bar-plot')], width=4),
#     ]),
#     dbc.Row([
#         dbc.Col([dcc.Graph(id='family-bar-plot')], width=8),
#         dbc.Col([dcc.Graph(id='material-bar-plot')], width=4),
#     ]),
#     dash_table.DataTable(
#         id='datatable',
#         columns=[{'name': col, 'id': col} for col in default_df.columns],
#         data=default_df.to_dict('records'),
#         fixed_rows={'headers': True},
#         style_table={'height': '500px', 'paddingTop': '5px'},
#         style_cell={'textAlign': 'left', 'minWidth': '30px', 'maxWidth': '150px', 'whiteSpace': 'normal'},
#         style_header={
#             'backgroundColor': '#D3D3D3',  # Set a slightly darker grey color for the header background
#             'fontWeight': 'bold',
#             'border': '1px solid black'  # Define border properties for the header
#         },
#         style_data={
#             'border': '1px solid black'  # Define border properties for the data cells
#         }
#     )
# ], fluid=True)
#
#
# # Callbacks to update the bar plots based on filters
# @app.callback(
#     [
#         Output('item-bar-plot', 'figure'),
#         Output('category-bar-plot', 'figure'),
#         Output('family-bar-plot', 'figure'),
#         Output('material-bar-plot', 'figure')
#     ],
#     [
#         Input('category-dropdown', 'value'),
#         Input('family-dropdown', 'value'),
#         Input('material-dropdown', 'value'),
#         Input('item-dropdown', 'value'),
#         Input('sort-order-radio', 'value')
#     ]
# )
# def update_bar_plots(category_filter, family_filter, material_filter, item_filter, sort_order):
#     filtered_data = merged_df.copy()
#
#     if category_filter:
#         filtered_data = filtered_data[filtered_data['Category'].isin(category_filter)]
#     if family_filter:
#         filtered_data = filtered_data[filtered_data['Family'].isin(family_filter)]
#     if material_filter:
#         filtered_data = filtered_data[filtered_data['Material'].isin(material_filter)]
#     if item_filter:
#         filtered_data = filtered_data[filtered_data['Item'].isin(item_filter)]
#
#     # Item bar plot
#     item_data = filtered_data.groupby('Item')['Date Difference'].mean().reset_index()
#     item_data.columns = ['Item', 'Average Lead Time']
#     item_data = item_data.sort_values(by='Average Lead Time', ascending=(sort_order == 'asc')).head(50)
#
#     item_fig = go.Figure(data=[
#         go.Bar(x=item_data['Item'], y=item_data['Average Lead Time'])
#     ])
#     item_fig.update_layout(title='Average Lead Time by Item', xaxis_title='Item', yaxis_title='Average Lead Time')
#
#     # Category bar plot
#     category_data = filtered_data.groupby('Category')['Date Difference'].mean().reset_index()
#     category_data.columns = ['Category', 'Average Lead Time']
#     category_data = category_data.sort_values(by='Average Lead Time', ascending=(sort_order == 'asc'))
#
#     category_fig = go.Figure(data=[
#         go.Bar(x=category_data['Category'], y=category_data['Average Lead Time'])
#     ])
#     category_fig.update_layout(title='Average Lead Time by Category', xaxis_title='Category',
#                                yaxis_title='Average Lead Time')
#
#     # Family bar plot
#     family_data = filtered_data.groupby('Family')['Date Difference'].mean().reset_index()
#     family_data.columns = ['Family', 'Average Lead Time']
#     family_data = family_data.sort_values(by='Average Lead Time', ascending=(sort_order == 'asc')).head(50)
#
#     family_fig = go.Figure(data=[
#         go.Bar(x=family_data['Family'], y=family_data['Average Lead Time'])
#     ])
#     family_fig.update_layout(title='Average Lead Time by Family', xaxis_title='Family', yaxis_title='Average Lead Time')
#
#     # Material bar plot
#     material_data = filtered_data.groupby('Material')['Date Difference'].mean().reset_index()
#     material_data.columns = ['Material', 'Average Lead Time']
#     material_data = material_data.sort_values(by='Average Lead Time', ascending=(sort_order == 'asc'))
#
#     material_fig = go.Figure(data=[
#         go.Bar(x=material_data['Material'], y=material_data['Average Lead Time'])
#     ])
#     material_fig.update_layout(title='Average Lead Time by Material', xaxis_title='Material',
#                                yaxis_title='Average Lead Time')
#
#     return item_fig, category_fig, family_fig, material_fig
#
#
# # Callbacks to update DataTable based on filters
# @app.callback(
#     Output('datatable', 'data'),
#     [
#         Input('category-dropdown', 'value'),
#         Input('family-dropdown', 'value'),
#         Input('material-dropdown', 'value'),
#         Input('item-dropdown', 'value')
#     ]
# )
# # def update_datatable(selected_names, min_available, min_to_order):
# def update_datatable(category_filter, family_filter, material_filter, item_filter):
#     filtered_data = default_df.copy()
#     filtered_data.rename(columns={'Date Difference': 'Lead Time'}, inplace=True)
#     filtered_data['Sales Date'] = filtered_data['Sales Date'].dt.strftime('%m/%d/%Y')
#     filtered_data['Invoice Date'] = filtered_data['Invoice Date'].dt.strftime('%m/%d/%Y')
#
#     if category_filter:
#         filtered_data = filtered_data[filtered_data['Category'].isin(category_filter)]
#     if family_filter:
#         filtered_data = filtered_data[filtered_data['Family'].isin(family_filter)]
#     if material_filter:
#         filtered_data = filtered_data[filtered_data['Material'].isin(material_filter)]
#     if item_filter:
#         filtered_data = filtered_data[filtered_data['Item'].isin(item_filter)]
#
#     filtered_data = filtered_data.sort_values(by='Invoice Date', ascending=True)
#
#     return filtered_data.to_dict('records')
#
#
# # Callback to update the time series plot based on filters
# @app.callback(
#     Output('time-series-plot', 'figure'),
#     [
#         Input('category-dropdown', 'value'),
#         Input('family-dropdown', 'value'),
#         Input('material-dropdown', 'value'),
#         Input('item-dropdown', 'value')
#     ]
# )
# def update_time_series_plot(category_filter, family_filter, material_filter, item_filter):
#     filtered_data = merged_df.copy()
#
#     if category_filter:
#         filtered_data = filtered_data[filtered_data['Category'].isin(category_filter)]
#     if family_filter:
#         filtered_data = filtered_data[filtered_data['Family'].isin(family_filter)]
#     if material_filter:
#         filtered_data = filtered_data[filtered_data['Material'].isin(material_filter)]
#     if item_filter:
#         filtered_data = filtered_data[filtered_data['Item'].isin(item_filter)]
#
#     # Group by Invoice Date and calculate the average Date Difference
#     time_series_data = filtered_data.groupby('Invoice Date')['Date Difference'].mean().reset_index()
#
#     time_series_fig = go.Figure(data=[
#         go.Scatter(x=time_series_data['Invoice Date'], y=time_series_data['Date Difference'], mode='lines+markers')
#     ])
#     time_series_fig.update_layout(title='Average Lead Time Over Time', xaxis_title='Invoice Date',
#                                   yaxis_title='Average Lead Time')
#
#     return time_series_fig
#
#
# # Run the app
# if __name__ == '__main__':
#     app.run_server(debug=True)