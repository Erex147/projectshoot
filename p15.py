s = input("Enter character: ")

if s in "abcdefghijklmnopqrstuvwxyz":
    print("Lowercase letter")
elif s in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
    print("Uppercase letter")
elif s in "0123456789":
    print("Digit")
else:
    print("Special character")