def get_clock_hours(time: int) -> int:
    return time // 60 // 60


def get_clock_minutes(time: int) -> int:
    return time // 60 % 60


def get_clock_seconds(time: int) -> int:
    return time % 60


def get_clock_time(time: int) -> str:
    return f"{get_clock_hours(time):02d};{get_clock_minutes(time):02d}"


def make_plural(n: int) -> str:
    return "" if n == 1 else "s"
