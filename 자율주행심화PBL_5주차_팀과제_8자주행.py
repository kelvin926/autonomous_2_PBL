# 자율주행심화PBL_8자주행
# 2021271424 장현서 / 2021271429 이민석 / 2021271428 진유리 / 2021271421 최승권

import time 
from pop import Pilot

def playsound(m): # playsound 모듈 대신 사용
    print(m)

class AutoCarN(Pilot.AutoCar):

    super().setSensorStatus(ultrasonic, axis9, euler, gravity, battery, cds) # 센서 받아옴

    def voltage(self):
        battery = super().getBattery() # 현재 전압과 온도 반환
        voltage = battery[0] # 전압, 슬라이스 범위 수정 예정
        return voltage

    def turn_on(self): # 시동 킴
        playsound("turn_on.mp3")
        playsound("voltage"+voltage()+".mp3") # 높음/보통/낮음
    
    def turn_off(self): # 시동 끔
        playsound("turn_off.mp3")
        playsound("voltage"+voltage()+".mp3") # 높음/보통/낮음

    def setSpeed(self, speed): # 속도 변경
        if speed == 80:
            playsound("Speed_80.mp3")
            playsound("Fast.mp3") # 빠른 승차감
        elif speed == 50:
            playsound("Speed_50.mp3")
            playsound("Soft.mp3") # 편안한 승차감
        else:
            playsound("Error.mp3")
        super().setSpeed = speed

    def forward(self, speed = None): # 전진
        playsound("forward.mp3")
        super().forward(speed)

    def backward(self, speed = None): # 후진
        playsound("backward.mp3")
        playsound("reverse.mp3") # 후진 시 소리
        super().backward(speed)

    def turn_left(self, steering = -1.0): # 좌회전
        playsound("turn_left.mp3")
        playsound("signal.mp3") # 좌회전 신호음
        super().steering = steering

    def turn_right(self, steering = 1.0): # 우회전
        playsound("turn_right.mp3")
        playsound("signal.mp3") # 우회전 신호음
        super().steering = steering

    def stop(self): # 일시 정지
        playsound("stop.mp3")
        super().stop()

    def horn(self): # 경적 울림
        playsound("horn.mp3")

    def get_cds_sensor(self):
        cds = super().getLight()
        pass # 어두움 / 밝음 감지 후 소리 출력 예정

'''
[ 추가 예정 알람 기능 ]
- 전방 충돌 감지 (AEB) - (비프음) by 전방 초음파 센서
- 차선 변경 경고 (LKA) (비프음) - 카메라 사용
- 측면 충돌 경고 (FCA-LS(Line-Change)) - (비프음) - 라이다 사용
- 라이다 작동 시작 종료
- 전후방 거리 감지 (비프음 - 저음/중음/고음) (멀리 / 중간 / 가까이) - by 라이다
'''

car = AutoCarN()

# 8자 주행 시나리오

car.turn_on() # 시동 킴

car.setSpeed(50)
car.turn_right()
car.forward()
time.sleep(3.0) # 3초동안 우회전 후 일시정지
car.stop()

car.setSpeed(80)
car.turn_left()
car.forward()
time.sleep(3.0) # 3초동안 좌회전 후 일시정지
car.stop()

car.setSpeed(50)
car.turn_right()
car.forward()
time.sleep(1.0) # 1초동안 우회전 후 일시정지
car.stop()

car.turn_off() # 시동 끔