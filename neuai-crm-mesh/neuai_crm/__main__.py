"""
Entry point for running NeuAI CRM Data Mesh as a module.

Usage:
    python -m neuai_crm serve --port 8080
    python -m neuai_crm translate --from salesforce --to dynamics365 --file data.json
    python -m neuai_crm query "How many contacts are in each CRM?"
"""

from neuai_crm.cli.commands import main

if __name__ == "__main__":
    main()
