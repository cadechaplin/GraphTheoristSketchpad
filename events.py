

class Event:
    def __init__(self):
        self.update = []
    
    def trigger(self):
        for func in self.update:
            func()