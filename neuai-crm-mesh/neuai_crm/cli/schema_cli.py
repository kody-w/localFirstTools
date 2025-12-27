"""
Interactive CLI for Schema Brain - Human-in-the-Loop Learning Interface

This provides an interactive way to:
1. Review proposed mappings
2. Correct wrong inferences
3. Teach new mappings
4. Monitor learning progress
"""

import argparse
import json
import sys
from typing import Dict, List, Optional
from pathlib import Path

from neuai_crm.services.schema_brain import (
    SchemaBrain, schema_brain,
    ConfidenceLevel, MappingSource
)
from neuai_crm.models.schemas import Platform


# ANSI color codes for pretty output
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


def colorize(text: str, color: str) -> str:
    """Add color to text."""
    return f"{color}{text}{Colors.ENDC}"


def confidence_color(confidence: float) -> str:
    """Get color based on confidence level."""
    if confidence >= 0.95:
        return Colors.GREEN
    elif confidence >= 0.80:
        return Colors.CYAN
    elif confidence >= 0.60:
        return Colors.YELLOW
    elif confidence >= 0.40:
        return Colors.RED
    return Colors.RED + Colors.BOLD


def print_header(text: str):
    """Print a styled header."""
    print()
    print(colorize("=" * 60, Colors.BLUE))
    print(colorize(f"  {text}", Colors.BOLD + Colors.BLUE))
    print(colorize("=" * 60, Colors.BLUE))
    print()


def print_subheader(text: str):
    """Print a styled subheader."""
    print()
    print(colorize(f"── {text} ", Colors.CYAN) + colorize("─" * (55 - len(text)), Colors.DIM))
    print()


def print_mapping(mapping: Dict, show_details: bool = False):
    """Pretty print a field mapping."""
    conf = mapping.get('confidence', 0)
    conf_color = confidence_color(conf)

    source = f"{mapping['source_platform']}.{mapping['source_field']}"
    target = f"{mapping['target_platform']}.{mapping['target_field']}"

    print(f"  {colorize(source, Colors.YELLOW)} → {colorize(target, Colors.GREEN)}")
    print(f"  {colorize('Confidence:', Colors.DIM)} {colorize(f'{conf:.0%}', conf_color)}")
    print(f"  {colorize('Entity:', Colors.DIM)} {mapping['entity_type']}")
    print(f"  {colorize('Source:', Colors.DIM)} {mapping['source']}")

    if show_details:
        if mapping.get('times_used'):
            print(f"  {colorize('Used:', Colors.DIM)} {mapping['times_used']} times")
        if mapping.get('times_corrected'):
            print(f"  {colorize('Corrected:', Colors.DIM)} {mapping['times_corrected']} times")
        if mapping.get('inference_reasons'):
            print(f"  {colorize('Inference reasons:', Colors.DIM)}")
            for reason in mapping['inference_reasons']:
                print(f"    - {reason}")
        if mapping.get('notes'):
            print(f"  {colorize('Notes:', Colors.DIM)} {mapping['notes']}")

    print()


# =============================================================================
# CLI COMMANDS
# =============================================================================

def cmd_status(args):
    """Show Schema Brain status and statistics."""
    print_header("SCHEMA BRAIN STATUS")

    report = schema_brain.generate_report()
    print(report)


