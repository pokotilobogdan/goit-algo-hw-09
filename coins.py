import matplotlib.pyplot as plt
from timeit import timeit
import copy

def find_coins_greedy(value, coins):
    result = {}
    
    # just in a case we have a coins list being not sorted
    sorted_coins = sorted(coins, reverse=True)

    for coin in sorted_coins:
        while coin <= value:
            if coin not in result.keys():
                result[coin] = 0
            # value -= coin
            # result[coin] += 1
            result[coin] += value // coin
            value = value - result[coin]*coin       # рахуємо залишок
    return f"Coins used in greedy: {result if value == 0 else 'Даним набором монет не можна видати таку решту'}"


def find_min_coins(value, coins: list[int], n):
    
    # Створюємо таблицю K для зберігання оптимальних значень підзадач
    
    # Елементом таблиці є список. Першим елементом списку є оптимальна кількість монет на задану кількість грошей.
    # Другим елементом списку є перелік монет з їх кількістю, які ми для цього використовуємо.
    K = [[[float('inf'), {}] for _ in range(value + 1)] for _ in range(n + 1)]
    
    # Для ціни 0 у нас завжди буде 0 монет для використання
    for i in range(n+1):
        K[i][0] = [0, {}]

    for i, coin in enumerate(coins):

        # Дивимось внесок монети в рішення задачі. На даному етапі в табличку вноситься рішення, отримане з цією монетою, і всіма до неї по списку
        for price_goal in range(1, value + 1):
            
            # Якщо монета не більша за решту, яку ми хочемо видати, то перевіряємо як краще: з цією монетою, або без неї -- min(з монетою, без монети)
            if coin <= price_goal:
                
                # Якщо монета оптимізує рішення:
                if 1+K[i+1][price_goal-coin][0] < K[i][price_goal][0]:
                    
                    K[i+1][price_goal][0] = 1+K[i+1][price_goal-coin][0]
                    K[i+1][price_goal][1] = copy.copy(K[i+1][price_goal - coin][1])

                    # Додаємо використану монету до списку (словника) використаних
                    if coin in K[i+1][price_goal][1].keys():
                        K[i+1][price_goal][1][coin] += 1
                    else:
                        K[i+1][price_goal][1][coin] = 1
                # Якщо монета не робить краще, то залишаємо те, що було й без неї:
                else:
                    K[i+1][price_goal][0] = K[i][price_goal][0]
                    K[i+1][price_goal][1] = copy.copy(K[i][price_goal][1])

            # Якщо монета більша за решту, яку ми хочемо видати - результат такий же, як і до цього
            else:
                K[i+1][price_goal][0] = K[i][price_goal][0]
                K[i+1][price_goal][1] = copy.copy(K[i][price_goal][1])

    return f"Coins used: {K[n][value][1] if K[n][value][0] != float('inf') else 'Даним набором монет не можна видати таку решту'}"


if __name__ == "__main__":

    coins = [10, 50, 5, 1, 25, 2]
    # coins.sort()
    
    results_greedy = []
    results_dynamic = []
    
    max_amount = 1000

    print("Please, wait, it's still calculating results...")
    print("It takes several seconds, be patient :)")

    for amount in range(1, max_amount):
        greedy_time = timeit(lambda: find_coins_greedy(amount, coins), number=10)
        results_greedy.append(greedy_time)
        # print("Greedy:", round(greedy_time, 6), end='\t')
        
        dynamic_time = timeit(lambda: find_min_coins(amount, coins, n=len(coins)), number=10)
        results_dynamic.append(dynamic_time)
        # print("Dynamic:", round(dynamic_time, 6))

    print("Now we're gonna cook")
    
    fig, ax = plt.subplots(figsize=(16, 8), layout='constrained')
    ax.plot(range(1, max_amount), results_greedy, label='greedy')  # Plot some data on the axes.
    ax.plot(range(1, max_amount), results_dynamic, label='dynamic')  # Plot more data on the axes...
    ax.set_xlabel('Value to get')  # Add an x-label to the axes.
    ax.set_ylabel('Time for calculations')  # Add a y-label to the axes.
    ax.set_title("Greedy time vs Dynamic time")  # Add a title to the axes.
    ax.legend();  # Add a legend.
    
    plt.show()