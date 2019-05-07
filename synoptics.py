from bible.bible import Bible
from bible.new_book_signal import NewBookSignal
from bible.verse import Verse
from vector import Vector
from collections import Counter
import os


def get_verses_in_gospels(bible):
    print("\n[collecting all verses in gospels]")

    verses_in_books = {}
    book_title = None

    for signal in bible:

        if type(signal) is NewBookSignal:

            if "gospel" in signal.title.lower():
                print("reading " + signal.title)
                book_title = signal.title
                verses_in_books[book_title] = []
            else:
                book_title = None

        elif book_title is not None and type(signal) is Verse:
            verses_in_books[book_title].append(signal)

    return verses_in_books


def get_verse_vector_pairs(verses_in_books):
    print("\n[generating vectors for all verses]")

    verse_vector_pairs_in_books = {}

    for book_title in verses_in_books:
        print(book_title + " contains " + str(len(verses_in_books[book_title])) + " verses")

        verse_vector_pairs_in_books[book_title] = []

        for verse in verses_in_books[book_title]:

            verse_counts = Counter()
            for token in verse.tokens:
                if token not in Vector.stop_words:
                    verse_counts[token] += 1

            verse_vector = Vector(verse_counts)
            verse_vector_pairs_in_books[book_title].append((verse, verse_vector))

    return verse_vector_pairs_in_books


def get_verse_similarities(verse_vector_pairs_in_books, book1_title, book2_title, threshold=0.5):
    print("\n[computing similarities between verses in " + book1_title + " and " + book2_title + "]")

    similarities = []

    i = 0
    n = len(verse_vector_pairs_in_books[book1_title]) * len(verse_vector_pairs_in_books[book2_title])

    for verse1, vector1 in verse_vector_pairs_in_books[book1_title]:
        for verse2, vector2 in verse_vector_pairs_in_books[book2_title]:
            sim = vector1.dot(vector2)
            i += 1
            if i % 10000 == 0:
                print("" + str(i) + "/" + str(n) + " verses have been compared")
            if sim >= threshold:
                similarities.append((
                    sim,
                    (verse1.chapter_number, verse1.verse_number),
                    verse1,
                    (verse2.chapter_number, verse2.verse_number),
                    verse2
                ))

    return similarities


def align_verses(similarities, book1_title, book2_title):
    print("\n[aligning verses in " + book1_title + " and " + book2_title + "]")

    for comparison in sorted(similarities, reverse=True):
        sim = comparison[0]
        verse1 = comparison[2]
        verse2 = comparison[4]

        if book1_title not in verse1.alignments and book2_title not in verse2.alignments:
            verse1.alignments[book2_title] = (sim, verse2)
            verse2.alignments[book1_title] = (sim, verse1)


def print_alignments(verses_in_books, book1_title, book2_title):
    print("\n[printing verse alignments (" + book1_title + " -> " + book2_title + ")]")

    for verse in verses_in_books[book1_title]:
        s = str(verse)
        if book2_title in verse.alignments:
            sim, aligned_verse = verse.alignments[book2_title]
            sim_string = str(int(sim * 100)) + "%"
            s += "\n\t(" + sim_string + ") " + str(aligned_verse)
        print(s)


def write_alignments_to_file(verses_in_books, book1_title, book2_title, file_path):
    print("[writing verse alignments (" + book1_title + " -> " + book2_title + ") to " + file_path + "]")

    f = open(file_path, "w")

    for verse in verses_in_books[book1_title]:
        s = str(verse)
        if book2_title in verse.alignments:
            sim, aligned_verse = verse.alignments[book2_title]
            sim_string = str(int(sim * 100)) + "%"
            s += "\n\t(" + sim_string + ") " + str(aligned_verse)
        f.write(s + "\n")

    f.close()


file_path = "C:\\Users\\w.blacoe\\Desktop\\python\\synoptics\\bible.txt"
file_handler = open(file_path, "r")
bible = Bible(file_handler, lower_case=True)

verses_in_gospels = get_verses_in_gospels(bible)
book_titles = [key for key in verses_in_gospels.keys()]

verse_vector_pairs_in_gospels = get_verse_vector_pairs(verses_in_gospels)

authors = ["matthew", "mark", "luke", "john"]
folder_path = "C:\\Users\\w.blacoe\\Desktop\\python\\synoptics\\output"

for i in range(4):
    for j in range(i):

        similarities = get_verse_similarities(verse_vector_pairs_in_gospels, book_titles[i], book_titles[j])
        align_verses(similarities, book_titles[i], book_titles[j])

        file_path = os.path.join(folder_path, authors[i] + "_" + authors[j] + ".txt")
        write_alignments_to_file(verses_in_gospels, book_titles[i], book_titles[j], file_path)

        file_path = os.path.join(folder_path, authors[j] + "_" + authors[i] + ".txt")
        write_alignments_to_file(verses_in_gospels, book_titles[j], book_titles[i], file_path)

#print_alignments(verses_in_gospels, book_titles[0], book_titles[1])