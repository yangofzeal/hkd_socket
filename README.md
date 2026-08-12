# ⚡ HKD Socket

### High-Performance Stateful File Transport for Python

**HKD Socket** is a socket-compatible transport designed for
applications that repeatedly transmit large, incrementally changing
data. It uses **HKD∞ active-state reduction** to avoid retransmitting
information that the receiver already possesses.

In the included benchmark, HKD Socket reduces measured TCP application
payload by approximately **261×** while reconstructing the transmitted
state exactly.

> **Measured on both Linux and macOS: \~261× TCP payload reduction.**

------------------------------------------------------------------------

## 🔌 Drop-In Python Socket Migration

A conventional Python socket application may begin with:

``` python
import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

with open("data.npz", "rb") as f:
    sock.sendfile(f)
```

With HKD Socket, the migration is intentionally small:

``` python
import hkd_socket as socket

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, port))

with open("data.npz", "rb") as f:
    sock.sendfile(f)
```

The key change is:

``` diff
- import socket
+ import hkd_socket as socket
```

HKD Socket preserves the familiar lowercase `socket` namespace while
adding **HKD∞ stateful transport capabilities**.

Python's standard `socket.sendfile()` is already a high-performance
baseline: on supported systems it uses the operating system's `sendfile`
facility rather than requiring an ordinary Python read/send loop.

HKD Socket's benchmark therefore compares against an **optimized
system-level file transmission path**, not an intentionally slow Python
baseline.

------------------------------------------------------------------------

# 🚀 Performance

The included HKD Socket benchmark measures real TCP traffic between a
sender and receiver and verifies the reconstructed result
cryptographically.

Typical benchmark result:

