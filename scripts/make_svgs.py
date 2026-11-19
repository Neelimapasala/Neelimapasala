"""Generates the animated SVGs used in the GitHub profile README.

Run:  python3 scripts/make_svgs.py
Output goes to ./assets/ — commit that folder to the Neelimapasala/Neelimapasala repo.
"""
from pathlib import Path
from xml.sax.saxutils import escape
import textwrap

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

PURPLE, VIOLET, CYAN, BG, PANEL, MUTED, TEXT, GREEN = (
    "#7f00ff", "#a78bfa", "#00d4ff", "#0d1117", "#161b22", "#8b949e", "#e6edf3", "#22c55e")
SANS = "'Segoe UI', Ubuntu, 'Helvetica Neue', Arial, sans-serif"
MONO = "'Fira Code', 'JetBrains Mono', Consolas, 'Courier New', monospace"


def write(name, body):
    (OUT / name).write_text(body, encoding="utf-8")
    print("wrote", name)


def neon_border(w, h, r=14, dur=6):
    """Rounded border with a rotating gradient + a light that travels around it."""
    per = 2 * (w + h)
    return f'''
  <defs>
    <linearGradient id="bd" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{PURPLE}"/><stop offset=".5" stop-color="{CYAN}"/><stop offset="1" stop-color="{PURPLE}"/>
      <animateTransform attributeName="gradientTransform" type="rotate" from="0 .5 .5" to="360 .5 .5" dur="{dur}s" repeatCount="indefinite"/>
    </linearGradient>
  </defs>
  <rect x="1.5" y="1.5" width="{w-3}" height="{h-3}" rx="{r}" fill="{BG}" stroke="url(#bd)" stroke-width="2"/>
  <rect x="1.5" y="1.5" width="{w-3}" height="{h-3}" rx="{r}" fill="none" stroke="{CYAN}" stroke-width="3"
        stroke-dasharray="90 {per}" stroke-linecap="round" opacity=".9">
    <animate attributeName="stroke-dashoffset" from="0" to="-{per+90}" dur="{dur}s" repeatCount="indefinite"/>
  </rect>'''


# ------------------------------------------------------------------ ABOUT ME
def about():
    W, H, CYCLE = 860, 400, 16.0
    lines = [
        ("$ ", "whoami", CYAN),
        ("> ", "Pasala Neelima — AI/ML Engineer & Data Scientist", TEXT),
        ("$ ", "cat education.txt", CYAN),
        ("> ", "🎓 M.Sc. Data Science · Vellore Institute of Technology", TEXT),
        ("$ ", "ls ./focus", CYAN),
        ("> ", "GenAI  AI-Agents  RAG  NLP  Computer-Vision", VIOLET),
        ("$ ", "cat now_learning.md", CYAN),
        ("> ", "Multi-Agent Systems · MLOps · LLM Eval · Advanced RAG", TEXT),
        ("$ ", "echo $GOAL", CYAN),
        ("> ", "Turning data into intelligence 🚀  (open to AI/ML roles)", GREEN),
    ]
    cw = 8.4  # approx char width at 14px mono
    out, defs = [], []
    t = 0.4
    y0 = 92
    for i, (prompt, txt, col) in enumerate(lines):
        y = y0 + i * 27
        full = (len(prompt) + len(txt)) * cw + 30
        typing = 0.9 if prompt == "$ " else 0.35
        k0, k1 = t / CYCLE, (t + typing) / CYCLE
        defs.append(f'''<clipPath id="c{i}"><rect x="30" y="{y-17}" height="24" width="0">
      <animate attributeName="width" dur="{CYCLE}s" repeatCount="indefinite" calcMode="linear"
        values="0;0;{full:.0f};{full:.0f};0" keyTimes="0;{k0:.3f};{k1:.3f};0.96;1"/></rect></clipPath>''')
        pc = GREEN if prompt == "$ " else MUTED
        out.append(f'<g clip-path="url(#c{i})"><text x="34" y="{y}" font-family="{MONO}" font-size="14">'
                   f'<tspan fill="{pc}">{escape(prompt)}</tspan><tspan fill="{col}">{escape(txt)}</tspan></text></g>')
        t += typing + (0.25 if prompt == "$ " else 0.55)
    cursor_y = y0 + len(lines) * 27
    k = t / CYCLE
    cursor = f'''<rect x="34" y="{cursor_y-14}" width="9" height="17" fill="{CYAN}" opacity="0">
      <animate attributeName="opacity" dur="{CYCLE}s" repeatCount="indefinite"
        values="0;0;1;0;1;0;1;0;1;0;0" keyTimes="0;{k:.3f};{k+.04:.3f};{k+.08:.3f};{k+.12:.3f};{k+.16:.3f};{k+.2:.3f};{k+.24:.3f};{k+.28:.3f};0.96;1"/></rect>'''

    # neural network on the right
    nx = [640, 715, 790]
    layers = [[130, 190, 250, 310], [110, 170, 230, 290, 350], [180, 260]]
    edges, nodes = [], []
    n = 0
    for li in range(2):
        for ya in layers[li]:
            for yb in layers[li + 1]:
                d = 1.2 + (n % 5) * 0.23
                edges.append(f'<line x1="{nx[li]}" y1="{ya}" x2="{nx[li+1]}" y2="{yb}" stroke="{VIOLET}" stroke-opacity=".18" stroke-width="1"/>'
                             f'<line x1="{nx[li]}" y1="{ya}" x2="{nx[li+1]}" y2="{yb}" stroke="{CYAN}" stroke-width="1.6" stroke-dasharray="6 120" stroke-linecap="round">'
                             f'<animate attributeName="stroke-dashoffset" from="126" to="0" dur="{d:.2f}s" begin="{(n%7)*0.17:.2f}s" repeatCount="indefinite"/></line>')
                n += 1
    m = 0
    for li, ys in enumerate(layers):
        col = [CYAN, VIOLET, GREEN][li]
        for y in ys:
            nodes.append(f'<circle cx="{nx[li]}" cy="{y}" r="9" fill="{PANEL}" stroke="{col}" stroke-width="2">'
                         f'<animate attributeName="r" values="8;11;8" dur="1.8s" begin="{m*0.21:.2f}s" repeatCount="indefinite"/></circle>'
                         f'<circle cx="{nx[li]}" cy="{y}" r="4" fill="{col}"><animate attributeName="opacity" values=".3;1;.3" dur="1.8s" begin="{m*0.21:.2f}s" repeatCount="indefinite"/></circle>')
            m += 1

    float_icons = "".join(
        f'<text x="{x}" y="{y}" font-size="22">{e}<animateTransform attributeName="transform" type="translate" values="0 0;0 -8;0 0" dur="{d}s" repeatCount="indefinite"/></text>'
        for e, x, y, d in [("🤖", 600, 380, 3), ("🧠", 594, 222, 3.6), ("📊", 815, 380, 2.8), ("✨", 820, 92, 2.4)])

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  {neon_border(W, H)}
  <defs>{"".join(defs)}</defs>
  <!-- terminal -->
  <rect x="18" y="18" width="565" height="364" rx="10" fill="{PANEL}"/>
  <rect x="18" y="18" width="565" height="34" rx="10" fill="#21262d"/>
  <rect x="18" y="40" width="565" height="12" fill="#21262d"/>
  <circle cx="40" cy="35" r="6" fill="#ff5f56"/><circle cx="60" cy="35" r="6" fill="#ffbd2e"/><circle cx="80" cy="35" r="6" fill="#27c93f"/>
  <text x="300" y="40" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{MUTED}">neelima@vit: ~/about-me</text>
  {"".join(out)}
  {cursor}
  <!-- neural net -->
  <text x="715" y="60" text-anchor="middle" font-family="{SANS}" font-size="13" font-weight="600" fill="{VIOLET}" letter-spacing="2">NEURAL NET · TRAINING</text>
  {"".join(edges)}{"".join(nodes)}
  <text x="715" y="395" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MUTED}">loss ↓
    <animate attributeName="opacity" values="1;.4;1" dur="1.5s" repeatCount="indefinite"/></text>
  {float_icons}
