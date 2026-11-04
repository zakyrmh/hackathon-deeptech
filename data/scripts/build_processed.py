#!/usr/bin/env python3
"""Build normalized Sumbar supply-demand CSVs from source snapshots."""

import csv
from pathlib import Path

DATA = Path(__file__).resolve().parents[1]
RAW = DATA / "raw"
OUT = DATA / "processed"
OUT.mkdir(exist_ok=True)

PRODUCTION_URL = "https://sumbar.bps.go.id/id/statistics-table/3/ZUhFd1JtZzJWVVpqWTJsV05XTllhVmhRSzFoNFFUMDkjMw==/produksi-tanaman-sayuran-dan-buah-buahan-semusim-menurut-kabupaten-kota-dan-jenis-tanaman---di-provinsi-sumatera-barat--2024.html?year=2024"
CONSUMPTION_URL = "https://sumbar.bps.go.id/id/publication/2026/03/17/07378cc39d6b72a965e75336/pola-konsumsi-makanan-penduduk-provinsi-sumatera-barat-2025.html"
POPULATION_URL = "https://sumbar.bps.go.id/id/statistics-table/3/V1ZSbFRUY3lTbFpEYTNsVWNGcDZjek53YkhsNFFUMDkjMw==/jumlah-penduduk--laju-pertumbuhan-penduduk--distribusi-persentase-penduduk--kepadatan-penduduk--rasio-jenis-kelamin-penduduk-menurut-kabupaten-kota-di-provinsi-sumatera-barat--2025.html?year=2025"

REGION_CODES = {
    "Kepulauan Mentawai": ("1301", "Kab. Kepulauan Mentawai"),
    "Kab. Kep. Mentawai": ("1301", "Kab. Kepulauan Mentawai"),
    "Pesisir Selatan": ("1302", "Kab. Pesisir Selatan"),
    "Kab. Pesisir Selatan": ("1302", "Kab. Pesisir Selatan"),
    "Solok": ("1303", "Kab. Solok"), "Kab. Solok": ("1303", "Kab. Solok"),
    "Sijunjung": ("1304", "Kab. Sijunjung"), "Kab. Sijunjung": ("1304", "Kab. Sijunjung"),
    "Tanah Datar": ("1305", "Kab. Tanah Datar"), "Kab. Tanah Datar": ("1305", "Kab. Tanah Datar"),
    "Padang Pariaman": ("1306", "Kab. Padang Pariaman"), "Kab. Padang Pariaman": ("1306", "Kab. Padang Pariaman"),
    "Agam": ("1307", "Kab. Agam"), "Kab. Agam": ("1307", "Kab. Agam"),
    "Lima Puluh Kota": ("1308", "Kab. Lima Puluh Kota"), "Kab. Lima Puluh Kota": ("1308", "Kab. Lima Puluh Kota"),
    "Pasaman": ("1309", "Kab. Pasaman"), "Kab. Pasaman": ("1309", "Kab. Pasaman"),
    "Solok Selatan": ("1310", "Kab. Solok Selatan"), "Kab. Solok Selatan": ("1310", "Kab. Solok Selatan"),
    "Dharmasraya": ("1311", "Kab. Dharmasraya"), "Kab. Dharmasraya": ("1311", "Kab. Dharmasraya"),
    "Pasaman Barat": ("1312", "Kab. Pasaman Barat"), "Kab. Pasaman Barat": ("1312", "Kab. Pasaman Barat"),
    "Kota Padang": ("1371", "Kota Padang"), "Kota Solok": ("1372", "Kota Solok"),
    "Kota Sawah Lunto": ("1373", "Kota Sawahlunto"), "Kota Sawahlunto": ("1373", "Kota Sawahlunto"),
    "Kota Padang Panjang": ("1374", "Kota Padang Panjang"),
    "Kota Bukittinggi": ("1375", "Kota Bukittinggi"),
    "Kota Payakumbuh": ("1376", "Kota Payakumbuh"),
    "Kota Pariaman": ("1377", "Kota Pariaman"),
}

