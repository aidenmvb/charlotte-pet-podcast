# Charlotte’s Pet Podcast

This is a static HTML, CSS, and JavaScript site. There are no dependencies to install.

## Run locally

From the project directory, start the server:

```sh
python3 -B scripts/serve.py
```

Open <http://localhost:5500/>. Stop the server with Ctrl+C.

## Edit the site

The checked-in HTML is ready to serve. The Python 3.9+ generator keeps navigation, layouts, and repeated content in sync. Edit `scripts/build.py` for layout and standalone pages, `scripts/editorial.py` for animal stories, guide copy, and artwork, and `assets/site.css` for styling. Regenerate the HTML from the project directory:

```sh
python3 -B scripts/build.py
```

Keep each existing story slug so bookmarks and shared links continue to work. Places remains a secondary index. The Lemonade Society has a dedicated page at `/lemonade/`.

## Add an interview

Add the title, slug and cover alt text to `scripts/interviews.json`. Save the prepared cover as `assets/photos/interview-<slug>.webp` and the edited recording as `assets/video/interview-<slug>.mp4`. Add a `duration` such as `"2:34"` after checking the actual export. If an English caption file has been reviewed against the audio, save it beside the recording as `interview-<slug>.vtt`.

Rebuild the site. An interview without its MP4 displays its cover and a pending status. With its MP4 in place, the card links to a local player with standard controls and playback starts on request.

## Private editorial checklist

- Preserve the real photo in `assets/charlotte-porch.jpg`. Check the hero crop on a phone and laptop if it changes.
- Replace the illustrated horse in `assets/art/horse-barn.jpg` with an approved photo for the Crispy story. Update the caption and alt text to match the actual subject.
- Replace `assets/art/baby-elephant.jpg` and `assets/art/puppies.jpg` with approved photos when available. Add names, dates, or details only after Charlotte confirms them.
- The horse-care feature (`pony-and-horse-pasture.jpg`) uses temporary artwork. Their filenames and alt text live in `ART` in `scripts/editorial.py`. For a real photograph, update its alt text and remove the corresponding key from `ILLUSTRATIONS` so the illustration caption disappears.
- Use a landscape 3:2 crop for cards and serve compressed JPEG or WebP files. Rebuild after updating paths and check desktop and phone crops.
- Add Charlotte’s original story write-ups as they’re ready. Update the Martha Wunder story status once there is a confirmed, publishable conversation. Add the first interview through the data file when a real recording is available.
