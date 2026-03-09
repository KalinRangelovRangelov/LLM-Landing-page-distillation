"""Generate 50 training + 5 test examples of landing pages."""
import json

def page(title, tagline, color1, color2, sections, extra_css="", extra_html=""):
    """Generate a compact but beautiful single-file landing page."""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<style>
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif; color: #1a1a2e; line-height: 1.6; }}
.hero {{ min-height: 90vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 60px 24px; background: linear-gradient(135deg, {color1}, {color2}); color: #fff; }}
.hero h1 {{ font-size: clamp(2rem, 5vw, 3.5rem); font-weight: 800; margin-bottom: 16px; letter-spacing: -0.5px; }}
.hero p {{ font-size: 1.15rem; max-width: 560px; opacity: 0.9; margin-bottom: 32px; }}
.btn {{ display: inline-block; padding: 14px 32px; border-radius: 8px; font-weight: 600; font-size: 1rem; text-decoration: none; transition: transform 0.2s, box-shadow 0.2s; }}
.btn-primary {{ background: #fff; color: {color1}; box-shadow: 0 4px 15px rgba(0,0,0,0.15); }}
.btn-primary:hover {{ transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,0,0,0.2); }}
.section {{ padding: 80px 24px; max-width: 1100px; margin: 0 auto; }}
.section h2 {{ font-size: 2rem; font-weight: 700; margin-bottom: 12px; text-align: center; }}
.section .subtitle {{ text-align: center; color: #666; margin-bottom: 48px; max-width: 600px; margin-left: auto; margin-right: auto; }}
.grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; }}
.card {{ background: #fff; border: 1px solid #eee; border-radius: 12px; padding: 28px; transition: transform 0.2s, box-shadow 0.2s; }}
.card:hover {{ transform: translateY(-4px); box-shadow: 0 12px 32px rgba(0,0,0,0.08); }}
.card h3 {{ font-size: 1.15rem; margin-bottom: 8px; }}
.card p {{ color: #555; font-size: 0.95rem; }}
.icon {{ font-size: 2rem; margin-bottom: 12px; }}
.cta {{ text-align: center; padding: 80px 24px; background: linear-gradient(135deg, {color1}, {color2}); color: #fff; }}
.cta h2 {{ font-size: 2rem; margin-bottom: 12px; }}
.cta p {{ opacity: 0.9; margin-bottom: 28px; }}
footer {{ text-align: center; padding: 32px 24px; background: #111; color: #888; font-size: 0.85rem; }}
{extra_css}
</style>
</head>
<body>
<div class="hero">
  <h1>{title}</h1>
  <p>{tagline}</p>
  <a href="#learn" class="btn btn-primary">Learn More</a>
</div>
{sections}
{extra_html}
<footer>&copy; 2025 {title}. All rights reserved.</footer>
</body>
</html>"""


businesses = [
    # (prompt, title, tagline, color1, color2, cards: [(icon, name, desc), ...], cta_text)
    ("Create a landing page for a spacecraft manufacturer",
     "Nova Aerospace", "Engineering the next generation of spacecraft for deep space exploration",
     "#0f0c29", "#302b63",
     [("🚀", "Launch Systems", "Reliable heavy-lift vehicles for orbital and interplanetary missions"),
      ("🛰️", "Satellite Platforms", "Modular satellite buses for communications and Earth observation"),
      ("🌍", "Mission Planning", "End-to-end mission design from concept through orbit insertion")],
     "Ready to reach the stars?"),

    ("Create a landing page for a semiconductor chip manufacturer",
     "SiliconForge", "Pushing the boundaries of chip fabrication at 2nm and beyond",
     "#1a1a2e", "#16213e",
     [("⚡", "2nm Process", "Industry-leading transistor density with unmatched power efficiency"),
      ("🔬", "R&D Labs", "12 research facilities driving next-generation lithography"),
      ("🏭", "Foundry Services", "High-volume production with 99.97% yield rates")],
     "Partner with the future of silicon"),

    ("Create a landing page for a cosmetic salon",
     "Lumière Beauty", "Where art meets science for your most radiant self",
     "#c94b4b", "#4b134f",
     [("💆", "Facial Treatments", "Custom facials using organic botanicals and advanced LED therapy"),
      ("💅", "Nail Artistry", "From classic manicures to avant-garde nail art designs"),
      ("✨", "Skin Analysis", "AI-powered skin diagnostics for personalized treatment plans")],
     "Book your transformation today"),

    ("Create a landing page for a defense contractor",
     "Sentinel Defense Systems", "Protecting nations with next-generation defense technology",
     "#1b1b2f", "#334155",
     [("🛡️", "Cybersecurity", "Advanced threat detection and zero-trust network architecture"),
      ("📡", "C4ISR Systems", "Command, control, and intelligence systems for modern warfare"),
      ("🎯", "Precision Systems", "Guided munitions and targeting platforms with surgical accuracy")],
     "Securing tomorrow's defense needs"),

    ("Create a landing page for a private school",
     "Westfield Academy", "Nurturing curious minds since 1952 — where every student thrives",
     "#2c3e50", "#3498db",
     [("📚", "Rigorous Academics", "College-prep curriculum with AP courses and small class sizes"),
      ("🎨", "Arts & Innovation", "Dedicated studios for visual arts, music, and digital media"),
      ("⚽", "Athletics", "25 varsity sports with state-of-the-art training facilities")],
     "Schedule a campus visit"),

    ("Create a landing page for a coffee roastery",
     "Ember Roasters", "Single-origin beans, small-batch roasted to perfection",
     "#3e2723", "#bf360c",
     [("☕", "Single Origin", "Direct-trade beans from Ethiopia, Colombia, and Guatemala"),
      ("🔥", "Small Batch", "Roasted in 15kg batches for peak freshness and flavor"),
      ("📦", "Subscription", "Fresh beans delivered to your door every two weeks")],
     "Start your coffee journey"),

    ("Create a landing page for a veterinary clinic",
     "PawCare Veterinary", "Compassionate care for every member of your family",
     "#1b5e20", "#4caf50",
     [("🐕", "Wellness Exams", "Comprehensive checkups with preventive care plans"),
      ("🏥", "Surgery Center", "Board-certified surgeons with advanced surgical suites"),
      ("💊", "In-House Pharmacy", "Convenient prescriptions filled during your visit")],
     "Book an appointment for your pet"),

    ("Create a landing page for a fintech startup",
     "PayFlow", "The payment infrastructure for the modern internet economy",
     "#0d1117", "#6e40c9",
     [("💳", "Payment Processing", "Accept payments in 135+ currencies with one integration"),
      ("🔒", "Fraud Detection", "ML-powered fraud prevention that adapts in real-time"),
      ("📊", "Analytics Dashboard", "Real-time transaction insights and revenue forecasting")],
     "Start processing payments today"),

    ("Create a landing page for an architecture firm",
     "Forma Studio", "Designing spaces that inspire, endure, and transform communities",
     "#37474f", "#607d8b",
     [("🏛️", "Commercial", "Office towers, retail spaces, and mixed-use developments"),
      ("🏠", "Residential", "Custom homes and luxury apartment complexes"),
      ("🌿", "Sustainable Design", "LEED-certified buildings with net-zero energy targets")],
     "Let's design your vision"),

    ("Create a landing page for a drone delivery company",
     "SkyDrop", "Autonomous drone delivery in under 30 minutes",
     "#006064", "#00bcd4",
     [("🚁", "Fast Delivery", "From warehouse to doorstep in under 30 minutes"),
      ("📱", "Real-Time Tracking", "Watch your delivery approach live on the app"),
      ("🌐", "Wide Coverage", "Serving 50+ metro areas with expanding rural routes")],
     "Get your first delivery free"),

    ("Create a landing page for a yoga studio",
     "Zenith Yoga", "Find your balance — body, mind, and spirit in harmony",
     "#4a148c", "#e040fb",
     [("🧘", "Classes", "Vinyasa, Hatha, Yin, and hot yoga for all levels"),
      ("🧠", "Meditation", "Guided sessions for stress relief and mental clarity"),
      ("👥", "Community", "Workshops, retreats, and teacher training programs")],
     "Try your first class free"),

    ("Create a landing page for a cybersecurity firm",
     "IronWall Security", "Enterprise-grade protection for an increasingly hostile digital world",
     "#1a1a2e", "#e53935",
     [("🔐", "Penetration Testing", "Red team exercises that expose vulnerabilities before attackers do"),
      ("🛡️", "SOC-as-a-Service", "24/7 monitoring with real-time threat response"),
      ("📋", "Compliance", "SOC 2, HIPAA, and PCI DSS readiness assessments")],
     "Get a free security assessment"),

    ("Create a landing page for a space tourism company",
     "Orbital Journeys", "Your ticket to the edge of space — the ultimate human experience",
     "#0a0a2a", "#1e88e5",
     [("🌌", "Suborbital Flights", "Experience weightlessness 100km above Earth"),
      ("🏨", "Space Hotel", "48-hour stay aboard our orbital station — launching 2027"),
      ("🎓", "Training Program", "Three-day astronaut preparation with veteran pilots")],
     "Reserve your seat among the stars"),

    ("Create a landing page for an organic farm",
     "Green Roots Farm", "Regenerative agriculture feeding communities with honest food",
     "#33691e", "#8bc34a",
     [("🌱", "Organic Certified", "USDA organic since 2008 with beyond-organic practices"),
      ("🥬", "CSA Boxes", "Weekly seasonal produce boxes delivered locally"),
      ("🐝", "Biodiversity", "200-acre pollinator habitat and heritage seed preservation")],
     "Join our community farm"),

    ("Create a landing page for a luxury watch brand",
     "Chronocraft", "Swiss precision. Timeless elegance. A legacy on your wrist.",
     "#1a1a1a", "#b8860b",
     [("⌚", "Masterpiece Collection", "Hand-assembled movements with 72-hour power reserve"),
      ("💎", "Limited Editions", "Numbered pieces with rare materials and complications"),
      ("🔧", "Lifetime Service", "Complimentary maintenance and restoration for every timepiece")],
     "Discover the collection"),

    ("Create a landing page for an electric vehicle startup",
     "Volterra Motors", "Electric performance vehicles that redefine the driving experience",
     "#0d47a1", "#42a5f5",
     [("⚡", "600mi Range", "Industry-leading battery technology for all-day driving"),
      ("🏎️", "0-60 in 2.8s", "Dual-motor AWD with instant torque delivery"),
      ("🔋", "Fast Charging", "10-80% in 18 minutes on our Superlink network")],
     "Reserve yours today"),

    ("Create a landing page for a music streaming platform",
     "SoundWave", "100 million tracks. Lossless audio. Your music, uncompromised.",
     "#1a1a2e", "#e91e63",
     [("🎵", "Lossless Audio", "Studio-quality streaming up to 24-bit/192kHz"),
      ("🤖", "AI Discovery", "Personalized recommendations that actually understand your taste"),
      ("🎧", "Spatial Audio", "Immersive 3D sound with Dolby Atmos support")],
     "Start listening free"),

    ("Create a landing page for a law firm",
     "Sterling & Associates", "Trusted counsel for complex legal challenges since 1987",
     "#1b2838", "#455a64",
     [("⚖️", "Corporate Law", "M&A, securities, and corporate governance for Fortune 500 clients"),
      ("🏛️", "Litigation", "Trial-tested attorneys with a 94% success rate"),
      ("📜", "IP Protection", "Patent prosecution and trademark enforcement worldwide")],
     "Schedule a consultation"),

    ("Create a landing page for a meal prep delivery service",
     "FreshBox", "Chef-prepared meals delivered. Healthy eating, zero effort.",
     "#e65100", "#ff9800",
     [("🍽️", "Chef-Crafted", "New menu every week by our team of executive chefs"),
      ("📊", "Macro-Balanced", "Every meal designed with precise nutritional targets"),
      ("♻️", "Eco Packaging", "100% compostable containers and carbon-neutral delivery")],
     "Get 50% off your first week"),

    ("Create a landing page for a cloud hosting provider",
     "NimbusCloud", "Infinitely scalable infrastructure. Zero downtime. Global edge.",
     "#0f172a", "#3b82f6",
     [("☁️", "Auto-Scaling", "Resources scale instantly with demand — pay only for what you use"),
      ("🌐", "42 Regions", "Edge servers on every continent for sub-20ms latency"),
      ("🔒", "SOC 2 Certified", "Enterprise security with encryption at rest and in transit")],
     "Deploy in 30 seconds"),

    ("Create a landing page for a dental practice",
     "BrightSmile Dental", "Modern dentistry. Gentle care. Smiles that last a lifetime.",
     "#00695c", "#26a69a",
     [("🦷", "General Dentistry", "Cleanings, fillings, and preventive care for all ages"),
      ("✨", "Cosmetic", "Veneers, whitening, and Invisalign for your perfect smile"),
      ("🏥", "Implants", "Titanium implant placement with same-day provisional crowns")],
     "Book your visit today"),

    ("Create a landing page for a pet grooming service",
     "Pampered Paws", "Premium grooming that keeps tails wagging and coats gleaming",
     "#6a1b9a", "#ab47bc",
     [("🐩", "Full Grooming", "Bath, haircut, nail trim, and ear cleaning"),
      ("🧴", "Organic Products", "Hypoallergenic shampoos and conditioners for sensitive skin"),
      ("🚗", "Mobile Service", "We come to you — fully equipped grooming van at your door")],
     "Book a grooming session"),

    ("Create a landing page for a language learning app",
     "Polyglot", "Learn any language through conversation — not memorization",
     "#311b92", "#7c4dff",
     [("🗣️", "AI Conversations", "Practice with AI tutors that adapt to your level in real-time"),
      ("🌍", "40+ Languages", "From Spanish and Mandarin to Icelandic and Swahili"),
      ("📈", "Smart Progress", "Spaced repetition and fluency tracking that actually works")],
     "Start learning for free"),

    ("Create a landing page for a wedding photography studio",
     "Golden Hour Studios", "Capturing love stories — one frame at a time",
     "#880e4f", "#f48fb1",
     [("📸", "Full Coverage", "12-hour coverage with two photographers and drone footage"),
      ("🎞️", "Cinematic Films", "4K wedding films edited with a documentary storytelling approach"),
      ("📱", "Online Gallery", "Private gallery delivered within 4 weeks, shareable with guests")],
     "Check our availability"),

    ("Create a landing page for a moving company",
     "SwiftMove", "Stress-free moving. On time. Every time.",
     "#e65100", "#ff6d00",
     [("🚛", "Local & Long Distance", "Licensed movers for residential and commercial moves nationwide"),
      ("📦", "Packing Services", "Professional packing with premium materials and insurance"),
      ("📋", "Free Estimates", "Transparent pricing with no hidden fees — guaranteed")],
     "Get a free quote"),

    ("Create a landing page for a meditation app",
     "Stillness", "Five minutes of calm can change your entire day",
     "#1a237e", "#5c6bc0",
     [("🧘", "Guided Sessions", "500+ meditations for sleep, focus, stress, and anxiety"),
      ("🌙", "Sleep Stories", "Soothing narrations that gently guide you to deep sleep"),
      ("📊", "Mindfulness Tracking", "Track streaks, mood patterns, and meditation minutes")],
     "Try 7 days free"),

    ("Create a landing page for a surf school",
     "Pacific Wave Academy", "Ride your first wave today — lessons for all ages and levels",
     "#01579b", "#29b6f6",
     [("🏄", "Beginner Lessons", "Two-hour sessions with certified instructors and all gear included"),
      ("🌊", "Surf Camps", "Week-long immersive camps with video analysis and ocean safety"),
      ("🛒", "Gear Shop", "Premium boards, wetsuits, and accessories from top brands")],
     "Catch your first wave"),

    ("Create a landing page for an AI research lab",
     "DeepMind Dynamics", "Advancing artificial intelligence for the benefit of humanity",
     "#0d1117", "#00e676",
     [("🧠", "Foundation Models", "Training frontier models with novel architectures"),
      ("🔬", "Safety Research", "Alignment, interpretability, and robustness at scale"),
      ("📄", "Open Science", "200+ published papers and open-source tools for the community")],
     "View our research"),

    ("Create a landing page for a brewery",
     "Iron Kettle Brewing", "Craft beer brewed with obsession, served with pride",
     "#4e342e", "#ff8f00",
     [("🍺", "Core Lineup", "Six flagship beers from crisp pilsner to bold imperial stout"),
      ("🧪", "Experimental Series", "Monthly limited releases pushing the boundaries of flavor"),
      ("🏠", "Taproom", "Open 7 days — live music, food trucks, and 20 taps")],
     "Visit the taproom"),

    ("Create a landing page for a private jet charter service",
     "AeroElite", "Fly on your schedule. Land where others can't.",
     "#0a0a0a", "#c9b037",
     [("✈️", "Global Fleet", "200+ aircraft from light jets to ultra-long-range heavy jets"),
      ("🕐", "2-Hour Notice", "Wheels up within two hours from any major airport"),
      ("👤", "Concierge", "Dedicated flight coordinator handling every detail door-to-door")],
     "Request a charter quote"),

    ("Create a landing page for a rock climbing gym",
     "Summit Wall", "Push your limits. Climb higher. Build strength from within.",
     "#263238", "#ff7043",
     [("🧗", "40ft Walls", "Lead, top-rope, and bouldering across 15,000 sq ft"),
      ("💪", "Training Center", "Campus boards, hangboards, and strength training area"),
      ("👥", "Youth Programs", "After-school climbing clubs and competitive team training")],
     "Try a day pass"),

    ("Create a landing page for a botanical garden",
     "Eden Gardens", "30 acres of living art — a sanctuary for plants and people",
     "#1b5e20", "#66bb6a",
     [("🌺", "Tropical House", "2,000 species from rainforests around the world"),
      ("🦋", "Butterfly Pavilion", "Walk among hundreds of free-flying butterflies year-round"),
      ("🎓", "Education", "Field trips, workshops, and master gardener certification")],
     "Plan your visit"),

    ("Create a landing page for a 3D printing company",
     "LayerForge", "Industrial 3D printing. From prototype to production in days.",
     "#1a1a2e", "#00bfa5",
     [("🖨️", "Multi-Material", "Metal, polymer, ceramic, and composite printing capabilities"),
      ("⚡", "Rapid Turnaround", "Prototypes in 24 hours, production runs in under a week"),
      ("🔧", "DFM Support", "Design-for-manufacturing review included with every order")],
     "Upload your design"),

    ("Create a landing page for a wine vineyard",
     "Crestview Vineyards", "Estate wines from sun-drenched hillsides — since 1978",
     "#4a0e0e", "#c62828",
     [("🍷", "Estate Wines", "Pinot Noir, Chardonnay, and Cabernet from our own 120 acres"),
      ("🏡", "Tasting Room", "Guided tastings with views of the valley, open daily"),
      ("🎉", "Private Events", "Weddings, corporate retreats, and harvest celebrations")],
     "Book a tasting"),

    ("Create a landing page for a video game studio",
     "Obsidian Forge Games", "Crafting worlds you'll never want to leave",
     "#0a0a1a", "#9c27b0",
     [("🎮", "AAA Titles", "Open-world RPGs with deep narrative and player choice"),
      ("🌐", "Online Worlds", "Persistent MMO experiences with millions of active players"),
      ("🛠️", "Modding Tools", "Full mod SDK — our community is our greatest asset")],
     "See our latest game"),

    ("Create a landing page for a solar energy installer",
     "SunGrid Energy", "Power your home with clean, affordable solar energy",
     "#e65100", "#ffca28",
     [("☀️", "Custom Design", "Satellite-mapped system design optimized for your roof"),
      ("💰", "30% Tax Credit", "Federal ITC plus state incentives — we handle all paperwork"),
      ("🔋", "Battery Storage", "Tesla Powerwall integration for 24/7 energy independence")],
     "Get a free solar quote"),

    ("Create a landing page for a ski resort",
     "Powder Peak Resort", "4,200 acres of legendary terrain. The mountain is calling.",
     "#1a237e", "#e3f2fd",
     [("⛷️", "128 Trails", "Beginner to expert terrain with 3,200ft vertical drop"),
      ("🏔️", "Summit Lodge", "Ski-in ski-out luxury with heated pools and spa"),
      ("🎿", "Ski School", "World-class instructors for kids and adults at every level")],
     "Book your ski trip"),

    ("Create a landing page for a personal trainer platform",
     "FitForge", "Expert personal training — anywhere, anytime, on your terms",
     "#1b1b1b", "#f44336",
     [("💪", "1-on-1 Coaching", "Matched with certified trainers specializing in your goals"),
      ("📱", "Live Sessions", "HD video training from your home gym or hotel room"),
      ("📊", "Progress Tracking", "AI body composition analysis and strength benchmarks")],
     "Start your free trial"),

    ("Create a landing page for an escape room venue",
     "Enigma Rooms", "Can you solve it before time runs out? 60 minutes. No hints. Pure thrill.",
     "#1a1a2e", "#ff6f00",
     [("🔑", "6 Themed Rooms", "From haunted mansion to space station — difficulty 1-5 stars"),
      ("👥", "Team Building", "Corporate packages for 10-100 people with catered options"),
      ("🏆", "Leaderboards", "Compete for the fastest escape time — updated live")],
     "Book your escape"),

    ("Create a landing page for a book publisher",
     "Meridian Press", "Stories that matter. Voices that endure.",
     "#3e2723", "#795548",
     [("📖", "Literary Fiction", "Award-winning authors pushing the boundaries of narrative"),
      ("🌍", "Translations", "Bringing international voices to English-speaking readers"),
      ("✍️", "New Authors", "Open submissions — we read every manuscript, guaranteed")],
     "Browse our catalog"),

    ("Create a landing page for a co-working space",
     "The Hive", "Where ambitious people build the future — together",
     "#212121", "#ffd600",
     [("🏢", "Flexible Desks", "Hot desks, dedicated desks, and private offices month-to-month"),
      ("🚀", "Startup Perks", "AWS credits, legal hours, and investor introductions"),
      ("☕", "Full Amenities", "Barista coffee, podcast studios, rooftop, and 24/7 access")],
     "Tour the space"),

    ("Create a landing page for a marine biology research center",
     "Oceanus Institute", "Understanding the ocean to protect our planet's future",
     "#01579b", "#0097a7",
     [("🐋", "Marine Research", "Tracking migration patterns and ecosystem health across five oceans"),
      ("🌊", "Conservation", "Coral reef restoration and marine protected area advocacy"),
      ("🎓", "Education", "PhD programs, summer fellowships, and public ocean literacy")],
     "Support ocean science"),

    ("Create a landing page for a tattoo studio",
     "Black Ink Collective", "Custom tattoo artistry — your story, permanently told",
     "#1a1a1a", "#616161",
     [("🎨", "Custom Design", "One-on-one consultations to create your unique piece"),
      ("🖋️", "Styles", "Realism, Japanese, geometric, blackwork, and watercolor"),
      ("🏅", "Award-Winning", "Artists with 10+ years and international convention awards")],
     "Book a consultation"),

    ("Create a landing page for a children's museum",
     "Wonderlab Museum", "Where play meets learning — 40,000 sq ft of pure imagination",
     "#f57f17", "#ffee58",
     [("🔬", "Science Zone", "Hands-on experiments with electricity, magnets, and chemistry"),
      ("🎭", "Imagination Studio", "Costumes, puppets, and a full stage for creative play"),
      ("🌊", "Water World", "Interactive water tables, dam building, and flow experiments")],
     "Plan your family visit"),

    ("Create a landing page for a luxury hotel",
     "The Meridian Hotel", "Five-star hospitality where every detail is unforgettable",
     "#1a1a1a", "#d4a574",
     [("🛏️", "Suites", "180 rooms with panoramic city views and Italian marble baths"),
      ("🍽️", "Fine Dining", "Two Michelin-starred restaurant with a 3,000-bottle cellar"),
      ("🧖", "Wellness Spa", "Rooftop infinity pool, thermal baths, and 24-hour fitness")],
     "Reserve your stay"),

    ("Create a landing page for a robotics company",
     "Atlas Robotics", "Intelligent machines that work alongside humans",
     "#0d1117", "#76ff03",
     [("🤖", "Warehouse Robots", "Autonomous picking and packing at 3x human speed"),
      ("🦾", "Collaborative Arms", "Safe, precise robotic arms for manufacturing lines"),
      ("🧠", "AI Vision", "3D perception and object recognition for unstructured environments")],
     "See a live demo"),

    ("Create a landing page for a perfume house",
     "Maison Éclat", "Fragrances composed like symphonies — complex, emotional, unforgettable",
     "#4a148c", "#ce93d8",
     [("🌹", "Signature Line", "12 eau de parfums crafted with rare natural ingredients"),
      ("🧪", "Bespoke Service", "Create your own fragrance with our master perfumer"),
      ("🎁", "Discovery Set", "Five 10ml samples to find your signature scent")],
     "Explore the collection"),

    ("Create a landing page for a mountain biking park",
     "Ridgeline Bike Park", "50 miles of purpose-built trails. Gravity is your engine.",
     "#33691e", "#ff6e40",
     [("🚵", "Trail Network", "50 miles of flow trails, jump lines, and technical descents"),
      ("🎫", "Season Pass", "Unlimited riding plus 20% off gear and rentals"),
      ("🔧", "Pro Shop", "Full-service bike repairs, demos, and expert fitting")],
     "Get your pass"),

    ("Create a landing page for a podcast hosting platform",
     "EchoCast", "Launch, grow, and monetize your podcast — all in one place",
     "#1a1a2e", "#ff4081",
     [("🎙️", "Easy Publishing", "Record, edit, and distribute to Spotify, Apple, and 20+ platforms"),
      ("📈", "Advanced Analytics", "Listener demographics, retention curves, and episode benchmarks"),
      ("💰", "Monetization", "Dynamic ad insertion and premium subscriber support built-in")],
     "Start your podcast free"),
]

def make_sections(cards, cta_text):
    cards_html = "\n".join([
        f'    <div class="card"><div class="icon">{icon}</div><h3>{name}</h3><p>{desc}</p></div>'
        for icon, name, desc in cards
    ])
    return f"""
<div class="section" id="learn">
  <h2>What We Offer</h2>
  <p class="subtitle">Built with precision, delivered with passion</p>
  <div class="grid">
{cards_html}
  </div>
</div>

<div class="cta">
  <h2>{cta_text}</h2>
  <p>Join thousands who already trust us</p>
  <a href="#" class="btn btn-primary">Get Started</a>
</div>"""


# Generate JSONL
train_items = []
test_items = []

for i, (prompt, title, tagline, c1, c2, cards, cta) in enumerate(businesses):
    sections = make_sections(cards, cta)
    html = page(title, tagline, c1, c2, sections)
    item = {"messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": html}
    ]}
    if i >= 45:  # last 5 = test
        test_items.append(item)
    else:
        train_items.append(item)

# Split train into train + valid
valid_items = train_items[40:]
train_items = train_items[:40]

for name, items in [("train", train_items), ("valid", valid_items), ("test", test_items)]:
    with open(f"data/{name}.jsonl", "w") as f:
        for item in items:
            f.write(json.dumps(item) + "\n")
    print(f"{name}: {len(items)} examples")

# Also save test HTML files for preview
import os
os.makedirs("results/pages", exist_ok=True)
for item in test_items:
    prompt = item["messages"][0]["content"]
    html = item["messages"][1]["content"]
    # extract a slug from the prompt
    slug = prompt.split("for ")[-1].strip().lower().replace(" ", "-")[:30]
    with open(f"results/pages/expected-{slug}.html", "w") as f:
        f.write(html)
    print(f"Saved expected page: {slug}")

print("\nDone! Data ready for training.")
