# Adeola Mary — Portfolio Website

Five-page portfolio site for Adeola Mary, Executive Virtual Assistant and Social Media Manager.

Pages: `index.html` (Home), `about.html`, `services.html`, `portfolio.html`, `contact.html`.
It is plain HTML, CSS and JavaScript, so there is nothing to install or build.

## Put it online with GitHub Pages

1. Create a new repository on GitHub, for example `adeolamary-portfolio`.
2. Click **Add file → Upload files** and drag in everything from this folder (keep the `assets` folder as is).
3. Click **Commit changes**.
4. Go to **Settings → Pages**, set **Source** to *Deploy from a branch*, choose `main` and `/ (root)`, and click **Save**.
5. After a minute the site is live at `https://YOUR-USERNAME.github.io/adeolamary-portfolio/`.

## Contact form

The form uses FormSubmit (formsubmit.co), which is free, needs no account and works on GitHub Pages.
Messages are emailed to adeolamary703@gmail.com.

**One-time activation:** after the site is live, send one test message through the contact page.
FormSubmit then emails adeolamary703@gmail.com an activation link (check Spam too). Click it once,
and every message after that goes straight to the inbox.

## Editing the content

All text, services, projects and contact details live in `_build/build.py`.
Edit that file, then run:

```bash
python3 _build/build.py
```

This regenerates the five HTML pages. Styles are in `assets/css/style.css`, scripts in `assets/js/main.js`, and images in `assets/img/`.
