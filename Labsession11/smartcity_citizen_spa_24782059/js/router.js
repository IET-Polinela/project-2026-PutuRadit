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
                                <label class="form-label">Username</label>

                                <input
                                    type="text"
                                    id="username"
                                    class="form-control"
                                    required>
                            </div>

                            <div class="mb-3">
                                <label class="form-label">Password</label>

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

                    <button class="btn btn-primary w-100 py-3 fw-bold fs-5">

                        <i class="bi bi-plus-circle"></i>
                        Laporan Baru

                    </button>

                    <hr class="my-4">

                    <h5 class="fw-bold mb-3">
                        <i class="bi bi-menu-button-wide"></i>
                        Menu Utama
                    </h5>

                    <a href="#" class="menu-link menu-active">
                        <i class="bi bi-house-fill me-2"></i>
                        Dashboard
                    </a>

                    <a href="#" class="menu-link">
                        <i class="bi bi-card-list me-2"></i>
                        Daftar Laporan
                    </a>

                    <a href="#" class="menu-link">
                        <i class="bi bi-person me-2"></i>
                        Profil
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

                            <h3 class="mb-0">0</h3>
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

                            <h3 class="mb-0">0</h3>
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

                            <h3 class="mb-0">0</h3>
                        </div>

                    </div>

                </div>

            </div>

        </aside>


        <!-- KONTEN TENGAH -->
        <section class="col-12 col-lg-6">

            <div class="card center-card">

                <div
                    class="card-body d-flex flex-column justify-content-center align-items-center text-center">

                    <i
                        id="welcome-icon"
                        class="bi bi-inbox">
                    </i>

                    <h1 class="fw-light mt-4">
                        Selamat Datang!
                    </h1>

                    <p class="text-secondary fs-5">
                        Koneksi API untuk data laporan
                        akan diimplementasikan pada Lab 12.
                    </p>

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
                        <strong>"Laporan Baru"</strong>
                        untuk membuat laporan Anda.

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

    `
};


function logout() {

    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");

    window.location.hash = "#login";
}


function handleRouting() {

    const hash = window.location.hash || "#login";

    document.getElementById("app").innerHTML =
        routes[hash] || routes["#login"];

    if (hash === "#login") {
        setupLoginForm();
    }
}
