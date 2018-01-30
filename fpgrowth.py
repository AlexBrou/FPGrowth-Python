readme='''

FPGrowth PYTHON
by Alex Brou, 28/01/2018

The dataset is stored at the variable __testcase__

Run the program.




showpatterns() - gets the frequent patterns

tree.printthis() - shows the fptree

showcondfptree() - shows the conditional fptree

showsupdict()    - shows a lot of stuff



'''


print(readme)

from operator import itemgetter
import copy
import itertools


testcase=[

[1,2,3],
[2,3],
[2]

]



testcase=[

"MONKEY",
"DONKEY",
"MAKE",
"MUCKY",
"COOKIE"

]


for i in range(len(testcase)):
    testcase[i]=list(testcase[i])
    




min_support=3


class FPTree:
    
    def __init__(self,label=None,father=None,count=0):
        self.label=label
        self.count=count
        self.father=father
        self.sons={}
        
    def makeson(self,label):
        self.sons[label]=FPTree(label,self,1)
        support_dict[label][1].append(self.getpath())
    
    def insertitemset(self,xs):
        node=self
        while xs!=[]:
            x=xs[0]
            if x in node.sons:
                node=node.sons[x]
                node.count+=1
            else:
                node.makeson(x)
                node=node.sons[x]
            xs=xs[1:]
            
    def printthis(self,deepness=0):
        for i in self.sons:
            ii=self.sons[i]
            print(deepness*"  ",end="")
            print(ii.label,":",ii.count)
            ii.printthis(deepness+1)
    
    def __str__(self):
        self.printthis()
        return ""
    
    def findnode(self,xs):
        node=self
        for i in xs:
            node=node.sons[i]
        return node

    def getpath(self):
        node=self
        ret=""
        while node.label!=None:
            ret=node.label+ret 
            node=node.father
        return ret
        
        


def get_support_list(arr):
    """Gets an array of arrays of items and returns a sorted array with each present item and its' support count"""
    dic={}
    for i in arr:
        uniques=[]
        for ii in i:
            if ii not in uniques:
                uniques.append(ii)
        for j in uniques:
            try:
                dic[j]+=1
            except KeyError:
                dic[j]=1
            
    itemset=[]
    for key, value in dic.items():
        itemset.append([key,value])
    itemset.sort(key=lambda x: x[1],reverse=True)
    
    return [dic,itemset]

#here's where min_support acts 
def reorder(xs):
    newar=[]
    for i in xs:
        if support_dict[i]>=min_support and i not in newar:
            newar.append(i)
    newar.sort(key=lambda x: support_dict[x],reverse=True)
    return newar
    




def transformed_dataset():
    ret=[]
    for i in testcase:
        ii=reorder(i)
        ret.append(ii)
    return ret
        

def transftotree(xs):
    for i in xs:
        tree.insertitemset(i)



def addapt_sup_dic():
    for i in support_dict:
        support_dict[i] = [ support_dict[i] , [] ]


def update_sup_dic():
    for i in support_dict:
        k=support_dict[i][1]
        newarr=[]
        for ii in range(len(k)):
            na=[k[ii]]
            na.append(  tree.findnode(k[ii]).sons[i].count     )
            newarr.append(na)
        support_dict[i][1]=newarr
        
            
            
def showsupdict():
    for i in support_dict:
        if support_dict[i][0]>=min_support:
            print(i , " : ",support_dict[i] )

def showcondfptree():
    for i in cond_fp_tree:
        if cond_fp_tree[i][0]>=min_support:
            print(i , " : ",cond_fp_tree[i] )    


def commonitemslist():
    for i in cond_fp_tree:
        if cond_fp_tree[i][0]>=min_support:
            ar=cond_fp_tree[i][1]
            naaa=[]
            for iii in ar:
                naaa.append(iii[0])
            naaa=getcommon(naaa)
            cond_fp_tree[i][1]=naaa


def getcommon(p):
    result = set(p[0])
    for s in p[1:]:
        result.intersection_update(s)
    return list(result)



def combinations(xs,xtra):
    ret=[]
    for L in range(1,len(xs)+1):
        for subset in itertools.combinations(xs,L):
            ret.append(    list(subset) +[xtra]      )
    return ret


class Pattern:
    
    def __init__(self,xs,sup):
        self.xs=xs
        self.sup=sup
    
    def __str__(self):
        return str(self.xs) + " : " +str(self.sup)

def getpatterns():
    ret=[]
    for i in cond_fp_tree:
        combs=combinations(   cond_fp_tree[i][1]  , i     )
        for j in combs:
            ret.append(   Pattern(j,cond_fp_tree[i][0])  )
    return ret
        

def showpatterns():
    for i in patterns:
        print(i)

def run():
    global support_list
    global support_dict
    
    #creates a support count list (how many times an item occurs)
    #without removing the items with a count below min_support
    support_dict , support_list = get_support_list(testcase)
    
    
    global transfset
    #reshapes the dataset, reordering the entries according to the support count. descending
    transfset=transformed_dataset()
    
    #dont mind this
    addapt_sup_dic()
    
    global tree
    #creates the FPTree and gets the items in the tree
    tree=FPTree()
    transftotree(transfset)
    
    #places the shortcuts to each item in the dictionary
    update_sup_dic()
    global cond_fp_tree
    cond_fp_tree=copy.deepcopy(support_dict)
    
    #gets the conditional fptree
    commonitemslist()
    
    global patterns
    #gets the patterns
    patterns=getpatterns()
    
run()