#!/bin/bash
#
# daily-rollover.sh - archive the running daily note and reseed it for today.
#
# The vault has ONE file you write in every day: vault/daily/today.md. Its
# frontmatter carries the date it belongs to. This script checks that stamped
# date: if it is not today, the file is archived to vault/daily/<date>.md and
# today.md is rewritten from vault/templates/daily.md with the new date.
#
# RUN THIS BY HAND. There is no scheduled job, by design (see below). Run it
# whenever you sit down to write, before opening the vault:
#
#   /Users/monishver/Downloads/site-v2/tooling/daily-rollover.sh
#
#   --dry-run    print what it would do, change nothing
#
# Running it by hand is safe and cheap because it is idempotent and catches up.
# Running it twice does nothing the second time. Running it after the Mac was
# off, or after you forgot for a week, still archives the stale note under its
# correct date. So there is no such thing as running it too often, and missing
# a day costs you nothing.
#
# Note the day boundary is the date STAMPED in today.md, not the wall clock, so
# writing at 1am still lands in the previous day's note. That was the intent.
#
# WHY NO SCHEDULED JOB: a launchd agent cannot read file contents under
# ~/Downloads (macOS TCC), which is where this project lives, so a scheduled
# run fails with "Operation not permitted". An interactive terminal is granted
# that access, which is why running it yourself works. If the project ever
# moves out of ~/Downloads, tooling/com.monishver.daily-rollover.plist is kept
# in the repo and will work once its ProgramArguments points back here.
# Full detail in progress.md, 2026-07-20.
#
# Nothing here publishes or commits. vault/daily/* is gitignored and stays local.

set -euo pipefail

VAULT="/Users/monishver/Downloads/site-v2/vault"
DAILY_DIR="$VAULT/daily"
TODAY_FILE="$DAILY_DIR/today.md"
TEMPLATE="$VAULT/templates/daily.md"
GOALS="$VAULT/goals.md"
LOG="$DAILY_DIR/.rollover.log"

DRY_RUN=0
[ "${1:-}" = "--dry-run" ] && DRY_RUN=1

TODAY="$(date +%Y-%m-%d)"

log() {
  printf '%s  %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$1" >> "$LOG"
  [ "$DRY_RUN" -eq 1 ] && printf '%s\n' "$1" >&2
  return 0
}

die() {
  log "ERROR: $1"
  printf 'daily-rollover: %s\n' "$1" >&2
  exit 1
}

# Build the Goals block: one "### <goal>" per '## ' heading in goals.md, each
# followed by an empty bullet to fill in.
build_goals() {
  local line out=""
  if [ ! -f "$GOALS" ]; then
    printf '_No goals.md yet._\n'
    return 0
  fi
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in
      '## '*)
        out="${out}### ${line#\#\# }"$'\n'"- "$'\n'
        ;;
    esac
  done < "$GOALS"
  if [ -z "$out" ]; then
    printf '_No active goals in goals.md._\n'
  else
    printf '%s' "$out"
  fi
}

# Render the template for a given date: substitute the date placeholder and
# expand the <!-- goals --> marker.
render_template() {
  local d="$1" line goals_block
  goals_block="$(build_goals)"
  while IFS= read -r line || [ -n "$line" ]; do
    case "$line" in
      '<!-- goals -->')
        printf '%s\n' "$goals_block"
        ;;
      *)
        printf '%s\n' "${line//\{\{date:YYYY-MM-DD\}\}/$d}"
        ;;
    esac
  done < "$TEMPLATE"
}

# Pull "date: YYYY-MM-DD" out of the frontmatter.
stamped_date() {
  awk '
    NR == 1 && $0 != "---" { exit }
    NR > 1 && $0 == "---"  { exit }
    /^date:[[:space:]]*/   { gsub(/^date:[[:space:]]*/, ""); print; exit }
  ' "$TODAY_FILE"
}

write_file() {
  local path="$1" content="$2"
  if [ "$DRY_RUN" -eq 1 ]; then
    log "DRY RUN: would write $path"
    return 0
  fi
  # Trailing newline: command substitution strips it, so put it back.
  printf '%s\n' "$content" > "$path"
}

[ -d "$DAILY_DIR" ] || die "daily dir not found: $DAILY_DIR"
[ -f "$TEMPLATE" ]  || die "template not found: $TEMPLATE"

# No running note yet: seed one and stop.
if [ ! -f "$TODAY_FILE" ]; then
  write_file "$TODAY_FILE" "$(render_template "$TODAY")"
  log "seeded today.md for $TODAY (no prior file)"
  exit 0
fi

STAMP="$(stamped_date)"
if [ -z "$STAMP" ]; then
  die "no 'date:' in $TODAY_FILE frontmatter, refusing to archive blindly"
fi

if [ "$STAMP" = "$TODAY" ]; then
  log "no-op: today.md already stamped $TODAY"
  exit 0
fi

CURRENT="$(cat "$TODAY_FILE")"
PRISTINE="$(render_template "$STAMP")"

if [ "$CURRENT" = "$PRISTINE" ]; then
  # Nothing was written that day. Reseed without leaving an empty archive file.
  write_file "$TODAY_FILE" "$(render_template "$TODAY")"
  log "reseeded for $TODAY; $STAMP was untouched, not archived"
  exit 0
fi

ARCHIVE="$DAILY_DIR/$STAMP.md"
if [ -e "$ARCHIVE" ]; then
  # Never clobber an existing archive. Park the collision beside it instead.
  n=1
  while [ -e "$DAILY_DIR/$STAMP-$n.md" ]; do n=$((n + 1)); done
  ARCHIVE="$DAILY_DIR/$STAMP-$n.md"
  log "WARN: $DAILY_DIR/$STAMP.md exists, archiving to $ARCHIVE instead"
fi

write_file "$ARCHIVE" "$CURRENT"
write_file "$TODAY_FILE" "$(render_template "$TODAY")"
log "archived $STAMP to $(basename "$ARCHIVE"); today.md reseeded for $TODAY"
