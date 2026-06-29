const USERNAME_PATTERN = /^[A-Za-z0-9._-]{1,40}$/;

const STATUS_META = {
  available: { label: "Available", cls: "is-available" },
  taken: { label: "Taken", cls: "is-taken" },
  unsure: { label: "Unsure", cls: "is-unsure" },
  error: { label: "Error", cls: "is-error" },
};

const ICON_SLUGS = {
  YouTube: "youtube",
  WordPress: "wordpress",
  X: "x",
  Facebook: "facebook",
  Instagram: "instagram",
  GitHub: "github",
  Reddit: "reddit",
  LinkedIn: "linkedin",
  Pinterest: "pinterest",
  Tumblr: "tumblr",
  TikTok: "tiktok",
  Twitch: "twitch",
  Medium: "medium",
  Vimeo: "vimeo",
  DeviantArt: "deviantart",
  SoundCloud: "soundcloud",
  Flickr: "flickr",
  Dribbble: "dribbble",
  Slack: "slack",
  Blogger: "blogger",
  GitLab: "gitlab",
  Telegram: "telegram",
  Patreon: "patreon",
  Behance: "behance",
  CodePen: "codepen",
  Replit: "replit",
  Steam: "steam",
  Bandcamp: "bandcamp",
  Kick: "kick",
  Threads: "threads",
  Spotify: "spotify",
  Snapchat: "snapchat",
  Gravatar: "gravatar",
  Quora: "quora",
  ProductHunt: "producthunt",
  Etsy: "etsy",
  Bluesky: "bluesky",
  LastFM: "lastdotfm",
  "Ko-fi": "kofi",
  BuyMeACoffee: "buymeacoffee",
  Gumroad: "gumroad",
  "Itch.io": "itchdotio",
  DevTo: "devdotto",
  Hashnode: "hashnode",
  Substack: "substack",
  Mixcloud: "mixcloud",
  VK: "vk",
  Letterboxd: "letterboxd",
  "Chess.com": "chessdotcom",
  Keybase: "keybase",
  Fiverr: "fiverr",
  Freelancer: "freelancer",
  "About.me": "aboutdotme",
  Disqus: "disqus",
  Trakt: "trakt",
  Newgrounds: "newgrounds",
  Wattpad: "wattpad",
  Giphy: "giphy",
  Codeberg: "codeberg",
  Bitbucket: "bitbucket",
  SourceForge: "sourceforge",
  npm: "npm",
  PyPI: "pypi",
  "Docker Hub": "docker",
  Kaggle: "kaggle",
  HackerRank: "hackerrank",
  LeetCode: "leetcode",
  Codewars: "codewars",
  freeCodeCamp: "freecodecamp",
  CodeChef: "codechef",
  Codeforces: "codeforces",
  Imgur: "imgur",
  "500px": "500px",
  Unsplash: "unsplash",
  ArtStation: "artstation",
  Foursquare: "foursquare",
  Untappd: "untappd",
  Myspace: "myspace",
  Lichess: "lichess",
  Wikipedia: "wikipedia",
  Weibo: "sinaweibo",
  Douban: "douban",
  Odnoklassniki: "odnoklassniki",
  Xing: "xing",
  Linktree: "linktree",
  Venmo: "venmo",
  PayPal: "paypal",
  Liberapay: "liberapay",
  "Open Collective": "opencollective",
  Genius: "genius",
  Discogs: "discogs",
  Trello: "trello",
  Figma: "figma",
  "Hacker News": "ycombinator",
  Glitch: "glitch",
  CodeSandbox: "codesandbox",
  Launchpad: "launchpad",
  RubyGems: "rubygems",
  GameJolt: "gamejolt",
  Wellfound: "wellfound",
};

const form = document.getElementById("username-form");
const input = document.getElementById("username");
const button = form.querySelector("button[type='submit']");
const buttonLabel = button.querySelector(".btn-label");
const fieldHelp = document.getElementById("username-help");
const select = document.getElementById("all-previous-usernames");
const summaryEl = document.getElementById("results-summary");
const usernameDisplay = document.getElementById("username-display");
const summaryCount = document.getElementById("summary-count");
const progressBar = document.getElementById("progress-bar");
const filtersEl = document.getElementById("filters");
const grid = document.getElementById("results-grid");
const emptyEl = document.getElementById("empty-state");
const toastContainer = document.getElementById("toast-container");

