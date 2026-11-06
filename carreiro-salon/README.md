# Carreiro Studio Salon website

The redesign of carreirosalon.com. It is a static site with no framework and no monthly platform fee, and it's ready to deploy.

```
carreiro-salon/
├── build.py          # all page content + the shared header/footer; run to regenerate public/
├── content/legal.json# Terms & Shipping text carried over from the old site
├── netlify.toml      # hosting config (publish dir, caching)
└── public/           # the finished website: upload this folder
    ├── index.html, our-story.html, meet-the-team.html, contact.html, join.html, news.html
    ├── news/*.html   # 10 news posts
    ├── terms-conditions.html, shipping.html, 404.html
    ├── _redirects    # old Squarespace URLs -> new pages
    ├── sitemap.xml, robots.txt
    └── assets/       # css, js, optimized images, the original logo (unchanged)
```

## Edit and rebuild

All copy, prices, hours, team members and news posts live at the top of `build.py`.

```bash
python3 build.py
```

## Launch checklist

1. **Deploy.** In Netlify, use "Add new site" and import this repo with base directory `carreiro-salon`, or drag the `public/` folder onto app.netlify.com/drop.
2. **Point the domain.** Add `carreirosalon.com` in Netlify → Domain settings, then update the DNS records where the domain is registered (this moves it off Squarespace).
3. **Newsletter.** Sign-ups go to Netlify Forms (Site → Forms → "newsletter"). Export them to your email tool or add a Netlify notification.
4. **Check the booking links.** "Reserve" opens a Broadmead / Duncan chooser that links to your Zenoti booking pages. Gift cards and Shop also go to Zenoti.
5. **Google.** Both existing Google site-verification tags are kept. Submit `https://carreirosalon.com/sitemap.xml` in Search Console after launch.

Page URLs match the old site (`/our-story`, `/meet-the-team`, `/contact`, `/join`, `/news/...`), and `_redirects` covers the rest, so existing links and search rankings carry over.
