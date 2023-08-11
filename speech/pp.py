from posixpath import split
import pyopenjtalk
import re


def numeric_feature_by_regex(regex, s):
    match = re.search(regex, s)

    # In the undefined(xx) case, return a value that is out of context
    if match is None:
        return -50
    return int(match.group(1))


def pp_symbols(labels, drop_unvoiced_vowels=True):
    PP = []
    N = len(labels)

    for n in range(N):
        lab_curr = labels[n]

        # retrieve a phoneme
        p3 = re.search(r"\-(.*?)\+", lab_curr).group(1)

        # Treat unvoiced vowels as voiced vowels
        if drop_unvoiced_vowels and p3 in "AIUEO":
            p3 = p3.lower()

        # "sil" at head or tail is special case
        if p3 == "sil":
#            if n == 0:
#                PP.append("^")
#            elif n == N - 1:
            if n == N - 1:
                # is interrogative?
                e3 = numeric_feature_by_regex(r"!(\d+)", lab_curr)
                if e3 == 0:
                    PP.append("")
                elif e3 == 1:
                    PP.append("?")
            continue
        elif p3 == "pau":
            # pause
            PP.append("_")
            continue
        else:
            PP.append(p3)

        a1 = numeric_feature_by_regex(r"/A:([0-9\-]+)\+", lab_curr)
        a2 = numeric_feature_by_regex(r"\+(\d+)\+", lab_curr)
        a3 = numeric_feature_by_regex(r"\+(\d+)/", lab_curr)
        f1 = numeric_feature_by_regex(r"/F:(\d+)_", lab_curr)
        a2_next = numeric_feature_by_regex(r"\+(\d+)\+", labels[n + 1])

        if a3 == 1 and a2_next == 1:
            PP.append("#")
        elif a1 == 0 and a2_next == a2 + 1 and a2 != f1:
            PP.append("]")
        elif a2 == 1 and a2_next == 2:
            PP.append("[")
    return PP

def split_sentence(text):
    result = []
    temp = []
    for c in text:
        temp.append(c)
        if c in "！？。":
            result.append("".join(temp))
            temp = []
    if len(temp):
        result.append("".join(temp))
    return result

def pp(text):
    ps = []
    PPs = []
    for sentence in split_sentence(text):
        labels = pyopenjtalk.extract_fullcontext(sentence)
        print(labels)
        PP = pp_symbols(labels)
        ps.append(pyopenjtalk.g2p(sentence))
        PPs.append("".join(PP))
    return " pau ".join(ps), "_".join(PPs)

if __name__ == "__main__":
    import sys
    print(pp(sys.argv[1]))
