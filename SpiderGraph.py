import matplotlib.pyplot as plt
import numpy as np

# Assume these are the scores from the evaluation
scores = {
    "Team": team_score,
    "Fundraising": fundraising_score,
    "Market": market_score,
    "Business Model": business_model_score,
    "Product": product_score,
    "Traction": traction_score,
}

# Function to create a spider graph
def create_spider_graph(startup_name, scores):
    categories = list(scores.keys())
    values = list(scores.values())
    
    # Adding the first value at the end to close the circular graph
    values += values[:1]

    N = len(categories)
    
    # Setting up the angle for each axis
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    # Plot setup
    plt.figure(figsize=(6, 6))
    ax = plt.subplot(111, polar=True)
    
    # Draw the plot
    ax.fill(angles, values, color='blue', alpha=0.3)
    ax.plot(angles, values, color='blue', linewidth=2)

    # Set the category labels
    plt.xticks(angles[:-1], categories)

    # Set the scale for the radial axis
    ax.set_rlabel_position(0)
    plt.yticks([2, 4, 6, 8, 10], ["2", "4", "6", "8", "10"], color="grey", size=7)
    plt.ylim(0, 10)

    # Title of the graph
    plt.title(f"{startup_name} - Pitch Deck Scores", size=15, color='blue', y=1.1)

    # Display the plot
    plt.show()