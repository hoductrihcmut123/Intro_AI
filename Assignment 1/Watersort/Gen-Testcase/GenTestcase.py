import random


for time in range(0,10):        
    level = 210 + time                                                # checkkkkkkkkkkkkkkkkk
    OutputPath = "Testcase/Testcase" + str(level) +".txt"          
    
    initStr = "aaaabbbbccccddddeeeeffffgggghhhhiiiijjjjkkkkllllmmmmnnnnooooppppqqqqrrrrssssttttuuuuvvvvwwww"     # checkkkkkkkkkkkkkkkkk
    genStr = ''.join(random.sample(initStr,len(initStr)))
    Grid = ["","","","","","","","","","","","","","","","","","","","","","","","",""]                        # checkkkkkkkkkkkkkkkkk
    k = 0

    for i in range(0,len(genStr)):
        if i!=0 and (i%4 == 0):
            k += 1
        Grid[k] += genStr[i]
        
    with open(OutputPath, mode='x') as f:
        f.write(str(level))
        f.write('\n')
        f.write(str(len(Grid)))
        f.write("\n")
        f.write("2")                
        f.write("\n")
        f.write(str(Grid))
        
    
    