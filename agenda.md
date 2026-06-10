---
layout: default
title: Agenda
permalink: /agenda/
---

## Agenda at a Glance

<div class="panel">
  <ul class="agenda-list">
    <li>
      <span class="time">7:30-8:30 AM</span>
      <div class="agenda-session">
        <p class="agenda-title"><a class="agenda-session-link" href="{{ '/agenda/sessions/registration/' | relative_url }}">Registration</a></p>
      </div>
    </li>
    <li id="welcoming-remarks">
      <span class="time">8:30-8:45 AM</span>
      <div class="agenda-session">
        <p class="agenda-title"><a class="agenda-session-link" href="{{ '/agenda/sessions/welcoming-remarks/' | relative_url }}">Welcoming Remarks</a></p>
        {% assign session = site.pages | where: "permalink", "/agenda/sessions/welcoming-remarks/" | first %}
        {% if session.speakers and session.speakers.size > 0 %}
        <div class="agenda-speaker-line">
          {% for speaker in session.speakers %}
          {% assign speaker_page = site.pages | where: "url", speaker.url | first %}
          {% assign speaker_photo = speaker.photo | default: speaker_page.photo | default: '/assets/images/speakers/placeholder.svg' %}
          <a class="agenda-speaker-link" href="{{ speaker.url | relative_url }}" title="{{ speaker.name }} — {{ speaker.role }}">
            <img class="agenda-headshot" src="{{ speaker_photo | relative_url }}" alt="{{ speaker.name }}" loading="lazy" />
          </a>
          {% endfor %}
        </div>
        {% endif %}
      </div>
    </li>
    <li>
      <span class="time">8:45-10:00 AM</span>
      <div class="agenda-session">
        <p class="agenda-title"><a class="agenda-session-link" href="{{ '/agenda/sessions/project-findings/' | relative_url }}">Resilient Maryland Defense Communities Project Findings</a></p>
        {% assign session = site.pages | where: "permalink", "/agenda/sessions/project-findings/" | first %}
        {% if session.speakers and session.speakers.size > 0 %}
        <div class="agenda-speaker-line">
          {% for speaker in session.speakers %}
          {% assign speaker_page = site.pages | where: "url", speaker.url | first %}
          {% assign speaker_photo = speaker.photo | default: speaker_page.photo | default: '/assets/images/speakers/placeholder.svg' %}
          <a class="agenda-speaker-link" href="{{ speaker.url | relative_url }}" title="{{ speaker.name }} — {{ speaker.role }}">
            <img class="agenda-headshot" src="{{ speaker_photo | relative_url }}" alt="{{ speaker.name }}" loading="lazy" />
          </a>
          {% endfor %}
        </div>
        {% endif %}
      </div>
    </li>
    <li>
      <span class="time">10:00-10:45 AM</span>
      <div class="agenda-session">
        <p class="agenda-title"><a class="agenda-session-link" href="{{ '/agenda/sessions/fireside-chat-flooding-community-partnerships/' | relative_url }}">Fireside Chat: Flooding and Community Partnerships</a></p>
        {% assign panel = site.pages | where: "permalink", "/agenda/sessions/fireside-chat-flooding-community-partnerships/" | first %}
        {% include agenda-panel-detail.html panel=panel %}
      </div>
    </li>
    <li>
      <span class="time">10:45-11:00 AM</span>
      <div class="agenda-session">
        <p class="agenda-title"><a class="agenda-session-link" href="{{ '/agenda/sessions/break-morning/' | relative_url }}">Break</a></p>
      </div>
    </li>
    <li>
      <span class="time">11:00-11:45 AM</span>
      <div class="agenda-session">
        <p class="agenda-title"><a class="agenda-session-link" href="{{ '/agenda/sessions/panel-innovative-energy-partnerships/' | relative_url }}">Panel: Innovative Energy Partnerships</a></p>
        {% assign panel = site.pages | where: "permalink", "/agenda/sessions/panel-innovative-energy-partnerships/" | first %}
        {% include agenda-panel-detail.html panel=panel %}
      </div>
    </li>
    <li class="agenda-has-parallel">
      <span class="time">11:15 AM-1:15 PM</span>
      <div class="agenda-session">
        <p class="agenda-title">Parallel Tracks</p>
        <div class="agenda-parallel">
          <article class="agenda-track">
            <p class="agenda-track-time">11:15 AM-1:15 PM</p>
            <p class="agenda-track-title"><a class="agenda-session-link" href="{{ '/agenda/sessions/military-installation-commanders-meeting/' | relative_url }}">Military Installation Commanders Meeting + Lunch (closed door session)</a></p>
          </article>
          <article class="agenda-track">
            <p class="agenda-track-time">11:45 AM-12:45 PM</p>
            <p class="agenda-track-title"><a class="agenda-session-link" href="{{ '/agenda/sessions/catered-lunch-networking/' | relative_url }}">Catered Lunch and Networking</a></p>
          </article>
        </div>
      </div>
    </li>
    <li>
      <span class="time">12:45-1:35 PM</span>
      <div class="agenda-session">
        <p class="agenda-title"><a class="agenda-session-link" href="{{ '/agenda/sessions/panel-federal-state-financing-opportunities/' | relative_url }}">Panel: Federal and State Financing Opportunities</a></p>
        {% assign panel = site.pages | where: "permalink", "/agenda/sessions/panel-federal-state-financing-opportunities/" | first %}
        {% include agenda-panel-detail.html panel=panel %}
      </div>
    </li>
    <li>
      <span class="time">1:35-2:25 PM</span>
      <div class="agenda-session">
        <p class="agenda-title"><a class="agenda-session-link" href="{{ '/agenda/sessions/panel-creative-financing-opportunities/' | relative_url }}">Panel: Creative Financing Opportunities</a></p>
        {% assign panel = site.pages | where: "permalink", "/agenda/sessions/panel-creative-financing-opportunities/" | first %}
        {% include agenda-panel-detail.html panel=panel %}
      </div>
    </li>
    <li>
      <span class="time">2:25-2:35 PM</span>
      <div class="agenda-session">
        <p class="agenda-title"><a class="agenda-session-link" href="{{ '/agenda/sessions/break-afternoon/' | relative_url }}">Break</a></p>
      </div>
    </li>
    <li>
      <span class="time">2:35-3:20 PM</span>
      <div class="agenda-session">
        <p class="agenda-title"><a class="agenda-session-link" href="{{ '/agenda/sessions/regional-workshops-breakouts/' | relative_url }}">Regional Workshops / Breakouts</a></p>

      </div>
    </li>
    <li>
      <span class="time">3:20-3:30 PM</span>
      <div class="agenda-session">
        <p class="agenda-title"><a class="agenda-session-link" href="{{ '/agenda/sessions/transition-break/' | relative_url }}">Transition &amp; Break</a></p>
      </div>
    </li>
    <li>
      <span class="time">3:30-4:00 PM</span>
      <div class="agenda-session">
        <p class="agenda-title"><a class="agenda-session-link" href="{{ '/agenda/sessions/wrap-up-next-steps/' | relative_url }}">Wrap-Up and Next Steps</a></p>

      </div>
    </li>
    <li>
      <span class="time">4:00 PM</span>
      <div class="agenda-session">
        <p class="agenda-title"><a class="agenda-session-link" href="{{ '/agenda/sessions/adjourn/' | relative_url }}">Adjourn</a></p>
      </div>
    </li>
  </ul>
</div>

