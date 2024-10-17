"""the main file which runs the app"""

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
#without this part, we lose the ability to run the app either from the terminal or from the file.

import asyncio
import logging
from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, PollAnswer, Poll
from config import settings
import const
from schemas import OptionsTest, GettedTests
from typing import List
from cache_utils import initcache, EngCache
from api_interact import get_test, update_test
from error_handlers import global_error_handler_async, global_error_handler_sync


class EnGram():

    def __init__(self, token):
        self.dp = Dispatcher()
        self.bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
        self.handlers()
        self.keyboard_level = LevelButtuns()  #create levels keyboard
        self.keyboard_nextchange = CreateNewTestButtons()  #create Next and Cange Level buttons
        redis = initcache()    
        self.engcache = EngCache(redis)  #init redis cache in order to save a user's level


    def handlers(self):
        @self.dp.message(CommandStart())
        @global_error_handler_async
        async def command_start_handler(message: Message) -> None:
            """
            This handler receives messages with `/start` command
            We send introduction and levels keyboard
            """
            await message.answer(const.IntroTxt.format(html.bold(message.from_user.full_name)))
            await self.bot.send_message(message.from_user.id, text=const.SelectLevel, reply_markup=self.keyboard_level)
            await self.engcache.add_update_to_cache(message.from_user.id, '')  #clear current level


        @self.dp.message()
        @global_error_handler_async
        async def echo_handler(message: Message) -> None:
            """
            Handle all message types (like a text, photo, sticker etc.)
            """
            await self.engcache.add_update_to_cache(message.from_user.id)
            await self.bot.send_message(message.from_user.id, text=const.CanNonUnd, reply_markup=self.keyboard_nextchange)


        @self.dp.poll_answer(lambda poll: True)
        @global_error_handler_async
        async def poll_handler(poll_answer: PollAnswer):
            """
            Handle answer in the test. 
            If user does not exist in the cache we propose to choose a level
            """ 
            user_level = await self.engcache.get_cached_user(poll_answer.user.id)
            if not user_level:
                await self.bot.send_message(poll_answer.user.id, text=const.SelectLevel, reply_markup=self.keyboard_level)
            else:
                await self.bot.send_message(poll_answer.user.id, text=const.ClickNext, reply_markup=self.keyboard_nextchange)
                await self.engcache.add_update_to_cache(poll_answer.user.id)



        @self.dp.callback_query(lambda call: call.data in const.Levels)
        @global_error_handler_async
        async def level_button(call):
            """
            Handle level selections. Send a corresponding test 
            """
            user_level = await self.engcache.add_update_to_cache(call.from_user.id, call.data)
            
            await self.bot.send_message(call.from_user.id, const.WillGenerate.format(level = user_level))
            await self.NextTest(call.from_user.id, user_level)



        @self.dp.callback_query(lambda call: call.data == 'nexttest')
        @global_error_handler_async
        async def next_button(call):
            """
            Handle next button clicking. 
            If user does not exist in the cache we propose to choose a level.
            """
            user_level = await self.engcache.get_cached_user(call.from_user.id)
            if not user_level:
                await self.bot.send_message(call.from_user.id, text=const.SelectLevel, reply_markup=self.keyboard_level)
            else:
                await self.engcache.add_update_to_cache(call.from_user.id)
                await self.NextTest(call.from_user.id, user_level)


        @self.dp.callback_query(lambda call: call.data == 'changelevel')
        @global_error_handler_async
        async def change_level(call):
            """
            Handle change level button clicking
            """
            await self.engcache.add_update_to_cache(call.from_user.id, '') #clear current level
            await self.bot.send_message(call.from_user.id, text=const.NewLevel, reply_markup=self.keyboard_level)


    @global_error_handler_async
    async def start(self) -> None:
        """Initialize the Bot instance with default bot properties which will be passed to all API calls
            And the run events dispatching"""
        
        await self.dp.start_polling(self.bot)



    @global_error_handler_async
    async def NextTest(self, chat_id, level):

        """Create a test when clicking Next"""

        response = await get_test(level)
        if isinstance(response, dict):
            thetest = GettedTests(**response)
            await CreateTest(thetest.Question, 
                            thetest.Options, 
                            thetest.correct_option_id, 
                            thetest.explanation,
                            self.bot, 
                            chat_id)
            await update_test(level, thetest.ID)
        elif isinstance(response, str):  #tests were not found and the API returns str message
            await self.bot.send_message(chat_id, text=const.NoTestsAnswer, reply_markup=self.keyboard_level)



@global_error_handler_sync
def LevelButtuns():

    """Create levels keyboard"""

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    for i in const.Levels:
        button = InlineKeyboardButton(text = const.Levels[i], callback_data=i)
        keyboard.inline_keyboard.append([button])
    return keyboard


@global_error_handler_async
async def CreateTest(question, options: List[OptionsTest], correct_option_id, explanation, bot: Bot, id):  
    
    """Building a test"""

    PollOptionsList = [o.option_text for o in options]
    await bot.send_poll(chat_id=id,
                type='quiz',
                is_closed=False,
                question=question, 
                options=PollOptionsList,
                correct_option_id = correct_option_id - 1,
                is_anonymous=False,
                allows_multiple_answers=False,
                explanation = explanation)

    
@global_error_handler_sync
def CreateNewTestButtons():

    """Creation of Next and Change Level buttons"""

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])
    buttonNext = InlineKeyboardButton(text = const.NextButton, callback_data='nexttest')
    buttonChangeLevel = InlineKeyboardButton(text = const.ChangeLevelButton, callback_data='changelevel')
    keyboard.inline_keyboard.append([buttonNext, buttonChangeLevel])
    return keyboard



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    bot = EnGram(settings.BOT_TOKEN)
    asyncio.run(bot.start())