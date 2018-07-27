import requests
import json

def JSON_settings():
    with open("settings.json", "r") as f:
        f = f.read()
    settings = json.loads(f)
    
    token = settings["token"]
    ran = settings["range"]
    id = settings["id"]
    return token, ran, id

def vk_API(func):
	def wrapper(method, arguments, *token):
		new_method = method + "?"
		for arg in arguments:
			new_method = new_method + arg + "&"
		func(new_method, *token)
	return wrapper

@vk_API
def vk_request(new_method, token):
    request = "https://api.vk.com/method/" + new_method + "access_token=" + token + "&v=5.80"
    print(request)
    s = requests.get(request)
    global data
    data = s.json()
    
if __name__ == "__main__":
    
    token, ran, id = JSON_settings()
    owner_id = "owner_id=" + str(id)

    vk_request("wall.get", [owner_id, "count=100"], token)
    count = data["response"]["count"]
    
    print("На стене обнаружено: ", count, " записей")
    print("Будет удалены записи, начиная от: ", ran)
    print('')
    
    a = data["response"]["items"]

    for post in range(ran, count):
        post_id = "post_id=" + str(a[post]["id"])
        vk_request("wall.delete", [owner_id, post_id], token)
        
    post_id = "post_id=" + str(a[0]["id"])
    vk_request("wall.delete", [owner_id, post_id], token)
    print("Записи удалены")
    
    input("Enter для выхода")