</svg>'''
    write("about.svg", svg)


# ------------------------------------------------------------------ REPO CARDS (VFX)
PINK = "#ff2bd6"
REPOS = [
    ("decisiontwin", "🧭", "DecisionTwin AI", "AGENTIC AI", "Agentic AI that turns natural-language business questions into what-if simulations to explore outcomes and risks.", ["Agentic AI", "LLMs", "Simulation"]),
    ("tracelens", "🔍", "TraceLens AI", "AI DEVTOOLS", "AI debugging workspace that links logs, code diffs and API context into evidence-backed findings, patches and tests.", ["AI Agents", "DevTools", "LLMs"]),
    ("vidai", "🎬", "VidAI Studio", "GENERATIVE AI", "One prompt → a full video: AI scripts, scenes, voice-overs, captions and FFmpeg rendering.", ["Python", "GenAI", "FFmpeg"]),
    ("bugagent", "🐞", "AI Bug Detection Agent", "AI AGENT", "An intelligent agent that scans code to detect and explain bugs automatically.", ["AI Agents", "LLMs", "Code Analysis"]),
    ("rag", "📚", "RAG Chatbot Backend", "RAG · LLM", "Retrieval-Augmented Generation chatbot backend for grounded, document-aware answers.", ["Python", "RAG", "Vector DB"]),
    ("quickpark", "🚗", "QuickPark", "COMPUTER VISION", "Smart parking with computer vision for slot detection, booking and traffic insights.", ["Python", "OpenCV", "Analytics"]),
    ("agriai", "🌿", "AgriAI · Plant Disease Dx", "DEEP LEARNING", "Detects plant diseases from leaf images so farmers can act early.", ["Deep Learning", "CNN", "AgriTech"]),
    ("tigerjaguar", "🐯", "Tiger vs Jaguar Classifier", "COMPUTER VISION", "CNN-based wildlife image classifier evaluated with standard performance metrics.", ["TensorFlow", "CNN", "Vision"]),
]
MORE_REPOS = [
    ("querymind", "🧠", "QueryMind · SQL Agent", "AGENTIC AI", "Ask your database questions in plain English: an AI agent writes the SQL, runs it and returns a clean answer.", ["LLM Agent", "SQL", "NL→SQL"]),
    ("docmind", "📄", "DocMind AI", "DOCUMENT AI", "Upload any document and get instant AI-powered answers, summaries, insights and deep analysis.", ["LLMs", "Groq", "Doc QA"]),
    ("promptopt", "🪄", "Prompt AI Optimizer", "PROMPT ENGINEERING", "Detects the domain of a rough prompt, rewrites it with structured guidelines and scores its quality.", ["Prompting", "React", "Analytics"]),
    ("supportagent", "🛒", "E-commerce Support Agent", "MULTI-AGENT RAG", "Multi-agent RAG system that resolves support tickets from policy docs with citations and safety checks.", ["CrewAI", "LangChain", "RAG"]),
    ("disaster", "🌪️", "Disaster Intelligence System", "AI SYSTEM", "AI-powered disaster intelligence system built in Python and deployed as a web app.", ["Python", "AI", "Render"]),
    ("sentiment", "💬", "Twitter Sentiment Analysis", "NLP", "Sentiment classification model that analyzes public opinion and social media trends.", ["NLP", "ML", "Python"]),
]
ACCENTS = [(PURPLE, CYAN), (CYAN, PURPLE), (PINK, PURPLE), (PURPLE, PINK), (CYAN, GREEN), (GREEN, CYAN), (PURPLE, CYAN), (PINK, CYAN)]


def repo_card(slug, icon, title, cat, desc, tags, idx):
    import random
    rnd = random.Random(idx * 31 + 5)
    W, H = 480, 214
    a1, a2 = ACCENTS[idx % len(ACCENTS)]
    t1, t2 = (VIOLET if a1 == PURPLE else a1), (VIOLET if a2 == PURPLE else a2)  # readable text tints
    lines = textwrap.wrap(desc, 56)[:3]
    dl = "".join(f'<tspan x="92" dy="{0 if i == 0 else 18}">{escape(s)}</tspan>' for i, s in enumerate(lines))
    px, pills = 92, []
    for i, tg in enumerate(tags):
        w = len(tg) * 7 + 20
        pills.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{1.0+i*0.15:.2f}s" dur=".4s" fill="freeze"/>'
                     f'<rect x="{px}" y="162" width="{w}" height="24" rx="12" fill="{a1}" fill-opacity=".14" stroke="{a1}" stroke-opacity=".55"/>'
                     f'<text x="{px + w/2}" y="178" text-anchor="middle" font-family="{SANS}" font-size="11" font-weight="600" fill="{TEXT}">{escape(tg)}</text></g>')
        px += w + 8
    parts = "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}"><animate attributeName="cy" values="{y};{y-30}" dur="{d:.1f}s" begin="{-rnd.uniform(0,d):.1f}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="0;.9;0" dur="{d:.1f}s" begin="{-rnd.uniform(0,d):.1f}s" repeatCount="indefinite"/></circle>'
        for x, y, r, c, d in [(rnd.randint(10, W-10), rnd.randint(20, H-10), rnd.choice([.8, 1.1, 1.5]), rnd.choice(["#fff", a1, a2]), rnd.uniform(4, 8)) for _ in range(14)])
    # circuit traces on the right
    traces = []
    for k in range(3):
        y0 = 40 + k * 26
        d = f"M{W} {y0} H{W-60-k*14} V{y0+18} H{W-120-k*10}"
        traces.append(f'<path d="{d}" fill="none" stroke="{a2}" stroke-opacity=".25" stroke-width="1.2"/>'
                      f'<path d="{d}" fill="none" stroke="{a2}" stroke-width="2" stroke-dasharray="10 200" stroke-linecap="round">'
                      f'<animate attributeName="stroke-dashoffset" from="210" to="0" dur="{2+k*0.6:.1f}s" repeatCount="indefinite"/></path>'
                      f'<circle cx="{W-120-k*10}" cy="{y0+18}" r="2.5" fill="{a2}"><animate attributeName="opacity" values=".3;1;.3" dur="1.5s" begin="{k*0.4}s" repeatCount="indefinite"/></circle>')
    per = 2 * (W + H)
    cw = len(cat) * 7.2 + 30
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <clipPath id="fr"><rect x="1" y="1" width="{W-2}" height="{H-2}" rx="16"/></clipPath>
    <filter id="bl" x="-80%" y="-80%" width="260%" height="260%"><feGaussianBlur stdDeviation="38"/></filter>
    <filter id="gl" x="-10%" y="-50%" width="120%" height="200%"><feGaussianBlur stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <linearGradient id="tg" gradientUnits="userSpaceOnUse" x1="0" x2="400" y1="0" y2="0" spreadMethod="repeat">
      <stop offset="0" stop-color="#e9d5ff"/><stop offset=".35" stop-color="{t1}"/><stop offset=".7" stop-color="{t2}"/><stop offset="1" stop-color="#e9d5ff"/>
      <animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="400 0" dur="5s" repeatCount="indefinite"/></linearGradient>
    <linearGradient id="bd" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{a1}"/><stop offset=".5" stop-color="{a2}"/><stop offset="1" stop-color="{a1}"/>
      <animateTransform attributeName="gradientTransform" type="rotate" from="0 .5 .5" to="360 .5 .5" dur="6s" repeatCount="indefinite"/></linearGradient>
    <linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".09"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
  </defs>
  <g clip-path="url(#fr)">
    <rect width="{W}" height="{H}" fill="#07051a"/>
    <circle cx="70" cy="40" r="90" fill="{a1}" opacity=".45" filter="url(#bl)"><animate attributeName="cx" values="70;150;70" dur="11s" repeatCount="indefinite"/></circle>
    <circle cx="{W-60}" cy="{H-20}" r="90" fill="{a2}" opacity=".3" filter="url(#bl)"><animate attributeName="cy" values="{H-20};{H-70};{H-20}" dur="9s" repeatCount="indefinite"/></circle>
    {"".join(traces)}
    {parts}
    <rect x="0" y="0" width="{W}" height="1.5" fill="{a2}" opacity=".25"><animate attributeName="y" values="0;{H}" dur="4s" repeatCount="indefinite"/></rect>
    <rect x="-200" y="0" width="140" height="{H}" fill="url(#sh)" transform="skewX(-20)">
      <animate attributeName="x" values="-200;{W+180};{W+180}" keyTimes="0;.4;1" dur="5s" begin="{idx*0.5:.1f}s" repeatCount="indefinite"/></rect>
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur=".7s" fill="freeze"/>
      <animateTransform attributeName="transform" type="translate" from="0 14" to="0 0" dur=".7s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"/>
      <!-- icon badge -->
      <circle cx="48" cy="58" r="30" fill="#120b2e" stroke="{a1}" stroke-width="1.5"/>
      <circle cx="48" cy="58" r="36" fill="none" stroke="{a2}" stroke-width="1.5" stroke-dasharray="4 6">
        <animateTransform attributeName="transform" type="rotate" from="0 48 58" to="360 48 58" dur="12s" repeatCount="indefinite"/></circle>
      <circle cx="48" cy="58" r="30" fill="none" stroke="{a1}" stroke-width="2" opacity=".6"><animate attributeName="r" values="30;40" dur="2.2s" repeatCount="indefinite"/><animate attributeName="opacity" values=".6;0" dur="2.2s" repeatCount="indefinite"/></circle>
      <text x="48" y="68" text-anchor="middle" font-size="28">{icon}<animateTransform attributeName="transform" type="translate" values="0 0;0 -4;0 0" dur="2.6s" repeatCount="indefinite"/></text>
      <!-- category -->
      <rect x="92" y="22" width="{cw:.0f}" height="20" rx="10" fill="{t2}" fill-opacity=".12" stroke="{t2}" stroke-opacity=".5"/>
      <circle cx="104" cy="32" r="3" fill="{t2}"><animate attributeName="opacity" values="1;.2;1" dur="1.2s" repeatCount="indefinite"/></circle>
      <text x="113" y="36" font-family="{MONO}" font-size="10" font-weight="700" letter-spacing="1.5" fill="{t2}">{escape(cat)}</text>
      <text x="92" y="72" font-family="{SANS}" font-size="21" font-weight="800" fill="url(#tg)" filter="url(#gl)">{escape(title)}</text>
      <text x="92" y="100" font-family="{SANS}" font-size="12.5" fill="{TEXT}" fill-opacity=".85">{dl}</text>
    </g>
    {"".join(pills)}
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="1.4s" dur=".5s" fill="freeze"/>
      <text x="{W-58}" y="199" text-anchor="end" font-family="{MONO}" font-size="10.5" font-weight="700" letter-spacing="2" fill="{t2}">VIEW PROJECT</text>
      <text x="{W-50}" y="200" font-family="{SANS}" font-size="15" font-weight="700" fill="{t2}">→<animateTransform attributeName="transform" type="translate" values="0 0;6 0;0 0" dur="1.2s" repeatCount="indefinite"/></text>
    </g>
    <g stroke="{a2}" stroke-width="2" fill="none" opacity=".6">
      <path d="M10 26 V10 H26"/><path d="M{W-26} {H-10} H{W-10} V{H-26}"/>
    </g>
  </g>
  <rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="16" fill="none" stroke="url(#bd)" stroke-width="2"/>
  <rect x="1.5" y="1.5" width="{W-3}" height="{H-3}" rx="16" fill="none" stroke="#fff" stroke-width="2.5" stroke-opacity=".8"
        stroke-dasharray="70 {per}" stroke-linecap="round"><animate attributeName="stroke-dashoffset" from="0" to="-{per+70}" dur="{5+idx%3}s" repeatCount="indefinite"/></rect>
</svg>'''
    write(f"repo-{slug}.svg", svg)


