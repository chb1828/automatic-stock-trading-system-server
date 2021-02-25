from django.apps import AppConfig

class ClientSocketConfig(AppConfig):
    name = 'client_socket'
    
    def ready(self):
        import client_socket.signal
