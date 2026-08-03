# SIC--Stark handoff

State: `C_FROZEN`; stopped at `C254/B091`. Dimension-six TCC is not proved.

- Authoritative state: [PROGRAM.md](PROGRAM.md)
- Terminal record: [artifacts/cycle-254-b091-terminal-replay-handoff-v1.json](artifacts/cycle-254-b091-terminal-replay-handoff-v1.json)

```sh
source ../../tools/dev-env.sh
research rebuild
research cycle 254
python3 proof/build_cycle_254_terminal_replay_handoff_v1.py --check
```
