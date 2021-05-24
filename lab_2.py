class OneIndexedList():
    def __init__(self, items=None):
        self.items = items or []

    def __getitem__(self, idx):
        return self.items[idx - 1]

    def __setitem__(self, idx, value):
        self.items[idx - 1] = value

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()


my_list = OneIndexedList()
for i in range(5):
    my_list.push(i)

for i in range(1, 5 + 1):
    print(my_list[i])

for i in range(1, 5 + 1):
    print(my_list.pop())