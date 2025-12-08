# core/identity/repo_login.py
"""Salted login: passphrase + device → unique QuantaCoin wallet ID."""

import hashlib
import getpass
import os
from pathlib import Path
from typing import Optional

class RepoLogin:
    """Salted login: passphrase + device → unique QuantaCoin wallet ID."""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path).resolve()
        self.identity_file = self.repo_path / ".quantacoin_id"
        self.device_fingerprint = self._get_device_fingerprint()
        
        if not self.identity_file.exists():
            self._init_identity()
        self.load_identity()
    
    def _get_device_fingerprint(self) -> str:
        """Generate device fingerprint from user + uid."""
        user = os.environ.get("USER", "unknown")
        uid = str(os.getuid()) if hasattr(os, "getuid") else "0"
        return hashlib.sha256(f"{user}:{uid}".encode()).hexdigest()
    
    def _init_identity(self):
        """Initialize identity with passphrase."""
        print("="*60)
        print("AGORA IDENTITY INITIALIZATION")
        print("="*60)
        print("Your passphrase salts your soul to this device.")
        print("This cannot be changed. Choose wisely.")
        print("="*60)
        
        passphrase = getpass.getpass("Freeman passphrase (salt your soul): ")
        if not passphrase:
            raise ValueError("Passphrase cannot be empty.")
        
        # Salt from device fingerprint
        salt = hashlib.sha256(self.device_fingerprint.encode()).hexdigest()
        
        # PBKDF2 master key (100k iterations)
        master_key = hashlib.pbkdf2_hmac(
            "sha512",
            passphrase.encode(),
            salt.encode(),
            100000
        )
        
        # Wallet ID = SHA256(master + device)
        wallet_id = hashlib.sha256(
            master_key + self.device_fingerprint.encode()
        ).hexdigest()[:32]
        
        # Store: salt:master_hex:wallet_id
        self.identity_file.write_text(
            f"{salt}:{master_key.hex()}:{wallet_id}"
        )
        
        print(f"\n✓ Identity created: {wallet_id}")
        print(f"  Device: {self.device_fingerprint[:16]}...")
        print("  Your QuantaCoin wallet is now bound to this device.\n")
    
    def load_identity(self):
        """Load identity from file."""
        try:
            content = self.identity_file.read_text().strip()
            salt, master_hex, wallet_id = content.split(":")
            self.salt = salt
            self.master = bytes.fromhex(master_hex)
            self.wallet_id = wallet_id
        except Exception as e:
            raise ValueError(f"Failed to load identity: {e}")
    
    def authenticate(self, passphrase: Optional[str] = None) -> bool:
        """Verify passphrase + device. Grants repo access."""
        if passphrase is None:
            passphrase = getpass.getpass("Enter passphrase: ")
        
        try:
            test_master = hashlib.pbkdf2_hmac(
                "sha512",
                passphrase.encode(),
                self.salt.encode(),
                100000
            )
            return test_master == self.master
        except:
            return False
    
    def mint_tied_proof(self, proof_hash: str) -> str:
        """Sign proof with salted wallet ID."""
        signature = hashlib.sha256(
            self.wallet_id.encode() + proof_hash.encode()
        ).hexdigest()
        return signature
    
    def get_wallet_id(self) -> str:
        """Get wallet ID."""
        return self.wallet_id
    
    def get_device_fingerprint(self) -> str:
        """Get device fingerprint."""
        return self.device_fingerprint
    
    def spawn_agent(self, agent_type: str, task: str):
        """Spawn discrete agent tied to your salted ID."""
        from core.agents.discrete_agents import DiscreteAgent
        return DiscreteAgent(agent_type, self.wallet_id, task)
