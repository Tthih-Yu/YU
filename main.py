import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import schedule
import time
import json
import config
import os
import urllib.parse
import re

# 设置matplotlib中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

class ElectricityMonitor:
    def __init__(self):
        self.session = requests.Session()
        self.data_file = config.DATA_FILE
        self.headers = config.HEADERS.copy()
        self.initialize_data_file()
        if config.JSESSIONID:
            self.session.cookies.set("JSESSIONID", config.JSESSIONID)

    def initialize_data_file(self):
        """初始化数据文件"""
        if not os.path.exists(self.data_file):
            df = pd.DataFrame(columns=['timestamp', 'balance', 'consumption'])
            df.to_csv(self.data_file, index=False)

    def extract_balance(self, errmsg):
        """从错误消息中提取余额"""
        match = re.search(r'剩余电量(\d+\.\d+)', errmsg)
        if match:
            return float(match.group(1))
        return 0.0

    def get_electricity_data(self):
        """获取电费数据"""
        try:
            # 构建请求数据
            query_data = {
                "query_elec_roominfo": {
                    "aid": "0030000000002501",
                    "account": config.ACCOUNT,
                    "room": {
                        "roomid": config.ROOM_ID,
                        "room": config.ROOM_ID
                    },
                    "floor": {
                        "floorid": "",
                        "floor": ""
                    },
                    "area": {
                        "area": config.AREA_NAME,
                        "areaname": config.AREA_NAME
                    },
                    "building": {
                        "buildingid": config.BUILDING_ID,
                        "building": config.BUILDING_NAME
                    }
                }
            }
            
            # 构建表单数据
            form_data = {
                "jsondata": json.dumps(query_data),
                "funname": "synjones.onecard.query.elec.roominfo",
                "json": "true"
            }
            
            # 发送请求获取电费数据
            response = self.session.post(
                f"{config.BASE_URL}{config.API_ENDPOINT}",
                headers=self.headers,
                data=urllib.parse.urlencode(form_data)
            )
            
            if response.status_code == 200:
                data = response.json()
                # 解析返回的数据
                if "query_elec_roominfo" in data:
                    room_info = data["query_elec_roominfo"]
                    if room_info["retcode"] == "0":  # 成功返回
                        balance = self.extract_balance(room_info["errmsg"])
                        return {
                            'timestamp': datetime.now(),
                            'balance': balance,
                            'consumption': 0.0  # 暂时没有用电量数据
                        }
                    else:
                        print(f"查询失败: {room_info.get('errmsg', '未知错误')}")
                        return None
                else:
                    print("返回数据格式错误")
                    return None
            else:
                print(f"获取数据失败: HTTP {response.status_code}")
                return None
                
        except Exception as e:
            print(f"获取数据失败: {str(e)}")
            return None

    def save_data(self, data):
        """保存数据到文件"""
        if data:
            df = pd.read_csv(self.data_file)
            new_row = pd.DataFrame([data])
            df = pd.concat([df, new_row], ignore_index=True)
            df.to_csv(self.data_file, index=False)

    def plot_data(self):
        """绘制数据图表"""
        try:
            df = pd.read_csv(self.data_file)
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            
            plt.figure(figsize=(10, 6))
            plt.plot(df['timestamp'], df['balance'], label='余额')
            plt.plot(df['timestamp'], df['consumption'], label='用电量')
            plt.title('电费数据趋势')
            plt.xlabel('时间')
            plt.ylabel('金额/用电量')
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig('electricity_trend.png')
            plt.close()
        except Exception as e:
            print(f"绘制图表失败: {str(e)}")

    def check_balance(self):
        """检查余额并发送提醒"""
        data = self.get_electricity_data()
        if data and data['balance'] < config.LOW_BALANCE_THRESHOLD:
            print(f"警告：电费余额不足！当前余额：{data['balance']}元")
            # TODO: 实现通知功能（如发送邮件或微信消息）

    def run(self):
        """运行监控程序"""
        print("开始监控电费数据...")
        print(f"正在监控 {config.BUILDING_NAME} {config.ROOM_ID} 房间的电费情况")
        
        # 设置定时任务
        schedule.every(config.CHECK_INTERVAL).minutes.do(self.check_balance)
        
        while True:
            schedule.run_pending()
            data = self.get_electricity_data()
            if data:
                print(f"当前电费余额：{data['balance']}元")
                self.save_data(data)
                self.plot_data()
            time.sleep(60)

if __name__ == "__main__":
    monitor = ElectricityMonitor()
    monitor.run() 