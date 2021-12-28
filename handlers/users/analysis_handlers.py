from aiogram.dispatcher.storage import FSMContext
from aiogram.types import Message

from keyboards.default import menu, back_to_menu, analysis_menu
from utils.misc.prepare_data_for_analsis import prepare_data
from loader import dp
from data.config import BASE_DIR, db
from states.first_adding_url import FirstURL

changing_url_info = 'Чтобы проанализировать конкурентов, нужно отправить'
changing_url_info += ' сюда URL booking.com сообщением. Для этого' 
changing_url_info += ' войдите на сайт booking.com, выберите все'
changing_url_info += ' соответсвующие поиску ваших конкурентов фильтры,'
changing_url_info += ' которые можно видеть на фото в жёлтом окне'
changing_url_info += ' "Найти" и под ним, и после загрузки страницы'
changing_url_info += ' выделите весь URL-адрес как показано на фото,'
changing_url_info += ' скопируйте и отправьте его сюда.' 


@dp.message_handler(text="♻️Обновить URL")
async def update_url(message: Message) -> None:
    photo_path = BASE_DIR / "data/booking_screen.png"
    with photo_path.open("rb") as photo:
            await message.answer_photo(photo=photo,
                                       caption=changing_url_info,
                                       reply_markup=back_to_menu)
        
    await FirstURL.first()


@dp.message_handler(text="🏨Проанализировать конкурентов")
async def analyse_booking(message: Message, state: FSMContext) -> None:
    url = db.get_entry("users", "tg_id", message.from_user.id)[2]
    if url != None:
        info_with_URL = 'Чтобы проанализировать конкурентов,'
        info_with_URL += ' можно добавить новый URL или использовать'
        info_with_URL += ' ранее добавленный'
        await message.answer(text=info_with_URL, reply_markup=analysis_menu)
        await state.update_data({"url": url})
    else:
        await update_url(message)


@dp.message_handler(text="✅Использовать старый URL")
async def analyse_exisiting_url(message: Message, state: FSMContext):
    data = await state.get_data()
    url = data.get("url")
    info = prepare_data(url)

    await message.answer(text=info, reply_markup=menu)
    await state.finish()


@dp.message_handler(state=FirstURL.sending_URL)
async def take_url(message: Message, state: FSMContext) -> None:
    url = message.text
    db.update_user_url(message.from_user.id, url)
    info = prepare_data(url)

    await message.answer(text=info, reply_markup=menu)
    await state.finish()
