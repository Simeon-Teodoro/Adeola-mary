#!/usr/bin/env python3
"""Generates the five static pages of Mary's site from shared parts.
Run:  python3 _build/build.py   (from the project root)
Edit CONFIG below to change contact details, then re-run."""
import html, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

CONFIG = {
    "name": "Adeola Mary",
    "email": "adeolamary703@gmail.com",
    "upwork": "https://www.upwork.com/freelancers/~01d9eeecc5e9f0b713",
    "linkedin": "https://www.linkedin.com/in/adeola-mary-275b38332/",
    "location": "Lagos, Nigeria",
    "hours": "Mon–Sat · GMT+1, overlaps US & UK hours",
}

# ---------------------------------------------------------------- icons
def svg(body, vb="0 0 24 24", sw="1.6"):
    return ('<svg class="icon" viewBox="%s" fill="none" stroke="currentColor" stroke-width="%s" '
            'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">%s</svg>' % (vb, sw, body))

I = {
 "arrow": svg('<path d="M7 17 17 7M8 7h9v9"/>', sw="2"),
 "right": svg('<path d="M5 12h14M13 6l6 6-6 6"/>', sw="2"),
 "left": svg('<path d="M19 12H5M11 6l-6 6 6 6"/>', sw="2"),
 "up": svg('<path d="M12 19V5M6 11l6-6 6 6"/>', sw="2"),
 "mail": svg('<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3 7 9 6 9-6"/>'),
 "calendar": svg('<rect x="3" y="4" width="18" height="17" rx="2"/><path d="M8 2v4M16 2v4M3 10h18M8 14h2M14 14h2M8 17h2"/>'),
 "social": svg('<rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r=".8" fill="currentColor"/>'),
 "chart": svg('<path d="M3 3v18h18"/><path d="m7 15 4-4 3 3 5-6"/><path d="M15 8h4v4"/>'),
 "users": svg('<circle cx="9" cy="8" r="3.5"/><path d="M2.5 20a6.5 6.5 0 0 1 13 0"/><path d="M16 4.5a3.5 3.5 0 0 1 0 7M18 14a6 6 0 0 1 3.5 6"/>'),
 "search": svg('<circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/>'),
 "layers": svg('<path d="m12 3 9 5-9 5-9-5 9-5Z"/><path d="m3 13 9 5 9-5"/>'),
 "home": svg('<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-6h4v6"/>'),
 "heart": svg('<path d="M20.8 8.6a5 5 0 0 0-8.8-3.2 5 5 0 0 0-8.8 3.2c0 5.4 8.8 11 8.8 11s8.8-5.6 8.8-11Z"/><path d="M3.5 12h4l2-3 3 6 2-3h6"/>'),
 "cart": svg('<circle cx="9" cy="20" r="1.4"/><circle cx="18" cy="20" r="1.4"/><path d="M2 3h3l2.6 12.4a2 2 0 0 0 2 1.6h8.2a2 2 0 0 0 2-1.5L22 8H6"/>'),
 "pen": svg('<path d="M12 20h9"/><path d="M16.5 3.5a2.1 2.1 0 0 1 3 3L7 19l-4 1 1-4Z"/>'),
 "file": svg('<path d="M14 3H6a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V9Z"/><path d="M14 3v6h6M8 13h8M8 17h6"/>'),
 "plane": svg('<path d="M17.8 19.2 16 11l3.5-3.5C21 6 21.5 4 21 3c-1-.5-3 0-4.5 1.5L13 8 4.8 6.2c-.5-.1-.9.1-1.1.5l-.3.5c-.2.5-.1 1 .3 1.3L9 12l-2 3H4l-1 1 3 2 2 3 1-1v-3l3-2 3.5 5.3c.3.4.8.5 1.3.3l.5-.2c.4-.3.6-.7.5-1.2Z"/>'),
 "bolt": svg('<path d="M13 2 4 14h7l-1 8 9-12h-7Z"/>'),
 "megaphone": svg('<path d="m3 11 15-6v14L3 13Z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/><path d="M21 9v6"/>'),
 "clock": svg('<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>'),
 "check": svg('<path d="m5 12 4.5 4.5L19 7"/>', sw="2.2"),
 "star": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="m12 2.5 2.9 6.1 6.6.8-4.9 4.6 1.3 6.6L12 17.3l-5.9 3.3 1.3-6.6-4.9-4.6 6.6-.8Z"/></svg>',
 "pin": svg('<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/>'),
 "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5ZM3 9.5h4V21H3Zm7 0h3.8v1.6h.06c.53-1 1.83-2 3.77-2 4.03 0 4.77 2.65 4.77 6.1V21h-4v-5.1c0-1.22-.02-2.8-1.7-2.8-1.71 0-1.97 1.33-1.97 2.7V21h-4Z"/></svg>',
 "upwork": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M18.56 13.73c-1.04 0-2.02-.44-2.9-1.16l.21-1.01.01-.04c.19-1.07.8-2.87 2.68-2.87a2.54 2.54 0 0 1 0 5.08Zm0-7.64c-2.4 0-4.27 1.56-5.02 4.13-1.15-1.73-2.02-3.8-2.53-5.55H8.43v6.7a2.35 2.35 0 1 1-4.7 0v-6.7H1.15v6.7a4.93 4.93 0 0 0 9.86 0v-1.12c.47.98 1.05 1.97 1.75 2.86l-1.49 7.02h2.64l1.08-5.1c.95.6 2.04.99 3.3.99a5.1 5.1 0 0 0 0-10.2Z"/></svg>',
 "quote": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4 18h6v-6H6.5c0-2.2 1.3-3.6 3.5-4V5c-4 .5-6 3.3-6 7.5Zm10 0h6v-6h-3.5c0-2.2 1.3-3.6 3.5-4V5c-4 .5-6 3.3-6 7.5Z"/></svg>',
 "copy": svg('<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15V5a2 2 0 0 1 2-2h10"/>'),
 "send": svg('<path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>'),
 "grid": svg('<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/><rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>'),
}

def esc(s): return html.escape(s, quote=True)

