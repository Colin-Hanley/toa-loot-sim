class LootingBag:
    """
    This is a class to store the items that are dropped from the raid.
    The stored items will be used to visualise the volume in the flask app.
    """
    def __init__(self):
        self.items = {}

    def store_rewards(self, rewards:dict):
        for item, volume in rewards.items():
            if item in self.items:
                self.items[item] += volume
            else:
                self.items[item] = volume

    def remove_item(self, item):
        self.items.remove(item)

    def __str__(self):
        return f"LootingBag({self.items})"