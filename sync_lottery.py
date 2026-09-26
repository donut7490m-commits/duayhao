import json

# คลังข้อมูลผลรางวัลสลากกินแบ่งรัฐบาลย้อนหลัง 2567 - 2569 (จำนวน 65 งวด)
REAL_LOTTERY_DATA = [
    # --- ปี 2569 ---
    {"date": "16 กันยายน 2569", "first_prize": "730640", "last_two": "64"},
    {"date": "1 กันยายน 2569", "first_prize": "417212", "last_two": "04"},
    {"date": "16 สิงหาคม 2569", "first_prize": "004615", "last_two": "53"},
    {"date": "1 สิงหาคม 2569", "first_prize": "932479", "last_two": "69"},
    {"date": "16 กรกฎาคม 2569", "first_prize": "639214", "last_two": "71"},
    {"date": "1 กรกฎาคม 2569", "first_prize": "751495", "last_two": "62"},
    {"date": "16 มิถุนายน 2569", "first_prize": "287184", "last_two": "48"},
    {"date": "1 มิถุนายน 2569", "first_prize": "173770", "last_two": "95"},
    {"date": "16 พฤษภาคม 2569", "first_prize": "107387", "last_two": "08"},
    {"date": "2 พฤษภาคม 2569", "first_prize": "536077", "last_two": "43"},
    {"date": "16 เมษายน 2569", "first_prize": "309612", "last_two": "77"},
    {"date": "1 เมษายน 2569", "first_prize": "292514", "last_two": "47"},
    {"date": "16 มีนาคม 2569", "first_prize": "833009", "last_two": "64"},
    {"date": "1 มีนาคม 2569", "first_prize": "820866", "last_two": "06"},
    {"date": "16 กุมภาพันธ์ 2569", "first_prize": "340563", "last_two": "07"},
    {"date": "1 กุมภาพันธ์ 2569", "first_prize": "174629", "last_two": "48"},
    {"date": "17 มกราคม 2569", "first_prize": "878972", "last_two": "02"},
    {"date": "2 มกราคม 2569", "first_prize": "837706", "last_two": "16"},

    # --- ปี 2568 ---
    {"date": "16 ธันวาคม 2568", "first_prize": "763895", "last_two": "52"},
    {"date": "1 ธันวาคม 2568", "first_prize": "461252", "last_two": "22"},
    {"date": "16 พฤศจิกายน 2568", "first_prize": "458145", "last_two": "37"},
    {"date": "1 พฤศจิกายน 2568", "first_prize": "345898", "last_two": "87"},
    {"date": "16 ตุลาคม 2568", "first_prize": "059696", "last_two": "61"},
    {"date": "1 ตุลาคม 2568", "first_prize": "876978", "last_two": "77"},
    {"date": "16 กันยายน 2568", "first_prize": "074646", "last_two": "58"},
    {"date": "1 กันยายน 2568", "first_prize": "506356", "last_two": "31"},
    {"date": "16 สิงหาคม 2568", "first_prize": "994865", "last_two": "63"},
    {"date": "1 สิงหาคม 2568", "first_prize": "811852", "last_two": "50"},
    {"date": "16 กรกฎาคม 2568", "first_prize": "245324", "last_two": "26"},
    {"date": "1 กรกฎาคม 2568", "first_prize": "949246", "last_two": "91"},
    {"date": "16 มิถุนายน 2568", "first_prize": "507392", "last_two": "06"},
    {"date": "1 มิถุนายน 2568", "first_prize": "559352", "last_two": "20"},
    {"date": "16 พฤษภาคม 2568", "first_prize": "251309", "last_two": "87"},
    {"date": "2 พฤษภาคม 2568", "first_prize": "213388", "last_two": "06"},
    {"date": "16 เมษายน 2568", "first_prize": "266227", "last_two": "85"},
    {"date": "1 เมษายน 2568", "first_prize": "669687", "last_two": "36"},
    {"date": "16 มีนาคม 2568", "first_prize": "757563", "last_two": "32"},
    {"date": "1 มีนาคม 2568", "first_prize": "818894", "last_two": "54"},
    {"date": "16 กุมภาพันธ์ 2568", "first_prize": "847377", "last_two": "50"},
    {"date": "1 กุมภาพันธ์ 2568", "first_prize": "558700", "last_two": "51"},
    {"date": "17 มกราคม 2568", "first_prize": "807779", "last_two": "23"},
    {"date": "2 มกราคม 2568", "first_prize": "730209", "last_two": "51"},

    # --- ปี 2567 ---
    {"date": "16 ธันวาคม 2567", "first_prize": "097863", "last_two": "21"},
    {"date": "1 ธันวาคม 2567", "first_prize": "669843", "last_two": "61"},
    {"date": "16 พฤศจิกายน 2567", "first_prize": "187221", "last_two": "38"},
    {"date": "1 พฤศจิกายน 2567", "first_prize": "536044", "last_two": "32"},
    {"date": "16 ตุลาคม 2567", "first_prize": "482962", "last_two": "00"},
    {"date": "1 ตุลาคม 2567", "first_prize": "718665", "last_two": "59"},
    {"date": "16 กันยายน 2567", "first_prize": "608662", "last_two": "37"},
    {"date": "1 กันยายน 2567", "first_prize": "199606", "last_two": "94"},
    {"date": "16 สิงหาคม 2567", "first_prize": "095867", "last_two": "28"},
    {"date": "1 สิงหาคม 2567", "first_prize": "407041", "last_two": "46"},
    {"date": "16 กรกฎาคม 2567", "first_prize": "367336", "last_two": "21"},
    {"date": "1 กรกฎาคม 2567", "first_prize": "434503", "last_two": "89"},
    {"date": "16 มิถุนายน 2567", "first_prize": "518504", "last_two": "31"},
    {"date": "1 มิถุนายน 2567", "first_prize": "530593", "last_two": "42"},
    {"date": "16 พฤษภาคม 2567", "first_prize": "205690", "last_two": "60"},
    {"date": "2 พฤษภาคม 2567", "first_prize": "980116", "last_two": "17"},
    {"date": "16 เมษายน 2567", "first_prize": "943598", "last_two": "79"},
    {"date": "1 เมษายน 2567", "first_prize": "803481", "last_two": "90"},
    {"date": "16 มีนาคม 2567", "first_prize": "997626", "last_two": "78"},
    {"date": "1 มีนาคม 2567", "first_prize": "253603", "last_two": "79"},
    {"date": "16 กุมภาพันธ์ 2567", "first_prize": "941395", "last_two": "43"},
    {"date": "1 กุมภาพันธ์ 2567", "first_prize": "607063", "last_two": "09"},
    {"date": "17 มกราคม 2567", "first_prize": "105979", "last_two": "61"},
]


def update_data():
    output = {
        "status": "online",
        "total_records": len(REAL_LOTTERY_DATA),
        "history": REAL_LOTTERY_DATA,
    }

    with open("data.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(
        f"✅ Updated data.json successfully with {len(REAL_LOTTERY_DATA)}"
        " records."
    )


if __name__ == "__main__":
    update_data()
