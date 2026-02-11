#!/usr/bin/env bash
set -euo pipefail

TEAM="${1:-}"

if [[ -z "$TEAM" ]]; then
echo "Usage: $0 <teamNumber>"
exit 1
fi

declare -A TEAM_PORT=(
[1]=9101
[2]=9106
[3]=9111
[4]=9116
[5]=9121
[6]=9126
[7]=9131
[8]=9136
[9]=9141
[10]=9146
[11]=9151
[12]=9156
[13]=9161
[14]=9166
[15]=9171
)

if [[ -z "${TEAM_PORT[$TEAM]:-}" ]]; then
echo "Invalid team number: $TEAM"
exit 1
fi

COMPOSE_FILE="../team${TEAM}/docker-compose.yml"

if [[ ! -f "$COMPOSE_FILE" ]]; then
    if [[ -f "../team${TEAM}/docker-compose.yaml" ]]; then
        COMPOSE_FILE="../team${TEAM}/docker-compose.yaml"
    else
        echo "Missing docker-compose file for team $TEAM"
        exit 1
    fi
fi

TARGET_PORT="${TEAM_PORT[$TEAM]}"

echo "Starting team$TEAM on port $TARGET_PORT..."

TEAM_PORT="$TARGET_PORT" docker compose -f "$COMPOSE_FILE" up -d --build

echo "Team $TEAM started: http://localhost:${TARGET_PORT}/"