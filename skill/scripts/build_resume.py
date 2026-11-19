"""Original-layout resume builder (classic one-column look): name top-left over a rule, contact line split
left/right, bold underlined caps headings, skills bullets near the top, Experience / Other Experience.
Usage: SP=<scratch> python build_resume.py <resume.json> <abs_out_dir>
"""
import html, json, re, subprocess, sys, os, shutil, tempfile
from pathlib import Path

src, out = Path(sys.argv[1]), Path(sys.argv[2])
R = json.loads(src.read_text())
FONT, PT, M = R.get("font", "Times New Roman"), R.get("body_pt", 11), R.get("margin_in", 0.55)
e = html.escape

def entries_html(s):
    o = []
    for en in s.get("entries", []):
        o.append('<div class="entry">')
        o.append(f'<div class="row"><b>{e(en["left"])}</b><b>{e(en.get("right",""))}</b></div>')
        o.append(f'<div class="row"><i>{e(en.get("left2",""))}</i><i>{e(en.get("right2",""))}</i></div>')
        if en.get("bullets"):
            o.append("<ul>" + "".join(f"<li>{e(b)}</li>" for b in en["bullets"]) + "</ul>")
        o.append("</div>")
    return "".join(o)

h = [f"""<!doctype html><html><head><meta charset="utf-8"><title>{e(R['name'])} Resume</title><style>
@page {{ size: Letter; margin: {M}in; }}
body {{ font-family: '{FONT}', serif; font-size: {PT}pt; line-height: 1.17; margin: 0; color: #000; font-variant-ligatures: none; font-feature-settings: 'liga' 0, 'clig' 0; }}
.name {{ font-size: {PT+15}pt; line-height: 1; border-bottom: 1.5px solid #000; padding-bottom: 2px; }}
.row {{ display: flex; justify-content: space-between; }}
h2 {{ font-size: {PT}pt; font-weight: bold; text-decoration: underline; text-transform: uppercase; margin: 7px 0 1px; }}
.entry {{ margin-top: 3px; }}
ul {{ margin: 0; padding-left: 40px; }} li {{ margin: 0; padding-left: 4px; }}
p {{ margin: 0; }}
</style></head><body>
<div class="name">{e(R['name'])}</div>
<div class="row"><span>{e(R['contact_left'])}</span><span>{e(R['contact_right'])}</span></div>
"""]
for s in R["sections"]:
    h.append(f"<h2>{e(s['title'])}</h2>")
    if s.get("text"): h.append(f"<p>{e(s['text'])}</p>")
    if s.get("school"):
        sc = s["school"]
        h.append(f'<div class="row"><b>{e(sc["left"])}</b><b>{e(sc["right"])}</b></div>')
        h.append(f'<div class="row"><span>{e(sc["left2"])}</span><i>{e(sc["right2"])}</i></div>')
        h.extend(f"<p>{e(l)}</p>" for l in sc["lines"])
    if s.get("bullets"):
        h.append("<ul>" + "".join(f"<li>{e(b)}</li>" for b in s["bullets"]) + "</ul>")
    h.append(entries_html(s))
h.append("</body></html>")
(out / "resume.html").write_text("".join(h))

prof = tempfile.mkdtemp(dir=os.environ.get("SP", "/tmp"))
subprocess.run(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", "--headless=new", "--disable-gpu",
                f"--user-data-dir={prof}", "--no-pdf-header-footer", f"--print-to-pdf={prof}/resume.pdf",
                (out / "resume.html").as_uri()], capture_output=True, timeout=90)
shutil.copy(f"{prof}/resume.pdf", out / "resume.pdf")

# ---------- DOCX (same content, tab stops not tables) ----------
from docx import Document
from docx.shared import Pt, Inches
from docx.enum.text import WD_TAB_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

d = Document(); sec = d.sections[0]
sec.page_width, sec.page_height = Inches(8.5), Inches(11)
for side in ("left_margin", "right_margin", "top_margin", "bottom_margin"):
    setattr(sec, side, Inches(M))
W = Inches(8.5 - 2 * M)
st = d.styles["Normal"]; st.font.name, st.font.size = FONT, Pt(PT)
st.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
st.paragraph_format.space_before = st.paragraph_format.space_after = Pt(0)

def para(before=0):
    p = d.add_paragraph(); p.paragraph_format.space_before = Pt(before); return p
def two(left, right, lb=False, li=False, rb=False, ri=False, before=0):
    p = para(before); p.paragraph_format.tab_stops.add_tab_stop(W, WD_TAB_ALIGNMENT.RIGHT)
    r = p.add_run(left); r.bold, r.italic = lb, li
    r = p.add_run("\t" + right); r.bold, r.italic = rb, ri
def bullet(t):
    p = d.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent = Inches(0.55); p.paragraph_format.first_line_indent = Inches(-0.2)
    p.add_run(t)

p = para(); r = p.add_run(R["name"]); r.font.size = Pt(PT + 15)
pPr = p._p.get_or_add_pPr(); b = OxmlElement("w:pBdr"); bt = OxmlElement("w:bottom")
for k, v in (("w:val", "single"), ("w:sz", "12"), ("w:space", "1"), ("w:color", "000000")): bt.set(qn(k), v)
b.append(bt); pPr.append(b)
two(R["contact_left"], R["contact_right"])
for s in R["sections"]:
    p = para(7); r = p.add_run(s["title"].upper()); r.bold = r.underline = True
    if s.get("text"): para().add_run(s["text"])
    if s.get("school"):
        sc = s["school"]
        two(sc["left"], sc["right"], lb=True, rb=True); two(sc["left2"], sc["right2"], ri=True)
        for l in sc["lines"]: para().add_run(l)
    for t in s.get("bullets", []): bullet(t)
    for en in s.get("entries", []):
        two(en["left"], en.get("right", ""), lb=True, rb=True, before=3)
        two(en.get("left2", ""), en.get("right2", ""), li=True, ri=True)
        for t in en.get("bullets", []): bullet(t)
d.save(out / "resume.docx")

# ---------- CHECKS ----------
from pypdf import PdfReader
pdf = PdfReader(str(out / "resume.pdf")); pt = "\n".join(pg.extract_text() for pg in pdf.pages)
(out / "resume-as-ats-sees-it.txt").write_text(pt)
dt = "\n".join(p.text for p in Document(out / "resume.docx").paragraphs)
BANNED = r"\b(leverag\w*|spearhead\w*|utiliz\w*|foster\w*|synerg\w*|dynamic|passionate|results-driven|robust|seamless\w*|cutting-edge|innovative|showcas\w*|delv\w*|orchestrat\w*|hone[ds]?|navigat\w*|ensur\w*|various|responsible for)\b"
print("PDF pages:", len(pdf.pages))
print("banned:", sorted(set(m.lower() for m in re.findall(BANNED, dt, re.I))) or "none", "| dashes:", len(re.findall("[—–]", dt)))
print("orphan lines:", [l for l in pt.splitlines() if len(l.split()) <= 2 and not l.isupper() and not re.search(r"\d{4}|RI$", l)])
