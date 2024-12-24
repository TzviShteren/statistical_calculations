import matplotlib.pyplot as plt
import numpy as np
import base64
import io


def the_deadliest_attack_types_plt(rating):
    plt.figure(figsize=(10, 6))
    plt.bar(rating['attack_type'], rating['casualty_points'], color='skyblue')
    plt.xlabel('Attack Type')
    plt.ylabel('Casualty Points')
    plt.title('Deadliest Attack Types')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plt.close()
    return img


def top_5_groups_by_casualties_endpoint_plt(group_data):
    groups = group_data['group']
    casualties = group_data['total_casualty_points']

    fig, ax = plt.subplots(figsize=(10, 6))
    y_positions = np.arange(len(groups))

    bars = ax.barh(y_positions, casualties, color=plt.cm.plasma(np.linspace(0, 1, len(groups))), edgecolor="black")

    for bar, casualty in zip(bars, casualties):
        ax.text(
            bar.get_width() + 500,
            bar.get_y() + bar.get_height() / 2,
            f'{int(casualty)}',
            va='center',
            ha='left',
            fontsize=10,
            color='black'
        )

    ax.set_yticks(y_positions)
    ax.set_yticklabels(groups, fontsize=12)
    ax.set_xlabel('Total Casualty Points', fontsize=14)
    ax.set_title('Top 5 Groups by Casualty Points', fontsize=16, fontweight='bold', pad=20)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_color('gray')
    ax.grid(axis='x', linestyle='--', alpha=0.6)

    fig.tight_layout()

    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    plt.close()

    return img


def generate_yearly_trends_graph(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data['year'], data['attack_frequency'], marker='o')
    ax.set_title('Yearly Attack Frequency Trends')
    ax.set_xlabel('Year')
    ax.set_ylabel('Attack Frequency')
    ax.grid(True)

    # Save the figure to a BytesIO buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close(fig)

    return encoded_image


def generate_monthly_trends_graph(data):
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(data['year_month'], data['attack_frequency'], marker='o')
    ax.set_title('Monthly Attack Frequency Trends')
    ax.set_xlabel('Month')
    ax.set_ylabel('Attack Frequency')
    ax.grid(True)
    plt.xticks(rotation=45)

    # Save the figure to a BytesIO buffer
    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    encoded_image = base64.b64encode(buffer.getvalue()).decode('utf-8')
    buffer.close()
    plt.close(fig)

    return encoded_image
