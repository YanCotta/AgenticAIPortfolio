class ConversationMemory:
    def __init__(self):
        self.history = []

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})

    def get_history(self, limit=5):
        return self.history[-limit:]

    def clear_history(self):
        self.history = []
