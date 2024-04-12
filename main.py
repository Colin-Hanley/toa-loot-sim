import random
import statistics
from math import floor


class RewardChest:
    unique_items = {
        "Osmumtens's fang": {"probability": 1 / 3.429, "reduced_rate_sub_150": False},
        "Lightbearer": {"probability": 1 / 3.429, "reduced_rate_sub_150": False},
        "Elidinis' ward": {"probability": 1 / 8, "reduced_rate_sub_150": True},
        "Masori mask": {"probability": 1 / 12, "reduced_rate_sub_150": True},
        "Masori body": {"probability": 1 / 12, "reduced_rate_sub_150": True},
        "Masori chaps": {"probability": 1 / 12, "reduced_rate_sub_150": True},
        "Tumeken's shadow": {"probability": 1 / 24, "reduced_rate_sub_150": True},
    }

    common_items = {
        "Coins": {"Divisor Value": 1},
        "Death runes": {"Divisor Value": 20},
        "Soul runes": {"Divisor Value": 40},
        "Gold ore": {"Divisor Value": 90},
        "Dragon dart tip": {"Divisor Value": 100},
        "Mahogany logs": {"Divisor Value": 180},
        "Sapphire": {"Divisor Value": 200},
        "Emerald": {"Divisor Value": 250},
        "Gold bar": {"Divisor Value": 250},
        "Potato cactus": {"Divisor Value": 250},
        "Raw Shark": {"Divisor Value": 250},
        "Ruby": {"Divisor Value": 300},
        "Diamond": {"Divisor Value": 400},
        "Raw manta ray": {"Divisor Value": 450},
        "Cactus spine": {"Divisor Value": 600},
        "Dragonstone": {"Divisor Value": 600},
        "Battlestaff": {"Divisor Value": 1100},
        "Coconut Milk": {"Divisor Value": 1100},
        "Lily of the sands": {"Divisor Value": 1100},
        "Toadflax seed": {"Divisor Value": 1400},
        "Ranaar seed": {"Divisor Value": 1800},
        "Torstol seed": {"Divisor Value": 2200},
        "Snapdragon Seeds": {"Divisor Value": 2200},
        "Dragon med helm": {"Divisor Value": 4000},
        "Magic seed": {"Divisor Value": 6500},
        "Blood essence": {"Divisor Value": 7500},
    }

    def __init__(self, points: int, raid_level: int, deaths: int):
        self._points = points
        self.raid_level = raid_level  # Using the property setter
        self.deaths = deaths
        self.true_reward_points = self.calculate_true_reward_points(deaths, points)
        self.unique_items_names = list(self.unique_items.keys())
        self.unique_item_probabilities = [self.unique_items[item]["probability"] for item in self.unique_items_names]
        self.common_item_names = list(self.common_items.keys())
        self.common_item_weights = [1 for _ in self.common_item_names]

    @staticmethod
    def calculate_true_reward_points(deaths, points):
        if deaths:
            return (
                64000
                if points + (5000 * (0.8 ** deaths)) > 64000
                else points + (5000 * (0.8 ** deaths))
            )
        else:
            return points + 5000

    def get_unique_chance(self):
        """
        Calculate the chance of getting a unique item from the reward chest
        Returns:
            float: The chance of getting a unique item. E.g. 5.10 for 5.10%
        """

        # If the raid level is 400 or higher, unique chance is calculated differently
        if self._upper_raid_value:
            unique_chance = self.points / (
                    10500 - 20 * (self._lower_raid_value + (self._upper_raid_value / 3))
            )
            return round(unique_chance, 2)

        unique_chance = self.points / (10500 - (20 * self._lower_raid_value))
        return round(unique_chance, 2)

    def is_loot_unique(self):
        """
        Determine if the loot from the reward chest is unique
        Returns:
            bool: True if the loot is unique, False otherwise
        """
        unique_chance = self.get_unique_chance()
        if random.random() <= unique_chance / 100:
            return True
        return False

    def roll_loot_reward(self):
        # add a flag to rerrn a common or unique drop so it can be filtered out later
        if self.is_loot_unique():
            return (self.roll_unique_reward(), 'Unique')

        common_items_selected = random.choices(
            self.common_item_names,
            weights=self.common_item_weights,
            k=3
        )
        common_item_volumes = {item: self.get_common_reward_volume(item) for item in common_items_selected}

        return (common_item_volumes, 'Common')

    def get_common_reward_volume(self, common_item):
        if self._lower_raid_value <= 300:
            return floor(
                self.true_reward_points
                / self.common_items[common_item].get("Divisor Value")
            )

        if self._lower_raid_value > 300:
            return floor(
                (
                        self.true_reward_points
                        / self.common_items[common_item].get("Divisor Value")
                )
                * (1.15 + (0.01 * ((self._lower_raid_value - 300) / 5)))
            )

    def roll_unique_reward(self):
        unique_item = random.choices(
            self.unique_items_names,
            weights=self.unique_item_probabilities,
            k=1
        )[0]

        if self.raid_level <= 49:
            if random.random() <= 1 / 50:
                return {unique_item: 1}  # Ensure the return format is consistent
            return {"Common items": 0}

        if 50 <= self.raid_level <= 149:
            if self.unique_items[unique_item]["reduced_rate_sub_150"]:
                if random.random() <= 1 / 50:
                    return {unique_item: 1}
            return {"Common items": 0}

        return {unique_item: 1}

    @property
    def points(self):
        return self._points

    @points.setter
    def points(self, value: int):
        if not isinstance(value, int) or value < 0 or value >= 64000:
            raise ValueError(
                "Points must be a non-negative integer and less than 59000,"
                " as point cap is 6400 with 5k invisible starting bonus"
            )

        self._points = value
        if value > 64000:
            self._points = 64000

    @property
    def raid_level(self):
        return self._lower_raid_value

    @raid_level.setter
    def raid_level(self, value: int):
        if not isinstance(value, int) or value < 0 or value >= 600:
            raise ValueError(
                "Raid level must be a non-negative integer and less than 10"
            )

        self._lower_raid_value = value
        self._upper_raid_value = 0
        if value >= 400:
            self._upper_raid_value = value - 400
            self._lower_raid_value = value - self._upper_raid_value


if __name__ == "__main__":

    trial_counts = []
    reward_chest = RewardChest(points=23000, raid_level=350, deaths=0)

    for _ in range(10000):
        trial_count = 0
        while True:
            trial_count += 1
            loot, loot_type = reward_chest.roll_loot_reward()
            if loot_type == 'Unique' and 'Osmumtens\'s fang' in loot:
                trial_counts.append(trial_count)
                break

    # Calculating statistics
    mean_count = statistics.mean(trial_counts)
    median_count = statistics.median(trial_counts)
    max_count = max(trial_counts)
    min_count = min(trial_counts)
    std_dev_count = statistics.stdev(trial_counts)

    # Display results
    print(f"Mean: {mean_count}")
    print(f"Median: {median_count}")
    print(f"Max: {max_count}")
    print(f"Min: {min_count}")
    print(f"Standard Deviation: {std_dev_count}")
    print(f"Raid Level: {reward_chest.raid_level}")
    print(f"Points: {reward_chest.points}")
