# Write a python script to input a number
# and tell if the number is divisible by 7 and also by 9


# input
n = int(input("Enter a number: "))

# process
if n % 7 == 0 and n % 9 == 0:
    print("The number is divisible by both 7 and 9.")
else:
    print("The number is not divisible by both 7 and 9.")

# output