let savedEntries = [];
let activeFilter = "all";
let lastRendered = null;

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text !== undefined) node.textContent = text;
  return node;
}

function normalizeStatus(raw) {
  if (!raw) return "unsure";
  const s = String(raw).toLowerCase();
  if (s === "available") return "available";
  if (s === "taken") return "taken";
  if (s.includes("error")) return "error";
  return "unsure";
}

function platformIcon(site) {
  const wrap = el("div", "platform-icon");
  const slug = ICON_SLUGS[site];
  const monogram = () => {
    wrap.textContent = site.charAt(0).toUpperCase();
  };
  if (slug) {
    const img = new Image(22, 22);
    img.alt = "";
    img.loading = "lazy";
    img.addEventListener("error", monogram);
    img.src = "https://cdn.simpleicons.org/" + slug;
    wrap.appendChild(img);
  } else {
    monogram();
  }
  return wrap;
}

function statusBadge(status) {
  const meta = STATUS_META[status] || STATUS_META.unsure;
  const badge = el("span", "badge " + meta.cls);
  badge.appendChild(el("span", "badge-dot"));
  badge.appendChild(document.createTextNode(meta.label));
  return badge;
}

function buildCard(site, info) {
  const status = normalizeStatus(info && info.status);
  const url = status === "taken" && info && info.url ? info.url : null;
  const card = el(url ? "a" : "div", "card");
  card.dataset.status = status;
  if (url) {
    card.href = url;
    card.target = "_blank";
    card.rel = "noopener noreferrer";
    card.classList.add("is-link");
    card.setAttribute("aria-label", site + ": taken — open profile");
  }
  card.appendChild(platformIcon(site));
  const body = el("div", "card-body");
  body.appendChild(el("span", "card-name", site));
  body.appendChild(statusBadge(status));
  card.appendChild(body);
  if (url) card.appendChild(el("span", "card-go", "↗"));
  return card;
}

function renderFilters(counts, total) {
  filtersEl.innerHTML = "";
  const defs = [
    ["all", "All", total],
    ["available", "Available", counts.available],
    ["taken", "Taken", counts.taken],
    ["unsure", "Unsure", counts.unsure],
    ["error", "Error", counts.error],
  ];
  defs.forEach(function (def) {
    const key = def[0];
    const count = def[2];
    if (key !== "all" && count === 0) return;
    const chip = el("button", "chip", def[1]);
    chip.type = "button";
    chip.dataset.filter = key;
    chip.appendChild(el("span", "chip-count", String(count)));
    if (key === activeFilter) chip.classList.add("is-active");
    chip.addEventListener("click", function () {
      activeFilter = key;
      filtersEl.querySelectorAll(".chip").forEach(function (c) {
        c.classList.toggle("is-active", c.dataset.filter === key);
      });
      applyFilter();
    });
    filtersEl.appendChild(chip);
  });
}

function applyFilter() {
  grid.querySelectorAll(".card").forEach(function (card) {
    const show = activeFilter === "all" || card.dataset.status === activeFilter;
    card.classList.toggle("is-hidden", !show);
  });
}

function renderResults(username, resultsObj) {
  lastRendered = { username: username, results: resultsObj };
  activeFilter = "all";

  const sites = Object.keys(resultsObj);
  const counts = { available: 0, taken: 0, unsure: 0, error: 0 };
  sites.forEach(function (site) {
    counts[normalizeStatus(resultsObj[site] && resultsObj[site].status)]++;
  });
  const total = sites.length;

  usernameDisplay.textContent = "Results for “" + username + "”";
  summaryCount.textContent =
    "Available on " + counts.available + " of " + total + " platforms";
  progressBar.style.width =
    (total ? Math.round((counts.available / total) * 100) : 0) + "%";

  renderFilters(counts, total);

  grid.setAttribute("aria-busy", "false");
  grid.innerHTML = "";
  sites.forEach(function (site) {
    grid.appendChild(buildCard(site, resultsObj[site]));
  });
  applyFilter();

  summaryEl.hidden = false;
  emptyEl.hidden = true;
}

