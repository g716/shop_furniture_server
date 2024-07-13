from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from db import db
from keyboard import keyboard

bot = Bot('7062289584:AAESDlt2059jXKdqO-8w2syJvW5qmkDLKbs')

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
db_shop_furniture = db.Database('identifier.sqlite')
keyboard_panel = keyboard.Panel(db_shop_furniture)


class OrderCatalog(StatesGroup):
    name = State()


class OrderProduct(StatesGroup):
    name = State()
    price = State()
    about = State()
    count = State()
    image = State()
    catalog = State()


class Order(StatesGroup):
    id_ = State()
    id_product = State()
    phone_number = State()
    address = State()
    count_product = State()


class EditCatalog(StatesGroup):
    id_ = State()
    name = State()


class EditProduct(StatesGroup):
    id_ = State()
    name = State()
    price = State()
    about = State()
    count = State()
    image = State()
    catalog = State()


@dp.callback_query_handler()
async def callback_query(call: types.CallbackQuery, state: FSMContext):
    # Товары
    if 'delete_product' in call.data:
        await db_shop_furniture.delete_product(int(call.data.split(';')[1]))
        await call.answer('Товар удален')
    if 'edit_product' in call.data:
        await bot.send_message(chat_id=call.from_user.id, text='Редактировать: ',
                               reply_markup=keyboard.product_panel_edit(int(call.data.split(';')[1])))
    if 'name_product' in call.data:
        await EditProduct.id_.set()
        async with state.proxy() as data:
            data['id_'] = int(call.data.split(';')[1])
        await EditProduct.name.set()
        keyboard_to_delete = types.ReplyKeyboardRemove()
        await bot.send_message(chat_id=call.from_user.id, text='Редактирование товара:',
                               reply_markup=keyboard_to_delete)
        await bot.send_message(chat_id=call.from_user.id, text='Введите новое название',
                               reply_markup=keyboard.cancel_panel())
    if 'about_product' in call.data:
        await EditProduct.id_.set()
        async with state.proxy() as data:
            data['id_'] = int(call.data.split(';')[1])
        await EditProduct.about.set()
        keyboard_to_delete = types.ReplyKeyboardRemove()
        await bot.send_message(chat_id=call.from_user.id, text='Редактирование товара:',
                               reply_markup=keyboard_to_delete)
        await bot.send_message(chat_id=call.from_user.id, text='Введите новое описание товара не более 800 символов',
                               reply_markup=keyboard.cancel_panel())
    if 'price_product' in call.data:
        await EditProduct.id_.set()
        async with state.proxy() as data:
            data['id_'] = int(call.data.split(';')[1])
        await EditProduct.price.set()
        keyboard_to_delete = types.ReplyKeyboardRemove()
        await bot.send_message(chat_id=call.from_user.id, text='Редактирование товара:',
                               reply_markup=keyboard_to_delete)
        await bot.send_message(chat_id=call.from_user.id, text='Укажите новую цену',
                               reply_markup=keyboard.cancel_panel())
    if 'count_product' in call.data:
        await EditProduct.id_.set()
        async with state.proxy() as data:
            data['id_'] = int(call.data.split(';')[1])
        await EditProduct.count.set()
        keyboard_to_delete = types.ReplyKeyboardRemove()
        await bot.send_message(chat_id=call.from_user.id, text='Редактирование товара:',
                               reply_markup=keyboard_to_delete)
        await bot.send_message(chat_id=call.from_user.id, text='Укажите количество товара',
                               reply_markup=keyboard.cancel_panel())
    if 'image_product' in call.data:
        await EditProduct.id_.set()
        async with state.proxy() as data:
            data['id_'] = int(call.data.split(';')[1])
        await EditProduct.image.set()
        keyboard_to_delete = types.ReplyKeyboardRemove()
        await bot.send_message(chat_id=call.from_user.id, text='Редактирование товара:',
                               reply_markup=keyboard_to_delete)
        await bot.send_message(chat_id=call.from_user.id, text='Отправьте фотографию товара',
                               reply_markup=keyboard.cancel_panel())

    if 'order_product' in call.data:
        await Order.id_.set()
        async with state.proxy() as data:
            data['tg_id'] = call.from_user.id
            data['id_product'] = int(call.data.split(';')[1])
        await Order.phone_number.set()
        keyboard_to_delete = types.ReplyKeyboardRemove()
        await bot.send_message(chat_id=call.from_user.id, text='Оформление заказа:',
                               reply_markup=keyboard_to_delete)
        await bot.send_message(chat_id=call.from_user.id, text='Введите контактный телефон',
                               reply_markup=keyboard.cancel_panel())

    # Каталоги
    if 'product_list' in call.data:
        if len(await db_shop_furniture.get_id_products_from_catalog(int(call.data.split(';')[1]))) > 0 and len:
            for data_catalog in await db_shop_furniture.get_id_products_from_catalog(int(call.data.split(';')[1])):
                id_product = data_catalog[1]
                product_item = await db_shop_furniture.get_product(id_product)
                photo = open(f'photo/{product_item[2]}.jpg', 'rb')
                if int(product_item[5]) > 0:
                    count_answer = """В наличии: """ + str(product_item[5]) + """ шт"""
                else:
                    count_answer = 'Нет в наличии'
                await bot.send_photo(call.from_user.id, photo, caption=f'Название: {product_item[1]}\n'
                                                                     f'Описание:\n{product_item[3]}\n'
                                                                     f'Цена: {product_item[4]} р\n'
                                                                     f'{count_answer}',
                                     reply_markup=keyboard.product_panel(product_item[0]))
        else:
            await bot.send_message(chat_id=call.from_user.id, text='Простите но каталог пока что пуст')
    if 'delete_catalog' in call.data:
        await db_shop_furniture.delete_catalog(int(call.data.split(';')[1]))
        await call.answer('Катаалог удален')
    if 'name_catalog' in call.data:
        await EditCatalog.id_.set()
        async with state.proxy() as data:
            data['id_'] = int(call.data.split(';')[1])
        await EditCatalog.name.set()
        keyboard_to_delete = types.ReplyKeyboardRemove()
        await bot.send_message(chat_id=call.from_user.id, text='Редактирование каталога:',
                               reply_markup=keyboard_to_delete)
        await bot.send_message(chat_id=call.from_user.id, text='Введите новое название',
                               reply_markup=keyboard.cancel_panel())


