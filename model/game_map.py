import pytiled_parser as pp
import arcade



class MapModel:
    def __init__(self):
        # карта - затычка 
        self.map = pp.parse_map("")
        # arcade.tilemap.process_layer("Слой тайлов 1")
        
    
