import googlemaps
from threading import Lock

class GoogleMapsClient:
    _instance = None
    _lock = Lock()

    API_KEY = ''

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.client = googlemaps.Client(key=cls.API_KEY)
        return cls._instance

    def get_client(self):
        return self.client

    def get_api_key(self):
        return self.API_KEY