@dp.callback_query_handler(state=[OrderProduct, OrderCatalog, Order, EditProduct, EditCatalog])
async def cancel_order(call: types.CallbackQuery, state: FSMContext):

    if 'cancel' in call.data:
        if not bool(len([item for item in await db_shop_furniture.get_admins() if item[0] == int(call.from_user.id)])):
            markup_shop = keyboard.shop_panel()
        else:
            markup_shop = await keyboard_panel.admin_panel()
        await state.finish()
        await bot.send_message(chat_id=call.from_user.id,
                               text='Действия отменены', reply_markup=markup_shop)


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not bool(len(await db_shop_furniture.get_admins())):
        await db_shop_furniture.add_admin(
            tg_id=int(message.from_id),
            phone_number='',
            state='phone_number'
        )
        answer = f'Привет admin {message.from_user.first_name}'
        markup_shop = await keyboard_panel.admin_panel()
    else:
        if not bool(len([item for item in await db_shop_furniture.get_admins() if item[0] == int(message.from_id)])):
            answer = 'Добро пожаловать в магазин!'
            markup_shop = keyboard.shop_panel()
        else:
            answer = f'Привет admin {message.from_user.first_name}'
            markup_shop = await keyboard_panel.admin_panel()
    await message.answer(answer, reply_markup=markup_shop)


@dp.message_handler(commands=['shop'])
async def shop(message: types.Message):
    await message.answer('Добро пожаловать в магазин!', reply_markup=keyboard.shop_panel())


