import requests
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib as mpl

handle = "Jaardo"

# Dark theme
plt.style.use("dark_background")
mpl.rcParams['axes.edgecolor'] = 'white'
mpl.rcParams['axes.labelcolor'] = 'white'
mpl.rcParams['xtick.color'] = 'white'
mpl.rcParams['ytick.color'] = 'white']
mpl.rcParams['text.color'] = 'white'
mpl.rcParams['figure.facecolor'] = '#111111'

# Fetch data
url = f"https://codeforces.com/api/user.rating?handle={handle}"
response = requests.get(url)
data = response.json()

if data["status"] == "OK":
    contests = data["result"]
    if not contests:
        print("No contests found.")
        exit()

    x = np.array([i + 1 for i in range(len(contests))])
    y = np.array([contest["newRating"] for contest in contests])

    x_smooth = np.linspace(x.min(), x.max(), 300)
    y_smooth = make_interp_spline(x, y, k=2)(x_smooth)

    plt.figure(figsize=(5.5, 2.5))  # Around 400px width (5.5 in × 72 dpi)

    # Plot
    plt.plot(x_smooth, y_smooth, color='#00bfff', linewidth=2.5)
    plt.scatter(x, y, color='#00bfff', edgecolor='white', s=50, zorder=5)

    # Fill
    plt.fill_between(x_smooth, y_smooth, y.min() - 50, color='#00bfff', alpha=0.1)

    # Styling
    plt.title(f"{handle}'s Codeforces Rating", fontsize=13, weight='bold')
    plt.xlabel("Contest #", fontsize=11)
    plt.ylabel("Rating", fontsize=11)
    plt.grid(visible=True, linestyle='--', alpha=0.3)
    plt.tight_layout()
    plt.savefig("rating-graph.svg", bbox_inches='tight')
    print("Graph generated successfully")
else:
    print("Failed to fetch rating data")
