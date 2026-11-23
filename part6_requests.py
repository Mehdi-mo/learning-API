import requests

response = requests.get(
    url = 'https://api.github.com//users/this-user-does-not-exist-12345',

                        )


print(response.status_code)

response.raise_for_status()

# data = response.json()

# # print('created_at' in list(data.keys()))
# print(data['created_at'])
