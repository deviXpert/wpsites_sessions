"""Career (page 693). Elementor Pro form keeps the original recruitment fields (cleaned)."""
from lib import *
TITLE = 'Career'
SEO = ('Translator Jobs & Careers | Join Pak Translations Linguist Team',
       'Freelance translator, editor, transcriber, subtitler and content writer jobs at Pak Translations. Apply online to join our network of quality-focused linguists.',
       'translator jobs')

def build():
    seed('career')
    hero = phero('Career', 'Careers for Translators &amp; <span class="x-hl">Language Professionals</span>',
                 'We are always looking for quality-oriented, responsive and honest linguists. If that sounds like you, apply below and join our growing network.',
                 [BTN('Apply Now', '#apply', 'x-btn', 'arrow-down')])
    roles = [('language', 'Translators', 'Native-speaker translators in any of our 120+ languages.'),
             ('spell-check', 'Editors &amp; Proofreaders', 'Detail-obsessed reviewers who make text flawless.'),
             ('headphones', 'Transcribers', 'Accurate, time-coded transcription of audio and video.'),
             ('closed-captioning', 'Subtitlers', 'Precise subtitle creation and translation (SRT and more).'),
             ('pen-nib', 'Content Writers', 'Creative writers for blogs, ads and social media.'),
             ('comments', 'Interpreters', 'Consecutive and simultaneous interpreting skills.'),
             ('object-group', 'DTP Specialists', 'Typesetting and layout, including RTL scripts.'),
             ('project-diagram', 'Linguists', 'Phonetics, tagging, corpus and TTS data work.')]
    who = sec([head('Who We Are Looking For', 'Open Roles in Our <span class="x-hl">Linguist Network</span>', 'Remote, project-based work with a team that values quality and fair collaboration.'),
               C([IBOX(i, t, d, 'x-card x-svc x-nomore', tag='h3') for i, t, d in roles], 'x-g4 rv-st', 'grid')], 'x-bg')
    steps = [('paper-plane', 'Apply', 'Submit the form below with your CV and details. Write “N/A” for fields that do not apply.'),
             ('user-check', 'HR Review', 'Our HR team reviews your profile against current requirements.'),
             ('clipboard-check', 'Screening', 'Translators take a short test (under 200 words); writers and editors share work samples.'),
             ('handshake', 'Onboarding', 'Successful candidates are added to our team and contacted for relevant projects.')]
    how = steps_sec('Hiring Process', 'How Our <span class="x-hl">Recruitment</span> Works', 'A simple, transparent four-step process.', steps)
    f = lambda cid, t, label, req=False, w='50', **kw: F(cid, t, label, '', req, w, **kw)
    form = FORM('Career Application', [
        f('name', 'text', 'Full name', True), f('email', 'email', 'Email address', True),
        f('phone', 'tel', 'Phone number'), f('country', 'text', 'Country'),
        f('education', 'select', 'Education', True, field_options='Bachelors\nMasters\nMPhil\nPhD\nOther'), f('experience', 'text', 'Years of experience', True),
        f('input_language_1', 'text', 'Source language 1', True), f('input_language_2', 'text', 'Source language 2'),
        f('input_language_3', 'text', 'Source language 3'), f('output_language', 'text', 'Target language (native)', True),
        f('services', 'text', 'Services provided', True, '100'),
        f('rate_translation', 'text', 'Translation rate (per word)'), f('rate_writing', 'text', 'Content writing rate (per word)'),
        f('rate_editing', 'text', 'Editing rate (per word)'), f('rate_transcription', 'text', 'Transcription rate (per minute)'),
        f('rate_subtitling', 'text', 'Subtitling rate (per minute)'), f('rate_dtp', 'text', 'DTP rate (per page)'),
        f('rate_hourly', 'text', 'Hourly rate (proofreading, review, linguistic services)', False, '100'),
        f('specialization', 'text', 'Areas of specialization'), f('tools', 'text', 'CAT &amp; other tools'),
        f('daily_output', 'text', 'Daily word output'), f('payment_method', 'text', 'Preferred payment method', True),
        f('profile_link', 'url', 'Website / LinkedIn / ProZ profile'), f('references', 'text', 'References'),
        f('additional_info', 'textarea', 'Additional information', False, '100', rows='4'),
        F('cv', 'upload', 'Upload your CV (required)', '', True, '50', allow_multiple_upload='', max_files='1'),
        F('supporting_files', 'upload', 'Supporting files (optional, up to 4)', '', False, '50', max_files='4'),
    ], 'Submit Application', subject='New career application — Pak Translations website')
    apply = sec([C([
        C([EB('Apply Now'), H('Join the <span class="x-hl">Pak Translations</span> Team', 'h2', 'x-title'),
           P('Fill out the form and our HR team will get back to you if your profile matches our requirements. Uploading your CV is required; other supporting files are optional.', 'x-lead'),
           IMG(UP + '2022/03/beautiful-curly-female-freelancer-with-cute-manicure-using-laptop-smiling-indoor-portrait-blonde-secretary-sitting-beside-african-coworker-blue-shirt-min-scaled.jpg', 'x-side-img', 'Freelance translators working remotely with Pak Translations'),
           ILIST([(t, 'check-circle') for t in ('Remote, flexible project work', 'Regular projects in your language pair', 'Clear instructions and prompt communication')], 'x-checks x-checks-1')], 'x-faq-side rv'),
        C([form], 'x-form-card rv'),
    ], 'x-faq-wrap', 'row')], _element_id='apply')
    return [hero, who, how, apply]
