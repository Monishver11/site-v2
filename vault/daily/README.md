Private daily logs. Excluded from Quartz publish and gitignored, so nothing in
this folder leaves the machine.

## How the daily note works

You write in ONE file: `today.md`. Never rename it, never create dated files by
hand. Its frontmatter `date:` records which day it belongs to.

Everything else in this folder is an archive: `YYYY-MM-DD.md`, one per past day,
created for you.

## Run this before you start writing

```
/Users/monishver/Downloads/site-v2/tooling/daily-rollover.sh
```

If `today.md` still carries an older date, the script files it away as
`YYYY-MM-DD.md` and gives you a fresh `today.md`. If it is already stamped
today, it does nothing.

Run it by hand. There is no scheduled job, by design.

- Run it as often as you like. After the first run each day it is a no-op.
- Forgetting is not destructive. Skip a week and the next run still archives
  that stale note under its correct date. Nothing is lost or misfiled.
- Writing past midnight stays with the previous day, since the day boundary is
  the date stamped in the file, not the wall clock. A 1am entry counts as
  yesterday, which is the intent.

The one thing to avoid is hand-editing the `date:` line in `today.md`, since
that is what the script uses to decide where the note gets filed.

## Goals

The Goals section of each day's note is generated from `../goals.md`, one entry
per `##` heading there. Edit that file to change which goals show up tomorrow.
