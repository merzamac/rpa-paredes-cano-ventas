from loguru import logger
from getpass import getpass
from keyring import get_credential, set_password
from keyring.credentials import Credential


class CredentialManager:
    @classmethod
    def get_credential(cls, service_name: str) -> Credential:
        while not (credentials := get_credential(service_name, None)):
            creds: dict[str, str] = cls.get_data(service_name)
            set_password(
                service_name=service_name,
                username=creds["username"],
                password=creds["password"],
            )
        return credentials

    @classmethod
    def get_data(cls, service_name: str) -> dict[str, str]:
        print(f"|------------Enter your {service_name} credentials------------|")
        print("|for token use 'token' as username and your token as password|")
        username = input(f"Enter your username: ").strip()
        password = getpass(f"Enter your password: ")
        return {"username": username, "password": password}
