from vector import Vector
import collections

verses = []
verses.append("And he straitly charged them that they should not make him known".split(" "))
verses.append("See that ye refuse not him that speaketh For if they escaped not who refused him that spake on earth much more shall not we escape if we turn away from him that speaketh from heaven".split(" "))

vectors = []
for verse in verses:
    counter = collections.Counter()
    for token in verse:
        counter[token] += 1
    vector = Vector(counter)
    vectors.append(vector)
    print(verse)
    print(vector)

print(vectors[0].dot(vectors[1]))