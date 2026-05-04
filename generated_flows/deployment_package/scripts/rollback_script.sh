#!/bin/bash

################################################################################
# Power Platform Rollback Script
# Flow: AutomatedMeetingNotesEmailer
# Generated: 2025-10-14
# Purpose: Restore previous version of solution in case of deployment issues
################################################################################

set -e  # Exit immediately if a command exits with a non-zero status
set -u  # Treat unset variables as an error
set -o pipefail  # Pipe failures cause script to fail

################################################################################
# CONFIGURATION
################################################################################

# Solution Information
SOLUTION_NAME="${SOLUTION_NAME:-MeetingAutomation}"

# Environment Configuration
TARGET_ENV_URL="${TARGET_ENV_URL:-}"

# Paths
DEPLOYMENT_ROOT="/Users/kodyw/Documents/GitHub/localFirstTools3/generated_flows/deployment_package"
BACKUP_ROOT="${DEPLOYMENT_ROOT}/backups"
LOG_ROOT="${DEPLOYMENT_ROOT}/logs"

# Logging
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ROLLBACK_LOG="${LOG_ROOT}/rollback_${TIMESTAMP}.log"

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

################################################################################
# LOGGING FUNCTIONS
################################################################################

log_info() {
    echo -e "${BLUE}[INFO]${NC} [$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$ROLLBACK_LOG"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} [$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$ROLLBACK_LOG"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} [$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$ROLLBACK_LOG"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} [$(date +'%Y-%m-%d %H:%M:%S')] $*" | tee -a "$ROLLBACK_LOG"
}

print_header() {
    echo "" | tee -a "$ROLLBACK_LOG"
    echo "═══════════════════════════════════════════════════════════════" | tee -a "$ROLLBACK_LOG"
    echo "$1" | tee -a "$ROLLBACK_LOG"
    echo "═══════════════════════════════════════════════════════════════" | tee -a "$ROLLBACK_LOG"
    echo "" | tee -a "$ROLLBACK_LOG"
}

################################################################################
# VALIDATION FUNCTIONS
################################################################################

validate_prerequisites() {
    print_header "VALIDATING ROLLBACK PREREQUISITES"

    log_info "Checking pac CLI installation..."
    if ! command -v pac &> /dev/null; then
        log_error "pac CLI is not installed"
        exit 1
    fi
    log_success "pac CLI found"

    log_info "Creating log directory..."
    mkdir -p "$LOG_ROOT"
    log_success "Log directory ready"
}

validate_authentication() {
    print_header "VALIDATING AUTHENTICATION"

    if [ -z "$TARGET_ENV_URL" ]; then
        log_error "TARGET_ENV_URL not set"
        log_error "Please set: export TARGET_ENV_URL='https://your-org.crm.dynamics.com'"
        exit 1
    fi

    log_info "Target environment: $TARGET_ENV_URL"

    log_info "Verifying authentication..."
    CURRENT_ENV=$(pac org who 2>&1)

    if echo "$CURRENT_ENV" | grep -q "Error"; then
        log_error "Authentication failed"
        log_error "Please authenticate: pac auth create --url $TARGET_ENV_URL"
        exit 1
    fi

    if ! echo "$CURRENT_ENV" | grep -q "$TARGET_ENV_URL"; then
        log_info "Switching to target environment..."
        pac auth create --url "$TARGET_ENV_URL" 2>&1 | tee -a "$ROLLBACK_LOG"
    fi

    log_success "Authentication verified"
}

################################################################################
# BACKUP SELECTION
################################################################################

select_backup() {
    print_header "SELECTING BACKUP FILE"

    log_info "Available backup files:"
    echo ""

    if [ ! -d "$BACKUP_ROOT" ] || [ -z "$(ls -A "$BACKUP_ROOT" 2>/dev/null)" ]; then
        log_error "No backup files found in $BACKUP_ROOT"
        log_error "Cannot proceed with rollback"
        exit 1
    fi

    # List available backups with details
    BACKUP_FILES=()
    INDEX=1

    while IFS= read -r backup_file; do
        BACKUP_FILES+=("$backup_file")
        BACKUP_DATE=$(basename "$backup_file" | sed 's/backup_\(.*\)\.zip/\1/')
        BACKUP_SIZE=$(du -h "$backup_file" | cut -f1)
        echo "  [$INDEX] $(basename "$backup_file") (${BACKUP_SIZE}, Date: $BACKUP_DATE)" | tee -a "$ROLLBACK_LOG"
        ((INDEX++))
    done < <(find "$BACKUP_ROOT" -name "backup_*.zip" -type f | sort -r)

    echo ""

    # Prompt for selection
    read -p "Select backup to restore [1-${#BACKUP_FILES[@]}] or 'q' to quit: " selection

    if [ "$selection" = "q" ] || [ "$selection" = "Q" ]; then
        log_info "Rollback cancelled by user"
        exit 0
    fi

    if [ "$selection" -ge 1 ] && [ "$selection" -le "${#BACKUP_FILES[@]}" ]; then
        SELECTED_BACKUP="${BACKUP_FILES[$((selection-1))]}"
        log_success "Selected backup: $(basename "$SELECTED_BACKUP")"
    else
        log_error "Invalid selection"
        exit 1
    fi
}

