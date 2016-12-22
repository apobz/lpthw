directions = ['north', 'south', 'east',
              'west', 'down', 'up',
              'left', 'right', 'back']
verbs = ['go', 'stop', 'kill', 'eat']
stop_words = ['the', 'in', 'of', 'from', 'at', 'it']
nouns = ['door', 'bear', 'princess', 'cabinet']

def scan(s):
    sentence = []
    words = [word.lower() for word in s.split()]
    for w in words:
        if w in directions:
            sentence.append(('direction', w))
        elif w in verbs:
            sentence.append(('verb', w))
        elif w in stop_words:
            sentence.append(('stop', w))
        elif w in nouns:
            sentence.append(('noun', w))
        elif convert_number(w):
            sentence.append(('number', int(w)))
        else:
            sentence.append(('stop', w))
    return sentence

def convert_number(x):
    try:
        return int(x)
    except ValueError:
        return None
