import json
import os
from datetime import datetime


class StateManager:
    def __init__(self, state_dir="state"):
        self.state_dir = state_dir
        os.makedirs(self.state_dir, exist_ok=True)

        self.prev_path = os.path.join(self.state_dir, "prev.json")
        self.curr_path = os.path.join(self.state_dir, "curr.json")

    def load_prev(self):
        if not os.path.exists(self.prev_path):
            return []
        with open(self.prev_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def save_curr(self, data):
        with open(self.curr_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def promote_curr_to_prev(self):
        """
        After successful run:
        curr -> prev
        """
        if os.path.exists(self.curr_path):
            with open(self.curr_path, "r", encoding="utf-8") as f:
                data = json.load(f)

            with open(self.prev_path, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

    def has_prev(self):
        return os.path.exists(self.prev_path)