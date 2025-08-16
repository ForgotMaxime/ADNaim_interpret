# ADNaim_interpret
# Mouse Data Analyzer – Guide Complet

Ce dossier contient des outils avancés pour analyser les mouvements de souris à partir de fichiers CSV très complets. Vous trouverez ici :
- `ultra_complete_analyzer.py` : un script d'analyse avancée.
- `interpret_mouse_metrics.py` : un script d'interprétation et de visualisation des données.
- Un exemple de fichier de données : `ultra_complete_mouse_data_20250816_033909.csv`.

## 1. Comment utiliser les scripts ?

### a) Analyse automatique

1. Placez vos fichiers CSV dans ce dossier.
2. Ouvrez un terminal dans ce dossier.
3. Lancez l'analyse :
   ```powershell
   python interpret_mouse_metrics.py votre_fichier.csv
   ```
4. Un dossier de résultats sera créé pour chaque fichier, contenant :
   - Des graphiques (PNG)
   - Un rapport statistique (CSV)
   - Un rapport PDF (si activé)
   - Un résumé des anomalies et des points clés

### b) Fonctionnement général
- Les scripts lisent toutes les colonnes du CSV.
- Ils produisent des statistiques, des visualisations et des alertes automatiques.
- Les résultats sont exportés dans un dossier dédié par fichier analysé.

## 2. Guide pédagogique des metrics

Chaque ligne du CSV représente un échantillon de mouvement de souris. Voici la signification de chaque metric, comment l’interpréter, et ce qui est considéré comme "bon" ou "mauvais" selon le contexte (précision, fluidité, performance, etc.).

### Position et déplacement
- **timestamp** : Temps (en secondes) depuis le début de l’enregistrement.
- **x, y** : Position de la souris à l’écran (pixels).
- **dx, dy** : Déplacement instantané en x et y (pixels).
- **distance** : Distance parcourue entre deux points (pixels).
- **path_length** : Longueur totale du chemin parcouru.
- **net_displacement** : Distance droite entre le point de départ et d’arrivée.
- **straightness** : Rapport net_displacement/path_length (1 = ligne droite, <1 = chemin sinueux).
- **tortuosity** : Mesure de la sinuosité du chemin (plus c’est élevé, plus le chemin est tordu).
- **deviation_from_ideal** : Écart par rapport à la trajectoire idéale.
- **path_efficiency** : Efficacité du chemin (1 = parfait, <1 = détours inutiles).
- **detour_ratio** : Ratio de détours (plus c’est élevé, moins c’est optimal).

### Vitesse et accélération
- **speed** : Vitesse instantanée (pixels/seconde). Haute = rapide, trop haute = perte de contrôle.
- **velocity_x, velocity_y, velocity_magnitude** : Composantes de la vitesse.
- **dpi_normalized_speed, cm_per_second, inches_per_second** : Vitesse normalisée selon la résolution.
- **acceleration, acceleration_x, acceleration_y, acceleration_magnitude** : Accélération instantanée.
- **hz_corrected_acceleration** : Accélération corrigée selon la fréquence d’échantillonnage.
- **centripetal_acceleration** : Accélération lors des virages.
- **jerk, jerk_x, jerk_y, jerk_magnitude** : Variation de l’accélération (mesure de la brutalité du mouvement).

### Direction et trajectoire
- **direction** : Angle du mouvement (radian).
- **angular_velocity** : Vitesse de rotation (radian/s).
- **angular_acceleration** : Accélération angulaire.
- **curvature** : Courbure du chemin.
- **direction_change** : Variation d’angle entre deux points.
- **bearing** : Direction absolue.
- **heading_stability** : Stabilité de la direction (1 = stable).

### Contrôle, pauses et fréquence
- **time_since_last** : Temps écoulé depuis le dernier échantillon.
- **time_since_start** : Temps depuis le début.
- **pause_duration** : Durée des pauses.
- **movement_frequency** : Fréquence des mouvements (Hz).
- **sampling_rate** : Fréquence d’échantillonnage (Hz).
- **is_moving, is_accelerating, is_decelerating, is_paused, is_burst, is_smooth, is_jerky, is_turning** : Indicateurs booléens d’état du mouvement.

