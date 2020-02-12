import pandas as pd

from create_csv import PROCESSING_DURATION_CSV_PATH, SUCCESS_RATE_CSV_PATH, plot_data_frames


def get_data_frames():
    return pd.read_csv(PROCESSING_DURATION_CSV_PATH, index_col=0), pd.read_csv(SUCCESS_RATE_CSV_PATH, index_col=0)


def main():
    duration_data_frame, success_rate_data_frame = get_data_frames()
    plot_data_frames(duration_data_frame, success_rate_data_frame)


if __name__ == '__main__':
    main()