def projects_header():
    import random
    rnd = random.Random(3)
    W, H = 1000, 130
    bars = "".join(
        f'<rect x="{x}" y="0" width="5" height="40" rx="2" fill="url(#eq)" transform="translate(0 {H-24}) scale(1 -1)">'
        f'<animate attributeName="height" values="{";".join(str(rnd.randint(6, 46)) for _ in range(6))}" dur="{rnd.uniform(1.2, 2.2):.1f}s" repeatCount="indefinite"/></rect>'
        for x in range(W - 170, W - 30, 9))
    stream = "".join(
        f'<text x="{x}" y="0" font-family="{MONO}" font-size="11" fill="{c}" opacity=".35">{rnd.choice(["01", "10", "11", "AI", "ML", "∑", "λ", "∇"])}'
        f'<animate attributeName="y" values="-10;{H+10}" dur="{rnd.uniform(3, 6):.1f}s" begin="{-rnd.uniform(0, 6):.1f}s" repeatCount="indefinite"/></text>'
        for x, c in [(rnd.randint(20, 220), rnd.choice([CYAN, VIOLET])) for _ in range(16)])
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <clipPath id="fr"><rect width="{W}" height="{H}" rx="18"/></clipPath>
    <filter id="bl" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="45"/></filter>
    <filter id="gl" x="-10%" y="-50%" width="120%" height="200%"><feGaussianBlur stdDeviation="7" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <linearGradient id="tg" gradientUnits="userSpaceOnUse" x1="0" x2="600" y1="0" y2="0" spreadMethod="repeat">
      <stop offset="0" stop-color="#c4b5fd"/><stop offset=".33" stop-color="{CYAN}"/><stop offset=".66" stop-color="{PINK}"/><stop offset="1" stop-color="#c4b5fd"/>
      <animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="600 0" dur="6s" repeatCount="indefinite"/></linearGradient>
    <linearGradient id="eq" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{PURPLE}"/></linearGradient>
  </defs>
  <g clip-path="url(#fr)">
    <rect width="{W}" height="{H}" fill="#07051a"/>
    <circle cx="300" cy="60" r="140" fill="{PURPLE}" opacity=".45" filter="url(#bl)"><animate attributeName="cx" values="300;600;300" dur="14s" repeatCount="indefinite"/></circle>
    <circle cx="850" cy="80" r="120" fill="{CYAN}" opacity=".25" filter="url(#bl)"/>
    {stream}
    {bars}
    <text x="{W/2}" y="64" text-anchor="middle" font-family="{SANS}" font-size="38" font-weight="800" letter-spacing="3" fill="url(#tg)" filter="url(#gl)">FEATURED AI PROJECTS</text>
    <text x="{W/2}" y="96" text-anchor="middle" font-family="{MONO}" font-size="13" letter-spacing="2" fill="{MUTED}">agents · LLMs · RAG · computer vision · deep learning</text>
    <rect x="0" y="0" width="{W}" height="1.5" fill="{CYAN}" opacity=".3"><animate attributeName="y" values="0;{H}" dur="3.5s" repeatCount="indefinite"/></rect>
    <g stroke="{CYAN}" stroke-width="2" fill="none" opacity=".7"><path d="M14 34 V14 H34"/><path d="M{W-34} {H-14} H{W-14} V{H-34}"/>
      <animate attributeName="opacity" values=".3;.9;.3" dur="3s" repeatCount="indefinite"/></g>
  </g>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="17" fill="none" stroke="url(#tg)" stroke-width="2" opacity=".8"/>
