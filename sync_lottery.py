import json
import requests


def main():
    print("🚀 กำลังดึงข้อมูลสถิติสลากกินแบ่งรัฐบาลย้อนหลัง 5 ปี (120 งวด)...")

    # ใส่ User-Agent เพื่อป้องกันโดนเซิร์ฟเวอร์ API บล็อก
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            " (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        )
    }

    all_draws = []
    for page in range(1, 9):
        list_url = f"https://lotto.api.rayriffy.com/list/{page}"
        try:
            res = requests.get(list_url, headers=headers, timeout=10)
            if res.status_code == 200:
                draws = res.json().get("response", [])
                all_draws.extend(draws)
            else:
                print(f"⚠️ หน้า {page} ตอบกลับด้วย Status: {res.status_code}")
                break
        except Exception as e:
            print(f"❌ เกิดข้อผิดพลาดในหน้า {page}: {e}")
            break

    print(f"📦 รวมรายการงวดที่พบทั้งหมด: {len(all_draws)} งวด")

    lottery_history = []
    total_draws = min(len(all_draws), 120)

    for index, draw in enumerate(all_draws[:total_draws]):
        draw_id = draw.get("id")
        detail_url = f"https://lotto.api.rayriffy.com/lotto/{draw_id}"

        try:
            res = requests.get(detail_url, headers=headers, timeout=10)
            if res.status_code == 200:
                data = res.json().get("response", {})
                prizes = data.get("prizes", [])

                first_prize = ""
                last_two = ""
                front_three = []
                last_three = []

                for item in prizes:
                    p_id = item.get("id")
                    num_list = item.get("number", [])

                    if p_id == "prizeFirst" and num_list:
                        first_prize = num_list[0]
                    elif p_id == "prizeTwo" and num_list:
                        last_two = num_list[0]
                    elif (
                        p_id in ["prizeFrontThree", "runningNumberFrontThree"]
                    ) and num_list:
                        front_three = num_list
                    elif (
                        p_id in ["prizeRearThree", "runningNumberRearThree"]
                    ) and num_list:
                        last_three = num_list

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
            print(f"Error fetching draw {draw_id}: {e}")

    # ทำการบันทึกเฉพาะเมื่อดึงข้อมูลได้จริงเท่านั้น
    if len(lottery_history) > 0:
        output_data = {
            "status": "online",
            "total_records": len(lottery_history),
            "history": lottery_history,
        }
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(
            f"✅ อัปเดต data.json สำเร็จ! บันทึกข้อมูลเรียบร้อย"
            f" {len(lottery_history)} งวด"
        )
    else:
        print("⚠️ ไม่สามารถดึงข้อมูลสถิติได้ ยกเลิกการบันทึกไฟล์")


if __name__ == "__main__":
    main()
