const routes = {

    "#login": `
        <div class="row justify-content-center mt-5">

            <div class="col-md-5">

                <div class="card shadow border-0">

                    <div class="card-body p-4">

                        <h2 class="text-center mb-4">
                            <i class="bi bi-person-circle"></i>
                            Citizen Login
                        </h2>

                        <form id="loginForm">

                            <div class="mb-3">

                                <label class="form-label">
                                    Username
                                </label>

                                <input
                                    type="text"
                                    id="username"
                                    class="form-control"
                                    required>

                            </div>

                            <div class="mb-3">

                                <label class="form-label">
                                    Password
                                </label>

                                <input
                                    type="password"
                                    id="password"
                                    class="form-control"
                                    required>

                            </div>

                            <button
                                type="submit"
                                class="btn btn-primary w-100">

                                <i class="bi bi-box-arrow-in-right"></i>
                                Login

                            </button>

                        </form>

                    </div>

                </div>

            </div>

        </div>
    `,

    "#dashboard": `

    <div class="row g-4">

        <!-- SIDEBAR -->
        <aside class="col-12 col-lg-3">

            <div class="card mb-4">

                <div class="card-body">

                    <button
                        id="btnNewReport"
                        class="btn btn-primary w-100 py-3 fw-bold fs-5">

                        <i class="bi bi-plus-circle"></i>
                        Laporan Baru

                    </button>

                    <hr class="my-4">

                    <h5 class="fw-bold mb-3">
                        <i class="bi bi-menu-button-wide"></i>
                        Menu Utama
                    </h5>

                    <a href="#dashboard"
                    class="menu-link menu-active">

                        <i class="bi bi-person-lines-fill me-2"></i>
                        Laporan Saya

                    </a>

                    <a href="#feed"
                    class="menu-link">

                        <i class="bi bi-globe2 me-2"></i>
                        Feed Kota

                    </a>

                </div>

            </div>

            <div class="card">

                <div class="card-body">

                    <h5 class="fw-bold mb-4">
                        <i class="bi bi-bar-chart-fill"></i>
                        Statistik
                    </h5>

                    <div class="stat-card d-flex align-items-center">

                        <div class="stat-icon bg-primary-subtle text-primary">
                            <i class="bi bi-folder-fill"></i>
                        </div>

                        <div class="ms-3">

                            <div class="text-secondary">
                                Total Laporan
                            </div>

                            <h3
                                id="totalReports"
                                class="mb-0">

                                0

                            </h3>

                        </div>

                    </div>

                    <div class="stat-card d-flex align-items-center">

                        <div class="stat-icon bg-success-subtle text-success">
                            <i class="bi bi-check-circle-fill"></i>
                        </div>

                        <div class="ms-3">

                            <div class="text-secondary">
                                Selesai
                            </div>

                            <h3
                                id="resolvedReports"
                                class="mb-0">

                                0

                            </h3>

                        </div>

                    </div>

                    <div class="stat-card d-flex align-items-center">

                        <div class="stat-icon bg-warning-subtle text-warning">
                            <i class="bi bi-clock-fill"></i>
                        </div>

                        <div class="ms-3">

                            <div class="text-secondary">
                                Proses
                            </div>

                            <h3
                                id="progressReports"
                                class="mb-0">

                                0

                            </h3>

                        </div>

                    </div>

                </div>

            </div>

        </aside>

        <!-- CONTENT -->
        <section class="col-12 col-lg-6">

            <div class="card center-card">

                <div
                    id="dashboardContent"
                    class="card-body">

                    <div class="text-center mt-5">

                        <i
                            id="welcome-icon"
                            class="bi bi-inbox">
                        </i>

                        <h1 class="fw-light mt-4">
                            Selamat Datang!
                        </h1>

                        <p class="text-secondary fs-5">

                            Dashboard siap untuk
                            Lab Session 12.

                        </p>

                    </div>

                </div>

            </div>

        </section>

        <!-- PANEL KANAN -->
        <aside class="col-12 col-lg-3">

            <div class="card">

                <div class="card-body">

                    <h4 class="fw-bold mb-4">

                        <i class="bi bi-info-circle-fill text-primary"></i>

                        Pengumuman

                    </h4>

                    <div class="alert alert-primary">

                        Gunakan tombol
                        <strong>Laporan Baru</strong>
                        untuk membuat laporan.

                    </div>

                    <button
                        onclick="logout()"
                        class="btn btn-outline-danger w-100 mt-3">

                        <i class="bi bi-box-arrow-right"></i>
                        Logout

                    </button>

                </div>

            </div>

        </aside>

    </div>

    `,

    "#feed": `

    <div class="card">

        <div class="card-body">

            <h2 class="fw-bold mb-4">
                Feed Kota
            </h2>

            <div id="feedContent">

                Memuat laporan...

            </div>

        </div>

    </div>

    `

};


