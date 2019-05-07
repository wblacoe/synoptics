class Verse:

    def __init__(self, chapter_number, verse_number, original_tokens, tokens):
        self.chapter_number = chapter_number
        self.verse_number = verse_number
        self.original_tokens = original_tokens
        self.tokens = tokens
        self.alignments = {}

    def __str__(self):
        return str(self.chapter_number) + ":" + str(self.verse_number) + " " + " ".join(self.original_tokens)

    def __eq__(self, other):
        return type(other) is Verse\
            and self.chapter_number == other.chapter_number\
            and self.verse_number == other.verse_number

    def __lt__(self, other):
        return self.chapter_number < other.chapter_number\
            or (self.chapter_number == other.chapter_number and self.verse_number < other.verse_number)