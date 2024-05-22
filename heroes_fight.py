import random
import time

# Класс Hero представляет героя с именем, здоровьем и силой удара
class Hero:
    def __init__(self, name, health=100, attack_power=20):
        self.name = name
        self.health = health
        self.attack_power = attack_power

    # Метод attack наносит урон другому герою
    def attack(self, other):
        other.health -= self.attack_power
        print(f"{self.name} атакует {other.name} и наносит {self.attack_power} урона.")

    # Метод is_alive проверяет, жив ли герой
    def is_alive(self):
        return self.health > 0

# Класс Game представляет саму игру
class Game:
    def __init__(self, player_name):
        self.player = Hero(player_name)
        self.computer = Hero("Компьютер", health=100, attack_power=random.randint(15, 25))

    # Метод start запускает игру
    def start(self):
        print("Игра начинается!")
        round_num = 1

        while self.player.is_alive() and self.computer.is_alive():
            print(f"\nРаунд {round_num}")
            if round_num % 2 == 1:
                self.player_turn()
            else:
                self.computer_turn()
            round_num += 1

            if self.player.is_alive() and self.computer.is_alive():
                self.countdown()

        if self.player.is_alive():
            print("\nПоздравляем, вы победили!")
        else:
            print("\nВы проиграли. Компьютер победил.")

    # Метод player_turn описывает ход игрока
    def player_turn(self):
        self.player.attack(self.computer)
        print(f"У {self.computer.name} осталось {self.computer.health} здоровья.")

    # Метод computer_turn описывает ход компьютера
    def computer_turn(self):
        self.computer.attack(self.player)
        print(f"У {self.player.name} осталось {self.player.health} здоровья.")

    # Метод countdown выполняет обратный отсчет перед следующим раундом
    def countdown(self):
        for i in range(5, 0, -1):
            print(f"\rДо следующего раунда {i} секунд", end='', flush=True)
            time.sleep(1)
        print("\r" + " " * 30 + "\r", end='')  # Очищает строку после завершения отсчета

# Основная часть программы
if __name__ == "__main__":
    player_name = input("Введите имя вашего героя: ")
    game = Game(player_name)
    game.start()
