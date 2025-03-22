class UndoStack:
    def __init__(self):
        self._entries = []
        return

    def push(self, on_undo):
        self._entries.append(on_undo)
        return

    def undo(self):
        if len(self._entries) > 0:
            entry = self._entries.pop()
            entry()
        return

    def remove_all(self):
        self._entries.clear()
        return