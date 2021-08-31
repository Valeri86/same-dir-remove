import filecmp
from datetime import date
import os

CURRENT_DATE = date.today()
latest_dir = '/example_dir/%s' % CURRENT_DATE

# Make sure latest dir is not part of the comparison
all_other_dirs = [f for f in os.listdir("/example_dir/") if f not in latest_dir]


def dir_compare(latest, others):
    DIR_DIFF = ''
    FILE_DIFF = ''

    # Remove directory if it is empty
    if not os.listdir(others):
        os.rmdir(others)

    else:
        toplevel_dir_compare = filecmp.dircmp(latest, others)

        # If exclusive files or directories exist in one of the directories, nothing will be done
        if not (len(toplevel_dir_compare.left_only) > 0 or len(toplevel_dir_compare.right_only) > 0):
            DIR_DIFF = False

        # Make sure all common files will be compared with their content (shallow=False)
        # filecmp.cmpfiles returns three lists of file names: match, mismatch, errors
        # Mismatch if common files have different content, can not be read, or same file name is compared with same dir name
        (match, mismatch, errors) = filecmp.cmpfiles(latest, others, toplevel_dir_compare.common_files, shallow=False)
        if not (len(mismatch) > 0 or len(errors) > 0):
            FILE_DIFF = False

        if DIR_DIFF == False and FILE_DIFF == False:
            for common_files in toplevel_dir_compare.common_files:
                common_files_latest = os.path.join(latest, common_files)
                common_files_others = os.path.join(others, common_files)
                os.remove(common_files_others)

        # Iterate common subdirectories
        for common_subdir in toplevel_dir_compare.common_dirs:
            common_subdir_latest = os.path.join(latest, common_subdir)
            common_subdir_others = os.path.join(others, common_subdir)

            # start recursion
            dir_compare(common_subdir_latest, common_subdir_others)


if os.path.isdir(latest_dir):
    for _ in range(100):
        for dirs in all_other_dirs:
            full_path_for_all_other_dirs = os.path.join("/example_dir/", dirs)
            # Do not compare empty directories
            # Remove directory if it is empty
            if os.path.isdir(full_path_for_all_other_dirs):
                dir_compare(latest_dir, full_path_for_all_other_dirs)
