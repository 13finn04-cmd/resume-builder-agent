---
name: resume-builder
description: Review and rebuild a resume with three separate Claudes (a format reviewer, a bullet rewriter using Google's XYZ formula, and a mock interviewer that scores answers out of 10), then build a clean one-page resume as .docx and .pdf. Use when the user types /resume-builder followed by a resume (file path or pasted text), asks to "review / fix / rebuild my resume", or wants to "practice interview questions" (/resume-builder interview).
---

# /resume-builder

Three jobs, in this order: find what's unclear or broken (Reviewer), make every bullet stronger without changing what's true (Remixer), then practice talking about it (Interviewer). Then build the page. Never flatter, and never invent anything about the person.

## Facts behind the rules
- **XYZ formula.** Laszlo Bock, Google's former SVP of People Operations (2014): "Accomplished [X] as measured by [Y], by doing [Z]." X = the result, Y = the number or comparison that proves it, Z = what you actually did.
- **How hiring software reads a resume.** The popular "75% of resumes are auto-rejected" line has no real source (it traces to a 2012 sales pitch from a defunct resume company). What actually matters: the file reads cleanly into fields, and a human can understand your real work fast. So the goal is a clean, honest, readable page, not tricks.
- **Clean format** (college career center guides): one column; no tables, text boxes, headers or footers, images or icons; standard section names ("Education", "Experience", "Skills"); a standard font; full month and year for dates; standard round bullets; links as visible URLs.

## 0. Modes
- `/resume-builder <file or text>`: the full run, steps 1 to 5.
- `/resume-builder interview [role]`: the Interviewer only, step 6.

## 1. Read
Read the resume (PDF, .docx or pasted text) and save exactly what text extraction returns to `parsed.txt`, since that is what hiring software sees. Note layout facts: page count, columns, tables, header/footer content, fonts, date format.

The user may share facts that are not on the resume yet. Write them as a "Fact sheet" with the source of each line. Nothing outside the resume and the fact sheet may appear in the new resume.

Remove street address, phone and email before anything goes to a sub-agent.

## 2. Reviewer and Remixer
**Reviewer** (no tools). Inputs: `parsed.txt` and the layout facts.
"You are a hiring-system parser and then the recruiter who reads what it produced. Work only from the text and layout facts given."
Format: PARSE RESULT (fields extracted, anything misread), FORMAT FIXES (each issue quoted, with the fix), ONE PAGE (what to cut or merge, weakest first), SCORE (1 to 10), TOP 5 MUST-FIX. Under 400 words.

**Remixer** (after the Reviewer, no tools). Inputs: the resume text, the fact sheet, the Reviewer's TOP 5.
"You rewrite resume bullets with the XYZ formula. You write like a sharp person talking, not like AI."
- Rewrite every bullet. Keep titles, employers and dates exactly as given.
- Y is a real number from the resume or fact sheet. If there is none, write `[ADD YOUR NUMBER: what to count]`. Never guess a number, never round up.
- One to two lines per bullet, a plain specific verb each time.
- Human voice. Banned: leveraged, spearheaded, utilized, fostered, synergy, dynamic, passionate, results-driven, robust, seamless, cutting-edge, innovative, delve, orchestrated, "responsible for", em dashes. Every line must be something the person can explain out loud in one breath.
Format per role: each bullet as BEFORE / AFTER / X, Y, Z labels.

## 3. Show the review
Print the Reviewer's score and TOP 5, then before and after for the three biggest bullet upgrades. Don't soften anything.

## 4. Build the one-page resume
- **One page, hard limit.** Students: Education, Experience, Skills. Experienced hires: Experience first.
- **Header:** name, then city and state, phone, email and LinkedIn as plain text.
- **Format:** one column, 0.5 to 0.75 inch margins, 10.5 to 11.5 pt, one standard font, right-aligned dates with a tab stop (not a table).
- **The user's own layout and voice win.** If they like their current look, keep it and edit their bullets rather than rewriting from scratch.
- **Builder:** `scripts/build_resume.py` turns a `resume.json` into html, pdf and docx, then checks its own work: exactly one page, banned words, em dashes, and lines with a single orphaned word. See `examples/resume.example.json` for the schema. Run: `SP=<temp dir> python scripts/build_resume.py resume.json <absolute out dir>` (needs python-docx, pypdf and Chrome).
- **PDF trap:** turn off font ligatures (`font-variant-ligatures: none`) or text extraction drops letters ("Staff" becomes "Staf").

## 5. Write the result
`resume-builder-output/` next to the resume: `review.md`, `new-resume.md` (every bullet before and after, plus every `[ADD YOUR NUMBER]` question), `resume.docx`, `resume.pdf`, `parsed.txt`. Never overwrite the original.

## 6. Interviewer (interactive)
Play a hiring manager for the target role. Ask six questions, one at a time, and wait for each answer:
1. "Walk me through your resume."
2. Two behavioral questions from the resume: the strongest bullet and the most surprising one.
3. Two role questions a real interviewer asks for this job.
4. "Why this role, given what you've built?"

Score each answer out of 10: Structure 0 to 3, Specifics 0 to 3, Relevance 0 to 2, Delivery 0 to 2. Then one line on what worked, one fix, and a 10/10 version built only from the person's real resume. End with the average, the weakest area and three questions to drill.

## Rules
- Be honest. If the resume is strong, say so.
- Never invent employers, titles, dates, degrees, licenses, tools, numbers or results.
- This is a structured second opinion from one model playing three parts, not a real recruiter, and not a guarantee of an interview or a job.
