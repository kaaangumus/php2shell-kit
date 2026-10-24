.PHONY: bootstrap test labs-up labs-down labs-status labs-test lint clean

bootstrap:                     ## Fetch and pin the upstream exploit
	python3 tools/bootstrap_upstream.py

test:                          ## Run the unit test suite
	python3 -m unittest discover -s tests -v

lint:                          ## Run gitleaks to detect leaked secrets
	gitleaks detect --source . --no-git --redact -v

labs-up:                       ## Start all local laboratories (ports 8100-8106)
	python3 tools/php2shell_labs.py up

labs-down:                     ## Stop all local laboratories
	python3 tools/php2shell_labs.py down

labs-status:                   ## Show laboratory container status
	python3 tools/php2shell_labs.py status

labs-test:                     ## Run the dispatcher against each lab
	python3 tools/php2shell_labs.py test

inventory:                     ## Print the profile and offset inventory
	python3 tools/php2shell_inventory.py

validate-profiles:             ## Validate profiles (requires jsonschema)
	python3 -c "import json, jsonschema; \
	  schema = json.load(open('profiles/schema.json')); \
	  from pathlib import Path; \
	  [jsonschema.validate(json.loads(p.read_text()), schema) or print(f'  ok  {p.name}') \
	   for p in sorted(Path('profiles').glob('*.json')) if p.name != 'schema.json']"

clean:                         ## Remove generated files and vendor checkout
	rm -rf vendor/php2shell-upstream
	rm -rf lab/rce/out/

help:                          ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) | \
	  awk 'BEGIN {FS = ":.*## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
