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
        # In a notebook, you might not want to exit, just skip plotting
        # exit()
    else:
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
        ax = plt.gca() # Get the current axes

        # Remove the spines
        ax.spines['top'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['right'].set_visible(False)


        # Plot only the smoothed line with reduced linewidth
        plt.plot(x_smooth, y_smooth, color='#00bfff', linewidth=1.5)

        # Area fill under the line
        #plt.fill_between(x_smooth, y_smooth, y.min() - 100, color='#00bfff', alpha=0.1)

        # Graph styling
        plt.title(f"{handle}", fontsize=13, weight='bold')
        plt.grid(axis='y', visible=True, linestyle='-', alpha=0.3) # Only horizontal grid lines
        plt.tight_layout()

        # Save as SVG
        plt.savefig("rating-graph.svg", bbox_inches='tight')
        print("Graph generated successfully.")
else:
    print("Failed to fetch rating data.")
