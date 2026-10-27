// Convert docs/PROJECT_REPORT.md into a formatted Word document.
//
// Run (from SupportSense/):  node tools/build_report_docx.js
// Output: docs/SupportSense_Project_Report.docx
//
// Supports the Markdown used in the report: # / ## / ### headings, paragraphs,
// **bold**, *italic*, `code`, pipe tables, - bullets, 1. numbered lists, images.

const fs = require("fs");
const path = require("path");
const {
  AlignmentType, BorderStyle, Document, Footer, HeadingLevel, ImageRun, LevelFormat,
  Packer, PageBreak, PageNumber, Paragraph, ShadingType, Table, TableCell, TableRow,
  TextRun, WidthType,
} = require("docx");

const ROOT = path.resolve(__dirname, "..");
const SRC = path.join(ROOT, "docs", "PROJECT_REPORT.md");
const OUT = path.join(ROOT, "docs", "SupportSense_Project_Report.docx");

// A4 with 1-inch margins
const PAGE_W = 11906, PAGE_H = 16838, MARGIN = 1440;
const TEXT_W = PAGE_W - 2 * MARGIN; // 9026 DXA
const TEXT_W_PX = Math.round((TEXT_W / 1440) * 96); // ≈ 602 px

const BLUE = "1F3864", ACCENT = "2E75B6", LIGHT = "EAF1FB", GRID = "B4C6E7";
const FONT = "Calibri", MONO = "Consolas";

// ---------- Inline formatting: **bold**, *italic*, `code`, \* ----------
function inline(text, base = {}) {
  const runs = [];
  let buf = "", bold = false, italic = false, i = 0;
  const flush = () => {
    if (buf) runs.push(new TextRun({ text: buf, bold: bold || base.bold, italics: italic || base.italics,
                                     color: base.color, size: base.size, font: base.font }));
    buf = "";
  };
  while (i < text.length) {
    const c = text[i];
    if (c === "\\" && text[i + 1] === "*") { buf += "*"; i += 2; continue; }
    if (c === "`") {
      const end = text.indexOf("`", i + 1);
      if (end > i) {
        flush();
        runs.push(new TextRun({ text: text.slice(i + 1, end), font: MONO, bold: bold || base.bold,
                                size: base.size ? base.size - 1 : 20, color: base.color || "333333" }));
        i = end + 1; continue;
      }
    }
    if (c === "*" && text[i + 1] === "*") { flush(); bold = !bold; i += 2; continue; }
    if (c === "*") { flush(); italic = !italic; i += 1; continue; }
    buf += c; i += 1;
  }
  flush();
  return runs;
}

// ---------- Tables ----------
function splitRow(line) {
  return line.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((s) => s.trim());
}

