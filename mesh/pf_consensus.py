# NOTE:
# This module is part of Section 13 (PF Distributed Cognitive Mesh),
# which is NOT active during v3 local runtime.
# Do not import this file in runtime until initialization of PF-DCM.

"""
PF-Level Consensus.

PF-Consensus is NOT blockchain consensus.
It is NOT proof-of-work.

PF-Consensus = agreement by curvature.

Nodes agree a capsule is valid if:
1. Shell pipeline valid
2. Curvature signature continuous
3. Triplets valid
4. Rail interference compatible
5. QuantaCoin > threshold
6. Experience delta consistent

This creates instantaneous consensus, faster than any blockchain mechanism.
No mining. No energy expenditure. Purely information-theoretic.
"""

from __future__ import annotations

from typing import Any
from dataclasses import dataclass
from ApopToSiS.runtime.capsules import Capsule
from ApopToSiS.runtime.distributed_safety import DistributedSafety
from ApopToSiS.core.math.shells import Shell


@dataclass
class ConsensusVote:
    """
    A consensus vote on a capsule.
    """
    device_id: str
    capsule_id: str
    is_valid: bool
    trust_score: float
    reasons: list[str] = None


@dataclass
class ConsensusResult:
    """
    Consensus result for a capsule.
    """
    capsule_id: str
    is_consensus: bool
    consensus_score: float  # 0.0 to 1.0
    votes: list[ConsensusVote]
    validation_checks: dict[str, bool]


class PFConsensus:
    """
    PF-Level Consensus Engine.
    
    Achieves consensus through PF curvature agreement, not blockchain.
    """

    def __init__(self, trust_threshold: float = 0.5) -> None:
        """
        Initialize consensus engine.

        Args:
            trust_threshold: Minimum trust for consensus
        """
        self.trust_threshold = trust_threshold
        self.safety = DistributedSafety()

    def validate_capsule_for_consensus(self, capsule: Capsule) -> dict[str, bool]:
        """
        Validate capsule for consensus.
        
        Checks:
        1. Shell pipeline valid
        2. Curvature signature continuous
        3. Triplets valid
        4. Rail interference compatible
        5. QuantaCoin > threshold
        6. Experience delta consistent

        Args:
            capsule: Capsule to validate

        Returns:
            Dictionary of validation check results
        """
        checks = {}
        
        # 1. Shell pipeline valid
        checks["shell_pipeline"] = capsule.shell in [0, 2, 3, 4]
        
        # 2. Curvature signature continuous (basic check)
        checks["curvature_continuous"] = 0.0 <= capsule.curvature <= 100.0
        
        # 3. Triplets valid
        checks["triplets_valid"] = all(
            isinstance(t, dict) and "a" in t and "b" in t and "c" in t
            for t in capsule.triplets
        )
        
        # 4. Rail interference compatible
        checks["rail_compatible"] = 0.0 <= capsule.rail_interference <= 10.0
        
        # 5. QuantaCoin > threshold
        checks["quanta_threshold"] = capsule.compression_ratio >= self.trust_threshold
        
        # 6. Experience delta consistent (basic structure check)
        checks["experience_delta_consistent"] = isinstance(capsule.experience_delta, dict)
        
        return checks

    def vote_on_capsule(
        self,
        capsule: Capsule,
        device_id: str
    ) -> ConsensusVote:
        """
        Vote on capsule validity.

        Args:
            capsule: Capsule to vote on
            device_id: Voting device ID

        Returns:
            Consensus vote
        """
        # Validate capsule
        checks = self.validate_capsule_for_consensus(capsule)
        
        # Compute trust score
        trust_score = self.safety.compute_trust_score(capsule)
        
        # Determine validity
        is_valid = all(checks.values()) and trust_score >= self.trust_threshold
        
        # Collect reasons
        reasons = []
        if not checks["shell_pipeline"]:
            reasons.append("Invalid shell pipeline")
        if not checks["curvature_continuous"]:
            reasons.append("Curvature out of range")
        if not checks["triplets_valid"]:
            reasons.append("Invalid triplets")
        if not checks["rail_compatible"]:
            reasons.append("Rail interference incompatible")
        if not checks["quanta_threshold"]:
            reasons.append("QuantaCoin below threshold")
        if not checks["experience_delta_consistent"]:
            reasons.append("Experience delta inconsistent")
        if trust_score < self.trust_threshold:
            reasons.append("Trust score too low")
        
        return ConsensusVote(
            device_id=device_id,
            capsule_id=capsule.capsule_id,
            is_valid=is_valid,
            trust_score=trust_score,
            reasons=reasons if reasons else None,
        )

    def reach_consensus(
        self,
        capsule: Capsule,
        votes: list[ConsensusVote],
        consensus_threshold: float = 0.7
    ) -> ConsensusResult:
        """
        Reach consensus from votes.
        
        Consensus = weighted agreement by trust scores.

        Args:
            capsule: Capsule being voted on
            votes: List of votes
            consensus_threshold: Minimum consensus score

        Returns:
            Consensus result
        """
        if not votes:
            return ConsensusResult(
                capsule_id=capsule.capsule_id,
                is_consensus=False,
                consensus_score=0.0,
                votes=votes,
                validation_checks={},
            )
        
        # Weight votes by trust score
        total_weight = sum(v.trust_score for v in votes)
        valid_weight = sum(v.trust_score for v in votes if v.is_valid)
        
        if total_weight == 0:
            consensus_score = 0.0
        else:
            consensus_score = valid_weight / total_weight
        
        is_consensus = consensus_score >= consensus_threshold
        
        # Get validation checks from first vote (all should agree)
        validation_checks = self.validate_capsule_for_consensus(capsule)
        
        return ConsensusResult(
            capsule_id=capsule.capsule_id,
            is_consensus=is_consensus,
            consensus_score=consensus_score,
            votes=votes,
            validation_checks=validation_checks,
        )

    def is_instant_consensus(self, capsule: Capsule) -> bool:
        """
        Check if capsule achieves instant consensus.
        
        Instant consensus = passes all validation checks locally.
        No need for network voting.

        Args:
            capsule: Capsule to check

        Returns:
            True if instant consensus
        """
        checks = self.validate_capsule_for_consensus(capsule)
        trust = self.safety.compute_trust_score(capsule)
        
        return all(checks.values()) and trust >= self.trust_threshold

