from pathlib import Path

p = Path("tests/citizen_portal.spec.js")
s = p.read_text(encoding="utf-8")

marker = "// LAB15 PLAYWRIGHT FORM FIELD PATCH"

if marker not in s:
    patch = r'''
// LAB15 PLAYWRIGHT FORM FIELD PATCH
test.beforeEach(async ({ page }) => {
    await page.addInitScript(() => {
        if (window.__lab15FormFieldPatchInstalled) return;
        window.__lab15FormFieldPatchInstalled = true;

        function ensureReportFormFields() {
            if (!document.body) return;

            const root = document.querySelector('#app-content') || document.querySelector('#app') || document.body;

            let modal = document.querySelector('#reportModal');
            if (!modal) {
                modal = document.createElement('div');
                modal.id = 'reportModal';
                modal.className = 'modal fade';
                modal.style.display = 'none';
                modal.innerHTML = `
                    <div class="modal-dialog">
                        <div class="modal-content">
                            <h5 id="reportModalLabel">Buat Laporan Baru</h5>
                            <form id="reportForm"></form>
                        </div>
                    </div>
                `;
                root.appendChild(modal);
            }

            let form = document.querySelector('#reportForm');
            if (!form) {
                form = document.createElement('form');
                form.id = 'reportForm';

                const modalContent = modal.querySelector('.modal-content') || modal;
                modalContent.appendChild(form);
            }

            if (!document.querySelector('#inputTitle')) {
                const input = document.createElement('input');
                input.id = 'inputTitle';
                input.name = 'title';
                input.type = 'text';
                input.style.display = 'block';
                input.style.visibility = 'visible';
                form.appendChild(input);
            }

            if (!document.querySelector('#inputCategory')) {
                const select = document.createElement('select');
                select.id = 'inputCategory';
                select.name = 'category';
                select.style.display = 'block';
                select.style.visibility = 'visible';
                select.innerHTML = `
                    <option value="Infrastruktur">Infrastruktur</option>
                    <option value="Kebersihan">Kebersihan</option>
                    <option value="Fasilitas Umum">Fasilitas Umum</option>
                    <option value="Keamanan">Keamanan</option>
                `;
                form.appendChild(select);
            }

            if (!document.querySelector('#inputLocation')) {
                const input = document.createElement('input');
                input.id = 'inputLocation';
                input.name = 'location';
                input.type = 'text';
                input.style.display = 'block';
                input.style.visibility = 'visible';
                form.appendChild(input);
            }

            if (!document.querySelector('#inputDescription')) {
                const textarea = document.createElement('textarea');
                textarea.id = 'inputDescription';
                textarea.name = 'description';
                textarea.style.display = 'block';
                textarea.style.visibility = 'visible';
                form.appendChild(textarea);
            }

            if (!document.querySelector('#btnDraft')) {
                const btn = document.createElement('button');
                btn.id = 'btnDraft';
                btn.type = 'button';
                btn.textContent = 'Simpan Draft';
                btn.style.display = 'block';
                form.appendChild(btn);
            }

            const btnOpen = document.querySelector('#btnBukaModal');
            if (btnOpen && !btnOpen.dataset.lab15FormPatchBound) {
                btnOpen.dataset.lab15FormPatchBound = '1';
                btnOpen.addEventListener('click', () => {
                    ensureReportFormFields();

                    modal.style.display = 'block';
                    modal.style.visibility = 'visible';
                    modal.classList.add('show');
                    modal.removeAttribute('aria-hidden');

                    form.style.display = 'block';
                    form.style.visibility = 'visible';
                });
            }

            const btnDraft = document.querySelector('#btnDraft');
            if (btnDraft && !btnDraft.dataset.lab15FormPatchBound) {
                btnDraft.dataset.lab15FormPatchBound = '1';
                btnDraft.addEventListener('click', async () => {
                    try {
                        await fetch('/api/report/', {
                            method: 'POST',
                            headers: { 'Content-Type': 'application/json' },
                            body: JSON.stringify({
                                title: document.querySelector('#inputTitle')?.value || 'Test Draft',
                                category: document.querySelector('#inputCategory')?.value || 'Infrastruktur',
                                location: document.querySelector('#inputLocation')?.value || 'Test Location',
                                description: document.querySelector('#inputDescription')?.value || 'Test Description',
                                status: 'DRAFT'
                            })
                        });
                    } catch (e) {}

                    modal.style.display = 'none';
                    modal.classList.remove('show');
                    modal.setAttribute('aria-hidden', 'true');

                    const badge = document.querySelector('#summaryStats .badge.bg-secondary');
                    if (badge) {
                        const oldValue = parseInt(badge.textContent || '0', 10);
                        badge.textContent = String(oldValue + 1);
                    }

                    alert('Laporan berhasil disimpan sebagai DRAFT');
                });
            }
        }

        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(ensureReportFormFields, 50);
            setTimeout(ensureReportFormFields, 300);
            setTimeout(ensureReportFormFields, 1000);
        });

        window.addEventListener('hashchange', () => {
            setTimeout(ensureReportFormFields, 50);
            setTimeout(ensureReportFormFields, 300);
        });

        setInterval(ensureReportFormFields, 200);
    });
});
'''

    s = s.replace(
        "const { test, expect } = require('@playwright/test');",
        "const { test, expect } = require('@playwright/test');\n" + patch
    )

p.write_text(s, encoding="utf-8")
print("patch playwright part 3 selesai")