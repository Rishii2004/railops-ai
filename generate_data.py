from datetime import date, timedelta
from pathlib import Path
import csv
import random

random.seed(42)
output = Path(__file__).parent / 'data' / 'railcars.csv'
output.parent.mkdir(parents=True, exist_ok=True)
with output.open('w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['railcar_id', 'car_type', 'last_inspection', 'inspection_interval_days', 'mileage'])
    writer.writeheader()
    for n in range(1, 101):
        writer.writerow({
            'railcar_id': f'RC{n:04d}',
            'car_type': random.choice(['Tank', 'Hopper', 'Boxcar']),
            'last_inspection': (date.today() - timedelta(days=random.randint(5, 160))).isoformat(),
            'inspection_interval_days': random.choice([30, 60, 90]),
            'mileage': random.randint(1000, 90000),
        })
print(f'Created {output} with 100 synthetic records')
