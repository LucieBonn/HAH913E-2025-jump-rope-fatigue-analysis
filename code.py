import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


<<<<<<< Updated upstream
# 1) Lecture robuste : auto-détection du séparateur
try:
    df = pd.read_csv(path, header=None, sep=None, engine="python")  # Sniffer
except Exception:
    # fallback si Sniffer échoue
    df = pd.read_csv(path, header=None)

# 2) Si une seule colonne a été lue, tenter différents séparateurs courants
if df.shape[1] == 1:
    for sep_try in [";", ",", "\t", "|"]:
        df_try = pd.read_csv(path, header=None, sep=sep_try)
        if df_try.shape[1] >= 3:  # on veut au moins ax, ay, az
            df = df_try
            break

# 3) Vérifier le nombre de colonnes et nommer proprement
#   Cas standard attendu : 5 colonnes -> date, heure, ax, ay, az
if df.shape[1] == 5:
    df.columns = ["date", "heure", "ax", "ay", "az"]
#   Cas alternatif : 4 colonnes -> une seule colonne temporelle + 3 axes
elif df.shape[1] == 4:
    df.columns = ["datetime_raw", "ax", "ay", "az"]
    # découpe possible si datetime est "date heure" séparé par un espace
    # sinon on gardera datetime_raw tel quel
else:
    raise ValueError(f"Format inattendu : {df.shape[1]} colonnes lues.\n"
                     f"Inspectez les premières lignes du CSV pour connaître sa structure.")

# 4) Construire le temps
if "date" in df.columns and "heure" in df.columns:
    df["datetime"] = pd.to_datetime(df["date"] + " " + df["heure"], dayfirst=True, errors="coerce")
elif "datetime_raw" in df.columns:
    df["datetime"] = pd.to_datetime(df["datetime_raw"], dayfirst=True, errors="coerce")
else:
    raise ValueError("Impossible de construire la colonne datetime.")

# 5) Nettoyage lignes sans datetime parsable
df = df.dropna(subset=["datetime"]).reset_index(drop=True)

# 6) Conversion numérique des axes (au cas où)
for c in ["ax", "ay", "az"]:
    df[c] = pd.to_numeric(df[c], errors="coerce")
df = df.dropna(subset=["ax", "ay", "az"]).reset_index(drop=True)

# 7) Calcul de la norme + lissage simple
df["a_norm"] = np.sqrt(df["ax"]**2 + df["ay"]**2 + df["az"]**2)
df["a_norm_filt"] = df["a_norm"].rolling(window=5, center=True, min_periods=1).mean()

# ---- Indicateurs ----
moyenne    = df["a_norm_filt"].mean()
ecart_type = df["a_norm_filt"].std()
rms        = np.sqrt(np.mean(df["a_norm_filt"]**2))
max_val    = df["a_norm_filt"].max()

print("----- Indicateurs généraux -----")
print(f"Moyenne : {moyenne:.3f} m/s²")
print(f"Écart-type : {ecart_type:.3f} m/s²")
print(f"RMS : {rms:.3f} m/s²")
print(f"Max : {max_val:.3f} m/s²")

# ---- Graphe temporel en SECONDES (unique tracé) ----
start_time = df["datetime"].iloc[0]
time_seconds = (df["datetime"] - start_time).dt.total_seconds()

plt.figure(figsize=(10,5))
plt.plot(time_seconds, df["a_norm_filt"], linewidth=1)
plt.xlabel("Temps écoulé (s)")
plt.ylabel("Accélération totale (m/s²)")
plt.title("Accélération totale pendant l'exercice (filtrée)")
plt.grid(True)
plt.tight_layout()

# Sauvegarde dans le dossier resultats/
output_path = os.path.join("resultats", "Bomane1_corde_poignetdroit_graph.png")
plt.savefig(output_path, dpi=200)
plt.show()

print(f"\n✅ Graphique sauvegardé dans : {output_path}")

## ============================
# --- Construction du temps en secondes ---
df["t"] = (df["datetime"] - df["datetime"].iloc[0]).dt.total_seconds()

# -----------------------
# LISTE DES FICHIERS À TRAITER
# -----------------------
file_list = [
    "data/Bomane1_corde_poignetdroit.csv",
    "data/Bomane2_corde_poignetdroit.csv",
    "data/Bomane3_corde_poignetdroit.csv"
]

