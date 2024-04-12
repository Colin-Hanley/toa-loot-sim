import random
import statistics
from math import floor
from typing import Dict, Tuple, List


class RewardChest:
    """A class representing a reward chest which may contain unique or common items based on a gaming reward system."""

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
        """Initialize the RewardChest with given parameters.

        Args:
            points (int): The number of points scored by the player.
            raid_level (int): The level of the raid completed by the player.
            deaths (int): The number of times the player died.

        Raises:
            ValueError: If the initial parameters are outside of expected ranges.
        """

        self._validate_initial_values(points, raid_level)
        self.points = points  # Using the property setter
        self.raid_level = raid_level
        self.deaths = deaths
        self.true_reward_points = self.calculate_true_reward_points(deaths, points)
        self.unique_items_names = list(self.unique_items.keys())
        self.unique_item_probabilities = [
            self.unique_items[item]["probability"] for item in self.unique_items_names
        ]
        self.common_item_names = list(self.common_items.keys())
        self.common_item_weights = [1 for _ in self.common_item_names]

    def roll_loot(self) -> Tuple[Dict[str, int], str]:
        """Simulate rolling for loot and determine if the loot is unique or common.

        Returns:
            Tuple[Dict[str, int], str]: A tuple containing the rolled items and the type of loot ('Unique' or 'Common').
        """
        if self._is_loot_unique():
            return self._roll_unique_reward(), "Unique"
        else:
            common_items_selected = random.choices(
                self.common_item_names, weights=self.common_item_weights, k=3
            )
            common_item_volumes = {
                item: self._get_common_reward_volume(item)
                for item in common_items_selected
            }
            return common_item_volumes, "Common"

    def _is_loot_unique(self) -> bool:
        """Determine if the loot from the reward chest is unique based on calculated chances.

        Returns:
            bool: True if the loot is unique, otherwise False.
        """
        unique_chance = self._get_unique_chance()
        return random.random() <= unique_chance / 100

    def _get_unique_chance(self) -> float:
        """Calculate the chance of getting a unique item.

        Returns:
            float: The chance of getting a unique item as a percentage (e.g., 5.10 for 5.10%).
        """
        if self.raid_level >= 400:
            unique_chance = self.points / (
                10500 - 20 * (self.raid_level + (self.raid_level - 400) / 3)
            )
        else:
            unique_chance = self.points / (10500 - 20 * self.raid_level)
        return round(unique_chance, 2)

    def _roll_unique_reward(self):
        unique_item = random.choices(
            self.unique_items_names, weights=self.unique_item_probabilities, k=1
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

    def _get_common_reward_volume(self, common_item: str) -> int:
        """Calculate the volume of common reward based on the raid level and divisor values.

        Args:
            common_item (str): The common item for which volume is calculated.

        Returns:
            int: The calculated volume of the common item.
        """
        if self.raid_level <= 300:
            return floor(
                self.true_reward_points
                / self.common_items[common_item]["Divisor Value"]
            )
        else:
            adjustment_factor = 1.15 + 0.01 * ((self.raid_level - 300) / 5)
            return floor(
                (
                    self.true_reward_points
                    / self.common_items[common_item]["Divisor Value"]
                )
                * adjustment_factor
            )

    @staticmethod
    def calculate_true_reward_points(deaths: int, points: int) -> int:
        """Calculate the true reward points adjusting for deaths.

        Args:
            deaths (int): The number of deaths.
            points (int): The starting points.

        Returns:
            int: The adjusted reward points.
        """
        additional_points = 5000 * (0.8**deaths) if deaths else 5000
        return min(points + additional_points, 64000)

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

    def _validate_initial_values(self, points: int, raid_level: int):
        """Validate the initial points and raid level values.

        Args:
            points (int): Points to be validated.
            raid_level (int): Raid level to be validated.

        Raises:
            ValueError: If the points or raid level are out of expected range.
        """
        if not (0 <= points < 64000):
            raise ValueError(
                "Points must be a non-negative integer and less than 64000."
            )
        if not (0 <= raid_level < 600):
            raise ValueError(
                "Raid level must be a non-negative integer and less than 600."
            )


if __name__ == "__main__":

    trial_counts = []
    reward_chest = RewardChest(points=23000, raid_level=350, deaths=0)

    for _ in range(10000):
        trial_count = 0
        while True:
            trial_count += 1
            loot, loot_type = reward_chest.roll_loot()
            if loot_type == "Unique" and "Osmumtens's fang" in loot:
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
