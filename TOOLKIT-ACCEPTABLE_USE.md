# Acceptable use

PHP2Shell is a research toolkit for **authorized** security testing. This page
is part of the project's terms of use, together with [LICENSE](LICENSE) and
[SECURITY.md](SECURITY.md).

## You may use it only when

- you own the target system, or
- you have explicit, written permission from the owner to test it, and
- your testing complies with the law and with the rules of any program you
  participate in.

A public website, an IP address you found online, or a domain that "looks like a
lab" is **not** authorization.

## You must not

- test third-party or public infrastructure;
- build or distribute target lists, scanners or mass-exploitation tooling;
- use the remote worker-saturation mode against systems you do not own: it opens
  many connections and is disruptive;
- cause denial of service, data loss or persistence on systems without written
  authorization;
- publish data obtained from systems you do not own (hostnames, cookies,
  credentials, file contents).

## Disruptive behavior

The chain sends large request bodies, triggers out-of-memory conditions and
kills Apache children. Run it against disposable laboratories. The reference
labs bind to `127.0.0.1` and mount an `/out` directory; keep it that way.

## Disclosure

If you find a new affected build or a new PHP issue, prefer coordinated
disclosure with the PHP security team and the distribution vendor. Do not
publish an unpatched exploit or third-party data.

## No warranty

The software is provided "as is", without warranty of any kind. The authors
accept no liability for misuse or damage. The license grants copyright
permissions only; it does not grant authorization to test any system.
