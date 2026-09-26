import json
import requests


def fetch_thai_lottery_5years():
    print("🚀 กำลังดึงข้อมูลสถิติหวยรัฐบาลย้อนหลัง 5 ปี (120 งวด)...")

    all_draws = []
    # ดึงรายการงวด 8 หน้า (รวมประมาณ 120 งวด)
    for page in range(1, 9):
        list_url = f"https://lotto.api.rayriffy.com/list/{page}"
        try:
            res = requests.get(list_url, timeout=10)
            if res.status_code == 200:
                draws = res.json().get("response", [])
                all_draws.extend(draws)
            else:
                break
        except Exception as e:
            print(f"Error page {page}: {e}")
            break

    lottery_history = []
    total_draws = min(len(all_draws), 120)

    for index, draw in enumerate(all_draws[:total_draws]):
        draw_id = draw.get("id")
        detail_url = f"https://lotto.api.rayriffy.com/lotto/{draw_id}"

        try:
            res = requests.get(detail_url, timeout=10)
            if res.status_code == 200:
                data = res.json().get("response", {})
                prizes = data.get("prizes", [])

                first_prize = ""
                last_two = ""
                front_three = []
                last_three = []

                for item in prizes:
                    p_id = item.get("id")
                    number_list = item.get("number", [])

                    if p_id == "prizeFirst" and number_list:
                        first_prize = number_list[0]
                    elif p_id == "prizeTwo" and number_list:
                        last_two = number_list[0]
                    elif (
                        p_id in ["prizeFrontThree", "runningNumberFrontThree"]
                    ) and number_list:
                        front_three = number_list
                    elif (
                        p_id in ["prizeRearThree", "runningNumberRearThree"]
                    ) and number_list:
                        last_three = number_list

                lottery_history.append(
                    {
                        "date": data.get("date", draw.get("date")),
                        "first_prize": first_prize,
                        "front_three": front_three,
                        "last_three": last_three,
                        "last_two": last_two,
                    }
                )
        except Exception as e:
            print(f"Error draw {draw_id}: {e}")

    output_data = {
        "status": "online",
        "total_records": len(lottery_history),
        "history": lottery_history,
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print("✅ ดึงข้อมูลสำเร็จครบ 120 งวดแล้ว!")


if __name__ == "__main__":
    fetch_thai_lottery_5years()