def btn(label, href, cls="", ext=False, sm=False):
    attrs = ' target="_blank" rel="noopener"' if ext else ""
    return ('<a class="btn %s%s" href="%s"%s><span>%s</span><span class="btn__icon">%s</span></a>'
            % ("btn--sm " if sm else "", cls, href, attrs, label, I["arrow"]))

def eyebrow(t): return '<span class="eyebrow">%s</span>' % t

def ring_badge(text, core, cid):
    return ('<div class="badge-rotate"><svg class="ring-text" viewBox="0 0 140 140" aria-hidden="true">'
            '<defs><path id="%s" d="M70,70 m-54,0 a54,54 0 1,1 108,0 a54,54 0 1,1 -108,0"/></defs>'
            '<text><textPath href="#%s" textLength="336" lengthAdjust="spacing">%s</textPath></text></svg>'
            '<div class="badge-rotate__core">%s</div></div>' % (cid, cid, text, core))

NAV = [("index.html", "Home"), ("about.html", "About"), ("services.html", "Services"),
       ("portfolio.html", "Portfolio"), ("contact.html", "Contact")]

# ---------------------------------------------------------------- data
SERVICES = [
 ("calendar", "Executive Virtual Assistance", "Inbox triage, calendar and meeting scheduling, follow-ups and SOPs, so your week runs without you chasing it.", ""),
 ("social", "Social Media Management", "Content calendars, posts and Reels, captions, scheduling, community replies and monthly reports across IG, TikTok, FB, LinkedIn and YouTube.", ""),
 ("mail", "Inbox & Email Management", "Inbox Zero systems, filters and labels, drafted replies and email deliverability fixes so important messages never slip.", ""),
 ("users", "CRM & GoHighLevel Support", "Lead tracking, pipeline updates, contact clean-up and automations in HubSpot and GoHighLevel.", ""),
 ("search", "Online & Market Research", "Market research, lead lists and data collection organised in clean Google Sheets you can act on.", ""),
 ("pen", "Canva Graphics & Content", "On-brand flyers, carousels and social graphics designed in Canva to match your voice.", ""),
]

PROJECTS = [
 # title, category key, category label, role, description, skills, gradient, icon
 ("Social Media Launch for a Mobile App", "social", "Social Media", "Social Media Manager",
  "Ran social media for an app launch: built the content calendar, wrote captions, scheduled posts and Reels, replied to the community and reported on reach each week.",
  ["Social Media Marketing", "Content Calendar", "Instagram", "TikTok"], "g1", "social"),
 ("CRM & Lead Management for a Real Estate Agency", "realestate", "Real Estate", "Virtual Assistant · CRM & Admin Support",
  "Managed and optimised the agency's CRM by entering and updating client and property data, tracked lead generation, answered property inquiries, scheduled viewings and kept email follow-ups on time.",
  ["CRM", "Lead Generation", "Email Management", "Administrative Support"], "g2", "home"),
 ("Executive Calendar & Inbox Management", "executive", "Executive VA", "Executive Assistant",
  "Handled high-volume email by filtering priority messages, drafting replies and following up. Kept the executive's calendar conflict-free while coordinating with internal and external stakeholders.",
  ["Calendar Management", "Email Management", "Appointment Scheduling"], "g3", "calendar"),
 ("Flyer Design for an Executive Brand", "social", "Social Media", "Executive VA · Canva Design",
  "Designed a clean, professional flyer that captured the client's brand. The client called it perfect for executive-level design work.",
  ["Canva", "Graphic Design", "Branding"], "g4", "pen"),
 ("Healthcare Admin & Patient Support", "healthcare", "Healthcare", "Remote Admin Assistant",
  "Supported a clinic by answering patient inquiries, managing incoming email, organising patient records and forwarding urgent requests to the right staff.",
  ["Customer Support", "Data Entry", "Email Management"], "g2", "heart"),
 ("Executive VA for a Social Media Agency Founder", "executive", "Executive VA", "Executive Virtual Assistant",
  "Improved daily operations for an agency founder by managing schedules, coordinating meetings, handling email and organising Google Docs and file structures for the social media team.",
  ["Google Workspace", "Project Coordination", "CRM"], "g1", "users"),
 ("Property Management Virtual Assistant", "realestate", "Real Estate", "Property Management VA",
  "Managed tenant inquiries, scheduled inspections, tracked maintenance requests, updated lease data in the CRM and coordinated vendors for repair follow-ups.",
  ["Property Management", "CRM", "Spreadsheets"], "g4", "home"),
 ("Executive Travel Planning", "executive", "Executive VA", "Travel & Event Coordinator",
  "Coordinated business and personal travel for executives by comparing flights, booking accommodation and building day-by-day itineraries. Built a Business Vacation Planner workbook with a trip overview, budget tracker, planning checklist, attendee list, itinerary, bookings and packing tabs.",
  ["Travel Planning", "Excel / Google Sheets", "Budget Tracking", "Scheduling"], "g3", "plane"),
 ("Socioflow: AI for Social Media Management", "social", "Social Media", "Social Media Manager",
  "A demo project using AI tools to speed up content planning, scheduling and basic marketing strategy for social media workflows.",
  ["AI Tools", "Content Planning", "Scheduling"], "g2", "bolt"),
 ("Shopify Product Listings", "admin", "Admin & Ops", "Shopify Product Listing Assistant",
  "Uploaded and optimised Shopify product listings with titles, descriptions, variants and images, keeping catalogue data accurate across the store.",
  ["Shopify", "Data Entry", "E-commerce"], "g1", "cart"),
 ("Home Services Booking Support", "admin", "Admin & Ops", "Virtual Assistant",
  "Answered customer emails, booked service appointments and kept client and job records organised for cleaning, HVAC, plumbing and roofing businesses.",
  ["Appointment Scheduling", "Customer Service", "Record Keeping"], "g3", "clock"),
 ("Medisphere: Virtual Medical Platform", "healthcare", "Healthcare", "Virtual Assistant",
  "Supported an online medical platform that connects patients with healthcare professionals by handling operations, communication and record keeping.",
  ["Virtual Assistance", "Healthcare Admin", "Communication"], "g4", "heart"),
]

