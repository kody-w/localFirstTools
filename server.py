#!/usr/bin/env python3
"""
NeuAI CRM Data Mesh Server
==========================

Quick-start launcher for the NeuAI CRM Data Mesh API.

For the full organized package with all features, see: ./neuai-crm-mesh/

Usage:
    # Start the API server (default port 8080)
    python server.py

    # Custom port
    python server.py --port 3000

    # With debug mode
    python server.py --port 8080 --debug

    # Using the full package (recommended)
    cd neuai-crm-mesh
    pip install -r requirements.txt
    python -m neuai_crm serve --port 8080
"""

import sys
import os

# Add the package directory to path
package_dir = os.path.join(os.path.dirname(__file__), 'neuai-crm-mesh')
if os.path.exists(package_dir):
    sys.path.insert(0, package_dir)

def main():
    """Main entry point."""
    import argparse

    parser = argparse.ArgumentParser(
        description="NeuAI CRM Data Mesh API Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Quick Start:
    python server.py                    # Start on port 8080
    python server.py --port 3000        # Custom port
    python server.py --debug            # Enable debug mode

Full Package:
    cd neuai-crm-mesh
    pip install -r requirements.txt
    python -m neuai_crm serve --port 8080

For more commands (translate, sync, migrate, etc.):
    python -m neuai_crm --help
        """
    )

    parser.add_argument("--port", type=int, default=8080, help="Port to listen on (default: 8080)")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to (default: 0.0.0.0)")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    args = parser.parse_args()

    try:
        # Try to import from the package
        from neuai_crm.api.server import app
        import uvicorn

        print("=" * 60)
        print("  NeuAI CRM Data Mesh API")
        print("=" * 60)
        print(f"\n  Server starting on http://{args.host}:{args.port}")
        print(f"  API Docs: http://localhost:{args.port}/docs")
        print(f"  Health: http://localhost:{args.port}/health")
        print(f"\n  Debug mode: {'ON' if args.debug else 'OFF'}")
        print("\n" + "=" * 60 + "\n")

        uvicorn.run(
            app,
            host=args.host,
            port=args.port,
            reload=args.debug,
            log_level="debug" if args.debug else "info"
        )

    except ImportError as e:
        print(f"\nDependencies not installed. Please run:\n")
        print(f"  cd neuai-crm-mesh")
        print(f"  pip install -r requirements.txt")
        print(f"\nThen try again with:")
        print(f"  python server.py --port {args.port}")
        print(f"\nOr use the package directly:")
        print(f"  python -m neuai_crm serve --port {args.port}")
        print(f"\nMissing: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