</svg>'''
    write("projects-header.svg", svg)


# ------------------------------------------------------------------ GAME: TIC-TAC-TOE vs MINIMAX AI
def tictactoe():
    W, H, CYC = 410, 330, 11.0
    gx, gy, cs = 115, 70, 60
    moves = [(0, "X"), (4, "O"), (1, "X"), (2, "O"), (8, "X"), (6, "O")]
    status = ["Your move, human…", "🤖 AI thinking… (minimax)"]
    els = []

    def kt(a, b=None):
        a /= CYC
        return f'values="0;0;1;1;0" keyTimes="0;{a:.3f};{a+0.02:.3f};0.93;1"'

    for i, (cell, who) in enumerate(moves):
        t = 0.8 + i * 1.25
        cx, cy = gx + (cell % 3) * cs + cs / 2, gy + (cell // 3) * cs + cs / 2
        if who == "X":
            g = (f'<line x1="{cx-15}" y1="{cy-15}" x2="{cx+15}" y2="{cy+15}" stroke="{CYAN}" stroke-width="6" stroke-linecap="round"/>'
                 f'<line x1="{cx+15}" y1="{cy-15}" x2="{cx-15}" y2="{cy+15}" stroke="{CYAN}" stroke-width="6" stroke-linecap="round"/>')
        else:
            g = f'<circle cx="{cx}" cy="{cy}" r="17" fill="none" stroke="{VIOLET}" stroke-width="6"/>'
        els.append(f'<g opacity="0"><animate attributeName="opacity" dur="{CYC}s" repeatCount="indefinite" {kt(t)}/>{g}</g>')
        # status line for each turn
        nxt = 0.8 + (i + 1) * 1.25 if i < 5 else 7.6
        s = status[1] if who == "X" else status[0]
        a, b = t / CYC, nxt / CYC
        els.append(f'<text x="{W/2}" y="292" text-anchor="middle" font-family="{SANS}" font-size="14" fill="{VIOLET if who=="X" else CYAN}" opacity="0">{escape(s)}'
                   f'<animate attributeName="opacity" dur="{CYC}s" repeatCount="indefinite" values="0;0;1;1;0;0" keyTimes="0;{a:.3f};{a+.01:.3f};{b-.01:.3f};{b:.3f};1"/></text>')
    # first status before move 1
    els.append(f'<text x="{W/2}" y="292" text-anchor="middle" font-family="{SANS}" font-size="14" fill="{CYAN}">{status[0]}'
               f'<animate attributeName="opacity" dur="{CYC}s" repeatCount="indefinite" values="1;1;0;0;1" keyTimes="0;{0.79/CYC:.3f};{0.8/CYC:.3f};0.99;1"/></text>')
    # win line 2 -> 6
    x1, y1 = gx + 2 * cs + cs - 10, gy + 10
    x2, y2 = gx + 10, gy + 3 * cs - 10
    L = ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
    a = 7.4 / CYC
    els.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{GREEN}" stroke-width="7" stroke-linecap="round" stroke-dasharray="{L:.0f}" stroke-dashoffset="{L:.0f}" opacity="0">'
               f'<animate attributeName="opacity" dur="{CYC}s" repeatCount="indefinite" values="0;0;1;1;0" keyTimes="0;{a:.3f};{a+.001:.3f};0.93;1"/>'
               f'<animate attributeName="stroke-dashoffset" dur="{CYC}s" repeatCount="indefinite" values="{L:.0f};{L:.0f};0;0;{L:.0f}" keyTimes="0;{a:.3f};{a+.05:.3f};0.93;1"/></line>')
    a = 7.6 / CYC
    els.append(f'<text x="{W/2}" y="292" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="700" fill="{GREEN}" opacity="0">🏆 AI WINS — diagonal!'
               f'<animate attributeName="opacity" dur="{CYC}s" repeatCount="indefinite" values="0;0;1;.4;1;.4;1;0" keyTimes="0;{a:.3f};{a+.03:.3f};{a+.07:.3f};{a+.11:.3f};{a+.15:.3f};0.93;1"/></text>')
    grid = "".join(
        f'<line x1="{gx+i*cs}" y1="{gy+6}" x2="{gx+i*cs}" y2="{gy+3*cs-6}" stroke="{MUTED}" stroke-opacity=".5" stroke-width="3" stroke-linecap="round"/>'
        f'<line x1="{gx+6}" y1="{gy+i*cs}" x2="{gx+3*cs-6}" y2="{gy+i*cs}" stroke="{MUTED}" stroke-opacity=".5" stroke-width="3" stroke-linecap="round"/>'
        for i in (1, 2))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  {neon_border(W, H, 14, 7)}
  <text x="{W/2}" y="34" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="700" fill="{TEXT}">🎮 Tic-Tac-Toe vs Minimax AI</text>
  <text x="{W/2}" y="54" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MUTED}">❌ Human   ⭕ AI · game-tree search</text>
  {grid}
  {"".join(els)}
  <text x="{W/2}" y="316" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{MUTED}" opacity=".7">nodes searched: 549,946 · best move found</text>
</svg>'''
    write("game-tictactoe.svg", svg)


