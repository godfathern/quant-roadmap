import backtrader

cerebro = backtrader.Cerebro()

cerebro.broker.set_cash(1000000)
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

cerebro.run()

print('Final Portfolio value: %.2f' % cerebro.broker.getvalue())