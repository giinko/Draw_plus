import tkinter as tk
from instruction import Cursor
import math
from tkinter import ttk, filedialog, messagebox,simpledialog
import os
from t_parseur import tokenize,parse,parse_block
from execute import execute
from test12 import instrctions_listed,parseur_2


class Application:
    def __init__(self, root):
        # Initialisation of the main window
        self.root = root
        self.root.title("IDE for DRAW ++")
        self.root.geometry("1000x600")
                
        self.dossier_racine = {}

        self.menu()
        self.app()



    def menu(self):

        self.menu_barre = tk.Menu(self.root)
        self.root.config(menu=self.menu_barre)

        # File menu
        self.menu_fichier = tk.Menu(self.menu_barre, tearoff=0)
        self.menu_barre.add_cascade(label="Fichier", menu=self.menu_fichier)
        self.menu_fichier.add_command(label="Open folder", command=self.ouvrir_dossier)
        self.menu_fichier.add_command(label="New file",command=self.creer_fichier)
        self.menu_fichier.add_command(label="Save",command=self.enregistrer_fichier)
        self.menu_fichier.add_command(label="Delete",)
        self.menu_fichier.add_command(label="Remove Folder",command=self.supprimer_dossier)
        self.menu_fichier.add_separator()
        self.menu_fichier.add_command(label="Quitter", command=self.root.quit)

        # Help menu
        self.menu_help = tk.Menu(self.menu_barre, tearoff=0)
        self.menu_barre.add_cascade(label="Help", menu=self.menu_help)

    def app(self):

        self.fen = tk.PanedWindow(self.root,orient="vertical")
        self.fen.pack(fill="both", expand=True)

        # Main frame for the arrengement of widgets
        self.cadre_principal = tk.PanedWindow(self.root,orient="horizontal")
        self.cadre_principal.pack(fill="both", expand=True)

        self.gestion_fichier()
        self.gestion_text()
        self.fen.add(self.cadre_principal)
        self.zone_canva()

    def zone_canva(self):
        # Area of the canevas on the right
        self.canevas = tk.Canvas(self.fen, bg="white", width=500, height=500)
        self.fen.add(self.canevas)


    def gestion_text(self):
        # Area of the text on the right
        self.zone_texte = tk.Text(self.cadre_principal, wrap="word", width=40)
        self.cadre_principal.add(self.zone_texte)

        button_exe = tk.Button(self.zone_texte,text="Lancer",command=self.executer_code2)
        button_exe.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)


    def executer_code2(self):

        # Recover the code written by the user
        code = self.zone_texte.get("1.0", tk.END).strip()
        if not code:
            messagebox.showerror("Erreur", "Veuillez écrire du code avant d'exécuter.")
            return

        # Analyze and execution
        try:

            self.canevas.delete("all")
            cursor = Cursor(self.canevas, x=100, y=100, color="red", thickness=2)

            context={"canvas": self.canevas,"cursor" : cursor}

            toks = instrctions_listed(code)
            toks2 = parseur_2(toks)
            print(toks2)
            for token in toks2:
                if "error" in token:
                    messagebox.showerror("Erreur", token["error"])
                    return

                # Execution on the canevas
                context = execute(token["ast"], context)

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'exécution : {e}")
            print("erreur")


    def gestion_fichier(self):
        self.frame_glob = tk.Frame(self.cadre_principal,bg="lightblue")
        self.cadre_principal.add(self.frame_glob)

        self.treeview_window = ttk.Treeview(self.frame_glob)
        self.treeview_window.pack(fill="both", expand=True)

        self.treeview_window.bind("<<TreeviewSelect>>", self.afficher_fichier)

        # Style
        self.treeview_window.heading("#0", text="Folders", anchor="w")

    # Open the menu to select the folder to open
    def ouvrir_dossier(self):

        folder_selected = filedialog.askdirectory()

        if folder_selected:
            base = self.treeview_window.insert("", "end", text=os.path.basename(folder_selected), open=True)
            self.dossier_racine[base] = folder_selected
            self.inserer_fichier(folder_selected, base)



    # Allow us to insert a file in the treeview
    def inserer_fichier(self, parent_path, parent_node):

        try:
            for item in os.listdir(parent_path):
                chemin_item = os.path.join(parent_path, item)
                noeud = self.treeview_window.insert(parent_node, "end", text=item, open=False)
                self.dossier_racine[noeud] = chemin_item
                if os.path.isdir(chemin_item):
                    self.inserer_fichier(chemin_item, noeud)
        except :
            pass

    # Allow us to remove a folder/file of the treeview
    # SUPP DANS DOSSIER RACINE NE PAS OUBLIER ! 
    def supprimer_dossier(self,dos=""):
        selected_item = self.treeview_window.focus()
        if selected_item:
            self.treeview_window.delete(selected_item)


    # Allow to display the file in the text area
    def afficher_fichier(self, event):

        selected_item = self.treeview_window.focus()  

        if not selected_item:
            return

        fichier_selectionne = self.dossier_racine[selected_item]

        if os.path.isfile(fichier_selectionne): 
            try:
                with open(fichier_selectionne, "r", encoding="utf-8") as f:
                    contenu = f.read()
                self.zone_texte.delete("1.0", "end")
                self.zone_texte.insert("1.0", contenu)
        #Voir pour traiter les erreurs différament, mais pour le moment c'est bon
            except Exception as e:
                self.zone_texte.delete("1.0", "end")
                self.zone_texte.insert("1.0", f"Erreur lors de la lecture du fichier : {e}")


    def enregistrer_fichier(self):

        selected_item = self.treeview_window.focus() 

        if not selected_item:
            messagebox.showerror("Erreur", "Aucun fichier sélectionné.")
            return

        chemin_fichier = self.dossier_racine[selected_item]
        
        if os.path.isfile(chemin_fichier):  
            try:
                contenu = self.zone_texte.get("1.0", "end").strip() 
                with open(chemin_fichier, "w", encoding="utf-8") as f:
                    f.write(contenu)
                messagebox.showinfo("Succès", f"Fichier enregistré : {self.treeview_window.item(selected_item, "text")}")
            except Exception as e:
                messagebox.showerror("Erreur", f"Impossible d'enregistrer le fichier : {e}")
        else:
            messagebox.showerror("Erreur", "L'élément sélectionné n'est pas un fichier.")


    def creer_fichier(self):

        selected_item = self.treeview_window.focus()

        if not selected_item:
            messagebox.showerror("Erreur", "Aucun dossier sélectionné.")
            return

        chemin_dos = self.dossier_racine[selected_item]
        if os.path.isdir(chemin_dos):  
            nom_fichier = simpledialog.askstring("Créer un fichier", "Nom du fichier (avec extension) :")
            if not nom_fichier:
                return 
            chemin_fichier = os.path.join(chemin_dos, nom_fichier)
            try:
                with open(chemin_fichier, "w", encoding="utf-8") as fichier:
                    fichier.write("") 
                

                noeud = self.treeview_window.insert(selected_item, "end", text=nom_fichier, open=False)
                self.dossier_racine[noeud] = chemin_fichier

                messagebox.showinfo("Succès", f"Fichier créé : {nom_fichier}")
            
            except:
                print("erreur durant la création du fichier")
        else:
            messagebox.showerror("Erreur", "L'élément sélectionné n'est pas un dossier.")



# Creation of the main window and launch the application
if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()

