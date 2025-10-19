#!/bin/bash

REPO="https://github.com/danigomezdev/bombsquad"
MODS_DIR="."
DATA_FILE="data.json"
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

# Function to clean and extract text from meta lines
extract_meta_value() {
    local value="$1"
    # Remove surrounding quotes if present and trim whitespace
    value=$(echo "$value" | sed -e 's/^[[:space:]]*//' -e 's/[[:space:]]*$//')
    # Remove quotes at the beginning and end only
    value=$(echo "$value" | sed -e 's/^"\(.*\)"$/\1/' -e "s/^'\(.*\)'$/\1/")
    # Remove any trailing comments
    value=$(echo "$value" | sed 's/#.*$//')
    echo "$value"
}


# Function to extract mod name from file
extract_mod_name() {
    local file_path="$1"
    local default_name=$(basename "$file_path" .py)
    
    # Look for ba_meta name pattern with or without colon
    local name_line=$(grep -m 1 "^# ba_meta name" "$file_path" 2>/dev/null)
    
    if [ -n "$name_line" ]; then
        # Extract everything after "name" (with optional colon)
        local extracted_name=$(echo "$name_line" | sed -E 's/^# ba_meta name:?[[:space:]]*//')
        extracted_name=$(extract_meta_value "$extracted_name")
        
        # If extraction failed or resulted in empty string, use default
        if [ -z "$extracted_name" ]; then
            echo "$default_name"
        else
            echo "$extracted_name"
        fi
    else
        echo "$default_name"
    fi
}

