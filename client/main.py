import requests
from urllib.parse import urljoin


class Client:
    def __init__(self, username, password) -> None:
        self.url = "http://127.0.0.1:5000/"
        self.username = username
        self.password = password
        self.token = ""
        self.header = {"x-access-token": ""}

    def get_token(self):
        myjson = requests.get(
            urljoin(self.url, "login"), auth=(self.username, self.password)
        ).json()
        self.token = myjson["token"]
        self.header["x-access-token"] = self.token
        return print("token: " + self.token)

    def all_todo(self):
        return print(
            requests.get(urljoin(self.url, "todo"), headers=self.header).json()
        )

    def post_todo(self, task_name):
        print(
            requests.post(
                urljoin(self.url, "todo"), headers=self.header, data={"text": task_name}
            ).json()
        )

    def delete_task(self, task_id):
        return print(
            requests.delete(
                urljoin(urljoin(self.url, "/todo/"), str(task_id)), headers=self.header
            ).json()
        )

    def put_task(self, task_id):
        return print(
            requests.put(
                urljoin(urljoin(self.url, "/todo/"), str(task_id)), headers=self.header
            ).json()
        )


c = Client("Boba", "12345")
c.get_token()
c.all_todo()
c.delete_task(101)
c.put_task(101)
c.post_todo("do api client")
c.all_todo()
c.put_task(2)
c.all_todo()
c.delete_task(2)
c.all_todo()
