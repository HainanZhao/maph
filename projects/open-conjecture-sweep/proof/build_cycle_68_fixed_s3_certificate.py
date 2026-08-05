"""Seal C68's exact fixed-S3 comparison theorem."""

from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from proof.check_cycle68_fixed_s3_certificate import audit
from proof.cycle_seal_v1 import check_runtime, freeze_inputs, run_cli, sha256

H = {
 "c67":("artifacts/cycle-67-b067-s3-boundary-positivity-v1.json","49112c9ad1ced71c79c274a6f5f5b95c2b8a5c54f8bc1a5deede743128f7fff0"),
 "prereg":("docs/cycle-68-b068-s3-interior-chord-preregistration-v1.md","df5f9041d96ae973af789823c9d12638d97c1c0b8927ae2bda254844fbaa8d77"),
 "source":("discovery/out/cycle63-orbit-minimizer/source-polynomial.tsv","64940bd62507415c112c26a72bef08799a97d5db40d7cf79700703ed5c966948"),
 "orbit":("discovery/out/cycle63-orbit-minimizer/orbit-polynomial.tsv","1966204bef5189f821885223ac7b3a7bcb0828543b6d7dbf28dd2daad8c784c4"),
 "source_builder":("proof/cycle63_s3_source_polynomial.cpp","032a175fb02ce8e38631253c1da5c2e360e4fc013f38cdab767d44f239d85bc5"),
 "orbit_reducer":("proof/cycle63_reduce_orbit.py","26022a7de0299027e4884f7497a8d12cc481bd8f9293f21787908d3e679a2d78"),
 "secant":("proof/cycle68_secant_polynomials.py","4ba3d5c33e0dd66c2531aea70efaae52e3950b35cc1acbbbf5404a773ef16f56"),
 "strip":("proof/cycle68_strip_boundary_factors.py","3405b12e2a7c98e6d6b914b3cd1c7edee1fb6bad1431a339c297697a684e08aa"),
 "primary":("proof/cycle68_secant_equality_blowup.py","3fa177b37c0e14f209af0b6c2be849eb38cb0b15226e58c2b7fbda3829ff8117"),
 "secondary":("proof/cycle68_secant_secondary_blowup.py","d97192fbc7ad63dacd8f722e3cf1a33f77cb441588d5a9d4e09183832221df9e"),
 "sparse_audit":("proof/cycle68_blowup_sparse_audit.py","a64a019616f097ee711310df6ba4ea84787313c9cdf583da463e176ff49d5437"),
 "coverage":("proof/check_cycle68_secant_cover.py","17bbeb431144dc928f397ae70c6c53393f0fcb925183585bb6678ad780ffcf79"),
 "audit":("proof/check_cycle68_fixed_s3_certificate.py","2c7bd7a90eeab963e11bc041ba9474ea522b753e9c24f0afec3be2db5cb656cd"),
 "replay":("proof/replay_cycle68_fixed_s3.sh","acdedf14a19b98eb6bdb20d628f1824fec9fcf2bb052c001acd397349323c79d"),
 "scaffold":("proof/cycle_seal_v1.py","9494b7693cff5ea537764211fa3a6b980ae96b121fcb35aeb5b13022d550d4e7"),
 "validator":("../../tools/preregistration_check.py","a1d4ef9ce6714c8a774deeb11db7684e7e244ff342f2ee6b8546d57520181359"),
}

def payload():
    checked=audit()
    return {"artifact_id":"cycle-68-b068-s3-fixed-comparison-v1","budget_ordinal":"B068","cycle":68,
      "record_type":"PROVED_FIXED_S3_COMPARISON_THEOREM","recorded_at_utc":"2026-08-05T14:00:00Z","status":"SEALED","epistemic_status":"PROVED",
      "outcome":"For every nonnegative a:S3->R, the fixed-host deficit N(a)-N(a_cl) is nonnegative.","claim_boundary":checked["claim_boundary"],"audit":checked,
      "cycle_decision":{"companion_identity":"/root/darwin_cycle25_short","companion_advice":"After direct source replay and exact chart coverage, seal; do not call this a universal Zhao or Sidorenko proof.","decision":"Seal the fixed-S3 theorem. The next distinct question must seek a representation-theoretic or conditional-expectation lift, not an S4/S5 census.","falsifier":"An exact nonnegative rational S3 function with negative direct deficit."},
      "contained_events":{"chord":"Exact witnesses refuted global u-chord dominance but not the theorem.","resource":"The abandoned full SymPy blow-up audit exceeded the aggregate memory cap; its output is not evidence. The sparse independent audit replaced it."},
      "frozen_hashes":freeze_inputs(ROOT,{k:(ROOT/p,h) for k,(p,h) in H.items()}),"runtime":check_runtime("c68"),"sealer":{"path":"proof/build_cycle_68_fixed_s3_certificate.py","sha256":sha256(Path(__file__))},
      "replay":{"full":"bash proof/replay_cycle68_fixed_s3.sh REPLAY_DIR","audit":"python3 proof/check_cycle68_fixed_s3_certificate.py","check":"python3 proof/build_cycle_68_fixed_s3_certificate.py --check"}}

if __name__ == "__main__":
    raise SystemExit(run_cli(description=__doc__,output=ROOT/"artifacts/cycle-68-b068-s3-fixed-comparison-v1.json",payload_factory=payload))
