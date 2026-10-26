/* ClubQuest uses the existing FastAPI quiz and scoring endpoints unchanged.
   Answers live in memory; only bookmarked club IDs are stored on this device. */
"use strict";
const main = document.querySelector("#main");
const dialog = document.querySelector("#club-dialog");
const state = {
  clubs: [],
  byId: new Map(),
  question: null,
  history: [],
  answers: {},
  results: null,
  busy: false,
  routeVersion: 0,
  limit: 12,
  filter: { search: "", category: "", beginner: false },
};
let saved = new Set();
try {
  const raw = JSON.parse(localStorage.getItem("clubquest.saved.v1") || "[]");
  if (Array.isArray(raw))
    saved = new Set(raw.filter((x) => typeof x === "string"));
} catch {
  /* Private browsing can disable storage. */
}

const paths = {
  music:
    '<path d="M9 18V5l11-2v13M9 9l11-2"/><ellipse cx="6" cy="18" rx="3" ry="2.5"/><ellipse cx="17" cy="16" rx="3" ry="2.5"/>',
  dance:
    '<circle cx="14" cy="4" r="2"/><path d="m3 9 7 2 5-3 6 2M11 11l2 5 5 5M13 16l-5 1-3 4"/>',
  theatre:
    '<path d="M3 4c4 2 7 2 11 0v8c0 4-3 7-5.5 8C6 19 3 16 3 12V4ZM16 6l5-2v8c0 4-2 6-4 8"/><path d="M6 9h1m3 0h1m-5 5c1 2 4 2 5 0"/>',
  visual_arts:
    '<path d="M12 3a9 9 0 1 0 0 18h1c2 0 2-3 0-4-1-1 0-3 2-3h3c5 0 2-11-6-11Z"/><circle cx="7" cy="10" r=".8"/><circle cx="10" cy="6.5" r=".8"/><circle cx="15" cy="7" r=".8"/>',
  writing_media:
    '<path d="M4 4h6c2 0 2 1 2 2v15c0-2-2-3-4-3H3V4h1ZM20 4h-6c-2 0-2 1-2 2v15c0-2 2-3 4-3h5V4h-1Z"/>',
  games:
    '<rect x="3" y="3" width="18" height="18" rx="4"/><circle cx="8" cy="8" r="1"/><circle cx="16" cy="8" r="1"/><circle cx="12" cy="12" r="1"/><circle cx="8" cy="16" r="1"/><circle cx="16" cy="16" r="1"/>',
  food: '<path d="M4 9h13v5a6.5 6.5 0 0 1-13 0V9ZM17 10h2a3 3 0 0 1 0 6h-2M7 3v2m4-2v2m4-2v2M3 21h16"/>',
  tech: '<path d="m8 7-5 5 5 5m8-10 5 5-5 5m-2-14-4 18"/>',
  outdoors: '<path d="m12 2-6 8h3l-5 7h7v5h2v-5h7l-5-7h3L12 2Z"/>',
  sustainability: '<path d="M20 3C7 1 2 8 5 15s15 7 15-12ZM4 21 16 9"/>',
  cultural:
    '<circle cx="12" cy="12" r="9"/><ellipse cx="12" cy="12" rx="4" ry="9"/><path d="M3 12h18M5 6h14M5 18h14"/>',
  language:
    '<path d="M3 3h13v11H8l-5 4V3Zm13 5h5v13l-5-4h-5v-3M6 7h7M6 10h4"/>',
  identity:
    '<path d="M12 21S2 15 2 8a5 5 0 0 1 10-1A5 5 0 0 1 22 8c0 7-10 13-10 13Z"/>',
  faith:
    '<path d="M4 18h16M6 14a6 6 0 0 1 12 0M12 2v3M3 7l2 2m16-2-2 2M2 14h2m16 0h2M7 22h10"/>',
  service:
    '<path d="m12 20-8-8a5 5 0 0 1 8-6 5 5 0 0 1 8 6l-8 8ZM9 12h6m-3-3v6"/>',
  advocacy: '<path d="m3 10 15-6v15L3 13v-3Zm3 4 2 7h4l-2-6M21 8v7"/>',
  bookmark: '<path d="M6 3h12v18l-6-4-6 4V3Z"/>',
  search: '<circle cx="10.5" cy="10.5" r="7"/><path d="m16 16 5 5"/>',
  spark:
    '<path d="m12 2 2.5 7.5L22 12l-7.5 2.5L12 22l-2.5-7.5L2 12l7.5-2.5L12 2Z"/>',
  check: '<path d="m5 12 4 4L20 5"/>',
};
const categoryMeta = [
  ["music", "Music & Singing", "Find your rhythm", "#eadacb"],
  ["dance", "Dance & Movement", "Move in good company", "#edd9d2"],
  ["theatre", "Theatre, Comedy & Storytelling", "Take the stage", "#e9dbcc"],
  [
    "visual_arts",
    "Visual Arts, Crafts & Design",
    "Make something together",
    "#ece2c3",
  ],
  [
    "writing_media",
    "Writing, Media & Publications",
    "Share your perspective",
    "#e6dfea",
  ],
  ["games", "Games, Puzzles & Fandom", "Find your next game night", "#dedfc9"],
  ["food", "Food & Drink", "A seat at the table", "#efd8c2"],
  ["tech", "Tech & Making", "Build for the fun of it", "#dbe4e5"],
  [
    "outdoors",
    "Outdoors, Nature & Animals",
    "Take the scenic route",
    "#dee5cb",
  ],
  [
    "sustainability",
    "Sustainability & Environment",
    "Make a greener tomorrow",
    "#d9e3d2",
  ],
  ["cultural", "Cultural & Heritage", "Celebrate what connects us", "#eddbc9"],
  ["language", "Language & Global Exchange", "Start a conversation", "#dfe4ed"],
  ["identity", "Identity & Community", "A place to feel at home", "#e9dce3"],
  [
    "faith",
    "Faith, Spirituality & Mindfulness",
    "Find space to reflect",
    "#e5e0d0",
  ],
  ["service", "Service & Volunteering", "Do a little good together", "#e2e6d5"],
  [
    "advocacy",
    "Advocacy, Politics & Debate",
    "Put your voice to work",
    "#e8d8d4",
  ],
];
const esc = (value) =>
  String(value ?? "").replace(
    /[&<>"']/g,
    (c) =>
      ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" })[
        c
      ],
  );
