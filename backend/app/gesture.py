import math

def distance(a, b):
    return math.hypot(a[0]-b[0], a[1]-b[1])

def is_pinch(hand_landmarks, threshold=0.05):
    
    t = hand_landmarks[4]
    i = hand_landmarks[8]
    d = distance((t.x, t.y), (i.x, i.y))
    return d < threshold

def is_point(hand_landmarks, finger_extended_threshold=0.02):
   
    def y(a): return a.y
    index_extended = (y(hand_landmarks[8]) < y(hand_landmarks[6]) - finger_extended_threshold)
    middle_folded = (y(hand_landmarks[12]) > y(hand_landmarks[10]) - 0.01)
    ring_folded   = (y(hand_landmarks[16]) > y(hand_landmarks[14]) - 0.01)
    pinky_folded  = (y(hand_landmarks[20]) > y(hand_landmarks[18]) - 0.01)
    return index_extended and middle_folded and ring_folded and pinky_folded

def is_open(hand_landmarks):
    
    tips = [hand_landmarks[i] for i in (4, 8, 12, 16, 20)]
    base = hand_landmarks[0]
    avg_dist = sum([distance((t.x, t.y), (base.x, base.y)) for t in tips]) / len(tips)
    return avg_dist > 0.15  
