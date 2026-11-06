#!/usr/bin/env python3
"""Build the Carreiro Studio Salon website into ./public.

Every page shares one header, footer and reserve chooser, so edit the content
here and run `python3 build.py`. The output is plain static HTML that any host
can serve; netlify.toml and public/_redirects are set up for Netlify.
"""
import html
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parent
OUT = ROOT / "public"
SITE = "https://carreirosalon.com"

BOOK_ANY = "https://carreirosalon.zenoti.com/WebstoreNew"
BOOK_BROADMEAD = "https://carreirosalon.zenoti.com/webstoreNew/services/451d915c-c74d-4cfe-8830-e6ff97b4ba68"
BOOK_DUNCAN = "https://carreirosalon.zenoti.com/webstoreNew/services/2e644194-1e77-49fb-88d5-e0a21b09a771"
GIFT_CARDS = "https://carreirosalon.zenoti.com/webstoreNew/giftcards/451d915c-c74d-4cfe-8830-e6ff97b4ba68"
SHOP = "https://carreirosalon.zenoti.com/WebstoreNew"
INSTAGRAM = "https://www.instagram.com/carreirothestudio"
FACEBOOK = "https://www.facebook.com/carreirosalon"
YOUTUBE = "https://www.youtube.com/@carreirosalon"
AVEDA_LOCATOR = "https://www.aveda.ca/locator/get_the_facts.tmpl?vanity=1&SalonID=61303"
PRESS_VIDEO = "https://www.youtube.com/watch?v=KMR-HDD7ZCA"

LOCATIONS = [
    {
        "key": "broadmead", "name": "Broadmead", "area": "Saanich",
        "street": "410-777 Royal Oak Drive", "city": "Saanich", "region": "BC",
        "phone": "(778) 432-4247", "tel": "+17784324247",
        "hours": [("Monday", "9am – 5pm"), ("Tuesday", "9am – 5pm"), ("Wednesday", "9am – 5pm"),
                  ("Thursday", "9am – 5pm"), ("Friday", "9am – 5pm"), ("Saturday", "9am – 5pm"), ("Sunday", None)],
        "hours_short": "Monday to Saturday 9am – 5pm",
        "schema_hours": [{"days": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], "opens": "09:00", "closes": "17:00"}],
        "book": BOOK_BROADMEAD, "img": "location-broadmead.webp",
        "img_alt": "The Carreiro Studio Salon storefront at Broadmead, with the Aveda sign in the window",
        "map": "https://www.google.com/maps/search/?api=1&query=Carreiro+Studio+Salon+777+Royal+Oak+Drive+Saanich+BC",
    },
    {
        "key": "duncan", "name": "Duncan", "area": "Downtown Duncan",
        "street": "106-80 Craig Street", "city": "Duncan", "region": "BC",
        "phone": "(250) 856-1020", "tel": "+12508561020",
        "hours": [("Monday", None), ("Tuesday", None), ("Wednesday", "10am – 5pm"), ("Thursday", "10am – 5pm"),
                  ("Friday", "10am – 5pm"), ("Saturday", "10am – 5pm"), ("Sunday", "11am – 5pm")],
        "hours_short": "Wednesday to Saturday 10am – 5pm, Sunday 11am – 5pm",
        "schema_hours": [{"days": ["Wednesday", "Thursday", "Friday", "Saturday"], "opens": "10:00", "closes": "17:00"},
                         {"days": ["Sunday"], "opens": "11:00", "closes": "17:00"}],
        "book": BOOK_DUNCAN, "img": "location-duncan.webp",
        "img_alt": "The Carreiro Studio Salon storefront on Craig Street in downtown Duncan",
        "map": "https://www.google.com/maps/search/?api=1&query=Carreiro+Studio+Salon+80+Craig+Street+Duncan+BC",
    },
]

SERVICES = [
    {"kind": "Styling", "name": "wash &amp; style", "pre": "from", "price": 45,
     "desc": "A wash, a relaxing head massage and a finished style."},
    {"kind": "Cutting", "name": "hair cut &amp; style", "pre": "from", "price": 60,
     "desc": "Your cut, shaped by one of our studio artists and finished with a style."},
    {"kind": "Purescription", "name": "conditioning treatment", "pre": "", "price": 30,
     "desc": "A conditioning treatment chosen for what your hair needs today."},
    {"kind": "Colour", "name": "colour", "pre": "from", "price": 80,
     "desc": "All-over colour, grey blending and gloss, mixed for you."},
    {"kind": "Foil", "name": "highlights", "pre": "", "price": 120,
     "desc": "Foil highlights placed to brighten and add dimension."},
    {"kind": "Relax", "name": "stress-relieving treatment", "pre": "", "price": 35,
     "desc": "Reconnect with your body and mind as you escape the noise of everyday life."},
]

TEAM = [
    ("Nick", "team-nick.webp"), ("Ayah", "team-ayah.webp"), ("Pam", "team-pam.webp"),
    ("Taylor", "team-taylor.webp"), ("Annah", "team-annah.webp"), ("Chelsy", "team-chelsy.webp"),
]

