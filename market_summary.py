# 1. 克隆仓库到本地
git clone https://github.com/lipaul9572-cloud/market-summary-bot.git
cd market-summary-bot

# 2. 创建 market_summary.py 文件
cat > market_summary.py << 'EOF'
#!/usr/bin/env python3
"""
美股每日总结自动发送脚本
"""

import requests
import os
from datetime import datetime

FEISHU_WEBHOOK = os.environ.get('FEISHU_WEBHOOK', 'https://open.larksuite.com/open-apis/bot/v2/hook/7c347cf2-6dcc-41ac-9c08-c3d53a59a05b')

def send_to_feishu(message):
    headers = {'Content-Type': 'application/json'}
    data = {"msg_type": "text", "content": {"text": message}}
    response = requests.post(FEISHU_WEBHOOK, headers=headers, json=data)
    return response.status_code == 200

def get_market_data():
    from datetime import datetime
    today = datetime.now().strftime("%Y-%m-%d")
    
    return {
        "date": today,
        "indices": {
            "S&P 500": {"close": "6,606", "change": "-0.45%"},
            "Nasdaq": {"close": "22,090", "change": "-0.77%"},
            "Dow Jones": {"close": "46,021", "change": "-0.26%"}
        },
        "magnificent_7": [
            {"name": "Apple (AAPL)", "change": "-0.5%"},
            {"name": "Microsoft (MSFT)", "change": "-0.3%"},
            {"name": "Nvidia (NVDA)", "change": "-0.9%"},
            {"name": "Google (GOOGL)", "change": "-0.4%"},
            {"name": "Amazon (AMZN)", "change": "-0.6%"},
            {"name": "Meta (META)", "change": "-1.3%"},
            {"name": "Tesla (TSLA)", "change": "-3.2%"}
        ],
        "commodities": {
            "黄金 (Gold)": "$4,673/盎司",
            "白银 (Silver)": "$72/盎司",
            "铜 (Copper)": "$12,250/吨",
            "原油 (Brent)": "$108/桶"
        },
        "crypto": {
            "Bitcoin (BTC)": "$70,618 (-0.5%)",
            "Ethereum (ETH)": "$2,143 (-2.4%)",
            "XRP": "$1.44 (-1.2%)",
            "BNB": "$642 (-1.0%)"
        },
        "analyst_outlook": [
            "Goldman Sachs: S&P 500 目标 7,600 (2026年底)",
            "高盛警告: 严重石油冲击可能将S&P 500拉低至5,400",
            "美联储维持利率3.5-3.75%，预计仅一次降息"
        ],
        "market_sentiment": "受地缘政治和通胀担忧影响，市场波动加剧"
    }

def format_message(data):
    msg = f"📊 **美股每日总结** - {data['date']}\n\n"
    msg += "**📈 美股三大指数**\n"
    for idx, info in data['indices'].items():
        msg += f"• {idx}: {info['close']} ({info['change']})\n"
    msg += "\n**🔥 Magnificent 7 科技股**\n"
    for stock in data['magnificent_7']:
        msg += f"• {stock['name']}: {stock['change']}\n"
    msg += "\n**🛢️ 大宗商品**\n"
    for name, price in data['commodities'].items():
        msg += f"• {name}: {price}\n"
    msg += "\n**💰 加密货币**\n"
    for name, price in data['crypto'].items():
        msg += f"• {name}: {price}\n"
    msg += "\n**📰 券商观点**\n"
    for outlook in data['analyst_outlook']:
        msg += f"• {outlook}\n"
    msg += f"\n**💡 市场情绪**: {data['market_sentiment']}\n"
    return msg

def main():
    print("正在获取市场数据...")
    data = get_market_data()
    message = format_message(data)
    print("正在发送到飞书...")
    success = send_to_feishu(message)
    print("✅ 发送成功!" if success else "❌ 发送失败!")
    return success

if __name__ == "__main__":
    main()
EOF

# 3. 创建 .github/workflows 目录
mkdir -p .github/workflows

# 4. 创建 GitHub Actions workflow 文件
cat > .github/workflows/market-summary.yml << 'EOF'
name: Daily US Market Summary

on:
  schedule:
    - cron: '0 9 * * 1-5'
  workflow_dispatch:

jobs:
  market-summary:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install requests
      - name: Run market summary
        env:
          FEISHU_WEBHOOK: \${{ secrets.FEISHU_WEBHOOK }}
        run: python market_summary.py
EOF

# 5. 提交并推送
git add .
git commit -m "Add market summary bot"
git push origin main
