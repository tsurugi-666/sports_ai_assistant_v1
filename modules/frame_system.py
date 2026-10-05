class Frame:
    def __init__(self, name: str, parent=None):
        self.name = name
        self.parent = parent  # Связь наследования (is_a)
        self.slots = {}

    def set_slot(self, key: str, value):
        self.slots[key] = value

    def get_slot(self, key: str):
        # Наследование свойств: если нет у себя, ищем у родителя
        if key in self.slots:
            return self.slots[key]
        elif self.parent:
            return self.parent.get_slot(key)
        return None

class FrameKnowledgeBase:
    def __init__(self):
        self.frames = {}

    def add_frame(self, frame: Frame):
        self.frames[frame.name] = frame

    def find_frame(self, name: str) -> Frame:
        return self.frames.get(name)

    def search_by_slot_value(self, key: str, value) -> list:
        results = []
        for f_name, frame in self.frames.items():
            if frame.get_slot(key) == value:
                results.append(f_name)
        return results