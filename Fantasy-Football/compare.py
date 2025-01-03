import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

data = {
    'Year': [2021, 2022, 2023],
    'WinPercentage': [42, 42, 35],  # This is Metric 1 (Percentage)
    'PointsFor': [1704.52, 1666.88, 1639.00],  # This is Metric 2
    'PointsAgainst': [1781.24, 1640.96, 1708.00],  # This is Metric 3
}

df = pd.DataFrame(data)

fig, ax1 = plt.subplots(figsize=(14, 8))

ax1.plot(df['Year'], df['PointsFor'], marker='o', label='PointsFor', color='green')
ax1.plot(df['Year'], df['PointsAgainst'], marker='o', label='PointsAgainst', color='red')

ax1.set_xlabel('Year')
ax1.set_ylabel('PointsFor / PointsAgainst', color='black')
ax1.tick_params(axis='y', labelcolor='black')

ax2 = ax1.twinx()
ax2.plot(df['Year'], df['WinPercentage'], marker='o', label='Win Percentage', color='blue', linestyle='--')
ax2.set_ylabel('Win Percentage (%)', color='blue')
ax2.tick_params(axis='y', labelcolor='blue')

fig.legend(loc="upper left", bbox_to_anchor=(0.1,0.9))
plt.title('MyWifePhil Metrics Over 3 Years')
ax1.grid(True)
plt.tight_layout()
plt.show()