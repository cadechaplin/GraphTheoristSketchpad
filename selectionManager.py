from events import Event


class selectionManager:
    def __init__(self):
        self.__Items = []
        self.onSelectionChanged = Event()
        self.selected = None
        
    def __len__(self):
        return len(self.__Items)
        
    def append(self, item):
        self.__Items.append(item)
        self.t()
    
    
    def __iter__(self):
        return iter(self.__Items)
        
        
    # So that I dont need to type self.onSelectionChanged.trigger() every time I want to trigger the event
    def t(self):
        self.onSelectionChanged.trigger()
        
    def remove(self, item):
        self.__Items.remove(item)
        self.t()
        
    def add(self, item):
        self.__Items.append(item)
        self.t()
        
    def setSelected(self, item):
        if self.selected:
            self.selected.viewModel.selected = False
            self.selected.viewModel.update()
        self.selected = item
        self.t()
    
    
    
    
        
        