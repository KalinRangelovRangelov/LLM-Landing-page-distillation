"""Generate 1000 diverse landing page training examples using DeepSeek API."""
import json
import os
import time
import random
from openai import OpenAI

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

SYSTEM = """You are an expert web developer. When given a landing page request, output ONLY a complete single-file HTML document. No explanations, no markdown, no code fences — just the raw HTML starting with <!DOCTYPE html>.

Requirements:
- Single file with embedded <style> and optional <script>
- Modern, beautiful design
- Responsive (works on mobile and desktop)
- Use system fonts (-apple-system, system-ui, sans-serif)
- Keep it under 200 lines but visually impressive
- Every page must have a UNIQUE layout — vary hero styles, section layouts, color schemes, navigation, footers
- Be creative: use gradients, shadows, animations, grid, flexbox
- DO NOT output any text before or after the HTML"""

# Business types (100)
businesses = [
    "spacecraft manufacturer", "semiconductor chip fab", "luxury cosmetic salon", "defense contractor",
    "elite private school", "specialty coffee roastery", "veterinary clinic", "fintech payment platform",
    "architecture firm", "drone delivery startup", "yoga studio", "cybersecurity firm",
    "space tourism company", "organic farm", "luxury watch brand", "electric vehicle startup",
    "music streaming app", "corporate law firm", "meal prep delivery service", "cloud hosting provider",
    "dental practice", "mobile pet grooming service", "language learning app", "wedding photography studio",
    "moving company", "meditation app", "surf school", "AI research lab",
    "craft brewery", "private jet charter", "rock climbing gym", "botanical garden",
    "3D printing company", "wine vineyard", "video game studio", "solar energy installer",
    "ski resort", "personal trainer platform", "escape room venue", "book publisher",
    "co-working space", "marine biology institute", "tattoo studio", "children's museum",
    "luxury hotel", "robotics company", "perfume house", "mountain bike park",
    "podcast hosting platform", "vintage record store", "sushi restaurant", "quantum computing startup",
    "dog walking service", "Formula 1 racing team", "independent bookshop", "scuba diving school",
    "artisan bakery", "electric bike shop", "interior design studio", "pet adoption agency",
    "classical music orchestra", "food truck collective", "sustainable fashion brand", "art gallery",
    "coworking café", "sleep clinic", "adventure travel agency", "leather goods workshop",
    "aquarium", "helicopter tour company", "cheese shop", "boxing gym",
    "piano tuning service", "mushroom farm", "ice cream parlor", "antique shop",
    "board game café", "flower delivery service", "martial arts dojo", "ballet school",
    "VR arcade", "custom shoe maker", "candle company", "astronomy observatory",
    "food bank charity", "dating app", "genealogy service", "haunted house attraction",
    "puzzle company", "tiny house builder", "hot air balloon rides", "ceramics studio",
    "whiskey distillery", "cat café", "drone racing league", "bonsai nursery",
    "escape boat experience", "rooftop bar", "knife sharpening service", "beekeeping supplies",
]

# Design styles (10)
styles = [
    "Use a dark theme with neon accents and glassmorphism cards.",
    "Use a bright, minimal design with lots of whitespace and a single accent color.",
    "Use a retro/vintage aesthetic with warm gradients, rounded corners, and playful typography.",
    "Use a brutalist design with bold black borders, raw typography, and asymmetric layout.",
    "Use an editorial/magazine layout with large serif headings and elegant spacing.",
    "Use a futuristic design with animated CSS gradients and geometric shapes.",
    "Use a nature-inspired design with earthy greens, organic shapes, and soft shadows.",
    "Use a corporate/professional design with a fixed navbar, hero stats, and client logos section.",
    "Use a vibrant, Gen-Z aesthetic with bold colors, emoji icons, and playful animations.",
    "Use a luxury/premium design with black and gold, thin fonts, and subtle animations.",
]

# Layout variations (10)
layouts = [
    "Include a split hero (text left, image placeholder right), feature grid, and testimonials.",
    "Include a full-screen video placeholder hero, a how-it-works timeline, and a FAQ accordion.",
    "Include a centered hero with floating cards, a pricing table, and a newsletter signup footer.",
    "Include a diagonal hero section, icon feature row, team grid, and a multi-column footer.",
    "Include a sidebar navigation, scrollable content area, stats counters, and a CTA banner.",
    "Include a hero with a search bar, category cards, a featured items carousel placeholder, and social proof.",
    "Include an overlapping hero with cards, a comparison table, and a contact form.",
    "Include a sticky header, parallax-style hero, tabbed features section, and a blog preview grid.",
    "Include a full-width hero, alternating left-right feature sections, and a map placeholder.",
    "Include a animated hero background, a masonry portfolio grid, and a minimalist footer.",
]

