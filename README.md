# ⚡ HKD Socket

### High-Performance Stateful File Transport for Python

**HKD Socket** is a socket-compatible transport designed for applications that repeatedly transmit large, incrementally changing data. It uses **HKD∞ active-state reduction** to avoid retransmitting information that the receiver already possesses.

In the included benchmark, HKD Socket reduces measured TCP application payload by approximately **261×** while reconstructing the transmitted state exactly.

> **Measured on both Linux and macOS: ~261× traffic reduction.**

---

## 🔌 Drop-In Python Socket Migration

A conventional Python socket application may begin with:

```python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

with open("data.npz", "rb") as f:
    sock.sendfile(f)
```

With HKD Socket, the migration is intentionally small:

```python
import hkd_socket as socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

with open("data.npz", "rb") as f:
    sock.sendfile(f)
```

The key change is:

```diff
- import socket
+ import hkd_socket as socket
```

HKD Socket preserves the familiar lowercase `socket` namespace while adding **HKD∞ stateful transport capabilities**.

Python's standard `socket.sendfile()` is already a high-performance baseline: on supported systems it uses the operating system's `sendfile` facility rather than requiring an ordinary Python read/send loop.

HKD Socket's benchmark therefore compares against an **optimized system-level file transmission path**, not an intentionally slow Python baseline.

---

# 🚀 Performance

The included HKD Socket benchmark measures real TCP traffic between a sender and receiver and verifies the reconstructed result cryptographically.

Typical benchmark result:

```text
HKD_INFINITY_FREE_SIZE_BENCHMARK
LABEL=NON_CHEAT_REAL_TCP_LOOPBACK_EXACT_DIRTY_RANGE_TRACKING

file_size=8.000 MiB
versions=280
logical_version_bytes=2.188 GiB

metric,socket.sendfile,hkd_socket,improvement
tcp_payload_tx,2.188 GiB,8.575 MiB,261.22x

traffic_reduction_x=261.224834

exact=True
traffic_target_pass=True
```

### Linux

Measured traffic reduction:

```text
~261x
```

### macOS

Measured traffic reduction:

```text
~261x
```

The principal performance result is **traffic reduction**, not a claim that every program executes 261× faster.

Actual wall-clock acceleration depends on:

- network bandwidth
- latency
- storage performance
- operating system
- workload
- update density
- hardware

On a bandwidth-constrained network, avoiding hundreds of bytes of transmission for each byte actually required can translate into very large end-to-end gains.

---

# 🧠 Why HKD Socket Is Fast

HKD Socket is **not simply another compression codec**.

Traditional compression asks approximately:

> **How can this byte sequence be represented using fewer bits?**

HKD Socket asks a different question:

> **Given the state already established at the receiver, what information must actually cross the network to advance that state exactly?**

This distinction is particularly important for large objects that change incrementally.

Consider successive states:

$$
\boxed{
X_0,\;X_1,\;X_2,\;\ldots,\;X_n
}
$$

A conventional full-file transmission repeatedly communicates an amount proportional to:

$$
\boxed{
T_{\mathrm{full}}
\propto
\sum_{k=0}^{n}|X_k|
}
$$

If each state is approximately the same size \(N\), the transmitted volume is approximately:

$$
\boxed{
T_{\mathrm{full}}
\approx
(n+1)N
}
$$

HKD∞ instead maintains a continuation state and identifies the **active portion** required to advance:

$$
\boxed{
X_k
\;\longrightarrow\;
X_{k+1}
}
$$

Let:

$$
\boxed{
A_k \subseteq X_k
}
$$

denote the active information associated with the transition.

Conceptually, HKD Socket seeks a transport representation:

$$
\boxed{
T_k
=
\mathcal{H}_{\infty}
\left(
X_k,\,
X_{k+1},\,
S_k
\right)
}
$$

where \(S_k\) represents synchronized continuation state.

The receiver performs:

$$
\boxed{
(X_k,S_k,T_k)
\;\xrightarrow{\;\mathcal{H}_{\infty}\;}
(X_{k+1},S_{k+1})
}
$$

The critical property is **exactness**:

$$
\boxed{
\widehat{X}_{k+1}
=
X_{k+1}
}
$$

When the active information is much smaller than the complete state:

$$
\boxed{
|A_k| \ll |X_k|
}
$$

the required transmission can also be much smaller than retransmitting \(X_k\) in its entirety.

This is the source of the large measured reduction.

---

# ∞ HKD∞ Active-State Reduction

HKD∞ is based on repeatedly eliminating state that no longer requires active work.

At a high level, a state can be considered as:

$$
\boxed{
X=A\cup I
}
$$

where:

- \(A\) is the currently **active state**
- \(I\) is state whose existing representation can be **preserved**

The transport operation concentrates computation and communication on \(A\).

After each transition, HKD∞ constructs the next continuation state:

$$
\boxed{
(A_k,S_k)
\;\xrightarrow{\;\mathcal{H}_{\infty}\;}
(A_{k+1},S_{k+1})
}
$$

For sparse modifications:

$$
\boxed{
|A_k| \ll |X_k|
}
$$

Consequently, the useful scaling target becomes approximately:

$$
\boxed{
T_{\mathrm{HKD}}
=
O
\left(
\sum_k |A_k|
+
M_k
\right)
}
$$

where \(M_k\) represents the compact protocol information required for the transition.

Full retransmission instead scales approximately as:

$$
\boxed{
T_{\mathrm{full}}
=
O
\left(
\sum_k |X_k|
\right)
}
$$

Therefore, in the sparse-update regime:

$$
\boxed{
\frac{T_{\mathrm{full}}}
     {T_{\mathrm{HKD}}}
\gg 1
}
$$

HKD Socket's advantage increases when successive versions are **large** but their active changes are **small**.

The proprietary implementation contains additional mechanisms for efficiently maintaining and transporting this continuation state.

Those implementation details are not required to use HKD Socket.

---

# 📦 Is HKD Socket Compression?

**Not in the conventional sense.**

HKD Socket and compression attack different sources of redundancy.

### Traditional compression

Compression exploits redundancy **inside the current payload**.

Conceptually:

$$
X
\longrightarrow
C(X)
$$

where \(C(X)\) is a smaller representation of the same information.

### HKD Socket

HKD Socket exploits redundancy **between states already shared by the sender and receiver**.

Conceptually:

$$
\boxed{
(X_k,S_k)
+
\Delta_k
\longrightarrow
(X_{k+1},S_{k+1})
}
$$

where \(\Delta_k\) represents the information required to advance the synchronized state.

For example, consider a **1 TB object** where only **10 MB** has changed.

Traditional full transmission starts with a 1 TB transfer and may then compress it.

HKD Socket instead attempts to make communication proportional to the information necessary to advance the receiver from its previous state to the new state.

In the ideal sparse regime:

$$
\boxed{
|\Delta_k|
\ll
|X_k|
}
$$

This also means HKD Socket can provide substantial traffic reduction on **high-entropy binary data** that does not compress particularly well, provided that changes between successive versions remain sparse.

HKD Socket can therefore be viewed as a:

> **Stateful transport optimization rather than merely a file compressor.**

---

# 🔐 Exact Reconstruction

HKD Socket is designed for **exact transport**.

The benchmark verifies the final receiver state using SHA-256.

A successful test requires:

```text
baseline_exact=True
hkd_exact=True
cross_path_same_final_file=True
exact=True
```

The objective is not approximate reconstruction, lossy encoding, or similarity.

It is:

$$
\boxed{
\operatorname{SHA256}
\left(
X_{\mathrm{sender}}
\right)
=
\operatorname{SHA256}
\left(
X_{\mathrm{receiver}}
\right)
}
$$

---

# 🔬 Benchmark Methodology

The included benchmark compares:

```text
Python socket.sendfile()

        vs.

HKD Socket
```

Python's `socket.socket.sendfile()` uses the operating system's high-performance `sendfile` facility when supported.

The benchmark uses:

- **real TCP sockets**
- **high-entropy binary payload data**
- **repeated incremental modifications**
- **actual transmitted application payload accounting**
- **identical logical state sequences**
- **independent receiver reconstruction**
- **SHA-256 exactness verification**

High-entropy data is intentional.

It prevents the benchmark from obtaining its principal gain simply because the source consists of trivially compressible repeated bytes.

The benchmark result therefore measures the benefit of **maintaining state across transmissions**.

---

# 🧪 Run the Benchmark

Prebuilt distributions are supplied for **Linux** and **macOS**.

## Linux

```bash
cd dist_linux
python test.py
```

Expected result includes approximately:

```text
traffic_reduction_x=261.x
exact=True
traffic_target_pass=True
```

## macOS

```bash
cd dist_macos
python test.py
```

Expected result includes approximately:

```text
traffic_reduction_x=261.x
exact=True
traffic_target_pass=True
```

Exact wall-clock timing will vary by machine.

The important reproducible metrics are:

> **transmitted traffic reduction + exact reconstruction**

---

# 🆓 Free Edition

HKD Socket Free is intended to allow the complete transport mechanism and benchmark behavior to be evaluated before purchasing Unlimited.

### Maximum file size

```text
8 MiB
8,388,608 bytes
```

A file of exactly:

```text
8,388,608 bytes
```

is accepted.

A file of:

```text
8,388,609 bytes
```

exceeds the Free limit.

Therefore, the boundary is exactly:

$$
\boxed{
\text{Free}
\iff
|X|
\le
8{,}388{,}608
\text{ bytes}
}
$$

The included `data_free.npz` is sized specifically to exercise the Free edition at its maximum supported file size while still reaching the demonstrated asymptotic benchmark regime.

Run:

```bash
cd dist_linux
python test.py
```

or:

```bash
cd dist_macos
python test.py
```

The Free benchmark is designed to demonstrate approximately **261× traffic reduction** while remaining inside the **8 MiB limit**.

---

# 💎 HKD Socket Unlimited

HKD Socket Unlimited removes the HKD Socket Free file-size restriction.

| Edition | Maximum File Size |
|---|---:|
| **HKD Socket Free** | **8 MiB / 8,388,608 bytes** |
| **HKD Socket Unlimited** | **No HKD Socket file-size limit** |

Files larger than the Free limit produce a licensing message directing the user to HKD Socket Unlimited.

## 🛒 Buy HKD Socket Unlimited

