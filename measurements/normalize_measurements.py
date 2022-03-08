# -*- coding: utf-8 -*-

import os
import sys
import argparse
import pathlib
from glob import glob
sys.path.insert(1, os.path.realpath(os.path.join(sys.path[0], os.pardir)))

ROOT_DIR = os.path.abspath(os.path.join(__file__, os.pardir, os.pardir))
from frequency_response import FrequencyResponse

def batch_processing(input_dir, output_dir, compensation):
    comp = FrequencyResponse.read_from_csv(compensation)
    comp.interpolate()
    for fp in glob(os.path.join(input_dir, '*', '*.csv')):
        relfile = os.path.relpath(fp, input_dir)
        print(f"Processing: {relfile}")
        data = FrequencyResponse.read_from_csv(fp)
        data.interpolate()
        data.raw -= comp.raw
        out_file = os.path.join(output_dir, relfile)
        pathlib.Path(os.path.dirname(out_file)).mkdir(parents=True, exist_ok=True)
        data.write_to_csv(file_path=out_file)

def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('--innerfidelity', action='store_true', help='Process Innerfidelity measurements?')
    arg_parser.add_argument('--headphonecom', action='store_true', help='Process Headphone.com measurements?')
    arg_parser.add_argument('--oratory1990', action='store_true', help='Process oratory1990 measurements?')
    arg_parser.add_argument('--rtings', action='store_true', help='Process Rtings measurements?')
    arg_parser.add_argument('--referenceaudioanalyzer', action='store_true',
                            help='Process Reference Audio Analyzer measurements?')
    arg_parser.add_argument('--crinacle', action='store_true', help='Process Crinacle measurements?')
    arg_parser.add_argument('--onear', action='store_true', help='Process on-ear measurements?')
    arg_parser.add_argument('--inear', action='store_true', help='Process in-ear measurements?')
    arg_parser.add_argument('--earbud', action='store_true', help='Process ear bud measurements?')
    cli_args = arg_parser.parse_args()

    innerfidelity = bool(cli_args.innerfidelity)
    headphonecom = bool(cli_args.headphonecom)
    oratory1990 = bool(cli_args.oratory1990)
    rtings = bool(cli_args.rtings)
    referenceaudioanalyzer = bool(cli_args.referenceaudioanalyzer)
    crinacle = bool(cli_args.crinacle)

    onear = bool(cli_args.onear)
    inear = bool(cli_args.inear)
    earbud = bool(cli_args.earbud)

    if not innerfidelity and not headphonecom and not oratory1990 and not rtings and not referenceaudioanalyzer and not crinacle:
        innerfidelity = True
        headphonecom = True
        oratory1990 = True
        rtings = True
        referenceaudioanalyzer = True
        crinacle = True
    if not onear and not inear and not earbud:
        onear = True
        inear = True
        earbud = True

    innerfidelity_overear = os.path.join(ROOT_DIR, 'measurements', 'innerfidelity', 'resources', 'innerfidelity_zero_over-ear.csv')
    innerfidelity_inear = os.path.join(ROOT_DIR, 'measurements', 'innerfidelity', 'resources', 'innerfidelity_zero_in-ear.csv')
    headphonecom_overear = os.path.join(ROOT_DIR, 'measurements', 'headphonecom', 'resources', 'headphonecom_zero_over-ear.csv')
    headphonecom_inear = os.path.join(ROOT_DIR, 'measurements', 'headphonecom', 'resources', 'headphonecom_zero_in-ear.csv')
    rtings_overear = os.path.join(ROOT_DIR, 'measurements', 'rtings', 'resources', 'rtings_zero_over-ear.csv')
    rtings_inear = os.path.join(ROOT_DIR, 'measurements', 'rtings', 'resources', 'rtings_zero_in-ear.csv')
    harman_inear = os.path.join(ROOT_DIR, 'compensation', 'zero.csv')
    harman_overear = os.path.join(ROOT_DIR, 'compensation', 'zero.csv')
    crinacle_ears711_overear = os.path.join(ROOT_DIR, 'measurements', 'crinacle', 'resources', 'crinacle_ears-711_zero_over-ear.csv')
    raa_hdmx = os.path.join(ROOT_DIR, 'measurements', 'referenceaudioanalyzer', 'resources', 'referenceaudioanalyzer_hdm-x_zero_over-ear.csv')
    raa_hdm1 = os.path.join(ROOT_DIR, 'measurements', 'referenceaudioanalyzer', 'resources', 'referenceaudioanalyzer_hdm1_zero_over-ear.csv')
    raa_siec = os.path.join(ROOT_DIR, 'measurements', 'referenceaudioanalyzer', 'resources', 'referenceaudioanalyzer_siec_zero_in-ear.csv')

    if innerfidelity:
        if onear:
            print('\nProcessing Innerfidelity on-ear measurements...')
            batch_processing(
                input_dir=os.path.join(ROOT_DIR, 'measurements', 'innerfidelity', 'data', 'onear'),
                output_dir=os.path.join(ROOT_DIR, 'measurements_normalized', 'innerfidelity', 'data', 'onear'),
                compensation=innerfidelity_overear,
            )

        if inear:
            print('\nProcessing Innerfidelity in-ear measurements...')
            batch_processing(
                input_dir=os.path.join(ROOT_DIR, 'measurements', 'innerfidelity', 'data', 'inear'),
                output_dir=os.path.join(ROOT_DIR, 'measurements_normalized', 'innerfidelity', 'data', 'inear'),
                compensation=innerfidelity_inear,
            )

        if earbud:
            print('\nProcessing Innerfidelity earbud measurements...')
            batch_processing(
                input_dir=os.path.join(ROOT_DIR, 'measurements', 'innerfidelity', 'data', 'earbud'),
                output_dir=os.path.join(ROOT_DIR, 'measurements_normalized', 'innerfidelity', 'data', 'earbud'),
                compensation=innerfidelity_inear,
            )

    if headphonecom:
        if onear:
            print('\nProcessing Headphone.com on-ear measurements...')
            batch_processing(
                input_dir=os.path.join(ROOT_DIR, 'measurements', 'headphonecom', 'data', 'onear'),
                output_dir=os.path.join(ROOT_DIR, 'measurements_normalized', 'headphonecom', 'data', 'onear'),
                compensation=headphonecom_overear,
            )

        if inear:
            print('\nProcessing Headphone.com in-ear measurements...')
            batch_processing(
                input_dir=os.path.join(ROOT_DIR, 'measurements', 'headphonecom', 'data', 'inear'),
                output_dir=os.path.join(ROOT_DIR, 'measurements_normalized', 'headphonecom', 'data', 'inear'),
                compensation=headphonecom_inear,
            )

        if earbud:
            print('\nProcessing Headphone.com earbud measurements...')
            batch_processing(
                input_dir=os.path.join(ROOT_DIR, 'measurements', 'headphonecom', 'data', 'earbud'),
                output_dir=os.path.join(ROOT_DIR, 'measurements_normalized', 'headphonecom', 'data', 'earbud'),
                compensation=headphonecom_inear,
            )

    if oratory1990:
        if onear:
            print('\nProcessing oratory1990 on-ear measurements...')
            batch_processing(
                input_dir=os.path.join(ROOT_DIR, 'measurements', 'oratory1990', 'data', 'onear'),
                output_dir=os.path.join(ROOT_DIR, 'measurements_normalized', 'oratory1990', 'data', 'onear'),
                compensation=harman_overear,
            )

        if inear:
            print('\nProcessing oratory1990 in-ear measurements...')
            batch_processing(
                input_dir=os.path.join(ROOT_DIR, 'measurements', 'oratory1990', 'data', 'inear'),
                output_dir=os.path.join(ROOT_DIR, 'measurements_normalized', 'oratory1990', 'data', 'inear'),
                compensation=harman_inear,
            )

        if earbud:
            print('\nProcessing oratory1990 ear bud measurements...')
            batch_processing(
                input_dir=os.path.join(ROOT_DIR, 'measurements', 'oratory1990', 'data', 'earbud'),
                output_dir=os.path.join(ROOT_DIR, 'measurements_normalized', 'oratory1990', 'data', 'earbud'),
                compensation=harman_inear,
            )

    if rtings:
        if onear:
            # Rtings on-ear Avg
            print('\nProcessing Rtings on-ear measurements...')
            batch_processing(
                input_dir=os.path.join(ROOT_DIR, 'measurements', 'rtings', 'data', 'onear'),
                output_dir=os.path.join(ROOT_DIR, 'measurements_normalized', 'rtings', 'data', 'onear'),
                compensation=rtings_overear,
            )

        if inear:
            print('\nProcessing Rtings in-ear measurements...')
            batch_processing(
                input_dir=os.path.join(ROOT_DIR, 'measurements', 'rtings', 'data', 'inear'),
                output_dir=os.path.join(ROOT_DIR, 'measurements_normalized', 'rtings', 'data', 'inear'),
                compensation=rtings_inear,
            )

        if earbud:
            print('\nProcessing Rtings earbud measurements...')
            batch_processing(
                input_dir=os.path.join(ROOT_DIR, 'measurements', 'rtings', 'data', 'earbud'),
                output_dir=os.path.join(ROOT_DIR, 'measurements_normalized', 'rtings', 'data', 'earbud'),
                compensation=rtings_inear,
            )

    if referenceaudioanalyzer:
        if onear:
            print('\nProcessing Reference Audio Analyzer HDM-X on-ear measurements...')
            batch_processing(
                input_dir=os.path.join(ROOT_DIR, 'measurements', 'referenceaudioanalyzer', 'data', 'onear', 'HDM-X'),
                output_dir=os.path.join(ROOT_DIR, 'measurements_normalized', 'referenceaudioanalyzer', 'data', 'onear', 'HDM-X'),
                compensation=raa_hdmx,
            )
            print('\nProcessing Reference Audio Analyzer HDM1 on-ear measurements...')
            batch_processing(
                input_dir=os.path.join(ROOT_DIR, 'measurements', 'referenceaudioanalyzer', 'data', 'onear', 'HDM1'),
                output_dir=os.path.join(ROOT_DIR, 'measurements_normalized', 'referenceaudioanalyzer',  'data', 'onear', 'HDM1'),
                compensation=raa_hdm1,
            )
        if inear:
            print('\nProcessing Reference Audio Analyzer SIEC in-ear measurements...')
            batch_processing(
                input_dir=os.path.join(ROOT_DIR, 'measurements', 'referenceaudioanalyzer', 'data', 'inear', 'SIEC'),
                output_dir=os.path.join(ROOT_DIR, 'measurements_normalized', 'referenceaudioanalyzer', 'data', 'inear', 'SIEC'),
                compensation=raa_siec,
            )
            print('\nProcessing Reference Audio Analyzer SIEC CUSTOM in-ear measurements...')
            batch_processing(
                input_dir=os.path.join(ROOT_DIR, 'measurements', 'referenceaudioanalyzer', 'data', 'inear', 'SIEC CUSTOM'),
                output_dir=os.path.join(ROOT_DIR, 'measurements_normalized', 'referenceaudioanalyzer', 'data', 'inear', 'SIEC CUSTOM'),
                compensation=raa_siec,
            )
        if earbud:
            print('\nProcessing Reference Audio Analyzer SIEC earbud measurements...')
            batch_processing(
                input_dir=os.path.join(ROOT_DIR, 'measurements', 'referenceaudioanalyzer', 'data', 'earbud', 'SIEC'),
                output_dir=os.path.join(ROOT_DIR, 'measurements_normalized', 'referenceaudioanalyzer', 'data', 'earbud', 'SIEC'),
                compensation=raa_siec,
            )

    if crinacle:
        if onear:
            print('\nProcessing Crinacle Ears-711 on-ear measurements...')
            batch_processing(
                input_dir=os.path.join(ROOT_DIR, 'measurements', 'crinacle', 'data', 'onear', 'Ears-711'),
                output_dir=os.path.join(ROOT_DIR, 'measurements_normalized', 'crinacle', 'data', 'onear', 'Ears-711'),
                compensation=crinacle_ears711_overear,
            )
            print('\nProcessing Crinacle GRAS 43AG-7 on-ear measurements...')
            batch_processing(
                input_dir=os.path.join(ROOT_DIR, 'measurements', 'crinacle', 'data', 'onear', 'GRAS 43AG-7'),
                output_dir=os.path.join(ROOT_DIR, 'measurements_normalized', 'crinacle', 'data', 'onear', 'GRAS 43AG-7'),
                compensation=harman_overear,
            )
        if inear:
            print('\nProcessing Crinacle in-ear measurements...')
            batch_processing(
                input_dir=os.path.join(ROOT_DIR, 'measurements', 'crinacle', 'data', 'inear'),
                output_dir=os.path.join(ROOT_DIR, 'measurements_normalized', 'crinacle', 'data', 'inear'),
                compensation=harman_inear,
            )


if __name__ == '__main__':
    main()
