async def change_price(cost: float):
    exchange_rate_of_rubl = 150.0
    cost_in_sum = cost * exchange_rate_of_rubl
    cost_to_pay = cost_in_sum + (cost_in_sum * 3)
    return '{:,.2f} сум'.format(cost_to_pay)


async def percent_from_bonus(bonus):
    return (bonus / 1000) * 100

