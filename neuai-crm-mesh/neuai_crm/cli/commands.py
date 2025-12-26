"""
CLI commands for NeuAI CRM Data Mesh.
"""

import argparse
import json
import sys
from typing import Optional

from neuai_crm.models.schemas import Platform
from neuai_crm.services.data_mesh import DataMesh
from neuai_crm.services.intelligence import IntelligenceLayer


# Initialize services
data_mesh = DataMesh()
intelligence = IntelligenceLayer(data_mesh)


def cmd_serve(args):
    """Start the API server."""
    try:
        import uvicorn
        from neuai_crm.api.server import app

        print(f"Starting NeuAI CRM Data Mesh API...")
        print(f"  Host: {args.host}")
        print(f"  Port: {args.port}")
        print(f"  Debug: {args.debug}")
        print(f"\nAPI docs: http://{args.host}:{args.port}/docs")
        print(f"Health check: http://{args.host}:{args.port}/health\n")

        uvicorn.run(
            app,
            host=args.host,
            port=args.port,
            reload=args.debug,
            log_level="debug" if args.debug else "info"
        )
    except ImportError:
        print("Error: uvicorn is required for the server.")
        print("Install it with: pip install uvicorn")
        sys.exit(1)


def cmd_translate(args):
    """Translate data between platforms."""
    try:
        from_platform = Platform(args.from_platform)
        to_platform = Platform(args.to_platform)
    except ValueError as e:
        print(f"Error: Invalid platform - {e}")
        sys.exit(1)

    # Load source data
    try:
        result = data_mesh.load_from_file(from_platform, args.file)
        print(f"Loaded {result['records_loaded']} records from {args.file}")
    except FileNotFoundError:
        print(f"Error: File not found - {args.file}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON - {e}")
        sys.exit(1)

    # Sync to target
    sync_result = data_mesh.sync_platforms(from_platform, to_platform)
    print(f"Translated {sync_result['synced']} records")

    if sync_result['errors']:
        print(f"Errors: {len(sync_result['errors'])}")

    # Export
    output = data_mesh.export_to_platform(to_platform)

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(output, f, indent=2)
        print(f"Output saved to {args.output}")
    else:
        print(json.dumps(output, indent=2))


def cmd_sync(args):
    """Sync data between platforms."""
    try:
        source = Platform(args.source)
        target = Platform(args.target)
    except ValueError as e:
        print(f"Error: Invalid platform - {e}")
        sys.exit(1)

    if args.source_file:
        try:
            result = data_mesh.load_from_file(source, args.source_file)
            print(f"Loaded {result['records_loaded']} records from {args.source_file}")
        except FileNotFoundError:
            print(f"Error: File not found - {args.source_file}")
            sys.exit(1)

    result = data_mesh.sync_platforms(source, target)
    print(f"\nSync complete!")
    print(f"  Records synced: {result['synced']}")
    print(f"  Errors: {len(result['errors'])}")

    if result['entity_counts']:
        print("\nEntity counts:")
        for entity, count in result['entity_counts'].items():
            print(f"  {entity}: {count}")

    if result['errors']:
        print("\nFirst 5 errors:")
        for err in result['errors'][:5]:
            print(f"  - {err['error']}")


def cmd_duplicates(args):
    """Detect duplicates across platforms."""
    # Load data from files if provided
    files_loaded = 0

    if args.salesforce:
        try:
            result = data_mesh.load_from_file(Platform.SALESFORCE, args.salesforce)
            print(f"Loaded {result['records_loaded']} Salesforce records")
            files_loaded += 1
        except FileNotFoundError:
            print(f"Warning: Salesforce file not found - {args.salesforce}")

    if args.dynamics:
        try:
            result = data_mesh.load_from_file(Platform.DYNAMICS365, args.dynamics)
            print(f"Loaded {result['records_loaded']} Dynamics 365 records")
            files_loaded += 1
        except FileNotFoundError:
            print(f"Warning: Dynamics file not found - {args.dynamics}")

    if args.local:
        try:
            result = data_mesh.load_from_file(Platform.LOCAL, args.local)
            print(f"Loaded {result['records_loaded']} Local CRM records")
            files_loaded += 1
        except FileNotFoundError:
            print(f"Warning: Local file not found - {args.local}")

    if files_loaded == 0:
        print("No data files loaded. Use --salesforce, --dynamics, or --local to specify files.")
        return

    print(f"\nDetecting duplicates (threshold: {args.threshold})...")
    duplicates = data_mesh.detect_duplicates(args.threshold)

    print(f"\nFound {len(duplicates)} potential duplicates:\n")

    for i, dup in enumerate(duplicates, 1):
        print(f"{i}. {dup['type'].title()}: {dup['match_value']}")
        print(f"   Match field: {dup['match_field']}")
        print(f"   Confidence: {dup['confidence']:.0%}")
        print(f"   Platforms:")
        for record in dup['records']:
            print(f"     - {record['platform']}")
        print()


