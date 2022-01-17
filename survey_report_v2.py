import sys
import time
import logging
import subprocess
import configparser
from docxtpl import DocxTemplate, InlineImage, RichText
from docx.shared import Mm






def parse_kmer_stat(jellyfish_stat, genomescope_summary):
    kmer_stat = {}
    with open(jellyfish_stat, 'r') as JS:
        for line in JS:
            if line.startswith('Total'):
                entry = line.rstrip().split()
                kmer_stat['total_kmer_num'] = format(int(entry[1]), ',')

                # stat peak_depth
    # start_parse = False
    # with open(genomescope_model, 'r') as GM:
    #     for line in GM:
    #         if line.startswith('Parameters'):
    #             start_parse = True
    #             continue
    #
    #         if start_parse:
    #             if line.startswith('kmercov'):
    #                 entry = line.rstrip().split()
    #                 kmer_stat['peak_depth'] = float(entry[1]) * 2
    #                 break

    with open(genomescope_summary, 'r') as GS:
        for line in GS:
            if line.startswith('k ='):
                entry = line.rstrip().split()
                kmer_stat['kmer'] = int(entry[-1])
            elif line.startswith('Heterozygous') or line.startswith('Heterozygosity'):
                entry = line.rstrip().split()
                kmer_stat['hete_perc'] = round(float((float(entry[-1][:-1]) + float(entry[-2][:-1]))/2), 2)
                if  kmer_stat['hete_perc'] > 0.5:
                    kmer_stat['heterozygosity'] = "高杂合"
                else:
                    kmer_stat['heterozygosity'] = "低杂合"
            elif line.startswith('Genome Haploid Length'):
                entry = line.rstrip().split()
                kmer_stat['genome_size'] = entry[-2]
                genome_size = int(entry[-2].replace(',', ''))
            elif line.startswith('Genome Repeat Length'):
                entry = line.rstrip().split()
                repeat_size = int(entry[-2].replace(',', ''))

    kmer_stat['repeat_perc'] = round(repeat_size / genome_size * 100, 2)
    if kmer_stat['repeat_perc'] > 50:
        kmer_stat['repeat'] = "高重复"
    else:
        kmer_stat['repeat'] = "低重复"
    kmer_stat['depth'] = round( (float(clean_data_Gb) / (genome_size/1000000000)) , 2)

    return kmer_stat

def add_reference(software):
    ref = {}
    if "SOAP" in software:
        reference = RichText("Chen, Y. ")
        reference.add("et al", italic=True)
        reference.add(
            ". SOAPnuke: a MapReduce acceleration-supported software for integrated quality control and preprocessing of high-throughput sequencing data. ")
        reference.add("Gigascience", italic=True)
        reference.add(" 7", bold=True)
        reference.add(", gix120 (2018).")
    elif "fastp" in software:
        reference = RichText("Chen S, Zhou Y, Chen Y, Gu J. fastp: an ultra-fast all-in-one FASTQ preprocessor. ")
        reference.add("Bioinformatics", italic = True)
        reference.add(" 34", bold = True)
        reference.add(", i884-i890 (2018).")
    ref["reference"] = reference
    return ref


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format='%(asctime)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    config = configparser.ConfigParser()
    config.read(sys.argv[1])

    tpl = DocxTemplate('基因组Survey结题报告_v2.docx')

    context = {'species': config['base']['species'],
               'project_code': config['base']['project_code'],
               'author_writer': config['base']['author_writer'],
               'author_checker': config['base']['author_checker'],
               'year': time.localtime(time.time()).tm_year,
               'month': time.localtime(time.time()).tm_mon,
               'day': time.localtime(time.time()).tm_mday,
               'filter_software': config['base']['filter_software'],
               'filter_opts': config['base']['filter_opts'],
               'sample_name': config['base']['sample_name'],
               'read_length': config['base']['read_length'],
               'raw_data_Gb': config['base']['raw_data_Gb'],
               'clean_data_Gb': config['base']['clean_data_Gb'],
               'genomescope_figure': InlineImage(tpl, config['base']['genomescope_figure'], width=Mm(160))}
    clean_data_Gb = config['base']['clean_data_Gb']


    logging.info('Parse k-mer stat.')
    context.update(parse_kmer_stat(config['base']['jellyfish_stat'], \
                                   config['base']['genomescope_summary']))
                                   #config['base']['genomescope_model']))
    logging.info("add_reference")
    context.update(add_reference(config['base']['filter_software']))
    # config['base']['genomescope_model']))
    logging.info('Render docx file')
    tpl.render(context)
    tpl.save(config['base']['outfile'])
