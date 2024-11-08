import math

class Cursor:
    def __init__(self, canvas, x=0, y=0, color="black", thickness=1):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        self.thickness = thickness
        self.angle = 0  # Angle initial

    def move_forward(self, distance):
        # Calcul des nouvelles coordonnées
        new_x = self.x + distance * math.cos(math.radians(self.angle))
        new_y = self.y + distance * math.sin(math.radians(self.angle))
        # Dessine une ligne sur le canevas
        self.canvas.create_line(self.x, self.y, new_x, new_y, fill=self.color, width=self.thickness)
        # Met à jour la position
        self.x, self.y = new_x, new_y

    def rotate(self, degrees):
        # Mise à jour de l'angle
        self.angle = (self.angle + degrees) % 360

    def draw_circle(self, radius):
        # Dessine un cercle autour de la position actuelle
        self.canvas.create_oval(self.x - radius, self.y - radius, self.x + radius, self.y + radius,
                                outline=self.color, width=self.thickness)
