#!/bin/bash

################################################################################
# Power Platform Deployment Script
# Flow: AutomatedMeetingNotesEmailer
# Generated: 2025-10-14
# Type: DRY-RUN ANALYSIS - FOR REFERENCE ONLY
################################################################################

set -e  # Exit immediately if a command exits with a non-zero status
set -u  # Treat unset variables as an error
set -o pipefail  # Pipe failures cause script to fail

################################################################################
# CONFIGURATION
################################################################################

# Flow Information
FLOW_NAME="AutomatedMeetingNotesEmailer"
FLOW_DISPLAY_NAME="Automated Meeting Notes Emailer"
FLOW_JSON_PATH="/Users/kodyw/Documents/GitHub/localFirstTools3/generated_flows/AutomatedMeetingNotesEmailer.json"

# Solution Information
SOLUTION_NAME="${SOLUTION_NAME:-MeetingAutomation}"
SOLUTION_DISPLAY_NAME="${SOLUTION_DISPLAY_NAME:-Meeting Automation Solution}"
SOLUTION_VERSION="${SOLUTION_VERSION:-1.0.0.0}"
SOLUTION_PUBLISHER_NAME="${SOLUTION_PUBLISHER_NAME:-contoso}"
SOLUTION_PUBLISHER_PREFIX="${SOLUTION_PUBLISHER_PREFIX:-new}"

# Environment Configuration
TARGET_ENV_URL="${TARGET_ENV_URL:-}"
TARGET_ENV_ID="${TARGET_ENV_ID:-}"
DEPLOYMENT_TYPE="${DEPLOYMENT_TYPE:-unmanaged}"  # unmanaged or managed

# Connection Configuration
CONNECTION_MAPPING_FILE="/Users/kodyw/Documents/GitHub/localFirstTools3/generated_flows/deployment_package/config/connection-mapping.json"

# Deployment Paths
DEPLOYMENT_ROOT="/Users/kodyw/Documents/GitHub/localFirstTools3/generated_flows/deployment_package"
SOLUTION_ROOT="${DEPLOYMENT_ROOT}/solution"
BACKUP_ROOT="${DEPLOYMENT_ROOT}/backups"
LOG_ROOT="${DEPLOYMENT_ROOT}/logs"

# Logging Configuration
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
LOG_FILE="${LOG_ROOT}/deployment_${TIMESTAMP}.log"
BACKUP_FILE="${BACKUP_ROOT}/backup_${TIMESTAMP}.zip"

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

################################################################################
# LOGGING FUNCTIONS
################################################################################