REVIEWS = [
 ("Working with Adeola as an Executive Virtual Assistant was a smooth and productive experience. Adeola handled tasks efficiently with strong attention to detail, demonstrating excellent organizational skills in managing Google Docs and file structures to keep everything accessible for the social media manager.",
  "Verified Upwork client · 5.0", "Executive VA for a Social Media Manager"),
 ("Great Executive Virtual Assistant! Professional, organized and detail oriented. She completed the task accurately, communicated well, and delivered on time. I would happily work with them again.",
  "Verified Upwork client · 5.0", "Virtual assistant for administrative support"),
 ("Adeola my Executive virtual assistant delivered a clean, professional flyer that perfectly captured our brand. Highly recommend for any executive level design work.",
  "Verified Upwork client · 5.0", "Executive VA for flyer design"),
]

FAQ = [
 ("What tasks can you take off my plate?", "Inbox and calendar management, meeting and appointment scheduling, CRM updates, online research, data entry, SOP writing, travel planning, and social media from planning to monthly reports."),
 ("Which tools do you work with?", "Google Workspace, Microsoft Outlook, Canva, HubSpot, GoHighLevel, Notion, Trello, Calendly, Zoom, Shopify, WordPress, Meta Business Suite and most scheduling tools. If you use something else, I learn it quickly."),
 ("How do we get started?", "Send a message with what is taking too much of your time. We hop on a short call, agree on priorities and how you like to communicate, and I usually start within 48 hours."),
 ("Do you work in my time zone?", "I'm based in Lagos (GMT+1) and keep working hours that overlap with the UK, Europe and US East Coast. Urgent items are handled the same day."),
 ("How is pricing structured?", "Every business is different, so I quote based on your tasks and hours. You can hire me for a one-off project, a monthly package or an ongoing retainer, directly or through Upwork."),
 ("Is my information kept confidential?", "Yes. I treat client inboxes, files and passwords with strict confidentiality, use password managers for access, and am happy to sign an NDA."),
]

TOOLS = ["Google Workspace", "Canva", "HubSpot", "GoHighLevel", "Notion", "Calendly", "Shopify", "Meta Business Suite", "Trello", "WordPress", "Zoom", "Slack"]

# ---------------------------------------------------------------- shared parts
def head(title, desc):
    return ('<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n'
            '<title>%s</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n<meta name="description" content="%s">\n'
            '<meta name="theme-color" content="#0d0918">\n'
            '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
            '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,400;9..40,500;9..40,600;9..40,700&family=Sora:wght@300;400;600;700;800&display=swap">\n'
            '<link rel="stylesheet" href="assets/css/style.css">\n' % (esc(title), esc(desc)))

def header(active):
    nav = "".join('<a href="%s"%s>%s</a>' % (h, ' aria-current="page"' if h == active else "", t) for h, t in NAV)
    oc = "".join('<a href="%s"%s>%s %s</a>' % (h, ' aria-current="page"' if h == active else "", t, I["arrow"]) for h, t in NAV)
    return """
<a class="skip" href="#main">Skip to content</a>
<div class="preloader" aria-hidden="true"><div class="preloader__inner"><div class="preloader__dot"></div><div class="preloader__text">Loading…</div><div class="preloader__bar"><span></span></div></div></div>
<header class="header"><div class="wrap header__row">
  <a class="logo" href="index.html" aria-label="Adeola Mary home"><span class="logo__mark">AM</span><span>adeola<b>.</b>mary</span></a>
  <nav class="nav" aria-label="Main">%s</nav>
  <div class="header__actions">%s<button class="burger" type="button" data-open-menu aria-label="Open menu"><span></span></button></div>
</div></header>
<div class="offcanvas" aria-hidden="true">
  <div class="offcanvas__shade" data-close-menu></div>
  <aside class="offcanvas__panel" role="dialog" aria-modal="true" aria-label="Menu">
    <div class="offcanvas__top"><a class="logo" href="index.html"><span class="logo__mark">AM</span><span>adeola<b>.</b>mary</span></a><button class="offcanvas__close" type="button" data-close-menu aria-label="Close menu">✕</button></div>
    <nav class="offcanvas__nav" aria-label="Mobile">%s</nav>
    <div class="offcanvas__info">
      <p>Executive Virtual Assistant and Social Media Manager helping founders stay organised and visible.</p>
      <div><strong>Email</strong>%s</div>
      <div><strong>Based in</strong>%s · %s</div>
    </div>
    %s
  </aside>
</div>
<div class="switcher" role="group" aria-label="Choose accent colour"><span class="switcher__label">Colour</span>
  <button type="button" data-accent="purple" style="background:#6d28d9" aria-label="Purple"></button>
  <button type="button" data-accent="lavender" style="background:#c4a8ff" aria-label="Lavender"></button>
  <button type="button" data-accent="royal" style="background:#4338ca" aria-label="Royal blue-purple"></button>
  <button type="button" data-accent="magenta" style="background:#c026d3" aria-label="Magenta"></button>
  <button type="button" data-accent="white" style="background:#ffffff;box-shadow:inset 0 0 0 1px #c9c2d8" aria-label="White"></button>
</div>
""" % (nav, btn("Let's Talk", "contact.html", sm=True), oc, esc(CONFIG["email"]), CONFIG["location"], CONFIG["hours"].split(" ·")[0],
       btn("Hire me on Upwork", CONFIG["upwork"], ext=True))

