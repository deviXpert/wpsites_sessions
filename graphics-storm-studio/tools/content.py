"""All copy for the redesign (SEO-focused: digital marketing agency, website development,
SEO services, social media marketing, graphic design). Facts kept from the old site:
addresses, email, phone, Instagram, team names, counters, testimonials."""

BRAND = 'Graphics Storm Studio'
EMAIL = 'info@graphicsstormstudio.com'
PHONE_DISPLAY = '+1 (812) 818-2053'
PHONE_TEL = 'tel:+18128182053'
WHATSAPP = 'https://wa.me/18128182053'
INSTAGRAM = 'https://www.instagram.com/graphics_storm/'
OFFICES = [('Canada', '1 Deauville Ln, North York, ON M3C 1Z7, Canada'),
           ('USA', '2501 Chatham Rd, Suite R, Springfield, IL 62704, USA')]

URL = {'home': '/', 'reviews': '/reviews/', 'about': '/about-us/', 'services': '/services/', 'work': '/our-portfolio/', 'contact': '/contact-us/',
       'web': '/website-development/', 'seo': '/search-engine-optimization/', 'smm': '/social-media-marketing/',
       'design': '/graphics-designing/'}

STATS = [(514, 'Projects delivered last month'), (180, 'Websites developed'), (130, 'Happy clients'), (5, 'Years of experience')]

TESTIMONIALS = [  # from the old site (photos removed – they were hot-linked from another domain)
 ('Mr. James', 'Brand identity client', 'The brand guidelines and logos were absolutely fantastic! They have transformed my brand and will help me scale up for more business. Great communication and very speedy delivery – ahead of schedule.'),
 ('Anthony', 'Website client', 'Working with [the team] was very pleasant and professional. Communication was fast and I am more than satisfied with the result. Looking forward to the next project.'),
 ('Lisa P.', 'Marketing client', 'My first time working with [Graphics Storm Studio] and it has been a pleasure. Brief well met, clear communication and fast delivery. Not much more you can ask for.'),
 ('Patrick', 'Design client', 'Wonderful experience as always – so happy with the final product. Highly recommend!'),
]

SERVICES_GRID = [
 ('fas fa-laptop-code', 'Website Development', 'Fast, mobile-first WordPress websites engineered to rank on Google and turn visitors into enquiries.', URL['web']),
 ('fas fa-search-dollar', 'Search Engine Optimization', 'Technical SEO, content and local SEO that put you on page one for the searches your customers make.', URL['seo']),
 ('fas fa-hashtag', 'Social Media Marketing', 'Scroll-stopping content and paid social campaigns on Instagram, Facebook, TikTok and LinkedIn.', URL['smm']),
 ('fas fa-pen-nib', 'Graphic Design', 'Social creatives, brochures, packaging and ad designs that make your brand impossible to ignore.', URL['design']),
 ('fas fa-bezier-curve', 'Logo & Brand Identity', 'Memorable logos and complete brand guidelines that build trust from the very first impression.', URL['design']),
 ('fas fa-bullhorn', 'Paid Advertising (PPC)', 'Google Ads and Meta Ads campaigns tracked to the lead – so every dollar is accountable.', URL['contact']),
]

HOME_FAQ = [
 ('What does a digital marketing agency do?', 'A digital marketing agency plans and runs the online activity that brings you customers – your website, search engine optimization (SEO), social media marketing, paid ads and the design that ties it together. At Graphics Storm Studio one team handles all of it, so your brand and results stay consistent.'),
 ('How much do your digital marketing services cost?', 'Every business is different, so we quote after a free strategy call. We offer one-off projects (for example a new website or logo) and flexible monthly plans for SEO and social media marketing – with no long lock-in contracts.'),
 ('How long does SEO take to show results?', 'Most clients see early ranking and traffic gains within 8–12 weeks, with stronger, compounding results after 4–6 months. We report progress monthly so you always know what has been done and what it achieved.'),
 ('How long does it take to build a website?', 'A typical business website takes 3–6 weeks from kickoff to launch, depending on the number of pages and features. You get a clear timeline before we start and a staging link to review along the way.'),
 ('Do you work with clients outside the USA and Canada?', 'Yes. We have offices in Springfield (IL, USA) and North York (ON, Canada) and work remotely with businesses worldwide.'),
]

PROCESS = [
 ('01', 'Discover', 'We learn your business, audience and competitors, and audit your current website, SEO and social channels.'),
 ('02', 'Strategy', 'You get a clear, prioritised plan with goals, channels, timelines and the KPIs we will be measured on.'),
 ('03', 'Create & Launch', 'Our designers, developers and marketers build and launch – with your approval at every milestone.'),
 ('04', 'Measure & Grow', 'We track leads and sales, report monthly and keep optimising what works to compound your growth.'),
]

