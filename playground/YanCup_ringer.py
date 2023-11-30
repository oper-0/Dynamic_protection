class MyClass:
    @staticmethod
    def my_decorator(func):
        def wrapper(*args, **kwargs):
            print("Something is happening before the function is called.")
            result = func(*args, **kwargs)
            print("Something is happening after the function is called.")
            return result
        return wrapper

    @my_decorator  # Применяем декоратор к методу
    def say_hello(self, name):
        print(f"Hello, {name}!")

# Создаем экземпляр класса
my_instance = MyClass()

# Вызываем декорированный метод
my_instance.say_hello("John")




# def ring_counter(time, X, alarms):
#     counter = 0
#     for i in alarms:
#         single_alarm_count = (time - i) // X + 1
#         if single_alarm_count < 0:
#             continue
#         counter += (time - i) // X + 1
#     return int(counter)
#
#
# def start():
#     N, X, K = map(int, input().split())
#     alarms = list(map(int, input().split()))
#
#     # N, X, K = 6, 5, 10
#     # alarms = [1, 2, 3, 4, 5, 6]
#
#     # N, X, K = 5, 7, 12
#     # alarms = [5, 22, 17, 13, 8]
#     #
#     # _, X, K = 0, 5, 9  # X K
#     # alarms = [5, 13]
#
#     map_by_mod = {}
#     for alarm in alarms:
#         if not map_by_mod.get(alarm % X):
#             map_by_mod[alarm % X] = []
#         map_by_mod[alarm % X].append(alarm)
#     # print(f"groped by mod: {map_by_mod}")
#
#     shrankAlarms = []
#     for alarms in map_by_mod.values():
#         shrankAlarms.append(min(alarms))
#     # print(f"Shrank alarms: {shrankAlarms}")
#
#     near_awake_time = 0
#     min_t, max_t = 0, max(shrankAlarms) + X * K
#     while min_t <= max_t:
#         t = (min_t + max_t) // 2
#         rings = ring_counter(t, X, shrankAlarms)
#         if rings == K:
#             near_awake_time = t
#             break
#         elif rings < K:
#             min_t = t + 1
#         else:
#             max_t = t - 1
#
#     alarm_rings = ((ALARM + X * x for x in range(K)) for ALARM in shrankAlarms)
#
#     closest_times = []
#     for ring_times in alarm_rings:
#         ranges_beneath = [x for x in ring_times if x <= near_awake_time]
#         if not ranges_beneath:
#             continue
#         tmp = [near_awake_time - x for x in ranges_beneath]
#         closest_times.append(ranges_beneath[tmp.index(min(tmp))])
#
#     print(max(closest_times))
#
#
# start()
