import scipy
import scipy.sparse
import os
from sklearn.metrics.pairwise import cosine_similarity
from scipy.stats import pearsonr

#download from Google Ngram Corpus
#for i in range(200)[100:]:
#	os.system("wget \'http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-1M-3gram-20090715-\'" + str(i) + ".csv.zip")
for i in range(200)[200:]:
	os.system("wget \'http://storage.googleapis.com/books/ngrams/books/googlebooks-eng-1M-2gram-20090715-\'" + str(i) + ".csv.zip")

#list of target words from http://www.kilgarriff.co.uk/BNClists/lemma.al
f = open('lemma.al', 'r')
lines2 = f.readlines()
f.close()
targets = dict()
i = 0
for l in lines2:
	ls = l.split()
	if not ls[2] in targets:
		targets[ls[2]] = i
		i += 1


#list of context words from http://www-personal.umich.edu/~jlawler/wordlist
f = open('wordlist', 'r')
lines3 = f.readlines()
f.close()
contexts = dict()
i = 0
for l in lines3:
	ls = l.split()
	if not ls[0] in contexts:
		contexts[ls[0]] = i
		i += 1

#build matrix M_list to contain trigram co-occurrences as described in report
M_list = []
for i in range(20):
	M_list.append(scipy.sparse.lil_matrix((len(targets), len(contexts))))

for i in range(200):
	os.system("unzip *-" + str(i) + ".csv.zip")
	f = open('googlebooks-eng-1M-3gram-20090715-' + str(i) + '.csv', 'r')
	lines = f.readlines()
	f.close()
	os.system("yes | rm googlebooks-eng-1M-3gram-20090715-" + str(i) + ".csv")
	for l in lines:
		ls = l.split()
		if ls[0] in targets and ls[2] in contexts and ls[3] >= '1800' and ls[2] < '2000':
			M_list[(int(ls[3]) - 1800) / 10][targets[ls[0]], contexts[ls[2]]] += int(ls[4])

#save/load sparse vectors for later, comment out when needed
for i in range(20):
	scipy.sparse.save_npz('M' + str(i) + '.npz', M_list[i].tocsr())

#for i in range(20):
#	M_list.append(scipy.sparse.load_npz('M' + str(i) + '.npz').tolil())

#MMM is list of cosine distances between target words' vector at 1800-1810 and vector at 1990-2000
rows0 = M_list[0].sum(axis=1)
rows19 = M_list[19].sum(axis=1)
MMM = []
for i in range(len(targets)):
	if rows1[i][0] >= 10:
		MMM.append((cosine_similarity(M_list[0][i], M_list[19][i])[0][0], i))
	else:
		MMM.append((-1, i))

MMM.sort()

#use this if want to use PPMIs
#sum = M_list[0].sum()
#rows = M_list[0].sum(axis=1)
#cols = M_list[0].sum(axis=0)
#M10plus = scipy.sparse.lil_matrix((len(targets), len(contexts)))
#for i in range(len(targets)):
#	for j in range(len(targets) * 4):
#		if i % 100 == 0 and j == 0:
#			print i
#		M10plus[i, j] = max((M_list[0][i, j] / sum) / ((rows[i, 0] / sum) * (cols[0, j] / sum) + 1e-31), 0)

print "Most changing words:"
j = 0
for i in range(len(targets)):
	if j >= 30:
		break
	if MMM[i][0] > -1:
		z = MMM[i][1]
		for k,v in targets.iteritems():
			if v == z:
				print k, " ", MMM[i][0]
				j += 1
				if j >= 30:
					break


print "Least changing words:"
j = 0
for i in range(len(targets)):
	if j >= 30:
		break
	if MMM[len(targets) - i - 1][0] > -1:
		z = MMM[len(targets) - i - 1][1]
		for k,v in targets.iteritems():
			if v == z:
				print k, MMM[len(targets) - i - 1][0]
				j += 1
				if j >= 30:
					break


#model's measure of rate of change
list1 = [0.001873677,
0.004029538,
0.004522792,
0.007995725,
0.010942196,
0.015062539,
0.015765319,
0.021572282,
0.023348059,
0.026009141,
0.026038846,
0.029987064,
0.032197853,
0.03226493,
0.035217788,
0.039202024,
0.040568872,
0.042545284,
0.045482889,
0.047408335,
0.049849813,
0.050053329,
0.053121623,
0.057424857,
0.058653996,
0.059387356,
0.060409404,
0.063066909,
0.063743899,
0.06401225,
0.999937303,
0.999915102,
0.999882957,
0.999876952,
0.999843878,
0.999837644,
0.999832961,
0.999811166,
0.999797493,
0.999785891,
0.999717323,
0.999607238,
0.999597636,
0.999582701,
0.999539848,
0.999504224,
0.99943275,
0.999357882,
0.999351422,
0.999324462,
0.999314353,
0.999313521,
0.999310217,
0.99924491,
0.999199413,
0.999180982,
0.999156368,
0.999125356,
0.999101713,
0.999080733]

#number of new definitions acquired based on http://historicalthesaurus.arts.gla.ac.uk/
list2 = [3,
3,
1,
1,
4,
3,
2,
3,
2,
1,
2,
4,
2,
4,
0,
0,
2,
5,
1,
1,
5,
4,
1,
2,
3,
1,
3,
2,
4,
0,
0,
0,
0,
0,
0,
1,
5,
1,
0,
1,
0,
0,
2,
0,
1,
2,
0,
1,
1,
1,
1,
0,
0,
1,
0,
5,
2,
1,
4,
0]

#should be inversely correlated
print "Pearson correlation between number of definitions gained and model's metric of change:"
print pearsonr(list1, list2)
