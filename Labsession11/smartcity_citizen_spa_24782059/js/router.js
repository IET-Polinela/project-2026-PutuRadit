const routes = {

    "#login": `
        <div class="row justify-content-center mt-5">

            <div class="col-md-5">

                <div class="card shadow">

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
        <div class="row g-3">

            <div class="col-12 col-lg-3">

                <div class="card shadow-sm">
                    <div class="card-body">

                        <h5>
                            <i class="bi bi-person-fill"></i>
                            Profile
                        </h5>

                        <hr>

                        <p>Citizen User</p>

                    </div>
                </div>

            </div>

            <div class="col-12 col-lg-6">

                <div class="card shadow-sm">

                    <div class="card-body">

                        <h4>
                            <i class="bi bi-house-fill"></i>
                            Dashboard
                        </h4>

                        <hr>

                        <p>
                            Selamat datang di Smart City Citizen Portal.
                        </p>

                        <p>
                            Sistem siap terhubung dengan API Django.
                        </p>

                    </div>

                </div>

            </div>

            <div class="col-12 col-lg-3">

                <div class="card shadow-sm">

                    <div class="card-body">

                        <h5>
                            <i class="bi bi-gear-fill"></i>
                            Menu
                        </h5>

                        <hr>

                        <button
                            onclick="logout()"
                            class="btn btn-danger w-100">

                            <i class="bi bi-box-arrow-right"></i>
                            Logout

                        </button>

                    </div>

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


function handleRouting() {

    const hash =
        window.location.hash || "#login";

    document.getElementById("app")
        .innerHTML = routes[hash];

    if (hash === "#login") {
        setupLoginForm();
    }
}
