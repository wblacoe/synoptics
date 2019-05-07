class NewBookSignal:

    def __init__(self, title):
        self.title = title

    def __str__(self):
        return "NEW BOOK: " + self.title