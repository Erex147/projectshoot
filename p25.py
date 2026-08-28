s = input("Enter string: ").lower()
if s == s[::-1]:
    print("Palindrome")
else:
    print("Not a palindrome")