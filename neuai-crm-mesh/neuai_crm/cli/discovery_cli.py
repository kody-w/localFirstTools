"""
Schema Discovery CLI - Automatic schema extraction and audit workflow.

Commands:
  discover   - Pull metadata from live CRMs
  propose    - Generate mapping proposals
  audit      - Interactive audit of proposals
  approve    - Approve proposals
  export     - Export approved mappings
"""

import argparse
import json
import sys
import os
from typing import Optional

from neuai_crm.services.schema_discovery import (
    schema_discovery, AuditStatus, MappingProposal
)


# ANSI colors
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'


def c(text: str, color: str) -> str:
    return f"{color}{text}{Colors.ENDC}"


def print_header(text: str):
    print()
    print(c("=" * 70, Colors.BLUE))
    print(c(f"  {text}", Colors.BOLD + Colors.BLUE))
    print(c("=" * 70, Colors.BLUE))
    print()


def print_subheader(text: str):
    print()
    print(c(f"── {text} ", Colors.CYAN) + c("─" * (65 - len(text)), Colors.DIM))
    print()


def confidence_color(conf: float) -> str:
    if conf >= 0.9:
        return Colors.GREEN
    elif conf >= 0.7:
        return Colors.CYAN
    elif conf >= 0.5:
        return Colors.YELLOW
    return Colors.RED


def print_proposal(p: MappingProposal, show_details: bool = True):
    """Pretty print a mapping proposal."""
    conf_col = confidence_color(p.confidence)

    status_icons = {
        AuditStatus.PENDING: c("⏳ PENDING", Colors.YELLOW),
        AuditStatus.APPROVED: c("✓ APPROVED", Colors.GREEN),
        AuditStatus.REJECTED: c("✗ REJECTED", Colors.RED),
        AuditStatus.MODIFIED: c("✎ MODIFIED", Colors.CYAN),
        AuditStatus.AUTO_APPROVED: c("⚡ AUTO", Colors.GREEN),
    }

    print(f"  {c('ID:', Colors.DIM)} {p.id}")
    print(f"  {c(p.source_platform, Colors.YELLOW)}.{c(p.source_entity, Colors.DIM)}.{c(p.source_field.name, Colors.BOLD)}")
    print(f"    {c('↓', Colors.DIM)}")

    if p.target_field:
        print(f"  {c(p.target_platform, Colors.GREEN)}.{c(p.target_entity, Colors.DIM)}.{c(p.target_field.name, Colors.BOLD)}")
    else:
        print(f"  {c('No mapping found', Colors.RED)}")

    print(f"  {c('Confidence:', Colors.DIM)} {c(f'{p.confidence:.0%}', conf_col)}  |  {status_icons[p.status]}")

    if show_details:
        print(f"  {c('Field Type:', Colors.DIM)} {p.source_field.field_type.value}")
        if p.source_field.required:
            print(f"  {c('Required:', Colors.DIM)} Yes")

        if p.reasoning:
            print(f"  {c('AI Reasoning:', Colors.DIM)}")
            for r in p.reasoning[:3]:
                print(f"    • {r}")

        if p.alternatives:
            print(f"  {c('Alternatives:', Colors.DIM)}")
            for alt_name, alt_conf in p.alternatives[:3]:
                print(f"    • {alt_name} ({alt_conf:.0%})")

        if p.value_mappings:
            print(f"  {c('Value Mappings:', Colors.DIM)} {len(p.value_mappings)} values")

    print()


# =============================================================================
# COMMANDS
# =============================================================================

