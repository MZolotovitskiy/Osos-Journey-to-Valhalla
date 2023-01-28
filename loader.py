import datetime as dt

# поддерживаются математические и логические операции
# для интервалов времени
delta_time1 = dt.timedelta(days=4, hours=4)
delta_time2 = dt.timedelta(days=1, hours=1)
print(str(delta_time1 - delta_time2))
print(delta_time1 + delta_time2)
print(delta_time1 * 10)
print(delta_time1 / 10)
print(delta_time1 / delta_time2)