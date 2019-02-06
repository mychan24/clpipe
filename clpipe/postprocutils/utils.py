import numpy
from scipy.signal import butter, sosfilt


def find_sub_list(sl,l):
    results=[]
    sll=len(sl)
    for ind in (i for i,e in enumerate(l) if e==sl[0]):
        if l[ind:ind+sll]==sl:
            results.append((ind,ind+sll))

    return results

def scrub_setup(fdts, fd_thres = .3, fd_behind = 1, fd_ahead = 1, fd_contig = 3):
    scrubTargets = [i for i, e in enumerate(fdts) if e > fd_thres]

    for t in numpy.arange(0, fd_behind+1):
        scrubTargetsAdd = scrubTargets - t
        scrubTargets.extend(scrubTargetsAdd)

    for t in numpy.arange(0, fd_ahead+1):
        scrubTargetsAdd = scrubTargets + t
        scrubTargets.extend(scrubTargetsAdd)

    scrubTargets = list(set(scrubTargets))
    scrubTargets = [e for i, e in enumerate(scrubTargets) if e >= 0]
    scrubTargets= [e for i, e in enumerate(scrubTargets) if e <= len(fdts)-1]
    scrubTargets = set(scrubTargets)
    scrubVect = [0]*len(fdts)
    scrubVect = [1 if i in scrubTargets else 0 for i,e in enumerate(scrubVect)]

    if fd_contig > 0:
        target = [0]*fd_contig
        contigSets = find_sub_list(target, scrubVect)
        scrubVectTemp = [1]*len(fdts)
        for conSet in contigSets:
            scrubVectTemp[conSet[0]:conSet[1]] = target
        scrubVect = scrubVectTemp
    return scrubVect


def scrub_image(data, fdts):
    scrubTargets = [i for i, e in enumerate(fdts) if e == 1]
    data[scrubTargets,:] = numpy.nan
    return data

def calc_filter(hp, lp, tr, order):

    nyq = 1/(tr*2)
    l = lp / nyq
    h = hp / nyq

    if l >0 and h <=0:
        sos = butter(order, l, analog=False, btype='lowpass' , output='sos')
    if l <= 0 and h > 0:
        sos = butter(order, h, analog=False, btype='highpass', output='sos')
    if l > 0 and h > 0:
        sos = butter(order, [h,l], analog=False, btype='bandpass', output='sos')
    if l <= 0 and h <= 0:
        sos = "none"
    return sos

def apply_filter(sos, arr):
    if sos is "none":
        return arr
    else:
        toReturn = sosfilt(sos, arr, axis = 0)
        return toReturn

def regress(pred, target):
    A = numpy.linalg.pinv(pred)
    beta = (numpy.matmul(A, target))
    predVal = numpy.matmul(pred, beta)
    toReturn = target - predVal
    return(toReturn)