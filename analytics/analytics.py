import csv, os
from collections import Counter
import matplotlib.pyplot as plt

CAPTURE_FILE = os.path.join(os.path.dirname(__file__), '..', 'captured_credentials_redacted.csv')
OUT = os.path.join(os.path.dirname(__file__), '..', 'screenshots', 'analytics_report.png')

def load_usernames():
    users = []
    if not os.path.exists(CAPTURE_FILE):
        return users
    with open(CAPTURE_FILE) as f:
        reader = csv.DictReader(f)
        for r in reader:
            users.append(r.get('username_redacted', 'unknown'))
    return users

def run():
    users = load_usernames()
    if not users:
        print("No captured data found.")
        return
    c = Counter(users)
    labels = list(c.keys())
    values = list(c.values())
    plt.figure(figsize=(6,3))
    plt.bar(range(len(labels)), values)
    plt.xticks(range(len(labels)), labels, rotation=45, ha='right')
    plt.title('Credential Submissions by Redacted Username (demo)')
    plt.tight_layout()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    plt.savefig(OUT)
    print("Saved analytics to:", OUT)

if __name__ == '__main__':
    run()
