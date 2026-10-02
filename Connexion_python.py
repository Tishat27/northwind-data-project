"""
Created on Thu Oct  1 23:55:16 2026

@author: Tishat27
"""

import os
import time

import pandas as pd
import sqlalchemy
from dotenv import load_dotenv

# Charge le contenu du fichier .env
load_dotenv()

# Récupère les variables de manière sécurisée
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")


def mesurer_temps(fonction):
    def wrapper(*args, **kwargs):
        debut = time.time()
        resultat = fonction(*args, **kwargs)
        fin = time.time()
        delai = fin - debut
        print(f"Le délai d'exécution est de {delai:.4f} secondes.")
        return resultat

    return wrapper

# ==========================================
# VERSION 1 : PROCÉDURALE (Fonction seule)
# ==========================================

@mesurer_temps
def recuperer_top_commandes(db_url: str) -> pd.DataFrame:
    # 1 Définnir la reqête
    requete_sql = """WITH best_order AS(
      SELECT e.employee_id,o.order_id, e.last_name, e.first_name, 
      ROUND(SUM(od.unit_price*(1-od.discount)*od.quantity)::numeric, 2) AS order_value
     
       FROM orders o
       JOIN order_details od ON o.order_id=od.order_id
       JOIN employees e ON o.employee_id=e.employee_id
       GROUP BY o.order_id,e.employee_id),
       --Possible de faire un seul CTE en remplaçant order_value par son calcul directement dans le RANK
       rank_data AS(
       SELECT bo.employee_id,bo.order_id, bo.last_name, bo.first_name,bo.order_value,
      RANK() OVER (PARTITION BY bo.employee_id ORDER BY bo.order_value DESC) AS order_rank
       FROM best_order bo)
       
       SELECT rd.employee_id, rd.last_name, rd.first_name,rd.order_id,order_rank,rd.order_value
     
       FROM rank_data rd
       WHERE order_rank<=2
       ORDER BY rd.employee_id,order_rank;"""

    # 2 Crééer la connexion avec l'URL de connexion
    engine = sqlalchemy.create_engine(db_url)

    # 3 Charger le résultat dans pandas
    df_top_commandes = pd.read_sql(requete_sql, con=engine)

    # afficher les résultats
    return df_top_commandes


# Construit l'URL dynamiquement
db_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

df_resultat = recuperer_top_commandes(db_url)

print("\n--- Aperçu des résultats ---")
print(df_resultat.head(10))


# ==========================================
# VERSION 2 : POO (Orientée Objet avec Classe)
# ==========================================

class NorthwindtopOrder :
    def __init__(self):
        """Initialise la connexion à la base de données automatiquement."""
        DB_USER = os.getenv("DB_USER")
        DB_PASSWORD = os.getenv("DB_PASSWORD")
        DB_HOST = os.getenv("DB_HOST")
        DB_PORT = os.getenv("DB_PORT")
        DB_NAME = os.getenv("DB_NAME")
        
        #  Crééer la connexion avec l'URL de connexion

        self.db_url = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        
        
        self.engine = sqlalchemy.create_engine(self.db_url)
        
        
    @mesurer_temps
    def recuperer_top_commandes(self) -> pd.DataFrame:
        # 1 Définnir la reqête
        requete_sql = """WITH best_order AS(
          SELECT e.employee_id,o.order_id, e.last_name, e.first_name, 
          ROUND(SUM(od.unit_price*(1-od.discount)*od.quantity)::numeric, 2) AS order_value
         
           FROM orders o
           JOIN order_details od ON o.order_id=od.order_id
           JOIN employees e ON o.employee_id=e.employee_id
           GROUP BY o.order_id,e.employee_id),
           --Possible de faire un seul CTE en remplaçant order_value par son calcul directement dans le RANK
           rank_data AS(
           SELECT bo.employee_id,bo.order_id, bo.last_name, bo.first_name,bo.order_value,
          RANK() OVER (PARTITION BY bo.employee_id ORDER BY bo.order_value DESC) AS order_rank
           FROM best_order bo)
           
           SELECT rd.employee_id, rd.last_name, rd.first_name,rd.order_id,order_rank,rd.order_value
         
           FROM rank_data rd
           WHERE order_rank<=2
           ORDER BY rd.employee_id,order_rank;"""
       

        # 3 Charger le résultat dans pandas
        df_top_commandes = pd.read_sql(requete_sql, con=self.engine)

        # afficher les résultats
        return df_top_commandes




Order=NorthwindtopOrder()


df_resultat = Order.recuperer_top_commandes()

print("\n--- Aperçu des résultats ---")
print(df_resultat.head(10))




































