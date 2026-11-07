"""
Generates Academic Conference / Term Paper Presentation (.pptx)
Includes clean layout, timing charts, and security evaluation slides.
"""

from pathlib import Path
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

def create_presentation():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5) # 16:9 Widescreen standard

    # Theme Colors
    COLOR_PRIMARY = RGBColor(26, 54, 93)   # Deep Navy
    COLOR_ACCENT = RGBColor(197, 48, 48)   # Crimson Red
    COLOR_SUCCESS = RGBColor(40, 167, 69)  # Green
    COLOR_TEXT = RGBColor(45, 55, 72)      # Charcoal

    blank_layout = prs.slide_layouts[6]

    def add_header(slide, title_text, category="ADVANCED COMPUTER NETWORKS"):
        # Header banner text
        txBox = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(1.0))
        tf = txBox.text_frame
        tf.word_wrap = True
        
        p_sub = tf.paragraphs[0]
        p_sub.text = category.upper()
        p_sub.font.size = Pt(11)
        p_sub.font.bold = True
        p_sub.font.color.rgb = COLOR_ACCENT

        p_main = tf.add_paragraph()
        p_main.text = title_text
        p_main.font.size = Pt(24)
        p_main.font.bold = True
        p_main.font.color.rgb = COLOR_PRIMARY

    # --- SLIDE 1: Title Slide ---
    slide1 = prs.slides.add_slide(blank_layout)
    tb1 = slide1.shapes.add_textbox(Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.0))
    tf1 = tb1.text_frame
    tf1.word_wrap = True

    p1 = tf1.paragraphs[0]
    p1.text = "Experimental Security and Performance Evaluation of Diffie–Hellman Key Exchange"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = COLOR_PRIMARY
    p1.alignment = PP_ALIGN.CENTER

    p1_sub = tf1.add_paragraph()
    p1_sub.text = "Man-in-the-Middle Attacks and Authentication-Based Countermeasures"
    p1_sub.font.size = Pt(20)
    p1_sub.font.color.rgb = COLOR_ACCENT
    p1_sub.alignment = PP_ALIGN.CENTER

    p1_meta = tf1.add_paragraph()
    p1_meta.text = "\nCourse: Advanced Computer Networks\nControlled Experimental Cryptographic Benchmark"
    p1_meta.font.size = Pt(14)
    p1_meta.font.color.rgb = COLOR_TEXT
    p1_meta.alignment = PP_ALIGN.CENTER

    # --- SLIDE 2: Research Motivation & Problem Statement ---
    slide2 = prs.slides.add_slide(blank_layout)
    add_header(slide2, "Research Motivation: The Missing Authentication in DHKE")
    tb2 = slide2.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    bullets2 = [
        ("The Foundation of Transport Security: ", "Diffie–Hellman (DHKE) is essential for key agreement in TLS, IPsec, and SSH."),
        ("The Inherent Vulnerability: ", "Standard DHKE guarantees forward secrecy against passive eavesdroppers, but provides zero endpoint authentication."),
        ("The Threat Model: ", "An active Man-in-the-Middle (MitM) attacker (Mallory) can intercept public parameters, deceive both endpoints, and split the channel."),
        ("The Performance Dilemma: ", "While digital signatures solve this problem, does authentication introduce an unacceptable latency overhead for high-throughput networks?"),
        ("Primary Goal: ", "Empirically measure the attack success rate and quantify the exact microsecond overhead of RSA-PSS authentication.")
    ]
    for bold_txt, norm_txt in bullets2:
        p = tf2.add_paragraph()
        p.space_after = Pt(14)
        r1 = p.add_run()
        r1.text = "• " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(16)
        r1.font.color.rgb = COLOR_PRIMARY
        r2 = p.add_run()
        r2.text = norm_txt
        r2.font.size = Pt(16)
        r2.font.color.rgb = COLOR_TEXT

    # --- SLIDE 3: Methodology & Experimental Scenarios ---
    slide3 = prs.slides.add_slide(blank_layout)
    add_header(slide3, "Controlled Experimental Architecture (E1, E2, E3)")
    tb3 = slide3.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    bullets3 = [
        ("Scenario E1 — Baseline Standard DH: ", "Alice <-> Bob (Verify functionality and establish reference latency)."),
        ("Scenario E2 — Active MitM Attack: ", "Alice <-> Mallory <-> Bob (Mallory establishes independent keys K_AM and K_MB)."),
        ("Scenario E3 — Authenticated Countermeasure: ", "Alice <-> Bob with mutual RSA-2048 PSS signatures over SHA-256 digests."),
        ("Experimental Rigor: ", "Executed on Python 3.13 with cryptography library; high-precision monotonic timing (perf_counter_ns)."),
        ("Statistical Protocol: ", "5 warm-up runs + 50 measured trials (n = 50) per scenario to ensure statistical confidence.")
    ]
    for bold_txt, norm_txt in bullets3:
        p = tf3.add_paragraph()
        p.space_after = Pt(14)
        r1 = p.add_run()
        r1.text = "• " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(16)
        r1.font.color.rgb = COLOR_PRIMARY
        r2 = p.add_run()
        r2.text = norm_txt
        r2.font.size = Pt(16)
        r2.font.color.rgb = COLOR_TEXT

    # --- SLIDE 4: Handshake Execution Time Comparison (Figure 1) ---
    slide4 = prs.slides.add_slide(blank_layout)
    add_header(slide4, "Empirical Execution Time Comparison")
    fig1 = Path("figures/fig1_execution_time_comparison.png")
    if fig1.exists():
        slide4.shapes.add_picture(str(fig1), Inches(0.8), Inches(1.7), width=Inches(7.2))
    tb4 = slide4.shapes.add_textbox(Inches(8.2), Inches(1.7), Inches(4.5), Inches(5.0))
    tf4 = tb4.text_frame
    tf4.word_wrap = True
    bullets4 = [
        "Standard DH (E1): Mean 9.06 ms (Baseline reference).",
        "Authenticated DH (E3): Mean 9.17 ms — Handshake time remains virtually identical!",
        "MitM Interception (E2): Mean 17.23 ms (~90% latency increase).",
        "Key Takeaway: Adversary incurs a heavy computational penalty to maintain two dual sessions (4 key generations & 4 derivations)."
    ]
    for b in bullets4:
        p = tf4.add_paragraph()
        p.space_after = Pt(12)
        p.text = "• " + b
        p.font.size = Pt(15)
        p.font.color.rgb = COLOR_TEXT

    # --- SLIDE 5: Computational Latency Breakdown (Figure 2) ---
    slide5 = prs.slides.add_slide(blank_layout)
    add_header(slide5, "Why is Authentication Overhead so Low? (+1.28%)")
    fig2 = Path("figures/fig2_authenticated_dh_breakdown.png")
    if fig2.exists():
        slide5.shapes.add_picture(str(fig2), Inches(0.8), Inches(1.7), width=Inches(7.2))
    tb5 = slide5.shapes.add_textbox(Inches(8.2), Inches(1.7), Inches(4.5), Inches(5.0))
    tf5 = tb5.text_frame
    tf5.word_wrap = True
    bullets5 = [
        "Modular Exponentiation Dominates: KeyGen (4.25 ms) & Secret Derivation (4.19 ms) consume 91.9% of total time.",
        "RSA Signing (0.66 ms): Fast asymmetric operation over SHA-256 digest.",
        "RSA Verification (0.07 ms): 9x faster than signing due to small public exponent (e = 65537).",
        "Conclusion: Adding signatures is computationally absorbed by the finite-field DH operations."
    ]
    for b in bullets5:
        p = tf5.add_paragraph()
        p.space_after = Pt(12)
        p.text = "• " + b
        p.font.size = Pt(15)
        p.font.color.rgb = COLOR_TEXT

    # --- SLIDE 6: Security Resilience Evaluation (Figure 3) ---
    slide6 = prs.slides.add_slide(blank_layout)
    add_header(slide6, "Security Resilience: Complete Attack Mitigation")
    fig3 = Path("figures/fig3_security_metrics_comparison.png")
    if fig3.exists():
        slide6.shapes.add_picture(str(fig3), Inches(0.8), Inches(1.7), width=Inches(6.8))
    tb6 = slide6.shapes.add_textbox(Inches(7.8), Inches(1.7), Inches(4.8), Inches(5.0))
    tf6 = tb6.text_frame
    tf6.word_wrap = True
    bullets6 = [
        "Unauthenticated DH: Attack Success Rate (ASR) = 100.00% across all 50 trials. Channels were silently hijacked.",
        "Authenticated DH: Attack Detection Rate (ADR) = 100.00%. All tampered keys immediately failed signature verification.",
        "Zero False Negatives: Mallory failed to bypass mutual authentication in 100% of attempts.",
        "Trade-off Summary: 100% security improvement achieved for only a +0.12 ms latency cost."
    ]
    for b in bullets6:
        p = tf6.add_paragraph()
        p.space_after = Pt(12)
        p.text = "• " + b
        p.font.size = Pt(15)
        p.font.color.rgb = COLOR_TEXT

    # --- SLIDE 7: Summary Table of Results ---
    slide7 = prs.slides.add_slide(blank_layout)
    add_header(slide7, "Final Experimental Results Summary (n = 50)")
    rows, cols = 7, 4
    table_shape = slide7.shapes.add_table(rows, cols, Inches(1.0), Inches(1.8), Inches(11.3), Inches(4.5))
    table = table_shape.table
    summary_data = [
        ["Metric", "E1: Standard DH", "E2: MitM Attack", "E3: Authenticated DH"],
        ["Mean Total Latency", "9.06 ms", "17.23 ms", "9.17 ms"],
        ["Standard Deviation (σ)", "0.56 ms", "0.70 ms", "0.39 ms"],
        ["Attack Success Rate (ASR)", "N/A", "100.00%", "0.00% (Thwarted)"],
        ["Attack Detection Rate (ADR)", "0.00%", "0.00%", "100.00%"],
        ["Absolute Overhead (ms)", "Baseline (0.00 ms)", "+8.17 ms", "+0.12 ms"],
        ["Percentage Overhead (%)", "Baseline (0.00%)", "+90.24%", "+1.28%"]
    ]
    for r in range(rows):
        for c in range(cols):
            cell = table.cell(r, c)
            cell.text = summary_data[r][c]
            for p in cell.text_frame.paragraphs:
                p.alignment = PP_ALIGN.CENTER
                for run in p.runs:
                    run.font.size = Pt(14)
                    if r == 0:
                        run.font.bold = True
                        run.font.color.rgb = COLOR_PRIMARY

    # --- SLIDE 8: Network Protocol Implications ---
    slide8 = prs.slides.add_slide(blank_layout)
    add_header(slide8, "Network Protocol & Real-World Implications")
    tb8 = slide8.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf8 = tb8.text_frame
    tf8.word_wrap = True
    bullets8 = [
        ("TLS 1.2 / TLS 1.3: ", "Explains why modern web security insists on PKI certificates signing ephemeral DHE/ECDHE keys without perceptible user latency."),
        ("IPsec / IKEv2: ", "VPN security associations can guarantee identity authentication while sustaining high throughput and sub-millisecond setup."),
        ("Asymmetry Benefit: ", "Clients verify signatures in 0.07 ms, making authentication ideal for battery-constrained mobile and IoT nodes connecting to edge servers."),
        ("Layer 2/3 Threat Protection: ", "Even if routing is compromised via ARP spoofing or BGP hijacking, cryptographic signatures render MitM attacks completely ineffective.")
    ]
    for bold_txt, norm_txt in bullets8:
        p = tf8.add_paragraph()
        p.space_after = Pt(14)
        r1 = p.add_run()
        r1.text = "• " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(16)
        r1.font.color.rgb = COLOR_PRIMARY
        r2 = p.add_run()
        r2.text = norm_txt
        r2.font.size = Pt(16)
        r2.font.color.rgb = COLOR_TEXT

    # --- SLIDE 9: Conclusion & Viva Takeaways ---
    slide9 = prs.slides.add_slide(blank_layout)
    add_header(slide9, "Conclusion & Key Takeaways for Defense / Viva")
    tb9 = slide9.shapes.add_textbox(Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2))
    tf9 = tb9.text_frame
    tf9.word_wrap = True
    bullets9 = [
        ("Vulnerability Confirmed: ", "Unauthenticated Diffie–Hellman failed 100% of trials against an active interceptor."),
        ("Countermeasure Proven: ", "RSA-PSS mutual digital signatures achieved 100% attack detection rate."),
        ("Negligible Cost: ", "The performance penalty is only +1.28% (+0.12 ms), conclusively debunking claims that authentication causes excessive computational bottlenecks."),
        ("Defense Summary Statement: ", "'Authentication provides total cryptographic resilience against active MitM attacks with virtually zero overhead penalty in finite-field key exchange.'")
    ]
    for bold_txt, norm_txt in bullets9:
        p = tf9.add_paragraph()
        p.space_after = Pt(16)
        r1 = p.add_run()
        r1.text = "• " + bold_txt
        r1.font.bold = True
        r1.font.size = Pt(16)
        r1.font.color.rgb = COLOR_PRIMARY
        r2 = p.add_run()
        r2.text = norm_txt
        r2.font.size = Pt(16)
        r2.font.color.rgb = COLOR_TEXT

    # Save presentation
    output_path = Path("presentation.pptx")
    prs.save(output_path)
    print(f"[+] Presentation generated successfully: {output_path.resolve()}")

if __name__ == "__main__":
    create_presentation() 