# grass-stats

GRASS GIS and R: the GRASS-R interface and statistics in GRASS

Automated mbox archive. Updated daily via GitHub Actions.

## Structure

- `raw/` - Monthly .mbox files downloaded from [https://lists.osgeo.org/pipermail/grass-stats/](https://lists.osgeo.org/pipermail/grass-stats/)
- `processed/` - Structured JSON output from rmail-parser
- `tools/fix-rebuilt-dates.py` - run once on the files up to November 2007: the list's move to lists.osgeo.org wrote that month into the Date line of almost every earlier message, and this put back each one's date from its envelope line. It also escaped the few lines of text that start with "From ".
- `sources/` - Where present, each message's page at the source and the characters that page restores, one JSON file per period
- `attachments/` - Text Mailman scrubbed out of messages, fetched once from the source and put back by rmail-parser, one gzip-compressed JSON file per period
- `meta.json` - List statistics

## Viewer

Browse these archives at [r-mailing-lists.thecoatlessprofessor.com](https://r-mailing-lists.thecoatlessprofessor.com/lists/grass-stats/)
