# Security policy

## Scope

PHP2Shell is a research toolkit for **authorized** testing of
CVE-2026-109618 / CVE-2026-109619. It ships no target list and must not be used
against third-party systems.

## Reporting a problem in this toolkit

If you find a bug in the tooling (dispatcher, profile engine, laboratory
configuration, documentation), open a GitHub issue or a private advisory. Include:

- the affected script and version;
- the exact command and configuration;
- the observed and expected behavior;
- logs with target hostnames, IP addresses, cookies and credentials removed.

Do not include data from systems you do not own.

## Reporting a PHP vulnerability

This repository is not a vendor channel. If you find a new affected build or a
new PHP issue, report it to the PHP security team and the distribution vendor
through their coordinated disclosure process.

## Acceptable use

Testing is allowed only on systems you own or have explicit written permission
to test. The chain is disruptive: it sends large request bodies, triggers
out-of-memory conditions and kills Apache children. Do not use the remote
worker-saturation mode against third-party infrastructure.
