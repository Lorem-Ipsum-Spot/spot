from pocketsphinx import LiveSpeech
for phrase in LiveSpeech(kws="./kws.txt"):
    print(phrase.segments(detailed=True))