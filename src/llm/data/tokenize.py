# This is a tokenizer based on Byte-Pair Encoding (BPE)

import re
import typer
import unicodedata

from collections import defaultdict


def normalize(corpus: list[str]) -> list[str]:
    """
    Normalize a list of strings by:
    - removing needless whitespace
    - lowercasing
    - removing accents
    """
    norm_corpus: list[str] = []
    for string in corpus:
        # remove accents
        nfd = unicodedata.normalize("NFD", string)
        nfd_string: str = "".join(c for c in nfd if unicodedata.category(c) != "Mn")
        
        # remove whitespace
        words: list[str] = nfd_string.split()

        # lowercasing
        lowercased_words: list[str] = []
        for word in words:
            lc_word: str = word.lower()
            lowercased_words.append(lc_word)
        
        norm_corpus.append(" ".join(word for word in lowercased_words))

    return norm_corpus


def pre_tokenize(corpus: list[str]) -> list[str]:
    "Splits sentences into words and keeps track of whitespace."
    pre_tokenized_corpus: list[str] = []
    for sentence in corpus:
        words = [t.replace(' ', 'Ġ') for t in re.findall(r' ?\S+', sentence)]
        pre_tokenized_corpus += words
    return pre_tokenized_corpus


def generate_token_set(words: list[str], vocab_size: int = 1000) -> tuple[list[str], dict[tuple, str]]:
    "Build a vocabulary of tokens"
    word_freqs = defaultdict(int)
    for word in words:
        word_freqs[word] += 1

    alphabet: list[str] = []
    for word in word_freqs.keys():
        for letter in word:
            if letter not in alphabet:
                alphabet.append(letter)
    alphabet.sort()

    splits: dict[str, list[str]] = {word: [c for c in word] for word in word_freqs.keys()}
    merges: dict[tuple, str] = {}


    while len(alphabet) < vocab_size:
        pair_freqs: dict[tuple, int] = _compute_pair_freqs(splits, word_freqs)
        if not pair_freqs:
            break
        best_pair = ""
        max_freq = None
        for pair, freq in pair_freqs.items():
            if max_freq is None or max_freq < freq:
                best_pair = pair
                max_freq = freq  
        splits = _merge_pair(*best_pair, splits, word_freqs)
        merges[best_pair] = best_pair[0] + best_pair[1]
        alphabet.append(best_pair[0] + best_pair[1])

    alphabet.sort()
    return alphabet, merges


def tokenize(words: list[str], merges: dict[tuple, str]) -> list[str]:
    splits = [[l for l in word] for word in words]
    for pair, merge in merges.items():
        for idx, split in enumerate(splits):
            i = 0
            while i < len(split) - 1:
                if split[i] == pair[0] and split[i + 1] == pair[1]:
                    split = split[:i] + [merge] + split[i + 2 :]
                else:
                    i += 1
            splits[idx] = split

    return sum(splits, [])



def _compute_pair_freqs(splits: dict[str, list[str]], word_freqs: dict[str, int]) -> dict[tuple, int]:
    pair_freqs = defaultdict(int)
    for word, freq in word_freqs.items():
        split = splits[word]
        if len(split) == 1:
            continue
        for i in range(len(split) - 1):
            pair = (split[i], split[i + 1])
            pair_freqs[pair] += freq
    return pair_freqs


def _merge_pair(a, b, splits, word_freqs):
    for word in word_freqs:
        split = splits[word]
        if len(split) == 1:
            continue
        i = 0
        while i < len(split) - 1:
            if split[i] == a and split[i + 1] == b:
                split = split[:i] + [a + b] + split[i + 2 :]
            else:
                i += 1
        splits[word] = split
    return splits
