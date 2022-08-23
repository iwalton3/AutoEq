import os
import sys
sys.path.insert(1, os.path.realpath(os.path.join(sys.path[0], os.pardir)))
from frequency_response import FrequencyResponse, DEFAULT_F_MIN, DEFAULT_F_MAX

ROOT_DIR = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))

ief_inear = FrequencyResponse.read_from_csv(os.path.join(ROOT_DIR, 'compensation', 'ief_neutral_in-ear.csv'))
ief_inear.interpolate()
ief_overear = FrequencyResponse.read_from_csv(os.path.join(ROOT_DIR, 'compensation', 'ief_neutral_over-ear.csv'))
ief_overear.interpolate()

ief_inear_boost = ief_inear.copy()
ief_inear_boost.raw += ief_inear_boost.create_target(6)
ief_inear_boost.write_to_csv(file_path=os.path.join(ROOT_DIR, 'compensation', 'ief_neutral_in-ear_with_bass.csv'))

ief_overear_boost = ief_overear.copy()
ief_overear_boost.raw += ief_overear_boost.create_target(4)
ief_overear_boost.write_to_csv(file_path=os.path.join(ROOT_DIR, 'compensation', 'ief_neutral_over-ear_with_bass.csv'))
