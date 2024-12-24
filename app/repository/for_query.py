from app.db.mongo_db.connection import get_collection
import pandas as pd


# Question number 1
def deadliest_attack_types_rating(top_5: bool = False):
    data = list(get_collection().find({}))

    df = pd.DataFrame(data)

    df['num_killed'] = pd.to_numeric(df['casualties'].apply(lambda x: x.get('num_killed', 0)), errors='coerce').fillna(
        0)
    df['num_wounded'] = pd.to_numeric(df['casualties'].apply(lambda x: x.get('num_wounded', 0)),
                                      errors='coerce').fillna(0)

    df['casualty_points'] = (df['num_killed'] * 2) + df['num_wounded']

    attack_type_summary = df.groupby('attack_type')['casualty_points'].sum().reset_index()

    attack_type_summary = attack_type_summary.sort_values(by='casualty_points', ascending=False)

    if top_5:
        attack_type_summary = attack_type_summary.head(5)

    return attack_type_summary


# Question number 2
def casualties_with_event_coords(top_5: bool = False):
    data = list(get_collection().find({}))
    df = pd.DataFrame(data)

    df['region'] = df['location'].apply(lambda x: x.get('region') if isinstance(x, dict) else None)
    df['latitude'] = df['location'].apply(lambda x: x.get('latitude') if isinstance(x, dict) else None)
    df['longitude'] = df['location'].apply(lambda x: x.get('longitude') if isinstance(x, dict) else None)

    df['num_killed'] = pd.to_numeric(df['casualties'].apply(lambda x: x.get('num_killed', 0)), errors='coerce').fillna(0)
    df['num_wounded'] = pd.to_numeric(df['casualties'].apply(lambda x: x.get('num_wounded', 0)), errors='coerce').fillna(0)

    df['casualty_points'] = (df['num_killed'] * 2) + df['num_wounded']

    df = df.dropna(subset=['latitude', 'longitude'])

    region_summary = df.groupby('region').agg(
        total_events=('casualty_points', 'count'),
        total_casualty_points=('casualty_points', 'sum'),
        latitude=('latitude', 'first'),
        longitude=('longitude', 'first')
    ).reset_index()

    region_summary['average_casualty_points'] = region_summary['total_casualty_points'] / region_summary['total_events']
    region_summary = region_summary.sort_values(by='average_casualty_points', ascending=False)

    if top_5:
        region_summary = region_summary.head(5)

    return region_summary


# Question number 3
def top_5_groups_by_casualties():
    data = list(get_collection().find({}))
    df = pd.DataFrame(data)

    # Filter out unknown groups
    df = df[df['group'] != "Unknown"]

    # Extract and clean data
    df['num_killed'] = pd.to_numeric(df['casualties'].apply(lambda x: x.get('num_killed', 0)),
                                     errors='coerce').fillna(0)
    df['num_wounded'] = pd.to_numeric(df['casualties'].apply(lambda x: x.get('num_wounded', 0)),
                                      errors='coerce').fillna(0)

    df['casualty_points'] = (df['num_killed'] * 2) + df['num_wounded']

    # Group by group and calculate total casualty points
    group_summary = df.groupby('group').agg(
        total_casualty_points=('casualty_points', 'sum')
    ).reset_index()

    # Sort and get top 5 groups
    group_summary = group_summary.sort_values(by='total_casualty_points', ascending=False).head(5)

    return group_summary


# Question number 5
def attack_frequency_trends(year_filter=None):
    data = list(get_collection().find({}))

    # Convert to DataFrame
    df = pd.DataFrame(data)

    # Extract year and month from the date field
    df['year'] = df['date'].apply(lambda x: x.get('year') if isinstance(x, dict) else None)
    df['month'] = df['date'].apply(lambda x: x.get('month') if isinstance(x, dict) else None)

    # Filter out rows with missing year or month
    df = df.dropna(subset=['year', 'month'])

    # Group by year and count unique events for yearly trends
    yearly_trends = df.groupby('year').size().reset_index(name='attack_frequency')

    # Filter data for monthly trends if year_filter is provided
    if year_filter:
        df = df[df['year'] == year_filter]

    # Group by year and month to get monthly trends
    df['year_month'] = df['year'].astype(str) + '-' + df['month'].astype(str).str.zfill(2)
    monthly_trends = df.groupby('year_month').size().reset_index(name='attack_frequency')

    return {
        "yearly_trends": yearly_trends,
        "monthly_trends": monthly_trends
    }



# Question number 10
def events_vs_casualties_correlation(region: str = None):
    data = list(get_collection().find({}))
    df = pd.DataFrame(data)

    # Extract region, casualties, and location data
    df['region'] = df['location'].apply(lambda x: x.get('region') if isinstance(x, dict) else None)
    df['latitude'] = df['location'].apply(lambda x: x.get('latitude') if isinstance(x, dict) else None)
    df['longitude'] = df['location'].apply(lambda x: x.get('longitude') if isinstance(x, dict) else None)

    # Filter out rows with missing latitude or longitude
    df = df.dropna(subset=['latitude', 'longitude'])

    # Convert casualties to numeric
    df['num_killed'] = pd.to_numeric(df['casualties'].apply(lambda x: x.get('num_killed', 0)), errors='coerce').fillna(0)
    df['num_wounded'] = pd.to_numeric(df['casualties'].apply(lambda x: x.get('num_wounded', 0)), errors='coerce').fillna(0)

    # Calculate casualty points (weighted sum)
    df['casualty_points'] = (df['num_killed'] * 2) + df['num_wounded']

    # Filter by region if specified
    if region:
        df = df[df['region'] == region]

        if df.empty:
            return {"error": f"No data available for region: {region}"}

        correlation = df['num_killed'].corr(df['num_wounded'])
        return {"region": region, "correlation": correlation, "data": df.to_dict(orient='records')}

    # Calculate correlation for all regions
    correlations = []
    for region_name, group in df.groupby('region'):
        correlation = group['num_killed'].corr(group['num_wounded'])
        correlations.append({"region": region_name, "correlation": correlation})

    return {"correlations": correlations, "data": df.to_dict(orient='records')}
