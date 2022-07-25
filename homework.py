from typing import Dict, Type, List

class InfoMessage:
    """Информационное сообщение о тренировке"""
  
    # Свойства класса
    # training_type — тип тренировки;
    # duration — длительность тренировки;
    # distance — дистанция, преодолённая за тренировку;
    # speed — средняя скорость движения;
    # calories — потраченные за время тренировки килокалории.    
    def __init__(self, 
        training_type: str, 
        duration: float, 
        distance: float, 
        speed: float, 
        calories: float
        ) -> None:

        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    # Методы класса
    def get_message(self) -> str: 
        # метод возвращает строку сообщения.
        # все значения типа float округляются до 3 знаков после запятой.
        return (f"Тип тренировки: {self.training_type}; "
            f"Длительность: {self.duration:.3f} ч.; "
            f"Дистанция: {self.distance:.3f} км; "
            f"Ср. скорость: {self.speed:.3f} км/ч; "
            f"Потрачено ккал: {self.calories:.3f}.")

class Training:
    """Базовый класс тренировки"""
    # константа для перевода значений из метров в километры
    M_IN_KM = 1000
    
    #расстояние, которое спортсмен преодолевает за один шаг или гребок. 
    # Один шаг — это  `0.65` метра, один гребок — `1.38` метра.
    LEN_STEP = 0.65
    
    def __init__(self,
        action: int,
        duration: float,
        weight: float
        ) -> None:

        self.action = action
        self.duration = duration
        self.weight = weight
    
    # Методы класса
    def get_distance(self) -> float:
        """Получить дистанцию в км"""
        # метод возвращает значение дистанции, преодолённой за тренировку.
        # базовая формула расчёта: шаг * LEN_STEP / M_IN_KM
        return (self.action * self.LEN_STEP / self.M_IN_KM)

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения"""
        # метод возвращает значение средней скорости движения.
        # базовая формула расчёта: дистанция / длительность        
        distance = self.get_distance()
        return (distance / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий""" 
        # метод возвращает число потраченных калорий BMR.
        return (1 * self.weight * self.duration)

    def show_training_info(self) -> InfoMessage: 
        """Вернуть информационное сообщение о выполненной тренировке"""
        distance = self.get_distance()
        calories = self.get_spent_calories()
        speed = self.get_mean_speed()
        # training_type — тип тренировки;
        training_type = self.__class__.__name__
        return InfoMessage(training_type, 
            self.duration, 
            distance, 
            speed, 
            calories)

class Running(Training):
    """Беговая тренировка"""
    # Свойства класса наследуются
    # переопределить метод:
    def get_spent_calories(self) -> float: 
        """Получить количество затраченных калорий"""
        speed = self.get_mean_speed()
        # формула расчёта: 
        # (18 * средняя_скорость – 20) * 
        # * вес_спортсмена / M_IN_KM * время_тренировки_в_минутах        
        return ((18 * speed - 20) * self.weight 
                / self.M_IN_KM * (self.duration * 60))

class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    # Свойства класса наследуются
    # добавляется:
    # height — рост
    def __init__(self,
        action: str,
        duration: float,
        weight: float,   
        height: float
        ) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий"""
        # формула расчёта: (0.035 * вес + (скорость ** 2 // рост) 
        # * 0.029 * вес) * время_тренировки_в_минутах
        speed = self.get_mean_speed()
        return ((0.035 * self.weight + (speed ** 2 // self.height) 
                * 0.029 * self.weight) * (self.duration * 60))

class Swimming(Training):
    """Тренировка в бассейне"""
    LEN_STEP = 1.38
    # Свойства класса наследуются
    # Добавляемые свойства:
    # length_pool — длина бассейна;
    # count_pool — количество проплытых бассейнов.
    def __init__(self,
            action: str,
            duration: float,
            weight: float,   
            length_pool: float,
            count_pool: int
            ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения"""
        # формула расчёта: длина_бассейна * count_pool 
        # / M_IN_KM /время_тренировки
        return (self.length_pool * self.count_pool 
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий"""
        # формула расчёта: (скорость + 1.1) * 2 * вес
        speed = self.get_mean_speed()
        return ((speed + 1.1) * 2 * self.weight)

# Функции модуля
def read_package(workout_type: str, data: List[int])-> Training:
    """Прочитать данные полученные от датчиков.""" 
    training_dict: Dict[str, Type[Training]] = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking
    }
    if workout_type not in training_dict:
        raise ValueError('Выбран неверный тип тренировки!')
    return training_dict[workout_type](*data)

def main(training: Training) -> None:
    info = training.show_training_info()
    print(info.get_message())

if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)