import requests
import matplotlib.pyplot as plt

handle = "https://codeforces.com/profile/Jaardo"

url = f"https://codeforces.com/api/user.rating?handle={handle}"
response = requests.get(url)
data = response.json()

if data["status"] == "OK":
    contests = data["result"]
    x = [contest["contestId"] for contest in contests]
    y = [contest["newRating"] for contest in contests]
    labels = [contest["contestName"] for contest in contests]

    plt.figure(figsize=(10, 4))
    plt.plot(x, y, marker='o', linestyle='-', color='blue')
    plt.title(f"Codeforces Rating Graph for {handle}")
    plt.xlabel("Contest")
    plt.ylabel("Rating")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig("rating-graph.svg")  # Save as SVG
else:
    print("Failed to fetch rating data")
