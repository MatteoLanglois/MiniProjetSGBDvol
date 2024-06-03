from src.views.view import view
import tkinter as vtk
import src.model as db

"""
Classe viewAccount

Vue permettant à l'utilisateur de changer son mot de passe et de voir ses 
réservations. Elle hérite de la classe view.
"""


class viewAccount(view):
    """
    Méthode __init__

    Constructeur de la classe viewAccount
    """
    def __init__(self, parent, controller):
        vtk.Frame.__init__(self, parent)
        self.controller = controller
        self.init_widget()
        self.label_error = None
        self.title = "Mon compte"

    def init_widget(self):
        self.init_header()

        if self.controller.is_connected:
            frame_mdp = vtk.Frame(self, bd=1, relief=vtk.RIDGE)
            # Changement de mot de passe
            label_change_password = vtk.Label(frame_mdp, self.font_style("subtitle"),
                                              text="Changer de mot de passe")
            label_change_password.grid(padx=10)

            label_old_password = vtk.Label(frame_mdp, self.font_style("label"),
                                           text="Ancien mot de passe")
            label_old_password.grid(padx=10)
            entry_old_password = vtk.Entry(frame_mdp, self.entry_style(), show="*")
            entry_old_password.grid(padx=10)

            label_new_password = vtk.Label(frame_mdp, self.font_style("label"),
                                           text="Nouveau mot de passe")
            label_new_password.grid(padx=10)
            entry_new_password = vtk.Entry(frame_mdp, self.entry_style(), show="*")
            entry_new_password.grid(padx=10)

            label_confirm_password = vtk.Label(frame_mdp, self.font_style("label"),
                                               text="Confirmer le mot de passe")
            label_confirm_password.grid(padx=10)
            entry_confirm_password = vtk.Entry(frame_mdp, self.entry_style(),
                                               show="*")
            entry_confirm_password.grid(padx=10)

            button_change_password = vtk.Button(frame_mdp, self.button_style(),
                                                text="Changer de mot de passe",
                                                command=lambda: self.change_password(
                                                    entry_old_password.get(),
                                                    entry_new_password.get(),
                                                    entry_confirm_password.get()))
            button_change_password.grid(padx=10, pady=10)

            self.label_error = vtk.Label(frame_mdp, self.font_style("label"),
                                         text="")
            self.label_error.grid()

            frame_mdp.grid(padx=10, pady=10)

            # Réservations
            frame_reservations = vtk.Frame(self, bd=1, relief=vtk.RIDGE)
            label_reservations = vtk.Label(frame_reservations, self.font_style("subtitle"),
                                           text="Mes réservations")
            label_reservations.grid(padx=10)

            reservations = db.Reservation.get_by_user(self.controller.userConnected)
            listbox_reservations = vtk.Listbox(frame_reservations, selectmode=vtk.SINGLE, width=100,
                                                  height=10, font=self.font_style("subtitle"))
            listbox_reservations.grid(padx=10)

            for reservation in reservations:
                listbox_reservations.insert(vtk.END, reservation)



    """
    Méthode change_password
    
    Méthode permettant de changer le mot de passe de l'utilisateur.
    """
    def change_password(self, old_password: str, new_password: str,
                        new_password_confirm: str):
        if new_password != new_password_confirm:
            self.label_error.config(text="Les mots de passe ne correspondent "
                                         "pas")
        elif not db.User.try_connect(self.controller.userConnected.mailUser,
                                     old_password):
            self.label_error.config(text="Mot de passe incorrect")
        else:
            self.controller.userConnected.mdpUser = db.User.hashPassword(
                new_password)
            self.label_error.config(text="Mot de passe changé avec succès")
            db.session.commit()

