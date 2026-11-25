"""Render the site into plain HTML with Python's standard library."""
from hashlib import sha256
from html import escape
import json
from pathlib import Path
import re

from editorial import ART, GUIDES, ILLUSTRATIONS, STORIES

ROOT = Path(__file__).resolve().parents[1]
BRAND = "Charlotte’s Pet Podcast"
INTRO = "From hoof care at the barn to questions for the people who look after animals, come explore with Charlotte."
NAV = [("", "Home"), ("horse-care/", "Horse Care"), ("interviews/", "Interviews"), ("about/", "About Charlotte")]
PONY = "ponies-and-horses"
PORTRAIT = "Charlotte smiling on a brick porch while holding a poster and a shirt"


def prefix(route):
    return "../" * route.count("/")


def link(route, text, style="button secondary", label=None):
    accessible_name = f' aria-label="{escape(label, quote=True)}"' if label else ""
    return f'<a class="{style}" href="{escape(route or "./", quote=True)}"{accessible_name}>{escape(text)}</a>'


def figure(base, art, eager=False):
    filename, alt = ART[art]
    loading = "eager" if eager else "lazy"
    caption = "<figcaption>Illustrative artwork</figcaption>" if art in ILLUSTRATIONS else ""
    return (f'<figure class="art"><img src="{base}assets/art/{filename}" alt="{escape(alt)}" '
            f'width="1248" height="832" loading="{loading}" decoding="async">'
            f'{caption}</figure>')


def photo(base, name, alt, width, height, eager=False, css=""):
    return (
        f'<img class="{css}" src="{base}assets/photos/{name}.webp" alt="{escape(alt, quote=True)}" '
        f'width="{width}" height="{height}" loading="{"eager" if eager else "lazy"}" decoding="async">'
    )


def photo_card(name, alt, width, height, caption):
    return (
        f'<figure class="drive-photo">{photo("../", name, alt, width, height)}'
        f'<figcaption>{escape(caption)}</figcaption></figure>'
    )


def mark():
    return '<span class="paw" aria-hidden="true"><i></i><i></i><i></i><i></i><b></b></span>'


def asset_version(filename):
    return sha256((ROOT / "assets" / filename).read_bytes()).hexdigest()[:10]


def render(route, title, description, body, current=None, filename="index.html"):
    base = prefix(route)
    home = f"{base}index.html"
    current = route if current is None and filename == "index.html" else current
    active = ' aria-current="page"'
    nav = "\n".join(
        f'<a href="{base + path if path else home}"{active if path == current else ""}>{label}</a>'
        for path, label in NAV
    )
    full_title = BRAND if route == "" and filename == "index.html" else f"{title} | {BRAND}"
    error_metadata = ""
    error_script = ""
    if filename == "404.html":
        error_metadata = """<meta name="robots" content="noindex">
  <base href="/">
  <script>
    if (location.pathname.startsWith("/charlotte-pet-podcast/")) {
      document.querySelector("base").href = "/charlotte-pet-podcast/";
    }
  </script>"""
        error_script = '<script>document.querySelector(".skip").href = location.pathname + "#content";</script>'
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="{escape(description, quote=True)}">
  <title>{escape(full_title)}</title>
  {error_metadata}
  <link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="{base}assets/site.css?v={asset_version("site.css")}">
  <script src="{base}assets/site.js?v={asset_version("site.js")}" defer></script>
</head>
<body>
  <a class="skip" href="#content">Skip to content</a>
  {error_script}
  <header class="mast">
    <div class="wrap mast-inner">
      <a class="brand" href="{home}">{mark()}<span>Charlotte’s <strong>Pet Podcast</strong></span></a>
      <button class="nav-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu <span aria-hidden="true">☰</span></button>
      <nav id="site-nav" aria-label="Primary">
        {nav}
      </nav>
    </div>
  </header>
  <main id="content" tabindex="-1">
{body}
  </main>
  <footer class="footer">
    <div class="wrap footer-inner">
      <a class="brand" href="{home}">{mark()}<span>Charlotte’s <strong>Pet Podcast</strong></span></a>
      <nav aria-label="Explore more">
        {link(base + "stories/", "Animal stories", "footer-link")}
        {link(base + "places/", "Places", "footer-link")}
        {link(base + "lemonade/", "The Lemonade Society", "footer-link")}
      </nav>
    </div>
  </footer>
