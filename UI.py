import tkinter as tk
from instruction import Cursor
import math
from tkinter import ttk, filedialog, messagebox,simpledialog
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

        self.menu_fichier.add_command(label="Open folder", command=self.ouvrir_dossier)
        self.menu_fichier.add_command(label="New file",command=self.creer_fichier)
        self.menu_fichier.add_command(label="Save",command=self.enregistrer_fichier)
        self.menu_fichier.add_command(label="Delete",)
        self.menu_fichier.add_command(label="Remove Folder",command=self.supprimer_dossier)
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

    def gestion_fichier(self):
        self.frame_glob = tk.Frame(self.cadre_principal,bg="lightblue")
        self.cadre_principal.add(self.frame_glob)

        self.gest = ttk.Treeview(self.frame_glob)
        self.gest.pack(fill="both", expand=True)

        self.gest.bind("<<TreeviewSelect>>", self.afficher_fichier)

        # Bouton pour ouvrir un dossier
        self.btn_open = ttk.Button(self.frame_glob, text="Ouvrir un dossier", command=self.ouvrir_dossier)
        self.btn_open.pack(pady=20,padx=0)

        # Bouton pour supp un dossier
        self.btn_delete = ttk.Button(self.frame_glob, text="Supprimer", command=self.enregistrer_fichier)
        self.btn_delete.pack(pady=20,padx=0)

        # Configuration des colonnes et du style de l'arborescence
        self.gest.heading("#0", text="Folders", anchor="w")

    def ouvrir_dossier(self):

        self.folder_selected = filedialog.askdirectory()

        if self.folder_selected:
            self.root_node = self.gest.insert("", "end", text=os.path.basename(self.folder_selected), open=True)
            self.inserer_fichier(self.folder_selected, self.root_node)


    def inserer_fichier(self, parent_path, parent_node):

        try:
            for item in os.listdir(parent_path):

                self.item_path = os.path.join(parent_path, item)
                self.node = self.gest.insert(parent_node, "end", text=item, open=False)

                if os.path.isdir(self.item_path):
                    self.inserer_fichier(self.item_path, self.node)
        except :
            pass

    def supprimer_dossier(self,dos=""):
        self.selected_item = self.gest.focus()
        if self.selected_item:
            self.gest.delete(self.selected_item)

    def afficher_fichier(self, event):

        selected_item = self.gest.focus()  
        if not selected_item:
            return
        fichier_selectionne = os.path.join(self.folder_selected, self.gest.item(selected_item, "text"))
        if os.path.isfile(fichier_selectionne): 
            try:
                with open(fichier_selectionne, "r", encoding="utf-8") as f:
                    contenu = f.read()
                self.zone_texte.delete("1.0", "end")
                self.zone_texte.insert("1.0", contenu)
            except Exception as e:
                self.zone_texte.delete("1.0", "end")
                self.zone_texte.insert("1.0", f"Erreur lors de la lecture du fichier : {e}")
        else:
            self.zone_texte.delete("1.0", "end")
            self.zone_texte.insert("1.0", "Sélectionnez un fichier pour afficher son contenu.")


    def enregistrer_fichier(self):

        selected_item = self.gest.focus()  
        if not selected_item:
            messagebox.showerror("Erreur", "Aucun fichier sélectionné.")
            return

        fichier_selectionne = os.path.join(self.folder_selected, self.gest.item(selected_item, "text"))
        if os.path.isfile(fichier_selectionne):  
            try:
                contenu = self.zone_texte.get("1.0", "end").strip() 
                with open(fichier_selectionne, "w", encoding="utf-8") as f:
                    f.write(contenu)
                messagebox.showinfo("Succès", f"Fichier enregistré : {fichier_selectionne}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'enregistrer le fichier : {e}")
        else:
            messagebox.showerror("Erreur", "L'élément sélectionné n'est pas un fichier.")


    def creer_fichier(self):

        selected_item = self.gest.focus()

        if not selected_item:
            messagebox.showerror("Erreur", "Aucun dossier sélectionné.")
            return

        if os.path.isdir(self.folder_selected):  
            nom_fichier = simpledialog.askstring("Créer un fichier", "Nom du fichier (avec extension) :")
            if not nom_fichier:
                return 
            chemin_fichier = os.path.join(self.folder_selected, nom_fichier)
            try:
                with open(chemin_fichier, "w", encoding="utf-8") as fichier:
                    fichier.write("") 
                    
                #self.gest.insert(selected_item, "end", text=nom_fichier,open=False)
                #messagebox.showinfo("Succès", f"Fichier créé : {chemin_fichier}")
            except:
                print("erreur durant la création du fichier")
        else:
            messagebox.showerror("Erreur", "L'élément sélectionné n'est pas un dossier.")

   #Faire fonction récurcive pour recup l'id de ce que je veux dans le tree 
   #Soit on ajoute directement, soit on supp tt l'arbre et re affiche tt ?

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