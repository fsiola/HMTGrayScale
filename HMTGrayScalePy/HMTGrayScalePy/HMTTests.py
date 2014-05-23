from HMT import *
from Utils import *

def main():
    #KSHMT - Adapted example from original paper
    f = array([0,0,10,10,10,0,0,5,10,5,0,0,10,10,10,0,0])
    se = array([5,10,5])
    result = ksHMT(f, se)
    print(result)

    #KSHMT
    f = array([0,0,255,255,255,0,0,100,255,100,0,0,255,255,255,0,0])
    bfg = array([25,25,25])
    bbg = array([255,255,255])
    result = ksHMT(f, bfg)
    print(result)

    #SUHMT
    f = array([0,0,255,255,255,0,0,100,255,100,0,0,255,255,255,0,0])
    bfg = array([25,25,25])
    bbg = array([255,255,255])
    result = suHMT(f, bfg, bbg)
    print(result)

    #BHMT
    f = array([0,0,255,255,255,0,0,100,255,100,0,0,255,255,255,0,0])
    bfg = array([25,25,25])
    bbg = array([255,255,255])
    result = bHMT(f, bfg, bbg)
    print(result)

    #RHMT
    f = array([0,0,255,255,255,0,0,100,255,100,0,0,255,255,255,0,0])
    bfg = array([25,25,25])
    bbg = array([255,255,255])
    result = rHMT(f, bfg, bbg)
    print(result)

    #RGHMT
    f = array([0,0,255,255,255,0,0,100,255,100,0,0,255,255,255,0,0])
    bfg = array([25,25,25])
    bbg = array([255,255,255])
    result = rgHMT(f, bfg, bbg)
    print(result)

if __name__ == "__main__":
    main() 