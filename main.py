import os


WG_PATH = '/etc/wireguard/'
SERVER_IP = ''
SERVER_PORT = '51820'

def init():
    """Проверяет наличие файлов freeIP wg-server.cfg и создает их при необходимости"""
    checkFilesAvailability(WG_PATH+'freeIP')
    validateConfig(WG_PATH+'wg-server.cfg')
    pass


def checkFilesAvailability(files):
    """Ищет файлы по указанному пути и возвращает False, если хотя бы один не найден"""
    pass


def validateConfig(path):
    """Проверяет данные в конфиге"""
    #TODO: сделать автоматическое создание конфига при его отсутствии
    pass


def createUserKeys(username) -> (str, str):
    """Создает пару ключей для пользователя и возвращает их в виде кортежа (userPrivateKey, userPublicKey)"""

    os.system('wg genkey | tee /etc/wireguard/{username}_privatekey | wg pubkey | tee /etc/wireguard/{username}_publickey'.format(username=username))
    
    with open ('/etc/wireguard/{}_publickey'.format(username), 'r') as f:
        userPublicKey = f.read().rstrip('\n')

    with open ('/etc/wireguard/{}_privatekey'.format(username), 'r') as f:
        userPrivateKey = f.read().rstrip('\n')
    
    return (userPrivateKey, userPublicKey)


def getIP() -> str:
    """Возвращает последнюю часть IP из файла freeIP и увеличивает число на 1"""

    with open ('/etc/wireguard/freeIP', 'r') as f:
        userIP = f.read().rstrip('\n')

    with open ('/etc/wireguard/freeIP', 'w') as f:
        f.write(str(int(userIP)+1))

    return userIP


def addUser(username, userPublicKey, userIP):
    """Добавляет пользователя в wg0.conf"""

    with open('./templates/peer-template', 'r') as f:
        peer = f.read().rstrip('\n')

    tmp = ('<username>', '<userPublicKey>', '<userIP>')
    data = (username, userPublicKey, userIP)

    for old, new in zip(tmp, data):
        peer = peer.replace(old, new)

    with open(WG_PATH+'wg0.conf', 'a') as f:
        f.write(peer)


def genUserConfig(username, userPrivateKey, userIP):
    """Создает конфигурационный файл для клиента"""

    with open('./templates/user-conf-template', 'r') as f:
        userConfig = f.read().rstrip('\n')

    with open(WG_PATH+'public.key', 'r') as f:
        serverPublicKey = f.read().rstrip('\n')

    tmp = ('<userPrivateKey>', '<userIP>', '<serverPublicKey>', '<serverIP>', '<serverPort>')
    data = (userPrivateKey, userIP, serverPublicKey, SERVER_IP, SERVER_PORT)

    for old, new in zip(tmp, data):
        userConfig = userConfig.replace(old, new)

    with open('./wg-client-config-{}'.format(username), 'w') as f:
        f.write(userConfig)


def main():
    #init()
    users = input("Enter names for users via space: \n").split()
    for username in users:
        userPrivateKey, userPublicKey = createUserKeys(username)
        userIP = getIP()
        addUser(username, userPublicKey, userIP)
        genUserConfig(username, userPrivateKey, userIP)


if __name__ == "__main__":
    main()
