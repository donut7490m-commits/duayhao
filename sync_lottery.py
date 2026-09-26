import json
import sys
import time
import requests


def fetch_lottery_data(target_draws=48):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
    }

    history = []

    for page in range(1, 7):
        url = f"https://lotto.api.rayriffy.com/list/{page}"
        try:
            res = requests.get(url, headers=headers, timeout=15)
            if res.status_code != 200:
                print(f"Page {page} Status Code: {res.status_code}")
                continue

            records = res.json().get("response", [])
            if not records:
                break

            for item in records:
                draw_id = item.get("id")
                detail_url = f"https://lotto.api.rayriffy.com/get/{draw_id}"
                detail_res = requests.get(
                    detail_url, headers=headers, timeout=15
                )

                if detail_res.status_code == 200:
                    detail = detail_res.json().get("response", {})

                    p1 = ""
                    prizes = detail.get("prizes", [])
                    if prizes and len(prizes) > 0:
                        nums = prizes[0].get("number", [])
                        if nums:
                            p1 = nums[0]

                    front_three, last_three, last_two = [], [], ""
                    for r in detail.get("runningNumbers", []):
                        if r.get("id") == "runningNumberFrontThree":
                            front_three = r.get("number", [])
                        elif r.get("id") == "runningNumberBackThree":
                            last_three = r.get("number", [])
                        elif r.get("id") == "runningNumberBackTwo":
                            nums = r.get("number", [])
                            last_two = nums[0] if nums else ""

                    history.append({
                        "date": detail.get("date", ""),
                        "first_prize": p1,
                        "front_three": front_three,
                        "last_three": last_three,
                        "last_two": last_two,
                    })

                    if len(history) >= target_draws:
                        break

                time.sleep(0.1)

        except Exception as e:
            print(f"Error fetching page {page}: {e}")

        if len(history) >= target_draws:
            break

    # หากดึงไม่ได้เลย ให้ส่ง Error ออกไปเพื่อให้ Workflow รู้
    if not history:
        print("❌ Error: Could not fetch lottery data from API.")
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
