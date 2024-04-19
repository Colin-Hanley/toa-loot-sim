from flask import Flask, request, jsonify, render_template
from looting_bag import LootingBag  # Your custom module
from tombs_of_amascut_chest import RewardChest  # Your custom module

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('form.html')

@app.route('/roll_loot', methods=['POST'])
def roll_loot():
    try:
        points = int(request.form.get('points', 23000))
        raid_level = int(request.form.get('raid_level', 350))
        deaths = int(request.form.get('deaths', 0))
        trials = int(request.form.get('trials', 100))
    except ValueError:
        return jsonify({"error": "Invalid input parameters"}), 400

    reward_chest = RewardChest(points=points, raid_level=raid_level, deaths=deaths)
    looting_bag = LootingBag()

    for _ in range(trials):
        looting_bag.store_rewards(reward_chest.roll_loot())

    uniques = {key: looting_bag.items[key] for key in looting_bag.items if key in RewardChest.unique_items}
    normal_loot = {key: looting_bag.items[key] for key in looting_bag.items if key not in RewardChest.unique_items}

    return render_template('results.html', uniques=uniques, normal_loot=normal_loot)

if __name__ == "__main__":
    app.run(debug=True)  # It's often useful to enable debug mode during development.
