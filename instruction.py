import math

class Cursor:
    def __init__(self, canvas, x=0, y=0, color="black", thickness=1):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.color = color
        self.thickness = thickness
        self.angle = 0  # Initial angle

    def move_forward(self, distance):
        # Calculation of news coordinates
        new_x = self.x + distance * math.cos(math.radians(self.angle))
        new_y = self.y + distance * math.sin(math.radians(self.angle))
        # Draw a line on the canevas
        self.canvas.create_line(self.x, self.y, new_x, new_y, fill=self.color, width=self.thickness)
        # Update position
        self.x, self.y = new_x, new_y

    def rotate(self, degrees):
        # Update angle
        self.angle = (self.angle + degrees) % 360

    def draw_circle(self, radius):
        # Draw a circle around actual position
        self.canvas.create_oval(self.x - radius, self.y - radius, self.x + radius, self.y + radius,
                                outline=self.color, width=self.thickness)

    def draw_rectangle(self, width, height):
        self.canvas.create_rectangle(
            self.x, self.y, 
            self.x + width, self.y + height, 
            outline=self.color, width=self.thickness
        )

    def draw_arc(self, radius, start_angle, extent):
        self.canvas.create_arc(
            self.x - radius, self.y - radius,
            self.x + radius, self.y + radius,
            start=start_angle, extent=extent,
            outline=self.color, width=self.thickness
        )

    def draw_triangle(self, side_length):
        points = [
            self.x, self.y,
            self.x + side_length, self.y,
            self.x + side_length / 2, self.y - (side_length * (3 ** 0.5) / 2)
        ]
        self.canvas.create_polygon(points, outline=self.color, fill="", width=self.thickness)

    def draw_polygon(self, points):
        # Draw a polygon with a list of coordinates [(x1, y1), (x2, y2), ...].   
        flat_points = [coord for point in points for coord in point]
        self.canvas.create_polygon(flat_points, outline=self.color, fill="", width=self.thickness)

    def draw_text(self, text):
        self.canvas.create_text(self.x, self.y, text=text, fill=self.color, font=("Arial", self.thickness * 5))

    def draw_point(self):
        self.canvas.create_oval(
            self.x - 1, self.y - 1, self.x + 1, self.y + 1, 
            fill=self.color
        )

    def draw_half_circle(self, radius):
        self.canvas.create_arc(
            self.x - radius, self.y - radius,
            self.x + radius, self.y + radius,
            start=0, extent=180,
            outline=self.color, width=self.thickness
        )

