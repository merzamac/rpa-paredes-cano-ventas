from rpa_paredes_cano_ventas.utils.credentials import CredentialManager


def test_get_credential():
    aconsys_credentials = CredentialManager.get_credential(
        service_name="Aconsys Plataform"
    )
    import_credentials = CredentialManager.get_credential(
        service_name="Import Plataform"
    )
    recaptcha_credentials = CredentialManager.get_credential(service_name="reCAPTCHA")
