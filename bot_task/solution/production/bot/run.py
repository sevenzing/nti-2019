from personal_data_bot import app
from personal_data_bot.configtools import BOT_PORT

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int(BOT_PORT))