# Товары
@dp.message_handler(text='Товары')
async def product_list(message: types.Message):
    admin = False
    if not bool(len([item for item in await db_shop_furniture.get_admins() if item[0] == int(message.from_id)])):
        markup_shop = keyboard.shop_panel()
        products = await db_shop_furniture.get_products_available()
    else:
        markup_shop = await keyboard_panel.admin_panel()
        products = await db_shop_furniture.get_products()
        admin = True
    if bool(len(products)):
        for product_item in products:
            if admin:
                product_panel = keyboard.product_panel_admin(product_item[0])
            else:
                product_panel = keyboard.product_panel(product_item[0])
            photo = open(f'photo/{product_item[2]}.jpg', 'rb')
            if int(product_item[5]) > 0:
                count_answer = """В наличии: """ + str(product_item[5]) + """ шт"""
            else:
                count_answer = 'Нет в наличии'
            await bot.send_photo(message.chat.id, photo, caption=f'Название: {product_item[1]}\n'
                                 f'Описание:\n{product_item[3]}\n'
                                 f'Цена: {product_item[4]} р\n'
                                 f'{count_answer}',
                                 reply_markup=product_panel)
    else:
        await message.answer('Товаров пока что нет', reply_markup=markup_shop)


@dp.message_handler(state=EditProduct.name)
async def edit_name_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data_product = await db_shop_furniture.get_product(int(data['id_']))
        data['name'] = message.text
        data['id_'] = int(data['id_'])
        data['price'] = int(data_product[4])
        data['about'] = data_product[3]
        data['count'] = int(data_product[5])
        data['image'] = data_product[2]

    await db_shop_furniture.update_product(state)
    await message.answer('Название обнавленно', reply_markup=await keyboard_panel.admin_panel())
    await state.finish()


@dp.message_handler(state=EditProduct.about)
async def edit_about_product(message: types.Message, state: FSMContext):
    error = False
    async with state.proxy() as data:
        if len(message.text) < 800:
            data_product = await db_shop_furniture.get_product(int(data['id_']))
            data['name'] = data_product[1]
            data['id_'] = int(data['id_'])
            data['price'] = int(data_product[4])
            data['about'] = message.text
            data['count'] = int(data_product[5])
            data['image'] = data_product[2]
        else:
            error = True
    if error:
        await message.answer('Описание превышает 800 символов!')
    else:
        await db_shop_furniture.update_product(state)
        await message.answer('Описание обнавленно', reply_markup=await keyboard_panel.admin_panel())
        await state.finish()


@dp.message_handler(state=EditProduct.price)
async def edit_price_product(message: types.Message, state: FSMContext):
    error = False
    async with state.proxy() as data:
        try:
            data_product = await db_shop_furniture.get_product(int(data['id_']))
            data['name'] = data_product[1]
            data['id_'] = int(data['id_'])
            data['price'] = int(message.text)
            data['about'] = data_product[3]
            data['count'] = int(data_product[5])
            data['image'] = data_product[2]
        except ValueError:
            error = True
    if error:
        await message.answer('Укажите цену товара используя только цифры и без пробелов!')
    else:
        await db_shop_furniture.update_product(state)
        await message.answer('Цена обнавленна', reply_markup=await keyboard_panel.admin_panel())
        await state.finish()


@dp.message_handler(state=EditProduct.count)
async def edit_count_product(message: types.Message, state: FSMContext):
    error = False
    async with state.proxy() as data:
        try:
            data_product = await db_shop_furniture.get_product(int(data['id_']))
            data['name'] = data_product[1]
            data['id_'] = int(data['id_'])
            data['price'] = int(data_product[4])
            data['about'] = data_product[3]
            data['count'] = int(message.text)
            data['image'] = data_product[2]
        except ValueError:
            error = True
    if error:
        await message.answer('Укажите количество товара используя только цифры и без пробелов!')
    else:
        await db_shop_furniture.update_product(state)
        await message.answer('Наличие обнавленно', reply_markup=await keyboard_panel.admin_panel())
        await state.finish()


