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
    const rows = data.random_rows;

    // rata-rata prediksi
    const avgPred = Math.round(data.avg_pred);

    // prediksi hari terakhir (Zi ke-n)
    const last = rows[rows.length - 1];
    const lastPred = last.prediksi;

    document.getElementById("summary").innerHTML =
        `Perkiraan rata-rata jumlah pelanggan per hari: <b>${avgPred}</b> pelanggan<br>` +
        `Prediksi jumlah pelanggan di hari ke-${rows.length}: <b>${lastPred}</b> pelanggan`;
}
