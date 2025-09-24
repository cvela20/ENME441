# Cameron Vela lab 3
import random
maxturns = 12
guessnumber = 1

def guess(n):
	while True:
		print('Guess a sequence 4 values from 1-6: ')
		guess = input(f'Guess {n} of 12: ')
		guess = list(guess)
		if len(guess) == 4 and all(x in "123456" for x in guess):
			return guess
		else:
			print('Input errror: ')

def symbol(a):
	for i in range(0,4):
		if a[i] == 1:
			print('\u25CF', end='')
		elif a[i] == 0:
			print('\u25CB', end='')
	print()


sequence = []
for x in range(0,4):
	sequence.append(str(random.randint(1,6)))

while True:
	g = guess(guessnumber)
	a = [2, 2, 2, 2]
	check = [0, 0, 0, 0]
	correctdigit = [0, 0, 0, 0]
	for i in range(0,4):
		if g[i] == sequence[i]:
			a[i] = 1
			check[i] = 1
			correctdigit[i] = 1

	for i in range(0,4):
		if correctdigit != 1:
			for j in range(0,4):
				if a[j] != 1:
					if g[i] == sequence[j] and check[j] != 1:
						a[i] = 0
						check[j] = 1

					else:
						pass

	symbol(a)
	if all(x == 1 for x in a):
		print(f'Congratualtions! You correctly guessed in {guessnumber} guesses!')
		break

	guessnumber += 1
	
	if guessnumber > 12:
		print(f'You lost. You excceeded the maximum allowed guesses. The correct sequence was {sequence}')
		break

print('Thanks for Playing!')