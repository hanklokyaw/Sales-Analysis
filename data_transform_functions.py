# Function to extract material
def extract_material(item):
    if '-yg-' in item.lower():
        return 'YG'
    elif '-rg-' in item.lower():
        return 'RG'
    elif '-wg-' in item.lower():
        return 'WG'
    elif '-ss-' in item.lower():
        return 'SS'
    elif '-ti-' in item.lower():
        return 'TI'
    elif '-nb-' in item.lower():
        return 'NB'
    elif '-sv-' in item.lower():
        return 'SV'
    elif '-br-' in item.lower():
        return 'BR'
    elif '-cop-' in item.lower():
        return 'CP'
    elif '-rb-' in item.lower():
        return 'RB'
    elif '-display-' in item.lower():
        return 'acrylic'
    elif '-nb/hm-' in item.lower():
        return 'NB/HM'
    elif '-nb/ti-' in item.lower():
        return 'NB/TI'
    elif '-nblti-' in item.lower():
        return 'NB/TI'
    elif '-nblhm-' in item.lower():
        return 'NB/HM'
    elif '-ti/rg-' in item.lower():
        return 'TI/RG'
    elif '-sgy-' in item.lower():
        return 'SGY'
    elif '-ssv-' in item.lower():
        return 'SSV'
    elif '-ggw-' in item.lower():
        return 'GGW'
    elif '-ggy-' in item.lower():
        return 'GGY'
    elif '-ggr-' in item.lower():
        return 'GGR'
    elif '-gysv-' in item.lower():
        return 'GYSV'
    elif '-oring-' in item.lower():
        return 'SLC'
    elif '-tle-' in item.lower():
        return 'TLE'
    elif '-tlepost-' in item.lower():
        return 'TLE'
    elif '-sv' in item.lower():
        return 'SV'
    elif '-ti' in item.lower():
        return 'TI'
    else:
        return 'Unknown'


def extract_length(item):
    if 'L7l32' in item.lower():
        return '7/32'
    elif 'L1l4' in item.lower():
        return '1/4'
    elif 'L9l32' in item.lower():
        return '9/32'
    elif 'L5l16' in item.lower():
        return '5/16'
    elif 'L11l32' in item.lower():
        return '11/32'
    elif '3l8' in item.lower():
        return '3/8'
    elif 'L7l16' in item.lower():
        return '7/16'
    elif 'L9l16' in item.lower():
        return '9/16'
    elif 'L7l8' in item.lower():
        return '7/8'
    elif 'L1 1l16' in item.lower():
        return '1 1/16'
    elif 'L1 1l8' in item.lower():
        return '1 1/8'
    elif 'L1' in item.lower():
        return '1"'
    elif 'L3l4' in item.lower():
        return '3/4'
    elif 'L5l8' in item.lower():
        return '5/8'
    elif 'L1l2' in item.lower():
        return '1/2'
    elif 'L3l16' in item.lower():
        return '3/16'
    elif 'L5l32' in item.lower():
        return '5/32'
    elif 'L-1l8' in item.lower():
        return '1/8'
    else:
        return 'Unknown'


def agg_so(so):
    # Ensure all necessary columns are of type string
    so['Document Number'] = so['Document Number'].astype(str)
    so['Item'] = so['Item'].astype(str)
    so['Product Set ID'] = so['Product Set ID'].astype(str)
    # Filter for items starting with 'ED-', 'RN-', or 'BB-' or 'SN-' or 'PL-' or 'JU-' or 'NC-' or 'OT-'
    so = so[(so["Item"].str.startswith('BB-')) |
            (so["Item"].str.startswith('ED-')) |
            (so["Item"].str.startswith('JU-')) |
            (so["Item"].str.startswith('PL-')) |
            (so["Item"].str.startswith('NC-')) |
            (so["Item"].str.startswith('OT-')) |
            (so["Item"].str.startswith('RN-')) |
            (so["Item"].str.startswith('SN-'))]
    so = so[['Item', 'Date', 'Quantity', 'Amount']]
    agg_df = so.groupby(['Item', 'Date']).agg({'Quantity': 'sum', 'Amount': 'sum'}).reset_index()
    agg_df.rename(columns={'Date': 'Sales Date', 'Quantity': 'Sales Quantity', 'Amount': 'Sales Amount'}, inplace=True)
    return agg_df