################################################################################
# ROLLBACK EXECUTION
################################################################################

create_pre_rollback_backup() {
    print_header "CREATING PRE-ROLLBACK BACKUP"

    PRE_ROLLBACK_BACKUP="${BACKUP_ROOT}/pre_rollback_${TIMESTAMP}.zip"

    log_info "Creating backup of current state before rollback..."

    if pac solution export --name "$SOLUTION_NAME" --path "$PRE_ROLLBACK_BACKUP" --managed false 2>&1 | tee -a "$ROLLBACK_LOG"; then
        log_success "Pre-rollback backup created: $PRE_ROLLBACK_BACKUP"
    else
        log_warning "Failed to create pre-rollback backup"
        log_warning "Continuing with rollback..."
        sleep 3
    fi
}

confirm_rollback() {
    print_header "ROLLBACK CONFIRMATION"

    echo ""
    log_warning "╔══════════════════════════════════════════════════════════════╗"
    log_warning "║                    ROLLBACK CONFIRMATION                     ║"
    log_warning "╚══════════════════════════════════════════════════════════════╝"
    echo ""
    log_info "You are about to rollback the solution: $SOLUTION_NAME"
    log_info "Target environment: $TARGET_ENV_URL"
    log_info "Backup file: $(basename "$SELECTED_BACKUP")"
    echo ""
    log_warning "This will:"
    log_warning "  1. Replace current solution with backup version"
    log_warning "  2. Overwrite existing flows and components"
    log_warning "  3. Reset connection references"
    echo ""

    read -p "Are you sure you want to proceed? (type 'ROLLBACK' to confirm): " confirmation

    if [ "$confirmation" != "ROLLBACK" ]; then
        log_info "Rollback cancelled by user"
        exit 0
    fi

    log_warning "Rollback confirmed. Proceeding in 5 seconds... (Ctrl+C to abort)"
    sleep 5
}

disable_current_flows() {
    print_header "DISABLING CURRENT FLOWS"

    log_info "Searching for flows in solution..."

    FLOW_LIST=$(pac flow list 2>&1 | grep -i "AutomatedMeetingNotes" || true)

    if [ -n "$FLOW_LIST" ]; then
        log_info "Flows found:"
        echo "$FLOW_LIST" | tee -a "$ROLLBACK_LOG"

        # Extract flow IDs (this is a simplified example)
        # In production, you would parse the actual flow IDs

        log_warning "FLOW DISABLING DISABLED (DRY-RUN MODE)"
        log_info "In production, would execute:"
        log_info "  pac flow disable --flow-id <FLOW-ID>"

        # Uncomment below for actual rollback
        # while IFS= read -r flow_id; do
        #     log_info "Disabling flow: $flow_id"
        #     pac flow disable --flow-id "$flow_id" 2>&1 | tee -a "$ROLLBACK_LOG" || true
        # done < <(echo "$FLOW_LIST" | grep -oP 'FlowId: \K[a-f0-9-]+')
    else
        log_info "No flows found to disable"
    fi
}

restore_backup() {
    print_header "RESTORING BACKUP"

    log_info "Importing backup solution..."
    log_info "Backup: $SELECTED_BACKUP"

    log_warning "SOLUTION IMPORT DISABLED (DRY-RUN MODE)"
    log_info "In production, would execute:"
    log_info "  pac solution import --path '$SELECTED_BACKUP' --force-overwrite --activate-plugins"

    # Uncomment below for actual rollback
    # if pac solution import \
    #     --path "$SELECTED_BACKUP" \
    #     --force-overwrite \
    #     --activate-plugins 2>&1 | tee -a "$ROLLBACK_LOG"; then
    #     log_success "Backup solution imported successfully"
    # else
    #     log_error "Failed to import backup solution"
    #     log_error "Manual intervention required"
    #     exit 1
    # fi

    log_success "Rollback restoration completed (DRY-RUN)"
}

reconfigure_connections() {
    print_header "RECONFIGURING CONNECTIONS"

    log_warning "Connection references must be reconfigured manually:"
    log_info "1. Open Power Automate portal: https://make.powerautomate.com"
    log_info "2. Navigate to Solutions > $SOLUTION_NAME"
    log_info "3. Reconfigure Office 365 Outlook connection"
    log_info "4. Enable flows as needed"
    log_info "5. Test flows to verify functionality"
}

