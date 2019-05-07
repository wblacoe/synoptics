import re
from bible.verse import Verse
from bible.new_book_signal import NewBookSignal
from bible.new_chapter_signal import NewChapterSignal
from queue import Queue


class Signal:

    # for cleaning tokens
    suffixes_to_be_removed = [",", ".", ";", ":", "!", "?", ":)", "'s"]
    prefixes_to_be_removed = ["("]

    # these variables must be used by class methods to be independent of Verse instances
    verse_index_pattern = re.compile("[0-9]+\\:[0-9]+")  # pattern for verse index, e.g. 13:6
    book_name_buffer = "Unknown Book"  # save book name that will be needed for future verses
    chapter_number_buffer = -1  # save chapter number that will be needed for future verses
    verse_number_buffer = -1  # save verse number that will be needed for future verses
    original_tokens_buffer = []  # save original tokens that will be needed for future verses
    tokens_buffer = []  # save tokens that will be needed for future verses
    signal_queue = Queue()  # for new verses, new-chapter signals and new-book signals
    consecutive_empty_lines = 0
    new_book_detected = True

    def __init__(self):
        pass

    @classmethod
    def clean_token(cls, token):
        for prefix in cls.prefixes_to_be_removed:
            if token.startswith(prefix):
                token = token[len(prefix):]
        for suffix in cls.suffixes_to_be_removed:
            if token.endswith(suffix):
                token = token[:-len(suffix)]
        return token

    @classmethod
    def read(cls, file_handler, lower_case):
        chapter_number = -1
        verse_number = -1
        tokens = None
        end_of_file_reached = False

        # if there are no signals waiting in the queue to be emitted, create new ones
        while cls.signal_queue.empty() and not end_of_file_reached:

            # read until next non-empty line is found
            line = "\n"
            while line == "\n":
                cls.consecutive_empty_lines += 1
                line = file_handler.readline()
                # end of main text / file detected
                if cls.consecutive_empty_lines >= 10 or line == "":
                    end_of_file_reached = True

            # create and queue one last verse from buffer contents
            if end_of_file_reached:
                chapter_number = cls.chapter_number_buffer
                verse_number = cls.verse_number_buffer
                original_tokens = cls.original_tokens_buffer
                tokens = cls.tokens_buffer
                cls.chapter_number_buffer = -1
                cls.verse_number_buffer = -1
                cls.original_tokens_buffer = []
                cls.tokens_buffer = []
                if chapter_number != -1 and verse_number != -1 and tokens is not None:
                    cls.signal_queue.put(Verse(chapter_number, verse_number, original_tokens, tokens))
                continue

            line = line[:-1]

            # detect the title of a new book
            if cls.consecutive_empty_lines > 4:
                cls.book_name_buffer = line
                # wait for the next new-chapter signal to add a new-book signal to the signal queue
                # save this information in flag:
                cls.new_book_detected = True
                cls.consecutive_empty_lines = 0
                continue

            cls.consecutive_empty_lines = 0

            # iterate over tokens rather than lines because a new verse sometimes begins mid-line
            original_tokens = line.split(" ")
            for original_token in original_tokens:

                # detect verse index
                if re.match(cls.verse_index_pattern, original_token):

                    if len(cls.tokens_buffer) > 0:
                        # get buffered chapter number, verse number and tokens to create a new verse below
                        chapter_number = cls.chapter_number_buffer
                        verse_number = cls.verse_number_buffer
                        original_tokens = cls.original_tokens_buffer
                        tokens = cls.tokens_buffer
                        cls.original_tokens_buffer = []
                        cls.tokens_buffer = []

                    # buffer chapter and verse numbers for next verse
                    entries = original_token.split(":")
                    cls.chapter_number_buffer = int(entries[0])
                    cls.verse_number_buffer = int(entries[1])

                    # create new verse and stick it in the signal queue
                    if chapter_number != -1 and verse_number != -1 and tokens is not None:
                        cls.signal_queue.put(Verse(chapter_number, verse_number, original_tokens, tokens))

                    # detect change of chapter -> stick a new-chapter signal in the queue
                    if cls.chapter_number_buffer != chapter_number or cls.verse_number_buffer <= verse_number:
                        if cls.new_book_detected:
                            cls.signal_queue.put(NewBookSignal(cls.book_name_buffer))
                            cls.new_book_detected = False
                        cls.signal_queue.put(NewChapterSignal())

                # current token is a regular text token
                else:
                    token = cls.clean_token(original_token)
                    if lower_case:
                        token = token.lower()
                    cls.original_tokens_buffer.append(original_token)
                    cls.tokens_buffer.append(token)

        if cls.signal_queue.empty():
            return None
        else:
            return cls.signal_queue.get()