``` text
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

Measured TCP payload reduction:

``` text
~261x
```

### macOS

Measured TCP payload reduction:

``` text
~261x
```

The principal performance result is **traffic reduction**, not a claim
that every program executes 261× faster.

Actual wall-clock acceleration depends on network bandwidth, latency,
storage performance, operating system, workload, update density, and
hardware.

On a bandwidth-constrained network, avoiding hundreds of bytes of
transmission for each byte actually required can translate into very
large end-to-end gains.

The larger benchmark was run with:

python test_large.py local --size-gib 0.20 --versions 20 --changed-mib 1

Here, --size-gib 0.20 means the persistent file state is about 204.8 MiB, --versions 20 means that state is transmitted or updated 20 times total, and --changed-mib 1 means that after the first complete snapshot, only 1 MiB changes in each later version. A conventional full-state socket.sendfile() path therefore retransmits roughly 204.8 MiB × 20 = 4.0 GiB, while HKD Socket sends the initial 204.8 MiB once and then only nineteen 1 MiB active updates, for about 223.8 MiB plus tiny protocol metadata. On macOS the measured result was:

BASELINE tx_bytes=4294967461 tx=4.000 GiB elapsed_s=2.006864
HKD tx_bytes=234671869 tx=223.801 MiB elapsed_s=0.442248 active_bytes=19922944 active_ranges=19

same_final_source_sha256=True
payload_reduction_x=18.302012
wall_clock_speedup_x=4.537868
baseline_elapsed_s=2.006864
hkd_elapsed_s=0.442248
baseline_tx=4.000 GiB
hkd_tx=223.801 MiB
PASS_CLIENT=True

This larger run shows the intended HKD∞ scaling more clearly than the earlier --size-gib 0.05 --versions 10 --changed-mib 1 test. In the 0.05 GiB run, the file was only about 51.2 MiB and there were 10 versions, so the full-send baseline moved about 512 MiB, while HKD moved about 60.2 MiB, giving an 8.50× payload reduction. In the new 0.20 GiB run, the persistent state is four times larger and the number of versions doubles to 20, while the active change remains fixed at only 1 MiB per version. That causes the full-send baseline to grow to 4.0 GiB, while HKD grows only to about 223.8 MiB, producing an 18.30× payload reduction—more than twice the 8.50× reduction from the smaller test. The wall-clock speedup does not scale identically because loopback performance is also influenced by memory copies, filesystem writes, system calls, and receiver processing; nevertheless, HKD still completed the Mac run in 0.442 s versus 2.007 s, or 4.54× faster, while reconstructing exactly the same SHA-256 state. The previously marketed ~261× HKD Socket figure comes from a different workload with many more versions and extremely tiny active updates: the gain is fundamentally bounded by how much unchanged state can be reused. With 10 versions, the theoretical ceiling is below 10× because HKD must send the first full snapshot; with 20 versions, the ceiling is below 20×, which is why this run approaches 18.3×. With hundreds of versions and only a few kilobytes changing each time, the full-retransmission baseline repeatedly sends the entire object while HKD continues sending almost only the active deltas, allowing ratios such as ~261×. In other words, 8.5×, 18.3×, and 261× are not conflicting numbers—they are different points on the same scaling curve, controlled primarily by state size, number of versions, and fraction of the state that changes per update.

------------------------------------------------------------------------

# 🧠 Why HKD Socket Is Fast

HKD Socket is **not simply another compression codec**.

Traditional compression asks approximately:

> **How can this byte sequence be represented using fewer bits?**

HKD Socket asks a different question:

> **Given the state already established at the receiver, what
> information must actually cross the network to advance that state
> exactly?**

This distinction is particularly important for large objects that change
incrementally.

------------------------------------------------------------------------

# ∞ HKD∞ Mathematical Model

HKD Socket treats a transmitted object as a sequence of states, written
conceptually as **X0, X1, X2, ..., Xn**. A conventional full-state
transport sends each complete state, so its total transmitted volume
grows approximately with the sum of the sizes of all states. If each
state contains approximately **N bytes** and there are **n + 1 states**,
conventional transmission therefore communicates approximately **(n + 1)
× N bytes** before accounting for ordinary protocol overhead.

HKD∞ instead maintains synchronized continuation state between the
sender and receiver. For each transition from state **Xk** to state
**X(k+1)**, HKD∞ identifies an active subset **Ak** containing the
information necessary to advance the receiver to the next exact state.
The remainder of the state is treated as already established information
and does not need to be retransmitted merely because another version has
been produced.

The fundamental sparse-update condition is that the size of **Ak** is
much smaller than the size of **Xk**. In mathematical terminology,
**\|Ak\| \<\< \|Xk\|**. Under this condition, full-state transport
remains proportional to the complete state size, while HKD∞ transport is
governed primarily by the active information plus the continuation
metadata required to reconstruct the transition.

Conceptually, conventional transmission has total communication
proportional to **the sum of \|Xk\| over all k**, whereas HKD∞ seeks
communication proportional to **the sum of \|Ak\| plus continuation
metadata over all k**. The ratio between these quantities describes the
available traffic-reduction opportunity.

The receiver is required to reconstruct each new state exactly. If the
reconstructed state is denoted **X-hat(k)**, the exactness requirement
is simply that **X-hat(k) equals Xk for every transmitted state**. The
included benchmark verifies this requirement independently using
SHA-256: the sender and receiver must produce identical SHA-256 digests
for the reconstructed final object.

------------------------------------------------------------------------

# 🔄 Active-State Reduction

At a high level, HKD∞ divides the logical state into two conceptual
components: an **active component A**, which requires new communication,
and an **inactive or preserved component I**, whose information is
already represented by the synchronized continuation state.

The purpose of HKD∞ is not to approximate or discard the inactive
component. Instead, the existing receiver state preserves it while
communication concentrates on the active component. After a successful
transition, the resulting state becomes the continuation point for the
next transition.

For sparse modifications, the active component can be much smaller than
the complete object. If a very large object changes only in a relatively
small number of places, the amount of information that must be
communicated can therefore be dramatically smaller than the size of the
complete object.

The proprietary implementation contains additional mechanisms for
efficiently maintaining and transporting this continuation state. Those
implementation details are not required to use HKD Socket.

------------------------------------------------------------------------

# 📦 Is HKD Socket Compression?

**Not in the conventional sense.**

HKD Socket and compression attack different sources of redundancy.

Traditional compression attempts to find redundancy **within one
payload** and encode that payload using fewer bits.

HKD Socket instead exploits information **already shared between
successive sender and receiver states**.

For example, suppose a **1 TB object** has already been established at
the receiver and the next version differs by only **10 MB**.
Conventional full-file transmission begins with another 1 TB logical
transfer and may then attempt to compress it. HKD Socket instead seeks
to communicate the information necessary to advance the existing 1 TB
receiver state to the new state.

This distinction is particularly important for high-entropy binary data.
A high-entropy object may offer relatively little conventional
compression while still exhibiting enormous temporal redundancy if only
a small portion changes between versions.

HKD Socket can therefore be described more precisely as a:

> **Stateful continuation transport optimization rather than simply a
> compression algorithm.**

------------------------------------------------------------------------

# 🔐 Exact Reconstruction

HKD Socket is designed for **exact transport**.

Traffic reduction does not relax the correctness requirement.

For every successful HKD Socket transition, the receiver must
reconstruct exactly the state represented by the sender. The benchmark
therefore compares cryptographic hashes rather than relying on
approximate equality, similarity, compression ratios, or
application-level interpretation.

The required condition is:

**SHA-256(sender state) = SHA-256(receiver state)**

A successful benchmark reports:

``` text
baseline_exact=True
hkd_exact=True
cross_path_same_final_file=True
exact=True
```

------------------------------------------------------------------------

# 🔬 Benchmark Methodology

The included benchmark compares:

``` text
Python socket.sendfile()
        vs.
