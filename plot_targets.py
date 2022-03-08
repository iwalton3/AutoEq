from frequency_response import FrequencyResponse, DEFAULT_F_MIN, DEFAULT_F_MAX
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from PIL import Image
import os

ROOT_DIR = os.path.abspath(os.path.join(__file__,  os.pardir))


fig, ax = plt.subplots()
fig.set_size_inches(10, 6)
fig.set_facecolor('white')
ax.set_facecolor('white')

ief_inear = FrequencyResponse.read_from_csv(os.path.join(ROOT_DIR, 'compensation', 'ief_neutral_in-ear.csv'))
ief_inear.interpolate()
ief_overear = FrequencyResponse.read_from_csv(os.path.join(ROOT_DIR, 'compensation', 'ief_neutral_over-ear.csv'))
ief_overear.interpolate()

ief_inear_boost = ief_inear.copy()
ief_inear_boost.raw += ief_inear_boost.create_target(6)
ief_overear_boost = ief_overear.copy()
ief_overear_boost.raw += ief_overear_boost.create_target(4)

harman_inear = FrequencyResponse.read_from_csv(os.path.join(ROOT_DIR, 'compensation', 'harman_in-ear_2019v2_wo_bass.csv'))
harman_inear.raw += harman_inear.create_target(6)
harman_overear = FrequencyResponse.read_from_csv(os.path.join(ROOT_DIR, 'compensation', 'harman_over-ear_2018_wo_bass.csv'))
harman_overear.raw += harman_overear.create_target(4)

def do_plot(target, label, color):
    ax.plot(
            target.frequency, target.raw,
            label=label, linewidth=1, color=color
        )

ax.set_xlabel('Frequency (Hz)')
ax.semilogx()
ax.set_xlim([DEFAULT_F_MIN, DEFAULT_F_MAX])
ax.set_ylim([-10, 10])
ax.set_ylabel('Amplitude (dBr)')

do_plot(ief_inear, "IEF In-Ear", '#6666FF')
do_plot(ief_inear_boost, "IEF In-Ear (With Bass)", '#000066')
do_plot(harman_inear, "Harman In-Ear", 'green')

do_plot(ief_overear, "IEF Over-Ear", '#FF6666')
do_plot(ief_overear_boost, "IEF Over-Ear (With Bass)", '#660000')
do_plot(harman_overear, "Harman Over-Ear", 'purple')

ax.set_title("Target Comparison")
if len(ax.lines) > 0:
    ax.legend(fontsize=8)
ax.grid(True, which='major')
ax.grid(True, which='minor')
ax.xaxis.set_major_formatter(ticker.StrMethodFormatter('{x:.0f}'))
ax.set_xticks([20, 50, 100, 200, 500, 1000, 2000, 5000, 10000, 20000])

file_path = "./targets.png"
fig.savefig(file_path, dpi=120)
im = Image.open(file_path)
im = im.convert('P', palette=Image.ADAPTIVE, colors=60)
im.save(file_path, optimize=True)