def footer():
    links = "".join('<li><a href="%s">%s</a></li>' % (h, t) for h, t in NAV)
    svc = "".join('<li><a href="services.html">%s</a></li>' % s[1] for s in SERVICES[:5])
    return """
<footer class="footer">
  <div class="footer__glow"></div>
  <div class="wrap">
    <div class="footer__top">
      <div class="footer__cta reveal"><h2>Let's Talk<br><span class="accent">Work Together</span></h2></div>
      <div class="footer__contact reveal" style="--d:.1s">
        <span class="muted">Ready when you are</span>
        <a href="contact.html">%s</a>
        <a href="%s" target="_blank" rel="noopener">Hire on Upwork ↗</a>
      </div>
    </div>
    <div class="footer__mid">
      <div>
        <a class="logo" href="index.html"><span class="logo__mark">AM</span><span>adeola<b>.</b>mary</span></a>
        <p class="muted" style="margin-top:16px;max-width:36ch">Leave your email and I'll reach out to book a free 15-minute discovery call.</p>
        <form class="news" data-go="contact.html" novalidate><label class="sr-only" for="news-email">Your email</label><input id="news-email" type="email" placeholder="Enter your email" autocomplete="email"><button type="submit" aria-label="Request a call">%s</button></form>
        <div class="socials"><a href="%s" target="_blank" rel="noopener" aria-label="LinkedIn">%s</a><a href="%s" target="_blank" rel="noopener" aria-label="Upwork">%s</a><a href="contact.html" aria-label="Email">%s</a></div>
      </div>
      <div><h4>Quick links</h4><ul>%s</ul></div>
      <div><h4>Services</h4><ul>%s</ul></div>
      <div><h4>Contact</h4><ul><li>%s</li><li>%s</li><li>%s</li></ul></div>
    </div>
  </div>
  <div class="footer__big" aria-hidden="true">ADEOLA MARY</div>
  <div class="wrap"><div class="footer__bottom"><span>© <span id="yr">2026</span> Adeola Mary. All rights reserved.</span><span>Executive VA · Social Media Manager</span></div></div>
</footer>
<button class="to-top" type="button" aria-label="Back to top"><svg class="ring" viewBox="0 0 52 52" aria-hidden="true"><circle class="track" cx="26" cy="26" r="24"/><circle class="bar" cx="26" cy="26" r="24"/></svg>%s</button>
<script src="assets/js/main.js"></script>
<script>document.getElementById("yr").textContent=new Date().getFullYear();</script>
""" % (esc(CONFIG["email"]), CONFIG["upwork"], I["send"], CONFIG["linkedin"], I["linkedin"], CONFIG["upwork"], I["upwork"], I["mail"],
       links, svc, esc(CONFIG["email"]), CONFIG["location"], CONFIG["hours"], I["up"])

def page_hero(title_html, crumb, lead):
    return """
<section class="page-hero"><div class="hero__glow"></div><div class="rings" aria-hidden="true"><span></span><span></span><span></span></div>
  <div class="wrap page-hero__inner">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><i>/</i><span aria-current="page">%s</span></nav>
    <h1 class="h-xl" data-split>%s</h1>
    <p class="lead reveal">%s</p>
  </div>
</section>""" % (crumb, title_html, lead)

NEW_PROJECTS = [
 ("Instagram Content for a Rochester Realtor", "social", "Social Media", "Social Media Manager",
  "Managed Instagram content for a Rochester, NY realtor, including a \u201cThanksgiving Made Easy\u201d local guide, listing highlights and community posts in the realtor's signature pink brand style.",
  ["Instagram", "Canva", "Content Calendar", "Real Estate Marketing"], "g1", "social"),
 ("Featured Property Listings for a Luxury Brokerage", "realestate", "Real Estate", "Real Estate VA \u00b7 Listing Management",
  "Uploaded and maintained featured property listings for a luxury brokerage in Scottsdale, Arizona, keeping photos, addresses, sale and lease tags and property details accurate across the website.",
  ["Listing Management", "Website Updates", "Real Estate VA"], "g2", "home"),
 ("Property Search & Listing Updates for a Realtor", "realestate", "Real Estate", "Real Estate Virtual Assistant",
  "Kept a Rochester, NY realtor's property search up to date by checking prices, Active and Pending status changes and property details, so buyers always saw current homes.",
  ["MLS Listings", "Data Accuracy", "Real Estate VA"], "g4", "home"),
]
PROJECTS = PROJECTS[:4] + NEW_PROJECTS + [p for p in PROJECTS[4:] if p[0] == "Executive Travel Planning"] + [p for p in PROJECTS[4:] if p[0] != "Executive Travel Planning"]

SHOTS = {
 "Social Media Launch for a Mobile App": [("work-app-launch.webp", 779, 2000)],
 "CRM & Lead Management for a Real Estate Agency": [("work-realestate-crm.webp", 782, 2000)],
 "Executive Calendar & Inbox Management": [("work-calendar-inbox.webp", 1400, 1076)],
 "Flyer Design for an Executive Brand": [("work-flyer-design.webp", 1400, 998)],
 "Instagram Content for a Rochester Realtor": [("work-realtor-ig-1.webp", 1038, 666), ("work-realtor-ig-2.webp", 1400, 693), ("work-realtor-ig-3.webp", 1000, 400)],
 "Featured Property Listings for a Luxury Brokerage": [("work-luxury-listings-1.webp", 1300, 1128), ("work-luxury-listings-2.webp", 1235, 877), ("work-luxury-listings-3.webp", 613, 2000)],
 "Property Search & Listing Updates for a Realtor": [("work-realtor-search.webp", 1400, 790)],
 "Executive Travel Planning": [("work-travel-planner.webp", 1400, 671)],
}

PROJECTS = [p for p in PROJECTS if p[0] in SHOTS]  # only projects with real work images

def gallery(p):
    return "|".join("assets/img/%s,%d,%d" % g for g in SHOTS.get(p[0], []))

def media(p):
    shots = SHOTS.get(p[0])
    if shots:
        shot = shots[0]
        more = ('<span class="shot-count">%d images</span>' % len(shots)) if len(shots) > 1 else ""
        return ('<img class="shot" src="assets/img/%s" width="%d" height="%d" alt="%s work sample" loading="lazy">%s'
                '<span class="project__view" aria-hidden="true">%s</span>' % (shot[0], shot[1], shot[2], esc(p[0]), more, I["arrow"]))
    return mock(p[6], p[7])

def mock(g, icon):
    return ('<div class="mock %s"><div class="mock__screen"><div class="mock__bar"><i></i><i></i><i></i></div>'
            '<div class="mock__body"><span></span><span></span><span></span><span></span><span></span></div></div>'
            '<div class="mock__icon">%s</div></div><span class="project__view" aria-hidden="true">%s</span>' % (g, I[icon], I["arrow"]))

