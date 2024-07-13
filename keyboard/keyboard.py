import asyncio

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def shop_panel():
    panel = ReplyKeyboardMarkup(resize_keyboard=True)
    panel.add('Товары')
    panel.add('Каталоги')
    return panel


def cancel_panel():
    panel = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    panel.add(InlineKeyboardButton('Отмена', callback_data='cancel'))
    return panel


def product_panel_admin(id_product):
    panel = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    panel.add(InlineKeyboardButton('Удалить', callback_data=f'delete_product;{id_product}'))
    panel.add(InlineKeyboardButton('Редактировать', callback_data=f'edit_product;{id_product}'))
    return panel


def product_panel(id_product):
    panel = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    panel.add(InlineKeyboardButton('Купить', callback_data=f'order_product;{id_product}'))
    return panel


def product_panel_edit(id_product):
    panel = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    panel.add(InlineKeyboardButton('Фотография', callback_data=f'image_product;{id_product}'))
    panel.add(InlineKeyboardButton('Название', callback_data=f'name_product;{id_product}'))
    panel.add(InlineKeyboardButton('Описание', callback_data=f'about_product;{id_product}'))
    panel.add(InlineKeyboardButton('Цена', callback_data=f'price_product;{id_product}'))
    panel.add(InlineKeyboardButton('Наличие', callback_data=f'count_product;{id_product}'))
    return panel


def catalog_panel_edit(id_catalog):
    panel = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
    panel.add(InlineKeyboardButton('Удалить', callback_data=f'delete_catalog;{id_catalog}'))
    panel.add(InlineKeyboardButton('Переименовать', callback_data=f'name_catalog;{id_catalog}'))
    return panel


class Panel:
    def __init__(self, db):
        self.db = db

    async def admin_panel(self):
        panel = ReplyKeyboardMarkup(resize_keyboard=True)
        if not bool(len(await self.db.get_catalogs())):
            panel.add('Создать каталог')
        else:
            if bool(len(await self.db.get_products())):
                panel.add('Товары')
            if bool(len(await self.db.get_orders())):
                panel.add('Заказы')
            panel.add('Каталоги')
            panel.add('Создать каталог')
            panel.add('Создать товар')
        return panel

    async def check_admin(self, tg_id: int):
        return bool(len([item for item in await self.db.get_admins() if item[0] == tg_id]))

    async def catalog_panel(self):
        catalog_panel = ReplyKeyboardMarkup(resize_keyboard=True)
        for item in await self.db.get_catalogs():
            catalog_panel.add(item[1])
        return catalog_panel

    async def inline_catalog_panel(self):
        catalog_panel = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
        for item in await self.db.get_catalogs():
            catalog_panel.add(InlineKeyboardButton(item[1], callback_data=item[0]))
        return catalog_panel

    async def inline_catalogs_panel(self):
        catalog_panel = InlineKeyboardMarkup(resize_keyboard=True, row_width=2)
        for item in await self.db.get_catalogs():
            catalog_panel.add(InlineKeyboardButton(item[1], callback_data=f'product_list;{item[0]}'))
        return catalog_panel



