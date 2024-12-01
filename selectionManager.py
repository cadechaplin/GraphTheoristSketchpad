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
        
    def index(self, item):
        return self.__Items.index(item)

    def __getitem__(self, key):
        return self.__Items[key]

    def __contains__(self, item):
        return item in self.__Items
        
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
        if item:
            item.viewModel.selected = True
            item.viewModel.update()
        self.t()
    
    def deselect(self):
        if self.selected:
            self.selected.viewModel.selected = False
            self.selected.viewModel.update()
            self.selected = None
            self.t()
    
    def clear(self):
        self.__Items.clear()
        if self.selected:
            self.selected.viewModel.selected = False
            self.selected.viewModel.update()
            self.selected = None
        self.t()