# ------------------------------------------------------------------ GAME: AI AGENT RUNNER
def runner():
    W, H = 410, 330
    ground = 250
    robot_x = 70
    travel, dur = 470.0, 3.0               # bug moves 470px in 3s, starting at x=430
    hit_t = (430 - robot_x) / travel * dur  # when a bug reaches the robot
    period = dur / 2                        # two bugs, evenly spaced
    phase = (hit_t % period) / period
    a, b = max(phase - 0.22, 0), min(phase + 0.22, 1)
    jump = f'values="0 0;0 0;0 -70;0 0;0 0" keyTimes="0;{a:.3f};{phase:.3f};{b:.3f};1" calcMode="spline" keySplines="0 0 1 1;.2 .7 .4 1;.6 0 .8 .3;0 0 1 1"'
    bugs = "".join(
        f'<text y="{ground-4}" font-size="26" x="0">{e}<animateTransform attributeName="transform" type="translate" from="430 0" to="-40 0" dur="{dur}s" begin="{beg}s" repeatCount="indefinite"/></text>'
        for e, beg in [("🐞", 0), ("🐛", -period)])
    stars = "".join(
        f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" opacity=".6"><animate attributeName="cx" from="{x}" to="{x-420}" dur="{s}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values=".2;.8;.2" dur="{s/4:.1f}s" repeatCount="indefinite"/></circle>'
        f'<circle cx="{x+420}" cy="{y}" r="{r}" fill="#fff" opacity=".6"><animate attributeName="cx" from="{x+420}" to="{x}" dur="{s}s" repeatCount="indefinite"/></circle>'
        for x, y, r, s in [(40, 90, 1.2, 9), (120, 130, 1, 12), (210, 80, 1.5, 8), (300, 150, 1, 11), (370, 100, 1.3, 10), (260, 190, 1, 13)])
    tokens = "".join(
        f'<text y="{y}" font-size="16" x="0" opacity=".9">{e}<animateTransform attributeName="transform" type="translate" from="440 0" to="-40 0" dur="{s}s" begin="{bg}s" repeatCount="indefinite"/></text>'
        for e, y, s, bg in [("⭐", 175, 4.5, 0), ("💡", 150, 5.5, -2), ("📊", 200, 6, -4)])
    score = "".join(
        f'<text x="140" y="297" font-family="{MONO}" font-size="14" font-weight="700" fill="{GREEN}" opacity="0">{v * 7 + 42}<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;{i/10:.2f};{i/10+.001:.3f};{(i+1)/10:.3f};1" dur="{period*10}s" begin="{hit_t:.2f}s" repeatCount="indefinite"/></text>'
        for i, v in enumerate(range(10)))
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  {neon_border(W, H, 14, 8)}
  <defs><clipPath id="ar"><rect x="4" y="60" width="{W-8}" height="{H-64}" rx="12"/></clipPath>
    <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#1a1040"/><stop offset="1" stop-color="{BG}"/></linearGradient></defs>
  <text x="{W/2}" y="34" text-anchor="middle" font-family="{SANS}" font-size="16" font-weight="700" fill="{TEXT}">🕹️ AI Agent Runner</text>
  <text x="{W/2}" y="54" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MUTED}">reinforcement-learned to dodge bugs</text>
  <g clip-path="url(#ar)">
    <rect x="4" y="60" width="{W-8}" height="{H-64}" fill="url(#sky)"/>
    {stars}
    <text x="320" y="110" font-size="30" opacity=".85">🌙</text>
    {tokens}
    <line x1="0" y1="{ground}" x2="{W}" y2="{ground}" stroke="{VIOLET}" stroke-width="2"/>
    <line x1="0" y1="{ground+14}" x2="{W}" y2="{ground+14}" stroke="{PURPLE}" stroke-opacity=".6" stroke-width="2" stroke-dasharray="14 18">
      <animate attributeName="stroke-dashoffset" from="0" to="64" dur=".4s" repeatCount="indefinite"/></line>
    {bugs}
    <g><animateTransform attributeName="transform" type="translate" dur="{period}s" repeatCount="indefinite" {jump}/>
      <ellipse cx="{robot_x+16}" cy="{ground-2}" rx="14" ry="3" fill="{CYAN}" opacity=".35"/>
      <text x="{robot_x}" y="{ground-4}" font-size="34">🤖</text>
    </g>
    <rect x="16" y="272" width="{W-32}" height="40" rx="10" fill="{PANEL}" fill-opacity=".85"/>
    <text x="30" y="297" font-family="{MONO}" font-size="12" fill="{MUTED}">BUGS DODGED ×</text>
    {score}
    <text x="{W-30}" y="297" text-anchor="end" font-family="{MONO}" font-size="12" fill="{CYAN}">reward ↑ ε=0.05
      <animate attributeName="opacity" values="1;.4;1" dur="1.2s" repeatCount="indefinite"/></text>
  </g>
