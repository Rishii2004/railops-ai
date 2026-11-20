import pandas as pd

REQUIRED_COLUMNS = ['railcar_id', 'last_inspection', 'inspection_interval_days']


def analyze_maintenance(data: pd.DataFrame, today=None) -> pd.DataFrame:
    missing = [col for col in REQUIRED_COLUMNS if col not in data.columns]
    if missing:
        raise ValueError(f'Missing required columns: {", ".join(missing)}')
    df = data.copy()
    if df.empty:
        raise ValueError('CSV contains no railcar records.')
    if df['railcar_id'].isna().any() or df['railcar_id'].astype(str).str.strip().eq('').any():
        raise ValueError('Railcar IDs cannot be blank.')
    if df['railcar_id'].duplicated().any():
        raise ValueError('Duplicate railcar IDs found.')
    df['last_inspection'] = pd.to_datetime(df['last_inspection'], errors='coerce')
    df['inspection_interval_days'] = pd.to_numeric(df['inspection_interval_days'], errors='coerce')
    if df['last_inspection'].isna().any():
        raise ValueError('Invalid or missing inspection dates found.')
    if df['inspection_interval_days'].isna().any() or (df['inspection_interval_days'] <= 0).any():
        raise ValueError('Inspection intervals must be positive numbers.')
    reference = pd.Timestamp(today).normalize() if today is not None else pd.Timestamp.today().normalize()
    if (df['last_inspection'] > reference).any():
        raise ValueError('Last inspection dates cannot be in the future.')
    df['next_inspection'] = df['last_inspection'] + pd.to_timedelta(df['inspection_interval_days'], unit='D')
    df['days_remaining'] = (df['next_inspection'] - reference).dt.days
    df['inspection_status'] = 'On Track'
    df.loc[df['days_remaining'].between(0, 14), 'inspection_status'] = 'Due Soon'
    df.loc[df['days_remaining'] < 0, 'inspection_status'] = 'Overdue'
    return df.sort_values(['days_remaining', 'railcar_id']).reset_index(drop=True)
