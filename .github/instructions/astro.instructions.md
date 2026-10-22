---
applyTo: "**/*.astro,**/astro.config.*,**/content.config.ts,src/pages/**,src/content/**,src/layouts/**"
description: "Astro site structure, components, content collections and build rules"
---

# Astro Guidelines
https://astro.build

## Purpose
Rules for building and reviewing websites with Astro. Target: **Astro 7.x** (latest stable), on the Node.js versions in [nodejs.instructions.md](./nodejs.instructions.md).

**TypeScript and Node.js rules apply:** follow [typescript.instructions.md](./typescript.instructions.md) for `.ts` files and the frontmatter of `.astro` files, and [nodejs.instructions.md](./nodejs.instructions.md) for tooling and server code. This file adds Astro-specific rules; where they overlap, this file wins for Astro projects.

## When to use Astro (versus Alpine.js or Angular)
Astro is mainly a **static site generator** for content-driven websites. It renders pages to plain HTML at build time and ships **zero JavaScript by default**; interactivity is added only where needed.

| Choose | For | Typical examples |
| --- | --- | --- |
| **Astro** | Mostly static, content-heavy pages that should be fast and SEO-friendly; built once, served from a CDN or static host. | Marketing and landing pages, company websites, documentation, blogs, product catalogs. |
| **Alpine.js** | Small, local interactivity sprinkled on HTML that already exists (rendered by Astro, Fastify or another server). Not a site generator or app framework. | Menus, dropdowns, tabs, modals, form helpers, simple filtering. |
| **Angular** | Full single-page applications with complex client state, routing, forms and long user sessions. | Dashboards, admin portals, line-of-business apps, authenticated tools. |

- Astro and Alpine.js complement each other: Astro produces the pages, Alpine.js adds small behavior on them (see [alpinejs.instructions.md](./alpinejs.instructions.md)). This is the default for interactive bits on an Astro site.
- Don't use Astro for an application whose main value is client-side interaction and state; use Angular (or another SPA framework) for that.
- Don't use Angular for a mostly static website; the page weight and complexity don't pay off.
- A server-rendered app on Fastify with Alpine.js (see the Node.js instructions) remains the default for dynamic, data-driven pages that are not mainly static content.

## Project setup
- Create projects with `npm create astro@latest` and keep the generated structure: `src/pages/`, `src/layouts/`, `src/components/`, `src/content/`, `public/`.
- Use the strict TypeScript preset (`"extends": "astro/tsconfigs/strictest"`) and run `astro check` in CI next to linting and the build.
- Add integrations with `npx astro add <name>` (e.g. `alpinejs`, `sitemap`, `mdx`) so the config is updated correctly.
- `package.json` scripts: `dev` (`astro dev`), `build` (`astro check && astro build`), `preview` (`astro preview`), plus `lint`, `format`, `test`.
- Set `site` in `astro.config.mjs` so canonical URLs, sitemaps and RSS feeds are correct.

## Rendering
- Default to static output (prerendered at build time). Only opt individual routes into on-demand rendering (`export const prerender = false`) when they need per-request data, and add an adapter (`@astrojs/node` for our Node hosting) only then.
- Fetch data in the component frontmatter at build time; never expose secrets to the client.
- Define environment variables with the `astro:env` schema (`env.schema` in the config) and mark each as `client` or `server` and `public` or `secret`.
- Use server islands (`server:defer`) for small personalized parts of an otherwise static page instead of making the whole page dynamic.

## Interactivity
- Prefer plain HTML and CSS first, then an Alpine.js directive or a `<script>` in the component.
- Use framework islands (`client:*` directives with React, Vue, Svelte etc.) only when a component is genuinely complex. Prefer `client:visible` or `client:idle` over `client:load`.
- Don't add a UI framework integration just for a single widget.

## Content
- Store Markdown/MDX and data in content collections defined in `src/content.config.ts` with loaders and a Zod schema for every collection; fail the build on invalid content.
- Use `<Image />` / `<Picture />` from `astro:assets` for images in `src/` (optimized, with `width`, `height` and `alt`); put files that must keep their URL in `public/`.
- One shared layout per page type with `<title>`, meta description, Open Graph tags, canonical link and `lang` on `<html>`.

## Styling
- Use scoped `<style>` blocks in components and the shared theme files from `assets/` (see the styling skill) for global tokens; avoid `is:global` except for content rendered from Markdown.

## Accessibility and performance
- Semantic HTML, one `<h1>` per page, keyboard-accessible controls, visible focus, WCAG 2.2 AA contrast.
- Keep the shipped JavaScript minimal; check the build output and Lighthouse scores for regressions.
- Use `<ClientRouter />` (view transitions) only when it adds value; re-initialize Alpine.js components after swaps as described in the Alpine.js instructions.

## Testing
- Unit-test helpers with Vitest (`getViteConfig` from `astro/config`); test components with the Container API where useful.
- End-to-end and accessibility checks with Playwright against `astro preview`.

## Code review focus
Flag in this order: secrets exposed to the client or missing `astro:env` schema, on-demand rendering or framework islands where static HTML would do, `client:load` without reason, content without a collection schema, images without `alt` or outside `astro:assets`, missing `site` or SEO meta tags, `astro check` errors.
