function runSimulation() {
    const days = document.getElementById("days").value;

    if (!days || days <= 0) {
        alert("Jumlah hari / bilangan acak harus lebih dari 0");
        return;
    }

    fetch("/simulate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ days: days })
    })
    .then(res => res.json())
    .then(data => {
        fillIntervalTable(data.interval_rows);
        fillRandomTable(data.random_rows);
        updateSummary(data);

        // Tampilkan bagian hasil setelah simulasi berhasil
        document.getElementById("resultSection").style.display = "block";
    })
    .catch(err => {
        console.error(err);
        alert("Terjadi kesalahan saat menjalankan simulasi.");
    });
}

function fillIntervalTable(rows) {
    const tbody = document.querySelector("#intervalTable tbody");
    tbody.innerHTML = "";

    rows.forEach(row => {
        const html = `
            <tr>
                <td>${row.no}</td>
                <td>${row.label}</td>
                <td>${row.freq}</td>
                <td>${row.prob.toFixed(3)}</td>
                <td>${row.cum_prob.toFixed(3)}</td>
                <td>${row.low} - ${row.high}</td>
            </tr>
        `;
        tbody.innerHTML += html;
    });
}

function fillRandomTable(rows) {
    const tbody = document.querySelector("#randomTable tbody");
    tbody.innerHTML = "";

    rows.forEach(r => {
        const pred = (r.prediksi === null) ? "-" : r.prediksi;
        const html = `
            <tr>
                <td>${r.i}</td>
                <td>${r.aZi_plus_c}</td>
                <td>${r.mod_m}</td>
                <td>${String(r.three_digit).padStart(3, "0")}</td>
                <td>${pred}</td>
            </tr>
        `;
        tbody.innerHTML += html;
    });
}

function updateSummary(data) {
    // rata-rata per hari (nilai asli, tanpa pembulatan)
    const avgPred = data.avg_pred;

    // prediksi per tahun (nilai asli, tidak dibulatkan)
    const yearlyPred = avgPred * 365;

    // format angka Indonesia (78.840,000)
    const formattedYearly = yearlyPred.toLocaleString("id-ID", {
        minimumFractionDigits: 3,
        maximumFractionDigits: 3
    });

    const formattedAvg = avgPred.toLocaleString("id-ID", {
        minimumFractionDigits: 3,
        maximumFractionDigits: 3
    });

    document.getElementById("summary").innerHTML =
        `Perkiraan rata-rata jumlah pelanggan per hari: <b>${formattedAvg}</b> pelanggan<br>` +
        `Prediksi rata-rata jumlah pelanggan dalam 1 tahun adalah <b>${formattedYearly}</b> pelanggan`;
}
