import random
 
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message
 
# Вместо BOT TOKEN HERE нужно вставить токен вашего бота,
# полученный у @BotFather
BOT_TOKEN = ''
 
# Создаем объекты бота и диспетчера
bot = Bot(BOT_TOKEN)
dp = Dispatcher()
 
# Количество попыток, доступных пользователю в игре
ATTEMPTS = 5
word_list = ['год', 'человек', 'время', 'дело', 'жизнь', 'день', 'рука', 'раз', 'работа', 'слово', 'место', 'лицо', 'друг', 'глаз', 'вопрос', 'дом', 'сторона', 'страна', 'мир', 'случай', 'голова', 'ребенок', 'сила', 'конец']
 
# Словарь, в котором будут храниться данные пользователя
users = {}
 
# Функция возвращающая случайное целое число от 1 до 100
def get_random_number() -> str:
    return random.choice(word_list)
 
# Этот хэндлер будет срабатывать на команду "/start"
@dp.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(
        'Привет!\nДавайте сыграем в игру "Угадай число"?\n\n'
        'Чтобы получить правила игры и список доступных '
        'команд - отправьте команду /help'
    )
    # Если пользователь только запустил бота и его нет в словаре '
    # 'users - добавляем его в словарь
    if message.from_user.id not in users:
        users[message.from_user.id] = {
            'in_game': False,
            'secret_number': None,
            'attempts': None,
            'total_games': 0,
            'wins': 0
            'res': ''
        }
 
# Этот хэндлер будет срабатывать на команду "/help"
@dp.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(
        f'Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ вас есть {ATTEMPTS} '
        f'попыток\n\nДоступные команды:\n/help - правила '
        f'игры и список команд\n/cancel - выйти из игры\n'
        f'/stat - посмотреть статистику\n\nДавай сыграем?'
    )
 
# Этот хэндлер будет срабатывать на команду "/stat"
@dp.message(Command(commands='stat'))
async def process_stat_command(message: Message):
    await message.answer(
        f'Всего игр сыграно: '
        f'{users[message.from_user.id]["total_games"]}\n'
        f'Игр выиграно: {users[message.from_user.id]["wins"]}'
    )
 
# Этот хэндлер будет срабатывать на команду "/cancel"
@dp.message(Command(commands='cancel'))
async def process_cancel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снова - напишите об этом'
        )
    else:
        await message.answer(
            'А мы и так с вами не играем. '
            'Может, сыграем разок?'
        )
 
# Этот хэндлер будет срабатывать на согласие пользователя сыграть в игру
@dp.message(F.text.lower().in_(['да', 'давай', 'сыграем', 'игра',
                                'играть', 'хочу играть']))
async def process_positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        users[message.from_user.id]['attempts'] = ATTEMPTS
        await message.answer(
            'Ура!\n\nЯ загадал число от 1 до 100, '
            'попробуй угадать!'
        )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat'
        )
 
# Этот хэндлер будет срабатывать на отказ пользователя сыграть в игру
@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def process_negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(
            'Жаль :(\n\nЕсли захотите поиграть - просто '
            'напишите об этом'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )
 
# Этот хэндлер будет срабатывать на отправку пользователем чисел от 1 до 100
@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def process_numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if not message.text.isalpha():
            await message.answer('Ошибка нужно ввести букву')
        if len(message.text) != 1:
            await message.answer('Ошибка, нужно ввести только одну букву')
          
        if message.text in users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['res'] = ''.join(users[message.from_user.id]['secret_number'][i] if message.text == users[message.from_user.id]['secret_number'][i] or users[message.from_user.id]['res'].isalpha() else '*' for i in (range(len(users[message.from_user.id]['secret_number']))))
            await message.answer(f'Вот результат: {users[message.from_user.id]['res'].upper()}')
 
        elif message.text not in users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['attempts'] -= 1
            await message.answer(f'Такой буквы нет. У вас осталось {users[message.from_user.id]['attempts']} попыток')
     
 
        if users[message.from_user.id]['secret_number'] = users[message.from_user.id]['res']:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            await message.answer(
                f'Поздравляю Вы угадали слово {users[message.from_user.id]['secret_number']}'
                f'И у вас осталось {users[message.from_user.id]['attempts']} попыток. '
                f'\n\nДавайте сыграем еще?'
            )
        
        if users[message.from_user.id]['attempts'] == 0:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            await message.answer(
                f'К сожалению, у вас больше не осталось '
                f'попыток. Вы проиграли :(\n\nСлово '
                f'было {users[message.from_user.id]["secret_number"]}'
                f'\n\nДавайте сыграем еще?'
            )
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')
 
# Этот хэндлер будет срабатывать на остальные любые сообщения
@dp.message()
async def process_other_answers(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer(
            'Мы же сейчас с вами играем. '
            'Присылайте, пожалуйста, числа от 1 до 100'
        )
    else:
        await message.answer(
            'Я довольно ограниченный бот, давайте '
            'просто сыграем в игру?'
        )
 
if __name__ == '__main__':
    dp.run_polling(bot)
