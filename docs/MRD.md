# Market Requirements Document (MRD)

**Document Status:** Draft
**Version:** 1.0
**Author:** Hanish Paturi
**Date:** 2025-11-16

## 1. Introduction & Market Problem

The board game hobby is experiencing explosive [growth](https://www.gminsights.com/industry-analysis/board-games-market), leading to a market saturated with tens of thousands of titles. This "paradox of choice" presents a significant challenge for both new and experienced gamers. Newcomers are often overwhelmed and rely on generic "Top 10" lists, while experienced players struggle to discover niche games that perfectly match their unique tastes beyond what their immediate circle recommends. Existing recommendation tools on platforms like BoardGameGeek (BGG) are powerful but can be unintuitive and often lack a modern, personalized, and context-aware recommendation engine.

There is a clear market need for a more intelligent, accessible, and personalized recommendation service that can guide users through the vast landscape of board games.

## 2. Target Market & User Personas

The primary market for this product is the global community of board game enthusiasts, which can be segmented as follows:

* **Persona 1: The "Gateway" Gamer (Newcomer)**
* **Description:** Has played a few popular "gateway" games (e.g., *Catan*, *Ticket to Ride*) and is eager to explore more, but doesn't know where to start.
* **Needs:** Simple, similarity-based recommendations ("If you like X, you'll love Y"). They need to build confidence and vocabulary in game mechanics and themes.
* **Pain Points:** Overwhelmed by BGG's complexity; recommendations from friends are limited to what they own.

* **Persona 2: The "Dedicated" Hobbyist (Experienced Player)**
* **Description:** Owns 20-100+ games, actively rates games on BGG, and has well-defined tastes (e.g., "I love heavy Euro-style games but dislike high-luck dice games").
* **Needs:** Deeply personalized recommendations that understand their nuanced preferences. They value novelty and the discovery of "hidden gems."
* **Pain Points:** Standard recommendations are often too popular or obvious. They want a system that "gets" their unique taste profile.

* **Persona 3: The "Social" Organizer (Group Planner)**
* **Description:** Responsible for choosing games for their game night group, which may have varying player counts and preferences.
* **Needs:** Context-aware recommendations that filter based on player count, play time, and complexity.
* **Pain Points:** It's time-consuming to cross-reference game recommendations with the specific constraints of their game group for a given evening.

## 3. Competitive Landscape

* **BoardGameGeek (BGG):** The market leader and primary data source. Its recommendation features are built-in but are often considered dated and not deeply personalized. It serves as both a competitor and a data provider.
* **Recommender.games:** A web application that provides similarity-based recommendations. It is a direct competitor but focuses primarily on a single recommendation modality.
* **Friend/Community Recommendations:** The most common method of discovery, but it is limited by the knowledge and collection of one's immediate social circle.
* **Retailer Recommendations (e.g., Amazon):** Often generic and based on sales data ("Customers who bought this also bought..."), lacking nuanced understanding of game mechanics or themes.

## 4. Market Opportunity & Strategy

The opportunity lies in creating a "best-in-class" recommendation engine that surpasses existing tools in personalization, accuracy, and user experience.

* **Strategic Positioning:** Position the product as a "smart assistant" for board gamers.
* **Key Differentiator:** The **hybrid model** is the core differentiator. By combining content-based (RAG) and collaborative filtering, the system can serve both new users (cold start problem) and experienced users with rich data histories, providing a superior experience for all personas.
* **Go-to-Market Strategy:**
    1. **Phase 1 (Portfolio):** Develop the core engine and API as a public portfolio project to demonstrate technical expertise and attract potential collaborators or employers.
    2. **Phase 2 (Community Tool):** Build a simple, free-to-use web frontend (e.g., using Streamlit or Next.js) that consumes the API. Promote it within board game communities (Reddit, BGG forums) to gather feedback and build a user base.
    3. **Phase 3 (Potential Integration):** Explore opportunities for the API to be integrated into third-party fan sites, content creator pages, or other community tools.