HKD Socket
```

Python's `socket.socket.sendfile()` is a strong baseline because it uses
the operating system's high-performance file-transmission facilities
when supported.

The benchmark uses:

-   **real TCP sockets**
-   **high-entropy binary payload data**
-   **repeated incremental modifications**
-   **actual transmitted application payload accounting**
-   **identical logical state sequences**
-   **independent receiver reconstruction**
-   **SHA-256 exactness verification**

High-entropy data is intentional. It prevents the benchmark from
obtaining its principal gain simply because the source consists of
trivially compressible repeated bytes.

The benchmark result therefore measures the benefit of **maintaining
state across transmissions**.

------------------------------------------------------------------------

# 🧪 Run the Benchmark

Prebuilt distributions are supplied for **Linux** and **macOS**.

## Linux

``` bash
cd dist_linux
python test.py
```

Expected result includes approximately:

``` text
traffic_reduction_x=261.x
exact=True
traffic_target_pass=True
```

## macOS

``` bash
cd dist_macos
python test.py
```

Expected result includes approximately:

``` text
traffic_reduction_x=261.x
exact=True
traffic_target_pass=True
```

Exact wall-clock timing will vary by machine.

The principal reproducible metrics are:

> **Transmitted TCP payload reduction + exact reconstruction**

------------------------------------------------------------------------

# 🆓 Free Edition

HKD Socket Free is intended to allow the complete transport mechanism
and benchmark behavior to be evaluated before purchasing Unlimited.

## Maximum File Size

``` text
8 MiB
8,388,608 bytes
```

A file of exactly:

``` text
8,388,608 bytes
```

is accepted.

A file of:

``` text
8,388,609 bytes
```

exceeds the Free limit.

In plain mathematical terms:

**Free edition is permitted when file size is less than or equal to
8,388,608 bytes.**

The included `data_free.npz` is sized specifically to exercise the Free
edition at its maximum supported file size while still reaching the
demonstrated benchmark regime.

Run:

``` bash
cd dist_linux
python test.py
```

or:

``` bash
cd dist_macos
python test.py
```

The Free benchmark is designed to demonstrate approximately **261× TCP
payload reduction** while remaining inside the **8 MiB limit**.

------------------------------------------------------------------------

# 💎 HKD Socket Unlimited

HKD Socket Unlimited removes the HKD Socket Free file-size restriction.

  Edition                                      Maximum File Size
  -------------------------- -----------------------------------
  **HKD Socket Free**                **8 MiB / 8,388,608 bytes**
  **HKD Socket Unlimited**     **No HKD Socket file-size limit**

Files larger than the Free limit produce a licensing message directing
the user to HKD Socket Unlimited.

## 🛒 Buy HKD Socket Unlimited

**[Buy HKD Socket
Unlimited](https://buy.stripe.com/cNi00c7CH8wfbDQ1grgUM02)**

Unlimited is intended for production and large-data workloads where the
objects being transported exceed the Free evaluation limit.

------------------------------------------------------------------------

# 🌐 Large-Scale Transport

HKD Socket is designed around **streaming and stateful operation**
rather than requiring an entire large object to reside in memory.

The transport representation uses large-file-compatible addressing,
making the architecture applicable to very large datasets.

Potential applications include:

-   AI/ML model checkpoints
-   database snapshots
-   scientific datasets
-   replicated storage
-   VM and container state
-   large binary artifacts
-   frequently updated object-store data
-   backup systems
-   distributed computing
-   telemetry state
-   large numerical arrays

For very large objects, the distinction between **total state** and
**active state** becomes increasingly important.

If a PB-scale object changes only sparsely between transmissions,
retransmitting the complete PB-scale state wastes network bandwidth
regardless of how efficient the underlying full-file transmission
primitive is.

HKD∞ is intended to avoid that repeated work.

------------------------------------------------------------------------

# 📈 Active Fraction

A useful quantity for describing an HKD Socket workload is the **active
fraction**.

For state k, define the active fraction conceptually as:

**rho(k) = \|Ak\| / \|Xk\|**

When rho is close to **1**, most of the object has changed and there is
relatively little historical state to exploit.

When rho is much smaller than **1**, only a small fraction of the object
requires new communication. This is the regime in which HKD Socket can
provide large traffic reductions.

As the active fraction approaches zero, the potential advantage of
avoiding complete retransmission increases.

This leads to the practical workload rule:

> ### Large object + relatively small changes + repeated transmission = strong HKD Socket workload.

If every byte changes unpredictably between every transmission, there is
little historical state to exploit and HKD Socket should **not** be
expected to produce a 261× reduction.

> **261× is a measured benchmark result, not a universal compression
> ratio.**

Performance depends on workload structure.

------------------------------------------------------------------------

# ⚙️ Runtime Scaling

Let **N** represent the complete object size and **a** represent the
amount of active modification data for a particular transition.

A conventional complete transfer communicates an amount of data governed
primarily by **N**.

In the sparse-update regime, HKD∞ instead seeks a continuation cost
governed primarily by **a plus the metadata necessary to describe and
reconstruct the transition**.

The important condition is:

**a \<\< N**

This distinction becomes increasingly important as N becomes very large.
If a TB-scale or PB-scale object changes sparsely, repeatedly
retransmitting N bytes wastes network bandwidth even if the underlying
full-file transmission primitive itself is highly optimized.

HKD Socket is designed to avoid that repeated full-state communication.

The included **8 MiB benchmark** is intentionally small enough to run
quickly while being large enough to demonstrate stable sparse-update
transport behavior.

The same HKD∞ transport principle is used by the Unlimited edition
without the Free edition's 8 MiB file-size ceiling.

------------------------------------------------------------------------

# 📊 Interpreting the 261× Result

The measured approximately **261× result is a TCP payload-reduction
measurement for the included sparse-update benchmark**.

It is not a claim that every network workload will receive a 261×
reduction, nor that every application will execute 261× faster.

The benchmark represents a workload where successive states are large
relative to their active modifications. In that regime, HKD∞ can avoid
transmitting information already established at the receiver.

If every byte changes independently and unpredictably between successive
versions, the active fraction approaches 1 and there is correspondingly
less redundant transmission for HKD Socket to eliminate.

The benchmark result should therefore be interpreted as:

> **Approximately 261× less TCP application payload than repeated full
> `socket.sendfile()` transmission on the included sparse-update
> workload, while maintaining exact receiver reconstruction.**

The same approximately **261× TCP payload-reduction result** is
demonstrated by the included Linux and macOS benchmark distributions.

------------------------------------------------------------------------

# 🔄 Standard Socket vs HKD Socket

### Standard Python

``` python
import socket
```

### HKD Socket

``` python
import hkd_socket as socket
```

The goal is deliberately simple:

``` diff
- import socket
+ import hkd_socket as socket
```

while allowing large, repeatedly changing state to use **HKD∞
transport**.

------------------------------------------------------------------------

# 📊 Performance Summary

  Property                                                        HKD Socket
  -------------------------------------- -----------------------------------
  Linux measured TCP payload reduction                            **\~261×**
  macOS measured TCP payload reduction                            **\~261×**
  Reconstruction                                                   **Exact**
  Verification                                                   **SHA-256**
  Transport                                                     **Real TCP**
  Test payload                                       **High-entropy binary**
  Free maximum                                   **8 MiB / 8,388,608 bytes**
  Unlimited maximum                        **No HKD Socket file-size limit**

------------------------------------------------------------------------

# ⚡ HKD∞ Transport Summary

At the highest level, HKD Socket replaces repeated complete-state
transmission with **continuation-preserving active-state transport**.

Instead of treating every new version as an entirely new object that
must be sent from beginning to end, HKD∞ treats the receiver's existing
state as part of the transport context.

For each transition:

-   **Xk** represents the current complete state.
-   **X(k+1)** represents the next complete state.
-   **Ak** represents the active information required for the
    transition.
-   The desired sparse regime is **\|Ak\| \<\< \|Xk\|**.
-   The reconstructed receiver state must equal the sender state
    exactly.

The objective is simple:

> **Do not repeatedly transmit information that the receiver already
> has.**

------------------------------------------------------------------------

# Summary

**HKD Socket** is a stateful high-performance transport for large,
incrementally changing data.

It is designed around three properties:

1.  **Transmit active information rather than repeatedly retransmitting
    complete state.**
2.  **Preserve exact receiver reconstruction.**
3.  **Maintain a familiar Python socket-style interface.**

### Measured Benchmark

``` text
Linux:  ~261x TCP payload reduction
macOS:  ~261x TCP payload reduction
Exact:  True
```

### Free Edition

``` text
Maximum file size:
8 MiB
8,388,608 bytes
```

### Unlimited Edition

``` text
No HKD Socket file-size limit
```

### Receiver Requirement

HKD Socket requires HKD-aware transport at both ends of the network connection to achieve the measured ~261× TCP payload reduction. The sender transmits an initial state followed by compact HKD∞ continuation updates rather than retransmitting the complete file each time, so the receiving endpoint must preserve synchronized state and reconstruct each new version exactly. The receiving application itself can still be ordinary Python or other unmodified software if an HKD Socket receiver or proxy sits in front of it and presents the reconstructed data as a normal byte stream or file. In short: the application behind the receiver does not have to change, but the network endpoint receiving HKD traffic must understand HKD Socket.

------------------------------------------------------------------------

# 🛒 Get HKD Socket Unlimited

### **[Buy HKD Socket Unlimited](https://buy.stripe.com/cNi00c7CH8wfbDQ1grgUM02)**

**Remove the 8 MiB Free limit and use HKD Socket with large-scale
production workloads.**
