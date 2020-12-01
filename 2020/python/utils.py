import typing as t


def int_numbers(input_data: str) -> t.List[int]:
    return [int(num) for num in input_data.splitlines() if num.strip()]
