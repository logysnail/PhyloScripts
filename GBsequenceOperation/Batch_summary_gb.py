import seqmoder
import os
import Readgb


def batch_summary_gb(all_file_path):
    os.makedirs(f'{all_file_path}_summary')
    for file in os.listdir(all_file_path):
        with open(f'{all_file_path}_summary/{file}.csv', "w") as summary_gb_file:
            try:
                gb_records = seqmoder.get_list(f'{all_file_path}/{file}/GenBank/sequence.gb')
                summary_list = Readgb.summary_undivided_gb(gb_records)
                for summary in summary_list:
                    summary_gb_file.write(f'{summary}\n')
            except:
                continue


if __name__ == '__main__':
    path = "../YYC"
    batch_summary_gb(path)