def services_grid(with_price=False, limit=6):
    out = []
    for n, (ic, t, d, p) in enumerate(SERVICES[:limit], 1):
        out.append('<article class="service reveal" style="--d:%.2fs"><span class="service__num">%02d</span><span class="service__dot"></span>'
                   '<div class="service__icon">%s</div><h3 class="h-md">%s</h3><p>%s</p><a class="link-arrow" href="%s">%s %s</a></article>'
                   % ((n - 1) % 3 * 0.1, n, I[ic], t, d,
                      "contact.html" if with_price else "services.html", "Request a quote" if with_price else "View details", I["right"]))
    return '<div class="services-grid">%s</div>' % "".join(out)

def faq_block(items):
    out = []
    for n, (q, a) in enumerate(items):
        out.append('<div class="faq__item reveal"><button class="faq__q" type="button" aria-expanded="false" aria-controls="faq-%d">%s<span class="faq__plus" aria-hidden="true">+</span></button>'
                   '<div class="faq__a" id="faq-%d"><div><p>%s</p></div></div></div>' % (n, q, n, a))
    return '<div class="faq">%s</div>' % "".join(out)

def stars(n=5): return '<div class="stars" aria-label="%d out of 5 stars">%s</div>' % (n, I["star"] * n)

def testimonials():
    qs = "".join('<figure class="quote">%s<blockquote>“%s”</blockquote><cite><span class="avatar">%s</span><span><b>%s</b><small>%s</small></span></cite></figure>'
                 % (stars(), r[0], "UC", r[1], r[2]) for r in REVIEWS)
    return """
<section class="section"><div class="wrap">
  <div class="sec-head sec-head--split"><div class="sec-head">%s<h2 class="h-lg" data-split>What Clients <span class="accent">Say About My Work</span></h2></div>
  <p class="lead reveal">Real reviews from my Upwork clients, shared word for word.</p></div>
  <div class="testi">
    <div class="panel testi__badge reveal">%s</div>
    <div class="panel testi__slider reveal" data-slider>%s
      <div class="testi__nav"><button class="round-btn" type="button" data-q-prev aria-label="Previous review">%s</button><button class="round-btn" type="button" data-q-next aria-label="Next review">%s</button><div class="dots"></div></div>
    </div>
  </div>
  <div class="panel ratings reveal"><h3><span class="accent">My clients</span><br>consistently rate me 4.8/5</h3>
    <div class="ratings__items">
      <div class="rating"><span class="rating__logo">%s</span><div><b>4.8 / 5</b><small>Upwork client feedback</small></div></div>
      <div class="rating"><span class="rating__logo">15</span><div><b>15 jobs</b><small>completed on Upwork</small></div></div>
      <div class="rating"><span class="rating__logo">%s</span><div><b>100+ projects</b><small>in my portfolio</small></div></div>
    </div>
  </div>
  <div class="review-link reveal">%s</div>
</div></section>""" % (eyebrow("Testimonials"), ring_badge("Trusted by clients • Trusted by clients •", "”", "tb"), qs, I["left"], I["right"], I["upwork"], I["grid"], btn("Read all reviews on Upwork", CONFIG["upwork"], "btn--ghost", ext=True, sm=True))

def ribbons(words):
    def track(): return "".join("<span>%s</span><i>✦</i>" % w for w in words)
    return ('<div class="ribbons" aria-hidden="true"><div class="ribbon ribbon--b"><div class="ribbon__track">%s</div><div class="ribbon__track">%s</div></div>'
            '<div class="ribbon ribbon--a"><div class="ribbon__track">%s</div><div class="ribbon__track">%s</div></div></div>' % (track(), track(), track(), track()))

def process_block():
    steps = [("Discovery Call", "We talk through your week, your tools and what is draining your time, then agree on the top priorities."),
             ("Systems Setup", "I get access, organise your inbox, calendar and files, and write simple SOPs so nothing depends on memory."),
             ("Daily Execution", "I handle the work, keep follow-ups moving and flag what needs your decision, without being chased."),
             ("Weekly Report", "You get a clear summary of what was done, what is next and how your social channels performed.")]
    s = "".join('<div class="step"><div class="step__tab"><span>Step %02d</span></div><div><h3>%s</h3><p>%s</p></div></div>' % (i, t, d) for i, (t, d) in enumerate(steps, 1))
    return """
<section class="section"><div class="wrap process">
  <div class="process__sticky">%s<h2 class="h-lg" data-split>Shaping Your Week <span class="accent">Step by Step</span></h2>
    <p class="lead reveal">A simple, repeatable process so you always know what is happening and nothing falls through the cracks.</p>
    %s
    <div class="cube" aria-hidden="true"><div class="cube__in"><div></div><div></div><div></div><div></div><div></div><div></div></div></div>
  </div>
  <div class="steps">%s</div>
</div></section>""" % (eyebrow("How I work"), btn("Book a discovery call", "contact.html", "reveal"), s)

TOOLS_MARQUEE = lambda: ('<div class="logos" aria-label="Tools I use"><div class="logos__track">%s</div><div class="logos__track" aria-hidden="true">%s</div></div>'
                         % (("".join('<span class="logos__item">%s%s</span>' % (I["check"], t) for t in TOOLS),) * 2))

def doc(path, title, desc, active, main):
    full = '<!doctype html>\n<html lang="en">\n<head>\n' + head(title, desc) + '</head>\n<body>' + header(active) + '<main id="main">' + main + "</main>" + footer() + "</body>\n</html>\n"
    with open(os.path.join(ROOT, path), "w") as f: f.write(full)

