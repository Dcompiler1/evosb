from database import *
from telegram import (Update, KeyboardButton, ReplyKeyboardMarkup,
                      InlineKeyboardButton, InlineKeyboardMarkup,ReplyKeyboardRemove)
from telegram.ext import (CallbackContext, CommandHandler, MessageHandler, Filters,
                          Updater, ConversationHandler,CallbackQueryHandler)

db = Database()
# db.add()

def start(update,context):
    buttons = [
        [KeyboardButton('Buyurtma qilish')]
    ]
    update.message.reply_text('Quyidagilardan birini tanlang:',reply_markup=ReplyKeyboardMarkup(buttons,resize_keyboard=True))
    return 1

def menu(update,context):
    categories = db.get_menu()
    buttons = make_button(categories,"parent")
    update.message.reply_text('Quyidagilardan birini tanlang: ',reply_markup=InlineKeyboardMarkup(buttons))
    return 2

def inline_menu(update,context):
    query = update.callback_query
    data = query.data
    data_split = data.split('_')
    if data_split[0] == "category":
        if data_split[1] == "parent":
            categories = db.get_menu_child(data_split[2])
            buttons = make_button(categories,"child")
            buttons.append([InlineKeyboardButton('BACK TO parent',callback_data=f'back_{data_split[2]}')])
            query.message.edit_text('Quyidagilardan birini tanlang: ', reply_markup=InlineKeyboardMarkup(buttons))
        elif data_split[1] == "child":
            types = db.get_type(int(data_split[2]))
            buttons = []
            btn = []
            for data in types:
                btn.append(
                    InlineKeyboardButton(f"{data['name']}", callback_data=f"type_{data_split[2]}_{data['id']}"))
                if len(btn) == 2:
                    buttons.append(btn)
                    btn = []
            if len(btn) == 1:
                buttons.append(btn)
            buttons.append([InlineKeyboardButton('BACK TO - child',callback_data=f'back_{data_split[2]}')])
            query.message.edit_text('Quyidagilardan birini tanlang: ',reply_markup=InlineKeyboardMarkup(buttons))
    elif data_split[0] == "type":
        sonlar = {1: '1️⃣', 2: '2️⃣', 3: '3️⃣', 4: '4️⃣', 5: '5️⃣', 6: '6️⃣', 7: '7️⃣', 8: '8️⃣', 9: '9️⃣'}
        ctg_id = int(data_split[1])
        type_id = int(data_split[2])
        product = db.get_product(ctg_id,type_id)
        button = make_btn(sonlar,product["id"])
        query.message.delete()
        button.append([InlineKeyboardButton('BACK TO types',callback_data=f'back_{data_split[2]}')])
        query.message.reply_photo(photo=open('photo/lavash.jpg','rb',),caption=f"Narxi: {product['price']}\nTarkibi: {product['description']}\nMiqdorni tanlang yoki kiriting:",reply_markup=InlineKeyboardMarkup(button))
    elif data_split[0] == "product":
        product_id = data_split[1]
        count = data_split[2]
        savatcha = db.get_product_by_id(product_id)
        query.message.delete()
        query.message.reply_text(f"<b>Savatchada:</b>\n{str(count).replace('1','1️⃣').replace('2','2️⃣').replace('3','3️⃣').replace('4','4️⃣').replace('5','5️⃣').replace('6','6️⃣').replace('7','7️⃣').replace('8','8️⃣').replace('9','9️⃣')} - {savatcha['name']}\n\n<b>Mahsulotlar:</b>{int(count)*int(savatcha['price'])} so`m\n<b>Yetkazib berish:</b> 9 000 so`m\n<b>Jami: {int(count)*int(savatcha['price'])+9000}</b>",parse_mode='html')
def make_button(categories,ctg_type):
    buttons = []
    btn = []
    for category in categories:
        btn.append(InlineKeyboardButton(f"{category['name']}", callback_data=f"category_{ctg_type}_{category['id']}"))
        if len(btn) == 2:
            buttons.append(btn)
            btn = []
    if len(btn) == 1:
        buttons.append(btn)
    return buttons


def make_btn(categories,product_id):
    buttons = []
    btn = []
    for son,harf in categories.items():
        btn.append(InlineKeyboardButton(f"{harf}", callback_data=f"product_{product_id}_{son}"))
        if len(btn) == 2:
            buttons.append(btn)
            btn = []
    if len(btn) == 1:
        buttons.append(btn)
    return buttons

def main():
    TOKEN = '5298470905:AAFYQUgM-4d9-DAmHnjOnUjde9bMlH47kmA'
    updater = Updater(TOKEN)

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            1: [MessageHandler(Filters.regex('Buyurtma qilish'),menu)],
            2: [CallbackQueryHandler(inline_menu)]
        },
        fallbacks=[]
    )
    updater.dispatcher.add_handler(conv_handler)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
