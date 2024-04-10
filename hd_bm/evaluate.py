#    Copyright 2021 Division of Medical Image Computing, German Cancer Research Center (DKFZ), Heidelberg, Germany
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.


from hd_bm.utils import blockPrint, enablePrint

blockPrint()
from nnunet.evaluation.evaluator import evaluate_folder

enablePrint()

import argparse


def main():
    parser = argparse.ArgumentParser(
        description="This script will allow you to run HD-BM (slim) to predict multiple cases with modalities"
        " (with index):\n T1ce (0000), FLAIR (0001)"
        "The different modalities should follow nnUNet naming convention `{SOME_ID}_{ModalityID}.nii.gz`"
        "To predict single cases, please use `hd_bm_slim_predict`"
        "Should you have access to the T1 and T1sub modality please use the `hd_bm_predict` or "
        "`hd_bm_predict_folder` function instead."
    )
    parser.add_argument(
        "-o",
        "--output_folder",
        type=str,
        required=True,
        help="Output folder. This is where the resulting segmentations will be saved. Cannot be the "
        "same folder as the input folder. If output_folder does not exist it will be created",
    )
    parser.add_argument(
        "-gt",
        "--groundtruth_folder",
        type=str,
        required=True,
        help="Folder containing ground truth segmentations for the input cases provided.",
    )
    args = parser.parse_args()

    print("Evaluating predictions of a model")
    evaluate_folder(
        folder_with_gts=args.groundtruth_folder, folder_with_predictions=args.output_folder, labels=(1, 2)
    )
    print("Finished predicting and evaluating HD-BM. \n Exiting.")


if __name__ == "__main__":
    main()