function makeTable(lines) {
  const header = splitRow(lines[0]);
  const body = lines.slice(2).map(splitRow);
  const n = header.length;
  // Column widths proportional to the longest text in each column (with a floor)
  const plain = (s) => s.replace(/[*`\\]/g, "");
  const lens = header.map((h, c) =>
    Math.max(6, Math.min(60, Math.max(plain(h).length, ...body.map((r) => plain(r[c] || "").length)))));
  const total = lens.reduce((a, b) => a + b, 0);
  const widths = lens.map((l) => Math.floor((l / total) * TEXT_W));
  widths[n - 1] += TEXT_W - widths.reduce((a, b) => a + b, 0);

  const border = { style: BorderStyle.SINGLE, size: 4, color: GRID };
  const borders = { top: border, bottom: border, left: border, right: border };
  // keepNext on every row but the last keeps short tables on one page
  const keepTogether = body.length <= 15;
  const cell = (text, c, isHeader, shade, last) => new TableCell({
    width: { size: widths[c], type: WidthType.DXA },
    borders,
    shading: { type: ShadingType.CLEAR, color: "auto", fill: isHeader ? BLUE : shade ? LIGHT : "FFFFFF" },
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    children: [new Paragraph({
      spacing: { before: 0, after: 0 },
      keepNext: keepTogether && !last,
      children: inline(text, isHeader ? { bold: true, color: "FFFFFF", size: 19 } : { size: 19 }),
    })],
  });

  return new Table({
    width: { size: TEXT_W, type: WidthType.DXA },
    columnWidths: widths,
    rows: [
      new TableRow({ tableHeader: true, cantSplit: true,
                     children: header.map((h, c) => cell(h, c, true, false, body.length === 0)) }),
      ...body.map((r, ri) => new TableRow({
        cantSplit: true,
        children: header.map((_, c) => cell(r[c] || "", c, false, ri % 2 === 1, ri === body.length - 1)),
      })),
    ],
  });
}

// ---------- Images ----------
let figureNo = 0;
function pngSize(buf) {
  return { w: buf.readUInt32BE(16), h: buf.readUInt32BE(20) };
}
function makeImage(alt, relPath) {
  const file = path.resolve(path.dirname(SRC), relPath);
  const data = fs.readFileSync(file);
  const { w, h } = pngSize(data);
  // Wide diagrams use the full text width; squarer charts are kept smaller
  const width = w / h > 1.6 ? TEXT_W_PX : Math.round(TEXT_W_PX * 0.78);
  const height = Math.round((width * h) / w);
  figureNo += 1;
  return [
    new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { before: 160, after: 60 }, keepNext: true,
      children: [new ImageRun({ type: "png", data, transformation: { width, height },
                                altText: { title: alt, description: alt, name: alt } })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER, spacing: { after: 240 },
      children: [new TextRun({ text: `Figure ${figureNo}: ${alt}`, italics: true, size: 19, color: "555555" })],
    }),
  ];
}

// ---------- Main conversion ----------
const lines = fs.readFileSync(SRC, "utf8").split("\n");
const children = [];
let listCount = 0;

// Title page: first heading + the bold "Key: value" lines that follow it
const titleLine = lines.shift().replace(/^#\s+/, "");
const [mainTitle, subTitle] = titleLine.split(/:\s+/);
const meta = [];
while (lines.length && !lines[0].startsWith("---")) {
  const l = lines.shift().trim();
  if (l) meta.push(l.replace(/\s{2,}$/, ""));
}
children.push(
  new Paragraph({ spacing: { before: 3200, after: 120 }, alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: mainTitle, bold: true, size: 64, color: BLUE, font: FONT })] }),
  new Paragraph({ spacing: { after: 480 }, alignment: AlignmentType.CENTER,
                  children: [new TextRun({ text: subTitle || "", size: 30, color: ACCENT })] }),
  new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 1600 },
                  border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: ACCENT, space: 8 } },
                  children: [new TextRun({ text: "NLP Project Report", size: 26, color: "555555" })] }),
  ...meta.map((m) => new Paragraph({ alignment: AlignmentType.CENTER, spacing: { after: 120 },
                                     children: inline(m, { size: 24 }) })),
  new Paragraph({ children: [new PageBreak()] }),
);

let i = 0;
while (i < lines.length) {
  const line = lines[i];
  const t = line.trim();

  if (!t || t === "---") { i++; continue; }

  if (t.startsWith("### ")) {
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_2, children: inline(t.slice(4)) }));
    i++; continue;
  }
  if (t.startsWith("## ")) {
    children.push(new Paragraph({ heading: HeadingLevel.HEADING_1, children: inline(t.slice(3)) }));
    i++; continue;
  }

  const img = t.match(/^!\[(.*?)\]\((.*?)\)$/);
  if (img) { children.push(...makeImage(img[1], img[2])); i++; continue; }

  if (t.startsWith("|")) {
    const block = [];
    while (i < lines.length && lines[i].trim().startsWith("|")) block.push(lines[i++]);
    children.push(makeTable(block));
    children.push(new Paragraph({ spacing: { after: 120 }, children: [] }));
    continue;
  }

  if (/^- /.test(t)) {
    while (i < lines.length && /^- /.test(lines[i].trim())) {
      children.push(new Paragraph({ numbering: { reference: "bullets", level: 0 }, spacing: { after: 60 },
                                    children: inline(lines[i].trim().slice(2)) }));
      i++;
    }
    continue;
  }

  if (/^\d+\. /.test(t)) {
    listCount += 1; // each list restarts at 1
    while (i < lines.length && /^(\d+\. |\s+- )/.test(lines[i])) {
      const item = lines[i];
      const sub = /^\s+- /.test(item); // indented "- " = sub-bullet inside the numbered list
      children.push(new Paragraph({
        numbering: sub ? { reference: "bullets", level: 1 }
                       : { reference: "numbers", level: 0, instance: listCount },
        spacing: { after: 60 },
        children: inline(item.trim().replace(sub ? /^-\s+/ : /^\d+\.\s+/, "")),
      }));
      i++;
    }
    continue;
  }

  // Indented line = formula
  if (/^\s{2,}\S/.test(line)) {
    children.push(new Paragraph({ alignment: AlignmentType.CENTER, spacing: { before: 120, after: 120 },
                                  children: [new TextRun({ text: t, italics: true, size: 23 })] }));
    i++; continue;
  }

  // Placeholder for the team to fill in
  if (/^\*\[.*\]\*$/.test(t)) {
    children.push(new Paragraph({ spacing: { after: 160 },
      children: [new TextRun({ text: t.slice(1, -1), italics: true, color: "C00000", highlight: "yellow" })] }));
    i++; continue;
  }

  // Normal paragraph (joins consecutive non-empty lines)
  const parts = [t];
  i++;
  while (i < lines.length && lines[i].trim() && !/^(#|\||- |\d+\. |!\[|---)/.test(lines[i].trim())) {
    parts.push(lines[i].trim()); i++;
  }
  children.push(new Paragraph({ spacing: { after: 140 }, children: inline(parts.join(" ")) }));
}

const doc = new Document({
  creator: "SupportSense team",
  title: "SupportSense Project Report",
  styles: {
    default: { document: { run: { font: FONT, size: 22 }, paragraph: { spacing: { line: 276 } } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, color: BLUE, font: FONT },
        paragraph: { spacing: { before: 360, after: 160 }, outlineLevel: 0, keepNext: true,
                     border: { bottom: { style: BorderStyle.SINGLE, size: 6, color: GRID, space: 4 } } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, color: ACCENT, font: FONT },
        paragraph: { spacing: { before: 240, after: 120 }, outlineLevel: 1, keepNext: true } },
    ],
  },
  numbering: {
    config: [
      { reference: "bullets", levels: [
        { level: 0, format: LevelFormat.BULLET, text: "•",
          alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } },
        { level: 1, format: LevelFormat.BULLET, text: "–",
          alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 1260, hanging: 360 } } } },
      ] },
      { reference: "numbers", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.",
        alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 720, hanging: 360 } } } }] },
    ],
  },
  sections: [{
    properties: { page: { size: { width: PAGE_W, height: PAGE_H },
                          margin: { top: MARGIN, bottom: MARGIN, left: MARGIN, right: MARGIN } },
                  titlePage: true },
    footers: {
      default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [
        new TextRun({ text: "SupportSense — Project Report   |   Page ", size: 18, color: "777777" }),
        new TextRun({ children: [PageNumber.CURRENT], size: 18, color: "777777" }),
      ] })] }),
      first: new Footer({ children: [new Paragraph({ children: [] })] }),
    },
    children,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync(OUT, buf);
  console.log("Saved", OUT);
});
