import requests
from http import HTTPStatus
from src.utils.api_modules import BaseApiClass
from schemas import UserDocument


class UserDocumentsModule(BaseApiClass):

    URL_USER_DOCS = "/user_documents"

    def get_user_documents(self) -> list[UserDocument]:
        self.authorization()
        url = f"/{self.URL_USER_DOCS}"
        r = requests.get(
            url=self.host + url,
            headers={'Authorization': f'Bearer {self.access_token}'})

        if r.status_code == HTTPStatus.OK:
            user_documents = []
            for document in r.json():
                user_documents.append(
                    UserDocument(
                        id=document['id'],
                        owner=document['owner'],
                        title=document['title'],
                    ))
            return user_documents
        self.raise_exception_if_received_not_expected_status_code(r)

    def create_user_document(self, title: str, file: bytes, owner: int) -> UserDocument:
        self.authorization()
        url = f"/{self.URL_USER_DOCS}"
        r = requests.post(
            url=self.host + url,
            headers={'Authorization': f'Bearer {self.access_token}'},
            json={
                "file": file,
                "owner": owner,
                "title": title
            })

        if r.status_code == HTTPStatus.CREATED:
            r = r.json()
            return UserDocument(id=r['id'],
                                owner=r['owner'],
                                title=r['title'])
        self.raise_exception_if_received_not_expected_status_code(r)

    def delete_document_user(self, id_document: str or int):
        self.authorization()
        headers = {
            'Authorization': f'Bearer {self.access_token}'
        }
        end_point = f"{self.URL_USER_DOCS}/{id_document}"
        requests.delete(url=self.host + end_point, headers=headers)

    def update_document_user(self, id_document: int , new_title: str):
        self.authorization()
        url = f"/{self.URL_USER_DOCS}"
        r = requests.put(
            url=self.host + url,
            headers={'Authorization': f'Bearer {self.access_token}'},
            json={
                "id": id_document,
                "title": new_title
            })

        if r.status_code == HTTPStatus.CREATED:
            r = r.json()
            return UserDocument(id=r['id'],
                                owner=r['owner'],
                                title=r['title'])
        self.raise_exception_if_received_not_expected_status_code(r)