def cmd_discover(args):
    """Discover schema from live CRM."""
    print_header(f"DISCOVERING {args.platform.upper()} SCHEMA")

    if args.platform == "salesforce":
        if not args.mock:
            try:
                from simple_salesforce import Salesforce
                from dotenv import load_dotenv
                load_dotenv()

                print("  Connecting to Salesforce...")
                sf = Salesforce(
                    username=os.getenv('SALESFORCE_USERNAME'),
                    password=os.getenv('SALESFORCE_PASSWORD') + os.getenv('SALESFORCE_SECURITY_TOKEN', ''),
                    consumer_key=os.getenv('SALESFORCE_CLIENT_ID'),
                    consumer_secret=os.getenv('SALESFORCE_CLIENT_SECRET'),
                    domain=os.getenv('SALESFORCE_DOMAIN', 'login')
                )
                print(c(f"  ✓ Connected to {sf.sf_instance}", Colors.GREEN))
                print()

                print("  Discovering objects and fields...")
                result = schema_discovery.discover_salesforce(sf)

                print()
                print(c("  DISCOVERY COMPLETE", Colors.GREEN + Colors.BOLD))
                print(f"  • Entities discovered: {result.entities_discovered}")
                print(f"  • Fields discovered: {result.fields_discovered}")
                print(f"  • Custom fields: {result.custom_fields}")
                print(f"  • Duration: {result.duration_seconds:.1f}s")

                if result.errors:
                    print(c(f"\n  Errors ({len(result.errors)}):", Colors.YELLOW))
                    for err in result.errors[:5]:
                        print(f"    • {err}")

            except ImportError:
                print(c("  Error: simple-salesforce not installed", Colors.RED))
                print("  Run: pip install simple-salesforce python-dotenv")
                return
            except Exception as e:
                print(c(f"  Error: {e}", Colors.RED))
                return
        else:
            # Mock discovery for testing
            print("  Using mock Salesforce data...")
            _mock_salesforce_discovery()
            print(c("  ✓ Mock discovery complete", Colors.GREEN))

    elif args.platform == "dynamics365":
        if not args.mock:
            try:
                from msal import ConfidentialClientApplication
                from dotenv import load_dotenv
                load_dotenv()

                print("  Acquiring Dynamics 365 access token...")

                client_id = os.getenv('DYNAMICS_CLIENT_ID')
                client_secret = os.getenv('DYNAMICS_CLIENT_SECRET')
                tenant_id = os.getenv('DYNAMICS_TENANT_ID')
                env_url = os.getenv('DYNAMICS_ENVIRONMENT_URL', '').rstrip('/')

                app = ConfidentialClientApplication(
                    client_id=client_id,
                    client_credential=client_secret,
                    authority=f"https://login.microsoftonline.com/{tenant_id}"
                )

                token_result = app.acquire_token_for_client(scopes=[f"{env_url}/.default"])

                if 'access_token' not in token_result:
                    print(c(f"  Error: {token_result.get('error_description', 'Token acquisition failed')}", Colors.RED))
                    return

                print(c("  ✓ Token acquired", Colors.GREEN))
                print()

                print("  Discovering entities and attributes...")
                result = schema_discovery.discover_dynamics365(token_result['access_token'], env_url)

                print()
                print(c("  DISCOVERY COMPLETE", Colors.GREEN + Colors.BOLD))
                print(f"  • Entities discovered: {result.entities_discovered}")
                print(f"  • Fields discovered: {result.fields_discovered}")
                print(f"  • Custom fields: {result.custom_fields}")
                print(f"  • Duration: {result.duration_seconds:.1f}s")

                if result.errors:
                    print(c(f"\n  Errors ({len(result.errors)}):", Colors.YELLOW))
                    for err in result.errors[:5]:
                        print(f"    • {err}")

            except ImportError:
                print(c("  Error: msal not installed", Colors.RED))
                print("  Run: pip install msal python-dotenv")
                return
            except Exception as e:
                print(c(f"  Error: {e}", Colors.RED))
                return
        else:
            # Mock discovery for testing
            print("  Using mock Dynamics 365 data...")
            _mock_dynamics_discovery()
            print(c("  ✓ Mock discovery complete", Colors.GREEN))


def cmd_propose(args):
    """Generate mapping proposals between platforms."""
    print_header("GENERATING MAPPING PROPOSALS")

    source = args.source
    target = args.target

    print(f"  Source: {c(source, Colors.YELLOW)}")
    print(f"  Target: {c(target, Colors.GREEN)}")
    print(f"  Auto-approve threshold: {args.threshold}")
    print()

    # Check if we have schemas
    if not schema_discovery.schemas.get(source):
        print(c(f"  Error: No schema discovered for {source}", Colors.RED))
        print(f"  Run: python -m neuai_crm.cli.discovery_cli discover {source}")
        return

    if not schema_discovery.schemas.get(target):
        print(c(f"  Error: No schema discovered for {target}", Colors.RED))
        print(f"  Run: python -m neuai_crm.cli.discovery_cli discover {target}")
        return

    print("  Analyzing schemas and generating proposals...")
    proposals = schema_discovery.generate_mapping_proposals(
        source, target, auto_approve_threshold=args.threshold
    )

    # Summarize
    auto_approved = len([p for p in proposals if p.status == AuditStatus.AUTO_APPROVED])
    pending = len([p for p in proposals if p.status == AuditStatus.PENDING])
    no_match = len([p for p in proposals if p.target_field is None])

    print()
    print(c("  PROPOSAL GENERATION COMPLETE", Colors.GREEN + Colors.BOLD))
    print(f"  • Total proposals: {len(proposals)}")
    print(f"  • {c(f'Auto-approved (>{args.threshold:.0%}):', Colors.GREEN)} {auto_approved}")
    print(f"  • {c('Pending audit:', Colors.YELLOW)} {pending}")
    print(f"  • {c('No match found:', Colors.RED)} {no_match}")

    if pending > 0:
        print()
        print(f"  Run {c('audit', Colors.CYAN)} to review pending proposals.")


