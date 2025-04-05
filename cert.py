from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import Name, NameAttribute, CertificateBuilder
from cryptography.x509.oid import NameOID
import datetime

def gen_cert():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    subject = issuer = Name([
        NameAttribute(NameOID.COUNTRY_NAME, "DE"),
        NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "SomeState"),
        NameAttribute(NameOID.LOCALITY_NAME, "SomeCity"),
        NameAttribute(NameOID.ORGANIZATION_NAME, "MyOrganization"),
        NameAttribute(NameOID.COMMON_NAME, "localhost")
    ])
    cert_builder = CertificateBuilder()
    cert_builder = cert_builder.subject_name(subject)
    cert_builder = cert_builder.issuer_name(issuer)
    cert_builder = cert_builder.not_valid_before(datetime.datetime.utcnow())
    cert_builder = cert_builder.not_valid_after(datetime.datetime.utcnow() + datetime.timedelta(days=365))
    cert_builder = cert_builder.public_key(private_key.public_key())
    cert_builder = cert_builder.serial_number(1000)
    cert = cert_builder.sign(private_key, hashes.SHA256(), default_backend())

    with open("key.pem", "wb") as key_file:
        key_file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ))

    with open("cert.pem", "wb") as cert_file:
        cert_file.write(cert.public_bytes(serialization.Encoding.PEM))

    print("passt")

if __name__ == "__main__":
    gen_cert()