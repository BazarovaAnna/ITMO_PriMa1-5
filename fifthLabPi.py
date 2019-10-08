#Вычислить параметры кода d, m, k, p, l, S. Найти образующий многочлен,
#воспользовавшись таблицей неприводимых многочленов.   Проверить, имеются
#ли ошибки в исследуемой комбинации, при наличии ошибок – исправить их.
#Провести программный контроль выполнения  на примере случайных кодовых
#комбинаций

import numpy as np
import LinearBlockCode as lbc
from GaloisField import GF2, X, degree #для образующего многочлена
#из таблицы неприводимых двоичных многочленов
from LinearBlockCode import LinearBlockCode 

#Каждый массив будем переворачивать
#    Это делает библиотека:
#        [0,1,0,1] -> X^2 + 1
#    Это получим мы:
#        [0,1,0,1] -> X + X^3 

def shift(v, i = 1): #циклический сдвиг на 1
    return np.roll(v, i) 
 
def encode(m, g, systematic = True):
    if systematic:
        r = degree(g) # r = n - k
        Xr = X(r) # X^(n-k)
        XrmX = GF2.multPoly(Xr, m) # X^(n-k) * m(X)
        p = GF2.modPoly(XrmX, g) # p(X) = (X^(n-k) * m(X)) mod g(X) 
        c = GF2.addPoly(p, XrmX) # c(X) = p(X) + (X^(n-k) * m(X))
    else:
        c = GF2.multPoly(m, g)
    return c.astype(int) 
 
def gToG(g, n, systematic = True, verbose = False):#получаем образующую матрицу
    k = n - degree(g)
    g = padEnd(g, n)
    G = np.empty([k, n])
    for i in range(0, k):
        G[i,:] = shift(g, i)
    # матрицу необходимо повернуть
    # -> systematic form
    if systematic:
        G = makeSystematic(G, verbose) 
    return G.astype(int) 
 
def makeSystematic(G, verbose = True):
    k, n = G.shape
    if verbose:
        print('unsystematic:')
        print(G.astype(int))
        print() 
 
    # start with bottom row
    for i in range(k-1, 0, -1):
        if verbose: s = ''
        # start with most right hand bit
        for j in range(n-1, n-k-1, -1):
            # eleminate bit if it does not belong to identity matrix
            if G[i,j] == 1 and i != j-(n-k):
                if verbose: s += ' + g' + str(k-n+j)
                G[i,:] = (G[i,:] + G[k-n+j,:]) % 2 
 
        if verbose and s != '':
            print('g' + str(i) + ' = g' + str(i) + s)
            print(G.astype(int));
            print()
    return G.astype(int) 

def printAllCyclicCodes(factorPolynomials):#выводим все циклические коды, которые можем сделать

    s = ''
    product = np.array([])
    for i in range(0, len(factorPolynomials)):
        if i == 0:
            product = factorPolynomials[i]
        else:
            product = GF2.multPoly(product, factorPolynomials[i])
            s += '(' + GF2.polyToString(factorPolynomials[i]) + ') '
    print(s + '= ' + GF2.polyToString(product))
    print() 
 
    numberCodes = 2**(len(factorPolynomials)) - 2
    n = degree(product)
    print('Всего возможны', numberCodes, 'различных циклических кодов длиной', n)
    print('так как мы можем найти', numberCodes, 'различных неприводимых двоичных полиномов')
    print(GF2.polyToString(product))
    print(np.bitwise_and(1, 3))
     
    print('Code <- Generator polynomial')
    for i in range(0, numberCodes):
        s = ''
        gp = np.array([]) # generator polynomial
        for j in range(0, len(factorPolynomials)):
            if np.bitwise_and(i+1, 2**j) > 0:
                if s =='':
                    gp = factorPolynomials[j]
                else:
                    gp = GF2.multPoly(gp, factorPolynomials[j])
                s += '(' + GF2.polyToString(factorPolynomials[j]) + ')' 
 
        print('Ccyc(' + str(n) + ', ' + str(degree(gp)) + ') <- g' + str(i+1) + ' = ' + s + ' = ' + GF2.polyToString(gp)) 
 
def padEnd(p, length):
    assert p.size <= length, \
           "padEnd() failed because polynomial is longer than given size." 
 
    p = np.pad(p, (0, length-p.size), 'constant', constant_values=0)
    return p 
 
class CyclicCode(LinearBlockCode):
    """
    Cyclic Code 
    Attr:
        _g: The Generator Polynomial of the Cyclic Code
        _n: Code length
    """ 
 
    _g = np.empty([0])
    _n = 0 
 
    def __init__(self, g, n):
        assert g[0] == 1, \
               "g0 must equal to 1"
        assert n >= degree(g), \
               "n=%i must be >= degree(g)=%i" % (n, degree(g))
        self._g = g[:n]; #auto remove too much dangling zeros
        self._n = n 
 
    def g(self):
        return self._g.astype(int) 
 
    def printg(self):
        print(GF2.polyToString(self.g())) 
 
    def n(self): # override
        return self._n 
 
    def k(self): # override
        return self.n() - degree(self.g()) 
 
    def dmin(self, verbose = False): # override
        #(LinearBlockCode dmin would work, but is slower)
            dmin = lbc.w(self.g())
            if verbose:
                print()
                print('Minimum Hamming distance (d_min) equals weight of generator polynomial g(X):')
                print('g(X) =', GF2.polyToString(self.g()))
                print('d_min =', dmin)
                print()
            return dmin 
 
    def dminVerbose(self):
        self.dmin(True) 
 
    def G(self, systematic = True, verbose = False): # override
        return gToG(self.g(), self.n(), systematic, verbose) 
 
    def setG(self): # override
        assert False, "setG() not usable with cyclic codes." 
 
    def setH(self): # override
        assert False, "setH() not usable with cyclic codes." 
 
    def shift(self, c, i = 1):
        """
        Cyclic right shift of c using division
        """
        Xi = X(i) # X^i polynomial
        XiCX = GF2.multPoly(Xi, c) # X^i * c(X) polynomial
        Xn1 = GF2.addPoly(X(self.n()), X(0)) # X^n + 1 polynomial
        ci = GF2.modPoly(XiCX, Xn1) # i times shifted c
        return padEnd(ci, self.n()) 
 
    def c(self, m, systematic = True): # override
        """
        encode message polynomial m
        Args:
            m: message polynomial
            systematic: return codeword in systematic form (default: True)
        Returns:
            codeword
        """
        c = encode(m, self.g(), systematic)
        return padEnd(c, self.n()) 
 
    def printMessageCodewordTable(self, systematic = True): # override
        """
        Print all messages and their corresponding codewords.
        Args:
            systematic: print codewords in systematic form (default: True)
        """
        M = self.M()
        print('Messages -> Codewords')
        for m in M:
            c = self.c(m, systematic)
            print(m, c, 'm(X) =', GF2.polyToString(m), '\tc(X) =', GF2.polyToString(c) )
            
    def S(self, r):
        """
        Calculate Syndrome polynomial from receive or error polynomial.
        Args:
            r: receive or error polynomial
        Returns:
            Syndrome polynomial
        """
        return GF2.modPoly(r, self.g()) 
 
    def shiftSyndrome(self, S, i = 1):
        """
        Shift syndrome i times
        """
        for i in range(0, i):
            # S1(X) = XS(X) mod g(X)
            S = GF2.modPoly(GF2.multPoly(X(1), S), self.g())
        return S

