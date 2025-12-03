from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
import random  # kalau mau pakai seed acak

app = Flask(__name__)

# ============
# LOAD DATASET
# ============
df = pd.read_csv("coffee_shop_revenue.csv")
data = df["Number_of_Customers_Per_Day"]

# ================================
# MEMBANGUN TABEL HITUNG INTERVAL
# ================================
# Kita pakai 5 kelas interval pelanggan per hari
bins = np.linspace(data.min(), data.max(), 11)  # 10 interval
cats = pd.cut(data, bins=bins, right=False)
freq = cats.value_counts().sort_index()
prob = freq / len(data)
cum_prob = prob.cumsum()

interval_rows = []
start = 0
for i, (iv, f, p, cp) in enumerate(
    zip(freq.index, freq.values, prob.values, cum_prob.values),
    start=1
):
    if i == len(freq):
        end = 999            # interval terakhir dipaksa sampai 999
    else:
        width = int(round(p * 1000))
        end = start + width - 1
    if end > 999:
        end = 999

    mid_customer = (iv.left + iv.right) / 2

    interval_rows.append({
        "no": i,
        "label": f"{int(iv.left)} - {int(iv.right) - 1}",
        "freq": int(f),
        "prob": float(round(p, 3)),
        "cum_prob": float(round(cp, 3)),
        "low": int(start),
        "high": int(end),
        "mid": float(round(mid_customer, 0))
    })

    start = end + 1

# ================================
# FUNGSI LCG UNTUK BILANGAN ACAK
# ================================
# Z_{i+1} = (A * Zi + C) mod M
A = 17
C = 43
M = 1000   # supaya hasil 0–999 (tiga digit)

def lcg_generate(n, z0):
    rows = []
    Zi = z0
    preds = []

    for i in range(1, n + 1):
        aZi_plus_c = A * Zi + C
        mod_m = aZi_plus_c % M
        three_digit = mod_m

        # mapping angka tiga digit ke interval
        pred_val = None
        for row in interval_rows:
            if three_digit >= row["low"] and three_digit <= row["high"]:
                pred_val = row["mid"]
                break

        rows.append({
            "i": i,
            "zi": int(Zi),
            "aZi_plus_c": int(aZi_plus_c),
            "mod_m": int(mod_m),
            "three_digit": int(three_digit),
            "prediksi": None if pred_val is None else int(pred_val)
        })

        if pred_val is not None:
            preds.append(pred_val)

        Zi = mod_m

    avg_pred = float(np.mean(preds)) if preds else 0.0
    return rows, avg_pred

# ==========
# ROUTES
# ==========
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/simulate", methods=["POST"])
def simulate():
    payload = request.json
    n = int(payload["days"])

    # Opsi 1: seed tetap (hasil simulasi konsisten setiap kali)
    z0 = 145

    # Opsi 2: kalau mau seed acak, pakai baris di bawah dan hapus z0=145
    # z0 = random.randint(0, 999)

    random_rows, avg_pred = lcg_generate(n, z0)

    return jsonify({
        "interval_rows": interval_rows,
        "random_rows": random_rows,
        "avg_pred": avg_pred,
        "avg_hist": float(data.mean())
    })

if __name__ == "__main__":
    app.run(debug=True)