### Précision et stabilité
- **pixel_perfect_precision** : Précision du mouvement (1 = parfait, <1 = imprécis).
- **sub_pixel_accuracy** : Précision sous le pixel.
- **stability_score** : Stabilité du mouvement (1 = très stable).
- **steadiness** : Régularité du mouvement.
- **drift_rate** : Tendance à dévier.
- **noise_level** : Niveau de bruit (parasites).

### Tremblements et micro-mouvements
- **tremble_rms, tremble_amplitude, tremble_frequency** : Mesures du tremblement de la main.
- **dominant_frequency, frequency_spectrum_peak** : Fréquence dominante du mouvement.
- **oscillation_index** : Indice d’oscillation.
- **hand_tremor_score** : Score global de tremblement.
- **micro_movement_count** : Nombre de micro-mouvements.

### Variabilité et robustesse
- **speed_variance, direction_variance, position_variance, acceleration_variance** : Variabilité des metrics.
- **speed_median, speed_percentile_95** : Valeurs médianes et extrêmes de la vitesse.
- **flick_intensity** : Intensité des mouvements brusques (flicks).
- **tracking_smoothness** : Fluidité du suivi (1 = très fluide).
- **micro_correction_ratio** : Proportion de micro-corrections.
- **target_acquisition_efficiency** : Efficacité pour atteindre une cible.
- **overshoot_ratio** : Tendance à dépasser la cible.

### Fatigue, stress et rythme
- **fatigue_index** : Indice de fatigue (0 = repos, 1 = très fatigué).
- **stress_indicator** : Indice de stress (0 = calme, 1 = stressé).
- **rhythm_consistency** : Régularité du rythme.

### Habitudes et biais
- **hand_dominance_bias** : Biais de main (gauche/droite).
- **grip_stability_estimate** : Stabilité de la prise en main.
- **screen_zone, distance_from_center, edge_proximity, quadrant, relative_position_x, relative_position_y** : Position relative sur l’écran.
- **repetitive_pattern_score, habit_strength, predictability_index** : Mesures d’habitude et de prévisibilité.

### Complexité et chaos
- **chaos_metric** : Mesure du chaos dans le mouvement (0 = régulier, 1 = chaotique).
- **entropy_score** : Entropie du mouvement (0 = prévisible, 1 = imprévisible).

### Qualité du signal
- **signal_to_noise_ratio** : Rapport signal/bruit.
- **bandwidth_usage, spectral_centroid, zero_crossing_rate, energy_density** : Mesures de la qualité et de la richesse du signal.
- **data_quality_score** : Score global de qualité des données.
- **outlier_probability** : Probabilité d’être un point aberrant.
- **confidence_level** : Confiance dans la mesure.

## 3. Comment interpréter les valeurs ?

- **Précision (pixel_perfect_precision, stability_score, tracking_smoothness)** :
  - Proche de 1 = excellent contrôle.
  - <0.7 = à améliorer.
- **Fatigue/Stress (fatigue_index, stress_indicator)** :
  - <0.3 = reposé/calme.
  - >0.7 = fatigué/stressé.
- **Vitesse/accélération** :
  - Trop élevé = perte de contrôle possible.
  - Trop bas = manque de réactivité.
- **Tremblements (tremble_rms, hand_tremor_score)** :
  - Faible = main stable.
  - Élevé = tremblements, fatigue ou stress.
- **Chaos/Entropie (chaos_metric, entropy_score)** :
  - <0.3 = mouvement régulier.
  - >0.7 = mouvement imprévisible ou chaotique.
- **Path efficiency, straightness** :
  - Proche de 1 = chemin optimal.
  - <0.7 = beaucoup de détours.

## 4. Conseils d’analyse
- Comparez vos résultats à différentes sessions pour voir votre progression.
- Surveillez les indicateurs de fatigue et de stress pour éviter la sur-sollicitation.
- Un bon joueur combine précision, fluidité, et faible chaos/entropie.
- Utilisez les graphiques générés pour repérer les pics, anomalies ou tendances.

## 5. Ressources complémentaires
- Les scripts sont extensibles : vous pouvez ajouter vos propres analyses ou visualisations.
- Pour toute question ou suggestion, ouvrez une issue ou contactez le développeur.

---

Ce guide est conçu pour rendre l’analyse des metrics accessible, pédagogique et exploitable, même sans expertise technique. Bonne analyse !