WHY = [
 ('fas fa-chart-line', 'Results you can measure', 'Every campaign is tied to clear KPIs – traffic, leads and revenue – with honest monthly reporting.'),
 ('fas fa-users', 'One dedicated team', 'Strategists, designers, developers and marketers under one roof, with one point of contact.'),
 ('fas fa-hand-holding-usd', 'Budget-friendly plans', 'Premium quality without agency bloat – flexible plans that grow with your business.'),
 ('fas fa-clock', 'On-time delivery', 'Agreed timelines, fast communication and no surprises. We do what we say, when we say it.'),
]

SERVICE_PAGES = {
 'web': dict(
  slug='website-development', info='gss-website-development.svg', title='Website Development',
  meta_title='Website Development Services | Custom WordPress Websites – Graphics Storm Studio',
  meta_desc='Professional website development services: fast, mobile-friendly, SEO-ready WordPress websites that turn visitors into leads. Get a free quote today.',
  eyebrow='Website Development Services',
  h1='Websites That Look Premium and <span>Win You Customers</span>',
  lead='We design and develop fast, mobile-first WordPress websites that are built to rank on Google, load in under two seconds and turn visitors into enquiries.',
  included=['Custom UI/UX design – no generic templates', 'Mobile-first, fully responsive build', 'On-page SEO & schema built in', 'Speed & Core Web Vitals optimisation', 'Contact forms, WhatsApp & analytics setup', 'Training + 30 days of free support'],
  benefits=[('fas fa-tachometer-alt', 'Lightning fast', 'Optimised images, clean code and caching for top PageSpeed scores and lower bounce rates.'),
            ('fas fa-mobile-alt', 'Mobile-first', 'Over 60% of visits are on phones – every layout is designed and tested for small screens first.'),
            ('fas fa-search', 'SEO-ready', 'Clean heading structure, meta data, schema and sitemaps so Google understands every page.')],
  features=[('fas fa-store', 'Business websites', 'Credible multi-page sites that explain what you do and why customers should choose you.'),
            ('fas fa-shopping-cart', 'eCommerce stores', 'WooCommerce shops with secure checkout, payment gateways and easy product management.'),
            ('fas fa-rocket', 'Landing pages', 'High-converting pages for ads and campaigns, built for A/B testing.'),
            ('fas fa-sync-alt', 'Website redesigns', 'Modernise an outdated site without losing your Google rankings.'),
            ('fas fa-shield-alt', 'Security & care plans', 'Updates, backups, uptime monitoring and malware protection.'),
            ('fas fa-universal-access', 'Accessibility', 'WCAG-friendly colour contrast, keyboard navigation and readable typography.')],
  faq=[('How much does a website cost?', 'Most business websites fall between a small starter site and a larger custom build. After a short call we send a fixed quote with no hidden costs.'),
       ('Which platform do you use?', 'We mainly build on WordPress with Elementor, so you can easily edit content yourself. For online stores we use WooCommerce.'),
       ('Will my website be mobile-friendly and SEO-ready?', 'Yes. Every website is responsive, speed-optimised and includes on-page SEO basics like titles, meta descriptions, headings and schema.'),
       ('Do you offer maintenance after launch?', 'Yes – every site includes 30 days of free support, and optional monthly care plans cover updates, backups and security.')]),
 'seo': dict(
  slug='search-engine-optimization', info='gss-seo-services.svg', title='Search Engine Optimization',
  meta_title='SEO Services That Rank | Search Engine Optimization Agency – Graphics Storm Studio',
  meta_desc='Results-driven SEO services: technical SEO, keyword research, content and local SEO that grow organic traffic and leads. Get your free SEO audit.',
  eyebrow='SEO Services',
  h1='SEO Services That Put You on <span>Page One of Google</span>',
  lead='Stop paying for every click. Our search engine optimization services grow the free, high-intent traffic that turns into calls, leads and sales – month after month.',
  included=['Full technical SEO audit', 'Keyword & competitor research', 'On-page optimisation & content', 'Local SEO & Google Business Profile', 'Quality link building', 'Monthly ranking & traffic reports'],
  benefits=[('fas fa-bullseye', 'High-intent traffic', 'Rank for the searches people make when they are ready to buy, not just browse.'),
            ('fas fa-chart-line', 'Compounding growth', 'Unlike ads, rankings keep working for you long after the work is done.'),
            ('fas fa-file-alt', 'Transparent reporting', 'Clear monthly reports on rankings, traffic and leads – in plain English.')],
  features=[('fas fa-cogs', 'Technical SEO', 'Site speed, indexing, crawl errors, Core Web Vitals and structured data fixed properly.'),
            ('fas fa-key', 'Keyword strategy', 'Data-led keyword mapping so every page targets the right search terms.'),
            ('fas fa-pen-fancy', 'SEO content', 'Helpful, expert content and service pages that rank and convert.'),
            ('fas fa-map-marker-alt', 'Local SEO', 'Google Business Profile, citations and reviews to win the map pack.'),
            ('fas fa-link', 'Link building', 'White-hat outreach that earns authority from relevant websites.'),
            ('fas fa-store', 'eCommerce SEO', 'Category and product optimisation that grows online store revenue.')],
  faq=[('How long does SEO take?', 'Expect early movement in 8–12 weeks and strong results in 4–6 months. Competitive keywords can take longer – we set realistic targets up front.'),
       ('Do you guarantee #1 rankings?', 'No honest agency can guarantee a #1 position – Google controls the rankings. We guarantee transparent, best-practice work and measurable progress.'),
       ('Is local SEO included?', 'Yes. For businesses serving a local area we optimise your Google Business Profile, local citations and location pages.'),
       ('Will I own the content and reports?', 'Absolutely. All content, data and accounts are yours.')]),
 'smm': dict(
  slug='social-media-marketing', info='gss-social-media-marketing.svg', title='Social Media Marketing',
  meta_title='Social Media Marketing Agency | Content & Paid Social – Graphics Storm Studio',
  meta_desc='Social media marketing services for Instagram, Facebook, TikTok and LinkedIn: content creation, community management and paid ads that grow your brand.',
  eyebrow='Social Media Marketing',
  h1='Social Media Marketing That <span>Builds Brands & Sales</span>',
  lead='From scroll-stopping content to targeted paid campaigns, we grow an engaged audience on the platforms your customers use every day – and turn followers into customers.',
  included=['Social media strategy & content calendar', 'Custom post, reel & story designs', 'Captions, hashtags & scheduling', 'Community management', 'Meta, TikTok & LinkedIn ads', 'Monthly analytics report'],
  benefits=[('fas fa-eye', 'More brand awareness', 'Consistent, on-brand content keeps you top-of-mind with your ideal customers.'),
            ('fas fa-comments', 'Real engagement', 'We start conversations and build communities, not just follower counts.'),
            ('fas fa-hand-holding-usd', 'Paid social ROI', 'Precise targeting and creative testing to lower cost per lead.')],
  features=[('fab fa-instagram', 'Instagram marketing', 'Reels, carousels and stories designed to grow reach and engagement.'),
            ('fab fa-facebook-f', 'Facebook marketing', 'Page management and lead-generation ad campaigns.'),
            ('fab fa-tiktok', 'TikTok content', 'Short-form video concepts that ride trends and build awareness.'),
            ('fab fa-linkedin-in', 'LinkedIn for B2B', 'Thought-leadership content and B2B lead generation.'),
            ('fas fa-ad', 'Paid social ads', 'Full-funnel campaigns with pixel tracking and retargeting.'),
            ('fas fa-chart-pie', 'Analytics & insights', 'Clear reporting on reach, engagement, leads and sales.')],
  faq=[('Which platforms should my business be on?', 'It depends on your audience. We usually recommend two or three platforms done well over being everywhere – we will advise during your free strategy call.'),
       ('Do you create the content?', 'Yes. Our designers and copywriters create posts, reels, stories and ad creatives in your brand style.'),
       ('How many posts per month do I get?', 'Plans are flexible – typically 12 to 30 pieces of content per month across your chosen platforms.'),
       ('Is ad spend included?', 'Ad spend is paid directly to the platform, so you keep full control and transparency. Our fee covers strategy, creative and management.')]),
 'design': dict(
  slug='graphics-designing', info='gss-graphic-design.svg', title='Graphic Design',
  meta_title='Graphic Design & Logo Design Services | Graphics Storm Studio',
  meta_desc='Creative graphic design services: logo design, brand identity, social media graphics, print and packaging design that make your brand stand out.',
  eyebrow='Graphic Design Services',
  h1='Graphic Design That Makes Your <span>Brand Unforgettable</span>',
  lead='Logos, brand identities, social creatives and print design crafted by experienced designers – so your business looks as good as it really is, everywhere it shows up.',
  included=['Logo design with multiple concepts', 'Brand guidelines (colours, fonts, usage)', 'Social media post & ad designs', 'Brochures, flyers & business cards', 'Packaging & label design', 'Unlimited revisions on concepts'],
  benefits=[('fas fa-lightbulb', 'Original ideas', 'Every design starts from research and strategy – never from a template.'),
            ('fas fa-layer-group', 'Consistent brand', 'A cohesive look across web, social and print builds recognition and trust.'),
            ('fas fa-bolt', 'Fast turnaround', 'Clear briefs and quick feedback rounds keep your projects moving.')],
  features=[('fas fa-bezier-curve', 'Logo design', 'Distinctive, scalable logos delivered in every file format you need.'),
            ('fas fa-swatchbook', 'Brand identity', 'Colour palettes, typography and brand guidelines for consistent use.'),
            ('fas fa-hashtag', 'Social media graphics', 'Post, story and ad templates designed for engagement.'),
            ('fas fa-book-open', 'Print design', 'Brochures, flyers, business cards, banners and signage.'),
            ('fas fa-box-open', 'Packaging design', 'Shelf-ready packaging and labels that sell your product.'),
            ('fas fa-desktop', 'UI & web graphics', 'Website banners, icons and illustrations that fit your brand.')],
  faq=[('How many logo concepts will I get?', 'Our logo packages include multiple initial concepts and revision rounds, so you can refine your favourite until it is perfect.'),
       ('What files do I receive?', 'You receive print and web-ready files – AI, EPS, SVG, PDF and PNG – plus colour codes and fonts.'),
       ('Do I own the copyright?', 'Yes. Once the project is complete, full ownership of the final designs transfers to you.'),
       ('Can you redesign my existing logo?', 'Yes – we can modernise your current logo while keeping the recognition you have already built.')]),
}

