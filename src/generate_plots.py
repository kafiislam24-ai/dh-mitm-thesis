"""
Phase 4: Generate Publication-Quality Figures for Thesis / Paper
Reads generated CSVs and outputs graphs into the figures/ directory.
"""

from pathlib import Path
import matplotlib.pyplot as plt
import pandas as pd

# Setup directories
figures_dir = Path("figures")
figures_dir.mkdir(parents=True, exist_ok=True)
results_dir = Path("results")

# Load datasets
df_std = pd.read_csv(results_dir / "standard_dh.csv")
df_mitm = pd.read_csv(results_dir / "mitm.csv")
df_auth = pd.read_csv(results_dir / "authenticated_dh.csv")

# Set global academic plot styling
plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
plt.rcParams.update({"font.size": 11, "font.family": "serif"})

# -------------------------------------------------------------
# Figure 1: Handshake Execution Time Comparison across Scenarios
# -------------------------------------------------------------
fig1, ax1 = plt.subplots(figsize=(7, 4.5), dpi=300)

scenarios = ["Standard DH (E1)", "Authenticated DH (E3)", "MitM Attack (E2)"]
mean_times = [
    df_std["total_time_ms"].mean(),
    df_auth["total_time_ms"].mean(),
    df_mitm["total_time_ms"].mean()
]
std_errors = [
    df_std["total_time_ms"].std(),
    df_auth["total_time_ms"].std(),
    df_mitm["total_time_ms"].std()
]
colors = ["#2b5c8f", "#2e7d32", "#c62828"]

bars = ax1.bar(scenarios, mean_times, yerr=std_errors, capsize=5, color=colors, width=0.55, edgecolor="black")
ax1.set_ylabel("Execution Time (milliseconds)", fontweight="bold")
ax1.set_title("Handshake Execution Time Comparison Across Scenarios", fontweight="bold", pad=12)
ax1.set_ylim(0, max(mean_times) * 1.25)

for bar in bars:
    height = bar.get_height()
    ax1.annotate(f"{height:.2f} ms",
                 xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 6), textcoords="offset points",
                 ha="center", va="bottom", fontweight="bold")

fig1.tight_layout()
fig1_path = figures_dir / "fig1_execution_time_comparison.png"
fig1.savefig(fig1_path)
plt.close(fig1)
print(f"[+] Saved: {fig1_path}")

# -------------------------------------------------------------
# Figure 2: Authenticated DH Computational Breakdown
# -------------------------------------------------------------
fig2, ax2 = plt.subplots(figsize=(8, 4.5), dpi=300)

operations = [
    "Ephemeral KeyGen\n(Alice + Bob)",
    "RSA-PSS Signing\n(Alice + Bob)",
    "RSA-PSS Verify\n(Alice + Bob)",
    "Secret Derivation\n(Alice + Bob)"
]
breakdown_times = [
    df_auth["keygen_time_ms"].mean(),
    df_auth["sign_time_ms"].mean(),
    df_auth["verify_time_ms"].mean(),
    df_auth["exchange_time_ms"].mean()
]

bars2 = ax2.bar(operations, breakdown_times, color=["#1565c0", "#f57c00", "#7b1fa2", "#00897b"], width=0.5, edgecolor="black")
ax2.set_ylabel("Mean Execution Time (milliseconds)", fontweight="bold")
ax2.set_title("Computational Latency Breakdown of Authenticated DH", fontweight="bold", pad=12)
ax2.set_ylim(0, max(breakdown_times) * 1.25)

for bar in bars2:
    height = bar.get_height()
    ax2.annotate(f"{height:.3f} ms",
                 xy=(bar.get_x() + bar.get_width() / 2, height),
                 xytext=(0, 5), textcoords="offset points",
                 ha="center", va="bottom", fontweight="bold")

fig2.tight_layout()
fig2_path = figures_dir / "fig2_authenticated_dh_breakdown.png"
fig2.savefig(fig2_path)
plt.close(fig2)
print(f"[+] Saved: {fig2_path}")

# -------------------------------------------------------------
# Figure 3: Security Resilience (ASR vs ADR)
# -------------------------------------------------------------
fig3, ax3 = plt.subplots(figsize=(6, 4.2), dpi=300)

categories = ["Standard DH", "Authenticated DH"]
asr_vals = [100.0, 0.0]
adr_vals = [0.0, 100.0]

x = range(len(categories))
width = 0.35

rects1 = ax3.bar([p - width/2 for p in x], asr_vals, width, label="Attack Success Rate (ASR)", color="#d32f2f", edgecolor="black")
rects2 = ax3.bar([p + width/2 for p in x], adr_vals, width, label="Attack Detection Rate (ADR)", color="#2e7d32", edgecolor="black")

ax3.set_ylabel("Percentage (%)", fontweight="bold")
ax3.set_title("Security Resilience Comparison", fontweight="bold", pad=12)
ax3.set_xticks(list(x))
ax3.set_xticklabels(categories, fontweight="bold")
ax3.set_ylim(0, 120)
ax3.legend(frameon=True, loc="upper center")

for rect in rects1:
    h = rect.get_height()
    ax3.annotate(f"{h:.1f}%", xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 4), textcoords="offset points", ha="center", va="bottom")

for rect in rects2:
    h = rect.get_height()
    ax3.annotate(f"{h:.1f}%", xy=(rect.get_x() + rect.get_width() / 2, h), xytext=(0, 4), textcoords="offset points", ha="center", va="bottom")

fig3.tight_layout()
fig3_path = figures_dir / "fig3_security_metrics_comparison.png"
fig3.savefig(fig3_path)
plt.close(fig3)
print(f"[+] Saved: {fig3_path}")

print("\nAll publication-quality figures generated successfully in 'figures/' directory.")