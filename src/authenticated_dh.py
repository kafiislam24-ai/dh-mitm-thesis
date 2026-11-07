"""
Phase 3A: Authenticated Diffie-Hellman using RSA Digital Signatures
Demonstrates:
  1. Normal Authenticated Exchange (Alice <-> Bob): Valid Signatures
  2. MitM Tampering Attempt (Alice <-> Mallory <-> Bob): Attack Detection
"""

from cryptography.hazmat.primitives.asymmetric import dh, rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature

def run_authenticated_dh_demo():
    print("=" * 65)
    print("PHASE 3A: AUTHENTICATED DIFFIE-HELLMAN (RSA-PSS + SHA-256)")
    print("=" * 65)

    # 1. Generate DH Domain Parameters
    print("[*] Generating 2048-bit DH parameters...")
    dh_parameters = dh.generate_parameters(generator=2, key_size=2048)

    # 2. RSA Long-Term Identity Key Generation (Provisioned offline/in advance)
    print("[*] Provisioning RSA identity keys for Alice and Bob...")
    alice_rsa_priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    alice_rsa_pub = alice_rsa_priv.public_key()

    bob_rsa_priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    bob_rsa_pub = bob_rsa_priv.public_key()

    # =========================================================================
    # SCENARIO 1: Legitimate Authenticated Key Exchange (Alice <-> Bob)
    # =========================================================================
    print("\n--- Scenario 1: Legitimate Handshake (Alice <-> Bob) ---")

    # Ephemeral DH Keys
    alice_dh_priv = dh_parameters.generate_private_key()
    alice_dh_pub = alice_dh_priv.public_key()

    bob_dh_priv = dh_parameters.generate_private_key()
    bob_dh_pub = bob_dh_priv.public_key()

    # Serialize ephemeral public keys to raw bytes for signing
    alice_dh_pub_bytes = alice_dh_pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    bob_dh_pub_bytes = bob_dh_pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Signing step
    alice_signature = alice_rsa_priv.sign(
        alice_dh_pub_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    bob_signature = bob_rsa_priv.sign(
        bob_dh_pub_bytes,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    # Verification step
    try:
        bob_rsa_pub.verify(
            bob_signature,
            bob_dh_pub_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        alice_verified_bob = True
    except InvalidSignature:
        alice_verified_bob = False

    try:
        alice_rsa_pub.verify(
            alice_signature,
            alice_dh_pub_bytes,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        bob_verified_alice = True
    except InvalidSignature:
        bob_verified_alice = False

    # Establish shared secret if signatures are valid
    if alice_verified_bob and bob_verified_alice:
        legit_alice_secret = alice_dh_priv.exchange(bob_dh_pub)
        legit_bob_secret = bob_dh_priv.exchange(alice_dh_pub)
        secrets_match = (legit_alice_secret == legit_bob_secret)
        print(f"[+] Alice verified Bob signature : {alice_verified_bob}")
        print(f"[+] Bob verified Alice signature : {bob_verified_alice}")
        print(f"[+] Shared secrets match         : {secrets_match}")
    else:
        print("[-] Handshake aborted due to signature failure.")

    # =========================================================================
    # SCENARIO 2: MitM Tampering Attempt by Mallory
    # =========================================================================
    print("\n--- Scenario 2: Active MitM Tampering Attempt by Mallory ---")

    # Mallory creates her own DH key to replace Alice's key
    mallory_dh_priv = dh_parameters.generate_private_key()
    mallory_dh_pub = mallory_dh_priv.public_key()
    mallory_dh_pub_bytes = mallory_dh_pub.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    # Mallory forwards HER public key to Bob, but Bob expects Alice's signature on it.
    # Mallory does not possess Alice's RSA private key.
    attack_detected = False
    try:
        # Bob tries to verify Mallory's injected key using Alice's genuine public key
        alice_rsa_pub.verify(
            alice_signature,        # Alice's signature (which covers Alice's key, not Mallory's)
            mallory_dh_pub_bytes,   # Mallory's tampered DH key
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        print("[-] Mallory bypassed authentication (Unsafe)!")
    except InvalidSignature:
        attack_detected = True
        print("[!] SECURITY ALERT: Signature verification failed!")
        print("[+] Bob detected key manipulation: Mallory's DH key does not match Alice's signature.")
        print("[+] Handshake aborted. MitM Attack successfully thwarted.")

    print("\n" + "=" * 65)
    print("PHASE 3A FUNCTIONAL SUMMARY")
    print("=" * 65)
    print(f"Legitimate Authenticated Exchange : {'SUCCESS' if secrets_match else 'FAILED'}")
    print(f"MitM Tampering Detected            : {'SUCCESS (Attack Defeated)' if attack_detected else 'FAILED'}")

if __name__ == "__main__":
    run_authenticated_dh_demo()