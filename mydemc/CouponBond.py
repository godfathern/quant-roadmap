class CouponBond:
    
    def __init__(self, principal, maturity, interest_rate, yield_rate):
        
        self.principal = principal
        self.maturity = maturity
        self.interest_rate = interest_rate / 100 # Market interest rate
        self.yield_rate = yield_rate / 100 # Bond interest rate aka amount of coupon payment in %
    
    
    def present_value(self, p, m, ir, yr):
        total = 0
        for i in (1, m +1):
            total += yr*p/(1+ir)**(i)
        
        return total + p/(1+ir)**m
    
    def calculate_price(self):
        return self.present_value(self.principal, self.maturity, self.interest_rate, self.yield_rate)


if __name__== '__main__':
    bond = CouponBond(1000, 3, 4, 10)
    print(bond.calculate_price())