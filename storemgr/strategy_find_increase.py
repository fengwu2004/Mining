# 寻找上升趋势中的调整浪
# 高点依次增加
# 最后一个低点的时间在最后一个高点的前面
# 当前价格比最近的低点高

def checkInAdjustWave (waveUnit):
    if len(waveUnit.crest) < 2 or len(waveUnit.trough) < 1:
        return False
    
    maxsLength = len(waveUnit.crest)
    
    minsLength = len(waveUnit.trough)
    
    
    if waveUnit.crest[maxsLength - 1].close * 0.90 <= waveUnit.crest[maxsLength - 2].close:
        return False
    
    
    if waveUnit.trough[minsLength - 1].date > waveUnit.crest[maxsLength - 1].date:
        return False
    
    
    if waveUnit.lastday.close < waveUnit.trough[minsLength - 1].close:
        return False
    
    return True