**[Buy HKD Socket Unlimited](https://buy.stripe.com/cNi00c7CH8wfbDQ1grgUM02)**

Unlimited is intended for production and large-data workloads where the objects being transported exceed the Free evaluation limit.

---

# 🌐 Large-Scale Transport

HKD Socket is designed around **streaming and stateful operation** rather than requiring an entire large object to reside in memory.

The transport representation uses large-file-compatible addressing, making the architecture applicable to very large datasets.

Potential applications include:

- AI/ML model checkpoints
- database snapshots
- scientific datasets
- replicated storage
- VM and container state
- large binary artifacts
- frequently updated object-store data
- backup systems
- distributed computing
- telemetry state
- large numerical arrays

For very large objects, the distinction between **total state** and **active state** becomes increasingly important.

If a PB-scale object changes only sparsely between transmissions, retransmitting the complete PB-scale state wastes network bandwidth regardless of how efficient the underlying system call is.

HKD∞ is intended to avoid that repeated work.

---

# 📈 When Will HKD Socket Help Most?

The largest gains occur when:

$$
\boxed{
\frac{|A_k|}
     {|X_k|}
\ll
1
}
$$

In practical terms:

> ### Large object + relatively small changes + repeated transmission = strong HKD Socket workload.

For example, define the active fraction:

$$
\boxed{
\rho_k
=
\frac{|A_k|}
     {|X_k|}
}
$$

As:

$$
\rho_k \rightarrow 0
$$

the opportunity to eliminate redundant transmission grows.

If every byte changes unpredictably between every transmission, there is little historical state to exploit and HKD Socket should **not** be expected to produce a 261× reduction.

Therefore:

> **261× is a measured benchmark result, not a universal compression ratio.**

Performance depends on workload structure.

---

# ⚙️ Runtime Characteristics

HKD Socket is designed so that the continuation workload can follow the active modification set rather than requiring the entire logical object to be retransmitted.

For an object of size \(N\) with active modification volume \(a\), where:

$$
\boxed{
a \ll N
}
$$

the desired continuation behavior is governed primarily by \(a\), rather than repeatedly transmitting \(N\).

Conceptually:

$$
\boxed{
T_{\mathrm{full}}
\sim N
}
$$

per complete transmission, while the HKD∞ continuation target is:

$$
\boxed{
T_{\mathrm{HKD}}
\sim
a+\text{continuation metadata}
}
$$

in the sparse-update regime.

This property is what makes HKD Socket relevant to very large data.

The included **8 MiB benchmark** is intentionally small enough to run quickly while being large enough to demonstrate stable sparse-update transport behavior.

The same HKD∞ transport principle is used by the Unlimited edition without the Free edition's 8 MiB file-size ceiling.

---

# 🔄 Standard Socket vs HKD Socket

### Standard Python

```python
import socket
```

### HKD Socket

```python
import hkd_socket as socket
```

### Standard setup

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
```

### HKD Socket setup

```python
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))
```

The goal is deliberately simple:

```diff
- import socket
+ import hkd_socket as socket
```

while allowing large, repeatedly changing state to use **HKD∞ transport**.

---

# 📊 Performance Summary

| Property | HKD Socket |
|---|---:|
| Linux measured traffic reduction | **~261×** |
| macOS measured traffic reduction | **~261×** |
| Reconstruction | **Exact** |
| Verification | **SHA-256** |
| Transport | **Real TCP** |
| Test payload | **High-entropy binary** |
| Free maximum | **8 MiB** |
| Unlimited maximum | **No HKD Socket file-size limit** |

---

# ⚡ HKD∞ Transport Summary

At the highest level, HKD Socket replaces repeated full-state transmission:

$$
\boxed{
X_0
\rightarrow
X_1
\rightarrow
X_2
\rightarrow
\cdots
\rightarrow
X_n
}
$$

with continuation-preserving active-state transport:

$$
\boxed{
(X_k,S_k)
\xrightarrow{\;\mathcal H_\infty(A_k)\;}
(X_{k+1},S_{k+1})
}
$$

subject to:

$$
\boxed{
|A_k|\ll|X_k|
}
$$

while requiring:

$$
\boxed{
\widehat X_k=X_k
\qquad
\forall k
}
$$

The objective is simple:

> **Do not repeatedly transmit information that the receiver already has.**

---

# Summary

**HKD Socket** is a stateful high-performance transport for large, incrementally changing data.

It is designed around three properties:

1. **Transmit active information rather than repeatedly retransmitting complete state.**
2. **Preserve exact receiver reconstruction.**
3. **Maintain a familiar Python socket-style interface.**

### Measured Benchmark

```text
Linux:  ~261x TCP payload reduction
macOS:  ~261x TCP payload reduction
Exact:  True
```

### Free Edition

```text
Maximum file size:
8 MiB
8,388,608 bytes
```

### Unlimited Edition

```text
No HKD Socket file-size limit
```

---

# 🛒 Get HKD Socket Unlimited

### **[Buy HKD Socket Unlimited](https://buy.stripe.com/cNi00c7CH8wfbDQ1grgUM02)**

**Remove the 8 MiB Free limit and use HKD Socket with large-scale production workloads.**
