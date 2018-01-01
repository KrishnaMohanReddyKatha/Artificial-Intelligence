
"""    written by
       Name : Krishna Mohan Reddy Katha, Anshul Dupare
       NetId : Kxk171830,axd171630 """

import random
BN = {}
BN["B"] = {"Parent":[],"CPT":[0.001]}
BN["E"] = {"Parent":[],"CPT":[0.002]}
BN["A"] = {"Parent":["B","E"],"CPT":[0.95,.94,0.29,0.001]}
BN["J"] = {"Parent":["A"],"CPT":[0.90,0.05]}
BN["M"] = {"Parent":["A"],"CPT":[0.70,0.01]}

def EnumerationAsk(X,E) :
     Y = ["B", "E", "A", "J", "M"]
     Q =[]
     Ex = E[:]
     Ex.append((X,'t'))
     result1 = 0.0
     result1 = EnumerateAll(Y,Ex)
     Ex = E[:]
     Ex.append((X, 'f'))
     result2 = 0.0
     result2 = EnumerateAll(Y,Ex)
     sum = 0.0
     sum = result1 + result2
     result1 =  float (float(result1)/float(sum))
     result2 = float (float(result2)/float(sum))
     return [result1,result2]

def prob(val, var, Ex):
    pb = 0
    if(len(BN[var]['Parent']) == 0):
        if val == 't' :
           return BN[var]['CPT'][0]
        else:
           return (1 - BN[var]['CPT'][0])
    elif(len(BN[var]['Parent']) == 1):
        for item in Ex :
            if item[0] == BN[var]['Parent'][0] and item[1] == 't':
                if val == 't':
                 return BN[var]['CPT'][0]
                else:
                 return (1 - BN[var]['CPT'][0])
            if item[0] == BN[var]['Parent'][0] and item[1] == 'f':
                if val == 't':
                 return BN[var]['CPT'][1]
                else:
                 return (1 - BN[var]['CPT'][1])
    elif(len(BN[var]['Parent']) == 2):
        p =[]
        for item in BN[var]['Parent'] :
            for it in Ex:
                if it[0] == item :
                    p.append(it[1])
        if(p[0] == 't' and p[1] == 't'):
            pb = BN[var]['CPT'][0]
        elif(p[0] == 't' and p[1] == 'f'):
            pb = BN[var]['CPT'][1]
        elif(p[0] == 'f' and p[1] == 't'):
            pb = BN[var]['CPT'][2]
        elif(p[0] == 'f' and p[1] == 'f'):
            pb = BN[var]['CPT'][3]
        if val == 'f':
            pb = 1 - pb
    return float(pb)

def EnumerateAll(Y,Ex):
     if len(Y) == 0 :
         return 1
     yNew = Y[:]
     yNew.pop(0)
     pRes = 0.0
     eRes = 0.0
     fRes = 0.0
     if ((Y[0],'t') in Ex or (Y[0],'f') in Ex):
         if((Y[0],'t') in Ex):
             pRes = prob('t',Y[0],Ex)
             eRes = float(EnumerateAll(yNew,Ex))
             fRes = pRes*eRes
             return fRes
             #return prob('t',Y[0],Ex) * float(EnumerateAll(yNew,Ex))
         else:
             pRes = prob('f', Y[0], Ex)
             eRes = float(EnumerateAll(yNew, Ex))
             fRes = pRes*eRes
             return fRes
             #return prob('f', Y[0], Ex) * float(EnumerateAll(yNew, Ex))
     else:
         NEx1 = Ex[:]
         NEx1.append((Y[0],'t'))
         NEx2 = Ex[:]
         NEx2.append((Y[0],'f'))
         prob1 = 0.0
         E1 = 0.0
         prob2 = 0.0
         E2 = 0.0
         finalRes = 0.0
         prob1 = prob('t', Y[0], Ex)
         E1 = float(EnumerateAll(yNew,NEx1))
         prob2 = prob('f',Y[0],Ex)
         E2 = float(EnumerateAll(yNew,NEx2))
         finalRes = float((prob1*E1) + (prob2 * E2))
         return finalRes
         #return  * float(EnumerateAll(yNew,NEx1)) + prob('f',Y[0],Ex) * float(EnumerateAll(yNew,NEx2))
def WeightedSample(E):
    w = 1.0
    truthV = {"B":"t","E":"t","A":"t","J":"t","M":"t"}
    totVar = ["B","E","A","J","M"]
    for item in E :
        truthV[item[0]] = item[1]
    Enew = E[:]
    for var in totVar:
        pob = 0.0
        if (var,"t") in E :
           pob = prob("t",var,Enew)
           w = w * pob
        elif((var,"f") in E) :
           pob = prob("f",var,Enew)
           w = w * pob
        else:
            rand = random.uniform(0,1)
            check = 0.0
            if len(BN[var]["Parent"]) == 0 :
                check = BN[var]["CPT"][0]
            elif len(BN[var]["Parent"]) == 1 :
                 if truthV[BN[var]["Parent"][0]] == "t" :
                     check = BN[var]["CPT"][0]
                 else :
                     check = BN[var]["CPT"][1]
            elif len(BN[var]["Parent"]) == 2 :
                 if truthV[BN[var]["Parent"][0]] == "t" and truthV[BN[var]["Parent"][1]] == "t" :
                     check = BN[var]["CPT"][0]
                 elif truthV[BN[var]["Parent"][0]] == "t" and truthV[BN[var]["Parent"][1]] == "f" :
                     check = BN[var]["CPT"][1]
                 elif truthV[BN[var]["Parent"][0]] == "f" and truthV[BN[var]["Parent"][1]] == "t" :
                     check = BN[var]["CPT"][2]
                 elif truthV[BN[var]["Parent"][0]] == "f" and truthV[BN[var]["Parent"][1]] == "f" :
                     check = BN[var]["CPT"][3]
            if rand <= check :
                truthV[var] = "t"
                Enew.append((var,"t"))
            else:
                truthV[var] = "f"
                Enew.append((var,"f"))
    return truthV,w

