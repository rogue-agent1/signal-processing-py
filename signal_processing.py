import math
def moving_average(signal,window):
    result=[]
    for i in range(len(signal)):
        start=max(0,i-window//2); end=min(len(signal),i+window//2+1)
        result.append(sum(signal[start:end])/(end-start))
    return result
def low_pass(signal,cutoff,sr):
    n=len(signal); alpha=1/(1+sr/(2*math.pi*cutoff))
    result=[signal[0]]
    for i in range(1,n): result.append(alpha*signal[i]+(1-alpha)*result[-1])
    return result
def high_pass(signal,cutoff,sr):
    lp=low_pass(signal,cutoff,sr)
    return [signal[i]-lp[i] for i in range(len(signal))]
def rms(signal): return math.sqrt(sum(x**2 for x in signal)/len(signal))
def zero_crossings(signal):
    return sum(1 for i in range(1,len(signal)) if signal[i-1]*signal[i]<0)
def autocorrelate(signal,max_lag=None):
    n=len(signal); max_lag=max_lag or n//2
    result=[]
    for lag in range(max_lag):
        s=sum(signal[i]*signal[i+lag] for i in range(n-lag))/n
        result.append(s)
    return result
if __name__=="__main__":
    sr=100; t=[i/sr for i in range(200)]
    signal=[math.sin(2*math.pi*5*x)+0.3*math.sin(2*math.pi*50*x) for x in t]
    smoothed=moving_average(signal,10)
    assert rms(smoothed)<rms(signal)  # smoothing reduces amplitude
    lp=low_pass(signal,10,sr)
    hp=high_pass(signal,10,sr)
    assert rms(lp)<rms(signal)
    zc=zero_crossings(signal)
    assert zc>10
    ac=autocorrelate(signal,50)
    assert ac[0]>ac[10]  # autocorrelation peaks at lag 0
    print(f"RMS: orig={rms(signal):.3f}, smoothed={rms(smoothed):.3f}")
    print(f"Zero crossings: {zc}")
    print("All tests passed!")
