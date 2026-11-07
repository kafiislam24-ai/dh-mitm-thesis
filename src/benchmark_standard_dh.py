import time
from cryptography.hazmat.primitives.asymmetric import dh


# -------------------------------------------------
# STEP 1: Generate common DH parameters
# This is done OUTSIDE the measured key exchange.
# -------------------------------------------------
parameters = dh.generate_parameters(
    generator=2,
    key_size=2048
)


# -------------------------------------------------
# STEP 2: Measure Alice and Bob key generation
# -------------------------------------------------
keygen_start = time.perf_counter_ns()

alice_private_key = parameters.generate_private_key()
alice_public_key = alice_private_key.public_key()

bob_private_key = parameters.generate_private_key()
bob_public_key = bob_private_key.public_key()

keygen_end = time.perf_counter_ns()

keygen_time_ms = (keygen_end - keygen_start) / 1_000_000


# -------------------------------------------------
# STEP 3: Measure shared-secret computation
# -------------------------------------------------
exchange_start = time.perf_counter_ns()

alice_shared_secret = alice_private_key.exchange(
    bob_public_key
)

bob_shared_secret = bob_private_key.exchange(
    alice_public_key
)

exchange_end = time.perf_counter_ns()

exchange_time_ms = (
    exchange_end - exchange_start
) / 1_000_000


# -------------------------------------------------
# STEP 4: Total measured DH operation time
# -------------------------------------------------
total_time_ms = keygen_time_ms + exchange_time_ms


# -------------------------------------------------
# STEP 5: Verify shared secret
# -------------------------------------------------
shared_secret_match = (
    alice_shared_secret == bob_shared_secret
)


# -------------------------------------------------
# STEP 6: Display results
# -------------------------------------------------
print("=== Standard Diffie-Hellman Benchmark ===")

print(
    f"Key generation time: "
    f"{keygen_time_ms:.6f} ms"
)

print(
    f"Shared-secret computation time: "
    f"{exchange_time_ms:.6f} ms"
)

print(
    f"Total measured DH time: "
    f"{total_time_ms:.6f} ms"
)

print(
    f"Shared secrets match: "
    f"{shared_secret_match}"
)