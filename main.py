from sync.tg import execute
import multiprocessing


if __name__ == "__main__":
    tgBot = multiprocessing.Process(target=execute)
    tgBot.start()
    try:
        tgBot.join()
    except (KeyboardInterrupt, SystemExit):
        print("\rОтключаем ботов! До свидания!")
        tgBot.kill()