def cmd_migrate(args):
    """Migrate data between platforms."""
    try:
        source = Platform(args.from_platform)
        target = Platform(args.to_platform)
    except ValueError as e:
        print(f"Error: Invalid platform - {e}")
        sys.exit(1)

    if args.source_file:
        try:
            result = data_mesh.load_from_file(source, args.source_file)
            print(f"Loaded {result['records_loaded']} records from {args.source_file}")
        except FileNotFoundError:
            print(f"Error: File not found - {args.source_file}")
            sys.exit(1)

    # Check for conflicts
    conflicts = data_mesh.get_conflicts(source, target)

    if conflicts and not args.force:
        print(f"\nFound {len(conflicts)} conflicts!")
        print("Use --force to migrate anyway, or resolve conflicts first.\n")

        for c in conflicts[:5]:
            print(f"  - {c['type']}: {c['match_value']}")

        if len(conflicts) > 5:
            print(f"  ... and {len(conflicts) - 5} more")

        sys.exit(1)

    # Perform migration
    result = data_mesh.sync_platforms(source, target)
    print(f"\nMigration complete!")
    print(f"  Records migrated: {result['synced']}")

    if args.output:
        output = data_mesh.export_to_platform(target)
        with open(args.output, 'w') as f:
            json.dump(output, f, indent=2)
        print(f"  Output saved to: {args.output}")


def cmd_query(args):
    """Process a natural language query."""
    result = intelligence.process_query(args.query)

    print(f"\nIntent: {result.get('intent', 'unknown')}")
    print(f"Action: {result.get('action', 'unknown')}")
    print(f"\n{result.get('message', '')}\n")

    # Print additional details based on intent
    if result.get('stats'):
        print("Statistics:")
        for platform, entities in result['stats'].items():
            total = sum(entities.values())
            print(f"  {platform}: {total} records")

    if result.get('duplicates'):
        print(f"\nDuplicates found: {len(result['duplicates'])}")

    if result.get('conflicts'):
        print(f"\nConflicts found: {len(result['conflicts'])}")


def cmd_stats(args):
    """Show statistics."""
    # Load data from files if provided
    if args.salesforce:
        try:
            data_mesh.load_from_file(Platform.SALESFORCE, args.salesforce)
        except FileNotFoundError:
            print(f"Warning: File not found - {args.salesforce}")

    if args.dynamics:
        try:
            data_mesh.load_from_file(Platform.DYNAMICS365, args.dynamics)
        except FileNotFoundError:
            print(f"Warning: File not found - {args.dynamics}")

    if args.local:
        try:
            data_mesh.load_from_file(Platform.LOCAL, args.local)
        except FileNotFoundError:
            print(f"Warning: File not found - {args.local}")

    stats = data_mesh.get_stats()

    print("\n" + "=" * 50)
    print("  NeuAI CRM Data Mesh Statistics")
    print("=" * 50)

    grand_total = 0

    for platform, entities in stats.items():
        total = sum(entities.values())
        grand_total += total

        print(f"\n{platform.upper()} ({total} total)")
        print("-" * 30)

        for entity, count in entities.items():
            print(f"  {entity:<20} {count:>6}")

    print("\n" + "=" * 50)
    print(f"  GRAND TOTAL: {grand_total} records")
    print("=" * 50 + "\n")


