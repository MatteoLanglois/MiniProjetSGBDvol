from src.view.view import view
import tkinter as vtk
from src.views import viewInscription


"""
Classe viewConnexion

Vue permettant à l'utilisateur de se connecter. Elle hérite de la classe view.
"""


class ViewConnexion(view):
    """
    Méthode __init__

    Constructeur de la classe viewConnexion
    """
    def __init__(self, parent, controller):
        vtk.Frame.__init__(self, parent)
        self.controller = controller
        self.init_widget()
        self.title = "Se connecter"

    """
    Méthode init_widget
    
    Méthode permettant d'initialiser les widgets de la vue
    """
    def init_widget(self):
        label_titre = vtk.Label(self, self.font_style("title"), text="Connexion")
        label_titre.grid()

        label_login = vtk.Label(self, self.font_style("label"), text="Email")
        label_login.grid()

        entry_login = vtk.Entry(self, self.entry_style())
        entry_login.grid(padx=10, pady=10)

        label_password = vtk.Label(self, self.font_style("label"),
                                   text="Password")
        label_password.grid()

        entry_password = vtk.Entry(self, self.entry_style(), show="*")
        entry_password.grid(padx=10, pady=10)
        entry_password.bind('<Return>', lambda event: self.controller.connect(
            entry_login.get(), entry_password.get()))

        button_connexion = vtk.Button(self, self.button_style(),
                                      text="Connexion",
                                      command=lambda:
                                      self.controller.connect(
                                          entry_login.get(),
                                          entry_password.get()))
        button_connexion.grid(padx=10, pady=10)

        label_inscription = vtk.Label(self, self.font_style("label"),
                                      text="Pas encore inscrit ?")
        label_inscription.grid(padx=10, pady=10)

        button_inscription = vtk.Button(self, self.button_style(),
                                        text="Inscription",
                                        command=
                                        lambda:
                                        self.controller.show_frame(
                                            viewInscription.viewInscription))
        button_inscription.grid(padx=10, pady=10)
