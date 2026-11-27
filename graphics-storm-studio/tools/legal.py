"""Privacy Policy + Terms of Service for graphicsstormstudio.com, written from what the site and
business actually do (forms, Elementor Submissions, WP Mail SMTP, Tidio, reCAPTCHA, Google Fonts,
Google Tag Manager/Analytics, Hostinger, WhatsApp links; agency services and the promises on the site).
NOT legal advice – the owner should have a lawyer review before relying on it."""
import content as K

UPDATED = 'November 27, 2026'
CONTACT = (f'<p><strong>Graphics Storm Studio</strong><br>Email: <a href="mailto:{K.EMAIL}">{K.EMAIL}</a><br>'
           f'Phone: <a href="{K.PHONE_TEL}">{K.PHONE_DISPLAY}</a><br>'
           + '<br>'.join(f'{c} office: {a}' for c, a in K.OFFICES) + '</p>')

PRIVACY = [
 ('who-we-are', 'Who we are', f'''<p>This Privacy Policy explains how Graphics Storm Studio (“<strong>we</strong>”, “<strong>us</strong>”, “<strong>our</strong>”) collects, uses and protects personal information when you visit <strong>graphicsstormstudio.com</strong> (the “Website”), contact us, or use our digital marketing services – including website development, search engine optimization (SEO), social media marketing, graphic design, branding and paid advertising.</p>
<p>We have offices in the United States and Canada and work with clients worldwide. We are responsible for the personal information described in this policy. If you have any questions, contact us using the details in the “Contact us” section below.</p>'''),
 ('information-we-collect', 'Information we collect', '''<p><strong>Information you give us</strong></p>
<ul><li><strong>Enquiry and quote forms:</strong> your name, email address, phone/WhatsApp number, website address, monthly budget range, the services you are interested in, and anything you write in the message field.</li>
<li><strong>Email, phone, WhatsApp and live chat:</strong> the content of your messages and the contact details you use.</li>
<li><strong>Client projects:</strong> business details, billing information, brand assets, content, logins or access you share so we can deliver your project.</li></ul>
<p><strong>Information collected automatically</strong></p>
<ul><li><strong>Technical data:</strong> IP address, browser and device type, operating system, pages visited, referring website and the date and time of your visit, collected through server logs, security tools and (where enabled) analytics.</li>
<li><strong>Cookies and similar technologies:</strong> see “Cookies” below.</li></ul>
<p>Our forms include a hidden anti-spam field and may use Google reCAPTCHA to tell people from bots. We do not knowingly collect sensitive personal information, and we ask you not to send it through our forms.</p>'''),
 ('how-we-use', 'How we use your information', '''<ul><li>To reply to your enquiry, prepare proposals and quotes, and arrange strategy calls.</li>
<li>To deliver, manage and support the services you buy from us, including project communication and invoicing.</li>
<li>To operate, secure and improve the Website – for example, preventing spam and abuse and understanding which pages are useful.</li>
<li>To send you information you have asked for. We only send marketing emails if you have agreed or where the law allows, and every marketing email includes a way to unsubscribe.</li>
<li>To meet legal, accounting and tax obligations, and to establish or defend legal claims.</li></ul>
<p><strong>Legal bases (for visitors in the EU/UK):</strong> we process personal data to take steps at your request before entering into a contract and to perform a contract; for our legitimate interests in running and securing our business and Website; with your consent (for example, non-essential cookies or marketing); and to comply with legal obligations.</p>'''),
 ('sharing', 'How we share information', '''<p>We do <strong>not sell or rent</strong> your personal information, and we do not share it for cross-context behavioural advertising. We share it only with trusted service providers who help us run our business, and only as needed:</p>
<ul><li><strong>Website hosting:</strong> Hostinger (servers and backups).</li>
<li><strong>Email delivery:</strong> our email provider, via WP Mail SMTP, to send form notifications and replies.</li>
<li><strong>Live chat:</strong> Tidio, if you use the chat widget.</li>
<li><strong>Spam protection:</strong> Google reCAPTCHA.</li>
<li><strong>Analytics:</strong> Google Analytics / Google Tag Manager, where enabled.</li>
<li><strong>Messaging:</strong> WhatsApp (Meta), if you choose to contact us there.</li>
<li><strong>Project tools:</strong> platforms you ask us to use for your project, such as ad accounts, social media platforms or your website host.</li>
<li><strong>Professional advisers and authorities:</strong> accountants, lawyers, or authorities when the law requires it, or to protect our rights, safety or property.</li>
<li><strong>Business transfers:</strong> a buyer or successor if our business is reorganised, merged or sold.</li></ul>
<p>These providers may process information in the United States, Canada or other countries. Where required, we rely on appropriate safeguards (such as standard contractual clauses) for international transfers.</p>'''),
 ('cookies', 'Cookies', '''<p>Cookies are small files stored on your device. We use:</p>
<ul><li><strong>Essential cookies:</strong> needed for the Website to work and stay secure, for example security and form protection.</li>
<li><strong>Functional cookies:</strong> to remember chat conversations (Tidio).</li>
<li><strong>Analytics cookies:</strong> to understand how visitors use the Website (Google Analytics, where enabled). Where the law requires it, we ask for your consent first.</li></ul>
<p>The Website also loads fonts from Google Fonts, and Google receives your IP address when the fonts load. You can block or delete cookies in your browser settings; some parts of the Website may not work properly if you do.</p>'''),
 ('retention', 'How long we keep information', '''<p>We keep enquiry and form submissions for up to <strong>24 months</strong> after our last contact, unless you become a client. Client project and billing records are kept for as long as needed to provide the services and then for the period required by tax and accounting laws (usually up to 7 years). After that, we delete or anonymise the information.</p>'''),
 ('security', 'How we protect information', '''<p>We use reasonable technical and organisational measures to protect personal information. These include encrypted HTTPS connections, access limited to authorised staff, security monitoring and regular software updates. No method of transmission or storage is 100% secure, so we cannot guarantee absolute security. If a breach affects your rights, we will notify you and the relevant authorities where the law requires.</p>'''),
 ('your-rights', 'Your privacy rights', '''<p>Depending on where you live, you may have the right to:</p>
<ul><li>access the personal information we hold about you and get a copy;</li><li>correct inaccurate information;</li>
<li>delete your information, subject to legal exceptions;</li><li>withdraw consent or object to certain processing, including direct marketing;</li>
<li>restrict processing or receive your data in a portable format (EU/UK);</li><li>not be discriminated against for using your rights (California).</li></ul>
<p><strong>Canada:</strong> we handle personal information in line with the Personal Information Protection and Electronic Documents Act (PIPEDA). <strong>California:</strong> California residents have rights under the CCPA/CPRA; we do not sell or share personal information as defined by that law. <strong>EU/UK:</strong> you may also complain to your local data protection authority.</p>
<p>To use any of these rights, email <a href="mailto:info@graphicsstormstudio.com">info@graphicsstormstudio.com</a>. We may need to verify your identity, and we will respond within the time the law requires (usually 30 days).</p>'''),
 ('children', 'Children', '''<p>Our Website and services are meant for businesses and adults. We do not knowingly collect personal information from children under 16. If you believe a child has sent us information, contact us and we will delete it.</p>'''),
 ('third-party-links', 'Third-party links', '''<p>The Website links to other sites and platforms, such as Instagram, Facebook, LinkedIn and WhatsApp. Their own privacy policies apply, and we are not responsible for how they handle your information.</p>'''),
 ('changes', 'Changes to this policy', f'''<p>We may update this Privacy Policy from time to time. The “Last updated” date at the top shows when it last changed. If we make significant changes, we will make that clear on the Website.</p>'''),
 ('contact', 'Contact us', f'''<p>For privacy questions or requests, contact us at:</p>{CONTACT}'''),
]

