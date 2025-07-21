import sympy
import math
import csv
import matplotlib.pyplot as plt
import numpy as np

# Constants
e = math.e
N = 1000  # Range up to 1000
data = []
cum_avg_sum = 0.0  # For cumulative sum of average divisors
cum_Z = 0.0  # For cumulative Z

# Lists for plotting
n_values = []
Z_values = []
D_values = []
cum_Z_values = []
prime_n = []
prime_Z = []
prime_D = []
prime_cum_Z = []

for n in range(1, N + 1):
    divisors = sympy.divisors(n)
    c_fs = len(divisors)
    avg_div = sum(divisors) / c_fs if c_fs > 0 else 0
    cum_avg_sum += avg_div
    avg_fs = cum_avg_sum / n
    Z = c_fs * (avg_fs / e)
    D = c_fs - avg_fs
    cum_Z += Z
    is_prime = sympy.isprime(n)
    
    # Append to data
    data.append((n, Z, c_fs, avg_fs, D, is_prime))
    
    # For plotting
    n_values.append(n)
    Z_values.append(Z)
    D_values.append(D)
    cum_Z_values.append(cum_Z)
    
    if is_prime:
        prime_n.append(n)
        prime_Z.append(Z)
        prime_D.append(D)
        prime_cum_Z.append(cum_Z)

# Write to CSV
with open('z_prime_table_n1_to_1000.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['n', 'Z(n)', 'c_fs', 'avg_fs', 'D(n)', 'Is Prime?'])
    writer.writerows(data)

print("CSV file 'z_prime_table_n1_to_1000.csv' has been generated.")

# Generate plots

# Plot 1: Z(n) vs n
plt.figure(figsize=(12, 6))
plt.plot(n_values, Z_values, label='Z(n)', color='blue')
plt.scatter(prime_n, prime_Z, color='red', label='Primes')
plt.xlabel('n')
plt.ylabel('Z(n)')
plt.title('Z(n) vs n with Primes Highlighted')
plt.legend()
plt.grid(True)
plt.savefig('Z_vs_n.png')
plt.close()

# Plot 2: D(n) vs n
plt.figure(figsize=(12, 6))
plt.plot(n_values, D_values, label='D(n)', color='green')
plt.scatter(prime_n, prime_D, color='red', label='Primes')
plt.xlabel('n')
plt.ylabel('D(n)')
plt.title('D(n) vs n with Primes Highlighted')
plt.legend()
plt.grid(True)
plt.savefig('D_vs_n.png')
plt.close()

# Plot 3: Cumulative Z vs n
plt.figure(figsize=(12, 6))
plt.plot(n_values, cum_Z_values, label='CumZ(n)', color='purple')
plt.scatter(prime_n, prime_cum_Z, color='red', label='Primes')
plt.xlabel('n')
plt.ylabel('CumZ(n)')
plt.title('Cumulative Z vs n with Primes Highlighted')
plt.legend()
plt.grid(True)
plt.savefig('CumZ_vs_n.png')
plt.close()

print("Plots saved as 'Z_vs_n.png', 'D_vs_n.png', and 'CumZ_vs_n.png'.")
