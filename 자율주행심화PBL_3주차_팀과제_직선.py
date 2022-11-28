# 자율주행심화PBL_직선
# 2021271424 장현서 / 2021271429 이민석 / 2021271428 진유리 / 2021271421 최승권

import time
from pop import Pilot
Car = Pilot.AutoCar()
Car.steering=0

print("롤스로이스급 승차감을 원하시면 50을,\n평범한 승차감을 원하시면 65을,\n정신못차릴 정도로 빠르게 달리고 싶으시다면 80을 입력해주세요  :")
speed = input()
print("원하는 거리를 입력해주세요 (cm)")
distance = input()

def cal_sec(speed, distance): # 50->43cm 65->60cm 80->78cm
    if speed == 50:
        return distance/43
    elif speed == 65:
        return distance/60
    elif speed == 80:
        return distance/78

Car.setSpeed(speed)
Car.forward()
time.sleep(cal_sec(speed,distance))

Car.stop()