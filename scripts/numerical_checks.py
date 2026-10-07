"""Exact / numerical checks of explicit claims in
'The Quasi-Riemann Hypothesis: A Zero-Free Half-Plane Re s>7/8' (openai/math adc7f1241b42).

Every check records: id, TeX line, claim, computed value, pass/fail.
Exact rational arithmetic uses sympy; numerics use mpmath.
"""
import json
import sympy as sp
import mpmath as mp

R = sp.Rational
checks = []


def chk(cid, line, claim, lhs, rhs, rel="=="):
    lhs_s, rhs_s = sp.nsimplify(lhs), sp.nsimplify(rhs)
    if rel == "==":
        ok = sp.simplify(lhs_s - rhs_s) == 0
    elif rel == "<":
        ok = bool(lhs_s < rhs_s)
    elif rel == "<=":
        ok = bool(lhs_s <= rhs_s)
    elif rel == ">":
        ok = bool(lhs_s > rhs_s)
    elif rel == ">=":
        ok = bool(lhs_s >= rhs_s)
    checks.append(dict(id=cid, tex_line=line, claim=claim, lhs=str(lhs_s), rel=rel,
                       rhs=str(rhs_s), passed=bool(ok)))
    return ok


# ---------------------------------------------------------------- geometry (eq old-eq:5.1)
b, h, ell = R(1, 8), R(13, 16), R(1, 6)
lx = 1 + ell - h
ly = lx + b
chk("G1", 6861, "l_x = 1+ell-h = 17/48", lx, R(17, 48))
chk("G2", 6862, "l_y = l_x+b = 23/48", ly, R(23, 48))
chk("G3", 6864, "M = l_x+l_y = 5/6", lx + ly, R(5, 6))
chk("G4", 6864, "M+ell = 1", lx + ly + ell, 1)

# ---------------------------------------------------------------- boundary bookkeeping
s = sp.symbols("s")
C2 = lx / 2 + s - 1 + h / 6
chk("B1", 8641, "C_II(s) = l_x/2+s-1+h/6 = s-11/16", sp.expand(C2 - s), R(-11, 16))
chk("B2", 8642, "C_II(7/8) = 3/16 = l_x/2+b/12", C2.subs(s, R(7, 8)), lx / 2 + b / 12)
chk("B3", 8794, "17/96 - 1 + 13/96 = -11/16", R(17, 96) - 1 + R(13, 96), R(-11, 16))
# general boundary formula sigma0 = 1 - h/6 + b/12 (C(sigma0) = low exponent)
sig0 = lambda hh, bb: 1 - hh / 6 + bb / 12
chk("B4", 8641, "Part II boundary 1-h/6+b/12 = 7/8", sig0(h, b), R(7, 8))
# Part I: X=Y=Z^{1/2} => l_x=l_y=1/2, b=0, ell=0, h=1-l_x+ell=1/2; C_I(s)=1/4+s-1+1/12
chk("B5", 509, "Part I boundary (h=1/2,b=0) = 11/12", sig0(R(1, 2), 0), R(11, 12))
chk("B6", 509, "Part I C_I(s) = 1/4+s-1+h/6 = s-2/3", R(1, 4) - 1 + R(1, 12), R(-2, 3))
chk("B7", 509, "Part I C_I(11/12) = 1/4", R(11, 12) - R(2, 3), R(1, 4))

# ---------------------------------------------------------------- Part II bootstrap constants
chk("P1", 6817, "Delta <= 11/12 - 7/8 = 1/24", R(11, 12) - R(7, 8), R(1, 24))
chk("P2", 6819, "kappa = 2*beta*-1 <= 5/6 at beta*=11/12", 2 * R(11, 12) - 1, R(5, 6))
chk("P3", 6819, "kappa = 3/4 + 2 Delta (identity)", 2 * (R(7, 8) + sp.Symbol("D")) - 1 - (R(3, 4) + 2 * sp.Symbol("D")), 0)

# ---------------------------------------------------------------- principal margins (old-eq:5.14)
chk("M1", 15674, "m_w = l_y/20 = 23/960", ly / 20, R(23, 960))
chk("M2", 15675, "m_z = h/600 = 13/9600", h / 600, R(13, 9600))