# ---------------------------------------------------------------- news posts
POSTS = [
    {
        "slug": "fall-winter-2026", "title": "Fall/Winter 2026", "date": "2026-10-20", "cats": ["News"],
        "img": "news-fall-winter-2026.webp", "img_alt": "Autumn leaves",
        "excerpt": "Black Friday sales, our 3rd annual toy drive, a new team member and our holiday hours.",
        "body": f"""
<p>Hello to all our wonderful guests!</p>
<p>As 2026 comes to a close, we wanted to take this time to thank all of you for your continued support and trust throughout the year! We truly value each and every one of you and always look forward to your visits!</p>
<p>We have a few exciting announcements to share as we head into our busiest time of year!</p>
<h2>Black Friday Sales!</h2>
<p>Black Friday sales on both Aveda and Kérastase products will run from November 23rd to November 30th, excluding holiday gift sets. It's the perfect time to treat yourself or get a head start on your holiday shopping!</p>
<h2>Our 3rd Annual Toy Drive!</h2>
<p>From November 1st to December 10th, we will be collecting new, unwrapped toys for The Zone radio's Willows Family Memorial Toy Drive. All donations will be distributed to various local charities throughout Greater Victoria.</p>
<p>We welcome toys for all ages, including puzzles, sports equipment, games, and art supplies!</p>
<p>As a special thank you for your generosity, every guest who brings in a toy will receive a complimentary deep conditioning treatment as our gift to you! We will also be accepting cash donations to purchase toys on your behalf.</p>
<p>Let's fill the salon with joy and help make a child smile this Christmas!</p>
<h2>Welcome, Kim!</h2>
<p>This year, we welcomed a new team member, Kim! She will be working at our Broadmead location on Mondays, Tuesdays, and Wednesdays!</p>
<h2>Holiday Hours</h2>
<ul>
<li>November 11th – Closed</li>
<li>December 24th – Closing at 3:00 PM</li>
<li>December 25th and 26th – Closed</li>
<li>December 31st – Closing at 3:00 PM</li>
<li>January 1st – Closed</li>
</ul>
<p>If you haven't <a href="{BOOK_ANY}" data-reserve>booked your holiday appointments</a> yet, we recommend booking soon, as spaces are filling up fast!</p>
<p>Once again, thank you all for another wonderful year of great people and great hair! We look forward to seeing everyone in 2027!</p>
<p>Cheers,<br>The Carreiro Studio Salon Staff and Family</p>
""",
    },
    {
        "slug": "pure-formance-grooming-clay", "title": "Aveda Men Pure-Formance Grooming Clay", "date": "2026-07-14",
        "cats": ["Product Spotlight"], "img": "news-grooming-clay.webp", "contain": True,
        "img_alt": "A jar of Aveda Men Pure-Formance Grooming Clay",
        "excerpt": "Our texture grooming clay creates definition with a strong, pliable hold and matte finish.",
        "body": """
<p>Texture grooming clay creates definition with a strong, pliable hold and matte finish.</p>
<p>This lightweight hair cream formula gives you control to create any style, perfect as a men's hair product for daily use. Adds texture and strong, pliable hold without adding shine. Its lightweight styling cream formula provides the control you need to create any style, with a comb or your fingers. Ideal for men's styling with the natural finish of grooming clay.</p>
<p>Available at both locations. <a href="https://www.aveda.ca/product/17776/16733/styling/mens-styling/aveda-men-pure-formance-grooming-clay?size=2.5_fl_oz%2F75_ml">Learn more at Aveda</a>.</p>
""",
    },
    {
        "slug": "holiday-kick-off", "title": "As 2025 Comes to a Close", "date": "2025-10-24", "cats": ["Events", "Promotions"],
        "img": "news-holiday-kick-off.webp", "img_alt": "Wrapped holiday gifts",
        "excerpt": "Save the date for our toy drive and the Aveda and Kérastase Black Friday sales.",
        "body": f"""
<p>Hello to all our wonderful guests!</p>
<p>As 2025 comes to a close, we wanted to take this time to thank all of you for your continued support and trust this year! We truly value you and always look forward to your visits!</p>
<h2>Save the Date</h2>
<ul>
<li><strong>November 1st</strong> – Willows Family Memorial Toy Drive</li>
<li><strong>November 20th</strong> – Aveda sale begins</li>
<li><strong>November 28th</strong> – Kérastase sale begins</li>
</ul>
<p>Black Friday sales are happening for both Aveda and Kérastase products, not including holiday packs. Aveda 25% off sale goes from November 20th to December 3rd and Kérastase 20% off sale goes from November 28th to December 3rd. A perfect time to get yourself a present!</p>
<p>Speaking of presents, we had so much success with our toy drive last year that we decided to do it again! From November 1st to December 12th we will be collecting new unwrapped toys for the Zone radio's Willows Family Memorial Toy Drive. All donations will be distributed to various local charities throughout Greater Victoria. Bring in toys for all ages, puzzles, sports equipment, games, and art supplies!</p>
<p>As a special thank you for your donation, every guest who brings in a toy will receive a complimentary deep conditioning treatment as our gift to you! We will also be accepting cash donations to purchase a toy on your behalf! Let's fill the salon with joy and make a kid smile this Christmas!</p>
<h2>Holiday Hours</h2>
<ul>
<li>November 11th – Closed</li>
<li>December 24th – Closed at 3pm</li>
<li>December 25th and 26th – Closed</li>
<li>December 31st – Closed at 3pm</li>
<li>January 1st – Closed</li>
</ul>
<p>If you haven't <a href="{BOOK_ANY}" data-reserve>booked your holiday appointments yet</a>, we recommend booking soon as space is filling up fast!</p>
<p>Once again, thank you all for another wonderful year of great people and great hair! We look forward to seeing everyone in 2026!</p>
<p>Cheers,<br>The Carreiro Salon staff and family</p>
""",
    },
    {
        "slug": "distinguished-gentlemans-ride", "title": "I'm Riding for Men's Health in The Distinguished Gentleman's Ride",
        "date": "2025-05-07", "cats": ["Events", "News"], "img": "news-dgr.webp", "contain": True,
        "img_alt": "The Distinguished Gentleman's Ride 2025 logo",
        "excerpt": "John rides to raise funds and awareness for prostate cancer and men's mental health on behalf of Movember.",
        "body": """
<p>On Sunday the 18th of May 2025, I'm riding in The Distinguished Gentleman's Ride with fellow men and women across the globe to raise funds and awareness for prostate cancer and men's mental health on behalf of Movember. Men die on average 6 years earlier than women and for largely preventable reasons. The number of men that are suffering is growing, and we need to do something about that.</p>
<p>So, before I press my tweed and polish my boots, I'm asking you to join me in raising funds and awareness for these causes by donating what you can for this meaningful cause and to help the men we love live happier and healthier lives.</p>
<p>– John</p>
<p><a class="btn" href="https://www.gentlemansride.com/fundraiser/JohnCarreiro649542">Help fund my ride</a></p>
""",
    },
    {
        "slug": "dear-carreiro-family", "title": "Dear Carreiro Family", "date": "2024-10-30", "cats": ["News", "Promotions"],
        "img": "news-dear-carreiro-family.webp", "img_alt": "Autumn still life",
        "excerpt": "As we approach the end of the year, we want to take a moment to thank you for a wonderful year.",
        "body": """
<p>As we approach the end of the year, we want to take a moment to thank you for a wonderful year! We truly appreciate each and every one of you.</p>
<p>It's been an eventful year. The closure of our flagship downtown location was a big change, but we have all settled in to our wonderful Broadmead location and our Duncan location continues to grow!</p>
<h2>Black Friday is just around the corner!</h2>
<p>November 25th to December 2nd we have 20% off all Aveda and Kérastase products! (Excluding gift packs, and price will be applied at checkout.)</p>
<p>We have always been a salon that strives to give back. We supported both local and international charities this year. In April we raised money for our Earth Month charity Mary's Meals, Ricardo donated his hair to Wigs for Kids and the salon raised money for the Cops for Cancer Tour de Rock! We want to finish off our year of giving in a personal way. Starting November 1st to December 15th, if you bring in a new, unwrapped toy, you'll receive a complimentary hair treatment as our thank you for supporting the Zone's toy drive in memory of the beloved Victoria radio host, Dylan Willows.</p>
<p>This year has brought many changes, and we are grateful for your patience and support throughout the process.</p>
<p>Wishing you all a wonderful holiday season, and we look forward to seeing you in the new year!</p>
<p>Warm regards,<br>Carreiro</p>
""",
    },
    {
        "slug": "were-hiring", "title": "We're Hiring", "date": "2024-01-19", "cats": ["Careers"],
        "img": "news-were-hiring.webp", "img_alt": "Salon styling tools",
        "excerpt": "Calling all stylists! Carreiro Salon is hiring for the Duncan location.",
        "body": """
<p>Calling all stylists! Carreiro Salon is hiring for the Duncan location.</p>
<h2>Join Our Team</h2>
<p>No matter what level of experience, we want to meet you. We want to learn about you and your career goals.</p>
<ul>
<li><strong>Flexibility</strong> with schedules and time-off</li>
<li><strong>Great earning potential</strong></li>
<li><strong>Choose your path:</strong> hair cutting, hair colour or both</li>
<li><strong>Opportunity</strong> for ongoing education</li>
</ul>
<h3>What to expect</h3>
<ul>
<li>Learn from Master Stylists</li>
<li>Find your creativity in one of our beautiful salons</li>
<li>Weekly education</li>
<li>Individual growth</li>
<li>One-on-one classes</li>
<li>Coaching and mentorship</li>
<li>A great time!</li>
</ul>
<p>Call <a href="tel:+17784324247">(778) 432-4247</a>, or see <a href="{P}join.html">current postings</a>.</p>
""",
    },
    {
        "slug": "come-celebrate-with-us", "title": "Come Celebrate with Us!", "date": "2023-11-07", "cats": ["Events"],
        "img": "location-broadmead.webp", "img_alt": "The Carreiro Broadmead storefront",
        "excerpt": "Celebrating our 5 year anniversary at Broadmead with a Customer Appreciation Day.",
        "body": """
<h2>Celebrating our 5 year anniversary for our Broadmead location</h2>
<p><strong>Customer Appreciation Day. Celebrating you and your support!</strong></p>
<p>Drop by our open house November 14th.<br>Time: 9:00am to 7:00pm<br>Location: <a href="{P}contact.html">Broadmead</a></p>
<ul>
<li>25% off Aveda (in-salon only)</li>
<li>Snack foods, drinks (non-alcoholic)</li>
<li>Get entered into a draw (huge gift basket worth approximately $750)</li>
<li>Hand treatments</li>
<li>Scalp massages</li>
<li>Skincare consultation with an esthetician</li>
<li>Gifts &amp; more…</li>
</ul>
""",
    },
    {
        "slug": "2023-best-hair-salon-in-victoria-bc", "title": "2023 Best Hair Salon in Victoria, BC", "date": "2023-09-02",
        "cats": ["News"], "img": "news-best-salon-2023.webp", "contain": True,
        "img_alt": "Quality Business Awards 2023 badge for Carreiro Studio Salon",
        "excerpt": "The Quality Business Awards recognizes businesses that achieve an average quality score of 95% or greater.",
        "body": """
<p>Carreiro Studio Salon Victoria achieved an overall quality score of 95% or greater.</p>
<p>The Quality Business Awards recognizes businesses that achieve an average quality score of 95% or greater over the previous 12 months. To learn more about the selection criteria, please visit <a href="http://www.qualitybusinessawards.ca/about-us">qualitybusinessawards.ca</a>.</p>
""",
    },
    {
        "slug": "genesis-homme", "title": "Genesis Homme", "date": "2022-06-15", "cats": ["Product Spotlight"],
        "img": "news-genesis-homme.webp", "contain": True, "img_alt": "Kérastase Genesis Homme products",
        "excerpt": "Genesis Homme by Kérastase is the first dual action anti-fall hair treatment for weakened hair prone to thinning.",
        "body": """
<p>Genesis Homme by Kérastase is the first dual action anti-fall hair treatment for weakened hair prone to thinning. It instantly thickens every fiber to give fuller hair on top while treating hair-fall in the long run.</p>
<p>The range, formulated with woody notes, rounder and warmer such as amber, is more masculine than its feminine counterpart.</p>
<h2>The Science Behind Hair Loss</h2>
<p>Did you know that <strong>70% of men worldwide</strong> report suffering from hair loss? It affects men of all ages, as even 1/3 of men under 30 are affected by hair loss. Typically, <strong>50 to 100 hairs fall</strong> naturally every day.</p>
<h3>Reduces hair loss in 6 weeks*. 5 times fuller hair**. 85% more hair fiber strength***.</h3>
<p class="muted">*Clinical test on 99 people. 6 weeks of use of Sérum Anti-chute Fortifiant. **Instrumental test Bain de Masse + Cire d'Épaisseur. ***Instrumental test on Bain de Masse Épaississant + Cire d'Épaisseur Texturisante + Sérum Anti-chute Fortifiant.</p>
<p>Ask your stylist about Genesis Homme at your next visit.</p>
""",
    },
    {
        "slug": "aveda-is-now-proudly-leaping-bunny-approved", "title": "Aveda is now proudly Leaping Bunny Approved!",
        "date": "2022-05-17", "cats": ["News"], "img": "news-leaping-bunny.webp", "contain": True,
        "img_alt": "Aveda Leaping Bunny approval announcement",
        "excerpt": "Aveda was born cruelty-free in 1978 and has now received Leaping Bunny approval through Cruelty Free International.",
        "body": """
<p>Dear Aveda Family,</p>
<p>Aveda was born cruelty-free in 1978 and has always been opposed to animal testing, a key component of our brand mission to care for the world and all of its inhabitants. Today, we are proudly sharing with you that we have received Leaping Bunny approval through Cruelty Free International, the globally recognized gold standard for cruelty-free products.</p>
<p>This is a truly exciting moment for Aveda because Leaping Bunny is the only internationally recognizable approval that requires a supplier monitoring system to be implemented by the brand, checks for animal testing down to and including the ingredient manufacturer level of the supply chain, and independent audits.</p>
<p>Aveda believes that cosmetic products should be cruelty free, and this approval through Leaping Bunny reaffirms our commitment.</p>
""",
    },
]

