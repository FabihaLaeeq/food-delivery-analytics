import pandas as pd
import numpy as np

TARGET_TIME = 'Time_taken (min)'


def load_data(file_path: str) -> pd.DataFrame:
    return pd.read_csv(file_path)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    data = df.copy()

    # Remove exact duplicate rows.
    data = data.drop_duplicates().copy()

    # Convert numeric columns explicitly where relevant.
    numeric_cols = [
        'Delivery_person_Age', 'Delivery_person_Ratings',
        'Vehicle_condition', 'multiple_deliveries', TARGET_TIME, 'distance_km'
    ]
    for col in numeric_cols:
        data[col] = pd.to_numeric(data[col], errors='coerce')

    # Age and rating have missing values. Median imputation keeps all delivery
    # records available for the required summary metrics.
    for col in ['Delivery_person_Age', 'Delivery_person_Ratings']:
        data[col] = data[col].fillna(data[col].median())

    # Time_Orderd is not needed for the required analysis, so its missing
    # values are retained as missing rather than inventing a time.

    # Invalid target values would make speed meaningless; remove them.
    data = data[data[TARGET_TIME] > 0]
    data = data[data['distance_km'] > 0]

    # Numeric delivery speed in km/h, derived from distance and delivery time.
    data['speed_kmh'] = data['distance_km'] / (data[TARGET_TIME] / 60)

    return data.reset_index(drop=True)


def dataset_info(df: pd.DataFrame) -> dict:
    return {
        'rows': len(df),
        'columns': len(df.columns),
        'column_names': df.columns.tolist(),
        'dtypes': df.dtypes.astype(str).to_dict(),
        'missing_values': df.isna().sum().to_dict(),
        'duplicate_records': int(df.duplicated().sum()),
    }


def basic_analysis(df: pd.DataFrame) -> dict:
    return {
        'total_deliveries': int(len(df)),
        'average_delivery_time': float(df[TARGET_TIME].mean()),
        'minimum_delivery_time': int(df[TARGET_TIME].min()),
        'maximum_delivery_time': int(df[TARGET_TIME].max()),
        'average_delivery_distance': float(df['distance_km'].mean()),
        'average_delivery_speed': float(df['speed_kmh'].mean()),
        'average_delivery_person_rating': float(df['Delivery_person_Ratings'].mean()),
        'average_delivery_person_age': float(df['Delivery_person_Age'].mean()),
    }


def competition_answers(df: pd.DataFrame) -> dict:
    traffic = (
        df.groupby('Road_traffic_density')[TARGET_TIME]
        .mean()
        .sort_values(ascending=False)
    )

    # Pearson correlation supports the distance/time relationship conclusion.
    correlation = float(df['distance_km'].corr(df[TARGET_TIME]))

    weather_traffic = (
        df.groupby(['Weather_conditions', 'Road_traffic_density'])[TARGET_TIME]
        .mean()
        .sort_values(ascending=False)
    )

    return {
        'q1_traffic': traffic,
        'q2_correlation': correlation,
        'q3_weather_traffic': weather_traffic,
    }


def business_insights(df: pd.DataFrame, answers: dict) -> list[str]:
    traffic = answers['q1_traffic']
    weather_traffic = answers['q3_weather_traffic']

    worst_traffic = traffic.index[0]
    worst_traffic_time = traffic.iloc[0]
    best_traffic = traffic.index[-1]
    best_traffic_time = traffic.iloc[-1]
    top_weather, top_density = weather_traffic.index[0]
    top_combo_time = weather_traffic.iloc[0]

    return [
        f"{worst_traffic} traffic has the highest average delivery time ({worst_traffic_time:.2f} min), while {best_traffic} traffic has the lowest ({best_traffic_time:.2f} min).",
        f"Delivery distance has a positive relationship with delivery time (Pearson correlation = {answers['q2_correlation']:.3f}), so longer routes generally take longer to complete.",
        f"The slowest weather + traffic combination is {top_weather} weather with {top_density} traffic ({top_combo_time:.2f} min on average), indicating combined conditions can create major delays.",
    ]
