# Price Scraper — USD to BRL

Scrapes a product catalog from the webscraper.io test site, converts every price to
Brazilian reais using the live exchange rate from the Frankfurter API, and saves the
result to `products.csv`.

## How to install and run

Requires Python 3.14.

1. Install the dependencies:

   ```
   pip install -r requirements.txt
   ```

2. Run the script:

   ```
   python main.py
   ```

   It defaults to the `laptops` category, so no arguments are needed. To scrape a
   different category, pass `--option`:

   ```
   python main.py --option tablets
   python main.py --option phones
   ```

The script writes `products.csv` in the current directory, with the columns
`title, price_usd, price_brl, rating, reviews`, and prints a summary to the terminal.

## Technical decisions

### Pagination

I checked this before writing the scraping loop instead of assuming it. The listing has
no pagination element in the footer. The catalog returns all products in a
single request, so one request per run is enough. If it were paginated, I would have
crawled the pages in a loop until there was no "next" link.

### `exit()` vs `raise`

Both would work. I chose `exit()` because it fits the audience better: whether the user
is a client or someone on the internal team, they get a clear message about what went
wrong instead of a traceback.

### pandas vs the `csv` module

Either one would have handled the writing. I went with pandas because it is more
practical and more common in real projects and once the data is in a DataFrame, the
summary comes almost for free (`.mean()`, `.idxmax()`, `.idxmin()`) instead of creating 
new variables to store these values.

### argparse vs a terminal menu

Both are valid. argparse was new to me and I wanted to learn it, and it also turned out
to be the better fit. The script runs without asking anything in the terminal, and argparse 
rejects any category outside the list on its own.

## Bonus items implemented

- **Resilience** — connection errors, timeouts and HTTP errors are caught and reported
  with a friendly message instead of crashing.
- **Caching** — the exchange rate API is called exactly once per run, and the rate is
  reused for every product.
- **Other categories** — `--option laptops|tablets|phones` reuses the same code path.
- **Summary** — total products, average ticket in BRL, and the most expensive and
  cheapest products are printed at the end.

## What I'd do differently with more time

### Price history and alerting

The brief describes a bot that *monitors* prices, and monitoring needs memory. Right now
each run overwrites `products.csv`, so there is no way to tell if R$ 4,569 is a
drop or simply the usual price. The first thing I would add is persistence: keep every
run instead of replacing it, with a `scraped_at` column, an append to the CSV would
already work, and also a small SQLite `price_history` table would be easier to query.

With history in place, the run can compare itself to the previous one and report what
actually changed: prices that fell, products that appeared in the catalog, and products 
that disappeared from it.

For delivery I would use a Discord or Slack incoming webhook — a single `requests.post`
to a URL. I considered WhatsApp, but the official API requires a Meta
Business account, a verified number, and pre-approved templates, which is a lot of process 
for a notification that a webhook delivers in a few lines.

