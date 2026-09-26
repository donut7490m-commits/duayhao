import json
import sys
import requests


def fetch_lottery_data(target_draws=48):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
    }

    # API แหล่งใหม่สำหรับดึงข้อมูลหวยรัฐบาลไทยย้อนหลัง
    url = f"https://thai-lottery-api.vercel.app/api/lottery/history?limit={target_draws}"

    history = []

    try:
        res = requests.get(url, headers=headers, timeout=15)
        if res.status_code == 200:
            data = res.json()
            records = (
                data.get("data", [])
                if isinstance(data, dict)
                else data if isinstance(data, list) else []
            )

            for item in records:
                history.append({
                    "date": item.get("date", ""),
                    "first_prize": str(item.get("first_prize", "")),
                    "front_three": [
                        str(x) for x in item.get("front_three", [])
                    ],
                    "last_three": [str(x) for x in item.get("last_three", [])],
                    "last_two": str(item.get("last_two", "")),
                })
    except Exception as e:
        print(f"Primary API Error: {e}")

    # หาก API หลักมีปัญหา ให้ดึงผ่าน API สำรองทันที
    if not history:
        try:
            backup_url = "https://raw.githubusercontent.com/code-m/thai-lottery-data/main/data.json"
            res = requests.get(backup_url, headers=headers, timeout=15)
            if res.status_code == 200:
                backup_data = res.json()
                history = backup_data.get("history", [])[:target_draws]
        except Exception as e:
            print(f"Backup API Error: {e}")

    if not history:
        print("❌ Error: Could not fetch lottery data from any API.")
        sys.exit(1)

    output = {
        "status": "online",
        "total_records": len(history),
        "history": history,
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"✅ Successfully saved {len(history)} draws to data.json")


if __name__ == "__main__":
    fetch_lottery_data(48)