REVIEW = [
    "I had such a meaningful experience at Carreiro Studio Salon in downtown Duncan, and I feel compelled to share how exceptional Nick truly is. On December 23rd, Nick was working completely on his own — the only stylist in the salon — and yet he handled every situation with calm, grace, and professionalism while doing hair for my daughter and me.",
    "During our appointment, a man clearly down on his luck came into the salon looking for a haircut. Although Nick wasn’t able to help him that day, he spoke to him with genuine kindness, patience, and respect, never making him feel dismissed. Nick thoughtfully offered alternative options nearby and treated him with dignity, which spoke volumes about his character.",
    "At the same time, Nick took a phone call from a dissatisfied customer. Once again, he responded with professionalism, empathy, and clear communication, offering a solution rather than defensiveness. When that same customer later arrived at the salon seeking further answers, Nick handled the situation calmly and worked toward a resolution that left the customer satisfied — all without interrupting the care and attention he was giving us.",
    "Nick’s professionalism, compassion, and ability to manage multiple challenging situations at once were truly impressive. It’s rare to see someone balance excellent customer service with such genuine humanity. I left not only loving our hair, but feeling grateful to support a stylist who clearly cares deeply about people. Highly recommend Nick and Carreiro Studio Salon.",
]

# ---------------------------------------------------------------- helpers
ICON_IG = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2.2c3.2 0 3.6 0 4.8.1 1.2.1 1.8.2 2.2.4.6.2 1 .5 1.4.9.4.4.7.8.9 1.4.2.4.4 1.1.4 2.2.1 1.3.1 1.6.1 4.8s0 3.6-.1 4.8c-.1 1.2-.2 1.8-.4 2.2-.2.6-.5 1-.9 1.4-.4.4-.8.7-1.4.9-.4.2-1.1.4-2.2.4-1.3.1-1.6.1-4.8.1s-3.6 0-4.8-.1c-1.2-.1-1.8-.2-2.2-.4-.6-.2-1-.5-1.4-.9-.4-.4-.7-.8-.9-1.4-.2-.4-.4-1.1-.4-2.2C2.2 15.6 2.2 15.2 2.2 12s0-3.6.1-4.8c.1-1.2.2-1.8.4-2.2.2-.6.5-1 .9-1.4.4-.4.8-.7 1.4-.9.4-.2 1.1-.4 2.2-.4C8.4 2.2 8.8 2.2 12 2.2M12 0C8.7 0 8.3 0 7.1.1 5.8.1 4.9.3 4.1.6c-.8.3-1.5.7-2.1 1.4C1.3 2.6.9 3.3.6 4.1.3 4.9.1 5.8.1 7.1 0 8.3 0 8.7 0 12s0 3.7.1 4.9c.1 1.3.3 2.2.6 2.9.3.8.7 1.5 1.4 2.1.6.7 1.3 1.1 2.1 1.4.8.3 1.6.5 2.9.6 1.2.1 1.6.1 4.9.1s3.7 0 4.9-.1c1.3-.1 2.2-.3 2.9-.6.8-.3 1.5-.7 2.1-1.4.7-.6 1.1-1.3 1.4-2.1.3-.8.5-1.6.6-2.9.1-1.2.1-1.6.1-4.9s0-3.7-.1-4.9c-.1-1.3-.3-2.2-.6-2.9-.3-.8-.7-1.5-1.4-2.1C21.4 1.3 20.7.9 19.9.6 19.1.3 18.3.1 16.9.1 15.7 0 15.3 0 12 0zm0 5.8a6.2 6.2 0 1 0 0 12.4 6.2 6.2 0 0 0 0-12.4zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.4-11.8a1.4 1.4 0 1 0 0 2.9 1.4 1.4 0 0 0 0-2.9z"/></svg>'
ICON_FB = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M24 12.1C24 5.4 18.6 0 12 0S0 5.4 0 12.1c0 6 4.4 11 10.1 11.9v-8.4h-3v-3.5h3V9.4c0-3 1.8-4.7 4.5-4.7 1.3 0 2.7.2 2.7.2v3h-1.5c-1.5 0-2 .9-2 1.9v2.3h3.3l-.5 3.5h-2.8V24C19.6 23.1 24 18.1 24 12.1z"/></svg>'
ICON_YT = '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M23.5 6.2a3 3 0 0 0-2.1-2.1C19.5 3.6 12 3.6 12 3.6s-7.5 0-9.4.5A3 3 0 0 0 .5 6.2 31.6 31.6 0 0 0 0 12a31.6 31.6 0 0 0 .5 5.8 3 3 0 0 0 2.1 2.1c1.9.5 9.4.5 9.4.5s7.5 0 9.4-.5a3 3 0 0 0 2.1-2.1c.4-1.9.5-5.8.5-5.8s0-3.9-.5-5.8zM9.6 15.6V8.4l6.2 3.6-6.2 3.6z"/></svg>'

NAV = [
    ("our-story.html", "Our Story", "story"),
    ("meet-the-team.html", "Team", "team"),
    ("index.html#menu", "Services", "services"),
    ("news.html", "News", "news"),
    ("join.html", "Careers", "careers"),
    ("contact.html", "Contact", "contact"),
]


def fmt_date(iso):
    y, m, d = (int(x) for x in iso.split("-"))
    months = ["January", "February", "March", "April", "May", "June", "July", "August",
              "September", "October", "November", "December"]
    return f"{months[m - 1]} {d}, {y}"


def esc(s):
    return html.escape(s, quote=True)