COMMODITIES = {
    "bawang_merah": ("Produksi Bawang Merah (kuintal)", "Bawang merah (kg/kapita/minggu)", "Bawang Merah", "Bawang merah"),
    "cabai_merah_keriting": ("Produksi Cabai Keriting (kuintal)", "Cabe merah (kg/kapita/minggu)", "Cabai Keriting", "Cabe merah (proxy cabai merah keriting)"),
    "cabai_rawit_merah": ("Produksi Cabai Rawit (kuintal)", "Cabe rawit (kg/kapita/minggu)", "Cabai Rawit", "Cabe rawit (proxy cabai rawit merah)"),
}


def number(value):
    if value in {"-", "–", ""}:
        return 0.0
    return float(value.replace(".", "").replace(",", "."))


def read(path):
    with path.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write(name, rows):
    with (OUT / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


production_raw = read(RAW / "bps_production/production_sumbar_2024_source_snapshot.csv")
consumption_raw = read(RAW / "bps_consumption/consumption_sumbar_2025_appendix4_source_snapshot.csv")
population_raw = read(RAW / "bps_population/population_sumbar_2025_source_snapshot.csv")

production_raw = {row["Kabupaten/Kota"]: row for row in production_raw if row["Kabupaten/Kota"] != "Sumatera Barat"}
consumption_raw = {REGION_CODES[row["Kabupaten/Kota"]][0]: row for row in consumption_raw if row["Kabupaten/Kota"] != "Sumatera Barat"}
population_raw = {REGION_CODES[row["Kabupaten/Kota"]][0]: row for row in population_raw if row["Kabupaten/Kota"] != "Sumatera Barat"}

population_rows, production_rows, consumption_rows, baseline_rows = [], [], [], []

for source_region, prod in production_raw.items():
    code, region = REGION_CODES[source_region]
    population = round(number(population_raw[code]["Jumlah Penduduk (Ribu)"]) * 1000)
    population_rows.append({"region_code": code, "region_name": region, "year": 2025, "population_people": population, "source_url": POPULATION_URL})

    for commodity, (prod_col, cons_col, prod_label, cons_label) in COMMODITIES.items():
        prod_q = number(prod[prod_col])
        weekly = number(consumption_raw[code][cons_col])
        prod_kg = prod_q * 100
        annual_demand = weekly * population * 52
        production_rows.append({"region_code": code, "region_name": region, "commodity": commodity, "source_commodity_label": prod_label, "year": 2024, "production_quintal": f"{prod_q:.2f}", "production_kg": f"{prod_kg:.2f}", "source_url": PRODUCTION_URL})
        consumption_rows.append({"region_code": code, "region_name": region, "commodity": commodity, "source_commodity_label": cons_label, "year": 2025, "consumption_kg_capita_week": f"{weekly:.3f}", "source_url": CONSUMPTION_URL})
        baseline_rows.append({"region_code": code, "region_name": region, "commodity": commodity, "population_2025": population, "consumption_kg_capita_week_2025": f"{weekly:.3f}", "estimated_demand_kg_day_2025": f"{weekly * population / 7:.2f}", "estimated_demand_kg_year_2025": f"{annual_demand:.2f}", "production_kg_year_2024": f"{prod_kg:.2f}", "structural_balance_kg": f"{prod_kg - annual_demand:.2f}", "production_source_year": 2024, "demand_baseline_year": 2025, "method_note": "Demand = konsumsi kg/kapita/minggu x populasi x 52; bukan transaksi aktual"})

assert len(population_rows) == 19 and len(production_rows) == len(consumption_rows) == len(baseline_rows) == 57
totals = {commodity: sum(float(row["production_quintal"]) for row in production_rows if row["commodity"] == commodity) for commodity in COMMODITIES}
assert all(abs(totals[key] - expected) < 0.01 for key, expected in {"bawang_merah": 2307184.11, "cabai_merah_keriting": 1141695.55, "cabai_rawit_merah": 277163.69}.items())

write("population_sumbar_2025.csv", population_rows)
write("production_three_commodities_sumbar_2024.csv", production_rows)
write("consumption_three_commodities_sumbar_2025.csv", consumption_rows)
write("regional_supply_demand_baseline.csv", baseline_rows)
