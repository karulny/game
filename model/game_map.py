import pytiled_parser as pp



class MapModel:
    def __init__(self, width=60, height=60):
        # карта - затычка
        self.width = width
        self.height = height
        # шаблон клеток - Затычка
        self.grid = [[0 for _ in range(width)] for _ in range(height)]

    #
    def load_from_tmx(self, tmx):
        pass

        
    
