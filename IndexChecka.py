def findIndex(stringArr, keyString):
 
    #  Iteration over all the elements
    #  of the 2-D array
    #  Rows
    for i in range(0,len(stringArr)):
        if stringArr[i][0] == keyString:
            return i

