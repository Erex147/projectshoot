l = [42, 124, 12, 153, 5, 600, 72, 81, 86]
t = (12, 124, 42, 13, 5, 0, 62, 821, 860)
largest = l[0]
smallest = l[0]
for i in l:
    if i > largest:
        largest = i
    if i < smallest:
        smallest = i
print(f"Largest in list: {largest}")
print(f"Smallest in list: {smallest}")
largest = t[0]
smallest = t[0]
for i in t:
    if i > largest:
        largest = i
    if i < smallest:
        smallest = i
print(f"Largest in tuple: {largest}")
print(f"Smallest in tuple: {smallest}")