from app.models import Auteur, Adherent, Ouvrage, Emprunt
from app.database import SessionLocal

from datetime import date, timedelta

aujourdhui = date.today()

def load_fixtures(): 
    with SessionLocal() as db: 
        # Réinitialisation des données 
        db.query(Adherent).delete() 
        db.query(Auteur).delete() 
        db.query(Ouvrage).delete()
        db.query(Emprunt).delete()
 
        hugo = Auteur(nom="Hugo", prenom="Victor", date_naissance=date(1802, 2, 26))
        camus = Auteur(nom="Camus", prenom="Albert", date_naissance=date(1913, 11, 7))
        christie = Auteur(nom="Christie", prenom="Agatha", date_naissance=date(1890, 9, 15))
        herbert = Auteur(nom="Herbert", prenom="Frank", date_naissance=date(1920, 10, 8))
        goscinny = Auteur(nom="Goscinny", prenom="René", date_naissance=date(1926, 8, 14))
        auteurs = [hugo, camus, christie, herbert, goscinny]
 
        ouvrages = [ 
            Ouvrage(titre="Les Misérables", isbn="9782070409228", annee_publication=1862, genre="Roman", auteur=hugo),
        Ouvrage(titre="Notre-Dame de Paris", isbn="9782070411573", annee_publication=1831, genre="Roman", auteur=hugo),
        Ouvrage(titre="Les Contemplations", isbn="9782070411580", annee_publication=1856, genre="Poésie", auteur=hugo),
        Ouvrage(titre="L'Étranger", isbn="9782070360024", annee_publication=1942, genre="Roman", auteur=camus),
        Ouvrage(titre="La Peste", isbn="9782070360420", annee_publication=1947, genre=None, auteur=camus),
        Ouvrage(titre="Le Crime de l'Orient-Express", isbn="9782253003083", annee_publication=1934, genre="Policier", auteur=christie),
        Ouvrage(titre="Dix petits nègres", isbn="9782253005438", annee_publication=1939, genre="Policier", auteur=christie),
        Ouvrage(titre="Dune", isbn="9782266320481", annee_publication=1965, genre="Science-fiction", auteur=herbert),
        Ouvrage(titre="Astérix le Gaulois", isbn="9782012101333", annee_publication=1961, genre="BD", auteur=goscinny),
        Ouvrage(titre="Le Petit Nicolas", isbn="9782070612888", annee_publication=1960, genre=None, auteur=goscinny),
        ]

        adherents = [
        Adherent(nom="Martin", prenom="Alice", email="alice.martin@mail.fr"),
        Adherent(nom="Bernard", prenom="Lucas", email="lucas.bernard@mail.fr"),
        Adherent(nom="Dubois", prenom="Emma", email="emma.dubois@mail.fr"),
        Adherent(nom="Petit", prenom="Hugo", email="hugo.petit@mail.fr"),
        Adherent(nom="Durand", prenom="Chloé", email="chloe.durand@mail.fr"),
        ]

            # --- Emprunts : date_retour vide = emprunt en cours ---
        def emprunt(adherent, ouvrage, il_y_a_jours, duree=21, rendu_apres=None):
            debut = aujourdhui - timedelta(days=il_y_a_jours)
            return Emprunt(
                adherent=adherent,
                ouvrage=ouvrage,
                date_emprunt=debut,
                duree=duree,
                date_retour=debut + timedelta(days=rendu_apres) if rendu_apres else None,
            )

        emprunts = [
            emprunt(adherents[0], ouvrages[0], 5),                           # en cours
            emprunt(adherents[0], ouvrages[7], 10, duree=14),                # en cours (2e emprunt d'Alice)
            emprunt(adherents[1], ouvrages[3], 40),                          # en cours et en retard (40 j > 21 j)
            emprunt(adherents[2], ouvrages[5], 2, duree=7),                  # en cours, très récent
            emprunt(adherents[2], ouvrages[6], 30, duree=14, rendu_apres=12),  # rendu
            emprunt(adherents[3], ouvrages[8], 15, duree=7, rendu_apres=9),    # rendu en retard (9 j > 7 j)
            emprunt(adherents[1], ouvrages[0], 60, duree=21, rendu_apres=18),  # rendu (même livre qu'Alice, plus ancien)
            # Chloé n'a aucun emprunt : cas d'un adhérent sans activité
        ]
 
        db.add_all(auteurs) 
        db.add_all(emprunts)
        db.add_all(ouvrages)
        db.add_all(adherents) 
        db.commit() 
 
        print("Fixtures chargées avec succès.") 
 
 
if __name__ == "__main__": 
    load_fixtures() 