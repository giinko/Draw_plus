import tkinter as tk
from instruction import Cursor

def test_cursor_functions():
    # Create main window Tkinter
    root = tk.Tk()
    root.title("Tests des formes")
    root.geometry("800x600")

    # Create a canevas for tests
    canvas = tk.Canvas(root, width=800, height=600, bg="white")
    canvas.pack()

    # Create a cursor
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

    # Test : Polygon (pentagon)
    cursor.draw_polygon([(cursor.x, cursor.y), (cursor.x + 50, cursor.y + 50),
                         (cursor.x + 100, cursor.y + 25), (cursor.x + 75, cursor.y - 50),
                         (cursor.x + 25, cursor.y - 50)])  # Pentagon
    cursor.move_forward(150)

    # Test : Text
    cursor.draw_text("Hello, Draw++!")  # Display text
    cursor.move_forward(150)

    # Test : Mark
    cursor.draw_point()  # Mark at actual position
    cursor.move_forward(150)

    # Test : Semi-circle
    cursor.draw_half_circle(50)  # Semi-ciorcle with a radius of 50

    # Run Tkinter window to visualize the shapes
    root.mainloop()

if __name__ == "__main__":
    test_cursor_functions()