log() {
    echo "[$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log_info() {
    echo -e "${BLUE}[INFO]${NC} [$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} [$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} [$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} [$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

print_header() {
    echo "" | tee -a "$LOG_FILE"
    echo "═══════════════════════════════════════════════════════════════" | tee -a "$LOG_FILE"
    echo "$1" | tee -a "$LOG_FILE"
    echo "═══════════════════════════════════════════════════════════════" | tee -a "$LOG_FILE"
    echo "" | tee -a "$LOG_FILE"
}

################################################################################
# VALIDATION FUNCTIONS
################################################################################

validate_prerequisites() {
    print_header "STEP 1: VALIDATING PREREQUISITES"

    log_info "Checking pac CLI installation..."
    if ! command -v pac &> /dev/null; then
        log_error "pac CLI is not installed. Please install from: https://aka.ms/PowerPlatformCLI"
        exit 1
    fi

    PAC_VERSION=$(pac --version 2>&1 | head -n 1)
    log_success "pac CLI found: $PAC_VERSION"

    log_info "Checking for flow JSON file..."
    if [ ! -f "$FLOW_JSON_PATH" ]; then
        log_error "Flow JSON file not found at: $FLOW_JSON_PATH"
        exit 1
    fi
    log_success "Flow JSON file found"

    log_info "Validating JSON syntax..."
    if ! jq empty "$FLOW_JSON_PATH" 2>/dev/null; then
        log_error "Flow JSON file has invalid syntax"
        exit 1
    fi
    log_success "JSON syntax is valid"

    log_info "Creating required directories..."
    mkdir -p "$SOLUTION_ROOT" "$BACKUP_ROOT" "$LOG_ROOT"
    log_success "Directory structure ready"
}

validate_authentication() {
    print_header "STEP 2: VALIDATING AUTHENTICATION"

    log_info "Checking pac authentication status..."

    if ! pac auth list > /dev/null 2>&1; then
        log_error "No pac authentication profiles found"
        echo ""
        echo "Please authenticate using one of these methods:"
        echo ""
        echo "  Interactive:"
        echo "    pac auth create --url <your-environment-url>"
        echo ""
        echo "  Service Principal:"
        echo "    pac auth create --kind SERVICEPRINCIPALSECRET \\"
        echo "      --url <your-environment-url> \\"
        echo "      --applicationId <app-id> \\"
        echo "      --clientSecret <secret> \\"
        echo "      --tenant <tenant-id>"
        echo ""
        exit 1
    fi

    log_info "Authentication profiles found:"
    pac auth list | tee -a "$LOG_FILE"

    log_info "Verifying current authentication..."
    CURRENT_ORG=$(pac org who 2>&1)

    if echo "$CURRENT_ORG" | grep -q "Error"; then
        log_error "Authentication verification failed"
        log_error "$CURRENT_ORG"
        exit 1
    fi

    log_success "Successfully authenticated"
    echo "$CURRENT_ORG" | tee -a "$LOG_FILE"
}

validate_environment() {
    print_header "STEP 3: VALIDATING TARGET ENVIRONMENT"

    if [ -z "$TARGET_ENV_URL" ]; then
        log_warning "TARGET_ENV_URL not specified. Please set environment variable:"
        log_warning "  export TARGET_ENV_URL='https://your-org.crm.dynamics.com'"
        log_warning ""
        log_warning "Available environments:"
        pac org list | tee -a "$LOG_FILE"
        exit 1
    fi

    log_info "Target environment URL: $TARGET_ENV_URL"

    log_info "Verifying environment access..."
    CURRENT_ENV=$(pac org who 2>&1)

    if echo "$CURRENT_ENV" | grep -q "$TARGET_ENV_URL"; then
        log_success "Already authenticated to target environment"
    else
        log_info "Switching to target environment..."
        if ! pac auth create --url "$TARGET_ENV_URL" 2>&1 | tee -a "$LOG_FILE"; then
            log_error "Failed to authenticate to target environment"
            exit 1
        fi
        log_success "Successfully authenticated to target environment"
    fi

    log_info "Checking environment capabilities..."
    pac org who | grep -E "(Environment|User|Version)" | tee -a "$LOG_FILE"
}

validate_connectors() {
    print_header "STEP 4: VALIDATING REQUIRED CONNECTORS"

    log_info "Checking for Office 365 Outlook connector..."

    CONNECTOR_CHECK=$(pac connector list 2>&1 | grep -i "office365" || true)

    if [ -z "$CONNECTOR_CHECK" ]; then
        log_warning "Office 365 Outlook connector not found in environment"
        log_warning "This connector may need to be enabled in Power Platform Admin Center"
    else
        log_success "Office 365 Outlook connector is available"
        echo "$CONNECTOR_CHECK" | head -n 5 | tee -a "$LOG_FILE"
    fi
}

################################################################################
# BACKUP FUNCTIONS
################################################################################

create_backup() {
    print_header "STEP 5: CREATING BACKUP"

    log_info "Checking if solution already exists..."

    EXISTING_SOLUTION=$(pac solution list 2>&1 | grep -i "$SOLUTION_NAME" || true)

    if [ -n "$EXISTING_SOLUTION" ]; then
        log_warning "Solution '$SOLUTION_NAME' already exists in environment"
        log_info "Creating backup before proceeding..."

        if pac solution export --name "$SOLUTION_NAME" --path "$BACKUP_FILE" --managed false 2>&1 | tee -a "$LOG_FILE"; then
            log_success "Backup created: $BACKUP_FILE"

            # Verify backup file
            if [ -f "$BACKUP_FILE" ] && [ -s "$BACKUP_FILE" ]; then
                BACKUP_SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
                log_info "Backup file size: $BACKUP_SIZE"
            else
                log_error "Backup file is invalid or empty"
                exit 1
            fi
        else
            log_error "Failed to create backup"
            log_warning "Proceeding without backup (use Ctrl+C to abort)"
            sleep 5
        fi
    else
        log_info "Solution does not exist yet - no backup needed"
    fi
}

################################################################################
# SOLUTION CREATION FUNCTIONS
################################################################################

create_solution_structure() {
    print_header "STEP 6: CREATING SOLUTION STRUCTURE"

    log_info "Cleaning solution directory..."
    rm -rf "${SOLUTION_ROOT:?}"/*

    log_info "Initializing solution..."
    cd "$SOLUTION_ROOT"

    if pac solution init \
        --publisher-name "$SOLUTION_PUBLISHER_NAME" \
        --publisher-prefix "$SOLUTION_PUBLISHER_PREFIX" 2>&1 | tee -a "$LOG_FILE"; then
        log_success "Solution initialized successfully"
    else
        log_error "Failed to initialize solution"
        exit 1
    fi

    log_info "Creating solution structure..."
    mkdir -p "$SOLUTION_ROOT/src/Workflows"

    log_info "Copying flow JSON to solution..."
    cp "$FLOW_JSON_PATH" "$SOLUTION_ROOT/src/Workflows/${FLOW_NAME}.json"

    log_success "Solution structure created"

    log_info "Solution contents:"
    find "$SOLUTION_ROOT" -type f | tee -a "$LOG_FILE"
}

update_solution_metadata() {
    print_header "STEP 7: UPDATING SOLUTION METADATA"

    SOLUTION_XML="$SOLUTION_ROOT/src/Other/Solution.xml"

    if [ -f "$SOLUTION_XML" ]; then
        log_info "Updating Solution.xml with flow metadata..."

        # Update solution version
        sed -i.bak "s/<Version>.*<\/Version>/<Version>$SOLUTION_VERSION<\/Version>/" "$SOLUTION_XML"

        # Update solution unique name
        sed -i.bak "s/<UniqueName>.*<\/UniqueName>/<UniqueName>$SOLUTION_NAME<\/UniqueName>/" "$SOLUTION_XML"

        log_success "Solution metadata updated"
    else
        log_warning "Solution.xml not found - skipping metadata update"
    fi
}

################################################################################
# DEPLOYMENT FUNCTIONS
################################################################################

package_solution() {
    print_header "STEP 8: PACKAGING SOLUTION"

    cd "$SOLUTION_ROOT"

    SOLUTION_ZIP="${DEPLOYMENT_ROOT}/solution_${TIMESTAMP}.zip"

    log_info "Packaging solution..."

    # Use pac solution pack if available, otherwise zip manually
    if command -v pac solution pack &> /dev/null; then
        if pac solution pack --zipfile "$SOLUTION_ZIP" --folder "$SOLUTION_ROOT" 2>&1 | tee -a "$LOG_FILE"; then
            log_success "Solution packaged using pac CLI"
        else
            log_warning "pac solution pack failed, using zip fallback"
            cd "$SOLUTION_ROOT/src"
            zip -r "$SOLUTION_ZIP" . >> "$LOG_FILE" 2>&1
        fi
    else
        log_info "Using zip to package solution..."
        cd "$SOLUTION_ROOT/src"
        zip -r "$SOLUTION_ZIP" . >> "$LOG_FILE" 2>&1
    fi

    if [ -f "$SOLUTION_ZIP" ] && [ -s "$SOLUTION_ZIP" ]; then
        PACKAGE_SIZE=$(du -h "$SOLUTION_ZIP" | cut -f1)
        log_success "Solution packaged: $SOLUTION_ZIP (${PACKAGE_SIZE})"

        log_info "Package contents:"
        unzip -l "$SOLUTION_ZIP" | head -n 20 | tee -a "$LOG_FILE"
    else
        log_error "Failed to create solution package"
        exit 1
    fi
}

deploy_solution() {
    print_header "STEP 9: DEPLOYING SOLUTION"

    SOLUTION_ZIP="${DEPLOYMENT_ROOT}/solution_${TIMESTAMP}.zip"

    log_info "Importing solution to environment..."
    log_info "Solution: $SOLUTION_NAME"
    log_info "Version: $SOLUTION_VERSION"
    log_info "Type: $DEPLOYMENT_TYPE"
    log_info "Package: $SOLUTION_ZIP"

    IMPORT_ARGS=(
        "--path" "$SOLUTION_ZIP"
        "--force-overwrite"
        "--activate-plugins"
    )

    if [ "$DEPLOYMENT_TYPE" = "managed" ]; then
        IMPORT_ARGS+=("--publish-changes")
    fi

    log_warning "DEPLOYMENT EXECUTION DISABLED (DRY-RUN MODE)"
    log_info "In production, would execute:"
    log_info "  pac solution import ${IMPORT_ARGS[*]}"

    # Uncomment below for actual deployment
    # if pac solution import "${IMPORT_ARGS[@]}" 2>&1 | tee -a "$LOG_FILE"; then
    #     log_success "Solution imported successfully"
    # else
    #     log_error "Solution import failed"
    #     log_error "Check log file for details: $LOG_FILE"
    #     exit 1
    # fi

    log_success "Deployment step completed (DRY-RUN)"
}

################################################################################
# POST-DEPLOYMENT FUNCTIONS
################################################################################

configure_connections() {
    print_header "STEP 10: CONFIGURING CONNECTION REFERENCES"

    log_info "Listing flows in environment..."

    log_warning "CONNECTION CONFIGURATION DISABLED (DRY-RUN MODE)"
    log_info "In production, would execute:"
    log_info "  pac flow list | grep -i 'AutomatedMeetingNotes'"

    # Uncomment below for actual deployment
    # FLOW_LIST=$(pac flow list 2>&1 | grep -i "AutomatedMeetingNotes" || true)
    #
    # if [ -z "$FLOW_LIST" ]; then
    #     log_error "Flow not found in environment after import"
    #     exit 1
    # fi
    #
    # log_success "Flow found in environment"
    # echo "$FLOW_LIST" | tee -a "$LOG_FILE"

    log_info "Connection references must be configured manually:"
    log_info "1. Open Power Automate portal: https://make.powerautomate.com"
    log_info "2. Navigate to Solutions > $SOLUTION_NAME"
    log_info "3. Select the flow: $FLOW_DISPLAY_NAME"
    log_info "4. Configure Office 365 Outlook connection"
    log_info "5. Test the flow"

    if [ -f "$CONNECTION_MAPPING_FILE" ]; then
        log_info "Connection mapping reference file: $CONNECTION_MAPPING_FILE"
    fi
}

enable_flow() {
    print_header "STEP 11: ENABLING FLOW"

    log_warning "FLOW ENABLEMENT DISABLED (DRY-RUN MODE)"
    log_info "In production, would execute:"
    log_info "  pac flow enable --flow-id <FLOW-ID>"

    # Uncomment below for actual deployment
    # if [ -n "$FLOW_ID" ]; then
    #     log_info "Enabling flow..."
    #     if pac flow enable --flow-id "$FLOW_ID" 2>&1 | tee -a "$LOG_FILE"; then
    #         log_success "Flow enabled successfully"
    #     else
    #         log_warning "Failed to enable flow - may need manual enablement"
    #     fi
    # fi
}

verify_deployment() {
    print_header "STEP 12: VERIFYING DEPLOYMENT"

    log_info "Running post-deployment verification..."

    log_warning "VERIFICATION DISABLED (DRY-RUN MODE)"

    log_info "Production verification steps would include:"
    log_info "  ✓ Verify solution appears in environment"
    log_info "  ✓ Verify flow is enabled"
    log_info "  ✓ Verify connection references are configured"
    log_info "  ✓ Test flow with sample payload"
    log_info "  ✓ Verify email delivery"
    log_info "  ✓ Check run history for errors"

    # Uncomment below for actual deployment
    # log_info "Checking solution status..."
    # pac solution list | grep -i "$SOLUTION_NAME" | tee -a "$LOG_FILE"
    #
    # log_info "Checking flow status..."
    # pac flow list | grep -i "AutomatedMeetingNotes" | tee -a "$LOG_FILE"
    #
    # log_info "Checking connections..."
    # pac connection list | grep -i "office365" | tee -a "$LOG_FILE"
}

################################################################################
# REPORTING FUNCTIONS
################################################################################

generate_deployment_report() {
    print_header "STEP 13: GENERATING DEPLOYMENT REPORT"

    REPORT_FILE="${DEPLOYMENT_ROOT}/reports/deployment_report_${TIMESTAMP}.md"

    log_info "Generating deployment report..."

    cat > "$REPORT_FILE" << EOF
# Deployment Report: AutomatedMeetingNotesEmailer

**Deployment Date**: $(date +'%Y-%m-%d %H:%M:%S')
**Deployment Type**: DRY-RUN ANALYSIS
**Status**: SIMULATION COMPLETE

---

## Deployment Summary

| Property | Value |
|----------|-------|
| Flow Name | $FLOW_DISPLAY_NAME |
| Solution Name | $SOLUTION_NAME |
| Solution Version | $SOLUTION_VERSION |
| Deployment Type | $DEPLOYMENT_TYPE |
| Target Environment | $TARGET_ENV_URL |
| Executed By | $(whoami) |

---

## Deployment Steps Executed

1. ✓ Prerequisites validated
2. ✓ Authentication verified
3. ✓ Environment validated
4. ✓ Connectors checked
5. ✓ Backup created (if applicable)
6. ✓ Solution structure created
7. ✓ Solution metadata updated
8. ✓ Solution packaged
9. ⚠ Solution deployment (DRY-RUN - not executed)
10. ⚠ Connection configuration (DRY-RUN - not executed)
11. ⚠ Flow enablement (DRY-RUN - not executed)
12. ⚠ Deployment verification (DRY-RUN - not executed)

---

## Files Generated

- Solution Package: \`solution_${TIMESTAMP}.zip\`
- Backup File: \`$BACKUP_FILE\` (if applicable)
- Deployment Log: \`$LOG_FILE\`
- This Report: \`$REPORT_FILE\`

---

## Next Steps

### For Actual Deployment:

1. **Set Environment Variables:**
   \`\`\`bash
   export TARGET_ENV_URL='https://your-org.crm.dynamics.com'
   export DEPLOYMENT_TYPE='unmanaged'  # or 'managed' for production
   \`\`\`

2. **Uncomment Deployment Code:**
   - Edit \`deployment_script.sh\`
   - Uncomment deployment execution sections
   - Remove DRY-RUN warnings

3. **Execute Deployment:**
   \`\`\`bash
   ./deployment_script.sh
   \`\`\`

4. **Configure Connections:**
   - Open Power Automate portal
   - Navigate to solution
   - Configure Office 365 connection

5. **Test Flow:**
   - Use sample payload from test plan
   - Verify email delivery
   - Check run history

### Manual Post-Deployment Tasks:

- [ ] Configure Office 365 Outlook connection reference
- [ ] Enable flow if not auto-enabled
- [ ] Obtain HTTP trigger URL
- [ ] Configure trigger authentication
- [ ] Test with sample meeting data
- [ ] Document API endpoint for consumers
- [ ] Set up monitoring and alerts

---

## Support Information

**Deployment Log**: \`$LOG_FILE\`
**Deployment Package**: \`$DEPLOYMENT_ROOT\`
**Rollback Script**: \`${DEPLOYMENT_ROOT}/scripts/rollback_script.sh\`

**Generated**: $(date +'%Y-%m-%d %H:%M:%S')
EOF

    log_success "Deployment report generated: $REPORT_FILE"
}

################################################################################
# MAIN EXECUTION
################################################################################

main() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                          ║"
    echo "║            Power Platform Deployment Script                             ║"
    echo "║            AutomatedMeetingNotesEmailer Flow                            ║"
    echo "║                                                                          ║"
    echo "║            DRY-RUN MODE - NO ACTUAL CHANGES WILL BE MADE                ║"
    echo "║                                                                          ║"
    echo "╚══════════════════════════════════════════════════════════════════════════╝"
    echo ""

    log_info "Deployment started at $(date +'%Y-%m-%d %H:%M:%S')"
    log_info "Log file: $LOG_FILE"

    # Execute deployment steps
    validate_prerequisites
    validate_authentication
    validate_environment
    validate_connectors
    create_backup
    create_solution_structure
    update_solution_metadata
    package_solution
    deploy_solution
    configure_connections
    enable_flow
    verify_deployment
    generate_deployment_report

    print_header "DEPLOYMENT COMPLETE"

    log_success "DRY-RUN deployment simulation completed successfully!"
    echo ""
    log_info "Summary:"
    log_info "  - Deployment log: $LOG_FILE"
    log_info "  - Deployment report: ${DEPLOYMENT_ROOT}/reports/deployment_report_${TIMESTAMP}.md"
    log_info "  - Solution package: ${DEPLOYMENT_ROOT}/solution_${TIMESTAMP}.zip"

    if [ -f "$BACKUP_FILE" ]; then
        log_info "  - Backup file: $BACKUP_FILE"
    fi

    echo ""
    log_info "To execute actual deployment:"
    log_info "  1. Set TARGET_ENV_URL environment variable"
    log_info "  2. Edit this script and uncomment deployment sections"
    log_info "  3. Run: ./deployment_script.sh"
    echo ""

    log_info "For rollback, use: ${DEPLOYMENT_ROOT}/scripts/rollback_script.sh"
    echo ""
}

# Execute main function
main "$@"

exit 0
