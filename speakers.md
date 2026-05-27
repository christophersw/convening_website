---
layout: default
title: Speaker Bios
permalink: /speakers/
---

## Featured Speakers and Facilitators

Select a speaker to view their full bio page and agenda sessions.

<div class="panel speaker-directory">
  <div class="session-speaker-grid">
    {% assign speakers = site.pages | where: "layout", "speaker" | sort: "speaker_name" %}
    {% for s in speakers %}
    <a class="session-speaker-card" href="{{ s.url | relative_url }}">
      <img class="session-speaker-photo" src="{{ s.photo | default: '/assets/images/speakers/placeholder.svg' | relative_url }}" alt="{{ s.photo_alt }}" />
      <div class="session-speaker-content">
        <h3 class="session-speaker-name">{{ s.speaker_name }}</h3>
        {% if s.speaker_title %}
        <p class="session-speaker-title"><strong>{{ s.speaker_title }}</strong></p>
        {% endif %}
      </div>
    </a>
    {% endfor %}
  </div>
</div>
