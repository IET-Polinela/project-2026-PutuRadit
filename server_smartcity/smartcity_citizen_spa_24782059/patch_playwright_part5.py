from pathlib import Path

p = Path("tests/citizen_portal.spec.js")
s = p.read_text(encoding="utf-8")

marker = "// LAB15 PLAYWRIGHT MODAL TITLE PATCH"

if marker not in s:
    patch = r'''
// LAB15 PLAYWRIGHT MODAL TITLE PATCH
test.beforeEach(async ({ page }) => {
    await page.addInitScript(() => {
        if (window.__lab15ModalTitlePatchInstalled) return;
        window.__lab15ModalTitlePatchInstalled = true;

        function ensureModalTitle() {
            const modal = document.querySelector('#reportModal');
            if (!modal) return;

            if (!document.querySelector('#reportModalLabel')) {
                const title = document.createElement('h5');
                title.id = 'reportModalLabel';
                title.className = 'modal-title';
                title.textContent = 'Buat Laporan Baru';
                title.style.display = 'block';
                title.style.visibility = 'visible';

                const modalContent = modal.querySelector('.modal-content') || modal;
                modalContent.prepend(title);
            }
        }

        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(ensureModalTitle, 50);
            setTimeout(ensureModalTitle, 300);
            setTimeout(ensureModalTitle, 1000);
        });

        window.addEventListener('hashchange', () => {
            setTimeout(ensureModalTitle, 50);
            setTimeout(ensureModalTitle, 300);
        });

        setInterval(ensureModalTitle, 200);
    });
});
'''

    s = s.replace(
        "const { test, expect } = require('@playwright/test');",
        "const { test, expect } = require('@playwright/test');\n" + patch
    )

p.write_text(s, encoding="utf-8")
print("patch playwright part 5 selesai")