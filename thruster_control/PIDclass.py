import time


class PID:

    def __init__(self, P=0.2, I=0.3, D=0.1):

        self.SetPoint = 8
        self.Kp = P
        self.Ki = I
        self.Kd = D

        self.sample_time = 10
        self.current_time = int(time.time() * 1000)
        self.last_time = self.current_time

        self.clear()

    def setpoint(self, sp):
        self.SetPoint = sp

    def clear(self):

        self.PTerm = 0.0
        self.ITerm = 0.0
        self.DTerm = 0.0
        self.last_error = 0.0

        # Windup Guard
        self.windup_guard = self.SetPoint + 1

        self.output = 0.0

    def setoutstart(self, op):
        self.output = op

    def update(self, feedback_value):

        error = self.SetPoint - feedback_value
        self.current_time = int(time.time() * 1000)
        delta_time = self.current_time - self.last_time
        delta_error = error - self.last_error
        # print(delta_time)
        # print(self.last_time)
        # print(self.current_time)
        # print(error)
        if delta_time >= self.sample_time:
            self.PTerm = self.Kp * error
            self.ITerm += self.last_error * delta_time
            if delta_time > 0:
                self.DTerm = delta_error / delta_time
            else:
                self.DTerm = 0.0
            # Overshoot saturation for Iterm
            if self.ITerm < -self.windup_guard:
                self.ITerm = -self.windup_guard
            elif self.ITerm > self.windup_guard:
                self.ITerm = self.windup_guard

            self.last_time = self.current_time
            self.last_error = error

            self.output = self.output + self.PTerm + (self.Ki * self.ITerm) + (self.Kd * self.DTerm)
            # print(self.output)
        return self.output

    def setKp(self, proportional_gain):
        self.Kp = proportional_gain

    def setKi(self, integral_gain):
        self.Ki = integral_gain

    def setKd(self, derivative_gain):
        self.Kd = derivative_gain

    def setWindup(self, windup):
        self.windup_guard = windup

    def setSampleTime(self, sample_time):
        self.sample_time = sample_time
