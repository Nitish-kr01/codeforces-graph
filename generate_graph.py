import requests
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
import matplotlib as mpl

handle = "Jaardo"  # Replace with your Codeforces handle

# Set dark theme and styling
plt.style.use("dark_background")
mpl.rcParams['axes.edgecolor'] = 'white'
mpl.rcParams['axes.labelcolor'] = 'white'
mpl.rcParams['xtick.color'] = 'white'
mpl.rcParams['ytick.color'] = 'white'
mpl.rcParams['text.color'] = 'white'
mpl.rcParams['figure.facecolor'] = '#111111'

# Fetch rating data
url = f"https://codeforces.com/api/user.rating?handle={handle}"
response = requests.get(url)
data = response.json()

if data["status"] == "OK":
    contests = data["result"]
    if not contests:
        print("No contests found for this handle.")
        exit()

    x = np.array([i + 1 for i in range(len(contests))])
    y = np.array([contest["newRating"] for contest in contests])

    # Smooth the curve
    x_smooth = np.linspace(x.min(), x.max(), 300)
    if len(x) >= 4:
        y_smooth = make_interp_spline(x, y, k=3)(x_smooth)  # cubic
    else:
        y_smooth = make_interp_spline(x, y, k=1)(x_smooth)  # linear fallback

    # Create figure with ~400px width (5.5in × 72dpi)
    plt.figure(figsize=(5.5, 2.5))
    ax = plt.gca()

    # Remove spines for clean look
    for spine in ax.spines.values():
        spine.set_visible(False)

    # Plot smooth line
    plt.plot(x_smooth, y_smooth, color='#00bfff', linewidth=1)

    # Grid on y-axis only
    plt.grid(axis='y', visible=True, linestyle='-', alpha=0.3)

    # Title and ticks
    plt.title(f"{handle}", fontsize=13, weight='bold')
    plt.xticks(np.arange(x.min(), x.max() + 1, 1))
    plt.tight_layout()

    # Save as SVG
    plt.savefig("rating-graph.svg", bbox_inches='tight')
    print("Graph generated successfully.")
else:
    print("Failed to fetch rating data.")