ABOUT = dict(
 meta_title='About Graphics Storm Studio | Creative Digital Marketing Agency',
 meta_desc='Meet Graphics Storm Studio – a design-led digital marketing agency in the USA and Canada helping businesses grow with websites, SEO, social media and branding.',
 h1='A Design-Led Digital Marketing Agency Built for <span>Growth</span>',
 lead='Graphics Storm Studio helps ambitious businesses grow online through strategic websites, SEO, social media marketing and brand design – all under one roof.',
 story_h2='We Combine Creative Design With <span>Data-Driven Marketing</span>',
 story=('<p>Graphics Storm Studio started with a big idea: build a creative agency that delivers purposeful, measurable work for the dreamers, doers and builders of the world.</p>'
        '<p>Today our team of strategists, designers, developers and marketers helps businesses in the USA, Canada and beyond turn their brand into a growth engine – from the first logo sketch to page-one rankings and campaigns that sell.</p>'),
 timeline=[('fas fa-flag', 'Where it began', 'A small studio with a design-first mindset and a promise to treat every client’s business like our own.'),
           ('fas fa-seedling', 'How we evolved', 'We added web development, SEO and social media so clients could grow with one trusted partner.'),
           ('fas fa-gem', 'Where we are today', 'A full-service digital marketing agency known for premium design, honest reporting and on-time delivery.')],
 ceo_quote='My idea behind Graphics Storm Studio was to build a state-of-the-art digital agency that transforms businesses, solves real challenges and celebrates every client win as our own.',
 ceo='Nabeel Ali Butt', ceo_role='Founder & CEO',
 values=[('fas fa-smile', 'Client satisfaction', 'We are not done until you are delighted with the result.'),
         ('fas fa-comments', 'Clear communication', 'Fast replies, regular updates and plain-English reports.'),
         ('fas fa-user-tie', 'Team of experts', 'Specialists in design, development, SEO and social media.'),
         ('fas fa-gem', 'Premium designs', 'Original, modern work that makes your brand stand out.'),
         ('fas fa-briefcase', 'Professional service', 'Clear processes, contracts and timelines on every project.'),
         ('fas fa-shipping-fast', 'On-time delivery', 'We respect your deadlines as much as you do.')],
 team=[('Fahad Mustafa Butt', 'CEO'), ('Nabeel Ali Butt', 'Creative Director'), ('Saba Baig', 'Project Manager'),
       ('Isha Tariq', 'Content Manager'), ('Muhammad Usman', 'Graphic Designer')],
)

PAGES_META = {
 'home': ('Digital Marketing Agency USA & Canada | Graphics Storm Studio',
          'Graphics Storm Studio is a results-driven digital marketing agency offering website development, SEO services, social media marketing and graphic design. Get a free proposal.'),
 'work': ('Our Work | Website, SEO & Design Portfolio – Graphics Storm Studio',
          'Explore our portfolio of websites, branding, social media and SEO projects for growing businesses in the USA, Canada and worldwide.'),
 'contact': ('Contact Graphics Storm Studio | Get a Free Digital Marketing Proposal',
             'Talk to our digital marketing team about websites, SEO, social media or design. Call +1 (812) 818-2053, email us or request a free proposal online.'),
 'services': ('Digital Marketing Services | Web, SEO, Social & Design – Graphics Storm Studio',
              'Explore our digital marketing services: website development, SEO, social media marketing, graphic design, branding and paid ads.'),
}
