import json
import time
import requests


def fetch_lottery_data(target_draws=48):
    # ปลอมแปลง User-Agent เพื่อป้องกันเซิร์ฟเวอร์ปฏิเสธการเชื่อมต่อ
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        ),
        "Accept": "application/json",
    }

    history = []
    page = 1

    # ดึงข้อมูลย้อนหลัง 2 ปี (ประมาณ 48-50 งวด)
    while len(history) < target_draws and page <= 6:
        url = f"https://lotto.api.rayriffy.com/list/{page}"
        try:
            res = requests.get(url, headers=headers, timeout=10)
            if res.status_code != 200:
                print(f"Page {page} HTTP Status: {res.status_code}")
                break

            records = res.json().get("response", [])
            if not records:
                break

            for item in records:
                draw_id = item.get("id")
                detail_url = f"https://lotto.api.rayriffy.com/get/{draw_id}"
                detail_res = requests.get(
                    detail_url, headers=headers, timeout=10
                )

                if detail_res.status_code == 200:
                    detail = detail_res.json().get("response", {})

                    # ดึงรางวัลที่ 1
                    p1 = detail.get("prizes", [{}])[0].get("number", [""])[0]

                    # ดึงเลขหน้า-เลขท้าย
                    p2 = detail.get("runningNumbers", [])
                    front_three, last_three, last_two = [], [], ""

                    for r in p2:
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

                time.sleep(0.2)  # หน่วงเวลาสั้นๆ ป้องกัน API บล็อก

        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break

        page += 1

    # สร้างโครงสร้างข้อมูลสำหรับบันทึก
    output = {
        "status": "online",
        "total_records": len(history),
        "history": history,
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"Successfully saved {len(history)} draws to data.json")


if __name__ == "__main__":
    fetch_lottery_data(48)
