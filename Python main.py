import json
import os
import datetime
import hashlib

CONFIG = {
    "name": "ZEYN",
    "title": "Strategic AI Unit",
    "memory_file": "memory.json"
}

# ================= MEMORY =================

class Memory:

    def __init__(self):
        self.file = CONFIG["memory_file"]
        self.data = self.load()

    def load(self):
        if os.path.exists(self.file):
            with open(self.file, "r") as f:
                return json.load(f)

        return {
            "users": {},
            "history": [],
            "learned": []
        }

    def save(self):
        with open(self.file, "w") as f:
            json.dump(self.data, f, indent=2)

    def add_user(self, uid, name):
        self.data["users"][uid] = {
            "name": name,
            "created": datetime.datetime.now().isoformat(),
            "sessions": 0
        }
        self.save()

    def increase_session(self, uid):
        self.data["users"][uid]["sessions"] += 1
        self.save()

    def add_history(self, uid, message, reply):
        self.data["history"].append({
            "time": datetime.datetime.now().isoformat(),
            "uid": uid,
            "message": message,
            "reply": reply
        })
        self.save()

    def learn(self, text):
        self.data["learned"].append({
            "time": datetime.datetime.now().isoformat(),
            "text": text
        })
        self.save()

# ================= AI CORE =================

class Brain:

    def __init__(self, memory):
        self.memory = memory

    def analyze(self, message):
        m = message.lower()

        if "hello" in m or "hi" in m:
            return "greet"

        if "learn" in m:
            return "learn"

        if "report" in m or "stats" in m:
            return "report"

        if "plan" in m or "strategy" in m:
            return "strategy"

        if "exit" in m or "bye" in m:
            return "exit"

        return "general"

    def reply(self, intent, name, message):

        if intent == "greet":
            return f"Welcome {name}. System ready."

        if intent == "learn":
            self.memory.learn(message)
            return "Information stored."

        if intent == "report":
            return self.report()

        if intent == "strategy":
            return self.strategy(message)

        if intent == "exit":
            return f"Goodbye {name}."

        return "Explain more so I can analyze properly."

    def report(self):
        total_users = len(self.memory.data["users"])
        total_messages = len(self.memory.data["history"])
        total_learned = len(self.memory.data["learned"])

        return f"""
=== SYSTEM REPORT ===
Users: {total_users}
Messages: {total_messages}
Learned Data: {total_learned}
"""

    def strategy(self, message):
        length = len(message)
        words = len(message.split())

        return f"""
=== STRATEGIC ANALYSIS ===
Characters: {length}
Words: {words}

Recommended method:
1. Define goal
2. Analyze resources
3. Identify risks
4. Execute plan
"""

# ================= MAIN =================

class ZeynAI:

    def __init__(self):
        self.memory = Memory()
        self.brain = Brain(self.memory)

    def start(self):

        print("=================================")
        print("ZEYN STABLE v3")
        print("=================================")

        name = input("Enter your name: ").strip() or "Commander"

        uid = hashlib.sha256(name.encode()).hexdigest()[:12]

        if uid not in self.memory.data["users"]:
            self.memory.add_user(uid, name)

        self.memory.increase_session(uid)

        print(f"\nSystem online {name}.\n")

        while True:
            message = input(f"{name}: ").strip()

            if not message:
                continue

            intent = self.brain.analyze(message)
            answer = self.brain.reply(intent, name, message)

            print("\nZEYN:", answer)

            self.memory.add_history(uid, message, answer)

            if intent == "exit":
                break


if __name__ == "__main__":
    ZeynAI().start()