# ---------------------------------------------------------------- HOME
home = """
<section class="hero">
  <canvas class="hero__canvas" aria-hidden="true"></canvas><div class="hero__glow"></div>
  <div class="capsules" aria-hidden="true"><span class="capsule"></span><span class="capsule"></span><span class="capsule"></span></div>
  <div class="hero__photo reveal reveal-right"><img src="assets/img/mary.webp" alt="Adeola Mary, Executive Virtual Assistant" width="801" height="1240" fetchpriority="high"></div>
  <div class="wrap hero__inner">
    <div class="hero__role reveal"><span class="chip"><i></i>Executive Virtual Assistant</span><span class="chip"><i></i>Social Media Manager</span></div>
    <h1 class="hero__title" data-split><span class="light">I Build Systems<svg viewBox="0 0 300 20" preserveAspectRatio="none" aria-hidden="true"><path d="M2 14 C 80 4, 200 2, 298 10" stroke="currentColor" stroke-width="3" fill="none" stroke-linecap="round"/></svg></span><br>That Give Founders<br>Their <span class="accent">Time Back</span></h1>
    <div class="hero__bottom">
      %s
      <p class="hero__text reveal">Hi, I'm Adeola Mary. I manage inboxes, calendars, CRMs and social media for busy founders and small teams, so your business stays organised and visible.</p>
      <div class="reveal" style="--d:.15s">%s</div>
    </div>
  </div>
</section>

<div class="wrap feature-strip"><div class="panel reveal">
  <div class="feature"><div class="feature__icon">%s</div><h3 class="h-md">Inbox & Calendar</h3><p>Priority filtering, drafted replies and a conflict-free calendar every week.</p><span class="plus" aria-hidden="true">+</span></div>
  <div class="feature"><div class="feature__icon">%s</div><h3 class="h-md">Social Media Growth</h3><p>Content calendars, Reels, captions and monthly reports that show what works.</p><span class="plus" aria-hidden="true">+</span></div>
  <div class="feature"><div class="feature__icon">%s</div><h3 class="h-md">CRM & Operations</h3><p>Clean pipelines, timely follow-ups and SOPs in HubSpot and GoHighLevel.</p><span class="plus" aria-hidden="true">+</span></div>
</div></div>

<section class="section"><div class="wrap about">
  <div class="about__media reveal reveal-left">
    <div class="arch"><img src="assets/img/mary.webp" alt="Adeola Mary smiling in a purple blazer with arms crossed" width="801" height="1240" loading="lazy"></div>
    <div class="panel about__card"><span class="num" data-count="15">15</span><p>Upwork jobs completed for founders and small businesses</p></div>
  </div>
  <div class="about__body">
    %s
    <h2 class="h-lg" data-split>A Proactive Assistant <span class="accent">Focused on Real Results</span></h2>
    <p class="lead reveal">Most VAs hand you a task list. I hand you a system. I spot what needs to happen next, keep follow-ups moving and protect your time, so your week runs without you chasing it.</p>
    <ul class="ticks reveal"><li>Inbox Zero systems</li><li>Calendar & scheduling</li><li>Content that converts</li><li>CRM & lead follow-up</li></ul>
    <div class="panel stat-row reveal"><div class="mini">%s</div><div><span class="num" data-count="4.8">4.8</span><p>Average client rating<br>on Upwork reviews</p></div></div>
    <div class="reveal">%s</div>
  </div>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">
  <div class="sec-head sec-head--center">%s<h2 class="h-lg" data-split>Helping You Succeed Through <span class="accent">Organised & Digital Support</span></h2></div>
  %s
</div></section>

<section class="section" style="padding-top:0"><div class="wrap">
  <div class="sec-head sec-head--split"><div class="sec-head">%s<h2 class="h-lg" data-split>My Recently Completed <span class="accent">Projects</span></h2></div>
    <div class="carousel__ctrl reveal"><button class="round-btn" type="button" data-prev="pc" aria-label="Previous projects">%s</button><button class="round-btn" type="button" data-next="pc" aria-label="Next projects">%s</button>%s</div></div>
  <div class="carousel" id="pc" data-carousel><div class="carousel__track">%s</div></div>
</div></section>

%s
%s

<section class="circle-cta"><div class="circle-cta__sticky"><div class="circle-cta__disc"></div>
  <div class="circle-cta__content"><h2>See How I Turn Busy Weeks Into Organised Systems</h2><p>Hand over the inbox, the calendar and the content calendar. Get back to the work only you can do.</p>%s</div>
</div></section>

%s

<section class="section"><div class="wrap">
  <div class="sec-head sec-head--center">%s<h2 class="h-lg" data-split>Questions? <span class="accent">Get the Answers Now</span></h2></div>
  %s
</div></section>
""" % (ring_badge("Executive VA • Social Media • ", "✦", "hb"),
       btn("Discover More", "about.html"),
       I["mail"], I["megaphone"], I["layers"],
       eyebrow("Who I am"), I["star"].replace('<svg', '<svg width="40" height="40"'), btn("More about me", "about.html"),
       eyebrow("What I do"), services_grid(),
       eyebrow("Portfolio"), I["left"], I["right"], btn("View all projects", "portfolio.html", "btn--ghost", sm=True),
       "".join('<a class="project" href="portfolio.html"><div class="project__media">%s</div><h3>%s</h3><div class="tags"><span>%s</span><span>%s</span></div></a>'
               % (media(p), p[0], p[2], p[5][0]) for p in PROJECTS[:7]),
       ribbons(["Inbox Zero", "Calendar Management", "Social Media", "Smart & Efficient", "CRM Systems", "Content Creation"]),
       process_block(),
       btn("Start working together", "contact.html"),
       testimonials(),
       eyebrow("FAQ"), faq_block(FAQ))

doc("index.html", "Adeola Mary", "Adeola Mary is an Executive Virtual Assistant and Social Media Manager helping founders stay organised and visible.", "index.html", home)

# ---------------------------------------------------------------- ABOUT
TIMELINE = [
 ("2018–21", "Digital Marketing Institute", "Social Media & CRM Systems", "Associate of Arts (AA)"),
 ("2019–21", "HubSpot Academy", "CRM & Marketing Strategy", "Certification programme"),
 ("2021–22", "Alison Online Learning", "Executive Virtual Assistance & CRM Systems", "Diploma"),
 ("2021–23", "Coursera", "Executive Administrative Support & Digital Management", "Professional certificate"),
 ("2022–24", "Udemy", "Executive Virtual Assistance", "Course certificate"),
]
SKILLS = [("Email & Calendar Management", 96), ("Social Media Management", 92), ("CRM (HubSpot, GoHighLevel)", 88), ("Research & Data Entry", 94), ("Canva Design", 85)]

