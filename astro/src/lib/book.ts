import bookData from "../data/book.json";

export interface BookMeta {
  title: string;
  subtitle: string;
  intro: string;
}

export interface Chapter {
  slug: string;
  partName: string;
  partIndex: number; // 1-based, front/back matter included
  chapterNumber: number | null; // running number across numbered parts; null for matter
  indexInBook: number; // 0-based position in the full flattened order
}

// Parts with a single unnamed-matter chapter (Front matter, Closing) are not
// numbered. Everything else gets a running chapter number so "Chapter 23" means
// something across the whole book.
const UNNUMBERED = new Set(["Front matter", "Closing"]);

function flatten(): Chapter[] {
  const out: Chapter[] = [];
  let chapterNumber = 0;
  bookData.parts.forEach((part, partIdx) => {
    const numbered = !UNNUMBERED.has(part.name);
    part.chapters.forEach((slug) => {
      out.push({
        slug,
        partName: part.name,
        partIndex: partIdx + 1,
        chapterNumber: numbered ? ++chapterNumber : null,
        indexInBook: out.length,
      });
    });
  });
  return out;
}

const ORDER = flatten();
const BY_SLUG = new Map(ORDER.map((c) => [c.slug, c]));

export const bookMeta: BookMeta = {
  title: bookData.title,
  subtitle: bookData.subtitle,
  intro: bookData.intro,
};

export const bookParts = bookData.parts;
export const bookChapters = ORDER;

export function chapterFor(slug: string): Chapter | undefined {
  return BY_SLUG.get(slug.toLowerCase());
}

export function prevNext(slug: string): {
  prev: Chapter | null;
  next: Chapter | null;
} {
  const c = BY_SLUG.get(slug.toLowerCase());
  if (!c) return { prev: null, next: null };
  return {
    prev: c.indexInBook > 0 ? ORDER[c.indexInBook - 1] : null,
    next: c.indexInBook < ORDER.length - 1 ? ORDER[c.indexInBook + 1] : null,
  };
}