def cmd_review(args):
    """Interactive review of pending mappings."""
    print_header("INTERACTIVE MAPPING REVIEW")

    pending = schema_brain.get_pending_reviews()

    if not pending:
        print(colorize("  ✓ No mappings need review! All mappings are confident.", Colors.GREEN))
        return

    print(f"  Found {colorize(str(len(pending)), Colors.YELLOW)} mappings needing review.")
    print()
    print("  For each mapping, you can:")
    print("    [c] Confirm - the mapping is correct")
    print("    [r] Reject - the mapping is wrong (will be removed)")
    print("    [f] Fix - provide the correct mapping")
    print("    [s] Skip - review later")
    print("    [q] Quit - stop reviewing")
    print()

    reviewed = 0
    for item in pending:
        mapping = item['mapping']
        print_subheader(f"Review {reviewed + 1}/{len(pending)}")
        print_mapping(mapping, show_details=True)

        if item.get('reasons'):
            print(f"  {colorize('Why this was proposed:', Colors.DIM)}")
            for reason in item.get('reasons', []):
                print(f"    • {reason}")
            print()

        while True:
            response = input(colorize("  [c]onfirm / [r]eject / [f]ix / [s]kip / [q]uit: ", Colors.BOLD)).lower().strip()

            if response == 'c':
                schema_brain.confirm_mapping(
                    mapping['source_platform'],
                    mapping['source_field'],
                    mapping['target_platform'],
                    mapping['entity_type']
                )
                print(colorize("  ✓ Mapping confirmed!", Colors.GREEN))
                reviewed += 1
                break

            elif response == 'r':
                reason = input("  Reason for rejection (optional): ").strip()
                schema_brain.reject_mapping(
                    mapping['source_platform'],
                    mapping['source_field'],
                    mapping['target_platform'],
                    mapping['entity_type'],
                    reason or None
                )
                print(colorize("  ✗ Mapping rejected.", Colors.RED))
                reviewed += 1
                break

            elif response == 'f':
                correct = input("  Enter correct target field: ").strip()
                if correct:
                    notes = input("  Notes (optional): ").strip()
                    schema_brain.provide_feedback(
                        mapping['source_platform'],
                        mapping['source_field'],
                        mapping['target_platform'],
                        mapping['entity_type'],
                        correct,
                        notes=notes or None
                    )
                    print(colorize(f"  ✓ Mapping updated to: {correct}", Colors.GREEN))
                    reviewed += 1
                    break
                else:
                    print(colorize("  Please enter a valid field name.", Colors.RED))

            elif response == 's':
                print(colorize("  → Skipped", Colors.YELLOW))
                break

            elif response == 'q':
                print()
                print(f"  Reviewed {reviewed} mappings.")
                return

            else:
                print(colorize("  Invalid option. Try again.", Colors.RED))

    print()
    print(colorize(f"  ✓ Review complete! Reviewed {reviewed} mappings.", Colors.GREEN))


def cmd_teach(args):
    """Teach the Schema Brain a new mapping."""
    print_header("TEACH NEW MAPPING")

    print("  Teach the Schema Brain a new field mapping.")
    print()

    # Get platforms
    print("  Available platforms: salesforce, dynamics365, local")
    source_platform = input("  Source platform: ").strip().lower()
    if source_platform not in ['salesforce', 'dynamics365', 'local']:
        print(colorize("  Invalid platform.", Colors.RED))
        return

    target_platform = input("  Target platform: ").strip().lower()
    if target_platform not in ['salesforce', 'dynamics365', 'local']:
        print(colorize("  Invalid platform.", Colors.RED))
        return

    if source_platform == target_platform:
        print(colorize("  Source and target must be different.", Colors.RED))
        return

    # Get entity type
    print()
    print("  Entity types: contacts, companies, deals, activities")
    entity_type = input("  Entity type: ").strip().lower()
    if entity_type not in ['contacts', 'companies', 'deals', 'activities']:
        print(colorize("  Invalid entity type.", Colors.RED))
        return

    # Get fields
    print()
    source_field = input("  Source field name: ").strip()
    target_field = input("  Target field name: ").strip()

    if not source_field or not target_field:
        print(colorize("  Field names cannot be empty.", Colors.RED))
        return

    # Optional notes
    notes = input("  Notes (optional): ").strip()

    # Confirm
    print()
    print(f"  Create mapping:")
    print(f"    {source_platform}.{source_field} → {target_platform}.{target_field}")
    print(f"    Entity: {entity_type}")

    confirm = input("  Confirm? [y/n]: ").strip().lower()

    if confirm == 'y':
        mapping = schema_brain.provide_feedback(
            source_platform,
            source_field,
            target_platform,
            entity_type,
            target_field,
            notes=notes or None
        )
        print()
        print(colorize("  ✓ Mapping created successfully!", Colors.GREEN))
        print()
        print_mapping(mapping.to_dict())
    else:
        print(colorize("  Cancelled.", Colors.YELLOW))


