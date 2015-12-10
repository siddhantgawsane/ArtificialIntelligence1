from sys import argv

if len(argv) > 1:
	observations = argv[1]
else:
	observations = ""

outFile = open("result.txt", 'w+')

outFile.write("Observation Sequence Q: %s\n" % observations)
outFile.write("Length of Q: %i\n" % len(observations))

observations = observations.upper()
observations = " "+observations +"C"		#assume Q+1 is C

pOfHypothesis = [{ 'h1':0.1, 'h2':0.2, 'h3':0.4, 'h4':0.2, 'h5':0.1 }]

priorProb = {
				'C|h1': 1, 'L|h1': 0,
				'C|h2': 0.75, 'L|h2': 0.25,
				'C|h3': 0.5, 'L|h3': 0.5,
				'C|h4': 0.25, 'L|h4': 0.75,
				'C|h5': 0, 'L|h5': 1 
			}

pOfQueries = []
p=0
for i in range(1,6):
	temp = (priorProb[observations[1]+'|h'+str(i)] * pOfHypothesis[0]['h'+str(i)])
	#print temp
	p = p + temp

pOfQueries.append({observations[1]:p})
length = len(observations)

for j in range(1,length-1):
	if len(pOfHypothesis)-1 < j:
		pOfHypothesis.append({})
	if len(pOfQueries)-1 < j:
		pOfQueries.append({})

	temp = 0
	for i in range(1,6):
		pOfHypothesis[j]['h'+str(i)] = priorProb[observations[j]+'|h'+str(i)] * pOfHypothesis[j-1]['h'+str(i)] / pOfQueries[j-1][observations[j]]
		temp = temp + priorProb[observations[j+1]+'|h'+str(i)] * pOfHypothesis[j]['h'+str(i)]
	pOfQueries[j][observations[j+1]] = temp

for i in range(1,6):
	outFile.write("P(h%d|Q) = %.5f\n" % (i, pOfHypothesis[-1]["h"+str(i)]))

pOfNextQisC = pOfQueries[-1]["C"]
outFile.write( "Probability that the next candy we pick will be C, given Q: %.5f\n" % pOfNextQisC )
outFile.write( "Probability that the next candy we pick will be L, given Q: %.5f\n" % (1.000-pOfNextQisC))
outFile.close()