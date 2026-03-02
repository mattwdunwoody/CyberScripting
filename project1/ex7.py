def add(x, y):
    print("test1")
    a = x + y
    return a

def sub(x, y):
    print("test2")
    a = x - y
    return a

def mul(x, y):
    print("multiplying")
    a = x * y
    return a

def main():
    print(add(2, 3))
    print(sub(2, 3))
    print(mul(2, 3))

main()