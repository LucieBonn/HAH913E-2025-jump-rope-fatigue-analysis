bomane-travail
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def analyse_essai1(base_name):
    path = f"data/{base_name}.csv"
    df = pd.read_csv(path, sep=",", engine="python", on_bad_lines="skip")

    if df.shape[1] == 4:
        df.columns = ["datetime_raw", "ax", "ay", "az"]
        df["datetime"] = pd.to_datetime(df["datetime_raw"], errors="coerce")
    elif df.shape[1] == 5:
        df.columns = ["date", "hour", "ax", "ay", "az"]
        df["datetime"] = pd.to_datetime(df["date"] + " " + df["hour"],
                                        dayfirst=True, errors="coerce")
    else:
        raise ValueError

    df = df.dropna(subset=["datetime"]).reset_index(drop=True)

    for c in ["ax", "ay", "az"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["ax", "ay", "az"]).reset_index(drop=True)

    df["norm_ms2"] = np.sqrt(df["ax"]**2 + df["ay"]**2 + df["az"]**2)
    df["norm_g"] = df["norm_ms2"] / 9.81
    df["ENMO"] = np.maximum(df["norm_g"] - 1.0, 0)

    t0 = df["datetime"].iloc[0]
    df["t_seconds"] = (df["datetime"] - t0).dt.total_seconds()

    dt = df["t_seconds"].diff().median()
    df["ENMO_dt"] = df["ENMO"] * dt

    window_10 = int(10 / dt)
    window_20 = int(20 / dt)
    window_30 = int(30 / dt)

    df["ENMO_10s"] = df["ENMO_dt"].rolling(window_10).sum()
    df["ENMO_20s"] = df["ENMO_dt"].rolling(window_20).sum()
    df["ENMO_30s"] = df["ENMO_dt"].rolling(window_30).sum()

    os.makedirs("resultats", exist_ok=True)

    plt.figure(figsize=(10, 4))
    plt.plot(df["t_seconds"], df["ENMO"], linewidth=1)
    plt.xlabel("Temps (s)")
    plt.ylabel("ENMO (g)")
    plt.title(f"ENMO instantané — {base_name}")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"resultats/{base_name}_ENMO_Essai1.png", dpi=200)
    plt.close()

    plt.figure(figsize=(10, 4))
    plt.plot(df["t_seconds"], df["ENMO_10s"], linewidth=1)
    plt.xlabel("Temps (s)")
    plt.ylabel("ENMO intégré (g·s)")
    plt.title(f"ENMO intégré sur 10 s — {base_name}")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"resultats/{base_name}_ENMO10s_Essai1.png", dpi=200)
    plt.close()

    plt.figure(figsize=(10, 4))
    plt.plot(df["t_seconds"], df["ENMO_20s"], linewidth=1)
    plt.xlabel("Temps (s)")
    plt.ylabel("ENMO intégré (g·s)")
    plt.title(f"ENMO intégré sur 20 s — {base_name}")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"resultats/{base_name}_ENMO20s_Essai1.png", dpi=200)
    plt.close()

    plt.figure(figsize=(10, 4))
    plt.plot(df["t_seconds"], df["ENMO_30s"], linewidth=1)
    plt.xlabel("Temps (s)")
    plt.ylabel("ENMO intégré (g·s)")
    plt.title(f"ENMO intégré sur 30 s — {base_name}")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"resultats/{base_name}_ENMO30s_Essai1.png", dpi=200)
    plt.close()

        # Boxplots par tranches de 10 % de l'enregistrement
    n_bins = 10
    df["rel_pos"] = np.linspace(0, 1, len(df))  # 0 → 1 sur tout l’enregistrement
    df["bin"] = np.floor(df["rel_pos"] * n_bins).astype(int)
    df.loc[df["bin"] == n_bins, "bin"] = n_bins - 1

    groups = [g["ENMO"].values for _, g in df.groupby(df["bin"])]
    labels = [f"{i*10}–{(i+1)*10}%" for i in range(n_bins)]

    plt.figure(figsize=(12, 5))
    plt.boxplot(groups, labels=labels, showfliers=True)
    plt.ylabel("ENMO (g)")
    plt.title(f"Boîtes ENMO — tranches de 10 % de l’enregistrement — {base_name}")
    plt.xticks(rotation=45)

    plt.ylim(0, df["ENMO"].quantile(0.95))

    plt.tight_layout()
    plt.savefig(f"resultats/{base_name}_BOXPLOT_10percent_Essai1.png", dpi=200)
    plt.close()


    enmo_pos = df["ENMO"][df["ENMO"] > 0]

    if len(enmo_pos) > 0:
        plt.figure(figsize=(8, 4))
        plt.hist(enmo_pos, bins=30, edgecolor="black")
        plt.xlabel("ENMO (g)")
        plt.ylabel("Fréquence")
        plt.title(f"Histogramme ENMO > 0 — {base_name}")
        plt.grid(True, axis="y")
        plt.tight_layout()
        plt.savefig(f"resultats/{base_name}_HIST_ENMO_pos_Essai1.png", dpi=200)
        plt.close()





