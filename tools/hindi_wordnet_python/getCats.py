import pickle

s= pickle.load(open("SynsetOnto.pk"))

cats= {}
for word in s.keys():
	for pos in s[word]:
		for cat in s[word][pos]:
			cats[cat]=1

for cat in cats:
	print cat
