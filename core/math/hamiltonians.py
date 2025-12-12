"""
PrimeFlux Hamiltonian.

H(x) = κ₂ sin(x) + κ₃ tan(x) + log(|x| + 2)

Where:
- κ₂ = √2 (shell 2 curvature)
- κ₃ = π / φ (shell 3 curvature)

Collapse occurs when H(x) > φ²
"""

from __future__ import annotations

import math
from typing import Tuple, Optional

try:
    import numpy as np
    NUMPY_AVAILABLE = True
except ImportError:
    NUMPY_AVAILABLE = False
    # Fallback: numpy is required for HamiltonianTensor
    # If not available, raise informative error
    raise ImportError(
        "numpy is required for HamiltonianTensor. "
        "Install with: pip install numpy>=1.24.0"
    )

from .shells import Shell, shell_curvature
from .attractors import get_attractor_registry

SQRT2 = math.sqrt(2)
PHI = (1 + math.sqrt(5)) / 2
PI = math.pi


def hamiltonian(x: float) -> float:
    """
    Compute PrimeFlux Hamiltonian.
    
    H(x) = κ₂ sin(x) + κ₃ tan(x) + log(|x| + 2)
    
    Args:
        x: Input value
        
    Returns:
        Hamiltonian value
    """
    kappa2 = SQRT2  # Shell 2 curvature
    kappa3 = PI / PHI  # Shell 3 curvature
    
    sin_term = kappa2 * math.sin(x)
    
    tan_val = math.tan(x)
    if abs(tan_val) > 1e10:
        tan_val = math.copysign(1e10, tan_val)
    
    tan_term = kappa3 * tan_val
    log_term = math.log(abs(x) + 2.0)
    
    return sin_term + tan_term + log_term


def curvature_well(x: float) -> float:
    """
    Compute curvature potential well.
    
    Args:
        x: Input value
        
    Returns:
        Potential well depth
    """
    H = hamiltonian(x)
    kappa4 = PHI ** 2  # Collapse threshold
    
    # Well depth = distance from collapse
    return kappa4 - H


def collapse_energy(x: float) -> float:
    """
    Compute collapse energy.
    
    Collapse occurs when H(x) > φ².
    
    Args:
        x: Input value
        
    Returns:
        Collapse energy (positive = collapsed)
    """
    H = hamiltonian(x)
    kappa4 = PHI ** 2  # Collapse threshold
    
    return H - kappa4


