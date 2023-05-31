
class Element:
    def __init__(self, element_type, internal_name, height, width, thickness, vertical_load_design, horizontal_load_design, steel_type=None, concrete_type=None,
                 file_path=None):
        self.type = element_type
        self.internal_name = internal_name
        self.height = height
        self.width = width
        self.thickness = thickness
        self.vertical_load_design = vertical_load_design
        self.horizontal_load_design = horizontal_load_design
        self.steel_type = steel_type
        self.concrete_type = concrete_type
        self.file_path = file_path
