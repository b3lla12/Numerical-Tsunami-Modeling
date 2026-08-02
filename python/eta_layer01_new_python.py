import numpy as np
import glob
import os

folder = r"D:\comcotpraba-master-20260211T080732Z-1-001\SIMULASI_SKRIPSI_1"
files = sorted(glob.glob(os.path.join(folder, "z_01_*.dat")))

print("Jumlah file:", len(files))

# ==============================
# LOAD FILE PERTAMA
# ==============================
data = np.genfromtxt(files[0], invalid_raise=False)

# buang baris rusak
data = data[~np.isnan(data).any(axis=1)]

# buang no data
data[data <= -900] = np.nan

ny, nx = data.shape
print("Grid:", ny, "x", nx)

# ==============================
# KOORDINAT COMCOT
# ==============================
x_start = 92.795833
x_end   = 97.292500
y_start = 3.129166
y_end   = 7.197500

lon = np.linspace(x_start, x_end, nx)
lat = np.linspace(y_start, y_end, ny)

xx, yy = np.meshgrid(lon, lat)

# ==============================
# LOOP DATA
# ==============================
all_z = []

for file in files:
    print("Processing:", os.path.basename(file))

    d = np.genfromtxt(file, invalid_raise=False)

    # buang baris rusak
    d = d[~np.isnan(d).any(axis=1)]

    # buang no data
    d[d <= -900] = np.nan

    all_z.append(d)

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
time = np.loadtxt(os.path.join(folder, "time.dat"))

threshold = 0.01
arrival_index = np.argmax(all_z > threshold, axis=0)
arrival_time = time[arrival_index]

# ==============================
# SAVE
# ==============================
np.savetxt(
    r"D:\python file skripsi\max_eta_layer01_geo.csv",
    np.column_stack((xx.flatten(), yy.flatten(), max_eta.flatten())),
    delimiter=",",
    header="lon,lat,max_eta",
    comments=""
)

np.savetxt(
    r"D:\python file skripsi\arrival_time_layer01_geo.csv",
    np.column_stack((xx.flatten(), yy.flatten(), arrival_time.flatten())),
    delimiter=",",
    header="lon,lat,arrival_time",
    comments=""
)

print("✅ SELESAI TANPA ERROR")
