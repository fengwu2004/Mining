# 寻找上升趋势中的调整浪
# 高点依次增加
# 最后一个低点的时间在最后一个高点的前面
# 当前价格比最近的低点高

def checkInAdjustWave (waveUnit):
    if len(waveUnit.maxs) < 2 or len(waveUnit.mins) < 1:
        return False
    
    maxsLength = len(waveUnit.maxs)
    
    minsLength = len(waveUnit.mins)
    
    
    if waveUnit.maxs[maxsLength - 1].close * 0.90 <= waveUnit.maxs[maxsLength - 2].close:
        return False
    
    
    if waveUnit.mins[minsLength - 1].date > waveUnit.maxs[maxsLength - 1].date:
        return False
    
    
    if waveUnit.lastday.close < waveUnit.mins[minsLength - 1].close:
        return False
    
    return True