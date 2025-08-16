import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def analyze_mouse_metrics(file_path):
    base = os.path.splitext(os.path.basename(file_path))[0]
    outdir = os.path.join(os.path.dirname(file_path), base + '_output')
    if not os.path.exists(outdir):
        os.makedirs(outdir)
    # Heatmap 2D des positions de la souris
    df = pd.read_csv(file_path)
    # Rapport statistique complet pour chaque colonne numérique
    stats = df.describe().T[['mean', 'std', 'min', 'max']].round(3)
    stats.to_csv(os.path.join(outdir, 'statistiques_completes.csv'))

    # Génération d'un histogramme pour chaque colonne numérique
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        plt.figure(figsize=(8,4))
        sns.histplot(df[col].dropna(), bins=50, kde=True, color='teal')
        plt.title(f'Distribution de {col}')
        plt.xlabel(col)
        plt.ylabel('Occurrences')
        plt.tight_layout()
        plt.savefig(os.path.join(outdir, f'hist_{col}.png'))
        plt.close()
    if 'x' in df.columns and 'y' in df.columns:
        plt.figure(figsize=(8,6))
        plt.hexbin(df['x'], df['y'], gridsize=60, cmap='inferno', mincnt=1)
        plt.colorbar(label='Densité')
        plt.title('Heatmap 2D des positions de la souris')
        plt.xlabel('x')
        plt.ylabel('y')
        plt.gca().invert_yaxis()
        plt.savefig(os.path.join(outdir, 'heatmap_positions.png'))
        plt.close()

    # Détection et marquage des flicks (pics de vitesse)
    if 'speed' in df.columns:
        flick_threshold = df['speed'].mean() + 2*df['speed'].std()
        flicks = df[df['speed'] > flick_threshold]
        plt.figure(figsize=(12,4))
        plt.plot(df['timestamp'], df['speed'], label='Vitesse')
        plt.scatter(flicks['timestamp'], flicks['speed'], color='red', label='Flicks détectés')
        plt.title('Détection des flicks (pics de vitesse)')
        plt.xlabel('Temps (s)')
        plt.ylabel('Vitesse (px/s)')
        plt.legend()
        plt.savefig(os.path.join(outdir, 'flicks_detection.png'))
        plt.close()

    # Détection d'anomalies (outliers sur la vitesse)
    if 'speed' in df.columns:
        q1 = df['speed'].quantile(0.25)
        q3 = df['speed'].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5*iqr
        upper = q3 + 1.5*iqr
        anomalies = df[(df['speed'] < lower) | (df['speed'] > upper)]
        if not anomalies.empty:
            print(f"\n🚨 {len(anomalies)} mouvements anormaux détectés (outliers vitesse)")
            anomalies[['timestamp','x','y','speed']].to_csv(os.path.join(outdir, 'anomalies.csv'), index=False)

    # Export PDF automatique du rapport (si matplotlib >=3.3)
    try:
        from matplotlib.backends.backend_pdf import PdfPages
        pdf_path = os.path.join(outdir, 'rapport_complet.pdf')
        with PdfPages(pdf_path) as pdf:
            for img in [
                'speed_distribution.png','precision_stability.png','correlation_heatmap.png',
                'fatigue_stress.png','bursts_micro.png','heatmap_positions.png',
                'flicks_detection.png','tracking_smoothness.png','chaos_metric.png','entropy_score.png']:
                img_path = os.path.join(outdir, img)
                if os.path.exists(img_path):
                    fig = plt.figure()
                    img_data = plt.imread(img_path)
                    plt.imshow(img_data)
                    plt.axis('off')
                    pdf.savefig(fig)
                    plt.close(fig)
        print(f"   • Rapport PDF exporté : {pdf_path}")
    except Exception as e:
        print(f"   • PDF non généré : {e}")

    print(f"\n📂 Analyse du fichier : {os.path.basename(file_path)}")
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"❌ Erreur de lecture : {e}")
        return
    print(f"   • {len(df)} lignes, {len(df.columns)} colonnes")
    print(f"   • Période : {df['timestamp'].min():.2f} à {df['timestamp'].max():.2f} s")

    # Statistiques globales
    print("\n📊 Statistiques principales :")
    print(df.describe().T[['mean', 'std', 'min', 'max']].round(3))

    # Corrélations principales
    print("\n🔗 Corrélations principales :")
    corr = df.corr(numeric_only=True)
    focus_cols = [c for c in ['speed','acceleration','flick_intensity','fatigue_index','stress_indicator','pixel_perfect_precision','stability_score','tracking_smoothness','micro_correction_ratio','target_acquisition_efficiency','overshoot_ratio','chaos_metric','entropy_score'] if c in df.columns]
    print(corr[focus_cols].sort_index().round(2))

    outdir = os.path.splitext(file_path)[0] + "_report"
    os.makedirs(outdir, exist_ok=True)

    # 1. Distribution de la vitesse
    plt.figure(figsize=(8,4))
    sns.histplot(df['speed'], bins=50, kde=True, color='royalblue')
    plt.title('Distribution de la vitesse (px/s)')
    plt.xlabel('Vitesse (px/s)')
    plt.ylabel('Occurrences')
    plt.savefig(os.path.join(outdir, 'speed_distribution.png'))
    plt.close()

    # 2. Précision et stabilité
    plt.figure(figsize=(10,4))
    plt.plot(df['timestamp'], df['pixel_perfect_precision'], label='Précision pixel')
    plt.plot(df['timestamp'], df['stability_score'], label='Stabilité')
    plt.legend()
    plt.title('Précision et stabilité dans le temps')
    plt.xlabel('Temps (s)')
    plt.ylabel('Score')
    plt.savefig(os.path.join(outdir, 'precision_stability.png'))
    plt.close()

    # 3. Heatmap des corrélations
    plt.figure(figsize=(14,12))
    sns.heatmap(corr, cmap='coolwarm', center=0, annot=True, fmt='.2f', cbar_kws={'shrink':.8})
    plt.title('Heatmap des corrélations')
    plt.savefig(os.path.join(outdir, 'correlation_heatmap.png'))
    plt.close()

    # 4. Fatigue et stress
    plt.figure(figsize=(10,4))
    plt.plot(df['timestamp'], df['fatigue_index'], label='Fatigue')
    plt.plot(df['timestamp'], df['stress_indicator'], label='Stress')
    plt.legend()
    plt.title('Fatigue et stress dans le temps')
    plt.xlabel('Temps (s)')
    plt.ylabel('Score')
    plt.savefig(os.path.join(outdir, 'fatigue_stress.png'))
    plt.close()

    # 5. Bursts et micro-mouvements
    plt.figure(figsize=(10,4))
    plt.plot(df['timestamp'], df['is_burst'].astype(int), label='Burst')
    plt.plot(df['timestamp'], df['micro_movement_count'], label='Micro-mouvements')
    plt.legend()
    plt.title('Bursts et micro-mouvements')
    plt.xlabel('Temps (s)')
    plt.ylabel('Valeur')
    plt.savefig(os.path.join(outdir, 'bursts_micro.png'))
    plt.close()

    # 6. Analyse dynamique : courbes de tracking, chaos, entropie
    if 'tracking_smoothness' in df.columns:
        plt.figure(figsize=(10,4))
        plt.plot(df['timestamp'], df['tracking_smoothness'], label='Tracking smoothness')
        plt.title('Tracking smoothness dans le temps')
        plt.xlabel('Temps (s)')
        plt.ylabel('Score')
        plt.savefig(os.path.join(outdir, 'tracking_smoothness.png'))
        plt.close()
    if 'chaos_metric' in df.columns:
        plt.figure(figsize=(10,4))
        plt.plot(df['timestamp'], df['chaos_metric'], label='Chaos metric')
        plt.title('Chaos metric dans le temps')
        plt.xlabel('Temps (s)')
        plt.ylabel('Score')
        plt.savefig(os.path.join(outdir, 'chaos_metric.png'))
        plt.close()
    if 'entropy_score' in df.columns:
        plt.figure(figsize=(10,4))
        plt.plot(df['timestamp'], df['entropy_score'], label='Entropy score')
        plt.title('Entropy score dans le temps')
        plt.xlabel('Temps (s)')
        plt.ylabel('Score')
        plt.savefig(os.path.join(outdir, 'entropy_score.png'))
        plt.close()

    # 7. Synthèse automatique des points forts/faibles
    print("\n🧠 Synthèse automatique :")
    if df['fatigue_index'].max() > 0.7:
        print("   • Fatigue détectée sur la session (fatigue_index élevé)")
    if df['stress_indicator'].max() > 0.7:
        print("   • Stress détecté sur la session (stress_indicator élevé)")
    if df['pixel_perfect_precision'].mean() > 0.8:
        print("   • Précision pixel globalement très bonne")
    if df['tracking_smoothness'].mean() < 0.5:
        print("   • Tracking peu fluide, travaillez la régularité")
    if df['chaos_metric'].mean() > 0.5:
        print("   • Mouvement chaotique, attention à la régularité")
    if df['entropy_score'].mean() > 0.7:
        print("   • Mouvement très imprévisible (entropie élevée)")
    print("   • Consultez les graphiques pour une analyse détaillée.")

    print(f"\n✅ Rapport généré dans : {outdir}")
    for f in os.listdir(outdir):
        print(f"   - {f}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("\nGlissez-déposez un ou plusieurs fichiers CSV sur ce script pour lancer l'analyse.")
        print("Ou lancez en ligne de commande : python interpret_mouse_metrics.py fichier1.csv fichier2.csv ...")
        sys.exit(0)
    # Analyse comparative multi-fichiers
    if len(sys.argv[1:]) > 1:
        print("\n📊 Analyse comparative multi-fichiers :")
        dfs = []
        names = []
        for file in sys.argv[1:]:
            if os.path.isfile(file):
                try:
                    df = pd.read_csv(file)
                    dfs.append(df)
                    names.append(os.path.basename(file))
                except Exception as e:
                    print(f"❌ Erreur lecture {file} : {e}")
        if len(dfs) >= 2:
            plt.figure(figsize=(10,5))
            for df, name in zip(dfs, names):
                if 'speed' in df.columns:
                    plt.plot(df['timestamp'], df['speed'], label=f"{name} (vitesse)", alpha=0.7)
            plt.legend()
            plt.title('Comparaison de la vitesse entre sessions')
            plt.xlabel('Temps (s)')
            plt.ylabel('Vitesse (px/s)')
            plt.savefig('comparaison_vitesse.png')
            plt.close()
            print("   • Graphique comparaison_vitesse.png généré")
    # Analyse individuelle
    for file in sys.argv[1:]:
        if os.path.isfile(file):
            analyze_mouse_metrics(file)
        else:
            print(f"❌ Fichier non trouvé : {file}")


def analyze_mouse_metrics(file_path):
    print(f"\n📂 Analyse du fichier : {os.path.basename(file_path)}")
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"❌ Erreur de lecture : {e}")
        return
    print(f"   • {len(df)} lignes, {len(df.columns)} colonnes")
    print(f"   • Période : {df['timestamp'].min():.2f} à {df['timestamp'].max():.2f} s")

    # Statistiques globales
    print("\n📊 Statistiques principales :")
    print(df.describe().T[['mean', 'std', 'min', 'max']].round(3))

    # Corrélations principales
    print("\n🔗 Corrélations principales :")
    corr = df.corr(numeric_only=True)
    print(corr[['speed', 'acceleration', 'flick_intensity', 'fatigue_index', 'stress_indicator']]
          .sort_index().round(2))

    # Visualisations rapides
    outdir = os.path.splitext(file_path)[0] + "_report"
    os.makedirs(outdir, exist_ok=True)

    # 1. Distribution de la vitesse
    plt.figure(figsize=(8,4))
    sns.histplot(df['speed'], bins=50, kde=True, color='royalblue')
    plt.title('Distribution de la vitesse (px/s)')
    plt.xlabel('Vitesse (px/s)')
    plt.ylabel('Occurrences')
    plt.savefig(os.path.join(outdir, 'speed_distribution.png'))
    plt.close()

    # 2. Précision et stabilité
    plt.figure(figsize=(10,4))
    plt.plot(df['timestamp'], df['pixel_perfect_precision'], label='Précision pixel')
    plt.plot(df['timestamp'], df['stability_score'], label='Stabilité')
    plt.legend()
    plt.title('Précision et stabilité dans le temps')
    plt.xlabel('Temps (s)')
    plt.ylabel('Score')
    plt.savefig(os.path.join(outdir, 'precision_stability.png'))
    plt.close()

    # 3. Heatmap des corrélations
    plt.figure(figsize=(12,10))
    sns.heatmap(corr, cmap='coolwarm', center=0)
    plt.title('Heatmap des corrélations')
    plt.savefig(os.path.join(outdir, 'correlation_heatmap.png'))
    plt.close()

    # 4. Fatigue et stress
    plt.figure(figsize=(10,4))
    plt.plot(df['timestamp'], df['fatigue_index'], label='Fatigue')
    plt.plot(df['timestamp'], df['stress_indicator'], label='Stress')
    plt.legend()
    plt.title('Fatigue et stress dans le temps')
    plt.xlabel('Temps (s)')
    plt.ylabel('Score')
    plt.savefig(os.path.join(outdir, 'fatigue_stress.png'))
    plt.close()

    # 5. Bursts et micro-mouvements
    plt.figure(figsize=(10,4))
    plt.plot(df['timestamp'], df['is_burst'].astype(int), label='Burst')
    plt.plot(df['timestamp'], df['micro_movement_count'], label='Micro-mouvements')
    plt.legend()
    plt.title('Bursts et micro-mouvements')
    plt.xlabel('Temps (s)')
    plt.ylabel('Valeur')
    plt.savefig(os.path.join(outdir, 'bursts_micro.png'))
    plt.close()

    print(f"\n✅ Rapport généré dans : {outdir}")
    print("   - speed_distribution.png")
    print("   - precision_stability.png")
    print("   - correlation_heatmap.png")
    print("   - fatigue_stress.png")
    print("   - bursts_micro.png")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("\nGlissez-déposez un ou plusieurs fichiers CSV sur ce script pour lancer l'analyse.")
        print("Ou lancez en ligne de commande : python interpret_mouse_metrics.py fichier1.csv fichier2.csv ...")
        sys.exit(0)
    for file in sys.argv[1:]:
        if os.path.isfile(file):
            analyze_mouse_metrics(file)
        else:
            print(f"❌ Fichier non trouvé : {file}")