def schema_salons():
    graph = []
    for loc in LOCATIONS:
        graph.append({
            "@type": "HairSalon",
            "@id": f"{SITE}/contact#{loc['key']}",
            "name": f"Carreiro Studio Salon {loc['name']}",
            "image": f"{SITE}/assets/img/{loc['img']}",
            "logo": f"{SITE}/assets/img/carreiro-logo.png",
            "url": SITE,
            "telephone": loc["phone"],
            "priceRange": "$$",
            "address": {"@type": "PostalAddress", "streetAddress": loc["street"], "addressLocality": loc["city"],
                        "addressRegion": loc["region"], "addressCountry": "CA"},
            "openingHoursSpecification": [
                {"@type": "OpeningHoursSpecification", "dayOfWeek": h["days"], "opens": h["opens"], "closes": h["closes"]}
                for h in loc["schema_hours"]
            ],
            "sameAs": [INSTAGRAM, FACEBOOK, YOUTUBE],
            "parentOrganization": {"@type": "Organization", "name": "Platino Salon Group"},
        })
    return json.dumps({"@context": "https://schema.org", "@graph": graph}, ensure_ascii=False)


def page(path, *, title, desc, body, active=None, og_image="og-image.jpg", schema=None, og_type="website", root_abs=False):
    depth = path.count("/")
    # Relative links so the site also works from a sub-folder or a preview host;
    # the 404 page is served from any URL, so it uses root-absolute links.
    p = "/" if root_abs else "../" * depth
    canonical = SITE + "/" + ("" if path == "index.html" else path[:-5])
    full_title = title if title.startswith("Carreiro") else f"{title} | Carreiro Studio Salon"
    nav = "\n      ".join(
        f'<a href="{p}{href}"{" aria-current=\"page\"" if key == active else ""}>{label}</a>'
        for href, label, key in NAV
    )
    loc_footer = "\n      ".join(
        f'<div class="footer-loc"><strong>{l["name"]}</strong><span>{l["street"]}</span><span>{l["city"]}, {l["region"]}</span><a href="tel:{l["tel"]}">{l["phone"]}</a></div>'
        for l in LOCATIONS
    )
    reserve_opts = "\n      ".join(
        f'<a class="reserve-option" href="{l["book"]}"><strong>{l["name"]}</strong><span>{l["street"]} · {l["phone"]}</span><i aria-hidden="true">→</i></a>'
        for l in LOCATIONS
    )
    schema_tag = f'<script type="application/ld+json">{schema}</script>' if schema else ""
    body = body.replace("{P}", p)
    return f'''<!doctype html>
<html lang="en-CA">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{esc(full_title)}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:site_name" content="Carreiro Studio Salon">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:type" content="{og_type}">
<meta property="og:image" content="{SITE}/assets/img/{og_image}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#f4f4f2">
<meta name="google-site-verification" content="DJB4DA9v7FGmvqfUy5ENje_hwns2goOTkqF-iJ-xXE4">
<meta name="google-site-verification" content="zm3FulGJxYwV8_t9lsu2u0T90LUv6EJ4ejQCAkEBOWo">
<link rel="icon" type="image/png" href="{p}assets/img/favicon.png">
<link rel="apple-touch-icon" href="{p}assets/img/favicon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Hanken+Grotesk:wght@400;500;600&amp;family=IBM+Plex+Mono:wght@400;500&amp;family=Instrument+Serif:ital@0;1&amp;display=swap">
<link rel="stylesheet" href="{p}assets/css/site.css">
{schema_tag}
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{p}index.html" aria-label="Carreiro Studio Salon, home"><img src="{p}assets/img/carreiro-logo.png" alt="Carreiro Studio Salon" width="984" height="196"></a>
    <nav class="nav" id="site-nav" aria-label="Main">
      {nav}
      <a class="nav-only-mobile" href="{GIFT_CARDS}">Gift Cards</a>
      <a class="nav-only-mobile" href="{SHOP}">Shop</a>
    </nav>
    <div class="header-cta">
      <a class="btn" href="{BOOK_ANY}" data-reserve>Reserve</a>
      <button class="menu-toggle" type="button" aria-controls="site-nav" aria-expanded="false" aria-label="Open menu"><span></span><span></span></button>
    </div>
  </div>
</header>

<main id="main">
{body}
</main>

<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <img src="{p}assets/img/carreiro-logo.png" alt="Carreiro Studio Salon" width="984" height="196" loading="lazy">
        <p>A salon, spa, barbershop and academy, led by master stylist John Carreiro. In Broadmead and downtown Duncan.</p>
        <div class="socials">
          <a href="{INSTAGRAM}" aria-label="Instagram">{ICON_IG}</a>
          <a href="{FACEBOOK}" aria-label="Facebook">{ICON_FB}</a>
          <a href="{YOUTUBE}" aria-label="YouTube">{ICON_YT}</a>
        </div>
      </div>
      {loc_footer}
      <div>
        <h4>Learn</h4>
        <ul>
          <li><a href="{p}our-story.html">Our Story</a></li>
          <li><a href="{p}meet-the-team.html">Team</a></li>
          <li><a href="{p}news.html">News</a></li>
          <li><a href="{p}terms-conditions.html">Terms &amp; Conditions</a></li>
          <li><a href="{p}shipping.html">Shipping</a></li>
        </ul>
      </div>
      <div>
        <h4>Interact</h4>
        <ul>
          <li><a href="{BOOK_ANY}" data-reserve>Book an Appointment</a></li>
          <li><a href="{GIFT_CARDS}">Gift Cards</a></li>
          <li><a href="{SHOP}">Shop</a></li>
          <li><a href="{p}join.html">Careers</a></li>
          <li><a href="{p}contact.html">Contact</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>©2026 Carreiro Studio Salon. Part of Platino Salon Group. All rights reserved.</span>
      <span>create. sculpt. form. hair</span>
    </div>
  </div>
</footer>

<div class="reserve-panel" id="reserve-panel" role="dialog" aria-modal="true" aria-labelledby="reserve-title" hidden>
  <div class="reserve-card">
    <button class="reserve-close" type="button" aria-label="Close">×</button>
    <p class="eyebrow"><span class="asterism">❋</span> Reserve an appointment</p>
    <h2 id="reserve-title">which studio?</h2>
    <div class="reserve-options">
      {reserve_opts}
    </div>
    <p class="muted">You’ll book online through our booking system. Prefer to call? Broadmead (778) 432-4247 · Duncan (250) 856-1020.</p>
  </div>
</div>
<script src="{p}assets/js/site.js" defer></script>
</body>
</html>
'''


def location_block(loc):
    return f'''
<article class="location">
  <figure class="artwork">
    <div class="frame"><img src="{{P}}assets/img/{loc["img"]}" alt="{esc(loc["img_alt"])}" loading="lazy"></div>
  </figure>
  <p class="eyebrow">{loc["area"]}</p>
  <h3>{loc["name"]}</h3>
  <dl class="location-meta">
    <dt>Visit</dt><dd><a href="{loc["map"]}">{loc["street"]}, {loc["city"]}</a></dd>
    <dt>Call</dt><dd><a href="tel:{loc["tel"]}">{loc["phone"]}</a></dd>
    <dt>Hours</dt><dd>{loc["hours_short"]}<br><span class="muted">Closed for stat holidays</span></dd>
  </dl>
  <div class="btn-row">
    <a class="btn" href="{loc["book"]}">Reserve {loc["name"]}</a>
    <a class="btn btn--ghost" href="{loc["map"]}">Directions</a>
  </div>
</article>'''


def placards():
    out = []
    for s in SERVICES:
        pre = f"<small>{s['pre']}</small>" if s["pre"] else ""
        out.append(f'''<article class="placard">
  <span class="placard-kind">{s["kind"]}</span>
  <div class="stack" style="gap:10px"><h3>{s["name"]}</h3><p>{s["desc"]}</p></div>
  <p class="price">{pre}<strong><sup>$</sup>{s["price"]}</strong></p>
</article>''')
    return "\n".join(out)


def post_card(post):
    cls = "frame contain" if post.get("contain") else "frame"
    cats = " · ".join(post["cats"])
    return f'''<a class="card" href="{{P}}news/{post["slug"]}.html" data-cats="{"|".join(post["cats"])}">
  <div class="{cls}"><img src="{{P}}assets/img/{post["img"]}" alt="{esc(post["img_alt"])}" loading="lazy"></div>
  <div class="card-meta"><time datetime="{post["date"]}">{fmt_date(post["date"])}</time><span>{cats}</span></div>
  <h3>{post["title"]}</h3>
  <p>{post["excerpt"]}</p>
</a>'''


