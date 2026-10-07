from cryptography.hazmat.primitives.asymmetric import dh


parameters = dh.generate_parameters(generator=2, key_size=2048)


alice_private_key = parameters.generate_private_key()
alice_public_key = alice_private_key.public_key()


bob_private_key = parameters.generate_private_key()
bob_public_key = bob_private_key.public_key()


alice_shared_secret = alice_private_key.exchange(bob_public_key)


bob_shared_secret = bob_private_key.exchange(alice_public_key)


print("Alice and Bob generated the same shared secret:")
print(alice_shared_secret == bob_shared_secret)