const icon = (name) =>
  `<svg class="icon" viewBox="0 0 24 24" aria-hidden="true">${paths[name] || paths.spark}</svg>`;
const meta = (category) =>
  categoryMeta.find((m) => m[1] === category) || [
    "spark",
    category || "Club",
    "",
    "#e3e8d7",
  ];
const truthy = (value) => /^(true|1|yes|y)$/i.test(String(value));
const safeUrl = (value) => {
  try {
    const u = new URL(String(value));
    return ["https:", "http:"].includes(u.protocol) ? u.href : "";
  } catch {
    return "";
  }
};
const timeLabel = (club) =>
  club.hours_per_week_min !== "" &&
  club.hours_per_week_max !== "" &&
  club.hours_per_week_min != null &&
  club.hours_per_week_max != null
    ? `${club.hours_per_week_min}–${club.hours_per_week_max} hrs / week`
    : "Time not listed";

async function api(path, body) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 45000);
  try {
    const response = await fetch(path, {
      signal: controller.signal,
      ...(body
        ? {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(body),
          }
        : {}),
    });
    if (!response.ok)
      throw new Error(
        `The app couldn't complete that request (${response.status}). Please try again.`,
      );
    return await response.json();
  } catch (error) {
    if (error.name === "AbortError")
      throw new Error(
        "The server is taking a little longer. Please try again.",
      );
    if (error instanceof TypeError)
      throw new Error(
        "We couldn't reach the server. Check your connection and try again.",
      );
    throw error;
  } finally {
    clearTimeout(timeout);
  }
}
function toast(message) {
  const el = document.querySelector("#toast");
  el.textContent = message;
  el.classList.add("visible");
  clearTimeout(toast.timer);
  toast.timer = setTimeout(() => el.classList.remove("visible"), 2700);
}
function updateSaved() {
  document.querySelector("#saved-count").textContent = saved.size;
  document.querySelectorAll("[data-save]").forEach((button) => {
    const isSaved = saved.has(button.dataset.save);
    const club = state.byId.get(button.dataset.save);
    button.setAttribute("aria-pressed", isSaved);
    button.setAttribute(
      "aria-label",
      `${isSaved ? "Unsave" : "Save"} ${club?.club_name || "club"}`,
    );
    if (button.classList.contains("detail-save"))
      button.innerHTML = `${icon("bookmark")} ${isSaved ? "Saved to your list" : "Save club"}`;
  });
}
function toggleSaved(id) {
  saved.has(id) ? saved.delete(id) : saved.add(id);
  let persisted = true;
  try {
    localStorage.setItem("clubquest.saved.v1", JSON.stringify([...saved]));
  } catch {
    persisted = false;
  }
  updateSaved();
  toast(
    persisted
      ? saved.has(id)
        ? "Saved to your list on this device"
        : "Removed from your saved clubs"
      : "Saved for this visit. Your browser blocked device storage.",
  );
  if (location.hash.startsWith("#saved")) renderDirectory(true);
}
function card(club, match) {
  const m = meta(club.category);
  const id = esc(club.club_id);
  const reasons = match?.reasons || [];
  return `<article class="club-card"><div class="card-banner" style="background:${m[3]}">${icon(m[0])}${match ? `<span class="match-label">${esc(match.match_percent)} / 100 score</span>` : ""}<button class="save-button" data-save="${id}" aria-pressed="${saved.has(club.club_id)}" aria-label="${saved.has(club.club_id) ? "Unsave" : "Save"} ${esc(club.club_name)}">${icon("bookmark")}</button></div><div class="card-content"><p class="card-kicker">${esc(club.subcategory || club.category)}</p><h3>${esc(club.club_name)}</h3><p class="summary">${esc(club.summary || "Explore this club and see whether it feels like your kind of community.")}</p>${reasons.length ? `<div class="result-reasons">${reasons.map((r) => `<span class="tag">${esc(r)}</span>`).join("")}</div>` : ""}<div class="card-tags">${truthy(club.beginner_friendly) ? '<span class="tag">Beginner friendly</span>' : ""}<span class="tag">${esc(timeLabel(club))}</span></div></div><div class="card-footer"><span>${esc(club.meeting_format || "Cornell community")}</span><button data-detail="${id}" aria-label="View ${esc(club.club_name)}">View club <span aria-hidden="true">↗</span></button></div></article>`;
}
function categoryTile(m) {
  const count = state.clubs.filter((c) => c.category === m[1]).length;
  return `<a class="category-tile" href="#explore?category=${encodeURIComponent(m[1])}"><span class="icon-box" style="background:${m[3]}">${icon(m[0])}</span><strong>${esc(m[1])}</strong><small>${count} club${count === 1 ? "" : "s"} to explore <span aria-hidden="true">↗</span></small></a>`;
}
function renderHome() {
  const picks = ["outdoors", "music", "visual_arts", "games"].map((id) =>
    categoryMeta.find((m) => m[0] === id),
  );
  main.innerHTML = `<div class="wrap"><section class="hero"><div class="hero-copy"><div class="eyebrow"><span class="dot"></span> A little more belonging</div><h1>Your people.<br>Your <em>place.</em></h1><p>There’s more to Cornell than your next class. Find clubs that feel like you, and a few that might surprise you.</p><div class="hero-actions"><a class="btn btn-primary" href="#quiz">Find my clubs <span aria-hidden="true">↗</span></a><a class="btn btn-secondary" href="#explore">Explore on my own <span aria-hidden="true">→</span></a></div><div class="hero-footnote">${icon("check")} Your interests. Your pace. No account needed.</div></div><div class="community-art" role="img" aria-label="Illustrated cards for outdoor adventures, music, and creative hobbies"><div class="art-grid"></div><div class="art-caption">THERE’S A WHOLE WORLD HERE</div><div class="art-orbit"></div><span class="art-star">✳</span><div class="mini-card one">${icon("outdoors")}<strong>Take the scenic route.</strong><small>Outdoors, nature & a little fresh air</small></div><div class="mini-card two">${icon("music")}<strong>Find your rhythm.</strong><small>Music, singing & shared stages</small></div><div class="mini-card three">${icon("visual_arts")}<strong>Make something good.</strong><small>Art, crafts & creative company</small></div><div class="art-sticker"><span>A LITTLE MORE</span><b>you.</b></div></div></section><div class="stat-strip"><div class="stat"><strong>${state.clubs.length}</strong><span>club records in our project dataset</span></div><div class="stat"><strong>${new Set(state.clubs.map((c) => c.category)).size}</strong><span>ways to follow your interests</span></div><div class="stat"><strong>1</strong><span>quiz built around what matters to you</span></div><p class="strip-note">Big interests. Small discoveries.<br>A starting point for your next chapter.</p></div><section class="section"><div class="section-heading"><div><p class="eyebrow">Follow your curiosity</p><h2>What’s your kind of thing?</h2></div><a href="#explore" class="text-link">See all categories <span aria-hidden="true">↗</span></a></div><div class="category-grid">${picks.map(categoryTile).join("")}</div></section><section class="how-strip" aria-label="How it works"><div class="how-step"><span class="num">01</span><div><strong>Tell us a little about you.</strong><p>Choose your interests, your availability, and the kind of experience you want.</p></div></div><div class="how-step"><span class="num">02</span><div><strong>Discover your possibilities.</strong><p>Get club suggestions with a reason behind every recommendation.</p></div></div><div class="how-step"><span class="num">03</span><div><strong>Make the first move.</strong><p>Save a few favorites and check with each club about getting involved.</p></div></div></section></div>`;
}
function renderDirectory(onlySaved = false) {
  main.innerHTML = `<div class="wrap"><header class="page-top"><p class="eyebrow"><span class="dot"></span> ${onlySaved ? "Your little shortlist" : "Follow your curiosity"}</p><h1>${onlySaved ? "Keep the possibilities close." : "A club for your kind of curious."}</h1><p>${onlySaved ? "Your saved clubs live on this device. Come back when you’re ready to take the next step." : "Browse the project’s club collection. Follow a familiar interest, or leave room for something new."}</p></header><div class="toolbar"><label class="search-box"><span class="hidden">Search clubs</span>${icon("search")}<input id="club-search" type="search" aria-label="Search clubs" placeholder="Search a club, an interest, a possibility…" value="${esc(state.filter.search)}"></label><select id="category-filter" aria-label="Filter by category"><option value="">All categories</option>${categoryMeta.map((m) => `<option value="${esc(m[1])}" ${state.filter.category === m[1] ? "selected" : ""}>${esc(m[1])}</option>`).join("")}</select><label class="check-filter"><input id="beginner-filter" type="checkbox" ${state.filter.beginner ? "checked" : ""}> Beginner friendly</label></div><div class="count-line"><span id="club-count" role="status" aria-live="polite"></span><span>Club details come from the project dataset.</span></div><div id="directory-grid"></div><div id="load-more" class="load-more"></div><p class="notice">Meeting times, dues, and membership details may change. Confirm current information with each organization.</p></div>`;
  renderDirectoryCards(onlySaved);
}
function renderDirectoryCards(onlySaved = location.hash.startsWith("#saved")) {
  const f = state.filter;
  const needle = f.search.trim().toLowerCase();
  const source = onlySaved
    ? state.clubs.filter((c) => saved.has(c.club_id))
    : state.clubs;
  const clubs = source.filter(
    (c) =>
      (!f.category || c.category === f.category) &&
      (!f.beginner || truthy(c.beginner_friendly)) &&
      (!needle ||
        [
          c.club_name,
          c.summary,
          c.category,
          c.subcategory,
          c.interest_tags,
        ].some((v) => String(v).toLowerCase().includes(needle))),
  );
  document.querySelector("#club-count").textContent =
    `${clubs.length} club${clubs.length === 1 ? "" : "s"}${f.search || f.category || f.beginner ? " found" : " to explore"}`;
  document.querySelector("#directory-grid").innerHTML = clubs.length
    ? `<div class="club-grid">${clubs
        .slice(0, state.limit)
        .map((c) => card(c))
        .join("")}</div>`
    : `<section class="empty-state">${icon(onlySaved && !source.length ? "bookmark" : "search")}<h2>${onlySaved && !source.length ? "Your next chapter starts here." : "Let’s try a different direction."}</h2><p>${onlySaved && !source.length ? "Tap the bookmark on a club to keep it here. No account needed." : "No clubs match these filters. Try a broader search or another category."}</p>${onlySaved && !source.length ? '<a href="#explore" class="btn btn-primary">Explore clubs ↗</a>' : '<button class="btn btn-secondary" data-action="reset-filters">Clear filters →</button>'}</section>`;
  document.querySelector("#load-more").innerHTML =
    clubs.length > state.limit
      ? `<button class="btn btn-secondary" data-action="load-more">Show more clubs <span aria-hidden="true">↓</span></button>`
      : "";
}
function renderQuestion() {
  const q = state.question;
  if (!q) return;
  const selected = state.answers[q.id];
  const total = 9 + (state.answers.categories?.length || 1);
  const title = q.question.replace(/\s*\(Select[^)]*\)/i, "");
  const instruction =
    q.type === "text"
      ? "Optional. This note does not change your recommendations in this version."
      : q.type === "single"
        ? "Choose the one that feels right."
        : q.max_selections
          ? `Choose up to ${q.max_selections}.`
          : "Choose as many as you like.";
  main.innerHTML = `<div class="quiz-wrap"><div class="quiz-top"><span>YOUR CLUB COMPASS <span aria-hidden="true"> / </span> Step ${state.history.length + 1} of ${total}</span><a href="#explore" class="quiet-button">Explore instead</a></div><div class="progress-track" role="progressbar" aria-label="Quiz progress" aria-valuemin="0" aria-valuemax="${total}" aria-valuenow="${state.history.length + 1}"><div class="progress-fill" style="width:${Math.min(100, ((state.history.length + 1) / total) * 100)}%"></div></div><div class="quiz-layout"><section class="quiz-main"><p class="eyebrow"><span class="dot"></span> ${q.id === "categories" ? "Start with what lights you up" : "A little more about you"}</p><h1 id="question-heading">${esc(title)}</h1><p class="quiz-instruction" id="question-instruction">${instruction}</p><form id="quiz-form" aria-labelledby="question-heading" aria-describedby="question-instruction">${q.type === "text" ? `<textarea id="text-answer" aria-label="Your ideal club experience" maxlength="2000" placeholder="A creative outlet? A weekly adventure? A new circle of friends?">${esc(selected || "")}</textarea><p class="text-hint">Up to 2,000 characters. Please leave out names and contact details.</p>` : `<div class="options-grid" role="group" aria-labelledby="question-heading">${q.options.map((o) => `<label class="option"><input type="${q.type === "single" ? "radio" : "checkbox"}" name="answer" value="${esc(o.id)}" ${(Array.isArray(selected) ? selected.includes(o.id) : selected === o.id) ? "checked" : ""}>${q.id === "categories" ? icon(o.id) : ""}<span>${esc(o.label)}</span></label>`).join("")}</div>`}<p class="quiz-error" id="quiz-error" role="alert"></p><div class="quiz-bottom"><button type="button" class="back" data-action="quiz-back">← ${state.history.length ? "Back" : "Home"}</button><button type="submit" class="btn btn-primary" id="quiz-continue">${q.id === "free_text" ? "Find my clubs" : "Continue"} <span aria-hidden="true">→</span></button></div></form></section><aside class="quiz-aside">${icon("spark")}<h2>There’s room<br>for all of you.</h2><p>You don’t have to fit into one category. Your recommendations will reflect the mix of things you’re curious about.</p><div class="aside-rule"></div><p>Change your mind? Go back anytime. No account is needed to get your recommendations.</p></aside></div></div>`;
}
function readAnswer() {
  if (state.question.type === "text")
    return document.querySelector("#text-answer").value.trim();
  const values = [
    ...document.querySelectorAll('input[name="answer"]:checked'),
  ].map((x) => x.value);
  return state.question.type === "single" ? values[0] : values;
}
async function submitAnswer(event) {
  event.preventDefault();
  if (state.busy) return;
  const value = readAnswer();
  const q = state.question;
  const error = document.querySelector("#quiz-error");
  if (q.type !== "text" && (!value || !value.length)) {
    error.textContent = "Choose at least one option to continue.";
    return;
  }
  if (q.max_selections && value.length > q.max_selections) {
    error.textContent = `Please choose no more than ${q.max_selections} options.`;
    return;
  }
  // Rebuild just the completed prefix so changing an earlier category removes
  // answers from abandoned quiz branches before the backend picks the next step.
  const nextAnswers = Object.fromEntries(
    state.history.map((item) => [item.id, state.answers[item.id]]),
  );
  nextAnswers[q.id] = value;
  state.busy = true;
  error.textContent = "";
  const button = document.querySelector("#quiz-continue");
  button.disabled = true;
  button.textContent =
    q.id === "free_text" ? "Finding your clubs…" : "One moment…";
  const version = state.routeVersion;
  try {
    const next = await api("/quiz/next", { answers: nextAnswers });
    const results = next.question
      ? null
      : await api("/recommend", { answers: nextAnswers, top_n: 12 });
    if (version !== state.routeVersion) return;
    state.answers = nextAnswers;
    state.history.push(q);
    state.question = next.question;
    if (next.question) {
      renderQuestion();
      main.focus({ preventScroll: true });
      window.scrollTo(0, 0);
    } else {
      state.results = results;
      location.hash = "results";
    }
  } catch (err) {
    if (version === state.routeVersion) {
      error.textContent = err.message;
      button.disabled = false;
      button.textContent =
        q.id === "free_text" ? "Try finding my clubs again →" : "Try again →";
    }
  } finally {
    state.busy = false;
  }
}
function quizBack() {
  if (state.busy) return;
  if (!state.history.length) {
    location.hash = "home";
    return;
  }
  state.answers[state.question.id] = readAnswer();
  state.question = state.history.pop();
  renderQuestion();
  main.focus({ preventScroll: true });
  window.scrollTo(0, 0);
}
function renderResults() {
  if (!state.results) {
    location.hash = "quiz";
    return;
  }
  const results = state.results.recommendations;
  main.innerHTML = `<div class="wrap"><header class="page-top"><p class="eyebrow"><span class="dot"></span> Your next chapter</p><h1>A few places to feel like you.</h1><p>Recommendations around your interests, your pace, and your kind of community. Think of these as open doors.</p></header><div class="result-tools">${(state.results.profile.categories || []).map((c) => `<span class="tag">${esc(c)}</span>`).join("")}<button class="quiet-button" data-action="retake">Retake quiz</button><a href="#explore" class="text-link">Explore all clubs ↗</a></div><p class="notice">Scores summarize the model’s weighted fit with your preferences; they are not probabilities. Results balance your selected categories, so they may not appear in score order.</p>${results.length ? `<div class="club-grid">${results.map((r) => card(state.byId.get(r.club_id) || r, r)).join("")}</div>` : `<section class="empty-state">${icon("search")}<h2>A little more room to explore.</h2><p>No clubs met all your selected filters. Try more interests or broader membership preferences.</p><button class="btn btn-primary" data-action="retake">Try the quiz again ↗</button></section>`}<p class="notice">This is a student project using a supplied club dataset. Verify current membership and meeting information directly with each club.</p></div>`;
}
function openDetail(id) {
  const c = state.byId.get(id);
  if (!c) return;
  const m = meta(c.category);
  const url = safeUrl(c.website_url);
  const field = (label, value) =>
    `<div class="detail-item"><small>${esc(label)}</small>${esc(value || "Not listed")}</div>`;
  document.querySelector("#dialog-content").innerHTML =
    `<div class="dialog-head" style="background:${m[3]}">${icon(m[0])}<button class="close-button" data-action="close-dialog" aria-label="Close club details">×</button></div><div class="dialog-body"><p class="card-kicker">${esc(c.category)} / ${esc(c.subcategory)}</p><h2 id="dialog-title">${esc(c.club_name)}</h2><p>${esc(c.description || c.summary)}</p><div class="detail-grid">${field("Weekly time", timeLabel(c))}${field("Meeting days", c.meeting_days)}${field("Meeting time", c.meeting_start_time)}${field("Location", c.typical_location)}${field("Semester dues", c.dues_usd_per_semester !== "" && c.dues_usd_per_semester != null ? `$${c.dues_usd_per_semester}` : "Not listed")}${field("Membership", c.membership_type)}</div>${c.typical_meeting ? `<h3 class="detail-heading">A typical get-together</h3><p>${esc(c.typical_meeting)}</p>` : ""}<div class="dialog-actions">${url ? `<a class="btn btn-primary" href="${esc(url)}" target="_blank" rel="noopener noreferrer">Visit club website ↗</a>` : ""}<button class="btn btn-secondary detail-save" data-save="${esc(c.club_id)}" aria-pressed="${saved.has(c.club_id)}">${icon("bookmark")} ${saved.has(c.club_id) ? "Saved to your list" : "Save club"}</button></div><p class="dialog-note">Details are from the project dataset and may be outdated. Confirm schedules, dues, and recruitment with the club.</p></div>`;
  if (!dialog.open) dialog.showModal();
}
async function route() {
  const version = ++state.routeVersion;
  const raw = location.hash.slice(1) || "home";
  const [page, query] = raw.split("?");
  const params = new URLSearchParams(query || "");
  if (dialog.open) dialog.close();
  document.querySelectorAll("[data-nav]").forEach((a) => {
    a.classList.toggle("active", a.dataset.nav === page);
    if (a.dataset.nav === page) a.setAttribute("aria-current", "page");
    else a.removeAttribute("aria-current");
  });
  document.title = `${{ home: "Find your people at Cornell", explore: "Explore Cornell clubs", saved: "Your saved clubs", quiz: "Your club compass", results: "Your club recommendations" }[page] || "Find your people"} — ClubQuest`;
  try {
    if (!state.clubs.length) {
      main.innerHTML =
        '<div class="busy"><div class="spinner"></div><h2>Good things are gathering.</h2><p>Loading your club collection…</p></div>';
      const clubs = await api("/clubs");
      if (version !== state.routeVersion) return;
      state.clubs = clubs;
      state.byId = new Map(clubs.map((c) => [c.club_id, c]));
      saved = new Set([...saved].filter((id) => state.byId.has(id)));
      updateSaved();
    }
    if (page === "explore" || page === "saved") {
      state.filter = {
        search: "",
        category: params.get("category") || "",
        beginner: false,
      };
      state.limit = 12;
      renderDirectory(page === "saved");
    } else if (page === "quiz") {
      if (!state.question) {
        const data = await api("/quiz/start");
        if (version !== state.routeVersion) return;
        state.question = data.question;
        state.history = [];
        state.answers = {};
      }
      renderQuestion();
    } else if (page === "results") renderResults();
    else renderHome();
    window.scrollTo(0, 0);
    main.focus({ preventScroll: true });
  } catch (error) {
    if (version !== state.routeVersion) return;
    main.innerHTML = `<div class="empty-state">${icon("spark")}<h2>We hit a small detour.</h2><p>${esc(error.message)}</p><button class="btn btn-primary" data-action="retry">Try again →</button></div>`;
  }
}

