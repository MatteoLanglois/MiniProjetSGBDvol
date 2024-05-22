from tkinter import ttk
import tkinter as vtk
from tkinter.messagebox import *
from src.views import (viewMain, viewConnexion, viewInscription)
import src.model as db

"""
Classe VolApp

Classe principale de l'application
"""


class VolApp(vtk.Tk):
    """
    Méthode __init__

    Constructeur de la classe VolApp
    """

    def __init__(self):
        vtk.Tk.__init__(self)
        self.title("Vol")
        self.is_connected = False
        self.user = None
        self.frame = None
        container = ttk.Frame(self)
        container.pack(side="top", fill="both", expand=False)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        self.frames = {}
        for F in (viewMain.ViewMain, viewConnexion.ViewConnexion,
                  viewInscription.viewInscription):
            frame = F(container, self)
            frame.place(x=0, y=0, anchor="nw", width=400, height=300)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        self.show_frame(viewMain.ViewMain)

        """
    Méthode show_frame
    
    Méthode permettant d'afficher un frame et de l'initialiser à la bonne taille
    """

    def show_frame(self, cont) -> None:
        # clear the old frame
        for frame in self.frames.values():
            for widget in frame.winfo_children():
                widget.destroy()

        # reduce the size of the window
        self.geometry("1x1")

        # init the new frame
        self.frame = cont
        self.frames[cont].init_widget()
        frame = self.frames[cont]
        frame.tkraise()
        self.title = frame.title

        self.update_idletasks()

        self.geometry(f"{frame.winfo_reqwidth()}x{frame.winfo_reqheight()}")
        self.update_idletasks()
        self.update()

    """
    Méthode connect
    
    Méthode permettant de connecter un utilisateur
    """

    def connect(self, mail: str, password: str) -> None:
        self.userConnected = db.User.try_connect(mail, password)
        if self.userConnected is not None:
            self.is_connected = True
            self.show_frame(viewMain.ViewMain)
            print(self.is_connected)
        else:
            self.is_connected = False
            self.error_message("Erreur", "Erreur de connexion")

    """
    Méthode disconnect
    
    Méthode permettant de déconnecter un utilisateur
    """

    def disconnect(self) -> None:
        self.userConnected = None
        self.is_connected = False
        self.show_frame(viewConnexion.ViewConnexion)

    """
    Méthode is_connected
    
    Méthode permettant de savoir si un utilisateur est connecté.
    """

    def is_connected(self) -> bool:
        return self.is_connected

    """
    Méthode error_message
    
    Méthode permettant d'afficher un message d'erreur
    """

    @staticmethod
    def error_message(title: str, message: str):
        showerror(title, message)

    """
    Méthode cancel_function
    
    Méthode permettant d'annuler une action
    """

    @staticmethod
    def cancel_function(controller):
        titre = "Annuler"
        question = "Etes vous sûr de vouloir annuler"
        if askyesno(titre, question):
            controller.show_frame(viewMain.ViewMain)
        else:
            pass

    """
    Méthode disconnect_message
    
    Méthode permettant d'afficher un message de déconnexion
    """

    @staticmethod
    def disconnect_message():
        titre = "Déconnexion"
        question = "Voulez vous vraiment vous déconnecter ?"
        if askyesno(titre, question):
            quit()
        else:
            pass

    """
    Méthode wip
    
    Méthode permettant d'afficher un message de fonctionnalité en cours
    de développement
    """

    @staticmethod
    def wip():
        titre = "Work in progress"
        question = "Cette fonctionnalité n'est pas encore implémentée"
        showwarning(titre, question)


"""
Fonction main

Fonction principale de l'application
"""


def main():
    app = VolApp()
    app.mainloop()


if __name__ == '__main__':
    main()