about = page_hero("About <span class=\"accent\">Adeola Mary</span>", "About",
                  "An Executive Virtual Assistant and Social Media Manager from Lagos, helping founders, small business owners and social media teams stay organised and visible.") + """
<section class="section"><div class="wrap about">
  <div class="about__media reveal reveal-left">
    <div class="arch"><img src="assets/img/mary.webp" alt="Adeola Mary smiling in a purple blazer with arms crossed" width="801" height="1240" loading="lazy"></div>
    <div class="panel about__card"><span class="num" data-count="5" data-suffix="+">5+</span><p>Years of training and hands-on remote support</p></div>
  </div>
  <div class="about__body">
    %s
    <h2 class="h-lg" data-split>I Don't Just Do Tasks. <span class="accent">I Build Systems.</span></h2>
    <p class="lead reveal">I'm Mary, and I work with founders, small business owners and social media teams who are drowning in admin. I'm proactive rather than reactive: I spot what needs to happen next, keep follow-ups moving and protect your time.</p>
    <p class="lead reveal">I've supported real estate agencies, healthcare clinics, e-commerce stores, coaches and agencies, and I've run social media for an app launch. My clients describe me as professional, organised and detail-oriented.</p>
    <ul class="ticks reveal"><li>Executive assistance</li><li>Personal assistance</li><li>Social media management</li><li>CRM & operations</li></ul>
    <div class="reveal">%s</div>
  </div>
</div></section>

%s

<section class="section"><div class="wrap">
  <div class="sec-head">%s<h2 class="h-lg" data-split>Learning That Powers <span class="accent">Client Growth</span></h2></div>
  <div class="timeline-wrap" style="margin-top:50px">
    <div class="timeline">%s</div>
    <div class="panel big-years reveal reveal-right"><span class="n" data-count="5" data-suffix="+">5+</span><h3 class="h-md">Years of learning<br>and remote support</h3><p class="muted">HubSpot Academy, Digital Marketing Institute, Coursera, Alison and Udemy.</p></div>
  </div>
</div></section>

<section class="section" style="padding-top:0"><div class="wrap about">
  <div class="about__body">
    %s
    <h2 class="h-lg" data-split>Skills You Can <span class="accent">Count On</span></h2>
    <p class="lead reveal">The skills clients hire me for most, from inbox control to on-brand content.</p>
    %s
  </div>
  <div class="skills">%s</div>
</div></section>

%s
""" % (eyebrow("My story"), btn("Work with me", "contact.html"),
       ribbons(["Professional", "Organised", "Detail-Oriented", "Proactive", "Reliable", "On Time"]),
       eyebrow("Education & certifications"),
       "".join('<div class="panel tl reveal"><span class="tl__year">%s</span><div><small>%s</small><h3>%s</h3><p>%s</p></div></div>' % t for t in TIMELINE),
       eyebrow("Expertise"), btn("See my services", "services.html", "btn--ghost reveal"),
       "".join('<div class="skill"><div class="skill__top"><span>%s</span><span class="accent">%d%%</span></div><div class="skill__bar"><span style="--w:%d%%"></span></div></div>' % (n, v, v) for n, v in SKILLS),
       TOOLS_MARQUEE() + testimonials())
doc("about.html", "About Adeola Mary", "Mary's story, education, certifications and skills.", "about.html", about)

# ---------------------------------------------------------------- SERVICES
PLANS = [
 ("One-off Project", "", "single task", ["Inbox clean-up or calendar set-up", "Online research in Google Sheets", "One Canva flyer or graphic", "Delivered in 2–3 days"], False),
 ("Monthly Social Media", "", "ongoing package", ["Content calendar for 1 platform", "12 posts with captions & hashtags", "Scheduling and publishing", "Monthly performance report"], True),
 ("Executive Retainer", "", "dedicated support", ["Daily inbox & calendar management", "CRM updates and follow-ups", "SOPs and travel coordination", "Weekly summary report"], False),
]
services = page_hero("Services That <span class=\"accent\">Save You Time</span>", "Services",
                     "Hire me for a single task, a monthly social media package or a dedicated executive assistant retainer.") + """
<section class="section"><div class="wrap">
  <div class="sec-head sec-head--center">%s<h2 class="h-lg" data-split>Everything I Can <span class="accent">Take Off Your Plate</span></h2></div>
  %s
</div></section>
%s
<section class="section"><div class="wrap">
  <div class="sec-head sec-head--center">%s<h2 class="h-lg" data-split>Flexible Ways to <span class="accent">Work Together</span></h2><p class="lead reveal">Pick the kind of support that fits your business. Every package is tailored to you, and you get a quote after a short discovery call.</p></div>
  <div class="pricing">%s</div>
</div></section>
%s
<section class="section" style="padding-top:0"><div class="wrap">
  <div class="sec-head sec-head--center">%s<h2 class="h-lg" data-split>Questions About <span class="accent">Working Together</span></h2></div>
  %s
</div></section>
""" % (eyebrow("Services"), services_grid(with_price=True),
       ribbons(["Executive VA", "Personal VA", "Social Media", "Inbox Zero", "GoHighLevel", "Research"]),
       eyebrow("Packages"),
       "".join('<article class="panel plan reveal%s" style="--d:%.1fs">%s<h3 class="h-md">%s</h3><div class="plan__price"><small>%s%s</small></div><ul>%s</ul>%s</article>'
               % (" featured" if f else "", i * 0.1, '<span class="plan__tag">Popular</span>' if f else "", n, p, u.capitalize(),
                  "".join("<li>%s%s</li>" % (I["check"], x) for x in feats), btn("Request a quote", "contact.html", "" if f else "btn--ghost", sm=True))
               for i, (n, p, u, feats, f) in enumerate(PLANS)),
       process_block(), eyebrow("FAQ"), faq_block(FAQ))
doc("services.html", "Mary's Services", "Executive assistance, social media management, CRM support and research packages.", "services.html", services)

# ---------------------------------------------------------------- PORTFOLIO
cats = [c for c in [("all", "All work"), ("executive", "Executive VA"), ("social", "Social Media"), ("realestate", "Real Estate"), ("healthcare", "Healthcare"), ("admin", "Admin & Ops")] if c[0] == "all" or any(p[1] == c[0] for p in PROJECTS)]
works = "".join(
  '<button class="work reveal" type="button" data-cat="%s" data-title="%s" data-role="%s" data-desc="%s" data-skills="%s" data-gallery="%s" aria-haspopup="dialog">'
  '<div class="project__media">%s</div><h3>%s</h3><div class="tags"><span>%s</span><span>%s</span></div></button>'
  % (p[1], esc(p[0]), esc(p[3]), esc(p[4]), esc("|".join(p[5])), gallery(p), media(p), p[0], p[2], p[3]) for p in PROJECTS)
