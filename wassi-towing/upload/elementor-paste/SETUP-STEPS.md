# Wassi Towing: header, footer and Home page setup (about 10 minutes)

**How pasting works:** open a `.txt` file, select everything (Ctrl+A) and copy it (Ctrl+C). In the Elementor editor, **right-click an empty part of the canvas → "Paste from other site"**, then press Ctrl+V in the box that appears.
The files point to the media you already uploaded, so icons and logos appear straight away.

---

## Step 1: Create the menu (Appearance → Menus)
1. Click **create a new menu** and name it exactly **Primary**.
2. Add 4 **Custom Links**, in this order:
   - Home → `https://wassitowing.ca/`
   - Services → `https://wassitowing.ca/services/`
   - About → `https://wassitowing.ca/about/`
   - FAQs → `https://wassitowing.ca/faqs/`
3. Click **Save Menu**.

## Step 2: Global CSS (Elementor → Site Settings → Custom CSS)
1. Open any page with Elementor and go to the hamburger menu (top left) → **Site Settings** → **Custom CSS**.
2. Paste the full contents of **`4-site-custom-css.css`** and click **Save Changes**.

## Step 3: Global script (Elementor → Custom Code)
1. In wp-admin, go to **Elementor → Custom Code → Add New**. Title: `Wassi Stranded mode`.
2. Set Location to **`</body> - End`**.
3. Paste the full contents of **`5-custom-code.html`** (it already includes the `<script>` tags).
4. Click **Publish**, choose the condition **Entire Site**, then **Save & Close**.

## Step 4: Header (Templates → Theme Builder → Header → Add New)
1. Name it **Wassi Header** and create it. If a template picker pops up, close it.
2. Paste **`1-header.txt`** (right-click on the canvas → Paste from other site).
3. Click **Publish**, add the condition **Entire Site**, then **Save & Close**.

## Step 5: Footer (Templates → Theme Builder → Footer → Add New)
1. Name it **Wassi Footer** and create it.
2. Paste **`2-footer.txt`**. You'll see the footer, the Stranded mode screen (dark, shown in the editor only) and the mobile sticky bar.
3. Click **Publish**, choose **Entire Site**, then **Save & Close**.

## Step 6: Home page (Pages → Home → Edit with Elementor)
1. Delete everything that's currently on the page.
2. Paste **`3-home.txt`**.
3. Click the **gear icon (Page Settings)** and set **Page Layout = Elementor Full Width**. Turn on **Hide Title** if it's there.
4. Click **Update**.

## Step 7: Make Home the front page (Settings → Reading)
Choose **Your homepage displays: A static page** → Homepage: **Home**, then click **Save**.

## Step 8: Clear the cache
1. Go to **Elementor → Tools → Regenerate CSS & Data** and click it.
2. If LiteSpeed Cache is installed, also click **Purge All**.

Then tell Claude "done", and the live page will be checked against the design at desktop and mobile sizes.
