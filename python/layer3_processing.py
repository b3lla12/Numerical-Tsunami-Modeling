import numpy as np
import glob
import os

# ==============================
# PATH FOLDER COMCOT
# ==============================

folder = r"D:\comcotpraba-master-20260211T080732Z-1-001\SIMULASI_SKRIPSI_1"

# ==============================
# AMBIL FILE LAYER 3
# ==============================

files = sorted(glob.glob(os.path.join(folder, "z_03_*.dat")))

print("Jumlah file:", len(files))

if len(files) == 0:
    print("❌ FILE LAYER 3 TIDAK DITEMUKAN!")
    exit()

# ==============================
# LOAD FILE PERTAMA
# ==============================

data = np.genfromtxt(files[0], invalid_raise=False)

data[data <= -900] = np.nan

ny, nx = data.shape

print("Grid:", ny, "x", nx)

# ==============================
# KOORDINAT LAYER 3
# ==============================
# sementara pakai domain layer 3 dari COMCOT

x_start = 94.7008
x_end   = 95.1992

y_start = 5.4008
y_end   = 5.7992

lon = np.linspace(x_start, x_end, nx)
lat = np.linspace(y_start, y_end, ny)

xx, yy = np.meshgrid(lon, lat)

# ==============================
# LOOP SEMUA FILE
# ==============================

all_z = []

for file in files:

    print("Processing:", os.path.basename(file))

    d = np.genfromtxt(file, invalid_raise=False)

    d[d <= -900] = np.nan

    # cek ukuran grid
    if d.shape != (ny, nx):
        print("⚠️ Skip (beda ukuran):", file)
        continue

    all_z.append(d)

if len(all_z) == 0:
    print("❌ DATA KOSONG!")
    exit()

all_z = np.array(all_z)

# ==============================
# MAX ETA
# ==============================

max_eta = np.nanmax(all_z, axis=0)

print("MAX ETA GLOBAL:", np.nanmax(max_eta))
print("MIN ETA GLOBAL:", np.nanmin(max_eta))

# ==============================
# ARRIVAL TIME
# ==============================

time_file = os.path.join(folder, "time.dat")

if not os.path.exists(time_file):
    print("❌ time.dat tidak ditemukan!")
    exit()

time = np.loadtxt(time_file)

# threshold 1 cm
threshold = 0.01

arrival_mask = np.abs(all_z) > threshold

arrival_index = np.argmax(arrival_mask, axis=0)

never_arrive = ~np.any(arrival_mask, axis=0)

arrival_time = time[arrival_index]

arrival_time[never_arrive] = np.nan

print("MAX ARRIVAL TIME:", np.nanmax(arrival_time))
print("MIN ARRIVAL TIME:", np.nanmin(arrival_time))

# ==============================
# OUTPUT FOLDER
# ==============================

output_folder = r"D:\python file skripsi"

# ==============================
# SAVE MAX ETA
# ==============================

np.savetxt(
    os.path.join(output_folder, "max_eta_layer03_geo.csv"),
    np.column_stack((xx.flatten(), yy.flatten(), max_eta.flatten())),
    delimiter=",",
    header="lon,lat,max_eta",
    comments=""
)

# ==============================
# SAVE ARRIVAL TIME
# ==============================

np.savetxt(
    os.path.join(output_folder, "arrival_time_layer03_geo.csv"),
    np.column_stack((xx.flatten(), yy.flatten(), arrival_time.flatten())),
    delimiter=",",
    header="lon,lat,arrival_time",
    comments=""
)

print("✅ ETA LAYER 3 SELESAI")
print("Threshold ETA = 0.01 m")
print("File tersimpan di:")
print(output_folder)