# ---------------------------------------------------------------- high exponent E(d) (eq:common-high-exponent)
a, d, Rr, q, dl = sp.symbols("a d R q delta")
E1 = a - R(7, 8) + h * (R(17, 50) - R(1, 6)) - a * ly - (1 - a) * ell - (dl / 2 - q) * ell + d * (Rr + dl / 2 - R(17, 50))
C0 = R(-1, 48)
E2 = C0 + R(2, 3) * dl + q / 6 - h * (1 - Rr) + (d - h) * (Rr + dl / 2 - R(17, 50))
chk("E1", 15728, "two lines of E(d) agree with a=(1+delta)/2", sp.expand(E1.subs(a, (1 + dl) / 2) - E2), 0)
chk("E2", 15831, "-(1-a)ell-(delta/2-q)ell = -ell/2+q ell (a=(1+delta)/2)",
    sp.expand((-(1 - a) * ell - (dl / 2 - q) * ell).subs(a, (1 + dl) / 2) - (-ell / 2 + q * ell)), 0)
# general form from lem:bin-contour-accounting eq:stage-high-exponent
z0 = R(17, 50)
Egen = a - R(7, 8) + h * (z0 - R(1, 6)) - a * ly - ell / 2 + q * ell + d * (Rr + dl / 2 - z0)
chk("E3", 6092, "E_{7/8}(d;R,g=q ell) equals first line of E(d) (a=(1+delta)/2)", sp.expand((Egen - E1).subs(a, (1 + dl) / 2)), 0)

# floor bound (eq:floor-bound): delta0=1/50, R=1, q<=delta0/2, d=h
d0 = R(1, 50)
Efloor = E2.subs({dl: d0, Rr: 1, q: d0 / 2, d: h})
chk("F1", 15847, "E(h) at floor <= C0 + 3/4 delta0", Efloor, C0 + R(3, 4) * d0)
chk("F2", 15847, "C0 + 3/4 delta0 = -7/1200", C0 + R(3, 4) * d0, R(-7, 1200))
chk("F3", 15849, "floor frequency slope R+delta0/2-17/50 > 0", 1 + d0 / 2 - R(17, 50), 0, ">")

# small rows (eq:small-frequency-margin)
chk("S1", 15877, "h(17/50-1/6) - l_y/2 = -79/800", h * (R(17, 50) - R(1, 6)) - ly / 2, R(-79, 800))
chk("S2", 15885, "-79/800 + 2 d_min = -63/800 (d_min=1/100)", R(-79, 800) + 2 * R(1, 100), R(-63, 800))
chk("S3", 15881, "row exponent 63/50 < 2", R(63, 50), 2, "<")
chk("S4", 15900, "B0 = l_x/2+1+l_y = 53/32", lx / 2 + 1 + ly, R(53, 32))

# large-delta endpoint (eq:large-delta-endpoint): R = 1-delta, q<=delta/2, d=h
Eld = E2.subs({Rr: 1 - dl, q: dl / 2, d: h})
chk("L1", 15944, "E(h) with R=1-delta,q=delta/2 equals C0+(3/4-h)delta", sp.expand(Eld - (C0 + (R(3, 4) - h) * dl)), 0)
chk("L2", 15945, "(3/4-h) = -1/16", R(3, 4) - h, R(-1, 16))