# Function to extract description from file
extract_description() {
    local file_path="$1"
    local default_description="No description available"
    
    # Look for ba_meta description pattern with or without colon
    local desc_line=$(grep -m 1 "^# ba_meta description" "$file_path" 2>/dev/null)
    
    if [ -n "$desc_line" ]; then
        # Extract everything after "description" (with optional colon)
        local extracted_desc=$(echo "$desc_line" | sed -E 's/^# ba_meta description:?[[:space:]]*//')
        extracted_desc=$(extract_meta_value "$extracted_desc")
        
        # Limit to 120 characters
        if [ ${#extracted_desc} -gt 120 ]; then
            extracted_desc="${extracted_desc:0:117}..."
        fi
        echo "$extracted_desc"
    else
        echo "$default_description"
    fi
}

# Function to extract version from file
extract_version() {
    local file_path="$1"
    
    # Look for ba_meta version pattern with or without colon
    local version_line=$(grep -m 1 "^# ba_meta version" "$file_path" 2>/dev/null)
    
    if [ -n "$version_line" ]; then
        # Extract everything after "version" (with optional colon)
        local extracted_version=$(echo "$version_line" | sed -E 's/^# ba_meta version:?[[:space:]]*//')
        extracted_version=$(extract_meta_value "$extracted_version")
        echo "$extracted_version"
    else
        echo "v1.0.0"
    fi
}

# Function to extract API version from file
extract_api_version() {
    local file_path="$1"
    
    # Look for ba_meta require api pattern
    local api_line=$(grep -m 1 "^# ba_meta require api" "$file_path" 2>/dev/null)
    
    if [ -n "$api_line" ]; then
        # Extract the API version number
        local api_version=$(echo "$api_line" | grep -o '[0-9]\+')
        echo "$api_version"
    else
        echo "unknown"
    fi
}

# Function to extract version from file
extract_version() {
    local file_path="$1"
    
    # Look for ba_meta version pattern
    local version_line=$(grep -m 1 "^# ba_meta version:" "$file_path" 2>/dev/null)
    
    if [ -n "$version_line" ]; then
        # Extract everything after "version:"
        local extracted_version=$(echo "$version_line" | sed 's/^# ba_meta version:\s*//')
        extracted_version=$(extract_meta_value "$extracted_version")
        echo "$extracted_version"
    else
        echo "v1.0.0"
    fi
}

# Function to check if file has nomod header
has_nomod() {
    local file_path="$1"
    
    # Check if file contains ba_meta nomod
    if grep -q "^# ba_meta nomod" "$file_path" 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

# Function to check if file is a Python mod file
is_mod_file() {
    local file_path="$1"
    
    # Check if it's a .py file and contains ba_meta require api and doesn't have nomod
    if [[ "$file_path" == *.py ]] && grep -q "^# ba_meta require api" "$file_path" 2>/dev/null && ! has_nomod "$file_path"; then
        return 0
    else
        return 1
    fi
}

# Function to escape JSON strings
escape_json_string() {
    local string="$1"
    # Escape backslashes, quotes, and newlines
    string=$(echo "$string" | sed -e 's/\\/\\\\/g' -e 's/"/\\"/g' -e 's/\//\\\//g' -e 's/\\n/\\\\n/g' -e 's/\\t/\\\\t/g')
    echo "$string"
}

# Function to check if README exists and generate URLs
get_readme_urls() {
    local file_path="$1"
    local dir_path=$(dirname "$file_path")
    local readme_path="$dir_path/README.md"
    
    if [ -f "$readme_path" ]; then
        local relative_readme_path=$(echo "$readme_path" | sed "s|^\./||")
        local url_readme="${REPO}/blob/mods/${relative_readme_path}"
        local url_raw_readme="${REPO}/raw/mods/${relative_readme_path}"
        
        # Replace spaces with %20 in URLs
        url_readme=$(echo "$url_readme" | sed 's/ /%20/g')
        url_raw_readme=$(echo "$url_raw_readme" | sed 's/ /%20/g')
        
        echo "$url_readme" "$url_raw_readme"
    else
        echo "" ""
    fi
}

# Function to generate mod data
generate_mod_data() {
    log "Scanning for mod files..."
    
    # Start JSON array
    echo "[" > "$TEMP_FILE"
    
    local first_entry=true
    local mod_count=0
    local excluded_count=0
    
    # Find all .py files and process them
    while IFS= read -r -d '' file; do
        if is_mod_file "$file"; then
            local relative_path=$(echo "$file" | sed "s|^\./||")
            local mod_name=$(extract_mod_name "$file")
            local description=$(extract_description "$file")
            local api_version=$(extract_api_version "$file")
            local version=$(extract_version "$file")
            
            # Generate mod URLs
            local url_mod="${REPO}/blob/mods/${relative_path}"
            local url_raw_mod="${REPO}/raw/mods/${relative_path}"
            
            # Generate README URLs if README exists
            read -r url_readme url_raw_readme <<< "$(get_readme_urls "$file")"
            
            # Replace spaces with %20 in URLs
            url_mod=$(echo "$url_mod" | sed 's/ /%20/g')
            url_raw_mod=$(echo "$url_raw_mod" | sed 's/ /%20/g')
            
            # Escape strings for JSON
            local escaped_name=$(escape_json_string "$mod_name")
            local escaped_desc=$(escape_json_string "$description")
            local escaped_version=$(escape_json_string "$version")
            
            if [ "$first_entry" = false ]; then
                echo "," >> "$TEMP_FILE"
            fi
            
            # Create mod entry with proper JSON formatting
            cat >> "$TEMP_FILE" << EOF
    {
        "name": "$escaped_name",
        "file_name": "$(basename "$file")",
        "path": "$relative_path",
        "api_version": $api_version,
        "version": "$escaped_version",
        "url_mod": "$url_mod",
        "url_raw_mod": "$url_raw_mod",
        "url_readme": "$url_readme",
        "url_raw_readme": "$url_raw_readme",
        "description": "$escaped_desc"
    }
EOF
            
            first_entry=false
            ((mod_count++))
            log "Found mod: $mod_name (API: $api_version, Version: $version)"
        elif [[ "$file" == *.py ]] && has_nomod "$file"; then
            warn "Excluding $(basename "$file") - has nomod header"
            ((excluded_count++))
        fi
    done < <(find "$MODS_DIR" -name "*.py" -type f -print0)
    
    # Close JSON array
    echo "]" >> "$TEMP_FILE"
    
    log "Found $mod_count mod files"
    if [ $excluded_count -gt 0 ]; then
        log "Excluded $excluded_count files with nomod header"
    fi
}

# Function to check if data needs to be updated
needs_update() {
    if [ ! -f "$DATA_FILE" ]; then
        return 0
    fi
    
    # Check if any .py files are newer than data.json
    if find "$MODS_DIR" -name "*.py" -newer "$DATA_FILE" | grep -q .; then
        return 0
    fi
    
    # Check if any .py files were deleted
    local current_files=$(find "$MODS_DIR" -name "*.py" -type f | sort)
    local stored_files=$(jq -r '.[].path' "$DATA_FILE" 2>/dev/null | sort)
    
    if [ "$current_files" != "$stored_files" ]; then
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
        
        # Check for modified mods (simplified - just check if files changed)
        local modified_count=$(find "$MODS_DIR" -name "*.py" -newer "$DATA_FILE" 2>/dev/null | wc -l)
        if [ "$modified_count" -gt 0 ]; then
            echo -e "${YELLOW}Modified files: $modified_count${NC}"
        fi
    else
        log "No existing data.json found - creating new one"
    fi
}

# Main execution
main() {
    log "Starting Mod Manager data generation..."
    log "Repository: $REPO"
    log "Mods directory: $MODS_DIR"
    
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
        log "Changes detected - updating data.json"
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
        log "No changes detected - data.json is up to date"
        rm -f "$TEMP_FILE"
    fi
    
    # Show final statistics
    if [ -f "$DATA_FILE" ]; then
        local total_mods=$(jq 'length' "$DATA_FILE")
        log "Total mods in data.json: $total_mods"
        
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
    fi
    
    log "Mod Manager data generation completed"
}

# Run main function
main "$@"
