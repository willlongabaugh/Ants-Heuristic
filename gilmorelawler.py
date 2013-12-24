# given a pair of cost matrices
# compute matrix L as given in li et al for a given 1..n
# solve linear assignment problem (using the Hungarian method)


from munkres import Munkres, print_matrix
    

"""
A module to compute gilmore-lawler bounds on QAP instances
"""

def minpdp(v,w):
    # computes a permutation with minimum permuted dot product of vectors v and w
    # pairs largest with smallest, next largest with next smallest, and so on and so on
    #perm = [None for n in range(len(v))]
    #vperm = sorted(range(n), key=lambda k: v[k])
    #wperm = sorted(range(n), key=lambda k: w[k],reverse=True)
    vs = sorted(v)
    ws = sorted(w,reverse=True)
    sum = 0
    for x in [vs[i] * ws[i] for i in range(len(v))]:
        sum = sum + x
    return sum
#    return reduce(lambda x,y:x+y, [vs[i] * ws[i] for i in range(len(v))])
    

    
def lb(a,b):
    n = len(a)

    l = [ [minpdp([a[i][ind] for ind in range(n) if ind != i],[b[j][ind] for ind in range(n) if ind != j]) for j in range(n)] for i in range(n) ]

    # now solve linear assignment problem on l
    m = Munkres()

    indices = m.compute(l)

    #print(indices)

    total = 0
    for row, column in indices:
        val = l[row][column]
        total += val
        #print '(%d, %d) -> %d' % (row,column,val)
    return total
def qap_objective(a,b,perm):
    cost = 0
    for i in range(len(perm)):
        for j in range(len(perm)):
            cost += a[i][j]*b[perm[i]][perm[j]]
    return cost

def lbpartial(a,b,perm):
    """
    Compute a lower bound for a partially-assigned QAP instance.
    Assumes locations will be assigned in order 0..n; facilities can
    be put in locations in any order.

    This follows the procedure in Maniezzo et al "The ant system applied to
    the quadratic assignment problem" but note that there seem to be typos in their 
    paper (esp involving limits on summations).
    """
    assigned_costs = qap_objective(a,b,perm)
    if len(perm) == len(a):
        return assigned_costs
    
    # the indices 0..len(perm) are the locations assigned so far
    # this is just deleting rows/columns of a matrix
    apartial = [ [a[i][j] for j in range(len(a[i])) if j not in range(len(perm))] for i in range(len(a)) if (i not in range(len(perm)) ) ]
    #print apartial

    # the values in perm are the facilities assigned so far
    # again, we're deleting rows/columns from matrix
    # taking minors, like when computing a determinant
    bpartial = [ [b[i][j] for j in range(len(b[i])) if j not in perm] for i in range(len(b)) if i not in perm ]
    #print bpartial
    reduced_bound = lb(apartial,bpartial)

    # here we compute the actual cost of all assignments so far
    #for i in range(len(perm)):
    #    for j in range(len(perm)):
    #        assigned_costs += a[i][j]*b[perm[i]][perm[j]]
    #print assigned_costs

    cost_matrix = [ [0 for j in range(len(a[i])-len(perm))] for i in range(len(a)-len(perm)) ]

    unassigned_locations = [loc for loc in range(len(a)) if loc not in range(len(perm))]
    #print(unassigned_locations)
    unassigned_facilities = [fac for fac in range(len(a)) if fac not in perm]
    #print(unassigned_facilities)

    #this is part of the maniezzo paper, but i can't get it to
    #work and they are quite vague

    for real_row in range(len(unassigned_facilities)):
        m = unassigned_facilities[real_row]
        for real_col in range(len(unassigned_locations)):
            l = unassigned_locations[real_col]
            cost = 0
            for i in range(len(perm)):
                toadd = a[i][l]*b[perm[i]][m] + a[l][i]*b[m][perm[i]]
                cost += toadd
                    # print toadd
                    #print "(%d,%d); (%d,%d) -> %d" % (real_row,real_col,m,l,cost)
            cost_matrix[real_row][real_col] = cost
            
            #print cost_matrix
    m = Munkres()
    indices = m.compute(cost_matrix)
    middle_lb = 0
    for row,column in indices:
        middle_lb += cost_matrix[row][column]
        #print middle_lb

    return assigned_costs + reduced_bound + middle_lb


def greedy_generate(a,b):
    """
    Greedily generates a solution following the best lower bound.
    """

    perm = []
    for loc in range(len(a)-2):
        print(loc)
        facilities = [i for i in range(len(a)) if i not in perm]
        lbs = [ lbpartial(a,b,perm+[f]) for f in facilities ]
        print(lbs)
        perm += [facilities[lbs.index(min(lbs))]]
        print(perm)
    
    # now explicitly generate the last two solutions
    remaining = [fac for fac in range(len(a)) if fac not in perm] # ought to be length 2
    choices = [ perm + [remaining[0],remaining[1]], perm + [remaining[1],remaining[0]]]
    vals = [qap_objective(a,b,choice) for choice in choices]
    return choices[vals.index(min(vals))]

def test_gilmorelawler():
    """ Tests on the example problem in the Maniezzo paper. """
    # basic test code
    a = [ [0,1,1,2,3],
          [1,0,2,1,2],
          [1,2,0,1,2],
          [2,1,1,0,1],
          [3,2,2,1,0] ]

    b = [ [0,5,2,4,1],
          [5,0,3,0,2],
          [2,3,0,0,0],
          [4,0,0,0,5],
          [1,2,0,5,0] ]

    #print lb(a,b)
    print(lbpartial(a,b,[1]))
    print(greedy_generate(a,b))

test_gilmorelawler()
