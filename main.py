import os
import json
import requests
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# 設定 logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# 嘗試讀取金鑰
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_TOKEN')

# 如果環境變數沒有，嘗試從 secrets.json 讀取（本地測試用）
if not TELEGRAM_TOKEN:
    try:
        if os.path.exists('secrets.json'):
            with open('secrets.json') as f:
                secrets = json.load(f)
            TELEGRAM_TOKEN = secrets.get('TELEGRAM_TOKEN')
            if TELEGRAM_TOKEN:
                logger.info("從 secrets.json 讀取金鑰成功")
    except Exception as e:
        logger.error(f"讀取 secrets.json 錯誤: {e}")

# 檢查是否有 Token
if not TELEGRAM_TOKEN:
    logger.error("❌ 錯誤：沒有找到 Telegram Token！")
    logger.info("請設定環境變數 TELEGRAM_TOKEN 或建立 secrets.json")
    # 不直接 exit，讓使用者在 logs 看到提示
else:
    logger.info("✅ 已取得 Telegram Token")

# Telegram 指令處理
async def start(update: Update, context: CallbackContext):
    """處理 /start 指令"""
    user = update.effective_user
    await update.message.reply_text(
        f'你好 {user.first_name}！👋\n'
        '我是你的 AI 助理，目前功能：\n'
        '/start - 顯示此訊息\n'
        '/weather [城市] - 查詢天氣\n'
        '/stock [股票代碼] - 查詢股價\n\n'
        '例如：\n'
        '/weather 台北\n'
        '/stock 2330'
    )

async def weather(update: Update, context: CallbackContext):
    """查詢天氣"""
    # 如果沒有輸入城市，預設為台北
    city = ' '.join(context.args) if context.args else '台北'
    
    await update.message.reply_text(f'正在查詢 {city} 的天氣...')
    
    # 這裡先模擬回應，稍後可以接真實 API
    weather_data = {
        '台北': '多雲時晴，25°C',
        '高雄': '晴天，28°C',
        '台中': '陰天，24°C'
    }
    
    if city in weather_data:
        await update.message.reply_text(f'{city}天氣：{weather_data[city]}')
    else:
        await update.message.reply_text(f'找不到 {city} 的天氣資料，請試試：台北、高雄、台中')

async def stock(update: Update, context: CallbackContext):
    """查詢股價"""
    stock_code = ' '.join(context.args) if context.args else '2330'
    
    await update.message.reply_text(f'正在查詢 {stock_code} 股價...')
    
    # 模擬股價資料
    stock_data = {
        '2330': '台積電：585 元',
        '2317': '鴻海：102 元',
        '2454': '聯發科：925 元',
        '2882': '國泰金：45 元'
    }
    
    if stock_code in stock_data:
        await update.message.reply_text(stock_data[stock_code])
    else:
        await update.message.reply_text(f'找不到 {stock_code} 的股價，請試試：2330, 2317, 2454, 2882')

async def help_command(update: Update, context: CallbackContext):
    """幫助指令"""
    await update.message.reply_text(
        '可用指令：\n'
        '/start - 開始使用\n'
        '/weather [城市] - 查天氣\n'
        '/stock [股票代碼] - 查股價\n'
        '/help - 顯示此幫助訊息\n\n'
        '範例：\n'
        '/weather 台北\n'
        '/stock 2330'
    )

async def echo(update: Update, context: CallbackContext):
    """回覆用戶訊息"""
    user_message = update.message.text
    await update.message.reply_text(f'你說了：{user_message}\n\n請使用指令，例如 /help 查看可用指令')

def main():
    """主程式"""
    if not TELEGRAM_TOKEN:
        logger.error("無法啟動：缺少 TELEGRAM_TOKEN")
        return

    logger.info("🤖 正在啟動 Telegram Bot...")
    
    # 建立 Application
    application = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # 加入指令處理器
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("weather", weather))
    application.add_handler(CommandHandler("stock", stock))
    application.add_handler(CommandHandler("help", help_command))
    
    # 加入訊息處理器（非指令訊息）
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    
    # 啟動 Bot
    logger.info("✅ Bot 啟動完成！等待訊息中...")
    application.run_polling()

if __name__ == '__main__':
    main()