</svg>'''
    write("game-runner.svg", svg)


# ------------------------------------------------------------------ AI WORKFLOW PIPELINE
def pipeline():
    W, H, CYC = 860, 230, 7.0
    steps = [("📊", "Data", "collect · clean"), ("🔬", "EDA", "explore · insight"),
             ("🧠", "ML / DL", "train · tune"), ("💬", "LLM + RAG", "retrieve · gen"),
             ("🤖", "AI Agent", "reason · act"), ("🚀", "Deploy", "API · app")]
    n = len(steps)
    bw, bh, gap = 112, 110, 26
    x0 = (W - (n * bw + (n - 1) * gap)) / 2
    y = 78
    path_y = y + bh / 2
    first_x, last_x = x0 + bw / 2, x0 + (n - 1) * (bw + gap) + bw / 2
    parts = [f'<line x1="{first_x}" y1="{path_y}" x2="{last_x}" y2="{path_y}" stroke="{VIOLET}" stroke-opacity=".35" stroke-width="2" stroke-dasharray="6 6">'
             f'<animate attributeName="stroke-dashoffset" from="24" to="0" dur=".8s" repeatCount="indefinite"/></line>']
    for i, (e, t, sub) in enumerate(steps):
        x = x0 + i * (bw + gap)
        a = (i / (n - 1)) * 0.8
        hl = (f'values="{VIOLET};{VIOLET};{CYAN};{VIOLET};{VIOLET}" '
              f'keyTimes="0;{max(a - .001, 0):.3f};{a + .04:.3f};{min(a + .16, 0.99):.3f};1"')
        parts.append(
            f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{i * 0.15:.2f}s" dur=".5s" fill="freeze"/>'
            f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="14" fill="{PANEL}" stroke="{VIOLET}" stroke-width="2">'
            f'<animate attributeName="stroke" dur="{CYC}s" repeatCount="indefinite" {hl}/></rect>'
            f'<text x="{x + bw / 2}" y="{y + 42}" text-anchor="middle" font-size="28">{e}</text>'
            f'<text x="{x + bw / 2}" y="{y + 72}" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="700" fill="{TEXT}">{escape(t)}</text>'
            f'<text x="{x + bw / 2}" y="{y + 92}" text-anchor="middle" font-family="{MONO}" font-size="10" fill="{MUTED}">{escape(sub)}</text></g>')
    parts.append(
        f'<circle r="7" cx="{first_x}" cy="{path_y}" fill="{CYAN}">'
        f'<animate attributeName="cx" values="{first_x};{last_x};{last_x}" keyTimes="0;.8;1" dur="{CYC}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.8;.82;1" dur="{CYC}s" repeatCount="indefinite"/>'
        f'<animate attributeName="r" values="6;9;6" dur=".7s" repeatCount="indefinite"/></circle>')
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  {neon_border(W, H, 14, 8)}
  <text x="{W / 2}" y="40" text-anchor="middle" font-family="{SANS}" font-size="15" font-weight="700" fill="{VIOLET}" letter-spacing="3">HOW I BUILD AI · END TO END</text>
  <text x="{W / 2}" y="60" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{MUTED}">from raw data to deployed intelligent agents</text>
  {"".join(parts)}
  <text x="{W / 2}" y="{H - 14}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{GREEN}" opacity="0">✔ model shipped<animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.8;.82;.98;1" dur="{CYC}s" repeatCount="indefinite"/></text>
</svg>'''
    write("pipeline.svg", svg)


