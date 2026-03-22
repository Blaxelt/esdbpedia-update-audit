import os
import matplotlib.pyplot as plt
import numpy as np

def plot_zipf():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.abspath(os.path.join(script_dir, '../../data/frequency/frecuencia_formas_ortograficas_1_4.txt'))
    
    if not os.path.exists(filepath):
        print(f"Error: File not found at {filepath}")
        return

    frequencies = []
    print(f"Reading file: {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        header = f.readline()
        for line in f:
            parts = line.strip('\n').split('\t')
            if len(parts) >= 2:
                try:
                    freq = int(parts[1])
                    frequencies.append(freq)
                except ValueError:
                    pass

    frequencies.sort(reverse=True)
    frequencies = np.array(frequencies)
    total = frequencies.sum()

    ranks   = np.arange(1, len(frequencies) + 1)
    rel_freq = frequencies / total

    fig, ax = plt.subplots(figsize=(8, 7))

    ax.loglog(ranks, rel_freq, color='blue', linewidth=1, label='CORPES')

    ax.set_xlabel('Rank', fontsize=12)
    ax.set_ylabel('Relative frequency', fontsize=12)
    ax.set_title('Zipf distribution — Orthographic forms (CORPES)', fontsize=13)
    ax.legend(fontsize=11)
    ax.grid(True, which='both', linestyle=':', linewidth=0.5, alpha=0.7)

    plt.tight_layout()

    output_path = os.path.join(script_dir, 'zipf_plot.png')
    plt.savefig(output_path, dpi=150)
    print(f"Graph saved to: {output_path}")

if __name__ == '__main__':
    plot_zipf()