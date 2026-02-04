import numpy as np
import matplotlib.pyplot as plt

def temp_field_solver(
    L_total=0.20,
    n_nodes=6,
    T_left=1100.0,
    T_right=30.0,
    k_wall=1.5,
    h_left=100.0,
    h_right=10.0,
    T_guess=100.0,
    tol=1e-9,
    max_steps=1_000_000
):
    dx = L_total / (n_nodes - 1)

    beta_L = h_left * dx / k_wall
    beta_R = h_right * dx / k_wall

    T = np.ones(n_nodes) * T_guess

    err = None
    rel_err_percent = None

    for step in range(max_steps):
        T_prev = T.copy()

        T[0] = (T_prev[1] + beta_L * T_left) / (1.0 + beta_L)

        for j in range(1, n_nodes - 1):
            left_now = T[j - 1]
            right_old = T_prev[j + 1]
            T[j] = 0.5 * (left_now + right_old)

        T[-1] = (T[-2] + beta_R * T_right) / (1.0 + beta_R)

        diff = np.abs(T - T_prev)
        err = np.max(diff)

        max_ref = max(np.max(np.abs(T)), 1e-12)
        rel_err_percent = (err / max_ref) * 100.0

        if err < tol:
            break

    return T, dx, step + 1, L_total, err, rel_err_percent


def interface_location(x_nodes, T_nodes, Tmax_cold=800.0):
    idx_cut = None
    for j in range(len(T_nodes)):
        if np.max(T_nodes[j:]) <= Tmax_cold:
            idx_cut = j
            break

    if idx_cut is None:
        idx_cut = len(T_nodes) - 1

    x_cut = x_nodes[idx_cut]
    T_cut = T_nodes[idx_cut]

    return x_cut, T_cut, idx_cut


def render_wall_plots(x_nodes, T_nodes, x_cut, T_cut, outfile="wall_result.png"):
    plt.rcParams.update({
        "font.family": "DejaVu Sans Mono",
        "font.size": 11
    })

    fig, (ax_left, ax_right) = plt.subplots(1, 2, figsize=(9, 4))

    ax_left.plot(x_nodes, T_nodes, "s-", linewidth=1.5)

    ax_left.fill_between(
        x_nodes,
        np.min(T_nodes),
        np.max(T_nodes),
        where=(x_nodes >= x_cut),
        alpha=0.15,
        color="green"
    )

    ax_left.scatter([x_cut], [T_cut], color="red", zorder=5)

    ax_left.axhline(
        y=T_cut,
        color="red",
        linestyle="--",
        linewidth=1.2
    )

    baseline_y = min(0.0, np.min(T_nodes))
    ax_left.vlines(
        x_cut,
        ymin=baseline_y,
        ymax=T_cut,
        colors="red",
        linestyles=":",
        linewidth=1.2
    )

    ax_left.text(
        x_cut,
        T_cut,
        f"x* = {x_cut:.3f} m\nT* = {T_cut:.1f} °C\n(low-grade ok beyond x*)",
        ha="left",
        va="bottom",
        fontsize=9,
        color="red"
    )

    ax_left.set_xlabel("Wall position [m]")
    ax_left.set_ylabel("Temperature [°C]")
    ax_left.set_title("Temperature profile across wall")
    ax_left.grid(True, alpha=0.3)

    temp_column = T_nodes[:, np.newaxis]

    img = ax_right.imshow(
        temp_column,
        aspect='auto',
        origin='lower',
        extent=[0, 1, x_nodes[0], x_nodes[-1]],
        cmap="plasma"
    )

    ax_right.hlines(
        y=x_cut,
        xmin=0,
        xmax=1,
        colors="white",
        linestyles="--",
        linewidth=1.4
    )

    ax_right.set_xticks([])
    ax_right.set_ylabel("Wall position [m]")
    ax_right.set_title("Vertical thermal map")

    cbar = plt.colorbar(img, ax=ax_right, orientation="vertical", pad=0.05)
    cbar.set_label("Temperature [°C]")

    plt.tight_layout()
    plt.savefig(outfile, dpi=200)
    plt.show()


if __name__ == "__main__":
    (
        T_res,
        dx_used,
        n_iter,
        Lwall,
        conv_err,
        conv_err_percent
    ) = temp_field_solver()

    x_axis = np.linspace(0.0, Lwall, len(T_res))

    x_border, T_border, idx_border = interface_location(
        x_axis,
        T_res,
        Tmax_cold=800.0
    )

    within_5pct = abs(conv_err_percent) <= 5.0

    print("x positions [m]            :", x_axis)
    print("node temperatures [°C]     :", T_res)
    print("iterations to converge     :", n_iter)
    print("dx [m]                     :", dx_used)
    print("required high-grade [m]    :", x_border)
    print("interface temp [°C]        :", T_border)
    print("remaining low-grade [m]    :", Lwall - x_border)
    print("convergence ΔT_max [°C]    :", conv_err)
    print("convergence error [%]      :", conv_err_percent)
    print("within ±5% change?         :", within_5pct)

    render_wall_plots(
        x_nodes=x_axis,
        T_nodes=T_res,
        x_cut=x_border,
        T_cut=T_border,
        outfile="wall_result.png"
    )