# ------------------------------------------------------------------ HERO BANNER
def hero():
    import random
    rnd = random.Random(7)
    W, H = 1000, 380
    PINK = "#ff2bd6"
    NAME = "Pasala Neelima"
    NX, NY = 64, 158

    # aurora blobs
    blobs = "".join(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c}" opacity="{o}" filter="url(#blur)">'
        f'<animate attributeName="cx" values="{cx};{cx+dx};{cx}" dur="{d}s" repeatCount="indefinite"/>'
        f'<animate attributeName="cy" values="{cy};{cy+dy};{cy}" dur="{d*1.3:.1f}s" repeatCount="indefinite"/></circle>'
        for cx, cy, r, c, o, dx, dy, d in [(180, 90, 170, PURPLE, .55, 140, 40, 14), (820, 120, 170, CYAN, .35, -120, 60, 17),
                                           (520, 330, 150, PINK, .28, 160, -50, 19), (980, 340, 120, PURPLE, .4, -80, -40, 15)])

    # synthwave perspective grid
    vx, vy = 500, 250
    grid = "".join(f'<line x1="{vx}" y1="{vy}" x2="{x}" y2="{H}" />' for x in range(-700, 1701, 100))
    hlines = "".join(
        f'<line x1="0" x2="{W}" y1="{vy}" y2="{vy}"><animate attributeName="y1" values="{vy};{H}" dur="3s" begin="{-i*0.75}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;1" keySplines=".6 0 1 1"/>'
        f'<animate attributeName="y2" values="{vy};{H}" dur="3s" begin="{-i*0.75}s" repeatCount="indefinite" calcMode="spline" keyTimes="0;1" keySplines=".6 0 1 1"/></line>'
        for i in range(4))

    # particles
    parts = []
    for _ in range(46):
        x, y = rnd.randint(10, W - 10), rnd.randint(10, H - 10)
        r = rnd.choice([0.8, 1, 1.2, 1.6, 2])
        d = rnd.uniform(5, 11)
        c = rnd.choice(["#ffffff", CYAN, VIOLET])
        parts.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{c}">'
                     f'<animate attributeName="cy" values="{y};{y-50}" dur="{d:.1f}s" begin="{-rnd.uniform(0, d):.1f}s" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="0;.9;0" dur="{d:.1f}s" begin="{-rnd.uniform(0, d):.1f}s" repeatCount="indefinite"/></circle>')

    # roles typing carousel
    roles = ["AI/ML Engineer", "Generative AI Builder", "LLM · RAG · AI Agents", "Computer Vision & NLP"]
    SLOT, CYC = 3.4, 3.4 * len(roles)
    RX, RY, CW = NX + 30, 214, 14.5
    role_defs, role_txt = [], []
    for i, ro in enumerate(roles):
        w = len(ro) * CW + 4
        s = i * SLOT
        pts = [(0, 0)] + ([(s, 0)] if s > 0 else []) + [(s + 1.1, w), (s + 2.6, w), (s + 3.1, 0), (CYC, 0)]
        kt = ";".join(f"{t/CYC:.4f}" for t, _ in pts)
        vals = ";".join(f"{v:.0f}" for _, v in pts)
        xs = ";".join(f"{RX + v:.0f}" for _, v in pts)
        role_defs.append(f'<clipPath id="r{i}"><rect x="{RX}" y="{RY-26}" height="36" width="0">'
                         f'<animate attributeName="width" values="{vals}" keyTimes="{kt}" dur="{CYC}s" repeatCount="indefinite"/></rect></clipPath>')
        on = f"0;0;1;1;0;0" if s > 0 else "1;1;0;0"
        okt = (f"0;{s/CYC:.4f};{(s+.01)/CYC:.4f};{(s+3.1)/CYC:.4f};{(s+3.11)/CYC:.4f};1" if s > 0
               else f"0;{3.1/CYC:.4f};{3.11/CYC:.4f};1")
        role_txt.append(
            f'<text x="{RX}" y="{RY}" clip-path="url(#r{i})" font-family="{MONO}" font-size="24" font-weight="600" fill="url(#roleg)">{escape(ro)}</text>'
            f'<rect y="{RY-22}" width="3" height="28" fill="{CYAN}" x="{RX}" opacity="0">'
            f'<animate attributeName="x" values="{xs}" keyTimes="{kt}" dur="{CYC}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="{on}" keyTimes="{okt}" dur="{CYC}s" repeatCount="indefinite"/></rect>')

    # chips
    chips_data = [("🎓", "M.Sc. Data Science · VIT", VIOLET), ("📍", "Chennai, India", CYAN), (None, "Open to AI/ML roles", GREEN)]
    cx, chips = NX, []
    for i, (e, t, c) in enumerate(chips_data):
        w = len(t) * 7.3 + (44 if e or True else 26)
        icon = (f'<text x="{cx+14}" y="{280}" font-size="14">{e}</text>' if e else
                f'<circle cx="{cx+20}" cy="275" r="4.5" fill="{GREEN}"><animate attributeName="r" values="4;6;4" dur="1.4s" repeatCount="indefinite"/></circle>'
                f'<circle cx="{cx+20}" cy="275" r="4" fill="none" stroke="{GREEN}"><animate attributeName="r" values="4;12" dur="1.4s" repeatCount="indefinite"/><animate attributeName="opacity" values=".9;0" dur="1.4s" repeatCount="indefinite"/></circle>')
        chips.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{1.0+i*0.2:.1f}s" dur=".6s" fill="freeze"/>'
                     f'<animateTransform attributeName="transform" type="translate" from="0 10" to="0 0" begin="{1.0+i*0.2:.1f}s" dur=".6s" fill="freeze"/>'
                     f'<rect x="{cx}" y="259" width="{w:.0f}" height="32" rx="16" fill="#0d0a1f" fill-opacity=".75" stroke="{c}" stroke-opacity=".6"/>'
                     f'{icon}<text x="{cx+36}" y="280" font-family="{SANS}" font-size="13" font-weight="600" fill="{TEXT}">{escape(t)}</text></g>')
        cx += w + 10

    # holographic AI core with orbiting skills
    OX, OY = 810, 178
    orbit_items = [("LLMs", VIOLET, 112, 16, 0), ("RAG", CYAN, 112, 16, -4), ("Agents", GREEN, 112, 16, -8), ("Vision", PINK, 112, 16, -12),
                   ("NLP", CYAN, 70, 11, 0), ("ML", VIOLET, 70, 11, -5.5)]
    orbits = []
    for label, c, r, d, beg in orbit_items:
        path = f"M{OX-r},{OY} a{r},{r} 0 1,1 {2*r},0 a{r},{r} 0 1,1 {-2*r},0"
        w = len(label) * 7.5 + 18
        orbits.append(f'<g><animateMotion path="{path}" dur="{d}s" begin="{beg}s" repeatCount="indefinite"/>'
                      f'<rect x="{-w/2}" y="-11" width="{w}" height="22" rx="11" fill="#0d0a1f" stroke="{c}" stroke-width="1.5"/>'
                      f'<text x="0" y="4.5" text-anchor="middle" font-family="{MONO}" font-size="11" font-weight="700" fill="{c}">{label}</text></g>')
    core = f'''
  <g>
    <circle cx="{OX}" cy="{OY}" r="150" fill="url(#coreGlow)"/>
    <circle cx="{OX}" cy="{OY}" r="112" fill="none" stroke="{VIOLET}" stroke-opacity=".35" stroke-dasharray="2 8">
      <animateTransform attributeName="transform" type="rotate" from="0 {OX} {OY}" to="360 {OX} {OY}" dur="40s" repeatCount="indefinite"/></circle>
    <circle cx="{OX}" cy="{OY}" r="70" fill="none" stroke="{CYAN}" stroke-opacity=".35" stroke-dasharray="12 6">
      <animateTransform attributeName="transform" type="rotate" from="360 {OX} {OY}" to="0 {OX} {OY}" dur="24s" repeatCount="indefinite"/></circle>
    <circle cx="{OX}" cy="{OY}" r="92" fill="none" stroke="url(#arc)" stroke-width="3" stroke-dasharray="120 460" stroke-linecap="round">
      <animateTransform attributeName="transform" type="rotate" from="0 {OX} {OY}" to="360 {OX} {OY}" dur="4s" repeatCount="indefinite"/></circle>
    <path d="M{OX},{OY} L{OX+112},{OY} A112,112 0 0,0 {OX+97},{OY-56} Z" fill="url(#sweep)" opacity=".5">
      <animateTransform attributeName="transform" type="rotate" from="0 {OX} {OY}" to="-360 {OX} {OY}" dur="6s" repeatCount="indefinite"/></path>
    <circle cx="{OX}" cy="{OY}" r="40" fill="#120b2e" stroke="{CYAN}" stroke-width="2" filter="url(#glow)">
      <animate attributeName="r" values="38;43;38" dur="2.4s" repeatCount="indefinite"/></circle>
    <text x="{OX}" y="{OY+15}" text-anchor="middle" font-size="40">🧠</text>
    {"".join(orbits)}
  </g>'''

    name_txt = f'x="{NX}" y="{NY}" font-family="{SANS}" font-size="66" font-weight="800" letter-spacing="-1"'
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  <defs>
    <clipPath id="frame"><rect width="{W}" height="{H}" rx="22"/></clipPath>
    <filter id="blur" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="55"/></filter>
    <filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <filter id="nameGlow" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur stdDeviation="9" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <linearGradient id="nameg" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="600" y2="0" spreadMethod="repeat">
      <stop offset="0" stop-color="#c4b5fd"/><stop offset=".33" stop-color="{CYAN}"/><stop offset=".66" stop-color="{PINK}"/><stop offset="1" stop-color="#c4b5fd"/>
      <animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="600 0" dur="6s" repeatCount="indefinite"/></linearGradient>
    <linearGradient id="roleg" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{VIOLET}"/></linearGradient>
    <linearGradient id="arc" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity="0"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
    <linearGradient id="sweep" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}" stop-opacity=".0"/><stop offset="1" stop-color="{CYAN}" stop-opacity=".45"/></linearGradient>
    <radialGradient id="coreGlow"><stop offset="0" stop-color="{PURPLE}" stop-opacity=".45"/><stop offset=".6" stop-color="{PURPLE}" stop-opacity=".08"/><stop offset="1" stop-color="{PURPLE}" stop-opacity="0"/></radialGradient>
    <linearGradient id="gridfade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#fff" stop-opacity="1"/></linearGradient>
    <mask id="gm"><rect x="0" y="{vy}" width="{W}" height="{H-vy}" fill="url(#gridfade)"/></mask>
    <linearGradient id="shine" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".85"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <clipPath id="nameClip"><text {name_txt}>{NAME}</text></clipPath>
    {"".join(role_defs)}
  </defs>
  <g clip-path="url(#frame)">
    <rect width="{W}" height="{H}" fill="#07051a"/>
    {blobs}
    <g mask="url(#gm)" stroke="{PURPLE}" stroke-width="1.2" opacity=".55">{grid}{hlines}</g>
    {"".join(parts)}
    <!-- scan line -->
    <rect x="0" y="0" width="{W}" height="2" fill="{CYAN}" opacity=".18"><animate attributeName="y" values="0;{H}" dur="5s" repeatCount="indefinite"/></rect>
    {core}
    <!-- intro label -->
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" begin=".2s" dur=".6s" fill="freeze"/>
      <text x="{NX+2}" y="92" font-family="{MONO}" font-size="14" fill="{CYAN}" letter-spacing="4">&lt;HELLO_WORLD/&gt;  I'M</text>
      <rect x="{NX+2}" y="100" width="46" height="2" fill="{CYAN}"><animate attributeName="width" values="46;150;46" dur="4s" repeatCount="indefinite"/></rect>
    </g>
    <!-- name with glow, glitch + shine -->
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" begin=".4s" dur=".8s" fill="freeze"/>
      <animateTransform attributeName="transform" type="translate" from="-24 0" to="0 0" begin=".4s" dur=".8s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"/>
      <text {name_txt} fill="{CYAN}" opacity="0">{NAME}
        <animate attributeName="opacity" values="0;0;.75;0;.6;0;0" keyTimes="0;.6;.61;.63;.65;.66;1" dur="7s" repeatCount="indefinite"/>
        <animateTransform attributeName="transform" type="translate" values="0 0;-5 1;3 -1;-3 0;0 0" keyTimes="0;.61;.63;.65;1" dur="7s" repeatCount="indefinite"/></text>
      <text {name_txt} fill="{PINK}" opacity="0">{NAME}
        <animate attributeName="opacity" values="0;0;.75;0;.6;0;0" keyTimes="0;.6;.61;.63;.65;.66;1" dur="7s" repeatCount="indefinite"/>
        <animateTransform attributeName="transform" type="translate" values="0 0;5 -1;-3 1;3 0;0 0" keyTimes="0;.61;.63;.65;1" dur="7s" repeatCount="indefinite"/></text>
      <text {name_txt} fill="url(#nameg)" filter="url(#nameGlow)">{NAME}</text>
      <g clip-path="url(#nameClip)"><rect x="-200" y="80" width="120" height="100" fill="url(#shine)" transform="skewX(-20)">
        <animate attributeName="x" values="-200;760;760" keyTimes="0;.35;1" dur="5s" begin="1.5s" repeatCount="indefinite"/></rect></g>
    </g>
    <!-- role typing -->
    <text x="{NX+2}" y="{RY}" font-family="{MONO}" font-size="24" font-weight="700" fill="{GREEN}">&gt;</text>
    {"".join(role_txt)}
    {"".join(chips)}
    <!-- HUD corners -->
    <g stroke="{CYAN}" stroke-width="2" fill="none" opacity=".7">
      <path d="M18 46 V18 H46"/><path d="M{W-46} 18 H{W-18} V46"/><path d="M18 {H-46} V{H-18} H46"/><path d="M{W-46} {H-18} H{W-18} V{H-46}"/>
      <animate attributeName="opacity" values=".35;.9;.35" dur="3s" repeatCount="indefinite"/>
    </g>
    <text x="{W-26}" y="{H-26}" text-anchor="end" font-family="{MONO}" font-size="10" fill="{MUTED}" letter-spacing="2">SYS.STATUS: LEARNING ▮
      <animate attributeName="opacity" values="1;.3;1" dur="1.6s" repeatCount="indefinite"/></text>
  </g>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="21" fill="none" stroke="url(#nameg)" stroke-width="2" opacity=".8"/>
</svg>'''
    write("hero.svg", svg)


if __name__ == "__main__":
    hero()
    about()
    pipeline()
    for i, r in enumerate(REPOS + MORE_REPOS):
        repo_card(*r, i)
    projects_header()
    tictactoe()
    runner()
