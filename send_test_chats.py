import random

from datetime import datetime, timedelta, timezone


import requests


WEBHOOK_URL = "http://127.0.0.1:8000/webhook"
AGENT_SPEED = {"Shalva": 0.8, "Giorgi": 1.0, "Lenka": 1.1, "Deme": 1.4}
CHANNELS = ["live_chat", "email", "whatsapp"]
NUM_CHATS = 200

random.seed(42)

# smaller sample = noisier numbers


def make_chat(number):
    agent = random.choice(list(AGENT_SPEED))
    start = datetime(2026, 9, 21, tzinfo=timezone.utc)+timedelta(
        days=random.randint(0, 6),
        hours=random.randint(5, 16),
        minutes=random.randint(0, 59),
    )

    handle_minutes = random.lognormvariate(2.2, 0.5) * AGENT_SPEED[agent]
    end = start + timedelta(minutes=handle_minutes)
    return {
        "chat_id": f"chat-{number:04d}",
        "agent_name": agent,
        "channel": random.choice(CHANNELS),
        "started_at": start.isoformat(),
        "ended_at": end.isoformat(),

    }


def main():
    counts = {}
    for number in range(1, NUM_CHATS + 1):
        response = requests.post(
            WEBHOOK_URL, json=make_chat(number), timeout=5)
        status = response.json().get("status", f"error{response.status_code}")
        counts[status] = counts.get(status, 0) + 1
    print("Done:", counts)


if __name__ == "__main__":
    main()


# გაკვეთილი ტესტირებიდან:  ერთ-ერთი მნიშვნელოვანი სქილი კპი-ებში არის:
# როდის იმოქმედო და როდის არა, მცირე რაოდენობის ჩატებში უფრო მაღალი ნოიზია ციფრებში
# რომელიც გაბნევს და ვერ ხვდები should react or no,
# not every difference in report means something !!!!!!!
# Aht(average handle time) შეიძლება უსამართლო იყოს რომელიმე საფორთისთვის, თუ მაგალითად
# დემე handles technical hard cases, აკეთებს მძიმე შრომას, კარგი რეპორტები უნდა შედარდეს
# ერთნაირ სამუშაოზე, ან at least add that context!
