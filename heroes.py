import random


class Hero:
    # Базовый класс, который не подлежит изменению
    # У каждого наследника будут атрибуты:
    # - Имя
    # - Здоровье
    # - Сила
    # - Жив ли объект
    # Каждый наследник будет уметь:
    # - Атаковать
    # - Получать урон
    # - Выбирать действие для выполнения
    # - Описывать своё состояние

    max_hp = 150
    start_power = 10

    def __init__(self, name):
        self.name = name
        self.__hp = self.max_hp
        self.__power = self.start_power
        self.__is_alive = True

    def get_hp(self):
        return self.__hp

    def set_hp(self, new_value):
        self.__hp = max(new_value, 0)

    def get_power(self):
        return self.__power

    def set_power(self, new_power):
        self.__power = new_power

    def is_alive(self):
        return self.__is_alive

    # Все наследники должны будут переопределять каждый метод базового класса (кроме геттеров/сеттеров)
    # Переопределенные методы должны вызывать методы базового класса (при помощи super).
    # Методы attack и __str__ базового класса можно не вызывать (т.к. в них нету кода).
    # Они нужны исключительно для наглядности.
    # Метод make_a_move базового класса могут вызывать только герои, не монстры.
    def attack(self, target):
        # Каждый наследник будет наносить урон согласно правилам своего класса
        raise NotImplementedError("Вы забыли переопределить метод Attack!")

    def take_damage(self, damage):
        # Каждый наследник будет получать урон согласно правилам своего класса
        # При этом у всех наследников есть общая логика, которая определяет жив ли объект.
        print("\t", self.name, "Получил удар с силой равной = ", round(damage), ". Осталось здоровья - ", round(self.get_hp()))
        # Дополнительные принты помогут вам внимательнее следить за боем и изменять стратегию, чтобы улучшить выживаемость героев
        if self.get_hp() <= 0:
            self.__is_alive = False

    def make_a_move(self, friends, enemies):
        # С каждым днём герои становятся всё сильнее.
        self.set_power(self.get_power() + 0.1)

    def __str__(self):
        # Каждый наследник должен выводить информацию о своём состоянии, чтобы вы могли отслеживать ход сражения
        raise NotImplementedError("Вы забыли переопределить метод __str__!")


class Healer(Hero):
    # Целитель:
    # Атрибуты:
    # - магическая сила - равна значению НАЧАЛЬНОГО показателя силы умноженному на 3 (self.__power * 3)
    # Методы:
    # - атака - может атаковать врага, но атакует только в половину силы self.__power
    # - получение урона - т.к. защита целителя слаба - он получает на 20% больше урона (1.2 * damage)
    # - исцеление - увеличивает здоровье цели на величину равную своей магической силе
    # - выбор действия - получает на вход всех союзников и всех врагов и на основе своей стратегии выполняет ОДНО из действий (атака,
    # исцеление) на выбранную им цель
    
    def __init__(self, name):
        super().__init__(name)
        self.__magic_power = self.get_power() * 3  # магическая сила

    def get_magic_power(self):
        return self.__magic_power

    def attack(self, target):
        damage = self.get_power() // 2
        target.take_damage(damage)

    def take_damage(self, damage):
        damage *= 1.2  # увеличиваем получаемый урон на 20%
        super().take_damage(damage)

    def heal(self, target):
        target.set_hp(target.get_hp() + self.get_magic_power())

    def make_a_move(self, friends, enemies):
        super().make_a_move(friends, enemies)

        # Целитель будет выбирать случайного союзника для исцеления и случайное действие
        target = random.choice(friends)

        # Выбор действия
        action = random.choice(["attack", "heal"])

        if action == "attack":
            self.attack(target)
        elif action == "heal":
            self.heal(target)

    def __str__(self):
        state = f"Имя: {self.name}, Здоровье: {self.get_hp()}, Сила: {self.get_power()}, Жив: {self.is_alive()}"
        state += f"\nМагическая сила: {self.get_magic_power()}"
        return state

