import pandas as pd


def consolidate_sex(value):

    if 'female' in value.lower():
        return 'female'

    elif ' male' in value.lower():
        return 'male'

    else:
        return 'unknown'


def df_cleaner(df_orig):

    df = df_orig
    df.drop_duplicates('Animal ID', keep=False, inplace=True)

    # Original name field had over 30000 NaN. I assumed these are important
    # and filled with no_name string

    df['Name'] = df['Name'].fillna('no_name')
    df.drop('Outcome Subtype', axis=1, inplace=True)
    df.dropna(inplace=True)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df.drop("MonthYear", axis=1, inplace=True)
    df['Date of Birth'] = pd.to_datetime(df['Date of Birth'])
    df['sex'] = df['Sex upon Outcome'].map(consolidate_sex)

    return df
