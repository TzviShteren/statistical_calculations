from app.db.mongo_db.connection import get_collection
import pandas as pd


def get_heatmap_data_by_time_period(time_period='all'):
    data = list(get_collection().find({}))
    df = pd.DataFrame(data)

    df['latitude'] = df['location'].apply(lambda x: x.get('latitude') if isinstance(x, dict) else None)
    df['longitude'] = df['location'].apply(lambda x: x.get('longitude') if isinstance(x, dict) else None)
    df['num_killed'] = pd.to_numeric(df['casualties'].apply(lambda x: x.get('num_killed', 0)), errors='coerce').fillna(
        0)
    df['num_wounded'] = pd.to_numeric(df['casualties'].apply(lambda x: x.get('num_wounded', 0)),
                                      errors='coerce').fillna(0)
    df['intensity'] = df['num_killed'] * 2 + df['num_wounded']

    # Drop rows without valid location data
    df = df.dropna(subset=['latitude', 'longitude'])

    # Add year and month columns
    df['year'] = df['date'].apply(lambda x: x.get('year') if isinstance(x, dict) else None)
    df['month'] = df['date'].apply(lambda x: x.get('month') if isinstance(x, dict) else None)

    # Filter by time period
    current_year = pd.Timestamp.now().year
    if time_period == 'year':
        df = df[df['year'] >= current_year - 1]
    elif time_period == '3_years':
        df = df[df['year'] >= current_year - 3]
    elif time_period == '5_years':
        df = df[df['year'] >= current_year - 5]

    # Prepare heatmap data
    heatmap_data = df[['latitude', 'longitude', 'intensity']].values.tolist()

    # Prepare data for animation if needed
    df['year_month'] = df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2)
    heatmap_with_time_data = []
    for period in sorted(df['year_month'].unique()):
        period_data = df[df['year_month'] == period][['latitude', 'longitude', 'intensity']].values.tolist()
        heatmap_with_time_data.append(period_data)

    return heatmap_data, heatmap_with_time_data