SIGNUP = '''
<section class="band-ink section--tight" aria-labelledby="signup-title">
  <div class="wrap signup">
    <div class="stack">
      <p class="eyebrow"><span class="asterism">❋</span> Newsletter</p>
      <h2 class="h-lg" id="signup-title">news, tips <em>&amp;</em> invitations</h2>
    </div>
    <form class="signup-form" name="newsletter" method="POST" data-netlify="true" netlify-honeypot="company" data-signup novalidate>
      <input type="hidden" name="form-name" value="newsletter">
      <p class="visually-hidden"><label>Leave this empty <input name="company" tabindex="-1" autocomplete="off"></label></p>
      <p>Sign up with your email address to receive news and updates.</p>
      <label class="visually-hidden" for="signup-email">Email address</label>
      <div class="signup-row">
        <input id="signup-email" type="email" name="email" placeholder="Email address" autocomplete="email" required>
        <button type="submit">Sign up →</button>
      </div>
      <p class="form-status" role="status" aria-live="polite"></p>
    </form>
  </div>
</section>'''


# ---------------------------------------------------------------- pages
def build_home():
    locs = "\n".join(location_block(l) for l in LOCATIONS)
    news = "\n".join(post_card(p) for p in POSTS[:3])
    review_full = "".join(f"<p>{x}</p>" for x in REVIEW)
    body = f'''
<section class="hero">
  <div class="wrap hero-grid">
    <div class="hero-copy">
      <p class="eyebrow"><span class="asterism">❋</span> Located in Broadmead &amp; Duncan</p>
      <h1 class="hero-title" aria-label="create. sculpt. form. hair"><span>create.</span><span>sculpt.</span><span>form.</span><span>hair</span></h1>
      <p class="lede">A salon, spa, barbershop and academy. Inspired by European spas that honour your body, Carreiro pays tribute to your hair.</p>
      <div class="btn-row">
        <a class="btn" href="{BOOK_ANY}" data-reserve>Reserve</a>
        <a class="btn btn--ghost" href="{{P}}meet-the-team.html">Meet the team</a>
      </div>
    </div>
    <figure class="artwork hero-art">
      <div class="frame"><img src="{{P}}assets/img/hero-trendvision.webp" alt="Editorial portrait of a model with a glossy copper-red bob" width="1170" height="1167" fetchpriority="high"></div>
      <figcaption class="wall-label"><b>Gold, Wella Trendvision Awards Canada</b><span>John Carreiro, 2017</span></figcaption>
    </figure>
  </div>
</section>

<section class="band-ink section" aria-labelledby="intro-title">
  <div class="wrap statement-grid">
    <h2 class="statement" id="intro-title">We are a hair salon on paper. We assure you, we are <em>much, much more…</em></h2>
    <div class="stack">
      <p class="lede">A salon, spa, barbershop and academy. Most of all, a place to relax and unwind. Led by master stylist John Carreiro, our talented hair artists are dedicated to making your visit an experience.</p>
      <a class="link-arrow" href="{{P}}our-story.html" style="justify-self:start">Read our story →</a>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="loc-title">
  <div class="wrap">
    <div class="section-head">
      <div class="stack"><p class="eyebrow"><span class="asterism">❋</span> Two studios</p><h2 class="h-lg" id="loc-title">book one of our <em>talented</em> stylists</h2></div>
      <p class="muted">Broadmead in Saanich, and Craig Street in downtown Duncan. Choose a studio to see its stylists and open appointments.</p>
    </div>
    <div class="locations">{locs}</div>
  </div>
</section>

<section class="section band-paper" id="menu" aria-labelledby="menu-title">
  <div class="wrap">
    <div class="section-head">
      <div class="stack"><p class="eyebrow"><span class="asterism">❋</span> The menu</p><h2 class="h-lg" id="menu-title">services &amp; <em>pricing</em></h2></div>
      <p class="muted">Available at both locations. Prices in Canadian dollars; your stylist will confirm your price at your consultation.</p>
    </div>
    <div class="menu-grid">{placards()}</div>
    <div class="menu-note">
      <p class="muted">Not sure what to book? Call either studio and we’ll help you choose.</p>
      <a class="btn" href="{BOOK_ANY}" data-reserve>Reserve an appointment</a>
    </div>
  </div>
</section>

<section class="band-ink section" aria-labelledby="expect-title">
  <div class="wrap split">
    <div class="stack" style="gap:28px">
      <p class="eyebrow"><span class="asterism">❋</span> What to expect</p>
      <h2 class="h-lg" id="expect-title">leave the outside world <em>outside</em></h2>
      <p class="lede">After being greeted, walk down the stairs and enter your own personal world. “What happened to all the noise of traffic?” That’s usually the second impression.</p>
      <ul class="ritual">
        <li><span>I</span>Warm greetings and a friendly smile</li>
        <li><span>II</span>Soothing signature tea</li>
        <li><span>III</span>A relaxing head massage</li>
        <li><span>IV</span>An exquisite experience, every time</li>
      </ul>
    </div>
    <figure class="artwork">
      <div class="frame" style="aspect-ratio:4/5"><img src="{{P}}assets/img/mood-wash-chairs.webp" alt="Black shampoo chairs in the quiet wash area" loading="lazy"></div>
      <figcaption class="wall-label"><b>The wash room</b><span>Downstairs, away from the street</span></figcaption>
    </figure>
  </div>
</section>

<section class="section" aria-labelledby="vision-title">
  <div class="wrap">
    <p class="eyebrow"><span class="asterism">❋</span> Our brand foundation. Vision &amp; core values.</p>
    <h2 class="visually-hidden" id="vision-title">Our vision</h2>
    <blockquote class="mt-m"><p class="vision">“To redefine what a salon can be: exceptional service, unmatched expertise, every time.”</p></blockquote>
    <div class="values">
      <div class="value"><p class="eyebrow"><span class="asterism">❋</span> care</p><h3>we genuinely care</h3><p>We genuinely care for every guest and team member. A safe, welcoming environment and exceptional guest experience is at the heart of everything we do.</p></div>
      <div class="value"><p class="eyebrow"><span class="asterism">❋</span> excel</p><h3>we set the standard</h3><p>We are committed to being the best at what we do. Through continuous growth, clear communication, and mastery of our craft, we set the standard.</p></div>
      <div class="value"><p class="eyebrow"><span class="asterism">❋</span> inspire</p><h3>we inspire</h3><p>We inspire confidence, creativity, and community. Every guest leaves feeling transformed. Every team member feels empowered. Every community connection matters.</p></div>
    </div>
  </div>
</section>

<section class="section band-paper" aria-labelledby="work-title">
  <div class="wrap">
    <div class="section-head">
      <div class="stack"><p class="eyebrow"><span class="asterism">❋</span> Recent work</p><h2 class="h-lg" id="work-title">from the <em>studio</em></h2></div>
      <a class="link-arrow" href="{INSTAGRAM}">More on Instagram @carreirothestudio →</a>
    </div>
    <div class="gallery">
      <figure class="artwork">
        <div class="frame"><img src="{{P}}assets/img/work-blonde-grey-blend.webp" alt="Long curled hair in a bright blonde and grey blend" loading="lazy"></div>
        <figcaption class="wall-label"><b>Blonde / grey blend</b><span>John Carreiro · Duncan</span></figcaption>
      </figure>
      <figure class="artwork">
        <div class="frame"><img src="{{P}}assets/img/work-creamy-balayage.webp" alt="Long straight hair with a creamy blonde balayage and layers" loading="lazy"></div>
        <figcaption class="wall-label"><b>Creamy blonde balayage &amp; layers</b><span>@pammihairstyles &amp; @kaiasstudio · Duncan</span></figcaption>
      </figure>
      <figure class="artwork">
        <div class="frame"><img src="{{P}}assets/img/mood-bob.webp" alt="Soft, tousled bob with lived-in colour" loading="lazy"></div>
        <figcaption class="wall-label"><b>Lived-in bob</b><span>Soft texture, natural finish</span></figcaption>
      </figure>
    </div>
  </div>
</section>

<section class="photo-band" aria-labelledby="aveda-title">
  <img src="{{P}}assets/img/aveda-botanical.webp" alt="" loading="lazy">
  <div class="wrap on-dark">
    <div class="stack" style="gap:28px;max-width:560px">
      <p class="eyebrow">Available at both locations</p>
      <h2 class="h-lg" id="aveda-title">come see the full collection of aveda</h2>
      <p class="lede">Our stylists’ favourites, in the studio and online. We also carry Kérastase.</p>
      <div class="btn-row">
        <a class="btn" href="{SHOP}">Shop stylists’ favourites</a>
        <a class="btn btn--ghost" href="{AVEDA_LOCATOR}">Aveda salon details</a>
      </div>
    </div>
  </div>
</section>

<section class="section" aria-labelledby="review-title">
  <div class="wrap quote-wrap">
    <div class="stack"><span class="quote-mark" aria-hidden="true">“</span><p class="eyebrow" id="review-title">Guest review</p></div>
    <blockquote>
      <p class="pull">“I left not only loving our hair, but feeling grateful to support a stylist who clearly cares deeply about people. Highly recommend Nick and Carreiro Studio Salon.”</p>
      <footer>Janet · Downtown Duncan</footer>
      <details class="full-review">
        <summary>Read Janet’s full review</summary>
        <div class="review-body">{review_full}<p>Thank you,<br>Janet</p></div>
      </details>
    </blockquote>
  </div>
</section>

<section class="section--tight" aria-label="Gift cards and press" style="padding-top:0">
  <div class="wrap duo">
    <article class="panel panel--image">
      <img src="{{P}}assets/img/giftcard.webp" alt="" loading="lazy">
      <div class="panel-inner">
        <p class="eyebrow">Gift cards</p>
        <h2 class="h-lg">give the gift of <em>graciousness</em></h2>
        <p>Salon visits are as thoughtful a gift as flowers. With a gift card, you can brighten up someone’s day, week and month with a salon service of their choice. They’re available in any denomination and we’ll mail it for free.</p>
        <a class="btn" href="{GIFT_CARDS}" style="--b:var(--on-dark);--f:var(--ink)">Buy a gift card</a>
      </div>
    </article>
    <article class="panel panel--ink on-dark">
      <p class="eyebrow">In the press · The Wealthy Life with Sybil Verch</p>
      <h2 class="h-lg">how much is your hair <em>worth?</em></h2>
      <p>Owner, John Carreiro, shares tips on how to save money on hair styling costs.</p>
      <a class="btn" href="{PRESS_VIDEO}">Watch the interview</a>
    </article>
  </div>
</section>

<section class="section" aria-labelledby="news-title" style="padding-top:clamp(32px,5vw,64px)">
  <div class="wrap">
    <div class="section-head">
      <div class="stack"><p class="eyebrow"><span class="asterism">❋</span> Is it news you’re after?</p><h2 class="h-lg" id="news-title">the <em>latest</em></h2></div>
      <p class="muted">Keep up-to-date with what’s happening at Carreiro. We love giving advice and tips on hair care, such as protecting yourself from the elements and exploring new styles. <a href="{{P}}news.html">All news →</a></p>
    </div>
    <div class="cards">{news}</div>
  </div>
</section>
{SIGNUP}'''
    return page("index.html", title="Carreiro Studio Salon | Hair Salon in Broadmead & Duncan, BC",
                desc="Carreiro Studio Salon is a salon, spa, barbershop and academy led by master stylist John Carreiro, with studios in Broadmead (Saanich) and downtown Duncan, BC. Reserve online.",
                body=body, schema=schema_salons())


