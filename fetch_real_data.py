import json
import requests


def fetch_thai_lottery_5years():
    print("🚀 กำลังดึงข้อมูลสถิติหวยรัฐบาลย้อนหลัง 5 ปี...")

    # ดึงรายการงวดหวยย้อนหลังผ่าน Open API (ดึงได้สูงสุด 120 งวด ~ 5 ปี)
    all_draws = []

    # API รองรับการดึงแบบเป็นสเปครายการงวด (Page 1 - 8)
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
            print(f"เกิดข้อผิดพลาดในการดึงรายการงวด หน้า {page}: {e}")
            break

    # นำ ID แต่ละงวดมาดึงรายละเอียดผลรางวัลจริง
    lottery_history = []
    total_draws = min(len(all_draws), 120)  # ย้อนหลังประมาณ 5 ปี (120 งวด)

    print(f"📦 พบรายการทั้งหมด {total_draws} งวด กำลังประมวลผล...")

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
                    elif p_id == "prizeTwo" and number_list:  # เลขท้าย 2 ตัว
                        last_two = number_list[0]
                    elif (
                        p_id == "prizeFrontThree" or p_id == "runningNumberFrontThree"
                    ) and number_list:
                        front_three = number_list
                    elif (
                        p_id == "prizeRearThree" or p_id == "runningNumberRearThree"
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
                print(
                    f"[{index + 1}/{total_draws}] ดึงข้อมูลสำเร็จ: งวด {data.get('date')}"
                )
        except Exception as e:
            print(f"เกิดข้อผิดพลาดที่งวด {draw_id}: {e}")

    # บันทึกลงไฟล์ data.json
    output_data = {
        "status": "online",
        "last_updated": "2026-09-26",
        "total_records": len(lottery_history),
        "history": lottery_history,
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)

    print("✅ บันทึกข้อมูลจริงย้อนหลัง 5 ปีลงใน data.json เรียบร้อยแล้วครับ!")


if __name__ == "__main__":
    fetch_thai_lottery_5years()
