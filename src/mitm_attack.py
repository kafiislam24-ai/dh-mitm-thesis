"""
Phase 2A: Controlled Man-in-the-Middle (MitM) Attack Simulation
Architecture: Alice <-> Mallory <-> Bob
"""

from cryptography.hazmat.primitives.asymmetric import dh

def run_mitm_simulation():
    print("=" * 60)
    print("PHASE 2A: MAN-IN-THE-MIDDLE (MitM) ATTACK SIMULATION")
    print("=" * 60)

    # 1. 2048-bit DH Domain Parameters (Outside handshake timing)
    print("[*] Generating 2048-bit DH domain parameters...")
    parameters = dh.generate_parameters(generator=2, key_size=2048)

    # 2. Key Generation Phase
    # Alice key pair
    alice_private_key = parameters.generate_private_key()
    alice_public_key = alice_private_key.public_key()

    # Bob key pair
    bob_private_key = parameters.generate_private_key()
    bob_public_key = bob_private_key.public_key()

    # Mallory (Attacker) generates two separate key pairs
    mallory_private_for_alice = parameters.generate_private_key()
    mallory_public_for_alice = mallory_private_for_alice.public_key()

    mallory_private_for_bob = parameters.generate_private_key()
    mallory_public_for_bob = mallory_private_for_bob.public_key()

    print("[+] Alice, Bob, and Mallory generated their keys.")

    # 3. Interception and Key Exchange Phase
    # Alice computes shared secret with Mallory's intercepted key
    alice_shared_secret = alice_private_key.exchange(mallory_public_for_alice)

    # Bob computes shared secret with Mallory's intercepted key
    bob_shared_secret = bob_private_key.exchange(mallory_public_for_bob)

    # Mallory computes shared secrets with both Alice and Bob
    mallory_secret_with_alice = mallory_private_for_alice.exchange(alice_public_key)
    mallory_secret_with_bob = mallory_private_for_bob.exchange(bob_public_key)

    # 4. Security & Integrity Verifications
    alice_mallory_match = (alice_shared_secret == mallory_secret_with_alice)
    bob_mallory_match = (bob_shared_secret == mallory_secret_with_bob)
    alice_bob_match = (alice_shared_secret == bob_shared_secret)

    print("\n" + "-" * 40)
    print("VERIFICATION RESULTS:")
    print("-" * 40)
    print(f"Alice & Mallory shared secret match: {alice_mallory_match}")
    print(f"Bob & Mallory shared secret match  : {bob_mallory_match}")
    print(f"Direct Alice & Bob secret match    : {alice_bob_match}")

    # 5. Attack Evaluation
    if alice_mallory_match and bob_mallory_match and not alice_bob_match:
        print("\n[SUCCESS] MitM Attack successfully demonstrated.")
        print("Mallory successfully split the channel into two independent secure channels.")
        return True
    else:
        print("\n[FAILURE] MitM condition was not satisfied.")
        return False

if __name__ == "__main__":
    run_mitm_simulation()