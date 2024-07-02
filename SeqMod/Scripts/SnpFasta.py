import AlignmentOperate as ao

file = ('../TripCpHap/TripCpSNP.fasta')
df_align = ao.read_fasta_as_df("../TripCpHap/TripCp.fasta")
align = ao.Alignment(df_align)
align.snp_cites()
align.write_align_fasta(file)