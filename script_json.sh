#!/bin/bash

REPO="https://github.com/danigomezdev/bombsquad"
MODS_DIR="."
DATA_FILE="indextest.json"
TEMP_FILE=".mods_temp.json"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to log messages
log() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to check if JSON file has valid mod structure
is_valid_mod_json() {
    local json_path="$1"
    
    if [ ! -f "$json_path" ]; then
        return 1
    fi
    
    # Check if it has metadata field with required properties
    if jq -e '.metadata | has("name") and has("file_name") and has("description-en") and has("api") and has("version")' "$json_path" > /dev/null 2>&1; then
        return 0
    else
        return 1
    fi
}

# Function to check if mod should be shown
should_show_mod() {
    local json_path="$1"
    
    if [ -f "$json_path" ]; then
        local show=$(jq -r '.metadata.show // "true"' "$json_path" 2>/dev/null)
        if [ "$show" = "false" ]; then
            return 1
        fi
    fi
    return 0
}

# Function to escape JSON strings
escape_json_string() {
    local string="$1"
    # Escape backslashes, quotes, and newlines
    string=$(echo "$string" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/\//\\\//g' -e 's/\\n/\\\\n/g' -e 's/\\t/\\\\t/g')
    echo "$string"
}

# Function to extract mod data from JSON file
extract_mod_data() {
    local json_path="$1"
    local relative_path=$(echo "$json_path" | sed "s|^\./||")
    
    # Extract all fields from JSON
    local mod_name=$(jq -r '.metadata.name // ""' "$json_path")
    local file_name=$(jq -r '.metadata.file_name // ""' "$json_path")
    local description_en=$(jq -r '.metadata."description-en" // ""' "$json_path")
    local description_es=$(jq -r '.metadata."description-es" // ""' "$json_path")
    local api_version=$(jq -r '.metadata.api // ""' "$json_path")
    local version=$(jq -r '.metadata.version // ""' "$json_path")
    local url_mod=$(jq -r '.metadata.url_mod // ""' "$json_path")
    local url_raw_mod=$(jq -r '.metadata.url_raw_mod // ""' "$json_path")
    local url_readme=$(jq -r '.metadata.url_readme // ""' "$json_path")
    local url_raw_readme=$(jq -r '.metadata.url_raw_readme // ""' "$json_path")
    
    # Generate more_url (raw URL for the JSON file)
    local more_url="https://raw.githubusercontent.com/danigomezdev/bombsquad/modmanager/${relative_path}"
    
    # If essential fields are missing, skip this mod
    if [ -z "$mod_name" ] || [ -z "$file_name" ] || [ -z "$description_en" ]; then
        warn "Skipping $json_path - missing essential fields"
        return 1
    fi
    
    # Use English description as main description
    local description="$description_en"
    
    # Escape strings for JSON
    local escaped_name=$(escape_json_string "$mod_name")
    local escaped_desc=$(escape_json_string "$description")
    local escaped_version=$(escape_json_string "$version")
    local escaped_desc_es=$(escape_json_string "$description_es")
    
    # Construct the path for the Python file (without ./ prefix)
    local dir_path=$(dirname "$json_path")
    local py_path="$dir_path/$file_name"
    # Remove ./ prefix if present
    py_path=$(echo "$py_path" | sed 's|^\./||')
    
    # Create mod entry
    cat << EOF
    {
        "name": "$escaped_name",
        "file_name": "$file_name",
        "path": "$py_path",
        "api_version": $api_version,
        "version": "$escaped_version",
        "url_mod": "$url_mod",
        "url_raw_mod": "$url_raw_mod",
        "url_readme": "$url_readme",
        "url_raw_readme": "$url_raw_readme",
        "description": "$escaped_desc",
        "description-es": "$escaped_desc_es",
        "more_url": "$more_url"
    }
EOF
    
    return 0
}

# Function to generate mod data
generate_mod_data() {
    log "Scanning for JSON mod files..."
    
    # Start JSON array
    echo "[" > "$TEMP_FILE"
    
    local first_entry=true
    local mod_count=0
    local excluded_count=0
    
    # Find all .json files and process them
    while IFS= read -r -d '' json_file; do
        if is_valid_mod_json "$json_file"; then
            # Check if we should show this mod
            if ! should_show_mod "$json_file"; then
                warn "Excluding $(basename "$json_file") - show is false"
                ((excluded_count++))
                continue
            fi
            
            # Extract mod data
            local mod_data=$(extract_mod_data "$json_file")
            if [ $? -eq 0 ] && [ -n "$mod_data" ]; then
                if [ "$first_entry" = false ]; then
                    echo "," >> "$TEMP_FILE"
                fi
                
                echo "$mod_data" >> "$TEMP_FILE"
                
                first_entry=false
                ((mod_count++))
                
                local mod_name=$(jq -r '.metadata.name' "$json_file")
                local api_version=$(jq -r '.metadata.api' "$json_file")
                local version=$(jq -r '.metadata.version' "$json_file")
                log "Found mod: $mod_name (API: $api_version, Version: $version)"
            else
                warn "Failed to extract data from $json_file"
                ((excluded_count++))
            fi
        fi
    done < <(find "$MODS_DIR" -name "*.json" -type f -print0)
    
    # Close JSON array
    echo "]" >> "$TEMP_FILE"
    
    log "Found $mod_count mod files with valid JSON metadata"
    if [ $excluded_count -gt 0 ]; then
        log "Excluded $excluded_count files (invalid JSON or show:false)"
    fi
}

# Function to check if data needs to be updated
needs_update() {
    if [ ! -f "$DATA_FILE" ]; then
        return 0
    fi
    
    # Check if any .json files are newer than indextest.json
    if find "$MODS_DIR" -name "*.json" -newer "$DATA_FILE" | grep -q .; then
        return 0
    fi
    
    # Check if any .json files were deleted
    local current_jsons=$(find "$MODS_DIR" -name "*.json" -type f | while read file; do
        if is_valid_mod_json "$file" && should_show_mod "$file"; then
            echo "$file"
        fi
    done | sort)
    
    local stored_files=$(jq -r '.[].path' "$DATA_FILE" 2>/dev/null | sort)
    
    if [ "$current_jsons" != "$stored_files" ]; then
        return 0
    fi
    
    return 1
}

# Function to validate generated JSON
validate_json() {
    if jq empty "$TEMP_FILE" 2>/dev/null; then
        return 0
    else
        error "Generated JSON is invalid"
        jq empty "$TEMP_FILE"  # This will show the actual error
        return 1
    fi
}

# Function to compare with existing data
show_changes() {
    if [ -f "$DATA_FILE" ]; then
        log "Changes detected:"
        
        # Get current mod names
        local current_mods=$(jq -r '.[].name' "$TEMP_FILE" 2>/dev/null | sort)
        local existing_mods=$(jq -r '.[].name' "$DATA_FILE" 2>/dev/null | sort)
        
        # Find added mods
        local added=$(comm -13 <(echo "$existing_mods") <(echo "$current_mods"))
        if [ -n "$added" ]; then
            echo -e "${BLUE}Added mods:${NC}"
            echo "$added"
        fi
        
        # Find removed mods
        local removed=$(comm -23 <(echo "$existing_mods") <(echo "$current_mods"))
        if [ -n "$removed" ]; then
            echo -e "${RED}Removed mods:${NC}"
            echo "$removed"
        fi
        
        # Check for modified mods
        local modified_count=$(find "$MODS_DIR" -name "*.json" -newer "$DATA_FILE" 2>/dev/null | wc -l)
        if [ "$modified_count" -gt 0 ]; then
            echo -e "${YELLOW}Modified JSON files: $modified_count${NC}"
        fi
    else
        log "No existing $DATA_FILE found - creating new one"
    fi
}

# Main execution
main() {
    log "Starting Mod Manager data generation..."
    log "Repository: $REPO"
    log "Mods directory: $MODS_DIR"
    log "Output file: $DATA_FILE"
    
    # Check if jq is available
    if ! command -v jq &> /dev/null; then
        error "jq is required but not installed. Please install jq to continue."
        exit 1
    fi
    
    # Check if mods directory exists
    if [ ! -d "$MODS_DIR" ]; then
        error "Mods directory '$MODS_DIR' not found"
        exit 1
    fi
    
    # Check if updates are needed
    if needs_update; then
        log "Changes detected - updating $DATA_FILE"
        show_changes
        
        # Generate new data
        generate_mod_data
        
        # Validate JSON
        if validate_json; then
            # Replace old file with new one
            mv "$TEMP_FILE" "$DATA_FILE"
            log "Successfully updated $DATA_FILE"
        else
            error "Failed to generate valid JSON"
            rm -f "$TEMP_FILE"
            exit 1
        fi
    else
        log "No changes detected - $DATA_FILE is up to date"
        rm -f "$TEMP_FILE"
    fi
    
    # Show final statistics
    if [ -f "$DATA_FILE" ]; then
        local total_mods=$(jq 'length' "$DATA_FILE")
        log "Total mods in $DATA_FILE: $total_mods"
        
        if [ "$total_mods" -gt 0 ]; then
            # Show API version distribution
            log "API version distribution:"
            jq -r '.[].api_version' "$DATA_FILE" | sort | uniq -c | while read count version; do
                echo "  API $version: $count mods"
            done
            
            # Show version distribution
            log "Version distribution:"
            jq -r '.[].version' "$DATA_FILE" | sort | uniq -c | while read count version; do
                echo "  $version: $count mods"
            done
            
            # Show mods with Spanish description
            local spanish_mods=$(jq -r '.[] | select(."description-es" != null and ."description-es" != "") | .name' "$DATA_FILE" | wc -l)
            log "Mods with Spanish description: $spanish_mods"
            
            # List all mods found
            log "Mods found:"
            jq -r '.[].name' "$DATA_FILE" | while read mod; do
                echo "  - $mod"
            done
        fi
    fi
    
    log "Mod Manager data generation completed"
}

# Run main function
main "$@"