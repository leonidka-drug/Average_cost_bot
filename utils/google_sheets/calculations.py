from .connect_to_sheets import get_values


async def calculate_cost(data):
    # Получение значений
    sold_days = await get_values(data['spreadsheet_id'], data['range_B'])
    sold_days = [int(val[0]) for val in sold_days['values'] if val]
    days_gone = await get_values(data['spreadsheet_id'], data['range_A'])
    days_gone = [val[0] for val in days_gone['values'] if val]
    days_gone = len(days_gone)
    number_of_rooms = data['ROOMS_NUMBER']

    # Все подсчёты
    remaining_days = data['days_number'] - days_gone
    # Средний чек прошлых дней
    sold_average = (sum(sold_days) + data['fora']) / number_of_rooms / days_gone
    # Недостача
    shortage = (data['needed_average_cost'] - sold_average) * days_gone
    # Средний чек след-их дней
    next_days_cost = data['needed_average_cost'] + shortage / remaining_days

    return {
        "days_gone": days_gone,
        "remaining_days": remaining_days,
        "sold_average": sold_average,
        "shortage": shortage,
        "next_days_cost": next_days_cost,
        "number_of_rooms": number_of_rooms,
    }
