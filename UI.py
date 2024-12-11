import tkinter as tk
import math
from tkinter import ttk, filedialog, messagebox,simpledialog
import os

from instruction import Cursor
from execute import execute
from parseur import instrctions_listed,parseur


class Application:
    def __init__(self, root):
        # Initialisation of the main window
        self.root = root
        self.root.title("IDE for DRAW ++")
        self.root.geometry("1000x600")
                
        self.dossier_racine = {}

        self.menu()
        self.app()


    #Menu de l'IDE
    def menu(self):

        self.menu_barre = tk.Menu(self.root)
        self.root.config(menu=self.menu_barre)

        # File menu
        self.menu_fichier = tk.Menu(self.menu_barre, tearoff=0)
        self.menu_barre.add_cascade(label="Fichier", menu=self.menu_fichier)
        self.menu_fichier.add_command(label="Open folder", command=self.ouvrir_dossier)
        self.menu_fichier.add_command(label="New file",command=self.creer_fichier)
        self.menu_fichier.add_command(label="Save",command=self.enregistrer_fichier)
        self.menu_fichier.add_command(label="Delete File", command=self.supprimer_fichier)
        self.menu_fichier.add_command(label="Remove Folder",command=self.supprimer_dossier)
        self.menu_fichier.add_separator()
        self.menu_fichier.add_command(label="Quitter", command=self.root.quit)

        # Help menu
        self.menu_help = tk.Menu(self.menu_barre, tearoff=0)
        self.menu_barre.add_cascade(label="Help", menu=self.menu_help)

    def app(self):

        self.cadre_1 = tk.PanedWindow(self.root,orient="vertical")
        self.cadre_1.pack(fill="both", expand=True)

        # Main frame for the arrengement of widgets
        self.cadre_2 = tk.PanedWindow(self.root,orient="horizontal")
        self.cadre_2.pack(fill="both", expand=True)
        self.cadre_1.add(self.cadre_2)

        self.gestion_fichier()
        self.gestion_text()
        self.zone_canva()

    #Zone canva pour déssiner
    def zone_canva(self):
        self.canevas = tk.Canvas(self.cadre_1, bg="white", width=500, height=500)
        self.cadre_1.add(self.canevas)

        #Pour gerer le déplacement dans le canvas
        self.canevas.bind("<ButtonPress-1>", self.start_drag)  
        self.canevas.bind("<B1-Motion>", self.drag) 
        self.canevas.bind("<MouseWheel>", self.zoom)

    #Zone de texte pour l'IDE
    def gestion_text(self):

        self.zone_texte = tk.Text(self.cadre_2, wrap="word", width=40)
        self.cadre_2.add(self.zone_texte)

        button_exe = tk.Button(self.zone_texte,text="Lancer",command=self.executer_code)
        button_exe.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    #Fonction pour éxécuter le code dans la zone de texte
    def executer_code(self):

        #Récupe le code
        code = self.zone_texte.get("1.0", tk.END).strip()
        if not code:
            messagebox.showerror("Erreur", "Veuillez écrire du code avant d'exécuter.")
            return

        try:
            self.canevas.delete("all")

            context={"canvas": self.canevas}

            toks = instrctions_listed(code)
            tokens = parseur(toks)
            
            for token in tokens:

                if "error" in token:
                    messagebox.showerror("Erreur", token["error"])
                    return

                #Si il y a bien un ast dans le token on reenvoie
                context = execute(token["ast"], context)
                
                if "error" in context :
                    messagebox.showerror("Erreur", context["error"])
                    return
             

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'exécution : {e}")
            

    #Gestionnaire d'affichage des dossiers et fichier
    def gestion_fichier(self):
        self.frame_glob = tk.Frame(self.cadre_2,bg="white")
        self.cadre_2.add(self.frame_glob)

        self.treeview_window = ttk.Treeview(self.frame_glob)
        self.treeview_window.pack(fill="both", expand=True)

        self.treeview_window.bind("<<TreeviewSelect>>", self.afficher_fichier)

        self.treeview_window.heading("#0", text="Folders", anchor="w")

    
    #Menu pour selectionner un dossier et l'ouvrire
    def ouvrir_dossier(self):

        folder_selected = filedialog.askdirectory()

        if folder_selected:
            base = self.treeview_window.insert("", "end", text=os.path.basename(folder_selected), open=True)
            self.dossier_racine[base] = folder_selected
            self.inserer_fichier(folder_selected, base)


    #Inserer de facon récurcive un fichier dans le gestionnaire de fichier
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


    #Permet d'afficher un fichier dans la zone de texte
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

    #Permet d'enregistrer une fichier
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

    def supprimer_fichier(self):
        selected_item = self.treeview_window.focus()  # Obtenir l'élément sélectionné
        if not selected_item:
            messagebox.showerror("Erreur", "Aucun fichier sélectionné.")
            return

        chemin_fichier = self.dossier_racine[selected_item]

        if os.path.isfile(chemin_fichier):
            confirmation = messagebox.askyesno("Confirmation", f"Voulez-vous supprimer le fichier {chemin_fichier} ?")
            if confirmation:
                try:
                    os.remove(chemin_fichier)  # Supprimer le fichier
                    self.treeview_window.delete(selected_item)  # Supprimer du Treeview
                    del self.dossier_racine[selected_item]  # Retirer du dictionnaire
                    messagebox.showinfo("Succès", "Fichier supprimé avec succès.")
                except Exception as e:
                    messagebox.showerror("Erreur", f"Erreur lors de la suppression : {e}")
        else:
            messagebox.showerror("Erreur", "L'élément sélectionné n'est pas un fichier.")


    # 3 fonctions qui gèrent le déplacement sur le canvas
    def start_drag(self,event):
        try : self.canevas.scan_mark(event.x, event.y)
        except: pass

    def drag(self,event):
        try : self.canevas.scan_dragto(event.x, event.y, gain=1)
        except: pass

    def zoom(self,event):

        global scale

        if event.delta > 0:
            scale *= 1.1

        elif event.delta < 0:
            scale *= 0.9

        self.canevas.scale("all", event.x, event.y, scale, scale)
        self.canevas.configure(scrollregion=self.canevas.bbox("all"))


if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()

