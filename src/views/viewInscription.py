from src.views import viewConnexion
from src.views.view import view
import tkinter as vtk
import src.model as db

"""
Classe viewInscription

Vue permettant de s'inscrire
"""


class viewInscription(view):
    """
    Méthode __init__

    Constructeur de la classe
    """
    def __init__(self, parent, controller):
        vtk.Frame.__init__(self, parent)
        self.controller = controller
        self.init_widget()
        self.label_error = None
        self.title = "Inscription"

    """
    Méthode init_widget
    
    Méthode permettant d'initialiser les widgets de la vue
    """
    def init_widget(self):
        self.init_header()

        label_titre = vtk.Label(self, self.font_style("title"),
                                text="Inscription")
        label_titre.grid(column=0, row=0, columnspan=5, pady=10, padx=10,
                         sticky='n')

        self.label_error = vtk.Label(self, self.font_style("label"),
                                     text="")
        self.label_error.grid(column=0, row=1, pady=10, padx=10)

        label_prenom = vtk.Label(self, self.font_style("label"), text="Prenom")
        label_prenom.grid(column=0, row=2, pady=10, padx=10)

        entry_prenom = vtk.Entry(self, self.entry_style())
        entry_prenom.grid(column=1, row=2, pady=10, padx=10)

        label_nom = vtk.Label(self, self.font_style("label"), text="Nom")
        label_nom.grid(column=0, row=3, pady=10, padx=10)

        entry_nom = vtk.Entry(self, self.entry_style())
        entry_nom.grid(column=1, row=3, pady=10, padx=10)

        label_login = vtk.Label(self, self.font_style("label"), text="Email")
        label_login.grid(column=0, row=4, pady=10, padx=10)

        entry_login = vtk.Entry(self, self.entry_style())
        entry_login.grid(column=1, row=4, pady=10, padx=10)

        label_password = vtk.Label(self, self.font_style("label"),
                                   text="Mot de passe")
        label_password.grid(column=0, row=5, pady=10, padx=10)

        entry_password = vtk.Entry(self, self.entry_style(), show="*")
        entry_password.grid(column=1, row=5, pady=10, padx=10)

        label_password_confirm = vtk.Label(self, self.font_style("label"),
                                           text="Confirmer le mot de passe")
        label_password_confirm.grid(column=0, row=6, pady=10, padx=10)

        entry_password_confirm = vtk.Entry(self, self.entry_style(), show="*")
        entry_password_confirm.grid(column=1, row=6, pady=10, padx=10)

        label_ville = vtk.Label(self, self.font_style("label"), text="Ville")
        label_ville.grid(column=3, row=2, pady=10, padx=10)

        entry_ville = vtk.Entry(self, self.entry_style())
        entry_ville.grid(column=4, row=2, pady=10, padx=10)

        label_code_postal = vtk.Label(self, self.font_style("label"),
                                      text="Code postal")
        label_code_postal.grid(column=3, row=3, pady=10, padx=10)

        entry_code_postal = vtk.Entry(self, self.entry_style())
        entry_code_postal.grid(column=4, row=3, pady=10, padx=10)

        label_rue = vtk.Label(self, self.font_style("label"), text="Rue")
        label_rue.grid(column=3, row=4, pady=10, padx=10)

        entry_rue = vtk.Entry(self, self.entry_style())
        entry_rue.grid(column=4, row=4, pady=10, padx=10)

        label_numero = vtk.Label(self, self.font_style("label"), text="Numéro")
        label_numero.grid(column=3, row=5, pady=10, padx=10)

        entry_numero = vtk.Entry(self, self.entry_style())
        entry_numero.grid(column=4, row=5, pady=10, padx=10)

        label_complement = vtk.Label(self, self.font_style("label"), text="Complément")
        label_complement.grid(column=3, row=6, pady=10, padx=10)

        entry_complement = vtk.Entry(self, self.entry_style())
        entry_complement.grid(column=4, row=6, pady=10, padx=10)

        button_inscription = vtk.Button(self, self.button_style(),
                                        text="Inscription",
                                        command=lambda:
                                        self.inscription(
                                            entry_prenom.get(),
                                            entry_nom.get(),
                                            entry_login.get(),
                                            entry_password.get(),
                                            entry_password_confirm.get(),
                                            entry_ville.get(),
                                            entry_code_postal.get(),
                                            entry_rue.get(),
                                            entry_numero.get(),
                                            entry_complement.get())
                                        )
        button_inscription.grid(column=3, row=7, padx=10, pady=10)

    """
    Méthode inscription
    
    Méthode permettant de s'inscrire
    """
    def inscription(self, prenom: str, nom: str, email: str, password: str,
                    password_confirm: str, ville: str, code_postal: str,
                    rue: str, numero: str, complement: str):
        if password != password_confirm:
            self.label_error.config(
                text="Les mots de passe ne correspondent pas")
            return
        if db.User.getByEmail(email) is not None:
            self.label_error.config(text="Cet email est déjà utilisé")
            return
        if (not prenom or not nom or not email or not password or not ville
                or not code_postal or not rue or not numero):
            self.label_error.config(text="Veuillez remplir tous les champs")
            return
        new_adresse = db.Adresse(ville, code_postal, rue, numero, complement)
        db.session.add(new_adresse)
        db.session.commit()

        new_user = db.User(prenom, nom, email, password)
        new_user.adresseUser = new_adresse.idAdresse
        db.session.add(new_user)

        db.session.commit()
        self.controller.connect(email, password)