def build_story():
    body = f'''
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow"><span class="asterism">❋</span> Our story</p>
    <h1 class="h-xl">a salon, spa, barbershop <em>and academy</em></h1>
  </div>
</section>

<section class="section--tight" style="padding-top:0">
  <div class="wrap">
    <figure class="artwork figure-wide">
      <div class="frame"><img src="{{P}}assets/img/story-john-trendvision.webp" alt="John Carreiro beside his gold-winning Trendvision look, a model with a copper-red bob" width="1500" height="1125"></div>
      <figcaption class="wall-label"><b>John Carreiro</b><span>Master stylist and owner, with his 2017 Wella Trendvision gold look</span></figcaption>
    </figure>
  </div>
</section>

<section class="section">
  <div class="wrap split split--top">
    <h2 class="h-lg">we are a hair salon <em>on paper</em></h2>
    <div class="prose">
      <p class="dropcap">We assure you, we are much, much more… a salon, spa, barbershop and academy. Most of all, a place to relax and unwind. Inspired by European spas that honour your body, Carreiro pays tribute to your hair. Led by master stylist John Carreiro, our talented hair artists are dedicated to making your visit an experience.</p>
      <p>At times, passers-by mistake us for an art gallery on first impression, but when you choose to walk in, all that changes. Our goal is to have you forget the outside world, well… leave it outside at least. After being greeted, walk down the stairs and enter your own personal world. “What happened to all the noise of traffic?” That’s usually the second impression.</p>
    </div>
  </div>
</section>

<section class="band-ink section" aria-labelledby="john-title">
  <div class="wrap">
    <div class="split split--top">
      <div class="stack" style="gap:24px">
        <p class="eyebrow"><span class="asterism">❋</span> Led by John Carreiro</p>
        <h2 class="h-lg" id="john-title">a care space for hair that is very much <em>his own</em></h2>
      </div>
      <div class="stack" style="gap:20px">
        <p class="lede">After 25 years of international experience as a platform artist, mentor, product educator and salon manager, John created a care space for hair that is very much his own. Sleek and sophisticated, it provides the perfect atmosphere for creativity and personal excellence.</p>
        <p class="lede">Passionate about his industry, John mentors our studio artists, from the most seasoned stylists to new talent, to ensure they are the best in the profession.</p>
      </div>
    </div>
    <dl class="facts mt-l">
      <div><dt>25 years</dt><dd>of international experience</dd></div>
      <div><dt>Platform artist</dt><dd>mentor, product educator and salon manager</dd></div>
      <div><dt>2017 Gold</dt><dd>Wella Trendvision Awards Canada</dd></div>
      <div><dt>95%+</dt><dd>Quality Business Awards, Best Hair Salon in Victoria, 2023</dd></div>
    </dl>
  </div>
</section>

<section class="section">
  <div class="wrap split">
    <figure class="artwork">
      <div class="frame" style="aspect-ratio:3/2"><img src="{{P}}assets/img/mood-wash-bowls.webp" alt="A row of black shampoo bowls" loading="lazy"></div>
    </figure>
    <div class="stack" style="gap:24px">
      <p class="eyebrow"><span class="asterism">❋</span> Together</p>
      <h2 class="h-lg">an <em>exquisite</em> experience</h2>
      <p class="lede">Together, we focus on excellence and ensuring each studio guest has an exquisite experience. Warm greetings, a friendly smile, soothing signature tea and a relaxing head massage all await you.</p>
      <div class="btn-row"><a class="btn" href="{BOOK_ANY}" data-reserve>Reserve</a><a class="btn btn--ghost" href="{{P}}meet-the-team.html">Meet the team</a></div>
    </div>
  </div>
</section>

<section class="section band-paper" aria-labelledby="give-title">
  <div class="wrap split split--top">
    <div class="stack" style="gap:24px">
      <p class="eyebrow"><span class="asterism">❋</span> Giving back</p>
      <h2 class="h-lg" id="give-title">we have always been a salon that strives to <em>give back</em></h2>
    </div>
    <div class="prose">
      <p>We support both local and international charities. We have raised money for our Earth Month charity Mary’s Meals, our team has donated hair to Wigs for Kids, and the salon has raised money for the Cops for Cancer Tour de Rock.</p>
      <p>Every holiday season we collect new, unwrapped toys for The Zone radio’s Willows Family Memorial Toy Drive, in memory of the beloved Victoria radio host Dylan Willows. Every guest who brings in a toy receives a complimentary deep conditioning treatment as our thank you.</p>
      <p>John also rides in The Distinguished Gentleman’s Ride, raising funds and awareness for prostate cancer and men’s mental health on behalf of Movember. <a href="{{P}}news/distinguished-gentlemans-ride.html">Read John’s note →</a></p>
    </div>
  </div>
</section>
{SIGNUP}'''
    return page("our-story.html", title="Our Story", active="story",
                desc="Carreiro Studio Salon is a hair salon on paper, and much more: a salon, spa, barbershop and academy led by master stylist John Carreiro.",
                body=body)