</body>
</html>
"""
    path = ROOT / route / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    html = "\n".join(line for line in html.splitlines() if line.strip()) + "\n"
    path.write_text(html, encoding="utf-8")


def heading(title, summary, label=None):
    eyebrow = f'<p class="eyebrow">{escape(label)}</p>' if label else ""
    return f'<header class="wrap page-head">{eyebrow}<h1>{escape(title)}</h1><p class="lede">{escape(summary)}</p></header>'


def story_cards(base, exclude=None, title_tag="h3", compact=False):
    cards = []
    for slug, story in STORIES.items():
        if slug == exclude:
            continue
        cards.append(f"""
        <article class="story-card">
          {figure(base, story["art"])}
          <div class="card-copy">
            <p class="eyebrow">{story["label"]}</p>
            <{title_tag}>{story["title"]}</{title_tag}>
            <p>{escape(story["summary"])}</p>
            {link(base + "stories/" + slug + "/", "View story", label="View story: " + story["title"])}
          </div>
        </article>""")
    layout = "story-grid compact-stories" if compact else "story-grid"
    return f'<div class="{layout}">' + "".join(cards) + '</div>'


def featured(base, title_tag="h3"):
    guide = GUIDES[PONY]
    return f"""
      <article class="feature">
        {figure(base, guide["art"])}
        <div>
          <p class="eyebrow">Featured guide</p>
          <{title_tag}>{guide["title"]}</{title_tag}>
          <p>{guide["summary"]}</p>
          {link(base + "horse-care/" + PONY + "/", "Read the guide", "button")}
        </div>
      </article>
"""


def homepage(episodes):
    playable = any(item["available"] for item in episodes)
    interview_copy = (
        "Watch Charlotte’s conversations at the barn and around the paddock."
        if playable else "Explore photos from Charlotte’s conversations at the barn and around the paddock."
    )
    body = f"""
    <section class="hero" aria-labelledby="hero-title">
      <div class="hero-photo">
        <img src="assets/charlotte-porch.jpg" alt="{PORTRAIT}" width="923" height="1230" fetchpriority="high">
      </div>
      <div class="wrap hero-inner">
        <div class="hero-copy">
          <p class="eyebrow">For curious animal lovers</p>
          <h1 id="hero-title">Big questions.<br><em>Little paws.</em></h1>
          <p class="lede">{INTRO}</p>
          <div class="actions">
            {link("horse-care/", "Explore horse care", "button")}
            {link("about/", "Meet Charlotte", "button secondary")}
          </div>
        </div>
      </div>
    </section>
    <section class="wrap section" aria-labelledby="horse-heading">
      <div class="section-head">
        <h2 id="horse-heading">Horse care</h2>
        {link("horse-care/", "All horse-care guides")}
      </div>
      {featured("")}
    </section>
    <section class="wrap section stories-section" aria-labelledby="stories-heading">
      <div class="section-head"><h2 id="stories-heading">Animal stories</h2>{link("stories/", "All stories")}</div>
      {story_cards("")}
    </section>
    <div class="wrap section home-panels">
      <section class="home-panel interview-panel" aria-labelledby="interviews-heading">
        {interview_cover("", episodes[0])}
        <div class="home-panel-copy">
          <h2 id="interviews-heading">Interviews</h2>
          <p>{interview_copy}</p>
          {link("interviews/", "Watch interviews" if playable else "Explore interviews", "button")}
        </div>
      </section>
      <section class="home-panel" aria-labelledby="about-heading">
        <h2 id="about-heading">A hello from Charlotte</h2>
        <p>Hi, I’m Charlotte. I love animals and I love asking questions.</p>
        {link("about/", "More about Charlotte")}
      </section>
    </div>
    {lemonade_feature("", "home-lemonade-title", "Charlotte co-founded a book club that picks and packs books to share with young readers.")}
