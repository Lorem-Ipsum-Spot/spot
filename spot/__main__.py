from spot_sdk import SpotCameraClient

if __name__ == "__main__":
    from spot.cli import main

    main()

def connect():
    # Inicializace klienta (předpokládané metody)
    client = SpotCameraClient(username='user', password='password', robot_ip='192.168.50.3')

    # Připojení k robotu
    client.connect()
    