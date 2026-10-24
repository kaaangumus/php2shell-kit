# Contributing

Thanks for helping make PHP2Shell reproducible. Contributions are reviewed for
correctness, safety and evidence.

## Scope

Welcome:

- new build profiles with a real command proof and the exact image/tag;
- offset extraction for new distributions and architectures;
- laboratory fixes and calibration improvements;
- tests, documentation, detection guidance and defensive tooling;
- fixes for the open configurations (`display_errors=Off`, `expose_php=Off`,
  FPM).

Not welcome:

- target lists, mass-exploitation tooling or automation against third parties;
- data from systems you do not own (hostnames, IPs, cookies, credentials);
- changes that make remote saturation pinning a default;
- unverified "RCE" claims.

## Adding a profile

1. Use an exact image tag and the matching architecture.
2. Run `tools/php2shell_calibrate.py` against a local lab.
3. Confirm a real proof (`uid=...`), not just a successful response.
4. Add `profiles/<build>.json` with the offsets, heap parameters and
   `rce: true` only when the proof is reproducible.
5. If stage 3 is probabilistic, say so in the profile and in the README table.
6. Update `docs/profile-inventory.md` and the README status table together.

Profiles must not contain target data. `rce: false` is a valid and useful
result: negative data prevents false positives.

## Code style

- Python 3.11+ with the standard library; avoid new runtime dependencies.
- Keep the dispatcher's safe defaults: loopback automatic, remote opt-in.
- Error messages must not print secrets or raw target data.
- Run the tests before opening a pull request:

```sh
python3 -m unittest discover -s tests -v
gitleaks detect --source . --no-git --redact -v
```

## Pull request checklist

- [ ] Tests pass and new logic has a test.
- [ ] Profile changes include the exact image/tag and a proof.
- [ ] README/inventory tables are updated and accurate.
- [ ] No secrets, personal paths or third-party target data.
- [ ] Credits are preserved (9bie, Karasawa2025, WoYinDao, PHP team).
- [ ] The change does not weaken the authorization gates.

## Disclosure

This repository is not a vendor channel. If you find a new affected build or a
new PHP issue, report it to the PHP security team and the distribution vendor
through their coordinated disclosure process. Do not open a public issue with
an unpatched exploit.
