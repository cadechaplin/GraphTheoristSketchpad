
class EdgeCountManager:
    def __init__(self):
        self.current_count = 0
        self.available_positions = []  # Queue for recycled positions
    
    def get_next_position(self):
        """Get next available position - either from queue or increment counter"""
        if self.available_positions:
            return self.available_positions.pop(0)
        else:
            self.current_count += 1
            return self.current_count
            
    def recycle_position(self, position):
        """Add a position back to queue when edge is deleted"""
        if position not in self.available_positions:
            self.available_positions.append(position)
            self.available_positions.sort()
        