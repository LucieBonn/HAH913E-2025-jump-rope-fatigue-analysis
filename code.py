# # === Importation des bibliothèques ===
# #import os                    # gestion des chemins de fichiers
# #import pandas as pd           # manipulation de données
# #import numpy as np            # calculs numériques
# #import matplotlib.pyplot as plt  # visualisation
# #from scipy.signal import butter, filtfilt  # filtrage du signal


# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# import os

# path = r"data/Bomane1_corde_poignetdroit.csv"  # adapte si besoin

# # 1) Lecture robuste : auto-détection du séparateur
# try:
#     df = pd.read_csv(path, header=None, sep=None, engine="python")  # Sniffer
# except Exception:
#     # fallback si Sniffer échoue
#     df = pd.read_csv(path, header=None)

# # 2) Si une seule colonne a été lue, tenter différents séparateurs courants
# if df.shape[1] == 1:
#     for sep_try in [";", ",", "\t", "|"]:
#         df_try = pd.read_csv(path, header=None, sep=sep_try)
#         if df_try.shape[1] >= 3:  # on veut au moins ax, ay, az
#             df = df_try
#             break

# # 3) Vérifier le nombre de colonnes et nommer proprement
# #   Cas standard attendu : 5 colonnes -> date, heure, ax, ay, az
# if df.shape[1] == 5:
#     df.columns = ["date", "heure", "ax", "ay", "az"]
# #   Cas alternatif : 4 colonnes -> une seule colonne temporelle + 3 axes
# elif df.shape[1] == 4:
#     df.columns = ["datetime_raw", "ax", "ay", "az"]
#     # découpe possible si datetime est "date heure" séparé par un espace
#     # sinon on gardera datetime_raw tel quel
# else:
#     raise ValueError(f"Format inattendu : {df.shape[1]} colonnes lues.\n"
#                      f"Inspectez les premières lignes du CSV pour connaître sa structure.")

# # 4) Construire le temps
# if "date" in df.columns and "heure" in df.columns:
#     df["datetime"] = pd.to_datetime(df["date"] + " " + df["heure"], dayfirst=True, errors="coerce")
# elif "datetime_raw" in df.columns:
#     df["datetime"] = pd.to_datetime(df["datetime_raw"], dayfirst=True, errors="coerce")
# else:
#     raise ValueError("Impossible de construire la colonne datetime.")

# # 5) Nettoyage lignes sans datetime parsable
# df = df.dropna(subset=["datetime"]).reset_index(drop=True)

# # 6) Conversion numérique des axes (au cas où)
# for c in ["ax", "ay", "az"]:
#     df[c] = pd.to_numeric(df[c], errors="coerce")
# df = df.dropna(subset=["ax", "ay", "az"]).reset_index(drop=True)

# # 7) Calcul de la norme + lissage simple
# df["a_norm"] = np.sqrt(df["ax"]**2 + df["ay"]**2 + df["az"]**2)
# df["a_norm_filt"] = df["a_norm"].rolling(window=5, center=True, min_periods=1).mean()

# # ---- Indicateurs ----
# moyenne    = df["a_norm_filt"].mean()
# ecart_type = df["a_norm_filt"].std()
# rms        = np.sqrt(np.mean(df["a_norm_filt"]**2))
# max_val    = df["a_norm_filt"].max()

# print("----- Indicateurs généraux -----")
# print(f"Moyenne : {moyenne:.3f} m/s²")
# print(f"Écart-type : {ecart_type:.3f} m/s²")
# print(f"RMS : {rms:.3f} m/s²")
# print(f"Max : {max_val:.3f} m/s²")

# # ---- Graphe temporel en SECONDES (unique tracé) ----
# start_time = df["datetime"].iloc[0]
# time_seconds = (df["datetime"] - start_time).dt.total_seconds()

# plt.figure(figsize=(10,5))
# plt.plot(time_seconds, df["a_norm_filt"], linewidth=1)
# plt.xlabel("Temps écoulé (s)")
# plt.ylabel("Accélération totale (m/s²)")
# plt.title("Accélération totale pendant l'exercice (filtrée)")
# plt.grid(True)
# plt.tight_layout()

# # Sauvegarde dans le dossier resultats/
# output_path = os.path.join("resultats", "Bomane1_corde_poignetdroit_graph.png")
# plt.savefig(output_path, dpi=200)
# plt.show()

# print(f"\n✅ Graphique sauvegardé dans : {output_path}")


# ## ajout code ENMO
# def compute_enmo(df):
#     norm = np.sqrt(df['x']**2 + df['y']**2 + df['z']**2)
#     df['enmo'] = norm - 1  # keep negative values
#     return df
# df = compute_enmo(df)
# df.head()

# def aggregate_enmo_gmin(df, epoch_length):
#     df['epoch'] = (df['t'] // epoch_length).astype(int)
#     aggregated = df.groupby('epoch')['enmo'].sum().reset_index()
#     aggregated['enmo_gmin'] = aggregated['enmo'] * (epoch_length / 60)  # correct factor
#     aggregated['time_min'] = aggregated['epoch'] * epoch_length / 60
#     return aggregated

# aggregated_10s = aggregate_enmo_gmin(df, epoch_length=10)   # visualisation epoch 10s 

# df['time_min'] = df['t'] / 60  # convert seconds to minutes
# fig, axs = plt.subplots(2, 1, figsize=(12, 8))

# # Bar plot: ENMO aggregated
# axs[0].bar(aggregated_10s['time_min'], aggregated_10s['enmo_gmin'], width=0.15, color='grey')
# axs[0].set_title('ENMO integrated over 10.0 s intervals')
# axs[0].set_ylabel('Integrated ENMO (g·min)')
# axs[0].set_xlabel('Time (minutes)')
# axs[0].axhline(0, color='black', linewidth=0.8)

# # Line plot: raw ENMO
# axs[1].plot(df['time_min'], df['enmo'], color='steelblue')
# axs[1].set_title('Raw ENMO over Time')
# axs[1].set_xlabel('Time (minutes)')
# axs[1].set_ylabel('ENMO (g)')
# axs[1].axhline(0, color='black', linewidth=0.8)

# plt.tight_layout()
# plt.savefig('enmo_epoch_10s.png')
# plt.show()