if __name__ == "__main__" :
    input = raw_input("enter the input \n")
    N = int(raw_input("enter the sampling size"))
    E = []
    X = []
    flag = 1
    index = 2
    if input[0] == "[" and input[1] == "<" :
        while(flag):
            E.append((input[index],input[index+2]))
            index = index+4
            if(input[index]== "]"):
                flag = 0
            index = index+1
        flag = 1
        index = index+1
        while(flag):
            X.append(input[index])
            if(input[index+1] == "]"):
                flag = 0
            index = index + 2
    enumOutput = "["
    for itm in X :
     result = EnumerationAsk(itm,E)
     enumOutput += "<" + itm + "," + str(result[0]) + ">"
    enumOutput+="]"
    print "Enumeration : " + enumOutput

    # prior sampling
    #N = 10  #take input for no of samples if needed
    Y =["B", "E", "A", "J", "M"]
    prDic = {"B":[],"E":[],"A":[],"J":[],"M":[]}
    for item in Y:
        if len(BN[item]["Parent"]) == 0:
            for i in range(N):
               rand = random.uniform(0,1)
               if rand <= BN[item]["CPT"][0]:
                prDic[item].append("t")
               else:
                prDic[item].append("f")
        elif len(BN[item]["Parent"]) == 1:
               for i in range(N):
                   rand = random.uniform(0,1)
                   if prDic[BN[item]["Parent"][0]][i] == "t" :
                       check = BN[item]["CPT"][0]
                   else:
                       check = BN[item]["CPT"][1]
                   if rand <= check:
                         prDic[item].append("t")
                   else:
                       prDic[item].append("f")
        elif len(BN[item]["Parent"]) == 2:
               for i in range(N):
                   rand = random.uniform(0,1)
                   if prDic[BN[item]["Parent"][0]][i] == "t" and prDic[BN[item]["Parent"][1]][i] == "t" :
                       check = BN[item]["CPT"][0]
                   elif prDic[BN[item]["Parent"][0]][i] == "t" and prDic[BN[item]["Parent"][1]][i] == "f" :
                       check = BN[item]["CPT"][1]
                   elif prDic[BN[item]["Parent"][0]][i] == "f" and prDic[BN[item]["Parent"][1]][i] == "t" :
                       check = BN[item]["CPT"][2]
                   elif prDic[BN[item]["Parent"][0]][i] == "f" and prDic[BN[item]["Parent"][1]][i] == "f" :
                       check = BN[item]["CPT"][3]
                   if rand <= check :
                        prDic[item].append("t")
                   else:
                        prDic[item].append("f")
    #print prDic
    #prior sampling calculation
    posCount = 0
    priorOutput = "["
    for itm in X :
        posCount = 0
        for i in range(N):
            if prDic[itm][i] == "t":
                posCount+=1
        prb = float((float(posCount))/float(N))
        priorOutput += "<" + itm + "," + str(prb) + ">"
        #print "[" + str(prb) + "," + str((1-prb))+ "]"
    priorOutput += "]"
    print "Prior Sampling : " + priorOutput

    #rejection Sampling calculation
    posCount = 0
    negCount = 0
    rejectionOutput = "["
    for itm in X :
        posCount = 0
        negCount = 0
        for i in range(N):
            flag = 1
            for evd in E :
                if prDic[evd[0]][i] != evd[1]:
                    flag = 0
            if flag == 1 and prDic[itm][i] == "t" :
                posCount+=1
            elif flag == 1 and prDic[itm][i] == "f" :
                negCount+=1
        if posCount != 0 or negCount != 0 :
          prb = float((float(posCount)/(float(posCount+negCount))))
          rejectionOutput += "<" + itm + "," + str(prb) + ">"
        else:
            rejectionOutput += "<" + itm + "," + str(0) + ">"
    rejectionOutput += "]"
    print "Rejection Sampling : " + rejectionOutput

    #likelihood
    W = {"t":0,"f":0}
    likelihoodOutput = "["
    for item in X:
     W["t"] = 0.0
     W["f"] = 0.0
     for i in range(N):
       truthVal,w = WeightedSample(E)
       W[truthVal[item]]+= w
     prb = float(float(W["t"])/float(W["t"] +W["f"]))
     likelihoodOutput += "<" + item + "," + str(prb) + ">"
    likelihoodOutput += "]"
    print "Likelihood Sampling : " + likelihoodOutput