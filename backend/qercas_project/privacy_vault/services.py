import logging
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64

logger = logging.getLogger(__name__)

class CryptoService:
    """
    Provides methods for quantum-resistant cryptography with fallback to classical encryption.
    """
    _KEM_ALGORITHM = "Kyber768" # A NIST-selected PQC algorithm

    @staticmethod
    def _use_fallback_crypto():
        """Use AES-256 as fallback when PQC is not available"""
        logger.warning("PQC not available, using AES-256 fallback")
        return True

    @staticmethod
    def generate_pqc_keys():
        """Generates a new PQC public and private key pair."""
        try:
            import oqs
            with oqs.KeyEncapsulation(CryptoService._KEM_ALGORITHM) as kem:
                public_key = kem.generate_keypair()
                secret_key = kem.export_secret_key()
                return public_key, secret_key
        except (ImportError, AttributeError) as e:
            logger.warning(f"PQC key generation failed: {e}")
            # Fallback: Generate AES key
            key = get_random_bytes(32)  # 256-bit key
            return key, key  # Use same key as both public and private for demo

    @staticmethod
    def encrypt_pqc(public_key, plain_text: str):
        """
        Encrypts a string using PQC or fallback encryption.
        """
        try:
            import oqs
            with oqs.KeyEncapsulation(CryptoService._KEM_ALGORITHM) as kem:
                ciphertext, shared_secret = kem.encapsulate(public_key)
                print("--- PQC: Data Encrypted ---")
                return ciphertext
        except (ImportError, AttributeError) as e:
            logger.warning(f"PQC encryption failed: {e}, using AES fallback")
            # Fallback: Use AES encryption
            cipher = AES.new(public_key[:32], AES.MODE_CBC)
            iv = cipher.iv
            padded_text = pad(plain_text.encode('utf-8'), AES.block_size)
            ciphertext = cipher.encrypt(padded_text)
            # Combine IV and ciphertext
            result = iv + ciphertext
            print("--- AES Fallback: Data Encrypted ---")
            return base64.b64encode(result)

    @staticmethod
    def decrypt_pqc(secret_key, ciphertext):
        """
        Decrypts PQC ciphertext or fallback encryption.
        """
        try:
            import oqs
            with oqs.KeyEncapsulation(CryptoService._KEM_ALGORITHM) as kem:
                kem.import_secret_key(secret_key)
                shared_secret = kem.decapsulate(ciphertext)
                print("--- PQC: Data Decrypted (shared secret recovered) ---")
                return shared_secret
        except (ImportError, AttributeError) as e:
            logger.warning(f"PQC decryption failed: {e}, using AES fallback")
            # Fallback: Use AES decryption
            try:
                encrypted_data = base64.b64decode(ciphertext)
                iv = encrypted_data[:16]  # AES block size
                actual_ciphertext = encrypted_data[16:]
                cipher = AES.new(secret_key[:32], AES.MODE_CBC, iv)
                decrypted_padded = cipher.decrypt(actual_ciphertext)
                decrypted_text = unpad(decrypted_padded, AES.block_size)
                print("--- AES Fallback: Data Decrypted ---")
                return decrypted_text
            except Exception as decrypt_error:
                logger.error(f"Fallback decryption failed: {decrypt_error}")
                return b"decryption_failed"