from flask import Flask, render_template, request, redirect, url_for
import matplotlib.pyplot as plt
import numpy as np
import os

app = Flask(__name__)

# Define the root route
@app.route('/')
def index():
    return render_template('score.html')

# Define the route to handle form submission and generate the spider graph
@app.route('/submit', methods=['POST'])
def submit():
    scores = [
        int(request.form['team']),
        int(request.form['market']),
        int(request.form['business_model']),
        int(request.form['product']),
        int(request.form['traction']),
        int(request.form['finances']),
        int(request.form['innovation'])  # Assuming 'innovation' is the 7th input
    ]

    generate_spider_graph(scores)
    return redirect(url_for('index'))

def generate_spider_graph(scores):
    # Define the labels and number of variables
    labels = ['Team', 'Market', 'Business Model', 'Product', 'Traction', 'Finances', 'Innovation']
    num_vars = len(labels)

    # Compute angle for each axis
    angles = np.linspace(0, 2 * np.pi, num_vars, endpoint=False).tolist()

    # Complete the loop
    scores += scores[:1]
    angles += angles[:1]

    # Plotting
    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
    ax.fill(angles, scores, color='blue', alpha=0.25)
    ax.plot(angles, scores, color='blue', linewidth=2)
    ax.set_yticklabels([])

    # Set labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    # Save the figure
    if not os.path.exists('static'):
        os.makedirs('static')
    plt.savefig('static/spider_graph.png')
    plt.close()

if __name__ == '__main__':
    app.run(debug=True)
