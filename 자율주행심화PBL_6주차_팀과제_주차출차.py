# 자율주행심화PBL_주차출차.py
# 2021271424 장현서 / 2021271429 이민석 / 2021271428 진유리 / 2021271421 최승권

import time 
from pop import Pilot
from pop import Tone
import math
from playsound import playsound
from multiprocessing import Process

def out_voice(wav_file):
    p = Process(target=playsound, args=(wav_file,))
    p.start()
    if (AutoCarN._out_voice != None):
            AutoCarN._out_voice.terminate()
            AutoCarN._out_voice = None
    return p

def ultrasonic(power_num):
        while power_num == 1:
            ultrasonic = AutoCarN.getUltrasonic()
            ultrasonic_re = str(ultrasonic) # 초음파 범위 수정 예정
            print(ultrasonic_re)

def processing_ultrasonic():
    global power_num
    power_num = 1
    for_ultrasonic = Process(target=ultrasonic, args=(power_num,))
    for_ultrasonic.start()

class AutoCarN(Pilot.AutoCar):
    _out_voice = None
    
    def __init__(self):
        super().__init__() # 부모쪽 생성자 -> 하드웨어 초기화 Code
        self.setSensorStatus(euler=1, gravity=1, battery=1, cds=1) # 모든 센서 받아옴

    def voltage(self):
        battery = self.getBattery() # 현재 전압과 온도 반환
        voltage = str(battery[0:1])
        voltage_re = float(voltage[1:5]) # 14.8V ~ 15.4V / 15.5V ~ 16.1V / 16.2V ~ 16.8V
        if voltage_re >= 14.8 and voltage_re <= 15.4:
            return "low"
        elif voltage_re >= 15.5 and voltage_re <= 16.1:
            return "normal"
        elif voltage_re >= 16.2 and voltage_re <= 16.8:
            return "high"
        else:
            return "error" # 전압 오류

    def turn_on(self): # 시동 킴
        self.power_num = 1
        out_voice("engine.wav")
        time.sleep(7)
        out_voice("turn_on.wav")
        time.sleep(2)
        out_voice("voltage_"+self.voltage()+".wav") # 높음/보통/낮음
        time.sleep(2)
    
    def turn_off(self): # 시동 끔
        self.power_num = 0
        out_voice("turn_off.wav")
        time.sleep(2)
        out_voice("voltage_"+self.voltage()+".wav") # 높음/보통/낮음
        time.sleep(2)

    def setSpeed(self, speed): # 속도 변경
        if speed == 80:
            out_voice("Speed_80.wav")
            time.sleep(1)
            out_voice("Fast.wav") # 빠른 승차감
            time.sleep(1)
        elif speed == 50:
            out_voice("Speed_50.wav")
            time.sleep(1)
            out_voice("Soft.wav") # 편안한 승차감
            time.sleep(1)
        elif speed == 30:
            out_voice("Speed_30.wav") # 느린 승차감
            time.sleep(1)
            out_voice("Slow.wav")
            time.sleep(1)
        else:
            out_voice("speed_error.wav")
            time.sleep(1)
        super().setSpeed(speed)

    def forward(self, speed = None): # 전진
        out_voice("forward.wav")
        super().forward(speed)

    def backward(self, speed = None): # 후진
        out_voice("backward.wav")
        # out_voice("reverse.wav") # 후진 시 소리
        super().backward(speed)

    def turn_left(self, steering = -1.0): # 좌회전
        out_voice("turn_left.wav")
        # out_voice("signal.wav") # 좌회전 신호음
        self.steering = steering

    def turn_right(self, steering = 1.0): # 우회전
        out_voice("turn_right.wav")
        # out_voice("signal.wav") # 우회전 신호음
        self.steering = steering
    
    def turn_straight(self, steering = 0): # 조향 앞으로
        # out_voice("turn_straight.wav")
        # out_voice("signal.wav") # 우회전 신호음
        self.steering = steering

    def stop(self): # 일시 정지
        # out_voice("stop.wav")
        super().stop()

    def horn(self): # 경적 울림
        out_voice("horn.wav")

    def get_cds_sensor(self):
        self.cds = super().getLight()
        pass # 어두움 / 밝음 감지 후 소리 출력 예정

    def cal_straight_sec(speed, distance): # 50->43cm 65->60cm 80->78cm 직선 이동 거리 계산
        if speed == 50:
            return distance/43
        elif speed == 65:
            return distance/60
        elif speed == 80:
            return distance/78

    def cal_theta(speed, distance):
        if speed == 50:
            if (distance<=100)and(0<distance):
                theta = math.asin(distance/120)
            elif (100<distance)and(distance<=150):
                theta = math.asin(distance/150)
            else:
                print("[오류] 지원되지 않는 값을 입력했습니다.")
        elif speed == 80:
            if (distance<=110)and(0<distance):
                theta = math.asin(distance/135)
            elif (110<distance)and(distance<=160):
                theta = math.asin(distance/160)
            else:
                print("[오류] 지원되지 않는 값을 입력했습니다.")
        else:
            print("오류 발생")
        return(theta)

    def cal_round_sec(steering, speed, distance):
        theta = self.cal_theta(speed, distance)
        right_50 = ((150*math.pi)/2)/2.0
        left_50 = ((135*math.pi)/2)/2.7
        right_80 = ((150*math.pi)/2)/1.3
        left_80 = ((160*math.pi)/2)/1.5
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

def main():
    car = AutoCarN()
    processing_ultrasonic()
###################### 구동 부분 시작 (여기 아래만 변경) ######################
    car.turn_on() # 시동 킴
    car.setSpeed(30)
    # car.forward()
    # time.sleep(5)
    # car.stop()
    # time.sleep(0.3)

    car.turn_straight()
    car.forward()
    time.sleep(0.9)
    car.stop()
    time.sleep(0.3)

    car.turn_right()
    car.forward()
    time.sleep(1.2)
    car.stop()
    time.sleep(0.3)

    car.turn_left()
    car.forward()
    time.sleep(1.0)
    car.stop()
    time.sleep(0.3)

    car.turn_straight()
    time.sleep(0.1)
    car.stop()

    car.turn_right()
    car.backward()
    time.sleep(0.3)
    car.stop()

    car.turn_left()
    car.forward()
    time.sleep(0.4)
    car.stop()
    time.sleep(3.0)

    car.turn_straight()
    car.backward()
    time.sleep(0.4)
    car.stop()
    time.sleep(1.0)

    car.turn_right()
    car.backward()
    time.sleep(0.2)
    car.stop()
    time.sleep(1.0)

    car.turn_left()
    car.forward()
    time.sleep(1.1)
    car.stop()
    time.sleep(0.3)

    car.turn_right()
    car.forward()
    time.sleep(1.2)
    car.stop()
    time.sleep(0.3)


    # car.turn_forward()
    # car.forward()
    # time.sleep(1.5)
    # car.stop()
    # time.sleep(0.3)

    car.turn_off() # 시동 끔
    processing_ultrasonic.power_num = 0

###################### 구동 부분 끝 (여기 위에만 변경) ######################

if __name__ == "__main__":
    main()