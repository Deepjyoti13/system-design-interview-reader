# System Design Interview — Reader

A single-file reading shell for the *System Design Interview* chapter pages: one index, a
persistent table of contents, search, progress tracking, and keyboard navigation, instead of
31 loose `.html` files in a folder.

**[▶ Open the live reader](https://deepjyoti13.github.io/system-design-interview-reader/)**

> **No book content is included in this repository.** The chapters are a paid commercial
> product by [ByteByteGo](https://bytebytego.com) (Alex Xu) and are not mine to redistribute.
> This repo contains only `index.html` — the reader — which is why the live demo shows the
> interface with every chapter link broken. To actually read anything, point it at your own
> legally obtained copies (see below).

## What it does

- **Library home** — every chapter as a card, grouped into Start Here / Foundations /
  Volume 1 / Volume 2 / Wrap Up.
- **Reader** — the chapter renders in-frame beside a table of contents that never scrolls away.
- **Search** — filter by title, chapter number, or section. `/` focuses the box, `Enter` opens
  the first match.
- **Progress** — mark chapters read; the count, the bar, and the card states persist in
  `localStorage`.
- **Resume** — the primary button remembers the last chapter you opened.
- **Keyboard** — `←` / `→` between chapters, `Esc` back to the library, `/` to search.
- **Deep links** — `index.html#ch=14` opens chapter 14 directly.
- Light and dark themes (follows the OS by default), responsive down to phone width.

No build step, no dependencies, no network calls. One HTML file.

## Using it with your own copy

Put `index.html` in the same folder as your chapter files and open it in a browser. The reader
resolves each chapter by filename, so the names have to match exactly:

```
0. Foreword.html
1. Join the Community.html
2. Scale From Zero To Millions Of Users.html
3. Back-of-the-envelope Estimation.html
4. A Framework For System Design Interviews.html
5. Design A Rate Limiter.html
6. Design Consistent Hashing.html
7. Design A Key-value Store.html
8. Design A Unique ID Generator In Distributed Systems.html
9. Design A URL Shortener.html
10. Design A Web Crawler.html
11. Design A Notification System.html
12. Design A News Feed System.html
13. Design A Chat System.html
14. Design A Search Autocomplete System.html
15. Design YouTube.html
16. Design Google Drive.html
17. Proximity Service.html
18. Nearby Friends.html
19. Google Maps.html
20. Distributed Message Queue.html
21. Metrics Monitoring and Alerting System.html
22. Ad Click Event Aggregation.html
23. Hotel Reservation System.html
24. Distributed Email Service.html
25. S3-like Object Storage.html
26. Real-time Gaming Leaderboard.html
27. Payment System.html
28. Digital Wallet.html
29. Stock Exchange.html
30. The Learning Continues.html
```

If a chapter fails to load, the reader says so and offers to open the file directly. Two
things cause that: the file isn't in the folder, or the browser is refusing to embed one local
file inside another. Chrome and Firefox handle local embedding fine; Safari is stricter — use
the *New tab* button there, or serve the folder over HTTP:

```sh
python3 -m http.server 8000   # then visit http://localhost:8000
```

## Adapting it to another book

The chapter list is one array near the top of the `<script>` block:

```js
var CHAPTERS = [
  { n: 0, t: "Foreword", g: "Start Here" },
  ...
];
```

`n` is the chapter number, `t` the title, `g` the sidebar group. Filenames are derived as
`n + ". " + t + ".html"`. Change the array and the whole interface follows.

## License

Reader code: [MIT](LICENSE). The book it is designed to display is not covered by that license
and is not distributed here.
