import unittest
import random
from ecdsa import ecdsa_sign, ecdsa_pubkey, verify_ecdsa, n

# Test private keys
PRIV_KEY_1 = 0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80
PRIV_KEY_2 = 0x59c6995e998f97a5a0044966f0945389dc9e86dae88c7a8412f4603b6b78690d


class TestECDSA(unittest.TestCase):
    """Test suite for ECDSA implementation"""
    
    def test_basic_sign_and_verify(self):
        """Test basic signing and verification"""
        msg = "Hello, World!"
        pub_key = ecdsa_pubkey(PRIV_KEY_1)
        r, s = ecdsa_sign(msg, PRIV_KEY_1)
        
        self.assertTrue(verify_ecdsa(msg, pub_key, r, s))
    
    def test_verify_with_wrong_message(self):
        """Test that verification fails with wrong message"""
        msg1 = "Hello, World!"
        msg2 = "Goodbye, World!"
        
        pub_key = ecdsa_pubkey(PRIV_KEY_1)
        r, s = ecdsa_sign(msg1, PRIV_KEY_1)
        
        self.assertFalse(verify_ecdsa(msg2, pub_key, r, s))
    
    def test_verify_with_wrong_public_key(self):
        """Test that verification fails with wrong public key"""
        msg = "Hello, World!"
        
        pub_key_1 = ecdsa_pubkey(PRIV_KEY_1)
        pub_key_2 = ecdsa_pubkey(PRIV_KEY_2)
        
        r, s = ecdsa_sign(msg, PRIV_KEY_1)
        
        self.assertTrue(verify_ecdsa(msg, pub_key_1, r, s))
        self.assertFalse(verify_ecdsa(msg, pub_key_2, r, s))
    
    def test_multiple_signatures_different_k(self):
        """Test that multiple signatures of same message verify correctly"""
        msg = "Test message"
        pub_key = ecdsa_pubkey(PRIV_KEY_1)
        
        # Sign the same message multiple times (should get different signatures due to different k)
        signatures = []
        for _ in range(5):
            r, s = ecdsa_sign(msg, PRIV_KEY_1)
            signatures.append((r, s))
            self.assertTrue(verify_ecdsa(msg, pub_key, r, s))
        
        # All signatures should be different (very unlikely to be same with random k)
        unique_sigs = set(signatures)
        self.assertEqual(len(unique_sigs), 5, "All signatures should be unique")
    
    def test_different_messages(self):
        """Test signing and verifying different messages"""
        messages = [
            "Message 1",
            "Message 2",
            "A" * 100,  # Long message
            "",  # Empty message
            "Special chars: !@#$%^&*()",
        ]
        
        pub_key = ecdsa_pubkey(PRIV_KEY_1)
        
        for msg in messages:
            r, s = ecdsa_sign(msg, PRIV_KEY_1)
            self.assertTrue(verify_ecdsa(msg, pub_key, r, s))
    
    def test_invalid_signature_r_zero(self):
        """Test that verification rejects signature with r == 0"""
        msg = "Test message"
        pub_key = ecdsa_pubkey(PRIV_KEY_1)
        
        self.assertFalse(verify_ecdsa(msg, pub_key, 0, 12345))
    
    def test_invalid_signature_s_zero(self):
        """Test that verification rejects signature with s == 0"""
        msg = "Test message"
        pub_key = ecdsa_pubkey(PRIV_KEY_1)
        
        self.assertFalse(verify_ecdsa(msg, pub_key, 12345, 0))
    
    def test_invalid_signature_r_out_of_range(self):
        """Test that verification rejects signature with r >= n"""
        msg = "Test message"
        pub_key = ecdsa_pubkey(PRIV_KEY_1)
        
        self.assertFalse(verify_ecdsa(msg, pub_key, n, 12345))
        self.assertFalse(verify_ecdsa(msg, pub_key, n + 1, 12345))
    
    def test_invalid_signature_s_out_of_range(self):
        """Test that verification rejects signature with s >= n"""
        msg = "Test message"
        pub_key = ecdsa_pubkey(PRIV_KEY_1)
        
        # First get a valid r by signing
        r, _ = ecdsa_sign(msg, PRIV_KEY_1)
        
        self.assertFalse(verify_ecdsa(msg, pub_key, r, n))
        self.assertFalse(verify_ecdsa(msg, pub_key, r, n + 1))
    
    def test_invalid_signature_modified_r(self):
        """Test that verification fails when r is modified"""
        msg = "Test message"
        pub_key = ecdsa_pubkey(PRIV_KEY_1)
        r, s = ecdsa_sign(msg, PRIV_KEY_1)
        
        # Modify r slightly
        self.assertFalse(verify_ecdsa(msg, pub_key, r + 1, s))
        self.assertFalse(verify_ecdsa(msg, pub_key, r - 1, s))
    
    def test_invalid_signature_modified_s(self):
        """Test that verification fails when s is modified"""
        msg = "Test message"
        pub_key = ecdsa_pubkey(PRIV_KEY_1)
        r, s = ecdsa_sign(msg, PRIV_KEY_1)
        
        # Modify s slightly
        self.assertFalse(verify_ecdsa(msg, pub_key, r, s + 1))
        self.assertFalse(verify_ecdsa(msg, pub_key, r, s - 1))
    
    def test_public_key_consistency(self):
        """Test that same private key always generates same public key"""
        pub_key_1 = ecdsa_pubkey(PRIV_KEY_1)
        pub_key_2 = ecdsa_pubkey(PRIV_KEY_1)
        
        self.assertEqual(pub_key_1.x, pub_key_2.x)
        self.assertEqual(pub_key_1.y, pub_key_2.y)
    
    def test_different_private_keys_different_public_keys(self):
        """Test that different private keys generate different public keys"""
        pub_key_1 = ecdsa_pubkey(PRIV_KEY_1)
        pub_key_2 = ecdsa_pubkey(PRIV_KEY_2)
        
        self.assertTrue(pub_key_1.x != pub_key_2.x or pub_key_1.y != pub_key_2.y)
    
    def test_signature_determinism(self):
        """Test that signing same message multiple times produces different signatures"""
        msg = "Determinism test"
        pub_key = ecdsa_pubkey(PRIV_KEY_1)
        
        sig1 = ecdsa_sign(msg, PRIV_KEY_1)
        sig2 = ecdsa_sign(msg, PRIV_KEY_1)
        sig3 = ecdsa_sign(msg, PRIV_KEY_1)
        
        # All should verify
        self.assertTrue(verify_ecdsa(msg, pub_key, sig1[0], sig1[1]))
        self.assertTrue(verify_ecdsa(msg, pub_key, sig2[0], sig2[1]))
        self.assertTrue(verify_ecdsa(msg, pub_key, sig3[0], sig3[1]))
        
        # But signatures should be different (due to random k)
        self.assertTrue(sig1 != sig2 or sig1 != sig3, "Signatures should differ due to random k")
    
    def test_edge_case_empty_message(self):
        """Test signing and verifying empty message"""
        msg = ""
        pub_key = ecdsa_pubkey(PRIV_KEY_1)
        r, s = ecdsa_sign(msg, PRIV_KEY_1)
        
        self.assertTrue(verify_ecdsa(msg, pub_key, r, s))
    
    def test_edge_case_very_long_message(self):
        """Test signing and verifying very long message"""
        msg = "A" * 10000
        pub_key = ecdsa_pubkey(PRIV_KEY_1)
        r, s = ecdsa_sign(msg, PRIV_KEY_1)
        
        self.assertTrue(verify_ecdsa(msg, pub_key, r, s))
    
    def test_unicode_message(self):
        """Test signing and verifying unicode message"""
        msg = "Hello 世界 🌍"
        pub_key = ecdsa_pubkey(PRIV_KEY_1)
        r, s = ecdsa_sign(msg, PRIV_KEY_1)
        
        self.assertTrue(verify_ecdsa(msg, pub_key, r, s))


if __name__ == "__main__":
    unittest.main(verbosity=2)
