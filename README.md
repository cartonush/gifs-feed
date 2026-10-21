# LOOP — RedGIFs random feed

Reels-style RedGIFs feed for `cartonush/gifs-feed`. The app reads usernames from the extensionless `users` file, likes from `liked`, viewed random-feed history from `seen`, and clip metadata from `catalog.json`.

## First setup

1. Add RedGIFs usernames or profile URLs to `users`.
2. In **Settings → Pages**, select **Deploy from a branch**, branch `main`, folder `/ (root)`, and save. The site will be available at `https://cartonush.github.io/gifs-feed/`.
3. Open **Actions → Refresh RedGIFs catalog → Run workflow** once. The catalog then refreshes every six hours and when `users` changes.
4. Open the site. It can read the public files without a token. To commit likes and viewed history to the repo, open ⚙ and enter a fine-grained GitHub token restricted to this repo with **Contents: Read and write**. The token remains in tab memory and is discarded when the tab closes.

## Users file format

`users` accepts a JSON list of usernames or profile URLs. It starts empty:

```json
[
  "https://www.redgifs.com/users/example",
  "another_user"
]
```

The refresh workflow fetches up to five recent pages (up to 500 clips) per profile. RedGIFs' v2 API is undocumented and may change, so the workflow may need adjustment if RedGIFs changes its interface.
