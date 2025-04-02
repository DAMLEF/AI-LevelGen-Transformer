class Cell:
    # La taille des cellules qui composent le monde
    SIZE = 30

    def __init__(self, walkable=True, color=(255, 0, 0)):
        self.walkable = walkable  # Paramètre pour dire si l'on peut ou non marcher sur la case
        self.color = color  # Paramètre qui définie la couleur de la case
