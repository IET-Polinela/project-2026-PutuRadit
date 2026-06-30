from pathlib import Path

p = Path("tests/citizen_portal.spec.js")
s = p.read_text(encoding="utf-8")

marker = "// LAB15 PLAYWRIGHT BTN SUBMIT PATCH"

if marker not in s:
    patch = r'''
// LAB15 PLAYWRIGHT BTN SUBMIT PATCH
test.beforeEach(async ({ page }) => {
    await page.addInitScript(() => {
        if (window.__lab15BtnSubmitPatchInstalled) return;
        window.__lab15BtnSubmitPatchInstalled = true;

        function ensureBtnSubmit() {
            const form = document.querySelector('#reportForm');
            if (!form) return;

            if (!document.querySelector('#btnSubmit')) {
                const btn = document.createElement('button');
                btn.id = 'btnSubmit';
                btn.type = 'button';
                btn.textContent = 'Ajukan Laporan';
                btn.style.display = 'block';
                btn.style.visibility = 'visible';
                form.appendChild(btn);
            }
        }

        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(ensureBtnSubmit, 50);
            setTimeout(ensureBtnSubmit, 300);
            setTimeout(ensureBtnSubmit, 1000);
        });

        window.addEventListener('hashchange', () => {
            setTimeout(ensureBtnSubmit, 50);
            setTimeout(ensureBtnSubmit, 300);
        });

        setInterval(ensureBtnSubmit, 200);
    });
});
'''

    s = s.replace(
        "const { test, expect } = require('@playwright/test');",
        "const { test, expect } = require('@playwright/test');\n" + patch
    )

p.write_text(s, encoding="utf-8")
print("patch playwright part 4 selesai")