def cmd_analyze(args):
    """Analyze a JSON file and propose mappings for unknown fields."""
    print_header("ANALYZE RECORD FILE")

    filepath = args.file
    source_platform = Platform(args.source)
    target_platform = Platform(args.target)
    entity_type = args.entity

    print(f"  File: {filepath}")
    print(f"  Source: {source_platform.value}")
    print(f"  Target: {target_platform.value}")
    print(f"  Entity: {entity_type}")
    print()

    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(colorize(f"  Error loading file: {e}", Colors.RED))
        return

    # Handle both single records and arrays
    records = data if isinstance(data, list) else [data]

    # Get unique fields from all records
    all_fields = set()
    for record in records:
        all_fields.update(record.keys())

    print(f"  Found {len(all_fields)} unique fields in {len(records)} records.")
    print()

    # Analyze a sample record
    sample_record = records[0] if records else {}
    proposals = schema_brain.analyze_record(
        sample_record, source_platform, target_platform, entity_type
    )

    if not proposals:
        print(colorize("  ✓ All fields have known mappings!", Colors.GREEN))
        return

    print_subheader("Unknown Fields & Proposals")

    for field_name, inference in proposals.items():
        print(f"  {colorize(field_name, Colors.YELLOW)}")

        if inference.proposed_mapping:
            conf_color = confidence_color(inference.confidence)
            print(f"    Proposed: {colorize(inference.proposed_mapping, Colors.GREEN)}")
            print(f"    Confidence: {colorize(f'{inference.confidence:.0%}', conf_color)}")

            if inference.reasons:
                print(f"    Reasons:")
                for reason in inference.reasons[:3]:
                    print(f"      • {reason}")

            if inference.alternatives:
                print(f"    Alternatives:")
                for alt_field, alt_conf in inference.alternatives[:3]:
                    print(f"      • {alt_field} ({alt_conf:.0%})")

            if inference.needs_human_review:
                print(colorize("    ⚠ Needs human review", Colors.YELLOW))
        else:
            print(colorize("    ✗ Could not propose mapping", Colors.RED))
            print("    → Use 'schema teach' to add manually")

        print()

    # Offer to accept all proposals
    print()
    accept_all = input("  Accept all proposals above threshold? [y/n]: ").strip().lower()

    if accept_all == 'y':
        threshold = float(input("  Minimum confidence threshold (0.0-1.0, default 0.7): ").strip() or "0.7")
        accepted = 0

        for field_name, inference in proposals.items():
            if inference.proposed_mapping and inference.confidence >= threshold:
                schema_brain.provide_feedback(
                    source_platform.value,
                    field_name,
                    target_platform.value,
                    entity_type,
                    inference.proposed_mapping,
                    notes="Auto-accepted from analysis"
                )
                accepted += 1

        print()
        print(colorize(f"  ✓ Accepted {accepted} mappings.", Colors.GREEN))


def cmd_export(args):
    """Export learned mappings."""
    print_header("EXPORT MAPPINGS")

    format_type = args.format or "markdown"
    output = schema_brain.export_mappings(format_type)

    if args.output:
        with open(args.output, 'w') as f:
            f.write(output)
        print(f"  Exported to: {args.output}")
    else:
        print(output)