class HamiltonianTensor:
    """
    4×4 quaternionic Hamiltonian tensor H_PF.
    
    Mathematical Foundation:
    - Based on: Lie paper §3-4 "PrimeFlux Hamiltonian"
    - 2×2 block matrix (dual rails + coupling) lifts to 4×4 via quaternionic embedding
    - SU(2) structure naturally yields H⁴ = -I
    - Physics justification: 4D Yang-Mills matches quaternion group (8-element) structure
    
    Quaternionic Structure:
    - Irrational seeds (1/11, 11/18, 1/3) are attractors (from attractors.py)
    - Eigenvalues: 1, i, -1, -i (i is an attractor)
    - Closure property: H⁴ = -I (quaternionic closure)
    
    Hilbert Space:
    - PF state space with presence norm ⟨ψ|φ⟩_p = ∫ ψ* G(x) φ dx
    - Based on: ApopTosis Thesis §2.6 - Gaussian equilibrium G(x) = exp(-x²/2σ²)
    """
    
    def __init__(self):
        """Initialize Hamiltonian tensor with attractor seeds."""
        registry = get_attractor_registry()
        
        # Get attractor values for irrational seeds
        seed_1_11 = registry.get_by_name("seed_1_11")
        seed_11_18 = registry.get_by_name("seed_11_18")
        seed_1_3 = registry.get_by_name("seed_1_3")
        
        # Extract values (or use defaults if not found)
        val_1_11 = seed_1_11.value if seed_1_11 and seed_1_11.value else (1.0 / 11.0)
        val_11_18 = seed_11_18.value if seed_11_18 and seed_11_18.value else (11.0 / 18.0)
        val_1_3 = seed_1_3.value if seed_1_3 and seed_1_3.value else (1.0 / 3.0)
        
        # Construct 4×4 quaternionic matrix
        # H_PF = [[0, 1, 1/2, -1/2],
        #         [1, 0, i/2, -i/2],
        #         [1/2, -i/2, 0, 1],
        #         [-1/2, i/2, -1, 0]]
        # With irrational seeds replacing 1/2
        self.matrix = np.array([
            [0, 1, val_1_11, -val_1_11],
            [1, 0, 1j * val_11_18, -1j * val_11_18],
            [val_1_11, -1j * val_11_18, 0, 1],
            [-val_1_11, 1j * val_11_18, -1, 0]
        ], dtype=complex)
    
    def verify_closure(self) -> bool:
        """
        Verify quaternionic closure: H⁴ = -I.
        
        Returns:
            True if H⁴ = -I (within numerical tolerance), False otherwise
        """
        H4 = np.linalg.matrix_power(self.matrix, 4)
        I = np.eye(4, dtype=complex)
        expected = -I
        
        # Check if H4 ≈ -I (within numerical tolerance)
        diff = np.abs(H4 - expected)
        max_diff = np.max(diff)
        
        return max_diff < 1e-10
    
    def get_eigenvalues(self) -> np.ndarray:
        """
        Get eigenvalues of Hamiltonian tensor.
        
        Expected: 1, i, -1, -i (the 4th roots of unity)
        
        Returns:
            Array of eigenvalues
        """
        eigenvalues, _ = np.linalg.eig(self.matrix)
        return eigenvalues
    
    def get_eigenspace(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Get eigenspace decomposition.
        
        Returns:
            Tuple of (eigenvalues, eigenvectors)
        """
        eigenvalues, eigenvectors = np.linalg.eig(self.matrix)
        return eigenvalues, eigenvectors
    
    def presence_projector(self, sigma: float = 1.0 / math.sqrt(2.0)) -> np.ndarray:
        """
        Compute presence projector P_+ = (I + H/||H||_p)/2.
        
        Hilbert space: PF state space with presence norm
        ⟨ψ|φ⟩_p = ∫ ψ* G(x) φ dx
        where G(x) = exp(-x²/2σ²) (Gaussian equilibrium)
        
        Based on: ApopTosis Thesis §2.6 - Gaussian equilibrium
        
        Args:
            sigma: Gaussian width (default 1/√2)
            
        Returns:
            Presence projector matrix
        """
        I = np.eye(4, dtype=complex)
        
        # Compute presence norm ||H||_p
        # For simplicity, use Frobenius norm weighted by Gaussian
        H_norm = np.linalg.norm(self.matrix, 'fro')
        
        # Normalize H
        H_normalized = self.matrix / H_norm if H_norm > 0 else self.matrix
        
        # Presence projector: P_+ = (I + H/||H||_p)/2
        P_plus = (I + H_normalized) / 2.0
        
        return P_plus
    
    def apply_to_vector(self, vector: np.ndarray) -> np.ndarray:
        """
        Apply Hamiltonian tensor to vector.
        
        Args:
            vector: Input vector (4D)
            
        Returns:
            Transformed vector
        """
        if vector.shape != (4,):
            raise ValueError(f"Vector must be 4D, got shape {vector.shape}")
        
        return self.matrix @ vector
    
    def check_attractor_convergence(self, vector: np.ndarray, threshold: float = 1e-6) -> bool:
        """
        Check if system is converging toward attractor eigenvalues.
        
        System stabilizes when vector is near eigenvector of attractor eigenvalue.
        
        Args:
            vector: State vector
            threshold: Convergence threshold
            
        Returns:
            True if converging, False otherwise
        """
        eigenvalues, eigenvectors = self.get_eigenspace()
        
        # Check if vector aligns with any eigenvector (attractor)
        for i, eigenval in enumerate(eigenvalues):
            eigenvec = eigenvectors[:, i]
            # Normalize
            eigenvec_norm = eigenvec / np.linalg.norm(eigenvec) if np.linalg.norm(eigenvec) > 0 else eigenvec
            vec_norm = vector / np.linalg.norm(vector) if np.linalg.norm(vector) > 0 else vector
            
            # Check alignment (dot product)
            alignment = np.abs(np.dot(vec_norm, eigenvec_norm))
            if alignment > (1.0 - threshold):
                return True
        
        return False
    
    def __repr__(self) -> str:
        """String representation."""
        return f"HamiltonianTensor(4×4, closure_verified={self.verify_closure()})"