function showSkeletons(count) {
  grid.setAttribute("aria-busy", "true");
  grid.innerHTML = "";
  for (let i = 0; i < count; i++) {
    const sk = el("div", "card card-skeleton");
    sk.appendChild(el("div", "skeleton-icon"));
    const body = el("div", "card-body");
    body.appendChild(el("div", "skeleton-line"));
    body.appendChild(el("div", "skeleton-pill"));
    sk.appendChild(body);
    grid.appendChild(sk);
  }
  summaryEl.hidden = true;
  emptyEl.hidden = true;
}

function showEmpty() {
  summaryEl.hidden = true;
  grid.innerHTML = "";
  emptyEl.hidden = false;
}

function toast(message) {
  const node = el("div", "toast", message);
  toastContainer.appendChild(node);
  requestAnimationFrame(function () {
    node.classList.add("is-visible");
  });
  setTimeout(function () {
    node.classList.remove("is-visible");
    node.addEventListener(
      "transitionend",
      function () {
        node.remove();
      },
      { once: true },
    );
  }, 4500);
}

function setFieldError(message) {
  fieldHelp.textContent = message || "";
  fieldHelp.classList.toggle("is-error", Boolean(message));
  input.setAttribute("aria-invalid", message ? "true" : "false");
}

function populateDropdown(entries) {
  select.innerHTML = "";
  const seen = new Set();
  const placeholder = el("option", null, "Select a previous search…");
  placeholder.value = "none";
  select.appendChild(placeholder);
  for (let i = entries.length - 1; i >= 0; i--) {
    const name = entries[i].username;
    if (seen.has(name)) continue;
    seen.add(name);
    const option = el("option", null, name);
    option.value = name;
    select.appendChild(option);
  }
}

async function refreshHistory() {
  try {
    const response = await fetch("/saved-data");
    const data = await response.json();
    savedEntries = Array.isArray(data) ? data : [];
  } catch (err) {
    savedEntries = [];
  }
  populateDropdown(savedEntries);
  return savedEntries;
}

form.addEventListener("submit", async function (event) {
  event.preventDefault();
  const username = input.value.trim();

  if (!USERNAME_PATTERN.test(username)) {
    setFieldError("Use 1–40 letters, digits, dots, hyphens or underscores.");
    input.focus();
    return;
  }
  setFieldError("");

  button.disabled = true;
  button.classList.add("is-loading");
  buttonLabel.textContent = "Checking…";
  showSkeletons(12);

  try {
    const response = await fetch("/check", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: new URLSearchParams({ username: username }),
    });
    const data = await response.json();
    if (!response.ok || data.error) {
      throw new Error(data.error || "The check could not be completed.");
    }
    renderResults(data.username, data.results);
    await refreshHistory();
  } catch (err) {
    toast(err.message || "An error occurred while checking the username.");
    if (lastRendered) {
      renderResults(lastRendered.username, lastRendered.results);
    } else {
      showEmpty();
    }
  } finally {
    button.disabled = false;
    button.classList.remove("is-loading");
    buttonLabel.textContent = "Check";
  }
});

input.addEventListener("input", function () {
  if (fieldHelp.classList.contains("is-error")) setFieldError("");
});

select.addEventListener("change", function (event) {
  const value = event.target.value;
  if (value === "none") return;
  let entry = null;
  for (let i = savedEntries.length - 1; i >= 0; i--) {
    if (savedEntries[i].username === value) {
      entry = savedEntries[i];
      break;
    }
  }
  if (entry) renderResults(entry.username, entry.results);
});

(async function init() {
  const entries = await refreshHistory();
  if (entries.length) {
    const recent = entries[entries.length - 1];
    renderResults(recent.username, recent.results);
  } else {
    showEmpty();
  }
})();