def analyse_essai2(base_name):
    path = f"data/{base_name}.csv"
    df = pd.read_csv(path, header=0,
                     names=["time", "gFx", "gFy", "gFz", "norm_device"],
                     sep=",", engine="python")

    df["time"] = pd.to_datetime(df["time"], errors="coerce")
    df = df.dropna(subset=["time"]).reset_index(drop=True)

    for c in ["gFx", "gFy", "gFz"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")
    df = df.dropna(subset=["gFx", "gFy", "gFz"]).reset_index(drop=True)

    df["norm"] = np.sqrt(df["gFx"]**2 + df["gFy"]**2 + df["gFz"]**2)
    df["ENMO"] = np.maximum(df["norm"] - 1.0, 0)

    t0 = df["time"].iloc[0]
    df["t_seconds"] = (df["time"] - t0).dt.total_seconds()

    dt = df["t_seconds"].diff().median()
    df["ENMO_dt"] = df["ENMO"] * dt

    window_10 = int(10 / dt)
    window_20 = int(20 / dt)
    window_30 = int(30 / dt)

    df["ENMO_10s"] = df["ENMO_dt"].rolling(window_10).sum()
    df["ENMO_20s"] = df["ENMO_dt"].rolling(window_20).sum()
    df["ENMO_30s"] = df["ENMO_dt"].rolling(window_30).sum()

    os.makedirs("resultats", exist_ok=True)

    plt.figure(figsize=(10, 4))
    plt.plot(df["t_seconds"], df["ENMO"], linewidth=1)
    plt.xlabel("Temps (s)")
    plt.ylabel("ENMO (g)")
    plt.title(f"ENMO instantané — {base_name}")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"resultats/{base_name}_ENMO_Essai2.png", dpi=200)
    plt.close()

    plt.figure(figsize=(10, 4))
    plt.plot(df["t_seconds"], df["ENMO_10s"], linewidth=1)
    plt.xlabel("Temps (s)")
    plt.ylabel("ENMO intégré (g·s)")
    plt.title(f"ENMO intégré sur 10 s — {base_name}")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"resultats/{base_name}_ENMO10s_Essai2.png", dpi=200)
    plt.close()

    plt.figure(figsize=(10, 4))
    plt.plot(df["t_seconds"], df["ENMO_20s"], linewidth=1)
    plt.xlabel("Temps (s)")
    plt.ylabel("ENMO intégré (g·s)")
    plt.title(f"ENMO intégré sur 20 s — {base_name}")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"resultats/{base_name}_ENMO20s_Essai2.png", dpi=200)
    plt.close()

    plt.figure(figsize=(10, 4))
    plt.plot(df["t_seconds"], df["ENMO_30s"], linewidth=1)
    plt.xlabel("Temps (s)")
    plt.ylabel("ENMO intégré (g·s)")
    plt.title(f"ENMO intégré sur 30 s — {base_name}")
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(f"resultats/{base_name}_ENMO30s_Essai2.png", dpi=200)
    plt.close()

    n_bins = 10
    df["rel_pos"] = np.linspace(0, 1, len(df))
    df["bin"] = np.floor(df["rel_pos"] * n_bins).astype(int)
    df.loc[df["bin"] == n_bins, "bin"] = n_bins - 1

    groups = [g["ENMO"].values for _, g in df.groupby(df["bin"])]
    labels = [f"{i*10}–{(i+1)*10}%" for i in range(n_bins)]

    plt.figure(figsize=(12, 5))
    plt.boxplot(groups, labels=labels, showfliers=True)
    plt.ylabel("ENMO (g)")
    plt.title(f"Boîtes ENMO — tranches de 10 % de l’enregistrement — {base_name}")
    plt.xticks(rotation=45)
    plt.ylim(0, df["ENMO"].quantile(0.98) * 1.1)

    plt.tight_layout()
    plt.savefig(f"resultats/{base_name}_BOXPLOT_10percent_Essai2.png", dpi=200)
    plt.close()