function logout() {

    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");

    window.location.hash = "#login";
}


function setupDashboard() {

    const btn =
        document.getElementById(
            "btnNewReport"
        );

    if (btn) {

        btn.addEventListener(
            "click",
            function () {

                const modal =
                    new bootstrap.Modal(
                        document.getElementById(
                            "reportModal"
                        )
                    );

                modal.show();
            }
        );
    }

    const saveBtn =
        document.getElementById(
            "saveDraftBtn"
        );

    if (saveBtn) {

        saveBtn.addEventListener(
            "click",
            saveDraft
        );
    }
}


async function saveDraft() {

    const payload = {

        title:
            document.getElementById(
                "reportTitle"
            ).value,

        category:
            document.getElementById(
                "reportCategory"
            ).value,

        location:
            document.getElementById(
                "reportLocation"
            ).value,

        description:
            document.getElementById(
                "reportDescription"
            ).value
    };

    try {

        let response;

        if (
            window.editingReportId
        ) {

            response =
                await requestAPI(
                    `/api/reports/${window.editingReportId}/`,
                    "PATCH",
                    payload
                );

        } else {

            response =
                await requestAPI(
                    "/api/reports/",
                    "POST",
                    payload
                );
        }

        const data =
            await response.json();

        console.log(data);

        if (
            response.ok
        ) {

            alert(
                "Draft berhasil disimpan!"
            );

            window.editingReportId =
                null;

            document.getElementById(
                "reportForm"
            ).reset();

            const modalElement =
                document.getElementById(
                    "reportModal"
                );

            const modal =
                bootstrap.Modal.getInstance(
                    modalElement
                );

            if (modal) {

                modal.hide();
            }

            loadReports(
                currentPage
            );

        } else {

            alert(
                "Gagal menyimpan draft!"
            );

            console.log(data);
        }

    } catch(error) {

        console.error(error);

        alert(
            "Terjadi kesalahan!"
        );
    }
}


let currentPage = 1;

