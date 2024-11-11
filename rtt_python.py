import time
import csv
import subprocess
from datetime import datetime
import os

# Configuration
url = "weather.com"  # Changez ceci par l'URL souhaitée
output_file = os.path.join(os.getcwd(), "rtt_metrics_python_v2.csv")  # Crée le fichier dans le répertoire courant
total_runs = 72  # 24 heures * 3 fois par heure (toutes les 20 minutes)

# Initialisation du fichier CSV avec point-virgule comme délimiteur
with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerow(["Timestamp", "RTT (ms)"])

# Mesurer le RTT toutes les 20 minutes
for i in range(total_runs):
    # Capturer l'heure actuelle
    current_time = datetime.now().strftime('%H:%M')

    # Mesurer le RTT avec ping
    try:
        output = subprocess.check_output(["ping", "-n", "1", url], stderr=subprocess.STDOUT, universal_newlines=True)
        # Extraire le temps de réponse du résultat
        rtt_line = [line for line in output.splitlines() if "temps=" in line or "time=" in line]
        if rtt_line:
            # Pour Windows, il faut chercher "temps="
            if "temps=" in rtt_line[0]:
                rtt = rtt_line[0].split("temps=")[1].split("ms")[0].strip()
            else:  # Pour les systèmes Unix-like, utiliser "time="
                rtt = rtt_line[0].split("time=")[1].split("ms")[0].strip()
        else:
            rtt = "N/A"
    except subprocess.CalledProcessError:
        rtt = "N/A"

    # Enregistrer les résultats dans le fichier CSV
    with open(output_file, mode='a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow([current_time, rtt])

    # Afficher un message dans la console
    print(f"Entrée ajoutée: {current_time}, RTT: {rtt} ms")

    # Attendre 20 minutes avant la prochaine mesure
    time.sleep(1200)

print("Collecte des métriques RTT terminée.")

