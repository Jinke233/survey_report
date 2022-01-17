# survey_report

[base]
species = 某种植物
project_code = F21FTSSCKF0001
author_writer = 杜金科
author_checker = 傅涛

# 支持修改软件，文献自动替换，文献格式自动替换
filter_software = SOAPnuke-v2.1.0
filter_opts = -n 0.02 -l 20 -q 0.4 -i -G 2 --polyX 50 -Q 2 --seqType 0

#采meng查询
sample_name = ybwz

#read length 一般不修改
read_length = 150

# reads 数据量统计
raw_data_Gb = 11.85
clean_data_Gb = 11.64

#jellyfish + genomescope 统计
## jellyfish输出结果
jellyfish_stat = 21mer_counts.stats
## genomescope输出结果(支持 genomescope v1和v2)
genomescope_summary = summary.txt
genomescope_figure = transformed_linear_plot.png

# 输出文件名 默认 工程id+ 物种
outfile = %(project_code)s%(species)ssurvey报告.docx

