import tkinter as tk
import math
from tkinter import ttk, filedialog, messagebox,simpledialog
import os
import time
import subprocess

from instruction import Cursor
from execute import execute
from parseur import instrctions_listed,parseur
from generate_c import write_c_file,generate_c_code


class Application:
    def __init__(self, root):
        # Initialisation of the main window
        self.root = root
        self.root.title("IDE for DRAW ++")
        self.root.geometry("1213x750")
                
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
        self.menu_fichier.add_command(label="Compile file",command=self.comp_c)
        self.menu_fichier.add_separator()
        self.menu_fichier.add_command(label="Quitter", command=self.root.quit)

        # Canvas menu
        self.menu_fichier = tk.Menu(self.menu_barre, tearoff=0)
        self.menu_barre.add_cascade(label="Canvas", menu=self.menu_fichier)
        self.menu_fichier.add_command(label="Animate", command=self.animate_canvas)
        self.menu_fichier.add_separator()
        self.menu_fichier.add_command(label="Zoom in", command=self.zoom_in)
        self.menu_fichier.add_command(label="Zoom out", command=self.zoom_out)
        self.menu_fichier.add_command(label="Turn right", command=print())
        self.menu_fichier.add_command(label="Turn left", command=print())
        self.menu_fichier.add_separator()
        self.menu_fichier.add_command(label="Full screen", command=self.canvas_fullscreen)
        self.menu_fichier.add_command(label="Exit Full screen", command=self.restore_layout)

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

        self.zone_erreurs = tk.Text(self.cadre_1, height=0, bg="lightgray", state="disabled", wrap="word")
        self.zone_erreurs.tag_config("error", foreground="red")
        self.cadre_1.add(self.zone_erreurs)
        #self.zone_erreurs.pack(fill="x", padx=5, pady=5)

        self.cadre_1.paneconfig(self.cadre_2, stretch="always", minsize=100)
        self.cadre_1.paneconfig(self.zone_erreurs, stretch="never", minsize=100)

    #Zone canva pour déssiner
    def zone_canva(self):
        self.canevas = tk.Canvas(self.cadre_1, bg="white", width=500, height=200)
        self.cadre_1.add(self.canevas)

        self.button_zoomin = tk.Button(self.canevas,text="+",command=self.zoom_in)
        self.button_zoomin.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-50)

        self.button_zoomout = tk.Button(self.canevas,text="--",command=self.zoom_out)
        self.button_zoomout.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

        self.scale = 1
        self.is_fullscreen = False
        #Pour gerer le déplacement dans le canvas
        self.canevas.bind("<ButtonPress-1>", self.start_drag)  
        self.canevas.bind("<B1-Motion>", self.drag) 

    #Zone de texte pour l'IDE
    def gestion_text(self):

        self.zone_texte = tk.Text(self.cadre_2, height=100,wrap="word", width=40)
        self.cadre_2.add(self.zone_texte)

        button_exe = tk.Button(self.zone_texte,text="Lancer",command=self.executer_code)
        button_exe.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)

    #Fonction pour éxécuter le code dans la zone de texte
    def executer_code(self,timer=None):

        #Récupe le code
        code = self.zone_texte.get("1.0", tk.END).strip()
        if not code:
            messagebox.showerror("Erreur", "Veuillez écrire du code avant d'exécuter.")
            return

        try:
            self.canevas.delete("all")

            if timer:
                time.sleep(timer)
                self.canevas.update()

            context={"canvas": self.canevas}

            toks = instrctions_listed(code)
            tokens = parseur(toks)
            
            for token in tokens:

                if "error" in token:
                    self.afficher_erreur(token["error"])
                    continue

                #Si il y a bien un ast dans le token on reenvoie
                context = execute(token["ast"], context, timer)
                                
                if "error" in context :
                    #messagebox.showerror("Erreur", context["error"])
                    self.afficher_erreur(context["error"])
                        
            self.afficher_erreur("[Finished]")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de l'exécution : {e}")
            

    def afficher_erreur(self, message, ligne=None):
        self.zone_erreurs.config(state="normal")
        if ligne:
            self.zone_erreurs.insert("end", f"Ligne {ligne}: {message}\n", "error")
        else:
            self.zone_erreurs.insert("end", f"{message}\n", "error")
        self.zone_erreurs.config(state="disabled")

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


    #2 fonctions qui gèrent le déplacement sur le canvas
    def start_drag(self,event):
        try : self.canevas.scan_mark(event.x, event.y)
        except: pass

    def drag(self,event):
        try : self.canevas.scan_dragto(event.x, event.y, gain=1)
        except: pass


    # Fonction de zoom avant
    def zoom_in(self):
        new_scale = self.scale * 1.1  # Calculer la nouvelle échelle
        self.apply_zoom(new_scale)

    # Fonction de zoom arrière
    def zoom_out(self):
        new_scale = self.scale / 1.1  # Calculer la nouvelle échelle
        self.apply_zoom(new_scale)

    # Appliquer le zoom
    def apply_zoom(self, new_scale):
        if not self.canevas.bbox("all"):  # Si le canvas est vide, rien à zoomer
            return

        # Calculer le facteur de transformation
        scale_factor = new_scale / self.scale
        self.scale = new_scale  # Mettre à jour l'échelle actuelle

        # Calculer le centre du canvas
        bbox = self.canevas.bbox("all")
        x_center = (bbox[2] + bbox[0]) / 2
        y_center = (bbox[3] + bbox[1]) / 2

        # Appliquer le facteur de zoom
        self.canevas.scale("all", x_center, y_center, scale_factor, scale_factor)
        self.canevas.configure(scrollregion=self.canevas.bbox("all"))


    # Mettre le canvas en plein écran
    def canvas_fullscreen(self):
        if not self.is_fullscreen:
            self.cadre_1.remove(self.cadre_2)  
            self.cadre_1.remove(self.zone_erreurs)  
            self.canevas.pack(fill="both", expand=True)  
            self.is_fullscreen = True

    # Restaurer la mise en page initiale
    def restore_layout(self):
        if self.is_fullscreen:
            self.canevas.pack_forget()  
            self.cadre_1.add(self.cadre_2)  
            self.cadre_1.add(self.canevas)  
            self.cadre_1.add(self.zone_erreurs)  
            self.cadre_1.paneconfig(self.cadre_2, stretch="always", minsize=100)
            self.cadre_1.paneconfig(self.zone_erreurs, stretch="never", minsize=100)
            self.is_fullscreen = False

    def animate_canvas(self):

        timer = simpledialog.askfloat("Temps de latences","Saississez le temps (en s.) :")

        self.button_zoomin.place_forget()
        self.button_zoomout.place_forget()
        self.canvas_fullscreen()
        self.executer_code(timer)
        self.restore_layout()

        self.button_zoomin.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-50)
        self.button_zoomout.place(relx=1.0, rely=1.0, anchor="se", x=-10, y=-10)
        

    def comp_c(self):
        #Récupe le code
        code = self.zone_texte.get("1.0", tk.END).strip()
        if not code:
            messagebox.showerror("Erreur", "Veuillez écrire du code avant d'exécuter.")
            return


        try:

            toks = instrctions_listed(code)
            tokens = parseur(toks)

            for i in tokens:
                if "error" in i.keys():
                    self.afficher_erreur("[Compilation failled : check error in code]")
                    return
            code_c = generate_c_code(tokens)

            write_c_file(code_c)

            # Compiler le fichier C
            result = subprocess.run([
                "gcc", "-o", "output", "output.c", "draw_lib.c", "-lSDL2", "-lm", "-lSDL2_gfx"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                        
            self.afficher_erreur("[Compilation is done]")

        except Exception as e:
            messagebox.showerror("Erreur", f"Erreur lors de la compilation : {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = Application(root)
    root.mainloop()