@dp.message_handler(content_types=['photo'], state=EditProduct.image)
async def edit_photo_product(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data_product = await db_shop_furniture.get_product(int(data['id_']))
        data['name'] = data_product[1]
        data['id_'] = int(data['id_'])
        data['price'] = int(data_product[4])
        data['about'] = data_product[3]
        data['count'] = int(data_product[5])
        data['image'] = message.photo[0].file_id
        await message.photo[-1].download(destination_file=f'photo/{message.photo[0].file_id}.jpg')
    await db_shop_furniture.update_product(state)
    await message.answer('Фотография обнавленна', reply_markup=await keyboard_panel.admin_panel())
    await state.finish()


# Каталоги
@dp.message_handler(text='Каталоги')
async def catalog_list(message: types.Message):
    admin = False
    if not bool(len([item for item in await db_shop_furniture.get_admins() if item[0] == int(message.from_id)])):
        markup_shop = keyboard.shop_panel()
    else:
        markup_shop = await keyboard_panel.admin_panel()
        admin = True
    catalogs = await db_shop_furniture.get_catalogs()
    if bool(len(catalogs)):
        if admin:
            for catalog_item in catalogs:
                catalog_panel = keyboard.catalog_panel_edit(catalog_item[0])
                await bot.send_message(message.chat.id, text=catalog_item[1],
                                       reply_markup=catalog_panel)
        else:
            await message.answer('Все доступные каталоги:',
                                 reply_markup=await keyboard_panel.inline_catalogs_panel())
    else:
        await message.answer('Каталогов пока что нет', reply_markup=markup_shop)


@dp.message_handler(state=EditCatalog.name)
async def edit_name_catalog(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await db_shop_furniture.update_catalog(state)
    await message.answer('Название обнавленно', reply_markup=await keyboard_panel.admin_panel())
    await state.finish()


# Создание каталога
@dp.message_handler(text='Создать каталог')
async def creat_catalog(message: types.Message):
    if await keyboard_panel.check_admin(int(message.from_user.id)):
        await OrderCatalog.name.set()
        keyboard_to_delete = types.ReplyKeyboardRemove()

        await message.answer('Создание каталога:',
                             reply_markup=keyboard_to_delete)
        await message.answer('Напишите название каталога',
                             reply_markup=keyboard.cancel_panel())


@dp.message_handler(state=OrderCatalog.name)
async def add_catalog(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await db_shop_furniture.add_catalog(state)
    await message.answer('Каталог создан', reply_markup=await keyboard_panel.admin_panel())
    await state.finish()


# Создание товара
@dp.message_handler(text='Создать товар')
async def creat_product(message: types.Message):
    if await keyboard_panel.check_admin(int(message.from_user.id)):
        await OrderProduct.name.set()
        keyboard_to_delete = types.ReplyKeyboardRemove()

        await message.answer('Создание товара:',
                             reply_markup=keyboard_to_delete)
        await message.answer('Напишите название товара',
                             reply_markup=keyboard.cancel_panel())


@dp.message_handler(state=OrderProduct.name)
async def product_name(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['name'] = message.text
    await message.answer('Укажите цену товара',
                         reply_markup=keyboard.cancel_panel())
    await OrderProduct.next()


@dp.message_handler(state=OrderProduct.price)
async def product_price(message: types.Message, state: FSMContext):
    error = False
    async with state.proxy() as data:
        try:
            data['price'] = int(message.text)
        except ValueError:
            error = True
    if error:
        await message.answer('Укажите цену товара используя только цифры и без пробелов!',
                             reply_markup=keyboard.cancel_panel())
    else:
        await message.answer('Напишите описание товара не более 800 символов',
                             reply_markup=keyboard.cancel_panel())
        await OrderProduct.next()


@dp.message_handler(state=OrderProduct.about)
async def product_price(message: types.Message, state: FSMContext):
    error = False
    async with state.proxy() as data:
        if len(message.text) < 800:
            data['about'] = message.text
        else:
            error = True
    if error:
        await message.answer('Описание превышает 800 символов!',
                             reply_markup=keyboard.cancel_panel())
    else:
        await message.answer('Укажите количество товара',
                             reply_markup=keyboard.cancel_panel())
        await OrderProduct.next()


@dp.message_handler(state=OrderProduct.count)
async def product_count(message: types.Message, state: FSMContext):
    error = False
    async with state.proxy() as data:
        try:
            data['count'] = int(message.text)
        except ValueError:
            error = True
    if error:
        await message.answer('Укажите количество товара используя только цифры и без пробелов!',
                         reply_markup=keyboard.cancel_panel())
    else:
        await message.answer('Отправьте фотографию товара',
                         reply_markup=keyboard.cancel_panel())
        await OrderProduct.next()


@dp.message_handler(lambda message: not message.photo, state=[OrderProduct.image, EditProduct.image])
async def add_item_photo_check(message: types.Message):
    await message.answer('Это не фотография!')


@dp.message_handler(content_types=['photo'], state=OrderProduct.image)
async def add_item_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['image'] = message.photo[0].file_id
        await message.photo[-1].download(destination_file=f'photo/{message.photo[0].file_id}.jpg')
    await message.answer('Выберите каталог для товара', reply_markup=await keyboard_panel.inline_catalog_panel())
    await OrderProduct.next()


@dp.callback_query_handler(state=OrderProduct.catalog)
async def catalog_handler(query: types.CallbackQuery, state: FSMContext):
    id_product = await db_shop_furniture.add_product(state)
    id_catalog = await db_shop_furniture.get_catalog(query.data)
    await db_shop_furniture.add_product_into_catalog(int(id_catalog), int(id_product))
    await query.message.answer('Товар создан', reply_markup=await keyboard_panel.admin_panel())
    await state.finish()


@dp.message_handler(state=Order.phone_number)
async def order_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['phone_number'] = message.text
    await message.answer('Напишите аддрес доставки',
                         reply_markup=keyboard.cancel_panel())
    await Order.next()


@dp.message_handler(state=Order.address)
async def order_phone_number(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['address'] = message.text
    await message.answer('Укажите количество товара используя только цифры и без пробелов!\n'
                         'Количество не должно превышать количества доступного товара!',
                         reply_markup=keyboard.cancel_panel())
    await Order.next()


@dp.message_handler(state=Order.count_product)
async def order_count_product(message: types.Message, state: FSMContext):
    error = False
    message_admins = ''
    async with state.proxy() as data:
        try:
            print((await db_shop_furniture.get_product(data['id_product']))[5], int(message.text))
            if (await db_shop_furniture.get_product(data['id_product']))[5] >= int(message.text):
                data['count_product'] = int(message.text)
                id_product = data['id_product']
                product_item = await db_shop_furniture.get_product(id_product)
                message_admins = (f'ЗАКАЗ!\n'
                                  f'Название: {product_item[1]}\n'
                                  f'Описание:\n{product_item[3]}\n'
                                  f'Цена: {product_item[4]} р\n'
                                  f'О заказе:\n'
                                  f'Контактный телефон: {data["phone_number"]}\n'
                                  f'Адресс доставки: {data["address"]}\n'
                                  f'Количество требуемого товара: {data["count_product"]}')
                await db_shop_furniture.update_count_product(product_item[0],
                                                             int(product_item[5]) - int(data['count_product']))
            else:
                error = True
        except ValueError:
            error = True
    if error:
        await message.answer('Укажите количество товара используя только цифры и без пробелов!\n'
                             'Количество не должно превышать количества доступного товара!')
    else:
        await db_shop_furniture.add_orders(state)
        for tg_id in await db_shop_furniture.get_admins():
            await bot.send_message(chat_id=tg_id[0], text=message_admins)
        await message.answer('Заказ оформлен', reply_markup=keyboard.shop_panel())
        await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
