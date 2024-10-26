from events import Event


class selectionManager:
    def __init__(self):
        self.__selected = []
        self.onSelectionChanged = Event()
    def remove(self, item):
        self.selected.remove(item)
        
    def add(self, item):
        self.selected.append(item)
        
        