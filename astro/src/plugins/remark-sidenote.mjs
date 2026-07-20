import { visit } from "unist-util-visit";

/* Turns :sidenote[text] inline directives into numbered margin notes.
   Markup: <label> toggle + <span class="sidenote"> body, Tufte-style,
   so notes collapse to tap-to-expand on narrow screens with zero JS. */
export default function remarkSidenote() {
  return (tree) => {
    let n = 0;
    visit(tree, (node) => {
      if (node.type !== "textDirective" || node.name !== "sidenote") return;
      n += 1;
      const id = `sn-${n}`;
      node.data = {
        hName: "span",
        hProperties: { className: ["sidenote-wrap"] },
      };
      node.children = [
        {
          type: "html",
          value: `<label for="${id}" class="sidenote-number"></label><input type="checkbox" id="${id}" class="sidenote-toggle" /><span class="sidenote">`,
        },
        ...node.children,
        { type: "html", value: "</span>" },
      ];
    });
  };
}