TERMS = [
 ('agreement', 'Agreement to these terms', '''<p>These Terms of Service (“<strong>Terms</strong>”) apply to your use of <strong>graphicsstormstudio.com</strong> (the “Website”) and to the digital marketing services provided by Graphics Storm Studio (“<strong>we</strong>”, “<strong>us</strong>”, “<strong>our</strong>”). By using the Website or engaging our services you agree to these Terms. If a signed proposal, quote or statement of work (“<strong>Proposal</strong>”) says something different, the Proposal takes priority for that project.</p>'''),
 ('services', 'Our services', '''<p>We provide website development, search engine optimization (SEO), social media marketing, graphic design, logo and brand identity, and paid advertising management. The scope, deliverables, timeline and fees for each project are set out in your Proposal. Work outside the agreed scope is quoted separately before we start it.</p>'''),
 ('quotes-payment', 'Quotes, fees and payment', '''<ul><li>Quotes are valid for 30 days unless stated otherwise.</li>
<li>One-off projects usually need a deposit before work starts, with the balance due at the milestones or on the dates in your Proposal.</li>
<li>Monthly services (such as SEO or social media management) are billed in advance and continue month to month unless your Proposal sets a minimum term.</li>
<li>Invoices are due within the time stated on the invoice. We may pause work on overdue accounts.</li>
<li><strong>Advertising spend</strong> on Google, Meta, TikTok, LinkedIn or other platforms is paid by you directly to the platform and is separate from our management fees.</li>
<li>Third-party costs you approve, such as domains, hosting, premium plugins, stock images or fonts, are your responsibility unless your Proposal says otherwise.</li></ul>'''),
 ('client-responsibilities', 'Your responsibilities', '''<ul><li>Provide accurate information, content, feedback and approvals on time. Delays on your side may move the project timeline.</li>
<li>Give us the access we need (for example to your website, hosting, analytics, ad or social media accounts) and keep your own login details secure.</li>
<li>Make sure you have the rights to any text, images, logos or other materials you give us. You are responsible for claims arising from those materials.</li>
<li>Make sure your products, services and advertising claims comply with the law and platform policies.</li></ul>'''),
 ('revisions-approval', 'Revisions and approvals', '''<p>Each Proposal states the number of revision rounds included. Additional revisions or changes after approval may be charged at our standard rates. A deliverable counts as approved when you confirm it in writing, or when it is launched or used.</p>'''),
 ('intellectual-property', 'Ownership and intellectual property', '''<ul><li><strong>Final deliverables:</strong> once we receive full payment, ownership of the final approved deliverables created for you (such as your logo, designs and website content) transfers to you.</li>
<li><strong>Our tools and know-how:</strong> we keep ownership of our pre-existing materials, templates, code libraries, processes and know-how. You receive a licence to use any that are part of your deliverables.</li>
<li><strong>Third-party items</strong> (such as WordPress, plugins, fonts and stock images) remain subject to their own licences.</li>
<li>Unused concepts and drafts stay our property unless agreed otherwise.</li>
<li><strong>Portfolio:</strong> unless you ask us not to in writing, we may show completed work and your business name in our portfolio and marketing.</li></ul>'''),
 ('results', 'Results and guarantees', '''<p>We work hard to grow your business and use industry best practices, but marketing results depend on many factors outside our control. These include search engine and social media algorithms, competition, market conditions and your own products and pricing. <strong>We do not guarantee specific rankings (including a #1 position on Google), traffic, leads, sales or return on ad spend.</strong> Any figures on the Website, including statistics and infographics, are examples and do not promise future results.</p>'''),
 ('support-maintenance', 'Website support and maintenance', '''<p>New websites include <strong>30 days of free support</strong> after launch to fix defects in our work. After that, updates, backups, security monitoring and changes are covered by an optional care plan or billed separately. We are not responsible for problems caused by changes made by you or others, by third-party plugins or hosting, or by updates we were not engaged to manage.</p>'''),
 ('confidentiality', 'Confidentiality', '''<p>We each agree to keep the other’s confidential business information private and to use it only for the project. This does not cover information that is public, already known, or that must be disclosed by law. How we handle personal information is described in our <a href="/privacy-policy/">Privacy Policy</a>.</p>'''),
 ('cancellation', 'Cancellation and refunds', '''<ul><li>Either party may end monthly services with <strong>30 days’ written notice</strong>, unless your Proposal sets a minimum term.</li>
<li>If a one-off project is cancelled, you pay for work completed up to the cancellation date. Deposits cover scheduling and initial work and are non-refundable once work has started.</li>
<li>We may suspend or end services if invoices remain unpaid or if these Terms are seriously breached.</li></ul>'''),
 ('website-use', 'Using this website', '''<p>You may use the Website for lawful purposes only. You must not try to break its security, interfere with its operation, send spam through our forms, or copy its content, design or code for commercial use without our permission. The Website and its content (excluding client work shown with permission) belong to Graphics Storm Studio. Links to third-party websites are provided for convenience, and we are not responsible for their content.</p>'''),
 ('liability', 'Limitation of liability', '''<p>To the fullest extent permitted by law, the Website is provided “as is”. We are not liable for any indirect, incidental, special or consequential losses, including lost profits, revenue, data or business opportunities. Our total liability for any claim relating to a project is limited to the fees you paid us for that project (or, for monthly services, the fees paid in the three months before the claim). Nothing in these Terms limits liability that cannot be limited by law.</p>'''),
 ('indemnity', 'Indemnity', '''<p>You agree to compensate us for claims, losses and costs arising from materials you supply, from your products, services or advertising claims, or from your breach of these Terms.</p>'''),
 ('governing-law', 'Governing law', '''<p>These Terms are governed by the laws of the State of Illinois, USA, for clients in the United States, and by the laws of the Province of Ontario, Canada, for clients in Canada. For clients elsewhere, they are governed by the laws of the State of Illinois, USA. The courts of those places have jurisdiction. Before going to court, we both agree to try to resolve any dispute informally and in good faith.</p>'''),
 ('changes', 'Changes to these terms', '''<p>We may update these Terms from time to time. The version shown on this page, with its “Last updated” date, applies from that date. Signed Proposals continue under the Terms that applied when they were signed, unless we both agree otherwise.</p>'''),
 ('contact', 'Contact us', f'''<p>Questions about these Terms? Contact us:</p>{CONTACT}'''),
]
