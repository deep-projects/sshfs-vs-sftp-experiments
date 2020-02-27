import pandas as pd

from create_csv import PROCESSING_DURATION_CSV_PATH, plot_data_frames, PROCESSING_DURATION_LABEL, \
    NUM_CONCURRENT_BATCHES_LABEL, MOUNT_LABEL


def get_data_frames():
    processing_time_df = pd.read_csv(PROCESSING_DURATION_CSV_PATH, index_col=0)
    successful_processing_time_df = processing_time_df[processing_time_df.states == 'succeeded']
    return successful_processing_time_df


def analyse_data_frame(duration_data_frame):
    data_frame_5_concurrent_batches_sftp = duration_data_frame[
        (duration_data_frame[NUM_CONCURRENT_BATCHES_LABEL] == 5) & (duration_data_frame[MOUNT_LABEL] == 'sftp')
        ]
    data_frame_5_concurrent_batches_sshfs = duration_data_frame[
        (duration_data_frame[NUM_CONCURRENT_BATCHES_LABEL] == 5) & (duration_data_frame[MOUNT_LABEL] == 'sshfs')
        ]

    data_frame_30_concurrent_batches_sftp = duration_data_frame[
        (duration_data_frame[NUM_CONCURRENT_BATCHES_LABEL] == 30) & (duration_data_frame[MOUNT_LABEL] == 'sftp')
        ]
    data_frame_30_concurrent_batches_sshfs = duration_data_frame[
        (duration_data_frame[NUM_CONCURRENT_BATCHES_LABEL] == 30) & (duration_data_frame[MOUNT_LABEL] == 'sshfs')
        ]

    print('median sftp processing duration for 5 concurrent batches: {:.2f}'.format(
        data_frame_5_concurrent_batches_sftp[PROCESSING_DURATION_LABEL].median()
    ))
    print('median sshfs processing duration for 5 concurrent batches: {:.2f}'.format(
        data_frame_5_concurrent_batches_sshfs[PROCESSING_DURATION_LABEL].median()
    ))
    print('median sftp processing duration for 30 concurrent batches: {:.2f}'.format(
        data_frame_30_concurrent_batches_sftp[PROCESSING_DURATION_LABEL].median()
    ))
    print('median sshfs processing duration for 30 concurrent batches: {:.2f}'.format(
        data_frame_30_concurrent_batches_sshfs[PROCESSING_DURATION_LABEL].median()
    ))


def main():
    duration_data_frame = get_data_frames()
    plot_data_frames(duration_data_frame)

    analyse_data_frame(duration_data_frame)


if __name__ == '__main__':
    main()