def cmd_list(args):
    """List all mappings with optional filters."""
    print_header("ALL MAPPINGS")

    mappings = []
    for key, m in schema_brain.field_mappings.items():
        # Apply filters
        if args.entity and m.entity_type != args.entity:
            continue
        if args.source and m.source.value != args.source:
            continue
        if args.confidence:
            if m.confidence < float(args.confidence):
                continue

        mappings.append(m.to_dict())

    # Sort by confidence
    mappings.sort(key=lambda x: x['confidence'], reverse=True)

    print(f"  Showing {len(mappings)} mappings")
    if args.entity:
        print(f"  Filtered by entity: {args.entity}")
    if args.source:
        print(f"  Filtered by source: {args.source}")
    if args.confidence:
        print(f"  Minimum confidence: {args.confidence}")
    print()

    for mapping in mappings[:args.limit or 50]:
        print_mapping(mapping, show_details=args.detailed)

    if len(mappings) > (args.limit or 50):
        print(f"  ... and {len(mappings) - (args.limit or 50)} more. Use --limit to show more.")


def cmd_forget(args):
    """Remove a learned mapping."""
    print_header("FORGET MAPPING")

    source_platform = args.source_platform
    source_field = args.source_field
    target_platform = args.target_platform
    entity_type = args.entity

    key = schema_brain._mapping_key(
        source_platform, source_field, target_platform, entity_type
    )

    if key in schema_brain.field_mappings:
        mapping = schema_brain.field_mappings[key]

        if mapping.source == MappingSource.BUILTIN:
            print(colorize("  Cannot forget builtin mappings.", Colors.RED))
            return

        print("  Mapping to forget:")
        print_mapping(mapping.to_dict())

        confirm = input("  Confirm deletion? [y/n]: ").strip().lower()

        if confirm == 'y':
            del schema_brain.field_mappings[key]
            schema_brain._save_memory()
            print(colorize("  ✓ Mapping forgotten.", Colors.GREEN))
        else:
            print(colorize("  Cancelled.", Colors.YELLOW))
    else:
        print(colorize("  Mapping not found.", Colors.RED))


def cmd_simulate(args):
    """Simulate translating a record to see what would happen."""
    print_header("SIMULATE TRANSLATION")

    filepath = args.file
    source_platform = Platform(args.source)
    target_platform = Platform(args.target)
    entity_type = args.entity

    try:
        with open(filepath, 'r') as f:
            record = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(colorize(f"  Error loading file: {e}", Colors.RED))
        return

    if isinstance(record, list):
        record = record[0]

    print(f"  Source: {source_platform.value}")
    print(f"  Target: {target_platform.value}")
    print(f"  Entity: {entity_type}")
    print()

    print_subheader("Original Record")
    for field, value in record.items():
        print(f"  {colorize(field, Colors.CYAN)}: {value}")

    print_subheader("Translation Simulation")

    translated = {}
    issues = []

    for field_name, value in record.items():
        result = schema_brain.translate_field(
            field_name, source_platform, target_platform, entity_type, record
        )
        target_field, confidence, needs_review = result

        if target_field:
            # Also translate value if needed
            new_value, val_conf = schema_brain.translate_value(
                value, field_name, source_platform, target_platform, entity_type
            )

            translated[target_field] = new_value

            conf_color = confidence_color(confidence)
            status = ""
            if needs_review:
                status = colorize(" ⚠", Colors.YELLOW)
            elif confidence >= 0.95:
                status = colorize(" ✓", Colors.GREEN)

            print(f"  {colorize(field_name, Colors.DIM)} → "
                  f"{colorize(target_field, Colors.GREEN)} "
                  f"[{colorize(f'{confidence:.0%}', conf_color)}]{status}")

            if value != new_value:
                print(f"    Value: {value} → {new_value}")
        else:
            issues.append(field_name)
            print(f"  {colorize(field_name, Colors.RED)} → "
                  f"{colorize('??? (unknown)', Colors.RED)}")

    print_subheader("Translated Record")
    for field, value in translated.items():
        print(f"  {colorize(field, Colors.GREEN)}: {value}")

    if issues:
        print()
        print(colorize(f"  ⚠ {len(issues)} fields could not be translated:", Colors.YELLOW))
        for issue in issues:
            print(f"    • {issue}")
        print()
        print("  Run 'schema teach' to add these mappings.")


