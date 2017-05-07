# -*- coding: utf-8 -*-
def sortlist(inputlist):
    """
        :param inputlist: eg:[1,2,3,[4,5,6],[1,2]]
        :return outputlist: eg:[1,2,3,4,5,6,1,2]
    """
    outputlist=[]
    for x in inputlist:
        if isinstance(x,list):
            outputlist.extend(sortlist(x))
        else:
            outputlist.append(x)
    return outputlist
print sortlist([1,2,3,[4,5,6],[1,2]])

