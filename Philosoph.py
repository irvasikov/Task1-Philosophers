import threading
import time

forks = []
# создаем массив из 5 объектов вилок типа Lock
for i in range(5):
    fork = threading.Lock()
    forks.append(fork)


def is_both_of_forks_free(name: str) -> bool:
    """Проверяем свободны ли обе вилки по краям от текущего философа"""
    num_of_philosopher = int(name[-1])
    # если философ номер 5 то проверяем 4 и 0 вилку
    if num_of_philosopher == 5:
        if not forks[4].locked() and not forks[0].locked():
            return True
        return False
    if not forks[num_of_philosopher].locked() and not forks[num_of_philosopher - 1].locked():
        return True
    return False


def acquire_both_forks(name: str) -> None:
    """Занимаем обе вилки по краям от текущего философа"""
    num_of_philosopher = int(name[-1])
    if num_of_philosopher == 5:
        forks[4].acquire(timeout=5)
        forks[0].acquire(timeout=5)
    else:
        forks[num_of_philosopher].acquire(timeout=5)
        forks[num_of_philosopher - 1].acquire(timeout=5)


def release_both_forks(name: str) -> None:
    """Освобождаем обе вилки по краям от философа"""
    num_of_philosopher = int(name[-1])
    if num_of_philosopher == 5:
        forks[4].release()
        forks[0].release()
    else:
        forks[num_of_philosopher].release()
        forks[num_of_philosopher - 1].release()


def philosopher_emulation(name: str) -> None:
    """эмулирует философа способного только думать и поглощать пищу"""
    print(f"{name}: я появился")
    while True:
        print(f"{name}: я хочу есть!")
        if is_both_of_forks_free(name):
            acquire_both_forks(name)
            print(f"{name}: Вилки свободны, начну кушать!")
            time.sleep(3)
            print(f"{name}: Ох, теперь я сыт!")
            release_both_forks(name)
            print(f"{name}: Теперь можно и подумать!")
            time.sleep(5)
        else:
            print(f"{name}: Вилки заняты. Пойду думать думу великую!")
            time.sleep(4)


# создаем 5 философоф объектов типа Thread
for i in range(5):
    name_of_philosopher = f"Philosopher{i + 1}"
    philosopher = threading.Thread(target=philosopher_emulation, args=(name_of_philosopher, ))
    philosopher.start()