"""
    render("", BRAND, INTRO, body)


def horse_care():
    summary = "Start with the everyday ways people care for horses, from brushing a coat to checking a hoof."
    topics = "".join(f"""
      <li>
        <h3>{guide["title"]}</h3>
        <p>{guide["summary"]}</p>
        {link(slug + "/", "Read guide", label="Read guide: " + guide["title"])}
      </li>"""
        for slug, guide in GUIDES.items() if slug != PONY)
    render("horse-care/", "Horse Care", summary, heading("Horse Care", summary) + f"""
    <section class="wrap library" aria-label="Horse-care guides">
      {featured("../", title_tag="h2")}
      <h2 id="everyday">Everyday care</h2>
      <ul class="topic-grid" aria-labelledby="everyday">{topics}</ul>
    </section>
""")


def guide_page(slug, item):
    contents = []
    sections = []
    for title, copy in item["sections"]:
        anchor = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
        contents.append(f'<li>{link("#" + anchor, title, "contents-link")}</li>')
        sections.append(f'<section id="{anchor}"><h2>{escape(title)}</h2><p>{escape(copy)}</p></section>')
    contents.append(f'<li>{link("#sources", "Further reading", "contents-link")}</li>')
    contents.append(f'<li>{link("#related", "More horse care", "contents-link")}</li>')
    sources = "".join(f'<li>{link(url, label, "source-link")}</li>' for label, url in item["sources"])
    more = "".join(
        f'<li>{link("../" + other + "/", guide["title"])}</li>'
        for other, guide in GUIDES.items() if other != slug
    )
    render(f"horse-care/{slug}/", item["title"], item["summary"], f"""
    <article class="wrap reading">
      <header class="article-head">
        <p class="eyebrow">Horse-care guide</p>
        <h1>{item["title"]}</h1>
        <p class="lede">{item["summary"]}</p>
      </header>
      <div class="reading-grid">
        <nav class="contents" aria-labelledby="contents-heading">
          <h2 id="contents-heading">On this page</h2>
          <ul>{"".join(contents)}</ul>
        </nav>
        <div class="prose">
          {"".join(sections)}
          <aside class="sources" aria-labelledby="sources"><h2 id="sources">Further reading</h2><ul>{sources}</ul></aside>
          <section class="related" aria-labelledby="related"><h2 id="related">More horse care</h2><ul class="related-links">{more}</ul></section>
        </div>
        <aside class="reading-aside" aria-label="Article resources">
          {figure("../../", item["art"], eager=True)}
          <div class="reading-question"><h2>Something to think about</h2><p>{escape(item["question"])}</p></div>
          {link("../", "All horse-care guides")}
        </aside>
      </div>
    </article>
""", current="horse-care/")


def story_page(slug, item):
    title, paragraph = item["body"]
    body_anchor = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")
    question_anchor, questions = item["questions"]
    question_list = "".join(f"<li>{escape(question)}</li>" for question in questions)
    render(f"stories/{slug}/", item["title"], item["summary"], f"""
    <article class="wrap story-page">
      <div class="story-opening">
        <header>
          <p class="eyebrow">{escape(item["label"])}</p>
          <h1>{escape(item["title"])}</h1>
          <p class="lede">{escape(item["summary"])}</p>
          {link("../", "All animal stories")}
        </header>
        {figure("../../", item["art"], eager=True)}
      </div>
      <div class="story-reading">
        <section id="{body_anchor}"><h2>{escape(title)}</h2><p>{escape(paragraph)}</p></section>
        <section class="story-questions" id="{question_anchor}">
          <h2>What Charlotte wonders</h2>
          <ul>{question_list}</ul>
        </section>
      </div>
      <section class="related story-related" aria-labelledby="related">
        <h2 id="related">More animal stories</h2>
        {story_cards("../../", exclude=slug, compact=True)}
      </section>
    </article>
