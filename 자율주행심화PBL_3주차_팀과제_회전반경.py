# 자율주행심화PBL_회전반경
# 2021271424 장현서 / 2021271429 이민석 / 2021271428 진유리 / 2021271421 최승권

'''
<2번 - 회전반경>
[speed 50 고정]
-1.0 = 67.5cm
+1.0 = 60cm

[speed 65 고정]
-1.0 = 77.5cm
+1.0 = 62.5cm

[speed 80 고정]
-1.0 = 80cm
+1.0 = 75cm
'''

import math
import time 
from pop import Pilot
Car = Pilot.AutoCar()


def cal_theta(speed, distance):
    if speed == 50:
        if (distance<=100)and(0<distance):
            theta = math.asin(distance/120)
        elif (100<distance)and(distance<=150):
            theta = math.asin(distance/150)
        else:
            print("지원되지 않는 값을 입력했습니다.")
    elif speed == 80:
        if (distance<=110)and(0<distance):
            theta = math.asin(distance/135)
        elif (110<distance)and(distance<=160):
            theta = math.asin(distance/160)
        else:
            print("지원되지 않는 값을 입력했습니다.")
    else:
        print("오류 발생")
    return(theta)


def cal_sec(steering, speed, distance):
    theta = cal_theta(speed, distance)
    if speed == 50:
        if steering == 1.0:
            return theta/right_50
        elif steering == -1.0:
            return theta/left_50

    elif speed == 80:
        if steering == 1.0:
            return theta/right_80
        elif steering == -1.0:
            return theta/left_80


Car.steering=0

print("롤스로이스급 승차감을 원하시면 50을,\n정신못차릴 정도로 빠르게 달리고 싶으시다면 80을 입력해주세요 :")
speed = input()
print("원하는 위치의 직선 거리(현의 길이)를 입력해주세요 (cm)")
distance = input()
print("원하는 회전 방향을 알려주세요 (오른쪽 : 1.0, 왼쪽 : -1.0)")
steering = input()

# 둘레 1초당 몇 도 가는지 계산 (((지름*pi)/2)/180도에 걸린 시간)
right_50 = ((150*math.pi)/2)/2.0
left_50 = ((135*math.pi)/2)/2.7
right_80 = ((150*math.pi)/2)/1.3
left_80 = ((160*math.pi)/2)/1.5

Car.steering = steering
Car.setSpeed(speed)
Car.forward()
time.sleep(cal_sec(steering,speed,distance))
Car.stop()