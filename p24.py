s = input("Enter string: ")
l = 0
u = 0
d = 0
sc = 0
for i in s:
    if i in "abcdefghijklmnopqrstuvwxyz":
        l += 1
    elif i in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
        u += 1
    elif i in "0123456789":
        d += 1
    else:
        sc += 1
print(f"Lowercase letters: {l}")
print(f"Uppercase letters: {u}")
print(f"Digits: {d}")
print(f"Special characters: {sc}")