class Tank(Hero):
    # Танк:
    # Атрибуты:
    # - показатель защиты - изначально равен 1, может увеличиваться и уменьшаться
    # - поднят ли щит - танк может поднимать щит, этот атрибут должен показывать поднят ли щит в данный момент
    # Методы:
    # - атака - атакует, но т.к. доспехи очень тяжелые - наносит половину урона (self.__power)
    # - получение урона - весь входящий урон делится на показатель защиты (damage/self.defense) и только потом отнимается от здоровья
    # - поднять щит - если щит не поднят - поднимает щит. Это увеличивает показатель брони в 2 раза, но уменьшает показатель силы в 2 раза.
    # - опустить щит - если щит поднят - опускает щит. Это уменьшает показатель брони в 2 раза, но увеличивает показатель силы в 2 раза.
    # - выбор действия - получает на вход всех союзников и всех врагов и на основе своей стратегии выполняет ОДНО из действий (атака,
    # поднять щит/опустить щит) на выбранную им цель

    def __init__(self, name):
        super().__init__(name)
        self.__defense = 1  # показатель защиты
        self.__shield_raised = False  # поднят ли щит

    def get_defense(self):
        return self.__defense

    def set_defense(self, new_defense):
        self.__defense = new_defense

    def is_shield_raised(self):
        return self.__shield_raised

    def raise_shield(self):
        if not self.__shield_raised:
            self.__shield_raised = True
            self.set_defense(self.get_defense() * 2)
            self.set_power(self.get_power() // 2)

    def lower_shield(self):
        if self.__shield_raised:
            self.__shield_raised = False
            self.set_defense(self.get_defense() // 2)
            self.set_power(self.get_power() * 2)

    def attack(self, target):
        if self.is_shield_raised():
            damage = self.get_power() // 2  # атака с поднятым щитом
        else:
            damage = self.get_power()  # обычная атака

        target.take_damage(damage)

    def take_damage(self, damage):
        if self.is_shield_raised():
            damage //= self.get_defense()  # уменьшаем урон при поднятом щите
        super().take_damage(damage)

    def make_a_move(self, friends, enemies):
        super().make_a_move(friends, enemies)

        # Танк будет выбирать случайного противника для атаки и случайное действие
        target = random.choice(enemies)

        # Выбор действия
        action = random.choice(["attack", "raise_shield", "lower_shield"])

        if action == "attack":
            self.attack(target)
        elif action == "raise_shield":
            self.raise_shield()
        elif action == "lower_shield":
            self.lower_shield()

    def __str__(self):
        state = f"Имя: {self.name}, Здоровье: {self.get_hp()}, Сила: {self.get_power()}, Жив: {self.is_alive()}"
        state += f"\nЗащита: {self.get_defense()}, Поднят ли щит: {self.is_shield_raised()}"
        return state

class Attacker(Hero):
    # Убийца:
    # Атрибуты:
    # - коэффициент усиления урона (входящего и исходящего)
    # Методы:
    # - атака - наносит урон равный показателю силы (self.__power) умноженному на коэффициент усиления урона (self.power_multiply)
    # после нанесения урона - вызывается метод ослабления power_down.
    # - получение урона - получает урон равный входящему урона умноженному на половину коэффициента усиления урона - damage * (
    # self.power_multiply / 2)
    # - усиление (power_up) - увеличивает коэффициента усиления урона в 2 раза
    # - ослабление (power_down) - уменьшает коэффициента усиления урона в 2 раза
    # - выбор действия - получает на вход всех союзников и всех врагов и на основе своей стратегии выполняет ОДНО из действий (атака,
    # усиление, ослабление) на выбранную им цель

    def __init__(self, name):
        super().__init__(name)
        self.__power_multiply = 1  # коэффициент усиления урона

    def get_power_multiply(self):
        return self.__power_multiply

    def set_power_multiply(self, new_multiply):
        self.__power_multiply = new_multiply

    def attack(self, target):
        damage = self.get_power() * self.__power_multiply
        target.take_damage(damage)
        self.power_down()

    def take_damage(self, damage):
        damage *= self.__power_multiply / 2
        super().take_damage(damage)

    def power_up(self):
        self.__power_multiply *= 2

    def power_down(self):
        self.__power_multiply /= 2

    def make_a_move(self, friends, enemies):
        super().make_a_move(friends, enemies)

        # Убийца будет выбирать случайного противника для атаки и случайное действие
        target = random.choice(enemies)

        # Выбор действия
        action = random.choice(["attack", "power_up", "power_down"])

        if action == "attack":
            self.attack(target)
        elif action == "power_up":
            self.power_up()
        elif action == "power_down":
            self.power_down()

    def __str__(self):
        state = f"Имя: {self.name}, Здоровье: {self.get_hp()}, Сила: {self.get_power()}, Жив: {self.is_alive()}"
        state += f"\nКоэффициент усиления урона: {self.get_power_multiply()}"
        return state