def cmd_export(args):
    """Export data for a platform."""
    try:
        platform = Platform(args.platform)
    except ValueError as e:
        print(f"Error: Invalid platform - {e}")
        sys.exit(1)

    if args.source_file:
        try:
            data_mesh.load_from_file(platform, args.source_file)
        except FileNotFoundError:
            print(f"Error: File not found - {args.source_file}")
            sys.exit(1)

    output = data_mesh.export_to_platform(platform)

    if args.output:
        with open(args.output, 'w') as f:
            json.dump(output, f, indent=2)
        print(f"Exported to {args.output}")
    else:
        print(json.dumps(output, indent=2))


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="NeuAI CRM Data Mesh - Unified CRM Management",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Start the API server
  python -m neuai_crm serve --port 8080

  # Translate Salesforce data to Dynamics 365
  python -m neuai_crm translate --from salesforce --to dynamics365 --file sf.json -o d365.json

  # Sync platforms
  python -m neuai_crm sync --source local --target salesforce --source-file local.json

  # Detect duplicates
  python -m neuai_crm detect-duplicates --salesforce sf.json --dynamics d365.json

  # Migrate with conflict check
  python -m neuai_crm migrate --from salesforce --to dynamics365 --source-file sf.json -o d365.json

  # Natural language query
  python -m neuai_crm query "How many records are in each CRM?"

  # Show statistics
  python -m neuai_crm stats --salesforce sf.json --dynamics d365.json --local local.json
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Serve command
    serve_parser = subparsers.add_parser("serve", help="Start the API server")
    serve_parser.add_argument("--port", type=int, default=8080, help="Port (default: 8080)")
    serve_parser.add_argument("--host", default="0.0.0.0", help="Host (default: 0.0.0.0)")
    serve_parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    # Translate command
    translate_parser = subparsers.add_parser("translate", help="Translate data between platforms")
    translate_parser.add_argument("--from", dest="from_platform", required=True,
                                  choices=["salesforce", "dynamics365", "local"])
    translate_parser.add_argument("--to", dest="to_platform", required=True,
                                  choices=["salesforce", "dynamics365", "local"])
    translate_parser.add_argument("--file", required=True, help="Input JSON file")
    translate_parser.add_argument("-o", "--output", help="Output file")

    # Sync command
    sync_parser = subparsers.add_parser("sync", help="Sync data between platforms")
    sync_parser.add_argument("--source", required=True,
                             choices=["salesforce", "dynamics365", "local"])
    sync_parser.add_argument("--target", required=True,
                             choices=["salesforce", "dynamics365", "local"])
    sync_parser.add_argument("--source-file", help="Source data file")

    # Duplicates command
    dup_parser = subparsers.add_parser("detect-duplicates", help="Detect duplicates")
    dup_parser.add_argument("--threshold", type=float, default=0.8, help="Match threshold (0-1)")
    dup_parser.add_argument("--salesforce", help="Salesforce data file")
    dup_parser.add_argument("--dynamics", help="Dynamics 365 data file")
    dup_parser.add_argument("--local", help="Local CRM data file")

    # Migrate command
    migrate_parser = subparsers.add_parser("migrate", help="Migrate data between platforms")
    migrate_parser.add_argument("--from", dest="from_platform", required=True,
                                choices=["salesforce", "dynamics365", "local"])
    migrate_parser.add_argument("--to", dest="to_platform", required=True,
                                choices=["salesforce", "dynamics365", "local"])
    migrate_parser.add_argument("--source-file", help="Source data file")
    migrate_parser.add_argument("-o", "--output", help="Output file")
    migrate_parser.add_argument("--force", action="store_true", help="Force migration")

    # Query command
    query_parser = subparsers.add_parser("query", help="Natural language query")
    query_parser.add_argument("query", help="The query to process")

    # Stats command
    stats_parser = subparsers.add_parser("stats", help="Show statistics")
    stats_parser.add_argument("--salesforce", help="Salesforce data file")
    stats_parser.add_argument("--dynamics", help="Dynamics 365 data file")
    stats_parser.add_argument("--local", help="Local CRM data file")

    # Export command
    export_parser = subparsers.add_parser("export", help="Export data")
    export_parser.add_argument("platform", choices=["salesforce", "dynamics365", "local"])
    export_parser.add_argument("--source-file", help="Source data file to load first")
    export_parser.add_argument("-o", "--output", help="Output file")

    args = parser.parse_args()

    if args.command == "serve":
        cmd_serve(args)
    elif args.command == "translate":
        cmd_translate(args)
    elif args.command == "sync":
        cmd_sync(args)
    elif args.command == "detect-duplicates":
        cmd_duplicates(args)
    elif args.command == "migrate":
        cmd_migrate(args)
    elif args.command == "query":
        cmd_query(args)
    elif args.command == "stats":
        cmd_stats(args)
    elif args.command == "export":
        cmd_export(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
