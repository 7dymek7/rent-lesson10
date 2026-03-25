import random


def slow_processing(data_size=10000):
    items = list(range(data_size))
    to_find = [random.randint(0, data_size * 2) for _ in range(5000)]

    found_count = 0
    for item in to_find:
        if item in items:
            found_count += 1
    return found_count


def fast_processing(data_size=10000):
    items = set(range(data_size))
    to_find = [random.randint(0, data_size * 2) for _ in range(5000)]

    found_count = 0
    for item in to_find:
        if item in items:
            found_count += 1
    return found_count


def heavy_math():
    result = 0
    for i in range(1_000_000):
        result += i**0.5
    return result


def main():
    print("Rozpoczynam obliczenia...")

    print("Uruchamiam slow_processing...")
    slow_processing()

    print("Uruchamiam fast_processing...")
    fast_processing()

    print("Uruchamiam heavy_math...")
    heavy_math()

    print("Gotowe!")


if __name__ == "__main__":
    main()