portfolio = page_hero("Selected <span class=\"accent\">Work</span>", "Portfolio",
                      "Real samples of my work in executive support, social media and real estate, picked from more than 100 projects.") + """
<section class="section"><div class="wrap">
  <div class="sec-head sec-head--split"><div class="sec-head">%s<h2 class="h-lg" data-split>Projects That <span class="accent">Delivered Results</span></h2></div><span class="count reveal" data-work-count aria-live="polite">%d projects</span></div>
  <div class="filters reveal" role="group" aria-label="Filter projects">%s</div>
  <div class="works">%s</div>
  <div style="margin-top:50px;display:flex;justify-content:center" class="reveal">%s</div>
</div></section>
%s
<div class="modal" aria-hidden="true"><div class="modal__shade" data-close-modal></div>
  <div class="panel modal__box" role="dialog" aria-modal="true" aria-labelledby="m-title">
    <button class="modal__close" type="button" data-close-modal aria-label="Close project">✕</button>
    <div class="modal__media"></div>
    <div class="modal__body"><span class="eyebrow" data-m-role></span><h3 class="h-md" id="m-title" data-m-title></h3><p data-m-desc></p><div class="skill-tags" data-m-tags></div><div>%s</div></div>
  </div>
</div>
""" % (eyebrow("Portfolio"), len(PROJECTS),
       "".join('<button class="filter" type="button" data-filter="%s" aria-pressed="%s">%s</button>' % (k, "true" if k == "all" else "false", v) for k, v in cats),
       works, btn("See all 100+ projects on Upwork", CONFIG["upwork"], ext=True),
       ribbons(["Real Estate", "Healthcare", "E-commerce", "Agencies", "Coaches", "Startups"]),
       btn("Start a similar project", "contact.html", sm=True))
doc("portfolio.html", "Mary's Portfolio", "Selected projects from Adeola Mary's executive assistant and social media work.", "portfolio.html", portfolio)

# ---------------------------------------------------------------- CONTACT
contact = page_hero("Let's <span class=\"accent\">Work Together</span>", "Contact",
                    "Tell me what's taking up too much of your time. I reply within 24 hours.") + """
<section class="section"><div class="wrap contact">
  <div class="panel contact__info reveal reveal-left">
    %s
    <h2 class="h-md">I'd love to hear from you</h2>
    <div class="info-item"><span class="info-item__icon">%s</span><div><small>Email</small><b id="mail-txt">%s</b><br><button class="copy" type="button" data-copy="%s">%s<span>Copy email</span></button></div></div>
    <div class="info-item"><span class="info-item__icon">%s</span><div><small>Upwork</small><a href="%s" target="_blank" rel="noopener">Hire me on Upwork ↗</a></div></div>
    <div class="info-item"><span class="info-item__icon">%s</span><div><small>LinkedIn</small><a href="%s" target="_blank" rel="noopener">Connect on LinkedIn ↗</a></div></div>
    <div class="info-item"><span class="info-item__icon">%s</span><div><small>Location</small><b>%s</b></div></div>
    <div class="info-item"><span class="info-item__icon">%s</span><div><small>Hours</small><b>%s</b></div></div>
  </div>
  <form class="panel form reveal reveal-right" id="contact-form" name="contact" method="POST" action="https://formsubmit.co/ajax/%s" data-email="%s" novalidate>
    <input type="hidden" name="_subject" value="New enquiry from your website"><input type="hidden" name="_template" value="table"><input type="text" name="_honey" tabindex="-1" autocomplete="off" aria-hidden="true" style="display:none">
    <div class="field"><label for="f-name">Your name <span>*</span></label><input id="f-name" name="name" type="text" autocomplete="name" required placeholder="Jane Founder"><span class="err" aria-live="polite"></span></div>
    <div class="field"><label for="f-email">Email <span>*</span></label><input id="f-email" name="email" type="email" autocomplete="email" required placeholder="jane@company.com"><span class="err" aria-live="polite"></span></div>
    <div class="field"><label for="f-company">Company</label><input id="f-company" name="company" type="text" autocomplete="organization" placeholder="Optional"><span class="err"></span></div>
    <div class="field"><label for="f-service">I need help with <span>*</span></label><select id="f-service" name="service" required><option value="">Choose a service</option>%s<option>Something else</option></select><span class="err" aria-live="polite"></span></div>
    <div class="field field--full"><label for="f-msg">Tell me about it <span>*</span></label><textarea id="f-msg" name="message" required placeholder="What's taking too much of your time?"></textarea><span class="err" aria-live="polite"></span></div>
    <p class="form__status" role="status" hidden></p>
    <div class="field--full"><button class="btn" type="submit"><span class="lbl">Send message</span><span class="btn__icon">%s</span></button></div>
  </form>
</div></section>
<section class="section" style="padding-top:0"><div class="wrap">
  <div class="sec-head sec-head--center">%s<h2 class="h-lg" data-split>Before You <span class="accent">Reach Out</span></h2></div>
  %s
</div></section>
<script>(function(){try{var e=new URLSearchParams(location.search).get("email");if(e){document.getElementById("f-email").value=e;}}catch(x){}})();</script>
""" % (eyebrow("Contact"), I["mail"], esc(CONFIG["email"]), esc(CONFIG["email"]), I["copy"], I["upwork"], CONFIG["upwork"], I["linkedin"], CONFIG["linkedin"],
       I["pin"], CONFIG["location"], I["clock"], CONFIG["hours"], esc(CONFIG["email"]), esc(CONFIG["email"]),
       "".join("<option>%s</option>" % s[1] for s in SERVICES), I["send"], eyebrow("FAQ"), faq_block(FAQ[:4]))
doc("contact.html", "Contact Adeola Mary", "Get in touch with Adeola Mary for executive assistance and social media management.", "contact.html", contact)
print("built 5 pages")