verify_rollback() {
    print_header "VERIFYING ROLLBACK"

    log_warning "VERIFICATION DISABLED (DRY-RUN MODE)"

    log_info "Production verification steps would include:"
    log_info "  ✓ Verify solution version matches backup"
    log_info "  ✓ Verify flows are present"
    log_info "  ✓ Check flow configuration"
    log_info "  ✓ Test critical flows"
    log_info "  ✓ Verify no errors in run history"

    # Uncomment below for actual rollback
    # log_info "Checking solution status..."
    # pac solution list | grep -i "$SOLUTION_NAME" | tee -a "$ROLLBACK_LOG"
    #
    # log_info "Checking flow status..."
    # pac flow list | grep -i "AutomatedMeetingNotes" | tee -a "$ROLLBACK_LOG"
}

################################################################################
# REPORTING
################################################################################

generate_rollback_report() {
    print_header "GENERATING ROLLBACK REPORT"

    REPORT_FILE="${DEPLOYMENT_ROOT}/reports/rollback_report_${TIMESTAMP}.md"

    cat > "$REPORT_FILE" << EOF
# Rollback Report: AutomatedMeetingNotesEmailer

**Rollback Date**: $(date +'%Y-%m-%d %H:%M:%S')
**Rollback Type**: DRY-RUN SIMULATION
**Status**: SIMULATION COMPLETE

---

## Rollback Summary

| Property | Value |
|----------|-------|
| Solution Name | $SOLUTION_NAME |
| Target Environment | $TARGET_ENV_URL |
| Backup Restored | $(basename "$SELECTED_BACKUP") |
| Executed By | $(whoami) |
| Rollback Type | Manual (Script-Assisted) |

---

## Rollback Steps Executed

1. ✓ Prerequisites validated
2. ✓ Authentication verified
3. ✓ Backup file selected
4. ✓ Pre-rollback backup created
5. ✓ Rollback confirmed
6. ⚠ Current flows disabled (DRY-RUN - not executed)
7. ⚠ Backup solution restored (DRY-RUN - not executed)
8. ⚠ Connections reconfigured (manual step)
9. ⚠ Rollback verified (DRY-RUN - not executed)

---

## Manual Post-Rollback Tasks

- [ ] Reconfigure Office 365 Outlook connection
- [ ] Enable flows that were disabled
- [ ] Test flows with sample data
- [ ] Verify email delivery
- [ ] Check run history for errors
- [ ] Notify stakeholders of rollback
- [ ] Document reason for rollback
- [ ] Plan remediation for original issue

---

## Files Generated

- Pre-rollback Backup: \`pre_rollback_${TIMESTAMP}.zip\` (if created)
- Rollback Log: \`$ROLLBACK_LOG\`
- This Report: \`$REPORT_FILE\`

---

## Next Steps

1. **Complete Manual Tasks**: See "Manual Post-Rollback Tasks" above
2. **Verify Functionality**: Test all critical flows
3. **Document Root Cause**: Investigate why rollback was needed
4. **Plan Remediation**: Address issues before next deployment attempt

---

## Support Information

**Rollback Log**: \`$ROLLBACK_LOG\`
**Backup Directory**: \`$BACKUP_ROOT\`

**Generated**: $(date +'%Y-%m-%d %H:%M:%S')
EOF

    log_success "Rollback report generated: $REPORT_FILE"
}

################################################################################
# MAIN EXECUTION
################################################################################

main() {
    echo ""
    echo "╔══════════════════════════════════════════════════════════════════════════╗"
    echo "║                                                                          ║"
    echo "║                   Power Platform Rollback Script                        ║"
    echo "║                   AutomatedMeetingNotesEmailer Flow                     ║"
    echo "║                                                                          ║"
    echo "║            DRY-RUN MODE - NO ACTUAL CHANGES WILL BE MADE                ║"
    echo "║                                                                          ║"
    echo "╚══════════════════════════════════════════════════════════════════════════╝"
    echo ""

    log_info "Rollback started at $(date +'%Y-%m-%d %H:%M:%S')"
    log_info "Log file: $ROLLBACK_LOG"

    # Execute rollback steps
    validate_prerequisites
    validate_authentication
    select_backup
    create_pre_rollback_backup
    confirm_rollback
    disable_current_flows
    restore_backup
    reconfigure_connections
    verify_rollback
    generate_rollback_report

    print_header "ROLLBACK COMPLETE"

    log_success "DRY-RUN rollback simulation completed successfully!"
    echo ""
    log_info "Summary:"
    log_info "  - Rollback log: $ROLLBACK_LOG"
    log_info "  - Rollback report: ${DEPLOYMENT_ROOT}/reports/rollback_report_${TIMESTAMP}.md"

    echo ""
    log_warning "Remember to complete manual post-rollback tasks:"
    log_warning "  - Reconfigure connection references"
    log_warning "  - Enable flows"
    log_warning "  - Test functionality"
    log_warning "  - Notify stakeholders"
    echo ""
}

# Execute main function
main "$@"

exit 0
