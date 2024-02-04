from multiprocessing import Manager
from db_queries import add_user_variant

DONE = -1

class Request:
    def __init__(self, user_telegram_id: str, variant_id: str):
        self.user_telegram_id = user_telegram_id
        self.variant_id = variant_id

    def process(self):
        add_user_variant(user_telegram_id, variant_id)


class RequestQueue:
    def __init__(self):
        self._queue = Manager().Queue()
        self._is_finished = False

    def put(self, request: Request):
        self._queue.put(request)

    def start_polling(self):
        while not self._is_finished:
            request = self._queue.get()
            if request == DONE:
                return
            request.process()            

    def stop(self):
        self._is_finished = True
        self._queue.put(DONE)