async function loadReports(page = 1) {

    currentPage = page;

    try {

        const response =
            await requestAPI(
                `/api/reports/?page=${page}`
            );

        const data =
            await response.json();

        const totalPages =
            Math.ceil(
                data.count / 10
            );

        document.getElementById(
            "totalReports"
        ).innerText =
            data.count;

        const resolved =
            data.results.filter(
                report =>
                report.status ===
                "RESOLVED"
            ).length;

        document.getElementById(
            "resolvedReports"
        ).innerText =
            resolved;

        const progress =
            data.results.filter(
                report =>
                report.status ===
                "IN_PROGRESS"
            ).length;

        document.getElementById(
            "progressReports"
        ).innerText =
            progress;

        document.getElementById(
            "dashboardContent"
        ).innerHTML = `

            <div class="d-flex justify-content-between align-items-center mb-4">

                <h3 class="fw-bold mb-0">
                    Daftar Laporan
                </h3>

                <select
                    id="reportFilter"
                    class="form-select"
                    style="max-width:220px;">

                    <option value="all">
                        Semua Laporan
                    </option>

                    <option value="draft">
                        Draft Saya
                    </option>

                    <option value="published">
                        Published
                    </option>

                </select>

            </div>

            <div id="reportList"></div>

            <div class="d-flex justify-content-between align-items-center mt-4">

                <button
                    id="prevPage"
                    class="btn btn-outline-primary"
                    ${data.previous ? "" : "disabled"}>

                    ← Previous

                </button>

                <span class="fw-bold">

                    Page ${page} / ${totalPages}

                </span>

                <button
                    id="nextPage"
                    class="btn btn-outline-primary"
                    ${data.next ? "" : "disabled"}>

                    Next →

                </button>

            </div>

        `;

        function renderReports(filter = "all") {

            let reports =
                data.results;

            if (filter === "draft") {

                reports =
                    reports.filter(
                        report =>
                        report.status ===
                        "DRAFT"
                    );
            }

            if (filter === "published") {

                reports =
                    reports.filter(
                        report =>
                        report.status !==
                        "DRAFT"
                    );
            }

            document.getElementById(
                "reportList"
            ).innerHTML =

                reports
                .sort((a, b) => {
                    if (a.status === "DRAFT" && b.status !== "DRAFT") return -1;
                    if (a.status !== "DRAFT" && b.status === "DRAFT") return 1;
                    return b.id - a.id;
                })
                .map(report => `

                    <div class="card mb-3 shadow-sm">

                        <div class="card-body">

                            <div class="d-flex justify-content-between align-items-start">

                                <div class="w-100">

                                    <h5 class="mb-2">
                                        ${report.title}
                                    </h5>

                                    <p class="text-secondary mb-2">
                                        ${report.description}
                                    </p>

                                    <small class="text-muted d-block mb-2">
                                        📍 ${report.location || "-"}
                                    </small>

                                    ${
                                        report.status !== "DRAFT"
                                        ? `

                                        <div class="progress mb-2"
                                            style="height:20px;">

                                            <div
                                                class="progress-bar
                                                ${
                                                    report.status === "REPORTED"
                                                    ? "bg-primary"
                                                    : report.status === "VERIFIED"
                                                    ? "bg-info"
                                                    : report.status === "IN_PROGRESS"
                                                    ? "bg-warning text-dark"
                                                    : "bg-success"
                                                }"

                                                style="width:${
                                                    report.status === "REPORTED"
                                                    ? "25"
                                                    : report.status === "VERIFIED"
                                                    ? "50"
                                                    : report.status === "IN_PROGRESS"
                                                    ? "75"
                                                    : "100"
                                                }%;">

                                                ${
                                                    report.status === "REPORTED"
                                                    ? "25%"
                                                    : report.status === "VERIFIED"
                                                    ? "50%"
                                                    : report.status === "IN_PROGRESS"
                                                    ? "75%"
                                                    : "100%"
                                                }

                                            </div>

                                        </div>

                                        `
                                        : ""
                                    }

                                    ${
                                        report.status === "DRAFT"
                                        ? `
                                            <button
                                                class="btn btn-success btn-sm mt-2 me-1"
                                                onclick="publishReport(${report.id})">

                                                Ajukan

                                            </button>

                                            <button
                                                class="btn btn-warning btn-sm mt-2 me-1"
                                                onclick="editReport(${report.id})">

                                                Edit

                                            </button>

                                            <button
                                                class="btn btn-danger btn-sm mt-2"
                                                onclick="deleteReport(${report.id})">

                                                Hapus

                                            </button>
                                        `
                                        : ""
                                    }

                                </div>

                                <span class="badge ${
                                    report.status === "DRAFT"
                                    ? "bg-secondary"
                                    : report.status === "REPORTED"
                                    ? "bg-primary"
                                    : report.status === "VERIFIED"
                                    ? "bg-info"
                                    : report.status === "IN_PROGRESS"
                                    ? "bg-warning text-dark"
                                    : "bg-success"
                                }">

                                    ${report.status}

                                </span>

                            </div>

                        </div>

                    </div>

                `).join("");
        }

        renderReports();

        document.getElementById(
            "reportFilter"
        ).addEventListener(
            "change",
            function () {

                renderReports(
                    this.value
                );
            }
        );

        const prevBtn =
            document.getElementById(
                "prevPage"
            );

        const nextBtn =
            document.getElementById(
                "nextPage"
            );

        if (prevBtn) {

            prevBtn.addEventListener(
                "click",
                () => loadReports(page - 1)
            );
        }

        if (nextBtn) {

            nextBtn.addEventListener(
                "click",
                () => loadReports(page + 1)
            );
        }

    } catch(error) {

        console.error(error);

        document.getElementById(
            "dashboardContent"
        ).innerHTML = `

            <div class="alert alert-danger">

                Gagal memuat data laporan.

            </div>

        `;
    }
}


