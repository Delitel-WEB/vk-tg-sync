from sync.tg import execute
import multiprocessing



if __name__ == "__main__":
    tgBot = multiprocessing.Process(target=execute)
    tgBot.start()
    tgBot.join()