import datetime
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_key():
    """Generates a private key (RSA 2048)."""
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

def write_key_to_file(key, filename):
    """Writes a private key to a file."""
    with open(filename, "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption(),
        ))

def write_cert_to_file(cert, filename):
    """Writes a certificate to a file."""
    with open(filename, "wb") as f:
        f.write(cert.public_bytes(serialization.Encoding.PEM))

def generate_ca():
    """Generates a self-signed CA certificate and key."""
    print("Generating CA...")
    key = generate_key()
    
    subject = issuer = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Custom CA"),
        x509.NameAttribute(NameOID.COMMON_NAME, u"MyRootCA"),
    ])
    
    cert = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        issuer
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc)
    ).not_valid_after(
        # Valid for 1 year
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
    ).add_extension(
        x509.BasicConstraints(ca=True, path_length=None), critical=True,
    ).sign(key, hashes.SHA256())

    write_key_to_file(key, "ca.key")
    write_cert_to_file(cert, "ca.pem")
    return key, cert

def generate_signed_cert(ca_key, ca_cert, common_name, filename_base, is_server=False):
    """Generates a certificate signed by the CA."""
    print(f"Generating {filename_base} certificate...")
    key = generate_key()
    
    subject = x509.Name([
        x509.NameAttribute(NameOID.COUNTRY_NAME, u"US"),
        x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, u"California"),
        x509.NameAttribute(NameOID.ORGANIZATION_NAME, u"My Company"),
        x509.NameAttribute(NameOID.COMMON_NAME, common_name),
    ])

    builder = x509.CertificateBuilder().subject_name(
        subject
    ).issuer_name(
        ca_cert.subject
    ).public_key(
        key.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.datetime.now(datetime.timezone.utc)
    ).not_valid_after(
        datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365)
    )

    if is_server:
        # Important for Server: Add Subject Alternative Name (SAN) for localhost
        builder = builder.add_extension(
            x509.SubjectAlternativeName([
                x509.DNSName(u"localhost"),
                x509.DNSName(u"127.0.0.1"),
            ]),
            critical=False,
        )

    # Sign the certificate with the CA's private key
    cert = builder.sign(ca_key, hashes.SHA256())

    write_key_to_file(key, f"{filename_base}.key")
    write_cert_to_file(cert, f"{filename_base}.pem")

if __name__ == "__main__":
    # 1. Create the Certificate Authority
    ca_key, ca_cert = generate_ca()

    # 2. Create the Server Certificate (signed by CA)
    generate_signed_cert(ca_key, ca_cert, u"localhost", "server", is_server=True)

    # 3. Create the Client Certificate (signed by CA)
    generate_signed_cert(ca_key, ca_cert, u"MyClientUser", "client", is_server=False)

    print("\n--- Success! ---")
    print("Generated: ca.key, ca.pem")
    print("Generated: server.key, server.pem")
    print("Generated: client.key, client.pem")