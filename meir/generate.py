from collections import defaultdict
import random

class PCFG(object):
    def __init__(self):
        self._rules = defaultdict(list)
        self._symbols = defaultdict(str)
        self._sums = defaultdict(float)
        self._generatrees = False

    def add_rule(self, lhs, rhs, weight):
        assert(isinstance(lhs, str))
        assert(isinstance(rhs, list))
        self._rules[lhs].append((rhs, weight))
        self._sums[lhs] += weight

    @classmethod
    def from_file(cls, filename):
        grammar = PCFG()
        with open(filename) as fh:
            for line in fh:
                line = line.split("#")[0].strip()
                if not line: continue
                w,l,r = line.split(None, 2)
                r = r.split()
                w = float(w)
                grammar.add_rule(l,r,w)
        return grammar

    def is_terminal(self, symbol): return symbol not in self._rules

    def gen(self, symbol):
        if self.is_terminal(symbol): return symbol
        else:
            expansion = self.random_expansion(symbol)
            generated_sentence = " ".join(self.gen(s) for s in expansion)
            return "("+symbol+" "+generated_sentence+")" if self._generatrees else generated_sentence

    def random_sent(self):
        return self.gen("ROOT")

    def random_expansion(self, symbol):
        """
        Generates a random RHS for symbol, in proportion to the weights.
        """
        p = random.random() * self._sums[symbol]
        for r,w in self._rules[symbol]:
            p = p - w
            if p < 0:
                return r
        return r


if __name__ == '__main__':

    import sys
    if len(sys.argv) > 2 and sys.argv[2] not in ['-n','-t']:
        print "Usage: python generate.py <optional - > -n sentence_number"

    import sys
    if len(sys.argv) > 2 and sys.argv[2] not in ['-n','-t']:
        print "Usage: python generate.py <optional - > -n sentence_number"

    pcfg = PCFG.from_file(sys.argv[1])
    num_sentences = 1
    if len(sys.argv) > 2:
        if sys.argv[2] == '-n':
            num_sentences = int(sys.argv[3])
        if sys.argv[2] == '-t':
            pcfg._generatrees = True
        if len(sys.argv) > 3 and sys.argv[3] == '-n':
            num_sentences = int(sys.argv[4])
    for i in range(num_sentences):
        print pcfg.random_sent()
