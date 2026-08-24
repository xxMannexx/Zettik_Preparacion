def gen():
    print("A"); yield 1
    print("B"); yield 2
    print("C")
g = gen()
print(next(g)); print(next(g)); print(next(g))
