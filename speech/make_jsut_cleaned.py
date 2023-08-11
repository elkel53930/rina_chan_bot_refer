import pp

label_file = "~/dev/rc/speech/train_data/jsut-label/labels/basic5000/BASIC5000_%04d.lab"
wav_file = "~/dev/rc/speech/train_data/jsut_ver1.1/basic5000/wav/BASIC5000_%04d.wav"


vocab = set([])
for index in range(1, 5001):
    full_context_labels = []
    with open(label_file % index) as f:
        for line in f:
            full_context_labels.append(line.split(' ')[2])
        phono = "".join(pp.pp_symbols(full_context_labels))
        for c in phono:
            vocab.add(c)
        print(wav_file % index + "|0|" + phono)

vocab = list(vocab)
vocab.sort()
print("".join(vocab))
