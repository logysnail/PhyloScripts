import os
from math import sqrt
from itertools import combinations

"""计算tajimaD的数值"""
def makedir(output_file_path):
    if not os.path.exists(output_file_path):
        os.mkdir(output_file_path)


def tajima(file):
    sequences = _read_sequences(file)
    if len(sequences) < 3:
        return "-"
    pi = calculate_pairwise(sequences)
    print(f'Average number of nucleotide differences:{pi}')
    s = calculate_segregating_sites(sequences)
    print(f'Number of polymorphic (segregating) sites:{s}')
    length = len(sequences)
    d = get_d(length, pi, s)
    print("D = %f" % d)
    return f'{d}, {len(sequences)}'


def _read_sequences(file):
    sequences = []
    with open(file) as f:
        for name, seq in read_fasta(f):
            sequences.append(seq)
    return sequences


def calculate_pairwise(sequences):
    for seq in sequences:
        if len(seq) != len(sequences[0]):
            raise Exception("All sequences must have the same length.")
    numseqs = len(sequences)
    print(numseqs)
    num = float(numseqs * (numseqs - 1)) / float(2)
    combos = combinations(sequences, 2)
    counts = []
    for pair in combos:
        seqA = pair[0]
        seqB = pair[1]
        count = sum(1 for a, b in zip(seqA, seqB) if a != b)
        counts.append(count)

    return float(sum(counts)) / float(num)


def calculate_segregating_sites(sequences):
    combos = combinations(sequences, 2)
    indexes = []
    for pair in combos:
        seq_a = pair[0]
        seq_b = pair[1]
        for idx, (i, j) in enumerate(zip(seq_a, seq_b)):
            if i != j:
                indexes.append(idx)
    indexes = list(set(indexes))

    S = len(indexes)
    n = len(sequences)

    denom = 0
    for i in range(1, n):
        denom += (float(1) / float(i))

    return S


def get_d(seq_l, pi, s):
    a1 = sum([1.0 / i for i in range(1, seq_l)])
    a2 = sum([1.0 / (i ** 2) for i in range(1, seq_l)])

    b1 = float(seq_l + 1) / (3 * (seq_l - 1))
    b2 = float(2 * ((seq_l ** 2) + seq_l + 3)) / (9 * seq_l * (seq_l - 1))

    c1 = b1 - 1.0 / a1
    c2 = b2 - float(seq_l + 2) / (a1 * seq_l) + float(a2) / (a1 ** 2)

    e1 = float(c1) / a1
    e2 = float(c2) / ((a1 ** 2) + a2)

    D = (float(pi - (float(s) / a1)) /
         sqrt((e1 * s) +
              ((e2 * s) * (s - 1))))

    return D


def read_fasta(fp):
    name, seq = None, []
    for line in fp:
        line = line.rstrip()
        if line.startswith(">"):
            if name:
                yield name, ''.join(seq)
            name, seq = line, []
        else:
            seq.append(line)
    if name:
        yield name, ''.join(seq)


path = '{path}/input'
os.chdir(path)
with open(f'../{path}/output.csv', "x") as out:
    for file_name in os.listdir(path):
        out.write(f'{file_name},{tajima(file_name)}\n')
