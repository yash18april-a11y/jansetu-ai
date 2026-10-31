# JanSetu AI: Research and submission plan

## Problem statement
Government scheme information is dispersed and eligibility may be difficult to interpret. JanSetu AI aims to support discovery, transparent preliminary screening, document preparation, and official application navigation.

## Research questions
1. Does adaptive question selection reduce questions without increasing false eligibility decisions?
2. Does hybrid semantic and structured ranking outperform TF-IDF on labeled scheme-profile pairs?
3. Does source-versioned deterministic reasoning improve auditability of AI-generated guidance?

## Literature review topics (to verify and cite)
- myScheme, UMANG, DigiLocker official documentation
- Lewis et al. (2020), Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks
- Explainable AI and rule-based decision systems
- Information gain and adaptive questionnaires
- Recommender ranking evaluation and multilingual NLP

## Requirements
- Functional: auth, profile, scheme listing, relevance ranking, preliminary eligibility explanations, save schemes
- Planned: official-source ingestion, source versioning, admin review, RAG, agent controller, OCR, mobile client, notifications
- Non-functional: access control, privacy, evidence provenance, accessibility, latency, testing, logging

## Research evaluation
- Ranking: Precision@5, Recall@5, NDCG@5 using independently reviewed relevance labels
- Eligibility: accuracy, false-positive eligibility rate, unknown-condition handling
- Adaptive questions: average question count, accuracy, time-to-decision vs fixed order
- RAG: citation correctness, groundedness, retrieval precision, response latency
- OCR: field-level precision, recall and F1
Never report targets as measured results.

## Phases
1. Source validation and requirements; 2. MySQL and APIs; 3. ML baseline; 4. rule engine and adaptive questioning; 5. RAG/agents; 6. OCR/mobile; 7. evaluation/deployment; 8. synopsis/report/PPT/viva.

## Proposed four-person division
- Member A: Flask, MySQL, security and API tests
- Member B: ML experiments and adaptive questioning
- Member C: React web, mobile and UX
- Member D: source research, RAG, evaluation and academic writing
All members jointly review integration and evidence quality.

## Limitations of this first build
No official schemes are preloaded, because unverified eligibility rules must not be published. The TF-IDF recommender is an unsupervised baseline, not a trained supervised ranking model. RAG, LangGraph, OCR, mobile and deployment are not implemented yet. This is not an official government service.
