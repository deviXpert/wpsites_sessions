# Altus Emergency Centers — altusemergency.com

WordPress + Astra, Elementor Pro, WP Rocket, Code Snippets, Yoast, SG Security.
Access: REST API with the app password in the environment (`WP_URL`, `WP_USER`, `WP_APP_PASSWORD`).

## PageSpeed accessibility fixes (Code Snippets, saved inactive)

| Snippet | ID | Audit | Cause |
|---|---|---|---|
| `snippets/1-video.php` | 9 | aria-allowed-role | Elementor prints `role="presentation"` on background `<video>` |
| `snippets/2-aibtn.php` | 10 | aria-prohibited-attr | Footer (template 2123) AI-summary `<a>` tags have no href; HFCM snippet #20 sets it, but WP Rocket delays that script |
| `snippets/3-slack.php` | 11 | aria-required-parent | Slack wrapper markup pasted into text widgets (pages 13, 1088, 1299, 1412, 1491) |

All three filter `elementor/frontend/the_content` (covers page content and theme-builder header/footer).
`snippets/test.php` runs them against a saved page: `php test.php in.html out.html`.
Local Lighthouse on the patched homepage and Lumberton page: accessibility 92/86 → 100.
After activating, clear the WP Rocket cache.