if __name__ == "__main__":
    fichiers_essai1 = [
        "ankle_Series1_trial1",
        "ankle_Series2_trial1",
        "ankle_Series3_trial1",
    ]

    fichiers_essai2 = [
        "ankle_Series1_trial2",
        "ankle_Series2_trial2",
        "ankle_Series3_trial2",
    ]

    for f in fichiers_essai1:
        analyse_essai1(f)

    for f in fichiers_essai2:
        analyse_essai2(f)

 
import os
from pathlib import Path
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =============================
# Dossiers
# =============================
base_dir = Path(__file__).parent
data_dir = base_dir / "data"
os.makedirs(base_dir / "resultats", exist_ok=True)

# =============================
# Fonctions ENMO & MAD
# =============================
def calculate_enmo(x, y, z):
    enmo = np.sqrt(x**2 + y**2 + z**2) - 1
    enmo[enmo < 0] = 0
    return enmo

def calculate_mad(x, y, z):
    magnitude = np.sqrt(x**2 + y**2 + z**2)
    return np.mean(np.abs(magnitude - np.mean(magnitude)))

# =============================
# Lecture CSV robuste
# =============================
def read_accel_file(file_path):
    print(f"\n Lecture fichier : {file_path.name}")

    try:
        df = pd.read_csv(
            file_path,
            header=None,
            sep=",",
            names=["time", "X", "Y", "Z"]
        )
    except Exception as e:
        print(f" Erreur de lecture : {e}")
        return None

    if df.shape[1] != 4:
        print(f" Format inattendu : {file_path.name}")
        return None

    return df

# =============================
# Calcul ENMO & MAD
# =============================
def compute_metrics(df):
    df["ENMO"] = np.maximum(
        np.sqrt(df["X"]**2 + df["Y"]**2 + df["Z"]**2) - 1, 0
    )
    df["MAD"] = (df[["X", "Y", "Z"]] - df[["X", "Y", "Z"]].mean()).abs().mean(axis=1)
    return df

# =============================
# Plot comparaison ankle/wrist
# =============================
def plot_comparison(df_ankle, df_wrist, title):
    combined = pd.concat([
        pd.DataFrame({"location": "ankle", "ENMO": df_ankle["ENMO"], "MAD": df_ankle["MAD"]}),
        pd.DataFrame({"location": "wrist", "ENMO": df_wrist["ENMO"], "MAD": df_wrist["MAD"]})
    ])

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    sns.boxplot(ax=axes[0], data=combined, x="location", y="ENMO")
    axes[0].set_title(f"ENMO – {title}")

    sns.boxplot(ax=axes[1], data=combined, x="location", y="MAD")
    axes[1].set_title(f"MAD – {title}")

    plt.suptitle(title, fontsize=16)
    plt.tight_layout()

    # Sauvegarde automatique
    fig.savefig(base_dir / "resultats" / f"{title}.png", dpi=300)
    plt.show()

# =============================
# Liste des fichiers à comparer
# =============================
comparisons = [
    ("Series1_trial1", "ankle_Series1_trial1.csv", "wrist_Series1_trial1.csv"),
    ("Series1_trial2", "ankle_Series1_trial2.csv", "wrist_Series1_trial2.csv"),
    ("Series2_trial1", "ankle_Series2_trial1.csv", "wrist_Series2_trial1.csv"),
    ("Series2_trial2", "ankle_Series2_trial2.csv", "wrist_Series2_trial2.csv"),
    ("Series3_trial1", "ankle_Series3_trial1.csv", "wrist_Series3_trial1.csv"),
    ("Series3_trial2", "ankle_Series3_trial2.csv", "wrist_Series3_trial2.csv"),
]

# =============================
# Boucle principale
# =============================
print("\n==============================")
print(" Début de génération des figures")
print("==============================")

for label, ankle_file, wrist_file in comparisons:

    path_ankle = data_dir / ankle_file
    path_wrist = data_dir / wrist_file

    df_ankle = read_accel_file(path_ankle)
    df_wrist = read_accel_file(path_wrist)

    if df_ankle is None or df_wrist is None:
        print(f" Données insuffisantes pour {label}.")
        print("--------------------------------------------")
        continue

    df_ankle = compute_metrics(df_ankle)
    df_wrist = compute_metrics(df_wrist)

    plot_comparison(df_ankle, df_wrist, label)

    print(f" Figure générée pour {label}")
    print("--------------------------------------------")

print("\n Toutes les figures valides ont été générées.")
main
