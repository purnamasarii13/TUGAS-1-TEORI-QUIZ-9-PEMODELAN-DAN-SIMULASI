import pandas as pd
import numpy as np

# 1. Load data
df = pd.read_csv("coffee_shop_revenue.csv")
data = df["Number_of_Customers_Per_Day"]

# 2. Membuat interval (kelas) data
#    Di sini dari 50 sampai 500 dengan lebar 50: [50,100), [100,150), ..., [450,500)
bins = np.arange(50, 550, 50)
cats = pd.cut(data, bins=bins, right=False)  # left inclusive, right exclusive

freq = cats.value_counts().sort_index()
prob = freq / len(data)
cum_prob = prob.cumsum()

dist_table = pd.DataFrame({
    "Interval": freq.index.astype(str),
    "Frekuensi": freq.values,
    "Probabilitas": prob.values,
    "Prob_Kumulatif": cum_prob.values
})

print("Tabel Distribusi Probabilitas:")
print(dist_table)

# 3. Fungsi simulasi Monte Carlo
intervals = freq.index.to_list()
cum_p = cum_prob.values

def simulate_customers(n_days, random_seed=None):
    if random_seed is not None:
        np.random.seed(random_seed)

    # Bilangan acak uniform 0-1
    u = np.random.rand(n_days)

    simulated = []
    for r in u:
        # cari indeks interval berdasarkan F_i >= r
        idx = np.searchsorted(cum_p, r)
        inter = intervals[idx]

        # titik tengah interval sebagai estimasi jumlah pelanggan
        mid = (inter.left + inter.right) / 2
        simulated.append(mid)

    result = pd.DataFrame({
        "Hari": np.arange(1, n_days + 1),
        "Bilangan_Acak": u,
        "Jumlah_Pelanggan_Simulasi": simulated
    })

    return result

# 4. simulasi 30 hari ke depan
sim_result = simulate_customers(n_days=30, random_seed=42)

print("\nHasil Simulasi 30 Hari:")
print(sim_result)

avg_sim = sim_result["Jumlah_Pelanggan_Simulasi"].mean()
avg_hist = data.mean()

print("\nRata-rata pelanggan hasil simulasi:", round(avg_sim))
print("Rata-rata historis:", round(avg_hist))
