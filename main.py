from sync.tg import start_tg
from sync.vk import start_vk
import multiprocessing


if __name__ == "__main__":
    tgBot = multiprocessing.Process(target=start_tg)
    vkBot = multiprocessing.Process(target=start_vk)
    tgBot.start()
    vkBot.start()
    try:
        tgBot.join()
        vkBot.join()
    except (KeyboardInterrupt, SystemExit):
        print("\rОтключаем ботов! До свидания!")
        tgBot.kill()
        vkBot.kill()