def build_team():
    members = "\n".join(
        f'<figure class="member"><div class="frame"><img src="{{P}}assets/img/{img}" alt="{name}, studio artist at Carreiro" loading="lazy"></div><figcaption><strong>{name}</strong><span>Studio artist</span></figcaption></figure>'
        for name, img in TEAM
    )
    body = f'''
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow"><span class="asterism">❋</span> Meet the team</p>
    <h1 class="h-xl">our studio <em>artists</em></h1>
    <p class="lede">Together, we focus on excellence and ensuring each studio guest has an exquisite experience. Warm greetings, a friendly smile, soothing signature tea and a relaxing head massage all await you.</p>
    <div class="btn-row mt-m">
      <a class="btn" href="{BOOK_BROADMEAD}">Reserve Broadmead</a>
      <a class="btn btn--ghost" href="{BOOK_DUNCAN}">Reserve Duncan</a>
    </div>
  </div>
</section>

<section class="section--tight" style="padding-top:0">
  <div class="wrap team-lead">
    <figure class="artwork">
      <div class="frame"><img src="{{P}}assets/img/team-john.webp" alt="Portrait of John Carreiro" width="900" height="1436"></div>
    </figure>
    <div class="stack" style="gap:24px;padding-bottom:12px">
      <p class="eyebrow">Owner · Master stylist</p>
      <h2 class="h-xl">John</h2>
      <p class="lede">After 25 years of international experience as a platform artist, mentor, product educator and salon manager, John created a care space for hair that is very much his own. He mentors our studio artists, from the most seasoned stylists to new talent, to ensure they are the best in the profession.</p>
      <a class="link-arrow" href="{{P}}our-story.html" style="justify-self:start">Our story →</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <div class="stack"><p class="eyebrow"><span class="asterism">❋</span> The team</p><h2 class="h-lg">book one of our <em>talented</em> stylists</h2></div>
      <p class="muted">Our goal is to have you forget the outside world, well… leave it outside at least.</p>
    </div>
    <div class="team-grid">{members}</div>
  </div>
</section>

<section class="band-ink section--tight">
  <div class="wrap section-head" style="margin-bottom:0">
    <h2 class="h-lg">join the <em>team</em></h2>
    <div class="stack"><p class="lede">No matter what level of experience, we want to meet you.</p><a class="btn" href="{{P}}join.html" style="justify-self:start">See careers</a></div>
  </div>
</section>'''
    return page("meet-the-team.html", title="Meet the Team", active="team",
                desc="Meet John Carreiro and the studio artists at Carreiro Studio Salon in Broadmead and Duncan, BC.", body=body)


def build_contact():
    cards = []
    for loc in LOCATIONS:
        rows = "".join(
            f'<tr{" class=\"closed\"" if not h else ""}><th scope="row">{d}</th><td>{h or "Closed"}</td></tr>' for d, h in loc["hours"]
        )
        cards.append(f'''
<article class="contact-card" id="{loc["key"]}">
  <figure class="artwork"><div class="frame" style="aspect-ratio:16/9"><img src="{{P}}assets/img/{loc["img"]}" alt="{esc(loc["img_alt"])}" loading="lazy"></div></figure>
  <p class="eyebrow">{loc["area"]}</p>
  <h2>{loc["name"]}</h2>
  <p>{loc["street"]}<br>{loc["city"]}, {loc["region"]}</p>
  <a class="big-phone" href="tel:{loc["tel"]}">{loc["phone"]}</a>
  <table class="hours"><caption class="visually-hidden">{loc["name"]} opening hours</caption><tbody>{rows}</tbody></table>
  <p class="muted">Closed for stat holidays.</p>
  <div class="btn-row"><a class="btn" href="{loc["book"]}">Reserve {loc["name"]}</a><a class="btn btn--ghost" href="{loc["map"]}">Directions</a></div>
</article>''')
    body = f'''
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow"><span class="asterism">❋</span> Contact</p>
    <h1 class="h-xl">contact <em>us.</em></h1>
    <p class="lede">Call either studio, reserve online, or send us a message on Instagram <a href="{INSTAGRAM}">@carreirothestudio</a>.</p>
  </div>
</section>
<section class="section--tight" style="padding-top:0">
  <div class="wrap locations">{"".join(cards)}</div>
</section>
<section class="band-paper section--tight">
  <div class="wrap section-head" style="margin-bottom:0">
    <div class="stack"><p class="eyebrow">Follow along</p><h2 class="h-lg">@carreirothestudio</h2></div>
    <div class="btn-row"><a class="btn" href="{INSTAGRAM}">Instagram</a><a class="btn btn--ghost" href="{FACEBOOK}">Facebook</a><a class="btn btn--ghost" href="{YOUTUBE}">YouTube</a></div>
  </div>
</section>'''
    return page("contact.html", title="Contact & Hours", active="contact",
                desc="Addresses, phone numbers and hours for Carreiro Studio Salon in Broadmead (410-777 Royal Oak Drive) and downtown Duncan (106-80 Craig Street).",
                body=body, schema=schema_salons())


def build_join():
    body = f'''
<section class="page-head">
  <div class="wrap split split--top">
    <div class="stack" style="gap:20px">
      <p class="eyebrow"><span class="asterism">❋</span> Careers</p>
      <h1 class="h-xl">let’s work <em>together</em></h1>
    </div>
    <div class="stack" style="gap:20px;align-self:end">
      <p class="lede">No matter what level of experience, we want to meet you. We want to learn about you and your career goals.</p>
      <div class="btn-row"><a class="btn" href="tel:+17784324247">Call (778) 432-4247</a></div>
    </div>
  </div>
</section>

<section class="section--tight" style="padding-top:0">
  <div class="wrap">
    <p class="eyebrow" style="margin-bottom:20px">Current postings</p>
    <div class="postings">
      <article class="posting">
        <time datetime="2024-06-26">June 26, 2024</time>
        <div><h3>Stylist, Duncan</h3><p>Carreiro Salon is hiring for the Duncan location. Great earning potential.</p></div>
        <a class="btn btn--ghost" href="tel:+12508561020">Call Duncan</a>
      </article>
      <article class="posting">
        <time datetime="2024-06-25">June 25, 2024</time>
        <div><h3>Hiring for Broadmead</h3><p>Join the Carreiro team by submitting your resume or in person at 410-777 Royal Oak Drive.</p></div>
        <a class="btn btn--ghost" href="tel:+17784324247">Call Broadmead</a>
      </article>
    </div>
  </div>
</section>

<section class="band-ink section">
  <div class="wrap">
    <div class="section-head"><h2 class="h-lg">why <em>Carreiro</em></h2><p class="lede">Learn from master stylists and find your creativity in one of our beautiful salons.</p></div>
    <div class="perks">
      <div><h3>Flexibility</h3><p>With schedules and time-off.</p></div>
      <div><h3>Choose your path</h3><p>Hair cutting, hair colour or both, with great earning potential.</p></div>
      <div><h3>Opportunity</h3><p>Ongoing education, coaching and mentorship.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap split split--top">
    <div class="stack" style="gap:24px">
      <p class="eyebrow"><span class="asterism">❋</span> What to expect</p>
      <h2 class="h-lg">grow with <em>us</em></h2>
      <figure class="artwork"><div class="frame" style="aspect-ratio:3/2"><img src="{{P}}assets/img/careers-studio.webp" alt="Inside the Carreiro studio" loading="lazy"></div></figure>
    </div>
    <ul class="checklist">
      <li>Learn from Master Stylists</li>
      <li>Find your creativity in one of our beautiful salons</li>
      <li>Weekly education</li>
      <li>Individual growth</li>
      <li>One-on-one classes</li>
      <li>Coaching and mentorship</li>
      <li>A great time!</li>
    </ul>
  </div>
</section>'''
    return page("join.html", title="Careers", active="careers",
                desc="Stylist careers at Carreiro Studio Salon in Broadmead and Duncan, BC. Flexibility, great earning potential and ongoing education.",
                body=body)


