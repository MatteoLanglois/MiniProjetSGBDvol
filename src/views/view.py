import tkinter as vtk
from tkinter import RAISED


"""
Classe view

Cette classe représente la vue principale de l'application. Elle est utilisée
pour définir les éléments graphiques communs à toutes les vues de l'application.

Elle hérite de la classe Frame de tkinter.
"""


class view(vtk.Frame):
    """
    Méthode __init__

    Constructeur de la classe view
    """
    def __init__(self, parent, controller):
        vtk.Frame.__init__(self, parent)
        self.controller = controller
        self.title = "Le Bon Angle"

    """
    Méthode init_header
    
    Cette méthode permet d'initialiser l'en-tête de la vue. Elle est utilisée
    dans quasiment toutes les autres vues de l'application.    
    """
    def init_header(self):
        from src.views import viewMain
        label_title = vtk.Label(self, self.font_style("title"),
                                text="Le Bon Angle", anchor='center')
        label_title.grid(column=0, row=1, columnspan=5, pady=10, padx=10,
                         sticky='n')

        button_home = vtk.Button(self, self.button_style(), text="Retour",
                                 command=lambda: self.controller.show_frame(
                                     viewMain.ViewMain))
        button_home.grid(column=0, row=0, pady=10, padx=10, sticky='w')

        '''
        if self.controller.is_connected:
            button_account = vtk.Button(self, self.button_style(),
                                        text="Mon compte",
                                        command=lambda:
                                        self.controller.show_frame(
                                            viewAccount.viewAccount))
            button_account.grid(column=9, row=0, pady=10, padx=10)
            button_deconnexion = vtk.Button(self, self.button_style(),
                                            text="Déconnexion",
                                            command=lambda:
                                            self.controller.disconnect())
            button_deconnexion.grid(column=10, row=0, pady=10, padx=10)
        else:
            button_connexion = vtk.Button(self, self.button_style(),
                                          text="Connexion",
                                          command=lambda:
                                          self.controller.show_frame(
                                              viewConnexion.ViewConnexion))
            button_connexion.grid(column=10, row=0, pady=10, padx=10)
        '''

    """
    Méthode button_style
    
    Cette méthode permet de définir le style des boutons de l'application.
    """
    @staticmethod
    def button_style() -> dict:
        return {'borderwidth': 1, 'relief': RAISED, 'background': 'white',
                'activebackground': 'white',
                'cursor': 'hand2'} | view.font_style("button")

    """
    Méthode font_style
    
    Cette méthode permet de définir le style des éléments textuels de
    l'application. Elle prend en paramètre le type de texte à styliser.
    
    @param font_type: str
    """
    @staticmethod
    def font_style(font_type: str) -> dict:
        switcher = {
            'title': 24,
            'subtitle': 16,
            'button': 16,
            'label': 12
        }
        font_size = switcher.get(font_type, 12)
        return {'font': ('Bell MT', font_size),
                'foreground': 'black'}

    """
    Méthode entry_style
    
    Cette méthode permet de définir le style des champs de saisie de 
    l'application.
    """
    @staticmethod
    def entry_style() -> dict:
        return {'borderwidth': 1, 'relief': RAISED, 'background': 'white',
                'cursor': 'hand2'} | view.font_style("subtitle")