# -----------------------
# BOUCLE DE TRAITEMENT
# -----------------------
for path in file_list:
    
    print(f"\n--- Traitement de : {path} ---")
    
    # === 1. Lecture robuste du CSV (réutilise ton code) ===
    try:
        df = pd.read_csv(path, header=None, sep=None, engine="python")
    except:
        df = pd.read_csv(path, header=None)

    if df.shape[1] == 1:
        for sep_try in [";", ",", "\t", "|"]:
            df_try = pd.read_csv(path, header=None, sep=sep_try)
            if df_try.shape[1] >= 3:
                df = df_try
                break

    if df.shape[1] == 5:
        df.columns = ["date", "heure", "ax", "ay", "az"]
    elif df.shape[1] == 4:
        df.columns = ["datetime_raw", "ax", "ay", "az"]
    else:
        raise ValueError(f"Format inattendu dans {path}")

    if "date" in df.columns:
        df["datetime"] = pd.to_datetime(df["date"] + " " + df["heure"], dayfirst=True, errors="coerce")
    else:
        df["datetime"] = pd.to_datetime(df["datetime_raw"], dayfirst=True, errors="coerce")

    df = df.dropna(subset=["datetime"]).reset_index(drop=True)

    for c in ["ax", "ay", "az"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna(subset=["ax", "ay", "az"]).reset_index(drop=True)

    # -----------------------
    # === 2. CONSTRUCTION TEMPS T ===
    # -----------------------
    df["t"] = (df["datetime"] - df["datetime"].iloc[0]).dt.total_seconds()

    # -----------------------
    # === 3. CALCUL ENMO POSITIF ===
    # -----------------------
    norm = np.sqrt(df['ax']**2 + df['ay']**2 + df['az']**2)
    df['enmo'] = (norm - 1).clip(lower=0)

    # -----------------------
    # === 4. EPOCH 10 SECONDES ===
    # -----------------------
    epoch_length = 10
    df['epoch'] = (df['t'] // epoch_length).astype(int)
    
    aggregated = df.groupby('epoch')['enmo'].sum().reset_index()
    aggregated['enmo_gmin'] = aggregated['enmo'] * (epoch_length / 60)
    aggregated['time_min'] = aggregated['epoch'] * epoch_length / 60

    # -----------------------
    # === 5. GRAPHIQUE ===
    # -----------------------
    df['time_min'] = df['t'] / 60

    plt.figure(figsize=(12, 8))

    # ENMO intégré
    plt.subplot(2, 1, 1)
    plt.bar(aggregated['time_min'], aggregated['enmo_gmin'], width=0.15, color='grey')
    plt.title(f'ENMO intégré (10s) – {os.path.basename(path)}')
    plt.ylabel('ENMO intégré (g·min)')
    plt.axhline(0, color='black', linewidth=0.8)

    # ENMO brut
    plt.subplot(2, 1, 2)
    plt.plot(df['time_min'], df['enmo'], color='steelblue')
    plt.title('ENMO brut (>=0)')
    plt.xlabel('Temps (minutes)')
    plt.ylabel('ENMO (g)')
    plt.axhline(0, color='black', linewidth=0.8)
=======
# --------------------------------------------------------
#   FONCTION D’ANALYSE RÉUTILISABLE POUR CHAQUE FICHIER
# --------------------------------------------------------
def auto_scale_y(df, step=0.2, margin=0.5):
    """
    Choisit automatiquement l'échelle de l'axe Y selon les données.
    step = taille de graduation (0.2 m/s² par défaut)
    margin = marge ajoutée au max
    """
    max_val = df["a_norm_filt"].max()
    y_max = np.ceil((max_val + margin) / step) * step
    return y_max
>>>>>>> Stashed changes

    plt.tight_layout()

    # nom de sortie
    name = os.path.basename(path).replace(".csv", "_ENMO_10s.png")
    out_path = os.path.join("resultats", name)
    plt.savefig(out_path, dpi=200)
    plt.show()

<<<<<<< Updated upstream
    print(f"✅ Graphique sauvegardé : {out_path}")
=======
def analyse_fichier(base_name):

    print(f"\n=== Analyse de {base_name} ===")

    # ----- 1) Lecture fichier -----
        # ----- 1) Lecture fichier -----
    path = f"data/{base_name}.csv"

    # Lecture robuste : on laisse pandas détecter le header s'il existe
    df = pd.read_csv(path, sep=",", engine="python", on_bad_lines="skip")

    # ----- 2) Détection du format -----
    if "time" in df.columns:   # cas g-force : time,gFx,gFy,gFz
        df = df.rename(columns={
            "time": "datetime_raw",
            "gFx": "ax",
            "gFy": "ay",
            "gFz": "az"
        })

    elif df.shape[1] == 4:     # ancien format sans header : datetime_raw, ax, ay, az
        df.columns = ["datetime_raw", "ax", "ay", "az"]

    elif df.shape[1] == 5:     # ancien format : date, hour, ax, ay, az
        df.columns = ["date", "hour", "ax", "ay", "az"]

    else:
        raise ValueError(f"❌ Format inattendu dans {path} : {df.shape[1]} colonnes.")


    # ----- 3) Construction datetime -----
    if "datetime_raw" in df.columns:
        df["datetime"] = pd.to_datetime(df["datetime_raw"], errors="coerce")
    else:
        df["datetime"] = pd.to_datetime(
            df["date"] + " " + df["hour"],
            dayfirst=True,
            errors="coerce"
        )

    df = df.dropna(subset=["datetime"]).reset_index(drop=True)

    # ----- 4) Conversion numérique -----
    for c in ["ax", "ay", "az"]:
        df[c] = pd.to_numeric(df[c], errors="coerce")

    df = df.dropna(subset=["ax", "ay", "az"]).reset_index(drop=True)

    # ----- 5) Calcul a_norm -----
    df["a_norm"] = np.sqrt(df["ax"]**2 + df["ay"]**2 + df["az"]**2)
    df["a_norm_filt"] = df["a_norm"].rolling(window=5, center=True, min_periods=1).mean()

    # ----- 6) Sauvegarde CSV -----
    os.makedirs("data", exist_ok=True)
    output_csv = f"data/{base_name}_a_norm.csv"
    df[["datetime", "a_norm", "a_norm_filt"]].to_csv(output_csv, index=False)
    print(f"✅ Fichier sauvé : {output_csv}")

    # ----- 7) Temps en secondes -----
    start_time = df["datetime"].iloc[0]
    df["t_seconds"] = (df["datetime"] - start_time).dt.total_seconds()

    # ----- 8) Graphe temporel -----
    os.makedirs("resultats", exist_ok=True)


    

    plt.figure(figsize=(10, 5))
    plt.plot(df["t_seconds"], df["a_norm_filt"], linewidth=1)
    plt.xlabel("Temps écoulé (s)")
    plt.ylabel("a_norm filtrée (m/s²)")
    plt.title(f"Accélération filtrée — {base_name}")
    plt.grid(True)
    plt.tight_layout()

    graph_path = f"resultats/{base_name}_time_series.png"
    plt.savefig(graph_path, dpi=200)
    plt.close()
    print(f"📈 Graphe temporel : {graph_path}")

    # ----- 9) Boxplot avec epochs normalisées (0–20 %, ..., 80–100 %) -----
    n_epochs = 10  # nombre de tranches (0–20, 20–40, 40–60, 60–80, 80–100 %)

    t0 = df["t_seconds"].min()
    t1 = df["t_seconds"].max()
    duree = t1 - t0

    # Temps relatif entre 0 et 1
    df["rel_t"] = (df["t_seconds"] - t0) / duree

    # Epoch normalisée : 0,1,2,3,4
    df["epoch_norm"] = np.floor(df["rel_t"] * n_epochs).astype(int)
    df.loc[df["epoch_norm"] == n_epochs, "epoch_norm"] = n_epochs - 1  # sécurité sur le dernier point

    epochs = range(n_epochs)
    valeurs_par_epoch = [df[df["epoch_norm"] == e]["a_norm_filt"] for e in epochs]
    labels = [f"{int(e*100/n_epochs)}–{int((e+1)*100/n_epochs)}%" for e in epochs]

    plt.figure(figsize=(10, 5))
    plt.boxplot(valeurs_par_epoch, labels=labels)
    plt.xlabel("Fraction de la série (%)")
    plt.ylabel("a_norm filtrée (m/s²)")
    plt.title(f"Distribution de l'accélération (epochs normalisées) — {base_name}")
    plt.grid(True, axis="y")

    # Échelle Y automatique, comme avant
    y_max = auto_scale_y(df, step=0.2)
    plt.ylim(0, y_max)
    plt.yticks(np.arange(0, y_max + 0.001, 0.2))

    plt.tight_layout()

    boxplot_path = f"resultats/{base_name}_boxplot_normalise.png"
    plt.savefig(boxplot_path, dpi=200)
    plt.close()
    print(f"📊 Boxplot normalisé : {boxplot_path}")



        # ----- 10) Histogramme de la distribution de a_norm_filt -----

    plt.figure(figsize=(10, 5))
    plt.hist(df["a_norm_filt"], bins=30, edgecolor="black")
    plt.xlabel("a_norm (m/s²)")
    plt.ylabel("Fréquence")
    plt.title(f"Histogramme de la distribution — {base_name}")
    plt.grid(True, axis="y")

    hist_path = f"resultats/{base_name}_histogram.png"
    plt.savefig(hist_path, dpi=200)
    plt.close()
    print(f"📌 Histogramme : {hist_path}")


# --------------------------------------------------------
#          LISTE DES FICHIERS À ANALYSER
# --------------------------------------------------------
if __name__ == "__main__":

    fichiers = [
        "g-force1cheville",
        "g-force2cheville",
        "g-force3cheville",
        # change with data (cheville or poignet)

     
    ]

    for f in fichiers:
        analyse_fichier(f)
>>>>>>> Stashed changes