# ---------------------------------------------------------------- endpoint certificate (Lemma 20.2)
x, y, t = sp.symbols("x y t")
alpha = R(5, 6)
Dx = 3 - R(17, 9) * x
Px = (2 - R(8, 9) * x) * (1 - x)
chk("C1", 15972, "D_x - P_x = 1 + x - 8x^2/9", sp.expand(Dx - Px), 1 + x - R(8, 9) * x**2)
J = (alpha - dl) * Dx + dl * Px
tt = 1 + dl * Px / (2 * J)
Rshort = 1 - dl + dl * Px / Dx * (R(3, 2) - tt)
Lt = 1 - dl + (alpha - dl) * (tt - 1)
chk("C2", 15984, "R_short(t) = L(t) at the balancing t", sp.simplify(Rshort - Lt), 0)
Rstar = Lt
chk("C3", 16019, "R_* = 1-delta+(alpha-delta) delta P_x/(2J)", sp.simplify(Rstar - (1 - dl + (alpha - dl) * dl * Px / (2 * J))), 0)
Estar = E2.subs({Rr: Rstar, q: x * dl, d: h})
negE_claim = (1 + (3 + 8 * y) * dl) / 48 - R(13, 32) * (R(5, 6) - dl) * dl * Px / J
chk("C4", 16022, "-E_* closed form (y=1/2-x)", sp.simplify((-Estar - negE_claim).subs(y, R(1, 2) - x)), 0)
py_ = 7 + 18 * y + 8 * y**2
jy = 185 + 170 * y + (-138 + 12 * y + 96 * y**2) * dl
chk("C5", 16015, "D_x=(37+34y)/18", sp.expand((Dx - (37 + 34 * y) / 18).subs(x, R(1, 2) - y)), 0)
chk("C6", 16016, "P_x=p_y/9", sp.expand((Px - py_ / 9).subs(x, R(1, 2) - y)), 0)
chk("C7", 16017, "J=j_y/108", sp.expand((J - jy / 108).subs(x, R(1, 2) - y)), 0)
quad = 10 * (37 + 34 * y) - 8 * (237 + 377 * y + 26 * y**2) * dl + 48 * (51 + 131 * y + 94 * y**2 + 32 * y**3) * dl**2
lhs_q = 2 * jy * (1 + (3 + 8 * y) * dl) - 468 * (R(5, 6) - dl) * dl * py_
chk("C8", 16030, "2 j_y[1+(3+8y)d] - 468(5/6-d) d p_y = explicit quadratic", sp.expand(lhs_q - quad), 0)
chk("C9", 16030, "10368 J (-E_*) equals that expression", sp.simplify((10368 * J * negE_claim).subs(x, R(1, 2) - y) - lhs_q), 0)
v = 51 + 41 * y
cert = (3 + 5 * y) * ((4 * v * dl - 79) ** 2 + 49) + 4 * y * (4 * v * dl * ((1 + 3 * y) * (15 + 32 * y) * dl + 9 - 13 * y) + 265 + 3485 * y)
chk("C10", 16042, "completed-square certificate identity  v*quad == cert", sp.expand(v * quad - cert), 0)
chk("C11", 16066, "v = 51+41y <= 17(3+5y) for y>=0 (difference = 44y)", sp.expand(17 * (3 + 5 * y) - v), 44 * y)
chk("C12", 16068, "49/(10368*17*J) bound constant: 10368*17 = 176256", 10368 * 17, 176256)
chk("C13", 16069, "49/(176256 * 5/2) = 49/440640", R(49) / (176256 * R(5, 2)), R(49, 440640))
chk("C14", 16069, "49/440640 > 1/10000", R(49, 440640), R(1, 10000), ">")
chk("C15", 15976, "J range lower 35/54 at (delta=5/6,x=1/2)", J.subs({dl: R(5, 6), x: R(1, 2)}), R(35, 54))
chk("C16", 15970, "D_x at x=1/2 equals 37/18", Dx.subs(x, R(1, 2)), R(37, 18))
chk("C17", 15971, "P_x at x=1/2 equals 7/9", Px.subs(x, R(1, 2)), R(7, 9))
# numeric minimum of -E_* over the domain (independent check of the certificate's conclusion)
fE = sp.lambdify((dl, x), -Estar, "mpmath")
mp.mp.dps = 30
best = None
N = 400
for i in range(N + 1):
    for j in range(N + 1):
        dv = mp.mpf(i) / N * mp.mpf(5) / 6
        xv = mp.mpf(j) / N / 2
        val = fE(dv, xv)
        if best is None or val < best[0]:
            best = (val, dv, xv)
checks.append(dict(id="C18", tex_line=16000, claim="grid minimum of -E_* over 0<=delta<=5/6, 0<=x<=1/2 (401x401)",
                   lhs=f"{mp.nstr(best[0], 12)} at delta={mp.nstr(best[1], 6)}, x={mp.nstr(best[2], 6)}",
                   rel=">=", rhs=str(R(49, 440640)) + f" = {float(R(49, 440640)):.3e}",
                   passed=bool(best[0] >= mp.mpf(49) / 440640)))
min_negE = best

# adaptive endpoint (eq:adaptive-endpoint)
chk("A1", 16101, "1 - h/4 = 51/64", 1 - h / 4, R(51, 64))

# frequency ranges
chk("Q1", 16116, "ell/h = 8/39", ell / h, R(8, 39))
chk("Q2a", 16116, "8/39 > 1/5", R(8, 39), R(1, 5), ">")
chk("Q2b", 16116, "1/5 > 7/37", R(1, 5), R(7, 37), ">")
chk("Q3", 16123, "5 ell - h = 1/48", 5 * ell - h, R(1, 48))
chk("Q4", 16126, "1/5 - 7/37 = 2/185", R(1, 5) - R(7, 37), R(2, 185))
chk("Q5", 16133, "33/50 - delta/2 >= 4/25 at delta=1", R(33, 50) - R(1, 2), R(4, 25))
chk("Q6", 16139, "R_* <= 1-delta+(alpha-delta)/2 <= 17/12 (max at delta=0)", 1 + alpha / 2, R(17, 12))
chk("Q7", 16141, "17/12 + Delta/4 <= 139/96 (Delta<=1/24); exact max is 137/96 (bound has slack)", R(17, 12) + R(1, 24) / 4, R(139, 96), "<=")
chk("Q8", 16143, "139/96 + 1/2 - 17/50 < 2", R(139, 96) + R(1, 2) - R(17, 50), 2, "<")
chk("Q9", 16271, "8/39 - 7/37 = 23/1443", R(8, 39) - R(7, 37), R(23, 1443))
# intermediate range (eq:adaptive-intermediate): d=1/2, R=76/75-2delta/3, q=delta/2
Eint = E2.subs({d: R(1, 2), Rr: R(76, 75) - R(2, 3) * dl, q: dl / 2})
chk("I1", 16159, "E(1/2) = -529/2400 + 25/96 delta", sp.expand(Eint - (R(-529, 2400) + R(25, 96) * dl)), 0)
chk("I2", 16160, "-529/2400 + 25/96*(5/6) = -49/14400", R(-529, 2400) + R(25, 96) * R(5, 6), R(-49, 14400))
chk("I3", 16153, "76/75 - 2/3*(1/50) = 1", R(76, 75) - R(2, 3) * R(1, 50), 1)
chk("I4", 16154, "slope R+delta/2-17/50 = 101/150 - delta/6", sp.expand(R(76, 75) - R(2, 3) * dl + dl / 2 - R(17, 50)), R(101, 150) - dl / 6)