def cmd_audit(args):
    """Interactive audit of pending proposals."""
    print_header("AUDIT MAPPING PROPOSALS")

    pending = schema_discovery.get_audit_queue(AuditStatus.PENDING)

    if not pending:
        print(c("  ✓ No proposals pending audit!", Colors.GREEN))
        summary = schema_discovery.get_audit_summary()
        print(f"  • Auto-approved: {summary['auto_approved']}")
        print(f"  • Human-approved: {summary['human_approved']}")
        return

    # Sort by confidence (lowest first - need most attention)
    pending.sort(key=lambda x: x.confidence)

    print(f"  Found {c(str(len(pending)), Colors.YELLOW)} proposals pending audit.")
    print()
    print("  For each proposal:")
    print("    [a] Approve - AI got it right")
    print("    [r] Reject - This field shouldn't be mapped")
    print("    [m] Modify - Map to a different field")
    print("    [s] Skip - Review later")
    print("    [b] Bulk approve all above threshold")
    print("    [q] Quit")
    print()

    reviewed = 0
    for i, p in enumerate(pending):
        print_subheader(f"Proposal {i + 1}/{len(pending)}")
        print_proposal(p, show_details=True)

        while True:
            response = input(c("  [a]pprove / [r]eject / [m]odify / [s]kip / [b]ulk / [q]uit: ", Colors.BOLD)).lower().strip()

            if response == 'a':
                notes = input("  Notes (optional): ").strip()
                schema_discovery.approve_proposal(p.id, notes=notes or None)
                print(c("  ✓ Approved!", Colors.GREEN))
                reviewed += 1
                break

            elif response == 'r':
                notes = input("  Reason for rejection: ").strip()
                schema_discovery.reject_proposal(p.id, notes=notes or None)
                print(c("  ✗ Rejected.", Colors.RED))
                reviewed += 1
                break

            elif response == 'm':
                new_field = input("  Enter correct target field name: ").strip()
                if new_field:
                    notes = input("  Notes (optional): ").strip()
                    schema_discovery.modify_proposal(p.id, new_field, notes=notes or None)
                    print(c(f"  ✓ Modified to: {new_field}", Colors.CYAN))
                    reviewed += 1
                    break
                else:
                    print(c("  Please enter a field name.", Colors.RED))

            elif response == 's':
                print(c("  → Skipped", Colors.YELLOW))
                break

            elif response == 'b':
                threshold = float(input("  Minimum confidence for bulk approve (0.0-1.0): ").strip() or "0.85")
                count = schema_discovery.bulk_approve(threshold)
                print(c(f"  ✓ Bulk approved {count} proposals", Colors.GREEN))
                # Refresh pending list
                pending = schema_discovery.get_audit_queue(AuditStatus.PENDING)
                if not pending:
                    print(c("\n  All proposals reviewed!", Colors.GREEN))
                    return
                break

            elif response == 'q':
                print()
                print(f"  Reviewed {reviewed} proposals.")
                return

            else:
                print(c("  Invalid option.", Colors.RED))

    print()
    print(c(f"  ✓ Audit complete! Reviewed {reviewed} proposals.", Colors.GREEN))


