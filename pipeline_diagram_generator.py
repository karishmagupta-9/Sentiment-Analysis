import matplotlib.pyplot as plt
import matplotlib.patches as patches

def generate_academic_pipeline(output_filename="sentiment_sarcasm_pipeline.png"):
    """
    Renders an academic, high-resolution architecture and pipeline diagram
    specifically formatted for engineering project reports.
    """
    # Create 300 DPI high-resolution canvas with standard report proportions
    fig, ax = plt.subplots(figsize=(13, 8), dpi=300)
    ax.set_xlim(0, 13)
    ax.set_ylim(0, 8)
    ax.axis("off")

    # Helper function to draw rounded cards with text
    def draw_card(x, y, w, h, title, subtitle_lines, bg_col, border_col, title_col="#0f172a"):
        rect = patches.FancyBboxPatch(
            (x - w / 2, y - h / 2), w, h,
            boxstyle="round,pad=0.12,rounding_size=0.14",
            facecolor=bg_col,
            edgecolor=border_col,
            linewidth=1.8,
            zorder=2
        )
        ax.add_patch(rect)

        # Title text
        offset_y = 0.22 if subtitle_lines else 0
        ax.text(
            x, y + (h * offset_y), title,
            ha="center", va="center", fontsize=9.5, fontweight="bold",
            color=title_col, family="DejaVu Sans", zorder=3
        )

        # Subtitle bullet points / details
        if subtitle_lines:
            sub_y = y - (h * 0.16)
            ax.text(
                x, sub_y, "\n".join(subtitle_lines),
                ha="center", va="center", fontsize=7.8,
                color="#334155", family="DejaVu Sans", zorder=3, linespacing=1.35
            )

    # Stage 1: Data Ingestion
    draw_card(
        x=2.2, y=6.8, w=3.4, h=1.3,
        title="1. Dataset & Review Input",
        subtitle_lines=[
            "• Amazon Fine Food Reviews (100k samples)",
            "• Raw customer text & 1-5 star ratings"
        ],
        bg_col="#F0F9FF", border_col="#0284C7"
    )

    # Stage 2: Data Preprocessing
    draw_card(
        x=6.5, y=6.8, w=3.6, h=1.3,
        title="2. Text Preprocessing",
        subtitle_lines=[
            "• Lowercasing & contraction expansion",
            "• HTML tag & URL elimination",
            "• Punctuation & special character stripping"
        ],
        bg_col="#EEF2FF", border_col="#6366F1"
    )

    # Stage 3A: Classical ML Branch (Left)
    draw_card(
        x=3.4, y=4.4, w=4.4, h=2.0,
        title="Engine 1: Statistical ML Pipeline",
        subtitle_lines=[
            "• N-Gram Feature Extraction (1, 3)",
            "• Sublinear TF-IDF (75,000 features)",
            "• Multinomial Logistic Regression",
            "➔ Output: Polarity (Pos / Neu / Neg) + Conf %"
        ],
        bg_col="#ECFDF5", border_col="#059669"
    )

    # Stage 3B: Deep Transformer Branch (Right)
    draw_card(
        x=9.6, y=4.4, w=4.4, h=2.0,
        title="Engine 2: RoBERTa Sarcasm Head",
        subtitle_lines=[
            "• Byte-Pair Encoding (BPE) tokenization",
            "• Bidirectional self-attention layers",
            "• Semantic contradiction detection",
            "➔ Output: Sarcasm Probability P(Sarcastic) %"
        ],
        bg_col="#FAF5FF", border_col="#9333EA"
    )

    # Stage 4: Decision & Inversion Engine
    draw_card(
        x=6.5, y=2.0, w=6.8, h=1.4,
        title="3. Decision Boundary Inversion Engine",
        subtitle_lines=[
            "IF P(Sarcastic) ≥ 50% AND Sentiment == Positive:",
            "  ➔ Invert Final Output to Negative (Sarcasm Inverted)",
            "ELSE:",
            "  ➔ Retain Baseline Logistic Regression Prediction"
        ],
        bg_col="#FFFBEB", border_col="#D97706"
    )

    # Stage 5: Output Dashboard
    draw_card(
        x=6.5, y=0.6, w=6.8, h=0.75,
        title="4. Flask Web Application & Calibrated Output Dashboard",
        subtitle_lines=[],
        bg_col="#F8FAFC", border_col="#475569"
    )

    arrow_style = dict(arrowstyle="-|>", lw=1.8, color="#334155", mutation_scale=14)

    # 1 -> 2
    ax.annotate("", xy=(4.7, 6.8), xytext=(3.9, 6.8), arrowprops=arrow_style)

    # 2 -> Engine 1 (down-left)
    ax.annotate("", xy=(3.4, 5.4), xytext=(5.6, 6.15), arrowprops=arrow_style)

    # 2 -> Engine 2 (down-right)
    ax.annotate("", xy=(9.6, 5.4), xytext=(7.4, 6.15), arrowprops=arrow_style)

    # Engine 1 -> Decision (down-right)
    ax.annotate("", xy=(5.2, 2.7), xytext=(3.4, 3.4), arrowprops=arrow_style)

    # Engine 2 -> Decision (down-left)
    ax.annotate("", xy=(7.8, 2.7), xytext=(9.6, 3.4), arrowprops=arrow_style)

    # Decision -> Final Web Output
    ax.annotate("", xy=(6.5, 0.98), xytext=(6.5, 1.3), arrowprops=arrow_style)

    # Diagram Title Header
    ax.text(
        6.5, 7.7, "Dual-Engine Sentiment and Sarcasm Detection System Architecture",
        ha="center", va="center", fontsize=12.5, fontweight="bold",
        color="#0f172a", family="DejaVu Sans"
    )

    plt.tight_layout()
    plt.savefig(output_filename, dpi=300, bbox_inches="tight")
    plt.close()
    print(f"SUCCESS: Pipeline diagram exported cleanly as '{output_filename}'")

if __name__ == "__main__":
    generate_academic_pipeline()