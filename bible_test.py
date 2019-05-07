from bible.bible import Bible
from bible.new_book_signal import NewBookSignal


file_path = "C:\\Users\\w.blacoe\\Desktop\\python\\synoptics\\bible.txt"
file_handler = open(file_path, "r")
bible = Bible(file_handler)

pr = False
for sg in bible:
    if type(sg) == NewBookSignal:
        print("reading " + sg.title)
        if "mark" in sg.title.lower():
            pr = True
    if pr:
        print(sg)
