import tkinter as tk
from instruction import Cursor

def test_cursor_functions():
    # Créer une fenêtre principale Tkinter
    root = tk.Tk()
    root.title("Tests des formes")
    root.geometry("800x600")

    # Créer un canevas pour les tests
    canvas = tk.Canvas(root, width=800, height=600, bg="white")
    canvas.pack()

    # Instancier un curseur
    cursor = Cursor(canvas, x=100, y=100, color="blue", thickness=2)

    # Test : Rectangle
    cursor.draw_rectangle(100, 50)  
    cursor.move_forward(150)      

    # Test : Arc
    cursor.draw_arc(50, 0, 180)    
    cursor.move_forward(150)

    # Test : Triangle
    cursor.draw_triangle(100)     
    cursor.move_forward(150)

    # Test : Polygone (pentagone)
    cursor.draw_polygon([(cursor.x, cursor.y), (cursor.x + 50, cursor.y + 50),
                         (cursor.x + 100, cursor.y + 25), (cursor.x + 75, cursor.y - 50),
                         (cursor.x + 25, cursor.y - 50)])  # Pentagone
    cursor.move_forward(150)

    # Test : Texte
    cursor.draw_text("Hello, Draw++!")  # Affiche du texte
    cursor.move_forward(150)

    # Test : Point
    cursor.draw_point()  # Point à la position actuelle
    cursor.move_forward(150)

    # Test : Demi-cercle
    cursor.draw_half_circle(50)  # Demi-cercle avec un rayon de 50

    # Lancer la fenêtre Tkinter pour visualiser les formes
    root.mainloop()

if __name__ == "__main__":
    test_cursor_functions()
