import { QuartzConfig } from "./quartz/cfg"
import * as Plugin from "./quartz/plugins"

/**
 * Quartz 4 Configuration
 *
 * See https://quartz.jzhao.xyz/configuration for more information.
 */
const config: QuartzConfig = {
  configuration: {
    pageTitle: "Monishver’s Notes",
    pageTitleSuffix: "",
    enableSPA: true,
    enablePopovers: true,
    analytics: {
      provider: "google",
      tagId: "G-1HD0LJE1KY",
    },
    locale: "en-US",
    baseUrl: process.env.NOTES_BASE_URL ?? "monishver11.github.io/notes",
    // "goals" is personal planning, not published writing. It sits at the vault
    // root so Obsidian and the daily rollover can read it, which would
    // otherwise put it on /notes.
    // "goals.md" needs the extension: these patterns are globs against the path,
    // so a bare "goals" only matches a DIRECTORY called goals and the file
    // still published. Verified by checking for public/goals.html after build.
    ignorePatterns: ["private", "daily", "templates", ".obsidian", "goals.md"],
    defaultDateType: "modified",
    theme: {
      fontOrigin: "googleFonts",
      cdnCaching: true,
      typography: {
        header: "Source Serif 4",
        body: "Source Serif 4",
        code: "IBM Plex Mono",
      },
      colors: {
        lightMode: {
          light: "#fcfcf9",
          lightgray: "#e5e2d9",
          gray: "#8a857c",
          darkgray: "#5f5b54",
          dark: "#1c1b1a",
          secondary: "#b5533c",
          tertiary: "#96442f",
          highlight: "rgba(181, 83, 60, 0.11)",
          textHighlight: "#f5d76e66",
        },
        darkMode: {
          light: "#171614",
          lightgray: "#33312c",
          gray: "#7c786f",
          darkgray: "#a8a49b",
          dark: "#e8e6e1",
          secondary: "#d4785e",
          tertiary: "#e08f77",
          highlight: "rgba(212, 120, 94, 0.13)",
          textHighlight: "#b3aa0288",
        },
      },
    },
  },
  plugins: {
    transformers: [
      Plugin.FrontMatter(),
      Plugin.CreatedModifiedDate({
        priority: ["frontmatter", "git", "filesystem"],
      }),
      Plugin.SyntaxHighlighting({
        theme: {
          light: "github-light",
          dark: "github-dark",
        },
        keepBackground: false,
      }),
      Plugin.ObsidianFlavoredMarkdown({ enableInHtmlEmbed: false }),
      Plugin.GitHubFlavoredMarkdown(),
      Plugin.TableOfContents(),
      Plugin.CrawlLinks({ markdownLinkResolution: "shortest" }),
      Plugin.Description(),
      Plugin.Latex({ renderEngine: "katex" }),
    ],
    filters: [Plugin.RemoveDrafts()],
    emitters: [
      Plugin.AliasRedirects(),
      Plugin.ComponentResources(),
      Plugin.ContentPage(),
      Plugin.FolderPage(),
      Plugin.TagPage(),
      Plugin.ContentIndex({
        enableSiteMap: true,
        enableRSS: true,
      }),
      Plugin.Assets(),
      Plugin.Static(),
      Plugin.Favicon(),
      Plugin.NotFoundPage(),
      // Comment out CustomOgImages to speed up build time
      Plugin.CustomOgImages(),
    ],
  },
}

export default config
