import tkinter as tk
from instruction import Cursor
import math
from tkinter import ttk, filedialog, messagebox
import os

class Application:
    def __init__(self, root):
        # Initialisation de la fenêtre principale
        self.root = root
        self.root.title("IDE for DRAW ++")
        self.root.geometry("1000x600")
        
        # Création du canvas et de l'instance Cursor
        #self.canvas = tk.Canvas(self.root, width=800, height=400, bg="white")
        #self.canvas.grid(row=0,column=1)
        
        self.menu()

        self.app()
        #self.cursor = Cursor(self.canvas_droit, x=400, y=200)
        #self.cursor.move_forward(50)


    def menu(self):

        self.menu_barre = tk.Menu(self.root)
        self.root.config(menu=self.menu_barre)

        #Menu fichier
        self.menu_fichier = tk.Menu(self.menu_barre, tearoff=0)
        self.menu_barre.add_cascade(label="Fichier", menu=self.menu_fichier)

        self.menu_fichier.add_command(label="Ouvrir", )
        self.menu_fichier.add_command(label="Enregistrer",)
        self.menu_fichier.add_command(label="Effacer",)
        self.menu_fichier.add_separator()
        self.menu_fichier.add_command(label="Quitter", command=self.root.quit)

        #Menu help
        self.menu_fichier = tk.Menu(self.menu_barre, tearoff=0)
        self.menu_barre.add_cascade(label="Help", menu=self.menu_fichier)

    def app(self):
        # Cadre principal pour la disposition des widgets
        self.cadre_principal = tk.PanedWindow(self.root,orient="horizontal")
        self.cadre_principal.pack(fill="both", expand=True)


        
        self.gestion_fichier()
        self.gestion_text()
    
    def gestion_text(self):
        # Zone de texte à droite
        self.zone_texte = tk.Text(self.cadre_principal, wrap="word", width=40)
        self.cadre_principal.add(self.zone_texte)
        self.run_btn = tk.Button(self.zone_texte,text="RUN",command="")
        self.run_btn.pack(side="left")

    def gestion_fichier(self):
        self.frame_glob = tk.Frame(self.cadre_principal,bg="lightblue")
        self.cadre_principal.add(self.frame_glob)

        self.gest = ttk.Treeview(self.frame_glob)
        self.gest.pack(fill="both", expand=True)

        # Bouton pour ouvrir un dossier
        self.btn_open = ttk.Button(self.frame_glob, text="Ouvrir un dossier", command=self.open_directory)
        self.btn_open.pack(pady=20,padx=0)

        # Bouton pour supp un dossier
        self.btn_delete = ttk.Button(self.frame_glob, text="Supprimer", command=self.supp_dossier)
        self.btn_delete.pack(pady=20,padx=0)

        # Configuration des colonnes et du style de l'arborescence
        self.gest.heading("#0", text="Folders", anchor="w")

    def open_directory(self):

        self.folder_selected = filedialog.askdirectory()

        if self.folder_selected:
            self.root_node = self.gest.insert("", "end", text=os.path.basename(self.folder_selected), open=True)
            self.insert_files(self.folder_selected, self.root_node)


    def insert_files(self, parent_path, parent_node):

        try:
            for item in os.listdir(parent_path):

                self.item_path = os.path.join(parent_path, item)
                self.node = self.gest.insert(parent_node, "end", text=item, open=False)

                if os.path.isdir(self.item_path):
                    self.insert_files(self.item_path, self.node)
        except :
            pass

    def supp_dossier(self):
        self.selected_item = self.gest.focus()
        if self.selected_item:
            self.gest.delete(self.selected_item)


    def amelioration_plus_tard(self):
        self.scrollbar = tk.Scrollbar(self.zone_texte)
        self.scrollbar.pack(side="right", fill="y")
        self.zone_texte.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.zone_texte.yview)

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


"""
a faire ensuite : 
    - lier la zone de texte et le fichier 
    - 

"""