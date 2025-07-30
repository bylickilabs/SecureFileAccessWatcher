def detect_anomalies(df):
    df['is_night'] = df['Zeit'].str.contains(' 2[0-3]| 0[0-6]')
    return df[df['is_night']]