# ---------------------------------------------------------------- Part I row envelope (Prop 9.2)
Rd = lambda dd: sp.Min(1, sp.Max(1 - dd / 2, R(4, 3) - dd))
chk("R1", 5196, "R(1/50) = 1 (floor consistency)", Rd(R(1, 50)), 1)
chk("R2", 5196, "crossover 1-d/2 = 4/3-d at d=2/3", sp.solve(sp.Eq(1 - dl / 2, R(4, 3) - dl), dl)[0], R(2, 3))

# ---------------------------------------------------------------- transfer: L(1,chi_{-3}) = pi/(3 sqrt 3)
mp.mp.dps = 30
L1 = mp.nsum(lambda n: 1 / (3 * n + 1) - 1 / (3 * n + 2), [0, mp.inf])
checks.append(dict(id="T1", tex_line=6774, claim="L(1,chi_{-3}) = pi/(3 sqrt 3) > 0",
                   lhs=mp.nstr(L1, 20), rel="==", rhs=mp.nstr(mp.pi / (3 * mp.sqrt(3)), 20),
                   passed=bool(abs(L1 - mp.pi / (3 * mp.sqrt(3))) < mp.mpf(10) ** -20)))
# Mathlib junk value check: riemannZeta 1 = (gamma - log(4 pi))/2 != 0 (statement covers s=1)
z1 = (mp.euler - mp.log(4 * mp.pi)) / 2
checks.append(dict(id="T2", tex_line=0, claim="Mathlib riemannZeta 1 = (gamma - log 4pi)/2 is nonzero",
                   lhs=mp.nstr(z1, 15), rel="!=", rhs="0", passed=bool(z1 != 0)))

# ---------------------------------------------------------------- Euler-product necessity: Davenport-Heilbronn zero
# f(s) = ((1-i k)/2) L(s,chi) + ((1+i k)/2) L(s,conj chi), chi mod 5 with chi(2)=i,
# k = (sqrt(10-2 sqrt5)-2)/(sqrt5-1). Satisfies a Riemann-type functional equation, no Euler product.
mp.mp.dps = 25
kap = (mp.sqrt(10 - 2 * mp.sqrt(5)) - 2) / (mp.sqrt(5) - 1)
chi = {1: 1, 2: 1j, 4: -1, 3: -1j, 0: 0}


def Lchi(sv, conj=False):
    vals = [chi[n % 5] for n in range(5)]
    if conj:
        vals = [complex(v).conjugate() for v in vals]
    return sum(mp.mpc(vals[a]) * mp.zeta(sv, mp.mpf(a) / 5) for a in range(1, 5)) / mp.power(5, sv)


def DH(sv):
    return (1 - 1j * kap) / 2 * Lchi(sv) + (1 + 1j * kap) / 2 * Lchi(sv, True)


rho = mp.findroot(DH, mp.mpc(0.808517, 85.699348))
checks.append(dict(id="D1", tex_line=0,
                   claim="Davenport-Heilbronn function (functional equation, no Euler product) has a zero with 1/2<Re<1",
                   lhs=mp.nstr(rho, 12), rel="Re in (1/2,1)", rhs=f"|f(rho)|={mp.nstr(abs(DH(rho)), 3)}",
                   passed=bool(0.5 < rho.real < 1 and abs(DH(rho)) < 1e-15)))

if __name__ == "__main__":
    json.dump(dict(checks=checks, min_negE=[str(v) for v in min_negE], dh_zero=str(rho)),
              open("numerical_checks_results.json", "w"), indent=1)
    n_ok = sum(c["passed"] for c in checks)
    print(f"{n_ok}/{len(checks)} checks passed")
    for c in checks:
        if not c["passed"]:
            print("FAILED", c)
