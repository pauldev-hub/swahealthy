# base.html — One Line Change Only
**File location:** `templates/base.html`

Only change the Google Fonts `<link>` tag. Find this line:

```html
<link
    href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Noto+Sans+Bengali:wght@400;600;700&family=Noto+Sans+Devanagari:wght@400;600;700&display=swap"
    rel="stylesheet">
```

Replace it with:

```html
<link
    href="https://fonts.googleapis.com/css2?family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600;9..40,700&family=Noto+Sans+Bengali:wght@400;500;600&family=Noto+Sans+Devanagari:wght@400;500;600&display=swap"
    rel="stylesheet">
```

Also change the theme color meta tag from:
```html
<meta name="theme-color" content="#1D6A96">
```
To:
```html
<meta name="theme-color" content="#0D9488">
```

**That's it. Everything else in base.html stays exactly the same.**
