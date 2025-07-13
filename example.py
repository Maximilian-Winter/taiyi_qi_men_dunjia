import datetime

from divination.taiyi import TaiyiCalculator
from divination.qi_men_dunjia import QiMenCalculator

taiyi = TaiyiCalculator()

divination = taiyi.perform_divination(datetime.datetime.now())

print(taiyi.display_divination_result(divination))


calculator = QiMenCalculator()

chart = calculator.calculate_qi_men_chart(datetime.datetime.now())

print(calculator.display_qi_men_chart(chart))