export const CATEGORIES = [
  { slug: "ml-theory", label: "ML Theory" },
  { slug: "gpu-performance", label: "GPU & Performance" },
  { slug: "big-data-systems", label: "Big Data Systems" },
  { slug: "projects", label: "Projects" },
] as const;

export type CategorySlug = (typeof CATEGORIES)[number]["slug"];
