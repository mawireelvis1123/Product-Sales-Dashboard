import pandas as pd
import random
from faker import Faker
import numpy as np

fake = Faker()
Faker.seed(42)
random.seed(42)

# Countries across all continents
countries = [
    "United States", "Brazil", "Germany", "Nigeria", "India", "China", "Australia", "Canada", "Botswana", "France", "South Africa"
]

# Gender options
genders = ["Male", "Female"]

# Performance metrics
performance_metrics = ["scheduled_demo", "ai_request", "job_placement", "job_request"]

# Job types
job_types = ["Engineer", "Designer", "Data Analyst", "Sales Rep", "Manager"]

# Number of log entries
num_entries = 2000

data = []
for _ in range(num_entries):
    metric = random.choice(performance_metrics)

    entry = {
        "timestamp": fake.date_time_between(start_date="-90d", end_date="now"),
        "country": random.choice(countries),
        "gender": random.choice(genders),
        "performance_metric": metric,
        "job_type": random.choice(job_types) if metric in ["job_request", "job_placement"] else np.nan,
        "request_category": metric  # Optional: helps group logic if needed later
    }

    data.append(entry)

df = pd.DataFrame(data)
df.to_csv("web_logs.csv", index=False)
print("✅ Synthetic web log data generated and saved as 'web_logs.csv'")
