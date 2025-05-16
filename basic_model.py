import numpy as np
import matplotlib.pyplot as plt
import random
from collections import defaultdict
import math
import seaborn as sns
# Gale-Shapley Algorithm Implementation
def gale_shapley(n, doctor_prefs, hospital_prefs):
    free_doctors = list(range(n))
    proposals = np.zeros((n, n), dtype=bool)
    hospital_partners = [-1] * n
    doctor_partners = [-1] * n
    total_proposals = 0

    while free_doctors:
        d = free_doctors.pop(0)
        for h in doctor_prefs[d]:
            if not proposals[d][h]:
                proposals[d][h] = True
                total_proposals += 1
                if hospital_partners[h] == -1:
                    hospital_partners[h] = d
                    doctor_partners[d] = h
                else:
                    current = hospital_partners[h]
                    if hospital_prefs[h].index(d) < hospital_prefs[h].index(current):
                        hospital_partners[h] = d
                        doctor_partners[d] = h
                        doctor_partners[current] = -1
                        free_doctors.append(current)
                    else:
                        free_doctors.append(d)
                break

    return doctor_partners, hospital_partners, total_proposals

# Generate uniform random preferences
def generate_random_preferences(n):
    doctor_prefs = [random.sample(range(n), n) for _ in range(n)]
    hospital_prefs = [random.sample(range(n), n) for _ in range(n)]
    return doctor_prefs, hospital_prefs

# 1. Plot average number of proposals vs n
def plot_proposals_vs_n(random_pref_func, max_n=100, trials=30, name = "basic"):
    ns = list(range(2, max_n + 1, 2))
    avg_proposals = []

    for n in ns:
        total = 0
        for _ in range(trials):
            doc_prefs, hos_prefs = random_pref_func(n)
            _, _, proposals = gale_shapley(n, doc_prefs, hos_prefs)
            total += proposals
        avg_proposals.append(total / trials)

    plt.figure()
    plt.plot(ns, avg_proposals, marker='o')
    plt.title("Average Number of Proposals vs n")
    plt.xlabel("n")
    plt.ylabel("Average Number of Proposals")
    plt.grid(True)
    plt.savefig(f"avg_proposals_vs_n_{name}.png")
    plt.show()

# 2. Distribution of proposals for fixed n
def plot_proposal_distribution(random_pref_func, n=100, trials=1000, name = "basic"):
    proposal_counts = []
    for _ in range(trials):
        doc_prefs, hos_prefs = random_pref_func(n)
        _, _, proposals = gale_shapley(n, doc_prefs, hos_prefs)
        proposal_counts.append(proposals)

    plt.figure()
    plt.hist(proposal_counts, bins=30, edgecolor='black')
    plt.title(f"Distribution of Total Proposals (n={n})")
    plt.xlabel("Number of Proposals")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.savefig(f"proposal_distribution_{name}.png")
    plt.show()

# 3. Average rank of partners vs n
def plot_avg_rank_vs_n(random_pref_func, max_n=100, trials=30, name = "basic"):
    ns = list(range(2, max_n + 1, 2))
    doctor_ranks = []
    hospital_ranks = []

    for n in ns:
        total_doc_rank = 0
        total_hos_rank = 0

        for _ in range(trials):
            doc_prefs, hos_prefs = random_pref_func(n)
            doc_partners, hos_partners, _ = gale_shapley(n, doc_prefs, hos_prefs)

            for d, h in enumerate(doc_partners):
                total_doc_rank += doc_prefs[d].index(h) + 1  # +1 for 1-based rank
            for h, d in enumerate(hos_partners):
                total_hos_rank += hos_prefs[h].index(d) + 1

        doctor_ranks.append(total_doc_rank / (n * trials))
        hospital_ranks.append(total_hos_rank / (n * trials))

    plt.figure()
    plt.plot(ns, doctor_ranks, label="Doctor's Average Rank")
    plt.plot(ns, hospital_ranks, label="Hospital's Average Rank")
    plt.plot(ns, [math.log(n) for n in ns], '--', label="log(n)")
    plt.plot(ns, [n / math.log(n) for n in ns], '--', label="n/log(n)")
    plt.title("Average Rank of Partners vs n")
    plt.xlabel("n")
    plt.ylabel("Average Rank")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"avg_rank_vs_n_{name}.png")
    plt.show()


# 4. Optional: Rank distribution histograms for doctors and hospitals
def plot_rank_distribution(random_pref_func, n=100, trials=1000, name = "Basic"):
    doctor_ranks = []
    hospital_ranks = []

    for _ in range(trials):
        doc_prefs, hos_prefs = random_pref_func(n)
        doc_partners, hos_partners, _ = gale_shapley(n, doc_prefs, hos_prefs)

        for d, h in enumerate(doc_partners):
            doctor_ranks.append((doc_prefs[d].index(h) + 1) / n * 100)  # percentile
        for h, d in enumerate(hos_partners):
            hospital_ranks.append((hos_prefs[h].index(d) + 1) / n * 100)

    plt.figure()
    sns.histplot(doctor_ranks, bins=20, kde=True, edgecolor='black')
    plt.title("Doctor Rank Distribution Histogram")
    plt.xlabel("Percentile Rank of Matched Hospital")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.savefig(f"doctor_rank_distribution_{name}.png")
    plt.show()

    plt.figure()
    sns.histplot(hospital_ranks, bins=20, kde=True, edgecolor='black')
    plt.title("Hospital Rank Distribution Histogram")
    plt.xlabel("Percentile Rank of Matched Doctor")
    plt.ylabel("Frequency")
    plt.grid(True)
    plt.savefig(f"hospital_rank_distribution_{name}.png")
    plt.show()

# Run the histogram plots

if __name__ == "__main__":
    # Run all plots
    # plot_proposals_vs_n(random_pref_func= generate_random_preferences, max_n=50, trials=50)
    # plot_proposal_distribution(random_pref_func= generate_random_preferences,n=150, trials=2000)
    # plot_avg_rank_vs_n(random_pref_func= generate_random_preferences, max_n=50, trials=50)

    plot_rank_distribution(random_pref_func= generate_random_preferences, n=100, trials=1000)
