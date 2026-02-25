# Skill Builder — Anti-Patterns & Checklist

## Anti-Patterns to Avoid

### 1. Time-Sensitive Information
```markdown
# BAD
If before August 2025, use old API...

# GOOD
## Current method
Use v2 API: `api.example.com/v2/`

## Old patterns
<details>
<summary>Legacy v1 API (deprecated)</summary>
...
</details>
```

### 2. Too Many Options
```markdown
# BAD
You can use pypdf, or pdfplumber, or PyMuPDF, or...

# GOOD
Use pdfplumber for text extraction.
For scanned PDFs requiring OCR, use pdf2image with pytesseract instead.
```

### 3. Windows-Style Paths
```markdown
# BAD
scripts\helper.py

# GOOD
scripts/helper.py
```

### 4. Assuming Tools Installed
```markdown
# BAD
Use the pdf library to process the file.

# GOOD
Install required package: `pip install pypdf`
Then use it:
```python
from pypdf import PdfReader
```
```

---

## Checklist for Effective Skills

- [ ] Description is specific with trigger keywords
- [ ] Description written in third person
- [ ] SKILL.md under 500 lines
- [ ] Details in separate files (progressive disclosure)
- [ ] File references are one level deep
- [ ] Long reference files have TOC
- [ ] No time-sensitive information
- [ ] Consistent terminology
- [ ] Concrete examples provided
- [ ] Workflows have clear steps
- [ ] Scripts handle errors (don't punt to Claude)
- [ ] No Windows-style paths
- [ ] Required packages documented
- [ ] MCP tools use fully qualified names