def cmd_status(args):
    """Show discovery and audit status."""
    print_header("SCHEMA DISCOVERY STATUS")

    # Schema status
    print_subheader("Discovered Schemas")
    for platform, entities in schema_discovery.schemas.items():
        if entities:
            total_fields = sum(len(fields) for fields in entities.values())
            print(f"  {c(platform, Colors.CYAN)}: {len(entities)} entities, {total_fields} fields")
        else:
            print(f"  {c(platform, Colors.DIM)}: Not discovered")

    # Audit queue status
    print_subheader("Audit Queue")
    summary = schema_discovery.get_audit_summary()

    print(f"  Pending review: {c(str(summary['total_pending']), Colors.YELLOW)}")
    print(f"    • High confidence (>80%): {summary['by_confidence']['high']}")
    print(f"    • Medium confidence (60-80%): {summary['by_confidence']['medium']}")
    print(f"    • Low confidence (<60%): {summary['by_confidence']['low']}")

    print()
    print(f"  Auto-approved: {c(str(summary['auto_approved']), Colors.GREEN)}")
    print(f"  Human-approved: {c(str(summary['human_approved']), Colors.GREEN)}")

    # Discovery history
    if schema_discovery.discovery_history:
        print_subheader("Recent Discovery History")
        for h in schema_discovery.discovery_history[-5:]:
            print(f"  {h.timestamp[:16]} | {h.platform} | {h.entities_discovered} entities, {h.fields_discovered} fields")


def cmd_export(args):
    """Export approved mappings."""
    print_header("EXPORT APPROVED MAPPINGS")

    export_data = schema_discovery.export_approved_mappings()

    print(f"  Total mappings: {export_data['total_mappings']}")

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(export_data, f, indent=2)
        print(f"  Exported to: {c(args.output, Colors.GREEN)}")
    else:
        print()
        print(json.dumps(export_data, indent=2))


def cmd_list(args):
    """List proposals in audit queue."""
    print_header("AUDIT QUEUE")

    status_filter = AuditStatus(args.status) if args.status else None
    proposals = schema_discovery.get_audit_queue(status_filter)

    if args.entity:
        proposals = [p for p in proposals if p.source_entity.lower() == args.entity.lower()]

    if not proposals:
        print(c("  No proposals match the filter.", Colors.DIM))
        return

    print(f"  Showing {len(proposals)} proposals")
    if status_filter:
        print(f"  Filtered by status: {status_filter.value}")
    if args.entity:
        print(f"  Filtered by entity: {args.entity}")
    print()

    for p in proposals[:args.limit]:
        print_proposal(p, show_details=args.detailed)


# =============================================================================
# MOCK DATA FOR TESTING
# =============================================================================