""")


def interview_media(item, extension):
    return f'assets/video/interview-{item["slug"]}.{extension}'


def interview_entries():
    entries = json.loads((ROOT / "scripts/interviews.json").read_text(encoding="utf-8"))
    for entry in entries:
        media = ROOT / interview_media(entry, "mp4")
        entry["available"] = media.is_file() and media.stat().st_size > 0
    return entries


def interview_cover(base, item, eager=False):
    return photo(base, "interview-" + item["slug"], item["coverAlt"], 848, 480, eager, "interview-cover")


def interview_card(item, featured=False):
    title = item["title"]
    cls = "interview-card interview-featured" if featured else "interview-card"
    destination = item["slug"] + "/"
    cover = interview_cover("../", item, eager=True)
    if item["available"]:
        cover = f'<a class="interview-cover-link" href="{destination}" aria-label="{escape("Watch interview: " + title, quote=True)}">{cover}</a>'
    duration = item.get("duration")
    length = f'<p class="video-length">{escape(duration)}</p>' if duration and item["available"] else ""
    action = (
        link(destination, "Watch interview", "button", label="Watch interview: " + title)
        if item["available"] else '<p class="status">Video pending</p>'
    )
    return f"""
      <article class="{cls}">
        {cover}
        <div class="interview-copy">
          <h2>{escape(title)}</h2>
          {length}
          <p class="interview-description">{escape(item["description"])}</p>
          {action}
        </div>
      </article>"""


def interviews(episodes):
    summary = "Join Charlotte for three conversations, starting inside the barn and continuing outdoors by the paddock."
    cards = "".join(interview_card(item, featured=index == 0) for index, item in enumerate(episodes))
    render("interviews/", "Interviews", summary, heading("Interviews", summary) + f"""
    <section class="wrap library interview-list" aria-label="Interview collection">
      {cards}
    </section>
""")
    for item in episodes:
        if item["available"]:
            interview_page(item)


def interview_page(item):
    title = item["title"]
    base = "../../"
    source = interview_media(item, "mp4")
    captions = interview_media(item, "vtt")
    track = (
        f'<track kind="captions" src="{base}{captions}" srclang="en" label="English">'
        if (ROOT / captions).is_file() else ""
    )
    render(f'interviews/{item["slug"]}/', title, title, f"""
    <article class="wrap section video-page">
      <h1 id="video-title">{escape(title)}</h1>
      <video controls playsinline preload="none" width="848" height="480"
             poster="{base}assets/photos/interview-{item["slug"]}.webp" aria-labelledby="video-title">
        <source src="{base}{source}" type="video/mp4">
        {track}
        {link(base + source, "Open the MP4", "source-link")}
      </video>
      {link("../", "All interviews")}
    </article>
""", current="interviews/")


def lemonade_feature(base, heading_id, description, anchor=""):
    return f"""
    <section class="wrap section feature charity lemonade-feature"{anchor} aria-labelledby="{heading_id}">
      {photo(base, "book-drive-display", "Two young volunteers beside a display of children’s books", 1440, 1080)}
      <div>
        <h2 id="{heading_id}">The Lemonade Society</h2>
        <p>{escape(description)}</p>
        {link(base + "lemonade/", "Explore The Lemonade Society")}
      </div>
    </section>"""


def about():
    hello = "Hi, I’m Charlotte. I love animals and I love asking questions."
    render("about/", "About Charlotte", hello, f"""
    <section class="wrap about-intro">
      <div>
        <h1>About Charlotte</h1>
        <p class="lede">{hello}</p>
        <p>I’m curious about horses and what it takes to look after them. I also want to meet people who work with animals and hear what their days are like, whether they’re at a barn, a zoo, or a vet’s office.</p>
        <p>I share animal stories and interviews here as I learn more.</p>
        <div class="actions">
          {link("#charlottes-stories", "Explore my stories", "button")}
          {link("../interviews/", "Watch interviews")}
        </div>
      </div>
      <figure class="about-photo">{photo("../", "book-drive-about", "Charlotte in a Lemonade Society shirt beside stacks of book boxes", 1080, 1440, eager=True)}<figcaption>Charlotte beside book boxes at a Lemonade Society book drive.</figcaption></figure>
    </section>
    <section class="wrap section" aria-labelledby="charlottes-stories">
      <div class="section-head"><h2 id="charlottes-stories">My animal stories</h2></div>
      {story_cards("../", compact=True)}
    </section>
    {lemonade_feature("../", "lemonade-heading", "I co-founded The Lemonade Society with Hendrik. Come see how we choose and pack books to share with young readers.", anchor=' id="lemonade-society"')}
