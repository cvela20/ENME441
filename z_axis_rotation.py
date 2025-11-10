theta1 = float(input("Enter theta1: "))
theta2 = float(input("Enter theta2: "))

Beta = theta2 - theta1

phi = (180 - Beta)/2

if Beta > 180:
	print("Case 1")
elif Beta < 180 :
	print("Case 2")

print(f"Beta = {Beta} Phi = {phi}")