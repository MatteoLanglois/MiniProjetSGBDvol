"""
Fonction main

Fonction principale de l'application
"""
from src.app.app import VolApp


def main():
    app = VolApp()
    app.mainloop()


if __name__ == '__main__':
    main()
