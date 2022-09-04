
import requests
from pprint import pprint
from datetime import date
import configparser
import json

config = configparser.ConfigParser()
config.read("vk.ini")
token_vk = config["vk"]["token_vk"]
config.read("ya.ini")
token_ya = config["ya"]["token_ya"]

class Vk:

    def __init__(self, access_token):
        self.token_vk = access_token

    def users(self, id):
        url = "https://api.vk.com/method/users.get/"
        params = {'access_token': f'{self.token_vk}', 'user_ids': id, 'v': '5.131',
                  'extended': 1}
        res = requests.get(url, params=params)
        res = res.json()
        res = res["response"][0]
        user_id = res["id"]
        return user_id

    def uploading_photos(self, user_id, album):
        url = "https://api.vk.com/method/photos.get/"
        params = {'access_token': self.token_vk, 'owner_id': user_id, 'album_id': album, 'photo_sizes': '1',
                  'v': '5.131', 'extended': 1}
        res = requests.get(url, params=params)
        res = res.json()
        res = res["response"]["items"]
        photo_parameters = {}
        for index, photo in enumerate(res):
            if index <= int(limit)-1:
                name_photo = photo["likes"]["count"]
                for size in photo["sizes"]:
                    if size['type'] == 'z':
                        url_photo = size['url']
                    elif size['type'] == 'y':
                        url_photo = size['url']
                    elif size['type'] == 'x':
                        url_photo = size['url']
                    elif size['type'] == 'm':
                        url_photo = size['url']
                    elif size['type'] == 's':
                        url_photo = size['url']
                if name_photo in photo_parameters:
                    date_photo = date.fromtimestamp(photo["date"])
                    name_photo = (f'{photo["likes"]["count"]}_{date_photo}')
                else:
                    name_photo = photo["likes"]["count"]
                photo_parameters[name_photo] = url_photo
        return(photo_parameters)

class YaUploader:
   def __init__(self, token):
       self.token = token
       pass

   def download_file (self):
       upload_url = "https://cloud-api.yandex.net/v1/disk/resources"
       headers = {'Content-Type': 'application/json', 'Accept': 'application/json', 'Authorization': f'OAuth {self.token}'}
       params = {"path":"netology/photos", "overwrite": "True"}
       folder_path = requests.put(upload_url, headers=headers, params=params)
       upload_url_download = "https://cloud-api.yandex.net/v1/disk/resources/upload"
       list_download = {}
       for id, (name_photos, url_foto) in enumerate(list_photo_vk.items(), 1):
           path_download = (f'netology/photos/{name_photos}.png')
           params_download = {"path": path_download, "url": url_foto}
           download = requests.post(upload_url_download, headers=headers, params=params_download)
           if download.status_code == 202:
               print(f"Загружено фото № {id} из {len(list_photo_vk)}")
               download_json = download.json()
               list_download[name_photos] = download_json
           else:
               print (f"Ошибка загрузки, код ошибки {download.status_code}")
       with open("data.txt", 'w', encoding='utf-8') as json_file:
           json.dump(list_download, json_file)
       return pprint(list_download)


if __name__ == '__main__':

    id_screen_name = input("Введите id или screen_name пользователя : ")

    limit = input("Введите количество загружаемых фото : ")
    pprint('''Для служебных альбомов используются следующие идентификаторы:
        wall — фотографии со стены,
        profile — фотографии профиля,
        saved — сохраненные фотографии.
        ''')
    album = input("Введите id альбома либо идентификатор служебного альбома : ")
    user_id = Vk(token_vk)
    user_id_vk = user_id.users(id_screen_name)
    list_photo = Vk(token_vk)
    list_photo_vk = list_photo.uploading_photos(user_id_vk, album)
    download_foto = YaUploader(token_ya)
    result = download_foto.download_file()