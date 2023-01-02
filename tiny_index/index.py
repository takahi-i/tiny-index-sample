from collections import defaultdict
from typing import Dict, List
from janome.tokenizer import Tokenizer
import wanakana

_ja_tokenizer = Tokenizer()


class Index:
    _index: Dict[str, List[int]] = {}
    _doc_ids: Dict[int, str] = {}

    def __init__(self, docs: List[str]):
        self._build_index(docs)

    def _build_index(self, docs):
        for doc_id, doc in enumerate(docs):
            self._doc_ids[doc_id] = doc
            tokenized = list(_ja_tokenizer.tokenize(doc))
            for token in tokenized:
                self._add_surfaces(doc_id, token)
                self._add_readings(doc_id, token)

    def _add_readings(self, doc_id, token):
        reading = wanakana.to_hiragana(token.reading)
        if reading not in self._index:
            self._index[reading] = []
        self._index[reading].append(doc_id)

    def _add_surfaces(self, doc_id, token):
        surface = token.node.surface
        if surface not in self._index:
            self._index[surface] = []
        self._index[surface].append(doc_id)

    def search(self, sequence: str):
        candidates = defaultdict(float)
        tokenized = list(_ja_tokenizer.tokenize(sequence))
        for token in tokenized:
            self._extract(candidates, token.node.surface)
            self._extract(candidates, sequence)
            self._extract(candidates, wanakana.to_hiragana(token.reading))
        results = sorted(candidates.items(), key=lambda x: x[1], reverse=True)
        return list(map(lambda x: (self._doc_ids[x[0]], x[1]), results))

    def _extract(self, candidates, sequence):
        if sequence in self._index:
            for id in self._index[sequence]:
                candidates[id] += 1
