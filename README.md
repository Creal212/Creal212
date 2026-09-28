<!-- Original vector illustrations: assets/atlas. Essential content stays in native Markdown. -->

[Portfolio ↗](https://www.creal589.dev/) · [Résumé ↗](https://www.creal589.dev/resume) · [LinkedIn ↗](https://www.linkedin.com/in/creal212/) · [Email ↗](mailto:tommyfodaykailie@gmail.com)

<picture>
  <source media="(prefers-color-scheme: dark) and (max-width: 640px)" srcset="assets/atlas/cover-mobile-dark.svg">
  <source media="(max-width: 640px)" srcset="assets/atlas/cover-mobile.svg">
  <source media="(prefers-color-scheme: dark)" srcset="assets/atlas/cover-dark.svg">
  <img src="assets/atlas/cover.svg" alt="The Engineer’s Atlas. Ideas, made operational. An illustrated cutaway connects the interface, services, and data behind a product." width="100%">
</picture>

# Cyril Foday-Kailie

**Software engineer · Full-stack products · AI systems · Product design**<br>St. Paul, Minnesota · B.S. Computer Science, Metropolitan State University

I turn complicated systems into products people can understand and use. My work connects the visible details—interfaces, typography, interaction—with the machinery underneath: APIs, data pipelines, desktop tooling, and AI workflows.

**Open to software engineering roles.**

---

## The collection

Four products. Four different problems. One thread: **design the experience and the system together.**

[01 — Sign](#01--dev-autographs) · [02 — Understand](#02--the-book-of-blocks) · [03 — Build](#03--imperium) · [04 — Navigate](#04--world-trade-factory)

### 01 / Dev Autographs

<a href="https://www.devautographs.com/">
  <img src="assets/atlas/dev-autograph.svg" alt="Dev Autographs: an engraved signature flows into a cryptographic seal. Open the product." width="100%">
</a>

**A signature for the files you ship.**<br>A Windows app, CLI, and web desk connect Git workflows to cryptographic file signatures and public records. The optional <kbd>Shift</kbd> + <kbd>D</kbd> report brings those records into a website without adding a permanent badge.

`Tauri` `Node.js` `Git hooks` `Ed25519` `SHA-256` · **Early access**

[Explore the product ↗](https://www.devautographs.com/) · [Open the web desk ↗](https://www.devautographs.com/desk.html) · [Case study ↗](https://www.creal589.dev/my-projects/dev-autographs) · [Releases ↗](https://github.com/Creal212/Dev-Autographs-Installer/releases)

<details>
<summary><strong>Inside the mechanism</strong> — from a commit to an inspectable record</summary>

Enabled hooks sign staged file bytes and their recorded context. Publishing happens on push; website embedding is a separate opt-in. Private signing keys stay on the developer’s machine, and the registry receives fingerprints and signed records rather than source code.

The report checks the supplied file signatures and registry status. The design challenge is making that evidence understandable without interrupting the product around it.

</details>

<br>

### 02 / The Book of Blocks

<a href="https://www.bookofblocks.xyz/">
  <img src="assets/atlas/book-of-blocks.svg" alt="The Book of Blocks: a landscape of stacked blocks becomes a market instrument. Open the live project." width="100%">
</a>

**A reading room with a market observatory next door.**<br>Chaptered crypto guides, live rankings, price charts, and source notes share one reading experience. The project brings editorial structure to a subject that rarely slows down.

`Next.js` `React` `Supabase Realtime` `TradingView Lightweight Charts`

[Enter the observatory ↗](https://www.bookofblocks.xyz/) · [Case study ↗](https://www.creal589.dev/my-projects/book-of-blocks)

<details>
<summary><strong>Inside the mechanism</strong> — give moving data a readable home</summary>

The interface has two jobs: explain a project and show what its market is doing. Chapter navigation serves the first; rankings, charts, source notes, and visible timestamps serve the second.

The engineering work connects the reading experience to market ingestion, storage, and realtime updates. Data freshness belongs in the experience, alongside the numbers themselves.

</details>

<br>

### 03 / I.M.P.E.R.I.U.M

<a href="https://www.imperium589.world/">
  <img src="assets/atlas/imperium.svg" alt="I.M.P.E.R.I.U.M: an exploded workbench illustrates the path from a project clone through review to Main. Open the product." width="100%">
</a>

**From a conversation to a reviewed change.**<br>An AI desktop workspace for planning, building in a project clone, and reviewing patches before they reach Main. Local and connected model workflows share a deliberate human review boundary.

`Tauri` `Rust` `React` `TypeScript` `SQLite` · **Early access**

[Visit the workbench ↗](https://www.imperium589.world/) · [Case study ↗](https://www.creal589.dev/my-projects/imperium) · [Installer repository ↗](https://github.com/Creal212/I.M.P.E.R.I.U.M-Installer-Early-Access-)

<details>
<summary><strong>Inside the mechanism</strong> — make the approval boundary visible</summary>

Blueprint is the planning space. A project clone is the working space. Reviewed patches are the path back to Main.

That separation shapes both the architecture and the interface: model output needs to become a concrete change a person can inspect and approve. The desktop experience brings together model connections, project files, and the review workflow.

</details>

<br>

### 04 / World Trade Factory

<a href="https://wtf-trading-interface.vercel.app/">
  <img src="assets/atlas/world-trade-factory.svg" alt="World Trade Factory: a calibrated market console puts charts and controls around a central instrument. Open the live interface." width="100%">
</a>

**A market desk built around moving information.**<br>Live feeds, price charts, and wallet connections meet in a responsive workspace. The layout moves from a desktop trading desk to focused mobile views.

`Next.js` `React` `Recharts` `WebSockets` `ethers.js` · **Live interface · Integrations in progress**

[Explore the interface ↗](https://wtf-trading-interface.vercel.app/) · [Case study ↗](https://www.creal589.dev/my-projects/wtf)

<details>
<summary><strong>Inside the mechanism</strong> — density without losing direction</summary>

Markets, charts, and trading controls need a clear hierarchy when everything is changing at once. The case study follows those layout decisions across desktop and mobile, alongside live market feeds and wallet integrations.

Execution and settlement integrations remain in progress. Saved trading rules currently live in the browser.

</details>

<br>

**Also on the bench — [RevOps Data Sync ↗](https://github.com/Creal212/revops-data-sync)**<br>A compact data engineering project: mock CRM, support, and product data move through Python ingestion and SQL cleanup into a PostgreSQL account-health mart and a Metabase dashboard.<br>`Python` `SQL` `PostgreSQL` `Metabase` `Docker`

---

## The working practice

**Start with the person using it.** Give complex information a clear hierarchy, useful feedback, and a deliberate interaction model.

**Make the boundaries visible.** Show what the data describes, what an AI can change, and where a human decision belongs.

**Follow the feature all the way down.** Treat the interface, API, storage, and deployment as parts of the same product.

<details>
<summary><strong>Tools behind the work</strong></summary>

- **Interfaces:** TypeScript, JavaScript, React, Next.js, Tailwind CSS.
- **Data and services:** Python, Node.js, PostgreSQL, Supabase, SQL.
- **Desktop and AI workflows:** Tauri, Rust, SQLite, local and connected models.
- **Delivery:** Git, Docker, Vercel, Railway.

The project links above show where these tools are used and the decisions behind them.

</details>

<details>
<summary><strong>In the margins</strong> — there is still room to play</summary>

Careful engineering. A little anime. Always another idea on the bench.

<img src="assets/chop.gif" alt="Chopper from One Piece, an animated nod to the original profile." width="160">

</details>

<br>

<a href="https://www.creal589.dev/contact-me">
  <img src="assets/atlas/colophon.svg" alt="The next page is unwritten. Let’s build it. Contact Cyril." width="100%">
</a>

**Looking for someone who cares how it works and how it feels?**<br>I’m open to software engineering roles and thoughtful conversations about building useful products.

[Read my résumé ↗](https://www.creal589.dev/resume) · [Explore the portfolio ↗](https://www.creal589.dev/) · [Get in touch ↗](mailto:tommyfodaykailie@gmail.com)

<sub>Designed as an engineer’s atlas. Illustrated as product specimens. Built to be explored.</sub>
