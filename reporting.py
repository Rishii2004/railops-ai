"""Deterministic, auditable inspection scheduling report."""
import pandas as pd


def create_priority_report(df: pd.DataFrame) -> str:
    counts = df['inspection_status'].value_counts()
    overdue = df.loc[df['inspection_status'].eq('Overdue')].sort_values('days_remaining')
    lines = [
        'RAILOPS AI — SYNTHETIC INSPECTION SCHEDULING REPORT',
        'Demo only. These flags do not establish mechanical safety.',
        f'Total records: {len(df)}',
        f"Overdue: {int(counts.get('Overdue', 0))}",
        f"Due within 14 days: {int(counts.get('Due Soon', 0))}",
        f"On track: {int(counts.get('On Track', 0))}",
        '', 'MOST OVERDUE RECORDS (up to 10):',
    ]
    if overdue.empty:
        lines.append('None')
    else:
        for row in overdue.head(10).itertuples():
            lines.append(f'{row.railcar_id}: {-int(row.days_remaining)} days overdue; scheduled {row.next_inspection:%Y-%m-%d}')
    lines.extend(['', 'Recommended next step: have a qualified team review scheduling records.'])
    return '\n'.join(lines) + '\n'
