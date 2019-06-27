from random import random

def gen_val_op(r):
	n = random()*r+1
	trunc = int(random()+0.5)
	if trunc:
		int(n)
	op = int(random()*4)
	ops = ['*', '/', '+', '-']
	return (n, ops[op])

def compute(n, rand_int):
	l = n
	for i in xrange(l):
		n2, op = gen_val_op(rand_int)
		if op == '*':
			n *= n2
		elif op == '/':
			n /= n2
		elif op == '+':
			n += n2
		elif op == '-':
			n -= n2
	return n

def first_digit(n):
	n = abs(int(n))
	digit = 0
	while n > 0:
		digit = n % 10
		n /= 10
	return abs(digit)

def is_1st_digit_1(n):
	digit = first_digit(n)
	return digit == 1

def print_p(p):
	tot = float(sum(p.values()))
	for i in xrange(1, 10):
		per = round(p[i]/tot*100, 3)
		print(str(per)+'% chance that the first digit of a number after applying numerous operations is '+str(i))

if __name__ == '__main__':
	trials = 2000000
	p = {}
	rand_int = 9999
	num_values = 60
	for i in xrange(trials):
		values = int(random()*num_values)+1
		c = compute(values, rand_int)
		d1 = first_digit(c)

		if d1 in p:
			p[d1] += 1
		else:
			p[d1] = 1

		print (i, c)

	print ('='*32)
	print ('Including 0')
	print ('='*32)
	print_p(p)
	print ('='*32)

	if 0 in p:
		del p[0]

	tot = float(sum(p.values()))

	print ('Excluding 0')
	print ('='*32)
	print_p(p)
