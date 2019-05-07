from bible.signal import Signal


class Bible:

    def __init__(self, file_handler, lower_case=False):
        self.file_handler = file_handler
        self.lower_case = lower_case

    def __iter__(self):
        while True:
            sg = Signal.read(self.file_handler, self.lower_case)
            if sg is None:
                raise StopIteration
            else:
                yield sg
