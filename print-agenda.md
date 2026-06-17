---
layout: print
title: Agenda at a Glance
permalink: /agenda/print/
schedule:
  - time: "7:30–8:30 AM"
    label: "Registration"
    muted: true
  - time: "8:30–8:45 AM"
    label: "Welcoming Remarks"
  - time: "8:45–10:00 AM"
    label: "Project Findings"
  - time: "10:00–10:45 AM"
    label: "Fireside Chat: Flooding & Community Partnerships"
  - time: "10:45–11:00 AM"
    label: "Break"
    muted: true
  - time: "11:00–11:45 AM"
    label: "Panel: Innovative Energy Partnerships"
  - time: "11:45 AM–12:45 PM"
    label: "Catered Lunch & Networking"
    muted: true
  - time: "12:45–1:35 PM"
    label: "Panel: Federal & State Financing"
  - time: "1:35–2:25 PM"
    label: "Panel: Creative Financing"
  - time: "2:25–2:35 PM"
    label: "Break"
    muted: true
  - time: "2:35–3:20 PM"
    label: "Regional Workshops / Breakouts"
  - time: "3:20–3:30 PM"
    label: "Transition & Break"
    muted: true
  - time: "3:30–4:00 PM"
    label: "Wrap-Up & Next Steps"
  - time: "4:00 PM"
    label: "Adjourn"
    muted: true
sessions:
  - /agenda/sessions/welcoming-remarks/
  - /agenda/sessions/project-findings/
  - /agenda/sessions/fireside-chat-flooding-community-partnerships/
  - /agenda/sessions/panel-innovative-energy-partnerships/
  - /agenda/sessions/panel-federal-state-financing-opportunities/
  - /agenda/sessions/panel-creative-financing-opportunities/
  - /agenda/sessions/regional-workshops-breakouts/
---

<div class="phead">
  <div class="phead-inner">
    <p class="peyebrow">Statewide Convening &middot; Agenda at a Glance</p>
    <h1 class="ptitle">{{ site.title }}</h1>
    <p class="pmeta">Tuesday, June 23, 2026 &nbsp;&middot;&nbsp; 8:30&nbsp;AM&ndash;4:00&nbsp;PM &nbsp;&middot;&nbsp; University of Maryland, Baltimore &mdash; SMC Campus Center</p>
  </div>
</div>

<div class="pbody">
  <div class="pside">
    <aside class="prail">
      <h2 class="rail-h">At a Glance</h2>
      <ul class="prail-list">
        {%- for row in page.schedule -%}
        <li class="{% if row.muted %}muted{% endif %}">
          <span class="prail-time">{{ row.time }}</span>
          <span class="prail-label">{{ row.label }}</span>
        </li>
        {%- endfor -%}
      </ul>
    </aside>

    <div class="plogos">
      <img class="plogo" src="{{ '/assets/images/logos/maryland-commerce.jpg' | relative_url }}" alt="Maryland Department of Commerce logo" />
      <img class="plogo" src="{{ '/assets/images/logos/chhs.png' | relative_url }}" alt="University of Maryland Center for Cyber, Health, and Hazard Strategies logo" />
      <img class="plogo" src="{{ '/assets/images/logos/mdem-mor.png' | relative_url }}" alt="Maryland Department of Emergency Management, Office of Resilience logo" />
      <img class="plogo" src="{{ '/assets/images/logos/mdp.png' | relative_url }}" alt="Maryland Department of Planning logo" />
    </div>
  </div>

  <main class="pcards">
    {%- for permalink in page.sessions -%}
    {%- assign session = site.pages | where: "permalink", permalink | first -%}
    {%- if session -%}{%- include print-session-card.html session=session -%}{%- endif -%}
    {%- endfor -%}
  </main>
</div>