def _mock_salesforce_discovery():
    """Create mock Salesforce schema for testing."""
    from neuai_crm.services.schema_discovery import FieldMetadata, FieldType

    account_fields = [
        FieldMetadata(name="Id", label="Account ID", field_type=FieldType.ID, platform="salesforce", entity="account", api_name="Id"),
        FieldMetadata(name="Name", label="Account Name", field_type=FieldType.STRING, platform="salesforce", entity="account", required=True, api_name="Name"),
        FieldMetadata(name="Website", label="Website", field_type=FieldType.URL, platform="salesforce", entity="account", api_name="Website"),
        FieldMetadata(name="Phone", label="Phone", field_type=FieldType.PHONE, platform="salesforce", entity="account", api_name="Phone"),
        FieldMetadata(name="Industry", label="Industry", field_type=FieldType.PICKLIST, platform="salesforce", entity="account", picklist_values=["Technology", "Finance", "Healthcare"], api_name="Industry"),
        FieldMetadata(name="Description", label="Description", field_type=FieldType.TEXTAREA, platform="salesforce", entity="account", api_name="Description"),
        FieldMetadata(name="CreatedDate", label="Created Date", field_type=FieldType.DATETIME, platform="salesforce", entity="account", is_system=True, api_name="CreatedDate"),
        FieldMetadata(name="Custom_Rating__c", label="Custom Rating", field_type=FieldType.PICKLIST, platform="salesforce", entity="account", is_custom=True, picklist_values=["Hot", "Warm", "Cold"], api_name="Custom_Rating__c"),
    ]

    contact_fields = [
        FieldMetadata(name="Id", label="Contact ID", field_type=FieldType.ID, platform="salesforce", entity="contact", api_name="Id"),
        FieldMetadata(name="FirstName", label="First Name", field_type=FieldType.STRING, platform="salesforce", entity="contact", api_name="FirstName"),
        FieldMetadata(name="LastName", label="Last Name", field_type=FieldType.STRING, platform="salesforce", entity="contact", required=True, api_name="LastName"),
        FieldMetadata(name="Email", label="Email", field_type=FieldType.EMAIL, platform="salesforce", entity="contact", api_name="Email"),
        FieldMetadata(name="Phone", label="Phone", field_type=FieldType.PHONE, platform="salesforce", entity="contact", api_name="Phone"),
        FieldMetadata(name="Title", label="Title", field_type=FieldType.STRING, platform="salesforce", entity="contact", api_name="Title"),
        FieldMetadata(name="AccountId", label="Account ID", field_type=FieldType.REFERENCE, platform="salesforce", entity="contact", reference_to="Account", api_name="AccountId"),
    ]

    opportunity_fields = [
        FieldMetadata(name="Id", label="Opportunity ID", field_type=FieldType.ID, platform="salesforce", entity="opportunity", api_name="Id"),
        FieldMetadata(name="Name", label="Opportunity Name", field_type=FieldType.STRING, platform="salesforce", entity="opportunity", required=True, api_name="Name"),
        FieldMetadata(name="Amount", label="Amount", field_type=FieldType.CURRENCY, platform="salesforce", entity="opportunity", api_name="Amount"),
        FieldMetadata(name="StageName", label="Stage", field_type=FieldType.PICKLIST, platform="salesforce", entity="opportunity", picklist_values=["Prospecting", "Qualification", "Proposal", "Closed Won", "Closed Lost"], api_name="StageName"),
        FieldMetadata(name="CloseDate", label="Close Date", field_type=FieldType.DATE, platform="salesforce", entity="opportunity", required=True, api_name="CloseDate"),
        FieldMetadata(name="Probability", label="Probability (%)", field_type=FieldType.DECIMAL, platform="salesforce", entity="opportunity", api_name="Probability"),
        FieldMetadata(name="AccountId", label="Account ID", field_type=FieldType.REFERENCE, platform="salesforce", entity="opportunity", reference_to="Account", api_name="AccountId"),
    ]

    schema_discovery.schemas["salesforce"] = {
        "account": account_fields,
        "contact": contact_fields,
        "opportunity": opportunity_fields,
    }
    schema_discovery._save_state()


def _mock_dynamics_discovery():
    """Create mock Dynamics 365 schema for testing."""
    from neuai_crm.services.schema_discovery import FieldMetadata, FieldType

    account_fields = [
        FieldMetadata(name="accountid", label="Account", field_type=FieldType.ID, platform="dynamics365", entity="account", api_name="accountid"),
        FieldMetadata(name="name", label="Account Name", field_type=FieldType.STRING, platform="dynamics365", entity="account", required=True, api_name="name"),
        FieldMetadata(name="websiteurl", label="Website", field_type=FieldType.URL, platform="dynamics365", entity="account", api_name="websiteurl"),
        FieldMetadata(name="telephone1", label="Main Phone", field_type=FieldType.PHONE, platform="dynamics365", entity="account", api_name="telephone1"),
        FieldMetadata(name="industrycode", label="Industry", field_type=FieldType.PICKLIST, platform="dynamics365", entity="account", api_name="industrycode"),
        FieldMetadata(name="description", label="Description", field_type=FieldType.TEXTAREA, platform="dynamics365", entity="account", api_name="description"),
        FieldMetadata(name="createdon", label="Created On", field_type=FieldType.DATETIME, platform="dynamics365", entity="account", is_system=True, api_name="createdon"),
        FieldMetadata(name="new_rating", label="Rating", field_type=FieldType.PICKLIST, platform="dynamics365", entity="account", is_custom=True, api_name="new_rating"),
    ]

    contact_fields = [
        FieldMetadata(name="contactid", label="Contact", field_type=FieldType.ID, platform="dynamics365", entity="contact", api_name="contactid"),
        FieldMetadata(name="firstname", label="First Name", field_type=FieldType.STRING, platform="dynamics365", entity="contact", api_name="firstname"),
        FieldMetadata(name="lastname", label="Last Name", field_type=FieldType.STRING, platform="dynamics365", entity="contact", required=True, api_name="lastname"),
        FieldMetadata(name="emailaddress1", label="Email", field_type=FieldType.EMAIL, platform="dynamics365", entity="contact", api_name="emailaddress1"),
        FieldMetadata(name="telephone1", label="Business Phone", field_type=FieldType.PHONE, platform="dynamics365", entity="contact", api_name="telephone1"),
        FieldMetadata(name="jobtitle", label="Job Title", field_type=FieldType.STRING, platform="dynamics365", entity="contact", api_name="jobtitle"),
        FieldMetadata(name="parentcustomerid", label="Company Name", field_type=FieldType.REFERENCE, platform="dynamics365", entity="contact", reference_to="account", api_name="parentcustomerid"),
    ]

    opportunity_fields = [
        FieldMetadata(name="opportunityid", label="Opportunity", field_type=FieldType.ID, platform="dynamics365", entity="opportunity", api_name="opportunityid"),
        FieldMetadata(name="name", label="Topic", field_type=FieldType.STRING, platform="dynamics365", entity="opportunity", required=True, api_name="name"),
        FieldMetadata(name="estimatedvalue", label="Est. Revenue", field_type=FieldType.CURRENCY, platform="dynamics365", entity="opportunity", api_name="estimatedvalue"),
        FieldMetadata(name="stepname", label="Sales Stage", field_type=FieldType.STRING, platform="dynamics365", entity="opportunity", api_name="stepname"),
        FieldMetadata(name="estimatedclosedate", label="Est. Close Date", field_type=FieldType.DATE, platform="dynamics365", entity="opportunity", api_name="estimatedclosedate"),
        FieldMetadata(name="closeprobability", label="Probability", field_type=FieldType.DECIMAL, platform="dynamics365", entity="opportunity", api_name="closeprobability"),
        FieldMetadata(name="parentaccountid", label="Account", field_type=FieldType.REFERENCE, platform="dynamics365", entity="opportunity", reference_to="account", api_name="parentaccountid"),
    ]

    schema_discovery.schemas["dynamics365"] = {
        "account": account_fields,
        "contact": contact_fields,
        "opportunity": opportunity_fields,
    }
    schema_discovery._save_state()


