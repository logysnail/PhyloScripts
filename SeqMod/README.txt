python脚本SnpFasta.py
	使用一个位点出现频次最高的碱基填充了序列中的非ATCG字符，并且保留了snp位点
	或者选择保留gap/missing。
	DNAsp只能全部删除有gap/missing的位点或是把gap/missing作为一种碱基

生成的较短的alignment文件可以放入DNAsp软件生成nex格式或其他格式的单倍型文件

使用genious软件导出为普通的nex格式

使用分布文件与DNAsp文件的一部分内容，放入脚本TraitMatrixNex.py，输出结果调整一下格式后粘贴到genious生成的nex后

使用POPART计算并作图