def build_news():
    feat = POSTS[0]
    rest = "\n".join(post_card(p) for p in POSTS[1:])
    cats = []
    for p in POSTS[1:]:
        for c in p["cats"]:
            if c not in cats:
                cats.append(c)
    filters = '<button type="button" data-filter="all" aria-pressed="true">All</button>' + "".join(
        f'<button type="button" data-filter="{c}" aria-pressed="false">{c}</button>' for c in cats)
    body = f'''
<section class="page-head">
  <div class="wrap">
    <p class="eyebrow"><span class="asterism">❋</span> News</p>
    <h1 class="h-xl">is it news <em>you’re after?</em></h1>
    <p class="lede">Keep up-to-date with what’s happening at Carreiro. We love giving advice and tips on hair care, such as protecting yourself from the elements and exploring new styles.</p>
  </div>
</section>
<section class="section--tight" style="padding-top:0">
  <div class="wrap">
    <a class="feature-post" href="{{P}}news/{feat["slug"]}.html">
      <div class="frame"><img src="{{P}}assets/img/{feat["img"]}" alt="{esc(feat["img_alt"])}"></div>
      <div class="stack" style="gap:18px">
        <div class="card-meta"><span>Latest</span><time datetime="{feat["date"]}">{fmt_date(feat["date"])}</time><span>{" · ".join(feat["cats"])}</span></div>
        <h2 class="h-lg">{feat["title"]}</h2>
        <p class="lede">{feat["excerpt"]}</p>
        <span class="link-arrow" style="justify-self:start">Read more →</span>
      </div>
    </a>
    <div class="filters" role="group" aria-label="Filter posts by category">{filters}</div>
    <div class="cards">{rest}</div>
  </div>
</section>
{SIGNUP}'''
    return page("news.html", title="News", active="news",
                desc="News, events, product spotlights and promotions from Carreiro Studio Salon in Broadmead and Duncan, BC.", body=body)


def build_post(i, post):
    newer = POSTS[i - 1] if i > 0 else None
    older = POSTS[i + 1] if i + 1 < len(POSTS) else None
    cls = "frame contain" if post.get("contain") else "frame"
    nav = '<nav class="article-nav" aria-label="More posts">'
    nav += f'<a class="link-arrow" href="{{P}}news/{older["slug"]}.html">← Older</a>' if older else "<span></span>"
    nav += f'<a class="link-arrow" href="{{P}}news/{newer["slug"]}.html">Newer →</a>' if newer else "<span></span>"
    nav += "</nav>"
    article_schema = json.dumps({
        "@context": "https://schema.org", "@type": "BlogPosting", "headline": post["title"],
        "datePublished": post["date"], "image": f"{SITE}/assets/img/{post['img']}",
        "publisher": {"@type": "Organization", "name": "Carreiro Studio Salon",
                      "logo": {"@type": "ImageObject", "url": f"{SITE}/assets/img/carreiro-logo.png"}},
        "mainEntityOfPage": f"{SITE}/news/{post['slug']}",
    }, ensure_ascii=False)
    body = f'''
<article>
  <header class="page-head" style="padding-bottom:0">
    <div class="wrap">
      <div class="article-head">
        <a class="link-arrow" href="{{P}}news.html" style="justify-self:start">← All news</a>
        <div class="card-meta"><time datetime="{post["date"]}">{fmt_date(post["date"])}</time><span>{" · ".join(post["cats"])}</span></div>
        <h1 class="h-xl">{post["title"]}</h1>
      </div>
      <figure class="artwork article-hero"><div class="{cls}"><img src="{{P}}assets/img/{post["img"]}" alt="{esc(post["img_alt"])}"></div></figure>
    </div>
  </header>
  <div class="section">
    <div class="wrap article-body">
      <aside class="article-aside">
        <p class="eyebrow">Carreiro Studio Salon</p>
        <p class="muted">Broadmead (778) 432-4247<br>Duncan (250) 856-1020</p>
        <a class="btn" href="{BOOK_ANY}" data-reserve style="justify-self:start">Reserve</a>
      </aside>
      <div>
        <div class="prose">{post["body"]}</div>
        {nav}
      </div>
    </div>
  </div>
</article>
{SIGNUP}'''
    return page(f"news/{post['slug']}.html", title=post["title"], active="news", desc=post["excerpt"], body=body,
                og_image=post["img"], schema=article_schema, og_type="article")


TERMS_HEADS = ["Introduction", "Variation", "Limited Warranties", "Limitations and Exclusions of Liability",
               "Licence to Use Website", "External Links", "Law and Jurisdiction"]


def build_legal():
    data = json.loads((ROOT / "content" / "legal.json").read_text(encoding="utf-8"))
    parts, in_list = [], False
    for tag, text in data["terms-conditions"][1:]:
        if tag == "li":
            if not in_list:
                parts.append("<ul>")
                in_list = True
            parts.append(f"<li>{esc(text)}</li>")
            continue
        if in_list:
            parts.append("</ul>")
            in_list = False
        m = re.match(r"\((\d)\) (.*)", text)
        if m:
            head = TERMS_HEADS[int(m.group(1)) - 1]
            parts.append(f"<h2>({m.group(1)}) {head}</h2>")
            text = m.group(2)[len(head):].strip()
        parts.append(f"<p>{esc(text)}</p>")
    if in_list:
        parts.append("</ul>")
    terms = page("terms-conditions.html", title="Terms & Conditions",
                 desc="Terms and conditions of use for the Carreiro Studio Salon website.",
                 body=f'''<section class="page-head"><div class="wrap"><p class="eyebrow"><span class="asterism">❋</span> Legal</p><h1 class="h-xl">terms of <em>service.</em></h1></div></section>
<section class="section--tight" style="padding-top:0"><div class="wrap"><div class="prose">{"".join(parts)}</div></div></section>''')
    parts = []
    for tag, text in data["shipping"][1:]:
        if text.isupper() or text.startswith("FREE SHIPPING"):
            title = text.title().replace("Usa", "USA").replace("(Within", "(within")
            parts.append(f"<h2>{esc(title)}</h2>")
        else:
            t = esc(text).replace("please contact us.", 'please <a href="{P}contact.html">contact us</a>.')
            parts.append(f"<p>{t}</p>")
    ship = page("shipping.html", title="Shipping & Returns",
                desc="Shipping, returns and exchanges for online orders from Carreiro Studio Salon.",
                body=f'''<section class="page-head"><div class="wrap"><p class="eyebrow"><span class="asterism">❋</span> Shop</p><h1 class="h-xl">shipping <em>&amp; returns.</em></h1></div></section>
<section class="section--tight" style="padding-top:0"><div class="wrap"><div class="prose">{"".join(parts)}</div></div></section>''')
    return terms, ship


def build_404():
    body = f'''
<section class="section">
  <div class="wrap notfound">
    <p class="eyebrow"><span class="asterism">❋</span> Page not found</p>
    <h1 class="h-xl">this page has left <em>the gallery</em></h1>
    <p class="lede">The page you’re looking for has moved or no longer exists. Try the home page, or reserve your next visit.</p>
    <div class="btn-row"><a class="btn" href="/">Home</a><a class="btn btn--ghost" href="{BOOK_ANY}" data-reserve>Reserve</a></div>
  </div>
</section>'''
    return page("404.html", title="Page not found", desc="This page could not be found.", body=body, root_abs=True)


def build_meta():
    urls = ["", "our-story", "meet-the-team", "contact", "join", "news", "terms-conditions", "shipping"] + [
        f"news/{p['slug']}" for p in POSTS]
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    sm += "".join(f"  <url><loc>{SITE}/{u}</loc></url>\n" for u in urls)
    sm += "</urlset>\n"
    robots = f"User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n"
    retired = ["aveda-smooth-infusion-sale", "featuring-aro", "free-conditioning-treatment", "happy-new-year",
               "julys-mask-update", "k-water-treatment", "kerastase-nutritive-sale", "now-carrying-chronologiste",
               "operating-during-covid-19", "spring-giveaway"]
    lines = [
        "# Old Squarespace URLs -> new pages, so old links and search results keep working",
        "/about                 /meet-the-team   301",
        "/carreiro-locations    /contact         301",
        "/events                /news            301",
        "/events/*              /news            301",
        "/news/category/*       /news            301",
        f"/all                   {SHOP}   301",
        f"/shop                  {SHOP}   301",
        f"/cart                  {SHOP}   301",
        f"/gift-cards            {GIFT_CARDS}   301",
        f"/book                  {BOOK_ANY}   301",
    ] + [f"/news/{s}    /news    301" for s in retired]
    return sm, robots, "\n".join(lines) + "\n"


def main():
    files = {
        "index.html": build_home(),
        "our-story.html": build_story(),
        "meet-the-team.html": build_team(),
        "contact.html": build_contact(),
        "join.html": build_join(),
        "news.html": build_news(),
        "404.html": build_404(),
    }
    files["terms-conditions.html"], files["shipping.html"] = build_legal()
    for i, post in enumerate(POSTS):
        files[f"news/{post['slug']}.html"] = build_post(i, post)
    files["sitemap.xml"], files["robots.txt"], files["_redirects"] = build_meta()
    for rel, content in files.items():
        dest = OUT / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(content, encoding="utf-8")
    print(f"Built {len(files)} files into {OUT}")


if __name__ == "__main__":
    main()
