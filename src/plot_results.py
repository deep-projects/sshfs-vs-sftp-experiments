import pandas as pd

from create_csv import PROCESSING_DURATION_CSV_PATH, plot_data_frames


def get_data_frames():
    processing_time_df = pd.read_csv(PROCESSING_DURATION_CSV_PATH, index_col=0)
    successful_processing_time_df = processing_time_df[processing_time_df.states == 'succeeded']
    return successful_processing_time_df


def main():
    duration_data_frame = get_data_frames()
    plot_data_frames(duration_data_frame)


if __name__ == '__main__':
    main()