# Company names (will be generated)
name_prefixes = [
    "Nova", "Atlas", "Apex", "Ember", "Summit", "Nexus", "Vertex", "Pulse", "Zenith", "Forge",
    "Orbit", "Prism", "Echo", "Flux", "Crest", "Aura", "Onyx", "Velo", "Lux", "Terra",
    "Cobalt", "Helix", "Sage", "Drift", "Peak", "Dusk", "Ivory", "Slate", "Bloom", "Core",
    "Spark", "Tide", "Fern", "Haze", "Frost", "Cedar", "Nimbus", "Vivid", "Amber", "Indigo",
]
name_suffixes = [
    "", " Labs", " Co", " Studio", " Works", " Hub", " HQ", " Group", " Digital", " Collective",
    " Dynamics", " Systems", " Solutions", " Creative", " Design", " Tech", " Inc", " Global",
]


def make_prompt(idx):
    """Generate a unique prompt by combining business + style + layout."""
    biz = businesses[idx % len(businesses)]
    style = styles[idx % len(styles)]
    layout = layouts[idx % len(layouts)]

    prefix = name_prefixes[idx % len(name_prefixes)]
    suffix = name_suffixes[(idx * 7) % len(name_suffixes)]
    name = f"{prefix}{suffix}"

    # Rotate combinations so they don't repeat
    if idx >= len(businesses):
        # Shift style and layout picks to get new combos
        style = styles[(idx * 3) % len(styles)]
        layout = layouts[(idx * 7) % len(layouts)]

    return f"Create a landing page for a {biz} called {name}. {style} {layout}"


def generate_page(prompt, idx, total):
    """Call DeepSeek to generate a landing page."""
    label = prompt[:80]
    print(f"[{idx+1}/{total}] {label}...", end=" ", flush=True)

    for attempt in range(3):
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": SYSTEM},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=4000,
                temperature=0.9,
            )
            html = response.choices[0].message.content

            # Strip markdown fences if present
            if html.startswith("```"):
                html = html.split("\n", 1)[1]
                if html.endswith("```"):
                    html = html[:-3]
                elif "```" in html:
                    html = html[:html.rfind("```")]
            html = html.strip()

            if not html.startswith("<!DOCTYPE") and not html.startswith("<html"):
                # Try to find HTML in response
                start = html.find("<!DOCTYPE")
                if start == -1:
                    start = html.find("<html")
                if start >= 0:
                    html = html[start:]

            tokens = response.usage.total_tokens
            print(f"OK ({len(html)} chars, {tokens} tok)")
            return html

        except Exception as e:
            print(f"retry {attempt+1} ({e})")
            time.sleep(2 ** attempt)

    print("FAILED")
    return None


def main():
    TOTAL = 1010  # 1000 + 10 buffer for failures
    print(f"Generating {TOTAL} landing pages via DeepSeek API...")
    print(f"This will cost approximately $1-3\n")

    all_items = []
    os.makedirs("results/pages/deepseek", exist_ok=True)

    # Check for existing progress
    progress_file = "data_generation_progress.jsonl"
    start_idx = 0
    if os.path.exists(progress_file):
        with open(progress_file) as f:
            all_items = [json.loads(line) for line in f]
        start_idx = len(all_items)
        print(f"Resuming from {start_idx} (already generated)\n")

    for i in range(start_idx, TOTAL):
        if len(all_items) >= 1005:  # enough with buffer
            break

        prompt = make_prompt(i)
        html = generate_page(prompt, i, TOTAL)
        if not html or len(html) < 200:
            continue

        item = {"messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": html}
        ]}
        all_items.append(item)

        # Save preview
        slug = f"{i:04d}"
        with open(f"results/pages/deepseek/{slug}.html", "w") as f:
            f.write(html)

        # Save progress (resume-safe)
        with open(progress_file, "a") as f:
            f.write(json.dumps(item) + "\n")

        time.sleep(0.3)  # rate limit

    # Now split into 3 tiers
    random.seed(42)
    random.shuffle(all_items)

    # Reserve 5 for test, 5 for valid
    test_items = all_items[:5]
    valid_items = all_items[5:10]
    train_all = all_items[10:]

    for size, label in [(50, "sm"), (500, "md"), (1000, "lg")]:
        dirname = f"data_{label}"
        os.makedirs(dirname, exist_ok=True)
        train_subset = train_all[:min(size, len(train_all))]

        for name, items in [("train", train_subset), ("valid", valid_items), ("test", test_items)]:
            with open(f"{dirname}/{name}.jsonl", "w") as f:
                for item in items:
                    f.write(json.dumps(item) + "\n")

        print(f"\n{label}: {len(train_subset)} train, {len(valid_items)} valid, {len(test_items)} test → {dirname}/")

    print("\nDone! Three datasets ready:")
    print("  data_sm/  (50 train)   — quick experiment")
    print("  data_md/  (500 train)  — medium quality")
    print("  data_lg/  (1000 train) — best quality")


if __name__ == "__main__":
    main()
