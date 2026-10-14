# Solo-founder operator toolkit

The existing [SKILL.md](SKILL.md) remains the general workflow. This extension supplies a [one-person operating playbook](references/solo-operator-playbook.md), [source notes](references/solo-operator-sources.md), and an [offline constraint calculator](scripts/assess_constraints.py).

Use the playbook explicitly alongside the skill for capacity allocation, support triage, automation payback, cash break-even versus owner income, first-user distribution, incident recovery and scoped source delivery. The core SKILL.md was not modified by this extension; automatic loading of the new playbook is not established.

## Read and run

The playbook includes one decision card, ten conditional operating choices and one incident/recovery notebook. Its procedures are proposals and research adaptations, not newly verified personal business experience.

From the repository root:

```bash
python3 toris-solo-founder/scripts/assess_constraints.py toris-solo-founder/examples/solo-project.json
```

The [bundled input](examples/solo-project.json) is synthetic. The calculator reads only the named file (or standard input), prints JSON and performs no network, configuration or file-write operations. Numeric unknowns remain null. All recurring values share a period and all monetary inputs share one currency label; it does not convert units or verify the input source.

Its arithmetic separates operating capacity, cash costs, an additional owner-income target and automation maintenance. Results are scenarios, not verified profit, demand, growth or recovery capability. The [playbook](references/solo-operator-playbook.md) defines fields, formulas, caveats and acceptance evidence.

## Verification

```bash
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s scripts -p 'test_solo_constraints.py'
```

Run the repository-wide tests as well before delivery. Structural and scalar tests do not prove native agent behavior or production readiness. Private project inputs belong outside distributed skill files.
