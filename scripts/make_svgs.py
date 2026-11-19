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


# ------------------------------------------------------------------ REPO CARDS
REPOS = [
    ("decisiontwin", "🧭", "DecisionTwin AI", "Agentic AI that turns natural-language business questions into what-if simulations to explore outcomes and risks.", ["Agentic AI", "LLMs", "Simulation"]),
    ("tracelens", "🔍", "TraceLens AI", "AI debugging workspace that links logs, code diffs and API context into evidence-backed findings, patches and tests.", ["AI Agents", "DevTools", "LLMs"]),
    ("vidai", "🎬", "VidAI Studio", "One prompt → a full video: AI scripts, scenes, voice-overs, captions and FFmpeg rendering.", ["Python", "GenAI", "FFmpeg"]),
    ("bugagent", "🐞", "AI Bug Detection Agent", "An intelligent agent that scans code to detect and explain bugs automatically.", ["AI Agents", "LLMs", "Code Analysis"]),
    ("rag", "📚", "RAG Chatbot Backend", "Retrieval-Augmented Generation chatbot backend for grounded, document-aware answers.", ["Python", "RAG", "Vector DB"]),
    ("quickpark", "🚗", "QuickPark", "Smart parking with computer vision for slot detection, booking and traffic insights.", ["Python", "OpenCV", "Analytics"]),
    ("agriai", "🌿", "AgriAI · Plant Disease Dx", "Detects plant diseases from leaf images so farmers can act early.", ["Deep Learning", "CNN", "AgriTech"]),
    ("tigerjaguar", "🐯", "Tiger vs Jaguar Classifier", "CNN-based wildlife image classifier evaluated with standard performance metrics.", ["TensorFlow", "CNN", "Vision"]),
]


def repo_card(slug, icon, title, desc, tags, idx):
    W, H = 420, 170
    d = 7 + idx % 3
    desc_lines = textwrap.wrap(desc, 52)[:3]
    dl = "".join(f'<tspan x="70" dy="{0 if i == 0 else 18}">{escape(s)}</tspan>' for i, s in enumerate(desc_lines))
    px, pills = 70, []
    for i, tg in enumerate(tags):
        w = len(tg) * 7 + 18
        pills.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="{0.9+i*0.15:.2f}s" dur=".4s" fill="freeze"/>'
                     f'<rect x="{px}" y="134" width="{w}" height="22" rx="11" fill="{PURPLE}" fill-opacity=".18" stroke="{VIOLET}" stroke-opacity=".5"/>'
                     f'<text x="{px + w/2}" y="149" text-anchor="middle" font-family="{SANS}" font-size="11" fill="{VIOLET}">{escape(tg)}</text></g>')
        px += w + 8
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
  {neon_border(W, H, 12, d)}
  <defs>
    <linearGradient id="tg" x1="0" x2="1"><stop offset="0" stop-color="{VIOLET}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
    <linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".5" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
    <clipPath id="cl"><rect x="2" y="2" width="{W-4}" height="{H-4}" rx="12"/></clipPath>
  </defs>
  <g clip-path="url(#cl)"><rect x="-200" y="0" width="160" height="{H}" fill="url(#sh)" transform="skewX(-20)">
    <animate attributeName="x" values="-200;{W+150};{W+150}" keyTimes="0;.4;1" dur="5s" begin="{idx*0.6:.1f}s" repeatCount="indefinite"/></rect></g>
  <circle cx="38" cy="42" r="22" fill="{PURPLE}" fill-opacity=".15" stroke="{VIOLET}" stroke-opacity=".4">
    <animate attributeName="r" values="20;24;20" dur="2.4s" repeatCount="indefinite"/></circle>
  <text x="38" y="51" text-anchor="middle" font-size="24">{icon}<animateTransform attributeName="transform" type="translate" values="0 0;0 -4;0 0" dur="2.4s" repeatCount="indefinite"/></text>
  <g opacity="0"><animate attributeName="opacity" from="0" to="1" dur=".6s" fill="freeze"/>
    <animateTransform attributeName="transform" type="translate" from="-12 0" to="0 0" dur=".6s" fill="freeze"/>
    <text x="70" y="40" font-family="{SANS}" font-size="18" font-weight="700" fill="url(#tg)">{escape(title)}</text>
    <text x="70" y="58" font-family="{MONO}" font-size="10.5" fill="{MUTED}">github.com/Neelimapasala ↗</text>
  </g>
  <g opacity="0"><animate attributeName="opacity" from="0" to="1" begin=".4s" dur=".6s" fill="freeze"/>
    <text x="70" y="84" font-family="{SANS}" font-size="12.5" fill="{TEXT}" fill-opacity=".85">{dl}</text>
  </g>
  {"".join(pills)}
</svg>'''
    write(f"repo-{slug}.svg", svg)


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


if __name__ == "__main__":
    about()
    for i, r in enumerate(REPOS):
        repo_card(*r, i)
    tictactoe()
    runner()
