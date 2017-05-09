'''
Created on Dec 14, 2016
    ver 1.1
@author: 
'''

class cRegime(object):
    def __init__(self):
        self.name = 'Regime'
        self.posMulti = 2
        self.newPos = 0    
        self.prevPos = 0    #need to load 
        self.entryPx = 0    #need to load 
        
        self.regimeID = 0
        self.trendID3 = deque([])     #len() == 3, regime ID [t-2, t-1, cur]
        self.trendOC = deque([])    #this trend's oc
        self.trendOCp = deque([])    #prev trend's oc
        self.trendOCpp = deque([])    #pp trend's oc
        self.currO = 0
        self.currC = 0
        self.prevO = 0    #need to load 
        self.prevC = 0    #need to load
        
    def tradeSequence(self):
        self.locRegime()
        self.grandTrend()
        self.tradeTrend()
        
    def locRegime(self):
        self.currO = currBar_O #self compiled bar data
        self.currC = currBar_C
        
        if np.maximum(self.currO, self.currC) > np.maximum(self.prevO, self.prevC) and np.minimum(self.currO, self.currC) > np.minimum(self.prevO, self.prevC):
            self.regimeID = 1
        elif np.maximum(self.currO, self.currC) < np.maximum(self.prevO, self.prevC) and np.minimum(self.currO, self.currC) < np.minimum(self.prevO, self.prevC):
            self.regimeID = 2
        else:
            self.regimeID = 3
            
    def grandTrend(self):
        if self.regimeID == self.trendID3[2]:
            self.trendOC.append(self.currO)
            self.trendOC.append(self.currC)
            print '%s - Still in Trend[%d], no trade needed    Time: %s' %(self.name,self.regimeID,timeNow) 
            self.newPos = self.prevPos
        else:
            self.trendID3.popleft()  
            self.trendID3.append(self.regimeID)     #update recent 3 trends
            
            self.trendOCp = deque(self.trendOC)        #updating OC for curr, p, pp 
            self.trendOCpp = deque(self.trendOCp)
            self.trendOC = deque([])
            self.trendOC.append(self.currO)
            self.trendOC.append(self.currC)

            if self.trendID3[2] == 1 and (self.trendID3[1] == 2 or self.trendID3[1] == 3) and self.trendID3[0] == 1:  #uptrend
                if np.amax(self.trendOC) > np.amax(self.trendOCpp) and np.amin(self.trendOCp) >= np.amin(self.trendOCpp): #this assumes 2 
                    if self.trendID3[1] == 3:
                        if np.amax(self.trendOCp) <= np.amax(self.trendOCpp):   #has extra condition 
                            self.newPos = -1
                    else:
                        self.newPos = -1
            elif self.trendID3[2] == 2 and (self.trendID3[1] == 1 or self.trendID3[1] == 3) and self.trendID3[0] == 2:  #downtrend
                if np.amin(self.trendOC) < np.amin(self.trendOCpp) and np.amax(self.trendOCp) <= np.amax(self.trendOCpp): #this assumes 1
                    if self.trendID3[1] == 3:
                        if np.amin(self.trendOCp) >= np.amin(self.trendOCpp):   #has extra condition 
                            self.newPos = 1
                    else:
                        self.newPos = 1
            else:  
                self.newPos = 0
                    
    def tradeTrend(self):
        toTradePos = (self.newPos - self.prevPos)
        if toTradePos != 0:
            """send order"""
            
cReg = cRegime


def main():
    cReg.tradeSequence()
    
main()