import sympy
import math
import csv
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
import seaborn as sns

# Constants
e = math.e
N = 1000  # Range up to 1000
data = []
cum_avg_sum = 0.0  # For cumulative sum of average divisors
cum_Z = 0.0  # For cumulative Z

for n in range(1, N + 1):
    divisors = sympy.divisors(n)
    c_fs = len(divisors)
    avg_div = sum(divisors) / c_fs if c_fs > 0 else 0
    cum_avg_sum += avg_div
    avg_fs = cum_avg_sum / n
    Z = c_fs * (avg_fs / e)
    D = c_fs - avg_fs  # Deviation from cumulative average
    D_alt = c_fs - avg_div  # Deviation from own divisor average
    cum_Z += Z
    is_prime = sympy.isprime(n)

    data.append((n, Z, c_fs, avg_fs, D, D_alt, is_prime))

# Write to CSV
with open('z_prime_table_n1_to_1000_updated.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['n', 'Z(n)', 'c_fs', 'avg_fs', 'D(n)', 'D_alt(n)', 'Is Prime?'])
    writer.writerows(data)

# Load into df
df = pd.DataFrame(data, columns=['n', 'Z(n)', 'c_fs', 'avg_fs', 'D(n)', 'D_alt(n)', 'Is Prime?'])

# Separate primes and composites (exclude n=1 for composites)
primes = df[df['Is Prime?'] == True]
composites = df[(df['Is Prime?'] == False) & (df['n'] > 1)]

# Print basic statistics
print("="*80)
print("BASIC STATISTICS")
print("="*80)
print("\nStatistics for Z(n) - Primes:")
print(primes['Z(n)'].describe())
print("\nStatistics for Z(n) - Composites:")
print(composites['Z(n)'].describe())

print("\nStatistics for D(n) - Primes:")
print(primes['D(n)'].describe())
print("\nStatistics for D(n) - Composites:")
print(composites['D(n)'].describe())

print("\nStatistics for D_alt(n) - Primes:")
print(primes['D_alt(n)'].describe())
print("\nStatistics for D_alt(n) - Composites:")
print(composites['D_alt(n)'].describe())

# Statistical tests
print("\n" + "="*80)
print("STATISTICAL SIGNIFICANCE TESTS")
print("="*80)

# Z(n) tests
t_stat_z, p_val_z = stats.ttest_ind(primes['Z(n)'], composites['Z(n)'], equal_var=False)
u_stat_z, p_val_u_z = stats.mannwhitneyu(primes['Z(n)'], composites['Z(n)'])
print(f"\nWelch's T-test for Z(n): statistic={t_stat_z:.4f}, p-value={p_val_z:.4e}")
print(f"Mann-Whitney U for Z(n): statistic={u_stat_z:.4f}, p-value={p_val_u_z:.4e}")

# D(n) tests
t_stat_d, p_val_d = stats.ttest_ind(primes['D(n)'], composites['D(n)'], equal_var=False)
u_stat_d, p_val_u_d = stats.mannwhitneyu(primes['D(n)'], composites['D(n)'])
print(f"\nWelch's T-test for D(n): statistic={t_stat_d:.4f}, p-value={p_val_d:.4e}")
print(f"Mann-Whitney U for D(n): statistic={u_stat_d:.4f}, p-value={p_val_u_d:.4e}")

# D_alt(n) tests
t_stat_d_alt, p_val_d_alt = stats.ttest_ind(primes['D_alt(n)'], composites['D_alt(n)'], equal_var=False)
u_stat_d_alt, p_val_u_d_alt = stats.mannwhitneyu(primes['D_alt(n)'], composites['D_alt(n)'])
print(f"\nWelch's T-test for D_alt(n): statistic={t_stat_d_alt:.4f}, p-value={p_val_d_alt:.4e}")
print(f"Mann-Whitney U for D_alt(n): statistic={u_stat_d_alt:.4f}, p-value={p_val_u_d_alt:.4e}")

# Effect sizes
def cohens_d(group1, group2):
    n1, n2 = len(group1), len(group2)
    var1, var2 = group1.var(ddof=1), group2.var(ddof=1)
    pooled_var = ((n1-1)*var1 + (n2-1)*var2) / (n1 + n2 - 2)
    return (group1.mean() - group2.mean()) / math.sqrt(pooled_var)

cohen_d_z = cohens_d(primes['Z(n)'], composites['Z(n)'])
cohen_d_d = cohens_d(primes['D(n)'], composites['D(n)'])
cohen_d_d_alt = cohens_d(primes['D_alt(n)'], composites['D_alt(n)'])

def effect_label(d):
    if abs(d) < 0.2: return 'negligible'
    elif abs(d) < 0.5: return 'small'
    elif abs(d) < 0.8: return 'medium'
    else: return 'large'

print("\n" + "="*80)
print("EFFECT SIZES (Cohen's d)")
print("="*80)
print(f"Cohen's d for Z(n): {cohen_d_z:.4f} ({effect_label(cohen_d_z)} effect)")
print(f"Cohen's d for D(n): {cohen_d_d:.4f} ({effect_label(cohen_d_d)} effect)")
print(f"Cohen's d for D_alt(n): {cohen_d_d_alt:.4f} ({effect_label(cohen_d_d_alt)} effect)")

# Correlations
print("\n" + "="*80)
print("CORRELATION ANALYSIS")
print("="*80)
df_filtered = df[df['n'] > 1]
correlation = df_filtered['Z(n)'].corr(df_filtered['D(n)'])
correlation_alt = df_filtered['Z(n)'].corr(df_filtered['D_alt(n)'])
print(f"Correlation between Z(n) and D(n) (excluding n=1): {correlation:.4f}")
print(f"Correlation between Z(n) and D_alt(n) (excluding n=1): {correlation_alt:.4f}")

# Normality checks
print("\n" + "="*80)
print("NORMALITY TESTS (Shapiro-Wilk)")
print("="*80)
def shapiro_report(name, data):
    stat, p = stats.shapiro(data)
    normal = "NORMAL" if p > 0.05 else "NON-NORMAL"
    return f"{name}: W={stat:.4f}, p={p:.4e} ({normal})"

print(shapiro_report("Z(n) - Primes", primes['Z(n)']))
print(shapiro_report("Z(n) - Composites", composites['Z(n)']))
print(shapiro_report("D_alt(n) - Primes", primes['D_alt(n)']))
print(shapiro_report("D_alt(n) - Composites", composites['D_alt(n)']))

# Prime analysis
print("\n" + "="*80)
print("PRIME CHARACTERISTICS ANALYSIS")
print("="*80)
prime_zs = primes[['n', 'Z(n)', 'D_alt(n)']].copy()
prime_zs['D_alt_abs'] = prime_zs['D_alt(n)'].abs()
print("\nTop 5 primes by Z(n):")
print(prime_zs.nlargest(5, 'Z(n)'))
print("\nPrimes closest to divisor equilibrium (|D_alt(n)| smallest):")
print(prime_zs.nsmallest(5, 'D_alt_abs'))
print("\nPrimes with largest deviation (|D_alt(n)| largest):")
print(prime_zs.nlargest(5, 'D_alt_abs'))

# Visualization
print("\n" + "="*80)
print("GENERATING VISUALIZATIONS")
print("="*80)

# Set style
sns.set_theme(style="whitegrid")

# Z(n) Histogram
plt.figure(figsize=(10, 6))
bins = np.linspace(min(df['Z(n)']), max(df['Z(n)']), 50)
plt.hist(primes['Z(n)'], bins=bins, alpha=0.7, label='Primes', color='blue', density=True)
plt.hist(composites['Z(n)'], bins=bins, alpha=0.7, label='Composites', color='orange', density=True)
plt.xlabel('Z(n)')
plt.ylabel('Density')
plt.title('Distribution of Z(n) for Primes and Composites')
plt.legend()
plt.savefig('Z_histogram.png', dpi=300)
plt.close()

# D_alt(n) Histogram
plt.figure(figsize=(10, 6))
bins = np.linspace(min(df['D_alt(n)']), max(df['D_alt(n)']), 50)
plt.hist(primes['D_alt(n)'], bins=bins, alpha=0.7, label='Primes', color='blue', density=True)
plt.hist(composites['D_alt(n)'], bins=bins, alpha=0.7, label='Composites', color='orange', density=True)
plt.xlabel('D_alt(n) = τ(n) - σ(n)/τ(n)')
plt.ylabel('Density')
plt.title('Deviation from Own Divisor Average')
plt.legend()
plt.savefig('D_alt_histogram.png', dpi=300)
plt.close()

# Scatter plots
fig, ax = plt.subplots(1, 2, figsize=(18, 6))
ax[0].scatter(primes['n'], primes['Z(n)'], color='blue', label='Primes', alpha=0.7)
ax[0].scatter(composites['n'], composites['Z(n)'], color='orange', label='Composites', alpha=0.3)
ax[0].set_xlabel('n')
ax[0].set_ylabel('Z(n)')
ax[0].set_title('Z(n) vs n')
ax[0].legend()
ax[0].grid(True)

ax[1].scatter(primes['n'], primes['D_alt(n)'], color='blue', label='Primes', alpha=0.7)
ax[1].scatter(composites['n'], composites['D_alt(n)'], color='orange', label='Composites', alpha=0.3)
ax[1].set_xlabel('n')
ax[1].set_ylabel('D_alt(n)')
ax[1].set_title('D_alt(n) vs n')
ax[1].legend()
ax[1].grid(True)
plt.savefig('combined_scatter.png', dpi=300)
plt.close()

# Boxplots
fig, ax = plt.subplots(1, 3, figsize=(20, 6))
df.boxplot(column='Z(n)', by='Is Prime?', ax=ax[0])
ax[0].set_title('Z(n) by Primality')
ax[0].set_xlabel('Is Prime?')

df.boxplot(column='D(n)', by='Is Prime?', ax=ax[1])
ax[1].set_title('D(n) by Primality')
ax[1].set_xlabel('Is Prime?')

df.boxplot(column='D_alt(n)', by='Is Prime?', ax=ax[2])
ax[2].set_title('D_alt(n) by Primality')
ax[2].set_xlabel('Is Prime?')

plt.suptitle('')
plt.savefig('boxplot_comparison.png', dpi=300)
plt.close()

print("\nAnalysis complete. Visualizations saved as:")
print("- Z_histogram.png")
print("- D_alt_histogram.png")
print("- combined_scatter.png")
print("- boxplot_comparison.png")