def choose_house(GH_number):
    # Выбор аргументов нужного отеля
    # GH_number = int(input("\nНапиши 1, если нужна информация по Теплу, Напиши 2 - по Софии: "))
    if GH_number == 1:
        data = GH_data['teplo']
    else:
        data = GH_data['sofia']
    return data


def calculate_cost(data):
    # Получение значений
    sold_days = get_values(data['spreadsheet_id'], data['range_B'])
    sold_days = [int(val[0]) for val in sold_days['values'] if val]
    days_gone = get_values(data['spreadsheet_id'], data['range_A'])
    days_gone = [val[0] for val in days_gone['values'] if val]
    days_gone = len(days_gone)

    # Все подсчёты
    remaining_days = data['days_number'] - days_gone
    sold_avarege = (sum(sold_days) + data['fora']) / data['ROOMS_NUMBER'] / days_gone  # Средний чек прошлых дней
    shortage = (data['needed_avarege_cost'] - sold_avarege) * days_gone                # Недостача
    next_days_cost = data['needed_avarege_cost'] + shortage / remaining_days           # Средний чек след-их дней

    return {
        "remaining_days": remaining_days,
        "sold_avarege": sold_avarege,
        "shortage": shortage,
        "next_days_cost": next_days_cost,
    }