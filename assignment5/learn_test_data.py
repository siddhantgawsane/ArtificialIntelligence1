from sys import argv
import decimal
script,dataFile = argv

txt = open(dataFile)
g=0
w=0
o=0
f=0
total=365
pWgivenG = 0
pFandWandO = 0
pFandWandNotO = 0
pFandOandNotW = 0
pWandO = 0
pWandNotO = 0
pNotWandO = 0
pNotWandNotO = 0

for line in txt:
	temp = line.split()
	
	isGameOn = int(temp[0])
	doesWatch = int(temp[1])
	isOutOfCatFood = int(temp[2])
	feedsCat = int(temp[3])

	if isGameOn:
		g = g + 1
	if doesWatch:
		w = w + 1
	if isOutOfCatFood:
		o = o + 1
	if feedsCat:
		f = f + 1

	if isGameOn and doesWatch:
		pWgivenG = pWgivenG + 1
	if feedsCat:
		if doesWatch and isOutOfCatFood:
			pFandWandO = pFandWandO + 1
		else:
			if doesWatch:
				pFandWandNotO = pFandWandNotO + 1
			if isOutOfCatFood:
				pFandOandNotW = pFandOandNotW + 1
	if doesWatch and isOutOfCatFood:
		pWandO = pWandO + 1
	if doesWatch and not isOutOfCatFood:
		pWandNotO = pWandNotO + 1
	if not doesWatch and isOutOfCatFood:
		pNotWandO = pNotWandO + 1
	if not doesWatch and not isOutOfCatFood:
		pNotWandNotO = pNotWandNotO + 1
txt.close()

# print g,w,o,f
print "\nP(GameOn)\n%.5f\n" % (float(g)/total)
print "\nP(OutOfCatFood)\n%.5f\n" % (float(o)/total)
print "\nP(WatchesTV|GameOn)"
print "GameOn=True	%.5f" % (float(pWgivenG)/g)
print "GameOn=False	%.5f\n" % (float(w-pWgivenG)/(total-g))
print "\nP(FeedsCat|WatchesTV,OutOfCatFood)"
print "WatchesTV=True,OutOfCatFood=True	%.5f" % (float(pFandWandO)/pWandO)
print "WatchesTV=True,OutOfCatFood=False	%.5f" % (float(pFandWandNotO)/pWandNotO)
print "WatchesTV=False,OutOfCatFood=True	%.5f" % (float(pFandOandNotW)/pNotWandO)
print "WatchesTV=False,OutOfCatFood=False	%.5f\n" % (float(f - pFandWandO - pFandWandNotO - pFandOandNotW) / pNotWandNotO)
