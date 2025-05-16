
from basic_model import gale_shapley, plot_avg_rank_vs_n, plot_rank_distribution, plot_proposal_distribution, plot_proposals_vs_n
import  random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns



def weighted_permutation(weights):
    items = np.arange(len(weights))
    perm = []
    weights = weights.copy()
    for _ in range(len(weights)):
        probs = weights / weights.sum()
        chosen_index = np.random.choice(len(items), p=probs)
        perm.append(items[chosen_index])
        weights = np.delete(weights, chosen_index)
        items = np.delete(items, chosen_index)
    return perm

def generate_weighted_preferences(n):
    ai = np.arange(1, n + 1)
    doc_prefs = [weighted_permutation(ai) for _ in range(n)]
    hos_prefs = [weighted_permutation(ai) for _ in range(n)]
    return doc_prefs, hos_prefs

# Function to generate a weighted random preference list using popularity scores
def generate_popularity_weighted_preferences(n, popularity_scores):
    preferences = []
    for _ in range(n):
        remaining = list(range(n))
        remaining_scores = popularity_scores[:]
        pref_list = []

        for _ in range(n):
            total_weight = sum(remaining_scores[i] for i in remaining)
            r = random.uniform(0, total_weight)
            upto = 0
            for i in remaining:
                weight = remaining_scores[i]
                if upto + weight >= r:
                    pref_list.append(i)
                    remaining.remove(i)
                    break
                upto += weight

        preferences.append(pref_list)
    return preferences

# Experiment function for different popularity distributions
def compare_popularity_models(n=50, trials=100, model_type="equal"):
    if model_type == "equal":
        a = [1] * n
    elif model_type == "linear":
        a = list(range(1, n + 1))
    elif model_type == "exponential":
        a = [2 ** i for i in range(n)]

    avg_doc_ranks = []
    avg_hos_ranks = []

    for _ in range(trials):
        doc_prefs = generate_popularity_weighted_preferences(n, a)
        hos_prefs = generate_popularity_weighted_preferences(n, a)
        doc_partners, hos_partners, _ = gale_shapley(n, doc_prefs, hos_prefs)

        doc_rank_sum = sum(doc_prefs[d].index(h) + 1 for d, h in enumerate(doc_partners))
        hos_rank_sum = sum(hos_prefs[h].index(d) + 1 for h, d in enumerate(hos_partners))

        avg_doc_ranks.append(doc_rank_sum / n)
        avg_hos_ranks.append(hos_rank_sum / n)

    return np.mean(avg_doc_ranks), np.mean(avg_hos_ranks)

def compare_model():
    # Compare models: Equal, Linear, Exponential
    models = ["equal", "linear", "exponential"]
    results = {"Model": [], "Avg Doctor Rank": [], "Avg Hospital Rank": []}

    for model in models:
        doc_rank, hos_rank = compare_popularity_models(n=50, trials=100, model_type=model)
        results["Model"].append(model)
        results["Avg Doctor Rank"].append(doc_rank)
        results["Avg Hospital Rank"].append(hos_rank)
    df = pd.DataFrame(results)
    df.to_csv("popularity_model_comparison.csv", index=False)
    print(df)
    # tools.display_dataframe_to_user(name="Popularity-Based Model Comparison", dataframe=)


if __name__ == "__main__":
    # Run all plots
    # plot_proposals_vs_n(random_pref_func= generate_weighted_preferences, max_n=50, trials=50, name="Popularity")
    # plot_proposal_distribution(random_pref_func= generate_weighted_preferences,n=150, trials=2000, name="Popularity")
    # plot_avg_rank_vs_n(random_pref_func= generate_weighted_preferences, max_n=50, trials=50, name="Popularity")
    # plot_rank_distribution(random_pref_func= generate_weighted_preferences, n=100, trials=1000, name="Popularity")
    #
    compare_model()
