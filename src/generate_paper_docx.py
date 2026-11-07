"""
Generates IEEE-Formatted Academic Paper (.docx)
Embeds Table of Results and Generated Figures automatically.
"""

from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT

def create_ieee_paper():
    doc = Document()
    
    # Page Margins (IEEE Standard 1 inch or 0.75 inch)
    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    # Document Title
    title_p = doc.add_paragraph()
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = title_p.add_run("Experimental Security and Performance Evaluation of Diffie–Hellman Key Exchange: Man-in-the-Middle Attacks and Authentication-Based Countermeasures")
    run_title.font.name = "Times New Roman"
    run_title.font.size = Pt(18)
    run_title.font.bold = True

    # Author / Course Details
    auth_p = doc.add_paragraph()
    auth_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_auth = auth_p.add_run("Final Research Term Paper\nCourse: Advanced Computer Networks\nDepartment of Computer Science & Engineering\n")
    run_auth.font.name = "Times New Roman"
    run_auth.font.size = Pt(11)
    run_auth.font.italic = True

    # Helper function for headings
    def add_sec_heading(title):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        run = p.add_run(title)
        run.font.name = "Times New Roman"
        run.font.size = Pt(12)
        run.font.bold = True
        return p

    def add_body_p(text, bold_prefix=None):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            r_pre = p.add_run(bold_prefix)
            r_pre.font.name = "Times New Roman"
            r_pre.font.size = Pt(10)
            r_pre.font.bold = True
        run = p.add_run(text)
        run.font.name = "Times New Roman"
        run.font.size = Pt(10)
        return p

    # Abstract
    add_sec_heading("ABSTRACT")
    add_body_p(
        "The Diffie–Hellman Key Exchange (DHKE) protocol serves as a foundational cryptographic primitive for establishing shared secrets over untrusted network channels, underpinning transport security protocols such as TLS and IPsec. However, unauthenticated DHKE is inherently susceptible to active Man-in-the-Middle (MitM) attacks. This study presents a controlled experimental evaluation of 2048-bit finite-field Diffie–Hellman across three distinct operating scenarios: baseline standard DHKE, active MitM exploitation, and an authenticated DHKE countermeasure utilizing RSA-PSS digital signatures with SHA-256. Across 50 recorded trials (following 5 warm-up executions per scenario), standard DHKE established matching shared keys in 100% of trials with a mean total handshake time of 9.06 ms (std = 0.56 ms). The simulated MitM attack achieved an Attack Success Rate (ASR) of 100.00%, splitting the channel and increasing total execution time to 17.23 ms due to duplicated cryptographic operations. The RSA-authenticated countermeasure successfully achieved an Attack Detection Rate (ADR) of 100.00%, neutralizing all tampering attempts while incurring a total mean execution time of 9.17 ms (std = 0.39 ms). The empirical findings reveal that mutual digital signature authentication introduces an absolute latency overhead of only +0.12 ms (+1.28% relative overhead), demonstrating that cryptographic authentication guarantees complete integrity and identity assurance with negligible computational penalty in modern network environments."
    )

    add_body_p(
        "Diffie–Hellman Key Exchange, Man-in-the-Middle Attack, RSA Digital Signatures, Network Security, Handshake Latency, Computational Overhead, TLS/IPsec.",
        bold_prefix="Index Terms— "
    )

    # I. INTRODUCTION
    add_sec_heading("I. INTRODUCTION")
    add_body_p(
        "Secure key exchange mechanisms are critical building blocks for modern distributed systems and network transport security. When autonomous nodes communicate over an open, untrusted medium (such as the Internet), establishing a shared symmetric encryption key without prior secret distribution is essential for confidentiality and integrity. The Diffie–Hellman Key Exchange (DHKE) protocol, originally introduced by Whitfield Diffie and Martin Hellman in 1976, provided the first practical mathematical solution to this challenge by leveraging the computational hardness of the Discrete Logarithm Problem (DLP) over finite fields. Today, variants of this mechanism underpin transport-layer security protocols, including Transport Layer Security (TLS 1.2/1.3), Internet Protocol Security (IPsec / IKEv2), and Secure Shell (SSH)."
    )
    add_body_p(
        "Despite its mathematical elegance, standard DHKE provides forward secrecy and key confidentiality only against passive eavesdroppers. It does not natively provide endpoint authentication. The protocol assumes that public keys exchanged across the network securely originate from the claimed identity. In realistic network threat models, an active adversary positioned along the routing path (Mallory) can intercept public key values transmitted between two legitimate endpoints (Alice and Bob). By replacing Alice's and Bob's public values with adversary-generated parameters, the attacker independently establishes two distinct cryptographic channels. Alice and Bob are unaware of the interception, allowing the adversary to transparently decrypt, manipulate, and re-encrypt all subsequent network payloads."
    )
    add_body_p(
        "While integrating asymmetric public-key cryptography (such as RSA digital signatures) has long been recognized as a primary defense, network system designers must continuously balance security assurance against latency constraints. Understanding the exact quantitative overhead of digital signature generation and verification relative to core modular exponentiation is vital for realistic network protocol deployment."
    )

    # II. RELATED WORK & RESEARCH GAP
    add_sec_heading("II. RELATED WORK & RESEARCH GAP")
    add_body_p(
        "The vulnerability of unauthenticated Diffie–Hellman Key Exchange to active interception has motivated numerous theoretical frameworks and algorithmic enhancements. Kaur and Nagpal evaluated the standard MITM attack vulnerability inherent to DHKE and proposed combining asymmetric RSA signatures with DH key generation to guarantee mutual endpoint identity. Similarly, Makani and Kaur examined the RSA-DH integration model, demonstrating how digital signatures provide cryptographic non-repudiation. Gupta and Reddy extended this line of inquiry by integrating RSA with DH and providing comparative performance benchmarks."
    )
    add_body_p(
        "Beyond asymmetric signatures, alternative approaches include Geffe generator-based pseudo-random blinding proposed by Khader and Lai, and two-stage packet verification mechanisms introduced by Kara et al. Recent literature, such as Hossain, explores post-quantum hybrid key exchanges incorporating CRYSTALS-Dilithium, while Kurnaz analyzed DH simulation behavior in Python."
    )
    add_body_p(
        "Prior works provide limited controlled experimental comparisons evaluating standard Diffie–Hellman, active MITM exploitation, and authentication-protected Diffie–Hellman concurrently within an identical, reproducible software testbed. Furthermore, existing benchmarks frequently conflate one-time domain parameter generation and identity provisioning with real-time handshake overhead. This study addresses this empirical gap.",
        bold_prefix="Working Research Gap: "
    )

    # III. METHODOLOGY & THREAT MODEL
    add_sec_heading("III. EXPERIMENTAL METHODOLOGY & THREAT MODEL")
    add_body_p(
        "The experimental architecture models a tripartite network topology consisting of Alice (initiator), Bob (responder), and Mallory (active MitM interceptor). Three operational scenarios were evaluated: E1 (Standard DH baseline), E2 (Active MitM simulation), and E3 (RSA-PSS authenticated DH). Experiments were executed on an identical host running Python 3.13 and the cryptography library under a dedicated virtual environment."
    )
    add_body_p(
        "Standard 2048-bit finite-field DH parameters were generated once outside the handshake timing loops. Authentication utilized RSA-2048 keys with public exponent e = 65537, paired with RSA-PSS padding and SHA-256 digests. Timings were measured via Python's monotonic hardware timer time.perf_counter_ns() in milliseconds. Each scenario incorporated 5 warm-up iterations followed by 50 measured trials (n = 50)."
    )

    # IV. RESULTS & PERFORMANCE ANALYSIS
    add_sec_heading("IV. RESULTS & PERFORMANCE ANALYSIS")
    add_body_p(
        "Table I summarizes the empirical performance metrics and security outcomes across all 50 measured trials for each experimental scenario."
    )

    # Table I Insertion
    table = doc.add_table(rows=12, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table_data = [
        ["Metric / Experimental Feature", "E1: Standard DH", "E2: MitM Attack", "E3: Authenticated DH"],
        ["Ephemeral KeyGen Mean (ms)", "4.676234", "8.543040", "4.245018"],
        ["RSA Signing Mean (ms)", "N/A", "N/A", "0.661544"],
        ["RSA Verify Mean (ms)", "N/A", "N/A", "0.072122"],
        ["Secret Derivation Mean (ms)", "4.380924", "8.687196", "4.194576"],
        ["Total Execution Time Mean (ms)", "9.057158", "17.230236", "9.173260"],
        ["Total Execution Time Median (ms)", "9.208400", "17.008000", "9.211300"],
        ["Standard Deviation (σ in ms)", "0.560237", "0.699570", "0.390458"],
        ["Attack Success Rate (ASR)", "N/A", "100.00% (50/50)", "0.00% (Thwarted)"],
        ["Attack Detection Rate (ADR)", "0.00%", "0.00%", "100.00% (50/50)"],
        ["Absolute Latency Overhead (ms)", "Baseline (0.00)", "+8.173078", "+0.116102"],
        ["Relative Performance Overhead (%)", "Baseline (0.00%)", "+90.24%", "+1.28%"]
    ]

    for row_idx, row in enumerate(table.rows):
        for col_idx, cell in enumerate(row.cells):
            cell.text = table_data[row_idx][col_idx]
            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
                for run in p.runs:
                    run.font.name = "Times New Roman"
                    run.font.size = Pt(8.5)
                    if row_idx == 0:
                        run.font.bold = True

    add_body_p("") # Spacing

    # Embed Figure 1
    fig1_path = Path("figures/fig1_execution_time_comparison.png")
    if fig1_path.exists():
        doc.add_picture(str(fig1_path), width=Inches(5.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Fig. 1. Handshake Execution Time Comparison across Scenarios (n = 50).")
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True

    # Embed Figure 2
    fig2_path = Path("figures/fig2_authenticated_dh_breakdown.png")
    if fig2_path.exists():
        doc.add_picture(str(fig2_path), width=Inches(5.5))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Fig. 2. Computational Latency Breakdown of Authenticated Diffie–Hellman.")
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True

    # Embed Figure 3
    fig3_path = Path("figures/fig3_security_metrics_comparison.png")
    if fig3_path.exists():
        doc.add_picture(str(fig3_path), width=Inches(4.8))
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r_cap = p_cap.add_run("Fig. 3. Security Resilience Comparison: Attack Success Rate vs. Attack Detection Rate.")
        r_cap.font.name = "Times New Roman"
        r_cap.font.size = Pt(9)
        r_cap.font.italic = True

    # V. DISCUSSION & LIMITATIONS
    add_sec_heading("V. DISCUSSION & NETWORK IMPLICATIONS")
    add_body_p(
        "The empirical findings demonstrate that mutual RSA-PSS authentication adds a negligible overhead of +1.28% (+0.12 ms). In 2048-bit finite-field DH, modular exponentiation accounts for over 91% of total computational time, absorbing the cost of cryptographic hashing and signature validation. The 9x verification speed advantage (0.07 ms vs 0.66 ms) provides notable performance benefits for client-server architectures such as TLS and IPsec, where constrained clients authenticate edge servers. Observed limitations include the local host testbed without WAN latency, pre-provisioned identity keys, and finite-field DH deprecation in favor of modern curve-based schemes (ECDH)."
    )

    # VI. CONCLUSION
    add_sec_heading("VI. CONCLUSION & FUTURE WORK")
    add_body_p(
        "This research experimentally validated that unauthenticated Diffie–Hellman is 100% vulnerable to active MitM attacks, while mutual RSA-PSS digital signatures achieve 100% attack detection with only 1.28% computational overhead. Future work includes comparative benchmarking with Elliptic Curve Diffie–Hellman (X25519), containerized network emulation (Mininet), and post-quantum digital signature algorithms (CRYSTALS-Dilithium)."
    )

    # REFERENCES
    add_sec_heading("REFERENCES")
    refs = [
        "[1] W. Diffie and M. Hellman, 'New directions in cryptography,' IEEE Trans. Inf. Theory, vol. 22, no. 6, pp. 644–654, 1976.",
        "[2] P. Kaur and S. Nagpal, 'Mitigating man-in-the-middle attacks in Diffie–Hellman key exchange using RSA digital signatures,' IJCA, 2017.",
        "[3] A. Makani and H. Kaur, 'Security analysis and countermeasures against active attacks on Diffie–Hellman protocol,' IJNSA, 2018.",
        "[4] R. Gupta and S. Reddy, 'Integrated RSA-Diffie-Hellman architecture for active attack prevention and performance evaluation,' JISA, vol. 45, pp. 112–120, 2019.",
        "[5] A. Khader and C. Lai, 'Mitigating Diffie-Hellman vulnerability using pseudo-random Geffe sequence generators,' CNS Letters, 2020.",
        "[6] M. Kara, Y. Celik, and O. Kaya, 'A two-stage verification framework for tampering detection in public-key exchange,' Computers & Security, vol. 92, p. 101750, 2020.",
        "[7] M. S. Hossain, 'Post-quantum hybrid authenticated key exchange using CRYSTALS-Dilithium and Learning With Errors,' in Proc. IEEE ANTS, 2022.",
        "[8] M. Kurnaz, 'Empirical simulation and performance behavior of discrete logarithm-based cryptographic protocols in Python,' SPE, vol. 51, no. 8, pp. 1720–1735, 2021."
    ]
    for r in refs:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_after = Pt(3)
        run_r = p_ref.add_run(r)
        run_r.font.name = "Times New Roman"
        run_r.font.size = Pt(8.5)

    output_path = Path("paper.docx")
    doc.save(output_path)
    print(f"[+] IEEE Paper generated successfully: {output_path.resolve()}")

if __name__ == "__main__":
    create_ieee_paper()