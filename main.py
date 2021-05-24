class LineSorter:

    def __init__(self, s):
        self.s = s

    def sort(self):
        for i in range(len(self.s)):
            min_idx = i
            for j in range(i + 1, len(self.s)):
                if ord(self.s[min_idx]) > ord(self.s[j]):
                    min_idx = j
            self.swap(i, min_idx)

    def swap(self, a, b):
        a, b = min(a, b), max(a, b)
        if a != b:
            self.s = self.s[:a] + self.s[b] + self.s[a + 1: b] + self.s[a] + self.s[b + 1:]

tests = [
    'ZYXWVUTSRQPONMLKJIHGFEDCBA',
    'cba',
    'abc',
    'a',
    'ba',
    'bb',
    'Helloworld',
    'ZYXWVUTSRQPONMLKJIHGFEDCBAzyxwvutsrqponmlkjihgfedcba'
]
for test in tests:
    sorter = LineSorter(test)
    sorter.sort()
    print('-' * 20)
    print(f'Before sort: {test}')
    print(f'After sort: {sorter.s}')
