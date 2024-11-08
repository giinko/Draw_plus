import tkinter as tk
from instruction import Cursor
import math

class Application:
    def __init__(self, root):
        # Initialisation de la fenêtre principale
        self.root = root
        self.root.title("Application Tkinter avec une Classe")
        self.root.geometry("1000x600")
        
        # Création du canvas et de l'instance Cursor
        self.canvas = tk.Canvas(self.root, width=800, height=400, bg="white")
        self.canvas.pack(pady=20)
        self.cursor = Cursor(self.canvas, x=400, y=200)  # Centre du canevas
        
        # Ajout des widgets
        self.creer_widgets()
    
    def creer_widgets(self):
        
        # Boutons pour manipuler le "curseur" (Cursor)
        self.bt1 = tk.Button(self.root, text="Avancer", command=lambda: self.cursor.move_forward(50))
        self.bt1.pack(side="left", padx=5, pady=10)
        
        self.bt2 = tk.Button(self.root, text="Tourner 90°", command=lambda: self.cursor.rotate(90))
        self.bt2.pack(side="left", padx=5, pady=10)
        
        self.bt3 = tk.Button(self.root, text="Dessiner un cercle", command=lambda: self.cursor.draw_circle(30))
        self.bt3.pack(side="left", padx=5, pady=10)


# Création de la fenêtre principale et lancement de l'application
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
