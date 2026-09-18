# Client reporting

Version 0.6.0 adds HTML and PDF views that render only from `AuditResult`; renderers never recalculate scores,
findings, or evidence. The self-contained HTML output uses semantic headings, scoped table headers, escaped
untrusted values, responsive layout, print styles, and configurable brand colors. The PDF uses the same canonical
content with repeated page chrome, page numbers, wrapping tables and URLs, and deterministic document metadata.

Install the PDF dependency and generate reports:

```bash
python -m pip install -e ".[reports]"
svgai-marketing audit https://example.com --format html --output report.html
svgai-marketing audit https://example.com --format pdf --output report.pdf
```

`ReportBrand` configures the client name, primary color, accent color, and footer without changing audit
semantics. `examples/client_report.py` produces a multi-page synthetic PDF for local regression review.

## Verification

- HTML and PDF tests cover sparse scores, long URLs, escaped hostile values, tables, extracted content, page
  numbering, and byte-for-byte deterministic PDF output.
- Package CI imports the optional reports extra after a clean wheel installation.
- Before release, the synthetic multi-page PDF is rendered to PNG with Poppler and visually checked for clipped
  text, overlaps, table alignment, page transitions, headers, and footers.