# =============================================================================
# MAIN CLI ENTRY POINT
# =============================================================================

def main():
    """Main entry point for schema CLI."""
    parser = argparse.ArgumentParser(
        description="Schema Brain - Self-Improving Schema Translator",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # View current status
  python -m neuai_crm.cli.schema_cli status

  # Interactive review of uncertain mappings
  python -m neuai_crm.cli.schema_cli review

  # Teach a new mapping
  python -m neuai_crm.cli.schema_cli teach

  # Analyze a file for unknown fields
  python -m neuai_crm.cli.schema_cli analyze --file data.json --source salesforce --target dynamics365 --entity contacts

  # Simulate translating a record
  python -m neuai_crm.cli.schema_cli simulate --file record.json --source salesforce --target local --entity deals

  # Export all mappings
  python -m neuai_crm.cli.schema_cli export --format markdown -o mappings.md

  # List mappings with filters
  python -m neuai_crm.cli.schema_cli list --entity contacts --confidence 0.8
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Status command
    subparsers.add_parser("status", help="Show Schema Brain status and statistics")

    # Review command
    subparsers.add_parser("review", help="Interactive review of pending mappings")

    # Teach command
    subparsers.add_parser("teach", help="Teach a new mapping interactively")

    # Analyze command
    analyze_parser = subparsers.add_parser("analyze", help="Analyze a file for unknown fields")
    analyze_parser.add_argument("--file", "-f", required=True, help="JSON file to analyze")
    analyze_parser.add_argument("--source", "-s", required=True,
                               choices=["salesforce", "dynamics365", "local"])
    analyze_parser.add_argument("--target", "-t", required=True,
                               choices=["salesforce", "dynamics365", "local"])
    analyze_parser.add_argument("--entity", "-e", required=True,
                               choices=["contacts", "companies", "deals", "activities"])

    # Export command
    export_parser = subparsers.add_parser("export", help="Export learned mappings")
    export_parser.add_argument("--format", choices=["json", "markdown"], default="markdown")
    export_parser.add_argument("--output", "-o", help="Output file (stdout if not specified)")

    # List command
    list_parser = subparsers.add_parser("list", help="List all mappings")
    list_parser.add_argument("--entity", "-e",
                            choices=["contacts", "companies", "deals", "activities"])
    list_parser.add_argument("--source", choices=["builtin", "inferred", "human", "pattern"])
    list_parser.add_argument("--confidence", "-c", type=float)
    list_parser.add_argument("--limit", "-n", type=int, default=50)
    list_parser.add_argument("--detailed", "-d", action="store_true")

    # Forget command
    forget_parser = subparsers.add_parser("forget", help="Remove a learned mapping")
    forget_parser.add_argument("source_platform")
    forget_parser.add_argument("source_field")
    forget_parser.add_argument("target_platform")
    forget_parser.add_argument("entity")

    # Simulate command
    simulate_parser = subparsers.add_parser("simulate", help="Simulate translating a record")
    simulate_parser.add_argument("--file", "-f", required=True, help="JSON record file")
    simulate_parser.add_argument("--source", "-s", required=True,
                                choices=["salesforce", "dynamics365", "local"])
    simulate_parser.add_argument("--target", "-t", required=True,
                                choices=["salesforce", "dynamics365", "local"])
    simulate_parser.add_argument("--entity", "-e", required=True,
                                choices=["contacts", "companies", "deals", "activities"])

    args = parser.parse_args()

    if args.command == "status":
        cmd_status(args)
    elif args.command == "review":
        cmd_review(args)
    elif args.command == "teach":
        cmd_teach(args)
    elif args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "export":
        cmd_export(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "forget":
        cmd_forget(args)
    elif args.command == "simulate":
        cmd_simulate(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
