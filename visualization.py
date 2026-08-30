import matplotlib.pyplot as plt


def traffic_chart(df):
    summary = df.groupby('Road_traffic_density')['Time_taken (min)'].mean().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    summary.plot(kind='bar', ax=ax)
    ax.set_title('Average Delivery Time by Traffic Density')
    ax.set_xlabel('Road Traffic Density')
    ax.set_ylabel('Average Delivery Time (minutes)')
    ax.tick_params(axis='x', rotation=0)
    fig.tight_layout()
    return fig


def distance_time_chart(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(df['distance_km'], df['Time_taken (min)'], alpha=0.35, s=12)
    ax.set_title('Delivery Distance vs. Delivery Time')
    ax.set_xlabel('Delivery Distance (km)')
    ax.set_ylabel('Delivery Time (minutes)')
    fig.tight_layout()
    return fig