async function publishReport(reportId) {

    try {

        const response =
            await requestAPI(
                `/api/reports/${reportId}/`,
                "PATCH",
                {
                    status: "REPORTED"
                }
            );

        if (response.ok) {

            alert(
                "Laporan berhasil diajukan!"
            );

            loadReports(currentPage);

        } else {

            const data =
                await response.json();

            console.log(data);

            alert(
                "Gagal mengajukan laporan!"
            );
        }

    } catch(error) {

        console.error(error);

        alert(
            "Terjadi kesalahan!"
        );
    }
}


async function editReport(reportId) {

    try {

        const response =
            await requestAPI(
                `/api/reports/${reportId}/`
            );

        const report =
            await response.json();

        document.getElementById(
            "reportTitle"
        ).value =
            report.title;

        document.getElementById(
            "reportCategory"
        ).value =
            report.category;

        document.getElementById(
            "reportLocation"
        ).value =
            report.location || "";

        document.getElementById(
            "reportDescription"
        ).value =
            report.description;

        window.editingReportId =
            report.id;

        const modal =
            new bootstrap.Modal(
                document.getElementById(
                    "reportModal"
                )
            );

        modal.show();

    } catch(error) {

        console.error(error);

        alert(
            "Gagal membuka draft!"
        );
    }
}


async function deleteReport(reportId) {

    const confirmed =
        confirm(
            "Yakin ingin menghapus draft ini?"
        );

    if (!confirmed) {
        return;
    }

    try {

        const response =
            await requestAPI(
                `/api/reports/${reportId}/`,
                "DELETE"
            );

        if (response.ok) {

            alert(
                "Draft berhasil dihapus!"
            );

            loadReports(
                currentPage
            );

        } else {

            alert(
                "Gagal menghapus draft!"
            );
        }

    } catch(error) {

        console.error(error);

        alert(
            "Terjadi kesalahan!"
        );
    }
}


async function loadFeed() {

    try {

        const response =
            await requestAPI(
                "/api/reports/?page=1"
            );

        const data =
            await response.json();

        const reports =
            data.results
            .filter(
                report =>
                report.status !== "DRAFT"
            )
            .sort(
                (a, b) =>
                b.id - a.id
            );

        document.getElementById(
            "feedContent"
        ).innerHTML =

            reports.map(report => `

                <div class="card mb-3">

                    <div class="card-body">

                        <h5>
                            ${report.title}
                        </h5>

                        <p>
                            ${report.description}
                        </p>

                        <small class="text-muted">

                            Pelapor:
                            ${report.reporter}

                        </small>

                        <span class="badge bg-primary ms-2">

                            ${report.status}

                        </span>

                    </div>

                </div>

            `).join("");

    } catch(error) {

        console.error(error);
    }
}


function handleRouting() {

    const hash =
        window.location.hash || "#login";

    document.getElementById("app").innerHTML =
        routes[hash] ||
        routes["#login"];

    if (hash === "#login") {

        setupLoginForm();
    }

    if (hash === "#dashboard") {

        setupDashboard();
        loadReports();
    }

    if (hash === "#feed") {

    loadFeed();
    }
}
