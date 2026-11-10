import sys


def verify_all():
    all_passed = True

    # 1. Classical Test
    print("--- Testing Classical Engine (RSA-2048) ---")
    try:
        from cryptography.hazmat.primitives.asymmetric import rsa
        rsa_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
        print("[PASS] Classical OpenSSL RSA-2048 initialized successfully.")
    except Exception as e:
        all_passed = False
        print(f"[FAIL] Classical Engine Error: {e}")

    # 2. Post-Quantum Test
    print("\n--- Testing Post-Quantum Engine (ML-DSA) ---")
    try:
        import oqs
        available_sigs = oqs.get_enabled_sig_mechanisms()
        sig_alg = "ML-DSA-44" if "ML-DSA-44" in available_sigs else "Dilithium2"

        with oqs.Signature(sig_alg) as signer:
            pubkey = signer.generate_keypair()
            payload = b"BB84_Sifting_Session_Verification_Test"
            signature = signer.sign(payload)
            is_valid = signer.verify(payload, signature, pubkey)

            if is_valid:
                print(f"[PASS] Post-Quantum Engine ({sig_alg}) initialized and verified signature.")
            else:
                all_passed = False
                print(f"[FAIL] Post-Quantum Engine ({sig_alg}) initialized, but signature verification returned False.")
    except Exception as e:
        all_passed = False
        print(f"[FAIL] Post-Quantum Engine Error: {e}")

    # Final Verdict
    print("\n" + "=" * 40)
    if all_passed:
        print("OVERALL STATUS: ALL ENGINES OPERATIONAL")
        sys.exit(0)
    else:
        print("OVERALL STATUS: ENVIRONMENT SETUP INCOMPLETE")
        sys.exit(1)

if __name__ == "__main__":
    verify_all()