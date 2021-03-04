from core import Hijriah


class Date(Hijriah):
    """Function for converted hijirah date
    into formatted string.

    TODO: fix this inheritance and property method
    and split the month value into new array
    in constants modules
    """

    def to_string(self, months):
        self.months = [
            "Muharram",
            "Safar",
            "Rabiul Awwal",
            "Rabiul Tsani",
            "Jumadil Ula",
            "Jumadil Tsani",
            "Rajab",
            "Sya'ban",
            "Ramadhan",
            "Syawwal",
            "Dzul Qa'dah",
            "Dzul Hijjah",
        ]
        m = self.months[self.month - 1] - 1
        return f"{self.day} - {m} - {self.year}"