document.addEventListener("click", (event) => {
  if (event.target.closest(".skip-link")) {
    event.preventDefault();
    main.focus();
    return;
  }
  const save = event.target.closest("[data-save]");
  if (save) {
    toggleSaved(save.dataset.save);
    return;
  }
  const detail = event.target.closest("[data-detail]");
  if (detail) {
    openDetail(detail.dataset.detail);
    return;
  }
  const action = event.target.closest("[data-action]")?.dataset.action;
  if (action === "quiz-back") quizBack();
  if (action === "retake") {
    state.question = null;
    state.history = [];
    state.answers = {};
    state.results = null;
    if (location.hash === "#quiz") route();
    else location.hash = "quiz";
  }
  if (action === "reset-filters") {
    state.filter = { search: "", category: "", beginner: false };
    state.limit = 12;
    renderDirectory(location.hash.startsWith("#saved"));
  }
  if (action === "load-more") {
    state.limit += 12;
    renderDirectoryCards();
  }
  if (action === "close-dialog") dialog.close();
  if (action === "retry") route();
});
document.addEventListener("input", (event) => {
  if (event.target.id === "club-search") {
    state.filter.search = event.target.value;
    state.limit = 12;
    renderDirectoryCards();
  }
});
document.addEventListener("change", (event) => {
  if (event.target.id === "category-filter") {
    state.filter.category = event.target.value;
    state.limit = 12;
    renderDirectoryCards();
  }
  if (event.target.id === "beginner-filter") {
    state.filter.beginner = event.target.checked;
    state.limit = 12;
    renderDirectoryCards();
  }
  if (event.target.name === "answer")
    document.querySelector("#quiz-error").textContent = "";
});
document.addEventListener("submit", (event) => {
  if (event.target.id === "quiz-form") submitAnswer(event);
});
dialog.addEventListener("click", (event) => {
  if (event.target === dialog) {
    const r = dialog.getBoundingClientRect();
    if (
      event.clientX < r.left ||
      event.clientX > r.right ||
      event.clientY < r.top ||
      event.clientY > r.bottom
    )
      dialog.close();
  }
});
window.addEventListener("hashchange", route);
updateSaved();
route();
