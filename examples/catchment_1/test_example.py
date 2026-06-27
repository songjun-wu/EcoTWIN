import shutil
import subprocess
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
import os

# =============================================================================
# A SIMPLE EXAMPLE OF MODEL EXECUTION
# The catchment is located in Estonia and Latvia, identified by WSO ID 831616
# in the Catchment Characterisation and Modelling database (CCM2, version 2.1).
# =============================================================================

# Configuration
path_cwd = Path.cwd()
path_source_codes = path_cwd.parents[1] / "release_linux"
path_output = path_cwd / "outputs"
clean_outputs = True


# === Step 1: Compile source codes ===
subprocess.run(["make", "all"], cwd=path_source_codes, check=True)
path_output.mkdir(exist_ok=True)


# === Step 2: Link executable to current path ===
source_exe = path_source_codes / "EcoTWIN"
target_exe = path_cwd / "EcoTWIN"
if target_exe.exists() or target_exe.is_symlink():
    target_exe.unlink()
target_exe.symlink_to(source_exe)


# === Step 3: Run EcoTWIN ===
#subprocess.run(["./EcoTWIN"], cwd=path_cwd, check=True)
os.system('./EcoTWIN')


# === Step 4: Visualise results ===
# Read outputs; here water age in top soil is shown as an example
mask = np.loadtxt(path_cwd / "spatial" / "age_layer1.asc", skiprows=6)
data = np.fromfile(path_output / "age_SMC_layer1_map.bin")
data = data.reshape(-1, mask.shape[0], mask.shape[1])
data = np.mean(data, axis=0)
data[mask == -9999] = np.nan
vmin = np.nanpercentile(data, 5)
vmax = np.nanpercentile(data, 95)

# Plot average water age for the period 1980-2024
fig, ax = plt.subplots(1, 1, figsize=(3, 2), dpi=300)
plt.subplots_adjust(left=0.0, bottom=0.0, right=0.8, top=0.85)
im = ax.imshow(data, vmin=vmin, vmax=vmax)
cax = fig.add_axes([0.8, 0.05, 0.04, 0.35])
cbar = fig.colorbar(im, cax=cax)
cbar.set_ticks([vmin, (vmin + vmax) / 2, vmax])
cbar.ax.tick_params(labelsize=8)
ax.text(
    1.28, 0.52,
    "Age (days)",
    ha="right",
    va="bottom",
    transform=ax.transAxes,
    fontsize=9
)
ax.text(
    0.63, 1.0,
    "Water age of top soil (0-20 cm)",
    ha="center",
    va="bottom",
    weight="bold",
    transform=ax.transAxes,
    fontsize=11
)
ax.axis("off")
fig.savefig(path_cwd / "water_age_top_soil.png", transparent=True)


# === Step 5: Clean outputs if needed ===
if clean_outputs:
    shutil.rmtree(path_output)
