import pandas as pd

def check_missing_datetimes(df):
    # Assuming df is already sorted by 'Date/time', we don't need to explicitly find start and end datetimes.
    full_datetime_range = pd.date_range(start=df['Date/time'].iloc[0], end=df['Date/time'].iloc[-1], freq='10T')
    # Create a DataFrame with the full datetime range
    full_datetime_df = pd.DataFrame(full_datetime_range, columns=['Date/time'])
    # Merge full datetime range with the actual data
    merged_df = full_datetime_df.merge(df[['Date/time']], on='Date/time', how='left', indicator=True)
    # Filter out missing datetimes
    missing_datetimes_df = merged_df[merged_df['_merge'] == 'left_only']
    # Add a message column
    missing_datetimes_df['Message'] = 'Datetime is missing'
    return missing_datetimes_df[['Date/time', 'Message']]

# Load data
file_path = input("Enter the file path: ")
df = pd.read_csv(file_path, delimiter='\t', header=None, skiprows=1, names=['Date/time','Anemometer 37m North;wind_speed;Avg','Anemometer 37m South;wind_speed;Avg',
                                                                'Temperature;temperature;Avg','Barometer @3.0m;air_pressure;Avg','A1;Avg','A2;Avg','C1;Avg','C2;Avg','D1;Avg','V;Avg','I;Avg','T;Avg'
])

# Print the first few rows of the DataFrame to diagnose the issue
print(df.head())

# Convert 'Date/time' column to datetime format
df['Date/time'] = pd.to_datetime(df['Date/time'], errors='coerce')

# Check for missing datetimes
missing_datetimes = check_missing_datetimes(df)
print(missing_datetimes)

# Drop rows containing NaN values
nan_count = df.isna().sum()
print(nan_count)
data = df.dropna()
print(data.count())
print(data)
