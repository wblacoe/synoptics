class Vector:
    # context words to be ignored
    stop_words = ["and", "it", "of", "the", "he", "they", "him", "them", "his", "their", "but", "be", "is", \
                  "will", "to", "ye", "was", "have", "has", "are", "I", "you", "my", "your", "me", "which", "that"]

    def __init__(self, counter, normalize=True):
        self.values = {}
        norm_squared = 0
        for token in counter:
            count = counter[token]
            self.values[token] = count
            norm_squared += count ** 2
        norm = norm_squared ** 0.5

        if normalize:
            for token in self.values:
                self.values[token] /= norm

    def add_value(self, token, value):
        self.values[token] += value

    def get_value(self, token):
        return self.values[token]

    def __str__(self):
        return str(self.values)

    def dot(self, v):
        r = 0
        for token in self.values:
            if token in v.values:
                r += self.values[token] * v.values[token]
        return r
