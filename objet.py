import db

class Cave : 

    def __init__(self, id = 0 ,  nb_etagere = 0, localisation = "unknown", nom = "unknown"):
        self.nb_etagere = nb_etagere
        self.localisation = localisation
        self.nom = nom
        self.id = id
    
    def new_cave(self):
        connection = db.connect_db()
        cursor = connection.cursor()
        cursor.execute(db.sql_new_cave(self.nb_etagere, self.localisation, self.nom))
        connection.commit()
        row = cursor.execute(db.sql_recup_id_new_cave())
        id_new_cave = db.adapte(row)[0][0]
        for num in range(1, int(self.nb_etagere)+1):
            cursor.execute(db.sql_new_etagere("unknown", "0", "0", id_new_cave, num))
            connection.commit()
        connection.close()
        #print("dans new_cave de objet :", id_new_cave)
        return id_new_cave
    
    def linked_etagere(self):
        connection = db.connect_db()
        cursor = connection.cursor()
        row = cursor.execute(db.sql_list_etagere(self.id))
        data = db.adapte(row)
        print(data)
    
    def del_cave(self):
        connection = db.connect_db()
        cursor = connection.cursor()
        cursor.execute(db.sql_remove_all_etageres(self.id))
        connection.commit()
        cursor.execute(db.sql_unpossessed_cave(self.id))
        connection.commit()
        cursor.execute(db.sql_remove_cave(self.id))
        connection.commit()
        connection.close()
        #print("dans new_cave de objet :", id_new_cave)

class Etagère :
    def __init__(self, num, region, disponibilite, capacite, id_etagere):
        self.num = num
        self.region = region
        self.disponibilite = disponibilite
        self.capacite = capacite
        self.id = id_etagere

class Vin :
    def __init__(self, domaine, nom, type, année, region, commentaires, note_perso, photo, prix):
        self.domaine = domaine
        self.nom = nom
        self.type = type
        self.année = année
        self.region = region
        self.commentaire = commentaires
        self.note_perso = note_perso
        self.photo = photo
        self.prix = prix

class User :
    def __init__(self, nom = "unknown", prenom = "unknown", login = "unknown", mdp = "unknown", id = 0):
        self.nom = nom
        self.prenom = prenom
        self.login = login
        self.mdp = mdp
        self.id = id

    def check_login_dispo(self, login):
        connection = db.connect_db()
        cursor = connection.cursor()
        row = cursor.execute(db.sql_check_dispo(login))
        data = db.adapte(row)
        connection.close()
        return data

    def check_personnalite(self, prenom, nom):
            connection = db.connect_db()
            cursor = connection.cursor()
            row = cursor.execute(db.sql_check_perso(nom, prenom))
            data = db.adapte(row)
            connection.close()
            return data

    def inscryption(self, nom, prenom, login, mdp):
        connection = db.connect_db()
        cursor = connection.cursor()
        cursor.execute(db.sql_new_user(login, mdp, nom, prenom))
        connection.commit()
        connection.close()
    
    def verification(self, login, mdp):
        connection = db.connect_db()
        cursor = connection.cursor()
        row = cursor.execute(db.sql_authentification(login, mdp))
        data = db.adapte(row)
        connection.close()
        return data

    def identification(self, nom, prenom, id):
        self.nom = nom
        self.prenom = prenom
        self.id = id

    def caves_perso(self):
        connection = db.connect_db()
        cursor = connection.cursor()
        row = cursor.execute(db.sql_list_cave(self.id))
        data = db.adapte(row)
        connection.close()
        caves_trouvees = []
        for cave in range(len(data)) :  
            cave_actuelle = [data[cave][3], data[cave][4], data[cave][5], data[cave][1]]
            caves_trouvees.append(cave_actuelle)
        #print("ici : ", caves_trouvees)
        return caves_trouvees
    
    def link_cave(self, id_cave):
        connection = db.connect_db()
        cursor = connection.cursor()
        cursor.execute(db.sql_link_cave(self.id, id_cave))
        connection.commit()
        connection.close()
        return 0
