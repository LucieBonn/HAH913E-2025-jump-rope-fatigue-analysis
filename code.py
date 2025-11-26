 
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
