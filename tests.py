from parser import *

print("Test preprocess() - 3 tests")

test_sentences = ["I am 27 years old.", "My life is amazing", "Human beings can rise to all of our challenges"]
answers = {}
answers["I am 27 years old."] = ["i", "am", "years", "old"]
answers["My life is amazing"] = ["my", "life", "is", "amazing"]
answers["Human beings can rise to all of our challenges"] = ["human","beings","can","rise","to","all","of","our","challenges"]

for test in test_sentences:
    print("test:")
    print(test)
    if preprocess(test) == answers[test]:
        print("Success!")
    else:
        print("Fail")
        print("got:")
        print(preprocess(test))
        print("wanted:")
        print(answers[test])