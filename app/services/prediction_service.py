from app.models.bin import Bin


def predict_full_time(bin):

    avg_hourly_fill = 5

    remaining = (
        100 - bin.fill_level
    )

    hours = (
        remaining /
        avg_hourly_fill
    )

    return round(hours, 1)