""")


def lemonade():
    summary = "A book club that reads together and shares books with young readers."
    packing = photo_card(
        "book-drive-books", "Children’s books resting on cardboard boxes in a bookstore aisle",
        1440, 1080, "Books and boxes in the bookstore aisle."
    )
    pickup = photo_card(
        "book-drive-pickup", "Two young volunteers stand behind a cart of book boxes outside a bookstore",
        1080, 1440, "Boxes of books ready for pickup outside the bookstore."
    )
    render("lemonade/", "The Lemonade Society", summary, f"""
    <section class="wrap section drive-lead" aria-labelledby="drive-title">
      <div>
        <h1 id="drive-title">The Lemonade Society</h1>
        <p class="lede">{summary}</p>
        <p>Charlotte and Hendrik co-founded The Lemonade Society in the Washington, DC area. It’s part of The LiTEArary Society, Inc., which helps preschool-age children in underserved communities discover a love of books.</p>
        <p>At book club, members read and talk about books, make things, and choose and prepare new books to donate. A parent or caregiver supervises each meeting.</p>
        {link("https://www.liteararysociety.org/the-lemonade-society", "Visit The Lemonade Society’s page")}
      </div>
      <figure class="drive-photo">
        {photo("../", "book-drive-display", "Two young volunteers in Lemonade Society shirts flank a display of children’s books", 1440, 1080, eager=True)}
        <figcaption>A book-drive display with children’s books.</figcaption>
      </figure>
    </section>
    <section class="wrap section" aria-labelledby="drive-gallery-title">
      <div class="section-head"><h2 id="drive-gallery-title">Packing and pickup</h2></div>
      <div class="drive-grid">{packing}{pickup}</div>
    </section>
""")


def secondary_pages():
    subtitle = "From the barn to the National Zoo to three puppies at home."
    render("stories/", "Animal stories", subtitle, heading("Animal stories", subtitle) +
           f'<section class="wrap library" aria-label="Stories">{story_cards("../", title_tag="h2")}</section>')
    places = [("barn", "At the barn", "martha-wunder"), ("zoo", "The National Zoo", "baby-elephant"),
              ("home", "At home", "puppies")]
    rows = "".join(f"""
      <article class="feature" id="{anchor}">
        {figure("../", STORIES[slug]["art"])}
        <div><h2>{title}</h2><p>{STORIES[slug]["summary"]}</p>
        {link("../stories/" + slug + "/", "View story", label="View story: " + STORIES[slug]["title"])}</div>
      </article>""" for anchor, title, slug in places)
    summary = "The barn, the zoo, and home. Each place leads to one of Charlotte’s animal stories."
    render("places/", "Places", summary, heading("Places", summary) + f'<div class="wrap library place-list">{rows}</div>')
    render("", "Page not found", "This page could not be found.", heading("Page not found", "Find your way back to Charlotte’s homepage.") +
           f'<div class="wrap library">{link("index.html", "Back to home", "button")}</div>', current=None, filename="404.html")


if __name__ == "__main__":
    episodes = interview_entries()
    homepage(episodes)
    horse_care()
    interviews(episodes)
    about()
    lemonade()
    secondary_pages()
    for slug, guide in GUIDES.items():
        guide_page(slug, guide)
    for slug, story in STORIES.items():
        story_page(slug, story)
