import requests
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline

handle = "Jaardo"  # Your Codeforces handle

url = f"https://codeforces.com/api/user.rating?handle={handle}"
response = requests.get(url)
data = response.json()

if data["status"] == "OK":
    contests = data["result"]
    x = np.array([i + 1 for i in range(len(contests))])
    y = np.array([contest["newRating"] for contest in contests])
    labels = [contest["contestName"] for contest in contests]

    # Smooth the curve using spline interpolation
    x_smooth = np.linspace(x.min(), x.max(), 300)
    spline = make_interp_spline(x, y, k=3)  # cubic spline
    y_smooth = spline(x_smooth)

    plt.figure(figsize=(12, 5))
    
    # Plot smooth curve
    plt.plot(x_smooth, y_smooth, color='#1f77b4', linewidth=3, alpha=0.9)
    
    # Plot original points
    plt.scatter(x, y, color='#1f77b4', edgecolor='white', linewidth=1.5, s=70, zorder=5)
    
    # Gradient fill under the curve
    plt.fill_between(x_smooth, y_smooth, y.min() - 100, color='#1f77b4', alpha=0.2)
    
    plt.title(f"Codeforces Rating Graph for {handle}", fontsize=16, weight='bold')
    plt.xlabel("Contest Number", fontsize=13)
    plt.ylabel("Rating", fontsize=13)
    
    # Improve grid style
    plt.grid(visible=True, linestyle='--', alpha=0.5)
    
    # Set y-axis limits with some padding
    y_min = max(0, y.min() - 100)
    y_max = y.max() + 100
    plt.ylim(y_min, y_max)
    
    # Ticks for x-axis every 5 contests or fewer if less contests
    step = 5 if len(x) > 10 else 1
    plt.xticks(np.arange(1, len(x)+1, step))
    
    plt.tight_layout()
    plt.savefig("rating-graph.svg")
    print("Graph generated successfully!")
else:
    print("Failed to fetch rating data")
