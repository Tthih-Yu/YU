import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 系统配置
BASE_URL = "http://tysf.ahpu.edu.cn:8063"
API_ENDPOINT = "/web/Common/Tsm.html"
JSESSIONID = os.getenv("JSESSIONID", "")  # 从环境变量获取会话ID

# 宿舍楼信息（所有ID已从抓包验证）
BUILDINGS = {
    # 男生宿舍楼
    "男25#楼": "6",    # 已确认：buildingid=6
    "男22#楼": "4",    # 已确认：buildingid=4
    "男21#楼": "2",    # 已确认：buildingid=2
    "男20#楼": "8",    # 已确认：buildingid=8
    "男19#楼": "10",   # 已确认：buildingid=10
    "男18#楼": "12",   # 已确认：buildingid=12
    "男17#楼": "14",   # 已确认：buildingid=14
    "男16#楼": "52",   # 已确认：buildingid=52
    "男15#楼": "50",   # 已确认：buildingid=50
    "男14#楼": "49",   # 已确认：buildingid=49
    "男12#楼": "44",   # 已确认：buildingid=44
    "男11#楼": "42",   # 已确认：buildingid=42
    "男06#楼": "21",   # 已确认：buildingid=21
    "男05#楼": "25",   # 已确认：buildingid=25
    
    # 女生宿舍楼
    "女13#楼": "61",   # 已确认：buildingid=61
    "女12#楼": "60",   # 已确认：buildingid=60
    "女11#楼": "19",   # 已确认：buildingid=19
    "女10#楼": "38",   # 未在抓包中找到，请验证
    "女09#楼": "57",   # 已确认：buildingid=57
    "女08#楼": "17",   # 已确认：buildingid=17
    "女07#楼": "36",   # 已确认：buildingid=36
    "女06#楼": "56",   # 已确认：buildingid=56
    "女05#楼": "34",   # 已确认：buildingid=34
    "女04#楼": "32",   # 已确认：buildingid=32
    "女03#楼": "30",   # 已确认：buildingid=30
    "女02#楼": "28",   # 已确认：buildingid=28
    "女01#楼": "26",   # 已确认：buildingid=26
    
    # 研究生宿舍楼
    "研05#楼": "63",   # 已确认：buildingid=63
    "研04#楼": "16",   # 已确认：buildingid=16
    "研03#楼": "15",   # 已确认：buildingid=15
    "研02#楼": "38",   # 未在抓包中找到，请验证
    "研01#楼": "37",   # 已确认：buildingid=37
    
    # 梦溪7栋宿舍楼
    "梦溪7-1栋": "65",  # 已确认：buildingid=65
    "梦溪7-2栋": "66",  # 已确认：buildingid=66
    "梦溪7-3栋": "67",  # 已确认：buildingid=67
    "梦溪7-4栋": "68",  # 已确认：buildingid=68
    "梦溪7-5栋": "69",  # 已确认：buildingid=69
    "梦溪7-6栋": "70",  # 已确认：buildingid=70
    "梦溪7-7栋": "71",  # 已确认：buildingid=71
    "梦溪7-8栋": "72",  # 已确认：buildingid=72
    
    # 梦溪7-9栋宿舍楼
    "梦溪7-9-A栋": "74",  # 已确认：buildingid=74
    "梦溪7-9-B栋": "73",  # 已确认：buildingid=73
    "梦溪7-9-C栋": "75"   # 已确认：buildingid=75
}

# 当前选择的宿舍信息
CURRENT_BUILDING = "梦溪7-5栋"  # 在这里修改宿舍楼
ROOM_ID = "312"                # 在这里修改房间号
ACCOUNT = "52885"              # 在这里修改账号（如果需要）

# 获取当前选择的宿舍楼ID（带错误处理）
try:
    BUILDING_ID = BUILDINGS[CURRENT_BUILDING]
    BUILDING_NAME = CURRENT_BUILDING
except KeyError:
    print(f"错误：未找到宿舍楼 '{CURRENT_BUILDING}' 的信息！")
    print(f"可用的宿舍楼包括：{', '.join(BUILDINGS.keys())}")
    print("请在 config.py 中修改 CURRENT_BUILDING 为以上列表中的宿舍楼名称")
    raise

# 区域信息
AREA_NAME = "安徽工程大学"

# 查询设置
CHECK_INTERVAL = 30  # 检查间隔（分钟）
LOW_BALANCE_THRESHOLD = 50  # 低余额提醒阈值（元）

# 数据存储
DATA_FILE = "electricity_data.csv"  # 数据存储文件名

# 通知设置
ENABLE_NOTIFICATION = True  # 是否启用通知
NOTIFICATION_THRESHOLD = 20  # 通知阈值（元）

# 请求头
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Linux; Android 15; 23127PN0CC Build/AQ3A.240627.003; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/134.0.6998.39 Mobile Safari/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
    "Origin": BASE_URL,
    "Referer": f"{BASE_URL}/web/common/checkEle.html"
} 