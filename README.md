# Resume Builder Agent

A [Claude Code](https://docs.claude.com/en/docs/claude-code) skill I built to review, rebuild and practice a resume. I made it for my own job search as a college senior.

## What it does

Three separate Claudes, each with one job:

| Role | Job |
|---|---|
| **Reviewer** | Reads the resume the way hiring software and a recruiter would. Flags anything that parses wrong, any format problems, and what to cut to fit one page. Scores it out of 10. |
| **Remixer** | Rewrites every bullet with Google's XYZ formula ("Accomplished X, as measured by Y, by doing Z") in a plain human voice. If a bullet has no real number, it asks you for one instead of making it up. |
| **Interviewer** | Runs a six-question mock interview, one question at a time, and scores each answer out of 10 with a specific fix. |

Then a Python builder turns the result into a clean one-page PDF and Word file and checks its own work: exactly one page, no filler words, no em dashes, no lines with a single dangling word.

## Design choices

- **Never invent anything.** No made-up numbers, tools or results. Missing numbers become questions for you.
- **Separate Claudes, not one long prompt.** Each role sees only its own inputs, so you get independent opinions instead of one model agreeing with itself.
- **Your layout and voice win.** If you like how your resume looks, it keeps your format and edits your words instead of replacing them.
- **Privacy.** Phone, email and address are removed before anything goes to a sub-agent.

## Examples (synthetic)

- [Bullet before and after, plus interview feedback](examples/before-after.md)
- [resume.json schema](examples/resume.example.json)

## Install

1. Copy `skill/` to `~/.claude/skills/resume-builder/`.
2. `pip install python-docx pypdf` and have Chrome installed.
3. In Claude Code: `/resume-builder <resume file>`, or `/resume-builder interview` to practice.

It's a structured second opinion, not a guarantee of an interview or a job.
