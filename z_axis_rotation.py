theta1 = float(input("Enter theta1: "))
theta2 = float(input("Enter theta2: "))

Beta = theta2 - theta1


if Beta > 0:
	phi = (180-Beta)/2
elif Beta < 0 :
	phi = 180 - (180-Beta)/2

print(f"Beta = {Beta} Phi = {phi}")