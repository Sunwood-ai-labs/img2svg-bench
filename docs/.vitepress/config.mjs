import { defineConfig } from "vitepress";

const sharedThemeConfig = {
  logo: "/logo.svg",
  outline: "deep",
  search: {
    provider: "local",
  },
  socialLinks: [{ icon: "github", link: "https://github.com/Sunwood-ai-labs/img2svg-bench" }],
  footer: {
    message: "Built for reproducible image-to-SVG benchmarking.",
    copyright: "MIT Licensed",
  },
};

const sidebar = [
  { text: "Getting Started", link: "/getting-started" },
  { text: "Benchmark Concepts", link: "/concepts" },
  { text: "Metrics & Outputs", link: "/metrics" },
  { text: "Reports", link: "/reports" },
  { text: "Contributing", link: "/contributing" },
];

const sidebarJa = [
  { text: "\u306f\u3058\u3081\u306b", link: "/ja/getting-started" },
  { text: "\u30d9\u30f3\u30c1\u30de\u30fc\u30af\u8a2d\u8a08", link: "/ja/concepts" },
  { text: "\u6307\u6a19\u3068\u51fa\u529b", link: "/ja/metrics" },
  { text: "\u30ec\u30dd\u30fc\u30c8", link: "/ja/reports" },
  { text: "\u8ca2\u732e", link: "/ja/contributing" },
];

export default defineConfig({
  title: "img2svg-bench",
  description: "A reproducible benchmark suite for image-to-SVG conversion workflows.",
  base: "/img2svg-bench/",
  lang: "en-US",
  cleanUrls: true,
  lastUpdated: true,
  head: [["link", { rel: "icon", href: "/logo.svg" }]],
  themeConfig: {
    ...sharedThemeConfig,
    nav: [{ text: "Documentation", link: "/getting-started" }],
    sidebar,
  },
  locales: {
    root: {
      label: "English",
      lang: "en-US",
      link: "/",
      themeConfig: {
        ...sharedThemeConfig,
        nav: [
          { text: "Documentation", link: "/getting-started" },
          { text: "\u65e5\u672c\u8a9e", link: "/ja/" },
        ],
        sidebar,
      },
    },
    ja: {
      label: "\u65e5\u672c\u8a9e",
      lang: "ja-JP",
      link: "/ja/",
      themeConfig: {
        ...sharedThemeConfig,
        nav: [
          { text: "\u30c9\u30ad\u30e5\u30e1\u30f3\u30c8", link: "/ja/getting-started" },
          { text: "English", link: "/" },
        ],
        sidebar: sidebarJa,
      },
    },
  },
});
