import math
class ContinuousModel:
    
    def __init__(self, principal, maturity, interest_rate):
        self.principal = principal
        self.maturity = maturity
        self.interest_rate = interest_rate
    
    def present_value(self):
        return self.principal/math.exp**(self.interest_rate*self.maturity)
    
    