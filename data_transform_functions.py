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
    so = so[['Item', 'Date', 'Quantity']]
    agg_df = so.groupby(['Item']).agg({'Date': 'max', 'Quantity': 'sum'}).reset_index()
    agg_df.rename(columns={'Date': 'Sales Date', 'Quantity': 'Sales Quantity'}, inplace=True)
    return agg_df
