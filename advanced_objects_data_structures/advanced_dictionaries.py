d = {"k1": 1, "k2": 2}

my_dict = {x: x ** 2 for x in range(10)}
print(my_dict)


for k in d.items():
    print(k)  # return tuples of key, value pairs


my_dict = {k: v ** 2 for k, v in zip(["a", "b"], range(2))}
print(my_dict)


