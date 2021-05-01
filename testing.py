if __name__ == "__main__":
    list = [[1,[2,3]],[1,3]]
    print([1,2,3] in list)
    print([1, 3] in list)
    print([1, [2,3]] in list)

    lst = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
    lst2 = lst[0]
    print(lst)
    print(lst2)
    lst2[0] = 10000
    lst[0] = None
    print(lst)

    print(lst2)