# =============================================================================
# MAIN
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Schema Discovery - Auto-extract schemas and generate mapping proposals",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
WORKFLOW:

  1. DISCOVER - Pull metadata from live CRMs
     $ python -m neuai_crm.cli.discovery_cli discover salesforce
     $ python -m neuai_crm.cli.discovery_cli discover dynamics365

  2. PROPOSE - Generate mapping proposals (AI does the work)
     $ python -m neuai_crm.cli.discovery_cli propose --source salesforce --target dynamics365

  3. AUDIT - Review and approve proposals (Human audits AI's work)
     $ python -m neuai_crm.cli.discovery_cli audit

  4. EXPORT - Export approved mappings
     $ python -m neuai_crm.cli.discovery_cli export -o mappings.json

The AI proposes, you audit. Not the other way around!
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # Discover
    discover_parser = subparsers.add_parser("discover", help="Discover schema from live CRM")
    discover_parser.add_argument("platform", choices=["salesforce", "dynamics365"])
    discover_parser.add_argument("--mock", action="store_true", help="Use mock data for testing")

    # Propose
    propose_parser = subparsers.add_parser("propose", help="Generate mapping proposals")
    propose_parser.add_argument("--source", "-s", required=True, choices=["salesforce", "dynamics365", "local"])
    propose_parser.add_argument("--target", "-t", required=True, choices=["salesforce", "dynamics365", "local"])
    propose_parser.add_argument("--threshold", type=float, default=0.95, help="Auto-approve threshold (default: 0.95)")

    # Audit
    subparsers.add_parser("audit", help="Interactive audit of proposals")

    # Status
    subparsers.add_parser("status", help="Show discovery and audit status")

    # Export
    export_parser = subparsers.add_parser("export", help="Export approved mappings")
    export_parser.add_argument("-o", "--output", help="Output file (stdout if not specified)")

    # List
    list_parser = subparsers.add_parser("list", help="List proposals")
    list_parser.add_argument("--status", choices=["pending", "approved", "rejected", "modified", "auto"])
    list_parser.add_argument("--entity", help="Filter by entity")
    list_parser.add_argument("--limit", "-n", type=int, default=20)
    list_parser.add_argument("--detailed", "-d", action="store_true")

    args = parser.parse_args()

    if args.command == "discover":
        cmd_discover(args)
    elif args.command == "propose":
        cmd_propose(args)
    elif args.command == "audit":
        cmd_audit(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "export":
        cmd_export(args)
    elif args.command == "list":
        cmd_list(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
