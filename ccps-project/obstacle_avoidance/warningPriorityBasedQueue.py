import heapq

class warningPriorityBasedQueue():
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(warningPriorityBasedQueue, cls).__new__(cls)
            cls.queue = []
        return cls._instance

    def add(self, message: str, distance: float, speed: float):
        heapq.heappush(self.queue, (distance, speed, message))
        
    def pop(self):
        return heapq.heappop(self.queue)
    
    def is_empty(self):
        return len(self.queue) == 0
    
    def clear(self):
        self.queue.clear()
    
    def __str__(self):
        return str(self.queue)
    
    def __len__(self):
        return len(self.queue)
    
if __name__ == "__main__":
    t = warningPriorityBasedQueue()
    t.add("World", 20, 30)
    t.add("Hello", 10, 20)
    
    t1 = warningPriorityBasedQueue()
    
    assert t1 == t
    
    assert t1.pop() == (10, 20, "Hello")
    assert t.pop() == (20, 30, "World")
    
    
    assert len(t) == len(t1) == 0